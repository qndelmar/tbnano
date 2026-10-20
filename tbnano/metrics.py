"""Metrics and report aggregation (spec section 6)."""

from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunRecord:
    task_id: str
    resolved: bool
    partial: float
    end_reason: str
    turns_used: int
    tokens_used: int
    invalid_calls: int
    exec_seconds: float
    level: int = 0
    category: str = ""
    template: str = ""
    sample: int = 0
    track: str = ""                # L0 sub-track: 'guided' | 'plain'
    # process metrics (spec v2 3)
    valid_calls: int = 0
    call_attempts: int = 0
    grounded_first: Any = None     # True/False or None (n/a: no file named)
    looped: bool = False
    err_calls: int = 0
    err_recovered: int = 0
    proper_end: bool = False
    refused: bool = False
    proc_excluded: bool = False    # harness_error: out of process-metric denominators


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def pass_at_k(num_samples: int, num_correct: int, k: int) -> float:
    """Unbiased pass@k estimator (Chen et al.): 1 - C(n-c, k)/C(n, k)."""
    n, c = num_samples, num_correct
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def cluster_bootstrap_ci(
    records: list[RunRecord],
    key: str = "template",
    iters: int = 2000,
    seed: int = 0,
) -> tuple[float, float]:
    """Cluster bootstrap 95% CI for pass@1, resampling *templates* not
    tasks: variants inside one template are correlated, so treating 300+
    tasks as independent understates the interval."""
    clusters: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        clusters[getattr(r, key, "") or r.task_id].append(r)
    names = sorted(clusters)
    if len(names) < 2:
        n = len(records)
        k = sum(1 for r in records if r.resolved)
        return wilson_ci(k, n)
    rng = random.Random(seed)
    stats = []
    for _ in range(iters):
        draw = [clusters[rng.choice(names)] for _ in range(len(names))]
        flat = [r for cl in draw for r in cl]
        stats.append(sum(1 for r in flat if r.resolved) / len(flat))
    stats.sort()
    return (stats[int(0.025 * iters)], stats[min(iters - 1, int(0.975 * iters))])


def _group_stats(records: list[RunRecord]) -> dict[str, Any]:
    n = len(records)
    n_proc = sum(1 for r in records if not r.proc_excluded)
    k = sum(1 for r in records if r.resolved)
    lo, hi = wilson_ci(k, n)
    end_counts: dict[str, int] = defaultdict(int)
    for r in records:
        end_counts[r.end_reason] += 1
    blo, bhi = cluster_bootstrap_ci(records)
    return {
        "n": n,
        "pass@1": k / n if n else 0.0,
        "pass@1_ci95": [round(lo, 4), round(hi, 4)],
        "pass@1_ci95_cluster": [round(blo, 4), round(bhi, 4)],
        "n_templates": len({r.template or r.task_id for r in records}),
        "partial": sum(r.partial for r in records) / n if n else 0.0,
        "invalid_call_rate": (
            sum(r.invalid_calls for r in records)
            / max(1, sum(r.turns_used for r in records))
        ),
        "turns_used": sum(r.turns_used for r in records) / n if n else 0.0,
        "tokens_used": sum(r.tokens_used for r in records) / n if n else 0.0,
        "exec_seconds": sum(r.exec_seconds for r in records) / n if n else 0.0,
        "end_reasons": {k2: v / n for k2, v in sorted(end_counts.items())},
        # process metrics (spec v2 3); harness_error episodes excluded upstream
        "valid_call_rate": (
            sum(r.valid_calls for r in records)
            / max(1, sum(r.call_attempts for r in records))
        ),
        "grounded_first_call": (
            lambda g: sum(g) / len(g) if g else None
        )([r.grounded_first for r in records if r.grounded_first is not None]),
        "loop_rate": sum(1 for r in records if r.looped) / n_proc if n_proc else 0.0,
        "error_recovery": (
            sum(r.err_recovered for r in records)
            / max(1, sum(r.err_calls for r in records))
            if sum(r.err_calls for r in records) else None
        ),
        "proper_end": sum(1 for r in records if r.proper_end) / n_proc if n_proc else 0.0,
        "refusal_rate": sum(1 for r in records if r.refused) / n_proc if n_proc else 0.0,
    }


