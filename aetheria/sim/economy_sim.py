"""Aetheria Aether economy sink/faucet simulation (GDD v1.1, §3 Pillar 3).

Stdlib only. Run:  python aetheria/sim/economy_sim.py
Writes aetheria/sim/results.md.

Model
-----
* Daily install cohorts; retention follows a power law fitted to the GDD KPIs
  (D1 42%, D30 12%; gives D7 ~21%).
* Each cohort tracks the average Aether balance of its *active* players.
  Churned players take their balance with them (dormant supply, not circulating).
* Marketplace trades between active players move Aether but only the fee /
  UGC platform share is burned. First-party catalogue purchases burn 100%.
* Discretionary spend = min(balance, base_desire + wealth_propensity * balance),
  so richer players spend more (gives a finite equilibrium when sinks are deep enough).
* Dynamic fee: if circulating Aether per DAU exceeds a threshold, the resale fee
  rises to 6% (GDD "Economy Health Adjustment").

All parameters are ASSUMPTIONS for tuning, not measured data.
"""

from __future__ import annotations

import copy
import math
from pathlib import Path

BASE = {
    "days": 365,
    "installs_per_day": 20_000,
    "d1": 0.42,
    "d30": 0.12,
    "starter_grant": 500,
    # Faucets (Aether per active player per day)
    "spark_base": 40,
    "spark_avg_multiplier": 1.4,
    "minigames": 150,
    "roleplay": 80,
    "ad_opt_in_rate": 0.5,
    "ads_per_day": 3,
    "ad_reward": 20,
    # Discretionary spend behaviour
    "base_desire": 200,
    "wealth_propensity": 0.05,
    "share_catalogue": 0.25,  # first-party items, Action Cards, furniture: 100% burn
    "share_market": 0.75,  # player marketplace
    "market_ugc_primary_share": 0.45,  # of market spend: first sale of UGC (30% burned)
    "ugc_burn": 0.30,
    "resale_fee": 0.05,
    "resale_fee_high": 0.06,
    "vip_trade_share": 0.15,
    "vip_fee": 0.03,
    "dynamic_fee_threshold": 6_000,  # circulating Aether per DAU
    # Fixed sinks
    "upkeep_per_day": 60,  # Loft+ weekly upkeep / 7
    "loft_max_share": 0.5,
    "loft_ramp_days": 120,
    "creator_share": 0.10,
    "creator_pack_spend": 100,
    "vfx_repair": 10,
    "casino_adult_share": 0.6,
    "casino_play_rate": 0.2,
    "casino_wager": 100,
    "casino_edge": 0.03,
    # Seasonal community burn
    "season_days": 42,
    "season_participation": 0.4,
    "season_donation_frac": 0.15,
}

SCENARIOS = {
    "A. GDD v1.1 as written": {},
    "B. No dynamic fee": {"dynamic_fee_threshold": math.inf},
    "C. Fee at 10% (fee-only fix)": {"resale_fee": 0.10, "resale_fee_high": 0.12},
    "D. Recommended tuning": {
        "minigames": 110,
        "roleplay": 60,
        "share_catalogue": 0.40,
        "share_market": 0.60,
        "wealth_propensity": 0.08,
        "upkeep_per_day": 70,
    },
    "E. Recommended + double-Aether week every season": {
        "minigames": 110,
        "roleplay": 60,
        "share_catalogue": 0.40,
        "share_market": 0.60,
        "wealth_propensity": 0.08,
        "upkeep_per_day": 70,
        "_double_week": True,
    },
}


def retention(age: int, p: dict) -> float:
    if age == 0:
        return 1.0
    k = math.log(p["d1"] / p["d30"]) / math.log(30)
    return p["d1"] * age ** (-k)


