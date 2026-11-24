# AETHERIA: LIVE YOUR NEXT LIFE

*"Not just a world. Your world, with feeling."*

**GAME DESIGN DOCUMENT — CONFIDENTIAL**

| | |
|---|---|
| Document Version | 1.0 |
| Role | Chief Product Officer & Lead Game Architect |
| Target Platforms | iOS, Android, PC (Windows/macOS), Web (Pixel Streaming) |
| Engine | Unreal Engine 5.4+ |
| Session Cap | 50–75 players per instance |
| Genre | 3D Social Virtual World MMO |
| Model | Free-to-Play with Premium Subscription |

> See [`REVIEW.md`](./REVIEW.md) for an internal-consistency and risk review of this document.

---

## 1. Executive Summary

Avakin Life proved that a persistent 3D social world could sustain over a decade of engagement, reaching 220,000 daily active users in 2025 and surpassing 500 million lifetime downloads. But its legacy is also a cautionary tale: Steam reviews sit at 63% positive, with players citing "heavy monetization," "chat toxicity," and "frequent performance problems" as persistent pain points. The premium currency (Crowns) is widely criticized as "completely ruining the experience," locking the best items behind paywalls that feel insurmountable without real-money spending.

Aetheria is built to inherit Avakin's throne by solving those exact failures. It delivers UE5-fidelity on mobile, a player-driven economy that rewards creativity over spending, an emotion-aware social engine that makes every interaction feel consequential, and a moderation-first architecture that protects the social fabric. The objective is not to be "Avakin with better graphics." It is to be the first social world where the economy, the avatar, and the conversation are all systems of genuine expression, not monetization gates.

**North Star Metric: Weekly Meaningful Social Interactions (WMSI)** — defined as a session with ≥3 proximity interactions (voice, gesture, or Action Card co-performance) and ≥1 economy action (purchase, trade, or listing). Target: **4.2 WMSI per WAU by Month 12.**

---

## 2. Core Gameplay Loop: The Aetheria Session

The loop is engineered for a 12–25 minute mobile session that converts a passive login into a social + economic + expressive cycle, with clear return hooks.

| Step | Player Action | System Response | Retention / Monetization Hook |
|---|---|---|---|
| **1. Arrive** (0–60s) | Login; avatar spawns in Apartment or last social zone. | "Mood" carries over from last session. Proximity voice hums with nearby players. Daily "Spark" reward delivered via a diegetic object (mailbox, phone notification). | Streak-based Spark multiplier (Day 7 = 2×). VIPs get a "Concierge" spawn with a curated social recommendation. |
| **2. Express** (1–3 min) | Open Wardrobe; adjust outfit, hair, body morph, or animation set. | Real-time preview with UE5 Lumen lighting. "Fit Check" button posts a snapshot to a zone-local feed for reactions. | Limited-time "Drop Window" items appear in wardrobe with a soft countdown; not paywalled, but earnable via play or tradeable on the market. |
| **3. Socialize** (3–12 min) | Enter a zone; approach a cluster; use proximity voice, gesture (wave/nod/hug), or deploy an Action Card (guitar, dance, cooking). | Mood system reacts: avatars blush, laugh, or withdraw based on chat sentiment and gesture responses. Action Card co-performance triggers a synchronized animation with nearby players. | Social "Resonance" meter fills with every positive interaction; at full, grants a Resonance Crate containing a cosmetic shard or marketplace credit. |
| **4. Create/Compete** (12–20 min) | Join a Fashion Show, Karaoke room, or roleplay scenario (Hospital shift, Café rush). | Mini-game scores feed into a weekly Creator Leaderboard. Top performers earn "Aether" (tradeable soft currency) and a featured slot in the zone's Hall of Fame. | Leaderboard visibility is the primary status signal; no power is sold, only recognition. VIPs get a second leaderboard entry and a replay-analysis tool. |
| **5. Circulate** (20–25 min) | List an item on the Marketplace, browse player-created furniture, or place a bid on a rare animation set. | Marketplace is fully player-driven; Aetheria takes a 5% transaction fee in Aether, which is burned (removed from economy). | The 5% sink is the primary inflation-control mechanism. VIP sellers pay 3% instead of 5%, a convenience perk, not an exclusive right. |
| **6. Return Hook** | Session ends; avatar enters "Idle Mood" visible to friends. | Push notification: "Mira left you a Resonance gift" or "Your Marketplace listing sold." | Idle Mood and async gifts create a social obligation loop that does not require the recipient to be online simultaneously. |

