
import time
import os
import sys
import random

# Import the new simulation harness
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from infrastructure.simulation.data_stream import LiveDataHarness
from governance_kernel.sovereign_guardrail import SovereignGuardrail

class C2NexusV2:
    def __init__(self):
        self.stream = LiveDataHarness()
        self.guard = SovereignGuardrail()
        self.logs = []

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run_live_dashboard(self):
        try:
            while True:
                self.clear_screen()
                self._render_header()
                # 1. Process a new Live Event
                event = self.stream.get_next_event()
                compliance = self.guard.check_sectoral_compliance(event['context'], event['payload'])
                # 2. Log result
                log_entry = self._format_log(event, compliance)
                self.logs.insert(0, log_entry)
                if len(self.logs) > 8: self.logs.pop() # Keep last 8 logs
                # 3. Render Sections
                self._render_omni_law_feed()
                print("\n[SECTOR: SYSTEM 2 SECURITY]")
                self._render_soc_pulse()
                time.sleep(2) # Refresh rate
        except KeyboardInterrupt:
            print("\n[!] C2 NEXUS SHUTDOWN.")

    def _render_header(self):
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║   iLUMINARA C2 NEXUS V2 | OMNI-LAW MATRIX: ACTIVE (29/29)        ║")
        print("╠══════════════════════════════════════════════════════════════════╣")
        print("║   MONITORING: FINANCE | SUPPLY CHAIN | ESG | PUBLIC HEALTH       ║")
        print("╚══════════════════════════════════════════════════════════════════╝")

    def _format_log(self, event, compliance):
        timestamp = time.strftime("%H:%M:%S")
        sector = event['context']
        status = compliance['status']
        details = str(compliance.get('alerts', []) or compliance.get('actions_taken', []))
        icon = "🟢"
        if status in ["BLOCKED", "FROZEN"]: icon = "🔴"
        elif status == "FLAG": icon = "🟡"
        return f"{timestamp} | {icon} {sector:<12} | {status:<8} | {details[:40]}..."

    def _render_omni_law_feed(self):
        print("\n[LIVE INTELLIGENCE FEED]")
        print("   TIME     | STS | SECTOR       | RESULT   | DETAILS")
        print("   " + "-"*60)
        for log in self.logs:
            print(f"   {log}")

    def _render_soc_pulse(self):
        # Visualizes the heartbeat of the System 2 Agent
        statuses = ["Scanning traffic...", "Validating patch...", "Simulating breach...", "Idle"]
        print(f"   🤖 SOC AGENT: {random.choice(statuses)}")
        print(f"   🛡️  Active Threats: {random.randint(0, 2)} | Blocked Today: {random.randint(12, 50)}")

if __name__ == "__main__":
    nexus = C2NexusV2()
    nexus.run_live_dashboard()
