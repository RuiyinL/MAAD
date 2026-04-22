# Non-Functional Requirements Results:
[NFR-001]: Real-Time Performance
**Description:** The system shall process and output all attitude control actions within 160ms per cycle, 99.9% of cycles. Metric: control_cycle.latency.p999 (rolling 10,000 cycles); Alert: error if >160ms.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):**  160ms per cycle, 99.9% of cycles
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---

[NFR-002]: Serial Port Communication
**Description:** The system uses serial ports for communication with ground commands, gyroscope, and sun sensor.
**Quality Attributes**: Performance, Reliability
**Measurable Criteria (if provided):**  Inter-byte spacing < 5us
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** None
---

[NFR-003]: Data Accuracy
**Description:** The system ensures the accuracy of the data acquired from the gyroscope and sun sensor, with gyro/sun sensor within ±0.1 deg error, dropout < 1/100,000 samples. Acceptance: 24hr test log vs reference input, all samples within ±0.1 deg, dropout <1 per 100,000.
**Quality Attributes**: Accuracy, Reliability
**Measurable Criteria (if provided):**  ±0.1 deg error, dropout < 1/100,000 samples
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004
- **Conflicts with:** None
---

[NFR-004]: Fault Tolerance
**Description:** The system detects and recovers from component faults within 5s; failover event rate < 1/mission day. Metric: fault.failover.event_rate (1d window), Alert: critical if >1/day.
**Quality Attributes**: Reliability, Availability
**Measurable Criteria (if provided):**  5s recovery time, failover event rate < 1/mission day
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** None
---

[NFR-005]: Security
**Description:** All command and telemetry data shall be validated using HMAC; commands from ground must require cryptographic authentication; no plaintext sensitive data allowed on serial port. Acceptance: All command/telemetry exchanges log cryptographic audit entries (key id, operation, status), test with invalid HMAC fails with alert/syslog entry, plaintext never appears in wire capture.
**Quality Attributes**: Security
**Measurable Criteria (if provided):**  HMAC validation, cryptographic authentication
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---