# Functional Requirements Results

[FR-001]: Translate external configuration into physical correlator configuration  
**Description**: “The Correlator Monitor and Control System shall receive configuration information from the VLA Expansion Project Monitor and Control System system and translate this info into a physical correlator hardware configuration.”  
**Rationale:** Describes a required input-to-output transformation behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001, ASR-002, NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-002]: Process and transfer dynamic control and monitor data  
**Description**: “The Correlator Monitor and Control System shall process and transfer dynamic control data and monitor data.”  
**Rationale:** Defines core runtime data-handling functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001, NFR-006, NFR-007  
- **Conflicts with:** NFR-020  
---

[FR-003]: Monitor subsystem health and autonomously take corrective action  
**Description**: “The Correlator Monitor and Control System shall monitor correlator and correlator subsystem health and take corrective action autonomously to recover from hardware and computing system faults.”  
**Rationale:** Specifies monitoring and automated recovery behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, NFR-008, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-004]: Provide limited real-time data processing/probing tools (auto-correlation display)  
**Description**: “The Correlator Monitor and Control System shall perform limited amounts of real-time data processing and probing such as providing tools to collect and display auto correlation products.”  
**Rationale:** Describes a concrete system capability/tooling function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-005]: Provide easy system access for testing and debugging  
**Description**: “Test/debug access: in production, must require per-incident approval, audit log start/stop, MFA by TOTP or FIDO2, and automatically expire access after job/incident closure.” (Derived from FR-005; Next action: Split requirement into sub-items per access phase and acceptance criteria.)  
**Rationale:** Describes an operational function enabling test/debug access.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-020, NFR-014  
- **Conflicts with:** NFR-014, NFR-015  
---

[FR-006]: Provide system-wide access to correlator system states  
**Description**: “The Correlator monitor subsystem will provide VLA Expansion Project system wide access to all correlator system states including the Monitor and Control System supervisor system state.”  
**Rationale:** Defines an information access function (exposing states).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, NFR-007  
- **Conflicts with:** NFR-014  
---

[FR-007]: Provide time-synchronous monitor information when required  
**Description**: “Some of this information will be provided on a time synchronous basis as required by other systems…”  
**Rationale:** Specifies a mode of delivering monitoring data (time-synchronous).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006, NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-008]: Provide request-based monitor information when required  
**Description**: “…and other information will only be presented on a request basis.”  
**Rationale:** Defines on-demand query behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006  
- **Conflicts with:** NFR-020  
---

[FR-009]: Provide concise time/location-referenced error and status messages with controllable content  
**Description**: “messages.proto includes {timestamp_utc, wallclock_local, location_id, message_id, severity, content} with type constraints and validation.” (Derived from FR-009; Next action: Produce initial schema and add to requirement baseline.)  
**Rationale:** Defines message generation and formatting behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, NFR-010, NFR-011  
- **Conflicts with:** NFR-020  
---

[FR-010]: Translate received configurations into goal-oriented hardware configuration tables  
**Description**: “The translation will provide the correlator with specific goal oriented hardware configuration tables to satisfy the configuration requested…”  
**Rationale:** Specifies a concrete output artifact (configuration tables) produced by translation.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, ASR-002  
- **Conflicts with:** NFR-020  
---

[FR-011]: Provide a human GUI interface for correlator configuration using the same table structures  
**Description**: “A second interface with a human GUI will also allow for configuration of the correlator hardware, preferably through the same table structures used above.”  
**Rationale:** Describes a user-facing configuration function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-010, FR-022, NFR-014  
- **Conflicts with:** NFR-014  
---

[FR-012]: Provide required data sets to Backend Data Processing System over a secondary virtual network  
**Description**: “Specific data sets required by the Backend Data Processing System will be provided in a timely and robust fashion over a secondary virtual network.”  
**Rationale:** Defines an external data delivery function and interface path.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, ASR-003, NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-013]: Spool ancillary monitor data to prevent loss during temporary network outages  
**Description**: “Monitor data spooled for up to 24 hours at peak rate before loss; overrun triggers alert.” (Derived from FR-013; Next action: Define buffer sizing and policy for data spooling.)  
**Rationale:** Specifies buffering/spooling behavior to preserve data.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, FR-006, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-014]: Allow control of data sample rates and contents via M&C or backend controller  
**Description**: “Data sample rates and contents will be fully controllable via either the VLA Expansion Project Monitor and Control System or the Backend processing controller.”  
**Rationale:** Describes a controllability function for sampling configuration.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, FR-012, NFR-014  
- **Conflicts with:** NFR-020  
---

