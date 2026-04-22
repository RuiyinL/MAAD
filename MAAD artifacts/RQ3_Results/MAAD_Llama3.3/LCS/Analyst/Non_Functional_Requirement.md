# Non-Functional Requirements Results:
[NFR-001]: Performance with Automated Response Time Measurements
**Description:** Create automated response time measurements for GUI updates (<2s), sampled every 30s under normal load, with alert on 3 consecutive breaches.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** 2 seconds for GUI updates, sampled every 30 seconds

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---

[NFR-002]: Security with FIPS 180-4 Compliant Hash Function
**Description:** No MD5 shall be used anywhere. All integrity and password hash operations SHALL use a FIPS 180-4 compliant hash function (e.g., SHA-256 or better).

**Quality Attributes**: Security

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** None
---

[NFR-003]: Availability with Explicit Measurement and Reporting
**Description:** Availability shall be recorded from system heartbeat logs (MON-AVAIL-001) aggregated per calendar month and per year; breach alerts must be sent by email to SRE team and logged in SLA dashboard.

**Quality Attributes**: Availability

**Measurable Criteria (if provided):** 99.0% uptime, 10 minutes MTTR

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---

[NFR-004]: Reliability with Automated Tracking
**Description:** Reliability shall be measured by automated tracking of unscheduled system resets/reboots due to RLCS errors; a failure is reported if any component is rebooted more than once in 30 consecutive days.

**Quality Attributes**: Reliability

**Measurable Criteria (if provided):** 30 consecutive days

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---