# Functional Requirements Results

[FR-001]: Perform sun acquisition and maintain sun-pointing attitude  
**Description**: **DEPRECATED (Derived from FR-001)**: This requirement combined sensor acquisition, attitude estimation, and actuation control into a single statement. It is replaced by FR-001A, FR-001B, and FR-001C. (Next action: Create three new atomic requirements for sensing, estimation, and actuation; update original FR.)  
**Rationale:** Describes the primary end-to-end control behavior (sense → estimate → actuate) the system must perform.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014
- **Conflicts with:** NFR-004 (timing constraints may constrain algorithm complexity)
---

[FR-001A]: Acquire gyroscope and sun sensor measurement data  
**Description**: Derived from FR-001: The sun search control system shall acquire all relevant measurement data from gyroscopes and sun sensors for sun acquisition. (Next action: Create three new atomic requirements for sensing, estimation, and actuation; update original FR.)  
**Rationale:** Describes a discrete sensing/data acquisition behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-008
- **Conflicts with:** None specified
---

[FR-001B]: Estimate current attitude from acquired sensor data  
**Description**: Derived from FR-001: The sun search control system shall determine/estimate the current attitude of the satellite using measurement data acquired from gyroscopes and sun sensors. Acceptance: Estimated attitude error < 1 deg RMS against known input profile over 10 cycles (test case ref: TestCase-Est-001). (Next action: Owner to specify or reference estimator algorithm and required accuracy.)  
**Rationale:** Describes an input-to-output transformation (estimation) that can be verified independently.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001A, FR-010
- **Conflicts with:** None specified
---

[FR-001C]: Control satellite rotation to enable sun detection and maintain sun-pointing  
**Description**: Derived from FR-001: The sun search control system shall control the satellite to rotate around the pitch or roll axis so that the sun sensor can detect the sun and maintain the spacecraft's sun-pointing attitude. (Next action: Create three new atomic requirements for sensing, estimation, and actuation; update original FR.)  
**Rationale:** Describes a discrete actuation/control behavior with a clear operational objective.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001B
- **Conflicts with:** None specified
---

[FR-002]: Receive and verify ground commands; set operating mode word  
**Description**: The sun search control system shall receive ground commands through a serial port, perform command verification, and set the satellite's operating mode word. Only commands that pass verification (data length, frame header, checksum) shall be executed, leading to setting the satellite working mode for the next cycle.  
**Rationale:** Defines command ingestion, validation, and mode-setting behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-001, NFR-002
- **Conflicts with:** None specified
---

[FR-003]: Receive remote control data each control cycle  
**Description**: The sun search control system shall receive data from the asynchronous serial port every 160 ms cycle; the remote control receiving serial port address shall be 0x88DA; and the digital control subsystem shall send no more than one remote command to the control software within each 160 ms interval.  
**Rationale:** Specifies periodic command reception behavior and an operational constraint on command rate.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** None specified
---

[FR-004]: Initialize on power-on/reset and start 32 ms timer interrupt  
**Description**: Upon power on or reset, the sun search control system shall execute initialization once in the main program, including controller parameter initialization, setting the initial working mode to rate damping, powering on sun sensor/gyroscope/thruster (per referenced procedure), and activating a continuous 32 ms timer interrupt by writing '1' to D[0] of GTCR0 (address 0x8083).  
**Rationale:** Defines required startup sequence and initialization actions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015, NFR-003, ASR-002
- **Conflicts with:** None specified
---

[FR-005]: Store mode control data in mode register  
**Description**: The sun search control system shall use a mode register to store the current operating mode word, the current mode duration, the target angle, and the target angular velocity in order to control the operating mode.  
**Rationale:** Defines required state management behavior for mode control.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-012, FR-013, FR-014
- **Conflicts with:** None specified
---

[FR-006]: Acquire gyroscope data each cycle (fetch + receive)  
**Description**: The sun search control system shall send a two-byte fetch command (0xEB91) to the gyroscope through the asynchronous serial port every cycle and shall receive the gyroscope measurement data through the asynchronous serial port; the serial port address used for sending commands and receiving data shall be 0x881A.  
**Rationale:** Defines the gyro data acquisition function and its interface.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-006, NFR-007
- **Conflicts with:** None specified
---

[FR-007]: Validate acquired gyroscope data frames  
**Description**: The sun search control system shall judge/verify the length, frame header, and checksum of the collected gyroscope data.  
**Rationale:** Defines data integrity checking behavior for sensor input.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** None specified
---

