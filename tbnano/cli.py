"""tbnano CLI (spec section 7).

    tbnano run --model hf:LiquidAI/LFM2.5-230M --format lfm_pythonic --backend transformers --jobs 8
    tbnano run --model ckpt:runs/small_sft/ckpt.pt --format json_tags --backend ours
    tbnano run --model api:gpt-4o-mini --format openai
    tbnano report runs/ --compare
    tbnano gen --split train --n 10000 --out train_tasks/
    tbnano validate
    tbnano build-image
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .adapters import get_adapter
from .tasksio import iter_tasks


def _default_tasks_dir() -> Path:
    for cand in (Path.cwd() / "tasks" / "test", Path(__file__).resolve().parents[1] / "tasks" / "test"):
        if cand.exists():
            return cand
    return Path("tasks/test")


def cmd_run(args: argparse.Namespace) -> int:
    from .backends import make_backend
    from .runner import run_benchmark

    model = args.model
    if args.agent == "oracle":
        model, fmt, backend_kind = "scripted:oracle", "json_tags", "scripted"
    elif args.agent == "quitter":
        model, fmt, backend_kind = "scripted:quitter", "json_tags", "scripted"
    else:
        fmt, backend_kind = args.format, args.backend

    adapter = get_adapter(fmt)
    tasks = list(iter_tasks(Path(args.tasks)))
    if not tasks:
        print(f"no tasks under {args.tasks}", file=sys.stderr)
        return 1
    if args.n:
        tasks = tasks[: args.n]
    print(f"{len(tasks)} tasks x {args.samples} sample(s), jobs={args.jobs}, sandbox={args.sandbox}")

    shared = {"b": None}

    def factory():
        if backend_kind == "scripted":
            return make_backend(model, "scripted")
        if shared["b"] is None:
            shared["b"] = make_backend(model, backend_kind)
        return shared["b"]

    tok = None
    if backend_kind != "scripted":
        tok = factory().tokenizer()

    run_benchmark(
        tasks,
        factory,
        adapter,
        model_name=args.name or model,
        out_root=Path(args.out),
        sandbox_kind=args.sandbox,
        jobs=args.jobs,
        samples=args.samples,
        temperature=args.temperature,
        seed=args.seed,
        tok=tok,
    )
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    from .metrics import format_table

    root = Path(args.runs_dir)
    reports = {}
    for rp in sorted(root.glob("*/report.json")):
        reports[rp.parent.name] = json.loads(rp.read_text())
    if not reports:
        print(f"no report.json under {root}", file=sys.stderr)
        return 1
    print(format_table(reports))
    if args.compare:
        for name, rep in reports.items():
            print(f"\n== {name} ==")
            for grp in ("by_level", "by_category"):
                if grp in rep:
                    print(f"  {grp}:")
                    for k, s in rep[grp].items():
                        ci = s["pass@1_ci95"]
                        print(
                            f"    {k:<14} n={s['n']:>4}  "
                            f"pass@1={s['pass@1'] * 100:5.1f}%  "
                            f"ci95=[{ci[0] * 100:.1f},{ci[1] * 100:.1f}]"
                        )
    return 0


def cmd_gen(args: argparse.Namespace) -> int:
    from .generators import FAMILIES, TEST_COUNTS, generate_split

    counts = None
    if args.split == "train" and args.n:
        per = max(1, args.n // len(FAMILIES))
        counts = {fam: per for fam in FAMILIES}
    elif args.n and args.split == "test":
        # scale test proportionally
        base = sum(TEST_COUNTS.values())
        counts = {
            fam: max(1, round(args.n * c / base)) for fam, c in TEST_COUNTS.items()
        }
    written = generate_split(args.split, Path(args.out), n_per_family=args.n, counts=counts)
    print(f"wrote {len(written)} tasks to {args.out}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    from .validate import validate_all

    tasks = list(iter_tasks(Path(args.tasks)))
    if args.n:
        tasks = tasks[: args.n]
    print(f"validating {len(tasks)} tasks (sandbox={args.sandbox}, jobs={args.jobs})")
    summary = validate_all(
        tasks,
        sandbox_kind=args.sandbox,
        jobs=args.jobs,
        check_leak=args.check_leak,
        train_root=Path(args.train) if args.train else None,
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "bad"}, indent=2))
    if summary["bad"]:
        print(f"{len(summary['bad'])} invalid tasks (first 10):")
        for b in summary["bad"][:10]:
            print(" ", b["id"], "->", "; ".join(b["problems"]))
        return 1
    return 0


def cmd_build_image(args: argparse.Namespace) -> int:
    from .sandbox.docker import build_image, IMAGE

    df = Path(args.dockerfile or Path(__file__).resolve().parents[1] / "docker" / "Dockerfile")
    print(f"building {IMAGE} from {df}")
    build_image(df, IMAGE)
    print("done")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tbnano", description="TerminalBench Nano")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run the benchmark")
    r.add_argument("--model", default="scripted:quitter")
    r.add_argument("--format", default="json_tags",
                   choices=["json_tags", "lfm_pythonic", "hermes", "openai"])
    r.add_argument("--backend", default="auto",
                   choices=["auto", "transformers", "vllm", "mlx", "ours", "openai", "scripted"])
    r.add_argument("--agent", choices=["oracle", "quitter"], default=None,
                   help="built-in validation agents (override --model/--format/--backend)")
    r.add_argument("--tasks", default=str(_default_tasks_dir()))
    r.add_argument("--sandbox", default="local", choices=["local", "docker"])
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--samples", type=int, default=1)
    r.add_argument("--temperature", type=float, default=0.0)
    r.add_argument("--seed", type=int, default=None)
    r.add_argument("--n", type=int, default=None, help="limit number of tasks")
    r.add_argument("--name", default=None, help="report/run dir name")
    r.add_argument("--out", default="runs")
    r.set_defaults(fn=cmd_run)

    rp = sub.add_parser("report", help="print report table(s)")
    rp.add_argument("runs_dir")
    rp.add_argument("--compare", action="store_true")
    rp.set_defaults(fn=cmd_report)

    g = sub.add_parser("gen", help="generate tasks")
    g.add_argument("--split", required=True, choices=["train", "test"])
    g.add_argument("--n", type=int, default=None)
    g.add_argument("--out", required=True)
    g.set_defaults(fn=cmd_gen)

    v = sub.add_parser("validate", help="validate the task set (spec 8)")
    v.add_argument("--tasks", default=str(_default_tasks_dir()))
    v.add_argument("--sandbox", default="local", choices=["local", "docker"])
    v.add_argument("--jobs", type=int, default=4)
    v.add_argument("--n", type=int, default=None)
    v.add_argument("--check-leak", action="store_true")
    v.add_argument("--train", default=None, help="train tasks dir for leak check")
    v.set_defaults(fn=cmd_validate)

    b = sub.add_parser("build-image", help="build the docker sandbox image")
    b.add_argument("--dockerfile", default=None)
    b.set_defaults(fn=cmd_build_image)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