def simulate(p: dict) -> dict:
    cohorts: list[float] = []  # avg active balance per cohort, index = install day
    faucet_total = sink_total = 0.0
    snapshots = {}
    fee_high_days = 0
    k = math.log(p["d1"] / p["d30"]) / math.log(30)
    ret = [retention(a, p) for a in range(p["days"] + 1)]
    for day in range(p["days"]):
        cohorts.append(float(p["starter_grant"]))
        # circulating supply per DAU (start of day) to drive the dynamic fee
        dau = sum(p["installs_per_day"] * ret[day - c] for c in range(len(cohorts)))
        circ = sum(p["installs_per_day"] * ret[day - c] * b for c, b in enumerate(cohorts))
        per_dau = circ / dau
        fee_high = per_dau > p["dynamic_fee_threshold"]
        fee_high_days += fee_high
        resale_fee = p["resale_fee_high"] if fee_high else p["resale_fee"]
        eff_resale = p["vip_trade_share"] * p["vip_fee"] + (1 - p["vip_trade_share"]) * resale_fee
        market_burn_rate = (
            p["market_ugc_primary_share"] * p["ugc_burn"]
            + (1 - p["market_ugc_primary_share"]) * eff_resale
        )
        double = p.get("_double_week") and (day % p["season_days"]) < 7
        faucet = (
            p["spark_base"] * p["spark_avg_multiplier"]
            + (p["minigames"] + p["roleplay"]) * (2 if double else 1)
            + p["ad_opt_in_rate"] * p["ads_per_day"] * p["ad_reward"]
        )
        season_day = day > 0 and day % p["season_days"] == 0
        day_f = day_s = 0.0
        for c, bal in enumerate(cohorts):
            age = day - c
            n = p["installs_per_day"] * ret[age]
            bal += faucet
            burn = 0.0
            # fixed sinks
            loft = min(p["loft_max_share"], age / p["loft_ramp_days"] * p["loft_max_share"])
            fixed = (
                loft * p["upkeep_per_day"]
                + p["creator_share"] * p["creator_pack_spend"]
                + p["vfx_repair"]
                + p["casino_adult_share"] * p["casino_play_rate"] * p["casino_wager"] * p["casino_edge"]
            )
            fixed = min(fixed, bal)
            bal -= fixed
            burn += fixed
            # discretionary spend
            spend = min(bal, p["base_desire"] + p["wealth_propensity"] * bal)
            cat = spend * p["share_catalogue"]
            mkt_burn = spend * p["share_market"] * market_burn_rate
            bal -= cat + mkt_burn  # non-burned market spend moves to sellers (net zero)
            burn += cat + mkt_burn
            if season_day:
                don = bal * p["season_donation_frac"] * p["season_participation"]
                bal -= don
                burn += don
            cohorts[c] = bal
            day_f += faucet * n
            day_s += burn * n
        faucet_total += day_f
        sink_total += day_s
        if day + 1 in (30, 90, 180, 365):
            snapshots[day + 1] = {
                "per_dau": per_dau,
                "sink_ratio": day_s / day_f,
                "vet_balance": cohorts[0],
            }
    return {
        "snapshots": snapshots,
        "sink_ratio_total": sink_total / faucet_total,
        "fee_high_days": fee_high_days,
        "faucet_per_day": faucet,
        "k": k,
    }


def main() -> None:
    lines = [
        "# Economy Simulation Results",
        "",
        "Generated by `economy_sim.py`. All inputs are assumptions; see the script header.",
        "",
        "Columns: circulating Aether per DAU / daily sink÷faucet ratio / balance of a day-1 veteran still playing.",
        "",
        "| Scenario | Day 30 | Day 90 | Day 180 | Day 365 | Year sink÷faucet | Days at 6% fee |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, override in SCENARIOS.items():
        p = copy.deepcopy(BASE)
        p.update(override)
        r = simulate(p)
        cells = []
        for d in (30, 90, 180, 365):
            s = r["snapshots"][d]
            cells.append(f"{s['per_dau']:,.0f} / {s['sink_ratio']:.2f} / {s['vet_balance']:,.0f}")
        lines.append(
            f"| {name} | " + " | ".join(cells) + f" | {r['sink_ratio_total']:.2f} | {r['fee_high_days']} |"
        )
        print(name, f"sink/faucet={r['sink_ratio_total']:.2f}", r["snapshots"][365])
    out = Path(__file__).with_name("results.md")
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
