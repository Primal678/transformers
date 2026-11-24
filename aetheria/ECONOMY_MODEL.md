# Aetheria Economy Model — First Pass

Companion to [`GDD.md`](./GDD.md) §3 Pillar 3. Model: [`sim/economy_sim.py`](./sim/economy_sim.py) (stdlib Python, runs in <1 s). Raw output: [`sim/results.md`](./sim/results.md).

> **Every input is an assumption** chosen to be plausible, not measured. The point of this pass is to find which levers matter and which design claims don't hold up; absolute numbers will move once playtest data replaces them. This is the pre-Machinations sanity check, not a substitute for it.

## What the model does

- 20k installs/day for a year; retention is a power law fitted to the GDD KPIs (D1 42%, D30 12% → D7 ≈ 21%).
- Each active player earns ~316 Aether/day (Sparks with streak, mini-games, roleplay, capped rewarded ads) and starts with a 500 grant.
- Spending: fixed sinks (upkeep for Loft+ owners, creator asset packs, VFX repair, casino house edge, seasonal donations) plus discretionary spend that rises with wealth, split between the **first-party catalogue** (100% burned) and the **player marketplace**.
- Marketplace Aether moves between players and is *not* destroyed; only the platform cut burns: 30% on first sale of UGC, 5% (3% VIP) on resale.
- Churned players' balances leave circulation.
- Dynamic fee: resale fee goes to 6% while circulating Aether per DAU exceeds 6,000.

## Results

| Scenario | Circulating Aether / DAU (day 365) | Day-1 veteran's balance (day 365) | Year sink ÷ faucet | Days at 6% fee |
|---|---|---|---|---|
| A. GDD v1.1 as written | 7,242 | 9,323 (~29 days of income) | 0.76 | 194 |
| B. No dynamic fee | 7,318 | 9,440 | 0.75 | 0 |
| C. Resale fee doubled to 10% | 6,801 | 8,653 | 0.77 | 166 |
| **D. Recommended tuning** | **2,158** | **2,296 (~9 days)** | **0.90** | **0** |
| E. D + a double-Aether week each season | 2,559 | 2,794 | 0.88 | 0 |

A sink÷faucet ratio below 1.0 during growth is expected (new players are still building balances); the stability signal is that **veteran balances plateau** instead of climbing.

## Findings

1. **The resale fee is not the primary sink.** At 5%/3% it burns ~2.6% of marketplace spend; the 30% UGC platform share burns ~13.5%. Doubling the fee to 10% (C) cuts supply by only ~6%. Fee changes are a fine-tuning knob, not a stabilizer.
2. **The dynamic fee, as specified, doesn't work.** In scenario A the threshold is crossed by about month 6 and stays crossed, so the "temporary 48-hour" adjustment becomes permanent. Even then it barely changes the outcome (A vs B). It also can't fire before supply is already high, because it reacts to supply instead of anticipating it.
3. **The levers that matter** are the faucet size and the share of spending that goes to **100%-burn first-party sinks** (catalogue items, base Action Cards, furniture, upkeep). Scenario D changes four inputs:
   - mini-game rewards 150 → 110 and roleplay wages 80 → 60 per day;
   - catalogue share of discretionary spend 25% → 40%, through a stronger rotating first-party Aether catalogue;
   - wealth propensity 0.05 → 0.08, via aspirational high-price Aether items aimed at rich players;
   - Loft+ upkeep 60 → 70 per day.

   Those changes cut veteran hoards by ~75% and keep supply flat from about month 6.
4. **Events leave a residue.** A double-Aether week each season (E) raises supply ~40% at its peak and still ~20% above D at year end. Events are survivable, but each one needs a matching first-party catalogue drop scheduled right after it.
5. **The casino hardly matters to the economy.** At a 3% house edge it burns <1 Aether per DAU per day, so geo-disabling it has no effect on balance. This is good news for the regulatory fallback.

## Design changes adopted into GDD v1.2

- The marketplace fee is described as a **secondary** sink. The primary sinks are the first-party Aether catalogue, upkeep, and the UGC platform share.
- **Economy Health Adjustment** now responds to the *trend* in veteran balances (7-day slope), not a supply threshold. Its first response is a first-party catalogue drop or aspirational sink; changing faucets is second, and the fee only third.
- Added a **rotating first-party Aether catalogue** (seasonal furniture, base-variant cosmetics, consumable party items) as an explicit sink.
- **Starting faucet targets:** ~255 Aether per active player per day (scenario D). A healthy veteran balance is ≤10 days of income.

## Limitations / next steps

- No player segmentation (whales vs. casuals, creators vs. buyers); hoarding by a top 1% is not modelled.
- Discretionary spend is a simple wealth function; real demand depends on catalogue appeal and prices.
- No price level. Item prices are assumed fixed, so "inflation" here means hoard size relative to income, not price drift.
- Next: port to Machinations with segments, then calibrate on closed-beta telemetry (faucet per DAU, spend split, veteran balance slope).