[FR-015]: Accept external data feeds (models, time standards, phase corrections) and package with control data  
**Description**: “The Master Correlator Control Computer will accept external data feeds for models, time standards, fiber-link phase corrections and other required data to be packaged with control data delivered to the correlator hardware.”  
**Rationale:** Defines ingestion and packaging behavior for control delivery.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, ASR-001  
- **Conflicts with:** NFR-020  
---

[FR-016]: Attempt recovery from failure or hot-swapped hardware devices  
**Description**: “The ability to attempt recovery from failure or hot-swapped hardware devices will be built into this system.”  
**Rationale:** Specifies recovery behavior in response to failures/hot-swap events.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, NFR-008, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-017]: Issue alert notice when a CMIB subsystem fails and does not respond to self-heal  
**Description**: “Should a CMIB subsystem fail and not respond to reboot requests or other self-heal attempts, an alert notice will be issued…”  
**Rationale:** Defines alerting behavior on unrecoverable failure.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-016, NFR-008  
- **Conflicts with:** NFR-020  
---

[FR-018]: Automatically restart and reconfigure CMIB subsystem into current operational environment  
**Description**: “The CMIB subsystem will then be automatically restarted and configured back into the current operational environment.”  
**Rationale:** Specifies automated restart and reconfiguration behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-016, NFR-008  
- **Conflicts with:** NFR-020  
---

[FR-019]: Support failover by rerouting communications to secondary master on primary hard failure  
**Description**: “...any hard failure in the primary node can be corrected by simply rerouting Monitor and Control System communications to the secondary.”  
**Rationale:** Defines failover behavior and operational procedure.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-020]: Provide software tools for users at all access levels (including low-level CMIB CLI)  
**Description**: “Software tools will be provided to assist the user at all access levels from system wide configuration and control to a low level CMIB command line instruction.”  
**Rationale:** Describes tooling functions for different user roles.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-016  
- **Conflicts with:** NFR-014  
---

[FR-021]: Provide remote inspection/monitoring and fault tracing to hot-swappable subsystem  
**Description**: “Tool supports only encrypted, authenticated sessions; all device status/readout is logged and RBAC enforced.” (Derived from FR-021; Next action: Specify protocol, security, and acceptance steps for remote inspection.)  
**Rationale:** Defines remote diagnostic and fault isolation functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006, FR-020, NFR-014  
- **Conflicts with:** NFR-014  
---

[FR-022]: Provide remote access for software developers for troubleshooting off-hours  
**Description**: “Remote developer access to production systems requires active incident, approval ticket, pre-scheduled 2-hour window, and explicit logging.” (Derived from FR-022; Next action: Decompose by access type and environment; specify concrete lift/approval process for prod.)  
**Rationale:** Describes a remote access function for a user group.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-015  
- **Conflicts with:** NFR-014  
---

[FR-023]: Use network switches to distribute traffic within a rack  
**Description**: “Network switches shall be employed to distribute traffic within a correlator rack and where their use will significantly reduce overall network wiring complexity.”  
**Rationale:** Specifies a required networking function/behavior in deployment.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-020  
---

[FR-024]: Provide redundant communication path between Master and Power Control for remote reboot  
**Description**: “There shall be a redundant communication path between the Master Correlator Control Computer and Correlator Power Control Computer to provide for remote reboot in the event of a networking or computing failure.”  
**Rationale:** Defines a concrete redundancy function enabling remote reboot.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-005, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-025]: CMIB reads 16-bit identifier and forms unique IP address (hot-swap carryover)  
**Description**: “16-bit identifier for each CMIB shall map to IP as 10.24.<high8bit>.<low8bit>; identifier allocation documented in Table 7.” (Derived from FR-025; Next action: Publish identifier/IP mapping algorithm.)  
**Rationale:** Specifies device identification and addressing behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-005, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-026]: CMIB read back contents of writeable hardware control registers  
**Description**: “The CMIB shall be able to read back the contents of all writeable hardware control registers where meaningful.”  
**Rationale:** Defines a hardware interrogation function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006  
- **Conflicts with:** NFR-020  
---

