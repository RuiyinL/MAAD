# Architecturally Significant Requirements Results

[ASR-001]: Daily automated telemetry processing pipeline (end-to-end batch workflow)
**Description**: The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude to automatically process the data on a daily basis.
**Architectural Impact:**  
Forces a scheduled, unattended batch pipeline and orchestration across ingest, processing, validation, archiving, distribution, and web publication steps; requires job control, retries, idempotency, and operational monitoring.
  
**Quality Attributes Affected:** Availability, Reliability, Operability, Performance (timeliness)

**Architectural Constraints:** Must support automated daily scheduling and execution of the ingest→process workflow.

**Rationale:** Cross-cutting operational requirement that shapes component decomposition (ingest, processor, scheduler, monitoring).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, NFR-002
- **Conflicts with:** NFR-006
---

[ASR-002]: Canonical data products in IDFS (mandated product format)
**Description**: These data products will be put into a form known as the Instrument Data File Set (IDFS). / The APAF system shall process all ASPERA-3 science data into IDFS data sets.
**Architectural Impact:**  
Requires dedicated data model/schema handling, IDFS writers/validators, versioning strategy, and consistent metadata across all processing components.
  
**Quality Attributes Affected:** Interoperability, Maintainability, Compliance

**Architectural Constraints:** Outputs must be produced as IDFS datasets (format constraint).

**Rationale:** Strong constraint on internal data representations and processing architecture.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004
- **Conflicts with:** NFR-003
---

[ASR-003]: Conditional telemetry cleanup path when ESOC cleaned telemetry is unavailable
**Description**: Intermediate files of cleaned-up ASPERA-3 and MEX OA telemetry shall be generated in the event that cleaned-up telemetry is not provided by ESOC... The clean-up process shall produce telemetry files in [format], validated via [tool], and log provenance/processing steps for auditability. (Owner: Not specified; Next action: Detail data flow, format, and acceptance for alternate cleanup path.)
**Architectural Impact:**  
Introduces an alternate processing branch and necessitates a “cleaning” subsystem, provenance tracking, and conditional workflow routing based on upstream availability.
  
**Quality Attributes Affected:** Reliability, Maintainability, Traceability

**Architectural Constraints:** System must support optional/conditional generation of cleaned telemetry intermediates.

**Rationale:** Adds significant workflow complexity and integration risk.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-001
- **Conflicts with:** NFR-010, NFR-011, NFR-012
---

[ASR-004]: Multi-tier storage/archival for reprocessing and analysis (local SwRI archive)
**Description**: The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing. / The ... IDFS data sets shall be stored on a local SwRI archive... / Any ... intermediate files ... shall be stored on a local SwRI archive...
**Architectural Impact:**  
Requires an archival subsystem with defined storage layout, indexing/metadata, lifecycle/retention, and retrieval performance adequate for reprocessing and analysis.
  
**Quality Attributes Affected:** Availability, Recoverability, Performance, Maintainability

**Architectural Constraints:** Must provide local archival storage for telemetry, IDFS, and intermediate artifacts.

**Rationale:** Storage and reprocessing are central, high-volume cross-cutting concerns impacting data architecture.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, FR-008, NFR-007
- **Conflicts with:** None specified
---

[ASR-005]: Public vs embargoed web access (access control boundary)
**Description**: Web-based displays of the most current ASPERA-3 data shall be provided for public view... / ...science analysis... shall be password protected until the ASPERA-3 data is made public... / The APAF system web server shall be password protected where appropriate...
**Architectural Impact:**  
Requires an authentication/authorization mechanism, separation of public vs restricted content, and an explicit release/embargo control model affecting the web tier and data-serving APIs.
  
**Quality Attributes Affected:** Security, Privacy, Usability, Compliance

**Architectural Constraints:** Must support public access for “most current” views while restricting team analysis views via password protection until public release.

**Rationale:** Cross-cutting security requirement that materially affects presentation, data access, and operational governance.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, FR-010, FR-011, NFR-004
- **Conflicts with:** FR-009 (if “current data” overlaps non-public data)
---

