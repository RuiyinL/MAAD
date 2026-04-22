# Functional Requirements Results:

[FR-001]: User Authentication and Session Management
**Description**: The RLCS software shall have a logon screen for the GUI that requests user name and corresponding password. The logon screen shall activate command control for the user if the user requests it and has authorization. Only one 'operator' may be logged onto the system at any given time with command control.
**Rationale:** This requirement is functional as it defines specific system behaviors regarding user access, input validation (username/password), and session state management (single active operator).
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003 (Security), ASR-006 (Single Operator Command Control)
- **Conflicts with:** None
---

[FR-002]: Graphical User Interface Status Display
**Description**: The GUI shall indicate the current date and time, user's name, and workstation location name. The GUI shall provide a display of the I-15 Reversible Lane Control System facility geographic area, including a layout of the mainline I-15. Status information shall continue to display when no user is logged on to the workstation and shall continually be updated every 2 seconds.
**Rationale:** This describes a specific output function of the system (displaying status, map, time) and the conditions under which it occurs.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance - Update Rate)
- **Conflicts with:** None
---

[FR-003]: Device Command and Control Execution
**Description**: The GUI shall provide an option that allows the system user to issue commands that monitor and control opening and closing events. The system shall control all system field elements to device sensor level for those device sensors that may be controlled. Each device control command shall check the current status of all closure devices in the system and shall abort if any closure control device status is unknown. Acceptance: For a device control command, if any closure device in the system is in 'unknown' state, the command is aborted and operator is notified within 2s; see Test Matrix T-001 for scenarios. Next action: Define input/output schema and add test plan reference.
**Rationale:** This defines the core task of the system: processing user input to change physical device states and enforcing pre-execution checks.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Multi-Layer Safety Screening), FR-009 (Safety Rule Validation)
- **Conflicts with:** None
---

[FR-004]: Automated Operational Sequencing
**Description**: The RLCS shall execute stored operational control command sequences based on the current system mode of operation and the schedule for each sequence. At a minimum of every 60 seconds, the system shall check the current date and time against a list of scheduled events for the current mode to determine if any event should be executed.
**Rationale:** This describes an automated behavior where the system triggers actions based on time and schedule data without direct user intervention.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance - Scheduling Check)
- **Conflicts with:** None
---

[FR-005]: Audit and Activity Logging
**Description**: The RLCS Application will create and store log files which will track all application activity. The system shall generate log files for Device Command Log, System Operation Command Log, Problem Work Order Log, Alarm Log, Daily Diary Log, Special Event Log, and System Operation Schedule Log. DeviceCommandLog schema: (id, command, timestamp, status, operator_id) is append-only; verify with SRE-005 audit. Device command log shall not be editable by users. Next action: Provide example entity/field definition for each primary log artifact; specify immutability test.
**Rationale:** This specifies the system's function to record transactions and events for audit purposes, defining specific log types and immutability constraints.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Maintainability - COTS DB)
- **Conflicts with:** None
---

[FR-006]: External Data Export
**Description**: All external systems shall retrieve RLCS status from a server outside the RLCS network. External status export is delivered in RFC-8259-compliant JSON; schema example: { "timestamp": "2022-01-02T12:00:00Z", "status": "open_southbound", "customer_type": "HOV", "access": "location_2_closed", "sign_message": "Express Lanes Closed" }; file/endpoint named 'rlcs_status_YYYYMMDDHHMMSS.json'. The transfer will occur every 30 seconds. This interface is a one-way output only interface. Next action: Document the external schema and add as an appendix to the API contract.
**Rationale:** This defines a specific data transformation and output function to external entities with a defined payload and frequency.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Network Segmentation)
- **Conflicts with:** None
---

[FR-007]: Alarm Notification and Management
**Description**: For alarm status, the GUI shall also issue an audible alarm, and the icon shall be different from the okay status for that device. The RLCS notification to the operator workstation of any critical alarms shall occur within 2 seconds of alarm detection. The GUI shall allow the operator to acknowledge an alarm and have the option to silence the audible portion.
**Rationale:** This describes the system's behavior in response to fault conditions, including visual, auditory, and timing constraints on notification.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance - Alarm Latency)
- **Conflicts with:** None
---

[FR-008]: Configuration Management
**Description**: The GUI shall provide an option for "Configuration" that is only accessible by the RLCS Software user with System Administrative privileges. It shall display and allow modification of all database tables with the exception of log tables. Configuration data schema must be fixed at design; changes require change control; log editing prohibited by access rules/tested in SRE-005. Example schema: CREATE TABLE DeviceCommandLog (id INT PRIMARY KEY, command VARCHAR(255), timestamp TIMESTAMP, status VARCHAR(20), operator_id INT, immutable_flag BOOLEAN DEFAULT TRUE); Test: No UPDATE/DELETE permissions for user role. When the system administrator modifies the database tables, the GUI shall analyze the data before storing in the database and notify the system administrator of any conflicting or redundant entries. Next action: Add log/config table schema examples and access policies to SRS appendix.
**Rationale:** This defines administrative functions for modifying system parameters and data validation rules prior to persistence.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Maintainability)
- **Conflicts with:** None
---

[FR-009]: Safety Rule Validation
**Description**: Each control command that is processed must be validated against the secured safety rules (stored in non-volatile memory) for the command. For example, if the operator issues a command to open the south gate while the north gate is open, the RLCS software will determine that opening the south gate cannot occur.
**Rationale:** This specifies a functional check that must occur during command processing to prevent unsafe states.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Multi-Layer Safety Screening)
- **Conflicts with:** None
---

[FR-010]: Device Initialization and Identification
**Description**: When each workstation and control unit comes online, the system shall identify it and all its associated device sensors. The RLCS software shall initialize each control unit and device sensor as it is identified. If everything is OK the start up process shall not exceed 30 seconds. Any control unit startup failure must cause entry in ErrorLog entity (schema: timestamp, unit_id, error_code, error_desc), alert operator within 5 seconds via GUI. Next action: Clarify log format, alerting protocol, timeout enforcement.
**Rationale:** This describes the startup behavior and initialization sequence of the system components.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance - Startup Time)
- **Conflicts with:** None
---