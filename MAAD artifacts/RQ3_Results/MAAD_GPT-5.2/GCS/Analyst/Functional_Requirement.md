# Functional Requirements Results

[FR-001]: Support disjoint operational levels with restricted access  
**Description**: “The Gemini system, when powered on, exists in one of several disjoint operational levels. Access to the system is restricted according to the current level of operation… observing level… maintenance level… test level.”  
**Rationale:** Defines system behavior (operational state model) and access behavior per state.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, NFR-007  
- **Conflicts with:** NFR-020 (remote transparency vs restrictions)  
---

[FR-002]: Provide access modes (observing/monitoring/operation/planning/testing/administrative)  
**Description**: “At any level… the software imposes… access modes… The access modes provided… observing mode… monitoring mode… operation mode… planning… testing mode… administrative mode.”  
**Rationale:** Enumerates required system functions (modes) and their intended capabilities.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-006  
- **Conflicts with:** NFR-020  
---

[FR-003]: Observing mode via sequencer only (no direct telescope/instrument control)  
**Description**: “Access to the system is through the sequencer with no direct control of telescope and instruments.”  
**Rationale:** Specifies a functional control path constraint for observing mode.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011  
- **Conflicts with:** FR-012 (direct interactive operation enablement)  
---

[FR-004]: Monitoring mode is read-only and non-intrusive  
**Description**: “The monitoring mode is a special, read-only case… Under no circumstances should monitoring affect the performance of an ongoing observation.”  
**Rationale:** Defines monitoring behavior and its read-only nature.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020  
- **Conflicts with:** NFR-001 (if monitoring load threatens performance)  
---

[FR-005]: Operation mode provides direct control for operator/sequencer  
**Description**: “The operation mode is the access used for direct control of the telescope and instruments… normally available only to the Telescope Operator and the science program sequencer…”  
**Rationale:** Defines who can perform direct control and in which mode.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-006  
- **Conflicts with:** FR-006 (astronomer no direct control)  
---

[FR-006]: Astronomers cannot send direct telescope control commands; can query status anytime  
**Description**: “Observing astronomers shall have no privileges as far as the direct control of the telescope is concerned… shall not be able to send control commands directly but… must be able to enquire about the status… at any time.”  
**Rationale:** Defines authorization behavior and allowed actions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020, NFR-006  
- **Conflicts with:** FR-005 (direct control)  
---

[FR-007]: Programs may request telescope control functions without allowing raw command entry  
**Description**: “Programs… may have the capability of direct control… allow… observing program which requested a telescope control function but would not allow the observer to enter… a command to slew…”  
**Rationale:** Defines functional mediation of control via programs.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006  
- **Conflicts with:** FR-006 (if not properly mediated)  
---

[FR-008]: Astronomers typically have control access to instruments  
**Description**: “Astronomers are typically given control access to instruments, however.”  
**Rationale:** Defines functional access scope for a user class.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006  
- **Conflicts with:** FR-003 (if instrument control bypasses sequencer in observing mode)  
---

[FR-009]: Provide science planning mode with virtual telescope simulator and online databases  
**Description**: “Access… during science planning… virtual telescope capability… provides a telescope simulator… as are on-line databases.”  
**Rationale:** Requires planning functionality including simulation and database access.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-030, ASR-006  
- **Conflicts with:** NFR-019 (internet use limited for essential tasks)  
---

[FR-010]: Provide automatic sequencer as primary interaction mechanism  
**Description**: “Traditional interactive operation shall normally be replaced by operation via an automatic sequencer… Interaction… user will interact with the scheduler program…”  
**Rationale:** Defines core operational function (sequencing/scheduling-driven control).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-013  
- **Conflicts with:** FR-012 (direct interactive operation)  
---

[FR-011]: Allow breaking and resequencing the observing queue  
**Description**: “It must also be possible to break and resequence this queue… as a result of the quality assessment of previous data.”  
**Rationale:** Defines required queue manipulation behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-040  
- **Conflicts with:** NFR-001 (if resequencing impacts ongoing observation performance)  
---

[FR-012]: Operations staff can enable direct interactive operation (not normal)  
**Description**: “Operations staff will be able to enable direct interactive operation, but this shall not be considered as the normal operation mode…”  
**Rationale:** Defines an operational override function.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006  
- **Conflicts with:** FR-010  
---

