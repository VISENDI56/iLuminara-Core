import requests
import os

PORTS = range(8501, 8520)
def check_nexus_health():
    print("--- iLuminara-Core Integrity Report ---")
    for port in PORTS:
        # Simple check to see if the port is listening
        response = os.system(f"lsof -i:{port} > /dev/null")
        status = "✅ ACTIVE" if response == 0 else "❌ PENDING"
        print(f"Module Port {port}: {status}")

if __name__ == "__main__":
    check_nexus_health()