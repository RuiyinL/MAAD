# Architecturally Significant Requirements Results

[ASR-001]: Physical link and primary interface between WIDAR hardware and VLA M&C  
**Description**: “The Correlator Monitor and Control System provides the physical link between the WIDAR Correlator hardware and the VLA Expansion Project monitor and control system. It is the primary interface by which the correlator is configured, operated, and serviced.”  
**Architectural Impact:**  
- Forces a clear boundary between external M&C and correlator hardware control.  
- Drives interface definitions, message routing, and hardware abstraction layers.  
- Implies high criticality in the astronomical data path, influencing redundancy and fault containment.  
**Quality Attributes Affected:** Availability, Reliability, Interoperability, Maintainability  
**Architectural Constraints:** Must implement a hardware abstraction/control interface that mediates all configuration/operation/service interactions.  
**Rationale:** Defines the system’s central integration role and boundary, shaping component decomposition and interfaces.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-002  
- **Conflicts with:** None identified  
---

[ASR-002]: Virtual Correlator Interface (VCI) as gateway and translation interface  
**Description**: “The gateway to the correlator will be through the Virtual Correlator Interface…” and “This translation interface will be called the Virtual Correlator Interface.” and “All use of the Correlator Monitor and Control System will be through the VCI or Master Correlator Control Computer.”  
**Architectural Impact:**  
- Requires a dedicated gateway/adapter component (VCI) that mediates all access paths (system-to-system and GUI).  
- Encourages contract/interface standardization and shared table structures for configuration.  
- Centralizes access control and auditing points.  
**Quality Attributes Affected:** Security, Modifiability, Interoperability, Testability  
**Architectural Constraints:** Must provide a VCI software entity that performs translation and serves as the primary access gateway.  
**Rationale:** A single gateway/translation interface is a major architectural constraint and cross-cutting integration point.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-010, FR-011, FR-037, NFR-014  
- **Conflicts with:** None identified  
---

[ASR-003]: Secondary virtual network for backend data delivery  
**Description**: “Specific data sets required by the Backend Data Processing System will be provided… over a secondary virtual network.”  
**Architectural Impact:**  
- Requires multi-network design and routing/segregation of traffic classes (control/monitor vs backend data).  
- Influences deployment topology, NIC counts, and data pipeline separation.  
**Quality Attributes Affected:** Performance, Reliability, Security  
**Architectural Constraints:** Must implement a secondary virtual network path dedicated to backend data sets.  
**Rationale:** Network topology and traffic segregation are foundational architectural decisions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-020, NFR-021  
- **Conflicts with:** None identified  
---

[ASR-004]: Redundant master with state replication and failover by rerouting communications  
**Description**: “It is intended that both primary and secondary Master… maintain full… state information such that any hard failure in the primary node can be corrected by simply rerouting… communications to the secondary.”  
**Architectural Impact:**  
- Requires state replication strategy, failover mechanism, and consistent state model.  
- Drives decisions on shared storage vs replicated storage, heartbeat/health checks, and switchover procedures.  
**Quality Attributes Affected:** Availability, Reliability, Recoverability  
**Architectural Constraints:** Must support active/standby (or equivalent) master redundancy with full state maintenance and communication reroute failover.  
**Rationale:** High-availability failover with state continuity is a major architectural driver and risk area.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003, NFR-009, FR-019  
- **Conflicts with:** NFR-020  
---

[ASR-005]: Network and physical interface constraints (Ethernet 100Mbps+, segmentation, fiber for shielded room)  
**Description**: “The interface between the CMIB, Master… and Correlator Power Control Computer shall be Ethernet of 100 Mbits/sec or better…”; “networks shall be on separate physical interfaces.”; “Pathways penetrating the correlator shielded room shall be fiber optic or other low RFI material…”  
**Architectural Impact:**  
- Constrains hardware selection (NICs/switches/media), cabling, and physical deployment.  
- Enforces network segmentation and influences security zoning and traffic engineering.  
**Quality Attributes Affected:** Performance, Security, Reliability, Compliance (RFI)  
**Architectural Constraints:** Must use Ethernet (≥100 Mbps) for specified links; must segment networks on separate physical interfaces; must use fiber/low-RFI media for shielded-room penetrations.  
**Rationale:** Hard technology and topology constraints directly shape the system’s physical and logical architecture.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-020, NFR-021  
- **Conflicts with:** NFR-019  
---

[ASR-006]: Deterministic real-time behavior to prevent data loss/corruption/overflows  
**Description**: “...responding to correlator hardware inputs in a deterministic fashion with sufficient performance to avoid data loss, corruption or overflows.”  
**Architectural Impact:**  
- Drives partitioning of real-time vs non-real-time workloads (e.g., slave layer), scheduling, OS choice, and bounded-latency communication patterns.  
- Influences buffering/queueing, backpressure, and watchdog/recovery design.  
**Quality Attributes Affected:** Real-time Performance, Reliability, Availability  
**Architectural Constraints:** Must implement deterministic processing paths for hardware input handling; architecture must support bounded latency.  
**Rationale:** Real-time determinism is a strong architectural driver with significant design trade-offs.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-002, NFR-006  
- **Conflicts with:** NFR-020  
---

