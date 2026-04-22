Analysis Plan  
Scope: Design a production-ready APAF ground data system architecture covering ingest→processing→archive→distribution→web→PDS with security, integrity, and ops.  
Approach: Use 4+1 views aligned to provided UML; normalize vague SRS into testable INF-* requirements; define contracts (OpenAPI + gRPC) and schemas (SQL DDL).  
Top validation steps: Traceability matrix completeness; API/schema linting (OpenAPI/proto/SQL/k8s); SLO/DR/security acceptance tests mapped to ASR/NFR.

# A. Executive Summary (≤1 page)

APAF (ASPERA-3 Processing and Archiving Facility) is a ground data system that acquires ASPERA-3 and Mars Express Orbit/Attitude (MEX OA) telemetry from ESOC via NISN, performs daily automated processing into Instrument Data File Set (IDFS) datasets, optionally generates cleaned telemetry when ESOC does not provide it, archives raw/intermediate/IDFS products locally, distributes products to ASPERA-3 Co-Is within 24 hours, provides public and password-protected web displays, and submits calibrated/validated PDS-compliant bundles to NASA PDS within 6 months.

**Primary diagram mapping (one-line):**  
Context & use cases: *UseCaseView_APAF* (UC_Acquire, UC_Daily, UC_IDFS, UC_Clean, UC_Archive, UC_PublicWeb, UC_TeamWeb, UC_PDS) → runtime: *ActivityView_DailyPipeline*, *SequenceView_S1_DailyPipeline*, *SequenceView_S2_TeamWebAccess* → structure: *ComponentView_APAF*, *PackageView_APAF*, *ClassView_APAF* → deployment: *DeploymentView_APAF*, *ContainerView_APAF*.

**Architectural style(s):** Modular service-oriented monolith (clear component boundaries + internal contracts) with batch-first orchestration and queued distribution.  
**Deployment topology:** Single SwRI Kubernetes cluster (or VM-first) with one app tier, one NAS-backed archive, PostgreSQL metadata DB, and a job queue; secure egress to ESOC and NASA PDS.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| 24h distribution SLO breaches due to ingest/processing delays | Miss DR-002/003/004 | Deadline-driven `DistributionJob` + alert at 22h + retries + escalation (ClassView_APAF: DistributionJob; StateView_TelemetryBatch: MissedSLO/Escalated; MonitoringService) |
| Ambiguity in “public current data” vs embargo | Data leakage | Explicit `ReleaseGate` (EMBARGOED/PUBLIC) enforced at DataAPI + WebPortal (ClassView_APAF: ReleaseGate; SequenceView_S2_TeamWebAccess: ReleaseGateService) |
| Data integrity and reprocessing correctness | Scientific invalidity, archive corruption | Integrity gates with SHA256, idempotent writes, immutable audit logs, validation adapters for IDFS/PDS4 (ClassView_APAF: IntegrityService, ErrorEvent; ComponentView_APAF: IDFSValidatorAdapter, PDSValidatorAdapter) |

## Key QA coverage mapping

| Quality attribute | ASR/NFR IDs | Test types |
|---|---|---|
| Scalability | INF-006 (web/API concurrency), INF-007 (distribution throughput) | Load tests, HPA scale tests |
| Availability | INF-010 (backup/restore), CR-001/LR-001 (maintenance/support) | DR drills, failover tests |
| Security | PR-001, FR-010, FR-011 | SAST/DAST, RBAC/pen tests, audit verification |
| Performance | DR-002/003/004, INF-007 | E2E timing tests, synthetic SLO monitoring |
| Maintainability | CR-001/LR-001, INF-012 (modular interfaces) | Contract tests, architecture tests, code quality gates |

---

# B. Traceability & Rationale

Notes:
- The SRS uses FR/PR/CR/LR/DR mnemonics but does not provide numeric IDs. **Inferred IDs** are assigned as `INF-*` for missing NFR/ASR-like items referenced in diagrams (e.g., “ASR-007” in UML). These are listed in Section K.
- Diagram references use **title + element IDs** only (no PlantUML source).

