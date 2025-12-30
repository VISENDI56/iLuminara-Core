import hashlib
import os
import json
from datetime import datetime

class IPDefenseAnchor:
    """
        Scans critical IP documentation and code, generates a SHA-256 hash,
            and logs it as an immutable record. Proves 'Prior Art'.
                """
                    def __init__(self, root_dir="."):
                            self.root_dir = root_dir
                                    self.critical_assets = [
                                              "core/jepa_architecture/mpc_controller.py",
                                                          "governance_kernel/omni_law_interceptor.py",
                                                                      "docs/product/technical_prd.md"
                                    ]

                                        def generate_ip_manifest(self):
                                                manifest = {"timestamp": str(datetime.now()), "assets": {}}
                                                        
                                                        for asset in self.critical_assets:
                                                                    if os.path.exists(asset):
                                                                                    with open(asset, "rb") as f:
                                                                                                file_hash = hashlib.sha256(f.read()).hexdigest()
                                                                                                            manifest["assets"][asset] = file_hash
                                                                                                                        
                                                                                                                                # Create a 'Genesis Block' of your IP
                                                                                                                                        manifest_hash = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
                                                                                                                                                
                                                                                                                                                        print(f"   [IP-Defense] ANCHOR HASH: {manifest_hash}")
                                                                                                                                                                print("   [IP-Defense] Store this hash in a public blockchain transaction immediately.")
                                                                                                                                                                        
                                                                                                                                                                                return manifest

                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                    anchor = IPDefenseAnchor()
                                                                                                                                                                                        manifest = anchor.generate_ip_manifest()
                                                                                                                                                                                            with open("IP_MANIFEST.json", "w") as f:
                                                                                                                                                                                                    json.dump(manifest, f, indent=2)