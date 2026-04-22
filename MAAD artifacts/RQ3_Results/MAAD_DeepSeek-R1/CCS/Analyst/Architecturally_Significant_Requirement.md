# Architecturally Significant Requirements Results:
[ASR-001]: Master/Slave Architecture  
**Description**: The system shall be designed as a Master/Slave network with a Master computer coordinating intelligent hardware control processors.  
**Architectural Impact:** Drives decomposition into Master (network/aggregation) and Slave (real-time control) layers, isolating deterministic tasks from chaotic loads.  
**Quality Attributes Affected:** Performance, Reliability  
**Architectural Constraints:** Mandates Master/Slave topology; real-time processing in slaves, quasi-real-time in Master.  
**Rationale:** High-impact decision for scalability, fault isolation, and meeting real-time/data-loss constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-002  
---

[ASR-002]: Virtual Correlator Interface (VCI) Gateway  
**Description**: All system access shall be through the VCI or Master Correlator Control Computer; the VCI translates configurations into goal-oriented hardware tables.  
**Architectural Impact:** Centralizes external interactions, translation, and security at a single ingress point (VCI).  
**Quality Attributes Affected:** Security, Interoperability  
**Architectural Constraints:** Requires VCI as the sole translation boundary and access gateway.  
**Rationale:** Critical for integration, security enforcement, and abstracting hardware complexity.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001  
---

[ASR-003]: Redundant Stateful Masters  
**Description**: Primary/secondary Master systems shall maintain full state continuity; failures reroute communications to secondary.  
**Architectural Impact:** Requires state replication, failover mechanisms, and versioning for high availability.  
**Quality Attributes Affected:** Availability, Reliability  
**Architectural Constraints:** Mandates redundant Masters with synchronized state.  
**Rationale:** Business-critical (data loss if unavailable); ensures continuity during failures.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---

[ASR-004]: Network Segmentation  
**Description**: Master-CMIB, Master-Power Control, and Master-VLA networks shall use separate physical interfaces.  
**Architectural Impact:** Isolates traffic classes, requiring dedicated NICs and segmented networks.  
**Quality Attributes Affected:** Performance, Security  
**Architectural Constraints:** Physically segregated interfaces for control/operations/backend traffic.  
**Rationale:** Prevents interference, meets RFI specs, and enforces security boundaries.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---

[ASR-005]: Standalone Operation  
**Description**: Must queue min 24h data at 2x avg rate; alert and block new configs when storage >95% full.  
**Architectural Impact:** Demands local storage, event queueing, and spooling for offline resilience.  
**Quality Attributes Affected:** Availability, Reliability  
**Architectural Constraints:** Systems must operate autonomously during network failures.  
**Rationale:** Ensures operation during upstream outages (prevents data loss).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006  
---

[ASR-006]: Full Observability  
**Description**: The system shall provide system-wide access to all correlator states and time-synchronous/on-demand data.  
**Architectural Impact:** Requires centralized logging, filtering, and timestamped messaging across layers.  
**Quality Attributes Affected:** Maintainability, Usability  
**Architectural Constraints:** Implement machine-readable schemas for messages (e.g., protobuf).  
**Rationale:** Cross-cutting need for diagnostics; informs monitoring/alerting structures.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003  
---

[ASR-007]: Automated Hot-Swap Recovery  
**Description**: Hot-swapped modules must: auto-detect/reconfigure within 3 minutes (0 data loss) with human intervention only for physical exchange.  
**Architectural Impact:** Forces modular hardware design and IP-based identification.  
**Quality Attributes Affected:** Maintainability, Availability  
**Architectural Constraints:** Full auto-reconfiguration within 3 minutes post-swap.  
**Rationale:** Minimizes downtime; critical for high-uptime goals.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-008  
---

[ASR-008]: Cryptographic Security Controls  
**Description**: Audit logs stored on encrypted volumes/S3 with server-side encryption; accessible only to 'audit' role users.  
**Architectural Impact:** Mandates RBAC, cryptographic protocols, and monitored access patterns.  
**Quality Attributes Affected:** Security  
**Architectural Constraints:** Requires encrypted auth and secure log retention.  
**Rationale:** Cross-cutting security affecting all access points and tooling.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-011, FR-012  
---

[ASR-009]: Durable Spooling  
**Description**: Monitor data shall be spooled during network loss to prevent data loss.  
**Architectural Impact:** Requires local buffering (e.g., 24+ hour spools) and overrun alerting.  
**Quality Attributes Affected:** Reliability, Availability  
**Architectural Constraints:** Implements durable storage/queues in CMIB/Master layers.  
**Rationale:** Addresses temporary outage resilience; impacts data-handling design.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006, ASR-005  
---