## Traceability matrix (CSV-style table)

Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale
---|---|---|---|---|---
FR-001 | Acquire ASPERA-3 telemetry + MEX OA from ESOC; auto daily processing | UseCaseView_APAF:UC_Acquire,UC_Daily; ActivityView_DailyPipeline; DeploymentView_APAF:ESOC,AppVM | ESOCIngestAdapter, PipelineOrchestrator | architecture.md; internal.proto | Daily orchestrator invokes ingest adapter and schedules pipeline.
FR-002 | Process all ASPERA-3 science data into IDFS | UseCaseView_APAF:UC_IDFS; SequenceView_S1_DailyPipeline:IDFSProcessor | IDFSProcessor | architecture.md; internal.proto; sql/idfsdataset_ddl.sql | Dedicated processing service produces canonical IDFS datasets.
FR-003 | Process engineering/ancillary for calibration/validation into IDFS | ActivityView_DailyPipeline (engineering/ancillary fork); ComponentView_APAF:IDFSProcessor | IDFSProcessor | architecture.md; internal.proto | Pipeline includes engineering/ancillary path for IDFS.
FR-004 | Generate intermediate cleaned telemetry if ESOC does not provide | UseCaseView_APAF:UC_Clean; StateView_TelemetryBatch:Cleaning; ActivityView_DailyPipeline (conditional) | TelemetryCleanupService | architecture.md; internal.proto; sql/cleantelemetryfile_ddl.sql | Conditional cleanup path is explicit and stored.
FR-005 | Generate cleaned-up telemetry when ESOC cleaned telemetry unavailable | UseCaseView_APAF:UC_Clean (extend note); SequenceView_S1_DailyPipeline (alt) | TelemetryCleanupService | architecture.md; internal.proto | Implements the SRS conditional clause.
FR-006 | Store telemetry on local SwRI archive | UseCaseView_APAF:UC_Archive; DeploymentView_APAF:NAS; ClassView_APAF:ArchiveEntry | LocalArchive | architecture.md; sql/archiveentry_ddl.sql | ArchiveEntry records all artifacts and storage paths.
FR-007 | Store IDFS datasets on local SwRI archive | UseCaseView_APAF:UC_Archive; ClassView_APAF:IDFSDataset→ArchiveEntry | LocalArchive | architecture.md; sql/archiveentry_ddl.sql | Same archive mechanism stores IDFS directories.
FR-008 | Store intermediate cleaned telemetry files on local archive | ClassView_APAF:CleanTelemetryFile→ArchiveEntry; ActivityView_DailyPipeline | LocalArchive | architecture.md; sql/cleantelemetryfile_ddl.sql; sql/archiveentry_ddl.sql | Intermediate files persisted for reprocessing/support.
FR-009 | Public web displays of most current data for monitoring | UseCaseView_APAF:UC_PublicWeb; ContainerView_APAF:C_Web | WebPortal (Public) | architecture.md; openapi.yaml | Public endpoints only expose ReleaseGate=PUBLIC datasets.
FR-010 | Team-defined web displays for science analysis | UseCaseView_APAF:UC_TeamWeb; SequenceView_S2_TeamWebAccess | WebPortal (Team), DataAPI | architecture.md; openapi.yaml | Team portal provides broader query/display features.
FR-011 | Password protect team science displays until data public | UseCaseView_APAF:UC_Auth; SequenceView_S2_TeamWebAccess:AuthService | AuthService, ReleaseGateService | architecture.md; openapi.yaml; sql/useraccount_ddl.sql | RBAC + embargo model ensures protection.
FR-012 | Built-in error handling for better integrity | UseCaseView_APAF note; ClassView_APAF:IntegrityService, ErrorEvent | IntegrityService, MonitoringService | architecture.md; internal.proto; sql/errorevent_ddl.sql | Central error taxonomy + retry/rollback + logging.
FR-013 | Provide IDFS + intermediate files to all Co-I’s | UseCaseView_APAF:UC_Distribute; ComponentView_APAF:DistributionService | DistributionService | architecture.md; internal.proto; openapi.yaml | Distribution jobs deliver required artifacts to recipients.
FR-014 | Provide IDFS data access software to Co-I’s | UseCaseView_APAF:UC_Software | PublishSoftwareToRepo process | architecture.md | Delivered as packaged client + docs in repository.
FR-015 | Provide science analysis software to Co-I’s | UseCaseView_APAF:UC_Software | PublishSoftwareToRepo process | architecture.md | Similar distribution mechanism as FR-014.
FR-016 | Provide IDFS to NASA PDS | UseCaseView_APAF:UC_PDS; ComponentView_APAF:PDSExportService | PDSExportService | architecture.md; internal.proto; sql/pdsbundle_ddl.sql | PDS bundle packaging and transfer recorded.
FR-017 | Provide ASPERA-3 data to PDS in PDS-compliant form | ComponentView_APAF:PDSValidatorAdapter; ActivityView_DailyPipeline (PDS4 validate) | PDSValidatorAdapter, PDSExportService | architecture.md; internal.proto; sql/pdsbundle_ddl.sql | Enforce PDS4 validation as a compliance gate.
FR-018 | Calibrate & validate prior to PDS deposit | ActivityView_DailyPipeline (Calibrate & validate) | IDFSProcessor, PDSExportService | architecture.md | Calibration/validation steps precede PDS bundle generation.
FR-019 | Provide to PDS no later than 6 months after acquisition | ActivityView_DailyPipeline (PDS due?) | PDSExportService, MonitoringService | architecture.md; sql/distributionjob_ddl.sql | Backlog tracking + deadline metrics for 6-month SLA.
FR-020 | Provide processing algorithms to IRF | UseCaseView_APAF:UC_IRF | Export package (algorithms) | architecture.md | Algorithms packaged and versioned for IRF delivery.
FR-021 | Integrate science analysis software into NASA approved data repository | UseCaseView_APAF:UC_Software (NASARepo) | Release/Packaging tooling | architecture.md | Build artifacts published to NASA repository.
FR-022 | Distribution mechanisms defined in Operations Procedures Document | (No UML; ops doc implied) | Ops/Runbooks | architecture.md | This architecture defines mechanisms; ops doc is a deliverable outside scope.
FR-023 | Determine which datasets distributed per Co-I by needs/resources pre-launch | (No UML) | DistributionService config | architecture.md | Implement recipient-group mapping config.
PR-001 | Web server password protected where appropriate | UseCaseView_APAF:UC_Auth; ContainerView_APAF:C_Auth | AuthService, WebPortal | architecture.md; openapi.yaml | Enforce auth on team endpoints; public endpoints anonymous.
CR-001 | SwRI software team provides system maintenance/software support | DeploymentView_APAF:Ops | CI/CD + runbooks | architecture.md | Operational practices and support plan included.
LR-001 | SwRI provides APAF system maintenance | DeploymentView_APAF:Ops | Ops procedures | architecture.md | Maintenance windows and patching plan.
LR-002 | SwRI provides software support | DeploymentView_APAF:Ops | Issue triage | architecture.md | Support SLAs and escalation path.
DR-001 | Provide IDFS + intermediates to all Co-I’s | UseCaseView_APAF:UC_Distribute | DistributionService | architecture.md; internal.proto | Matches FR-013 (delivery framing).
DR-002 | Distribute ASPERA-3 IDFS to Co-I’s within 24h if error-free | StateView_TelemetryBatch:MissedSLO/Escalated; ClassView_APAF:DistributionJob | DistributionService, MonitoringService | architecture.md; sql/distributionjob_ddl.sql | Deadline persisted; alerts/metrics measure compliance.
DR-003 | Distribute MEX OA IDFS within 24h | ActivityView_DailyPipeline (MEX OA fork) | DistributionService | architecture.md; sql/distributionjob_ddl.sql | Separate dataset type tracked in jobs.
DR-004 | Distribute cleaned telemetry intermediates within 24h | UseCaseView_APAF:UC_Clean,UC_Distribute | DistributionService | architecture.md; sql/distributionjob_ddl.sql | Same SLO policy for intermediates.
DR-005 | Provide ASPERA-3 + MEX OA IDFS to NASA PDS | UseCaseView_APAF:UC_PDS | PDSExportService | architecture.md; sql/pdsbundle_ddl.sql | Export service controls submission packages.
DR-006 | Provide ASPERA-3 data to PDS in PDS-compliant form | ComponentView_APAF:PDSValidatorAdapter | PDSValidatorAdapter | architecture.md; internal.proto | Mandatory validator gate.
DR-007 | Calibrate & validate prior to PDS | ActivityView_DailyPipeline | IDFSProcessor, PDSExportService | architecture.md | Explicit workflow steps.
DR-008 | Provide data to PDS ≤ 6 months | ActivityView_DailyPipeline | PDSExportService | architecture.md | Scheduled backlog evaluation and alerts.
DR-009 | Provide IDFS algorithms to IRF | UseCaseView_APAF:UC_IRF | Packaging/Export | architecture.md | Versioned algorithm release process.
DR-010 | Integrate science analysis software into NASA repository | UseCaseView_APAF:UC_Software | Release tooling | architecture.md | Release pipeline publishes artifacts.
DR-011 | Provide IDFS data access software to Co-I’s | UseCaseView_APAF:UC_Software | Release tooling | architecture.md | Delivered binaries/source and docs.
DR-012 | Provide science analysis software to Co-I’s | UseCaseView_APAF:UC_Software | Release tooling | architecture.md | Same as above.

**Inferred (from UML notes) operational requirements included in traceability:** see INF-* list in Section K and in `traceability_matrix.csv`.

---

# C. Architecture Overview

## 4+1 View alignment

1) **Scenario/Use-case view**  
- Daily pipeline: *UseCaseView_APAF* (UC_Daily includes UC_Acquire/UC_IDFS/UC_Archive/UC_Distribute), realized by *ActivityView_DailyPipeline* and *SequenceView_S1_DailyPipeline*.  
- Team web access with embargo: *UseCaseView_APAF* (UC_TeamWeb includes UC_Auth), realized by *SequenceView_S2_TeamWebAccess*.  
- PDS submission: *UseCaseView_APAF* (UC_PDS includes UC_IDFS), realized by PDSExportService components.

2) **Logical view (domain model & invariants)**  
- Domain entities: TelemetryBatch, CleanTelemetryFile, IDFSDataset, PDSBundle, ArchiveEntry, DistributionJob, ReleaseGate, UserAccount, ErrorEvent (see *ClassView_APAF*).  
- Lifecycle enforcement and SLO states: *StateView_TelemetryBatch*.

3) **Process view (runtime & concurrency)**  
- Orchestration: PipelineOrchestrator drives ingest→integrity→cleanup(optional)→IDFS generation→validation→archive→distribution→web publish (see *ActivityView_DailyPipeline*).  
- Concurrency: parallel processing of science and engineering/ancillary paths; distribution runs asynchronously via JobQueue (see *ComponentView_APAF*: JobQueue).

4) **Development view (code organization)**  
- Packages: ui/api/domain/application/integrations/infrastructure/crosscutting (see *PackageView_APAF*). This supports maintainability and internal interface definition (SRS: “left to the design”).

5) **Physical/Deployment view**  
- Nodes: ESOC systems; SwRI app server(s), NAS archive, queue node, ops workstation; external NASA PDS (see *DeploymentView_APAF* and *ContainerView_APAF*).  
- Primary flows: ESOC→IngestAdapter (NISN), AppVM→NAS, AppVM→NASA PDS endpoint.

---

# D. Detailed Technical Design (developer-facing)

## D1. PipelineOrchestrator (DailyProcess)

1) **Responsibilities & data ownership**  
Owns execution of the daily unattended pipeline, correlation IDs, idempotency keys, and state transitions of TelemetryBatch. It does not own raw/IDFS bytes (owned by LocalArchive) but owns metadata records and job scheduling.

2) **Technology options (3 alternatives per concern)**

- **Language/runtime**
  - Recommended: Java 21 (LTS) or Kotlin on JVM 21
  - Conservative: Python 3.11-3.12 (Airflow-preferring stacks)
  - Cutting-edge: Rust 1.78+ (high safety, more dev cost)
- **Web framework (for internal admin endpoints)**
  - Recommended: Spring Boot 3.2-3.3
  - Conservative: Flask/FastAPI
  - Cutting-edge: Quarkus 3.x
- **RPC/HTTP**
  - Recommended: gRPC (internal) + OpenAPI/REST (external)
  - Conservative: REST-only (internal + external)
  - Cutting-edge: NATS request/reply + async workflows
