# Non-Functional Requirements Results

[NFR-001]: MCU resource/platform constraints (80C32E, memory, clock)  
**Description:** The control computer CPU uses 80C32… PROM32K bytes, and SRAM8K bytes… 80C32E… main frequency is 11.0592MHZ, including 32KB of PROM and 8KB of SRAM. Acceptance criteria: compiled firmware image (.hex/.bin) shall be < 32KB PROM and RAM usage (static + stack) shall be < 8KB SRAM, verified at build as a gate/check. Owner: Not specified; Next action: Add resource-fit requirement and/or CI build check.  
**Quality Attributes**: Constraint / Portability  
**Measurable Criteria (if provided):** 80C32/80C32E; 11.0592 MHz; PROM 32KB; SRAM 8KB; firmware image <32KB; RAM (static+stack) <8KB; verified at build  
**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** Not specified  
---

[NFR-002]: Execution model constraint (main loop + interrupts; single interrupt)  
**Description:** The control computer runs in the mode of main program plus interruption… interruption is 32 milliseconds regular cycle interruption… Only one interrupt is processed… the 32ms timer interrupt.  
**Quality Attributes**: Reliability / Maintainability (determinism via constrained concurrency)  
**Measurable Criteria (if provided):** Single interrupt source; period 32ms  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** Not specified  
---

[NFR-003]: Timer configuration register constraint for interrupt start  
**Description:** The timer can be started… by writing a '1' to the D[0] bit of the timing control register GTCR0… address of register GTCR0 is 0x8083.  
**Quality Attributes**: Constraint  
**Measurable Criteria (if provided):** GTCR0 @ 0x8083; write 1 to D[0]  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005
- **Conflicts with:** Not specified  
---

[NFR-004]: Hard real-time cyclic scheduling (160ms control cycle; 32ms tick)  
**Description:** Command processing… mandated to occur in a 160ms cycle… sun sensor/thruster/attitude/mode/fault management scheduled every 160ms… interruption is 32 milliseconds regular cycle interruption… at the 128th ms of each 160ms control cycle thruster switch data output. The system shall detect and log any schedule overrun or missed cycle (e.g., ISR execution >32ms period or control loop exceeding 160ms) with status observable via telemetry. Owner: Not specified; Next action: Update requirement to mandate schedule observability.  
**Quality Attributes**: Performance (Real-time)  
**Measurable Criteria (if provided):** 160ms cycle; 32ms periodic interrupt; thruster output at 128ms; log on any ISR/control-cycle overrun/miss; observability via telemetry  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002
- **Conflicts with:** Not specified  
---

[NFR-005]: AD conversion data format for sun angle  
**Description:** The angle measurement data is obtained by analog-to-digital conversion… 12-bit measurement (offset binary code, range 0x000~0xFFF)… minimum code corresponds to 5/2048.  
**Quality Attributes**: Constraint / Interoperability  
**Measurable Criteria (if provided):** 12-bit; offset binary; 0x000–0xFFF; LSB mapping noted as 5/2048  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** Not specified  
---

[NFR-006]: Serial transmission inter-byte timing constraint  
**Description:** The interval between each byte sent is less than 5us… each byte of the telemetry data is sent with an interval of less than 5 microseconds between them.  
**Quality Attributes**: Performance (Timing)  
**Measurable Criteria (if provided):** Inter-byte gap < 5 µs (for gyro init/control commands and telemetry TX)  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-023
- **Conflicts with:** Not specified  
---

[NFR-007]: Limit on ground command rate  
**Description:** The digital control sub-system is restricted to sending no more than one remote command to the control software within each 160ms interval. The system shall reject or delay any remote command received within 160ms of a previous accepted command and shall log a reason code/event for the rejection/delay. Owner: Not specified; Next action: Amend requirement with criterion and test/monitoring hook.  
**Quality Attributes**: Performance / Safety (load limiting)  
**Measurable Criteria (if provided):** ≤ 1 command per 160ms; commands arriving <160ms after last accepted are rejected/delayed; reason code/event logged  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** Not specified  
---

[NFR-008]: Gyro fetch-to-read minimum delay constraint  
**Description:** The time interval from sending fetch instruction to reading data from asynchronous serial port should be greater than 5ms. The system firmware and test harness shall instrument and log the measured fetch-to-read delay and shall raise an error on any measurement <5ms. Owner: Not specified; Next action: Add explicit measurement/log to requirement and test.  
**Quality Attributes**: Performance (Timing) / Reliability  
**Measurable Criteria (if provided):** Delay > 5 ms; instrumented measurement and logged; error if <5ms  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** Not specified  
---

[NFR-009]: Sun sensor switching pulse timing constraint  
**Description:** The sun sensor switching pulse shall be a positive pulse of 190ms ±1ms. Owner: Not specified; Next action: Clarify and synchronize all documentation and requirements to use one pulse timing.  
**Quality Attributes**: Performance (Timing) / Interoperability  
**Measurable Criteria (if provided):** Positive pulse 190 ms ±1 ms  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020
- **Conflicts with:** Not specified  
---

[NFR-010]: Deterministic thruster output slot within cycle  
**Description:** At the 128th ms of each 160ms control cycle, the switch data of 12 10N thrusters will be sequentially output.  
**Quality Attributes**: Performance (Real-time determinism)  
**Measurable Criteria (if provided):** Output at t=128ms in each 160ms cycle  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, NFR-004
- **Conflicts with:** Not specified  
---

[NFR-011]: Serial port addressing constraints for device interfaces  
**Description:** Remote command receiving serial port designated as address 0x88DA… telemetry transmission uses asynchronous serial port address 0x88DB… All gyro command and data transactions shall utilize serial port address 0x881A exclusively. Owner: Not specified; Next action: Update all requirements (FR-007, FR-019, NFR-011, ASR-003) to use only 0x881A or define clear disambiguation.  
**Quality Attributes**: Constraint / Interoperability  
**Measurable Criteria (if provided):** Addresses 0x88DA, 0x88DB, 0x881A (gyro exclusively)  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-007, FR-019, FR-023
- **Conflicts with:** Not specified  
---