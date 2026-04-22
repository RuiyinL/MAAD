# Non-Functional Requirements Results:

[NFR-001]: Control Cycle Timing
**Description:** The sun search control system processes key functions (command reception, data acquisition, mode management, telemetry) in a 160ms cycle.

**Quality Attributes**: Performance, Timing

**Measurable Criteria (if provided):** 160ms cycle duration.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003
- **Conflicts with:** None
---

[NFR-002]: Interrupt Timing
**Description:** The control computer runs in the mode of main program plus interruption, where the interruption is a 32 milliseconds regular cycle interruption. Only one interrupt is processed in the system.

**Quality Attributes**: Performance, Determinism

**Measurable Criteria (if provided):** 32ms interrupt interval. ISR execution time must be <= 500us, measured every 32ms cycle; jitter in interrupt interval <= 5us. Metric: ISR_EXECUTION_TIME_us. Requirement: All ISR executions <= 500us; 99.9th percentile must be < 460us; measured using MCU timer capture. ISR_OVERRUN_COUNTER increments on each execution >500us. Send TLM ISR_STATUS with counter and max observed.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None
---

[NFR-003]: Thruster Output Latency
**Description:** At the 128th ms of each 160ms control cycle, the switch data of 12 10N thrusters will be sequentially output.

**Quality Attributes**: Performance, Timing

**Measurable Criteria (if provided):** Output must occur at t=128ms within the 160ms cycle.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005
- **Conflicts with:** None
---

[NFR-004]: Serial Communication Timing
**Description:** The interval between each byte sent via serial port (gyro commands, telemetry) is less than 5us. Metric: SERIAL_BYTE_INTERVAL_us at TX pin. All bytes in a frame must be separated by <5us as verified by logic analyzer; alert if >5us occurs 3+ cases per 1000 frames.

**Quality Attributes**: Performance, Interface

**Measurable Criteria (if provided):** Inter-byte interval < 5 microseconds.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-010
- **Conflicts with:** None
---

[NFR-005]: Gyro Response Timing
**Description:** The time interval from sending fetch instruction to reading data from asynchronous serial port should be greater than 5ms.

**Quality Attributes**: Performance, Timing

**Measurable Criteria (if provided):** Fetch-to-read delay > 5 milliseconds.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** None
---

[NFR-006]: Data Resolution
**Description:** The angle measurement data is obtained by analog-to-digital conversion of the angle analog signal, which is a 12-bit measurement (offset binary code, range 0x000~0xFFF).

**Quality Attributes**: Accuracy, Data Integrity

**Measurable Criteria (if provided):** 12-bit resolution, Range 0x000-0xFFF.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** None
---

[NFR-007]: Command Integrity
**Description:** The system must verify whether the received ground command data length, frame header, and checksum conform to specifications. Only verified commands are executed.

**Quality Attributes**: Reliability, Security

**Measurable Criteria (if provided):** Verification of length, header, checksum required.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---

[NFR-008]: Memory Constraints
**Description:** The control computer CPU uses 80C32, PROM 32K bytes, and SRAM 8K bytes.

**Quality Attributes**: Resource Efficiency, Portability

**Measurable Criteria (if provided):** 32KB PROM, 8KB SRAM. Build metric: PROM_SIZE, SRAM_USAGE. Build fails if PROM_SIZE > 32768B or SRAM_USAGE > 8192B.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001
- **Conflicts with:** None
---

[NFR-009]: Sun Sensor Switching Pulse
**Description:** The sun sensor switching instruction shall involve a positive pulse lasting 190 milliseconds, with an allowable deviation of ±1 millisecond.

**Quality Attributes**: Timing, Accuracy

**Measurable Criteria (if provided):** 190ms +/- 1ms pulse width. Metric: SUN_SW_PULSE_WIDTH_ms, measured at SUN_SENSOR_SWITCH_OUT; require 99.9th percentile in 189–191ms over 1000 tests.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-011
- **Conflicts with:** None (Resolved per Hardware Spec)
---