# AETHERIA: LIVE YOUR NEXT LIFE

*"Not just a world. Your world, with feeling."*

**GAME DESIGN DOCUMENT — CONFIDENTIAL**

| | |
|---|---|
| Document Version | 1.1 |
| Role | Chief Product Officer & Lead Game Architect |
| Target Platforms | iOS, Android, PC (Windows/macOS), Web (Pixel Streaming, trial/onboarding) |
| Engine | Unreal Engine 5.4+ |
| Session Cap | 50–75 players per instance |
| Genre | 3D Social Virtual World MMO |
| Model | Free-to-Play with Premium Subscription |
| Audience | 13+ globally (16+ where local law requires); several features 18+ only — see §1.1 |

> See [`REVIEW.md`](./REVIEW.md) for the v1.0 review that drove this revision, and the [Changelog](#changelog-v10--v11) at the end.

---

## 1. Executive Summary

Avakin Life proved that a persistent 3D social world could sustain over a decade of engagement, reaching 220,000 daily active users in 2025 and surpassing 500 million lifetime downloads. But its legacy is also a cautionary tale: Steam reviews sit at 63% positive, with players citing "heavy monetization," "chat toxicity," and "frequent performance problems" as persistent pain points. The premium currency (Crowns) is widely criticized as "completely ruining the experience," locking the best items behind paywalls that feel insurmountable without real-money spending.

> *Sourcing note: competitor figures and quotes above must be cited to primary sources, and comparative claims reviewed by legal, before this document circulates outside the core team.*

Aetheria is built to inherit Avakin's throne by solving those exact failures. It delivers a best-in-class UE5 social world that scales from mobile to high-end PC, a player-driven economy that rewards creativity over spending, an emotion-aware social engine that makes every interaction feel consequential, and a moderation-first architecture that protects the social fabric. The objective is not to be "Avakin with better graphics." It is to be the first social world where the economy, the avatar, and the conversation are all systems of genuine expression, not monetization gates.

**North Star Metric: Weekly Meaningful Social Interactions (WMSI)** — a session with ≥3 proximity interactions (voice, gesture, or Action Card co-performance) with at least one *other non-linked account*. Target: **4.2 WMSI per WAU by Month 12.**

The North Star is deliberately social-only: a great conversation that ends without a purchase still counts. Economy health is tracked as a separate **guardrail**, never as part of the North Star:

- **Economy Participation Rate:** % of WAU with ≥1 economy action (purchase, trade, or listing) per week. Target band: 35–55%. Live-ops may not ship features whose primary purpose is to move this metric by inserting purchase prompts into social flows.

### 1.1 Audience & Age Policy

| Bracket | Access |
|---|---|
| Under 13 | Not permitted. Neutral age screen at signup; no account creation. |
| 13–17 ("Teen") | Core loop, wardrobe, zones, mini-games (except below), marketplace (spending caps), proximity voice **off by default** and friends-only when enabled, Mood visibility defaults to *Friends only*, text-sentiment Mood input **off by default**. |
| 18+ ("Adult") | Full access, including Dating Simulation and Social Casino, subject to age assurance and territory. |

- Age assurance (platform age signals, ID or facial age estimation via a third-party provider) is required before any 18+ feature unlocks.
- Teen and Adult players are matched into separate instances for voice, Dating Simulation, and private apartment visits by non-friends.
- Compliance targets: COPPA, UK Age Appropriate Design Code, EU DSA minors' provisions, and platform store age-rating rules. A Data Protection Impact Assessment (DPIA) is a launch gate.

---

## 2. Core Gameplay Loop: The Aetheria Session

The loop is engineered for a 12–25 minute mobile session that converts a passive login into a social + economic + expressive cycle, with clear return hooks.

| Step | Player Action | System Response | Retention / Monetization Hook |
|---|---|---|---|
| **1. Arrive** (0–60s) | Login; avatar spawns in Apartment or last social zone. | "Mood" carries over from last session. Proximity voice hums with nearby players. Daily "Spark" reward delivered via a diegetic object (mailbox, phone notification). | Streak-based Spark multiplier (Day 7 = 2×). VIPs get a "Concierge" spawn with a curated social recommendation. |
| **2. Express** (1–3 min) | Open Wardrobe; adjust outfit, hair, body morph, or animation set. | Real-time preview in a studio-lit wardrobe scene (Lumen on supported PC hardware; high-quality baked lighting elsewhere). "Fit Check" button posts a snapshot to a zone-local feed for reactions. | Limited-time "Drop Window" items appear in wardrobe with a soft countdown; not paywalled, but earnable via play or tradeable on the market. |
| **3. Socialize** (3–12 min) | Enter a zone; approach a cluster; use proximity voice, gesture (wave/nod/hug), or deploy an Action Card (guitar, dance, cooking). | Mood system reacts: avatars blush, laugh, or withdraw based on gesture responses and (where enabled) chat sentiment. Action Card co-performance triggers a synchronized animation with nearby players. | Social "Resonance" meter fills with every positive interaction; at full, grants a Resonance Crate containing an **account-bound** cosmetic shard. |
| **4. Create/Compete** (12–20 min) | Join a Fashion Show, Karaoke room, or roleplay scenario (Hospital shift, Café rush). | Mini-game scores feed into a weekly Creator Leaderboard. Top performers earn "Aether" (tradeable soft currency) and a featured slot in the zone's Hall of Fame. | Leaderboard visibility is the primary status signal; no power and no status is sold. Every player gets exactly one ranked entry. VIPs get an unranked practice mode, a cosmetic leaderboard frame, and a replay-analysis tool. |
| **5. Circulate** (20–25 min) | List an item on the Marketplace, browse player-created furniture, or place a bid on a rare animation set. | Marketplace is fully player-driven; Aetheria takes a 5% transaction fee in Aether, which is burned (removed from economy). | The 5% sink is the primary inflation-control mechanism. VIP sellers pay 3% instead of 5%, a convenience perk, not an exclusive right. |
| **6. Return Hook** | Session ends; avatar enters "Idle Mood" visible to friends. | Push notification: "Mira left you a Resonance gift" or "Your Marketplace listing sold." | Idle Mood and async gifts create a social obligation loop that does not require the recipient to be online simultaneously. |

---

## 3. Feature Breakdown: The Five Pillars

### Pillar 1 — Avatar Customization & the Mood System

**Design Principle:** The avatar is not a mannequin; it is an emotional prosthesis. Customization must be deep enough to make the Mood system legible and socially meaningful.

**Customization Depth:**

- **Body:** Height, musculature, weight distribution, shoulder width, hip ratio, limb length, and 12 face-morph sliders (jaw, cheekbone, brow, nose, lip, eye spacing, etc.). No gender-locked morphs; all sliders are available to all avatars.
- **Hair & Face:** Layered card-based hair with physics simulation (UE5 Chaos) on the local player and near-LOD avatars; strand-based hair as a high-end PC option. 40+ makeup layers (blush, contour, eyeshadow, lip texture, freckles, scars), and facial hair with density control.
- **Clothing:** 3,000–5,000 launch SKUs across tops, bottoms, outerwear, shoes, accessories, and "Aetherwear" (fantasy/roleplay costumes), scaling via seasonal drops and the Creator Studio. Every item is fitted to the body morph through an automated morph-fitting pipeline, not a static mesh — a critical technical differentiator against Avakin's rigid garment system. The fitting pipeline must pass QA on the full morph range before SKU count is scaled.
- **Animations:** Idle sets (confident, shy, playful, brooding), walk styles, dance packs, and Action Card animations that can be equipped to gesture slots.

**The Mood System (Core Innovation):**
Every avatar has a persistent **Mood Vector** with four axes: **Valence** (positive/negative), **Arousal** (calm/excited), **Dominance** (assertive/submissive), and **Social Openness** (receptive/withdrawn). Mood is affected by:

- Gesture reception (a hug received when Openness is low produces a "startled" micro-animation; the same hug at high Openness produces a "melt" animation).
- Environmental context (a dark club raises Arousal; a quiet beach lowers it).
- Action Card co-performance (synchronized guitar duet raises Valence and Dominance for both players).
- Player self-set mood (a quick mood dial lets players override or nudge their own state at any time).
- Chat sentiment — **opt-in** for Adults, off by default for Teens; on-device or ephemeral processing only; text is not stored for Mood purposes.
- Voice is **never** used as a Mood input. Voice transcripts produced for moderation are used only for moderation and are never fed into Mood.

Mood manifests visibly through idle animation blending, facial expression, posture, and subtle particle effects (a soft glow for high Valence, a slight desaturation for low Valence). Crucially, **Mood is not purchasable.** It is earned through social behavior. This is the ethical line: self-expression is monetizable; emotional state is not.

**Mood Safeguards:**

- **Mood Privacy setting:** *Everyone / Friends only / Hidden.* Default is *Friends only* for Teens and *Everyone* for Adults. Hidden shows a neutral idle to others.
- **No vulnerability broadcasting:** low-Valence or low-Openness states are rendered to non-friends as neutral. Contextual gesture menus never surface "Comfort/Hug" options to strangers based on a target's low mood.
- **Mood is expressive, not reputational:** Mood values are never shown as numbers, never ranked, never used in matchmaking, and never affect rewards, prices, or access.
- **Data handling:** Mood state is stored as a coarse vector only, with a rolling retention window; players can view and reset it. Emotion inference is scoped and documented in the DPIA, with EU AI Act review.

### Pillar 2 — Social Interaction Engine: Voice, Gesture, and Action Cards

**Design Principle:** Avakin's social layer is text-first and emote-thin. Aetheria's is spatially aware, physically expressive, and co-operative.

**Proximity Voice Chat:**

- Spatial audio with distance-based attenuation, occlusion (walls muffle sound), and reverb profiles per zone (club = tight, echo-heavy; forest = open, diffuse).
- Push-to-talk on mobile (large, repositionable button) and open-mic with VAD (voice activity detection) on PC, with a visible "mic halo" so players know when they are transmitting.
- Teens: voice off by default; when enabled, friends-only and never mixed with Adult instances.
- **Technical approach:** A hosted voice SDK (ODIN Voice or comparable) using server-side selective forwarding with dynamic, proximity-based audio rooms. This avoids the bandwidth scalability problems of pure peer-to-peer and offloads codec, noise suppression, and routing to a proven vendor rather than a bespoke system.
- **Moderation:** Real-time voice transcription feeds an AI toxicity classifier. First offense = in-session mute + warning; repeat = 1-hour voice cooldown; pattern = escalation to human review. Industry benchmarks show AI moderation can reduce toxic voice exposure by up to 50% and cut response time from 24 hours to 5 seconds *(source to be cited)*.

**Gesture-Based Communication (Non-Verbal Layer):**

- **Contextual gestures:** A radial menu surfaces 4 gestures based on proximity and relationship (e.g., approaching a friend whose visible Mood is low surfaces Comfort, Wave, Ignore, Hug). Strangers see only neutral options (Wave, Nod, Ignore, Clap).
- **Consent:** Touch gestures (Hug, High-Five) between non-friends require acceptance; players can set "Friends only" or "Nobody" for touch gestures.
- **Gesture chaining:** Wave → High-Five → Hug produces a synchronized three-stage animation if both players reciprocate within a 2-second window. This creates a micro-skill ceiling for social bonding.
- **Gesture as status signal:** A player who receives Hug gestures from 50+ *unique qualified givers* in a week earns the "Beloved" title and a cosmetic aura. Status is earned socially, not bought.
  - Qualified giver: account ≥14 days old, not linked to the recipient (device, payment, IP-cluster signals), and counted at most once per week per recipient.
  - Linked-account rings detected by the anti-abuse service void the award.

**Action Cards (Complex Real-Time Performances):**

- **Equip-to-slot system:** 4 Action Card slots per avatar (e.g., Guitar, Dance — Salsa, Cook — Pasta, Skateboard).
- **Co-performance mechanics:** When two players deploy compatible Action Cards within proximity (Guitar + Vocals; Dance + Dance), the system merges them into a Duet Performance with a shared animation timeline, synchronized VFX, and a zone-wide notification ("A duet is happening at the Pier").
- **Monetization:** Action Cards are earnable through mini-games and roleplay scenarios; premium variants are cosmetic reskins (a golden guitar vs. a standard acoustic), never functionally superior. The base card is always accessible via play.

### Pillar 3 — Virtual Economy & Monetization: Player-Driven, Sink-Balanced, Ethical

**Design Principle:** Avakin's economy is first-party-supply and premium-currency-gated. Aetheria's economy is player-driven in supply, dual-currency in design, and sink-balanced by architecture. The lesson from Second Life and IMVU is clear: when players create and trade the goods, engagement and ARPPU both rise.

**Hard rule: there is no path, direct or indirect, from real money to Aether.** Lumen never converts to Aether, never buys anything that produces Aether, and never buys tradeable items. This rule is audited in the quarterly Economy Transparency Report.

**Currency Architecture:**

| Currency | Acquisition | Use | Tradeable? | Real-Money Link |
|---|---|---|---|---|
| **Aether** (soft) | Mini-games, roleplay shifts, daily Sparks, Marketplace sales, opt-in rewarded ads (capped) | Player marketplace purchases, base Action Cards, furniture, apartment upkeep, Creator Studio asset packs | Yes (via marketplace listings) | None. Cannot be bought with real money or converted from Lumen. Non-redeemable. |
| **Lumen** (premium) | Real-money purchase; VIP monthly stipend; rare seasonal rewards | Account-bound cosmetic items (premium SKUs), name changes, extra apartment slots, VIP | No (account-bound) | Direct IAP. Never required for functional progression. Lumen purchases are always account-bound and cannot be listed. |
| **Creator Shards** | Earned by selling player-created items; awarded for top leaderboard placements | Crafting player-made furniture and clothing via the Creator Studio | No — consumed when crafting; the resulting item is tradeable | No direct purchase. |

**The Player-Driven Marketplace:**

- **Listing types:** Fixed-price and timed auction with bid/buyout.
- **Fee structure:** 5% Aether fee on all sales (burned); 3% for VIP sellers. The fee is the primary currency sink — it removes Aether from circulation with every transaction, counteracting faucet inflation.
- **Teen spending caps:** Teen accounts have weekly Aether spend and trade-value caps, and cannot trade directly with Adult accounts outside the marketplace.
- **Creator Studio (UGC Pipeline):** Players design furniture and simple clothing using an in-engine tool with curated asset packs **purchased with Aether**. Approved items enter the marketplace; the creator earns 70% of the Aether sale price, 30% is burned as platform fee and curation cost. The Creator Studio is an economy sink and engagement driver, not a direct revenue line. This mirrors the IMVU model that proved third-party creators can sustain a virtual economy.
- **Anti-RMT safeguards:** Aether is non-redeemable for real currency. All trades are logged; velocity limits, price-outlier detection, and linked-account analysis flag wash trading and value transfer to alts.

**Virtual Real Estate:**

- Every player receives a starter apartment (free, permanent, **no upkeep**). Additional apartments are unlocked with Aether (soft) or Lumen (premium convenience for instant unlock; the apartment itself is account-bound).
- **Apartment tiers:** Studio → Loft → Townhouse → Estate. Higher tiers have more room slots, outdoor spaces, and a storefront slot where the owner can list furniture for sale directly from their home — turning real estate into a commercial asset.
- **Upkeep:** Loft and above carry a weekly Aether upkeep. On non-payment there is **no eviction and no item loss**: the apartment enters "Dormant" — the storefront pauses and party hosting is disabled until upkeep is paid. The starter apartment is always fully usable.
- **No land speculation:** Apartments are not tradeable between players. This prevents the land-rush dynamics that have destabilized other virtual worlds and keeps real estate a consumption sink, not an investment vehicle.

**Inflation Control (Sink-and-Faucet Equilibrium):**

- **Faucets:** Mini-game rewards, daily Sparks, roleplay wages, rewarded ads (capped 3/day), Creator Shard drops.
- **Sinks:** Marketplace fee (5%/3%), apartment upkeep (Aether), Creator Studio asset-pack purchases (Aether), cosmetic repair/refresh fees for Action Card VFX (small, frequent Aether drain), Social Casino house edge, and seasonal Aether burns (limited-time events where donating Aether to a community goal unlocks a server-wide reward).
- **Dynamic tuning:** Live-ops dashboard tracks net Aether flow per player cohort; if circulating Aether exceeds a threshold, the marketplace fee temporarily rises to 6% for 48 hours (communicated transparently as an "Economy Health Adjustment").

### Pillar 4 — World & Locations: Four Biomes, One Persistent Identity

**Design Principle:** Avakin's zones feel like backdrops. Aetheria's zones are social stages with mechanical purpose — each location biases a different interaction type and economy activity.

**Urban Core — "Neon District":**

- **Locations:** Nightclub (The Pulse), rooftop bar (Skyline), coffee house (Brew & Byte), Aether Exchange kiosk, vending-machine alleys, photo booths.
- **Interactive objects:** Aether Exchange kiosk (claim daily Spark, view balances and transaction history, and see the live Economy Health readout — current fee rate, weekly burn total; **no currency conversion**), vending machines (random cosmetic shard for Aether, odds published), photo booth (generates a shareable "Polaroid" with Mood-filtered lighting).
- **Social bias:** High Arousal, high Openness. Proximity voice is the default for Adults; Action Cards lean toward dance and music.

**Nature Escape — "Verdant Reach":**

- **Locations:** Beach (Tidefall), forest clearing (Whisperwood), mountain hot spring.
- **Interactive objects:** Fishing spots (mini-game with Aether reward and a rare furniture-material drop), campfire (Action Card Guitar + Cook co-performance creates a "Campfire Session" with a persistent group buff to Resonance gain), hidden cave (roleplay scenario trigger).
- **Social bias:** Low Arousal, high Valence. Gesture chaining and quiet voice interaction are favored.

**Fantasy Realm — "The Sundered Vale":**

- **Locations:** Elven market, dragon roost, ruined citadel.
- **Interactive objects:** Enchanting altar (cosmetic VFX application for Action Cards), dragon perch (mount interaction that produces a zone-wide flight animation), quest board (solo and co-op roleplay scenarios with Aether and Shard rewards).
- **Social bias:** Roleplay-heavy. Action Cards lean toward magic, crafting, and combat-pose performances. This is the primary Creator Shard faucet via quest completion.

**Private Apartments — "Your Space":**

- **Function:** The economic and social home base. Host parties, display Marketplace storefront, set apartment mood lighting (affects visitors' Mood vectors slightly), and leave async gifts for offline friends.
- **Visiting rules:** Owners choose Open / Friends / Invite-only. Teen apartments are Friends or Invite-only and cannot be visited by Adult non-friends.
- **Monetization:** Additional apartment slots and premium (account-bound) furniture are Lumen sinks; the starter apartment is fully functional and never feels "incomplete."

### Pillar 5 — Mini-Games & Activities: The Engagement Engine

**Design Principle:** Mini-games are not distractions from the social world; they are structured excuses to interact. Every activity produces a social artifact (a score, a performance, a story) that can be shared or competed over.

| Activity | Format | Social Hook | Reward |
|---|---|---|---|
| **Fashion Show** | 90-second timed styling challenge; audience votes live. | Audience uses gesture-based scoring (clap, heart, gasp); contestants see real-time reaction meters. Only votes from qualified, non-linked accounts count toward the result. | Aether + Creator Shard; winner gets a featured spot in Neon District for 24h. |
| **Karaoke** | Note-timing rhythm game with proximity voice integration (singers can opt to use real voice). | Duet mode; audience can "cheer" with gestures to boost score multiplier (per-cheerer cap). | Aether + exclusive microphone Action Card variant. |
| **Roleplay Scenarios** | Instanced 4–8 player scenarios: Hospital shift, Café rush, Police patrol, School day. | Players have assigned roles; success requires coordination via proximity voice and Action Cards. | Aether wages + scenario-specific cosmetic drops. |
| **Social Casino** *(18+, territory-gated)* | No real-money wagering. Players wager Aether (earned soft currency only) on low-stakes games (blackjack, roulette, virtual horse racing). | Spectator mode with gesture reactions; table chat is proximity-voice enabled. | Aether swings with a small house edge (net sink); no Lumen involvement. *Regulatory note: Aether has no purchase path and is non-redeemable; age assurance + per-territory legal review required; zone can be geo-disabled without affecting the core loop.* |
| **Dating Simulation** *(18+ only)* | Opt-in "Spark" compatibility mini-game: two players answer scenario prompts and co-perform an Action Card; compatibility score is revealed. | Produces a shareable "Spark Card" that can be posted to the zone feed (both players must consent to sharing). | Cosmetic "Spark" aura; no Aether reward (prevents farming). |

All mini-games are cross-platform with input abstraction: touch gestures on mobile, mouse/keyboard on PC, and gamepad support. The UI is built natively in UE5's UMG framework so the same windows work across input methods without a web-layer performance penalty.

---

## 4. Monetization Strategy: Revenue Without Resentment

Avakin's monetization is perceived as extractive because the best items are premium-gated and the premium currency is slow to earn without spending. Aetheria's strategy is **cosmetic-first, convenience-second, status-never-sold.**

**Revenue Streams (Target Mix by Year 2):**

| Stream | % of Revenue | Design |
|---|---|---|
| **Lumen IAP** | 53% | Account-bound cosmetic SKUs (premium outfits, hair, VFX), apartment slot expansions, Action Card reskins. No functional power, no exclusive social spaces, no Mood manipulation, no conversion to Aether. |
| **VIP Subscription** ("Aetheria Infinite") | 35% | $9.99/month. Benefits: 500 Lumen monthly stipend, 3% Marketplace fee (vs. 5%), +1 apartment slot, exclusive cosmetic variants (not exclusive item types), priority queue on full instances, unranked practice mode and replay-analysis tool for mini-games, cosmetic leaderboard frame. No extra leaderboard entries; no pay-to-win; convenience and expression only. |
| **Seasonal Pass** ("Aether Pass") | 12% | Free track + premium track ($4.99/season, 6 weeks). Premium track contains cosmetic-only, account-bound rewards and Lumen discounts, never Aether or tradeable items. Free track contains Aether and Shards to keep non-payers engaged. |

*The Creator Studio is intentionally not a revenue line: asset packs are bought with Aether and the 30% platform share is burned. Its value is engagement, supply, and economy stability.*

**Explicitly Rejected Monetization:**

- **No real-money path to Aether**, direct (conversion) or indirect (Lumen-bought tools or items that produce or sell for Aether).
- **No loot boxes with functional items.** Gacha mechanics, if used for cosmetic variants only, must disclose odds and include a pity guarantee; in territories that restrict paid random rewards, they are disabled. Teens cannot buy randomized items with Lumen.
- **No ads interrupting social flow.** Avakin players cite "constant ads" as a major frustration. Aetheria uses opt-in rewarded ads only (watch a 30s ad for a small Aether bonus, capped at 3/day), never between room transitions. No ads to Teens beyond contextual, non-personalized formats.
- **No paywalled social zones.** Every zone is accessible to every player (subject only to age gating). VIPs get queue priority, not exclusivity.
- **No sold status.** No paid leaderboard entries, titles, or social-ranking boosts.

**ARPPU Target:** $9–11 (in line with virtual-world benchmarks). **Conversion target:** 4–6% of MAU, with VIP conversion at 1.5–2%.

*Sanity check: 5% payer conversion × ~$10 ARPPU ≈ $0.50/MAU/month; VIP at 1.8% × $9.99 ≈ $0.18/MAU/month ≈ 36% of revenue, consistent with the 35% target.*

---

## 5. Tech Stack Recommendation

| Layer | Recommendation | Rationale |
|---|---|---|
| **Client Engine** | Unreal Engine 5.4+. **Scalable rendering tiers:** Mobile — UE5 mobile renderer with baked/stationary lighting, card-based hair, HLOD. High-end PC — Lumen GI/reflections, Nanite for environments, strand hair option. | One content pipeline, tiered presentation. UE5's mobile optimization toolchain (Mesh Auto-Instancing, Cull Distance Volumes, ASTC compression) makes 50-player mobile instances viable; Lumen is reserved for hardware that can sustain it. |
| **Server Architecture** | Authoritative server at 20–25 ticks/second, C++ core; UE5 client is a view onto server state. | Prevents client cheating and ensures cross-platform fairness. Proven in UE5 MMO builds that separate simulation from rendering. |
| **Persistence & Queue** | PostgreSQL (durable state) + Redis (hot-path queue between simulation and database). Persistence off the tick. | Keeps simulation responsive under load; mirrors production patterns from UE5 cross-platform MMOs. |
| **Networking / Replication** | Unreal Replication Graph + custom interest management (only replicate avatars and objects within a relevance radius). | Critical for 50+ player instances on mobile bandwidth. |
| **Voice** | Hosted voice SDK (ODIN Voice or equivalent) with server-side forwarding and dynamic proximity rooms; Aiba/GGWP integration for real-time voice toxicity detection. | Avoids building voice from scratch; proven proximity and moderation pipelines. |
| **Web / Trial Client** | UE5 Pixel Streaming via WebRTC for **instant-play trials and web onboarding**, with session-length limits and a hand-off to the native client. | GPU-per-viewer cost makes Pixel Streaming margin-negative as a standing F2P client; used for acquisition, not as the permanent low-end path. Low-end devices are served by the mobile "Performance Mode" tier. |
| **Backend Services** | Go for high-throughput economy and marketplace microservices; Python for live-ops analytics and moderation ML; AWS (EKS, Aurora, ElastiCache, S3) | Go's concurrency model is proven for virtual-world transaction processing at scale *(Avakin migration claim to be cited)*. |
| **Age Assurance** | Third-party age-estimation / ID provider + platform age signals; age bracket stored as a server-authoritative account attribute. | Gates 18+ features and Teen/Adult instance separation. |
| **Moderation** | AI text + voice moderation (Bodyguard.ai, GGWP, or in-house fine-tuned classifier) + human escalation queue. | AI cuts in-session toxicity response to seconds; escalation handles context-sensitive cases. |
| **Analytics** | Amplitude/Mixpanel for funnel, WMSI, and guardrail tracking; Machinations for economy simulation and sink/faucet modeling. | Economy balance must be simulated before live deployment; Machinations is industry-standard for token-sink modeling. |

**Performance Budget (Mobile, 50-player instance):**

- Target: 30 FPS stable on iPhone 13 / Snapdragon 8 Gen 1 equivalent, mobile renderer, no Lumen.
- Draw calls: < 180 per frame via instancing and HLOD.
- Avatar LOD: 4 levels; impostor at >30m. Hair/cloth simulation only on the local avatar and nearest ~8 avatars.
- Voice bandwidth: < 32 kbps per active speaker (Opus codec).
- Instance tick rate: 20 Hz; movement interpolation on client.

---

## 6. Unique Selling Point (USP): What Makes Aetheria Better Than Avakin

1. **The Mood System is an industry-first social-emotional layer.**
   No competitor in the mobile social MMO space has a persistent, socially-driven emotional state that visibly manifests on the avatar — with the player in control of who sees it. Avakin's avatars are static dolls; Aetheria's avatars *feel*. This creates emergent social stories that cannot be replicated by a skin shop.

2. **A player-driven economy that treats players as producers, not consumers.**
   Avakin is first-party supply only. Aetheria's Creator Studio and marketplace turn players into suppliers, which drives engagement (the IMVU/Second Life lesson) while the 5% burn fee controls inflation. Aether is earnable and tradeable; there is no path from real money to Aether. This is the structural fix to the "premium currency ruins everything" problem.

3. **A generational visual leap that scales from phone to high-end PC.**
   Aetheria's UE5 pipeline delivers morph-fitted clothing and physics-driven hair in 50-player zones at a stable 30 FPS on mainstream phones, and Lumen-lit, strand-hair presentation on capable PCs — one world, one content pipeline, the best fidelity each device can sustain.

4. **Moderation and safety are product features, not afterthoughts.**
   Aetheria bakes AI text and voice moderation into the social engine, with transparent escalation, age-separated instances, consent-based touch gestures, and a social credit system that rewards positive interactions (Resonance) and isolates repeat offenders into low-visibility matchmaking pools. Safety is the precondition for the emotional social design to work.

5. **No pay-to-win, ever — and the community can verify it.**
   Every functional item (Action Card base versions, apartment starter, mini-game access) is earnable through play. Lumen buys expression and convenience, never power, status, or social access. The fee structure, sink totals, and the no-real-money-to-Aether rule are published and auditable via a quarterly **Economy Transparency Report** — a trust-building differentiator that no incumbent offers.

---

## 7. Success Metrics & Risk Register

**Key Performance Indicators (Year 1 Targets):**

| Metric | Target | Rationale |
|---|---|---|
| D1 Retention | 42% | Social MMOs with strong customization and daily Sparks benchmark 35–45%. |
| D7 Retention | 22% | Mood system and async social gifts drive return visits. |
| D30 Retention | 12% | VIP conversion and Creator Studio investment create switching costs. |
| WMSI per WAU | 4.2 | North Star (social-only); measured via telemetry on voice, gesture, and Action Card events between non-linked accounts. |
| Economy Participation Rate (guardrail) | 35–55% of WAU | Healthy marketplace without forcing purchases into social flows. |
| VIP Conversion (of MAU) | 1.8% | $9.99/month with cosmetic + convenience benefits. |
| ARPPU | $9–11 | Within virtual-world benchmarks; no whale dependency. |
| Marketplace volume / DAU | 1,200 Aether / day | Aether-denominated; indicates a healthy player-driven economy. Tracked alongside median item price for inflation. |
| Moderation response (P95) | < 10 s in-session; < 24 h human review | Safety is a launch-critical KPI. |

**Top Risks & Mitigations:**

| Risk | Mitigation |
|---|---|
| Mobile thermal/performance throttling with UE5 | Mobile renderer without Lumen; aggressive LOD; simulation limited to nearest avatars; 30 FPS cap on mid-tier devices; "Performance Mode" that reduces avatar bone count and VFX. |
| Pixel Streaming cost | Trial/onboarding only, session-length limits, hand-off to native client; per-session GPU cost tracked against conversion. |
| Minors' safety & age regulation | 13+ minimum; age assurance for 18+ features; Teen/Adult instance separation; Teen defaults (voice off, Mood friends-only, sentiment off); DPIA; COPPA / AADC / DSA review. |
| Emotional-data privacy (Mood) | Sentiment opt-in, no voice input to Mood, coarse storage with retention window, player view/reset, Mood privacy setting, EU AI Act review. |
| Status/reward farming via alts | Unique qualified-giver rules, linked-account detection, per-giver caps on votes and cheers, award voiding. |
| UGC moderation burden (Creator Studio) | Curated asset packs (no free-form mesh upload at launch); AI texture/name screening; human review queue for first-time creators; revenue hold until item passes moderation. |
| Voice chat toxicity | AI real-time transcription + classifier; default push-to-talk on mobile; visible mic halo; progressive discipline ladder; VIPs held to same standard (no "paid immunity"). |
| Economy inflation from mini-game faucets | Dynamic marketplace fee adjustment; seasonal Aether burns; casino house edge; Machinations simulation before each content update; live-ops economy runbook. |
| Regulatory risk on casino mini-games | 18+ with age assurance; Aether-only wagering with no purchase path and no cash-out; legal review per territory; zone can be geo-disabled without affecting core loop. |
| Unsourced market claims | All competitor figures cited to primary sources and legal-reviewed before external circulation. |

---

*Aetheria is not a louder Avakin. It is a more honest one. It bets that the next decade of social virtual worlds belongs to the platform that treats the avatar as an emotional interface, the economy as a commons to be governed, and the player as a citizen rather than a wallet.*

---

## Changelog (v1.0 → v1.1)

Resolves the findings in [`REVIEW.md`](./REVIEW.md):

| # | Finding | Resolution |
|---|---|---|
| 1 | Lumen→Aether ATM contradicted "Aether can't be bought" | ATM replaced by a no-conversion Aether Exchange kiosk; added a hard "no real-money path to Aether" rule. |
| 2 | Creator Studio asset packs priced in Aether *and* Lumen | Packs are Aether-only; Creator Studio removed as a revenue line; mix rebalanced to 53 / 35 / 12. |
| 3 | VIP second leaderboard entry sold status | Replaced with unranked practice mode + cosmetic frame; one ranked entry per player. |
| 4 | No age policy | Added §1.1: 13+, Teen defaults, 18+ gating for Dating Sim and Social Casino, age assurance, instance separation. |
| 5 | Mood privacy and harassment surface | Mood Privacy setting, no vulnerability broadcasting, sentiment opt-in, voice never used for Mood, non-reputational, DPIA. |
| 6 | Farmable status/rewards | Unique qualified givers for "Beloved"; Resonance Crates account-bound; vote/cheer caps; linked-account detection. |
| 7 | North Star required an economy action | North Star is social-only; Economy Participation Rate added as a guardrail. |
| 8 | Unrealistic mobile rendering | Tiered rendering (no Lumen on mobile); card hair on mobile; SKU target 3–5k; USP #3 rewritten. |
| 9 | Pixel Streaming economics | Scoped to trials/onboarding with session limits. |
| 10 | Voice architecture wording | Described as hosted SDK with server-side forwarding. |
| — | Minor items | Apartment upkeep defined (no eviction, "Dormant" state); Creator Shards non-tradeable; ARPPU aligned at $9–11; marketplace KPI in Aether; sourcing notes added; touch-gesture consent added. |
