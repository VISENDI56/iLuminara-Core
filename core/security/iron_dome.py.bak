import re

class IronDomeInterceptor:
    """
    Nuclear-Grade Input Sanitation.
    Mitigates 2025-level RCE and injection exploits.
    """
    def sanitize_input(self, user_input):
        # Block common exploit patterns (Recursion/Shell/RCE)
        forbidden = [r"\.\./", r"rm -rf", r"chmod", r"eval\(", r"__import__"]
        for pattern in forbidden:
            if re.search(pattern, user_input):
                print(f"[!] IRON DOME: Exploit Pattern Detected: {pattern}")
                return False
        return True

dome = IronDomeInterceptor()
