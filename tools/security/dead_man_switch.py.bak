import os
import shutil

def emergency_wipe():
    """
        EMERGENCY PROTOCOL.
            Wipes all local `.env`, `adapters`, and `dist` folders.
                Triggered if a 'Duress Code' is entered during login.
                    """
                        print("🚨 DURESS SIGNAL DETECTED. INITIATING ASSET WIPE...")
                            
                                targets = [".env", "ml_ops/adapters", "dist"]
                                    
                                        for t in targets:
                                                if os.path.exists(t):
                                                            if os.path.isdir(t):
                                                                            shutil.rmtree(t)
                                                                                        else:
                                                                                                        os.remove(t)
                                                                                                                    print(f"   [WIPE] Destroyed: {t}")
                                                                                                                                
                                                                                                                                    print("✅ LOCAL ENVIRONMENT SANITIZED.")

                                                                                                                                    if __name__ == "__main__":
                                                                                                                                        confirm = input("Type 'BURN_ASSETS' to confirm: ")
                                                                                                                                            if confirm == "BURN_ASSETS":
                                                                                                                                                    emergency_wipe()