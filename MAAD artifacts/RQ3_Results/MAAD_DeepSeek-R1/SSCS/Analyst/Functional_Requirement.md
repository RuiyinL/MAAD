# Functional Requirements Results:
[FR-001]: Ground Command Handling  
**Description**: The system shall receive ground commands through asynchronous serial port (address 0x88DA) every 160ms cycle, verify command length/frame header/checksum per Table 3.2-1, and set satellite operating mode if valid. Only one command allowed per 160ms.  
**Rationale**: Describes input processing and verification behavior with explicit timing constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on**: ASR-001 (160ms cycle)  
---  
[FR-002]: Gyroscope Data Acquisition  
**Description**: The system shall send a two-byte command (0xEB91) via serial port (极001A) each 160ms cycle, wait >5ms, then receive gyroscope measurement data through the same port.  
**Rationale**: Specifies sensor interaction protocol with timing constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on**: ASR-001 (cycle timing), NFR-002 (inter-byte timing)  
---  
[FR-003]: Sensor Data Collection  
**Description**: The system shall collect power-on status and measurements every 160ms into SensorData struct with explicit fields/types:  
• sun_angle: uint16 (0x000-0xFFF)  
• gyro_pulse_count: uint16  
• thruster_status: bool[12]  
• SP_signal: uint8 bitmask  
Ranges/encodings as defined in ASR-004 schemas.  
**Rationale**: Defines multi-source data acquisition with codified contracts.  
**极ependencies** / **Conflicts**:  
- **Depends on**: ASR-002 (AD/serial addressing), ASR-004 (data schemas)  
---  
[FR-004]: Attitude Determination  
**Description**: The system shall calculate satellite three-axis angular velo极ity and estimate attitude angle every 160ms using gyroscope measurements, sun sensor angle, and visibility flag.  
**Rationale**: Describes core transformation of sensor inputs to navigation state.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-002, FR-003  
---  
[FR-005]: Mode Management  
**Description**: The system shall maintain four operational modes (RDSM, PASM, RASM, CSM), set target angular velo极ities (e.g., zero for RDSM), accumulate mode duration, and evaluate mode transitions per state transition table. Acceptance: Transition to PASM when gyro velo极ity < 0.02°/s for 3 consecutive cycles AND sun not visible for 3 cycles.  
**Rationale**: Defines state-dependent control with quantified transition thresholds.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-001 (mode setting), ASR-003 (state transitions)  
---  
[FR-006]: Fault Management  
**Description**: The system shall implement fault responses per state table: power-off gyroscope after 5 consecutive errors, thruster shutdown on jetting <1s/5s, backup sun sensor switch after 2 search failures. Each fault action must generate log entry:  
{timestamp:uint32 ms, fault_code:enum, action_taken:enum, prev_state:enum, next_state:enum}  
retained for ≥128 entries in onboard RAM.  
**Rationale**: Specifies error detection/recovery with explicit logging.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-003 (monitoring), ASR-003 (state logic)  
---  
[FR-007]: Thruster Control  
**Description**: The system shall output thruster switch signals at 128ms within each 160ms cycle to control roll/pitch/yaw torque using designated thruster pairs (e.g., 4A/4B for pitch).  
**Rationale**: Defines actuator output timing and mapping.  
**Dependencies** / **Conflicts**:  
- **Depends on**: ASR-001 (thruster timing slot)  
---  
[FR-008]: Telemetry Transmission  
**Description**: The system shall package and send operational status (mode word, angle, velo极ity) every 160ms via serial port (0x88DB) with <5µs inter-byte intervals.  
**Rationale**: Describes output generation and communication behavior.  
**Dependencies** / **Conflicts**:  
- **Depends on**: NFR-004 (telemetry timing)  
---