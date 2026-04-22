# Architecturally Significant Requirements Results:
[ASR-001]: Master/Slave Network Topology
**Description**: The Correlator Monitor and Control System will be designed and implemented as a Master/Slave network with one computer system coordinating the activities of a number of intelligent hardware control processors.
**Architectural Impact:**  
This requirement dictates the fundamental component decomposition of the system into a central coordinator (Master) and distributed controllers (Slaves/CMIBs). It influences communication patterns (command/response vs. peer-to-peer) and dictates that the Master handles external interfaces while Slaves handle hardware-specific control.
- **Component/Module Decomposition:** Distinct Master and Slave roles.
- **Communication Patterns:** Centralized coordination.

**Quality Attributes Affected:**  
Scalability, Reliability, Maintainability

**Architectural Constraints:**  
Must implement a Master/Slave topology; cannot use peer-to-peer or fully distributed control for hardware coordination.

**Rationale:**  
This is a high-level design decision that constrains the entire system structure. It addresses the need for scalable control of multiple hardware processors while maintaining a single point of coordination for external systems.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Config Translation), FR-002 (Data Transfer)
- **Conflicts with:** None
---
[ASR-002]: Virtual Correlator Interface (VCI) Gateway
**Description**: The gateway to the correlator will be through the Virtual Correlator Interface which will exist as a software entity on the Correlator Monitor and Control System. All use of the Correlator Monitor and Control System will be through the VCI or Master Correlator Control Computer.
**Architectural Impact:**  
Establishes a strict integration boundary and single entry point for all external interactions. This centralizes security, translation logic, and access control, preventing direct external access to internal subsystems (Slaves/CMIBs).
- **Integration Boundary:** VCI acts as the facade/adapter.
- **Security:** Centralized choke point for authentication/authorization.

**Quality Attributes Affected:**  
Security, Interoperability, Modularity

**Architectural Constraints:**  
All external configuration and control must pass through the VCI layer; direct hardware access from outside is prohibited.

**Rationale:**  
Critical for abstraction and security. It modularizes the correlator system within the larger VLA environment and ensures consistent configuration translation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Config Translation), FR-008 (GUI Config)
- **Conflicts with:** None
---
[ASR-003]: Redundant Primary/Secondary Master Control
**Description**: It is intended that both primary and secondary Master Correlator Control Computer systems maintain full Correlator Monitor and Control System state information such that any hard failure in the primary node can be corrected by simply rerouting Monitor and Control System communications to the secondary.
**Architectural Impact:**  
Requires a state replication mechanism between Master nodes and a failover routing strategy. This impacts the data architecture (shared state) and network architecture (rerouting capabilities).
- **Data/Communication Patterns:** State replication/synchronization.
- **Availability Strategy:** Active/Passive or Active/Active failover.

**Quality Attributes Affected:**  
Availability, Reliability

**Architectural Constraints:**  
Must deploy at least two Master nodes; state must be fully replicated; failover must be automatic or seamless via rerouting.

**Rationale:**  
High business value and risk mitigation. The correlator is a critical component in the astronomical data path; unavailability results in data loss. Redundancy is essential for uptime.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-015 (Master State Replication), FR-016 (Failover Rerouting)
- **Conflicts with:** None
---
[ASR-004]: Separation of Real-time and Network-chaotic Loads
**Description**: This topology will place the real-time computing requirements in the slave layer and the quasi real-time, network-chaotic loads into the master layer.
**Architectural Impact:**  
Drives a layered architecture where performance-critical paths are isolated from variable network loads. This influences processor selection (Real-time OS for Slaves) and network traffic shaping.
- **Component/Module Decomposition:** Separation of concerns based on timing constraints.
- **Technology Selection:** Real-time OS for Slaves, General Purpose for Master.

**Quality Attributes Affected:**  
Performance, Reliability, Determinism

**Architectural Constraints:**  
Slaves must handle deterministic hardware inputs; Masters must absorb network variability.

**Rationale:**  
Technical risk mitigation. Mixing real-time hardware control with chaotic network traffic risks data loss or corruption. Isolation ensures determinism.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-010 (CMIB OS), NFR-013 (Processor Determinism)
- **Conflicts with:** None
---
[ASR-005]: Network Segmentation
**Description**: The Master Correlator Control Computer-CMIB, Master Correlator Control Computer-Correlator Power Control Computer, and Master Correlator Control Computer-VLA Expansion Project Monitor and Control System networks shall be on separate physical interfaces.
**Architectural Impact:**  
Requires multiple network interface cards (NICs) on the Master and distinct physical network segments. This impacts deployment topology and security zoning.
- **Deployment Topology:** Segmented networks (Control, Power, Ops).
- **Security:** Physical isolation of traffic classes.

