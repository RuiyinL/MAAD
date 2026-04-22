# Non-Functional Requirements Results:
[NFR-001]: Daily Automated Processing
**Description:** Telemetry data processing must begin by 01:00 UTC and complete by 12:00 UTC each day.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** Daily, 01:00-12:00 UTC
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[NFR-002]: Password Protection
**Description:** Password storage shall use bcrypt (cost>=10); passwords must be changed at least every 180 days; previous 5 passwords may not be reused.
**Quality Attributes**: Security
**Measurable Criteria (if provided):** Password length: 12 characters, account lockout: 5 attempts
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** None
---
[NFR-003]: Error Handling
**Description:** The APAF system shall detect and log 100% of failed data processing events, provide retry at least 3 times, and flag any data loss over 0.01%.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):** 100% detection, 3 retries, 0.01% data loss threshold
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[NFR-004]: Data Integrity
**Description:** Intermediate files shall be validated with SHA-256 hash on storage, and backups scheduled daily; RPO (Recovery Point Objective) < 24 hours. Acceptance: System flags failed SHA-256 check on intermediate file, auto-alert to SRE if detected in daily window.
**Quality Attributes**: Data Integrity
**Measurable Criteria (if provided):** SHA-256 hash, daily backups, RPO < 24 hours
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** None
---
[NFR-005]: 24-Hour Distribution
**Description:** ASPERA-3 IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ASPERA-3 telemetry.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 24 hours
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[NFR-006]: PDS Compliance
**Description:** All ASPERA-3 data shall be compliant to NASA PDS4 and pass the PDS4 validator.
**Quality Attributes**: Compliance
**Measurable Criteria (if provided):** NASA PDS4 compliance
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** None
---
[NFR-007]: Six-Month Submission
**Description:** ASPERA-3 data shall be provided to NASA PDS no later than 6 months after acquisition.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 6 months
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** None
---
[NFR-008]: System Maintenance
**Description:** Critical issue = functionality loss or data corruption; notification to SRE on PagerDuty within 2 business days.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):** 2 business days, monthly preventive maintenance
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None