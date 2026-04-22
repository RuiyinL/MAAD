# Functional Requirements Results

[FR-001]: Acquire ASPERA-3 and Mars Express Orbit/Attitude telemetry from ESOC  
**Description**: “The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude to automatically process the data on a daily basis.” Updated per evaluator: “ESOC telemetry shall be acquired via [protocol X, format Y], with a retry policy for connection loss (max 5 attempts in 10 minutes); delivery of daily files in [formatName vZ].” (Next action: Define interface specification for ESOC telemetry acquisition.)  
**Rationale:** Describes a concrete system behavior (telemetry acquisition) and its operational cadence.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** Not identified  
---

[FR-002]: Process ASPERA-3 science telemetry into IDFS datasets  
**Description**: “The APAF system shall process all ASPERA-3 science data into IDFS data sets.” Updated per evaluator: “IDFS datasets produced must conform to IDFS schema vX.Y (document ref/link), validated on every output.” (Next action: Attach or reference strict IDFS schema.)  
**Rationale:** Defines a required transformation function from telemetry to a specified product format (IDFS).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** Not identified  
---

[FR-003]: Process engineering and ancillary data into IDFS datasets  
**Description**: “The APAF system shall process the engineering and ancillary information necessary for calibration and science validation into IDFS data sets.” Updated per evaluator: “Calibration step for engineering data must result in an absolute error <2% as per section 4.2.1 of [Engineering Data Guide v3.4].” (Next action: Attach or link data quality and calibration/validation acceptance reference.)  
**Rationale:** Specifies required processing of non-science telemetry/metadata into deliverable datasets.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** Not identified  
---

[FR-004]: Generate intermediate cleaned-up telemetry files when ESOC does not provide them  
**Description**: “Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC…” Updated per evaluator: “If ESOC telemetry in [cleaned-up format] is not available by 02:00 UTC, trigger local cleaning; output must conform to schema [link-to-schema].” (Next action: Draft the input check/handshake process and produce a schema stub or reference.)  
**Rationale:** Defines conditional system behavior to produce intermediate artifacts supporting downstream use.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** Not identified  
---

[FR-005]: Store raw telemetry on local SwRI archive  
**Description**: “The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing.”  
**Rationale:** Specifies a required data storage function for later access and reprocessing.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** Not identified  
---

[FR-006]: Store IDFS datasets on local SwRI archive  
**Description**: “The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive for data availability and analysis.”  
**Rationale:** Defines required persistence of produced datasets for analysis and access.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** Not identified  
---

[FR-007]: Store intermediate cleaned-up telemetry files on local SwRI archive  
**Description**: “Any APAF-generated intermediate files of ASPERA-3 and MEX OA cleaned-up telemetry shall be stored on a local SwRI archive…”  
**Rationale:** Requires persistence of intermediate products to support reprocessing and team needs.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** Not identified  
---

[FR-008]: Provide public web-based displays of most current ASPERA-3 data  
**Description**: “Web-based displays of the most current ASPERA-3 data shall be provided for public view to monitor instrument performance.” Updated per evaluator: “Public web display must refresh with new data <15min after telemetry ingestion; failure triggers operator alert.” (Next action: Attach measurable refresh/latency and display content specs.)  
**Rationale:** Specifies a user-facing function (web display) and its content scope (most current data).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** Not identified  
---

[FR-009]: Provide team-defined web displays for science analysis using any available data  
**Description**: “Web-based displays defined by ASPERA-3 team shall be provided where any available ASPERA-3 data… can be used for science analysis…”  
**Rationale:** Defines a configurable display capability supporting analysis over historical/available data.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** Not identified  
---

[FR-010]: Distribute IDFS data and intermediate files to all ASPERA-3 Co-Is  
**Description**: “ASPERA-3 and MEX OA IDFS data and any APAF-generated intermediate files… shall be provided to all ASPERA-3 Co-I’s.”  
**Rationale:** Specifies a distribution function to a defined recipient group.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007
- **Conflicts with:** Not identified  
---