[FR-013]: Support interactive capability for selected functions; evaluate for automation  
**Description**: “For some functions… it must be necessary to include interactive capability… each instance… examined as a candidate for automation.”  
**Rationale:** Requires support for interactive control for certain tasks.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012  
- **Conflicts with:** FR-010 (automation-first)  
---

[FR-014A]: Allow simultaneous user interface access to all mounted instruments  
**Description**: “Parallel access to all the mounted instruments shall be provided…” (Derived from FR-014; Next action: Decompose into atomic requirements.)  
**Rationale:** Defines multi-instrument operational behavior (UI access concurrency).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015  
- **Conflicts with:** NFR-001 (resource contention)  
---

[FR-014B]: Enforce single active instrument beam access at any time  
**Description**: “...though only one instrument has access to the telescope beam (active instrument).” (Derived from FR-014; Next action: Decompose into atomic requirements.)  
**Rationale:** Defines exclusivity constraint on telescope beam access.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015  
- **Conflicts with:** NFR-001 (resource contention)  
---

[FR-015]: Inactive instruments can calibrate/standby/operate at all levels without impacting active instrument  
**Description**: “Inactive instruments… take calibration… prepare… hot standby… work at all… levels… Regardless… it shall not be possible… to adversely impact the active instrument.”  
**Rationale:** Defines allowed behaviors and isolation constraints.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, NFR-006  
- **Conflicts with:** FR-014 (if isolation not enforced)  
---

[FR-016]: Support visitor instruments via standardized subset server interface  
**Description**: “Visitor instruments… subset… standardized interface… view all instruments as operating as servers… Visitor instruments must be capable of operating in this mode… interface… subset of existing instrumentation interface.”  
**Rationale:** Defines integration behavior and required interface style.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007, NFR-015  
- **Conflicts with:** NFR-014 (evolving standards vs stable interface)  
---

[FR-017]: Minimum visitor instrument interface capabilities  
**Description**: “At a minimum this interface should support acquisition of status information… capability to enter preprogrammed observing sequences and capability to offset the telescope position and focus.”  
**Rationale:** Enumerates concrete functions required for visitor instrument support.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-020, FR-010  
- **Conflicts with:** NFR-006 (privilege restrictions)  
---

[FR-018]: Provide observatory simulator usable by instruments via standard interfaces  
**Description**: “Provision of a Gemini observatory simulator… appearing to the instrument as a standard set of hardware and software interfaces…”  
**Rationale:** Requires a simulator function for integration/testing/support.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006  
- **Conflicts with:** NFR-001 (if simulator affects performance in production)  
---

[FR-019]: Simple logon/config to access any part of system from any station per privileges  
**Description**: “Independently of the location… they shall be able to access (according to their privileges) any part… with a simple logon and configuration operation.” Access to any part of system from any station must be mediated by RBAC; all privilege escalation events must generate an audit log entry reviewed weekly. (Next action: Specify RBAC model, audit mechanisms, and acceptance tests for privilege enforcement.)  
**Rationale:** Defines access and configuration behavior across stations.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, NFR-020  
- **Conflicts with:** NFR-018 (essential tasks on project-controlled resources)  
---

[FR-020]: Provide multi-point monitoring with automatic displays and explicit status queries  
**Description**: “Monitoring shall exist both in the form of automatic displays… and… explicit access… from any point.”  
**Rationale:** Defines monitoring functions and access patterns.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021  
- **Conflicts with:** NFR-001 (monitoring load)  
---

[FR-021]: Subsystems provide control-variable status on request without delaying control  
**Description**: “Control information on all controlled variables must be provided by all subsystems on request. No request… shall produce a delay of control activities or locking…”  
**Rationale:** Defines required subsystem behavior for status servicing.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, NFR-003  
- **Conflicts with:** NFR-001 (resource limits)  
---

[FR-022]: Support remote operations (remote observing/control/monitoring/diagnostics)  
**Description**: “Remote operations includes… remote observing… remote telescope operation… eavesdropping, monitoring, configuration, and diagnosis… All software should be developed to permit remote operations… It should be possible to do full operations remotely… Team observing… supported.”  
**Rationale:** Defines a major set of system functions for distributed operation.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-020, NFR-006  
- **Conflicts with:** FR-023 (remote control restricted)  
---

