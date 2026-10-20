"""Procedural task generators (spec 5.4 source 2).

Each generator family emits seeded task variants. `write_task` is the
single place that materialises a task directory, so every generated task
has exactly the spec's layout.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Optional

from . import code_tasks, data_tasks, env_tasks, files_text, physics

# family name -> (module.generate_one(rng, idx, out_root), n_test, n_train_capable)
FAMILIES = {
    "log_count": files_text.gen_log_count,
    "extract_ips": files_text.gen_extract_ips,
    "field_transform": files_text.gen_field_transform,
    "csv_agg": data_tasks.gen_csv_agg,
    "sqlite_q": data_tasks.gen_sqlite_q,
    "json_agg": data_tasks.gen_json_agg,
    "fix_python": code_tasks.gen_fix_python,
    "fix_bash": code_tasks.gen_fix_bash,
    "write_script": code_tasks.gen_write_script,
    "paths_perms": env_tasks.gen_paths_perms,
    "git_restore": env_tasks.gen_git_restore,
    "unit_conv": physics.gen_unit_conv,
    "energy_int": physics.gen_energy_int,
    "fix_formula": physics.gen_fix_formula,
    "multi_report": physics.gen_multi_report,
}

# Test-set counts per family (spec 5.3 proportions over ~300 tasks).
TEST_COUNTS = {
    "log_count": 45,      # files_text 90 total
    "extract_ips": 25,
    "field_transform": 20,
    "csv_agg": 20,        # data 60
    "sqlite_q": 20,
    "json_agg": 20,
    "fix_python": 25,     # code 60
    "fix_bash": 20,
    "write_script": 15,
    "paths_perms": 15,    # env 30
    "git_restore": 15,
    "unit_conv": 40,      # physics 85
    "energy_int": 20,
    "fix_formula": 10,
    "multi_report": 15,
}

# Seeds are partitioned by split so train/test data never coincide
# (spec 5.4); `tbnano validate --check-leak` verifies it by hashing.
SEED_BASE = {"test": 1_000_000, "train": 7_000_000}


def generate_split(split: str, out_root: Path, n_per_family: Optional[int] = None,
                   counts: Optional[dict[str, int]] = None) -> list[Path]:
    """Materialise a split: returns written task dirs."""
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    written = []
    for fam, gen in FAMILIES.items():
        n = counts.get(fam, 10) if counts else (TEST_COUNTS[fam] if split == "test" else (n_per_family or 20))
        for i in range(n):
            rng = random.Random(SEED_BASE[split] + hash_fam(fam) * 1000 + i)
            d = gen(rng, i, out_root, split)
            written.append(d)
    return written


def hash_fam(name: str) -> int:
    return sum(ord(c) * (i + 1) for i, c in enumerate(name)) % 1000