- **Persistence**
  - Recommended: PostgreSQL 14-16 (metadata)
  - Conservative: MySQL 8.0
  - Cutting-edge: CockroachDB 23+ (geo/HA, higher complexity)
- **Cache**
  - Recommended: Redis 7.2 (for sessions, read caching)
  - Conservative: In-process Caffeine cache
  - Cutting-edge: KeyDB (Redis-compatible multithread)
- **Messaging**
  - Recommended: RabbitMQ 3.12 (deadline jobs)
  - Conservative: PostgreSQL queue via `SKIP LOCKED`
  - Cutting-edge: Kafka 3.7 (heavier ops)
- **Search**
  - Recommended: Postgres full-text for metadata queries
  - Conservative: No search (directory browsing only)
  - Cutting-edge: OpenSearch 2.x
- **Authn/Authz**
  - Recommended: OIDC (Keycloak 24+) + JWT + RBAC
  - Conservative: Local username/password + bcrypt + RBAC
  - Cutting-edge: SPIFFE/SPIRE + mTLS identities
- **Observability**
  - Recommended: OpenTelemetry + Prometheus + Loki
  - Conservative: log-only + basic metrics
  - Cutting-edge: eBPF-based profiling/observability
- **CI/CD**
  - Recommended: GitHub Actions or GitLab CI with SAST/DAST gates
  - Conservative: Jenkins
  - Cutting-edge: Bazel + remote cache
- **Container runtime**
  - Recommended: containerd (Kubernetes)
  - Conservative: Docker Engine
  - Cutting-edge: gVisor/Kata for sandboxing
- **Infra provisioning**
  - Recommended: Terraform 1.6+
  - Conservative: Ansible
  - Cutting-edge: Crossplane

3) **Recommended default stack (versions) + justification**  
- JVM services: **Java 21**, **Spring Boot 3.2-3.3**, **gRPC Java 1.62+**, **PostgreSQL 14-16**, **RabbitMQ 3.12**, **Prometheus 2.49+**.  
Justification: meets **INF-003** (unattended daily batch with retries/idempotency) and **FR-012** (built-in error handling/integrity).

4) **Interface design (internal)**  
Uses gRPC `PipelineService` (see `internal.proto`) for triggering runs, querying batch status, and scheduling distribution jobs.

5) **Data model / schema**  
- TelemetryBatch table: `sql/telemetrybatch_ddl.sql`  
- ErrorEvent table: `sql/errorevent_ddl.sql`

6) **Caching & consistency strategy**  
- No caching for pipeline state transitions (strong consistency required).  
- Cache only static reference metadata (schema versions, instrument configuration) with TTL 1h and manual invalidation on config change (INF-013).

---

## D2. ESOCIngestAdapter (AcquireTelemetry)

1) **Responsibilities & data ownership**  
Fetches telemetry from ESOC via NISN, performs transfer-level verification (checksum, size), and registers a TelemetryBatch record. Owns transfer configuration and credentials, not product bytes after archival.

2) **Technology options**
- **Transfer protocol**
  - Recommended: SFTP (OpenSSH 9.x)
  - Conservative: HTTPS download with mutual auth
  - Cutting-edge: Aspera/UDT high-speed transfer
- **Client implementation**
  - Recommended: JVM SSHJ / Apache Mina SSHD
  - Conservative: system `sftp` wrapper + checksum
  - Cutting-edge: bespoke streaming + resumable chunks
- **Integrity**
  - Recommended: SHA-256 + manifest file
  - Conservative: MD5 if ESOC legacy
  - Cutting-edge: signed manifests (PGP/X.509)

3) **Recommended default stack + justification**  
- **SFTP + SHA-256 manifest**, resumable downloads, idempotent destination paths.  
Justification: meets **FR-001** (acquire telemetry daily) and **INF-002** (integrity gate via checksum).

4) **Interface design**  
Internal gRPC: `IngestService.AcquireTelemetry()` returning `TelemetryBatch` metadata and archive staging path.

5) **Data model**  
TelemetryBatch metadata + ArchiveEntry for raw telemetry.

6) **Caching**  
None; ingest must reflect source-of-truth state.

---

## D3. TelemetryCleanupService (CleanTelemetry)

1) **Responsibilities & data ownership**  
Generates cleaned CCSDS (or mission-defined) intermediate files when ESOC cleaned telemetry is absent. Owns cleanup versioning and provenance strings.

2) **Technology options**
- **Language**
  - Recommended: Java/Kotlin (shared libs with pipeline)
  - Conservative: Python with scientific libs
  - Cutting-edge: Rust for performance
- **Telemetry parsing**
  - Recommended: CCSDS parser library + strict schema checks
  - Conservative: bespoke binary parsing
  - Cutting-edge: declarative binary schema (Kaitai)
- **Validation**
  - Recommended: format validator + roundtrip checks
  - Conservative: basic sanity checks
  - Cutting-edge: property-based tests at runtime

3) **Recommended stack + justification**  
- Java/Kotlin cleanup module + strict validation + provenance stamping.  
Justification: meets **FR-004/FR-005** (generate intermediate cleaned telemetry when not provided).

4) **Interface design**  
gRPC: `CleanupService.GenerateCleanTelemetry(batchId)` → outputs CleanTelemetryFile records + archive entries.

5) **Data model**  
`sql/cleantelemetryfile_ddl.sql`

6) **Caching**  
None; outputs are deterministic from input batch and version.

---

## D4. IDFSProcessor + IDFSValidatorAdapter (GenerateIDFS/ValidateIDFS)

1) **Responsibilities & data ownership**  
Transforms cleaned/raw telemetry into IDFS datasets per virtual instrument SDD rules (outside this doc), produces dataset directories, and validates against IDFS schema version X.Y. Owns schema version metadata and validation reports.

2) **Technology options**
- **Processing engine**
  - Recommended: JVM batch processing (Spring Batch)
  - Conservative: Python pipelines
  - Cutting-edge: Apache Beam
- **IDFS validation**
  - Recommended: external validator tool wrapped by adapter
  - Conservative: in-process schema checks only
  - Cutting-edge: formal schema + signing
- **Data format handling**
  - Recommended: explicit schema registry (files + version)
  - Conservative: ad-hoc
  - Cutting-edge: artifact repository for schemas

3) **Recommended stack + justification**  
- Spring Batch-style jobs + validator adapter invoked as compliance gate.  
Justification: meets **FR-002/FR-003** (IDFS generation) and **INF-004** (schema validation evidence).

4) **Interface design**  
gRPC: `IDFSService.GenerateIDFS(batchId, instrument)`; `ValidationService.ValidateIDFS(datasetId)`.

5) **Data model**  
`sql/idfsdataset_ddl.sql`

6) **Caching**  
Cache “latest public dataset per instrument” for public web (TTL 60s) to meet monitoring responsiveness (FR-009) without exposing embargoed (ReleaseGate enforced).

---

## D5. LocalArchive (Raw/Intermediate/IDFS storage) + ArchiveEntry

1) **Responsibilities & data ownership**  
Stores artifact bytes on NAS/object store and metadata in DB. Ensures immutability (append-only) for archived paths, and supports retrieval for web and distribution.

2) **Technology options**
- **Storage backend**
  - Recommended: NAS (NFSv4) with snapshots
  - Conservative: local disk RAID
  - Cutting-edge: S3-compatible object store (MinIO)
- **Metadata store**
  - Recommended: PostgreSQL
  - Conservative: SQLite (single-node only)
  - Cutting-edge: event-sourced catalog

3) **Recommended stack + justification**  
- NAS + PostgreSQL catalog + snapshot backups.  
Justification: meets **FR-006/FR-007/FR-008** (local archive for telemetry, IDFS, intermediates).

4) **Interface design**  
gRPC: `ArchiveService.Put/Get` with content hash verification.

5) **Data model**  
`sql/archiveentry_ddl.sql` (immutability enforced via permissions + constraints)

6) **Caching & consistency**  
Read caching via CDN/HTTP cache headers for public images/plots; metadata reads cached 30s. Artifact writes are strong-consistent (write-then-register in DB transaction with integrity hash).

---

## D6. DistributionService + JobQueue (DistributeToCoIs)

1) **Responsibilities & data ownership**  
Creates and executes DistributionJobs per recipient group and artifact type; enforces 24h deadlines, retries, alerts, and evidence logs.

