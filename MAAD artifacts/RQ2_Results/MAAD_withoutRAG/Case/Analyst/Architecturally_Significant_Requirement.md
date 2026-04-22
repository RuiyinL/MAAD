# Architecturally Significant Requirements Results:

[ASR-001]: ICU periodic acquisition + alerting pipeline with persistence  
**Description**: The program reads these factors on a periodic basis (specified for each patient) and stores the factors in a database... If a factor falls outside a patient's safe range, or if an analog device fails, the nurses' station is notified.  
**Architectural Impact:**  
Requires a time-driven data acquisition subsystem, per-patient scheduling/configuration, reliable persistence, rule evaluation against safe ranges, and an alert/notification mechanism integrated with nurses’ station workflow. Drives separation of concerns (acquisition, storage, rules, notifications) and fault handling paths.  
**Quality Attributes Affected:** Performance (timeliness), Reliability, Safety, Maintainability  
**Architectural Constraints:**  
- Must support per-patient configurable sampling intervals.  
- Must integrate with a database for time-series storage.  
- Must provide a notification channel to the nurses’ station for alarms and device-failure events.  
**Rationale:** Cross-cutting, safety-critical behavior combining timing, persistence, and alerting; strongly shapes componentization and runtime scheduling.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003, FR-004, FR-005, NFR-001, NFR-003
- **Conflicts with:** NFR-004 (if security/privacy constraints hinder alerting/persistence design)
---

[ASR-002]: Biometric access control with video stream capture and feature database  
**Description**: A secure door is to be controlled by a computer that recognises facial features... face ... captured in a video stream ... compared with entries in a database of the features of people who have been cleared for entry.  
**Architectural Impact:**  
Forces inclusion of a video ingestion pipeline, feature extraction/matching component, biometric template storage, and an authorization decision point controlling a physical door actuator. Often drives specialized libraries/hardware acceleration and strong data protection.  
**Quality Attributes Affected:** Security, Privacy, Performance (decision latency), Reliability  
**Architectural Constraints:**  
- Must support continuous/sequential capture from a video stream.  
- Must store and query facial feature templates in a database.  
- Must interface with door control hardware for allow/deny decisions.  
**Rationale:** High-risk security functionality with specialized processing and sensitive data; major implications for tech choices and data protection.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008, NFR-005, NFR-006
- **Conflicts with:** None specified
---

[ASR-003]: Turnstile payment gating correctness (no unpaid entry; all paid entry allowed)  
**Description**: No visitor should be able to enter ... without ... two coins. ... any visitor who has paid the two coins should be allowed to enter.  
**Architectural Impact:**  
Requires a robust state machine for coin counting and barrier control, handling edge cases (double-entry, coin jams, power loss) and ensuring correctness of admission decisions. Likely influences transactional design around coin input events and actuator commands.  
**Quality Attributes Affected:** Reliability, Safety (physical control), Integrity  
**Architectural Constraints:**  
- Must integrate with coin acceptor and rotating barrier via computer ports.  
- Must enforce a strict admission state model tied to two-coin payment.  
**Rationale:** Business-critical invariant and hardware-control coupling; correctness constraints shape core control logic architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, FR-010, FR-011
- **Conflicts with:** None specified
---

[ASR-004]: Heating system closed-loop control with multi-mode behavior (manual, occupancy economy, predictive preheat)  
**Description**: The computer must regulate ... maintain room temperatures ... For economy ... unoccupied room ... 5 degrees below ... anticipate room use ... starting ... 30 minutes before occupancy ... control panel manual on/off ... display state and malfunction. Add: 'Manual control (FR-014) takes precedence over predictive preheat (FR-018), which takes precedence over economy setback (FR-016). If multiple commands are received, system behavior is defined by State Transition Table X (attached).' Acceptance: Pass functional test suite with all mode/transition combinations. [Next action: Draft and approve explicit mode arbitration statechart and test all conflict scenarios.]  
**Architectural Impact:**  
Drives a control architecture combining sensor ingestion, control algorithms, occupancy prediction/anticipation, manual override precedence, actuator control (valves/furnace), and fault monitoring UI. Requires explicit mode/precedence rules to avoid conflicts between manual commands and automatic regulation.  
**Quality Attributes Affected:** Performance (control responsiveness), Reliability, Safety, Maintainability, Efficiency  
**Architectural Constraints:**  
- Must support per-room sensors/knobs/occupancy and per-room actuation.  
- Must implement economy setback and predictive preheating timing.  
- Must provide manual control override and state/malfunction display.  
**Rationale:** Multi-mode cyber-physical control with timing and safety implications; strongly impacts decomposition and state machine design.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013, FR-014, FR-015, FR-016, FR-018, NFR-001, NFR-007
- **Conflicts with:** FR-012 vs FR-014/FR-016 precedence not specified
---

[ASR-005]: Roadworks traffic light controller with deterministic phased timing  
**Description**: The regime for the lights repeats a fixed cycle of four phases ... 50 seconds ... 120 seconds ... repeated. The computer controls the lights by emitting Pulses and Guises.  
**Architectural Impact:**  
Requires deterministic timing control loop, precise phase scheduling, and hardware pulse IO. Influences choice of real-time scheduling, timer mechanisms, and test/simulation of timing correctness.  
**Quality Attributes Affected:** Real-time Performance, Reliability, Safety  
**Architectural Constraints:**  
- Must emit specific control signals (pulses/guises) to light units.  
- Must implement exact phase durations (50s/120s) and sequencing.  
**Rationale:** Hard timing constraints and safety-critical physical signaling; architecture must ensure predictable behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, FR-023, NFR-001
- **Conflicts with:** FR-025, FR-026 (configurable/override regimes)
---

