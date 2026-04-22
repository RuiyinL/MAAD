# Architecturally Significant Requirements Results:

[ASR-001]: Hierarchical Control Topology
**Description**: Commands are only forwarded from superior units to inferior ones. This prevents a lower level unit from changing the state of a device which is controlled by either a higher level unit, or by a peer unit. The TSU is superior to the FCUs which are superior to the DCUs. Communications from the TMC to the DCU controllers is through the FCU controller.
**Architectural Impact:**  
Dictates a strict tree-based component hierarchy (TSU > FCU > DCU) for command routing. Prevents peer-to-peer control commands, requiring a centralized or parent-mediated communication pattern.
- component/module decomposition
- data/communication patterns
**Quality Attributes Affected:**  
Safety, Security, Reliability
**Architectural Constraints:**  
Command flow must be unidirectional (Top-Down); Network topology must reflect physical hierarchy (TMC-FCU-DCU).
**Rationale:**  
This is a high-risk safety constraint that fundamentally defines the system's communication architecture to prevent race conditions and unauthorized control state changes.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance)
- **Conflicts with:** None
---

[ASR-002]: Multi-Layer Safety Screening Architecture
**Description**: Safety screening of device commands shall be multi-layered. Safety screening shall be applied to all device commands at the originating control unit, and at all subordinate control units to which the device command or any of its subordinate device commands may be forwarded. Safety screening shall always be applied to any device command, or command step, by any control unit which directly operates the target entrance closure device(s). Total latency for command propagation and safety screening shall not exceed 4 seconds (including all unit hops and local checks) under nominal load; if exceeded, affected commands shall abort and log operator-visible error. Metric: command_propagation_latency (start: GUI cmd issue, end: field device ACK/log event); Alert if >2s (normal) or >4s (failover). Next action: Specify instrumentation and monitoring targets; include SRE acceptance criteria.
**Architectural Impact:**  
Requires distributed validation logic across all nodes (TSU, FCU, DCU). Each node must possess safety rule logic and configuration data. Introduces latency trade-offs for safety assurance.
- component/module decomposition
- cross-cutting concerns (security, logging, transactions)
**Quality Attributes Affected:**  
Safety, Reliability, Performance
**Architectural Constraints:**  
Safety rules must be replicated to all control units; Validation must occur at every hop in the command chain; Total latency ≤4s including all hops, else fail-safe abort.
**Rationale:**  
Critical safety requirement to prevent catastrophic events (wrong-way openings). The distributed nature impacts latency and data synchronization architecture.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009 (Safety Rule Validation), NFR-002 (Performance)
- **Conflicts with:** NFR-002 (Strict 2s latency may be challenged by multi-layer checks)
---

[ASR-003]: Degraded Mode and Failover Architecture
**Description**: If the TMC workstations or network server fails, resulting in loss of field status at the TMC, alternate control shall be at FCU South or FCU North. If FCUs North and South both fail: Alternate control units: Direct control at DCUs 1-5. The operator shall be able to connect a lap top computer at the DCUs and operate the devices.
**Architectural Impact:**  
Requires redundant control paths and local autonomy for field controllers (FCU/DCU). Field units must be capable of standalone operation (thick clients/controllers) rather than thin clients.
- scalability strategies
- component/module decomposition
**Quality Attributes Affected:**  
Availability, Reliability, Fault Tolerance
**Architectural Constraints:**  
Field controllers must host full control logic and configuration locally; Network must support direct local access (dial-up/laptop) bypassing TMC.
**Rationale:**  
Ensures 24/7 availability (NFR-001) despite central system failures. Drives the decision for intelligent field controllers vs. simple I/O modules.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (System Availability)
- **Conflicts with:** None
---

