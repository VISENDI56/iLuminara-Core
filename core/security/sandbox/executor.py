import subprocess
import shlex

class SovereignSandbox:
    """
    Prevents AI Agents from executing unauthorized OS commands.
    Strict Allow-list only.
    """
    def __init__(self):
        self.allow_list = ["git status", "ls core", "python3 --version"]

    def safe_execute(self, command):
        # Step 1: Tokenize and Sanitize
        safe_args = shlex.split(command)
        # Step 2: Check against Allow-list
        if command in self.allow_list:
            return subprocess.run(safe_args, capture_output=True, text=True)
        else:
            return "🚫 ACCESS DENIED: Command not in Sovereign Allow-list."

sandbox = SovereignSandbox()