[FR-023]: Restrict remote telescope control to specific sites; dynamic restriction independent of operations  
**Description**: “It must be possible to restrict specific operations to specific remote sites… method… independent of the operations themselves, and dynamic.”  
**Rationale:** Defines functional authorization and policy enforcement behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, ASR-002  
- **Conflicts with:** NFR-020 (transparency)  
---

[FR-024]: Remote control requires local safety presence (stop button, video/audio, control)  
**Description**: “Remote control will be restricted… for safety… commands cannot be issued without a staff member… access to a hard wired ‘stop’ button, real time video and audio and control of the telescope.”  
**Rationale:** Defines operational control preconditions and safety gating behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-012, NFR-013  
- **Conflicts with:** FR-022 (full remote operations)  
---

[FR-025]: Remote users submit commands via scheduler; remote keyboard does not affect local environment  
**Description**: “Remote users shall not control… directly… use a remote User interface to submit commands to… scheduler… monitor’s screen appears as a duplicate… keyboard would not have any effect…”  
**Rationale:** Defines remote interaction behavior and isolation.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006  
- **Conflicts with:** FR-022 (if interpreted as direct remote control)  
---

[FR-026]: Provide remote monitoring/eavesdropping with selectable displays; no local effect  
**Description**: “Remote monitoring… allows the remote user to ‘pick and choose’… remote keyboard will have no effect on the local user’s environment.”  
**Rationale:** Defines remote monitoring function and non-interference behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020  
- **Conflicts with:** NFR-001  
---

[FR-027]: Provide remote access for monitoring/diagnostics from base facility  
**Description**: “Remote access… required for monitoring and diagnostic purposes… must be possible from the… base facility.”  
**Rationale:** Defines diagnostic access function and location requirement.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, NFR-020  
- **Conflicts with:** NFR-018 (essential tasks on controlled resources; must be reconciled)  
---

[FR-028]: Support service observing programming environment for astronomer and observer  
**Description**: “Programming environment should be available both to the astronomer… and to the observer… for review and adjustment… may or may not be… concurrently…”  
**Rationale:** Defines required tooling/functionality for service observing workflows.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-022  
- **Conflicts with:** NFR-006 (privilege separation)  
---

[FR-029]: Scheduler supports queueing, resorting based on rules and conditions  
**Description**: “It should be possible to resort the queue… based on properties… current site conditions, and other rules…”  
**Rationale:** Defines scheduling behavior (prioritization/sorting).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-031  
- **Conflicts with:** NFR-001 (compute overhead)  
---

[FR-030]: All control software supports simulated use within virtual telescope  
**Description**: “All control software must provide support for simulated use within the virtual telescope.”  
**Rationale:** Defines a required operating mode for all control software.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006  
- **Conflicts with:** NFR-001 (if simulation impacts production)  
---

[FR-031]: Manage collection of science/environmental/engineering/reference/calibration data  
**Description**: “This includes managing the collection of science, environmental, engineering, reference, and calibration data.”  
**Rationale:** Defines core data acquisition/management functions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-032, FR-033  
- **Conflicts with:** NFR-001  
---

[FR-032]: Store detector data effectively; support preprocessing for IR; store preprocessed data  
**Description**: “Data from detectors must be stored in the most effective method… For data that requires preprocessing… only the preprocessed data is stored.”  
**Rationale:** Defines data handling behavior (storage and preprocessing).  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004  
- **Conflicts with:** FR-034 (raw data for quick look)  
---

[FR-033]: Store instrument/detector data as compressed data using a standard format  
**Description**: “Data from all instruments and detectors is stored as compressed data, using a standard format.”  
**Rationale:** Defines storage behavior and standardization.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004  
- **Conflicts with:** NFR-001 (compression overhead)  
---

[FR-034]: Provide quick-look data quality assessment using on-system storage  
**Description**: “Quick-look data quality assessment is done using this level.” / “Quick-look data processing should be provided… synchronous… usable within exposure sequences… provide results and feedback parameters…”  
**Rationale:** Defines quick-look processing and feedback function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-031, NFR-001  
- **Conflicts with:** FR-035 (data acquisition precedence)  
---

[FR-035]: Provide near-line processing asynchronously; data acquisition takes precedence  
**Description**: “Near-line processing… asynchronously from data acquisition… data acquisition takes precedence over near-line data reduction.”  
**Rationale:** Defines processing workflow and prioritization behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-031  
- **Conflicts with:** NFR-001 (resource contention)  
---

