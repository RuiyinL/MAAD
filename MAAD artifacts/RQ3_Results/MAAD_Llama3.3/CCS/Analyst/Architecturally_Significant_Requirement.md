# Architecturally Significant Requirements Results:
[ASR-001]: Master/Slave Architecture
**Description**: Within 5s after master node loss, a standby slave assumes master with full config state per Table X, with test plan validating all data continuity.
**Architectural Impact**: This requirement influences the overall system architecture, specifically the decomposition into master and slave components, and the communication patterns between them.
**Quality Attributes Affected**: Performance, Reliability, Scalability
**Architectural Constraints**: The system must be designed as a Master/Slave network.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's performance, reliability, and scalability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[ASR-002]: Virtual Correlator Interface
**Description**: The gateway to the correlator will be through the Virtual Correlator Interface which will exist as a software entity on the Master Correlator Control Computer.
**Architectural Impact**: This requirement influences the system's integration boundary, specifically the interface between the Correlator Monitor and Control System and the correlator hardware.
**Quality Attributes Affected**: Performance, Security
**Architectural Constraints**: The system must provide a Virtual Correlator Interface as the single external gateway to the correlator.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's performance and security.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-008
- **Conflicts with:** None
---
[ASR-003]: Redundancy
**Description**: Failover to backup node tested monthly, must complete in ≤60s and pass functional regression suite.
**Architectural Impact**: This requirement influences the system's reliability and availability, specifically the use of redundancy and modularity to ensure continued operation in the event of component failures.
**Quality Attributes Affected**: Reliability, Availability
**Architectural Constraints**: The system must be designed with redundancy and modularity in critical areas.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's reliability and availability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-011
- **Conflicts with:** None
---
[ASR-004]: Real-time Requirements
**Description**: All hardware inputs timestamped at ingest, with system producing latency/jitter metrics every 30s to Prometheus/Grafana for alerting.
**Architectural Impact**: This requirement influences the system's performance, specifically the need for real-time responses to hardware inputs.
**Quality Attributes Affected**: Performance, Reliability
**Architectural Constraints**: The system must be designed to respond to hardware inputs in real-time.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's performance and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-004
- **Conflicts with:** None
---
[ASR-005]: Security Mechanism
**Description**: VCI enforces RBAC per Table X; all access attempts, approvals, and role changes are logged to central syslog.
**Architectural Impact**: This requirement influences the system's security, specifically the need for a robust security mechanism to prevent unauthorized access.
**Quality Attributes Affected**: Security
**Architectural Constraints**: The system must be designed with a robust security mechanism.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's security.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, FR-015
- **Conflicts with:** None
---
[ASR-006]: Network Requirements
**Description**: The interface between the CMIB, Master Correlator Control Computer, and Correlator Power Control Computer shall be Ethernet of 100 Mbits/sec or better data rate.
**Architectural Impact**: This requirement influences the system's communication patterns, specifically the use of Ethernet for communication between components.
**Quality Attributes Affected**: Performance, Reliability
**Architectural Constraints**: The system must use Ethernet for communication between components.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's performance and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[ASR-007]: Data Storage
**Description**: Node storage shall be verified to handle peak data logging, buffering, and recovery within 24h of simulated failover.
**Architectural Impact**: This requirement influences the system's data storage, specifically the need for local disk and file system facilities.
**Quality Attributes Affected**: Performance, Reliability
**Architectural Constraints**: The system must have local disk and file system facilities.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's performance and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-011
- **Conflicts with:** None
---
[ASR-008]: Access Control
**Description**: All users of the Correlator Monitor and Control System must be uniquely identified, and access shall be restricted based on user roles.
**Architectural Impact**: This requirement influences the system's security, specifically the need for access control based on user roles.
**Quality Attributes Affected**: Security
**Architectural Constraints**: The system must be designed with access control based on user roles.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's security.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015
- **Conflicts with:** None
---
[ASR-009]: Error Handling
**Description**: Error and status messages will be provided in a concise time/location referenced format to upper system levels in a content controllable manner.
**Architectural Impact**: This requirement influences the system's error handling, specifically the need for concise and controllable error messages.
**Quality Attributes Affected**: Reliability, Maintainability
**Architectural Constraints**: The system must be designed to provide concise and controllable error messages.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's reliability and maintainability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** None
---
[ASR-010]: System Monitoring
**Description**: The Correlator Monitor and Control System shall be self-monitoring, capable of detecting, reporting on, and automatically taking action to remedy or lessen the impact of abnormal conditions.
**Architectural Impact**: This requirement influences the system's monitoring, specifically the need for self-monitoring and automatic remediation.
**Quality Attributes Affected**: Reliability, Maintainability
**Architectural Constraints**: The system must be designed to be self-monitoring and capable of automatic remediation.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the system design and has a measurable impact on the system's reliability and maintainability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** None
---