[ASR-006]: Built-in error handling to protect data integrity
**Description**: The APAF ground data system shall have built-in error handling for better data integrity. All critical errors must be logged to central event system and trigger on-call escalation if unresolved for 2 hours. (Owner: Not specified; Next action: Add error classification, logging, and escalation detail to requirements.)
**Architectural Impact:**  
Necessitates consistent error taxonomy, retry/rollback strategies, integrity checks, and centralized logging/alerting across ingest, processing, storage, and distribution components.
  
**Quality Attributes Affected:** Integrity, Reliability, Operability

**Architectural Constraints:** Error handling must be designed as a system-wide capability, not ad hoc per module.

**Rationale:** Cross-cutting quality requirement influencing many components and their contracts.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** NFR-010, NFR-011, NFR-012 (timeliness under failure conditions)
---

[ASR-007]: Co-I electronic distribution within 24 hours (SLO-driven distribution architecture)
**Description**: ...shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ... telemetry... (for ASPERA-3 IDFS, MEX OA IDFS, and intermediate files). A monitoring subsystem shall record time from telemetry ingest to Co-I data distribution, trigger alerts at 22h, and log missed windows with root cause. (Owner: Not specified; Next action: Add observable SLO measurement/monitoring to architecture.)
**Architectural Impact:**  
Forces time-bounded distribution workflows, queuing/scheduling, monitoring of deadlines, and back-pressure handling; impacts compute sizing and end-to-end pipeline design.
  
**Quality Attributes Affected:** Performance (timeliness), Reliability, Operability

**Architectural Constraints:** Distribution mechanism must reliably meet a 24-hour delivery window for electronically distributed products (conditional “error-free”).

**Rationale:** Measurable timeliness requirement that drives workflow orchestration and operational monitoring.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, NFR-010, NFR-011, NFR-012
- **Conflicts with:** NFR-003 (undefined “error-free” and integrity work may increase latency)
---

[ASR-008]: External long-term archival submission to NASA PDS with compliance and deadlines
**Description**: ASPERA-3 IDFS data and MEX OA IDFS data shall be provided to NASA PDS. / ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form. / ...calibrated and validated prior to depositing... / ...no later than 6 months after acquisition.
**Architectural Impact:**  
Requires a PDS submission/export subsystem, validation gates, packaging, metadata management, and traceable provenance of calibration/validation to satisfy external compliance.
  
**Quality Attributes Affected:** Compliance, Integrity, Timeliness, Interoperability

**Architectural Constraints:** Must generate PDS-compliant outputs and submit within 6 months; must enforce calibration/validation before submission.

**Rationale:** High business value/compliance risk with strong architectural implications on data models and workflows.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017, FR-018, NFR-013
- **Conflicts with:** NFR-003
---

[ASR-009]: Internal interfaces and internal data definitions deferred to SDDs (documentation-driven architecture constraint)
**Description**: All internal interfaces are left to the design. The Software Design Documents of each of the seven components shall contain the detailed information of the internal interfaces. / All internal data requirements are left to the design. The Software Design Documents ... shall contain the detailed information of the virtual instrument data items.
**Architectural Impact:**  
Forces contract-first internal architecture definition (explicit interface/data contracts per component) and governance to avoid integration ambiguity and ensure component interoperability.
  
**Quality Attributes Affected:** Maintainability, Modifiability, Testability

**Architectural Constraints:** Internal interfaces/data must be specified in SDDs for each component; architecture must accommodate componentized design with documented contracts.

**Rationale:** Determines how modules integrate and how verification can be performed; high risk if not made explicit.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008
- **Conflicts with:** None specified
---

[ASR-010]: Multi-stakeholder distribution and software provisioning (team + IRF + NASA repository)
**Description**: ...shall be provided to all ASPERA-3 Co-I’s. / SwRI shall provide IDFS data processing algorithms to IRF. / Science analysis software shall be integrated into the NASA approved data repository.
**Architectural Impact:**  
Requires packaging/versioning, release management, and potentially multiple distribution channels with access control and traceability for data and software artifacts.
  
**Quality Attributes Affected:** Operability, Maintainability, Security, Compliance

**Architectural Constraints:** Must support distribution/provisioning of both data products and software artifacts to multiple external parties/repositories.

**Rationale:** Cross-system integration and release governance significantly shape deployment and artifact management architecture.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-014, FR-015, FR-019, FR-020
- **Conflicts with:** NFR-004 (access restrictions)