# Functional Requirements Results:
[FR-001]: Configuration Reception and Translation
**Description**: The Correlator Monitor and Control System shall receive configuration information from the VLA Expansion Project Monitor and Control System system and translate this info into a physical correlator hardware configuration.

**Rationale:**  Describes the core input-output transformation behavior of the system (receiving external config and translating to hardware config).

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014 (Processor Deadlines), ASR-002 (VCI Gateway)
- **Conflicts with:** None
---
[FR-002]: Dynamic Data Processing and Transfer
**Description**: Control data must conform to schema defined in technical appendix; monitor data output in JSON with fields [timestamp, source_id, status, value]; process triggered upon valid data arrival. Acceptance: data validated against schema before processing.

**Rationale:**  Defines the primary data handling function of the system.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Network Speed), NFR-015 (Deterministic Response)
- **Conflicts with:** None
---
[FR-003]: Autonomous Health Monitoring and Correction
**Description**: Upon detection of hardware/OS fault (processor failure, OS hang, temperature deviation, communication failure), corrective action (reboot, reconfigure, alert) must occur within 60s, verifiable via log event ID. Acceptance is auto-recovery logged within 60 seconds.

**Rationale:**  Describes a specific behavior of monitoring and automatic reaction to faults.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Autonomous Recovery)
- **Conflicts with:** None
---
[FR-004]: Real-time Data Processing and Probing
**Description**: FITS files must have headers [OBSERVER, DATE-OBS, TELESCOP] and contain fields [lag, amplitude, phase] in 32-bit float format; CSV requires columns [timestamp, baseline, correlation_value]. Auto correlation products shall be exportable in FITS and CSV format and visualized in a GUI with 1-second update interval. Acceptance: Exported FITS passes 'fitsvalidator X'; GUI refreshes correlation plot within 1s in 90% of test runs.

**Rationale:**  Specifies a functional task related to data analysis and tooling.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-015 (Deterministic Response)
- **Conflicts with:** None
---
[FR-005]: System Access for Testing and Debugging
**Description**: Remote access must pass MFA or SSH public key authentication, with successful login completion in <30 seconds under normal network conditions. 'Easy' access is defined as requiring no more than two authentication steps. All login attempts audited. Acceptance: Each login attempt (success/failure) logs [user, method, timestamp, source IP] to audit.log; penetration test validates completeness.

**Rationale:**  Defines a function enabling user interaction for maintenance purposes.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Security Architecture)
- **Conflicts with:** NFR-021 (Security Mechanism)
---
[FR-006]: Correlator State Access
**Description**: States [operational_status, configuration_version, health_metrics, error_queue] available via API /v1/states for users with role [operator, admin]; access verified by audit log test. System wide access to correlator system states including the Monitor and Control System supervisor system state.

**Rationale:**  Describes the system's function to expose internal state information.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-016 (Timestamping)
- **Conflicts with:** None
---
[FR-007]: Error and Status Messaging
**Description**: User may filter on [severity], [source], [timestamp], via REST parameter; messages delivered within 2s. Error and status messages will be provided in a concise time/location referenced format to upper system levels in a content controllable manner. Acceptance: API returns correct message subset for all [severity,source,timestamp] combinations per OpenAPI spec V.

**Rationale:**  Specifies the format and delivery behavior of system messages.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-016 (Timestamping)
- **Conflicts with:** None
---
[FR-008]: Human GUI Configuration Interface
**Description**: GUI must validate all configuration fields before submission; must pass WCAG 2.1 AA tests. A second interface with a human GUI will also allow for configuration of the correlator hardware, preferably through the same table structures used above.

**Rationale:**  Defines a functional interface for human users to configure hardware.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (VCI Gateway)
- **Conflicts with:** None
---
[FR-009]: Backend Data Delivery
**Description**: Acceptance: 99.9% of data sets must reach backend within 5s over secondary network; loss triggers alert; data transferred in [format]. Specific data sets required by the Backend Data Processing System will be provided in a timely and robust fashion over a secondary virtual network.

