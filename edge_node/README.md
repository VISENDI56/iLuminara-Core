# Quantum & Biometric Security

## Crypto Shredder (IP-02)
- Post-quantum encryption with Kyber-1024 (if oqs-python is installed)
- AES-GCM fallback for legacy systems
- `shred()` destroys all keys in memory

## Acorn Protocol
- WebAuthnAuthenticator: FIDO2 biometric authentication (fingerprint/FaceID)
- CrisisFallbackAuth: Social recovery via Shamir's Secret Sharing (3-of-5 trusted nodes)

## Usage
- Use `CryptoShredder` for all long-term data storage.
- Use `WebAuthnAuthenticator` for user login; fallback to `CrisisFallbackAuth` if biometrics fail.
