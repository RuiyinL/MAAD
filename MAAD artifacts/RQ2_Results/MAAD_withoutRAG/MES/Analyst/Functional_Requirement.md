# Functional Requirements Results

[FR-001]: Acquire ASPERA-3 and Mars Express Orbit/Attitude telemetry from ESOC
**Description**: The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude to automatically process the data on a daily basis.

**Rationale:** Describes a required system behavior (data ingestion from an external source).

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002
- **Conflicts with:** NFR-003
---

[FR-002]: Automatically process telemetry daily
**Description**: The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude to automatically process the data on a daily basis.

**Rationale:** Specifies an operational behavior (scheduled/automated processing).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-002, NFR-003
- **Conflicts with:** NFR-006
---

[FR-003]: Process ASPERA-3 science data into IDFS datasets
**Description**: The APAF system shall process all ASPERA-3 science data into IDFS data sets. Processed IDFS data sets shall be valid against IDFS schema vX.Y and verified using the [validator-tool]. (Owner: Not specified; Next action: Add IDFS format/detail/canonical schema.)

**Rationale:** Defines a core transformation function producing a defined product.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** NFR-003
---

[FR-004]: Process engineering and ancillary information into IDFS datasets
**Description**: The APAF system shall process the engineering and ancillary information necessary for calibration and science validation into IDFS data sets.

**Rationale:** Defines required processing outputs supporting calibration/validation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** NFR-003
---

[FR-005]: Generate intermediate cleaned-up telemetry files when ESOC cleaned telemetry is not provided
**Description**: Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC to support the ASPERA-3 team in meeting mission goals and objectives.

**Rationale:** Specifies conditional system behavior and artifact generation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** NFR-003
---

[FR-006]: Store raw telemetry on local SwRI archive
**Description**: The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing.

**Rationale:** Defines required data retention/storage behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-007
- **Conflicts with:** NFR-003
---

[FR-007]: Store IDFS datasets on local SwRI archive
**Description**: The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive for data availability and analysis.

**Rationale:** Defines required storage of processed outputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, NFR-007
- **Conflicts with:** NFR-003
---

[FR-008]: Store APAF-generated intermediate cleaned telemetry files on local SwRI archive
**Description**: Any APAF-generated intermediate files of ASPERA-3 and MEX OA cleaned-up telemetry shall be stored on a local SwRI archive for data availability and re-processing, and to support the ASPERA-3 team.

**Rationale:** Defines required storage for generated intermediate artifacts.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-007
- **Conflicts with:** NFR-003
---

[FR-009]: Provide public web-based displays of most current ASPERA-3 data
**Description**: Web-based displays of the most current ASPERA-3 data shall be provided for public view to monitor instrument performance.

**Rationale:** Defines a user-facing capability (web display of current data).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-002
- **Conflicts with:** FR-011, NFR-004
---

[FR-010]: Provide ASPERA-3 team-defined web displays for science analysis using any available data
**Description**: Web-based displays defined by ASPERA-3 team shall be provided where any available ASPERA-3 data (as opposed to just the most current) can be used for science analysis to support the ASPERA-3 team in meeting mission goals and objectives. Team web displays may show ASPERA-3 data of types A, B, and C; embargoed files F and G must not be exposed. (Owner: Not specified; Next action: Clarify dataset types and restrictions.)

**Rationale:** Defines additional web functionality and data access scope.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-007, NFR-002
- **Conflicts with:** NFR-004
---

[FR-011]: Password-protect science-analysis web displays until data is public
**Description**: The web-based displays defined by the ASPERA-3 team to be used for science analysis shall be password protected until the ASPERA-3 data is made public to support the ASPERA-3 team in meeting mission goals and objectives.

**Rationale:** Specifies a system behavior related to access control for a function (restricted viewing).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-004
- **Conflicts with:** FR-009
---

[FR-012]: Provide built-in error handling
**Description**: The APAF ground data system shall have built-in error handling for better data integrity. System shall detect and log ingestion failures, processing errors, and storage failures; recovery procedures must be tested for each error type annually. (Owner: Not specified; Next action: Add error lists, detection points, and test evidence.)

