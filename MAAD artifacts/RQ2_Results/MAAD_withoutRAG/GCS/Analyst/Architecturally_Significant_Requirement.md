# Architecturally Significant Requirements Results (ASRs)

[ASR-001]: Mode/level-based access control across the whole system  
**Description**: “The Gemini system… exists in… disjoint operational levels. Access… restricted according to the current level… software imposes… access modes…” Updated per evaluator: Add: See doc/security/rbac-policy.json for role-to-op mapping; e2e tests verify role limitations (e.g., astronomer cannot issue CMD_SLEW). Owner: Team-Sec; Next action: Draft and publish schema plus skeleton role test cases for RBAC.  
**Architectural Impact:** Requires a centralized authorization model tied to both operational level (system state) and access mode (session capability), affecting identity management, UI capabilities, command routing, and subsystem gateways.  
**Quality Attributes Affected:** Security, Safety, Usability  
**Architectural Constraints:** Must implement consistent policy enforcement across all subsystems and interfaces (local + remote).  
**Rationale:** Cross-cutting; defines core control-plane structure and partitioning of capabilities.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-002, FR-003, NFR-008  
- **Conflicts with:** NFR-010 (simplicity vs restrictions)  
---

[ASR-002]: Sequencer/scheduler as primary control path; observers cannot issue direct telescope commands  
**Description**: “Access… through the sequencer with no direct control…” and “Traditional interactive operation shall normally be replaced by… automatic sequencer… user will interact with the scheduler…”  
**Architectural Impact:** Forces command orchestration component(s) (sequencer/scheduler) as the mediation layer between users/programs and hardware control services; impacts API boundaries, state machines, validation, and audit.  
**Quality Attributes Affected:** Safety, Reliability, Operability  
**Architectural Constraints:** Direct-control endpoints must be restricted; orchestration must support both pass-through and validated modes.  
**Rationale:** High impact on decomposition (OCS + sequencer) and control flow.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004, FR-012, FR-017, NFR-008  
- **Conflicts with:** FR-013 (interactive override)  
---

[ASR-003]: Non-interference guarantees for monitoring/testing/admin during observing  
**Description**: “Under no circumstances should monitoring… testing… administrative access affect the performance of an ongoing observation.” Updated per evaluator: Acceptance: During 24h soak test, with max monitoring and admin load, observing command response time increases ≤ 2% (median) and ≤ 4% (99th percentile). Metric: obs_cmd_latency_pct_change; window=24h. Owner: Team-SRE; Next action: Add load test scenario and metric details for acceptance.  
**Architectural Impact:** Requires resource isolation, prioritization, and possibly separate process/thread pools, QoS, rate limiting, and read-only data paths; influences telemetry architecture and concurrency controls.  
**Quality Attributes Affected:** Performance, Reliability, Availability  
**Architectural Constraints:** Monitoring/testing/admin must be read-only or safely sandboxed; must not contend with real-time control paths.  
**Rationale:** Strong operational constraint spanning most components.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, FR-008, FR-009, NFR-003  
- **Conflicts with:** NFR-015 (high-rate logging), FR-045 (quick-look feedback)  
---

[ASR-004]: Common command framework and reliable command protocol across subsystems/IOCs  
**Description**: “All subsystems must respond to a common set of commands… All IOC subsystems must respond to additional common commands… uniform ACK/NAK… Timeouts… 500 msec… Handshaking… 100-200 msec…”  
**Architectural Impact:** Implies standardized service interfaces, shared command schemas, and a common transport/protocol layer; constrains subsystem implementation and integration testing.  
**Quality Attributes Affected:** Interoperability, Performance, Maintainability  
**Architectural Constraints:** System-wide command taxonomy; protocol must support ACK/NAK, timeouts, delayed replies, and deterministic handshake timing.  
**Rationale:** Cross-cutting integration backbone; measurable timings affect design.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, FR-033, NFR-001  
- **Conflicts with:** NFR-020 (portability vs performance), NFR-008 (security overhead)  
---

