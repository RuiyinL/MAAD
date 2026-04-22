# Functional Requirements Results:

[FR-001]: Reversible lane operations (open/close) for peak hours and special events  
**Description**: “The purpose of the (I-15 RLCS) is to open and close the reversible lanes for morning and evening peak traffic hours and any special events defined by operators of the system.”  
**Rationale:** Describes a primary system behavior (operating the facility state).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-037, FR-038, FR-039, NFR-001, NFR-004  
- **Conflicts with:** Not specified  
---

[FR-002]: GUI for status, commands, configuration, log export, and reporting  
**Description**: “The system shall have a Graphical User Interface (GUI) that allows the operator to view system status, issue commands to change device status, configure the system, export log data, and generate reports.”  
**Rationale:** Specifies system functions exposed via UI.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-006, FR-012, FR-013, FR-016, FR-020, FR-027  
- **Conflicts with:** NFR-020 (single operator command control)  
---

[FR-003]: GUI logon with username/password  
**Description**: “The RLCS software shall have a logon screen for the GUI. The logon screen shall request user name and corresponding password.”  
**Rationale:** Defines authentication interaction/behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016, NFR-017  
- **Conflicts with:** Not specified  
---

[FR-004]: Enable command control only if authorized and requested  
**Description**: “The logon screen shall activate command control for the user if the user requests it and has authorization.”  
**Rationale:** Describes access-controlled behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, FR-006, NFR-016  
- **Conflicts with:** FR-028 (remote dial-in access) if workstation constraints exclude remote terminals  
---

[FR-005]: Command control limited to specified workstations  
**Description**: “Command control shall be from only specified workstations.”  
**Rationale:** Describes operational control behavior constraints (where commands can originate).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004, NFR-016  
- **Conflicts with:** FR-028 (dial-in from remote computer) if not included as “specified”  
---

[FR-006]: Command-control takeover workflow based on security level  
**Description**: “If command control is enabled by another user, and the logging in user is of higher security, the logging in user shall be requested to accept or deny command control. If another user is logged in with command control and the new user takes command control, the other user is notified.”  
**Rationale:** Defines multi-user interaction logic and control transfer behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, NFR-016, NFR-020  
- **Conflicts with:** NFR-020 (only one operator logged in) unless “operator” is distinct from other user types  
---

[FR-007]: GUI show timestamp, user, workstation ID; show logged-in users  
**Description**: “The GUI shall indicate the current date and time, user’s name, and workstation location name. The GUI shall also show other users currently logged in the other units within the RLCS network.”  
**Rationale:** Defines UI display behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-025  
- **Conflicts with:** Not specified  
---

[FR-008]: GUI control option to monitor/control opening and closing events  
**Description**: “The GUI shall provide an option that allows the system user to issue commands that monitor and control opening and closing events.”  
**Rationale:** Defines command issuance function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-009, FR-037, FR-038, NFR-016  
- **Conflicts with:** Not specified  
---

[FR-009]: Control option provides level of control based on security level  
**Description**: “Based on the user’s security level, the control option shall provide the user with the appropriate level of control.”  
**Rationale:** Defines authorization behavior for control functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-014, NFR-016  
- **Conflicts with:** Not specified  
---

[FR-010]: Allow setting operational status of failed devices  
**Description**: “The control option shall provide the user with the capability to set the operational status of failed devices.” Derived refinement per evaluator: Only users with Override role may change status of failed devices, with reason and operator credential logged to immutable audit trail. Owner/Next action: Document override permissions, approvals, and audit requirements.  
**Rationale:** Defines an operator function (status override/management).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-035, FR-036, NFR-016  
- **Conflicts with:** FR-033 (safety screening) if override can bypass safety rules (must be clarified)  
---

[FR-011]: Display active overrides and devices lacking rules protection  
**Description**: “The RLCS software shall display information about active overrides: Which are active, and which devices have no currently active 'rules protection' against erroneous opening/closing.”  
**Rationale:** Defines monitoring/display behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010, FR-025  
- **Conflicts with:** Not specified  
---

[FR-012]: Facility geographic map display  
**Description**: “The GUI shall provide a display of the I-15 Reversible Lane Control System facility geographic area, including a layout of the mainline I-15, SR-163 freeway area … Current facility boundaries extending one mile in either direction.”  
**Rationale:** Defines UI visualization function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-010 (map refresh)  
- **Conflicts with:** Not specified  
---

