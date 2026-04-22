# Non-Functional Requirements Results

[NFR-001]: Co-I Delivery Latency
**Description:** ASPERA-3 IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I's within 24 hours of acquiring ASPERA-3 telemetry as long as the transmission and processing are error-free to support the ASPERA-3 team in meeting MEX mission goals and objectives.

**Quality Attributes**: Performance, Timeliness

**Measurable Criteria (if provided):**  Within 24 hours of acquiring telemetry.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-008, ASR-005
- **Conflicts with:** None
---

[NFR-002]: PDS Submission Latency
**Description:** ASPERA-3 data shall be provided to NASA PDS no later than 6 months after acquisition.

**Quality Attributes**: Performance, Timeliness

**Measurable Criteria (if provided):**  No later than 6 months after acquisition.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** None
---

[NFR-003]: Access Control and Security
**Description:** All non-public web-based displays and APIs shall require RBAC with unique credentials per user, minimum 12-char passwords (or SSO integration with ESA/NASA), encrypted connections (TLS 1.2+), and audit logging of all data access events, with logs retained for at least 2 years. Audit logs SHALL at minimum include {user_id, access_time, client_ip, accessed_object, action_type, result_code}. Audit logs must be write-once, cryptographically signed, and monitored for unauthorized access/deletion events.

**Quality Attributes**: Security, Confidentiality

**Measurable Criteria (if provided):**  RBAC with unique credentials; min 12-char passwords or SSO; TLS 1.2+; audit logs retained 2 years; audit logs include {user_id, access_time, client_ip, accessed_object, action_type, result_code}; write-once, cryptographically signed, monitored for unauthorized access/deletion.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, ASR-004
- **Conflicts with:** None
---

[NFR-004]: Data Integrity and Error Handling
**Description:** Data integrity shall be ensured by implementing end-to-end checksums for every file and record; error handling shall guarantee automated retries for 99% of recoverable errors within 1 hour; unrecoverable error events shall generate SRE alerts and be logged with timestamp and error code. Metric: 'batch_data_integrity_failures', measured as count per day; alert if >0 errors of type 'corruption_detected'.

**Quality Attributes**: Reliability, Data Integrity

**Measurable Criteria (if provided):**  End-to-end checksums for every file/record; 99% automated retry rate within 1 hour; SRE alerts for unrecoverable errors; daily metric 'batch_data_integrity_failures'.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-004
- **Conflicts with:** None
---

[NFR-005]: PDS Format Compliance
**Description:** ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form.

**Quality Attributes**: Compliance, Interoperability

**Measurable Criteria (if provided):**  Must adhere to NASA PDS standards.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, ASR-003
- **Conflicts with:** None
---

[NFR-006]: System Safety
**Description:** Acceptance: APAF system passes a formal safety review with documented hazard analysis and has zero unfixed high/medium safety findings before launch. Acceptance: Hazard analysis per NASA-STD-8719.13; all action items <high/medium> resolved or waived by launch safety board prior to launch.

**Quality Attributes**: Safety

**Measurable Criteria (if provided):**  Formal safety review passed; zero unfixed high/medium safety findings before launch; Hazard analysis per NASA-STD-8719.13; all action items <high/medium> resolved or waived by launch safety board prior to launch.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[NFR-007]: Usability and Documentation
**Description:** Documentation shall be considered sufficient when at least 3 representative user groups (operator, analyst, admin) can independently complete installation and a set of defined operational scenarios (start, stop, submit data, check data status) without external assistance, with <1 major clarification request per person.

**Quality Attributes**: Usability, Maintainability

**Measurable Criteria (if provided):**  3 user groups complete scenarios independently; <1 major clarification request per person.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[NFR-008]: General Quality Attributes
**Description:** The system shall have >99.5% uptime during mission ops phase (excluding scheduled maintenance), successful data reprocessing of historical records must complete within 6 hours, and all components must be installable on at least two supported OS environments without source changes. Metrics: 'apaf_uptime' (prometheus gauge), tracked 24x7; alert if below 99.5% over trailing 30d; 'apaf_hist_reprocessing_duration', alert if >6h on any run.

**Quality Attributes**: Reliability, Maintainability, Availability, Flexibility, Portability, Testability, Usability

**Measurable Criteria (if provided):**  >99.5% uptime; reprocessing within 6 hours; installable on 2+ OS environments without source changes; 'apaf_uptime' metric tracked 24x7 with alert <99.5% trailing 30d; 'apaf_hist_reprocessing_duration' alert >6h.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---