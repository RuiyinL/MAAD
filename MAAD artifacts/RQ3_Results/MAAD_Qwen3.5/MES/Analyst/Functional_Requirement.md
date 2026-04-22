# Functional Requirements Results

[FR-001]: Telemetry Acquisition
**Description**: The APAF system shall acquire from ESOC telemetry conforming to [reference schema], rejecting and alerting on malformatted batches; acceptance: simulate 3 types of data errors and verify alert/exception within 1h.

**Rationale:**  This requirement is functional because it describes a specific input action (acquiring telemetry) and a trigger condition (daily basis) that the system must perform.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, ASR-001
- **Conflicts with:** None
---

[FR-002]: Science Data Processing
**Description**: The APAF system shall process all ASPERA-3 science data into IDFS data sets. Each processed batch must conform to the IDFS schema vX.Y; 100% of files pass validation gate; acceptance: run 10 known-good/known-bad sample files.

**Rationale:**  This requirement is functional because it defines a transformation task (processing science data) and a specific output format (IDFS data sets).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, ASR-003
- **Conflicts with:** None
---

[FR-003]: Engineering and Ancillary Data Processing
**Description**: The APAF system shall process the engineering and ancillary information necessary for calibration and science validation into IDFS data sets.

**Rationale:**  This requirement is functional because it specifies the processing of specific data types (engineering/ancillary) into a defined output (IDFS).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-011
- **Conflicts with:** None
---

[FR-004]: Intermediate File Generation
**Description**: Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC to support the ASPERA-3 team in meeting mission goals and objectives.

**Rationale:**  This requirement is functional because it describes a conditional behavior (generation of files) based on an external input condition (ESOC provision).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---

[FR-005a]: Telemetry Data Archiving
**Description**: The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing.

**Rationale:**  This requirement is functional because it mandates specific storage actions for telemetry data on a specific target (local SwRI archive). Derived from FR-005.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None
---

[FR-005b]: IDFS Data Sets Archiving
**Description**: The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive for data availability and analysis.

**Rationale:**  This requirement is functional because it mandates specific storage actions for IDFS data sets on a specific target (local SwRI archive). Derived from FR-005.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None
---

[FR-005c]: Intermediate Files Archiving
**Description**: All APAF-generated intermediate files shall be stored on a local SwRI archive for data availability and re-processing.

**Rationale:**  This requirement is functional because it mandates specific storage actions for intermediate files on a specific target (local SwRI archive). Derived from FR-005.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002
- **Conflicts with:** None
---

[FR-006]: Public Web Display
**Description**: Web-based displays of the most current ASPERA-3 data shall be provided for public view to monitor instrument performance. Public web display refreshes every 5 minutes, max server-to-browser latency 30 seconds; only non-restricted data displayed, evidence: public access log with fields checked for PII/sensitive info.

**Rationale:**  This requirement is functional because it specifies the creation of a user interface feature (web display) for a specific audience (public) and data scope (most current).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, ASR-004
- **Conflicts with:** None
---

[FR-007]: Team Science Web Display
**Description**: Web-based displays defined by ASPERA-3 team shall be provided where any available ASPERA-3 data (as opposed to just the most current) can be used for science analysis to support the ASPERA-3 team in meeting mission goals and objectives. Acceptance: List of required displays is frozen at system design review; API contract for team displays documented.

**Rationale:**  This requirement is functional because it defines a specific system capability (web display) with different data access rules (any available data) for a specific user group (ASPERA-3 team).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, ASR-004
- **Conflicts with:** None
---

[FR-008]: Data Distribution to Co-I's
**Description**: ASPERA-3 and MEX OA IDFS data and any APAF-generated intermediate files of ASPERA-3 and MEX OA cleaned-up telemetry shall be provided to all ASPERA-3 Co-I's.

**Rationale:**  This requirement is functional because it describes a distribution action (providing data) to specific recipients (Co-I's).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-004, NFR-001
- **Conflicts with:** None
---

[FR-009a]: IDFS Data Access Software Distribution
**Description**: IDFS data access software shall be made available to the ASPERA-3 Co-I's.

**Rationale:**  This requirement is functional because it mandates the delivery of specific software artifacts (IDFS access) to users. Derived from FR-009.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---

[FR-009b]: Science Analysis Software Distribution
**Description**: Science analysis software shall be made available to the ASPERA-3 Co-I's.

**Rationale:**  This requirement is functional because it mandates the delivery of specific software artifacts (Science analysis) to users. Derived from FR-009.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---

[FR-010]: PDS Data Submission
**Description**: ASPERA-3 IDFS data and MEX OA IDFS data shall be provided to NASA PDS. ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form.

**Rationale:**  This requirement is functional because it specifies an external handoff action (submission to PDS) with a format constraint.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-005, ASR-003
- **Conflicts with:** None
---

[FR-011]: Data Calibration and Validation
**Description**: ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS. Upon processing, all calibration steps conform to NASA PDS Standard X.Y; validator run returns 0 critical errors; acceptance: review validation log per dataset.

**Rationale:**  This requirement is functional because it defines a processing step (calibration/validation) that must occur before a specific event (PDS deposit).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-010
- **Conflicts with:** None
---

[FR-012]: Algorithm Provision to IRF
**Description**: SwRI shall provide IDFS data processing algorithms to IRF. Acceptance: SwRI provides full source, binaries, and usage documentation by <YYYY-MM-DD>, acknowledged as received by IRF.

**Rationale:**  This requirement is functional because it describes a deliverable action (providing algorithms) to an external entity (IRF).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---