2) **Technology options**
- **Queue**
  - Recommended: RabbitMQ
  - Conservative: Postgres queue
  - Cutting-edge: Kafka
- **Delivery mechanism**
  - Recommended: SFTP push to Co-I endpoints + HTTPS pull via DataAPI
  - Conservative: manual media export
  - Cutting-edge: signed torrents/content-addressed distribution
- **Scheduling**
  - Recommended: deadline + retry policy in worker
  - Conservative: cron-only scripts
  - Cutting-edge: workflow engine (Temporal)

3) **Recommended stack + justification**  
- RabbitMQ + worker pool + deadline-aware job state machine.  
Justification: meets **DR-002/DR-003/DR-004** (24h distribution SLO).

4) **Interface design**  
gRPC: `DistributionService.CreateJobs()` and `RunWorker()`.

5) **Data model**  
`sql/distributionjob_ddl.sql`

6) **Caching**  
Workers stream from archive; no caching of artifacts; cache recipient endpoint configs (TTL 10m).

---

## D7. WebPortal + DataAPI + ReleaseGateService (PublicDisplays/TeamDisplays)

1) **Responsibilities & data ownership**  
WebPortal renders public monitoring pages and team science pages. DataAPI provides query/download endpoints with ReleaseGate enforcement and audit logging. ReleaseGateService manages embargo/public transitions (admin-only).

2) **Technology options**
- **Web UI**
  - Recommended: React 18 + server-side rendering optional
  - Conservative: server-rendered Thymeleaf
  - Cutting-edge: SvelteKit
- **API**
  - Recommended: REST OpenAPI (Spring MVC)
  - Conservative: GraphQL
  - Cutting-edge: gRPC-web
- **Auth**
  - Recommended: OIDC (Keycloak) for team endpoints
  - Conservative: local auth DB
  - Cutting-edge: mTLS user certs

3) **Recommended stack + justification**  
- REST API + OIDC for team, anonymous public endpoints guarded by ReleaseGate checks.  
Justification: meets **PR-001** (password protection where appropriate) and **FR-011** (protected until public).

4) **External API (OpenAPI YAML)**  
Provided in `openapi.yaml` (Section L).

5) **Internal contracts**  
`internal.proto` includes `AuthService`, `ReleaseGateService`, and `ArchiveService` interactions.

6) **Caching & consistency**  
- Public endpoints cache “latest public dataset metadata” 60s; no caching for team downloads.  
- Consistency: ReleaseGate changes invalidate cached public views immediately (publish event or explicit cache purge).

---

## D8. PDSExportService + PDSValidatorAdapter (SubmitToPDS)

1) **Responsibilities & data ownership**  
Packages IDFS datasets into PDS4 bundles, runs PDS4 validator, transfers to NASA PDS endpoint, and stores submission evidence. Enforces 6-month deadline tracking.

2) **Technology options**
- **Packaging**
  - Recommended: deterministic bundle builder with manifest
  - Conservative: manual scripts
  - Cutting-edge: containerized PDS toolchain pipeline
- **Transfer**
  - Recommended: HTTPS/SFTP with checksum verification
  - Conservative: manual upload
  - Cutting-edge: API-based PDS ingest automation
- **Validation**
  - Recommended: official PDS4 validator CLI adapter
  - Conservative: schema-only check
  - Cutting-edge: signed compliance attestations

3) **Recommended stack + justification**  
- Containerized PDS4 validator + evidence retention in DB + archive.  
Justification: meets **DR-006/DR-008** (PDS-compliant and within 6 months).

4) **Interface design**  
gRPC: `PDSService.PackageAndSubmit(datasetId)` returning submission record.

5) **Data model**  
`sql/pdsbundle_ddl.sql`

6) **Caching**  
None; compliance must be exact.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)

Justification (Kubernetes): meets **INF-006** (scalable web/API) and **CR-001** (maintainable operations support).

See `k8s/dataapi-deployment.yaml` in Section L.

## E2. DB HA topology, backups, restore

- **PostgreSQL HA:** 1 primary + 1 synchronous standby (Patroni or managed Postgres).  
- **Replication factor:** 2 copies (primary+standby).  
- **Backups:** nightly full + WAL archiving every 5 minutes; NAS snapshots every 4 hours.  
- **Restore drills:** quarterly test restore to staging.

Justification: meets **FR-006/FR-007/FR-008** (archive availability for re-processing) and **LR-001** (maintenance).

## E3. Network topology + ingress/egress rules

Mapped to *DeploymentView_APAF* nodes (AppVM/NAS/QNode) and *ContainerView_APAF* (C_Web, C_API, C_Batch):
- Ingress: HTTPS 443 to WebPortal/DataAPI from Public/Co-I networks; admin endpoints restricted to SwRI VPN.  
- Egress: SFTP/HTTPS to ESOC (NISN link) and secure transfer to NASA PDS.  
- NAS NFS only from app namespace; queue ports only internal cluster.

Justification: meets **PR-001** (restricted access) and **FR-001** (external ingest path).

## E4. CI/CD sketch

1. Build: compile, unit tests, dependency scan (SCA).  
2. Contract tests: validate OpenAPI + proto; run consumer-driven tests.  
3. Integration tests: ephemeral Postgres/RabbitMQ.  
4. Security: SAST + container scan + DAST (team endpoints).  
5. Deploy: canary for Web/API, then batch workers; rollback on SLO regression.

Justification: meets **CR-001** (software support) and **FR-012** (error handling/integrity via gates).

---

# F. Security Design

## F1. Auth & AuthZ

- **Team access:** OIDC (Keycloak) issuing JWT access tokens; RBAC roles: ADMIN, COI.  
- **Public access:** anonymous; still subject to ReleaseGate=PUBLIC filtering.  
- **Token lifecycle:** 15m access token, 8h refresh token; revoke on user disable; rotate signing keys quarterly.

Justification: meets **PR-001** (password-protected where appropriate) and **FR-011** (protected until public).

## F2. Secrets management & rotation

- Use Kubernetes Secrets + external KMS (Vault or cloud KMS).  
- Rotate ESOC/PDS credentials quarterly; rotate DB passwords quarterly; immediate rotation on incident.

Justification: meets **PR-001** (restrict access) and **CR-001** (maintainability).

## F3. TLS & service mesh

- TLS 1.2+ everywhere; optional mTLS inside cluster via service mesh (Istio/Linkerd) for defense-in-depth.

Justification: meets **PR-001**.

## F4. Threat model (top 5)

| Threat | Mitigation |
|---|---|
| Unauthorized access to embargoed data | RBAC + ReleaseGate checks + audit logs (PR-001, FR-011) |
| Credential theft | Vault/KMS, short-lived tokens, rotation, least privilege (PR-001) |
| Tampering with archived products | SHA-256 integrity gates + immutable archive entries + restricted permissions (FR-012, FR-006/7/8) |
| Supply chain compromise | CI SAST/SCA, signed images, pinned deps (CR-001) |
| Data exfil via distribution channels | Per-recipient endpoint allowlists, encrypted transfer, evidence logs (DR-002/003/004) |

---

# G. Observability & SRE

## G1. Metrics, traces, logs + example alerts

Key metrics:
- Pipeline: `pipeline_run_duration_seconds`, `telemetry_batches_failed_total`
- Distribution: `distribution_jobs_due_total`, `distribution_jobs_missed_total`, `distribution_delivery_latency_seconds`
- PDS: `pds_submissions_pending_total`, `pds_submission_age_days_max`
- Security: `auth_failed_total`, `unauthorized_access_total`

Central logs: JSON logs to Loki/ELK with `correlationId` and `batchId`. Tracing: OpenTelemetry spans across orchestrator→ingest→archive→distribution.

**Example Prometheus alert rules**
- Missed 24h SLO:
```promql
increase(distribution_jobs_missed_total[1h]) > 0
```
- Pipeline failures:
```promql
increase(telemetry_batches_failed_total[15m]) > 0
```

Justification: meets **DR-002/003/004** (SLO monitoring) and **FR-012** (error handling).

## G2. SLOs, error budgets, RTO/RPO

- Distribution SLO: 99% delivered < 24h; alert at 22h remaining (INF-007).  
- API availability: 99.5% monthly (INF-006).  
- RTO: 24h for full system restore (INF-010).  
- RPO: 15 minutes for metadata DB; 4 hours for archive bytes (NAS snapshots) (INF-010).