[FR-008]: Acquire sun sensor data every 160 ms  
**Description**: The sun search control system shall acquire sun sensor data every 160 ms, including the component power-on status, the sun visible sign (SP), and the sun measurement angle (angle between sunlight and sensor normal line) via AD conversion and latch-circuit collection of SP/power-state signals.  
**Rationale:** Defines periodic sun sensor measurement acquisition and expected outputs.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-005
- **Conflicts with:** None specified
---

[FR-009]: Acquire thruster power-on status every 160 ms  
**Description**: The sun search control system shall acquire thruster data every 160 ms by reading an AD acquisition register address and outputting/recording the thruster power-on status; the power status signal shall be collected through AD conversion.  
**Rationale:** Defines periodic actuator status acquisition.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** None specified
---

[FR-010]: Determine three-axis attitude every 160 ms  
**Description**: Every 160 ms, the sun search control system shall determine the satellite three-axis attitude by receiving angular velocity measured by the gyroscope, attitude angle collected by the sun sensor, and sun visible sign; it shall calculate three-axis angular velocity based on gyro measurement data and estimate the attitude angle.  
**Rationale:** Defines the estimation function and its inputs/outputs.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008, NFR-001
- **Conflicts with:** None specified
---

[FR-011]: Manage sun-search mode switching every 160 ms  
**Description**: The sun search control system shall perform sun search mode switching management every 160 ms, including accumulating working time in the current mode and evaluating whether to switch working mode based on predefined criteria/thresholds.  
**Rationale:** Defines periodic supervisory control and mode transition behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-010, NFR-001
- **Conflicts with:** None specified
---

[FR-012]: Execute rate damping mode (RDSM)  
**Description**: When initiated during power-on initialization or when the sun is not detectable, the sun search control system shall set the target three-axis angular velocity to zero to stabilize attitude (minimize angular velocity), accumulate current-mode working time, and evaluate whether to switch modes.  
**Rationale:** Defines a specific operational mode behavior and control objective.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, FR-015
- **Conflicts with:** None specified
---

[FR-013]: Execute pitch-axis sun search mode (PASM)  
**Description**: When rate damping completes successfully or an initial sun search fails, the sun search control system shall set a control target to rotate the satellite around the Y (pitch) axis at a specified rate, track time in mode, and evaluate whether to switch working mode.  
**Rationale:** Defines pitch search behavior and mode progression logic.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, FR-015
- **Conflicts with:** None specified
---

[FR-014]: Execute roll-axis sun search mode (RASM)  
**Description**: If a previous pitch search is unsuccessful, the sun search control system shall set a new control target to rotate the satellite around the X (roll) axis at a specified rate, update the working mode word if necessary, track time in mode, and evaluate whether to switch working mode.  
**Rationale:** Defines roll search behavior and mode progression logic.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, FR-015
- **Conflicts with:** None specified
---

[FR-015]: Execute sun cruise mode (CSM) after sun detection  
**Description**: Following successful sun detection, the sun search control system shall set control targets to reduce three-axis angular velocity to zero to stabilize attitude, and continue to record time spent in the current operational mode.  
**Rationale:** Defines post-acquisition tracking/stabilization behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** None specified
---

[FR-016]: Switch to backup sun sensor after repeated search failure  
**Description**: **DEPRECATED (Derived from FR-016)**: This requirement conflated failure detection, sensor switching, thruster adjustment, and mode reset. It is replaced by FR-016A, FR-016B, FR-016C, and FR-016D. (Next action: Decompose as above; clarify triggering condition (N value), explicit outputs, and side effects.)  
**Rationale:** Defines fault-recovery/contingency behavior involving sensor redundancy and mode reset.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-011, FR-012, FR-013, FR-014, FR-017
- **Conflicts with:** None specified
---

[FR-016A]: Detect repeated sun search failure condition  
**Description**: Derived from FR-016: The sun search control system shall detect that the sun search has been unsuccessful when PASM_attempts >= 2 AND RASM_attempts >= 2 AND SP == not visible in all attempts; this condition shall trigger the failure logic. Added counter model: PASM_attempts:uint8; RASM_attempts:uint8; increment on each failed attempt; reset to 0 on sun-detection. (Next action: Document counter and reset model, cross-ref err handling.)  
**Rationale:** Defines a discrete detection/trigger condition that can be tested independently.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-014
- **Conflicts with:** None specified
---

[FR-016B]: Switch from primary to backup sun sensor upon repeated failure  
**Description**: Derived from FR-016: Upon the repeated sun search failure condition, the sun search control system shall switch off the primary sun sensor and activate the backup sun sensor. (Next action: Decompose as above; clarify triggering condition (N value), explicit outputs, and side effects.)  
**Rationale:** Defines a discrete hardware switching action.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016A, FR-017
- **Conflicts with:** None specified
---