[FR-013]: Visual/audible alarms and configurable alarm conditions  
**Description**: “For alarm status, the GUI shall also issue an audible alarm… visual alarm shall include a change of color… Alarm conditions shall be configurable on the screen.”  
**Rationale:** Defines alarm presentation and configurability behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-032, FR-015  
- **Conflicts with:** Not specified  
---

[FR-014]: Override status displayed with distinct color  
**Description**: “When a device status has been overridden, on the screen it shall appear with different color from the normal and alarm status colors.”  
**Rationale:** UI behavior for overridden state.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010  
- **Conflicts with:** Not specified  
---

[FR-015]: Continue displaying/updating status without a logged-on user  
**Description**: “Status information shall continue to display when no user is logged on to the workstation and shall continually be updated every 2 seconds.”  
**Rationale:** Defines system behavior independent of user session.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006, NFR-008  
- **Conflicts with:** Not specified  
---

[FR-016]: Configuration option restricted to System Administrator; modify DB tables except logs  
**Description**: “The GUI shall provide an option for “Configuration” that is only accessible by the RLCS Software user with System Administrative privileges. It shall display and allow modification of all database tables with the exception of log tables.”  
**Rationale:** Defines administrative function and access controls.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, NFR-016, FR-025  
- **Conflicts with:** FR-024 (user can export logs; must ensure export ≠ edit)  
---

[FR-017]: Validate configuration changes for conflicts/redundancy before storing  
**Description**: “When the system administrator modifies the database tables, the GUI shall analyze the data before storing in the database and notify the system administrator of any conflicting or redundant entries.”  
**Rationale:** Defines input validation behavior for configuration changes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016  
- **Conflicts with:** Not specified  
---

[FR-018]: Assign security level/password per staff; command/device/mode/workstation authorization  
**Description**: “The configuration option shall allow a security level and password to be assigned to each defined staff member. User security levels shall be assigned at the command level, device, mode, workstation…”  
**Rationale:** Defines security administration functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016, NFR-017, FR-016  
- **Conflicts with:** Not specified  
---

[FR-019]: Remotely change user accounts in field units  
**Description**: “The configuration option shall also allow user accounts to be changed remotely in the field units.”  
**Rationale:** Defines remote administrative behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028, NFR-015  
- **Conflicts with:** Not specified  
---

[FR-020]: Show impacted unit(s) when changing configuration  
**Description**: “When an operator is making changes on the system, the GUI configuration screen shall display to the user which device, controller, or workstation in the RLCS network will be affected by the changes.”  
**Rationale:** UI behavior supporting safe configuration changes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016  
- **Conflicts with:** Not specified  
---

[FR-021]: Additional password required to configure device rules  
**Description**: “The option to configure device rules shall require an additional login password for that option.”  
**Rationale:** Defines privileged action requiring step-up authentication.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016, NFR-016  
- **Conflicts with:** Not specified  
---

[FR-022]: Add/remove devices from GUI display without programming effort  
**Description**: “The GUI shall allow devices to be added and removed from the display without requiring programming effort.”  
**Rationale:** Defines configurability behavior (dynamic UI composition).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016, FR-025  
- **Conflicts with:** Not specified  
---

[FR-023]: Modify facility map without programming effort  
**Description**: “The GUI shall allow the facility map to be modified without requiring programming effort.”  
**Rationale:** Defines configurability behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016  
- **Conflicts with:** Not specified  
---

[FR-024]: Display logs and export logs as ASCII  
**Description**: “The system shall display information logs and provide the capability to export the logs in common ASCII text for importing to commercial database, spreadsheet, or reporting programs.”  
**Rationale:** Defines log access/export function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025, NFR-012  
- **Conflicts with:** FR-016 (logs must not be modifiable)  
---

[FR-025]: Create and store audit logs for all application activity  
**Description**: “Audit functions – The RLCS Application will create and store log files which will track all I-15 RLCS … application activity.” Derived refinement per evaluator: RLCS must retain all audit and device logs for at least 365 days in tamper-proof/protected storage. Owner/Next action: Specify log retention policy for all audit classes.  
**Rationale:** Defines system behavior to record activities.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-012, NFR-014  
- **Conflicts with:** Not specified  
---

