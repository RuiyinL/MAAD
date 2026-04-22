# Functional Requirements Results:
[FR-001]: Acquire Telemetry Data
**Description**: The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude in defined XML schema. Processing retries on failure as per NFR-003. Trigger: File arrival by 01:00 UTC. If telemetry file is not acquired by 01:00 UTC, a critical alert is raised in SRE channel, and acquisition retry is logged.
**Rationale:** This requirement describes a function of the system, specifically the acquisition and processing of telemetry data.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Process Science Data
**Description**: The APAF system shall process all ASPERA-3 science data into IDFS data sets. Output: IDFS data set in XML, schema version N.N; conform to XML Schema 1.1 as per ASR-002.
**Rationale:** This requirement describes a function of the system, specifically the processing of science data into IDFS data sets.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-003]: Process Engineering and Ancillary Information
**Description**: The APAF system shall process the engineering and ancillary information necessary for calibration and science validation into IDFS data sets. Input: Ancillary data in XML format, schema version X; Output: calibrated IDFS data as XML.
**Rationale:** This requirement describes a function of the system, specifically the processing of engineering and ancillary information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-004]: Generate Intermediate Files
**Description**: Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC to support the ASPERA-3 team in meeting mission goals and objectives. Intermediate files must use schema IDFS-INT-vX.Y, include timestamp/UUID in filename and XML header.
**Rationale:** This requirement describes a function of the system, specifically the generation of intermediate files.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-005]: Store Telemetry Data
**Description**: The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing. Telemetery shall be validated with SHA-256 before writing to SwRI archive.
**Rationale:** This requirement describes a function of the system, specifically the storage of telemetry data.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-006]: Store IDFS Data Sets
**Description**: The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive for data availability and analysis. IDFS data sets shall be stored no less than 7 years on redundant disk storage and offsite backup.
**Rationale:** This requirement describes a function of the system, specifically the storage of IDFS data sets.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-007]: Provide Web-Based Displays
**Description**: Web-based displays shall support Chrome, Firefox, Safari (last 2 versions), and refresh at least every 15 minutes. Input: IDFS data (as XML) from daily pipeline. Output: HTML5 dashboard with 15-min update via AJAX/REST. Acceptance: If new IDFS data is not displayed within 20 minutes after pipeline completion, dashboard status turns red and triggers SRE alert.
**Rationale:** This requirement describes a function of the system, specifically the provision of web-based displays.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-008]: Provide Password-Protected Web Displays
**Description**: Web-based displays for science analysis shall require authentication conformant to RBAC roles (admin, ASPERA-3 Co-I, public) as defined in ASR-003, with successful and failed access attempts logged per audit and password policy NFR-002.
**Rationale:** This requirement describes a function of the system, specifically the provision of password-protected web displays.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-009]: Distribute IDFS Data Sets
**Description**: ASPERA-3 and MEX OA IDFS data sets shall be provided to all ASPERA-3 Co-I’s.
**Rationale:** This requirement describes a function of the system, specifically the distribution of IDFS data sets.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-010]: Provide IDFS Data Access Software
**Description**: IDFS data access software developed by SwRI shall be made available to the ASPERA-3 Co-I’s to support the ASPERA-3 team in meeting mission goals and objectives.
**Rationale:** This requirement describes a function of the system, specifically the provision of IDFS data access software.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-011]: Provide Science Analysis Software
**Description**: Science analysis software developed by SwRI to analyze IDFS-formatted data shall be made available to the ASPERA-3 Co-I’s to support the ASPERA-3 team in meeting mission goals and objectives. Provided IDFS input sample must yield results file matching reference CSV/JSON; software must reject invalid XML with error log entry.
**Rationale:** This requirement describes a function of the system, specifically the provision of science analysis software.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-012]: Submit IDFS Data to PDS
**Description**: ASPERA-3 IDFS data shall be provided to NASA PDS. System shall log successful submission confirmation from PDS and alert SRE of failed/missing receipts within 24 hours.
**Rationale:** This requirement describes a function of the system, specifically the submission of IDFS data to PDS.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-013]: Calibrate and Validate ASPERA-3 Data
**Description**: ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS.
**Rationale:** This requirement describes a function of the system, specifically the calibration and validation of ASPERA-3 data.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-014]: Provide IDFS Data Processing Algorithms
**Description**: SwRI shall provide IDFS data processing algorithms to IRF.
**Rationale:** This requirement describes a function of the system, specifically the provision of IDFS data processing algorithms.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-015]: Integrate Science Analysis Software
**Description**: Science analysis software shall be integrated into the NASA approved data repository.
**Rationale:** This requirement describes a function of the system, specifically the integration of science analysis software.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011
- **Conflicts with:** None