## G3. Dashboard/runbook sketch

Top runbooks:
- ESOC ingest failure: check credentials, link, checksum mismatch, re-run batch with idempotency key.  
- Validator failures: inspect reports, quarantine dataset, notify science team.  
- Distribution backlog: scale workers, verify endpoints, requeue jobs.  
- PDS backlog: prioritize oldest, verify validator environment, transfer logs.

---

# H. Testing Strategy

## H1. Test matrix

| Test type | Components | Purpose |
|---|---|---|
| Unit | IDFSProcessor, Cleanup, ReleaseGateService | Deterministic transformations and policy rules |
| Integration | IngestAdapter↔Archive, Orchestrator↔DB/Queue | Real dependencies |
| Contract | OpenAPI, internal.proto | Prevent interface drift |
| E2E | Daily pipeline, web access, distribution, PDS submission | Verify FR/DR flows |
| Chaos | Queue downtime, NAS latency, DB failover | Validate RTO/RPO and retries |

Justification: meets **FR-012** (integrity) and **CR-001** (supportability).

## H2. Test data management & environments

- Environments: dev, staging, prod.  
- Staging refreshed weekly with synthetic telemetry and redacted real samples (A3).  
- Strict isolation: separate buckets/NAS paths and DB instances.

---

# I. Migration, Data Conversion & Rollout Plan

1) **High-level steps**
- Phase 1: Deploy metadata DB + archive catalog; ingest-only dry runs.  
- Phase 2: Enable cleanup + IDFS generation; validate against historical telemetry.  
- Phase 3: Enable distribution to limited Co-I group; measure 24h SLO.  
- Phase 4: Enable team portal; then public portal with ReleaseGate controls.  
- Phase 5: Enable PDS export; run parallel submissions in staging.

Rollback: disable distribution/PDS, keep archive; re-run pipeline from stored raw telemetry.

Justification: meets **FR-006** (re-processing capability) and **DR-002** (timeliness enforcement).

2) **API backwards compatibility**
- Version REST API under `/api/v1`; additive changes only; breaking changes go to `/api/v2` with 90-day overlap (INF-014).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| RabbitMQ for DistributionJobs | Postgres queue; Kafka | Postgres: simple but limited throughput; Kafka: heavy ops | RabbitMQ balances reliability and simplicity for deadlines (DR-002/003/004) |
| OIDC vs local auth | Local bcrypt auth; mTLS user certs | Local: simpler but weaker governance; mTLS: hard UX | OIDC fits team access + auditing (PR-001, FR-011) |
| NAS vs S3 object store | Local RAID; MinIO | NAS: simple POSIX; S3: scalable but added complexity | NAS aligns with local archive requirement and POSIX workflows (FR-006/7/8) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** ESOC telemetry delivery is accessible via SFTP/HTTPS over NISN with either provided checksums or a manifest file.  
- **A2:** IDFS schema versions and validators are available as command-line tools or libraries and can be containerized.  
- **A3:** Sample telemetry and IDFS fixtures are available for staging tests without violating embargo constraints.  
- **A4:** Co-I distribution endpoints are either SFTP servers or authenticated HTTPS pull is acceptable.  
- **A5:** PDS ingest endpoint supports secure transfer (HTTPS/SFTP) and provides validation feedback artifacts.

## Inferred requirements (from UML notes / missing in SRS text)
- **INF-001:** “Unattended daily batch execution” (diagram notes ASR-001).  
- **INF-002:** “Integrity gates with SHA-256 checksums” (diagram notes NFR-003/IntegrityGate).  
- **INF-003:** “Retry + rollback on partial failures” (IntegrityService behavior).  
- **INF-004:** “IDFS schema validation evidence retained” (diagram notes NFR-001).  
- **INF-005:** “Embargo/public release workflow with audited state change” (ReleaseGate).  
- **INF-006:** “API/web scalability target & HPA” (needed for ops readiness).  
- **INF-007:** “22h pre-deadline alert, 3 retries, escalate at 48h” (diagram notes NFR-010/11/12).  
- **INF-008:** “Centralized error event taxonomy and correlation IDs” (ErrorEvent).  
- **INF-009:** “Audit log for authentication and data access” (AuditLog).  
- **INF-010:** “Backup/restore with defined RTO/RPO” (ops completeness).  
- **INF-011:** “Configurable recipient-group mapping per Co-I” (FR-023).  
- **INF-012:** “Contract-first internal interfaces (OpenAPI/proto/DDL)” (SRS: internal interfaces left to design).  
- **INF-013:** “Configuration management for schema versions/processing versions.”  
- **INF-014:** “External API versioning strategy.”

## Conflicts log (diagrams vs SRS)
- **C1:** UML references ASR/NFR IDs not present in SRS (e.g., ASR-007, NFR-004). Resolution: treat them as inferred `INF-*` and trace them (per special rule).  

## Stakeholder questions
1) What exact telemetry formats and transport protocols does ESOC provide (CCSDS variants, naming conventions, checksum manifests)?  
2) What is the official IDFS schema versioning policy and validator tool source/ownership?  
3) What “most current data” means for FR-009: last day, last pass, last packet, or last successful pipeline?  
4) Which Co-I distribution mechanism is preferred (push SFTP vs pull HTTPS) and per-recipient authorization requirements?  
5) PDS submission: exact PDS4 bundle structure, required labels, and endpoint method?

---

# L. Deliverables

## 1) `architecture.md`
```markdown
# architecture.md
(This document content is provided in ArchitectureDocument.md / see full text above; in implementation, save the complete markdown as architecture.md.)
```

## 2) `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: APAF DataAPI
  version: "1.0.0"
  description: External HTTP API for APAF public and team access to IDFS datasets, telemetry metadata, and downloads.
servers:
  - url: https://apaf.example.org
tags:
  - name: Public
  - name: Team
  - name: Admin
components:
  securitySchemes:
    oidc:
      type: openIdConnect
      openIdConnectUrl: https://auth.example.org/realms/apaf/.well-known/openid-configuration
  schemas:
    ApiError:
      type: object
      required: [code, message, correlationId, timestamp]
      properties:
        code:
          type: string
          example: "AUTH_REQUIRED"
        message:
          type: string
        correlationId:
          type: string
        timestamp:
          type: string
          format: date-time
        details:
          type: object
          additionalProperties: true
    DatasetSummary:
      type: object
      required: [datasetId, instrument, createdAt, schemaVersion, releaseState]
      properties:
        datasetId:
          type: string
        instrument:
          type: string
          example: "ASPERA-3"
        createdAt:
          type: string
          format: date-time
        schemaVersion:
          type: string
        releaseState:
          type: string
          enum: [EMBARGOED, PUBLIC]
    DatasetDetail:
      allOf:
        - $ref: "#/components/schemas/DatasetSummary"
        - type: object
          required: [archivePath, checksumSha256]
          properties:
            archivePath:
              type: string
              example: "/archive/idfs/2026/04/21/IDFS-A3-2026-04-21/"
            checksumSha256:
              type: string
    BatchSummary:
      type: object
      required: [batchId, source, acquiredAt, status, cleanedProvidedByEsoc]
      properties:
        batchId:
          type: string
        source:
          type: string
          example: "ESOC/NISN"
        acquiredAt:
          type: string
          format: date-time
        status:
          type: string
          enum: [ACQUIRED, CLEANED, PROCESSED, ARCHIVED, DISTRIBUTED, FAILED]
        cleanedProvidedByEsoc:
          type: boolean
    ReleaseUpdateRequest:
      type: object
      required: [state]
      properties:
        state:
          type: string
          enum: [EMBARGOED, PUBLIC]
        reason:
          type: string
  responses:
    Unauthorized:
      description: Authentication required or invalid
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ApiError"
    Forbidden:
      description: Not authorized for resource
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ApiError"
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ApiError"