[FR-016C]: Adjust thruster settings for new search phase after sensor switch  
**Description**: Derived from FR-016: Upon switching to the backup sun sensor, the sun search control system shall emit a signal to adjust the thruster settings as necessary for the new search phase. (Next action: Decompose as above; clarify triggering condition (N value), explicit outputs, and side effects.)  
**Rationale:** Defines a discrete actuation configuration update.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016B
- **Conflicts with:** None specified
---

[FR-016D]: Restart sun search using backup sensor and re-enter rate damping mode  
**Description**: Derived from FR-016: After activating the backup sun sensor, the sun search control system shall restart the search for the sun using the backup sensor and re-enter rate damping mode to stabilize the satellite's attitude. (Next action: Decompose as above; clarify triggering condition (N value), explicit outputs, and side effects.)  
**Rationale:** Defines a discrete recovery flow step (restart + mode entry).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016B, FR-012
- **Conflicts with:** None specified
---

[FR-017]: Control sun sensor switching pulse output  
**Description**: When there is a failure in the visibility of the sun sensor, the sun search control system shall generate a sun sensor switching command by writing an enable signal to the sun sensor switch control register to output the specified switching pulse. Acceptance: 190±1 ms instruction, 1 ms pulse, verified by oscilloscope sample/trace at control register pin. (Next action: Attach test/measurement step for switching output.)  
**Rationale:** Defines the actuator/control action for switching sun sensors.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008
- **Conflicts with:** None specified
---

[FR-018]: Detect frequent thruster firing fault and shut off thruster  
**Description**: Every 160 ms, the sun search control system shall review thruster injection interval times; if thruster firing intervals are shorter than 1 second continuously for 5 seconds, the system shall declare a frequent-jetting fault and output a signal to switch off the thruster. Derived test interface detail: ThrusterIntervalMonitor input shall be thruster fire timestamps; the system shall compute firing intervals from consecutive timestamps using the control computer time reference; fault is detected if intervals are < 1 second continuously for 5 seconds. Emit: ThrusterFaultEvent { when, duration, shutdown:bool } to log/telemetry. (Next action: Define test/log/telemetry output for fault detection.)  
**Rationale:** Defines fault detection and mitigation behavior for actuators.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, NFR-001
- **Conflicts with:** None specified
---

[FR-019]: Handle gyroscope communication faults with power-cycle and retry  
**Description**: Every 160 ms, if the control computer detects a gyro communication error (data length/frame header/checksum), it shall increment an error cycle count; upon five consecutive error cycles it shall power off the gyro, wait five cycles, power on the gyro, wait five cycles, then reinitiate communication (send fetch command). If errors persist for another five consecutive cycles, it shall power off the gyro again and await further ground instructions.  
**Rationale:** Defines fault management state machine for gyro communications.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-002, NFR-001
- **Conflicts with:** None specified
---

[FR-020]: Power on and control gyro during initialization  
**Description**: During power-on initialization, the sun search control system shall send the gyro power-on command 0xEB92 via the asynchronous serial port and then send the gyro control command via the asynchronous serial port at address 0x881A to activate and control the gyro. Acceptance: Command 0xEB92 and subsequent control cmd issued with <5us interval; gyro responds with ready status within 50 ms; if not, raise GyroInitTimeout error; owner: AttitudeControlLead. (Next action: Add timeout/error logic and assign owner.)  
**Rationale:** Defines required initialization control of a critical sensor.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-006
- **Conflicts with:** None specified
---

[FR-021]: Output thruster switch data at specified time within control cycle  
**Description**: At the 128th ms of each 160 ms control cycle, the sun search control system shall sequentially output the switch data of 12 thrusters (jet outputs) at the required time. Acceptance: All 12 thruster outputs completed and observable on output lines within 2 ms of 128 ms control cycle event. (Next action: Specify timing acceptance/test for output sequence.)  
**Rationale:** Defines time-triggered actuator command output behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, ASR-002
- **Conflicts with:** None specified
---

[FR-022]: Package and transmit telemetry/status every 160 ms  
**Description**: Every 160 ms, the sun search control system shall collect telemetry including the current working mode word, orientation angle, and velocity; package it into a predefined format; and send it via the asynchronous serial port at address 0x88DB for display/monitoring. TelemetryMsg contract shall be defined as a concrete, version-controlled schema including explicit field types, order, units, encoding, and error/padding handling (e.g., TelemetryMsg = struct { mode:uint8, angle:int16, velocity:int16 }; total length = N bytes). TelemetryMsg format v1.0; see InterfaceDoc v1.0, Section 3.4. (Next action: Owner to define/reference TelemetryMsg data contract by version.)  
**Rationale:** Defines periodic telemetry generation and transmission behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, NFR-001, NFR-006
- **Conflicts with:** None specified
---