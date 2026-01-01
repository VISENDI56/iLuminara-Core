# VISUAL ARSENAL

Purpose: A single-page cheat sheet for the founder to deliver the Doha demo flawlessly.

**THE ONE COMMAND:**

Run the full demo (generates data and launches HUDs):

```bash
./launch_war_room.sh
```

**THE 4-STEP NARRATIVE:**

1. Calm — Baseline: All KPIs Green, system idle; visuals show stable green map and low alert rate.
2. Cut — Early Signal: Golden Thread anomalies appear; KPI flicker to yellow; explain brief model uncertainty.
3. Trigger — Confirmed Alert: Precision alert transmits (4.2s shown); dashboard flips Red; transparency view and field form pop for human validation.
4. Payout — Response & Audit: Field validation recorded, legal ledger updated, visuals move from Red → Green as containment metrics recover.

Visual cue mapping: Green → Yellow → Red (Calm → Cut → Trigger → Payout).

**GOVERNANCE TALKING POINTS:**

- **GDPR Art. 9 (Special categories):** We process sensitive health data only under strict lawful bases and implement purpose-limiting technical controls.
- **KDPA (Sovereign Data Protection):** Enforced via SovereignGuardrail policy engine and local ledgering to keep data under national control.
- **HIPAA (Operational Privacy):** Technical and administrative safeguards for handling PHI; auditing and field validation provide breach detection and mitigation.

Note: mention SHAP transparency during clinical validation to highlight interpretability for care teams.

**THE FAILURE SCENARIO:**

If the dashboard crashes, restart sequence:

1. Stop current run (if running in foreground): press Ctrl+C
2. From the project root re-launch the dashboard:

```bash
streamlit run dashboard.py
```

If you need to restart the whole demo (regenerates data and launches everything):

```bash
./launch_war_room.sh
```

**KEY METRIC EXPLANATIONS (one-liners):**

- **Z-Score:** A standardized score indicating how many standard deviations a current observation lies from the historical mean — used to quantify anomaly severity.
- **Golden Thread:** The end-to-end provenance trail that links raw sensor events through model inferences to governance decisions and legal ledger entries.
- **Parametric Bond:** A financial instrument construct used here as a notional risk-transfer primitive whose payout is triggered by verifiable parametric alerts from the system.

— End of cheat sheet —
# 🎭 War Room Demo: The Visual Arsenal

## The Three Components

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│              iLuminara Sovereign Command Console                │
│         (What Investors See on the Projector Screen)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           ▲
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐   ┌───────▼────────┐  ┌────▼─────┐
    │          │   │                │  │           │
    │Dashboard │   │ Outbreak Data  │  │  Demo     │
    │          │   │                │  │ Protocol  │
    │(Showing) │   │ (What's Being  │  │(How to    │
    │          │   │  Simulated)    │  │Show it)   │
    └──────────┘   └────────────────┘  └───────────┘
    Streamlit      SimulatedOutbreak    War Room
    (520 lines)    (514 lines)          Script
                                        (464 lines)
```

---

## 1. 🔬 The Outbreak Simulator

**File:** `edge_node/frenasa_engine/simulate_outbreak.py`

### What It Does
Generates a realistic 72-hour cholera outbreak timeline in Dadaab refugee camp.

### The 4-Phase Progression

| Phase | Hours | Events | What's Happening | Z-Score |
|-------|-------|--------|------------------|---------|
| **Background** | 0-12 | 13 | Normal illness patterns | 0.1-0.5 |
| **Weak Signal** | 12-24 | 4 CBS + context | First watery stool reports | 0.5-1.2 |
| **EMR Confirm** | 24-30 | 5 diagnoses | Clinical confirmation begins | 1.2-2.0 |
| **Critical** | 30-72 | 11,754 cases | Exponential spread | 2.0-10.3 |

### Output
```json
{
  "simulation_metadata": {
    "location": "Dadaab Refugee Complex, Kenya",
    "pathogen": "Vibrio cholerae",
    "total_events": 11776,
    "zones": ["Ifo Camp", "Hagadera Camp", "Dagahaley Camp", "Kambios"]
  },
  "events": [ ... 11,776 CBS/EMR signals ... ],
  "z_score_timeline": [ ... hourly Z-scores ... ],
  "parametric_bond_trigger": {
    "status": "PAYOUT_RELEASED",
    "current_max_z_score": 10.3
  }
}
```

### Run It
```bash
python edge_node/frenasa_engine/simulate_outbreak.py
# Output: simulated_outbreak.json (7.2 MB)
```

---

## 2. 📊 The Command Console Dashboard

**File:** `dashboard.py`

### Architecture
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  ⚡ iLuminara Sovereign Command | JOR-47 | ONLINE     │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Current Z-Score: 10.3 ● Z: 4.2 △  Cases: 11,776    │
│  Bond Status: PAYOUT_RELEASED ⚠️                       │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│              🗺️ Hexagon Map (Dadaab Zones)            │
│                                                        │
│         [RED]  [ORANGE]  [YELLOW]  [GREEN]           │
│       Hagadera  Ifo     Dagahaley   Kambios          │
│       (312)     (247)    (189)      (45)             │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Tabs: [ Timeline ] [ Golden Thread ] [ Alerts ] [ ⚖️ ]│
│                                                        │
│  📈 Z-Score Rising         🔗 CBS → EMR Fusion       │
│  ────────────────          ────────────────────      │
│  [Chart goes from          12:30 ○ ──→ 24:12 ▮      │
│   0 to 10 over 72h]        13:12 ○ ──→ 25:30 ▮      │
│                            14:48 ○ ──→ 27:06 ▮      │
│                                                        │
├────────────────────────────────────────────────────────┤
│  ✓ GDPR  ✓ KDPA  ✓ HIPAA  ✓ Kenya DPA                │
│  14/14 Frameworks Active | 100% Auditable             │
└────────────────────────────────────────────────────────┘
```