---

## 3. Feature Breakdown: The Five Pillars

### Pillar 1 — Avatar Customization & the Mood System

**Design Principle:** The avatar is not a mannequin; it is an emotional prosthesis. Customization must be deep enough to make the Mood system legible and socially meaningful.

**Customization Depth:**

- **Body:** Height, musculature, weight distribution, shoulder width, hip ratio, limb length, and 12 face-morph sliders (jaw, cheekbone, brow, nose, lip, eye spacing, etc.). No gender-locked morphs; all sliders are available to all avatars.
- **Hair & Face:** Layered hair with physics-enabled strands (UE5 Chaos), 40+ makeup layers (blush, contour, eyeshadow, lip texture, freckles, scars), and facial hair with density control.
- **Clothing:** 30,000+ launch SKUs across tops, bottoms, outerwear, shoes, accessories, and "Aetherwear" (fantasy/roleplay costumes). Every item is fitted to the body morph, not a static mesh — a critical UE5 technical differentiator against Avakin's rigid garment system.
- **Animations:** Idle sets (confident, shy, playful, brooding), walk styles, dance packs, and Action Card animations that can be equipped to gesture slots.

**The Mood System (Core Innovation):**
Every avatar has a persistent **Mood Vector** with four axes: **Valence** (positive/negative), **Arousal** (calm/excited), **Dominance** (assertive/submissive), and **Social Openness** (receptive/withdrawn). Mood is affected by:

- Chat sentiment (real-time NLP on text; opt-in transcription for voice).
- Gesture reception (a hug received when Openness is low produces a "startled" micro-animation; the same hug at high Openness produces a "melt" animation).
- Environmental context (a dark club raises Arousal; a quiet beach lowers it).
- Action Card co-performance (synchronized guitar duet raises Valence and Dominance for both players).

Mood manifests visibly through idle animation blending, facial expression, posture, and subtle particle effects (a soft glow for high Valence, a slight desaturation for low Valence). Crucially, **Mood is not purchasable.** It is earned through social behavior. This is the ethical line: self-expression is monetizable; emotional state is not.

### Pillar 2 — Social Interaction Engine: Voice, Gesture, and Action Cards

**Design Principle:** Avakin's social layer is text-first and emote-thin. Aetheria's is spatially aware, physically expressive, and co-operative.

**Proximity Voice Chat:**

- Spatial audio with distance-based attenuation, occlusion (walls muffle sound), and reverb profiles per zone (club = tight, echo-heavy; forest = open, diffuse).
- Push-to-talk on mobile (large, repositionable button) and open-mic with VAD (voice activity detection) on PC, with a visible "mic halo" so players know when they are transmitting.
- **Technical approach:** A distributed proxy architecture for audio routing, avoiding the bandwidth scalability problems of pure peer-to-peer and the single-point-of-failure risk of a central server. ODIN Voice or a comparable SDK handles codec, noise suppression, and dynamic group routing based on avatar proximity.
- **Moderation:** Real-time voice transcription feeds an AI toxicity classifier. First offense = in-session mute + warning; repeat = 1-hour voice cooldown; pattern = escalation to human review. Industry benchmarks show AI moderation can reduce toxic voice exposure by up to 50% and cut response time from 24 hours to 5 seconds.

**Gesture-Based Communication (Non-Verbal Layer):**

- **Contextual gestures:** A radial menu surfaces 4 gestures based on proximity and Mood (e.g., approaching a crying avatar surfaces Comfort, Wave, Ignore, Hug).
- **Gesture chaining:** Wave → High-Five → Hug produces a synchronized three-stage animation if both players reciprocate within a 2-second window. This creates a micro-skill ceiling for social bonding.
- **Gesture as economy signal:** A player who receives 50+ Hug gestures in a week earns the "Beloved" title and a cosmetic aura. Status is earned socially, not bought.

