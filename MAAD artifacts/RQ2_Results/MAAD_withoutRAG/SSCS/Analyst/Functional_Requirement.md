# Functional Requirements Results

[FR-001]: Sun acquisition and sun-pointing control  
**Description**: The main function of the sun search control system is to perform sun acquisition by collecting measurement data from gyroscopes and sun sensors to determine the current attitude of the satellite, and then control the satellite to rotate around the pitch or roll axis so that the sun sensor can detect the sun and maintain the spacecraft's sun-pointing attitude.  
**Rationale:** Describes the primary control behavior: sense → determine attitude → actuate rotation → maintain pointing.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, NFR-004, NFR-006
- **Conflicts with:** Not specified  
---

[FR-002]: Receive and verify ground commands; set operating mode word  
**Description**: The sun search control system can receive ground commands through a serial port, perform command verification, and set the satellite's operating mode word. Only commands that successfully pass this verification process will be executed, leading to the setting of the satellite's working mode for the next cycle.  
**Rationale:** Defines command-processing functionality including validation and mode update.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-004, NFR-007
- **Conflicts with:** Not specified  
---

[FR-003]: Ground command reception each control cycle via specified serial port  
**Description**: This process is mandated to occur in a 160ms cycle. Specifically, data is to be received from the asynchronous serial port every cycle, with the remote control receiving serial port being designated as address 0x88DA. The digital control sub-system is restricted to sending no more than one remote command to the control software within each 160ms interval.  
**Rationale:** Defines periodic command input behavior and command-rate limitation.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** Not specified  
---

[FR-004]: Verify command frames (length/header/checksum) against specification  
**Description**: Following the receipt of data, the sun search control system must verify whether the data length, frame header, and checksum conform to the specifications detailed in Table 3.2-1.  
**Rationale:** Defines validation function for inbound command frames.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** Not specified  
---

[FR-005]: Initialize system on power-on/reset and start 32ms timer interrupt  
**Description**: The initialization setting of the sun search control system should be executed once in the main program upon power on or reset… starts with controller parameter initialization, setting the initial working mode to rate damping… component power-on operation… Finally, a 32ms timer interrupt is activated to manage and monitor the operation timing accurately.  
**Rationale:** Defines required startup sequence and initial mode selection.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, FR-015, FR-016, NFR-003
- **Conflicts with:** Not specified  
---

[FR-006]: Collect component power status and sensor measurement data  
**Description**: The sun search control system need to collect the power-on status of each component and the sensor measurement data… outputs include the power-on status of each component, the count of seconds pulsed by the gyroscope, as well as the visibility, sign, and angle of the sun as detected by the sun sensor… power-on status and pulse count of the gyroscope are collected via the serial port… sun sensor power-on state, sun visibility/sign, measurement angle via AD conversion… thruster power-on state via AD conversion. Collected status outputs shall be defined with an explicit schema/table specifying output fields, types, and encoding (e.g., ComponentID, PowerOn bit, GyroPulseCount, SPSign bit, Angle u12). Owner: Not specified; Next action: Define schema/table for collected status outputs.  
**Rationale:** Defines data acquisition functions and expected outputs.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-008, FR-009
- **Conflicts with:** Not specified  
---

[FR-007]: Acquire gyroscope measurement data each cycle (fetch + receive + validate)  
**Description**: In order to acquire gyroscope data, the sun search control system sends a two-byte fetch command 0xEB91 to the gyro through the asynchronous serial port every cycle… receives the gyro measurement data through the asynchronous serial port… needs to judge the length, frame header and checksum of the collected data. All gyro command and data transactions shall utilize asynchronous serial port address 0x881A. The gyro command/response frame format (including length, field ordering, frame header, and checksum algorithm) shall be specified as an explicit schema/table and used for validation. Owner: Not specified; Next action: Update requirement for port and structure, attach/provide data contract/schema.  
**Rationale:** Defines sensor I/O behavior including request/response and integrity checking.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-008, NFR-006
- **Conflicts with:** Not specified  
---

