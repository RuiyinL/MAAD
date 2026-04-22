# Architecturally Significant Requirements Results

[ASR-001]: Automated Daily Processing Pipeline
**Description**: The APAF system shall acquire from ESOC the telemetry data of the ASPERA-3 Experiment and Mars Express Orbit/Attitude to automatically process the data on a daily basis.
**Architectural Impact:**  
This requirement dictates the need for a scheduled batch processing architecture. It influences the selection of orchestration tools (e.g., Celery, Airflow, Cron) and requires a stateless or state-managed pipeline capable of daily triggers without manual intervention. It drives the decomposition of the system into "Acquisition" and "Processing" modules.

**Quality Attributes Affected:**  
Performance, Automation, Reliability

**Architectural Constraints:**  
- Must support time-triggered jobs (daily).
- Must handle automated data ingestion from external source (ESOC/NISN).
- Pipeline must be robust enough to run unattended.

**Rationale:**  
This requirement is architecturally significant because it defines the core operational rhythm of the system. A failure in automation directly impacts mission goals (24-hour delivery). It necessitates a specific architectural pattern (Batch Pipeline) rather than real-time streaming or manual processing.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** None
---

[ASR-002]: Long-Term Local Archival Storage
**Description**: The ASPERA-3 and MEX OA telemetry data shall be stored on a local SwRI archive for data availability and re-processing. The ASPERA-3 and MEX OA IDFS data sets shall be stored on a local SwRI archive for data availability and analysis.
**Architectural Impact:**  
This requirement constrains the storage subsystem design. It necessitates a durable, high-capacity storage solution (e.g., S3-Glacier, NAS) integrated directly into the application's data layer. It influences data lifecycle management policies (retention, tiering) and disaster recovery strategies.

**Quality Attributes Affected:**  
Durability, Availability, Scalability

**Architectural Constraints:**  
- Storage must be "local SwRI archive" (on-premise or private cloud).
- Must support re-processing workflows (random access to historical data).
- High durability required for long-term retention.

**Rationale:**  
Storage architecture is a fundamental building block. The requirement for local archival for re-processing implies a need for indexed, queryable storage rather than simple cold backup, affecting database and file system choices.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005
- **Conflicts with:** None
---

[ASR-003]: PDS Compliance and Validation Architecture
**Description**: ASPERA-3 data shall be provided to NASA PDS in PDS-compliant form. ASPERA-3 data shall be calibrated and validated prior to depositing in the NASA PDS.
**Architectural Impact:**  
This requirement drives the need for a "Schema-First" validation layer. The architecture must include a dedicated validation module that enforces PDS standards before data leaves the system. It impacts the data model design, requiring metadata tracking and lineage (calibration history) to be stored alongside scientific data.

**Quality Attributes Affected:**  
Compliance, Data Integrity, Interoperability

**Architectural Constraints:**  
- Data transformation pipelines must include validation gates.
- System must support metadata enrichment for compliance.
- Export modules must strictly adhere to external PDS interface specifications.

**Rationale:**  
Compliance with external standards (PDS) is a high-risk area. Failure to comply results in rejection of data products. This necessitates architectural patterns that prioritize validation and data lineage over raw speed, potentially introducing synchronous validation steps in the pipeline.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, NFR-005
- **Conflicts with:** None
---

[ASR-004]: Security and Embargo Management
**Description**: The web-based displays defined by the ASPERA-3 team to be used for science analysis shall be password protected until the ASPERA-3 data is made public to support the ASPERA-3 team in meeting mission goals and objectives. Embargo is automatically lifted 180 days after initial file ingest; SRE to test embargo transition weekly using fictitious files and verify audit records generated for each lift event. Acceptance: SRE creates test user with embargoed data, advances clock/event, verifies access granted on embargo lift and that audit record is present.
**Architectural Impact:**  
This requirement mandates the inclusion of an Authentication and Authorization (AuthN/AuthZ) subsystem. It implies Role-Based Access Control (RBAC) to distinguish between "Public" and "Team" views. It requires an embargo management mechanism to automatically lift restrictions based on time or data status.

**Quality Attributes Affected:**  
Security, Confidentiality, Availability

**Architectural Constraints:**  
- Web server must support session management and password protection.
- Data access logic must check user roles against data embargo status.
- Audit logging may be required for team access.

**Rationale:**  
Security is a cross-cutting concern that affects the web interface, API layer, and data access layers. The "embargo" aspect adds temporal logic to security policies, requiring specific architectural support for time-based access rules.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, NFR-003
- **Conflicts with:** None
---

[ASR-005]: Data Throughput and Latency Constraints
**Description**: ASPERA-3 IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I's within 24 hours of acquiring ASPERA-3 telemetry as long as the transmission and processing are error-free.
**Architectural Impact:**  
This requirement imposes strict performance constraints on the processing pipeline. It influences hardware sizing, concurrency models (parallel processing), and error recovery strategies. If processing exceeds 24 hours, the architecture fails. This may require horizontal scaling of processing workers.

**Quality Attributes Affected:**  
Performance, Latency, Scalability

**Architectural Constraints:**  
- End-to-end pipeline latency must be < 24 hours.
- Error handling must not block the 24-hour window (requires retry queues or dead-letter queues).
- System must handle peak telemetry loads without degradation.

**Rationale:**  
The 24-hour deadline is a hard business constraint that translates directly into technical capacity planning. It dictates the choice between batch vs. stream processing and the level of parallelism required in the architecture.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-001
- **Conflicts with:** None
---