# Non-Functional Requirements Results:

[NFR-001]: System Performance and Latency
**Description:** Displays of environmental conditions shall be updated at least every two seconds. Sensor data shall have a minimum data acquisition rate of 10 Hz. ENV_DISPLAY_UPDATE_LATENCY (time between sensor value change and display) must be ≤2 seconds at the 95th percentile, measured hourly; automated tests must simulate sensor churn and log update timings. Display update latency must be logged (METRIC_ENV_DISPLAY_UPDATE_LATENCY) every minute; alert fired if 95th percentile >2s for 3 consecutive hours. Next action: Document monitoring points, log format, and alert logic for latency metrics.
**Quality Attributes**: Performance, Responsiveness
**Measurable Criteria (if provided):** ENV_DISPLAY_UPDATE_LATENCY p95 ≤ 2 seconds (measured hourly); Sensor acquisition >= 10 Hz; METRIC_ENV_DISPLAY_UPDATE_LATENCY logged every minute; Alert if p95>2s for 3 consecutive hours.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Communication Architecture)
- **Conflicts with:** None identified
---

[NFR-002]: System Reliability
**Description:** The DigitalHome System must be highly reliable with no more than 1 failure per 10,000 hours of operation. Reliability shall be measured as the number of unscheduled complete system outages (any loss of control or monitoring for >10 seconds) per 10,000 hours of planned uptime; system logs must record all such events for SRE review. Acceptance: List of allowed and disallowed system states; complete outage defined as any >10s loss of telemetry or control confirmed by heartbeat. Next action: Define system states and failure escalation process.
**Quality Attributes**: Reliability, Availability
**Measurable Criteria (if provided):** MTBF >= 10,000 hours (unscheduled outages >10s loss of control/monitoring <= 1 per 10,000 hours); Outage defined as >10s loss of telemetry/control confirmed by heartbeat.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Backup/Recovery)
- **Conflicts with:** None identified
---

[NFR-003]: Security and Encryption
**Description:** The DigitalHome web system shall provide for authentication and information encryption through a recognized reliable and effective security technology, such as Transport Layer Security (TLS). All authentication shall use at least TLS 1.3; user secrets must be hashed/salted at rest using bcrypt or stronger; the system must enforce password length ≥12, track failed login attempts, and log authentication actions. Audit logs must track: timestamp, userID, IP, action taken. Retention: 1 year. Lock account for 10 mins after 5 failed attempts. Acceptance: User PII will be deleted from all storage within 30 days of account closure. Deletion logged with user_id and timestamp. Next action: Define PII deletion SLO/SLA and data privacy statement.
**Quality Attributes**: Security, Confidentiality, Integrity
**Measurable Criteria (if provided):** TLS 1.3 minimum; bcrypt or stronger for secrets; Password length ≥12; Failed login tracking; Auth action logging; Audit logs (timestamp, userID, IP, action) retained 1 year; Lockout 10 mins after 5 failed attempts; PII deleted within 30 days of account closure; deletion logged with user_id and timestamp.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Authentication)
- **Conflicts with:** None identified
---

[NFR-004]: Usability and User Interface
**Description:** The general user shall be able to use the system capabilities via a web interface. The user shall be able to perform simple web operations (logging in, browsing, submitting requests). Task completion time for standard usage flows ≤ 60 seconds at 95th percentile for new users; all pages WCAG 2.1 AA compliant. Acceptance: Web UI must pass WCAG 2.1 AA automated checks for login, dashboard, and device control flows. Known gaps documented by issue ID. Next action: Specify scope/coverage of accessibility compliance.
**Quality Attributes**: Usability, Accessibility
**Measurable Criteria (if provided):** Web-based interface; supports standard web operations; Task completion time ≤ 60s p95; WCAG 2.1 AA for login, dashboard, device control flows; known gaps documented.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Web Server Architecture)
- **Conflicts with:** None identified
---

[NFR-005]: Maintainability and Documentation
**Description:** All system documents (SRS, ADS, Source Code, Test Plans) shall be up-to-date, use the HomeOwner document format [HO2305] and reside in the HomeOwner Document Archive. Development shall use object-oriented methods and UML 2.0. Project documentation must be reviewed for completeness and accuracy every sprint; all diagrams must use UML 2.0; all SRS/ADS updates delivered to Document Archive within 5 days of approval. Acceptance: Documentation is reviewed against a checklist for completeness and correctness at every sprint-end meeting; owner and reviewer noted; signoff logged. Next action: Define docs review SOP.
**Quality Attributes**: Maintainability, Compliance
**Measurable Criteria (if provided):** Adherence to HO2305 format; Use of UML 2.0; Sprint review cycle; Updates within 5 days of approval; Sprint-end checklist review with signoff.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Development Standards)
- **Conflicts with:** None identified
---

[NFR-006]: Compatibility and Standards
**Description:** The system shall be compatible with centralized HVAC systems (gas, oil, electricity, solar). The system shall adhere to ASHRAE 2010 standards, policies, and procedures. Acceptance: Interop test run with gas, oil, electric and solar HVAC simulators; ASHRAE test report archived. Next action: Document standards compliance and test plan.
**Quality Attributes**: Interoperability, Compliance
**Measurable Criteria (if provided):** ASHRAE 2010 compliance; Support for multiple HVAC types; Interop test with simulators; ASHRAE test report archived.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002 (Temperature Control)
- **Conflicts with:** None identified
---

[NFR-007]: Cost and Schedule Constraints
**Description:** The prototype version must be completed within twelve months. The cost of DigitalHome elements should be minimized.
**Quality Attributes**: Cost, Schedulability
**Measurable Criteria (if provided):** Duration <= 12 months; Cost minimized.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Development Standards)
- **Conflicts with:** None identified
---