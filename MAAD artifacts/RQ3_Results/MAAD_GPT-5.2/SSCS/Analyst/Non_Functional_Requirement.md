# Non-Functional Requirements Results

[NFR-001]: Control cycle scheduling (160 ms)  
**Description:** Multiple functions are mandated to occur in a 160 ms cycle (command receive/verify, sun sensor acquisition, thruster data acquisition, attitude determination, mode switching management, telemetry collection/transmission). Added observability/acceptance: Metric ControlCycleDuration shall be measured at a defined software event/log point each cycle; requirement is ControlCycleDuration = 160 ±2 ms; log at each cycle completion shall include {cycleId:uint32, duration:uint16 ms} with event ID and timestamp; alert/error condition is 3 consecutive out-of-bounds cycles. (Next action: Add observability metric, alert window, log field, and next-pulse error handling.)  
**Quality Attributes**: Performance, Real-time/Timing  
**Measurable Criteria (if provided):** 160 ms control cycle; ControlCycleDuration = 160 ±2 ms; per-cycle log {cycleId:uint32, duration:uint16 ms} with event ID and timestamp; alert on 3 consecutive out-of-bounds cycles.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None specified
---

[NFR-002]: Command verification criteria for ground commands  
**Description:** Following receipt of ground command data, the system must verify whether data length, frame header, and checksum conform to the specifications detailed in Table 3.2-1; only commands that successfully pass this verification process will be executed. Added schema requirement: either (a) restate the command field definitions in this requirement, or (b) include a direct, versioned normative reference to Table 3.2-1. Example schema: Command = struct { header:uint8, len:uint8, data:uint8[N], checksum:uint8 }; reference Table 3.2-1 v2.0. On verification failure, the command shall be dropped (not executed). On invalid command, emit: CommandRejected { ts, error, header, len } to log. (Next action: Insert testable log or metric for command verification failures.)  
**Quality Attributes**: Reliability, Integrity  
**Measurable Criteria (if provided):** Verification fields: header, len, checksum; command struct schema stub provided; normative reference: Table 3.2-1 v2.0; error response: drop command; rejection observability: CommandRejected { ts, error, header, len } log event.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** None specified
---

[NFR-003]: Interrupt timing (32 ms periodic interrupt)  
**Description:** The control computer runs main program + interruption; the interruption is a 32 ms regular cycle interruption; only one interrupt is processed: the 32 ms timer interrupt.  
**Quality Attributes**: Performance, Real-time/Timing, Determinism  
**Measurable Criteria (if provided):** 32 ms periodic interrupt; single interrupt source.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None specified
---

[NFR-004]: Thruster output timing within control cycle  
**Description:** At the 128th ms of each 160 ms control cycle, the switch data of 12 thrusters will be sequentially output (the system needs to output the jet at a certain time). Acceptance: 12 thruster switch outputs must be completed within 2 ms starting exactly at t=128 ms within the control cycle. (Next action: Owner to define and document output timing contract.)  
**Quality Attributes**: Real-time/Timing, Determinism  
**Measurable Criteria (if provided):** Output at t = 128 ms within each 160 ms cycle; all 12 outputs completed within 2 ms of the 128 ms trigger.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003
- **Conflicts with:** None specified
---

[NFR-005]: Sun sensor angle measurement encoding  
**Description:** Angle measurement data is obtained by AD conversion of the angle analog signal; it is a 12-bit measurement (offset binary code, range 0x000~0xFFF). SunSensorAngle = struct { uint16 value; } // offset binary, valid 0x000..0xFFF, little-endian, InterfaceDoc v1.2. Units/scale: SunSensorAngle.value represents angle in degrees with angle(deg) = code × (5/2048). Telemetry encoding: SunSensorAngle encoded as uint16, little-endian, no padding. (Next action: Add units and scale to schema/contract.)  
**Quality Attributes**: Data Quality, Interoperability (data format constraint)  
**Measurable Criteria (if provided):** 12-bit; offset binary; 0x000–0xFFF; InterfaceDoc v1.2; little-endian; no padding; unit degrees; scale factor 5/2048 deg per code.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-010
- **Conflicts with:** None specified
---

[NFR-006]: Serial byte transmission spacing (< 5 µs)  
**Description:** The interval between each byte sent is less than 5 µs (applies to gyro power-on/control commands and telemetry transmission). Acceptance: Inter-byte time for command/telemetry <5us, measured on line using oscilloscope/logic analyzer and recorded for one full cycle. (Next action: Specify observability/test evidence for timing.)  
**Quality Attributes**: Performance, Real-time/Timing  
**Measurable Criteria (if provided):** Inter-byte interval < 5 microseconds; acceptance via recorded oscilloscope/logic analyzer capture for one full cycle.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003
- **Conflicts with:** None specified
---

[NFR-007]: Gyro fetch-to-read delay (> 5 ms)  
**Description:** The time interval from sending the gyro fetch instruction to reading data from the asynchronous serial port should be greater than 5 ms. Acceptance: Delay between send and read >=5 ms, trace evidence stored for one test execution. (Next action: Specify test procedure for timing check.)  
**Quality Attributes**: Timing, Interface/Protocol Compliance  
**Measurable Criteria (if provided):** Delay > 5 ms; acceptance via stored logic analyzer/oscilloscope trace for one test execution.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** None specified
---

[NFR-008]: Sun sensor switching pulse timing  
**Description:** The sun sensor switching instruction is 190 ms, with a positive pulse of 1 ms (also stated as 190 ms with allowable deviation ±1 ms). Clarification: switching instruction total duration shall be 190 ±1 ms, with an active-high pulse of 1 ms occurring within that instruction window. Acceptance/test procedure: verify pulse timing using oscilloscope at the control register output; store oscilloscope capture (screenshot or sample trace) demonstrating compliance with 190 ±1 ms and 1 ms pulse. Owner: TestEngineer-Actuation. Evidence: screenshot/trace stored in doc repo. (Next action: Assign acceptance test owner/step.)  
**Quality Attributes**: Real-time/Timing, Interface/Protocol Compliance  
**Measurable Criteria (if provided):** Total duration 190 ±1 ms; active-high pulse width 1 ms; acceptance via stored oscilloscope capture at control register output; evidence stored in doc repo.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017, FR-016
- **Conflicts with:** None specified
---

[NFR-009]: Hardware/compute resource constraints  
**Description:** The control computer CPU uses 80C32/80C32E with main frequency 11.0592 MHz, PROM 32 KB, SRAM 8 KB.  
**Quality Attributes**: Resource Constraints, Portability (platform constraint)  
**Measurable Criteria (if provided):** 11.0592 MHz; 32 KB PROM; 8 KB SRAM; 80C32E.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** None specified
---