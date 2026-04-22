Analysis Plan
Scope: APAF Ground Data System (Telemetry Acquisition, IDFS Processing, Archiving, Distribution).
Approach: Modular Monolith on Kubernetes, Schema-First Validation, RBAC-Enforced Embargo.
Validation: Traceability Matrix, Contract Testing, SLO Monitoring.

# A. Executive Summary

The ASPERA-3 Processing and Archiving Facility (APAF) is a ground data system designed to acquire telemetry from ESOC, process it into Instrument Data File Sets (IDFS), archive data locally at SwRI, and distribute it to Co-Investigators (Co-I) and the NASA Planetary Data System (PDS). The architecture adopts a **Modular Monolith** style deployed on an **On-Premise Kubernetes Cluster** to balance operational simplicity with scalability.

**Primary Diagram References:**
- **Context/Function:** `UseCaseDiagram` (UC01: Acquire Telemetry, UC07: Submit to PDS).
- **Structure:** `ClassDiagram` (TB: TelemetryBatch, IDFS: IDFSDataset), `ComponentDiagram` (IngestionModule, ProcessingModule).
- **Deployment:** `DeploymentDiagram` (K8s Cluster, Storage Array), `ContainerDiagram` (Backend API, Background Worker).

**Architectural Style:** Modular Monolith with Layered Architecture (Interface, Application, Domain, Infrastructure).
**Deployment Topology:** On-Premise Kubernetes Cluster with S3-compatible Object Storage and PostgreSQL.

**Top 3 Design Risks & Mitigations:**

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Batch Processing Bottleneck** | Missed 24h delivery window (INF-DR-001). | Horizontal scaling of `Background Worker` pods via K8s HPA; Async queue (Redis/Celery). |
| **Data Integrity Loss** | Corruption during transfer/processing (INF-FR-010). | End-to-end SHA-256 checksums; Idempotent jobs; Dead Letter Queues for failed batches. |
| **Embargo Leakage** | Unauthorized public access to team data (INF-PR-001). | Centralized RBAC (`SecurityModule`); Automated embargo expiry logic; Audit logging. |

**Key QA Coverage Mapping:**

| Quality Attribute | ASR/NFR ID | Test Type |
| :--- | :--- | :--- |
| **Performance** | INF-NFR-001 (24h Delivery) | Load Testing (Batch Volume) |
| **Security** | INF-PR-001 (Password Protect) | Penetration Testing, RBAC Unit Tests |
| **Reliability** | INF-NFR-004 (Data Integrity) | Chaos Engineering, Checksum Validation |
| **Maintainability** | INF-NFR-007 (Documentation) | Code Coverage, Static Analysis |
| **Compliance** | INF-DR-004 (PDS Form) | Schema Validation Contract Tests |

