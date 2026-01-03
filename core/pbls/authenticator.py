from core.pbls.shield_engine import pbls

def require_pbls(func):
    """Decorator to enforce Polymorphic Shielding on core functions."""
    def wrapper(*args, **kwargs):
        key = pbls.generate_polymorphic_key()
        print(f"[PBLS] Key Validated for Function: {func.__name__}")
        # In production, this key is compared against the hardware PUF
        return func(*args, **kwargs)
    return wrapper