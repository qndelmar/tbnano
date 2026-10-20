"""Physics & aerospace family (spec 5.3, ~25%, our domain).

Every answer is a number checked with a relative tolerance.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from .base import answer_test, pick, with_id, write_task

# (src_unit, dst_unit, factor, src_col_label, ask)
UNIT_PAIRS = [
    ("ft/min", "m/s", 0.00508, "vspeed_fpm", "maximum vertical speed"),
    ("ft", "m", 0.3048, "alt_ft", "maximum altitude"),
    ("knots", "km/h", 1.852, "speed_kt", "maximum speed"),
    ("psi", "kPa", 6.894757, "pressure_psi", "maximum pressure"),
    ("lbs", "kg", 0.45359237, "mass_lbs", "total payload mass"),
]


def gen_unit_conv(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    fname = pick(rng, ["flight.csv", "telemetry.csv", "log.csv"],
                 ["track.csv", "sensors.csv", "series.csv"], split)
    unit_src, unit_dst, factor, col, what = rng.choice(UNIT_PAIRS)
    n = rng.randint(40, 150)
    vals = [round(rng.uniform(0, 3000) + rng.randint(0, 2000), 2) for _ in range(n)]
    ts = sorted(rng.sample(range(0, 7200), n))
    content = f"t_s,{col}\n" + "\n".join(f"{t},{v}" for t, v in zip(ts, vals)) + "\n"
    agg = rng.choice(["max", "mean"])
    if agg == "max":
        raw = max(vals)
        phrase = f"the {what}"
    else:
        raw = sum(vals) / len(vals)
        phrase = f"the mean {' '.join(what.split()[1:]) or what}"
    expected = raw * factor
    instr = (
        f"{fname} has a '{col}' column in {unit_src}. Report {phrase} "
        f"in {unit_dst}. Answer with just the number."
    )
    sol = (
        f"python3 -c \"import csv;"
        f"v=[float(r['{col}']) for r in csv.DictReader(open('{fname}'))];"
        f"print({('max(v)' if agg == 'max' else 'sum(v)/len(v)')}*{factor})\""
        f" > answer.txt\n"
    )
    tid = f"unitconv-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=1, category="physics",
        instruction=instr, answer_mode="answer", max_turns=4,
        tags=["units", "telemetry"], seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: content},
        test_py=answer_test(expected),
        solution_sh=sol,
    )


def gen_energy_int(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    fname = pick(rng, ["battery.csv", "power.csv", "bus.csv"],
                 ["cells.csv", "draw.csv", "rail.csv"], split)
    n = rng.randint(30, 120)
    dts = [rng.randint(1, 30) for _ in range(n)]
    ts = [0]
    for d in dts:
        ts.append(ts[-1] + d)
    powers = [round(rng.uniform(50, 800) * (1 + 0.3 * (i % 7)), 3) for i in range(n + 1)]
    content = "t_s,power_w\n" + "\n".join(f"{t},{p}" for t, p in zip(ts, powers)) + "\n"
    # trapezoid integral -> Wh
    energy_j = sum(
        (powers[i] + powers[i + 1]) / 2 * (ts[i + 1] - ts[i]) for i in range(n)
    )
    expected = energy_j / 3600.0
    instr = (
        f"{fname} logs bus power: columns t_s (seconds, uneven spacing) and "
        f"power_w (watts). Integrate power over time (trapezoid) and report "
        f"the total energy in Wh. Answer with just the number."
    )
    sol = (
        "python3 - <<'EOF'\n"
        "import csv\n"
        f"rows=list(csv.DictReader(open('{fname}')))\n"
        "t=[float(r['t_s']) for r in rows]\n"
        "p=[float(r['power_w']) for r in rows]\n"
        "e=sum((p[i]+p[i+1])/2*(t[i+1]-t[i]) for i in range(len(t)-1))/3600\n"
        "open('answer.txt','w').write(str(e))\n"
        "EOF\n"
    )
    tid = f"energy-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=3, category="physics",
        instruction=instr, answer_mode="answer", max_turns=8,
        tags=["integration", "energy"], seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: content},
        test_py=answer_test(expected, rel_tol=1e-3),
        solution_sh=sol,
    )


def gen_fix_formula(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    mdot_gs = round(rng.uniform(5, 50), 2)       # g/s
    ve = round(rng.uniform(1500, 3500), 1)       # m/s
    ae = round(rng.uniform(0.05, 0.5), 4)        # m^2
    pe, p0 = 80000.0, 101325.0
    expected = (mdot_gs / 1000.0) * ve + (pe - p0) * ae
    buggy = f'''\
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = {mdot_gs}      # g/s
ve = {ve}           # m/s
pe = {pe}           # Pa
p0 = {p0}           # Pa
Ae = {ae}           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
'''
    fixed = f'''\
# Rocket thrust: F = mdot*ve + (pe - p0)*Ae
# mdot is fed from the flow meter in g/s.
mdot = {mdot_gs} / 1000.0  # convert g/s -> kg/s
ve = {ve}           # m/s
pe = {pe}           # Pa
p0 = {p0}           # Pa
Ae = {ae}           # m^2

F = mdot * ve + (pe - p0) * Ae

with open('thrust_n.txt', 'w') as f:
    f.write(str(F))
print(F)
'''
    tid = f"fixform-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=3, category="physics",
        instruction=(
            f"thrust.py computes rocket thrust in N (flow meter reads "
            f"{mdot_gs} g/s), but the result is orders of magnitude too "
            f"large — there is a units bug. Fix it and run "
            f"`python3 thrust.py` so thrust_n.txt holds the correct thrust "
            f"in newtons."
        ),
        answer_mode="files", max_turns=8,
        tags=["units", "bugfix", "physics"], seed=rng.randint(0, 10**6), split=split,
        setup_files={"thrust.py": with_id(buggy, tid)},
        test_py=f'''\
import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_thrust():
    p = BASE / "thrust_n.txt"
    assert p.exists(), "thrust_n.txt missing — run thrust.py"
    got = float(p.read_text().strip())
    assert math.isclose(got, {expected!r}, rel_tol=1e-6), f"{{got}} != {expected!r}"
''',
        solution_sh=f"cat > thrust.py <<'EOF'\n{fixed}EOF\npython3 thrust.py\n",
    )


def gen_multi_report(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    csv_f = pick(rng, ["flight.csv"], ["track.csv"], split)
    meta_f = pick(rng, ["meta.json"], ["info.json"], split)
    rep = pick(rng, ["report.txt"], ["summary.txt"], split)
    n = rng.randint(60, 200)
    ts = sorted(rng.sample(range(0, 10000), n))
    alts_ft = [round(1000 + 29000 * abs(math.sin(i / n * 3.1)) + rng.uniform(-200, 200), 1) for i in range(n)]
    fuel0 = round(rng.uniform(500, 900), 1)
    fuel1 = round(fuel0 * rng.uniform(0.3, 0.7), 1)  # lbs remaining
    content = "t_s,alt_ft\n" + "\n".join(f"{t},{a}" for t, a in zip(ts, alts_ft)) + "\n"
    meta = f'{{"airframe": "FX-{rng.randint(10,99)}", "fuel_start_lbs": {fuel0}, "fuel_end_lbs": {fuel1}}}\n'
    duration = ts[-1] - ts[0]
    max_alt_m = max(alts_ft) * 0.3048
    fuel_kg = (fuel0 - fuel1) * 0.45359237
    expected_report = (
        f"duration_s={duration}\nmax_alt_m={max_alt_m}\nfuel_kg={fuel_kg}\n"
    )
    instr = (
        f"From {csv_f} (t_s, alt_ft) and {meta_f} (fuel_start_lbs, "
        f"fuel_end_lbs), produce {rep} with exactly three lines:\n"
        "duration_s=<last minus first t_s>\n"
        "max_alt_m=<max altitude converted ft->m>\n"
        "fuel_kg=<fuel burned converted lbs->kg>"
    )
    sol = (
        "python3 - <<'EOF'\n"
        "import csv, json\n"
        f"rows=list(csv.DictReader(open('{csv_f}')))\n"
        "t=[float(r['t_s']) for r in rows]\n"
        "a=[float(r['alt_ft']) for r in rows]\n"
        f"m=json.load(open('{meta_f}'))\n"
        "rep=(f\"duration_s={t[-1]-t[0]:g}\\n\"\n"
        "     f\"max_alt_m={max(a)*0.3048}\\n\"\n"
        "     f\"fuel_kg={(m['fuel_start_lbs']-m['fuel_end_lbs'])*0.45359237}\\n\")\n"
        f"open('{rep}','w').write(rep)\n"
        "EOF\n"
    )
    tid = f"multirep-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=4, category="physics",
        instruction=instr, answer_mode="files", max_turns=10,
        tags=["report", "telemetry", "units"], seed=rng.randint(0, 10**6), split=split,
        setup_files={csv_f: content, meta_f: meta},
        test_py=f'''\
import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_report():
    p = BASE / "{rep}"
    assert p.exists(), "{rep} missing"
    kv = {{}}
    for line in p.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = float(v)
    assert math.isclose(kv["duration_s"], {duration!r}, rel_tol=1e-9)
    assert math.isclose(kv["max_alt_m"], {max_alt_m!r}, rel_tol=1e-6)
    assert math.isclose(kv["fuel_kg"], {fuel_kg!r}, rel_tol=1e-6)
''',
        solution_sh=sol,
    )