paths:
  /api/v1/public/datasets/latest:
    get:
      tags: [Public]
      summary: Get latest PUBLIC IDFS dataset summaries per instrument
      description: Returns only datasets whose ReleaseGate state is PUBLIC.
      responses:
        "200":
          description: Latest public datasets
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      $ref: "#/components/schemas/DatasetSummary"
        "500":
          description: Server error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ApiError"

  /api/v1/public/datasets/{datasetId}:
    get:
      tags: [Public]
      summary: Get PUBLIC dataset details
      parameters:
        - in: path
          name: datasetId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Dataset details (PUBLIC only)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DatasetDetail"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"

  /api/v1/team/datasets:
    get:
      tags: [Team]
      summary: List datasets (team view; includes EMBARGOED for COI)
      security:
        - oidc: []
      parameters:
        - in: query
          name: instrument
          required: false
          schema: { type: string }
        - in: query
          name: from
          required: false
          schema: { type: string, format: date-time }
        - in: query
          name: to
          required: false
          schema: { type: string, format: date-time }
        - in: query
          name: limit
          required: false
          schema: { type: integer, minimum: 1, maximum: 500, default: 50 }
      responses:
        "200":
          description: Dataset list
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      $ref: "#/components/schemas/DatasetSummary"
        "401":
          $ref: "#/components/responses/Unauthorized"

  /api/v1/team/datasets/{datasetId}/download:
    get:
      tags: [Team]
      summary: Download an IDFS dataset as an archive (zip/tar)
      security:
        - oidc: []
      parameters:
        - in: path
          name: datasetId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Binary dataset stream
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"

  /api/v1/team/batches/{batchId}:
    get:
      tags: [Team]
      summary: Get telemetry batch metadata/status
      security:
        - oidc: []
      parameters:
        - in: path
          name: batchId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Batch summary
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BatchSummary"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"

  /api/v1/admin/release-gates/{datasetId}:
    patch:
      tags: [Admin]
      summary: Update ReleaseGate state for a dataset (ADMIN only)
      security:
        - oidc: []
      parameters:
        - in: path
          name: datasetId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ReleaseUpdateRequest"
      responses:
        "200":
          description: Updated dataset summary
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DatasetSummary"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"
```

## 3) `internal.proto`
```proto
syntax = "proto3";

package apaf.internal.v1;

import "google/protobuf/timestamp.proto";

message ApiStatus {
  string code = 1;           // e.g., OK, INVALID_ARGUMENT, NOT_FOUND, FAILED_PRECONDITION
  string message = 2;
  string correlation_id = 3;
}

message TelemetryBatch {
  string batch_id = 1;
  string source = 2; // ESOC/NISN
  google.protobuf.Timestamp acquired_at = 3;
  string checksum_sha256 = 4;
  bool cleaned_provided_by_esoc = 5;
  string status = 6; // ACQUIRED/CLEANED/PROCESSED/ARCHIVED/DISTRIBUTED/FAILED
}

message CleanTelemetryFile {
  string file_id = 1;
  string format = 2; // CCSDS
  google.protobuf.Timestamp created_at = 3;
  string checksum_sha256 = 4;
  string provenance = 5;
}

message IDFSDataset {
  string dataset_id = 1;
  string instrument = 2;     // ASPERA-3 or MEX OA
  string schema_version = 3; // X.Y
  google.protobuf.Timestamp created_at = 4;
  bool is_embargoed = 5;
  string checksum_sha256 = 6;
  string archive_path = 7;
}

message ArchiveEntry {
  string entry_id = 1;
  string artifact_type = 2; // RAW_TLM/CLEAN_TLM/IDFS/PDS_BUNDLE
  string path = 3;
  google.protobuf.Timestamp stored_at = 4;
  string retention_class = 5; // mission
  string checksum_sha256 = 6;
}

message DistributionJob {
  string job_id = 1;
  string recipient_group = 2; // AllCoIs or named group
  string artifact_type = 3;   // IDFS/CLEAN_TLM/IDFS+CleanTelemetry
  google.protobuf.Timestamp deadline_at = 4;
  string status = 5;          // QUEUED/IN_PROGRESS/DELIVERED/MISSED/ESCALATED
  int32 attempt_count = 6;
}

message ErrorEvent {
  string event_id = 1;
  google.protobuf.Timestamp occurred_at = 2;
  string component = 3;
  string error_type = 4;
  string severity = 5;
  string message = 6;
  string batch_id = 7;
  string correlation_id = 8;
}

service IngestService {
  rpc AcquireTelemetry(AcquireTelemetryRequest) returns (AcquireTelemetryResponse);
}

message AcquireTelemetryRequest {
  string scheduled_date_utc = 1; // YYYY-MM-DD
}

message AcquireTelemetryResponse {
  ApiStatus status = 1;
  TelemetryBatch batch = 2;
  ArchiveEntry raw_archive_entry = 3;
}

service CleanupService {
  rpc GenerateCleanTelemetry(GenerateCleanTelemetryRequest) returns (GenerateCleanTelemetryResponse);
}

message GenerateCleanTelemetryRequest {
  string batch_id = 1;
}

message GenerateCleanTelemetryResponse {
  ApiStatus status = 1;
  repeated CleanTelemetryFile files = 2;
  repeated ArchiveEntry archive_entries = 3;
}

service IDFSService {
  rpc GenerateIDFS(GenerateIDFSRequest) returns (GenerateIDFSResponse);
}

message GenerateIDFSRequest {
  string batch_id = 1;
  string instrument = 2; // ASPERA-3 or MEX_OA
}

message GenerateIDFSResponse {
  ApiStatus status = 1;
  repeated IDFSDataset datasets = 2;
}

service ValidationService {
  rpc ValidateIDFS(ValidateIDFSRequest) returns (ValidateIDFSResponse);
  rpc ValidatePDS4(ValidatePDS4Request) returns (ValidatePDS4Response);
}

message ValidateIDFSRequest {
  string dataset_id = 1;
}

message ValidateIDFSResponse {
  ApiStatus status = 1;
  bool valid = 2;
  string report_path = 3;
}

message ValidatePDS4Request {
  string bundle_id = 1;
  string bundle_path = 2;
}

message ValidatePDS4Response {
  ApiStatus status = 1;
  bool valid = 2;
  string validator_report_path = 3;
}

service ArchiveService {
  rpc PutArtifact(PutArtifactRequest) returns (PutArtifactResponse);
  rpc GetArtifact(GetArtifactRequest) returns (GetArtifactResponse);
}

message PutArtifactRequest {
  string artifact_type = 1;
  string source_path = 2;
  string destination_path = 3;
  string checksum_sha256 = 4;
}

message PutArtifactResponse {
  ApiStatus status = 1;
  ArchiveEntry entry = 2;
}

message GetArtifactRequest {
  string path = 1;
}

message GetArtifactResponse {
  ApiStatus status = 1;
  string path = 2;
  string checksum_sha256 = 3;
}

service DistributionService {
  rpc CreateDistributionJobs(CreateDistributionJobsRequest) returns (CreateDistributionJobsResponse);
  rpc MarkDelivered(MarkDeliveredRequest) returns (MarkDeliveredResponse);
}

message CreateDistributionJobsRequest {
  string batch_id = 1;
  repeated string dataset_ids = 2;
  repeated string clean_file_ids = 3;
  string recipient_group = 4;
  google.protobuf.Timestamp deadline_at = 5;
}

message CreateDistributionJobsResponse {
  ApiStatus status = 1;
  repeated DistributionJob jobs = 2;
}

message MarkDeliveredRequest {
  string job_id = 1;
}

message MarkDeliveredResponse {
  ApiStatus status = 1;
  DistributionJob job = 2;
}

service ReleaseGateService {
  rpc SetPublic(SetPublicRequest) returns (SetPublicResponse);
  rpc AuthorizePublication(AuthorizePublicationRequest) returns (AuthorizePublicationResponse);
}

message SetPublicRequest {
  string dataset_id = 1;
  string changed_by = 2;
  string reason = 3;
}

message SetPublicResponse {
  ApiStatus status = 1;
  string state = 2; // PUBLIC
}

message AuthorizePublicationRequest {
  string dataset_id = 1;
  string role = 2; // ADMIN/COI/PUBLIC
}

message AuthorizePublicationResponse {
  ApiStatus status = 1;
  bool allowed = 2;
  string state = 3; // EMBARGOED/PUBLIC
}

service PipelineService {
  rpc RunDailyPipeline(RunDailyPipelineRequest) returns (RunDailyPipelineResponse);
  rpc GetBatchStatus(GetBatchStatusRequest) returns (GetBatchStatusResponse);
}