**Action Cards (Complex Real-Time Performances):**

- **Equip-to-slot system:** 4 Action Card slots per avatar (e.g., Guitar, Dance — Salsa, Cook — Pasta, Skateboard).
- **Co-performance mechanics:** When two players deploy compatible Action Cards within proximity (Guitar + Vocals; Dance + Dance), the system merges them into a Duet Performance with a shared animation timeline, synchronized VFX, and a zone-wide notification ("A duet is happening at the Pier").
- **Monetization:** Action Cards are earnable through mini-games and roleplay scenarios; premium variants are cosmetic reskins (a golden guitar vs. a standard acoustic), never functionally superior. The base card is always accessible via play.

### Pillar 3 — Virtual Economy & Monetization: Player-Driven, Sink-Balanced, Ethical

**Design Principle:** Avakin's economy is first-party-supply and premium-currency-gated. Aetheria's economy is player-driven in supply, dual-currency in design, and sink-balanced by architecture. The lesson from Second Life and IMVU is clear: when players create and trade the goods, engagement and ARPPU both rise.

**Currency Architecture:**

| Currency | Acquisition | Use | Tradeable? | Real-Money Link |
|---|---|---|---|---|
| **Aether** (soft) | Mini-games, roleplay shifts, daily Sparks, Marketplace sales, Resonance Crates | Player marketplace purchases, base Action Cards, furniture, apartment rent (Aether only) | Yes (via marketplace listings) | No direct purchase. Cannot be bought with real money. |
| **Lumen** (premium) | Real-money purchase; VIP monthly stipend; rare seasonal rewards | Cosmetic-only items (premium SKUs), name changes, extra apartment slots, Marketplace fee reduction (VIP) | No (account-bound) | Direct IAP. Never required for functional progression. |
| **Creator Shards** | Earned by selling player-created items; awarded for top leaderboard placements | Crafting player-made furniture and clothing via the Creator Studio | Yes (bundled into items) | No direct purchase. |

**The Player-Driven Marketplace:**

- **Listing types:** Fixed-price and timed auction with bid/buyout.
- **Fee structure:** 5% Aether fee on all sales (burned); 3% for VIP sellers. The fee is the primary currency sink — it removes Aether from circulation with every transaction, counteracting faucet inflation.
- **Creator Studio (UGC Pipeline):** Players design furniture and simple clothing using an in-engine tool with curated asset packs. Approved items enter the marketplace; the creator earns 70% of the Aether sale price, 30% is burned as platform fee and curation cost. This mirrors the IMVU model that proved third-party creators can sustain a virtual economy.
- **Anti-RMT safeguards:** Aether is non-redeemable for real currency. All trades are logged; velocity limits and pattern detection flag wash trading.

**Virtual Real Estate:**

- Every player receives a starter apartment (free, permanent). Additional apartments are purchased with Aether (soft) or Lumen (premium convenience for instant unlock).
- **Apartment tiers:** Studio → Loft → Townhouse → Estate. Higher tiers have more room slots, outdoor spaces, and a storefront slot where the owner can list furniture for sale directly from their home — turning real estate into a commercial asset.
- **No land speculation:** Apartments are not tradeable between players. This prevents the land-rush dynamics that have destabilized other virtual worlds and keeps real estate a consumption sink, not an investment vehicle.

**Inflation Control (Sink-and-Faucet Equilibrium):**

- **Faucets:** Mini-game rewards, daily Sparks, roleplay wages, Resonance Crates, Creator Shard drops.
- **Sinks:** Marketplace fee (5%/3%), apartment rent (Aether), Creator Studio asset-pack purchases (Aether), cosmetic repair/refresh fees for Action Card VFX (small, frequent Aether drain), and seasonal Aether burns (limited-time events where donating Aether to a community goal unlocks a server-wide reward).
- **Dynamic tuning:** Live-ops dashboard tracks net Aether flow per player cohort; if circulating Aether exceeds a threshold, the marketplace fee temporarily rises to 6% for 48 hours (communicated transparently as an "Economy Health Adjustment").