def aggregate(records: list[RunRecord]) -> dict[str, Any]:
    """Full report dict: overall + per-level + per-category + pass@k."""
    report: dict[str, Any] = {"overall": _group_stats(records)}

    def _lvl_key(r: RunRecord) -> str:
        # L0 splits into the guided/plain sub-tracks (spec v2 2/5)
        if r.level == 0:
            return "L0g" if r.track == "guided" else "L0p" if r.track == "plain" else "L0"
        return f"L{r.level}"

    by_level: dict[str, list[RunRecord]] = defaultdict(list)
    by_cat: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        by_level[_lvl_key(r)].append(r)
        by_cat[r.category].append(r)
    lvl_order = {"L0g": 0, "L0p": 1, "L0": 2, "L1": 3, "L2": 4, "L3": 5, "L4": 6}
    report["by_level"] = {
        k: _group_stats(v)
        for k, v in sorted(by_level.items(), key=lambda kv: lvl_order.get(kv[0], 9))
    }
    report["by_category"] = {
        cat: _group_stats(rs) for cat, rs in sorted(by_cat.items())
    }
    by_tpl: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        by_tpl[r.template or r.task_id].append(r)
    report["by_template"] = {
        t: {"n": len(rs), "pass@1": sum(1 for r in rs if r.resolved) / len(rs)}
        for t, rs in sorted(by_tpl.items())
    }
    report["harness_errors"] = sum(
        1 for r in records if r.end_reason == "harness_error"
    )

    # pass@k: group samples per task.
    by_task: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        by_task[r.task_id].append(r)
    max_samples = max(len(v) for v in by_task.values()) if by_task else 1
    if max_samples > 1:
        k = max_samples
        scores = [
            pass_at_k(len(rs), sum(1 for r in rs if r.resolved), k)
            for rs in by_task.values()
        ]
        report[f"pass@{k}"] = sum(scores) / len(scores)
    return report


def tasks_hash(records_or_ids) -> str:
    """Fingerprint of the task set — `tbnano report` only compares runs
    over the same set (spec v2 4)."""
    import hashlib

    ids = sorted(
        r.task_id if hasattr(r, "task_id") else str(r) for r in records_or_ids
    )
    return hashlib.sha256("\n".join(ids).encode()).hexdigest()[:12]


def write_report(records: list[RunRecord], out_dir: Path, model: str,
                 protocol: dict | None = None) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = aggregate(records)
    report["model"] = model
    report["n_tasks"] = len({r.task_id for r in records})
    report["tasks_hash"] = tasks_hash(records)
    if protocol:
        report["protocol"] = protocol
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))
    return out_dir / "report.json"


_LVL_ORDER = ["L0g", "L0p", "L1", "L2", "L3", "L4"]


def _protocol_str(rep: dict) -> str:
    p = rep.get("protocol") or {}
    fmt = p.get("format", "?")
    fa = {"tool": "finish", "text": "text"}.get(p.get("final_answer"), p.get("final_answer", "?"))
    sm = p.get("sampling", "?")
    ft = ",flat" if p.get("flat_tools") else ""
    return f"{fmt}+{fa}+{sm}{ft}"


def format_table(reports: dict[str, dict]) -> str:
    """One row per run (spec v2 5):
    model protocol pass@1[L0g L0p L1 L2 L3 L4] partial valid grounded loop
    recover end refusal turns tok"""
    lines = [
        f"{'model':<24} {'protocol':<26} {'n':>4} "
        f"{'pass@1[L0g L0p L1 L2 L3 L4]':<30} {'partial':>7} {'valid':>6} "
        f"{'grnd':>5} {'loop':>5} {'recv':>5} {'end':>5} {'refus':>5} "
        f"{'turns':>5} {'tok':>6}"
    ]
    for name, rep in reports.items():
        o = rep.get("overall", {})
        bl = rep.get("by_level", {})
        cells = " ".join(
            f"{bl.get(l, {}).get('pass@1', 0) * 100:4.0f}"
            if l in bl else "   -" for l in _LVL_ORDER
        )
        pct = lambda v: "-" if v is None else f"{v * 100:4.0f}%"
        lines.append(
            f"{name:<24.24} {_protocol_str(rep):<26.26} "
            f"{rep.get('n_tasks', o.get('n', 0)):>4} "
            f"{cells:<30} "
            f"{o.get('partial', 0) * 100:>6.1f}% "
            f"{o.get('valid_call_rate', 0) * 100:>5.1f}% "
            f"{pct(o.get('grounded_first_call')):>5} "
            f"{o.get('loop_rate', 0) * 100:>4.0f}% "
            f"{pct(o.get('error_recovery')):>5} "
            f"{o.get('proper_end', 0) * 100:>4.0f}% "
            f"{o.get('refusal_rate', 0) * 100:>4.0f}% "
            f"{o.get('turns_used', 0):>5.1f} {o.get('tokens_used', 0):>6.0f}"
        )
        ci = o.get("pass@1_ci95_cluster") or o.get("pass@1_ci95", [0, 0])
        lines.append(
            f"{'':>24.24} {'':>26.26} {'':>4} "
            f"pass@1={o.get('pass@1', 0) * 100:.1f}% "
            f"ci95(cluster)=[{ci[0] * 100:.1f},{ci[1] * 100:.1f}]"
        )
    return "\n".join(lines)