[FR-008]: Acquire sun sensor data every 160ms (AD conversion + SP/latch)  
**Description**: The sun search control system needs to acquire sun sensor data, which must be carried out every 160ms… expected outputs include power-on status, sun visible sign, and measurement angle… 12-bit angle data is obtained through AD conversion… and the SP signal and the power state signal are compared by the latch circuit to collect.  
**Rationale:** Defines periodic acquisition of sun sensor observables.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-005
- **Conflicts with:** Not specified  
---

[FR-009]: Acquire thruster power-on status every 160ms (AD conversion)  
**Description**: The sun search control system needs to acquire thruster data, which is scheduled to occur every 160ms… output the thruster power-on status… collect the power status signal through AD.  
**Rationale:** Defines periodic acquisition of actuator status.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** Not specified  
---

[FR-010]: Determine three-axis attitude every 160ms from gyro + sun sensor inputs  
**Description**: The sun search control system needs to determine the three-axis attitude of the satellite, which is carried out every 160 ms… receive angular velocity measured by the gyroscope, attitude angle collected by the sun sensor and visible sign of the sun. Then the sun search control system calculate the three-axis angular velocity based on the gyro measurement data, and estimate the attitude angle. The attitude estimation algorithm and/or accuracy acceptance criteria, and the output data schema (e.g., Euler angles vs quaternion and units/encoding) shall be defined. Owner: Not specified; Next action: Define algorithm or accuracy criterion within requirement.  
**Rationale:** Defines estimation/processing function transforming measurements into attitude/velocity estimates.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-008, NFR-004
- **Conflicts with:** Not specified  
---

[FR-011]: Manage mode switching every 160ms (track mode time, evaluate transitions)  
**Description**: The sun search control system needs to have the sun search mode switching management, which must be scheduled to occur every 160ms… receives current three-axis angular velocity and current working mode word… sets target three-axis angular velocity to zero to stabilize… accumulates working time in the current mode… evaluates whether to switch the working mode based on predefined criteria or thresholds. Every mode transition shall generate a log entry/event describing from→to mode, cause, timestamp, and prior mode duration. Owner: Not specified; Next action: Add test/event description to mode management requirement.  
**Rationale:** Defines supervisory control logic and mode transition evaluation.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-017, FR-018, FR-019, FR-020, NFR-004
- **Conflicts with:** Not specified  
---

[FR-012]: Execute rate damping mode (RDSM) to reduce angular velocity  
**Description**: The whole search process is divided into four stages… rate damping RDSM… The function of rate damping is to reduce the angular velocity of the three-axis rotation… target three-axis angular velocity to zero to stabilize the satellite's attitude… initiated during power-on initialization or when the sun search control system fails to detect the sun.  
**Rationale:** Defines a concrete operational mode behavior and its trigger conditions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** Not specified  
---

[FR-013]: Execute pitch search mode (PASM) to rotate about Y (pitch) axis  
**Description**: The function of pitch search is to control the star to rotate along the pitch axis to search for the sun at a certain angular velocity… initiated when rate damping has been successfully completed or if an initial attempt to search for the sun has failed… sets a new control target to rotate the satellite around the Y axis at the specified rate.  
**Rationale:** Defines another operational mode and its control output.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** Not specified  
---

[FR-014]: Execute roll search mode (RASM) to rotate about X (roll) axis  
**Description**: The function of roll search is to control the star to rotate along the roll axis at a certain angular velocity searching for the sun… initiated if a previous pitch search for the sun proves unsuccessful… output is a new control target, which directs the satellite to rotate around the X axis at the specified rate, alongside an updated working mode word if necessary.  
**Rationale:** Defines roll search mode behavior and transition condition.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** Not specified  
---

[FR-015]: Execute sun cruise mode (CSM) after sun detection to stabilize and track  
**Description**: The functions of cruising towards the sun are to keep a stable attitude and keep tracking the sun after searching for the sun… following successful sun detection… set control targets aiming to reduce the three-axis angular velocity to zero… continue to record duration of time spent in the current operational mode.  
**Rationale:** Defines post-acquisition control behavior and stabilization objective.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** Not specified  
---