[ASR-004]: Non-Volatile Memory Integrity Check (SHA-256)
**Description**: In each FCU and DCU in the system, the following items shall be replicated from the central database server and maintained in non-volatile, non-removable memory: Reversible Lanes Operating Logic, Control Sequences, and Rule Sets. The system shall use SHA-256 or stronger (FIPS 180-4 compliant) for all integrity and password hashing operations. Integrity check status (cv_integrity_status) shall be measured daily on each field controller; failures auto-alerted to ops and logged persistently in audit log. Next action: Update SRS to remove MD5 references, replace with SHA-256+; align security controls and acceptance criteria.
**Architectural Impact:**  
Requires specific storage architecture (non-volatile memory) for critical logic in field units. Mandates a specific cryptographic module (SHA-256/FIPS) for integrity verification, impacting security library choices.
- technology or framework selection
- cross-cutting concerns (security, logging, transactions)
**Quality Attributes Affected:**  
Security, Integrity, Safety
**Architectural Constraints:**  
Use of SHA-256 or higher (FIPS-180-4); Storage of logic in non-volatile memory; Daily verification daemon process required; Metric cv_integrity_check.
**Rationale:**  
Prevents tampering or corruption of safety-critical logic in the field. The specific algorithm choice constrains the security implementation.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Data Integrity)
- **Conflicts with:** Modern Security Standards (MD5 is deprecated, but mandated by SRS)
---

[ASR-005]: Network Segmentation and External Interface
**Description**: The RLCS will also allow for remote access through a firewall via outside telecommunications networks by authorized users. The RLCS will provide access to system status data, to external systems through a firewall. This will be a one way data transfer to a computer outside of the RLCS network. RLCS workstations and controllers will reside on a private network.
**Architectural Impact:**  
Defines network zones (Private RLCS Network vs. External). Requires firewall components and a DMZ or proxy server for one-way data export.
- data/communication patterns
- technology or framework selection
**Quality Attributes Affected:**  
Security, Safety
**Architectural Constraints:**  
Physical or logical separation of RLCS network; One-way data flow enforcement for external exports; Firewall presence mandatory.
**Rationale:**  
Protects the safety-critical control network from external threats while allowing necessary data sharing. Impacts network topology and security gateway design.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006 (External Data Export)
- **Conflicts with:** None
---

[ASR-006]: Single Operator Command Control (Leasing)
**Description**: Only one 'operator' may be logged onto the system at any given time. If command control is enabled by another user, and the logging in user is of higher security, the logging in user shall be requested to accept or deny command control. If another user is logged in with command control and the new user takes command control, the other user is notified.
**Architectural Impact:**  
Requires a session management or "leasing" mechanism for command authority. Prevents concurrent modification of system state by multiple actors.
- cross-cutting concerns (security, logging, transactions)
- component/module decomposition
**Quality Attributes Affected:**  
Safety, Security, Usability
**Architectural Constraints:**  
Mutual exclusion lock on command control; Notification system for takeover events; Hierarchy-based pre-emption logic.
**Rationale:**  
Prevents conflicting commands that could lead to unsafe lane configurations. Centralizes authority for safety-critical actions.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (User Authentication)
- **Conflicts with:** None
---

[ASR-007]: Database Technology Stack
**Description**: A commercial off-the-shelf database management system shall be used for this function. RLCS persistence and reporting layers must use actively supported, DoT-approved COTS DBMS/Reporting solutions; Oracle 8i/HPUX/Solaris/NT/OS-9 are referenced only as legacy; update baseline per IT/InfoSec standards. Next action: Update stack/tooling language for modern/future-proof deployment; recruit IT/security for review.
**Architectural Impact:**  
Constrains the persistence layer to specific COTS RDBMS and OS based on current DoT approved/supported versions. Impacts driver selection, connection pooling, and deployment environment.
- technology or framework selection
**Quality Attributes Affected:**  
Maintainability, Portability, Performance
**Architectural Constraints:**  
Must use DoT-approved and current supported versions; COTS reporting tools (Crystal Reports/Brio or equivalents).
**Rationale:**  
Standardizes the data layer for support and integration with existing agency infrastructure. Limits technology choices for the backend.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Maintainability)
- **Conflicts with:** Modern Cloud-Native Architectures (Legacy OS/DB constraints)
---