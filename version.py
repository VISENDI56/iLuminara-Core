"""
iLuminara Sovereign OS - Version Control System
Standard: Semantic Versioning (SemVer) 2.0.0
"""
MAJOR = 2
MINOR = 0
PATCH = 171
BUILD_METADATA = "Apex-Sovereign-Nexus-IT"

def get_version_tuple():
    return (MAJOR, MINOR, PATCH)

def get_full_version():
    return f"v{MAJOR}.{MINOR}.{PATCH}+{BUILD_METADATA}"

if __name__ == "__main__":
    print(get_full_version())
