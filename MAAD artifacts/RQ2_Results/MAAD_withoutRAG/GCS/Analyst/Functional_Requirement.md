# Functional Requirements Results (FRs)

[FR-001]: Enforce operational levels with restricted access  
**Description**: “The Gemini system, when powered on, exists in one of several disjoint operational levels. Access to the system is restricted according to the current level of operation.”  
**Rationale:** Defines system behavior for mode/level-based access control.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008  
- **Conflicts with:** —  
---

[FR-002]: Provide operational levels (observing/maintenance/test)  
**Description**: “The observing level is the ‘normal’ operational mode… The maintenance level permits access… The most primitive operational level, test level operation is used for installation/deinstallation of subsystems…”  
**Rationale:** Enumerates required system operating states and their intended use.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001  
- **Conflicts with:** —  
---

[FR-003]: Provide access modes (observing/monitoring/operation/planning/testing/administrative)  
**Description**: “At any level… the software imposes… access modes… The access modes provided… observing… monitoring… operation… planning… testing… administrative…”  
**Rationale:** Specifies required system functions/modes available to users.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-002  
- **Conflicts with:** —  
---

[FR-004]: Observing mode via sequencer only (no direct telescope/instrument control)  
**Description**: “Access to the system is through the sequencer with no direct control of telescope and instruments.”  
**Rationale:** Defines the control pathway and disallows direct control in a specific mode.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, NFR-008  
- **Conflicts with:** FR-006, FR-018  
---

[FR-005]: Monitoring mode shall be read-only and non-intrusive  
**Description**: “The monitoring mode is a special, read-only case… Under no circumstances should monitoring affect the performance of an ongoing observation.”  
**Rationale:** Defines monitoring behavior and its effect on operations.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003  
- **Conflicts with:** FR-027 (if monitoring implemented using invasive mechanisms)  
---

[FR-006]: Operation mode provides direct control of telescope/instruments for authorized users  
**Description**: “The operation mode is the access used for direct control of the telescope and instruments… normally available only to the Telescope Operator and the science program sequencer…”  
**Rationale:** Defines a functional capability (direct control) and who can use it.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-008  
- **Conflicts with:** FR-004, FR-010, FR-011  
---

[FR-007]: Planning mode provides virtual telescope simulator and online databases; no real telescope access  
**Description**: “Actual access to the telescope is not permitted… the virtual telescope capability… provides a telescope simulator… useful for planning observations, as are on-line databases.”  
**Rationale:** Specifies planning functions and constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-019, FR-020, FR-043  
- **Conflicts with:** —  
---

[FR-008]: Testing mode allows full direct control of any subsystem, non-intrusive to ongoing observations  
**Description**: “The testing mode access allows full, direct control of any subsystem… Under no circumstances should testing affect the performance of an ongoing observation.”  
**Rationale:** Defines testing behavior and isolation constraint.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-003  
- **Conflicts with:** FR-027 (if shared resources not isolated)  
---

[FR-009]: Administrative mode provides status/scheduling/utilization inquiry only, non-intrusive  
**Description**: “During the administrative mode, it is possible to inquire about system utilization… No control is available… Under no circumstances should administrative access affect the performance of an ongoing observation.”  
**Rationale:** Defines administrative capabilities and restrictions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003, NFR-008  
- **Conflicts with:** —  
---

[FR-010]: Observing astronomers shall not directly control telescope; shall query status anytime  
**Description**: “Observing astronomers shall have no privileges as far as the direct control of the telescope… They shall not be able to send control commands directly but they must be able to enquire about the status… at any time.”  
**Rationale:** Defines role-based functional permissions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-008, FR-026  
- **Conflicts with:** FR-006  
---

[FR-011]: Programs may request telescope control functions without allowing direct command entry by observers  
**Description**: “Programs… may have the capability of direct control… would allow… requested… function but would not allow the observer to enter… a command to slew…”  
**Rationale:** Defines mediated control via programs/sequences.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, FR-017, NFR-008  
- **Conflicts with:** FR-010 (if improperly implemented)  
---

