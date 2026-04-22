# Functional Requirements Results:

[FR-001]: Sun Acquisition and Attitude Control
**Description**: The main function of the sun search control system is to perform sun acquisition by collecting measurement data from gyroscopes and sun sensors to determine the current attitude of the satellite, and then control the satellite to rotate around the pitch or roll axis so that the sun sensor can detect the sun and maintain the spacecraft's sun-pointing attitude.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
This describes the primary input-output transformation of the system (Sensor Data -> Attitude Determination -> Actuator Control).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, FR-005, FR-006
- **Conflicts with:** None
---

[FR-002]: Ground Command Reception and Verification
**Description**: The sun search control system shall receive ground commands through a serial port (address 0x88DA), perform command verification (data length, frame header, checksum), and set the satellite's operating mode word. Command accepted if [frame header==0xA5][length==8][checksum==CRC-8-CCITT]. Only commands that successfully pass verification will be executed. If command verification fails, increment CMD_REJECT_COUNTER and send telemetry with status code (0=OK, 1=Length, 2=Header, 3=Checksum).

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the specific behavior for handling external inputs and state changes based on validation logic.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-007
- **Conflicts with:** None
---

[FR-003]: Gyroscope Data Acquisition
**Description**: The sun search control system shall send a two-byte fetch command (0xEB91) to the gyroscope through the asynchronous serial port (ICD::Port_Gyro_Command, 0x881A) every cycle and receive the gyroscope measurement data through the same port. Gyro response packet: [status: 1 byte][angle_x: 2 bytes][angle_y: 2 bytes][angle_z: 2 bytes][checksum: 1 byte], Big Endian. Status byte: 0x00 = ok, 0x01 = comm fail, 0x02 = data invalid. All multi-byte fields Big Endian. Add to ICD. Owner: Team-HAL; Next action: baseline ICD and update all address references.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Describes the specific communication sequence and data collection task for the gyroscope subsystem.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-005, ASR-005
- **Conflicts with:** None (Resolved via ASR-005 ICD)
---

[FR-004]: Sun Sensor Data Acquisition
**Description**: The sun search control system shall acquire sun sensor data every 160ms via Analog to Digital (AD) conversion. Outputs include power-on status, sun visibility (SP signal), and measurement angle (12-bit). Sun sensor packet: byte0[bit7]=power-on, byte0[bit6]=visibility, bytes1-2: angle[11:0], Big Endian (see ICD::SUN_SENSOR_DATA).

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the data collection behavior for the sun sensor subsystem using AD conversion.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-006
- **Conflicts with:** None
---

[FR-005]: Thruster Control Output
**Description**: The sun search control system shall control the pulse output to the three-axis control thrusters (12 10N thrusters) by writing the enable signal to the controller. The switch data of 12 thrusters will be sequentially output at the 128th ms of each 160ms control cycle. All 12 thruster switch signals must be output sequentially starting at t=128ms; all outputs completed within 5ms; order: 2A,2B,3A,...7B. Output schema: [byte0: 2A enable][byte1: 2B enable][byte2: 3A enable][byte3: 3B enable][byte4: 4A enable][byte5: 4B enable][byte6: 5A enable][byte7: 5B enable][byte8: 6A enable][byte9: 6B enable][byte10: 7A enable][byte11: 7B enable]; each value: 1=ON, 0=OFF. If controller does not acknowledge all 12 switch signals within 5ms window, raise FAULT flag and enter Rate Damping mode.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Describes the actuation behavior and specific timing for driving the satellite's rotation.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003
- **Conflicts with:** None
---

[FR-006]: Operating Mode Management
**Description**: The sun search control system shall manage the operating mode using a mode register to store the current mode word, duration, target angle, and target angular velocity. The system shall support four stages: Rate Damping (RDSM), Pitch Search (PASM), Roll Search (RASM), and Sun Cruise (CSM), switching based on predefined criteria.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the state machine behavior and logic for transitioning between operational phases.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-008, FR-009
- **Conflicts with:** None
---

[FR-007]: System Initialization
**Description**: Upon power on or reset, the sun search control system shall execute initialization once in the main program. This includes controller parameter initialization (set to rate damping), component power-on (sun sensor, gyroscope, thruster), and activation of the 32ms timer interrupt. Step 1: Write value X to register Y for sun sensor power-on. Step 2: Write value Z to register T for gyro. (Reference ICD for specific register addresses/values).

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Describes the startup sequence and state setup behavior of the system.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None
---

[FR-008]: Gyroscope Fault Management
**Description**: If the control computer detects a gyro communication error (length, header, checksum) for five consecutive cycles, the system shall power off the gyroscope, wait five cycles, power on, wait five cycles, and retest. If errors persist for another five cycles, the system shall power off and await ground instructions.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the specific recovery behavior and state transitions in response to a specific fault condition.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-007
- **Conflicts with:** None
---

[FR-009]: Thruster Fault Management
**Description**: If the thruster fires at intervals shorter than 1 second for a continuous duration of 5 seconds, the sun search control system shall output a signal to switch off the thruster to prevent frequent jetting faults. Implementation MUST track thruster firing events: if 5+ firings with intervals <1s within any 5s window, trigger shutdown; test cases to inject mock firings and verify output within 160ms. Track rising edge of enable pulse per thruster; maintain timestamp FIFO size 5 per thruster.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the safety behavior to inhibit actuator operation under anomalous conditions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005
- **Conflicts with:** None
---

[FR-010]: Telemetry Data Transmission
**Description**: The sun search control system shall collect and transmit current operating status (mode word, orientation angle, velocity) every 160ms. Data shall be packaged and sent to the digital tube via asynchronous serial port (ICD::Port_Telemetry, 0x88DB). Telemetry data packet: [mode word: 2 bytes, uint16, BE][orientation: 3-axis, signed int16 each, BE][velocity: 3-axis, signed int16 each, BE][checksum: CRC-8]. Units: orientation (0.01 deg), velocity (0.001 deg/s). Orientation/velocity order: X(roll), Y(pitch), Z(yaw). Range: int16 -32768..32767. CRC error or send fail increments TLM_FAIL_COUNTER.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Describes the data packaging and external communication behavior for monitoring.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-004
- **Conflicts with:** None
---

[FR-011]: Sun Sensor Redundancy Switching
**Description**: If the sun's visible sign remains undetected following two consecutive attempts at both pitch and roll searches, the system shall switch off the primary sun sensor and activate the backup sun sensor, then restart the search and re-enter rate damping mode. To switch, set control register at ICD::SunSensorSwitch; provide telemetry flag SUN_SENSOR_STATUS (0=Primary, 1=Backup) in status packet. If sun sensor visibility bit is 0 in two consecutive pitch and roll cycles (4 total readings), trigger switchover.

**Rationale:** Why this requirement is functional (e.g., describes behavior, input-output transformation).
Defines the redundancy management behavior and mode transition in case of sensor failure.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-004
- **Conflicts with:** None
---