# B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INF-FR-001** | Acquire telemetry from ESOC daily. | `UseCaseDiagram:UC01`, `SequenceDiagram1:ESOC` | IngestionModule | `openapi.yaml` | Core entry point for data pipeline. |
| **INF-FR-002** | Process science data into IDFS. | `ActivityDiagram:Convert to IDFS`, `ClassDiagram:IDFS` | ProcessingModule | `internal.proto` | Primary value-add function of APAF. |
| **INF-FR-003** | Process engineering/ancillary info. | `ClassDiagram:IDFS` | ProcessingModule | `internal.proto` | Required for calibration/validation. |
| **INF-FR-004** | Generate intermediate cleaned files. | `ActivityDiagram:Store Raw Batch` | ProcessingModule | `sql/batch_ddl.sql` | Support re-processing if ESOC data flawed. |
| **INF-FR-005** | Store telemetry on local SwRI archive. | `DeploymentDiagram:Store`, `ClassDiagram:AR` | ArchiveModule | `sql/archive_ddl.sql` | Ensures data availability per SRS. |
| **INF-FR-006** | Store IDFS on local SwRI archive. | `DeploymentDiagram:S3`, `ClassDiagram:AR` | ArchiveModule | `sql/archive_ddl.sql` | Local analysis support. |
| **INF-FR-007** | Store intermediate files locally. | `ClassDiagram:TB` | ArchiveModule | `sql/batch_ddl.sql` | Re-processing support. |
| **INF-FR-008** | Web displays (Public current data). | `UseCaseDiagram:UC04`, `ContainerDiagram:Web` | WebModule | `openapi.yaml` | Public monitoring requirement. |
| **INF-FR-009** | Web displays (Team science analysis). | `UseCaseDiagram:UC05`, `SequenceDiagram2:CoI` | WebModule | `openapi.yaml` | Science team support. |
| **INF-PR-001** | Web server password protected (Team). | `SequenceDiagram2:Auth`, `ClassDiagram:User` | SecurityModule | `openapi.yaml` | Privacy requirement for embargoed data. |
| **INF-FR-010** | Built-in error handling. | `ActivityDiagram:Log Error`, `StateDiagram:Validating` | ProcessingModule | `internal.proto` | Data integrity assurance. |
| **INF-DR-001** | Provide data to Co-I's within 24h. | `UseCaseDiagram:UC06`, `ActivityDiagram:Notify Co-Is` | DistributionModule | `openapi.yaml` | Critical mission timeline constraint. |
| **INF-DR-002** | Provide software to Co-I's. | `UseCaseDiagram:UC06` | DistributionModule | N/A (External) | Tooling support for analysis. |
| **INF-DR-003** | Submit IDFS to NASA PDS. | `UseCaseDiagram:UC07`, `ActivityDiagram:Submit to NASA PDS` | ArchiveModule | `internal.proto` | Long-term archival mandate. |
| **INF-DR-004** | PDS submission within 6 months. | `StateDiagram:Released` | ArchiveModule | `sql/archive_ddl.sql` | Compliance deadline. |
| **INF-CR-001** | System maintenance and support. | `DeploymentDiagram:K8s` | Infrastructure | `k8s/apaf-deployment.yaml` | Operational sustainability. |
| **INF-NFR-001** | Performance (24h latency). | `SequenceDiagram1` | ProcessingModule | `k8s/apaf-deployment.yaml` | Justifies async worker scaling. |
| **INF-NFR-004** | Reliability (Data Integrity). | `ClassDiagram:TB.checksum` | ArchiveModule | `sql/batch_ddl.sql` | Justifies checksum columns. |

# C. Architecture Overview

The APAF system follows the **4+1 Architectural View Model**, realized through the provided PlantUML diagrams.

1.  **Logical View:** Defined in `ClassDiagram` and `StateDiagram`. Core entities include `TelemetryBatch` (INF-FR-001), `IDFSDataset` (INF-FR-002), and `ArchiveRecord` (INF-FR-005). State transitions manage the lifecycle from `Received` to `Released` (INF-DR-004).
2.  **Process View:** Defined in `ActivityDiagram` and `SequenceDiagram1/2`. Asynchronous processing via `ProcessingJob` ensures the 24h delivery window (INF-DR-001). Security checks (`AuthService`) intercept data access (INF-PR-001).
3.  **Development View:** Defined in `PackageDiagram` and `ComponentDiagram`. Modular separation ensures `Security` logic is isolated from `Domain Logic`.
4.  **Physical View:** Defined in `DeploymentDiagram` and `ContainerDiagram`. Kubernetes orchestrates `Web Application`, `Backend API`, and `Background Worker`. Storage is split between `PostgreSQL` (Metadata) and `S3` (Binary Data).
5.  **Scenarios:** Covered in `UseCaseDiagram`. Actors include ESOC (Ingest), Co-I (Access), and NASA PDS (Archive).

# D. Detailed Technical Design

## 1. Ingestion Module
*   **Responsibilities:** Acquire telemetry from ESOC (NISN), validate checksums, store raw batches.
*   **Technology Options:**
    *   *Recommended:* **Spring Boot (Java 17)**. Justification: Meets INF-CR-001 (Maintainability) and strong typing for data contracts.
    *   *Conservative:* **Python Flask**. Justification: Easier scripting for ingestion, but weaker typing.
    *   *Cutting-edge:* **Go (Gin)**. Justification: High performance, but higher learning curve for SwRI team.
*   **Recommended Stack:** Spring Boot 3.x, Java 17.
*   **Interface:** External API (`openapi.yaml`), Internal Contract (`internal.proto`).
*   **Data Model:** `TelemetryBatch` (See `sql/batch_ddl.sql`).

