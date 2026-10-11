#!/usr/bin/env python3
"""Oracle mirror of engine.js for Charger math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def article(n):
    s = str(int(n)) if isinstance(n, float) and n == int(n) else str(n)
    return "an" if s.startswith(("8", "11", "18")) else "a"

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def chargePlan(capMah, watts, fromPct, toPct):
    if not (capMah > 0) or not (watts > 0) or not (fromPct >= 0) or not (toPct > 0):
        return {"error": "capacity, power and percents must be positive"}
    if fromPct >= toPct:
        return {"error": "the start level must be lower than the target level"}
    if toPct > 100:
        return {"error": "the target level must be 100 or less"}
    wh = capMah * 3.7 / 1000 * (toPct - fromPct) / 100
    minutes = r1(wh / (watts * 0.8) * 60)
    return {"capMah": jsnum(float(capMah)), "watts": jsnum(float(watts)), "fromPct": jsnum(float(fromPct)),
            "toPct": jsnum(float(toPct)), "wh": jsnum(r2(wh)), "minutes": jsnum(minutes)}

def yearPlan(capMah, chargesWeek, tariff):
    if not (capMah > 0) or not (chargesWeek > 0) or not (tariff > 0):
        return {"error": "capacity, charges and tariff must be positive"}
    whFull = capMah * 3.7 / 1000
    kwhYear = r2(whFull / 0.8 * chargesWeek * 52 / 1000)
    cost = r2(kwhYear * tariff)
    return {"capMah": jsnum(float(capMah)), "chargesWeek": jsnum(float(chargesWeek)), "tariff": jsnum(float(tariff)),
            "kwhYear": jsnum(kwhYear), "cost": jsnum(cost)}

def comparePlan(oldW, newW, capMah, chargesWeek):
    if not (oldW > 0) or not (newW > 0) or not (capMah > 0) or not (chargesWeek > 0):
        return {"error": "power, capacity and charges must be positive"}
    if newW <= oldW:
        return {"error": "the new charger must be faster than the old one"}
    whFull = capMah * 3.7 / 1000
    mOld = r1(whFull / (oldW * 0.8) * 60)
    mNew = r1(whFull / (newW * 0.8) * 60)
    saved = r1(mOld - mNew)
    savedYearH = r1(saved * chargesWeek * 52 / 60)
    return {"oldW": jsnum(float(oldW)), "newW": jsnum(float(newW)), "capMah": jsnum(float(capMah)),
            "chargesWeek": jsnum(float(chargesWeek)), "mOld": jsnum(mOld), "mNew": jsnum(mNew),
            "savedMin": jsnum(saved), "savedYearH": jsnum(savedYearH)}

def renderCharge(r):
    return ("Charging " + article(r["capMah"]) + " " + fmt(r["capMah"]) + " mAh battery (labeled 3.7 V) from " + fmt(r["fromPct"]) + "% to " + fmt(r["toPct"]) + "% on " +
            article(r["watts"]) + " " + fmt(r["watts"]) + " W charger takes about " + fmt(r["minutes"]) + " minutes - " + fmt(r["wh"]) + " Wh at a labeled 80% efficiency.")

def renderYear(r):
    return ("Charging " + article(r["capMah"]) + " " + fmt(r["capMah"]) + " mAh battery " + fmt(r["chargesWeek"]) + " times a week uses about " + fmt(r["kwhYear"]) +
            " kWh a year - about " + fmt(r["cost"]) + " at your labeled " + fmt(r["tariff"]) + " per kWh tariff, at a labeled 80% efficiency.")

def renderCompare(r):
    return ("Swapping " + article(r["oldW"]) + " " + fmt(r["oldW"]) + " W charger for " + article(r["newW"]) + " " + fmt(r["newW"]) + " W charger saves about " + fmt(r["savedMin"]) +
            " minutes per full charge - about " + fmt(r["savedYearH"]) + " hours a year at " + fmt(r["chargesWeek"]) + " charges a week, at a labeled 80% efficiency.")

CASES = []
CASES.append({"fn": "chargePlan", "args": [4000, 25, 20, 80]})
CASES.append({"fn": "chargePlan", "args": [5000, 10, 0, 100]})
CASES.append({"fn": "chargePlan", "args": [3000, 65, 15, 90]})
CASES.append({"fn": "chargePlan", "args": [800, 18, 30, 85]})
CASES.append({"fn": "chargePlan", "args": [4500, 11, 10, 95]})
CASES.append({"fn": "chargePlan", "args": [2500, 33, 5, 50]})
CASES.append({"fn": "chargePlan", "args": [0, 25, 20, 80]})
CASES.append({"fn": "chargePlan", "args": [4000, 0, 20, 80]})
CASES.append({"fn": "chargePlan", "args": [4000, 25, 80, 20]})
CASES.append({"fn": "chargePlan", "args": [4000, 25, 50, 50]})
CASES.append({"fn": "chargePlan", "args": [4000, 25, 20, 120]})
CASES.append({"fn": "chargePlan", "args": [6000, 45, 25, 75]})
CASES.append({"fn": "yearPlan", "args": [4000, 5, 0.15]})
CASES.append({"fn": "yearPlan", "args": [5000, 7, 0.25]})
CASES.append({"fn": "yearPlan", "args": [3000, 3, 0.4]})
CASES.append({"fn": "yearPlan", "args": [2000, 14, 0.12]})
CASES.append({"fn": "yearPlan", "args": [6000, 10, 0.55]})
CASES.append({"fn": "yearPlan", "args": [8000, 2, 0.22]})
CASES.append({"fn": "yearPlan", "args": [0, 5, 0.15]})
CASES.append({"fn": "yearPlan", "args": [4000, 0, 0.15]})
CASES.append({"fn": "yearPlan", "args": [4000, 5, 0]})
CASES.append({"fn": "yearPlan", "args": [3500, 6, 0.3]})
CASES.append({"fn": "yearPlan", "args": [1200, 4, 0.18]})
CASES.append({"fn": "yearPlan", "args": [5500, 9, 0.65]})
CASES.append({"fn": "comparePlan", "args": [10, 25, 4000, 5]})
CASES.append({"fn": "comparePlan", "args": [5, 45, 5000, 7]})
CASES.append({"fn": "comparePlan", "args": [18, 65, 3000, 3]})
CASES.append({"fn": "comparePlan", "args": [8, 20, 6000, 4]})
CASES.append({"fn": "comparePlan", "args": [12, 30, 4500, 6]})
CASES.append({"fn": "comparePlan", "args": [7.5, 33, 3500, 2]})
CASES.append({"fn": "comparePlan", "args": [0, 25, 4000, 5]})
CASES.append({"fn": "comparePlan", "args": [25, 25, 4000, 5]})
CASES.append({"fn": "comparePlan", "args": [45, 25, 4000, 5]})
CASES.append({"fn": "comparePlan", "args": [10, 80, 8000, 1]})
CASES.append({"fn": "comparePlan", "args": [11, 18, 2200, 8]})
CASES.append({"fn": "comparePlan", "args": [15, 100, 10000, 3]})

out = []
for c in CASES:
    fn = {"chargePlan": chargePlan, "yearPlan": yearPlan, "comparePlan": comparePlan}[c["fn"]]
    r = fn(*c["args"])
    is_err = "error" in r
    if is_err:
        render = r["error"]
    else:
        render = {"chargePlan": renderCharge, "yearPlan": renderYear, "comparePlan": renderCompare}[c["fn"]](r)
    out.append({"fn": c["fn"], "args": c["args"], "result": r, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(out), "cases")
