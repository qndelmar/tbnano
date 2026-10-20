"""Task generation: ~64 test-only templates + ~40 train-only templates.

Template sets are DISJOINT between splits (train templates all start with
't_'), so test/train can never share a task template — the leak check in
validate.py enforces this on the `template` field too.
"""

from __future__ import annotations

import random
from pathlib import Path

from . import ct, dt, et, ft, pt

# template name -> function(rng, idx, out_root, split) -> Path
TEST_TEMPLATES = {
    # files_text (16)
    "log_count": ft.log_count,
    "log_count_window": ft.log_count_window,
    "log_first_err": ft.log_first_err,
    "extract_ips": ft.extract_ips,
    "extract_emails": ft.extract_emails,
    "extract_urls": ft.extract_urls,
    "csv_col": ft.csv_col,
    "sort_desc": ft.sort_desc,
    "upper_lines": ft.upper_lines,
    "dedup_lines": ft.dedup_lines,
    "longest_line": ft.longest_line,
    "count_regex": ft.count_regex,
    "merge_logs": ft.merge_logs,
    "jsonl_filter": ft.jsonl_filter,
    "seq_gap": ft.seq_gap,
    "sed_replace": ft.sed_replace,
    # data (11)
    "csv_agg": dt.csv_agg,
    "csv_topn": dt.csv_topn,
    "csv_join": dt.csv_join,
    "sqlite_count": dt.sqlite_count,
    "sqlite_join": dt.sqlite_join,
    "json_agg": dt.json_agg,
    "json_to_csv": dt.json_to_csv,
    "csv_stats": dt.csv_stats,
    "dedup_latest": dt.dedup_latest,
    "json_nested": dt.json_nested,
    "tsv_to_json": dt.tsv_to_json,
    # code (11)
    "fix_python": ct.fix_python,
    "fix_bash": ct.fix_bash,
    "fix_offbyone": ct.fix_offbyone,
    "fix_c": ct.fix_c,
    "fix_make": ct.fix_make,
    "fix_regex": ct.fix_regex,
    "write_tool": ct.write_tool,
    "merge_csv": ct.merge_csv,
    "add_flag": ct.add_flag,
    "fix_json_conf": ct.fix_json_conf,
    "fix_ini": ct.fix_ini,
    # env (7)
    "chmod_run": et.chmod_run,
    "misplaced_conf": et.misplaced_conf,
    "missing_dir": et.missing_dir,
    "git_restore": et.git_restore,
    "env_var": et.env_var,
    "symlink_fix": et.symlink_fix,
    "git_diff_stat": et.git_diff_stat,
    # physics (19)
    "unit_conv": pt.unit_conv,
    "vert_speed": pt.vert_speed,
    "energy_int": pt.energy_int,
    "thrust_isp": pt.thrust_isp,
    "center_mass": pt.center_mass,
    "battery_c": pt.battery_c,
    "course_dist": pt.course_dist,
    "lift_force": pt.lift_force,
    "peak_telem": pt.peak_telem,
    "fix_formula": pt.fix_formula,
    "multi_report": pt.multi_report,
    "orbital_v": pt.orbital_v,
    "drag_force": pt.drag_force,
    "delta_v": pt.delta_v,
    "fuel_time": pt.fuel_time,
    "pressure_alt": pt.pressure_alt,
    "mach_speed": pt.mach_speed,
    "impulse_int": pt.impulse_int,
    "glide_ratio": pt.glide_ratio,
}

# variants per template for the default test split (~338 tasks).
TEST_COUNTS = {
    "log_count": 6, "log_count_window": 5, "log_first_err": 6,
    "extract_ips": 5, "extract_emails": 5, "extract_urls": 5,
    "csv_col": 5, "sort_desc": 5, "upper_lines": 5, "dedup_lines": 5,
    "longest_line": 5, "count_regex": 6, "merge_logs": 5,
    "jsonl_filter": 5, "seq_gap": 5, "sed_replace": 5,
    "csv_agg": 6, "csv_topn": 6, "csv_join": 6, "sqlite_count": 6,
    "sqlite_join": 6, "json_agg": 6, "json_to_csv": 6, "csv_stats": 6,
    "dedup_latest": 5, "json_nested": 5, "tsv_to_json": 6,
    "fix_python": 6, "fix_bash": 4, "fix_offbyone": 4, "fix_c": 4,
    "fix_make": 4, "fix_regex": 4, "write_tool": 5, "merge_csv": 16,
    "add_flag": 4, "fix_json_conf": 4, "fix_ini": 4,
    "chmod_run": 5, "misplaced_conf": 5, "missing_dir": 5,
    "git_restore": 5, "env_var": 5, "symlink_fix": 4, "git_diff_stat": 4,
    "unit_conv": 8, "vert_speed": 5, "energy_int": 5, "thrust_isp": 5,
    "center_mass": 5, "battery_c": 6, "course_dist": 5, "lift_force": 6,
    "peak_telem": 5, "fix_formula": 5, "multi_report": 16, "orbital_v": 5,
    "drag_force": 5, "delta_v": 5, "fuel_time": 5, "pressure_alt": 5,
    "mach_speed": 5, "impulse_int": 5, "glide_ratio": 6,
}