[FR-012]: Provide automatic sequencer as normal operation; allow limited interaction via scheduler  
**Description**: “Traditional interactive operation shall normally be replaced by operation via an automatic sequencer… user will interact with the scheduler program, rather than with the control programs directly.”  
**Rationale:** Specifies required control workflow and interaction mechanism.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-017, FR-033  
- **Conflicts with:** FR-013 (direct interactive enabling must be exceptional)  
---

[FR-013]: Allow operations staff to enable direct interactive operation (not normal)  
**Description**: “Operations staff will be able to enable direct interactive operation, but this shall not be considered as the normal operation mode…”  
**Rationale:** Defines a functional override/escape path for staff.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008  
- **Conflicts with:** FR-012 (if used as default)  
---

[FR-014]: Allow breaking and resequencing of observing queue  
**Description**: “It must also be possible to break and resequence this queue… as a result of the quality assessment of previous data.”  
**Rationale:** Defines scheduler/queue manipulation capability.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-017, FR-045  
- **Conflicts with:** —  
---

[FR-015]: Support interactive capability for specific functions; evaluate for automation  
**Description**: “for some functions… it must be necessary to include interactive capability… each instance… examined as a candidate for automation…”  
**Rationale:** Requires support for interactive control for certain functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, FR-013  
- **Conflicts with:** —  
---

[FR-016]: Operations staff privileges: access all commands/maintenance procedures; direct control of physical units; restrictions while subsystems in normal operation  
**Description**: “Operations staff shall have privileges to access all commands and maintenance procedures… includes direct control… However, they shall not have access to subsystems while these are in normal operation.”  
**Rationale:** Defines role permissions and operational restrictions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-008  
- **Conflicts with:** FR-006 (requires arbitration/locking), FR-027  
---

[FR-017]: Queue-based observing: support preprogrammed observing sequences; queue/resort based on conditions and rules  
**Description**: “To maximize… it must be possible to queue… preprogrammed observing sequences… It should be possible to resort the queue… based on… current site conditions, and other rules…”  
**Rationale:** Defines scheduling/automation capabilities.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, FR-046, FR-047  
- **Conflicts with:** —  
---

[FR-018]: Remote operations: enable full operations remotely; team observing; restrict operations by site dynamically  
**Description**: “All software should be developed to permit remote operations… It should be possible to do full operations remotely… Team observing… must be possible to restrict specific operations to specific remote sites… independent… and dynamic.” Updated per evaluator: Policy admin API permits operator to add/remove allowed remote sites and validate policy changes take effect within 60s. Owner: Team-API; Next action: Document/admin API and runtime test for site restriction  
**Rationale:** Defines remote capability and dynamic policy enforcement.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-008, FR-031  
- **Conflicts with:** FR-021 (remote control restricted for safety)  
---

[FR-019]: Provide virtual telescope environment and simulator support across control software  
**Description**: “This simulator should function within the virtual telescope environment… All control software must provide support for simulated use within the virtual telescope.”  
**Rationale:** Requires a simulation capability integrated with control software.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-020, FR-066  
- **Conflicts with:** —  
---

[FR-020]: Simulator shall consider targets, weather, and instrument configurations  
**Description**: “This software must consider target positions, weather conditions, and instrument configurations.”  
**Rationale:** Defines required simulation behaviors/inputs.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-019, FR-046  
- **Conflicts with:** —  
---

[FR-021]: Remote control restricted to locations with hard-wired stop, real-time video/audio, and direct control access  
**Description**: “Remote control will be restricted… for safety… cannot be issued without… hard wired ‘stop’ button, real time video and audio and control of the telescope.”  
**Rationale:** Defines functional authorization constraints for remote control.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-012, NFR-008  
- **Conflicts with:** FR-018 (full remote operations must respect this)  
---

[FR-022]: Remote users shall not directly control the system; submit commands via scheduler; remote keyboard non-effective for monitoring  
**Description**: “Remote users shall not control any part… directly… use a remote User interface to submit commands to… scheduler… The monitor's keyboard would not have any effect…”  
**Rationale:** Defines remote interaction model and input suppression for monitor views.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, FR-018, NFR-008  
- **Conflicts with:** —  
---

[FR-023]: Provide remote monitoring/eavesdropping with selectable information; keyboard has no local effect  
**Description**: “Remote monitoring… allows the remote user to ‘pick and choose’… The remote keyboard will have no effect on the local user's environment.”  
**Rationale:** Defines remote monitoring behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, NFR-003  
- **Conflicts with:** —  
---