### The 5 Visualization Layers

1. **Header** — Node status, uptime, compliance
   ```
   ⚡ iLuminara Sovereign Command | Node: JOR-47 (Dadaab) | Status: 🟢 ONLINE
   ```

2. **Metrics** — Real-time indicators
   ```
   Current Z-Score: 10.3  |  Peak Z: 10.3  |  Cases: 11,776  |  Bond: RELEASED
   ```

3. **Map** — Geographic hexagon layer
   ```
   Dadaab zones color-coded by Z-score:
   • Green (Z < 1): Normal
   • Yellow (1 < Z < 2.576): Watch
   • Orange (2.576 < Z < 4): Alert
   • Red (Z > 4): Critical
   ```

4. **Timeline** — Z-score progression
   ```
   X-axis: Hours (0-72)
   Y-axis: Z-score (0-12)
   Curve shows: Flat → Exponential spike at hour 30
   ```

5. **Golden Thread** — CBS → EMR fusion
   ```
   [📡 CBS Signal] → [✓] → [📋 EMR Confirmation]
   Score: 1.0 (CONFIRMED)
   ```

### Run It
```bash
streamlit run dashboard.py
# Opens: http://localhost:8501
```

### What Investors See
- **First Load**: Green metrics, normal status
- **After Simulation**: Red metrics, exponential curve, map lighting up
- **Offline**: System still running, no internet needed
- **Gold**: Cross-source verification proving the outbreak is real

---

## 3. 🎭 The Demo Protocol

**File:** `docs/DEMO_PROTOCOL.md`

### The Narrative Arc

**MINUTE 0-1: "System Thinking"**
- Dashboard shows green status
- Z-score: 0.34 (normal)
- Bond: LOCKED (no payout)
- **Narration:** "This node protects 330,000 people in a refugee camp."

**MINUTE 1-2: "The Cut"**
- Turn off WiFi (visibly, on camera)
- System still shows ONLINE
- **Narration:** "Internet is dead. Cloud is gone. Watch what happens."

**MINUTE 2-4: "The Event"**
- Run outbreak simulator in terminal
- Watch 4 phases unfold:
  ```
  ✓ Rev 1: 13 background cases
  ✓ Rev 2: 4 CBS weak signals
  ✓ Rev 3: 5 EMR confirmations
  ✓ Rev 4: 11,754 critical cases
  ```
- **Narration:** "Hour 12: First reports. Hour 24: Confirmation. Hour 30: Spike."

**MINUTE 4-5: "The Reveal"**
- Refresh dashboard
- Watch live updates:
  ```
  Z-Score:  0.34 → 10.3  (RED)
  Cases:        0 → 11,776
  Bond:     LOCKED → RELEASED
  Map:      GREEN → RED
  ```
- **Narration:** "Outbreak detected. Bond released. Automatic payout. No bureaucracy."

**MINUTE 5-6: "The Law"**
- Open Python terminal
- Try to export health data to AWS:
  ```python
  guard.validate_action(
      action_type='Data_Transfer',
      payload={'data_type': 'PHI', 'destination': 'AWS_US'},
      jurisdiction='GDPR_EU'
  )
  # ❌ BLOCKED: Violates GDPR Art. 9 + Kenya DPA §37 + HIPAA §164.312
  ```
- **Narration:** "Even offline, data sovereignty is enforced. Law is code."