TRAIN_TEMPLATES = {
    "t_wc_lines": ft.t_wc_lines, "t_grep_count": ft.t_grep_count,
    "t_sort_alpha": ft.t_sort_alpha, "t_head_n": ft.t_head_n,
    "t_tail_n": ft.t_tail_n, "t_grep_v": ft.t_grep_v,
    "t_word_freq": ft.t_word_freq, "t_rev_lines": ft.t_rev_lines,
    "t_num_sum": ft.t_num_sum, "t_append_line": ft.t_append_line,
    "t_csv_sum": dt.t_csv_sum, "t_json_count": dt.t_json_count,
    "t_csv_reverse": dt.t_csv_reverse, "t_sql_minmax": dt.t_sql_minmax,
    "t_json_keys": dt.t_json_keys, "t_csv_swap": dt.t_csv_swap,
    "t_csv_head_filter": dt.t_csv_head_filter, "t_tsv_count": dt.t_tsv_count,
    "t_fix_print": ct.t_fix_print, "t_add_shebang": ct.t_add_shebang,
    "t_fix_none": ct.t_fix_none, "t_write_echo": ct.t_write_echo,
    "t_fix_range": ct.t_fix_range, "t_rm_blank": ct.t_rm_blank,
    "t_append_text": ct.t_append_text,
    "t_touch_flag": et.t_touch_flag, "t_mkpath": et.t_mkpath,
    "t_git_commit": et.t_git_commit, "t_cleanup": et.t_cleanup,
    "t_perm_read": et.t_perm_read,
    "t_kmh_mph": pt.t_kmh_mph, "t_c_to_k": pt.t_c_to_k,
    "t_rpm_rads": pt.t_rpm_rads, "t_m_km": pt.t_m_km, "t_w_kw": pt.t_w_kw,
    "t_avg_speed": pt.t_avg_speed, "t_total_mass": pt.t_total_mass,
    "t_fuel_pct": pt.t_fuel_pct, "t_n_lbf": pt.t_n_lbf, "t_pa_psi": pt.t_pa_psi,
}

TRAIN_COUNTS = {
    "t_wc_lines": 8, "t_grep_count": 8, "t_sort_alpha": 8, "t_head_n": 8,
    "t_tail_n": 8, "t_grep_v": 8, "t_word_freq": 8, "t_rev_lines": 8,
    "t_num_sum": 8, "t_append_line": 8,
    "t_csv_sum": 8, "t_json_count": 8, "t_csv_reverse": 7,
    "t_sql_minmax": 8, "t_json_keys": 7, "t_csv_swap": 7,
    "t_csv_head_filter": 7, "t_tsv_count": 8,
    "t_fix_print": 7, "t_add_shebang": 7, "t_fix_none": 7,
    "t_write_echo": 7, "t_fix_range": 7, "t_rm_blank": 7, "t_append_text": 7,
    "t_touch_flag": 7, "t_mkpath": 7, "t_git_commit": 8, "t_cleanup": 7,
    "t_perm_read": 7,
    "t_kmh_mph": 8, "t_c_to_k": 8, "t_rpm_rads": 8, "t_m_km": 8,
    "t_w_kw": 8, "t_avg_speed": 8, "t_total_mass": 8, "t_fuel_pct": 8,
    "t_n_lbf": 8, "t_pa_psi": 8,
}

REGISTRY = {"test": TEST_TEMPLATES, "train": TRAIN_TEMPLATES}
DEFAULT_COUNTS = {"test": TEST_COUNTS, "train": TRAIN_COUNTS}
FAMILIES = ["files_text", "data", "code", "env", "physics"]


def generate_split(
    split: str,
    out_root: Path,
    seed: int = 0,
    n_per_family=None,  # unused, kept for CLI compat
    counts: dict | None = None,
) -> list[Path]:
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    templates = REGISTRY[split]
    counts = counts or DEFAULT_COUNTS[split]
    written = []
    for ti, (name, fn) in enumerate(sorted(templates.items())):
        for i in range(counts.get(name, 0)):
            rng = random.Random(seed + ti * 7919 + i * 131)
            written.append(fn(rng, i, out_root, split))
    return written
