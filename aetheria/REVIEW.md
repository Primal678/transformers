# Aetheria GDD v1.0 — Review Notes

Scope: internal consistency, feasibility, and regulatory exposure of [`GDD.md`](./GDD.md). Ordered by severity.

> **Status:** All findings below are addressed in GDD v1.1 — see the changelog at the end of [`GDD.md`](./GDD.md).

## Blockers (the document contradicts itself)

### 1. The Lumen→Aether ATM breaks the core economic promise
- §3 Currency table: Aether "Cannot be bought with real money."
- §6 USP #2 / #5: Aether non-purchasability is *the* structural fix and is to be "auditable."
- §7 Risk register: casino is safe because there is "no purchase path to Aether."
- **But** §3 Pillar 4 (Neon District ATM): "convert Lumen to Aether at a transparent rate, with a daily cap."

Lumen is bought with cash, so the ATM *is* a purchase path. A daily cap limits the rate, not the fact. Knock-on effects:
- **Casino becomes simulated gambling with purchasable chips** — in most jurisdictions that turns it into "social casino" regulation, and on iOS/Google Play it pushes the age rating to 17+/18+ (and Belgium/Netherlands-style loot-box rules may reach the cosmetic gacha too).
- **Pay-to-progress in the marketplace**: Aether buys base Action Cards, furniture, rent, and other players' UGC — so Lumen now buys everything Aether buys.
- **RMT incentive**: buyers can launder Lumen → Aether → overpriced listings to alt accounts.

**Recommendation:** remove the ATM conversion (or make it one-way *into Lumen-only cosmetic credit*). If a conversion is commercially required, drop the "non-purchasable" claim everywhere and re-scope the casino, rather than shipping a USP the Transparency Report would disprove.

### 2. Creator Studio revenue source is defined two ways
- §3 Sinks: Creator Studio asset packs are bought with **Aether**.
- §4 Revenue: "Actual revenue comes from **Lumen** spent on Creator Studio asset packs" — and this stream is 15% of revenue.

Pick one. If packs cost Aether, this stream earns ~$0 and the revenue mix must be rebalanced (45/30/15/10 → ~53/35/0/12).

### 3. "Status-never-sold" vs. VIP leaderboard perks
§4 says status is never sold and §2 says leaderboards are "the primary status signal," yet VIPs get **a second leaderboard entry**. A paid extra shot at the primary status ladder is selling status. Suggest replacing with a VIP-only *practice* mode or cosmetic leaderboard frame.

## High risk

### 4. Audience age vs. dating sim, casino, and emotion inference
The document never states a minimum age. Avakin's audience skews teen. A teen-rated product cannot reasonably ship a dating/compatibility mini-game, Aether-wagering casino, and continuous sentiment profiling of chat. Needs: explicit age policy, age assurance, and age-gating per feature (COPPA, UK Age Appropriate Design Code, EU DSA minors' provisions).

### 5. The Mood System is an emotional-data and harassment surface
- Inferring mood from chat/voice is processing of potentially sensitive data (GDPR special-category risk if it reads as mental-health inference; EU AI Act restricts emotion recognition in some contexts). Needs a DPIA, opt-out, and data-retention limits.
- Text sentiment is listed as always-on while voice transcription for Mood is "opt-in" — but moderation transcribes voice in real time anyway. Clarify that moderation transcripts are never fed into Mood, or disclose that they are.
- **Broadcasting low Valence / low Openness publicly signals vulnerability to predators and bullies.** Add a "Mood privacy" setting (visible to friends only / hidden), and never surface a vulnerable state to strangers' contextual radial menus by default.
- "Mood is earned through social behavior" + "Dominance" axis can turn into an exploitable or socially stratifying score. Mood should be expressive, not a reputation number.

### 6. Earned-status mechanics are trivially farmable
"Beloved" (50 received hugs/week), Resonance Crates (contain marketplace credit), and gesture-scored Fashion Shows can all be farmed with alt accounts or friend rings. Count only unique, non-linked, account-age-qualified givers; diminishing returns per giver; exclude Resonance rewards that are tradeable.

### 7. North Star metric conflates social and economic engagement
WMSI requires ≥1 economy action per session. A player who has a great social session but buys nothing scores zero, which will steer live-ops toward monetization prompts — exactly the Avakin failure this doc diagnoses. Suggest: North Star = social interactions only; track economy participation as a separate guardrail metric.

## Feasibility

### 8. Rendering budget is optimistic
- UE5 **Lumen is not supported on the mobile renderer** in practice for mid-tier devices; "Lumen-lit avatars in a 50-player zone at stable mobile frame rates" (USP #3) will not hold on iPhone 13 / SD 8 Gen 1. Plan for baked/mobile lighting with Lumen as a high-end PC feature, and change the USP wording.
- Chaos strand hair ×50 avatars on mobile is not viable; use card-based hair with simulated hero strands only for the local player and close LOD.
- Morph-fitted garments for **30,000 launch SKUs** across arbitrary body morphs is a large content-and-QA cost; consider 3–5k launch SKUs with a fitting pipeline proven first.

### 9. Pixel Streaming economics
Pixel Streaming costs a dedicated GPU slice per concurrent viewer. For a F2P audience with ~5% payers this is very likely margin-negative at scale. Keep it for low-friction trials / web onboarding with session limits, not as the standing low-end client.

### 10. Voice architecture wording
"Distributed proxy architecture … avoiding P2P and a central server" then "ODIN Voice or comparable SDK" — ODIN is a hosted SFU-style service; the architecture paragraph should describe the vendor's model rather than a bespoke one, or justify building it.

## Minor / clarifications
- **Apartment rent**: starter apartment is "free, permanent," yet rent is a sink. State which tiers pay rent and what happens on non-payment (eviction of a paid-for space will be unpopular).
- **Creator Shards** "tradeable (bundled into items)" — define whether raw Shards can be traded; if not, mark "No."
- **ARPPU** is $8–12 in §4 and $9–11 in §7; align.
- **Revenue model sanity check:** 5% payer conversion × ~$10 ARPPU ≈ $0.50/MAU/month; VIP at 1.8% × $9.99 ≈ $0.18 → ~36% of revenue, consistent with the 30% target. OK.
- **Marketplace GMV/DAU $1.20** is denominated in dollars, but Aether has no dollar value by design. Express it in Aether or define the reference rate.
- **External statistics** (Avakin DAU, Steam %, "50% toxicity reduction", "24 h → 5 s") need sources before this document circulates outside the team, and the Avakin/Lockwood comparisons should be reviewed by legal for comparative-advertising use.
- **Casino**: even with no purchase path, platform policies treat simulated gambling as a rating driver; plan for geo-disable *and* age-gate from day one.