[FR-024]: Provide remote diagnostic/monitoring access from base facility  
**Description**: “Remote access… is required for monitoring and diagnostic purposes… must be possible from the… base facility.”  
**Rationale:** Defines remote support function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-018, NFR-008  
- **Conflicts with:** —  
---

[FR-025]: Provide parallel access to mounted instruments with one active instrument; inactive instrument parallel activities  
**Description**: “Parallel access to all the mounted instruments shall be provided, though only one instrument has access to the telescope beam… inactive instruments… take calibration… hot standby… work at all operation levels…”  
**Rationale:** Defines multi-instrument concurrency behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-060, FR-061  
- **Conflicts with:** FR-027  
---

[FR-026]: Prevent inactive instrument actions from adversely impacting active instrument  
**Description**: “Regardless of the status of an inactive instrument, it shall not be possible for any of its permitted actions to adversely impact the active instrument.”  
**Rationale:** Functional safety/isolation behavior between instruments.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025, FR-027  
- **Conflicts with:** —  
---

[FR-027]: Implement Access Mode Allocation system for critical resource assignment; avoid deadlock  
**Description**: “Protection against accidental interference… using an Access Mode Allocation system… Critical resources… assigned solely through this allocation system… must ensure… cannot remain deadlocked…”  
**Rationale:** Defines required resource arbitration and deadlock prevention behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, NFR-008  
- **Conflicts with:** FR-016 (if bypassing allocation), FR-025  
---

[FR-028]: Provide procedures for common tasks (startup/shutdown/self-tests/configuration)  
**Description**: “procedures must be implemented… telescope start-up and shutdown… self-testing… instrument start-up… self-diagnosis… Configuration and reconfiguration.”  
**Rationale:** Specifies required operational workflows.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-053, FR-054  
- **Conflicts with:** —  
---

[FR-029]: Provide multi-point monitoring (automatic displays + explicit queries) with permission procedures  
**Description**: “multi-point monitoring… Monitoring shall exist both in the form of automatic displays… and… explicit access… All other users… have to… get permission…”  
**Rationale:** Defines monitoring function and operational gating.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, NFR-008  
- **Conflicts with:** —  
---

[FR-030]: Allow simple logon/configuration to access any subsystem from any station (subject to privileges)  
**Description**: “they shall be able to access… any part… with a simple logon and configuration… any subsection… accessible and controllable from any single point (with protection…).”  
**Rationale:** Defines access function across stations.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008, FR-031  
- **Conflicts with:** —  
---

[FR-031]: Support simultaneous multi-mode access by a user  
**Description**: “It is entirely possible for a single user to be accessing the system through several modes simultaneously… typical… Telescope Operator…” Updated per evaluator: UI/API exposes current modes per user session; only permitted combinations launch; conflicting requests return explicit error. Owner: Team-API; Next action: Define and document session/mode state model and error handling for multi-mode access.  
**Rationale:** Functional concurrency requirement for sessions/modes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003, FR-027  
- **Conflicts with:** —  
---

[FR-032]: Provide common command set across subsystems (status/version/self-tests); common IOC commands (start/stop/init/reset)  
**Description**: “All subsystems must respond to a common set of commands… inquiries as to version, perform self-tests… All IOC subsystems must respond to additional common commands… start, stop, initialize, reset…” Updated per evaluator: Subsystems must support: CMD_VERSION, CMD_SELFTEST, CMD_START, CMD_STOP, CMD_INIT, CMD_RESET; each accepts standard command message format as per published interface schema. Add: See doc/API/command-enum.md for command schema. Example: {cmd: "CMD_VERSION"} → {version: "2.3.1", build: "2024-03-17"}. Owner: Team-API; Next action: Draft and circulate common command API contract.  
**Rationale:** Defines standardized command capabilities across components.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-053, FR-065  
- **Conflicts with:** —  
---

[FR-033]: Use uniform ACK/NAK protocol with timeouts; handshake between IOCs  
**Description**: “support structure… reliable, with a uniform ACK/NAK protocol… Timeouts… 500 msec… Handshaking… within 100-200 msec…”  
**Rationale:** Defines required communication behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-002  
- **Conflicts with:** —  
---

