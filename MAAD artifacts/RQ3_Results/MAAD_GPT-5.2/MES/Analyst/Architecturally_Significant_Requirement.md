# Architecturally Significant Requirements Results

[ASR-001]: End-to-end telemetry processing pipeline (acquire → process → distribute → archive → submit to PDS)  
**Description**: “The APAF data system acquires the telemetry data via NISN, processes the data into IDFS data sets, distributes the IDFS data sets to the ASPERA-3 team, provides web-based displays… stores the telemetry and IDFS data sets on a local SwRI archive, and submits the ASPERA-3 IDFS data sets to PDS for long-term archival.”  
**Architectural Impact:**  
Requires a multi-stage data pipeline architecture with ingestion, processing, product generation, distribution services, web presentation, local archival storage, and external archival submission integration.  
**Quality Attributes Affected:** Availability, Reliability, Maintainability, Interoperability  
**Architectural Constraints:** Must include components for ingestion (NISN/ESOC), IDFS generation, distribution, web server, local archive, and PDS submission.  
**Rationale:** Defines the system’s top-level decomposition and external integrations; strongly constrains architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003, FR-005, FR-006, FR-008, FR-010, FR-013
- **Conflicts with:** Not identified  
---

[ASR-002]: Standardized data product format (IDFS) for all processed outputs  
**Description**: “These data products will be put into a form known as the Instrument Data File Set (IDFS).” / “The APAF system shall process all ASPERA-3 science data into IDFS data sets.” / “...engineering and ancillary information… into IDFS data sets.” Updated per evaluator: “IDFS schema v1.3.2 at [https://example/schema/v1.3.2.json] must be used for all outputs.” (Next action: Produce or link authoritative IDFS schema document.)  
**Architectural Impact:**  
Forces a canonical data model and file/set structure across the pipeline; drives schema definitions, validators, versioning, and tooling compatibility (access/analysis software).  
**Quality Attributes Affected:** Interoperability, Maintainability, Portability  
**Architectural Constraints:** Processing outputs must conform to IDFS; internal representations likely need deterministic mapping to IDFS.  
**Rationale:** A mandated data standard shapes storage, processing, interfaces, and downstream tools.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-011, FR-012
- **Conflicts with:** Not identified  
---

[ASR-003]: External integration with ESOC telemetry sources and daily automated processing  
**Description**: “The APAF system shall acquire from ESOC the telemetry data… to automatically process the data on a daily basis.”  
**Architectural Impact:**  
Requires scheduled/automated ingestion and orchestration, robust connectivity to ESOC, and operational automation (batch pipeline, monitoring, retries).  
**Quality Attributes Affected:** Availability, Reliability, Operability  
**Architectural Constraints:** Must support unattended daily runs; must integrate with ESOC telemetry delivery mechanisms.  
**Rationale:** Cross-cutting operational constraint that drives orchestration, scheduling, and integration design.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** Not identified  
---

[ASR-004]: Local archival storage for telemetry, IDFS, and intermediate products  
**Description**: “The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive…” / “The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive…” / “Any APAF-generated intermediate files… shall be stored on a local SwRI archive…” Updated per evaluator: “Local archive must retain all files ≥5 years, perform nightly incremental backup, and pass annual restore test with >99% artifact recovery.” (Next action: Provide and attach explicit storage/backup/retention acceptance values.)  
**Architectural Impact:**  
Requires an on-prem/local archival subsystem with capacity planning, retention, indexing/metadata, and retrieval to support reprocessing and analysis.  
**Quality Attributes Affected:** Availability, Reliability, Maintainability  
**Architectural Constraints:** Must maintain local archive copies of multiple data classes (raw, intermediate, products).  
**Rationale:** Storage/retention is a major architectural driver affecting infrastructure and data management.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-006, FR-007
- **Conflicts with:** Not identified  
---

[ASR-005]: Conditional generation and handling of “cleaned-up telemetry” intermediates  
**Description**: “Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC…”  
**Architectural Impact:**  
Requires alternate processing paths and provenance tracking (source cleaned vs locally cleaned), plus storage and distribution of intermediates.  
**Quality Attributes Affected:** Reliability, Maintainability, Traceability  
**Architectural Constraints:** Must support fallback processing mode and intermediate artifact lifecycle.  
**Rationale:** Introduces branching workflows and additional artifacts that affect pipeline design and operations.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-007, FR-010
- **Conflicts with:** Not identified  
---

[ASR-006]: Web-based data dissemination with mixed public and restricted access  
**Description**: “Web-based displays of the most current ASPERA-3 data shall be provided for public view…” / “...displays… for science analysis… shall be password protected until the ASPERA-3 data is made public…” / “The APAF system web server shall be password protected where appropriate…” Updated per evaluator: “Roles: {public—read current data; Co-I—read all data, view science displays; admin—assign roles, manage display configs}. Session timeout: 30 min; RBAC actions logged in [access_log] retained 180 days.” (Next action: Enumerate RBAC roles, document explicitly in security/architecture supplement.)  
**Architectural Impact:**  
Requires a web presentation tier with authentication/authorization, content segregation (public vs team-only), and potentially separate endpoints or access policies.  
**Quality Attributes Affected:** Security, Privacy, Usability, Availability  
**Architectural Constraints:** Must implement password-protected access “where appropriate” and for science-analysis displays until public release.  
**Rationale:** Cross-cutting security and dissemination needs shape the web architecture and access control model.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-009, NFR-002, NFR-003
- **Conflicts with:** Not identified  
---

[ASR-007]: Timely electronic distribution to Co-Is (24-hour SLA, conditional)  
**Description**: “...shall be provided… within 24 hours of acquiring… telemetry as long as the transmission and processing are error-free…” (applies to ASPERA-3 IDFS, MEX OA IDFS, and intermediate files)  
**Architectural Impact:**  
Drives throughput, automation, monitoring, and failure handling; may require queueing, incremental processing, and operational alerting to meet the delivery window.  
**Quality Attributes Affected:** Performance (timeliness), Reliability, Operability  
**Architectural Constraints:** Must support end-to-end processing + distribution within 24 hours under stated conditions.  
**Rationale:** A measurable delivery constraint that impacts pipeline scheduling, processing capacity, and distribution mechanisms.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003, FR-004, FR-010, NFR-005, NFR-006, NFR-007
- **Conflicts with:** Not identified  
---

[ASR-008]: PDS archival compliance, validation, and submission deadline (≤ 6 months)  
**Description**: “ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form.” / “ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS.” / “...no later than 6 months after acquisition.”  
**Architectural Impact:**  
Requires a PDS submission subsystem, compliance validation tooling, calibration/validation workflow, and tracking of acquisition-to-submission timelines.  
**Quality Attributes Affected:** Compliance, Data Integrity, Maintainability  
**Architectural Constraints:** Must produce PDS-compliant packages and submit within 6 months; must include calibration/validation before submission.  
**Rationale:** External compliance and deadline requirements strongly constrain data formats, workflows, and governance.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-014, FR-015, NFR-008
- **Conflicts with:** Not identified  
---

[ASR-009]: Built-in error handling to protect data integrity across the pipeline  
**Description**: “The APAF ground data system shall have built-in error handling for better data integrity.”  
**Architectural Impact:**  
Requires consistent error detection/handling patterns across ingestion, processing, storage, and distribution (e.g., validation, retries, quarantine, audit/provenance).  
**Quality Attributes Affected:** Reliability, Data Integrity, Maintainability  
**Architectural Constraints:** Error handling must be designed-in (not ad hoc) across subsystems.  
**Rationale:** Cross-cutting reliability/integrity concern affecting most components and interfaces.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-010, FR-013
- **Conflicts with:** Not identified  
---

[ASR-010]: Internal interfaces and internal data requirements deferred to design documents (SDDs)  
**Description**: “All internal interfaces are left to the design.” / “The Software Design Documents of each of the seven components shall contain the detailed information of the internal interfaces.” / “All internal data requirements are left to the design.” / “...SDDs… shall contain the detailed information of the virtual instrument data items.” Updated per evaluator: “All SDD-defined interface contracts shall be stored in [requirements tracking system] with reference to SRS project-unique ID and change log.” (Next action: Define and implement interface contract repository and traceability policy.)  
**Architectural Impact:**  
Forces architecture governance via SDDs and implies componentized design (seven components/virtual instruments) with interface specifications defined outside the SRS.  
**Quality Attributes Affected:** Maintainability, Modularity, Traceability  
**Architectural Constraints:** Internal interfaces/data items must be specified in SDDs for each component; SRS does not constrain internal interface technology directly.  
**Rationale:** Establishes where architectural contracts live and enforces component-level interface documentation, shaping development and integration approach.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** NFR-010 (process/ID rigor may be harder if SDDs are not aligned)  
---