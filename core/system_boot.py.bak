import sys
import os
import subprocess
import google.protobuf
from core.security.visendi_dna import SovereignDNA
from core.security.integrity_monitor import verify_iron_dome_v2, verify_license_compliance

def enforce_security_patch():
    """
    Enforces the Protobuf recursion fix at the environment level.
    """
    # Force C++ implementation if available for performance and safety
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "cpp"
    
    # Check version explicitly
    pb_ver = google.protobuf.__version__
    if pb_ver < "4.25.8":
        print(f"[!] SECURITY ALERT: Vulnerable Protobuf detected ({pb_ver}).")
        print("[*] Attempting Autonomous Self-Patch...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "protobuf>=4.25.8"])
            print("[+] Self-Patch Successful. Rebooting Kernel...")
            os.execv(sys.executable, ['python3'] + sys.argv)
        except Exception as e:
            print(f"[FATAL] Autonomous Patch Failed: {e}")
            return False
    return True

def boot_iluminara():
    print("====================================================")
    print("   🚀 iLUMINARA SOVEREIGN OS - KERNEL BOOT v1.0")
    print("====================================================")
    
    # 1. Environment Enforcement
    if not enforce_security_patch():
        sys.exit("❌ KERNEL PANIC: Environment Security Breach.")

    # 2. Dependency Integrity Check (Iron Dome)
    if not verify_iron_dome_v2():
        sys.exit("❌ KERNEL PANIC: Dependency Integrity Failure.")

    # 3. License Compliance Check
    if not verify_license_compliance():
        sys.exit("❌ KERNEL PANIC: License Compliance Failure.")

    # 4. DNA Identity Verification
    dna = SovereignDNA()
    current_hash = dna.generate_genesis_seed()
    print(f"[BOOT] DNA Hash Verified: {current_hash[:16]}...")
    print(f"[BOOT] Root Admin: {dna.director_root}")
    
    print("\n✅ KERNEL ONLINE: All Sovereignty Shields Active.")
    return True

if __name__ == "__main__":
    if boot_iluminara():
        # Proceed to launch the Sovereign SOC / Dashboard
        pass