# Non-Functional Requirements Results:
[NFR-001]: Performance
**Description:** The system shall process all incoming configuration/control events within 10ms, with 99.99% of events processed within this threshold.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 10ms, 99.99%
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-002]: Reliability
**Description:** The system shall have an MTBF of at least 1 year, and never lose more than 0.5% of configuration/control events during external comms failure.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):** MTBF of at least 1 year, 0.5% event loss
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003
- **Conflicts with:** None
---
[NFR-003]: Availability
**Description:** Outages are defined as loss of all core M&C services, measured via continuous ping/heartbeat; incidents are logged and reported in the monthly availability report.
**Quality Attributes**: Availability
**Measurable Criteria (if provided):** Outage definition, measurement, and reporting
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-013
- **Conflicts with:** None
---
[NFR-004]: Security
**Description:** Logs exported in JSON Schema vN [link] to SIEM [list], by hourly batch. mTLS must meet RFC 8705 (https://datatracker.ietf.org/doc/rfc8705/). Retention/rotation policy per NFR-004 supersedes FR log statements.
**Quality Attributes**: Security
**Measurable Criteria (if provided):** JSON Schema, SIEM, mTLS, RFC 8705
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, FR-015
- **Conflicts with:** None
---
[NFR-005]: Maintainability
**Description:** Mean time to replace (MTTR) for field-swappable hardware shall not exceed 15 minutes.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):** MTTR of 15 minutes
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011
- **Conflicts with:** None
---
[NFR-006]: Scalability
**Description:** System shall scale to accommodate 200% of 2024 baseline data volume without architectural change.
**Quality Attributes**: Scalability
**Measurable Criteria (if provided):** 200% of 2024 baseline data volume
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-007]: Usability
**Description:** Usability test shall be performed with ≥10 target end users, requiring SUS score of 80+ prior to go-live.
**Quality Attributes**: Usability
**Measurable Criteria (if provided):** System Usability Scale score of 80+
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-012
- **Conflicts with:** None
---