[FR-011]: Provide IDFS data access software to ASPERA-3 Co-Is  
**Description**: “IDFS data access software developed by SwRI shall be made available to the ASPERA-3 Co-I’s…” Updated per evaluator: “Acceptance: signed confirmation by at least 2 Co-Is that software installs, operates, and passes supplied test scripts on OS X.Y and Linux Z platforms.” (Next action: Develop a user story matrix and readiness checklist document for handoff.)  
**Rationale:** Requires delivery/provisioning of a software capability to users.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** Not identified  
---

[FR-012]: Provide science analysis software for IDFS-formatted data to ASPERA-3 Co-Is  
**Description**: “Science analysis software developed by SwRI to analyze IDFS-formatted data shall be made available to the ASPERA-3 Co-I’s…”  
**Rationale:** Requires provisioning of analysis tooling to support use of produced datasets.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** Not identified  
---

[FR-013]: Provide ASPERA-3 and MEX OA IDFS data to NASA PDS  
**Description**: “ASPERA-3 IDFS data and MEX OA IDFS data shall be provided to NASA PDS.”  
**Rationale:** Defines an external delivery function to a long-term archive.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** Not identified  
---

[FR-014]: Provide ASPERA-3 data to NASA PDS in PDS-compliant form  
**Description**: “ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form.”  
**Rationale:** Specifies a required output format/standard for an external interface.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013
- **Conflicts with:** Not identified  
---

[FR-015]: Calibrate and validate ASPERA-3 data prior to PDS deposit  
**Description**: “ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS.”  
**Rationale:** Defines required processing steps before archival submission.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-013
- **Conflicts with:** Not identified  
---

[FR-016]: Provide IDFS data processing algorithms to IRF  
**Description**: “SwRI shall provide IDFS data processing algorithms to IRF.”  
**Rationale:** Requires delivery of processing algorithms to an external organization.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** Not identified  
---

[FR-017]: Define distribution mechanisms in APAF Operations Procedures Document  
**Description**: “The distribution mechanisms shall be clearly defined/described in the APAF Operation Procedures Document.”  
**Rationale:** Requires creation of an operational artifact specifying how distribution is performed.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** Not identified  
---

[FR-018]: Document any identified operating states/modes in APAF Operations Procedures Document  
**Description**: “The APAF data system is not required to operate in more than one state or mode. However, if any are identified, they shall be documented in the APAF Operations Procedures Document.”  
**Rationale:** Defines documentation behavior contingent on discovery of additional modes.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017
- **Conflicts with:** Not identified  
---

[FR-019]: Provide installation and operations procedures sufficient to avoid training requirements  
**Description**: “The APAF Operations Procedures Document shall provide installation and operations procedures… in enough detail where there are no training-related requirements for users and operators…”  
**Rationale:** Requires production of procedures/documentation to enable operation without training.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017
- **Conflicts with:** Not identified  
---

[FR-020]: Provide APAF system maintenance  
**Description**: “SwRI shall provide APAF system maintenance.” / “The SwRI software team shall provide system maintenance…” Updated per evaluator: “SwRI shall respond to critical system incidents within 4 business hours, and resolve support cases within 7 days unless escalated.” (Next action: Define maintenance/support expectations in measurable SLA terms.)  
**Rationale:** Specifies an operational support function to be performed by SwRI.  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** Not identified  
---

[FR-021]: Provide software support for the APAF system  
**Description**: “SwRI shall provide software support for the APAF system.” / “The SwRI software team shall provide… software support.”  
**Rationale:** Specifies an operational support function (software support).  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** Not identified  
---

[FR-022]: Integrate science analysis software into the NASA-approved data repository  
**Description**: “Science analysis software shall be integrated into the NASA approved data repository.”  
**Rationale:** Defines an integration/delivery function into a specified repository environment.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** Not identified  
---