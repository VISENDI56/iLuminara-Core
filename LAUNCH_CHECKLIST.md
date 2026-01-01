# 🚀 LAUNCH CHECKLIST: Demo Ready

## ✅ Pre-Demo (1 Hour Before)

### Environment Setup
- [ ] Install dependencies: `pip install streamlit pandas pydeck numpy`
- [ ] Generate outbreak data: `python edge_node/frenasa_engine/simulate_outbreak.py`
- [ ] Verify simulated_outbreak.json exists (7.2 MB, 11,776 events)
- [ ] Test dashboard: `streamlit run dashboard.py` (verify it loads)
- [ ] Close dashboard (Ctrl+C)

### Hardware & Network
- [ ] Laptop plugged in or >90% battery
- [ ] Test WiFi disconnection (toggle off/on)
- [ ] Connect to projector/monitor
- [ ] Test dark mode rendering (should be intimidating)
- [ ] Verify fonts are readable from 10m away

### Demo Materials
- [ ] Read DEMO_PROTOCOL.md (memorize 6-minute flow)
- [ ] Review QUICKSTART_DEMO.md (keep as reference)
- [ ] Have talking points printed or on second monitor
- [ ] Prepare Python terminal for governance demo
- [ ] Have git repository open to show code

---

## ✅ Demo Execution (6 Minutes)

