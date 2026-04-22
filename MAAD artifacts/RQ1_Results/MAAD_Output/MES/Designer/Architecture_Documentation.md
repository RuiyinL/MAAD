Analysis Plan  
Scope: Design a production-ready APAF ground data system architecture for telemetry acquisition, IDFS processing, archiving, web displays, distribution, and PDS submission.  
Approach: Normalize narrative SRS into atomic INF-* requirements, bind them to contracts (OpenAPI/gRPC), schemas (SQL), and the provided 11 UML views (4+1).  
Top validation steps: Traceability matrix completeness, contract/schema syntactic validation, and ops/SRE verification against timing/retention/security constraints.

# A. Executive Summary (≤1 page)

## System overview
APAF (ASPERA-3 Processing and Archiving Facility) is an on-prem SwRI ground data system that (1) acquires daily telemetry from ESOC, (2) processes science + engineering/ancillary data into IDFS datasets, (3) archives raw/cleaned/intermediate/IDFS artifacts locally, (4) provides public and team web displays, (5) distributes datasets to Co-Is, and (6) submits validated PDS-compliant packages to NASA PDS within 6 months.

Primary diagram mapping (one-line): End-to-end behavior is captured by **UseCase_APAF:UC_Acquire/UC_Process/UC_Archive/UC_Distribute/UC_PublicWeb/UC_TeamWeb/UC_PDS** and runtime flow by **Activity_DailyPipeline** and **Sequence_S1_DailyIngestProcess**.

## Architectural style(s) and deployment topology
- Style: **Modular monolith + hexagonal adapters** (clear boundaries: ingestion/processing/archiving/web/security/observability).  
- Topology: **SwRI on-prem single Kubernetes cluster + NAS archives + external integrations to ESOC/PDS/Co-Is** (Deployment_APAF:AppVM/NAS/Backup).

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---:|---|
| Ambiguous legacy SRS lacks stable IDs and measurable NFRs | High | Normalize into **INF-FR/INF-NFR/INF-ASR** with acceptance criteria; enforce contract-first (OpenAPI + proto) and schema validation gates (B, D4, D5). |
| Daily pipeline timing + conditional 24h delivery | High | Scheduler + idempotent jobs + retries; quarantine on integrity failures; distribution queue with retry/receipt confirmation (Activity_DailyPipeline, Class_APAF:DistributionJob). |
| Mixed public vs restricted web access | High | OIDC/MFA for team portal, RBAC, audit logs retention; separate public endpoints; session timeout (UseCase_APAF:UC_TeamWeb note; Class_APAF:UserAccount/AuditLogEntry). |

## Key QA coverage mapping (ASR/NFR → test types)
Because the SRS does not provide explicit NFR/ASR IDs, this architecture introduces **INF-NFR/INF-ASR** (listed in K) and maps them to tests.

| Quality attribute | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-AVAIL-001, INF-NFR-PERF-002 | Load tests (k6), HPA tests, DB index tests |
| Availability | INF-NFR-AVAIL-001, INF-ASR-ARCH-001 | Chaos tests (pod kill), backup/restore drills |
| Security | INF-PR-001, INF-NFR-SEC-001..004 | SAST/DAST, authZ tests, audit log verification |
| Performance | INF-NFR-PERF-001..003 | Pipeline timing E2E, web refresh latency tests |
| Maintainability | INF-CR-001, INF-LR-001..002 | Contract tests, schema migration tests, runbook drills |

---

# B. Traceability & Rationale

## Conflict log (requirements vs diagrams)
- The UML diagrams reference **NFR/ASR IDs (e.g., NFR-001, ASR-006)** that do **not** exist in the provided SRS text. Per rule, we prefer the SRS and **infer** IDs as **INF-***, while keeping diagram IDs as non-authoritative annotations. Logged in K.

## Traceability matrix (CSV)
(Also delivered as `traceability_matrix.csv` in section L.)