[FR-026]: Problem Work Order entry/edit/export  
**Description**: “The Problem Work Order shall be a separate display that allows the user to enter information about a system problem. The Problem Work Order data shall be editable and exportable…”  
**Rationale:** Defines a specific UI/data entry function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025  
- **Conflicts with:** Not specified  
---

[FR-027]: Daily Diary entry with edit restrictions  
**Description**: “The ‘Daily Diary’ shall be a separate display that allows the user to enter free form text comments. The user should not be able to update log entries other than for their own login, for the current day and current shift.”  
**Rationale:** Defines user journaling function and edit constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025, NFR-012  
- **Conflicts with:** Not specified  
---

[FR-028]: Remote access via secure dial-in through firewall  
**Description**: “The second consists of a secure remote dial-in interface through a firewall via a dial-up modem… allows connection into the RLCS network via a remote computer equipped with the application software, and with a user logon authorized for remote access.” Derived refinement per evaluator: Only remote dial-in computers registered in the RLCS authorized workstation list may initiate command control. Owner/Next action: Define dial-in workstation registration/authorization process.  
**Rationale:** Defines a remote access function and interaction.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, NFR-015, NFR-016  
- **Conflicts with:** FR-005 (specified workstations)  
---

[FR-029]: External systems retrieve status from server outside RLCS network; data elements in single file  
**Description**: “All external systems shall retrieve RLCS status from a server outside the RLCS network. A single data file will include… Status… Customers… Access… Signs…”  
**Rationale:** Defines an output data service/interface.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-030, NFR-018  
- **Conflicts with:** Not specified  
---

[FR-030]: One-way external data transfer via firewall and one-way serial transfer  
**Description**: “The RLCS will provide access to system status data, to external systems through a firewall… one way data transfer… transfer will occur every 30 seconds. A one way serial data transfer will also be provided.”  
**Rationale:** Defines system output behavior and interfaces.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-029, NFR-005  
- **Conflicts with:** Not specified  
---

[FR-031]: Monitor status of all field devices; process requests to change device status  
**Description**: “The RLCS software will monitor the status of all field devices and will process requests for changing field device status.”  
**Rationale:** Core monitoring/control behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-040, FR-041, FR-043  
- **Conflicts with:** Not specified  
---

[FR-032]: Monitor sensors and update DB with status of all field elements  
**Description**: “The RLCS software shall monitor, display, and update the database with the status of all system field elements.”  
**Rationale:** Defines data processing and state management function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-044, NFR-006  
- **Conflicts with:** Not specified  
---

[FR-033]: Multi-level integrity checks for any command that changes device state  
**Description**: “Any operator or system command, which changes the state of field control devices, must be checked for integrity at multiple levels in the RLCS.”  
**Rationale:** Defines required validation behavior before executing state changes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-034, FR-035, NFR-014  
- **Conflicts with:** FR-010 (override) if override bypasses integrity checks  
---

[FR-034]: Abort command if any closure device status is unknown  
**Description**: “Each device control command shall check the current status of all closure devices in the system and shall abort if any closure control device status is unknown.”  
**Rationale:** Defines command precondition behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-032  
- **Conflicts with:** FR-010 (override) if override can set unknown→known without field truth  
---

[FR-035]: Execute commands only when valid status exists for all device sensors  
**Description**: “Each command … shall only be executed when a valid or good status exists for all device sensors.”  
**Rationale:** Defines gating logic for command execution.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-032  
- **Conflicts with:** FR-010 (override)  
---

[FR-036]: Operator override of device status to continue sequences; override isolation  
**Description**: “The system operator shall be able to override any device and continue with a system operational command sequence… The process of overriding a device status shall not affect the status of any other device.” Derived refinement per evaluator: Device status override may not bypass multi-level safety screening; safety screenings must be re-applied after override; admin override cannot bypass safety interlocks; all override events must be logged with reason, time, and operator credential. Owner/Next action: Add a section on safe override handling that prohibits safety rule bypass.  
**Rationale:** Defines a specific operator function and its scope/side effects.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010, NFR-016  
- **Conflicts with:** FR-034, FR-035, FR-033 (safety/integrity gating)  
---

