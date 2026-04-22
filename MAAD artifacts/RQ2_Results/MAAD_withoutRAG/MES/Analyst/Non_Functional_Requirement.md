# Non-Functional Requirements Results

[NFR-001]: Conformance to IDFS and PDS product standards
**Description:** These data products will be put into a form known as the Instrument Data File Set (IDFS). / The APAF system shall process all ASPERA-3 science data into IDFS data sets. / ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form. The system shall generate IDFS datasets that pass validation using IDFS schema version X.Y and PDS datasets that pass the official PDS4 validator; compliance certified via acceptance test protocol documented in APAF Verification Plan. (Owner: Not specified; Next action: Specify schema, version, and validation process for both IDFS and PDS output.)

**Quality Attributes**: Compliance/Standards, Interoperability

**Measurable Criteria (if provided):** IDFS schema version X.Y validation pass; PDS4 validator pass; certification via APAF Verification Plan acceptance test protocol.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, FR-016, FR-017
- **Conflicts with:** NFR-003
---

[NFR-002]: Use NISN/ESOC telemetry acquisition path (external communication constraint)
**Description:** The APAF data system acquires the telemetry data via NISN. / The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude...

**Quality Attributes**: Interoperability, Operational Constraint

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None specified
---

[NFR-003]: Data integrity emphasis (via error handling and “error-free” processing assumptions)
**Description:** The APAF ground data system shall have built-in error handling for better data integrity. / (Delivery timelines apply) as long as the transmission and processing are error-free... Delivery is considered 'error-free' if data products match input telemetry checksums, all records pass schema validation, and error logs show zero processing errors for a data batch. (Owner: Not specified; Next action: Define precise error and integrity acceptance bounds and monitoring/alerting approach.)

**Quality Attributes**: Integrity, Reliability

**Measurable Criteria (if provided):** Data products match input telemetry checksums; all records pass schema validation; zero processing errors in error logs for a data batch.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** NFR-010, NFR-011
---

[NFR-004]: Privacy/security—password protection for appropriate web access
**Description:** The APAF system web server shall be password protected where appropriate to allow only pertinent ASPERA-3 team members access. / The web-based displays ... used for science analysis shall be password protected until the ASPERA-3 data is made public... All restricted web resources shall require password authentication (min 12 characters, complexity enforced, rotated quarterly); all accesses logged with user ID/timestamp; admin and Co-I roles enforced. (Owner: Not specified; Next action: Define and document access controls and logging policy for the web and data APIs.)

**Quality Attributes**: Security, Privacy, Access Control

**Measurable Criteria (if provided):** Minimum password length 12 characters; complexity enforced; rotation quarterly; access logging includes user ID and timestamp; role enforcement for admin and Co-I.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011
- **Conflicts with:** FR-009
---

[NFR-005]: Maintainability/Supportability via maintenance and software support
**Description:** The SwRI software team shall provide system maintenance and software support. / SwRI shall provide APAF system maintenance. / SwRI shall provide software support for the APAF system.

**Quality Attributes**: Maintainability, Supportability

**Measurable Criteria (if provided):** Not specified (no support hours, response times, or SLAs).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, FR-022
- **Conflicts with:** None specified
---

[NFR-006]: Usability/training constraint—no training-related requirements due to sufficient procedures
**Description:** The APAF Operations Procedures Document shall provide installation and operations procedures of the APAF system in enough detail where there are no training-related requirements for users and operators of the APAF data system.

**Quality Attributes**: Usability, Operability/Documentation

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, FR-022
- **Conflicts with:** FR-002 (automation may still require operator knowledge)
---

[NFR-007]: Local archival for availability and re-processing
**Description:** The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing. / (Similarly for) IDFS data sets and intermediate files... for data availability...

**Quality Attributes**: Availability, Recoverability, Data Retention

**Measurable Criteria (if provided):** Not specified (no retention duration, RPO/RTO, capacity).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008
- **Conflicts with:** None specified
---

[NFR-008]: Internal interface and internal data requirements deferred to design documentation
**Description:** All internal interfaces are left to the design. / The Software Design Documents of each of the seven components shall contain the detailed information of the internal interfaces. / All internal data requirements are left to the design. / The Software Design Documents ... shall contain the detailed information of the virtual instrument data items.

