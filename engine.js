/* Charger math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function article(n) { return /^(8|11|18)/.test(String(n)) ? "an" : "a"; }

  function chargePlan(capMah, watts, fromPct, toPct) {
    if (!(capMah > 0) || !(watts > 0) || !(fromPct >= 0) || !(toPct > 0)) return { error: "capacity, power and percents must be positive" };
    if (fromPct >= toPct) return { error: "the start level must be lower than the target level" };
    if (toPct > 100) return { error: "the target level must be 100 or less" };
    var wh = capMah * 3.7 / 1000 * (toPct - fromPct) / 100;
    var minutes = r1(wh / (watts * 0.8) * 60);
    return { capMah: capMah, watts: watts, fromPct: fromPct, toPct: toPct, wh: r2(wh), minutes: minutes };
  }

  function yearPlan(capMah, chargesWeek, tariff) {
    if (!(capMah > 0) || !(chargesWeek > 0) || !(tariff > 0)) return { error: "capacity, charges and tariff must be positive" };
    var whFull = capMah * 3.7 / 1000;
    var kwhYear = r2(whFull / 0.8 * chargesWeek * 52 / 1000);
    var cost = r2(kwhYear * tariff);
    return { capMah: capMah, chargesWeek: chargesWeek, tariff: tariff, kwhYear: kwhYear, cost: cost };
  }

  function comparePlan(oldW, newW, capMah, chargesWeek) {
    if (!(oldW > 0) || !(newW > 0) || !(capMah > 0) || !(chargesWeek > 0)) return { error: "power, capacity and charges must be positive" };
    if (newW <= oldW) return { error: "the new charger must be faster than the old one" };
    var whFull = capMah * 3.7 / 1000;
    var mOld = r1(whFull / (oldW * 0.8) * 60);
    var mNew = r1(whFull / (newW * 0.8) * 60);
    var saved = r1(mOld - mNew);
    var savedYearH = r1(saved * chargesWeek * 52 / 60);
    return { oldW: oldW, newW: newW, capMah: capMah, chargesWeek: chargesWeek, mOld: mOld, mNew: mNew, savedMin: saved, savedYearH: savedYearH };
  }

  function renderCharge(r) {
    return "Charging " + article(r.capMah) + " " + r.capMah + " mAh battery (labeled 3.7 V) from " + r.fromPct + "% to " + r.toPct + "% on " +
      article(r.watts) + " " + r.watts + " W charger takes about " + r.minutes + " minutes - " + r.wh + " Wh at a labeled 80% efficiency.";
  }

  function renderYear(r) {
    return "Charging " + article(r.capMah) + " " + r.capMah + " mAh battery " + r.chargesWeek + " times a week uses about " + r.kwhYear +
      " kWh a year - about " + r.cost + " at your labeled " + r.tariff + " per kWh tariff, at a labeled 80% efficiency.";
  }

  function renderCompare(r) {
    return "Swapping " + article(r.oldW) + " " + r.oldW + " W charger for " + article(r.newW) + " " + r.newW + " W charger saves about " + r.savedMin +
      " minutes per full charge - about " + r.savedYearH + " hours a year at " + r.chargesWeek + " charges a week, at a labeled 80% efficiency.";
  }

  var api = { chargePlan: chargePlan, yearPlan: yearPlan, comparePlan: comparePlan,
              renderCharge: renderCharge, renderYear: renderYear, renderCompare: renderCompare };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ChargerMath = api;
})(typeof window !== "undefined" ? window : this);
