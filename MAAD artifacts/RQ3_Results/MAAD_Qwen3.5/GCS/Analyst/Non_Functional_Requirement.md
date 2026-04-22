# Non-Functional Requirements Results:

[NFR-001]: Security and Access Protection
**Description:** Security must be provided to prevent accidental mix-up of commands from different users and to prevent intrusion from the wide area network. The astronomical database must be protected from intrusion. Acceptance: 100% of login/auth transactions use TLS1.2+, failed login threshold triggers alert; at least a monthly penetration test; all privileged actions logged and auditable for 180 days. Authentication, encryption (e.g., TLS1.2+), and intrusion detection system (IDS) metric/alerting for unauthorized access or failed login attempts shall be added.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** Network gateway/firewall required for intrusion security. Access privileges determined during login. 100% login/auth transactions use TLS1.2+; failed login threshold triggers alert; monthly penetration test; privileged actions logged and auditable for 180 days.
---

[NFR-002]: System Response Time
**Description:** Every command must be accepted/rejected within 2 sec before the corresponding action occurs. Status display update must be within 4 sec at local stations. Requests for subsystem status must be answered within 5 sec. Acceptance: 99.9% of commands must be accepted/rejected within 2 sec; status display update in 4 sec (p99); logs show no more than 1 in 1,000 command drops. SLOs for each path shall be defined; percentile/test window and rejection criteria shall be specified. Alert: Trigger when command drop rate exceeds 0.1% in 24h window.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** Command accept/reject: 2 sec (99.9%); Status display update: 4 sec (p99); Subsystem status response: 5 sec; Database access: 2-3 msec; Command drop rate: ≤1 in 1,000; Alert trigger: >0.1% drop rate in 24h window
---

[NFR-003]: Data Transfer Performance
**Description:** The LAN must support a transfer rate of 20-40 Mbits/second. Peak control information within the system is expected to be 100 TPS.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** LAN transfer rate: 20-40 Mbits/second; Peak control information: 100 TPS; Handshaking: 100-200 msec
---

[NFR-004]: Data Storage Capacity
**Description:** The system data capacity must retain 7 days of data produced by the largest instrument, with the last 3 days available interactively from hard disk or similar medium. Acceptance: Hourly check script ensures 7d of data retention; alert if oldest file <7d old; log capacity overrun events. Owner: Storage Team; Next action: implement retention monitor job and alert.

**Quality Attributes**: Capacity, Performance

**Measurable Criteria (if provided):** 7 days total retention; 3 days interactive access from hard disk; Hourly check ensures 7d retention; alert if oldest file <7d old
---

[NFR-005]: System Reliability and Availability
**Description:** The goal is to have restart conditions occur only on hardware failure. The system shall put itself into a safe state upon failure. Recovery and/or reconfiguration goal is 5 minutes from onset of error condition to observing again. Acceptance: From simulated hardware fault, system returns to observing in ≤5 min (p99) in 10 consecutive tests; logs confirm safe state entry. Test scenarios, error states, and recovery metrics (meantime-to-recover p99, max consecutive failures) shall be defined. Acceptance: On simulated error, system deactivates actuators, logs event, triggers hardware interlocks, and issues audible/visible alarm within 5 min. Minimum safe state (hardware powered down, all motors locked, critical interlocks engaged, alarms issued) shall be defined.

**Quality Attributes**: Reliability, Availability

**Measurable Criteria (if provided):** Recovery time: 5 minutes (p99, 10 consecutive tests); Restart only on hardware failure; Safe state entry confirmed in logs; System deactivates actuators, logs event, triggers hardware interlocks, issues audible/visible alarm within 5 min
---

[NFR-006]: Network Transparency for Remote Operations
**Description:** The system shall be totally transparent to local or remote use. The system design should minimize the impact of link bandwidth on transparency. Acceptance: For remote use, 99% of commands respond in <4 sec; user error rate delta with local ops <5% over 24h ops. Proxy metrics (remote command/response latency max, min jitter, error frequency per hour) and user transparency error threshold shall be specified. SLI: remote_cmd_latency_p99 <4s, error_delta_rate_remote_vs_local <5% over 24h, alert if exceeded for >1h.