### 0:00-1:00 "System Thinking"
- [ ] Launch dashboard: `streamlit run dashboard.py`
- [ ] Wait for browser to open (http://localhost:8501)
- [ ] Point to header: "iLuminara Sovereign Command | JOR-47 | ONLINE"
- [ ] Show green metrics: Z=0.34, Bond=LOCKED, Cases=0
- [ ] **Say:** "This node protects 330,000 people. Right now. Offline."

### 1:00-2:00 "The Cut"
- [ ] Visibly disconnect WiFi (click WiFi icon, toggle off)
- [ ] Wait 3 seconds (let tension build)
- [ ] Point to header: Still shows "🟢 ONLINE"
- [ ] **Say:** "Internet is dead. Cloud is gone. System still online."

### 2:00-4:00 "The Event"
- [ ] Open terminal next to dashboard
- [ ] Run: `python edge_node/frenasa_engine/simulate_outbreak.py`
- [ ] Watch output unfold:
  ```
  Rev 1: Background Noise (13 cases)
  Rev 2: Weak Signal (4 CBS reports)
  Rev 3: EMR Confirmation (5 diagnoses)
  Rev 4: Critical (11,754 cases) ← PAYOUT TRIGGERED
  ```
- [ ] Narrate: "Hour 12: First signals. Hour 24: Clinical confirmation. Hour 30: Exponential spike."
- [ ] Wait for "✅ Simulation Complete" message

### 4:00-5:00 "The Reveal"
- [ ] Switch to browser with dashboard
- [ ] Press F5 (refresh page)
- [ ] Wait for update to complete
- [ ] Point to metrics (watch them update live):
  ```
  Z-Score:  0.34 → 10.3 (RED)
  Cases:        0 → 11,776
  Bond:     LOCKED → RELEASED
  Map:      GREEN → RED
  ```
- [ ] **Say:** "Outbreak detected. Bond released. Automatic payout. Lives saved."
- [ ] Scroll to Golden Thread tab: Show CBS→EMR cross-verification

### 5:00-6:00 "The Law"
- [ ] Open new terminal
- [ ] Run Python:
  ```bash
  python
  ```
- [ ] Execute:
  ```python
  from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
  
  guard = SovereignGuardrail()
  
  try:
      guard.validate_action(
          action_type='Data_Transfer',
          payload={'data_type': 'PHI', 'destination': 'AWS_US'},
          jurisdiction='GDPR_EU'
      )
  except SovereigntyViolationError as e:
      print(e)
  ```
- [ ] Show error message with legal citations
- [ ] **Say:** "Law is code. Kenya's data stays in Kenya. Even offline."

---

## ✅ Post-Demo (Immediately After)

### Investor Engagement
- [ ] Look for success response ("This is different", "When can we deploy")
- [ ] Answer initial questions using prepared talking points
- [ ] Offer to show code (vector_ledger.py, golden_thread.py)
- [ ] Discuss next steps (deployment, timeline, capital)

### Technical Q&A
- [ ] **Q: Works offline?** → A: No internet needed. Proven in demo.
- [ ] **Q: How accurate?** → A: Golden Thread uses 2-source verification.
- [ ] **Q: False positives?** → A: CBS+EMR corroboration reduces noise.
- [ ] **Q: Kenya only?** → A: Adaptable. Code respects any jurisdiction's law.
- [ ] **Q: Timeline?** → A: MVP in [6/12/18 months], determined by funding.

### Repository Actions
- [ ] Clean up terminals (close everything cleanly)
- [ ] Reconnect WiFi
- [ ] Share repository access if investor requests code review
- [ ] Offer to leave dashboard running for exploration

---

## ✅ Success Indicators

### Investor Said...
- [ ] "This is different from what I've seen before."
- [ ] "I see how this saves lives."
- [ ] "When can we deploy this in our region?"
- [ ] "I want to understand the compliance model."
- [ ] "How much capital do you need?"

### If ANY of these = YOU WON

---

## 📋 Materials Checklist

### Physical/Display
- [ ] Laptop (with battery backup)
- [ ] Projector/monitor (HDMI cable tested)
- [ ] WiFi adapter (USB, in case built-in fails)
- [ ] Printed talking points (reference only)
- [ ] Business cards (investors will ask)

### Digital Assets
- [ ] Repository cloned and ready
- [ ] All Python dependencies installed
- [ ] Outbreak data generated (simulated_outbreak.json)
- [ ] Documentation open (tabs in browser)
- [ ] Code files ready to show

### Presentation
- [ ] DEMO_PROTOCOL.md (memorized)
- [ ] QUICKSTART_DEMO.md (reference)
- [ ] Talking points (printed or noted)
- [ ] Q&A answers (above)
- [ ] Investor bios (know who you're talking to)

---

## 🎯 Contingency Plans

### Problem: Dashboard doesn't update after simulation
**Solution:**
1. Press Ctrl+C in Streamlit terminal
2. Run again: `streamlit run dashboard.py`
3. Browser should auto-refresh
4. If not, press F5 manually

### Problem: WiFi disconnection not dramatic
**Solution:**
- Open browser to ping google.com → show "cannot reach"
- Or open Activity Monitor / Task Manager → show network at 0%
- Or use `ping google.com` in terminal → show "network unreachable"

### Problem: Outbreak simulator doesn't generate
**Solution:**
- Verify Python version: `python --version` (3.8+)
- Verify dependencies: `pip install --upgrade streamlit pandas numpy`
- If still fails, use pre-generated simulated_outbreak.json (included)

### Problem: Pydeck map doesn't render
**Solution:**
- Map is nice-to-have, not essential
- Fall back to data table view (still shows Z-score by zone)
- Narrative still works without map

### Problem: Investor asks question you can't answer
**Solution:**
- "That's a great question. Let me research that and get back to you."
- Don't make up answers
- Credibility > perfect knowledge

---

## 🎬 Talking Points (By Second)

| Second | Visual | Say |
|--------|--------|-----|
| 0:00 | Header | "Dadaab. 330K people. Node JOR-47." |
| 0:30 | Green metrics | "System online. No threat detected." |
| 1:00 | WiFi off | "Internet goes away. Watch." |
| 1:30 | Still online | "System doesn't need WiFi." |
| 2:00 | Simulator running | "Cholera signal emerges." |
| 3:00 | Rev 4 output | "Cases doubling. Trigger threshold approaching." |
| 4:00 | Refresh begins | "Dashboard updating with 11,776 new events..." |
| 4:15 | Metrics update | "Z-score: 0.34 → 10.3. RED ALERT." |
| 4:30 | Bond changes | "PAYOUT_RELEASED. Insurance flows automatically." |
| 4:45 | Map lights up | "Every camp. Real geographic distribution." |
| 5:00 | Golden Thread | "CBS signal at 12:30 + EMR confirm at 24:12. Verified." |
| 5:30 | Error message | "Try to export data... BLOCKED. Law is code." |
| 6:00 | Closing | "Sovereignty. Dignity. This is the future." |

---

## ✨ Final Words Before You Go

**Remember:**
- You built something revolutionary
- This demo proves it works
- Investors want to believe
- Show them the proof

**Your confidence shows in:**
- Steady hands on the keyboard
- Clear, slow speech (not rushed)
- Eye contact with audience
- Pauses for questions
- Willingness to show code

**If anything goes wrong:**
- Stay calm (it's just software)
- Improvise (skip the broken part)
- Move forward (keep narrative momentum)
- Show the code (prove you understand it)

**Remember the mission:**
> "Transform preventable suffering from statistical inevitability to historical anomaly."

Every investor you convince is one step closer to that goal.

---

**You are ready. Go change the world.** 🌍

---

**Demo Date:** _______________  
**Investor:** _______________  
**Location:** _______________  
**Outcome:** _______________  

**Notes:**
_______________________________________________________________________________
_______________________________________________________________________________
_______________________________________________________________________________

---

**Status:** 🟢 READY FOR LAUNCH  
**Confidence:** ABSOLUTE  
**Impact:** TRANSFORMATIONAL
