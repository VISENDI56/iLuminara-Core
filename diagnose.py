import sys
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")
print(f"Current directory: {sys.path[0]}")

try:
    import core
    print("✅ core module found at:", core.__file__)
except ImportError as e:
    print("❌ core module not found:", e)