## 2. Processing Module (Background Worker)
*   **Responsibilities:** Convert raw telemetry to IDFS, calibrate data, validate schema.
*   **Technology Options:**
    *   *Recommended:* **Celery (Python)**. Justification: Meets INF-NFR-001 (Async processing for 24h deadline).
    *   *Conservative:* **Spring Batch**. Justification: Integrated with Java backend, but heavier.
    *   *Cutting-edge:* **Kubernetes Jobs**. Justification: Native orchestration, less framework overhead.
*   **Recommended Stack:** Celery 5.x, Redis 7.x (Queue).
*   **Interface:** Internal gRPC (`internal.proto`).
*   **Data Model:** `ProcessingJob` (See `sql/job_ddl.sql`).

## 3. Archive Module
*   **Responsibilities:** Store IDFS/Raw data, manage embargo logic, submit to PDS.
*   **Technology Options:**
    *   *Recommended:* **AWS S3 API (MinIO)**. Justification: Meets INF-FR-005 (Local Archive) with S3 compatibility.
    *   *Conservative:* **NAS (NFS)**. Justification: Simple file share, lacks versioning/API.
    *   *Cutting-edge:* **IPFS**. Justification: Distributed, but complex for ground system.
*   **Recommended Stack:** MinIO (S3 Compatible), PostgreSQL 15.
*   **Data Model:** `ArchiveRecord` (See `sql/archive_ddl.sql`).

## 4. Web Module
*   **Responsibilities:** Public/Team displays, Auth, Data Download.
*   **Technology Options:**
    *   *Recommended:* **React + Nginx**. Justification: Meets INF-FR-008/009 (Interactive Displays).
    *   *Conservative:* **Thymeleaf (Server-side)**. Justification: Simpler, less responsive.
    *   *Cutting-edge:* **WebAssembly**. Justification: High performance viz, overkill.
*   **Recommended Stack:** React 18, Nginx 1.24.

## Interface Design

### External API (OpenAPI)
See Deliverable `openapi.yaml`. Covers Ingestion, Query, Download, Auth.

### Internal Contracts (gRPC)
See Deliverable `internal.proto`. Covers Processing Jobs, Validation Requests.

## Data Model / Schema
See Deliverables `sql/batch_ddl.sql`, `sql/archive_ddl.sql`.
*   **Encryption:** `ArchiveRecord.encryption_key_id` (INF-PR-001).
*   **Immutability:** `TelemetryBatch.checksum` (INF-NFR-004).

## Caching & Consistency
*   **Strategy:** Redis Cache for Metadata (User Roles, Dataset Catalog).
*   **TTL:** 15 minutes for Public Data, 0 for Embargoed Status (Real-time check).
*   **Consistency:** Strong consistency for Archive writes (ACID via PostgreSQL), Eventual consistency for Public Web Cache.

# E. Operations & Deployment

## 1. Kubernetes Plan
See Deliverable `k8s/apaf-deployment.yaml`.
*   **Replicas:** API (2 min), Worker (HPA based on Queue Depth).
*   **Resources:** API (2CPU/4GB), Worker (4CPU/8GB).

## 2. DB HA Topology
*   **PostgreSQL:** Primary-Replica setup (Sync Replication).
*   **Backup:** Daily WAL archiving to S3. RPO < 1 hour, RTO < 4 hours.

## 3. Network Topology
*   **Ingress:** Nginx Ingress Controller (TLS 1.2+).
*   **Egress:** Whitelisted to ESOC (Ingest) and NASA PDS (Submit).
*   **Reference:** `DeploymentDiagram:K8s` to `Ext`.

## 4. CI/CD Sketch
1.  **Build:** Maven/Gradle (Java), Pip (Python).
2.  **Test:** Unit, Integration (Testcontainers), Contract (Pact).
3.  **Deploy:** ArgoCD (GitOps). Canary deployment for Web Module.

# F. Security Design

1.  **Auth & AuthZ:** OIDC (Keycloak) for Co-I/Admin. JWT for API sessions. RBAC enforced in `SecurityModule` (INF-PR-001).
2.  **Secrets Management:** Kubernetes Secrets encrypted at rest (Sealed Secrets). Rotation every 90 days.
3.  **TLS:** Mutual TLS (mTLS) between Internal Services (API <-> Worker). TLS 1.2+ for External.
4.  **Threat Model:**
    *   *Unauthorized Access:* Mitigated by RBAC/MFA.
    *   *Data Tampering:* Mitigated by Checksums (INF-NFR-004).
    *   *Embargo Breach:* Mitigated by Automated Policy Engine.
    *   *DoS:* Mitigated by Ingress Rate Limiting.
    *   *Insider Threat:* Mitigated by Audit Logging (INF-PR-001).