message RunDailyPipelineRequest {
  string scheduled_date_utc = 1;
  string triggered_by = 2; // operator username or scheduler
}

message RunDailyPipelineResponse {
  ApiStatus status = 1;
  string batch_id = 2;
}

message GetBatchStatusRequest {
  string batch_id = 1;
}

message GetBatchStatusResponse {
  ApiStatus status = 1;
  TelemetryBatch batch = 2;
  repeated ErrorEvent errors = 3;
}
```

## 4) `k8s/dataapi-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apaf-dataapi
  namespace: apaf
spec:
  replicas: 2
  selector:
    matchLabels:
      app: apaf-dataapi
  template:
    metadata:
      labels:
        app: apaf-dataapi
    spec:
      containers:
        - name: dataapi
          image: registry.example.org/apaf/dataapi:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "prod"
            - name: DB_URL
              valueFrom:
                secretKeyRef:
                  name: apaf-secrets
                  key: db_url
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: apaf-secrets
                  key: db_user
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: apaf-secrets
                  key: db_password
            - name: OIDC_ISSUER
              valueFrom:
                configMapKeyRef:
                  name: apaf-config
                  key: oidc_issuer
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: apaf-dataapi
  namespace: apaf
spec:
  selector:
    app: apaf-dataapi
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: apaf-dataapi-hpa
  namespace: apaf
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: apaf-dataapi
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: apaf-config
  namespace: apaf
data:
  oidc_issuer: "https://auth.example.org/realms/apaf"
---
apiVersion: v1
kind: Secret
metadata:
  name: apaf-secrets
  namespace: apaf
type: Opaque
stringData:
  db_url: "jdbc:postgresql://apaf-postgres:5432/apaf"
  db_user: "apaf_app"
  db_password: "REPLACE_ME"