[FR-036]: Automatically archive data during observing and maintenance to Gemini Archive subsystem  
**Description**: “Archiving of data is automatically done while in observing and maintenance level operation to the Gemini Archive subsystem.”  
**Rationale:** Defines automated archival behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-010  
- **Conflicts with:** NFR-001 (archiving overhead)  
---

[FR-037]: Transmit data to home institutes in FITS with full headers  
**Description**: “Data is transmitted between Gemini and home Institutes using a FITS format and contains all header information…”  
**Rationale:** Defines external data exchange function and format.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-011  
- **Conflicts with:** NFR-019 (internet non-essential)  
---

[FR-038]: Provide access mode allocation system for resource assignment and deadlock avoidance  
**Description**: “Protection… implemented using an Access Mode Allocation system that dynamically identifies and assigns resources… Critical resources… assigned solely through this allocation system… must ensure… cannot remain deadlocked…”  
**Rationale:** Defines resource management function and deadlock prevention behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, NFR-009  
- **Conflicts with:** FR-019 (simple access vs allocation constraints)  
---

[FR-039]: Provide procedures for common tasks (startup/shutdown/self-test/configuration)  
**Description**: “Procedures must be implemented… telescope start-up and shutdown… system self-testing… instrument start-up and shut-down… self-testing and self-diagnosis… configuration and reconfiguration.” Each startup/shutdown procedure must include acceptance test steps and define error path, rollback conditions, and logging. (Next action: Add acceptance criteria to ops procedure FRs.)  
**Rationale:** Defines required operational workflows.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-041, FR-042  
- **Conflicts with:** None identified  
---

[FR-040]: Log bugs/faults/alarms/events with timestamps; enable reconstruction of observation sequence  
**Description**: “All software bugs should be logged… Subsystems must notify the user when faults occur… capable of being electronically logged… System logging… properly timestamped and indexed… recreate the steps in a observation from the system logs.” Log pipeline must sustain 200 Hz input rate for 30 minutes without data loss; audit daily for >1% log drop events; raise alert if log retention <30 days. (Next action: Add log system capacity specs and alerting policies.)  
**Rationale:** Defines logging/notification behaviors and audit trail function.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-016, NFR-017  
- **Conflicts with:** NFR-001 (logging overhead)  
---

[FR-041]: Provide built-in test (BIT), self-test sequences, and regression tests  
**Description**: “Software… shall contain built-in test (BIT)… Every… module shall have corresponding test specifications… provide for execution of self-test sequences… Regression tests should be a part of every… package.” Each module release must supply test plan covering normal operation, fail-over, and version compatibility. Test results archived for traceability. (Next action: Add release checklist item: test spec submitted with each software module.)  
**Rationale:** Defines test execution functions and required test artifacts.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014  
- **Conflicts with:** NFR-001 (test load during operations)  
---

[FR-042]: Reconfigure environment to continue operation after subsystem failure; transfer control between user stations  
**Description**: “Should a subsystem fail… predefined procedures must exist to redefine the environment… In case of… user station… possible to transfer control… via a simple software reconfiguration procedure.”  
**Rationale:** Defines recovery and reconfiguration behaviors.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008, NFR-009  
- **Conflicts with:** FR-001 (operational level restrictions may limit reconfig)  
---

[FR-043]: Provide common command sets across subsystems and IOCs (status/version/self-test/start/stop/reset)  
**Description**: “All subsystems must respond to a common set of commands… version… self-tests… All IOC subsystems must respond to additional common commands… start, stop, initialize, reset parameters…”  
**Rationale:** Defines standardized command functionality across components.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003  
- **Conflicts with:** None identified  
---

[FR-044]: Provide reliable command communications with uniform ACK/NAK, timeouts, and handshaking  
**Description**: “Support structure… reliable, with a uniform ACK/NAK protocol… Timeouts… 500 msec… Handshaking… within 100-200 msec… For delayed replies, timeouts… supported.”  
**Rationale:** Defines required communication behaviors and protocol features.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, NFR-003  
- **Conflicts with:** NFR-001 (if network cannot meet timing)  
---

[FR-045]: Enforce engineering/maintenance mode isolation from directives while still providing status  
**Description**: “A system that is operating in Engineering/Maintenance mode must ignore directives from other systems, though status information should still be provided…”  
**Rationale:** Defines mode-dependent command handling behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-006  
- **Conflicts with:** FR-022 (remote full operations)  
---