[FR-037]: Execute stored operational sequences based on system mode and schedule  
**Description**: “The RLCS shall execute stored operational control command sequences based on the current system mode of operation and the schedule for each sequence.”  
**Rationale:** Defines sequencing behavior (scheduled automation).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-038, FR-049, FR-050  
- **Conflicts with:** Not specified  
---

[FR-038]: Present scheduled operations for operator confirmation before executing  
**Description**: “The RLCS shall present scheduled command operations to the operator at the GUI for confirmation prior to executing the command.”  
**Rationale:** Defines human-in-the-loop approval function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, FR-037  
- **Conflicts with:** FR-015 / unattended monitoring (must clarify unattended scheduled ops behavior)  
---

[FR-039]: Halt sequences on step timeout or unsafe/unexpected device state changes  
**Description**: “At any point in an opening or closing sequence, the sequence shall be halted if: A device fails to report completion… within the response time window… or … device status … changes to ‘unknown’/‘closed’/‘open’ without operator-initiated command… At any point in an opening sequence… halted if … opposite direction … changes to ‘unknown’ or ‘open’.”  
**Rationale:** Defines deterministic sequencing control and fault handling.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-032, FR-033  
- **Conflicts with:** FR-036 (override/resume) if overrides allow bypass without proper mitigation  
---

[FR-040]: Resume halted sequences within configurable correction window  
**Description**: “To resume an opening or closing sequence after a halt has occurred, the operator shall be able to issue a command to resume if the offending device status can be corrected within a configurable time period as defined in the database and in non-volatile memory.”  
**Rationale:** Defines recovery behavior in sequencing.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-039, FR-049  
- **Conflicts with:** Not specified  
---

[FR-041]: Safety rules validation for each control command at each unit receiving the command  
**Description**: “Each control command that is processed must be validated against the secured safety rules (stored in non-volatile memory) for the command… The validation will occur at each control unit in the system that receives the command.”  
**Rationale:** Defines safety interlock validation behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-042, FR-049, NFR-013  
- **Conflicts with:** FR-036 (override)  
---

[FR-042]: Hierarchical command forwarding (superior to inferior units only)  
**Description**: “Commands are only forwarded from superior units to inferior ones… The TSU is superior to the FCUs which are superior to the DCUs.”  
**Rationale:** Defines command routing/control behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041  
- **Conflicts with:** Not specified  
---

[FR-043]: Retry status request; configurable retries; declare device failure on exhaustion  
**Description**: “If a status from any device is not received upon request, the system shall automatically request the status again. Failure to receive a valid status after a configurable number of retries shall be considered a device failure.”  
**Rationale:** Defines robustness behavior for polling/communications.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-049  
- **Conflicts with:** Not specified  
---

[FR-044]: Identify units and initialize devices when coming online  
**Description**: “When each workstation and control unit … comes online, the system shall identify it and all its associated device sensors… initialize each control unit and device sensor as it is identified.”  
**Rationale:** Defines startup discovery/init behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045  
- **Conflicts with:** Not specified  
---

[FR-045]: Field unit startup sequence: read cabinet ID, verify cards, integrity check, init tables  
**Description**: “RLCS software in the field shall first identify its unit … by reading the cabinet id… make sure that all the cards required … are present and working properly… do a control system integrity check … and initialize all the specified tables.”  
**Rationale:** Defines concrete startup processing behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009, NFR-014  
- **Conflicts with:** Not specified  
---

[FR-046]: Maintain current status for all devices at each controller unit  
**Description**: “The current status for all devices shall be maintained at each controller unit.”  
**Rationale:** Defines distributed state management behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-032  
- **Conflicts with:** Not specified  
---

[FR-047]: Generate alarm conditions (critical and warning) for specified triggers  
**Description**: “Critical alarms shall be generated when… verification failure… user logs in field units… override issued… computer down… power failure… cabinet ID changed… DCUs in manual mode. Warning alarms shall be generated when… security sensor activation… Air pressure, Temperature… Voltages outside thresholds…”  
**Rationale:** Defines alarm detection and classification behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-013, FR-032, FR-052  
- **Conflicts with:** Not specified  
---

