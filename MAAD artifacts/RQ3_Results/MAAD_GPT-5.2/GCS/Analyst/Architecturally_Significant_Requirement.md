# Architecturally Significant Requirements Results

[ASR-001]: Layered operational levels and access modes as core architecture concept  
**Description**: “The Gemini system… exists in… disjoint operational levels… Access… restricted… software imposes… access modes…”  
**Architectural Impact:**  
Forces a system-wide state/mode model that gates UI, command routing, subsystem behavior, and authorization. Requires centralized policy evaluation and consistent enforcement across all subsystems and stations.  
**Quality Attributes Affected:** Security, Safety, Modifiability, Usability  
**Architectural Constraints:** Must implement global operational-level state machine and mode-aware access control across all interfaces.  
**Rationale:** Cross-cutting constraint affecting every component and interaction path.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006  
- **Conflicts with:** NFR-020  
---

[ASR-002]: Sequencer/scheduler-mediated control as the primary control plane  
**Description**: “Access… through the sequencer with no direct control…” and “Traditional interactive operation shall normally be replaced by operation via an automatic sequencer… user will interact with the scheduler program…”  
**Architectural Impact:**  
Drives a centralized orchestration component (sequencer/scheduler) and command mediation layer; subsystems become command servers; UIs become clients of the sequencer rather than direct device controllers.  
**Quality Attributes Affected:** Safety, Reliability, Usability, Performance  
**Architectural Constraints:** Control commands in observing mode must flow through sequencer/scheduler; direct command paths must be restricted/role-gated.  
**Rationale:** Major decomposition and control-flow decision with safety and operational implications.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006  
- **Conflicts with:** FR-012  
---

[ASR-003]: Standardized command/response protocol and common command sets across subsystems  
**Description**: “Syntax… consistent across the system… All subsystems must respond to a common set of commands… uniform ACK/NAK… timeouts… handshaking…”  
**Architectural Impact:**  
Requires a shared messaging/IDL/protocol layer and consistent command taxonomy across heterogeneous subsystems (workstations + IOCs). Influences integration strategy, adapter design, and test harnesses.  
**Quality Attributes Affected:** Interoperability, Maintainability, Reliability, Performance  
**Architectural Constraints:** Single consistent command syntax; uniform ACK/NAK; mandated timeout/handshake behavior; common command set for status/version/self-test and IOC lifecycle.  
**Rationale:** Strong system-wide integration constraint; high leverage and high risk if inconsistent.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002  
- **Conflicts with:** NFR-019 (layering vs performance shortcuts)  
---

[ASR-004]: Real-time determinism confined to IOC layer  
**Description**: “Strict real-time control is restricted to the IOC layer… Real-time support is required at the IOC level.”  
**Architectural Impact:**  
Enforces a two-tier timing model: non-real-time OCS/UI layers and deterministic IOC controllers. Drives partitioning of control loops, scheduling, and failure containment boundaries.  
**Quality Attributes Affected:** Performance, Safety, Reliability  
**Architectural Constraints:** Time-critical control loops and hardware interfacing must reside in IOC layer; upper layers must tolerate non-deterministic network/OS behavior.  
**Rationale:** Fundamental allocation of responsibilities that shapes component boundaries and technology choices.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-028  
- **Conflicts with:** NFR-020 (remote transparency expectations)  
---

[ASR-005]: Distributed networked architecture with explicit LAN/WAN/time-bus/memory-bus elements  
**Description**: “LAN shall support… internal communication needs… supplemented with a Local Time Bus… digital reflective memory bus and an analog event-based bus…” and “LAN must support… 20-40 Mbits/second.”  
**Architectural Impact:**  
Forces multi-network/transport design, time synchronization distribution, and separation of traffic classes (control, data, timing/events). Impacts deployment topology and interface abstractions.  
**Quality Attributes Affected:** Performance, Reliability, Scalability  
**Architectural Constraints:** Must include LAN plus specialized buses for timing and event distribution; network interfaces must meet bandwidth/latency needs; homogeneous LAN/WAN interfaces based on standards.  
**Rationale:** Major infrastructure constraint affecting all communications and deployment.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-011, NFR-019  
- **Conflicts with:** NFR-018 (internet limitations)  
---

