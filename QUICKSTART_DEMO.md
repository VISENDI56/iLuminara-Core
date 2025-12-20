# 🚀 QUICK START: War Room Demo (5 Minutes)

> **The invisible made visible. The system thinking. Right now.**

## Prerequisites (Run Once)

```bash
# Install dependencies
pip install streamlit pandas pydeck numpy

# Generate outbreak data (72-hour Cholera simulation)
python edge_node/frenasa_engine/simulate_outbreak.py
# Output: simulated_outbreak.json (7.2 MB, 11,776 events)
```

## Launch the Full War Room Suite

### Option 1: Auto-Launch (Recommended)
```bash
./launch_war_room.sh
```

This single command will:
1. Generate fresh outbreak data
2. Start all three dashboards
3. **Automatically open all dashboards in Chrome**

### Option 2: Manual Launch (Single Dashboard)
```bash
streamlit run dashboard.py
```

**Browser opens to:**
```
http://localhost:8501
```

## The Demo Sequence

### ✅ Step 1: Show Online Status (1 min)
- Dashboard header shows "🟢 ONLINE"
- Z-Score: 0.34 (GREEN)
- Bond Status: LOCKED
- **Say:** *"System running. Everything normal."*

### ✅ Step 2: Disconnect WiFi (1 min)
- Click WiFi off on your laptop
- Point to header: Still shows "🟢 ONLINE"
- **Say:** *"The internet is gone. System still protecting the camp."*

### ✅ Step 3: Generate Outbreak (2 min)
- Open terminal next to dashboard
- Run: `python edge_node/frenasa_engine/simulate_outbreak.py`
- Watch output as simulation progresses:
  ```
  Phase 1: Background Noise (13 cases)
  Phase 2: Weak Signal (4 CBS reports)
  Phase 3: EMR Confirmation (5 diagnoses)
  Phase 4: Critical Spike (11,754 cases) ← PAYOUT TRIGGERED
  ```

### ✅ Step 4: Refresh Dashboard (1 min)
- Press F5 in browser
- Watch metrics UPDATE LIVE:
  ```
  Current Z-Score: 10.3 (WAS 0.34) → RED
  Cases: 11,776 (WAS 0)
  Bond Status: PAYOUT_RELEASED → RED
  Map: Dadaab hexagons turn RED
  ```

### ✅ Step 5: Show the Law (Optional, but powerful)
```bash
# Open Python terminal
python
```

```python
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

guard = SovereignGuardrail()

# Try to export health data to AWS during blackout
try:
    guard.validate_action(
        action_type='Data_Transfer',
        payload={'data_type': 'PHI', 'destination': 'AWS_US'},
        jurisdiction='GDPR_EU'
    )
except SovereigntyViolationError as e:
    print(e)
    # Output: ❌ SOVEREIGNTY VIOLATION + legal citations
```

**Say:** *"Even offline, even if internet came back, this system would REFUSE to export data to foreign clouds. The law is written in code."*

## The Narrative

| Time | What's Happening | What You Say |
|------|-----------------|-------------|
| 0:00 | Dashboard shows green status | "System online. Dadaab protected." |
| 1:00 | WiFi off, system still online | "No internet. No problem." |
| 2:00 | Outbreak simulation running | "Hour 0-12: Normal patterns. Hour 12: First signals..." |
| 4:00 | Dashboard updates RED | "Z-score hit 4.2. Bond released. Lives saved." |
| 4:30 | Show governance enforcement | "Data stays in Kenya. Always. The law is the code." |

## Files You're Showing

| File | Purpose | Size |
|------|---------|------|
| `dashboard.py` | Streamlit dark-mode console | 520 lines |
| `simulate_outbreak.py` | 72h Cholera outbreak generator | 514 lines |
| `simulated_outbreak.json` | Generated data (11,776 events) | 7.2 MB |
| `vector_ledger.py` | Legal framework enforcement | 330 lines |
| `golden_thread.py` | Data fusion engine | 505 lines |
| `DEMO_PROTOCOL.md` | Full 15-min demo script | 464 lines |

## Key Visual Moments (Photograph These)

1. **Header**: "iLuminara Sovereign Command | Node: JOR-47 | Status: ONLINE"
2. **Metrics Going Red**: Z-Score jumping from 0.34 to 10.3
3. **Map Lighting Up**: Dadaab hexagons turning red
4. **The Bond Trigger**: "PAYOUT_RELEASED" in red
5. **Your Face Next to Projector**: Pointing at the live system

## Troubleshooting (30 seconds)

| Problem | Solution |
|---------|----------|
| "simulated_outbreak.json not found" | Run: `python edge_node/frenasa_engine/simulate_outbreak.py` |
| Dashboard doesn't update after simulation | Press F5 or restart Streamlit |
| Map not rendering | Data is still there, just shown as table |
| Z-score too low | Make sure simulation completed (max should be >4) |

## Extended Q&A (If Investors Ask)

**Q: Can this work offline?**
> A: Yes. Everything you're watching is running locally on this laptop. No cloud. No internet.

**Q: How accurate is this?**
> A: The outbreak pattern is realistic. The Z-score algorithm is standard epidemiology. In production, we'd use 5 years of historical baseline data.

**Q: What about false alarms?**
> A: The Golden Thread requires CBS + EMR corroboration. Two independent sources agreeing = high confidence.

**Q: Why Kenya?**
> A: Because Dadaab refugee camp (330K people) has cholera risk, minimal cloud infrastructure, and Kenya DPA compliance requirements that demand data sovereignty.

## Next Steps After Demo

1. **Stop Streamlit**: Ctrl+C
2. **Reconnect WiFi**
3. **Take questions** (you've got code to back every claim)
4. **Discuss deployment**: Kenya EMR integration, government adoption, timeline
5. **Collect leads**: "When's this ready?" = "That investor is serious."

---

## 🎯 Success Criteria

Investors will say one of these:

- ✅ *"This is different. Show me more."*
- ✅ *"When can we deploy this in [our region]?"*
- ✅ *"How much capital do you need?"*
- ✅ *"I want to understand the compliance model better."*

**If they say any of those = you won.**

---

## 🌍 Mission Reminder

> *"Transform preventable suffering from statistical inevitability to historical anomaly."*

**This demo is proof that it's possible. The code is the blueprint. The investors are the fuel.**

**Go.**

---

**Status**: Ready for Live Demonstration  
**Last Tested**: December 13, 2025  
**Confidence**: 🟢 MAXIMUM
