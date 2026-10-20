"""Metrics and report aggregation (spec section 6)."""

from __future__ import annotations

import json
import math
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
    sample: int = 0


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


def _group_stats(records: list[RunRecord]) -> dict[str, Any]:
    n = len(records)
    k = sum(1 for r in records if r.resolved)
    lo, hi = wilson_ci(k, n)
    end_counts: dict[str, int] = defaultdict(int)
    for r in records:
        end_counts[r.end_reason] += 1
    return {
        "n": n,
        "pass@1": k / n if n else 0.0,
        "pass@1_ci95": [round(lo, 4), round(hi, 4)],
        "partial": sum(r.partial for r in records) / n if n else 0.0,
        "invalid_call_rate": (
            sum(r.invalid_calls for r in records)
            / max(1, sum(r.turns_used for r in records))
        ),
        "turns_used": sum(r.turns_used for r in records) / n if n else 0.0,
        "tokens_used": sum(r.tokens_used for r in records) / n if n else 0.0,
        "exec_seconds": sum(r.exec_seconds for r in records) / n if n else 0.0,
        "end_reasons": {k2: v / n for k2, v in sorted(end_counts.items())},
    }


def aggregate(records: list[RunRecord]) -> dict[str, Any]:
    """Full report dict: overall + per-level + per-category + pass@k."""
    report: dict[str, Any] = {"overall": _group_stats(records)}

    by_level: dict[int, list[RunRecord]] = defaultdict(list)
    by_cat: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        by_level[r.level].append(r)
        by_cat[r.category].append(r)
    report["by_level"] = {
        f"L{lvl}": _group_stats(rs) for lvl, rs in sorted(by_level.items())
    }
    report["by_category"] = {
        cat: _group_stats(rs) for cat, rs in sorted(by_cat.items())
    }

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


def write_report(records: list[RunRecord], out_dir: Path, model: str) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = aggregate(records)
    report["model"] = model
    report["n_tasks"] = len({r.task_id for r in records})
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))
    return out_dir / "report.json"


def format_table(reports: dict[str, dict]) -> str:
    """Short stdout table (and --compare across models)."""
    lines = [
        f"{'model':<28} {'n':>5} {'pass@1':>7} {'ci95':>15} {'partial':>7} "
        f"{'inv%':>6} {'turns':>5} {'tok':>6}"
    ]
    for name, rep in reports.items():
        o = rep.get("overall", {})
        ci = o.get("pass@1_ci95", [0, 0])
        lines.append(
            f"{name:<28} {rep.get('n_tasks', o.get('n', 0)):>5} "
            f"{o.get('pass@1', 0) * 100:>6.1f}% "
            f"[{ci[0] * 100:5.1f},{ci[1] * 100:5.1f}] "
            f"{o.get('partial', 0) * 100:>6.1f}% "
            f"{o.get('invalid_call_rate', 0) * 100:>5.1f}% "
            f"{o.get('turns_used', 0):>5.1f} {o.get('tokens_used', 0):>6.0f}"
        )
    return "\n".join(lines)
