# Functional Requirements Results:

[FR-001]: User Role-Based Access Control
**Description**: The system shall restrict access to subsystems according to user categories (Astronomer, Science Observer, Telescope Operator, Support Personnel, Developers, Administrators) with specific privileges assigned to each role. Acceptance: Given login(credentials), system issues an auth token/role set; concurrent access is logged; all role changes audited by user/session in security log. Login input shall include username and password or SSO credentials; session/auth token output shall be generated; multi-role resolution and audit logging shall be implemented. Acceptance: All role changes/audited operations are logged and retained ≥180 days; failed logins cause lockout after 5 attempts; audit logs reviewed monthly.

**Rationale:** This describes a specific function the system must perform - authenticating users and granting appropriate access levels based on their role.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Security), ASR-001 (Distributed Architecture)
- **Conflicts with:** None
---

[FR-002]: Operational Level Management
**Description**: The system shall operate in one of three disjoint operational levels (Observing, Maintenance, Test) with access restricted according to the current level of operation.

**Rationale:** This describes a behavioral function - the system must manage and enforce operational state levels.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** None
---

[FR-003]: Access Mode Implementation
**Description**: The system shall provide six access modes (Observing, Monitoring, Operation, Planning, Testing, Administrative) with different capabilities for each mode.

**Rationale:** This describes specific system functions that must be implemented for different access scenarios.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---

[FR-004]: Automatic Sequencer for Queue-Based Observing
**Description**: The system shall provide an automatic sequencer that executes preprogrammed observing sequences with minimal human interaction, supporting queue-based observing as the primary observation mode.

**Rationale:** This describes a specific functional capability - automated observation scheduling and execution.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010 (Data Acquisition), NFR-002 (Performance)
- **Conflicts with:** None
---

[FR-005]: Remote Operations Support
**Description**: The system shall support full remote operations including remote observing, remote telescope control, remote monitoring, remote configuration, and remote diagnostics from multiple facility locations.

**Rationale:** This describes functional capabilities that must be available for remote users.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Distributed Architecture), NFR-006 (Network Performance)
- **Conflicts with:** None
---

[FR-006]: Multi-Point Monitoring
**Description**: The system shall allow multiple users at different locations to simultaneously monitor telescope and instrument status without affecting ongoing observations.

**Rationale:** This describes a specific system behavior - concurrent monitoring capability.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-002
- **Conflicts with:** None
---

[FR-007]: Instrument Control and Management
**Description**: The system shall control multiple instruments mounted on the telescope, providing parallel access to all mounted instruments while ensuring only one instrument has access to the telescope beam at a time.

**Rationale:** This describes core functional behavior for instrument management.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, ASR-002 (Multi-Instrument Architecture)
- **Conflicts with:** None
---

[FR-008]: Visitor Instrument Interface
**Description**: The system shall provide a standardized interface for visitor instruments supporting status information acquisition, preprogrammed observing sequences, and telescope position/focus offset capabilities.

**Rationale:** This describes a functional interface requirement for external instrument integration.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, ASR-003 (Interface Standards)
- **Conflicts with:** None
---

[FR-009]: Virtual Telescope Simulation
**Description**: The system shall provide a virtual telescope simulator for science planning, testing, and development that responds to commands without requiring actual hardware. Acceptance: Simulated subsystem must pass 100% of standard test suite used on hardware, with output data matching format/contract for all commands. Minimum functional API that simulator must implement (API signature, returned data, error code handling) shall be defined; acceptance tests for simulation vs real hardware shall be specified.

**Rationale:** This describes a functional capability for simulation and testing.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Simulation Architecture), NFR-017 (Hardware Independence)
- **Conflicts with:** None
---

[FR-010]: Data Acquisition and Storage
**Description**: The system shall acquire and store astronomical data (science, engineering, reference, calibration) from detectors with support for compression and standard FITS format for transmission. Acceptance: Data saved for detector X is in FITS vN format, validated by external tool; compressed with lossless method Y; decompress round-trip tested for fidelity. Data output format/schema for each data type shall be defined; compression methods, acceptance checks, and error handling for data transfer/storage shall be specified. Schema: FITS schema for each data type; on transfer error, record event and retry ≤3 times then alert.

**Rationale:** This describes core functional behavior for data handling.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003 (Data Transfer), NFR-004 (Storage Capacity), NFR-011 (Data Compression)
- **Conflicts with:** None
---

[FR-011]: System Logging and Error Reporting
**Description**: The system shall log all important events with timestamps, record errors and alarms with source identification, and maintain engineering data at up to 200 Hz for short periods.

**Rationale:** This describes functional logging and reporting behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Reliability), ASR-005 (Logging Architecture)
- **Conflicts with:** None
---

