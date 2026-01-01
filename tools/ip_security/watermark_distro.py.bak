import os
import hashlib
import sys
import shutil

def watermark_build(recipient_name):
    """
        Creates a traceable copy of iLuminara for a specific recipient.
            Injects a 'Salted Hash' into the core config that identifies them.
                """
                    print(f"[*] Watermarking iLuminara-Core for recipient: {recipient_name}")
                        
                            # Generate a unique tracking ID
                                track_id = hashlib.sha256(recipient_name.encode()).hexdigest()[:16]
                                    watermark = f"# LICENSED_TO: {recipient_name} | TRACK_ID: {track_id}"
                                        
                                            # Inject into critical files (invisible to casual execution)
                                                targets = ["config.py", "Home.py", "LEGAL_NOTICE.md"]
                                                    
                                                        dist_dir = f"dist/iLuminara_{recipient_name.replace(' ', '_')}"
                                                            if os.path.exists(dist_dir): shutil.rmtree(dist_dir)
                                                                shutil.copytree(".", dist_dir, ignore=shutil.ignore_patterns('.git', 'venv'))
                                                                    
                                                                        for root, _, files in os.walk(dist_dir):
                                                                                for file in files:
                                                                                            if file in targets:
                                                                                                            path = os.path.join(root, file)
                                                                                                                            with open(path, "a") as f:
                                                                                                                                                f.write(f"\n\n{watermark}\n")
                                                                                                                                                    
                                                                                                                                                        print(f"✅ GENERATED TRACEABLE BUILD: {dist_dir}")
                                                                                                                                                            print(f"   - Track ID: {track_id}")
                                                                                                                                                                print(f"   - Status: Ready to Zip and Send.")

                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                    if len(sys.argv) < 2:
                                                                                                                                                                            print("Usage: python3 watermark_distro.py 'Investor Name'")
                                                                                                                                                                                else:
                                                                                                                                                                                        watermark_build(sys.argv[1])