### Success Metrics
Investors will say:
- ✅ *"This is different."*
- ✅ *"When can we deploy this?"*
- ✅ *"How much capital do you need?"*
- ✅ *"Can you do this in [my region]?"*

---

## 4. 📋 Quick Start Guide

**File:** `QUICKSTART_DEMO.md`

### 3-Step Launch
```bash
# 1. Install dependencies
pip install streamlit pandas pydeck numpy

# 2. Generate outbreak (11,776 events)
python edge_node/frenasa_engine/simulate_outbreak.py

# 3. Launch dashboard
streamlit run dashboard.py
```

### Timeline
| Min | What | Visual |
|-----|------|--------|
| 0-1 | Show normal system | Green dashboard |
| 1-2 | Disconnect WiFi | Still online |
| 2-4 | Run simulation | Terminal output |
| 4-5 | Refresh dashboard | RED everywhere |
| 5-6 | Show governance | Error message |

---

## 🎯 Key Talking Points (By Second)

| Second | Slide | Say |
|--------|-------|-----|
| 0:00 | Header | "Dadaab refugee camp. 330,000 people. No internet." |
| 0:30 | Green metrics | "System online. Z-score normal. No threat." |
| 1:00 | WiFi off | "Watch. The internet is going away." |
| 1:30 | Still online | "System still running. No cloud. No internet." |
| 2:00 | Run simulator | "Cholera outbreak. Starting now." |
| 3:00 | Rev 4 | "Cases doubling. Z-score rising. Insurance trigger." |
| 4:00 | Refresh | "Z-score 10.3. Bond released. Lives saved." |
| 4:30 | Map red | "Every camp has cases. Automatic response." |
| 5:00 | Governance | "Try to export data to foreign cloud..." |
| 5:30 | Blocked | "BLOCKED. Kenya's law. Respected offline." |
| 6:00 | Closing | "Sovereignty. Dignity. This is the future." |

---

## 📸 Moments to Photograph

1. **You pointing at header** — "iLuminara Command Console | ONLINE"
2. **Metrics going RED** — Z-score jumping from 0.34 to 10.3
3. **Map lighting up** — Hexagons turning red across Dadaab
4. **The bond trigger** — "PAYOUT_RELEASED" in big red letters
5. **The error message** — "Violates GDPR Art. 9 + Kenya DPA §37"
6. **Your face next to projector** — Pointing at live system, confident

---

## 🎬 Production Quality

### Dark Mode Aesthetics
- Background: `#0a0e27` (deep space black)
- Accent: `#00ff88` (neon green, sovereignty)
- Alert: `#ff3366` (warning red, action required)
- Fonts: Monospace (Courier New), tech look

### Projector Optimization
- 16pt+ fonts (readable from 10m away)
- High contrast (green on black)
- No small text (investors must see numbers)
- Full-screen mode (no UI distractions)

### Interactivity
- Tabs allow exploring without restarting
- Real-time metrics update
- Slider to move through timeline
- Click hexagons for zone details

---

## 🔄 The Data Flow

```
┌─────────────────────────────┐
│ simulate_outbreak.py        │
│ (514 lines)                 │
│ Generates 11,776 events     │
│ Over 72 hours               │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ simulated_outbreak.json     │
│ (7.2 MB)                    │
│ Ground truth data           │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ dashboard.py                │
│ (520 lines)                 │
│ Reads JSON                  │
│ Renders in Streamlit        │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ Browser at :8501            │
│ Dark-mode command console   │
│ Ready for investors         │
└─────────────────────────────┘
```

---

## ✨ Why This Works

1. **It's LIVE**
   - Not a recording or mockup
   - Actual code running in real-time
   - Investors trust what they see

2. **It's OFFLINE**
   - Proves no cloud dependency
   - Demonstrates edge-first architecture
   - Shows local sovereignty

3. **It's DRAMATIC**
   - WiFi off → system still working
   - Quiet normal → sudden RED crisis
   - Shows detection speed

4. **It's EXPLAINABLE**
   - Data fusion shown side-by-side
   - Legal enforcement demonstrated
   - No magic, just code

5. **It's REPEATABLE**
   - Same demo every time
   - Works on any laptop
   - No network required

---

## 🚀 You're Ready

Three commands:
```bash
python edge_node/frenasa_engine/simulate_outbreak.py
streamlit run dashboard.py
# Show investors the future
```

One narrative:
> "The internet is dead. The cloud is gone. But the sovereign intelligence is still protecting the camp."

One outcome:
> "Lives saved. Authority protected. Dignity respected. Let's build this together."

---

**Status**: War Room Deployment Ready  
**Last Tested**: December 13, 2025  
**Confidence**: 🟢 MAXIMUM  
**Impact**: Game-changing
