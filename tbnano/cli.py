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
    elif args.agent == "ls_then_quit":
        model, fmt, backend_kind = "scripted:ls_then_quit", "json_tags", "scripted"
    else:
        fmt, backend_kind = args.format, args.backend

    if args.sandbox == "local" and backend_kind != "scripted" and not args.unsafe_local:
        print(
            "refusing: --sandbox local executes model commands directly on "
            "this host (no container boundary, HOME=task dir only). Use "
            "--sandbox docker, or pass --unsafe-local to acknowledge.",
            file=sys.stderr,
        )
        return 2
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
            kw: dict = {}
            if backend_kind in ("transformers", "vllm", "mlx"):
                kw["fmt"] = fmt
                kw["sampling"] = args.sampling
                kw["flat_tools"] = args.flat_tools
            if backend_kind == "openai":
                kw["base_url"] = args.base_url
            shared["b"] = make_backend(model, backend_kind, **kw)
        return shared["b"]

    tok = None
    b0 = None
    if backend_kind != "scripted":
        b0 = factory()
        tok = b0.tokenizer()

    import subprocess as _sp
    try:
        git_hash = _sp.run(["git", "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1]
                           ).stdout.strip()
    except Exception:
        git_hash = ""
    from . import __version__
    protocol = {
        "format": fmt,
        "final_answer": args.final_answer,
        "sampling": args.sampling,
        "sampling_values": getattr(b0, "gen_cfg", None),
        "flat_tools": bool(args.flat_tools),
        "max_context": getattr(b0, "max_context", None),
        "tbnano_version": __version__,
        "git_hash": git_hash,
        "loop_stop": not args.no_loop_stop,
    }

    run_benchmark(
        tasks,
        factory,
        adapter,
        model_name=args.name or model,
        out_root=Path(args.out),
        sandbox_kind=args.sandbox,
        jobs=args.jobs,
        samples=args.samples,
        resume=args.resume,
        text_final=args.final_answer == "text",
        loop_stop=not args.no_loop_stop,
        protocol=protocol,
        temperature=args.temperature,
        seed=args.seed,
        tok=tok,
    )
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    """Recompute process metrics from saved trajectories (spec v2 3).

    Reads runs/<name>/*.jsonl, re-evaluates the per-episode metrics and
    updates report.json's metric fields in place (model/protocol kept)."""
    from .metrics import RunRecord, _group_stats
    from .procmetrics import episode_metrics
    from .tasksio import iter_tasks

    run_dir = Path(args.run_dir)
    report_path = run_dir / "report.json"
    specs = {s.id: s for s in iter_tasks(Path(args.tasks))}
    records: list[RunRecord] = []
    for f in sorted(run_dir.glob("*.jsonl")):
        lines = f.read_text().splitlines()
        try:
            s = json.loads(lines[-1])["summary"]
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
        traj = [json.loads(l) for l in lines[:-1]]
        spec = specs.get(s["task_id"])
        end_reason = s.get("end_reason", "")
        rec = RunRecord(
            task_id=s["task_id"], resolved=s["resolved"],
            partial=s.get("partial", 0.0), end_reason=end_reason,
            turns_used=s.get("turns_used", 0), tokens_used=s.get("tokens_used", 0),
            invalid_calls=s.get("invalid_calls", 0),
            exec_seconds=s.get("exec_seconds", 0.0),
            level=spec.level if spec else 0,
            category=spec.category if spec else "",
            template=spec.template if spec else "",
            track=spec.track if spec else "",
            proc_excluded=end_reason == "harness_error",
        )
        if not rec.proc_excluded:
            for k, v in episode_metrics(
                    traj, spec.instruction if spec else "", end_reason).items():
                setattr(rec, k, v)
        records.append(rec)
    stats = _group_stats(records)
    keys = ["valid_call_rate", "grounded_first_call", "loop_rate",
            "error_recovery", "proper_end", "refusal_rate"]
    print(json.dumps({k: stats[k] for k in keys}, indent=2))
    if report_path.exists():
        rep = json.loads(report_path.read_text())
        rep.setdefault("overall", {}).update({k: stats[k] for k in keys})
        report_path.write_text(json.dumps(rep, indent=2))
        print(f"updated {report_path}")
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
    # Runs are only comparable on the same task set; warn on mismatched
    # hashes or different run protocols (spec v2 4).
    hashes = {r.get("tasks_hash") for r in reports.values() if r.get("tasks_hash")}
    if len(hashes) > 1:
        print("warning: runs used different task sets — numbers are not "
              "directly comparable", file=sys.stderr)
    protos = {json.dumps((r.get("protocol") or {}), sort_keys=True)
              for r in reports.values() if r.get("protocol")}
    if len(protos) > 1:
        print("warning: runs used different protocols (format/final_answer/"
              "sampling/flat_tools) — see report.json 'protocol'", file=sys.stderr)
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
    if args.n and args.split == "test":
        # scale test proportionally
        base = sum(TEST_COUNTS.values())
        counts = {
            fam: max(1, round(args.n * c / base)) for fam, c in TEST_COUNTS.items()
        }
    written = generate_split(args.split, Path(args.out), counts=counts)
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
                   choices=["json_tags", "lfm_pythonic", "hermes", "qwen_xml", "openai"])
    r.add_argument("--backend", default="auto",
                   choices=["auto", "transformers", "vllm", "mlx", "ours", "openai", "scripted"])
    r.add_argument("--agent", choices=["oracle", "quitter", "ls_then_quit"], default=None,
                   help="built-in validation agents (override --model/--format/--backend)")
    r.add_argument("--tasks", default=str(_default_tasks_dir()))
    r.add_argument("--sandbox", default="docker", choices=["local", "docker"])
    r.add_argument("--unsafe-local", action="store_true",
                   help="allow --sandbox local with a real model backend "
                        "(DANGEROUS: commands run on this host)")
    r.add_argument("--base-url", default=None,
                   help="OpenAI-compatible endpoint for --backend openai "
                        "(e.g. http://localhost:8000/v1 for `vllm serve`)")
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--samples", type=int, default=1)
    r.add_argument("--final-answer", choices=["tool", "text"], default="tool",
                   help="tool: end with finish(answer=...); text: a plain-text reply is the "
                        "final answer (native protocol of e.g. LFM2.5)")
    r.add_argument("--sampling", choices=["greedy", "model"], default="greedy",
                   help="model: the model's generation_config.json (temperature, top_k, "
                        "top_p, min_p, repetition_penalty) instead of --temperature")
    r.add_argument("--flat-tools", action="store_true",
                   help="pass tools to the chat template as flat {name, description, "
                        "parameters} instead of {type: function, function: ...}")
    r.add_argument("--resume", action="store_true",
                   help="skip (task, sample) pairs whose trajectory already has a summary")
    r.add_argument("--no-loop-stop", action="store_true",
                   help="do not end the episode on 3 identical consecutive calls "
                        "(comparison with the pilot runs)")
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

    m = sub.add_parser("metrics", help="recompute process metrics on saved trajectories")
    m.add_argument("run_dir")
    m.add_argument("--tasks", default=str(_default_tasks_dir()))
    m.set_defaults(fn=cmd_metrics)

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
