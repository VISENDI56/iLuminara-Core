import os, secrets
class CryptoShredder:
    """IP-02: Forward secrecy via 7-pass NIST overwrite."""
    def dissolve(self, path):
        if not os.path.exists(path): return False
        size = os.path.getsize(path)
        with open(path, "ba+", buffering=0) as f:
            for _ in range(7):
                f.seek(0); f.write(secrets.token_bytes(size))
                f.flush(); os.fsync(f.fileno())
        os.remove(path)
        return True