**Quality Attributes**: Modifiability (constraint on specification), Architectural Constraint/Documentation

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004 (processing requires internal interfaces/data)
- **Conflicts with:** NFR-009 (traceability/identification vs deferred details)
---

[NFR-009]: Requirements governance—unique identifiers for each requirement
**Description:** Each requirement shall be: assigned a project-unique identifier.

**Quality Attributes**: Process/Traceability (constraint)

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-023
- **Conflicts with:** None specified
---

[NFR-010]: Co-I distribution timeliness—IDFS within 24 hours (ASPERA-3)
**Description:** ASPERA-3 IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ASPERA-3 telemetry as long as the transmission and processing are error-free... IDFS data shall be delivered to each Co-I within 24 hours of telemetry acquisition as measured by system logs; if delivery is delayed, alert generated within 30 minutes of missed deadline. (Owner: Not specified; Next action: Define metric and monitoring required for SLO, and failure notification path.)

**Quality Attributes**: Performance (Timeliness), Service Level

**Measurable Criteria (if provided):** Delivered within 24 hours of telemetry acquisition, measured by system logs; alert within 30 minutes of missed deadline.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003, FR-013
- **Conflicts with:** NFR-003
---

[NFR-011]: Co-I distribution timeliness—IDFS within 24 hours (MEX OA)
**Description:** MEX OA IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring MEX OA telemetry as long as the transmission and processing are error-free... MEX OA IDFS data shall be delivered to each Co-I within 24 hours of telemetry acquisition; system must log and report any missed SLAs. (Owner: Not specified; Next action: Update with measurable, monitorable SLO definition.)

**Quality Attributes**: Performance (Timeliness), Service Level

**Measurable Criteria (if provided):** Delivered within 24 hours of telemetry acquisition; system logs and reports missed SLAs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-004, FR-013
- **Conflicts with:** NFR-003
---

[NFR-012]: Co-I distribution timeliness—intermediate cleaned telemetry within 24 hours
**Description:** Any APAF-generated intermediate files ... that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ASPERA-3 and MEX OA telemetry as long as the transmission and processing are error-free... If error prevents delivery within 24h, the system shall alert stakeholders within 1h, retry delivery up to 3 times, and escalate to SRE if undelivered after 48h. (Owner: Not specified; Next action: Add operational process for retry/error and notification.)

**Quality Attributes**: Performance (Timeliness), Service Level

**Measurable Criteria (if provided):** Delivered within 24 hours; if not, alert within 1 hour; retry up to 3 times; escalate if undelivered after 48 hours.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-005, FR-013
- **Conflicts with:** NFR-003
---

[NFR-013]: PDS submission deadline—within 6 months after acquisition
**Description:** ASPERA-3 data shall be provided to NASA PDS no later than 6 months after acquisition. / ...validation and archiving ... in the NASA Planetary Data System (PDS) within 6 months of receipt... The APAF system shall deliver validated PDS-compliant data to NASA within 6 calendar months of initial ground receipt, as time-stamped in system logs; any risk of overrun shall alert project owner 1 month in advance. (Owner: Not specified; Next action: Clarify milestone trigger and deadline measurement.)

**Quality Attributes**: Timeliness, Compliance/Operational Constraint

**Measurable Criteria (if provided):** Within 6 calendar months of initial ground receipt (time-stamped in system logs); alert project owner 1 month in advance of risk of overrun.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017, FR-018
- **Conflicts with:** NFR-003
---

[NFR-014]: Safety—system shall not impose hazards
**Description:** The APAF data system will not impose hazards to personnel, property, or the environment.

**Quality Attributes**: Safety

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-021 (operations/maintenance)
- **Conflicts with:** None specified
---

[NFR-015]: Considered software quality factors (non-binding qualities to be considered)
**Description:** Some of the software quality factors that will be considered when developing the APAF data system include: reliability, maintainability, availability, flexibility, portability, testability, and usability.

**Quality Attributes**: Reliability, Maintainability, Availability, Flexibility, Portability, Testability, Usability

**Measurable Criteria (if provided):** Not specified.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, FR-022
- **Conflicts with:** None specified
---