[ASR-005]: Access Mode Allocation for critical resources with deadlock avoidance  
**Description**: “Access Mode Allocation… dynamically identifies and assigns resources… Critical resources… assigned solely through this allocation system… must ensure… cannot remain deadlocked…”  
**Architectural Impact:** Requires a centralized/distributed lock manager or allocator service with deadlock prevention/detection, resource modeling, and enforcement hooks across command execution.  
**Quality Attributes Affected:** Safety, Reliability, Availability  
**Architectural Constraints:** All critical resource usage must be mediated; no bypass; must guarantee progress (no deadlock).  
**Rationale:** High risk if incorrect; impacts nearly all control paths and concurrency.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-027, NFR-008  
- **Conflicts with:** FR-016 (staff direct control), FR-025 (parallel instruments)  
---

[ASR-006]: Remote operations as a first-class capability with dynamic site-based restrictions  
**Description**: “All software should be developed to permit remote operations… full operations remotely… restrict specific operations to specific remote sites… independent… and dynamic… system shall be totally transparent to local or remote use… minimize impact of link bandwidth…”  
**Architectural Impact:** Forces distributed-system architecture, remote-capable UIs, network-transparent APIs, and policy enforcement by site; requires careful separation of control vs presentation and support for WAN variability.  
**Quality Attributes Affected:** Scalability, Security, Usability, Availability  
**Architectural Constraints:** Remote/off-site must use same functional stack with policy gating; bandwidth-aware design required.  
**Rationale:** Major architectural driver with cross-cutting concerns and risk.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-018, FR-022, NFR-008  
- **Conflicts with:** FR-021 (safety restriction for remote control)  
---

[ASR-007]: Safety architecture with software-independent interlocks and safe-state behavior  
**Description**: “Safety protection… must be independent of the software… hard stops… interlocks… watch dogs… software shall be able to bring… quickly to a safe state…”  
**Architectural Impact:** Requires explicit safety boundary between software and hardware interlocks; mandates safety-monitoring pipelines, fault propagation, and safe-state orchestration independent of normal control flow.  
**Quality Attributes Affected:** Safety, Reliability  
**Architectural Constraints:** Passive/active interlocks outside software; software must integrate with safety signals and execute safe-state procedures.  
**Rationale:** Life/safety critical and system-wide.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-054, NFR-012  
- **Conflicts with:** FR-064 (retries), FR-013 (interactive overrides)  
---

[ASR-008]: Virtual telescope and mandatory subsystem simulators for development/testing without hardware  
**Description**: “All control software must provide support for simulated use within the virtual telescope… all hardware subsystems must provide a software simulation module… cannot require any hardware specific to the application.” Updated per evaluator: Simulation stub must implement all core commands as per ICD; response time must be within 2-3x real device baseline; must emit error on command XYZ as in actual hardware. Owner: Team-API; Next action: Draft simulation integration contract with representative scenarios.  
**Architectural Impact:** Requires abstraction layers/ports for hardware IO, simulation adapters, and a virtualized integration environment; affects CI/CD, test harnesses, and interface contracts.  
**Quality Attributes Affected:** Testability, Maintainability, Portability  
**Architectural Constraints:** Every subsystem must have a simulatable interface; simulation must run in standard environments without target hardware.  
**Rationale:** Strong constraint across subsystem implementations; key to integration strategy.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-019, FR-066, FR-044  
- **Conflicts with:** —  
---