[FR-027]: Provide correlator hardware state via interrogation across CMIB bus (desired)  
**Description**: “It is desired that the state of the correlator hardware be available through interrogation across the CMIB bus for monitoring and fault tolerance.”  
**Rationale:** Describes a monitoring function (noted as “desired” but still a requirement-like statement).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006, FR-026  
- **Conflicts with:** NFR-020  
---

[FR-028]: Support external command to reboot CMIB with option to force hardware warm boot  
**Description**: “The CMIB shall have control of hardware warm boots such that an external command from the Master Correlator Control Computer to reboot the CMIB shall have an option to force a hardware warm boot.”  
**Rationale:** Defines a control function (reboot with warm-boot option).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-016  
- **Conflicts with:** NFR-020  
---

[FR-029]: Provide externally visible indicator of CMIB operational status  
**Description**: “The carrier board for the CMIB shall have an externally visible indicator that will provide a user with a physical indication of CMIB operational status.”  
**Rationale:** Specifies a status indication function for operators.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** NFR-020  
---

[FR-030]: UPS signals power outage and remaining backup time to the system  
**Description**: “Acceptance: UPS sends status update every 60 seconds; event fields: event_type, time_remaining, timestamp.” (Derived from FR-030; Next action: Formalize message fields and reporting rate for UPS integration.)  
**Rationale:** Defines event notification and status reporting behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-031]: Provide remote logins for authorized users to access individual systems  
**Description**: “All computers within the Correlator Monitor and Control System system shall have the ability for authorized users to directly access individual systems for maintenance and monitoring through remote logins.”  
**Rationale:** Describes a user access function (remote login).  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-015  
- **Conflicts with:** NFR-014  
---

[FR-032]: Provide hardware watchdog timer to reboot on system hang and autonomously return to service  
**Description**: “Each computer system… shall have a hardware based watchdog timer configured to reboot… in the case of a system hang. Reboots should result in minimal system interruptions with the offending CPU reconfiguring and returning to service autonomously.”  
**Rationale:** Specifies automated detection and recovery behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-033]: Centralize lower-level error/debug messages at Master layer; avoid direct CPU access  
**Description**: “All lower system error and debug messages shall be present at the Master Correlator Control Computer layer… it should never be necessary to directly access a CPU to display error messages.”  
**Rationale:** Defines message aggregation and access behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-009, NFR-010  
- **Conflicts with:** NFR-020  
---

[FR-034]: Categorize and filter error/debug messages by content/detail/rate  
**Description**: “All system error and debug messages shall be categorized… such that message traffic can be filtered as to content, detail, and message rate.”  
**Rationale:** Describes message management functions (categorization/filtering).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-033  
- **Conflicts with:** NFR-020  
---

[FR-035]: Timestamp inter-layer messages with UTC and wall-clock; stamp by message type  
**Description**: “All messages passed between… layers shall have both UTC and wall clock time stamp information… Error messages… discovery time, control messages… generation time.”  
**Rationale:** Defines message enrichment behavior (timestamping rules).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-009, FR-033  
- **Conflicts with:** NFR-020  
---

[FR-036]: Provide authorized-user software for full access to messaging/monitor/control traffic  
**Description**: “All monitor/control traffic viewers enforce RBAC and mask data fields above role clearance.” (Derived from FR-036; Next action: Amend tooling requirement to include data filtering and access checks.)  
**Rationale:** Describes a tooling/access function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-015  
- **Conflicts with:** NFR-014  
---

[FR-037]: Provide GUI for test software enabling remote access through VCI  
**Description**: “A Graphical User Interface shall be provided… to access the Correlator Monitor and Control System remotely through the VCI.”  
**Rationale:** Defines a user interface function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036, ASR-002, NFR-014  
- **Conflicts with:** NFR-014  
---