**Quality Attributes Affected:**  
Security, Reliability, Performance

**Architectural Constraints:**  
Cannot use a single shared network for all traffic types; must use separate physical interfaces.

**Rationale:**  
Security and Reliability. Prevents external network traffic from interfering with critical control loops and limits the blast radius of network failures or attacks.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Network Segmentation), NFR-001 (Network Speed)
- **Conflicts with:** None
---
[ASR-006]: Autonomous Recovery and Self-Healing
**Description**: The Correlator Monitor and Control System shall monitor correlator and correlator subsystem health and take corrective action autonomously to recover from hardware and computing system faults.
**Architectural Impact:**  
Requires the inclusion of health monitoring agents and recovery logic within the control loops. This adds complexity to the state machine design of the controllers.
- **Cross-cutting Concerns:** Monitoring, Logging, Recovery Logic.
- **Component/Module Decomposition:** Health monitoring subsystems.

**Quality Attributes Affected:**  
Availability, Reliability, Maintainability

**Architectural Constraints:**  
System must be designed to detect faults and trigger recovery scripts/actions without human intervention.

**Rationale:**  
High availability requirement. Manual intervention is too slow for certain faults; autonomous recovery minimizes downtime and data loss.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003 (Autonomous Health Monitoring), FR-012 (Hardware Recovery)
- **Conflicts with:** None
---
[ASR-007]: Offline/Stand-alone Operation Capability
**Description**: The Master Correlator Control Computer shall have all required disk and file system facilities installed locally such that the EVLA Correlator Monitor and Control System can boot and run in a stand-alone configuration.
**Architectural Impact:**  
Dictates local storage architecture and dependency management. The system cannot rely on network-mounted file systems or external services for core boot/operation.
- **Data/Communication Patterns:** Local caching/queueing of commands.
- **Deployment Topology:** Self-contained nodes.

**Quality Attributes Affected:**  
Availability, Reliability

**Architectural Constraints:**  
Must operate independently of the external VLA Monitor and Control System network during outages.

**Rationale:**  
Continuity of operations. The correlator must continue processing even if the upstream control network fails (FR-026).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010 (Monitor Data Spooling), FR-026 (Queue Processing)
- **Conflicts with:** None
---
[ASR-008]: Comprehensive Security and Audit Architecture
**Description**: The Correlator Monitor and Control System needs a robust security mechanism in place so that unauthorized users are not allowed access. All attempts to access the EVLA Correlator Monitor and Control System should be logged.
**Architectural Impact:**  
Requires integration of authentication, authorization, and logging subsystems across all access points (VCI, Remote Login, GUI). This is a cross-cutting concern affecting all layers.
- **Cross-cutting Concerns:** Security, Logging, Audit.
- **Technology Selection:** Authentication protocols, Logging frameworks.

**Quality Attributes Affected:**  
Security, Observability

**Architectural Constraints:**  
All access must be authenticated and logged; role-based access control (RBAC) must be implemented.

**Rationale:**  
Security is mandatory for remote access and system integrity. Audit trails are required for accountability and troubleshooting.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-020 (Access Logging), FR-021 (User Management)
- **Conflicts with:** FR-005 (System Access for Debugging)
---
[ASR-009]: Hardware Watchdog and UPS Integration
**Description**: Each computer system in the Correlator Monitor and Control System shall have a hardware based watchdog timer configured to reboot the EVLA Correlator Monitor and Control System in the case of a system hang. UPS devices need the ability to signal the Correlator Monitor and Control System when a power outage has occurred.
**Architectural Impact:**  
Requires hardware-level integration for reliability. Software architecture must handle watchdog signals and UPS shutdown events gracefully.
- **Technology Selection:** Hardware watchdogs, UPS communication protocols.
- **Cross-cutting Concerns:** Power Management, System Reliability.

**Quality Attributes Affected:**  
Reliability, Availability

**Architectural Constraints:**  
Must implement hardware watchdogs on all nodes; must integrate UPS signaling into the shutdown sequence.

**Rationale:**  
Critical for system stability. Prevents hung systems from remaining offline and ensures safe shutdown during power loss to prevent data corruption.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-022 (Watchdog Reboot), FR-023 (UPS Signaling)
- **Conflicts with:** None
---