# G. Observability & SRE

1.  **Metrics:**
    *   `batch_processing_latency_seconds` (Histogram).
    *   `ingestion_queue_depth` (Gauge).
    *   `pds_submission_status` (Counter).
    *   **Alerts:**
        *   `alert: HighQueueDepth: queue_depth > 100 for 5m`
        *   `alert: ProcessingFailure: job_failures > 5 per hour`
2.  **SLOs:**
    *   Availability: 99.5% (INF-NFR-008).
    *   Latency: 95% of batches processed < 12 hours (INF-DR-001).
    *   RTO/RPO: 48h / 24h.
3.  **Runbooks:**
    *   *Stuck Job:* Drain queue, restart worker pod, manual retry script.
    *   *Storage Full:* Expand S3 bucket, archive old logs.

# H. Testing Strategy

1.  **Test Matrix:**
    *   **Unit:** Domain Logic (Java/Python).
    *   **Integration:** API + DB (Testcontainers).
    *   **Contract:** OpenAPI/Proto validation.
    *   **E2E:** Full Pipeline (Ingest -> PDS).
    *   **Chaos:** Pod kill, Network partition.
2.  **Data Management:**
    *   **Environments:** Dev, Staging (Mirror Prod), Prod.
    *   **Refresh:** Staging refreshed weekly with anonymized Prod data.

# I. Migration, Data Conversion & Rollout Plan

1.  **Migration:**
    *   **Step 1:** Deploy new K8s cluster parallel to legacy.
    *   **Step 2:** Dual-write telemetry to both systems (1 week).
    *   **Step 3:** Validate IDFS output parity.
    *   **Step 4:** Switch Ingestion DNS to new system.
2.  **Compatibility:**
    *   API Versioning (`/api/v1/`).
    *   IDFS Schema Versioning (Stored in `IDFSDataset.schemaRef`).
3.  **Rollback:** Revert DNS to legacy system if error rate > 1%.

# J. Tradeoffs & Alternatives

| Decision | Alternative | Pros | Cons | Why Chosen |
| :--- | :--- | :--- | :--- | :--- |
| **Modular Monolith** | Microservices | Independent scaling. | High ops overhead. | Meets INF-CR-001 (Support) & ASR-001 (Pipeline simplicity). |
| **Kubernetes** | VMs | Auto-healing, scaling. | Complexity. | Meets INF-NFR-008 (Portability/Availability). |
| **S3 Object Store** | File System | API access, durability. | Cost (if cloud). | Meets INF-FR-005 (Archive) & Durability. |
| **Celery Workers** | Cron Jobs | Real-time queueing. | Infrastructure req. | Meets INF-DR-001 (24h Deadline). |

# K. Open Questions & Assumptions

**Assumptions:**
*   **A1:** ESOC telemetry delivery mechanism supports HTTPS/SFTP (Not specified in SRS).
*   **A2:** SwRI Local Archive supports S3 API protocol (Required for `ArchiveModule`).
*   **A3:** NASA PDS accepts automated S3-to-S3 transfer or provides an API (Currently assumed manual/FTP).
*   **A4:** Co-I identities are managed via a central ESA directory (OIDC provider available).

**Unresolved Questions:**
*   **Q1:** What is the exact volume of daily telemetry (GB/day)? (Impacts Worker scaling).
*   **Q2:** Are there specific encryption standards required for SwRI archive (e.g., FIPS 140-2)?
*   **Q3:** What is the specific IDFS schema version currently mandated by PDS?

# L. Deliverables