**Quality Attributes**: Usability, Performance

**Measurable Criteria (if provided):** Remote command response: 99% <4 sec; User error rate delta vs local: <5% over 24h ops; SLI: remote_cmd_latency_p99 <4s; error_delta_rate_remote_vs_local <5% over 24h; Alert if exceeded for >1h
---

[NFR-007]: Safety Requirements
**Description:** The Gemini system must be self-monitoring to invoke safety monitoring to prevent risk to people or damage to equipment. Safety protection must be independent of software where implemented. All hazards capable of causing death and/or loss of irreplaceable equipment shall be passively interlocked. Acceptance: Safety interlocks tested automatically every 168h, any failure triggers hard shutdown; interface exposes interlock status to OCS for monitoring. Required periodic hardware interlock test interval and what constitutes failure shall be added; interface handling between software and hardware for interlock status shall be identified.

**Quality Attributes**: Safety

**Measurable Criteria (if provided):** Hardware interlocks required for critical hazards; Software-independent interlocks for severe damage hazards; Safety interlocks tested automatically every 168h; any failure triggers hard shutdown; interface exposes interlock status to OCS for monitoring
---

[NFR-008]: Maintainability and Portability
**Description:** All software which does not directly control specific hardware must be written as machine independent, portable code. Software must be strictly modular. All Gemini software must be fully documented with Unix-style man pages. Acceptance: Code builds without code changes on Windows and Linux, and passes all non-hardware tests. Doc coverage >90% per code linters. Mandatory test: code compiles and passes full regression suite on 2+ OS/arch; modules pass ABI checks. Acceptance: Doc coverage >=90% by 'doclint v2+'; module interface passes ABI and API contract tests on 2+ OS targets. Code/doc coverage thresholds by tool and module interface test steps shall be defined.

**Quality Attributes**: Maintainability, Portability

**Measurable Criteria (if provided):** Machine-independent code for non-hardware control software; Modular design with defined interfaces; Build on 2+ OS (Windows, Linux) without code changes; Doc coverage >90%; Doc coverage >=90% by 'doclint v2+'; module interface passes ABI and API contract tests on 2+ OS targets
---

[NFR-009]: Detector Readout Performance
**Description:** For focusing and related activities, maximum acceptable detector readout time is about 0.1 sec. For mosaicked, large optical detectors, a full readout must be done in about 2 or 3 minutes. Acceptance: 99% of 100 test focus reads ≤0.1s; full readout in ≤3 min in 99% of attempts. Validation method for detector readout rates and SLOs for read failures shall be stated.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** Focusing readout: 0.1 sec; Full optical detector readout: 2-3 minutes; 99% of 100 test focus reads ≤0.1s; full readout in ≤3 min in 99% of attempts
---

[NFR-010]: System Capacity (Nodes)
**Description:** The system shall allow simultaneous operation of up to six active control nodes and up to two more monitoring nodes without appreciable degradation of performance. Computers and software shall be capable of coping with the load of 10 active nodes.

**Quality Attributes**: Scalability, Performance

**Measurable Criteria (if provided):** 6 active control nodes + 2 monitoring nodes (minimum); 10 active nodes (maximum capability)
---

[NFR-011]: Data Compression and Format
**Description:** Data may be compressed using loss-less compression for transmission. High-quality transmission must require less than 20 sec. Data transmitted between Gemini and home Institutes using FITS format. Acceptance: 100% of archived files pass FITS NOST validator, and decompress to bitwise identical original. Compression error logged. Test with checksum/hash before/after compression, FITS validator run for file format shall be specified. Acceptance: SHA256(original)==SHA256(decompressed), FITS validator 100% pass, failure alert logged within 1h. Compression/decompression round-trip must result in bitwise identical file; FITS validator tool/version shall be required; hash check for round-trip shall be added.

**Quality Attributes**: Performance, Interoperability