**Rationale:**  Describes the data delivery function to an external subsystem.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Network Segmentation)
- **Conflicts with:** None
---
[FR-010]: Monitor Data Spooling
**Description**: Monitor data must be preserved for minimum of 24 hours or until comms restored; zero data loss allowed. Ancillary monitor data including system health, error messages and configuration echoes will be spooled such that temporary loss of network communication with the VLA Expansion Project Monitor and Control System network will not result in loss of monitor data. Acceptance: Spool at least 24 hours of monitor data at normal rate (~N GB); simulate outage and verify no data dropped in 99.9% of cases.

**Rationale:**  Defines a data persistence behavior during network outages.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Offline Operation)
- **Conflicts with:** None
---
[FR-011]: External Data Feed Acceptance
**Description**: Data feeds must be XML conforming to schema X or JSON as Y; invalid feeds must trigger logged error. The Master Correlator Control Computer will accept external data feeds for models, time standards, fiber-link phase corrections and other required data to be packaged with control data delivered to the correlator hardware. Acceptance: Invalid feeds rejected with error event; operator alerted within 30s.

**Rationale:**  Describes the ingestion function for external auxiliary data.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014 (Processor Deadlines)
- **Conflicts with:** None
---
[FR-012]: Hardware Recovery and Hot-Swap
**Description**: Hot-swappable components: [CMIB modules, Power Control Units, Network Interface Cards]. Recovery and auto-registration within 60 seconds. The ability to attempt recovery from failure or hot-swapped hardware devices will be built into this system.

**Rationale:**  Specifies the system's functional capability to handle hardware changes and failures.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Autonomous Recovery)
- **Conflicts with:** None
---
[FR-013]: Failure Alerting
**Description**: Should a CMIB subsystem fail and not respond to reboot requests or other self-heal attempts, an alert notice will be issued so appropriate personnel can affect a hardware repair. Acceptance: After final failed restart, alert sent to ops@domain within 15s, logged under event ID Y.

**Rationale:**  Defines the notification behavior when autonomous recovery fails.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003 (Autonomous Health Monitoring)
- **Conflicts with:** None
---
[FR-014]: CMIB Auto-Restart
**Description**: The CMIB subsystem will then be automatically restarted and configured back into the current operational environment.

**Rationale:**  Describes the automatic reconfiguration behavior following a failure.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Autonomous Recovery)
- **Conflicts with:** None
---
[FR-015]: Master State Replication
**Description**: It is intended that both primary and secondary Master Correlator Control Computer systems maintain full Correlator Monitor and Control System state information.

**Rationale:**  Defines the data consistency function between redundant nodes.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Redundant Masters)
- **Conflicts with:** None
---
[FR-016]: Failover Rerouting
**Description**: Such that any hard failure in the primary node can be corrected by simply rerouting Monitor and Control System communications to the secondary.

**Rationale:**  Describes the failover behavior mechanism.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Redundant Masters)
- **Conflicts with:** None
---
[FR-017]: Power Control Health Monitoring
**Description**: Monitor: online status, heartbeat every 10s, error rate <0.1%; alert if failed for >30s. Watchdog processes and the Master Correlator Control Computer will likewise monitor Correlator Power Control Computer health.

**Rationale:**  Specifies a monitoring function for a specific subsystem.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003 (Autonomous Health Monitoring)
- **Conflicts with:** None
---
[FR-018]: Software Tool Access Levels
**Description**: Defined roles: [admin, operator, tester, developer]; commands [configure, monitor, debug, restart] accessible to roles per RBAC matrix. Software tools will be provided to assist the user at all access levels from system wide configuration and control to a low level CMIB command line instruction. Acceptance: Permissions for each [command x role] pair enforced as specified in RBAC matrix V.