[FR-016]: Switch to backup sun sensor after repeated unsuccessful searches  
**Description**: When the sun visible sign (SP) remains undetected following two consecutive attempts at both pitch and roll searches… the sun search control system sends a signal to switch off the primary sun sensor and activate the backup sun sensor… restarts the search for the sun using the backup sensor and re-enters rate damping mode.  
**Rationale:** Defines fault/contingency behavior and hardware switching action.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-011, FR-012, FR-013, FR-014, FR-021
- **Conflicts with:** Not specified  
---

[FR-017]: Detect and mitigate frequent thruster firing fault  
**Description**: Routine review every 160ms… when the system detects that the thruster has been firing at intervals shorter than 1 second for a continuous duration of 5 seconds… outputs a signal to switch off the thruster.  
**Rationale:** Defines fault detection logic and protective action on actuators.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, NFR-004
- **Conflicts with:** Not specified  
---

[FR-018]: Detect and mitigate gyro communication faults with power-cycle recovery  
**Description**: Checks every 160ms… if gyro communication error (data length/frame header/checksum), increment error cycle count… if errors for five consecutive cycles, power off gyro… wait five cycles then power on… wait additional five cycles then resume communication… if errors persist for another five consecutive cycles, power off and await ground instructions.  
**Rationale:** Defines fault management state machine for gyro communications.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, NFR-004
- **Conflicts with:** Not specified  
---

[FR-019]: Power on and control gyro during initialization using specified commands  
**Description**: When powered on… sends a gyroscope home appliance command (0xEB92) through a serial port, and then sends a gyroscope control command through another serial port with address 0x881A. All gyro command and data transactions shall utilize asynchronous serial port address 0x881A. Owner: Not specified; Next action: Update all referring requirements to use only 0x881A or define clear disambiguation.  
**Rationale:** Defines required actuator/sensor initialization interactions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-006
- **Conflicts with:** Not specified  
---

[FR-020]: Control sun sensor switch via enable signal to generate switching pulse  
**Description**: When there is a failure in the visibility of the sun sensor… sending a switching command… positive pulse lasting for 190 milliseconds ±1 millisecond… achieved by software writing an enable signal to the designated control register to initiate the pulse.  
**Rationale:** Defines control output behavior to switch sun sensor state.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-009
- **Conflicts with:** Not specified  
---

[FR-021]: Store and use mode register fields for mode control  
**Description**: The sun search control system needs to use a mode register to store the current operating mode word, the current mode duration, the target angle, and the target angular velocity in order to control the operating mode.  
**Rationale:** Defines required state management needed for control logic.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011
- **Conflicts with:** Not specified  
---

[FR-022]: Output thruster switch data at defined point within the 160ms cycle  
**Description**: At the 128th ms of each 160ms control cycle, the switch data of 12 10N thrusters will be sequentially output (the system needs to output the jet at a certain time). The sequence order, inter-switch timing (gap/duration), and thruster switch data format/schema shall be explicitly defined (e.g., ordered list [2A,2B,...,7B] and per-output timing) in a referenced table/schema. Owner: Not specified; Next action: Expand requirement to specify order, per-output duration/gap, and signal schema.  
**Rationale:** Defines time-triggered actuator output behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-010
- **Conflicts with:** Not specified  
---

[FR-023]: Package and transmit software operational telemetry every 160ms  
**Description**: The sun search control system needs to collect and transmit the current operating status of its software… every 160 milliseconds… gather telemetry including current working mode word, orientation angle, and velocity… packaged into a predefined format… sent… using the asynchronous serial port address 0x88DB. The telemetry packet format (fields, sizes, ordering, and error checking such as checksum/CRC) shall be explicitly defined as a schema/table and referenced by this requirement. Owner: Not specified; Next action: Add a schema/table for telemetry output; reference in requirement.  
**Rationale:** Defines telemetry collection, formatting, and transmission behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, NFR-004, NFR-006
- **Conflicts with:** Not specified  
---

[FR-024]: Use data management computer for command/telemetry handling  
**Description**: The sun search control system needs to use a data management computer to receive ground operator commands for packaging telemetry data and sending telemetry commands.  
**Rationale:** Defines integration function/role allocation with an external on-board computer.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-023
- **Conflicts with:** Not specified  
---