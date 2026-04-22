# Architecturally Significant Requirements Results:
[ASR-001]: Hard Real-Time Traffic Light Control  
**Description**: Each phase duration tolerance ±50ms; phase duration logged per cycle for test.  
**Architectural Impact:**  
Requires time-triggered scheduling (cyclic executive), state-machine implementation, and hardware pulse synchronization.  
**Quality Attributes Affected:**  
Reliability, Timeliness  
**Architectural Constraints:**  
Deterministic timing; event-driven state transitions; hardware interface integration.  
**Rationale:**  
Imposes real-time constraints (fixed cycle) impacting scheduling and fault tolerance.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010  
- **Conflicts with:** None  
---  

[ASR-002]: Safety-Critical Anomaly Notification  
**Description**: Metric: anomaly_notification_latency_bucket{le="2s"} over rolling 1-hour window must be ≥ 99.9%; alert if below threshold for >5min.  
**Architectural Impact:**  
Mandates fault-detection mechanisms, prioritized messaging, and fail-safe alerting (redundant paths).  
**Quality Attributes Affected:**  
Reliability, Safety  
**Architectural Constraints:**  
High-availability notification subsystem; real-time monitoring; fallback mechanisms.  
**Rationale:**  
Critical safety requirement demanding architectural redundancy and immediate response.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
- **Conflicts with:** None  
---  

[ASR-003]: Bounded Motion Control for Shuttle  
**Description**: Shuttle movement speed ≤ 3.0 m/s, acceleration ≤ 1.2 m/s², deceleration ≤ 1.5 m/s² as measured in logs (per NFR-001).  
**Architectural Impact:**  
Requires physics-based motion profiling, sensor feedback loops, and hardware abstraction for motor/brake control.  
**Quality Attributes Affected:**  
Performance, Safety, Reliability  
**Architectural Constraints:**  
Closed-loop control system; hardware abstraction layer (HAL); real-time sensor processing.  
**Rationale:**  
Cross-cutting safety/performance constraints necessitate control algorithms and hardware isolation.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-015, NFR-001  
- **Conflicts with:** None  
---  

[ASR-004]: Deterministic Package Routing  
**Description**: Route packages without overtaking; set switches only when no package is present.  
**Architectural Impact:**  
Demands concurrent pipeline management, sensor-based interlocks, and transactional switch control.  
**Quality Attributes Affected:**  
Reliability, Safety  
**Architectural Constraints:**  
Concurrency control; atomic switch operations; collision-avoidance logic.  
**Rationale:**  
Safety-critical constraint (no overtaking) imposes strict synchronization and error handling.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-014  
- **Conflicts with:** None  
---  

[ASR-005]: Configurable Traffic Light Regimes  
**Description**: Regime: <PHASE_NAME> <DURATION_MS> per line; validate regime file on insert, reject and log if malformed.  
**Architectural Impact:**  
Requires pluggable regime parsing, dynamic state-machine loading, and card reader integration.  
**Quality Attributes Affected:**  
Maintainability, Usability  
**Architectural Constraints:**  
Externalized configuration; parser module; hot-swappable behavior.  
**Rationale:**  
Flexibility requirement drives modular, data-driven design for field adaptability.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010  
- **Conflicts with:** None  
---