**Rationale:** Requires the system to perform error handling (a behavior), even though the quality intent is integrity.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008
- **Conflicts with:** NFR-003
---

[FR-013]: Provide IDFS data and intermediate cleaned telemetry files to all ASPERA-3 Co-I’s
**Description**: ASPERA-3 and MEX OA IDFS data and any APAF-generated intermediate files of ASPERA-3 and MEX OA cleaned-up telemetry shall be provided to all ASPERA-3 Co-I’s.

**Rationale:** Defines a distribution function to specified recipients.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, FR-005, NFR-002
- **Conflicts with:** NFR-004
---

[FR-014]: Make IDFS data access software available to Co-I’s
**Description**: IDFS data access software developed by SwRI shall be made available to the ASPERA-3 Co-I’s to support the ASPERA-3 team in meeting mission goals and objectives.

**Rationale:** Defines a delivery/provisioning function for software artifacts.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013
- **Conflicts with:** NFR-004
---

[FR-015]: Make science analysis software available to Co-I’s
**Description**: Science analysis software developed by SwRI to analyze IDFS-formatted data shall be made available to the ASPERA-3 Co-I’s to support the ASPERA-3 team in meeting mission goals and objectives.

**Rationale:** Defines a delivery/provisioning function for analysis tooling.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013
- **Conflicts with:** NFR-004
---

[FR-016]: Provide ASPERA-3 and MEX OA IDFS data to NASA PDS
**Description**: ASPERA-3 IDFS data and MEX OA IDFS data shall be provided to NASA PDS.

**Rationale:** Defines an external submission/distribution function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, NFR-002
- **Conflicts with:** NFR-003
---

[FR-017]: Provide ASPERA-3 data to NASA PDS in PDS-compliant form
**Description**: ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form. The system shall package PDS data in compliance with PDS4 version X.Y, as validated by [tool], with evidence stored in the delivery record. (Owner: Not specified; Next action: Update with measurable PDS compliance target.)

**Rationale:** Defines required output formatting for an external interface.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, NFR-001
- **Conflicts with:** NFR-003
---

[FR-018]: Calibrate and validate ASPERA-3 data prior to PDS deposit
**Description**: ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS.

**Rationale:** Specifies required processing steps before submission.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, FR-016
- **Conflicts with:** NFR-003
---

[FR-019]: Provide IDFS data processing algorithms to IRF
**Description**: SwRI shall provide IDFS data processing algorithms to IRF.

**Rationale:** Defines provision/delivery of algorithms to an external party.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004
- **Conflicts with:** NFR-008
---

[FR-020]: Integrate science analysis software into NASA-approved data repository
**Description**: Science analysis software shall be integrated into the NASA approved data repository.

**Rationale:** Defines an integration function with an external repository.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-015
- **Conflicts with:** NFR-008
---

[FR-021]: Provide system maintenance for APAF
**Description**: The SwRI software team shall provide system maintenance and software support. / SwRI shall provide APAF system maintenance. SwRI shall provide maintenance and support with 8x5 coverage, response to critical issues within 4 hours, and resolution within 48 hours. (Owner: Not specified; Next action: Define support SLAs and escalation.)

**Rationale:** Specifies an operational/support activity required for the system lifecycle.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005
- **Conflicts with:** NFR-006
---

[FR-022]: Provide software support for the APAF system
**Description**: SwRI shall provide software support for the APAF system. Software support shall be provided via ticketing system; non-critical tickets answered within 2 business days. (Owner: Not specified; Next action: Define software support SLA.)

**Rationale:** Specifies required support function during operations.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005
- **Conflicts with:** NFR-006
---

[FR-023]: Assign project-unique identifiers to requirements
**Description**: Each requirement shall be: assigned a project-unique identifier.

**Rationale:** Defines a required process/task for requirements management.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-009
- **Conflicts with:** None specified
---