[ASR-006]: Virtual telescope / simulation-first capability across all control software  
**Description**: “Virtual telescope capability… provides a telescope simulator…” and “All control software must provide support for simulated use within the virtual telescope… all hardware subsystems must provide a software simulation module…”  
**Architectural Impact:**  
Requires simulation interfaces for every subsystem, simulator swap mechanisms, and environment-independent behavior. Drives dependency inversion and contract-based subsystem interfaces.  
**Quality Attributes Affected:** Testability, Modifiability, Maintainability  
**Architectural Constraints:** Each subsystem must ship a simulator module; simulation cannot require hardware specific to the application; must respond reasonably to commands.  
**Rationale:** Cross-cutting requirement that shapes subsystem packaging, interfaces, and CI/testing strategy.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-052, FR-030  
- **Conflicts with:** NFR-001 (if simulation overhead leaks into ops)  
---

[ASR-007]: Visitor instrument support via stable, long-lived standardized subset interface (server model)  
**Description**: “Visitor instruments… subset… standardized interface… instruments as servers… interface… stable and long-lived…” Visitor instrument interface must support semantic versioning; removed methods require minimum 2 years of backward-compatibility support. API method deprecation shall notify all clients 6 months prior to removal; maintain API backward compat for 2 years after deprecation. (Next action: Extend API docs with explicit changelog, notification process, and auditing.)  
**Architectural Impact:**  
Forces a public integration boundary/API that must remain backward compatible over years, likely requiring versioning, adapters, and strict contract management.  
**Quality Attributes Affected:** Interoperability, Modifiability, Maintainability  
**Architectural Constraints:** Visitor interface must be subset of existing instrument interface; must support status, preprogrammed sequences, telescope offset/focus; must be stable/long-lived; must support semantic versioning; removed methods require minimum 2 years backward compatibility; deprecation notice 6 months prior to removal; backward compatibility maintained for 2 years after deprecation.  
**Rationale:** External-facing contract with long lifecycle; high cost of change and strong architectural coupling.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017  
- **Conflicts with:** NFR-015 (evolving standards/COTS changes)  
---

[ASR-008]: Access Mode Allocation system for critical resource arbitration and deadlock freedom  
**Description**: “Access Mode Allocation system… dynamically identifies and assigns resources… Critical resources… assigned solely through this allocation system… must ensure… cannot remain deadlocked…”  
**Architectural Impact:**  
Requires a centralized or coordinated resource manager, lock/lease model, and deadlock-avoidance strategy across distributed subsystems and multi-user stations.  
**Quality Attributes Affected:** Safety, Reliability, Availability  
**Architectural Constraints:** All critical resource acquisition must go through allocation system; must guarantee deadlock freedom.  
**Rationale:** Cross-cutting concurrency control mechanism with correctness and safety implications.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-038, NFR-006  
- **Conflicts with:** NFR-020 (transparent access vs arbitration)  
---

[ASR-009]: High-rate observability and logging sufficient to reconstruct observations  
**Description**: “Sufficient information be recorded… to recreate the sequence of events… log engineering data at up to 200 Hz… errors/alarms… timestamped and indexed…”  
**Architectural Impact:**  
Drives a system-wide telemetry/logging pipeline, time synchronization, storage schemas, indexing, and performance isolation so logging doesn’t disrupt control.  
**Quality Attributes Affected:** Observability, Performance, Reliability  
**Architectural Constraints:** Must support 200 Hz short-burst engineering logs; long-term ≤1 Hz; logs must be timestamped/indexed; data available to external analysis software.  
**Rationale:** Cross-cutting and performance-sensitive; impacts storage, messaging, and time services.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-024, ASR-005  
- **Conflicts with:** NFR-007 (non-intrusive monitoring), NFR-001  
---

