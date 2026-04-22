# Architecturally Significant Requirements Results:
[ASR-001]: Periodic Real-Time Data Acquisition
**Description**: The program reads patient factors on a periodic basis (specified for each patient). Each periodic read must complete (including store) within the configured interval ±50ms.

**Architectural Impact:**  
- Requires a real-time scheduling mechanism (e.g., Time-Triggered Architecture or RTOS) to guarantee periodic execution.
- Influences task decomposition to separate data acquisition from storage and alerting.
- Impacts CPU load management to ensure no sample is missed.

**Quality Attributes Affected:**  
Performance, Reliability, Timing

**Architectural Constraints:**  
- Must support multiple concurrent periodic tasks with different frequencies.
- Requires deterministic timing behavior.
- Each periodic read must complete (including store) within the configured interval ±50ms.

**Rationale:**  
Periodic reading of medical data is safety-critical; missing a deadline could result in failure to detect a vital sign anomaly. This dictates the concurrency model.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[ASR-002]: Direct Hardware Interface Control
**Description**: The connection to the computer consists of four pulse lines for motor control and two status lines for the gate sensors (Sluice/Traffic/Lathe). All pulse signals must be generated with a timing deviation less than ±5ms; support for XYZ microcontroller series. Metric: 'pulse_deliver_jitter_ms' measured by scope/logger at I/O pin, ≤5ms jitter over 48 hours of normal and stress load. [Next Action: Add observability/test/verification logic to support required timing.]

**Architectural Impact:**  
- Requires a Hardware Abstraction Layer (HAL) or specific device drivers to manage pulse generation and status reading.
- Constrains the system to run on hardware capable of precise I/O timing (e.g., microcontrollers or real-time kernels).
- Prevents use of standard high-level OS I/O without real-time patches.

**Quality Attributes Affected:**  
Portability, Performance, Reliability

**Architectural Constraints:**  
- Software must map directly to specific physical I/O ports or interrupt lines.
- Timing of pulses must be precise (e.g., motor control).
- All pulse signals must be generated with a timing deviation less than ±5ms; support for XYZ microcontroller series.
- Metric: 'pulse_deliver_jitter_ms' measured by scope/logger at I/O pin, ≤5ms jitter over 48 hours of normal and stress load.

**Rationale:**  
Direct manipulation of hardware lines for safety-critical actuators (gates, lights, lathes) imposes a strict boundary between software and physical world, requiring specialized architectural layers.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-008
- **Conflicts with:** None
---
[ASR-003]: External File/Card-Based Configuration
**Description**: The regime is encoded on a magnetic card (Traffic) or dimensions held on a floppy disk file (Lathe) to control system behavior.

**Architectural Impact:**  
- Requires a file system or card-reading subsystem.
- Necessitates a configuration parsing module to interpret external data (ASCII text or binary).
- Decouples behavior logic from code, requiring a flexible command pattern or strategy pattern in software design.

**Quality Attributes Affected:**  
Modifiability, Maintainability

**Architectural Constraints:**  
- System must support dynamic loading of behavior parameters at startup or runtime.
- Input validation architecture required to prevent invalid configurations from causing hazards.

**Rationale:**  
Allowing external media to dictate system behavior (lathe shape, traffic regime) shifts the architecture from hardcoded logic to data-driven control, impacting modularity and safety validation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-010
- **Conflicts with:** None
---
[ASR-004]: Shared Memory Register Access
**Description**: The underlying registers of the counters are shared by the computer and the visible display (Car Speedometer).

**Architectural Impact:**  
- Requires careful synchronization or atomic access mechanisms to prevent race conditions between the computer updating the value and the display reading it.
- May necessitate a specific memory-mapped I/O architecture.

**Quality Attributes Affected:**  
Reliability, Data Integrity

**Architectural Constraints:**  
- Hardware/Software interface must ensure coherent reads/writes to shared registers.

**Rationale:**  
Shared resources between compute and display elements introduce concurrency risks that must be mitigated at the architectural level to prevent display corruption.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-005]: Safety-Critical Fault Detection
**Description**: If an analog device fails, the nurses' station is notified; Control panel indicates system state and any malfunction.

**Architectural Impact:**  
- Requires a dedicated monitoring subsystem or heartbeat mechanism to detect component failure.
- Influences the error handling architecture to prioritize fault reporting over normal operation.
- May require redundancy or watchdog timers.

**Quality Attributes Affected:**  
Safety, Reliability, Availability

**Architectural Constraints:**  
- System must remain capable of reporting faults even if primary monitoring functions degrade.
- Fault detection must be independent enough to detect primary system failure.

**Rationale:**  
In medical and industrial contexts, the ability to detect and report failure is as important as the primary function, dictating a fail-safe architectural design.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-001
- **Conflicts with:** None
---