[FR-034]: Store detector data effectively; support lossless compression for transmission; store preprocessed IR data only  
**Description**: “Data from detectors must be stored… Data… may be compressed using a loss-less compression technique for transmission… For data that requires preprocessing… only the preprocessed data is stored.”  
**Rationale:** Defines data handling/storage behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036, FR-037  
- **Conflicts with:** NFR-006 (if lossy used where prohibited)  
---

[FR-035]: Store instrument/detector data as compressed data in a standard format  
**Description**: “Data from all instruments and detectors is stored as compressed data, using a standard format.”  
**Rationale:** Defines data storage format behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-034  
- **Conflicts with:** —  
---

[FR-036]: Provide online data disk storage for quick-look; automatic archiving to Gemini Archive  
**Description**: “A second level of storage… data disk(s)… Quick-look… Archiving of data is automatically done… to the Gemini Archive subsystem.”  
**Rationale:** Defines storage tiers and archiving action.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045, NFR-007  
- **Conflicts with:** —  
---

[FR-037]: Transmit data to home institutes in FITS with full headers  
**Description**: “Data is transmitted… using a FITS format and contains all header information…”  
**Rationale:** Defines export/transfer behavior and format.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-035  
- **Conflicts with:** —  
---

[FR-038]: Provide rough-image fast transmission and high-quality transmission  
**Description**: “The system must allow for fast transmission of rough images… This high-quality transmission must require less than 20 sec, and can only be assisted with loss-less compression.”  
**Rationale:** Defines image transmission capabilities (with performance constraints captured in NFRs).  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006, NFR-005  
- **Conflicts with:** —  
---

[FR-039]: Determine user privileges during login  
**Description**: “These privileges should be determined in a simple manner during logging into the system.” Updated per evaluator: Authentication API accepts: {username:string, password:string, mfa_token?:string}; returns {session_token:string, user_id:string, roles:[string]}; failure returns {error_code:401|403, reason:string}. All attempts logged to audit trail. Acceptance: See doc/api/authentication.md for request/response JSON schema, password strength regex, audit log samples for login failure. Owner: Team-API; Next action: Stub authentication API and document policies with test vectors.  
**Rationale:** Defines authentication/authorization behavior at login.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008  
- **Conflicts with:** —  
---

[FR-040]: Provide built-in test (BIT), self-test sequences, and regression tests  
**Description**: “software shall contain built-in test (BIT)… provide for execution of self-test sequences… Regression tests should be a part of every… package.”  
**Rationale:** Defines test/diagnostic functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, FR-028  
- **Conflicts with:** —  
---

[FR-041]: Notify users of faults with origin/problem; enable electronic logging; support verbosity levels  
**Description**: “Subsystems must notify the user when faults occur… specific… capable of being electronically logged… useful to have multiple levels…”  
**Rationale:** Defines fault reporting behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-062, NFR-014  
- **Conflicts with:** —  
---

[FR-042]: Provide procedures to redefine environment to restart with remaining equipment after failure  
**Description**: “Should a subsystem fail… predefined procedures must exist to redefine the environment… operation can restart with the remaining equipment.”  
**Rationale:** Defines reconfiguration behavior for fault tolerance.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028, NFR-011  
- **Conflicts with:** —  
---

[FR-043]: Allow transfer of control between user stations via simple software reconfiguration on station hardware failure  
**Description**: “possible to transfer control from one user station to another via a simple software reconfiguration procedure.”  
**Rationale:** Defines control handover function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028, NFR-011  
- **Conflicts with:** —  
---

[FR-044]: Provide simulator replacement mechanism for subsystems  
**Description**: “Simple mechanisms should exist for replacing a subsystem with its simulation.”  
**Rationale:** Defines operational function for maintenance/test and integration.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-019, FR-066  
- **Conflicts with:** —  
---

[FR-045]: Provide quick-look processing synchronous with acquisition; usable within exposure sequences for feedback  
**Description**: “Quick-look… procedures suitable for fast on-line data preprocessing… Quick-look should be usable within exposure sequences to provide results and feedback parameters… without… manual intervention… should be synchronous.”  
**Rationale:** Defines processing workflow integrated with acquisition/control.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036  
- **Conflicts with:** FR-046 (acquisition precedence over near-line)  
---