### Pillar 4 — World & Locations: Four Biomes, One Persistent Identity

**Design Principle:** Avakin's zones feel like backdrops. Aetheria's zones are social stages with mechanical purpose — each location biases a different interaction type and economy activity.

**Urban Core — "Neon District":**

- **Locations:** Nightclub (The Pulse), rooftop bar (Skyline), coffee house (Brew & Byte), ATM bank branch, vending-machine alleys, photo booths.
- **Interactive objects:** ATM (convert Lumen to Aether at a transparent rate, with a daily cap — prevents whale-driven inflation), vending machines (random cosmetic shard for Aether), photo booth (generates a shareable "Polaroid" with Mood-filtered lighting).
- **Social bias:** High Arousal, high Openness. Proximity voice is the default; Action Cards lean toward dance and music.

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
- **Monetization:** Additional apartments and premium furniture are Lumen sinks; the starter apartment is fully functional and never feels "incomplete."

### Pillar 5 — Mini-Games & Activities: The Engagement Engine

**Design Principle:** Mini-games are not distractions from the social world; they are structured excuses to interact. Every activity produces a social artifact (a score, a performance, a story) that can be shared or competed over.

| Activity | Format | Social Hook | Reward |
|---|---|---|---|
| **Fashion Show** | 90-second timed styling challenge; audience votes live. | Audience uses gesture-based scoring (clap, heart, gasp); contestants see real-time reaction meters. | Aether + Creator Shard; winner gets a featured spot in Neon District for 24h. |
| **Karaoke** | Note-timing rhythm game with proximity voice integration (singers can opt to use real voice). | Duet mode; audience can "cheer" with gestures to boost score multiplier. | Aether + exclusive microphone Action Card variant. |
| **Roleplay Scenarios** | Instanced 4–8 player scenarios: Hospital shift, Café rush, Police patrol, School day. | Players have assigned roles; success requires coordination via proximity voice and Action Cards. | Aether wages + scenario-specific cosmetic drops. |
| **Casino** (Social, Not Gambling) | No real-money wagering. Players wager Aether (earned soft currency only) on low-stakes games (blackjack, roulette, virtual horse racing). | Spectator mode with gesture reactions; table chat is proximity-voice enabled. | Aether swings (sink and faucet simultaneously); no Lumen involvement. *Regulatory note: Aether is non-purchasable and non-redeemable; legal review required per territory.* |
| **Dating Simulation** | Opt-in "Spark" compatibility mini-game: two players answer scenario prompts and co-perform an Action Card; compatibility score is revealed. | Produces a shareable "Spark Card" that can be posted to the zone feed. | Cosmetic "Spark" aura; no Aether reward (prevents farming). |

All mini-games are cross-platform with input abstraction: touch gestures on mobile, mouse/keyboard on PC, and gamepad support. The UI is built natively in UE5's UMG framework so the same windows work across input methods without a web-layer performance penalty.

---

## 4. Monetization Strategy: Revenue Without Resentment

Avakin's monetization is perceived as extractive because the best items are Lumen-gated and Lumen is slow to earn without spending. Aetheria's strategy is **cosmetic-first, convenience-second, status-never-sold.**

**Revenue Streams (Target Mix by Year 2):**

| Stream | % of Revenue | Design |
|---|---|---|
| **Lumen IAP** | 45% | Cosmetic SKUs (premium outfits, hair, VFX), apartment expansions, Action Card reskins. No functional power, no exclusive social spaces, no Mood manipulation. |
| **VIP Subscription** ("Aetheria Infinite") | 30% | $9.99/month. Benefits: 500 Lumen monthly stipend, 3% Marketplace fee (vs. 5%), +1 apartment slot, exclusive cosmetic variants (not exclusive item types), priority queue on full instances, replay-analysis tool for mini-games. No pay-to-win; convenience and expression only. |
| **Creator Studio Revenue Share** | 15% | Platform takes 30% of player-created item sales (burned as Aether); 70% to creator. Platform's share is a sink, not a profit center — it stabilizes the economy. Actual revenue comes from Lumen spent on Creator Studio asset packs. |
| **Seasonal Pass** ("Aether Pass") | 10% | Free track + premium track ($4.99/season, 6 weeks). Premium track contains cosmetic-only rewards and Lumen discounts, never Aether or tradeable items. Free track contains Aether and Shards to keep non-payers engaged. |