[FR-038]: Detect/report/auto-remediate abnormal conditions (self-monitoring)  
**Description**: “The Correlator Monitor and Control System shall be self-monitoring… detecting, reporting on and automatically taking action to remedy or lessen the impact of… processor hardware failure, operating system hangs or crashes, temperature or voltage deviations, computational performance below minimum specifications, computational error rates above maximum specification, internal communications failures.”  
**Rationale:** Specifies detection, reporting, and automated mitigation functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-032, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-039]: Continue processing configuration/control events until queues exhausted during comms loss  
**Description**: “Minimum of 96 hours of config/control event queue storage for processing during outage.” (Derived from FR-039; Next action: Add buffer/queue sizing statement to requirement.)  
**Rationale:** Defines behavior under degraded connectivity (queue-based continuation).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002, FR-013, NFR-009  
- **Conflicts with:** NFR-020  
---

[FR-040]: Support idle state and resume operations with minimal delay  
**Description**: “The EVLA Correlator Monitor and Control System shall be able to sit at idle and resume operations with minimal delay.”  
**Rationale:** Describes operational behavior (idle/resume).  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-041]: Enforce unique user identification and deny access if unidentified  
**Description**: “Acceptance: X.509 certificates used for access must have 90-day max lifetime, automated rotation, and user revocation time ≤15 minutes after admin action; if CRL check cannot be performed, access is denied; include policy doc link.” (Derived from FR-041; Next action: Draft lifecycle procedures or reference compliance doc; insert policy for denial on CRL failure.)  
**Rationale:** Defines authentication behavior and access decision rule.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-015  
- **Conflicts with:** FR-005, FR-022  
---

[FR-042]: Log all access attempts  
**Description**: “Logs must be written only to encrypted volume; purge via admin job after 1 year.” (Derived from FR-042; Next action: Specify audit log lifecycle and security.)  
**Rationale:** Specifies audit logging behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, NFR-015  
- **Conflicts with:** NFR-020  
---

[FR-043]: Provide role-based privilege management (grant/revoke per user; least-privilege by need)  
**Description**: “Systems operations should be given unrestricted access… and should have the authority to grant and revoke privileges on a per-user basis… access level is needed that allows privileges to be granted on a per-user and what-do-you-need-to-do basis.”  
**Rationale:** Describes authorization/privilege management functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, NFR-014  
- **Conflicts with:** FR-005  
---

[FR-044]: Require users to login with unique identification  
**Description**: “All users… shall login using some form of unique identification.”  
**Rationale:** Defines a required user interaction/authentication function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041  
- **Conflicts with:** None identified  
---

[FR-045]: Provide system administrator unrestricted access  
**Description**: “A system administrator shall have unrestricted access to all aspects of the EVLA Correlator Monitor and Control System.”  
**Rationale:** Defines an authorization rule for a role.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-043  
- **Conflicts with:** None identified  
---

[FR-046]: Maintain per-user access properties defining privileges  
**Description**: “User access record: {user_id, active_roles:[], privileges:[], last_updated:timestamp}.” (Derived from FR-046; Next action: Add user privilege schema to admin docs/requirement.)  
**Rationale:** Specifies user privilege data management behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-043  
- **Conflicts with:** None identified  
---

[FR-047]: Admin can create/add users  
**Description**: “The administrator shall have the ability to create and add a new user…”  
**Rationale:** Defines a user management function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045, FR-046  
- **Conflicts with:** None identified  
---

[FR-048]: Admin can remove users  
**Description**: “The administrator shall have the ability to remove a user…”  
**Rationale:** Defines a user management function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045, FR-046  
- **Conflicts with:** None identified  
---

[FR-049]: Admin can edit user access properties  
**Description**: “Only role/privileges, email, status are editable; each change triggers audit log event.” (Derived from FR-049; Next action: Clarify set of editable properties and log policies.)  
**Rationale:** Defines authorization administration behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045, FR-046  
- **Conflicts with:** None identified  
---

[FR-050]: Admin can block all access globally or selectively by user  
**Description**: “The administrator shall have the ability to block all access… for all users or selectively by user.”  
**Rationale:** Defines an access control function for emergency/operations.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045, FR-046  
- **Conflicts with:** FR-022  
---