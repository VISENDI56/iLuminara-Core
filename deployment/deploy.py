import subprocess
def deploy(target):
    if target in ["laptop","edge"]: subprocess.run(["python","-m","streamlit","run","pages/1_🧬_Bio_Foundry.py"])
    elif target=="single-node-cloud": print("Deploying cloud container...")
    elif target=="kubernetes": print("Apply helm chart")
    else: raise ValueError(f"Unknown deployment target {target}")