**Explicitly Rejected Monetization:**

- **No loot boxes with functional items.** Gacha mechanics, if used for cosmetic variants only, must disclose odds and include a pity guarantee; independent research shows pity systems and transparency are essential for ethical retention.
- **No ads interrupting social flow.** Avakin players cite "constant ads" as a major frustration. Aetheria uses opt-in rewarded ads only (watch a 30s ad for a small Aether bonus, capped at 3/day), never between room transitions.
- **No paywalled social zones.** Every zone is accessible to every player. VIPs get queue priority, not exclusivity.

**ARPPU Target:** $8–12 (in line with virtual-world benchmarks). **Conversion target:** 4–6% of MAU, with VIP conversion at 1.5–2%.

---

## 5. Tech Stack Recommendation

| Layer | Recommendation | Rationale |
|---|---|---|
| **Client Engine** | Unreal Engine 5.4+ (Lumen, Nanite for hero assets, Chaos for hair/cloth) | UE5 delivers the visual fidelity gap that Avakin's Unity pipeline cannot close. UE5's cross-platform support and mobile optimization toolchain (Mesh Auto-Instancing, Cull Distance Volumes, ASTC compression) make 50-player mobile instances viable. |
| **Server Architecture** | Authoritative server at 20–25 ticks/second, C++ core; UE5 client is a view onto server state. | Prevents client cheating and ensures cross-platform fairness. Proven in UE5 MMO builds that separate simulation from rendering. |
| **Persistence & Queue** | PostgreSQL (durable state) + Redis (hot-path queue between simulation and database). Persistence off the tick. | Keeps simulation responsive under load; mirrors production patterns from UE5 cross-platform MMOs. |
| **Networking / Replication** | Unreal Replication Graph + custom interest management (only replicate avatars and objects within a relevance radius). | Critical for 50+ player instances on mobile bandwidth. |
| **Voice** | ODIN Voice or equivalent SDK with dynamic audio groups and proximity routing; Aiba/GGWP integration for real-time voice toxicity detection. | Avoids building voice from scratch; proven proximity and moderation pipelines. |
| **Web / Low-End Client** | UE5 Pixel Streaming via WebRTC for browser and low-end mobile users. | Extends reach to Chromebooks, web, and devices below native-client minimum specs without a separate port. WebRTC supports Chrome, Firefox, iOS, and Android browsers. |
| **Backend Services** | Go for high-throughput economy and marketplace microservices; Python for live-ops analytics and moderation ML; AWS (EKS, Aurora, ElastiCache, S3) | Go's concurrency model is proven for virtual-world transaction processing at scale — Avakin itself migrated to a Go-based architecture for millions of daily item sales. |
| **Moderation** | AI text + voice moderation (Bodyguard.ai, GGWP, or in-house fine-tuned classifier) + human escalation queue. | AI cuts in-session toxicity response to seconds; escalation handles context-sensitive cases. |
| **Analytics** | Amplitude/Mixpanel for funnel and WMSI tracking; Machinations for economy simulation and sink/faucet modeling. | Economy balance must be simulated before live deployment; Machinations is industry-standard for token-sink modeling. |

**Performance Budget (Mobile, 50-player instance):**

- Target: 30 FPS stable on iPhone 13 / Snapdragon 8 Gen 1 equivalent.
- Draw calls: < 180 per frame via instancing and HLOD.
- Avatar LOD: 4 levels; impostor at >30m.
- Voice bandwidth: < 32 kbps per active speaker (Opus codec).
- Instance tick rate: 20 Hz; movement interpolation on client.