[ASR-006]: Direct hardware I/O via ports/pulse lines/status lines/register access  
**Description**: Multiple systems specify direct connections: turnstile “two ports”; traffic lights controlled by “Pulses and Guises”; sluice “four pulse lines ... two status lines”; speedometer “detect pulses” and shared registers; lab A/D “register values ... directly accessible”.  
**Architectural Impact:**  
Forces a hardware abstraction layer (HAL/HardwareIO) and simulation/mocking strategy, plus clear boundaries between device drivers and domain logic. Impacts deployment topology (edge controller near devices) and testability.  
**Quality Attributes Affected:** Portability, Testability, Reliability, Maintainability  
**Architectural Constraints:**  
- Must support low-level read/write of ports, pulses, and registers.  
- Must encapsulate device-specific IO behind stable interfaces to avoid scattering hardware coupling.  
**Rationale:** Cross-cutting constraint spanning many subsystems; dictates foundational platform structure.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, FR-013, FR-022, FR-035, FR-036, FR-047, FR-050
- **Conflicts with:** None specified
---

[ASR-007]: Extensibility via add-on modules sharing control events (traffic light display module)  
**Description**: Add the Stop/Go display “as a separate module” and it “will share the RPulse and GPulse events of the existing system” to avoid disturbing the existing design.  
**Architectural Impact:**  
Requires an internal event-sharing mechanism (event bus/publish-subscribe or stable event interface) and modular boundaries so extensions can be added without modifying deterministic control logic.  
**Quality Attributes Affected:** Modifiability, Maintainability, Reliability  
**Architectural Constraints:**  
- Must expose RPulse/GPulse as shared/published events with a defined schema/contract.  
- Must allow a separate module to subscribe without altering existing controller internals.  
**Rationale:** Explicit constraint to extend without disturbing existing design; implies modular/event-driven architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-024, FR-022
- **Conflicts with:** None specified
---

[ASR-008]: Multi-mode operator override / command precedence for controllers  
**Description**: Traffic overseer can extend/curtail phases (Hold/Change); sluice can be operated “in response to the commands of an operator”; package router must obey operator commands; heating has manual on/off plus automatic regulation. Each system with override/manual/automatic must implement a state machine: manual input always defers or preempts automatic, timeouts revert to default mode; acceptance: pass test set validating transitions and unique final states. [Next action: Document and review detailed arbitration logic covering all inputs/mode transitions.]  
**Architectural Impact:**  
Forces explicit state machines, command arbitration/precedence rules, and safe transitions/timeouts across manual vs automatic modes. Impacts shared platform patterns for command handling and safety interlocks.  
**Quality Attributes Affected:** Safety, Reliability, Usability  
**Architectural Constraints:**  
- Must define mode precedence and transitions (manual override vs default regimes).  
- Must ensure deterministic behavior under concurrent/rapid operator inputs.  
**Rationale:** High-risk ambiguity and cross-cutting control-policy requirement; without precedence models architecture is unstable and unsafe.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-026, FR-037, FR-044, FR-014
- **Conflicts with:** FR-023, FR-034, FR-012 (default schedules/regulation vs overrides)
---

[ASR-009]: Shared-register / direct-state access constraints in embedded displays and sensors  
**Description**: Speedometer counters’ registers are shared by computer and visible display; lab A/D devices expose register values directly; shuttle computer has direct access to sensor state and sets motor/brake states directly. All register accesses must be wrapped in critical sections. Tests: Simulate concurrent read/write in mock environment, verify consistency and correct display value. [Next action: Design and document register access control patterns; add atomicity tests.]  
**Architectural Impact:**  
Requires careful concurrency/control of shared memory/register access, atomicity considerations, and hardware-safe update patterns. Typically drives low-level driver layer plus deterministic update scheduling.  
**Quality Attributes Affected:** Reliability, Performance, Safety  
**Architectural Constraints:**  
- Must coordinate access to shared registers between computation and display hardware.  
- Must support direct sensor reads and actuator writes in control loops.  
**Rationale:** Low-level coupling and potential race conditions significantly impact architecture and verification approach.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-027, FR-028, FR-047, FR-050
- **Conflicts with:** None specified
---

[ASR-010]: Package router physical constraints and safe switch actuation rules  
**Description**: Switches can be flipped “when no package is present between the incoming and outgoing pipes”; “A package cannot overtake another either in a pipe or in a switch”; packages slide at unpredictable speeds and may get too close together to allow a switch to be set correctly; misrouted package may be routed to any bin with message displayed. If time between packages at switch <500ms, divert package to misroute bin and log as status=‘close-follow’. Acceptance: Pass on hardware-in-loop simulation with 0 errors/unsafe actuations. [Next action: Add explicit timing/actuation spacing numbers and fallback rules.]  
**Architectural Impact:**  
Requires sensor-driven tracking of package positions, switch interlocking logic, conservative decision-making under uncertainty, and exception handling/reporting. Likely drives event-driven control with state estimation and safety constraints.  
**Quality Attributes Affected:** Safety, Reliability, Performance  
**Architectural Constraints:**  
- Must prevent switch changes when a package is in the switch segment.  
- Must handle unpredictable speeds and close-following packages (may require buffering policies and fallback routing).  
- Must support misroute detection and operator messaging.  
**Rationale:** Complex physical-domain constraints and uncertainty drive core control architecture and risk.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-043, FR-045, NFR-001
- **Conflicts with:** None specified
---