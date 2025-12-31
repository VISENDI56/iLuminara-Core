# Functional Requirements Document (FRD) v1.0

## 1. System Overview
iLuminara is a Sovereign Health OS designed for the 80/20 Software-Service ratio.
* **80% Automation:** HSTPU/BioNeMo handles diagnostics and routing.
* **20% Human Touch:** CHWs handle "Last Mile" care and ethical overrides.

## 2. Vulnerability-Weighted Ethical Engine
* **Requirement:** The system MUST prioritize resource allocation based on the WFP Vulnerability Index.
* **Constraint:** "Golden Rule Algorithm" - Equity Score >= Vulnerability Index.
* **Failure State:** If Equity Score is low, the `OmniLawMatrix` blocks the allocation.

## 3. HSTPU Technical Spec
* **Input:** 4D Tensor (Lat, Lon, Time, Severity).
* **Processing:** Spatiotemporal Graph Convolution (ST-GCN).
* **Output:** 72-Hour Crisis Prediction Window with 52ms latency target.

## 4. Active Inference (Friston)
* **Goal:** Minimize Free Energy (Surprise).
* **Implementation:** The JEPA model continuously updates its "World View" to reduce the delta between *Predicted Logistics* and *Actual Supply Consumption*.