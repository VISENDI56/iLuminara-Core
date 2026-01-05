import json, hashlib
from pathlib import Path
SECRETS_FILE = Path("core/security/secrets.json")
AUDIT_DIR = Path("audit_logs"); AUDIT_DIR.mkdir(exist_ok=True)

def load_secret(key): return json.loads(SECRETS_FILE.read_text()).get(key)
def rbac_check(user_role,permission):
    ROLE_PERMS = {"admin":["read","write","override"],"operator":["read","write"],"guest":["read"]}
    return permission in ROLE_PERMS.get(user_role,[])
def audit_event(event):
    content=json.dumps(event,sort_keys=True)
    h=hashlib.sha256(content.encode()).hexdigest()
    with open(AUDIT_DIR/f"{h}.json","w") as f:f.write(content)
    return h
def tamper_detect(file_path,expected_hash):
    return hashlib.sha256(file_path.read_bytes()).hexdigest()==expected_hash
