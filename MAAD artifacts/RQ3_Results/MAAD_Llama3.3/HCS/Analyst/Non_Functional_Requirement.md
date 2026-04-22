# Non-Functional Requirements Results:
[NFR-001]: System Reliability
**Description:** The DigitalHome System must be highly reliable with no more than 1 failure per 10,000 hours of operation.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):** 1 failure per 10,000 hours
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-002]: System Performance
**Description:** Displays: update device status panels (temperature, humidity, security, appliances) for all configured devices within 2s of state change; tested with 100 appliances under 10Mbps download/2Mbps upload WAN; alert SRE if p99 latency >2s for >5min.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 2 seconds
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-003]: Data Acquisition Rate
**Description:** If mean(sensor_acquisition_rate_hz) <10 for 60s on any configured sensor, issue P1 incident to SRE via PagerDuty.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 10 Hz
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-004]: Security
**Description:** Acceptance: 100% of network connections involving user data are logged with protocol details; automated audit scripts must confirm TLS1.3+ within 24h of new release; failure to meet triggers P0 security incident.
**Quality Attributes**: Security
**Measurable Criteria (if provided):** Not specified
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-005]: System Availability
**Description:** The system shall have 99.9% uptime per calendar month, excluding up to 4 hours/month for planned maintenance.
**Quality Attributes**: Availability
**Measurable Criteria (if provided):** 99.9% uptime
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-006]: System Maintainability
**Description:** Define: Critical defect = S1 outage/data loss; all modules >80% code coverage via CI; S1 restoration verified <8 hours.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):** 8 hours
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---