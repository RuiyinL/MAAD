# Architecturally Significant Requirements Results:
[ASR-001]: Distributed operations architecture  
**Description**: Support remote operations including observing, control, monitoring, diagnosis from multiple facilities (site/base/super/regional/satellite sites). Location refers to authenticated facility code, set by operator/login, or derived from trusted subnet (e.g., 10.20.0.0/16 = 'Base', 10.21.0.0/16 = 'Control Facility').  
**Architectural Impact:**  
Requires network-transparent interfaces, bandwidth-aware data compression, distributed command routing, and location-based access policies.  
**Quality Attributes Affected:**  
Performance, Security, Scalability  
**Architectural Constraints:**  
- Homogeneous LAN/WAN interfaces based on standards  
- Hardware redundancy not required but reconfiguration essential  
- Strict hierarchical communication model (ISO/OSI)  
**Rationale:**  
Cross-cutting requirement affecting communication protocols, security policies, and component decomposition.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-005 (Node support), FR-012 to FR-017  
---  
[ASR-002]: Operational level enforcement  
**Description**: System must enforce three disjoint operational levels (Observing, Maintenance, Test) with access restrictions. Every hardware interlock event must be logged; weekly self-tests required, with electronic report to safety officer. Privilege changes require supervisor approval and are logged as { 'time': ISO8601, 'user': string, 'old_level': string, 'new_level': string, 'approved_by': string }; self-test report is exported as JSON with summary + per-test status.  
**Architectural Impact:**  
Mandates state-machine implementation for mode transitions, privilege management subsystems, and hardware interlocks for level changes.  
**Quality Attributes Affected:**  
Security, Reliability  
**Architectural Constraints:**  
- Independent hardware interlocks for safety-critical transitions  
- Strict isolation between operational levels  
- Mandated interlock logging and testing  
**Rationale:**  
Safety-critical constraint requiring specialized hardware/software coordination with compliance monitoring.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002 (Level enforcement), ASR-006 (Safety mechanisms)  
---  
[ASR-003]: Multi-instrument concurrency  
**Description**: Support parallel operations for multiple instruments with one active instrument and inactive instruments performing calibrations without interference. System shall run deadlock detection tool nightly. All inter-instrument resource assignments logged and monitored for conflicts. Acceptance: Nightly job 'deadlock_scan' completes without error > 99% of nights, report exported weekly. Report format: { 'date': ISO8601, 'status': 'OK'|'ERROR', 'conflicts': [ { ... } ] }; incident triggers PagerDuty call and auto-jira ticket.  
**Architectural Impact:**  
Drives resource allocation system, concurrency control mechanisms, and priority-based scheduling.  
**Quality Attributes Affected:**  
Performance, Reliability  
**Architectural Constraints:**  
- Critical resource assignment via allocation system  
- Deadlock prevention mechanisms  
- Automated conflict monitoring  
**Rationale:**  
High-risk requirement affecting scheduling and resource management architecture with concurrency safeguards.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004 (Multi-instrument operations)  
---  
[ASR-004]: Real-time control constraints  
**Description**: Hard real-time control restricted to IOC layer with thruster outputs at 128ms in 160ms cycle; command handshaking within 100-200ms.  
**Architectural Impact:**  
Requires time-triggered architecture, deterministic scheduling, and hardware-specific I/O handling.  
**Quality Attributes Affected:**  
Performance, Reliability  
**Architectural Constraints:**  
- Cyclic executive pattern for real-time tasks  
- Hardware-specific I/O addressing  
**Rationale:**  
Safety-critical timing constraints dictating real-time patterns and component specialization.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006 (Command protocol), NFR-003 (Response times)  
---  
[ASR-005]: Fault tolerance mechanisms  
**Description**: System must reconfigure within 5 minutes after failures; support retry procedures; prevent failure cascading.  
**Architectural Impact:**  
Mandates redundancy design for critical components, state persistence for recovery, and failure containment domains.  
**Quality Attributes Affected:**  
Reliability, Availability  
**Architectural Constraints:**  
- Modular decomposition with strict interfaces  
- State persistence for system recovery  
**Rationale:**  
High-availability requirement affecting error handling and system recovery strategies.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-008 (Fault recovery), NFR-007 (Recovery time)  
---  
[ASR-006]: Safety-critical interlocks  
**Description**: Safety protection must be hardware-implemented independent of software; system must transition to defined safe state in <1 second upon danger condition, confirmed by hardware feedback and logged event. Acceptance: Each safety transition event emits log with 'event=safestate, latency_ms=<999, ...>'  
**Architectural Impact:**  
Requires hardware-based safety subsystems, watchdogs, and fail-safe state transitions.  
**Quality Attributes Affected:**  
Safety, Reliability  
**Architectural Constraints:**  
- Passive interlocks for catastrophic hazards  
- Software limits only for non-critical hazards  
- Sub-1s transition timing  
**Rationale:**  
Life-critical constraint dictating hardware/software boundary and safety patterns with timing verification.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-011 (Safety transition)  
---  
[ASR-007]: Centralized configuration management  
**Description**: All telescope/instrument parameters kept in online database accessible via standardized interface calls.  
**Architectural Impact:**  
Drives centralized configuration store, schema versioning, and distributed caching for performance.  
**Quality Attributes Affected:**  
Maintainability, Performance  
**Architectural Constraints:**  
- EPICS-based implementation for IOCs  
- Version-controlled data contracts  
**Rationale:**  
Cross-cutting requirement affecting data management and subsystem interfaces.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008 (Database access)  
---