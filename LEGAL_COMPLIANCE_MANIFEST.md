# iLuminara-Core: Open Source Compliance Manifest (2026)

## Weak Copyleft Acknowledgement
The following libraries are used under **MPL-2.0** or **LGPL-2.1**:
* `certifi`: (MPL-2.0) - Used for SSL Certificate verification.
* `soxr`: (LGPL-2.1) - Used via `librosa` for high-quality audio resampling.

## Sovereignty Assurance
1. **Dynamic Linking:** iLuminara links to these libraries dynamically at runtime. No code from these libraries has been incorporated or modified within the proprietary `iLuminara-Core` kernel.
2. **Derivative Work Separation:** All proprietary AI logic (HSTPU, TRM, etc.) resides in separate files and modules, satisfying the 'Larger Work' exception in MPL-2.0 and LGPL-2.1.