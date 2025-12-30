# Controlled Access Area (CAA) Protocol
**Status:** ACTIVE | **Enforcement:** Crypto-Shredder

## 1. Policy Statement
iLuminara strictly prohibits the transfer of "Core IP" (Source Code, Weights) to external partners. Instead, we offer a **Controlled Access Area (CAA)**.

## 2. The CAA Mechanism
- **No Transfer:** Partners never receive the code.
- **Enclave Access:** Partners submit queries to a secure AWS Nitro Enclave.
- **Output Only:** Only the *results* (inference/analytics) leave the enclave.
- **Audit:** Every query is logged via `blockchain_logger.py`.

## 3. Implementation
To initiate a CAA session, the partner must present a valid `Sovereign-Token` signed by the Ministry of Health.
