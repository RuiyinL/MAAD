# Architecturally Significant Requirements Results:

[ASR-001]: Hardware Platform Constraint
**Description**: The control computer takes the microcontroller 80C32E as the core, the main frequency is 11.0592MHZ, including 32KB of PROM and 8KB of SRAM.

**Architectural Impact:**  
- **Technology Selection:** Mandates the use of 80C32E MCU and associated toolchain (C99/Assembly).
- **Resource Constraints:** Limits software complexity, stack size, and data structures to fit within 8KB SRAM and 32KB PROM.
- **Performance:** CPU frequency limits instruction throughput, influencing algorithm choice (e.g., no floating point heavy math).

**Quality Attributes Affected:**  
Performance, Portability, Resource Efficiency.

**Architectural Constraints:**  
- Must use 80C32E architecture.
- No dynamic memory allocation (heap) due to memory constraints and safety criticality.
- Code must be statically linked and fit within PROM.

**Rationale:**  
This requirement dictates the fundamental execution environment. It prevents the use of modern OS features, RTOS, or dynamic languages, forcing a bare-metal design. It is high risk due to tight memory limits.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008
- **Conflicts with:** None
---

[ASR-002]: Single Interrupt Architecture
**Description**: Only one interrupt is processed in the sun search control system, that is, the 32ms timer interrupt. Initialization starts the timer to generate a continuous 32ms timer interrupt signal by writing a '1' to the D[0] bit of the timing control register GTCR0 (address 0x8083).

**Architectural Impact:**  
- **Concurrency Model:** Eliminates complex ISR nesting or prioritization schemes.
- **Scheduling:** Forces a time-triggered design where all periodic tasks are derived from this single tick.
- **Component Decomposition:** Requires a centralized scheduler or cyclic executive in the main loop/ISR boundary.

**Quality Attributes Affected:**  
Determinism, Reliability, Maintainability.

**Architectural Constraints:**  
- No other hardware interrupts allowed (e.g., serial RX must be polled or handled within the 32ms tick).
- ISR must be lightweight to avoid missing the next tick.
- Register GTCR0 at 0x8083 must be memory-mapped and accessible.

**Rationale:**  
This is a strong architectural constraint that simplifies verification and timing analysis but reduces flexibility. It is critical for meeting the hard real-time deadlines (128ms thruster output) without an RTOS.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, FR-007
- **Conflicts with:** None
---

[ASR-003]: Time-Triggered Cyclic Executive
**Description**: The system functions (command reception, data acquisition, mode management, telemetry) are mandated to occur in a 160ms cycle, with specific sub-timing (e.g., thruster output at 128ms).

**Architectural Impact:**  
- **Design Pattern:** Requires a Cyclic Executive pattern (Superloop + Timer ISR) rather than event-driven or multi-threaded architecture.
- **Task Scheduling:** Tasks must be partitioned into 32ms slots to fit the 160ms hyper-cycle (5 ticks).
- **Data Communication:** Data sharing between ISR and Main Loop must be atomic or protected (e.g., critical sections) since preemption is limited to the 32ms boundary.

**Quality Attributes Affected:**  
Performance, Timing, Reliability.

**Architectural Constraints:**  
- Must implement a 160ms cycle counter driven by 32ms interrupts.
- Thruster output logic must be scheduled precisely at tick 4 (128ms).
- All periodic tasks must complete within their allocated time slots to avoid cycle overrun.

**Rationale:**  
This requirement drives the entire software control structure. It ensures deterministic behavior required for satellite attitude control. Deviation risks mission failure (attitude loss).

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003, ASR-002
- **Conflicts with:** None
---

[ASR-004]: Safety and Fault Tolerance Strategy
**Description**: The system must manage faults (Gyro communication, Thruster frequent jetting) and redundancy (Backup Sun Sensor) through explicit state transitions and power cycling protocols.

**Architectural Impact:**  
- **State Machine:** Requires a formal Mode/State Machine (RDSM, PASM, RASM, CSM, FAULT) to manage transitions.
- **Health Monitoring:** Requires a dedicated subsystem or module for continuous health checking (every 160ms).
- **Recovery Logic:** Architecture must support power cycling of peripherals (Gyro/Sensor) via software control registers.

**Quality Attributes Affected:**  
Safety, Reliability, Availability.

**Architectural Constraints:**  
- Fault detection logic must run every 160ms.
- System must support "Safe Mode" (Rate Damping) as a fallback state.
- Hardware abstraction layer must expose power control for individual components (Gyro, Sensor, Thruster).

**Rationale:**  
Safety-critical nature of satellite control requires explicit handling of component failures. This influences module decomposition (separating Control Logic from Health Management) and data flow (fault flags influencing control outputs).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-009, FR-011
- **Conflicts with:** None
---

[ASR-005]: Interface Address Governance
**Description**: The system uses specific memory-mapped addresses for serial ports (ICD::Port_Gyro_Command, ICD::Port_Ground_Command, ICD::Port_Telemetry), control registers (GTCR0 0x8083), and AD conversion. All hardware interface addresses (serial, registers, AD) must be consolidated into a single ICD (icd.md); all requirements/implementations must reference this ICD by symbol, not literal address. All future references: ICD::Port_Gyro_Command, NOT literal 0x881A or 0x881. Owner: Team-Arch; Next action: produce and baseline ICD, update all requirements to reference ICD symbols only.

**Architectural Impact:**  
- **Hardware Abstraction:** Requires a Hardware Abstraction Layer (HAL) or InterfaceContract to centralize these addresses.
- **Integration:** Any change in hardware revision requires updating this canonical table.
- **Testing:** Test harnesses must mock these specific addresses or use hardware-in-the-loop to verify register access.

**Quality Attributes Affected:**  
Maintainability, Interoperability, Reliability.

**Architectural Constraints:**  
- All I/O access must go through defined address constants/tables (ICD symbols).
- Direct memory access to hardware registers is restricted to the HAL.
- Address conflicts (e.g., 0x881 vs 0x881A in documentation) must be resolved in the canonical interface definition.

**Rationale:**  
Hardcoded addresses scattered throughout logic create high maintenance risk and integration errors. Centralizing this governance is architecturally significant to ensure correct hardware interaction and resolve documented contradictions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-010
- **Conflicts with:** None
---