[ASR-009]: Online data management architecture: storage tiers, automatic archiving, FITS interchange, retention  
**Description**: “Archiving… automatically… to the Gemini Archive subsystem… transmitted… using a FITS format… system… retaining 7 days… last 3 days… interactively…”  
**Architectural Impact:** Drives storage tiering (hot disk vs archive), data pipelines, metadata/header management, and integration with archive subsystem; impacts throughput, retention, and retrieval design.  
**Quality Attributes Affected:** Availability, Capacity, Interoperability  
**Architectural Constraints:** Must implement automatic archival flows; FITS export with headers; on-site retention requirements.  
**Rationale:** Large data-volume cross-cutting requirement affecting multiple services and infrastructure.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036, FR-037, NFR-007  
- **Conflicts with:** —  
---

[ASR-010]: Parameter/control information via online database with stringent latency and distributed access  
**Description**: “parameters… on line database… Access times… 2-3 msec… Asynchronous writes… remote access and distributed data… internal (IOC) implementation… EPICS.”  
**Architectural Impact:** Implies a distributed data layer spanning IOCs and host workstations, with caching/in-memory for critical items and async write patterns; constrains technology choices (EPICS in IOCs).  
**Quality Attributes Affected:** Performance, Scalability, Maintainability  
**Architectural Constraints:** 2–3 ms access; async writes; distributed/remote access; EPICS-based IOC DB.  
**Rationale:** Measurable performance targets and mandated technology at a key integration layer.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-065, NFR-017  
- **Conflicts with:** NFR-008 (auth checks), NFR-020 (portability)  
---

[ASR-011]: Observability/logging to recreate observations plus high-rate engineering telemetry  
**Description**: “recreate the sequence of events… properly timestamped and indexed… log engineering data at up to 200 Hz… available to external software… long-term… common format (baselined as SYBASE).”  
**Architectural Impact:** Requires centralized logging/telemetry pipeline, time synchronization, indexing/search, storage/retention strategies, and export APIs for external analysis tools.  
**Quality Attributes Affected:** Operability, Diagnosability, Performance  
**Architectural Constraints:** Must support 200 Hz burst logging, low-rate long-term, common schema/format, and external access.  
**Rationale:** Cross-cutting and capacity/performance impacting; affects runtime overhead and storage.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-062, FR-063, NFR-015  
- **Conflicts with:** NFR-003 (non-interference)  
---

[ASR-012]: Multi-instrument concurrency with strict isolation between active and inactive instruments  
**Description**: “Parallel access to all… instruments… only one instrument has access to the telescope beam… inactive instruments… calibration/hot standby… Regardless… shall not be possible… to adversely impact the active instrument.” Updated per evaluator: Test: With beam assigned to Instrument A, run activities on B/C; measure obs_cmd_latency_p95 for A; alert if >2%. Metric: 'inst_concurrency_latency_p95'. Owner: Team-QA; Next action: Write test scenario doc and add SRE/QA metric to monitoring plan.  
**Architectural Impact:** Requires concurrency control and isolation boundaries between instrument control domains; impacts scheduling, resource allocation, and shared subsystem interactions (beam, telescope state).  
**Quality Attributes Affected:** Reliability, Safety, Performance  
**Architectural Constraints:** Enforce active-beam exclusivity; guarantee inactive actions cannot degrade active operations.  
**Rationale:** Core operational model with non-trivial coordination across subsystems.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025, FR-026, FR-027  
- **Conflicts with:** —  
---

[ASR-013]: Visitor instrument support via standardized, stable interface with minimum required capabilities  
**Description**: “subset… standardized interface… stable and long-lived… At a minimum… status… preprogrammed observing sequences… offset… position and focus.”  
**Architectural Impact:** Forces explicit external-facing instrument API subset and long-term versioning/backward compatibility strategy; impacts integration testing and documentation.  
**Quality Attributes Affected:** Interoperability, Maintainability  
**Architectural Constraints:** Stable interface over years; must expose minimum functions listed while limiting unsupported coordinated motions.  
**Rationale:** High integration risk; long-lived contract requirement is architecturally constraining.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-060, FR-061, NFR-021  
- **Conflicts with:** NFR-018 (evolving internal standards)  
---