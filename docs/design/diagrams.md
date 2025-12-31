# Architecture Diagrams

## 1. Ethical Decision Flow (Swimlane)
```mermaid
sequenceDiagram
    participant CHW as Field Worker
    participant App as Mobile Interface
    participant HSTPU as Predictive Brain
    participant Law as Omni-Law Matrix
        
        CHW->>App: Inputs Symptoms + Location
        App->>HSTPU: Sends 4D Context Vector
        HSTPU->>HSTPU: 72hr Prediction (Friston Energy Min)
        HSTPU->>Law: Proposes Action (e.g. Quarantine Sector 4)
        Law->>Law: Checks 47 Frameworks (WFP Index)
            
            alt Violation Detected
                Law-->>App: BLOCK: "Violates Geneva Convention"
            else Compliance Verified
                Law-->>App: PERMIT: "Action Safe"
            end
        App-->>CHW: Displays Green/Red Guidance

## 2. HSML Audit Trail
flowchart LR
    A[Action Trigger] --> B{HSML Logger}
    B --> C[Capture Geo-Context]
    B --> D[Capture WFP Score]
    C & D --> E[Generate Immutable Log]
    E --> F[Hash to Blockchain]
    F --> G[Transparency Portal]