[FR-046]: Provide near-line processing asynchronously; acquisition takes precedence  
**Description**: “Near-line processing… asynchronously from data acquisition… data acquisition takes precedence…” Updated per evaluator: Acceptance: During concurrent operation, data acquisition ops maintain ≤1% increased latency vs baseline, dropping near-line processes as needed; test plan exercises forced contention. Owner: Team-SRE; Next action: Define and test arbitration/policy function for acquisition vs near-line.  
**Rationale:** Defines sequencing/prioritization behavior between acquisition and processing.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-034  
- **Conflicts with:** FR-045 (if resources contend)  
---

[FR-047]: Provide online interactive access to archiving system (subject to archive policy)  
**Description**: “on-line interactive access to the data archiving system should exist… access to this database is possible…”  
**Rationale:** Defines an access function to archived data.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036, NFR-008  
- **Conflicts with:** —  
---

[FR-048]: Interface with star catalogues for automatic selection of guide/standard stars  
**Description**: “Computer access to star catalogues is also required, so that an automatic selection of candidate guide and standard stars can be made.”  
**Rationale:** Defines integration and automation behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-043 (planning environment), FR-007  
- **Conflicts with:** —  
---

[FR-049]: Integrate and interface with commercial/external software packages (e.g., DBMS)  
**Description**: “The … software must be able to interface with all commercial software packages… integrated… e.g.… DBMS… schedules, logs, problem reports…” Updated per evaluator: Integration layer wraps DBMS; supports versions 12.X and 13.X; all calls logged/audited; upgrade test plan included. Owner: Team-API; Next action: Write interface contract/document integration matrix for commercial SW.  
**Rationale:** Defines integration function with external systems.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-018  
- **Conflicts with:** NFR-008 (if external packages weaken security)  
---

[FR-050]: Provide centralized meteorological information access  
**Description**: “the meteorological information coming from a weather station should be available centrally.”  
**Rationale:** Defines required data availability function.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-026, FR-017  
- **Conflicts with:** —  
---

[FR-051]: Provide control-variable information on request; avoid delays/locking even when equipment faulty  
**Description**: “Control information on all controlled variables must be provided… on request. No request… shall produce a delay of control activities or locking, even if… equipment is not available or faulty.” Updated per evaluator: API returns: {timestamp: string (UTC ISO8601), variable: string, value: <type>, unit: string, statusCode: int, errorMessage?: string}. Add JSON schema definition. Acceptance: API documented at /api/control-variable-schema.json with all types, units, and status codes table. Owner: Team-API; Next action: Draft and release schema stub to API reference section.  
**Rationale:** Defines behavior for status queries under faults.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-011  
- **Conflicts with:** —  
---

[FR-052]: Provide time reference synchronization where necessary  
**Description**: “synchronization with the Time Reference System… is also necessary.”  
**Rationale:** Defines functional integration with time distribution.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** —  
---

[FR-053]: Provide subsystem self-check levels: background monitoring + full exercise module (startup/on-demand)  
**Description**: “Monitor level… background task… checking power… temperatures… correct responses… notify OCS… Full exercise… executed automatically during start-up and on demand… Problems… reported to the OCS…”  
**Rationale:** Defines diagnostic behaviors and OCS notification.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, NFR-011  
- **Conflicts with:** NFR-003 (must not disrupt observing)  
---

[FR-054]: Provide OCS safety response: bring system to safe state on danger notification/detection  
**Description**: “The Gemini system must be self-monitoring… quickly bring… to a safe state… Subsystems must be able to detect… and report it… software shall be able to bring… quickly to a safe state upon detection of danger.”  
**Rationale:** Defines safety behavior and response actions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-053, NFR-012  
- **Conflicts with:** —  
---

[FR-055]: Engineering/Maintenance mode shall ignore directives from other systems but still provide status  
**Description**: “A system that is operating in Engineering/Maintenance mode must ignore directives from other systems, though status information should still be provided…”  
**Rationale:** Defines operational gating behavior under maintenance.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-002  
- **Conflicts with:** FR-006 (control requests from others)  
---

