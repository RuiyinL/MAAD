# Architecturally Significant Requirements Results

[ASR-001]: Fixed embedded platform (80C32E, 32KB PROM, 8KB SRAM, 11.0592 MHz)  
**Description**: The control computer takes the microcontroller 80C32E as the core, the main frequency is 11.0592MHZ, including 32KB of PROM and 8KB of SRAM.  
**Architectural Impact:**  
Constrains language/toolchain, memory model, scheduling approach, buffering, telemetry packaging size, and algorithm complexity; drives a bare-metal or minimal-RTOS architecture and careful ISR/main-loop partitioning.  
**Quality Attributes Affected:** Performance, Maintainability, Portability, Reliability  
**Architectural Constraints:** Must run on 80C32E-class MCU with stated memory/clock limits.  
**Rationale:** Strong technology/resource constraint with pervasive impact on decomposition, timing, and implementation feasibility.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-009
- **Conflicts with:** None specified
---

[ASR-002]: Deterministic cyclic executive with single 32 ms timer interrupt and 160 ms control cycle  
**Description**: The control computer runs in the mode of main program plus interruption; the main program is an infinite loop; the interruption is 32 milliseconds regular cycle interruption; only one interrupt is processed (32ms timer interrupt); and multiple functions are mandated to occur in a 160ms cycle, including thruster output at 128ms.  
**Architectural Impact:**  
Forces a time-triggered architecture (cyclic executive) with fixed-rate tasks, deterministic scheduling, and careful time budgeting; influences module boundaries (ISR vs main loop), data handoff, and timing verification strategy.  
**Quality Attributes Affected:** Real-time Performance, Determinism, Reliability  
**Architectural Constraints:**  
- Single periodic interrupt at 32 ms  
- Control cycle of 160 ms (5 ticks)  
- Thruster command output at 128 ms within the cycle  
**Rationale:** Cross-cutting timing model that dictates the overall control software structure and integration of sensing/estimation/control/telemetry.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003, NFR-004
- **Conflicts with:** None specified
---

[ASR-003]: Fixed serial/AD hardware interfaces and addresses for command, gyro, and telemetry  
**Description**: The system uses asynchronous serial ports with specified addresses (e.g., remote command receive 0x88DA; gyro send/receive 0x881A; telemetry send 0x88DB; other text also cites 0x881) and uses AD conversion for sun sensor angle (12-bit offset binary) and power status signals. Added governance requirement: a canonical mapping table of all hardware addresses and signal names shall be created and referenced as a controlled, versioned artifact. All serial, AD, and latch addresses (0x88DA, 0x881A, 0x88DB, etc.) and associated signal names must appear in InterfaceAddressTable v1.0, stored in requirements repo, and be referenced here. InterfaceAddressTable shall disambiguate address usage (e.g., 'Gyro cmd': 0x881A, 'Gyro data': 0x881A, ...). (Next action: Owner to draft InterfaceAddressTable and insert stable reference.)  
**Architectural Impact:**  
Requires hardware abstraction layers/drivers for multiple serial endpoints and AD channels; enforces strict interface contracts and mapping tables; impacts test strategy (hardware-in-the-loop, simulators) and error handling paths.  
**Quality Attributes Affected:** Interoperability, Reliability, Maintainability, Testability  
**Architectural Constraints:**  
- Must communicate via specified serial port addresses  
- Must use AD conversion for specified signals with defined encoding  
**Rationale:** Hard interface constraints and mixed I/O modalities (serial + AD + latch) shape the system’s component design and integration risk.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-006, FR-022, NFR-005, NFR-006, NFR-007
- **Conflicts with:** None specified
---

[ASR-004]: Multi-stage mode-based control architecture (RDSM/PASM/RASM/CSM) with redundancy and fault management  
**Description**: The whole search process is divided into four stages: rate damping (RDSM), pitching search (PASM), rolling search (RASM) and sun cruise (CSM); includes switching to backup sun sensor after repeated failures; includes fault handling for frequent thruster firing and gyro communication errors with power-cycle/retry and ground intervention. Added model requirement: a full state/mode transition table or diagram shall be included or referenced, covering (state × event × inputs → next state, outputs, timers) for nominal modes (RDSM/PASM/RASM/CSM) and transitions for backup sensor switching and fault conditions. The model/table shall use columns: [Current State], [Trigger/Event], [Inputs/Conditions], [Actions/Outputs], [Next State], [Timer/Timeouts]. See StateTransitionTable v2.1 (Table 4.8 in Doc v2.1) for full transitions for RDSM/PASM/RASM/CSM/backup/faults. (Next action: Owner to produce/ref and link transition table/diagram.)  
**Architectural Impact:**  
Drives a state-machine/supervisory-control architecture with explicit mode state, timers, transition guards, and fault sub-states; requires persistent mode register/state, event detection, and safe actuator/sensor power control pathways.  
**Quality Attributes Affected:** Reliability, Safety, Maintainability, Testability  
**Architectural Constraints:**  
- Must implement the four named modes and their transition logic  
- Must implement backup sun sensor switching logic after defined failure pattern  
- Must implement thruster frequent-jetting fault shutdown and gyro comms power-cycle policy  
**Rationale:** High-risk, mission-critical control logic that spans sensing, estimation, actuation, and fault recovery; strongly shapes module decomposition and verification approach.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-018, FR-019, FR-005
- **Conflicts with:** None specified
---