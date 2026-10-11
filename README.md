# Charger math

What a charge actually costs in minutes, kWh and money - and what a faster charger really buys back. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/chargermath/

## The three tools

- **Charge plan** - `chargePlan(capMah, watts, fromPct, toPct)`: a percent range at a wattage becomes minutes on the cable and the Wh moved.
- **Year plan** - `yearPlan(capMah, chargesWeek, tariff)`: a charging habit becomes kWh a year and its cost at your tariff.
- **Upgrade plan** - `comparePlan(oldW, newW, capMah, chargesWeek)`: old versus new charger becomes minutes saved per charge and hours a year.

## Labeled norms (illustrative references, not rules)

- Cell voltage: 3.7 V nominal. Charge efficiency: 80% - some wall power leaves as heat.
- Reference tariff: 0.15 per kWh; put in your own.

Real charging slows near full and varies by device, so treat the minutes as honest estimates.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (36 cases, 108 checks)

Regenerate the oracle expectations: `python3 oracle.py`