[FR-046]: Provide on-line database for parameters; remote/distributed access; EPICS in IOC  
**Description**: “All telescope and instrument parameters are kept in an on line database… interface… via interface calls… Access times… 2-3 msec… Asynchronous writes… database must support both remote access and distributed data… internal (within the IOC)… based on EPICS.” ParameterDB schema includes: key(string), type(enum{float32,int32,bool,string}), value, allowed_range(min,max), error_response(enum{OUT_OF_RANGE,TYPE_MISMATCH}), etc. (Next action: Publish formal schema and static analysis contract for ParameterDB.)  
**Rationale:** Defines data management functions and access patterns.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005, ASR-005  
- **Conflicts with:** NFR-001 (DB load)  
---

[FR-047]: Provide version labeling and retrievable version info via control commands; boot-time version consistency check  
**Description**: “All Gemini software must be version labeled… retrievable… via control commands… At boot time… check the consistency of versions…”  
**Rationale:** Defines configuration/version management behaviors.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014  
- **Conflicts with:** None identified  
---

[FR-048]: Support table-driven constants update without recompilation; some modifiable during operation  
**Description**: “Table-driven software… Changing system constants… shall not require recompiling but will be updated as part of system startup… modifiable during operation.”  
**Rationale:** Defines configuration update behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-046  
- **Conflicts with:** NFR-006 (protecting parameters)  
---

[FR-049]: Provide safety monitoring and safe-state transitions on danger detection  
**Description**: “The Gemini system must be self-monitoring… software should be able to quickly bring… to a safe state… Subsystems must be able to detect such danger and report it…”  
**Rationale:** Defines safety functions (detection, reporting, safe-state action).  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-012, NFR-013  
- **Conflicts with:** NFR-001 (safety actions may preempt performance)  
---

[FR-050]: Provide command input range/validity checking before execution; support ahead-of-time sequence preparation and simulation  
**Description**: “Range checking and validity checking shall be supported before execution of any input command… possible ahead of time, preparing observing sequences… and simulating observations…”  
**Rationale:** Defines validation and pre-execution simulation functions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-030, NFR-009  
- **Conflicts with:** NFR-001 (validation overhead)  
---

[FR-051]: Support continuous monitoring of subsystems on request (active and idle)  
**Description**: “It must be possible to apply continuous monitoring to all subsystems on request, both when in operation and when idle…” Continuous monitoring may sample at up to 10 Hz per subsystem; at most 2 concurrent continuous monitoring sessions permitted per node. (Next action: Add rate limits and test schedule for monitoring.)  
**Rationale:** Defines monitoring function and scope.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020  
- **Conflicts with:** NFR-001  
---

[FR-052]: Provide subsystem simulator replacement mechanisms and self-check levels (monitor/exercise/diagnostic)  
**Description**: “Each subsystem… include a simulator… Simple mechanisms should exist for replacing a subsystem with its simulation… self-check levels… background task… notify OCS… module for fully exercising… executed automatically during start-up and on demand… diagnostic… on demand during maintenance…”  
**Rationale:** Defines test/maintenance functions and simulator swap behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-018, FR-041  
- **Conflicts with:** NFR-001  
---

[FR-053]: Support independent instrument startup/shutdown without affecting telescope operation  
**Description**: “These must allow startup and shutdown of instruments independently of the telescope and without affecting the telescope operation.”  
**Rationale:** Defines operational independence behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-039, FR-015  
- **Conflicts with:** NFR-012 (safety interlocks may constrain)  
---

[FR-054]: Support dynamic reconfiguration of observing environments and light path without restart  
**Description**: “Reconfiguration procedures must exist… definition… must be dynamic… feasible during operations without the need to restart everything. The same applies to the related light path.”  
**Rationale:** Defines runtime reconfiguration behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-039, FR-038  
- **Conflicts with:** NFR-012 (safety)  
---

[FR-055]: Provide voice connectivity permanently; make TV/voice/site monitoring data capable of being available  
**Description**: “TV data… and voice need to be capable of being available… It is a requirement that voice connectivity… be available on a permanent connection.”  
**Rationale:** Defines communications service functions (availability/capability).  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-019 (internet non-essential; voice may need controlled resources)  
---