**Legend**: Diagram references use `Title:ElementIDs`. Artifact filenames are those delivered in section L.

Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale
---|---|---|---|---|---
INF-FR-001 | Acquire ASPERA-3 + MEX Orbit/Attitude telemetry from ESOC daily and auto-process | UseCase_APAF:UC_Acquire; Activity_DailyPipeline; Sequence_S1_DailyIngestProcess | TelemetryIngestionService, ESOCAdapter, Scheduler | architecture.md; internal.proto | Core mission function; drives ingestion adapter, scheduling, and idempotent acquisition.
INF-FR-002 | Process all ASPERA-3 science data into IDFS datasets | UseCase_APAF:UC_Process; Activity_DailyPipeline | IDFSProcessingService, SchemaValidationService | architecture.md; internal.proto; sql/idfs_dataset_ddl.sql | Establishes processing pipeline and schema validation for science products.
INF-FR-003 | Process engineering + ancillary info for calibration/validation into IDFS | UseCase_APAF:UC_Process; Activity_DailyPipeline | IDFSProcessingService | architecture.md; sql/idfs_dataset_ddl.sql | Ensures calibration/ancillary products exist for scientific usability.
INF-FR-004 | Generate intermediate cleaned telemetry if ESOC cleaned telemetry not provided | UseCase_APAF:UC_Clean; Activity_DailyPipeline | TelemetryCleaningService | architecture.md; internal.proto; sql/cleaned_telemetry_file_ddl.sql | Supports mission goals when ESOC does not provide cleaned telemetry.
INF-FR-005 | Store raw telemetry locally for availability and re-processing | UseCase_APAF:UC_Archive; Deployment_APAF:NAS/dRaw | ArchiveService, RawTelemetryArchive | architecture.md; sql/telemetry_file_ddl.sql | Enables reprocessing and auditability; required by SRS.
INF-FR-006 | Store IDFS datasets locally for availability and analysis | UseCase_APAF:UC_Archive; Deployment_APAF:NAS/dIDFS | ArchiveService, IDFSArchive | architecture.md; sql/idfs_dataset_ddl.sql | Local archive is primary analysis source for team and web.
INF-FR-007 | Store intermediate cleaned telemetry locally | UseCase_APAF:UC_Archive | ArchiveService, IntermediateArchive | architecture.md; sql/cleaned_telemetry_file_ddl.sql | Required for reprocessing and team support.
INF-FR-008 | Provide public web displays of most current data to monitor performance | UseCase_APAF:UC_PublicWeb; Container_APAF:WebPortal | WebPortal, IDFSQueryService | architecture.md; openapi.yaml | Public transparency; requires fast refresh and safe read-only access.
INF-FR-009 | Provide team-defined web displays using any available data for science analysis | UseCase_APAF:UC_TeamWeb; Sequence_S2_TeamWebAccess | WebPortal, IDFSQueryService, AuthService | architecture.md; openapi.yaml | Enables science analysis; requires query flexibility and access control.
INF-FR-010 | Password protect team web displays until data is public | UseCase_APAF:UC_TeamWeb note | AuthService, WebPortal | architecture.md; openapi.yaml | Implements privacy requirement and embargo period.
INF-FR-011 | Built-in error handling for data integrity | UseCase_APAF:UC_Alert; State_IDFSDataset:L | MonitoringAlertingService, QuarantineStore | architecture.md; internal.proto; sql/quarantine_item_ddl.sql | Quarantine + alerting prevents silent corruption and supports recovery.
INF-FR-012 | Provide IDFS + intermediate files to all Co-Is | UseCase_APAF:UC_Distribute | DistributionService | architecture.md; openapi.yaml | Distribution is a primary deliverable; requires job tracking and receipts.
INF-FR-013 | Provide IDFS data access software to Co-Is | UseCase_APAF:UC_AccessSW | Release/Packaging (out-of-band) | architecture.md | Delivered as artifacts; tracked as release deliverable.
INF-FR-014 | Provide science analysis software to Co-Is | UseCase_APAF:UC_AnalysisSW | Release/Packaging (out-of-band) | architecture.md | Delivered as artifacts; may be integrated into repo.
INF-FR-015 | Internal interfaces left to design; SDDs define details | Package_APAF note | All services | architecture.md; internal.proto | We define internal contracts and version them; SDDs can extend.
INF-FR-016 | Internal data requirements left to design; SDDs define virtual instrument items | Class_APAF:IDFSDataset | Domain model + schemas | architecture.md; sql/*.sql | We define minimal metadata schema; instrument-specific payloads are versioned blobs.
INF-PR-001 | Web server password protected where appropriate | UseCase_APAF:UC_TeamWeb; Sequence_S2_TeamWebAccess | AuthService, WebPortal | architecture.md; openapi.yaml | Implements privacy requirement via RBAC/MFA and protected endpoints.
INF-CR-001 | SwRI team provides system maintenance and software support | Deployment_APAF:SwRI | Ops processes | architecture.md | Drives runbooks, monitoring, CI/CD, and support workflows.
INF-LR-001 | SwRI provides APAF system maintenance | Deployment_APAF:Backup | Ops | architecture.md | Requires backup/restore, patching, and operational procedures.
INF-LR-002 | SwRI provides software support for APAF | Observability | Ops | architecture.md | Requires alerting, ticketing integration, and on-call.
INF-DR-001 | Provide IDFS + intermediate files to all Co-Is | UseCase_APAF:UC_Distribute | DistributionService | architecture.md; openapi.yaml | Delivery requirement duplicates FR; treated as same capability with SLA.
INF-DR-002 | Distribute ASPERA-3 IDFS to Co-Is within 24h if error-free | Class_APAF:DistributionJob note | DistributionService, Scheduler | architecture.md | Enforced via job deadlines, monitoring, and retries.
INF-DR-003 | Distribute MEX OA IDFS to Co-Is within 24h if error-free | UseCase_APAF:UC_Distribute | DistributionService | architecture.md | Same mechanism; dataset type differs.
INF-DR-004 | Distribute intermediate cleaned telemetry within 24h if error-free | UseCase_APAF:UC_Distribute | DistributionService | architecture.md | Same distribution pipeline; artifact type differs.
INF-DR-005 | Provide ASPERA-3 + MEX OA IDFS to NASA PDS | UseCase_APAF:UC_PDS | PDSSubmissionService | architecture.md; internal.proto | PDS submission pipeline and packaging.
INF-DR-006 | Provide ASPERA-3 data to PDS in PDS-compliant form | UseCase_APAF:UC_PDS | PDSSubmissionService, SchemaValidationService | architecture.md | Requires PDS packaging validation and metadata completeness.
INF-DR-007 | Calibrate and validate prior to PDS deposit | Activity_DailyPipeline | IDFSProcessingService, PDSSubmissionService | architecture.md | Adds calibration status gates before submission.
INF-DR-008 | Submit to PDS no later than 6 months after acquisition | State_IDFSDataset:L | PDSSubmissionService, Scheduler | architecture.md | Enforced via deadline fields + alerts on approaching breach.
INF-DR-009 | Provide IDFS processing algorithms to IRF | UseCase_APAF:UC_IRF | Release/Packaging | architecture.md | Out-of-band delivery; tracked as release artifact.
INF-DR-010 | Integrate science analysis software into NASA approved repository | UseCase_APAF:UC_Repo | Release automation | architecture.md | Requires packaging + publishing pipeline.
INF-DR-011 | Make IDFS access software available to Co-Is | UseCase_APAF:UC_AccessSW | Release/Packaging | architecture.md | Same as FR-013; tracked as deliverable.
INF-DR-012 | Make science analysis software available to Co-Is | UseCase_APAF:UC_AnalysisSW | Release/Packaging | architecture.md | Same as FR-014; tracked as deliverable.
INF-DR-013 | Determine exact datasets per Co-I 6 months pre-launch | (no diagram) | DistributionService config | architecture.md; sql/distribution_job_ddl.sql | Implemented as configurable distribution policies.
INF-DR-014 | Distribution mechanisms defined in Operations Procedures | (no diagram) | Ops | architecture.md | Captured as runbooks + SOP deliverable (out of scope to author here).
INF-NFR-OPS-001 | System operates in one mode; if more, document in Ops Procedures | (no diagram) | Ops | architecture.md | Architecture assumes single operational mode; supports future mode flags.
INF-NFR-SAFE-001 | No hazards to personnel/property/environment | (no diagram) | Ops | architecture.md | Ground software; mitigated via standard IT safety practices.
INF-NFR-QUAL-001 | Consider reliability/maintainability/availability/flexibility/portability/testability/usability | Package_APAF | All | architecture.md | Addressed via modular design, contracts, CI, and observability.
INF-NFR-OPS-002 | Ops Procedures provide install/ops steps; no training required | (no diagram) | Ops | architecture.md | Drives runbooks, automation, and self-documenting deployment.

---

# C. Architecture Overview

## 4+1 view alignment
- **Context / Scenario view**: Actors and use cases in **UseCase_APAF** (ESOC, CoI, PublicUser, Admin, SRE, PDS, IRF, Repo) define system boundaries and external obligations.
- **Container view**: **Container_APAF** shows WebPortal + Backend Services + archives/logs/quarantine and external clouds (ESOC/PDS/CoI/Public/IRF/Repo).
- **Component/Package (development) view**: **Package_APAF** and **Component_APAF** define modules/services and their interfaces (IAuth, IESOC, IValidate, etc.).
- **Logical/Class + Runtime view**: **Class_APAF**, **State_IDFSDataset**, **Activity_DailyPipeline**, **Sequence_S1_DailyIngestProcess**, **Sequence_S2_TeamWebAccess** define domain entities, lifecycle, and key flows.
- **Deployment/Physical view**: **Deployment_APAF** places services on SwRI on-prem compute with NAS archives and backup system, plus external connectivity.

## Key architectural choices
1. **Contract-first interfaces**: external OpenAPI for web/API; internal gRPC for service-to-service.  
2. **Immutable artifact metadata + content-addressed storage**: store files in NAS/object store paths; store metadata in SQL with checksums and lifecycle state.  
3. **Quarantine-first integrity handling**: any checksum/schema failure creates QuarantineItem and triggers alerting (State_IDFSDataset).

---

# D. Detailed Technical Design (developer-facing)

## D1. WebPortal (Public + Team)

### 1) Responsibilities & data ownership
Serves public “current data” dashboards and team “all data” dashboards; enforces authentication/authorization for team views; does not own scientific data—reads via IDFSQueryService and logs access via AuthService/AuditLog.

### 2) Technology options (3+ per concern)
- Language/runtime: Recommended **TypeScript Node.js 20**; Conservative **Python 3.11**; Cutting-edge **Deno 1.40+**.  
- Web framework: Recommended **Next.js 14**; Conservative **Django 4.2**; Cutting-edge **SvelteKit 2**.  
- RPC/HTTP: Recommended **REST over HTTPS**; Conservative **server-rendered HTML only**; Cutting-edge **GraphQL**.  
- Persistence: Recommended **none (stateless)**; Conservative **SQLite cache**; Cutting-edge **edge KV**.  
- Cache: Recommended **CDN + in-cluster Redis**; Conservative **no cache**; Cutting-edge **HTTP/3 cache**.  
- AuthN/AuthZ: Recommended **OIDC (Keycloak)**; Conservative **local users in DB**; Cutting-edge **passkeys/WebAuthn-first**.  
- Observability: Recommended **OpenTelemetry JS**; Conservative **structured logs only**; Cutting-edge **eBPF RUM**.  
- CI/CD: Recommended **GitHub Actions**; Conservative **Jenkins**; Cutting-edge **Argo Workflows**.  
- Container runtime: Recommended **containerd**; Conservative **Docker**; Cutting-edge **gVisor**.  
- Infra provisioning: Recommended **Terraform**; Conservative **Ansible only**; Cutting-edge **Crossplane**.

### 3) Recommended default stack
- **Node.js 20.x**, **Next.js 14.x**, **OpenTelemetry JS 1.x**, **Keycloak 24-26**.  
Justification: meets **INF-PR-001** (password-protected access where appropriate) via OIDC/RBAC and supports auditability for restricted team views.

### 4) Interface design (external API)
See `openapi.yaml` (section L). Endpoints include auth callback, public current datasets, team dataset search, dataset download, and audit-visible admin actions.

### 5) Data model / schema
No primary ownership; relies on `idfs_dataset`, `user_account`, `audit_log_entry`.

### 6) Caching & consistency
- Cache public “current” dataset list for **60s**; invalidate on ingestion completion event.  
- Team search results cache **30s** keyed by query+user role.  
- Consistency: **read-after-write** for newly ingested datasets by querying DB first, then file store.

---

## D2. TelemetryIngestionService + ESOCAdapter

### 1) Responsibilities & data ownership
Connects to ESOC, acquires telemetry files (ASPERA-3 and MEX OA), verifies checksums, stores raw telemetry metadata and file paths, and emits events for downstream cleaning/processing.

### 2) Technology options
- Language/runtime: Recommended **Go 1.22-1.23**; Conservative **Java 17-21**; Cutting-edge **Rust 1.75+**.  
- Framework: Recommended **Go stdlib + grpc-go**; Conservative **Spring Boot**; Cutting-edge **NATS micro**.  
- RPC: Recommended **gRPC**; Conservative **internal REST**; Cutting-edge **Kafka event-only**.  
- Persistence: Recommended **PostgreSQL 14-16** for metadata; Conservative **MySQL 8**; Cutting-edge **CockroachDB**.  
- Messaging: Recommended **NATS JetStream**; Conservative **cron + DB polling**; Cutting-edge **Kafka**.  
- Observability: Recommended **OpenTelemetry Go**; Conservative **Prometheus only**; Cutting-edge **Grafana Alloy pipelines**.  
- CI/CD: Recommended **GitHub Actions**; Conservative **Jenkins**; Cutting-edge **Tekton**.  
- Container: Recommended **Distroless**; Conservative **Alpine**; Cutting-edge **WASM**.  
- Infra: Recommended **Terraform**; Conservative **Ansible**; Cutting-edge **Pulumi**.

### 3) Recommended default stack
- **Go 1.22**, **gRPC**, **PostgreSQL 15**, **NATS JetStream 2.10+**.  
Justification: meets **INF-FR-001** (daily acquisition + auto-processing) with reliable job/event orchestration and idempotent ingestion.

### 4) Internal contracts
See `internal.proto` (section L): `AcquireTelemetry`, `VerifyChecksum`, `EmitIngestedArtifact`.

### 5) Data model / schema
See `sql/telemetry_file_ddl.sql` and `sql/archive_object_ddl.sql`.

Fields requiring immutability/audit:
- `telemetry_file.checksum` immutable after insert (integrity).  
- `archive_object.path` immutable (traceability).

### 6) Caching & consistency
No cache; strong consistency via DB transactions per file acquisition.

---

## D3. TelemetryCleaningService

### 1) Responsibilities & data ownership
Determines whether ESOC cleaned telemetry exists; if missing, generates cleaned telemetry intermediate files, validates schema, stores intermediate artifacts and metadata.

### 2) Technology options
- Language: Recommended **Python 3.11-3.12** (scientific processing); Conservative **Go**; Cutting-edge **Julia 1.10+**.  
- Processing: Recommended **batch jobs**; Conservative **single long-running worker**; Cutting-edge **Spark**.  
- Schema validation: Recommended **JSON Schema / custom validators**; Conservative **ad-hoc checks**; Cutting-edge **Apache Arrow schemas**.  
- Persistence: Recommended **PostgreSQL + NAS**; Conservative **filesystem only**; Cutting-edge **object store + lakehouse**.  
- Messaging: Recommended **NATS**; Conservative **DB polling**; Cutting-edge **Kafka**.  
- Observability: Recommended **OTel + structured logs**; Conservative **logs only**; Cutting-edge **profiling always-on**.

### 3) Recommended default stack
- **Python 3.11**, **Pydantic v2** for schema validation, **PostgreSQL 15** metadata.  
Justification: meets **INF-FR-004** (generate intermediate cleaned telemetry when ESOC cleaned-up missing).

### 4) Internal contracts
`internal.proto`: `GenerateCleanedTelemetry`, `ValidateCleanedTelemetry`.

### 5) Data model / schema
See `sql/cleaned_telemetry_file_ddl.sql`.

### 6) Caching & consistency
No cache; deterministic generation keyed by raw file ID + schema version.

---

## D4. IDFSProcessingService + SchemaValidationService

### 1) Responsibilities & data ownership
Transforms cleaned telemetry into IDFS datasets (science + engineering/ancillary), validates against IDFS schema version, records calibration/validation status, and writes dataset metadata and file locations.

### 2) Technology options
- Language: Recommended **Python 3.11**; Conservative **Java 17**; Cutting-edge **Rust**.  
- Validation: Recommended **schema validator service**; Conservative **library-only**; Cutting-edge **policy-as-code (OPA)**.  
- Persistence: Recommended **PostgreSQL**; Conservative **filesystem manifests**; Cutting-edge **lakehouse**.  
- Messaging: Recommended **NATS**; Conservative **cron**; Cutting-edge **Kafka**.  
- Compute: Recommended **K8s Jobs for heavy runs**; Conservative **single VM**; Cutting-edge **Argo Workflows**.

### 3) Recommended default stack
- **Python 3.11**, **Kubernetes Jobs**, **PostgreSQL 15**, **separate SchemaValidationService**.  
Justification: meets **INF-FR-002/INF-FR-003** (process science + engineering/ancillary into IDFS) with explicit validation gates.

### 4) Internal contracts
`internal.proto`: `ProcessToIDFS`, `ValidateIDFS`.

### 5) Data model / schema
See `sql/idfs_dataset_ddl.sql` and `sql/quarantine_item_ddl.sql`.

Encryption-at-rest markers:
- `idfs_dataset.manifest_json` (may include sensitive metadata during embargo) → encrypt at rest. Justification: meets **INF-PR-001**.

### 6) Caching & consistency
- Cache schema documents in-memory (TTL 10 minutes).  
- Strong consistency for dataset state transitions (Created → Validated → Archived).

---

## D5. ArchiveService

### 1) Responsibilities & data ownership
Manages retention, storage paths, backup hooks, and restore verification for raw telemetry, intermediate cleaned telemetry, and IDFS datasets.

### 2) Technology options
- Storage: Recommended **NAS (NFS/SMB) + PostgreSQL metadata**; Conservative **single filesystem**; Cutting-edge **S3-compatible object store (MinIO)**.  
- Backup: Recommended **restic + immutable snapshots**; Conservative **rsync**; Cutting-edge **ZFS send/receive**.  
- Retention: Recommended **policy engine in service**; Conservative **manual scripts**; Cutting-edge **WORM storage**.

### 3) Recommended default stack
- **NAS + restic** backups, metadata in **PostgreSQL 15**.  
Justification: meets **INF-FR-005/006/007** (local archive for raw/IDFS/intermediate availability and re-processing).

### 4) Internal contracts
`internal.proto`: `ArchiveArtifact`, `SetRetentionPolicy`.

### 5) Data model / schema
See `sql/archive_object_ddl.sql`.

### 6) Caching & consistency
No cache; archive operations are idempotent by `(artifact_type, source_id, checksum)`.

---

## D6. DistributionService

### 1) Responsibilities & data ownership
Packages and distributes IDFS datasets and intermediate files to Co-Is; supports configurable “who gets what” policies; tracks job status, retries, and receipts.

### 2) Technology options
- Transport: Recommended **HTTPS download links + optional SFTP push**; Conservative **DVD/physical media**; Cutting-edge **Globus**.  
- Job tracking: Recommended **PostgreSQL jobs table**; Conservative **cron logs**; Cutting-edge **workflow engine**.  
- Notifications: Recommended **email + webhook**; Conservative **email only**; Cutting-edge **PagerDuty integration**.

### 3) Recommended default stack
- **HTTPS signed URLs** (time-limited) + **SFTP fallback**, job tracking in **PostgreSQL 15**.  
Justification: meets **INF-DR-002/003/004** (24h conditional electronic distribution) with retryable jobs and auditable receipts.

### 4) External API surface
Exposed via `openapi.yaml` endpoints for Co-I downloads and job status.

### 5) Data model / schema
See `sql/distribution_job_ddl.sql`.

### 6) Caching & consistency
Cache Co-I entitlement policy for 5 minutes; strong consistency for job state transitions.

---

## D7. PDSSubmissionService

### 1) Responsibilities & data ownership
Builds PDS submission packages from validated IDFS datasets, ensures PDS compliance, submits to NASA PDS, and tracks deadlines (≤6 months).

### 2) Technology options
- Packaging: Recommended **BagIt + PDS4 labels**; Conservative **custom zip**; Cutting-edge **RO-Crate**.  
- Submission: Recommended **HTTPS + checksum manifests**; Conservative **manual upload**; Cutting-edge **API-driven deposit**.  
- Tracking: Recommended **PostgreSQL**; Conservative **spreadsheets**; Cutting-edge **workflow engine**.

### 3) Recommended default stack
- **BagIt packaging**, **PDS4 label generation**, tracking in **PostgreSQL 15**.  
Justification: meets **INF-DR-006/007/008** (PDS-compliant, calibrated/validated, submitted ≤6 months).

### 4) Internal contracts
`internal.proto`: `BuildPDSSubmissionPackage`, `SubmitToPDS`.

### 5) Data model / schema
See `sql/pds_submission_package_ddl.sql`.

### 6) Caching & consistency
No cache; deadline enforcement via scheduled checks.

---

## D8. AuthService + Audit Logging

### 1) Responsibilities & data ownership
Provides authentication and authorization for team portal and restricted APIs; manages users/roles; writes access audit logs; supports deprovisioning.

### 2) Technology options
- Identity: Recommended **Keycloak 24-26**; Conservative **LDAP + app RBAC**; Cutting-edge **Auth0**.  
- MFA: Recommended **TOTP/WebAuthn**; Conservative **email OTP**; Cutting-edge **passkeys-only**.  
- Audit: Recommended **append-only table + WORM backups**; Conservative **log files**; Cutting-edge **SIEM**.

### 3) Recommended default stack
- **Keycloak** + **PostgreSQL audit tables** + **append-only constraints**.  
Justification: meets **INF-PR-001** (password protected where appropriate) and supports embargoed team access.

### 4) External API
OIDC endpoints are provided by IdP; APAF exposes `/auth/login` and `/auth/callback` in `openapi.yaml`.

### 5) Data model / schema
See `sql/user_account_ddl.sql` and `sql/audit_log_entry_ddl.sql` (immutability enforced).

### 6) Caching & consistency
JWT validation cached by JWK TTL; RBAC decisions cached 60s.

---

## D9. MonitoringAlertingService (Observability)

### 1) Responsibilities & data ownership
Collects metrics/logs/traces, triggers alerts on pipeline failures, integrity issues, missed deadlines, and distribution failures; stores error audit logs.

### 2) Technology options
- Metrics: Recommended **Prometheus**; Conservative **CloudWatch (not on-prem)**; Cutting-edge **VictoriaMetrics**.  
- Logs: Recommended **Loki**; Conservative **ELK**; Cutting-edge **OpenSearch**.  
- Tracing: Recommended **Tempo + OTel**; Conservative **no tracing**; Cutting-edge **Honeycomb**.

### 3) Recommended default stack
- **Prometheus + Alertmanager + Loki + Tempo** with **OpenTelemetry** instrumentation.  
Justification: meets **INF-FR-011** (built-in error handling for data integrity) by enabling rapid detection and response.

### 4) Internal contracts
`internal.proto`: `EmitMetric`, `EmitErrorAudit`.

### 5) Data model / schema
See `sql/error_audit_log_ddl.sql`.

### 6) Caching & consistency
N/A.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/telemetry-ingestion-deployment.yaml` in section L.

Replica sizing guidance (initial):
- Small: 1 replica ingestion/processing, 1 web, 1 query
- Medium: 2-3 replicas web/query, 2 workers
- Large: 3-5 web/query, separate worker pools for processing

Justification: meets **INF-CR-001** (maintenance/support) by standardizing deployment and scaling knobs.

## E2. DB HA topology, backup cadence, restore notes
- PostgreSQL: primary + 1 synchronous standby (Patroni or operator).  
- Backups: nightly full + WAL archiving; quarterly restore drill.  
Justification: meets **INF-LR-001** (system maintenance) by ensuring recoverability.

## E3. Network topology + ingress/egress rules
Mapped to **Deployment_APAF:SwRI/AppVM/NAS/Backup**:
- Ingress: HTTPS to WebPortal only; admin endpoints restricted to VPN.  
- Egress: ESOC acquisition endpoint, PDS submission endpoint, Co-I distribution endpoints.  
- Latency: on-prem service-to-NAS < 5ms typical; external depends on WAN.

## E4. CI/CD sketch
1. PR: lint + unit tests + contract tests (OpenAPI/proto) + SQL migration dry-run  
2. Build: container images + SBOM  
3. Deploy: staging via Helm/Kustomize  
4. Gate: E2E daily pipeline simulation  
5. Prod: blue/green for WebPortal; canary for workers

Justification: meets **INF-NFR-QUAL-001** (testability/maintainability).

---

# F. Security Design

## F1. Auth & AuthZ
- Use **OIDC** with JWT access tokens for APIs; WebPortal uses OIDC code flow.  
- Token lifetime: access 15 min, refresh 8 hours; revoke on user disable.  
Justification: meets **INF-PR-001** (password protected where appropriate).

## F2. Secrets management & rotation
- Kubernetes Secrets encrypted at rest; rotate DB credentials quarterly; rotate signing keys annually.  
Justification: meets **INF-LR-002** (software support) by reducing incident risk.

## F3. TLS & service-mesh
- TLS 1.2+ externally; optional mTLS internally via service mesh (Linkerd/Istio) if needed.  
Justification: meets **INF-NFR-QUAL-001** (reliability/security quality factors).

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Unauthorized access to embargoed team data | OIDC + RBAC; separate team endpoints; audit logs (INF-PR-001) |
| Tampered telemetry files | checksum verification + quarantine + immutable logs (INF-FR-011) |
| Data exfiltration via distribution links | signed URLs, short TTL, per-user authorization (INF-DR-001) |
| Ransomware on NAS | immutable backups, least privilege, restore drills (INF-LR-001) |
| Supply-chain compromise | SBOM, image signing, dependency scanning (INF-NFR-QUAL-001) |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + example alerts
Key metrics:
- `apaf_ingest_files_total{status}`  
- `apaf_pipeline_duration_seconds`  
- `apaf_quarantine_items_total{reason}`  
- `apaf_distribution_job_age_seconds`  
- `apaf_pds_deadline_days_remaining`

Example Prometheus alert rules:
- Pipeline failure / no successful run:
- Integrity quarantine spike

(Provided in runbook; see below rules in section L if needed—kept in architecture.md for brevity.)

Justification: meets **INF-FR-011** (error handling for integrity).

## G2. SLOs, error budgets, RTO/RPO
- SLO: daily pipeline completes by 03:00 UTC on 99% of days (inferred)  
- RTO: 24 hours for ingestion/processing services  
- RPO: 24 hours for metadata DB; 24 hours for NAS (nightly backup)

Justification: meets **INF-FR-001** (daily processing) and **INF-LR-001** (maintenance).

## G3. Dashboard & runbook sketch
Dashboards:
- Daily run status, ingest counts, validation failures, distribution backlog, PDS deadline tracker.  
Runbooks:
- ESOC connectivity failure, checksum mismatch quarantine, schema validation failure, NAS full, PDS submission failure.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Notes |
|---|---|---|
| Unit | all services | pure functions, validators |
| Integration | ingestion↔ESOCAdapter, processing↔validation, query↔DB | docker-compose/kind |
| Contract | OpenAPI + proto | CI gate: breaking changes |
| E2E | daily pipeline | simulated ESOC drop + expected IDFS outputs |
| Chaos | DB failover, pod kill | validate RTO/RPO |

Justification: meets **INF-NFR-QUAL-001** (reliability/testability).

## H2. Test data management & environment isolation
Environments: dev, staging, prod.  
Refresh: staging seeded weekly with anonymized/synthetic telemetry.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps (if replacing an existing system)
1. Stand up new APAF in parallel; ingest same ESOC drops (read-only).  
2. Validate IDFS equivalence; backfill archives.  
3. Cut over distribution endpoints; keep old system for 30 days.  
Rollback: switch distribution DNS/links back; keep dual archives.

## I2. Backwards compatibility & API versioning
- External API versioned under `/api/v1`; additive changes only; breaking changes require `/api/v2` and 90-day overlap.

Justification: meets **INF-DR-014** (distribution mechanisms clearly defined) by stabilizing interfaces.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| On-prem K8s vs single VM | VM-only; hybrid cloud | K8s adds complexity but standardizes ops | Supports **INF-CR-001** maintenance/support with repeatable deployments |
| gRPC internal contracts | internal REST; message bus only | gRPC strong typing; REST simpler | Contract-first reduces ambiguity (**INF-FR-015**) |
| NAS vs S3 object store | MinIO; cloud S3 | NAS simplest on-prem; S3 scales better | Aligns with **INF-FR-005..007** local archive requirement |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1**: ESOC provides daily telemetry file drops accessible via a stable network protocol (SFTP/HTTPS) even though SRS says “via NISN” without technical details.  
- **A2**: IDFS and PDS compliance rules are available as machine-checkable schemas or validation scripts maintained by the project.  
- **A3**: “Password protected where appropriate” implies role-based access control for team-only displays and downloads.  
- **A4**: Local archive retention period is at least 5 years (SRS says store locally but not duration); retention is configurable.  
- **A5**: Co-I distribution is primarily electronic; physical media is exceptional.

## Open stakeholder questions (suggested phrasing)
1. “What exact ESOC delivery protocol(s), authentication, and file naming conventions are mandated for NISN acquisition?”  
2. “What is the authoritative IDFS schema versioning and validation toolchain, and how are schema updates governed?”  
3. “What are the exact Co-I distribution entitlements (datasets per Co-I) and preferred mechanisms (HTTPS portal, SFTP, Globus)?”  
4. “What constitutes ‘most current data’ for public display (latest orbit, last 24h, last successful run)?”  
5. “What are the required audit log retention periods and any export requirements for compliance?”

## Diagram naming/ID conflicts recorded
- UML notes reference **NFR-001..012 and ASR-002..010** not present in SRS. We treat them as **non-authoritative** and map to **INF-*** requirements above.

---

# L. Deliverables

## 1) `architecture.md`
```markdown
# (This document is the content of ArchitectureDocument.md / architecture.md)
```

## 2) `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: APAF External API
  version: "1.0.0"
  description: External API for APAF public/team web displays and Co-I distribution.
servers:
  - url: https://apaf.example.org
paths:
  /api/v1/public/current-datasets:
    get:
      summary: List most current public IDFS datasets
      operationId: listPublicCurrentDatasets
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DatasetListResponse"
        "500":
          $ref: "#/components/responses/ServerError"
  /api/v1/team/datasets/search:
    post:
      summary: Search IDFS datasets (team-only)
      operationId: searchTeamDatasets
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DatasetSearchRequest"
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DatasetListResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "500":
          $ref: "#/components/responses/ServerError"
  /api/v1/team/datasets/{datasetId}:
    get:
      summary: Get dataset metadata (team-only)
      operationId: getTeamDataset
      security:
        - bearerAuth: []
      parameters:
        - name: datasetId
          in: path
          required: true
          schema: { type: string, minLength: 1 }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Dataset"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"
  /api/v1/team/datasets/{datasetId}/download:
    post:
      summary: Create a time-limited download URL for a dataset (team-only)
      operationId: createDatasetDownload
      security:
        - bearerAuth: []
      parameters:
        - name: datasetId
          in: path
          required: true
          schema: { type: string }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DownloadLinkResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"
  /api/v1/admin/distribution-jobs:
    post:
      summary: Create a distribution job (admin-only)
      operationId: createDistributionJob
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateDistributionJobRequest"
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DistributionJob"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  responses:
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    Forbidden:
      description: Forbidden
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    NotFound:
      description: Not Found
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    ServerError:
      description: Server Error
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string, example: "APAF_FORBIDDEN" }
        message: { type: string, example: "Access denied" }
        requestId: { type: string, example: "req_01HZY..." }
        details:
          type: object
          additionalProperties: true
    Dataset:
      type: object
      required: [datasetId, instrument, schemaVersion, coverageStartUtc, coverageEndUtc, validationStatus]
      properties:
        datasetId: { type: string }
        instrument: { type: string, example: "ASPERA-3" }
        schemaVersion: { type: string, example: "1.3.2" }
        coverageStartUtc: { type: string, format: date-time }
        coverageEndUtc: { type: string, format: date-time }
        validationStatus: { type: string, enum: ["Pass", "Fail", "Quarantined", "Pending"] }
        archivePath: { type: string }
    DatasetListResponse:
      type: object
      required: [items]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/Dataset" }
    DatasetSearchRequest:
      type: object
      required: [fromUtc, toUtc]
      properties:
        instrument: { type: string, nullable: true }
        fromUtc: { type: string, format: date-time }
        toUtc: { type: string, format: date-time }
        schemaVersion: { type: string, nullable: true }
        limit: { type: integer, minimum: 1, maximum: 500, default: 100 }
    DownloadLinkResponse:
      type: object
      required: [url, expiresAtUtc]
      properties:
        url: { type: string, format: uri }
        expiresAtUtc: { type: string, format: date-time }
    CreateDistributionJobRequest:
      type: object
      required: [targetGroup, datasetIds]
      properties:
        targetGroup: { type: string, example: "ASPERA-3 Co-Is" }
        datasetIds:
          type: array
          minItems: 1
          items: { type: string }
        includeIntermediate:
          type: boolean
          default: false
    DistributionJob:
      type: object
      required: [jobId, targetGroup, status, createdUtc]
      properties:
        jobId: { type: string }
        targetGroup: { type: string }
        status: { type: string, enum: ["Created", "Dispatched", "Completed", "Failed"] }
        createdUtc: { type: string, format: date-time }
```

## 3) `internal.proto`
```proto
syntax = "proto3";

package apaf.v1;

import "google/protobuf/timestamp.proto";

message ArtifactRef {
  string artifact_id = 1;
  string artifact_type = 2; // RawTelemetry | CleanedTelemetry | IDFS | PDSSubmission
  string checksum_sha256 = 3;
  string storage_path = 4;
}

message AcquireTelemetryRequest {
  string source = 1; // ESOC
  google.protobuf.Timestamp scheduled_run_utc = 2;
}

message AcquireTelemetryResponse {
  repeated ArtifactRef raw_files = 1;
}

message VerifyChecksumRequest {
  ArtifactRef artifact = 1;
}

message VerifyChecksumResponse {
  bool ok = 1;
  string failure_reason = 2;
}

message GenerateCleanedTelemetryRequest {
  ArtifactRef raw_file = 1;
  string clean_schema_ref = 2;
}

message GenerateCleanedTelemetryResponse {
  ArtifactRef cleaned_file = 1;
}

message ProcessToIDFSRequest {
  ArtifactRef cleaned_file = 1;
  string idfs_schema_version = 2;
  string instrument = 3; // ASPERA-3 | MEX-OA
}

message ProcessToIDFSResponse {
  ArtifactRef idfs_dataset = 1;
}

message QuarantineRequest {
  ArtifactRef artifact = 1;
  string reason = 2;
}

message QuarantineResponse {
  string quarantine_item_id = 1;
}

message BuildPDSSubmissionPackageRequest {
  string dataset_id = 1;
  string pds_standard = 2; // e.g., PDS4
}

message BuildPDSSubmissionPackageResponse {
  ArtifactRef pds_package = 1;
}

service IngestionService {
  rpc AcquireTelemetry(AcquireTelemetryRequest) returns (AcquireTelemetryResponse);
  rpc VerifyChecksum(VerifyChecksumRequest) returns (VerifyChecksumResponse);
  rpc Quarantine(QuarantineRequest) returns (QuarantineResponse);
}

service CleaningService {
  rpc GenerateCleanedTelemetry(GenerateCleanedTelemetryRequest) returns (GenerateCleanedTelemetryResponse);
  rpc Quarantine(QuarantineRequest) returns (QuarantineResponse);
}

service ProcessingService {
  rpc ProcessToIDFS(ProcessToIDFSRequest) returns (ProcessToIDFSResponse);
  rpc Quarantine(QuarantineRequest) returns (QuarantineResponse);
}

service PDSService {
  rpc BuildPDSSubmissionPackage(BuildPDSSubmissionPackageRequest) returns (BuildPDSSubmissionPackageResponse);
}
```

## 4) `k8s/telemetry-ingestion-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telemetry-ingestion
  namespace: apaf
spec:
  replicas: 1
  selector:
    matchLabels:
      app: telemetry-ingestion
  template:
    metadata:
      labels:
        app: telemetry-ingestion
    spec:
      containers:
        - name: telemetry-ingestion
          image: apaf/telemetry-ingestion:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: apaf-config
            - secretRef:
                name: apaf-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "2Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: telemetry-ingestion
  namespace: apaf
spec:
  selector:
    app: telemetry-ingestion
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: telemetry-ingestion-hpa
  namespace: apaf
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: telemetry-ingestion
  minReplicas: 1
  maxReplicas: 3
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
  ESOC_ENDPOINT: "sftp://esoc.example.org/drop"
  IDFS_SCHEMA_VERSION: "1.3.2"
---
apiVersion: v1
kind: Secret
metadata:
  name: apaf-secrets
  namespace: apaf
type: Opaque
stringData:
  ESOC_USERNAME: "change-me"
  ESOC_PASSWORD: "change-me"
```

## 5) `sql/<entity>_ddl.sql`
```sql
-- sql/telemetry_file_ddl.sql
CREATE TABLE telemetry_file (
  file_id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  format TEXT NOT NULL,
  acquisition_time_utc TIMESTAMPTZ NOT NULL,
  checksum_sha256 TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('Acquired','Quarantined','Archived')),
  storage_path TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_telemetry_file_acq_time ON telemetry_file (acquisition_time_utc);

-- sql/cleaned_telemetry_file_ddl.sql
CREATE TABLE cleaned_telemetry_file (
  file_id TEXT PRIMARY KEY,
  raw_file_id TEXT REFERENCES telemetry_file(file_id),
  schema_ref TEXT NOT NULL,
  generated_by TEXT NOT NULL CHECK (generated_by IN ('ESOC','APAF')),
  generation_time_utc TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('Validated','Failed','Quarantined')),
  checksum_sha256 TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_cleaned_raw_file ON cleaned_telemetry_file (raw_file_id);

-- sql/idfs_dataset_ddl.sql
CREATE TABLE idfs_dataset (
  dataset_id TEXT PRIMARY KEY,
  schema_version TEXT NOT NULL,
  instrument TEXT NOT NULL,
  coverage_start_utc TIMESTAMPTZ NOT NULL,
  coverage_end_utc TIMESTAMPTZ NOT NULL,
  validation_status TEXT NOT NULL CHECK (validation_status IN ('Pass','Fail','Quarantined','Pending')),
  manifest_json JSONB NOT NULL, -- encrypt at rest (A3/INF-PR-001)
  storage_path TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_idfs_dataset_coverage ON idfs_dataset (instrument, coverage_start_utc, coverage_end_utc);

-- sql/archive_object_ddl.sql
CREATE TABLE archive_object (
  archive_id TEXT PRIMARY KEY,
  artifact_type TEXT NOT NULL,
  source_id TEXT NOT NULL,
  path TEXT NOT NULL,
  retention_until_utc TIMESTAMPTZ NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_archive_object_type ON archive_object (artifact_type);

-- sql/distribution_job_ddl.sql
CREATE TABLE distribution_job (
  job_id TEXT PRIMARY KEY,
  target_group TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('Created','Dispatched','Completed','Failed')),
  retry_count INT NOT NULL DEFAULT 0,
  last_error TEXT NULL
);

-- sql/pds_submission_package_ddl.sql
CREATE TABLE pds_submission_package (
  package_id TEXT PRIMARY KEY,
  dataset_id TEXT NOT NULL REFERENCES idfs_dataset(dataset_id),
  pds_standard TEXT NOT NULL,
  submission_deadline_utc TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('Built','Submitted','Failed')),
  storage_path TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- sql/user_account_ddl.sql
CREATE TABLE user_account (
  user_id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL CHECK (role IN ('public','coi','admin')),
  mfa_enabled BOOLEAN NOT NULL DEFAULT false,
  password_last_rotated_utc TIMESTAMPTZ NULL,
  active BOOLEAN NOT NULL DEFAULT true,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- sql/audit_log_entry_ddl.sql (append-only)
CREATE TABLE audit_log_entry (
  entry_id TEXT PRIMARY KEY,
  log_type TEXT NOT NULL CHECK (log_type IN ('access','error')),
  timestamp_utc TIMESTAMPTZ NOT NULL,
  actor_id TEXT NOT NULL,
  action TEXT NOT NULL,
  details JSONB NOT NULL
);

CREATE INDEX idx_audit_log_time ON audit_log_entry (timestamp_utc);

-- sql/quarantine_item_ddl.sql
CREATE TABLE quarantine_item (
  item_id TEXT PRIMARY KEY,
  artifact_type TEXT NOT NULL,
  artifact_id TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  status TEXT NOT NULL CHECK (status IN ('Quarantined','Released','Discarded'))
);

-- sql/error_audit_log_ddl.sql
CREATE TABLE error_audit_log (
  id TEXT PRIMARY KEY,
  timestamp_utc TIMESTAMPTZ NOT NULL,
  component TEXT NOT NULL,
  error_code TEXT NOT NULL,
  message TEXT NOT NULL,
  context JSONB NOT NULL
);
```

## 6) `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,Acquire telemetry daily and auto-process,UseCase_APAF:UC_Acquire;Activity_DailyPipeline;Sequence_S1_DailyIngestProcess,TelemetryIngestionService|ESOCAdapter|Scheduler,architecture.md|internal.proto,Defines ingestion boundary and scheduling.
INF-FR-002,Process science data into IDFS,UseCase_APAF:UC_Process;Activity_DailyPipeline,IDFSProcessingService|SchemaValidationService,architecture.md|sql/idfs_dataset_ddl.sql,Core science product generation.
INF-FR-003,Process engineering/ancillary into IDFS,UseCase_APAF:UC_Process;Activity_DailyPipeline,IDFSProcessingService,architecture.md,Calibration/validation support.
INF-FR-004,Generate cleaned telemetry if ESOC missing,UseCase_APAF:UC_Clean;Activity_DailyPipeline,TelemetryCleaningService,architecture.md|internal.proto,Ensures continuity when ESOC cleaned not available.
INF-FR-005,Store raw telemetry locally,UseCase_APAF:UC_Archive;Deployment_APAF:NAS/dRaw,ArchiveService|RawTelemetryArchive,sql/telemetry_file_ddl.sql,Reprocessing and availability.
INF-FR-006,Store IDFS locally,UseCase_APAF:UC_Archive;Deployment_APAF:NAS/dIDFS,ArchiveService|IDFSArchive,sql/idfs_dataset_ddl.sql,Analysis availability.
INF-FR-007,Store intermediate locally,UseCase_APAF:UC_Archive,ArchiveService|IntermediateArchive,sql/cleaned_telemetry_file_ddl.sql,Supports team and reprocessing.
INF-FR-008,Public web display current data,UseCase_APAF:UC_PublicWeb;Container_APAF:WebPortal,WebPortal|IDFSQueryService,openapi.yaml,Public monitoring.
INF-FR-009,Team web display any data,UseCase_APAF:UC_TeamWeb;Sequence_S2_TeamWebAccess,WebPortal|AuthService|IDFSQueryService,openapi.yaml,Science analysis support.
INF-FR-010,Password protect team displays,UseCase_APAF:UC_TeamWeb,AuthService|WebPortal,openapi.yaml,Embargo enforcement.
INF-FR-011,Built-in error handling for integrity,UseCase_APAF:UC_Alert;State_IDFSDataset:L,MonitoringAlertingService|QuarantineStore,sql/quarantine_item_ddl.sql,Prevents silent corruption.
INF-FR-012,Provide IDFS/intermediate to Co-Is,UseCase_APAF:UC_Distribute,DistributionService,openapi.yaml|sql/distribution_job_ddl.sql,Distribution capability.
INF-FR-013,Provide IDFS access software,UseCase_APAF:UC_AccessSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-FR-014,Provide analysis software,UseCase_APAF:UC_AnalysisSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-FR-015,Internal interfaces left to design,Package_APAF,All services,internal.proto,Contract-first internal interfaces.
INF-FR-016,Internal data left to design,Class_APAF:IDFSDataset,Domain model,sql/idfs_dataset_ddl.sql,Defines minimal persisted metadata.
INF-PR-001,Password protect web server where appropriate,UseCase_APAF:UC_TeamWeb;Sequence_S2_TeamWebAccess,AuthService|WebPortal,openapi.yaml,Privacy requirement.
INF-CR-001,SwRI provides maintenance/support,Deployment_APAF:SwRI,Ops,architecture.md,Operational responsibility.
INF-LR-001,SwRI provides system maintenance,Deployment_APAF:Backup,Ops,architecture.md,Backup/restore and patching.
INF-LR-002,SwRI provides software support,Component_APAF:Mon,Ops,architecture.md,Monitoring and on-call.
INF-DR-001,Provide IDFS/intermediate to Co-Is,UseCase_APAF:UC_Distribute,DistributionService,openapi.yaml,Delivery requirement.
INF-DR-002,ASPERA-3 IDFS to Co-Is within 24h conditional,Class_APAF:DistributionJob,DistributionService,sql/distribution_job_ddl.sql,SLA via job deadlines.
INF-DR-003,MEX OA IDFS to Co-Is within 24h conditional,UseCase_APAF:UC_Distribute,DistributionService,sql/distribution_job_ddl.sql,SLA via same mechanism.
INF-DR-004,Intermediate cleaned telemetry within 24h conditional,UseCase_APAF:UC_Distribute,DistributionService,sql/distribution_job_ddl.sql,SLA via same mechanism.
INF-DR-005,Provide IDFS to NASA PDS,UseCase_APAF:UC_PDS,PDSSubmissionService,sql/pds_submission_package_ddl.sql,PDS pipeline.
INF-DR-006,PDS-compliant form,UseCase_APAF:UC_PDS,PDSSubmissionService|SchemaValidationService,architecture.md,Compliance packaging.
INF-DR-007,Calibrate/validate before PDS,Activity_DailyPipeline,IDFSProcessingService|PDSSubmissionService,architecture.md,Quality gate.
INF-DR-008,Submit to PDS <=6 months,State_IDFSDataset:L,PDSSubmissionService,sql/pds_submission_package_ddl.sql,Deadline tracking.
INF-DR-009,Provide algorithms to IRF,UseCase_APAF:UC_IRF,Release/Packaging,architecture.md,Out-of-band deliverable.
INF-DR-010,Integrate analysis software into NASA repo,UseCase_APAF:UC_Repo,Release automation,architecture.md,Repository publishing.
INF-DR-011,Make access software available,UseCase_APAF:UC_AccessSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-DR-012,Make analysis software available,UseCase_APAF:UC_AnalysisSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-DR-013,Determine datasets per Co-I 6 months pre-launch,,DistributionService config,sql/distribution_job_ddl.sql,Configurable entitlements.
INF-DR-014,Distribution mechanisms defined in Ops Procedures,,Ops,architecture.md,SOP/runbook requirement.
INF-NFR-OPS-001,Single mode unless documented,,Ops,architecture.md,Assumed single mode.
INF-NFR-SAFE-001,No hazards,,Ops,architecture.md,Ground system safety baseline.
INF-NFR-QUAL-001,Quality factors considered,Package_APAF,All,architecture.md,Design supports QA.
INF-NFR-OPS-002,Ops procedures sufficient no training,,Ops,architecture.md,Runbooks and automation.
```

---

## Verification (Acceptance Criteria)
| Item | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A-L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (as INF-*) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDLs provided for persisted entities | [x] |
| All major components have at least one API contract and a data schema | [x] (shared schemas; contracts via OpenAPI/proto) |
| Assumptions and unresolved questions listed | [x] |

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?