**Measurable Criteria (if provided):** High-quality transmission: < 20 sec; Format: FITS (NOST 100-1.0); 100% archived files pass FITS NOST validator; Decompress to bitwise identical original; SHA256(original)==SHA256(decompressed); FITS validator 100% pass; failure alert logged within 1h
---

[NFR-012]: Fault Notification and Logging
**Description:** Subsystems must notify the user when faults occur with specific origin and problem information. Notification must be capable of being electronically logged with multiple levels (detailed, verbose, short).

**Quality Attributes**: Reliability, Maintainability

**Measurable Criteria (if provided):** Multiple notification levels required; Electronic logging capability
---

[NFR-013]: Engineering Data Logging Rate
**Description:** It must be possible to log engineering data at up to 200 Hz rates for short periods. Long-term logging must be possible at slower (1 Hz or less) rates into a common format. Acceptance: 200 Hz log buffer holds ≥2 min of data, flushed on system alarm, retained ≥30 days. Max buffer size for short-term logs, min retention time, and log flush on critical faults shall be defined. Metric: log_buffer_utilization_p99, buffer flushes on 'system_alarm' event. Acceptance: In fault simulation, buffer flush confirmed; oldest kept≥30d. Owner: Logging Lead; Next action: document buffer config, flush protocol, and retention tests.

**Quality Attributes**: Performance, Maintainability

**Measurable Criteria (if provided):** Short-term logging: 200 Hz; Long-term logging: 1 Hz or less; 200 Hz log buffer holds ≥2 min of data; flushed on system alarm; retained ≥30 days; Metric: log_buffer_utilization_p99; buffer flushes on 'system_alarm' event
---

[NFR-014]: Software Version Management
**Description:** All Gemini software must be version labeled in source and binary form. Version information must be retrievable from executing software via control commands.

**Quality Attributes**: Maintainability

**Measurable Criteria (if provided):** Version labeling in source and binary; Retrieval via control commands
---

[NFR-015]: User Interface Consistency
**Description:** User interfaces for different access levels should be uniform across all subsystems, though different access levels should present different 'look-and-feels'. Similar functionality should be presented using similar user interfaces. Acceptance: All access modes use the same menu structure with <10% deviation in icon layout and color scheme, as checked by design review. UI design style guide, quantifiable consistency criteria (e.g. reuse of widgets, action layout, response time) shall be defined. Acceptance: All major UI screens pass 'ui-lint' tool with <10% style deviation; all icons button-aligned per style guide. UI style guide document shall be published; UI lint pass per screen/revision shall be required; conformity tracking by routine scan shall be implemented.

**Quality Attributes**: Usability

**Measurable Criteria (if provided):** Uniform interface philosophy across subsystems; <10% deviation in icon layout and color scheme across access modes; All major UI screens pass 'ui-lint' tool with <10% style deviation; all icons button-aligned per style guide
---

[NFR-016]: Voice Connectivity
**Description:** Voice connectivity must be available on a permanent connection. It is not a requirement that point to point video be available between Gemini operations facilities.

**Quality Attributes**: Availability

**Measurable Criteria (if provided):** Permanent voice connection required; Point-to-point video not required
---

[NFR-017]: Hardware Independence
**Description:** Microprocessor software should be hardware independent to allow later choice of target microprocessors. Computer hardware must provide compatibility in data format with identical internal data representation. Acceptance: Microprocessor-dependent modules compile and run on at least two distinct hardware targets in simulation. Hardware abstraction layer test: build and run full test suite for simulated alternate hardware platform shall be added.

**Quality Attributes**: Portability, Maintainability

**Measurable Criteria (if provided):** Hardware-independent microprocessor software; Identical internal data representation; Compile and run on 2+ distinct hardware targets in simulation
---

[NFR-018]: Concurrent Operation
**Description:** As much as possible, the system is to take advantage of parallel operation to improve efficiency. Failure of one subsystem should not affect other working subsystems.

**Quality Attributes**: Performance, Reliability

**Measurable Criteria (if provided):** Subsystem failures must not cascade to other subsystems
---