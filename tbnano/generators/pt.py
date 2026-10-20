"""physics templates (spec 5.3, ~30%): telemetry + rocketry computations.

All answers are numeric (answer.txt) or small key=value reports.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from .base import answer_test, files_test, json_dumps, kv_test, write_task


def _params_sol(expr: str) -> str:
    """solution.sh that reads params.json and evaluates `expr` with p[...] lookups."""
    return ("python3 - <<'PY' > answer.txt\n"
            "import json, math\n"
            "p = json.load(open('params.json'))\n"
            f"print({expr})\nPY\n")


def _telem(rng, n=200):
    # altitude: parabola rising then falling; speed: similar shape
    t0 = rng.randint(8, 14)
    lines, alts = [], []
    for i in range(n):
        t = i * 0.1
        s = math.sin(math.pi * t / (2 * t0))
        alt = max(0.0, 1200.0 * (max(0.0, s) ** 1.3))
        v = 60.0 * s
        alts.append(alt)
        lines.append(f"{t:.1f},{alt:.2f},{v:.2f},{rng.randint(20,30)}")
    return "t,alt,v,t_p\n" + "\n".join(lines) + "\n", alts


def unit_conv(rng, idx, out_root, split):
    convs = [(10, 0.3048, "feet", "meters"), (100, 0.453592, "pounds", "kg"),
             (60, 1.60934, "mph", "km/h"), (500, 0.001, "grams", "kg")]
    val, k, a, b = rng.choice(convs)
    exp = val * k
    tid = f"uconv-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has {value, factor, from_unit, to_unit}. Convert value "
        "to to_unit (value * factor). Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["convert"], template="unit_conv",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"value": val, "factor": k, "from_unit": a, "to_unit": b})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("p['value']*p['factor']"))


def vert_speed(rng, idx, out_root, split):
    # Adapted from TerminalBench 1.0 "telemetry-and-ml" telemetry family.
    telem, alts = _telem(rng)
    exp = max(alts)
    tid = f"vspeed-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "physics",
        "telem.csv has columns t,alt,v,t_p. What is the maximum altitude "
        "(m)? Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["telemetry"], template="vert_speed",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"telem.csv": telem},
        test_py=answer_test(exp, 1e-3),
        solution_sh=("tail -n +2 telem.csv | cut -d, -f2 | sort -rn | head -1 > answer.txt\n"))


def energy_int(rng, idx, out_root, split):
    m = rng.choice([0.5, 1.0, 1.5, 2.0, 2.5])
    thrust = rng.randint(20, 60)
    burn = rng.choice([1.0, 2.0, 3.0])
    w = m * 9.81
    # v_end = (thrust - w)/m * burn ; h = 0.5*a*t^2 ; energy check
    a = (thrust - w) / m
    v_end = a * burn
    exp = 0.5 * m * v_end ** 2  # kinetic energy at burnout
    tid = f"energy-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "params.json has mass_kg, thrust_n, burn_s: a rocket with constant "
        "thrust upward for burn_s from rest (g=9.81, ignore drag/mass loss). "
        "Compute the kinetic energy at burnout (J). Answer with just the "
        "number.",
        answer_mode="answer", max_turns=8, tags=["dynamics"], template="energy_int",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"mass_kg": m, "thrust_n": thrust, "burn_s": burn})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol(
            "0.5*p['mass_kg']*((p['thrust_n']-p['mass_kg']*9.81)/p['mass_kg']*p['burn_s'])**2"))


def thrust_isp(rng, idx, out_root, split):
    thrust = rng.choice([15, 20, 25, 30, 40, 50])
    burn = rng.choice([1.5, 2.0, 2.5, 3.0])
    prop = round(thrust * burn / (rng.choice([180, 200, 220]) * 9.81), 4)
    isp = thrust * burn / (prop * 9.81)
    tid = f"isp-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "params.json has thrust_n, burn_s, prop_kg for a motor. What is its "
        "specific impulse (s)? g=9.81. Answer with just the number.",
        answer_mode="answer", max_turns=7, tags=["rocket"], template="thrust_isp",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"thrust_n": thrust, "burn_s": burn, "prop_kg": prop})},
        test_py=answer_test(isp, 1e-4),
        solution_sh=_params_sol(
            "p['thrust_n']*p['burn_s']/(p['prop_kg']*9.81)"))


def center_mass(rng, idx, out_root, split):
    parts = [(round(rng.uniform(0.05, 0.5), 3), rng.randint(0, 100))
             for _ in range(rng.randint(3, 6))]
    M = sum(m for m, _ in parts)
    exp = sum(m * x for m, x in parts) / M
    lines = "\n".join(f"{m},{x}" for m, x in parts) + "\n"
    tid = f"cmass-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "physics",
        "parts.csv rows are 'mass_kg,pos_cm'. Compute the center of mass "
        "position (cm). Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["mass"], template="center_mass",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"parts.csv": lines},
        test_py=answer_test(exp, 1e-4),
        solution_sh=("head -3 thrust.csv\n"
                     "python3 - <<'PY' > answer.txt\n"
                     "rows=[l.split(',') for l in open('parts.csv').read().split()]\n"
                     "M=sum(float(m) for m,_ in rows)\n"
                     "print(sum(float(m)*float(x) for m,x in rows)/M)\nPY\n"))


def battery_c(rng, idx, out_root, split):
    mah = rng.choice([850, 1000, 1300, 1500, 2200])
    crate = rng.choice([10, 20, 25, 30])
    exp = mah / 1000.0 * crate
    tid = f"batt-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has mah and c_rating for a battery. What is the max "
        "continuous current (A)? Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["battery"], template="battery_c",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps({"mah": mah, "c_rating": crate})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("p['mah']/1000*p['c_rating']"))


def course_dist(rng, idx, out_root, split):
    lat1 = round(rng.uniform(30, 60), 4)
    lon1 = round(rng.uniform(-10, 30), 4)
    d_km = rng.randint(50, 500)
    # simple flat-earth-ish: use haversine to a point d_km east
    R = 6371.0
    lon2 = lon1 + (d_km / (R * math.cos(math.radians(lat1)))) * 180 / math.pi
    dlat = math.radians(0)
    dlon = math.radians(lon2 - lon1)
    a = math.cos(math.radians(lat1)) ** 2 * math.sin(dlon / 2) ** 2
    exp = 2 * R * math.asin(math.sqrt(a))
    tid = f"course-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        f"gps.txt has 'lat1={lat1}', 'lon1={lon1}', 'lat2={lat1}', "
        f"'lon2={lon2:.4f}'. Compute the haversine distance (km, R=6371). "
        f"Answer with just the number.",
        answer_mode="answer", max_turns=8, tags=["gps"], template="course_dist",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"gps.txt": f"lat1={lat1}\nlon1={lon1}\nlat2={lat1}\nlon2={lon2:.4f}\n"},
        test_py=answer_test(exp, 1e-3),
        solution_sh=("python3 - <<'PY' > answer.txt\nimport math\n"
                     "kv=dict(l.split('=') for l in open('gps.txt').read().split())\n"
                     "la=float(kv['lat1']);lo1=float(kv['lon1']);lo2=float(kv['lon2'])\n"
                     "dlon=math.radians(lo2-lo1)\n"
                     "a=math.cos(math.radians(la))**2*math.sin(dlon/2)**2\n"
                     "print(2*6371*math.asin(math.sqrt(a)))\nPY\n"))


def lift_force(rng, idx, out_root, split):
    rho = 1.225
    v = rng.randint(15, 45)
    s = round(rng.uniform(0.3, 1.5), 2)
    cl = round(rng.uniform(0.4, 1.2), 2)
    exp = 0.5 * rho * v * v * s * cl
    tid = f"lift-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has wing area_m2, cl, v_ms (rho=1.225 kg/m^3). Lift "
        "force (N)? Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["aero"], template="lift_force",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"area_m2": s, "cl": cl, "v_ms": v})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("0.5*1.225*p['v_ms']**2*p['area_m2']*p['cl']"))


def peak_telem(rng, idx, out_root, split):
    telem, alts = _telem(rng)
    # time of peak altitude
    lines = telem.splitlines()[1:]
    ti = alts.index(max(alts))
    t_peak = float(lines[ti].split(",")[0])
    tid = f"tpeak-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "telem.csv has t,alt,v,t_p. At what time t does altitude peak? "
        "Answer with just the number.",
        answer_mode="answer", max_turns=7, tags=["telemetry"], template="peak_telem",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"telem.csv": telem},
        test_py=answer_test(t_peak, 1e-6),
        solution_sh=("head -3 telem.csv\n"
                     "python3 - <<'PY' > answer.txt\n"
                     "rows=[l.split(',') for l in open('telem.csv').read().split()[1:]]\n"
                     "print(max(rows, key=lambda r: float(r[1]))[0])\n"
                     "PY\n"))


def fix_formula(rng, idx, out_root, split):
    m = rng.choice([1.0, 1.5, 2.0])
    thrust = rng.choice([20, 30, 40])
    buggy = ("m = %r\nT = %r\ng = 9.81\n"
             "a = T / m - g\nprint('accel:', a)\n") % (m, thrust)
    # bug is not the code but a wrong formula? Use: buggy uses T*m - g
    buggy = (f"m = {m}\nT = {thrust}\ng = 9.81\n"
             "a = T * m - g\nprint('accel:', a)\n")
    exp = thrust / m - 9.81
    tid = f"fixf-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "accel.py should compute net upward accel = T/m - g, but it uses "
        "T*m - g. Fix the formula, run it, write 'a=<value>' (just the "
        "number after 'accel:') to out.txt.",
        answer_mode="files", max_turns=7, tags=["debug", "formula"], template="fix_formula",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"accel.py": buggy},
        test_py=files_test("out.txt", f"{exp}\n"),
        solution_sh=("sed -i 's/T \\* m/T \\/ m/' accel.py\n"
                     "python3 accel.py | awk '{print $2}' > out.txt\n"))


def multi_report(rng, idx, out_root, split):
    telem, alts = _telem(rng)
    lines = telem.splitlines()[1:]
    ti = alts.index(max(alts))
    t_peak = float(lines[ti].split(",")[0])
    vmax = max(float(l.split(",")[2]) for l in lines)
    exp = {"apogee_m": max(alts), "t_apogee_s": t_peak, "vmax_ms": vmax}
    tid = f"mrep-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 4, "physics",
        "telem.csv has t,alt,v,t_p. Inspect the columns, then write "
        "report.txt with exactly three lines: 'apogee_m=<max alt>', "
        "'t_apogee_s=<t at max alt>', 'vmax_ms=<max v>'. Verify the file "
        "has 3 lines.",
        answer_mode="files", max_turns=12, tags=["telemetry", "report"],
        template="multi_report",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"telem.csv": telem},
        test_py=kv_test("report.txt", exp, 1e-4),
        solution_sh=("head -3 telem.csv\n"
                     "python3 - <<'PY'\n"
                     "rows=[l.split(',') for l in open('telem.csv').read().split()[1:]]\n"
                     "ap=max(rows,key=lambda r:float(r[1]))\n"
                     "vm=max(float(r[2]) for r in rows)\n"
                     "open('report.txt','w').write(\n"
                     " f'apogee_m={ap[1]}\\nt_apogee_s={ap[0]}\\nvmax_ms={vm}\\n')\n"
                     "PY\nwc -l report.txt\n"))


def orbital_v(rng, idx, out_root, split):
    alt = rng.choice([200, 300, 400, 550])
    exp = math.sqrt(3.986e14 / (6371e3 + alt * 1e3))
    tid = f"orbv-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has alt_km. Circular orbit speed at that altitude "
        "(mu=3.986e14 m^3/s^2, R_earth=6371 km), in m/s. Answer with just "
        "the number.",
        answer_mode="answer", max_turns=5, tags=["orbit"], template="orbital_v",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps({"alt_km": alt})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("math.sqrt(3.986e14/(6371e3+p['alt_km']*1e3))"))


def drag_force(rng, idx, out_root, split):
    v = rng.randint(20, 60)
    cd = round(rng.uniform(0.3, 0.9), 2)
    a = round(rng.uniform(0.005, 0.03), 4)
    exp = 0.5 * 1.225 * v * v * cd * a
    tid = f"drag-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has v_ms, cd, area_m2 (rho=1.225). Drag force (N)? "
        "Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["aero"], template="drag_force",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"v_ms": v, "cd": cd, "area_m2": a})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("0.5*1.225*p['v_ms']**2*p['cd']*p['area_m2']"))


def delta_v(rng, idx, out_root, split):
    isp = rng.choice([180, 200, 220, 250])
    m0 = round(rng.uniform(2.0, 5.0), 2)
    mf = round(m0 - rng.uniform(0.2, 1.0), 2)
    exp = isp * 9.81 * math.log(m0 / mf)
    tid = f"deltav-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "params.json has isp_s, m0_kg, mf_kg (g0=9.81). Tsiolkovsky "
        "delta-v (m/s)? Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["rocket"], template="delta_v",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"isp_s": isp, "m0_kg": m0, "mf_kg": mf})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol(
            "p['isp_s']*9.81*math.log(p['m0_kg']/p['mf_kg'])"))


def fuel_time(rng, idx, out_root, split):
    rate = round(rng.uniform(0.01, 0.08), 3)  # kg/s
    fuel = round(rng.uniform(0.4, 1.5), 2)
    exp = fuel / rate
    tid = f"fuel-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has burn_rate_kgs and fuel_kg for a motor. Burn time "
        "(s)? Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["rocket"], template="fuel_time",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps(
            {"burn_rate_kgs": rate, "fuel_kg": fuel})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("p['fuel_kg']/p['burn_rate_kgs']"))


def pressure_alt(rng, idx, out_root, split):
    p = rng.choice([700, 800, 850, 900, 950])  # hPa
    exp = 44330.0 * (1 - (p / 1013.25) ** 0.1903)
    tid = f"palt-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has pressure_hpa. Pressure altitude (ISA: "
        "h=44330*(1-(P/1013.25)^0.1903) m). Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["atmo"], template="pressure_alt",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps({"pressure_hpa": p})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("44330*(1-(p['pressure_hpa']/1013.25)**0.1903)"))


def mach_speed(rng, idx, out_root, split):
    t_c = rng.choice([-40, -20, 0, 15, 25])
    mach = rng.choice([0.5, 0.8, 1.2, 1.5])
    a = 331.3 * math.sqrt(1 + t_c / 273.15)
    exp = mach * a
    tid = f"mach-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics",
        "params.json has temp_c and mach. Speed of sound "
        "a=331.3*sqrt(1+T/273.15) m/s; what is Mach N in m/s? Answer with "
        "just the number.",
        answer_mode="answer", max_turns=5, tags=["aero"], template="mach_speed",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps({"temp_c": t_c, "mach": mach})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol(
            "p['mach']*331.3*math.sqrt(1+p['temp_c']/273.15)"))


def impulse_int(rng, idx, out_root, split):
    # integrate thrust curve
    peak = rng.randint(30, 80)
    n = 100
    vals = [peak * math.sin(math.pi * i / n) for i in range(n + 1)]
    dt = 0.01
    exp = sum((vals[i] + vals[i + 1]) / 2 * dt for i in range(n))
    content = "t,thrust\n" + "\n".join(f"{i * dt:.2f},{v:.3f}" for i, v in enumerate(vals)) + "\n"
    tid = f"impulse-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "physics",
        "thrust.csv has t,thrust at dt=0.01 s. Compute total impulse "
        "(N*s) by trapezoid integration. Answer with just the number.",
        answer_mode="answer", max_turns=8, tags=["integrate"], template="impulse_int",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"thrust.csv": content},
        test_py=answer_test(exp, 1e-3),
        solution_sh=("head -3 thrust.csv\n"
                     "python3 - <<'PY' > answer.txt\n"
                     "rows=[l.split(',') for l in open('thrust.csv').read().split()[1:]]\n"
                     "v=[float(r[1]) for r in rows]\n"
                     "print(sum((v[i]+v[i+1])/2*0.01 for i in range(len(v)-1)))\nPY\n"))


def glide_ratio(rng, idx, out_root, split):
    cl = round(rng.uniform(0.6, 1.4), 2)
    cd = round(rng.uniform(0.02, 0.08), 3)
    exp = cl / cd
    tid = f"glide-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "physics",
        "params.json has cl and cd. Glide ratio L/D? Answer with just the "
        "number.",
        answer_mode="answer", max_turns=4, tags=["aero"], template="glide_ratio",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"params.json": json_dumps({"cl": cl, "cd": cd})},
        test_py=answer_test(exp, 1e-4),
        solution_sh=_params_sol("p['cl']/p['cd']"))


# ---------------- train-only physics ------------------------------------

def _simple(rng, idx, out_root, split, template, q, exp, sol, tags):
    tid = f"{template.replace('t_','t')[:6]}-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics", q,
        answer_mode="answer", max_turns=4, tags=tags, template=template,
        seed=rng.randint(0, 10**6), split=split,
        test_py=answer_test(exp, 1e-4), solution_sh=sol)


def t_kmh_mph(rng, idx, out_root, split):
    v = rng.choice([50, 80, 100, 120])
    return _simple(rng, idx, out_root, split, "t_kmh_mph",
                   f"Convert {v} km/h to mph (x0.621371). Number only.",
                   v * 0.621371, f"python3 -c 'print({v}*0.621371)' > answer.txt\n",
                   ["convert"])


def t_c_to_k(rng, idx, out_root, split):
    c = rng.choice([-40, 0, 20, 100])
    return _simple(rng, idx, out_root, split, "t_c_to_k",
                   f"Convert {c} C to Kelvin. Number only.",
                   c + 273.15, f"python3 -c 'print({c}+273.15)' > answer.txt\n",
                   ["convert"])


def t_rpm_rads(rng, idx, out_root, split):
    r = rng.choice([600, 1200, 3000, 6000])
    import math as m
    return _simple(rng, idx, out_root, split, "t_rpm_rads",
                   f"Convert {r} rpm to rad/s. Number only.",
                   r * 2 * m.pi / 60,
                   f"python3 -c 'import math;print({r}*2*math.pi/60)' > answer.txt\n",
                   ["convert"])


def t_m_km(rng, idx, out_root, split):
    v = rng.choice([1500, 2500, 4200])
    return _simple(rng, idx, out_root, split, "t_m_km",
                   f"Convert {v} m to km. Number only.",
                   v / 1000, f"python3 -c 'print({v}/1000)' > answer.txt\n",
                   ["convert"])


def t_w_kw(rng, idx, out_root, split):
    v = rng.choice([1500, 2300, 4500])
    return _simple(rng, idx, out_root, split, "t_w_kw",
                   f"Convert {v} W to kW. Number only.",
                   v / 1000, f"python3 -c 'print({v}/1000)' > answer.txt\n",
                   ["convert"])


def t_avg_speed(rng, idx, out_root, split):
    d = rng.choice([100, 250, 400])
    t = rng.choice([2, 4, 5])
    return _simple(rng, idx, out_root, split, "t_avg_speed",
                   f"A rocket travels {d} km in {t} h. Average speed km/h? "
                   f"Number only.",
                   d / t, f"python3 -c 'print({d}/{t})' > answer.txt\n",
                   ["kinematics"])


def t_total_mass(rng, idx, out_root, split):
    parts = [round(rng.uniform(0.05, 0.5), 2) for _ in range(rng.randint(3, 6))]
    q = ("masses.txt has component masses in kg, one per line. Total mass? "
         "Number only.")
    tid = f"ttmass-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "physics", q,
        answer_mode="answer", max_turns=4, tags=["sum"], template="t_total_mass",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"masses.txt": "\n".join(map(str, parts)) + "\n"},
        test_py=answer_test(sum(parts), 1e-4),
        solution_sh="awk '{s+=$1}END{print s}' masses.txt > answer.txt\n")


def t_fuel_pct(rng, idx, out_root, split):
    m0 = rng.choice([2.0, 3.0, 4.0])
    f = round(rng.uniform(0.2, 0.8), 2)
    return _simple(rng, idx, out_root, split, "t_fuel_pct",
                   f"Rocket mass {m0} kg has {f} kg fuel. Fuel percent? "
                   f"Number only.",
                   f / m0 * 100,
                   f"python3 -c 'print({f}/{m0}*100)' > answer.txt\n",
                   ["percent"])


def t_n_lbf(rng, idx, out_root, split):
    v = rng.choice([10, 25, 50, 100])
    return _simple(rng, idx, out_root, split, "t_n_lbf",
                   f"Convert {v} N to lbf (x0.224809). Number only.",
                   v * 0.224809, f"python3 -c 'print({v}*0.224809)' > answer.txt\n",
                   ["convert"])


def t_pa_psi(rng, idx, out_root, split):
    v = rng.choice([100000, 101325, 200000])
    return _simple(rng, idx, out_root, split, "t_pa_psi",
                   f"Convert {v} Pa to psi (x0.000145038). Number only.",
                   v * 0.000145038,
                   f"python3 -c 'print({v}*0.000145038)' > answer.txt\n",
                   ["convert"])
