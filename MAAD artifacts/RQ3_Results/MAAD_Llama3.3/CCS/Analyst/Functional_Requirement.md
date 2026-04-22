# Functional Requirements Results:
[FR-001]: Correlator Configuration
**Description**: Configuration input SHALL comply with 'schema_v3.xsd' (provided at repo/url) and return error codes as per RFC yyyy Section 5.2 (attached). 
**Rationale:** This requirement describes a function of the system, specifically how it configures the correlator hardware.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Data Processing and Transfer
**Description**: The system shall process dynamic control data conforming to [ControlDataSchema v1], and output monitor data conforming to [MonitorDataSchema v2]; all errors shall return error codes per RFC XYZ.
**Rationale:** This requirement describes a behavior of the system, specifically how it handles data.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-003]: Correlator Health Monitoring
**Description**: System SHALL detect HW/SW faults and automatically recover from 95% of recoverable issues within 60 seconds; all incidents logged for post-mortem.
**Rationale:** This requirement describes a task of the system, specifically how it monitors and maintains the health of the correlator.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-004]: Real-time Data Processing
**Description**: The Correlator Monitor and Control System shall perform limited amounts of real-time data processing and probing such as providing tools to collect and display auto correlation products.
**Rationale:** This requirement describes a function of the system, specifically how it processes data in real-time.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-005]: System Access
**Description**: Acceptance: All unauthorized login attempts must be denied within 2s, logged with timestamp, source IP, username.
**Rationale:** This requirement describes a behavior of the system, specifically how it provides access for testing and debugging.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-006]: User Interface
**Description**: Graphical UI shall support all configuration and monitor features, provide response within 2s, and achieve a SUS score of 80+ in user testing.
**Rationale:** This requirement describes a function of the system, specifically how it provides a user interface.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-007]: Error Messaging
**Description**: Error and status messages will be provided in a concise time/location referenced format to upper system levels in a content controllable manner.
**Rationale:** This requirement describes a behavior of the system, specifically how it handles error messaging.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-008]: Configuration Translation
**Description**: Correlator configurations and control instructions will be received from the VLA Expansion Project Monitor and Control System system in a form suitable for translation by the Master Correlator Control Computer.
**Rationale:** This requirement describes a function of the system, specifically how it translates configurations and control instructions.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-009]: Data Provision
**Description**: Specific data sets required by the Backend Data Processing System will be provided in a timely and robust fashion over a secondary virtual network.
**Rationale:** This requirement describes a behavior of the system, specifically how it provides data to the Backend Data Processing System.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-010]: System Monitoring
**Description**: The Correlator Monitor and Control System shall be self-monitoring, capable of detecting, reporting on, and automatically taking action to remedy or lessen the impact of abnormal conditions.
**Rationale:** This requirement describes a function of the system, specifically how it monitors itself.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-011]: System Maintenance
**Description**: All system processing and interconnect hardware shall be readily accessible for maintenance, repair, replacement, and reconfiguration.
**Rationale:** This requirement describes a behavior of the system, specifically how it supports maintenance activities.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-012]: Software Tools
**Description**: Provide command-line and GUI tools for CMIB access, each with RBAC and full audit logging; each tool shall be tested to ensure access levels per role.
**Rationale:** This requirement describes a function of the system, specifically how it provides software tools for user assistance.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-013]: Remote Access
**Description**: Audit logs for remote access are handled and stored as per NFR-004; do not duplicate retention logic.
**Rationale:** This requirement describes a behavior of the system, specifically how it provides remote access.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-014]: Security Mechanism
**Description**: All admin access (SSH, web UI, API) must use TLS 1.3; full audit logs of access/changes, retained for 1 year; logs reviewed monthly by security admin.
**Rationale:** This requirement describes a function of the system, specifically how it provides security.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-015]: User Authentication
**Description**: Define roles {Admin, Operator, Maintainer}; each user must be assigned one; all role change events logged.
**Rationale:** This requirement describes a behavior of the system, specifically how it authenticates and authorizes users.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---