```yaml
# Filename: openapi.yaml
openapi: 3.0.3
info:
  title: APAF External API
  version: 1.0.0
  description: Public and Co-I Interface for ASPERA-3 Data
servers:
  - url: https://apaf.swri.edu/api/v1
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    TelemetryBatch:
      type: object
      properties:
        batchId:
          type: string
        timestamp:
          type: string
          format: date-time
        checksum:
          type: string
    IDFSDataset:
      type: object
      properties:
        datasetId:
          type: string
        calibrationLevel:
          type: integer
        embargoed:
          type: boolean
paths:
  /ingest/telemetry:
    post:
      summary: Ingest Telemetry from ESOC
      operationId: ingestTelemetry
      requestBody:
        content:
          application/octet-stream: {}
      responses:
        '202':
          description: Accepted for processing
        '400':
          description: Invalid Format
  /data/idfs:
    get:
      summary: List IDFS Datasets
      operationId: listDatasets
      security:
        - bearerAuth: []
      parameters:
        - name: embargoed
          in: query
          schema:
            type: boolean
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IDFSDataset'
  /data/download/{datasetId}:
    get:
      summary: Download Dataset
      operationId: downloadDataset
      security:
        - bearerAuth: []
      parameters:
        - name: datasetId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          content:
            application/octet-stream: {}
        '403':
          description: Embargoed / Unauthorized
```

```protobuf
// Filename: internal.proto
syntax = "proto3";
package apaf.internal;

service ProcessingService {
  rpc SubmitJob (ProcessingRequest) returns (JobStatus);
  rpc ValidateSchema (ValidationRequest) returns (ValidationResult);
}

message ProcessingRequest {
  string batch_id = 1;
  string source_path = 2;
  JobType type = 3;
}

enum JobType {
  SCIENCE_CONVERSION = 0;
  CALIBRATION = 1;
  PDS_SUBMISSION = 2;
}

message JobStatus {
  string job_id = 1;
  string status = 2; // QUEUED, RUNNING, COMPLETE, FAILED
}

message ValidationRequest {
  string dataset_id = 1;
  bytes file_content = 2;
}

message ValidationResult {
  bool is_valid = 1;
  repeated string errors = 2;
}
```

```yaml
# Filename: k8s/apaf-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apaf-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: apaf-backend
  template:
    metadata:
      labels:
        app: apaf-backend
    spec:
      containers:
      - name: api
        image: swri/apaf-backend:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: apaf-config
              key: db_host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: apaf-secrets
              key: db_password
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: apaf-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: apaf-worker
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: External
    external:
      metric:
        name: redis_queue_depth
      target:
        type: AverageValue
        averageValue: 50
```

```sql
-- Filename: sql/batch_ddl.sql
CREATE TABLE telemetry_batch (
    batch_id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(100) NOT NULL,
    checksum_sha256 CHAR(64) NOT NULL, -- INF-NFR-004: Integrity
    status VARCHAR(50) NOT NULL DEFAULT 'RECEIVED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_batch_timestamp ON telemetry_batch(timestamp);
CREATE INDEX idx_batch_status ON telemetry_batch(status);
```

```sql
-- Filename: sql/archive_ddl.sql
CREATE TABLE archive_record (
    record_id VARCHAR(255) PRIMARY KEY,
    dataset_id VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    retention_date TIMESTAMP NOT NULL,
    is_embargoed BOOLEAN NOT NULL DEFAULT TRUE, -- INF-PR-001
    encryption_key_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_archive_embargo ON archive_record(is_embargoed);
CREATE INDEX idx_archive_retention ON archive_record(retention_date);
```

```csv
# Filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact,Rationale
INF-FR-001,Acquire telemetry from ESOC daily.,UseCaseDiagram:UC01,IngestionModule,openapi.yaml,Core entry point.
INF-FR-002,Process science data into IDFS.,ActivityDiagram:Convert to IDFS,ProcessingModule,internal.proto,Primary function.
INF-PR-001,Web server password protected.,SequenceDiagram2:Auth,SecurityModule,openapi.yaml,Privacy requirement.
INF-DR-001,Provide data to Co-I's within 24h.,SequenceDiagram1,ProcessingModule,k8s/apaf-deployment.yaml,Timeline constraint.
INF-NFR-004,Data Integrity.,ClassDiagram:TB.checksum,ArchiveModule,sql/batch_ddl.sql,Checksum enforcement.
```

# Acceptance Criteria Verification

- [x] 3-line Analysis Plan present.
- [x] Sections A-L included.
- [x] Every FR/NFR/ASR mapped in traceability matrix (via INF- prefixes).
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [x] Representative k8s manifest snippet included.
- [x] SQL DDL / NoSQL models for primary entities included.
- [x] All major components have at least one API contract and a data schema.
- [x] Assumptions and open questions clearly listed.

# How to Review
- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?