[FR-056]: Support dynamic observing environment reconfiguration without restart; independent instrument/telescope startup/shutdown  
**Description**: “startup and shutdown of instruments independently of the telescope… Reconfiguration procedures must exist… dynamic… feasible during operations without the need to restart everything.”  
**Rationale:** Defines reconfiguration and lifecycle control behaviors.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028, FR-027  
- **Conflicts with:** —  
---

[FR-057]: Support simultaneous operation of multiple control/monitoring nodes  
**Description**: “allow simultaneous operation of up to six active control nodes and up to two more monitoring nodes… capable of coping with the load of 10 active nodes…” Updated per evaluator: Acceptance: When running 6 active and 2 monitoring nodes under reference workload, <obs_cmd_latency> increases ≤10% vs single-node baseline over 12h. Owner: Team-SRE; Next action: Add explicit multi-node load test plan as acceptance to FR-057.  
**Rationale:** Defines capacity behavior (quantitative limits captured in NFRs).  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** —  
---

[FR-058]: Provide system/version consistency checks at boot; version retrieval via commands  
**Description**: “On-line version control… At boot time… check the consistency of versions… Every system… able to supply its current version upon request.”  
**Rationale:** Defines operational/versioning functions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-019, FR-032  
- **Conflicts with:** —  
---

[FR-059]: Support table-driven parameter updates without recompilation; allow some runtime modification  
**Description**: “Table-driven software… Changing system constants… shall not require recompiling… updated as part of system startup… modifiable during operation.”  
**Rationale:** Defines configuration management behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-043, NFR-020  
- **Conflicts with:** NFR-012 (safety limits)  
---

[FR-060]: Provide stable, standardized visitor instrument interface as subset of existing instrumentation interface  
**Description**: “subset… made available through a standardized interface… goal… subset of the existing instrumentation interface… important… stable and long-lived…”  
**Rationale:** Defines required interface for a class of instruments.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, NFR-021  
- **Conflicts with:** —  
---

[FR-061]: Visitor instrument minimum interface: status, preprogrammed sequences, telescope offset/focus  
**Description**: “At a minimum this interface should support acquisition of status information… enter preprogrammed observing sequences and capability to offset the telescope position and focus.”  
**Rationale:** Defines minimum functional capabilities of the visitor instrument integration.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-060, FR-032  
- **Conflicts with:** —  
---

[FR-062]: Log sufficient information to recreate observation sequence; timestamp and index important events  
**Description**: “sufficient information be recorded during an observation to recreate the sequence of events… System logging information should include all important events, properly timestamped and indexed.”  
**Rationale:** Defines logging function and purpose.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-013, NFR-014  
- **Conflicts with:** NFR-003 (logging overhead)  
---

[FR-063]: Support engineering data logging at high rate short-term and low rate long-term; common format  
**Description**: “possible to log engineering data at up to 200 Hz… Long-term logging… at slower (1 Hz or less)… into a common format (baselined as SYBASE).”  
**Rationale:** Defines data logging behaviors and modes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-015, FR-062  
- **Conflicts with:** NFR-003 (performance impact)  
---

[FR-064]: Implement command retries for common timeouts/no-response automatically  
**Description**: “Command retries must be included… automatically in the command handling to avoid unnecessary error conditions.” Updated per evaluator: Acceptance: Table of retryable commands published; non-idempotent and safety commands not retried; max_retry and backoff parameters set per command; covered in test suite. Owner: Team-API; Next action: Write/publish retry policy for all commands.  
**Rationale:** Defines error-handling behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-011, FR-033  
- **Conflicts with:** NFR-012 (safety if retries on unsafe commands)  
---

[FR-065]: Maintain online database of telescope/instrument parameters; provide access at any operation level  
**Description**: “All telescope and instrument parameters are kept in an on line database… All telescope, instrument, and detector control information is to be available at any operation level.”  
**Rationale:** Defines core data management function and accessibility.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-017, NFR-008  
- **Conflicts with:** —  
---

[FR-066]: Provide software simulation module for each hardware subsystem; no hardware-specific dependencies  
**Description**: “all hardware subsystems must provide a software simulation module… responds in reasonable fashion… cannot require any hardware specific to the application.”  
**Rationale:** Defines simulation functionality per subsystem.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-019, FR-044  
- **Conflicts with:** —  
---