[FR-012]: Safety Interlock System
**Description**: The system shall implement safety monitoring to detect danger conditions and bring the system to a safe state, with hardware interlocks independent of software for critical hazards. Acceptance: Safety alerts delivered to all ops consoles in <15 sec (p99); alarm log includes cause, timestamp, affected subsystems. Timing for alert delivery and notification scope shall be defined.

**Rationale:** This describes functional safety behavior the system must perform.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-007 (Safety), ASR-006 (Safety Architecture)
- **Conflicts with:** None
---

[FR-013]: Configuration and Reconfiguration
**Description**: The system shall support dynamic reconfiguration of the observing environment during operations without requiring system restart, including instrument selection and light path changes. Acceptance: Instrument reconfiguration requests via API complete without restart in <30s (p99), with error/log if conflicted; rollbacks supported. State transitions, error paths, and test cases for reconfiguration shall be described; what can be reconfigured, how conflicts/errors are reported and rollback path shall be specified. Acceptance: For each allowed reconfigurable item, submit reconfig request via API, observe transition completes in <30s, with state and error logging. On simulated failure, rollback invoked and system returns to prior config in <30s (p99). Schema: Table of component types, update paths, rollback paths. Owner: Configuration Team; Next action: define configuration item matrix, rollback acceptance test, and error semantics.

**Rationale:** This describes functional configuration management behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-008 (Maintainability), ASR-008 (Modular Architecture)
- **Conflicts with:** None
---

[FR-014]: Database Access for Parameters
**Description**: The system shall maintain telescope, instrument, and detector control information in an on-line database accessible at any operation level with 2-3 msec access times. Acceptance: Database access to parameter X has latency ≤3ms p(99.9), schema=<provided>; update propagation between nodes completes within Y ms. Main parameter table schemas, concurrency rules, and atomicity of update/reads shall be defined; error cases shall be documented. Acceptance: MainParamTable: { param_name: string, value: any, source: string, <timestamp> } - supports atomic update/read. Error cases E01–E0N defined and logged with trace. Owner: DB Architect; Next action: furnish parameter table schema and error code documentation.

**Rationale:** This describes functional data access behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Database Architecture), NFR-002 (Performance)
- **Conflicts with:** None
---

[FR-015]: Version Control and Consistency Checking
**Description**: The system shall implement on-line version control with consistency checking of all software components at boot time and version information retrievable from executing software. Acceptance: Executing '/opt/gemini/moduleX --version' or HTTP GET /version returns source hash, build date, semantic version to stdout/JSON. CI verifies retrieval for all components. Owner: DevOps; Next action: publish version API/CLI retrieval spec and CI test.

**Rationale:** This describes functional version management behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008 (Maintainability), ASR-008 (Version Management)
- **Conflicts with:** None
---

[FR-016]: Subsystem Self-Testing
**Description**: The system shall provide built-in test (BIT) facilities for each subsystem including monitor level background tasks, full exercise modules, and automatic problem reporting to OCS. Acceptance: BIT triggers on boot and via API, produces {test_id, status, diagnostics} for all subsystems, sent to OCS and recorded in log. Failure paths logged. Owner: Testing Team; Next action: document BIT triggers, schema, and error reporting format.

**Rationale:** This describes functional testing and diagnostic behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Reliability), FR-011
- **Conflicts with:** None
---

[FR-017]: Flexible Scheduling Support
**Description**: The system shall support flexible scheduling that allows changing telescope scheduling quickly by exchanging observing programs based on weather and other conditions. Acceptance: 100% of program switches logged with timestamp, state, prior/next program, and rule applied. Logging of all scheduling decisions with timestamp, reason code, and policy used shall be required. Acceptance: All schedule changes (100%) logged as {timestamp, prior_program, next_program, rule}, with 99% latency <60s. Test plan covers 10+ scenarios of rule/prio/override transition. Owner: Scheduling Team; Next action: enumerate policy/rule matrix, test catalog, and rule provenance logs.

**Rationale:** This describes functional scheduling behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-002
- **Conflicts with:** None
---

[FR-018]: Command and Control Protocol
**Description**: The system shall implement a uniform ACK/NAK protocol across all subsystems with 500 msec timeouts and 100-200 msec handshaking between IOCs.

**Rationale:** This describes functional communication behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Distributed Architecture), NFR-002 (Performance)
- **Conflicts with:** None
---

[FR-019]: Quick-Look Data Processing
**Description**: The system shall provide synchronous quick-look data processing for fast on-line data preprocessing with results available within exposure sequences.

**Rationale:** This describes functional data processing behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-002
- **Conflicts with:** None
---

[FR-020]: Archive System Interface
**Description**: The system shall automatically archive data during observing and maintenance level operation with on-line interactive access to the data archiving system for users.

**Rationale:** This describes functional data management behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-004
- **Conflicts with:** None
---