[ASR-007]: Self-monitoring with automated remediation across multiple failure modes  
**Description**: “The Correlator Monitor and Control System shall be self-monitoring… detecting, reporting on and automatically taking action to remedy or lessen the impact of… [listed abnormal conditions].”  
**Architectural Impact:**  
- Requires pervasive health instrumentation, fault detection, and automated recovery workflows across components.  
- Implies centralized monitoring/alerting, policy engine/rules, and safe actuation mechanisms.  
**Quality Attributes Affected:** Reliability, Availability, Operability  
**Architectural Constraints:** Must implement health monitoring and automated mitigation for the specified condition classes.  
**Rationale:** Cross-cutting resilience requirement affecting most components and interfaces.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-038, NFR-024, NFR-009  
- **Conflicts with:** NFR-020  
---

[ASR-008]: Security architecture: unique identification, secure login, RBAC-like privileges, and audit logging  
**Description**: “The Correlator Monitor and Control System needs a robust security mechanism…”; “All users… must be uniquely identified…”; “All login attempts shall be done in a secure manner.”; “all attempts to access… should be logged.”; “authority to grant and revoke privileges on a per-user basis…” Supplement: “All operational access is governed under RBAC policy. Any elevated/diagnostic access is restricted by per-incident token expiring within 2 hours and includes mandatory audit logging.” (Derived from ASR-008; Next action: Align FR-005, FR-022, and RBAC model to one consistent set of security policy rules.)  
**Architectural Impact:**  
- Requires centralized identity/authn/authz services, role/privilege model, secure remote access mechanisms, and audit log pipeline.  
- Affects all interfaces (VCI, remote logins, tooling) and operational workflows (admin functions, lockout/blocking).  
**Quality Attributes Affected:** Security, Auditability, Compliance, Operability  
**Architectural Constraints:** Must enforce unique user identity, secure authentication, per-user privilege properties, admin management functions, and access-attempt logging.  
**Rationale:** Cross-cutting security and audit requirements strongly constrain design and are high risk if incorrect.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041 through FR-050, NFR-014, NFR-015  
- **Conflicts with:** FR-005, FR-022 (ease/availability of access vs security controls)  
---

[ASR-009]: Standalone operation during external network failures (local boot + continued processing)  
**Description**: “...boot and run in a stand-alone configuration… CMIBs… run without any communication outside…” and “shall be able to continue processing… until the queues… are exhausted and external communications are restored.” Add: “Offline operation supported for at least 96 hours at peak load.” (Derived from ASR-009; Next action: Propagate minimum storage/queue sizing from FR/NFR to this ASR.)  
**Architectural Impact:**  
- Requires local persistence/configuration, queueing, and degraded-mode operation without upstream dependencies.  
- Influences data spooling, state management, and reconnection/synchronization behavior.  
**Quality Attributes Affected:** Resilience, Availability, Reliability  
**Architectural Constraints:** Must support standalone boot/run and continued event processing during external comms loss (queue-based).  
**Rationale:** Offline-capable behavior is a major architectural driver affecting storage, messaging, and control flows.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-013, FR-013, FR-039  
- **Conflicts with:** NFR-020  
---

[ASR-010]: Hardware/OS platform constraints for CMIB and master/power control computers (COTS OS, near real-time, watchdog, interfaces)  
**Description**: “The CMIB shall contain 64 Mbytes or greater of SDRAM… 100BaseT… capacity to boot and run a generic COTS operating system in a near real-time environment…”; “The Master… shall be a high availability… general-purpose computer capable of supporting multiple Ethernet interfaces, COTS operating systems…”; “Each computer system… shall have a hardware based watchdog timer…” Acceptance: “System upgrade path is part of every annual design review and includes backward compatibility plan.” (Derived from ASR-010; Next action: Add explicit review/upgrade protocol to requirement.)  
**Architectural Impact:**  
- Constrains hardware selection, OS/runtime environment, and deployment packaging.  
- Drives design for near-real-time OS behavior on CMIB and HA characteristics on master/power control nodes.  
**Quality Attributes Affected:** Performance, Availability, Portability (constrained), Maintainability  
**Architectural Constraints:** Must use specified minimum CMIB hardware capabilities; must support COTS OS on nodes; must include hardware watchdog timers; must support multiple Ethernet interfaces on master.  
**Rationale:** Hard platform constraints and HA/real-time requirements directly shape the system architecture and procurement.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-020, NFR-006, NFR-009  
- **Conflicts with:** NFR-019 (future expandability may be limited by fixed platform constraints)  
---