**Rationale:**  Defines the functional scope of provided software tools.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-024 (Privilege Control)
- **Conflicts with:** None
---
[FR-019]: Remote Login Maintenance
**Description**: Remote login via SSH/TLS only; session timeout of 10 min inactivity. All computers within the Correlator Monitor and Control System system shall have the ability for authorized users to directly access individual systems for maintenance and monitoring through remote logins.

**Rationale:**  Describes the remote access function for maintenance.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-023 (Secure Login)
- **Conflicts with:** None
---
[FR-020]: Access Logging
**Description**: Access logs must capture time, user, origin IP, action; retained for min 1 year. In order to monitor all past access to the EVLA Correlator Monitor and Control System, all attempts to access the EVLA Correlator Monitor and Control System should be logged.

**Rationale:**  Defines the audit logging behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Security Architecture)
- **Conflicts with:** None
---
[FR-021]: User Management
**Description**: User IDs must be unique, min 8 chars; passwords per NIST 800-63B; all admin actions logged. The administrator shall have the ability to create and add a new user to the EVLA Correlator Monitor and Control System, remove a user, edit access properties, and block access.

**Rationale:**  Describes the administrative functions for user lifecycle management.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-022 (User Identification)
- **Conflicts with:** None
---
[FR-022]: Watchdog Reboot
**Description**: Test: deliberate CPU block triggers watchdog within 60s; node recovers and re-joins. Each computer system in the Correlator Monitor and Control System shall have a hardware based watchdog timer configured to reboot the EVLA Correlator Monitor and Control System in the case of a system hang.

**Rationale:**  Defines the automatic recovery function for system hangs.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009 (Watchdog/UPS Integration)
- **Conflicts with:** None
---
[FR-023]: UPS Signaling
**Description**: UPS must signal via SNMPv3, 10s poll interval; system must process outage signal within 15s. The UPS devices need the ability to signal the Correlator Monitor and Control System when a power outage has occurred and keep the Correlator Monitor and Control System apprised of time remaining on backup power.

**Rationale:**  Describes the communication function between UPS and System.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009 (Watchdog/UPS Integration)
- **Conflicts with:** None
---
[FR-024]: Board Identifier Reading
**Description**: The CMIB shall be capable of reading a 16-bit identifier from the host correlator board.

**Rationale:**  Specifies a hardware interface function for identification.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008 (CMIB Bus Interface)
- **Conflicts with:** None
---
[FR-025]: Self-Monitoring Conditions
**Description**: Monitored: CPU temp > 85°C, error rate >10/min, voltage deviation >5%; alert as syslog entry within 5s. The Correlator Monitor and Control System shall be self-monitoring. It will be capable of detecting, reporting on and automatically taking action to remedy or lessen the impact of the following types of abnormal conditions: processor hardware failure, operating system hangs or crashes, temperature or voltage deviations, computational performance below minimum specifications, computational error rates above maximum specification, internal communications failures. Acceptance: Log alerts with error code X and fields [type, subsystem, threshold, timestamp]; see table Y.

**Rationale:**  Defines the comprehensive self-diagnostic function.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Autonomous Recovery)
- **Conflicts with:** None
---
[FR-026]: Queue Processing during Comms Loss
**Description**: Max queue length = 1000; if full, log error and drop oldest entry. The EVLA Correlator Monitor and Control System shall be able to continue processing of all correlator configuration/control events until the queues of parameters are exhausted and external communications are restored. Acceptance: Dropped event triggers Error_DroppedQueueEntry type log; SRE alerted if more than 1% dropped in 7 days.

**Rationale:**  Describes the behavior of the system during external network failure.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Offline Operation)
- **Conflicts with:** None
---
[FR-027]: Source Code Availability
**Description**: All deployed codebase on branch main or release, under Apache 2.0, with README and API docs. All systems and application source code shall be available to or on the EVLA Correlator Monitor and Control Systems that execute it.

**Rationale:**  Defines the availability requirement for software artifacts on the system.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-027 (Documentation)
- **Conflicts with:** None
---