[ASR-010]: Remote operations as a first-class design requirement with dynamic site-based restrictions  
**Description**: “All software should be developed to permit remote operations… possible to do full operations remotely… restrict specific operations to specific remote sites… method… independent… and dynamic… security… might imply different operation levels and privileges at different sites.”  
**Architectural Impact:**  
Forces distributed architecture, remote-capable UIs/services, policy-driven authorization by site, and secure gateways. Requires designing for WAN latency/bandwidth variability from the start.  
**Quality Attributes Affected:** Security, Usability, Performance, Availability  
**Architectural Constraints:** Remote operations must be supported across facilities; restrictions must be dynamic and decoupled from operation implementations; remote users often mediated via scheduler.  
**Rationale:** Large-scope cross-cutting requirement with security and deployment implications; high risk if deferred.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, FR-023, NFR-029  
- **Conflicts with:** FR-024 (local safety presence), NFR-018 (internet limits)  
---

[ASR-011]: On-line distributed parameter database with EPICS in IOCs and strict latency targets  
**Description**: “All telescope and instrument parameters… on line database… access times… 2-3 msec… asynchronous writes… remote access and distributed data… internal (within the IOC)… based on EPICS.”  
**Architectural Impact:**  
Mandates a shared data backbone and access pattern (DB-mediated integration), influences caching, replication, and API design; EPICS requirement constrains IOC technology stack.  
**Quality Attributes Affected:** Performance, Interoperability, Modifiability  
**Architectural Constraints:** EPICS-based IOC database; 2–3 ms access; async writes; remote/distributed support; time-critical info in memory.  
**Rationale:** Strong technology and performance constraint central to integration and control.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-046, NFR-005  
- **Conflicts with:** NFR-001 (end-to-end latency budgets)  
---

[ASR-012]: Safety architecture requiring independent interlocks plus software safe-state behavior  
**Description**: “Safety protection… must be independent of the software… hard stops… interlocks… watch dogs… software shall be able to bring… quickly to a safe state…” The system software must initiate safe-state transition within 2 seconds of receiving a hazard notification; system must reach a confirmed safe state within 10 seconds. (Next action: Add measurable time windows to safety requirements.)  
**Architectural Impact:**  
Forces explicit safety boundary between software and hardware protections, safety event channels, and safe-state orchestration logic; constrains control flows and failure handling.  
**Quality Attributes Affected:** Safety, Reliability, Compliance  
**Architectural Constraints:** Interlocks must not depend on software; software must respond to danger detection and transition system to safe state; must initiate safe-state transition within 2 seconds of hazard notification; must reach confirmed safe state within 10 seconds; hazard analysis during functional specification.  
**Rationale:** High-risk, high-impact cross-cutting requirement affecting all control subsystems.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-049, NFR-013  
- **Conflicts with:** NFR-025 (recovery time goals may be limited by safety)  
---

[ASR-013]: Security boundary against WAN intrusion (firewall/gateway) and command mix-up prevention  
**Description**: “Security must be provided… prevent accidental mix-up… prevent intrusion from the wide area network… acceptable… firewall.”  
**Architectural Impact:**  
Requires network segmentation, security gateway/firewall, authentication/authorization model tied to modes/levels/sites, and auditing. Impacts all remote access and integration points.  
**Quality Attributes Affected:** Security, Safety, Reliability  
**Architectural Constraints:** Must include WAN intrusion protection (gateway/firewall); must prevent cross-user command mix-up; protect astronomical database.  
**Rationale:** Cross-cutting security requirement with major architectural and operational implications.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, ASR-010  
- **Conflicts with:** NFR-020 (transparency)  
---