---

## 6. Unique Selling Point (USP): What Makes Aetheria Better Than Avakin

1. **The Mood System is an industry-first social-emotional layer.**
   No competitor in the mobile social MMO space has a persistent, socially-driven emotional state that visibly manifests on the avatar. Avakin's avatars are static dolls; Aetheria's avatars *feel*. This creates emergent social stories that cannot be replicated by a skin shop.

2. **A player-driven economy that treats players as producers, not consumers.**
   Avakin is first-party supply only — Lockwood creates every item. Aetheria's Creator Studio and marketplace turn players into suppliers, which drives engagement (the IMVU/Second Life lesson) while the 5% burn fee controls inflation. Aether is earnable and tradeable; it cannot be bought with real money. This is the structural fix to Avakin's "Crowns ruin everything" problem.

3. **UE5 fidelity on mobile without the performance tax.**
   Avakin runs on Unity and is criticized for lag and bugs. Aetheria's UE5 pipeline, with mobile-specific LOD, instancing, and cull volumes, delivers Lumen-lit avatars and Chaos-physics hair in a 50-player zone at stable mobile frame rates — a visual and technical leap, not an incremental upgrade.

4. **Moderation is a product feature, not an afterthought.**
   Avakin's toxicity problem is documented. Aetheria bakes AI text and voice moderation into the social engine, with transparent escalation and a social credit system that rewards positive interactions (Resonance) and isolates repeat offenders into low-visibility matchmaking pools. Safety is the precondition for the emotional social design to work.

5. **No pay-to-win, ever — and the community can verify it.**
   Every functional item (Action Card base versions, apartment starter, mini-game access) is earnable through play. Lumen buys expression and convenience, never power or social access. The Marketplace fee structure and Aether non-purchasability are published and auditable via a quarterly **Economy Transparency Report** — a trust-building differentiator that no incumbent offers.

---

## 7. Success Metrics & Risk Register

**Key Performance Indicators (Year 1 Targets):**

| Metric | Target | Rationale |
|---|---|---|
| D1 Retention | 42% | Social MMOs with strong customization and daily Sparks benchmark 35–45%. |
| D7 Retention | 22% | Mood system and async social gifts drive return visits. |
| D30 Retention | 12% | VIP conversion and Creator Studio investment create switching costs. |
| WMSI per WAU | 4.2 | North Star; measured via telemetry on voice, gesture, and economy events. |
| VIP Conversion (of MAU) | 1.8% | $9.99/month with cosmetic + convenience benefits. |
| ARPPU | $9–11 | Within virtual-world benchmarks; no whale dependency. |
| Marketplace GMV / DAU | $1.20 | Indicates a healthy player-driven economy. |

**Top Risks & Mitigations:**

| Risk | Mitigation |
|---|---|
| Mobile thermal/performance throttling with UE5 | Aggressive LOD, 30 FPS cap on mid-tier devices, optional "Performance Mode" that disables Lumen reflections and reduces avatar bone count. Pixel Streaming fallback for low-end devices. |
| UGC moderation burden (Creator Studio) | Curated asset packs (no free-form mesh upload at launch); AI texture/name screening; human review queue for first-time creators; revenue hold until item passes moderation. |
| Voice chat toxicity | AI real-time transcription + classifier; default push-to-talk on mobile; visible mic halo; progressive discipline ladder; VIPs held to same standard (no "paid immunity"). |
| Economy inflation from mini-game faucets | Dynamic marketplace fee adjustment; seasonal Aether burns; Machinations simulation before each content update; live-ops economy runbook. |
| Regulatory risk on casino mini-games | Aether-only wagering, no purchase path to Aether, no cash-out. Legal review per territory; casino zone can be geo-disabled without affecting core loop. |

---

*Aetheria is not a louder Avakin. It is a more honest one. It bets that the next decade of social virtual worlds belongs to the platform that treats the avatar as an emotional interface, the economy as a commons to be governed, and the player as a citizen rather than a wallet.*