[FR-048]: Provide operator guidance actions on critical alarms during operations  
**Description**: “If a critical alarm occurs during opening or closing operation, the system shall present the operator with possible actions … If overriding … needed … determine if the operator has high enough security and provide advise on how to proceed.”  
**Rationale:** Defines decision-support behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-047, FR-036, NFR-016  
- **Conflicts with:** Not specified  
---

[FR-049]: Store/process/retrieve operational + reporting data; export status to external server data store  
**Description**: “The RLCS shall store, process, and retrieve all data necessary to operate … generate current and historical reports … and export system status data to an external server data store.”  
**Rationale:** Defines data management functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-029, FR-024  
- **Conflicts with:** Not specified  
---

[FR-050]: Use COTS DBMS for data management  
**Description**: “A commercial off-the-shelf database management system shall be used for this function.”  
**Rationale:** Functional/solution constraint requiring DBMS capability.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-049  
- **Conflicts with:** Not specified  
---

[FR-051]: Use COTS reporting tool and generate reports from exported DB data  
**Description**: “The system will use data exported from the RLCS database to create and format a variety of reports. A commercial off-the-shelf reporting tool shall be used…”  
**Rationale:** Defines reporting function implementation requirement.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-049, FR-024  
- **Conflicts with:** Not specified  
---

[FR-052]: Integrity hashing of non-volatile code/data; daily verification; log results; alarm on failure; block unit on failure  
**Description**: “The system shall … employ a one-way hash function… MD5 algorithm is acceptable… produce a table of … Message Digest values … maintained in non-volatile memory… periodic verification … at least once a day… results recorded in the system log… verification failure shall cause an alarm… prevent the affected unit from being used in control sequences… provide for verification requests by operator command… hash function … used to encrypt user passwords.” Derived refinement per evaluator: Integrity verification must run on every code/rules change and at system boot, and on scheduled basis (daily); and alert the operator within 1 minute on failure. Owner/Next action: Expand frequency and alerting for integrity checks.  
**Rationale:** Defines behaviors for integrity verification and password protection.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-047, FR-025, NFR-014, NFR-016  
- **Conflicts with:** NFR-015 (modern cryptography expectations; MD5 weaknesses)  
---

[FR-053]: Replicate operating logic, sequences, and rules in non-volatile memory in FCU/DCU  
**Description**: “In each FCU and DCU… items shall be replicated from the central database server and maintained in non-volatile, non-removable memory: Reversible Lanes Operating Logic, Control Sequences, and Rule Sets.”  
**Rationale:** Defines data distribution and persistence behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-049, NFR-013  
- **Conflicts with:** Not specified  
---

[FR-054]: Interface with field device I/O cards via I/O driver software  
**Description**: “The RLCS software shall send to and receive data from the field device I/O cards through I/O driver software.”  
**Rationale:** Defines the required mechanism to interact with field hardware.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-055  
- **Conflicts with:** Not specified  
---

[FR-055]: Interface with whichever intelligent controller is selected  
**Description**: “It is unknown at this time which particular controller will be used… but the software must interface with whichever controller is chosen…” Derived refinement per evaluator: All controllers must implement the provided RLCS Device Control API v1.x, as published in [Appendix TBD]. Owner/Next action: Publish hardware interface requirements/API.  
**Rationale:** Defines required adaptability in control interface behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-054  
- **Conflicts with:** Not specified  
---

[FR-056]: Degraded-mode alternate control behaviors and manual fallbacks  
**Description**: “The RLCS will function in a degraded mode… If the TMC workstations or network server fails… alternate control at FCU South or FCU North… operator shall be able to dial in… If FCUs North and South both fail… alternate control… direct control at DCUs… connect a laptop… If any MCU fails… devices can be manually controlled…”  
**Rationale:** Defines required behaviors under failure scenarios.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028, NFR-002, NFR-003  
- **Conflicts with:** FR-005 (specified command workstations) unless laptops/dial-in are authorized  
---

[FR-057]: Change management approval for changes after baseline approval  
**Description**: “After the baseline version of this document is approved, any changes made to the document must be approved in accordance with the provisions of the established Change Management Plan.”  
**Rationale:** Defines a process function governing requirements changes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** Not specified  
- **Conflicts with:** Not specified  
---