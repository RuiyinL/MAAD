# Architecturally Significant Requirements Results

[ASR-001]: Time-triggered cyclic executive with 32ms tick and 160ms superframe  
**Description**: The control computer runs in the mode of main program plus interruption… the interruption is 32 milliseconds regular cycle interruption… Only one interrupt is processed… the 32ms timer interrupt… multiple behaviors mandated every 160ms… At the 128th ms of each 160ms control cycle, the switch data of 12 10N thrusters will be sequentially output.  
**Architectural Impact:**  
Forces a time-triggered architecture with a deterministic schedule (slots) and minimal concurrency (single ISR). Impacts module decomposition into periodic tasks aligned to ticks, WCET budgeting, and timing-safe I/O drivers.  
**Quality Attributes Affected:** Performance (real-time), Reliability, Safety  
**Architectural Constraints:**  
- Single periodic interrupt at 32ms  
- Deterministic 160ms control cycle with a reserved thruster output slot at 128ms  
- Main-loop + ISR execution model (no multi-interrupt preemption)  
**Rationale:** Hard real-time, schedule-driven behavior is cross-cutting and dictates the system’s runtime structure and integration strategy.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-010, NFR-002
- **Conflicts with:** Not specified  
---

[ASR-002]: Constrained embedded platform (80C32E @ 11.0592MHz, 32KB PROM, 8KB SRAM)  
**Description**: The control computer takes the microcontroller 80C32E as the core… main frequency 11.0592MHZ… 32KB of PROM and 8KB of SRAM.  
**Architectural Impact:**  
Drives low-footprint design: static memory allocation, compact data structures, minimal dynamic features, optimized ISR/serial routines, and careful code partitioning between PROM/SRAM.  
**Quality Attributes Affected:** Performance, Maintainability, Portability  
**Architectural Constraints:**  
- Must run on 80C32/80C32E-class MCU  
- Strict memory ceilings (32KB ROM, 8KB RAM)  
**Rationale:** Platform constraints heavily influence technology choices, coding patterns, scheduling, and feasibility of abstractions/testing harnesses.  
**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** Not specified  
---

[ASR-003]: Serial/ADC hardware interface contracts with strict timing and addressing  
**Description**: Serial port addresses designated (e.g., 0x88DA for command RX, 0x88DB for telemetry TX, 0x881A for gyro)… interval between each byte sent is less than 5us… time interval from sending fetch instruction to reading gyro data > 5ms… 12-bit AD (0x000~0xFFF, offset binary)… power status via AD. All gyro command and data transactions shall utilize serial port address 0x881A exclusively. Owner: Not specified; Next action: Update all requirements (FR-007, FR-019, NFR-011, ASR-003) to use only 0x881A or define clear disambiguation.  
**Architectural Impact:**  
Requires explicit interface layers (UART/ADC drivers), versioned message/frame schemas (length/header/checksum), and schedule-aware I/O sequencing (fetch → delay → read). Also implies architectural need to isolate hardware contracts from control logic for testability and integration.  
**Quality Attributes Affected:** Interoperability, Performance (timing), Reliability, Testability  
**Architectural Constraints:**  
- Fixed register/port addresses and command codes  
- Inter-byte gap < 5µs for specific transmissions  
- Gyro read must occur > 5ms after fetch  
- AD data width/encoding fixed to 12-bit offset binary  
- Gyro port address fixed to 0x881A exclusively  
**Rationale:** Cross-cutting I/O constraints and timing sensitivities shape component boundaries and the end-to-end control pipeline.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006, NFR-008, NFR-011, NFR-005
- **Conflicts with:** Not specified  
---

[ASR-004]: Mode-based control architecture with defined phases and mode register state  
**Description**: The whole search process is divided into four stages: rate damping RDSM, pitching search PASM, rolling search RASM and sun cruise CSM… needs to use a mode register to store current operating mode word, current mode duration, target angle, target angular velocity… mode switching management scheduled every 160ms.  
**Architectural Impact:**  
Imposes a state-machine (mode manager) as a core architectural element with persistent mode state and time-in-mode accounting; influences data model, scheduling, and separation of estimation vs control vs supervision.  
**Quality Attributes Affected:** Reliability, Maintainability, Safety  
**Architectural Constraints:**  
- Must implement four explicit modes with transition logic  
- Must persist mode word, duration, targets in a mode register/state store  
- Must evaluate mode transitions every 160ms  
**Rationale:** The mode framework is central, cross-cutting, and drives the organization of control logic and data flows.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-021, NFR-004
- **Conflicts with:** Not specified  
---

[ASR-005]: Deterministic fault-management state machines for gyro comms and thruster over-firing  
**Description**: Gyro comm error handling: count consecutive error cycles; after 5 cycles power-off gyro; wait 5 cycles; power-on; wait 5 cycles; resume; if errors persist another 5 cycles power-off and await ground… Thruster fault: if firing intervals <1s for continuous 5s, switch off thruster… checks every 160ms.  
**Architectural Impact:**  
Requires system-wide fault manager integrated with the 160ms scheduler, persistent counters/timers, and component power-control interfaces. Influences telemetry/fault reporting and safe-state behaviors.  
**Quality Attributes Affected:** Reliability, Safety, Availability  
**Architectural Constraints:**  
- Fault checks executed on fixed cadence (160ms)  
- Deterministic thresholds (5 consecutive cycles; 5-cycle waits; <1s for 5s)  
- Must be able to power-cycle gyro and disable thrusters via control outputs  
**Rationale:** Safety/reliability behaviors are high-risk and cross-cutting, affecting control flow and hardware control architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017, FR-018, NFR-004
- **Conflicts with:** Not specified  
---

[ASR-006]: Sun sensor switching mechanism with tight pulse timing  
**Description**: The sun sensor switching instruction is a positive pulse of 190ms ±1ms… writing the enable signal to the controller… switch to backup sun sensor after unsuccessful searches. Owner: Not specified; Next action: Clarify and synchronize all documentation and requirements to use one pulse timing.  
**Architectural Impact:**  
Requires precise timing generation (likely hardware-timer-assisted or schedule slot) and a dedicated actuator-control interface for sensor switching; affects mode/fault handling integration and timing verification.  
**Quality Attributes Affected:** Performance (timing), Reliability  
**Architectural Constraints:**  
- Must generate a positive switching pulse of 190ms ±1ms via control register write  
- Must support switching between primary and backup sensors based on search outcome logic  
**Rationale:** Tight pulse timing combined with safety-critical sensor redundancy impacts scheduling, low-level driver design, and verification strategy.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-020, NFR-009, NFR-004
- **Conflicts with:** Not specified  
---

[ASR-007]: Telemetry packaging and high-rate serial transmission constraints  
**Description**: Telemetry is collected every 160ms… packaged into a predefined format… sent via asynchronous serial port address 0x88DB… each byte sent with interval <5us.  
**Architectural Impact:**  
Requires a defined telemetry data model and framing, plus an efficient TX path capable of meeting tight inter-byte timing; affects buffering strategy, CPU budget, and coupling with schedule slots.  
**Quality Attributes Affected:** Performance (timing), Interoperability, Observability  
**Architectural Constraints:**  
- Periodic telemetry at 160ms cadence  
- Fixed TX port address 0x88DB  
- Inter-byte gap < 5µs  
**Rationale:** Cross-cutting observability requirement with strict timing constraints drives interface contracts and runtime scheduling.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-023, NFR-006, NFR-004, NFR-011
- **Conflicts with:** Not specified  
---