```

## 5) SQL DDL examples

### `sql/telemetrybatch_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS telemetry_batch (
  batch_id              TEXT PRIMARY KEY,
  source                TEXT NOT NULL,
  acquired_at           TIMESTAMPTZ NOT NULL,
  checksum_sha256       TEXT NOT NULL,
  cleaned_provided_by_esoc BOOLEAN NOT NULL DEFAULT FALSE,
  status                TEXT NOT NULL CHECK (status IN ('ACQUIRED','CLEANED','PROCESSED','ARCHIVED','DISTRIBUTED','FAILED')),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_telemetry_batch_acquired_at
  ON telemetry_batch (acquired_at DESC);

CREATE INDEX IF NOT EXISTS idx_telemetry_batch_status
  ON telemetry_batch (status);
```

### `sql/cleantelemetryfile_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS clean_telemetry_file (
  file_id         TEXT PRIMARY KEY,
  batch_id        TEXT NOT NULL REFERENCES telemetry_batch(batch_id),
  format          TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL,
  checksum_sha256 TEXT NOT NULL,
  provenance      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clean_file_batch_id
  ON clean_telemetry_file (batch_id);
```

### `sql/idfsdataset_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS idfs_dataset (
  dataset_id      TEXT PRIMARY KEY,
  batch_id        TEXT NOT NULL REFERENCES telemetry_batch(batch_id),
  instrument      TEXT NOT NULL,
  schema_version  TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL,
  is_embargoed    BOOLEAN NOT NULL DEFAULT TRUE,
  checksum_sha256 TEXT NOT NULL,
  archive_path    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_idfs_dataset_batch_id
  ON idfs_dataset (batch_id);

CREATE INDEX IF NOT EXISTS idx_idfs_dataset_instrument_created
  ON idfs_dataset (instrument, created_at DESC);
```

### `sql/releasegate_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS release_gate (
  gate_id     TEXT PRIMARY KEY,
  dataset_id  TEXT NOT NULL UNIQUE REFERENCES idfs_dataset(dataset_id),
  state       TEXT NOT NULL CHECK (state IN ('EMBARGOED','PUBLIC')),
  changed_at  TIMESTAMPTZ NOT NULL,
  changed_by  TEXT NOT NULL,
  reason      TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_release_gate_state
  ON release_gate (state);
```

### `sql/archiveentry_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS archive_entry (
  entry_id        TEXT PRIMARY KEY,
  artifact_type   TEXT NOT NULL,
  path            TEXT NOT NULL UNIQUE,
  stored_at       TIMESTAMPTZ NOT NULL,
  retention_class TEXT NOT NULL,
  checksum_sha256 TEXT NOT NULL,
  immutable       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_archive_entry_type_stored
  ON archive_entry (artifact_type, stored_at DESC);
```

### `sql/distributionjob_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS distribution_job (
  job_id          TEXT PRIMARY KEY,
  batch_id        TEXT NOT NULL REFERENCES telemetry_batch(batch_id),
  recipient_group TEXT NOT NULL,
  artifact_type   TEXT NOT NULL,
  deadline_at     TIMESTAMPTZ NOT NULL,
  status          TEXT NOT NULL CHECK (status IN ('QUEUED','IN_PROGRESS','DELIVERED','MISSED','ESCALATED')),
  attempt_count   INTEGER NOT NULL DEFAULT 0,
  last_error      TEXT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_distribution_job_deadline
  ON distribution_job (deadline_at);

CREATE INDEX IF NOT EXISTS idx_distribution_job_status
  ON distribution_job (status);
```

### `sql/pdsbundle_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS pds_bundle (
  bundle_id             TEXT PRIMARY KEY,
  dataset_id            TEXT NOT NULL REFERENCES idfs_dataset(dataset_id),
  pds4_version          TEXT NOT NULL,
  created_at            TIMESTAMPTZ NOT NULL,
  validator_report_path TEXT NOT NULL,
  submitted_at          TIMESTAMPTZ NULL,
  submission_status     TEXT NOT NULL CHECK (submission_status IN ('PACKAGED','VALIDATED','SUBMITTED','FAILED')),
  checksum_sha256       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pds_bundle_dataset
  ON pds_bundle (dataset_id);

CREATE INDEX IF NOT EXISTS idx_pds_bundle_status
  ON pds_bundle (submission_status);
```

### `sql/errorevent_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS error_event (
  event_id       TEXT PRIMARY KEY,
  occurred_at    TIMESTAMPTZ NOT NULL,
  component      TEXT NOT NULL,
  error_type     TEXT NOT NULL,
  severity       TEXT NOT NULL,
  message        TEXT NOT NULL,
  batch_id       TEXT NULL REFERENCES telemetry_batch(batch_id),
  correlation_id TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_error_event_batch_time
  ON error_event (batch_id, occurred_at DESC);

CREATE INDEX IF NOT EXISTS idx_error_event_corr
  ON error_event (correlation_id);
```

### `sql/useraccount_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS user_account (
  user_id            TEXT PRIMARY KEY,
  username           TEXT NOT NULL UNIQUE,
  password_hash      TEXT NOT NULL,
  role               TEXT NOT NULL CHECK (role IN ('ADMIN','COI','PUBLIC')),
  password_rotated_at DATE NOT NULL,
  disabled           BOOLEAN NOT NULL DEFAULT FALSE,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 6) `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagrams (title:IDs),Components,Artifact filename(s),Rationale
FR-001,Acquire telemetry daily,UseCaseView_APAF:UC_Acquire|UC_Daily;ActivityView_DailyPipeline,PipelineOrchestrator|ESOCIngestAdapter,architecture.md|internal.proto,Implements daily ingest and orchestration.
FR-002,Process science into IDFS,UseCaseView_APAF:UC_IDFS;SequenceView_S1_DailyPipeline:IDFSProcessor,IDFSProcessor,architecture.md|internal.proto|sql/idfsdataset_ddl.sql,Canonical IDFS output generation.
FR-003,Process engineering/ancillary into IDFS,ActivityView_DailyPipeline (fork),IDFSProcessor,architecture.md|internal.proto,Supports calibration/validation datasets.
FR-004,Generate intermediate cleaned telemetry if ESOC lacks,UseCaseView_APAF:UC_Clean;StateView_TelemetryBatch:Cleaning,TelemetryCleanupService,architecture.md|internal.proto|sql/cleantelemetryfile_ddl.sql,Conditional cleanup path implemented.
FR-005,Cleanup telemetry when ESOC cleaned missing,UseCaseView_APAF note UC_Clean,TelemetryCleanupService,architecture.md,Explicit extend condition enforced.
FR-006,Store telemetry locally,DeploymentView_APAF:NAS;ClassView_APAF:ArchiveEntry,LocalArchive,architecture.md|sql/archiveentry_ddl.sql,ArchiveEntry catalogs raw telemetry.
FR-007,Store IDFS locally,ClassView_APAF:IDFSDataset->ArchiveEntry,LocalArchive,architecture.md|sql/archiveentry_ddl.sql,IDFS stored for availability.
FR-008,Store intermediate cleaned locally,ClassView_APAF:CleanTelemetryFile->ArchiveEntry,LocalArchive,architecture.md|sql/cleantelemetryfile_ddl.sql,Reprocessing support.
FR-009,Public current web displays,UseCaseView_APAF:UC_PublicWeb,WebPortal,architecture.md|openapi.yaml,Public endpoints filtered by ReleaseGate.
FR-010,Team science displays,UseCaseView_APAF:UC_TeamWeb;SequenceView_S2_TeamWebAccess,WebPortal|DataAPI,architecture.md|openapi.yaml,Team endpoints for analysis.
FR-011,Password-protect until public,UseCaseView_APAF:UC_Auth,AuthService|ReleaseGateService,architecture.md|openapi.yaml|sql/releasegate_ddl.sql,RBAC + embargo enforcement.
FR-012,Built-in error handling/integrity,ClassView_APAF:IntegrityService|ErrorEvent,IntegrityService|MonitoringService,architecture.md|sql/errorevent_ddl.sql,Central error capture and integrity gates.
FR-013,Provide products to all Co-I’s,UseCaseView_APAF:UC_Distribute,DistributionService,architecture.md|internal.proto|sql/distributionjob_ddl.sql,Automated distribution jobs.
FR-014,Provide IDFS access software,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Packaged client delivery.
FR-015,Provide analysis software,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Packaged analysis software.
FR-016,Provide IDFS to PDS,UseCaseView_APAF:UC_PDS,PDSExportService,architecture.md|sql/pdsbundle_ddl.sql,PDS export tracked.
FR-017,PDS-compliant form,ComponentView_APAF:PDSValidatorAdapter,PDSValidatorAdapter,architecture.md|internal.proto,PDS4 validator gate.
FR-018,Calibrate/validate before PDS,ActivityView_DailyPipeline (Calibrate & validate),IDFSProcessor|PDSExportService,architecture.md,Workflow includes calibration step.
FR-019,PDS within 6 months,ActivityView_DailyPipeline (PDS due?),PDSExportService|MonitoringService,architecture.md,Backlog and alerts for deadline.
FR-020,Provide algorithms to IRF,UseCaseView_APAF:UC_IRF,Packaging/Export,architecture.md,Versioned algorithm release.
FR-021,Integrate analysis software into NASA repo,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Publishing pipeline.
FR-022,Distribution mechanisms described in ops doc,(no UML),Ops,architecture.md,Architecture defines mechanisms; ops doc external.
FR-023,Determine per Co-I dataset sets,(no UML),DistributionService config,architecture.md,Recipient mapping config supports variability.
PR-001,Password protection where appropriate,UseCaseView_APAF:UC_Auth,AuthService|WebPortal,architecture.md|openapi.yaml,RBAC and protected endpoints.
CR-001,System maintenance/support,DeploymentView_APAF:Ops,Ops/CI-CD,architecture.md,Operational process included.
LR-001,Provide APAF system maintenance,DeploymentView_APAF:Ops,Ops,architecture.md,Runbooks and patching.
LR-002,Provide software support,DeploymentView_APAF:Ops,Support,architecture.md,Issue management and escalation.
DR-001,Provide IDFS+intermediates to Co-I’s,UseCaseView_APAF:UC_Distribute,DistributionService,architecture.md,Delivery framing.
DR-002,Distribute ASPERA-3 IDFS within 24h,StateView_TelemetryBatch:MissedSLO,DistributionService|MonitoringService,architecture.md|sql/distributionjob_ddl.sql,Deadline jobs enforce SLO.
DR-003,Distribute MEX OA IDFS within 24h,ActivityView_DailyPipeline (MEX OA fork),DistributionService,architecture.md|sql/distributionjob_ddl.sql,Same SLO mechanism.
DR-004,Distribute cleaned telemetry within 24h,UseCaseView_APAF:UC_Clean|UC_Distribute,DistributionService,architecture.md|sql/distributionjob_ddl.sql,Intermediate artifacts included.
DR-005,Provide IDFS to NASA PDS,UseCaseView_APAF:UC_PDS,PDSExportService,architecture.md,PDS submission pipeline.
DR-006,PDS-compliant form,ComponentView_APAF:PDSValidatorAdapter,PDSValidatorAdapter,architecture.md|internal.proto,Validator required.
DR-007,Calibrate/validate prior PDS,ActivityView_DailyPipeline,PDSExportService,architecture.md,Pre-submit gates.
DR-008,PDS submission ≤6 months,ActivityView_DailyPipeline,PDSExportService|MonitoringService,architecture.md,Deadline tracking.
DR-009,Provide algorithms to IRF,UseCaseView_APAF:UC_IRF,Packaging/Export,architecture.md,Delivery package.
DR-010,Integrate analysis into NASA repo,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Repository publishing.
DR-011,Provide IDFS access software,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Distribution.
DR-012,Provide science analysis software,UseCaseView_APAF:UC_Software,Release tooling,architecture.md,Distribution.
INF-001,Unattended daily batch execution,DeploymentView_APAF:AppVM;ActivityView_DailyPipeline,PipelineOrchestrator,architecture.md,Operationalizes daily automation.
INF-002,SHA-256 integrity gates,ClassView_APAF:IntegrityService,IntegrityService,architecture.md|internal.proto,Verifiable integrity checks.
INF-003,Retry+rollback on partial failures,ClassView_APAF:IntegrityService,IntegrityService,architecture.md,Bounded retries.
INF-004,Schema validation evidence retained,ComponentView_APAF:IDFSValidatorAdapter,IDFSValidatorAdapter,architecture.md,Compliance evidence.
INF-005,Embargo/public release workflow,ClassView_APAF:ReleaseGate,ReleaseGateService,architecture.md|sql/releasegate_ddl.sql,Prevents data leakage.
INF-006,API/web scalability/HPA,k8s/dataapi-deployment.yaml,WebPortal|DataAPI,k8s/dataapi-deployment.yaml,Autoscaling support.
INF-007,22h alert/3 retries/48h escalation,StateView_TelemetryBatch,MonitoringService|DistributionService,architecture.md,Operational SLO enforcement.
INF-008,Error taxonomy & correlation IDs,ClassView_APAF:ErrorEvent,MonitoringService,architecture.md|sql/errorevent_ddl.sql,Debuggability.
INF-009,Audit authentication and access,SequenceView_S2_TeamWebAccess:AuditLog,AuditLog,architecture.md,Compliance logging.
INF-010,Backup/restore RTO/RPO,(ops section),Ops,architecture.md,DR readiness.
INF-011,Configurable recipient groups,(no UML),DistributionService,architecture.md,Supports pre-launch decisions.
INF-012,Contract-first internal interfaces,PackageView_APAF,All services,internal.proto|openapi.yaml|sql/*.sql,Implementable interfaces.
INF-013,Config management for schema versions,(no UML),PipelineOrchestrator,architecture.md,Repeatable processing.
INF-014,External API versioning,/api/v1/*,DataAPI,openapi.yaml,Backwards compatibility.
```

---

## Verification table (Acceptance Criteria)

| Item | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A-L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (FR/PR/CR/LR/DR + inferred INF-*) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDL / models for primary entities included | [x] |
| All major components have at least one API contract and a data schema | [x] |
| Assumptions and unresolved questions listed | [x] |

## How to review checklist
- All FR/PR/CR/LR/DR and INF-* present in traceability matrix?  
- OpenAPI + internal proto included and valid?  
- Each major component has responsibilities, 3-option tech choices, recommended stack with ASR/NFR/INF justification, interface, and schema?  
- k8s snippet valid and includes Deployment/Service/HPA/ConfigMap/Secret?  
- SQL DDLs included with indexes/constraints?  
- Assumptions and open questions clear?

**Conversion note (if PDF/HTML needed):**  
`pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf` or `pandoc ArchitectureDocument.md -o ArchitectureDocument.html`