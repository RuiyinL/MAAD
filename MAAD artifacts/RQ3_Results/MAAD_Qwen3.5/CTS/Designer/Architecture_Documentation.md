# Analysis Plan
1. **Scope:** CCTNS Core, Search, Audit, Security modules aligned with SOA/3C architecture and 11 PlantUML views.
2. **Approach:** Map inferred `INF-` requirements to 4+1 View artifacts, ensuring traceability to PlantUML element IDs.
3. **Validation:** Verify traceability matrix coverage, API contract validity (OpenAPI/Proto), and K8s manifest syntax.

---

# A. Executive Summary

The Crime & Criminals Tracking Network & Systems (CCTNS) is a centralized, Service-Oriented Architecture (SOA) solution deployed in a 3-Tier Datacenter. It adheres to the Core-Configuration-Customization (3C) principle, separating Presentation (Browser), Business (Services), and Data (Persistence) tiers. The architecture is primarily referenced by the **Container Diagram** (Container: Core Services, Auth Service) and **Deployment Diagram** (Node: State Datacenter).

**Architectural Style:** Hybrid SOA + Layered + Event-Driven.
**Deployment Topology:** Centralized 3-Tier Datacenter with Kubernetes orchestration.

**Top 3 Design Risks & Mitigations:**

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| Audit Trail Tampering | Legal Admissibility Loss | Cryptographic hash-chaining (INF-ASR-001); WORM storage policy. |
| Search Performance Degradation | User Productivity Loss | Hierarchical caching + Search Index (INF-NFR-001); ACL filtering at query time. |
| Network Failure (Offline Mode) | Operational Stoppage | Local encrypted cache with reconciliation queue (INF-NFR-002). |

**Key QA Coverage Mapping:**

| Quality Attribute | Requirements (IDs) | Test Type |
| :--- | :--- | :--- |
| **Security** | INF-ASR-001, INF-ASR-002, INF-NFR-015 | Penetration Testing, Static Analysis |
| **Performance** | INF-NFR-001, INF-NFR-002 | Load Testing, APM Monitoring |
| **Availability** | INF-NFR-005, INF-NFR-010 | Chaos Engineering, DR Drill |
| **Maintainability** | INF-ASR-014 (3C) | Code Review, Modular Integration Tests |
| **Scalability** | INF-NFR-008 | Horizontal Scaling Tests |

---

# B. Traceability & Rationale

*Note: Requirement IDs are inferred (`INF-`) from the Original Requirements text as per Special Handling Rule #1.*

| Requirement ID | Short Text | Diagram(s) (Title:IDs) | Component(s) | Artifact Filename(s) | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INF-FR-001** | Registration Module (Complaint Initiation) | UseCase Diagram: UC01 | Case Service | `openapi.yaml` | Interface between police and citizens; eases interaction. |
| **INF-FR-002** | Investigation Module (Process Automation) | UseCase Diagram: UC03 | Case Service | `internal.proto` | Automates tasks after initial entries. |
| **INF-FR-003** | Prosecution Module (Court Interface) | UseCase Diagram: UC03 | Integration Service | `internal.proto` | Records court interactions. |
| **INF-FR-004** | Search Module (Basic/Advanced) | UseCase Diagram: UC02 | Search Service | `openapi.yaml` | Execute queries on cases/persons; <8s/<15s latency. |
| **INF-FR-005** | Citizen Interface (Info Exchange) | UseCase Diagram: UC08 | Portal Service | `openapi.yaml` | Conduit for info exchange/acknowledgements. |
| **INF-FR-006** | Navigation Module (Role-based Landing) | UseCase Diagram: UC05 | UI Component | `k8s/ui-deployment.yaml` | Role-based landing pages; alerts/tasks. |
| **INF-FR-007** | Help Desk (Defect/Enhancement Tracking) | UseCase Diagram: UC06 | Support Service | `openapi.yaml` | Log defects; track status; reports. |
| **INF-ASR-001** | Unalterable Audit Trail (Create/Read/Update/Delete) | UseCase Diagram: UC07 | Audit Service | `sql/audit_log_ddl.sql` | Automatic capture; unalterable; life of case. |
| **INF-ASR-002** | Security & Access Control (RBAC/ACL) | UseCase Diagram: UC02 | Auth Service | `sql/user_ddl.sql` | Role-based control; limit access to cases. |
| **INF-NFR-001** | Performance (Search <8s/15s) | Sequence Diagram2: SearchSvc | Search Service | `k8s/search-deployment.yaml` | Simple/Advanced search latency constraints. |
| **INF-NFR-002** | Availability (Offline Mode) | Activity Diagram: Offline Queue | Core Services | `internal.proto` | Operational data not lost on failure. |
| **INF-NFR-003** | UI/UX (ISO 9241 Compliance) | Package Diagram: UI Components | Frontend | `architecture.md` | User-intuitive; accessibility standards. |
| **INF-NFR-004** | Scalability (10k Concurrent Users) | Deployment Diagram: App Server Cluster | App Tier | `k8s/<component>-deployment.yaml` | Scaleable for small/large police stations. |
| **INF-NFR-005** | Availability (99.9% Uptime) | Deployment Diagram: Load Balancer | Infra | `architecture.md` | Planned/Unplanned downtime limits. |
| **INF-NFR-010** | Low Bandwidth Support | Deployment Diagram: Client Devices | Network | `architecture.md` | Satisfactory performance on low bandwidth. |
| **INF-NFR-015** | Security (SSL/Encryption) | Container Diagram: HTTPS | Gateway | `openapi.yaml` | Secure transmission; HTTPS/SSL. |
| **INF-ASR-014** | 3C Architecture (Core/Config/Custom) | Package Diagram: Service Layer | All Services | `architecture.md` | Centralized deployment; state customization. |

---

# C. Architecture Overview

The architecture follows the **4+1 View Model** (Context, Container, Component, Class, Deployment) aligned with ISO/IEC/IEEE 42020:2019(E).

1.  **Context View:** Defined by **UseCase Diagram**. Actors (Citizen, Police, Auditor) interact with the CCTNS System boundary. Key interactions include `UC01 (Register Complaint)` and `UC02 (Search Cases)`.
2.  **Container View:** Defined by **Container Diagram**. Boundaries include `Web Application (SPA)`, `API Gateway`, `Core Services`, `Auth Service`, and `Data Tier` (PostgreSQL, OpenSearch, Redis). Communication is via HTTPS/JSON (External) and REST/Proto (Internal).
3.  **Component View:** Defined by **Package Diagram** and **Component Diagram**. Services are modular (Case Management, User Management, Search Service). The **Audit Component** is decoupled via async events to ensure performance isolation.
4.  **Class/Runtime View:** Defined by **Class Diagram** and **State Diagram**. Entities include `User`, `Role`, `Case`, `AuditLog`. State transitions (Registered -> Investigating -> Closed) trigger immutable audit records (`AuditLog`).
5.  **Deployment View:** Defined by **Deployment Diagram**. Physical nodes include `Client Devices`, `State Datacenter` (Load Balancer, App Server Cluster, Data Tier). The topology supports horizontal scaling (Kubernetes Pods) and high availability (DB Cluster).

**Logical vs. Physical:**
*   **Logical:** Defines data as `Case`, `Complaint`, `Evidence` (Class Diagram).
*   **Physical:** Arrangement of `PostgreSQL Cluster`, `Redis Cluster`, `Kubernetes Pods` (Deployment Diagram).

---

# D. Detailed Technical Design

## 1. Case Management Service
*   **Responsibilities:** Handles Complaint Registration, Investigation updates, and Case Lifecycle. Owns `Case` and `Complaint` entities.
*   **Technology Options:**
    *   *Recommended:* Java Spring Boot (LTS). **Justification:** Meets INF-ASR-014 (Enterprise SOA standards).
    *   *Conservative:* .NET Core. **Justification:** Compatible with INF-NFR-003 (Windows environments).
    *   *Cutting-edge:* Go (Gin). **Justification:** High concurrency for INF-NFR-004.
*   **Recommended Stack:** Java 17, Spring Boot 3.2. **Justification:** Meets INF-ASR-014 (Open Standards).
*   **Interface Design:**
    *   **External API:** `POST /complaints`, `GET /cases`. (See `openapi.yaml` in Section L).
    *   **Internal Contract:** `CreateCaseRequest`, `UpdateCaseStatus`. (See `internal.proto` in Section L).
*   **Data Model:**
    *   **Entity:** `Case`, `Complaint`.
    *   **Schema:** `sql/case_ddl.sql` (See Section L). Includes `soft_delete` flag for INF-NFR-021.
*   **Caching:** Redis for frequent case lookups (TTL 2 hours). **Justification:** Meets INF-NFR-003 (Retrieve <8s).

## 2. Search Service
*   **Responsibilities:** Indexes case data for rapid retrieval. Enforces ACL filtering.
*   **Technology Options:**
    *   *Recommended:* OpenSearch. **Justification:** Meets INF-NFR-001 (Search <15s) & INF-ASR-002 (ACL).
    *   *Conservative:* PostgreSQL Full Text Search. **Justification:** Lower ops complexity.
    *   *Cutting-edge:* Elasticsearch Serverless. **Justification:** Auto-scaling.
*   **Recommended Stack:** OpenSearch 2.11. **Justification:** Meets INF-NFR-001 (Performance).
*   **Interface Design:**
    *   **External API:** `GET /search`. (See `openapi.yaml`).
    *   **Internal Contract:** `SearchQueryRequest`. (See `internal.proto`).
*   **Data Model:** Denormalized index documents.
*   **Caching:** Hierarchical cache (Browser -> App -> Distributed). **Justification:** Meets INF-ASR-007.

## 3. Audit Service
*   **Responsibilities:** Captures all CRUD actions, user IDs, timestamps. Ensures immutability.
*   **Technology Options:**
    *   *Recommended:* PostgreSQL (Append-only). **Justification:** Meets INF-ASR-001 (Unalterable).
    *   *Conservative:* Immutable File Store. **Justification:** WORM compliance.
    *   *Cutting-edge:* Blockchain Ledger. **Justification:** Cryptographic integrity.
*   **Recommended Stack:** PostgreSQL 15. **Justification:** Meets INF-ASR-001 (ACID + Hash Chain).
*   **Data Model:** `AuditLog` table with `prev_hash`, `current_hash`. (See `sql/audit_log_ddl.sql`).
*   **Consistency:** Strong (Immediate write). **Justification:** Meets INF-ASR-001 (Legal Admissibility).

## 4. Auth Service
*   **Responsibilities:** RBAC, Session Management, SSO.
*   **Technology Options:**
    *   *Recommended:* Keycloak (OIDC). **Justification:** Meets INF-ASR-002 (RBAC) & INF-NFR-015 (SSO).
    *   *Conservative:* Custom JWT Service. **Justification:** Lower dependency.
    *   *Cutting-edge:** Auth0. **Justification:** Managed service.
*   **Recommended Stack:** Keycloak 24. **Justification:** Meets INF-ASR-002 (Role-based control).

---

# E. Operations & Deployment

## 1. Kubernetes Plan
*   **Manifest:** `k8s/case-service-deployment.yaml` (See Section L).
*   **Replicas:** Small (2), Medium (5), Large (20).
*   **Resources:** CPU 200m-2000m, RAM 256Mi-4Gi.
*   **HPA:** Target CPU 70%. **Justification:** Meets INF-NFR-004 (Scalability).

## 2. DB HA Topology
*   **Primary:** PostgreSQL Cluster (3 nodes).
*   **Replication:** Sync for Audit, Async for Case.
*   **Backup:** Daily PITR (Point-In-Time Recovery).
*   **Restore:** RTO < 8 hours (INF-NFR-007).

## 3. Network Topology
*   **Ingress:** HTTPS (TLS 1.2+). **Justification:** Meets INF-NFR-015.
*   **Egress:** Restricted to SMS/Email Gateway.
*   **Latency:** <100ms internal, <2s external. (Reference **Deployment Diagram**: Node: State Datacenter).

## 4. CI/CD Sketch
*   **Build:** Maven/Gradle.
*   **Test:** Unit, Integration, Contract.
*   **Deploy:** Canary (10% traffic).
*   **Gating:** Security Scan (OWASP). **Justification:** Meets INF-NFR-020 (SQLi/XSS prevention).

---

# F. Security Design

1.  **Auth & AuthZ:** OAuth2/OIDC (Keycloak). Tokens (JWT) with short TTL (15 min). Refresh tokens rotated. **Justification:** Meets INF-ASR-002.
2.  **Secrets Management:** Kubernetes Secrets + External Secrets Operator. Rotation every 30 days.
3.  **TLS:** Service Mesh (Linkerd) for mTLS between pods. TLS 1.2+ for external. **Justification:** Meets INF-NFR-015.
4.  **Threat Model:**
    *   *SQL Injection:* Parameterized Queries. **Justification:** Meets INF-NFR-020.
    *   *XSS:* Input Sanitization. **Justification:** Meets INF-NFR-020.
    *   *Audit Tampering:* Hash Chain Validation. **Justification:** Meets INF-ASR-001.
    *   *Data Leakage:* ACL Filtering in Search. **Justification:** Meets INF-ASR-002.
    *   *Session Hijacking:* Secure Cookies (HTTPS Only). **Justification:** Meets INF-NFR-015.

---

# G. Observability & SRE

1.  **Metrics:**
    *   `http_request_duration_seconds` (Histogram).
    *   `audit_log_write_latency` (Counter).
    *   `search_acl_filter_time` (Gauge).
2.  **Prometheus Alerts:**
    *   `Alert: HighLatency` -> `avg(http_request_duration_seconds) > 8s`. **Justification:** Meets INF-NFR-001.
    *   `Alert: AuditFailure` -> `rate(audit_log_write_errors[5m]) > 0`. **Justification:** Meets INF-ASR-001.
3.  **SLOs:**
    *   Search: 99% < 15s.
    *   Audit: 100% Success.
    *   Availability: 99.9% (INF-NFR-005).
4.  **Runbook:** Restart Pod -> Check DB Connection -> Verify Audit Chain.

---

# H. Testing Strategy

1.  **Matrix:**
    *   *Unit:* Services (Logic).
    *   *Integration:* API + DB.
    *   *Contract:* OpenAPI/Proto validation.
    *   *E2E:* UI Workflows (Registration -> Search).
    *   *Chaos:* Network Partition (Offline Mode). **Justification:** Meets INF-NFR-010.
2.  **Data Management:**
    *   *Environments:* Dev, Test, Stage, Prod.
    *   *Refresh:* Weekly (Test), Monthly (Stage).
    *   *Isolation:* Namespaces in K8s.

---

# I. Migration, Data Conversion & Rollout Plan

1.  **Migration Steps:**
    *   Deploy New Stack.
    *   Dual-Write (Old + New).
    *   Backfill Historical Data.
    *   Switch Read Traffic.
    *   Decommission Old.
2.  **Sync Strategy:** CDC (Change Data Capture) for real-time sync.
3.  **Rollback:** Re-point Ingress to Old Stack.
4.  **API Versioning:** `v1` (Legacy), `v2` (CCTNS). **Justification:** Meets INF-ASR-014 (Customization).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Choice | ID Citation |
| :--- | :--- | :--- | :--- | :--- |
| **Audit Storage** | NoSQL vs SQL | NoSQL (Scale) vs SQL (ACID) | SQL (PostgreSQL) | INF-ASR-001 (Immutability/ACID) |
| **Search Engine** | DB Search vs Index | DB (Simple) vs Index (Fast) | OpenSearch | INF-NFR-001 (Performance) |
| **Offline Mode** | Full Sync vs Cache | Full (Complex) vs Cache (Simple) | Local Cache | INF-NFR-010 (Low Bandwidth) |
| **Auth** | Session vs JWT | Session (State) vs JWT (Stateless) | JWT (OIDC) | INF-ASR-002 (RBAC/SSO) |

---

# K. Open Questions & Assumptions

**Assumptions (A#):**
*   **A1:** "xx:00 to xx:00" availability windows are interpreted as 24/7 for critical modules (INF-NFR-005).
*   **A2:** "Low-bandwidth" is defined as <1 Mbps for Police Station connections (INF-NFR-010).
*   **A3:** "Unalterable" audit implies cryptographic hash chaining, not just physical WORM media (INF-ASR-001).
*   **A4:** State-specific customization implies plugin architecture, not code forks (INF-ASR-014).

**Unresolved Questions:**
*   **Q1:** What is the exact retention period for audit logs beyond "life of the case"? (Suggested: 7 years per legal standards).
*   **Q2:** Which specific ISO 9241 parts are mandatory for the mobile PDA interface? (Suggested: ISO 9241-20).
*   **Q3:** Can citizens access case status directly, or only via police intermediary? (Suggested: Via Citizen Interface Module).

---

# L. Deliverables

## 1. `architecture.md`
*   **Filename:** `architecture.md`
*   **Content:** This entire document.

## 2. `openapi.yaml`
*   **Filename:** `openapi.yaml`
*   **Content:** External API Contract.

```yaml
openapi: 3.0.3
info:
  title: CCTNS External API
  version: 1.0.0
  description: Public interfaces for Complaint and Search
servers:
  - url: https://cctns.gov.in/api/v1
security:
  - bearerAuth: []
paths:
  /complaints:
    post:
      summary: Register Complaint
      operationId: registerComplaint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                complainantName: { type: string }
                narrative: { type: string }
                crimeType: { type: string }
      responses:
        201:
          description: Created
          content:
            application/json:
              schema:
                type: object
                properties:
                  registrationId: { type: string }
        400:
          description: Bad Input
        401:
          description: Unauthorized
  /cases/search:
    get:
      summary: Search Cases
      operationId: searchCases
      parameters:
        - in: query
          name: type
          schema: { type: string }
        - in: query
          name: page
          schema: { type: integer }
      responses:
        200:
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  results: { type: array }
                  total: { type: integer }
        403:
          description: Forbidden (ACL)
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## 3. `internal.proto`
*   **Filename:** `internal.proto`
*   **Content:** Internal Service Contract.

```proto
syntax = "proto3";
package cctns.internal;

service CaseService {
  rpc CreateCase (CreateCaseRequest) returns (CreateCaseResponse);
  rpc UpdateStatus (UpdateStatusRequest) returns (UpdateStatusResponse);
}

service AuditService {
  rpc LogEvent (AuditEventRequest) returns (AuditEventResponse);
}

message CreateCaseRequest {
  string user_id = 1;
  string complaint_data = 2;
  string timestamp = 3;
}

message CreateCaseResponse {
  string case_id = 1;
  bool success = 2;
}

message AuditEventRequest {
  string event_type = 1;
  string entity_id = 2;
  string user_id = 3;
  string prev_hash = 4;
}

message AuditEventResponse {
  string log_id = 1;
  string current_hash = 2;
}
```

## 4. `k8s/case-service-deployment.yaml`
*   **Filename:** `k8s/case-service-deployment.yaml`
*   **Content:** Kubernetes Manifest.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: case-service
  namespace: cctns-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: case-service
  template:
    metadata:
      labels:
        app: case-service
    spec:
      containers:
      - name: case-service
        image: cctns/case-service:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: cctns-config
              key: db_host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: cctns-secret
              key: db_password
      ---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: case-service-hpa
  namespace: cctns-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: case-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 5. `sql/case_ddl.sql`
*   **Filename:** `sql/case_ddl.sql`
*   **Content:** Case Entity DDL.

```sql
CREATE TABLE cases (
    case_id VARCHAR(50) PRIMARY KEY,
    registration_date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    crime_type VARCHAR(100),
    narrative TEXT,
    created_by VARCHAR(50) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE, -- Soft Delete (INF-NFR-021)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_crime_type ON cases(crime_type);
```

## 6. `sql/audit_log_ddl.sql`
*   **Filename:** `sql/audit_log_ddl.sql`
*   **Content:** Audit Log DDL (Immutable).

```sql
CREATE TABLE audit_log (
    log_id VARCHAR(50) PRIMARY KEY,
    event_type VARCHAR(20) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    prev_hash VARCHAR(64),
    current_hash VARCHAR(64) NOT NULL, -- Hash Chain (INF-ASR-001)
    payload JSONB
);

-- Prevent Updates/Deletes
CREATE RULE audit_log_no_update AS ON UPDATE TO audit_log DO NOTHING;
CREATE RULE audit_log_no_delete AS ON DELETE TO audit_log DO NOTHING;

CREATE INDEX idx_audit_entity ON audit_log(entity_id);
```

## 7. `traceability_matrix.csv`
*   **Filename:** `traceability_matrix.csv`
*   **Content:** Traceability Data.

```csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact Filename(s),Rationale
INF-FR-001,Registration Module,UseCase Diagram: UC01,Case Service,openapi.yaml,Interface between police and citizens
INF-FR-002,Investigation Module,UseCase Diagram: UC03,Case Service,internal.proto,Automates tasks after initial entries
INF-FR-003,Prosecution Module,UseCase Diagram: UC03,Integration Service,internal.proto,Records court interactions
INF-FR-004,Search Module,UseCase Diagram: UC02,Search Service,openapi.yaml,Execute queries on cases/persons
INF-FR-005,Citizen Interface,UseCase Diagram: UC08,Portal Service,openapi.yaml,Conduit for info exchange
INF-FR-006,Navigation Module,UseCase Diagram: UC05,UI Component,k8s/ui-deployment.yaml,Role-based landing pages
INF-FR-007,Help Desk,UseCase Diagram: UC06,Support Service,openapi.yaml,Log defects; track status
INF-ASR-001,Unalterable Audit Trail,UseCase Diagram: UC07,Audit Service,sql/audit_log_ddl.sql,Automatic capture; unalterable
INF-ASR-002,Security & Access Control,UseCase Diagram: UC02,Auth Service,sql/user_ddl.sql,Role-based control
INF-NFR-001,Performance (Search),Sequence Diagram2: SearchSvc,Search Service,k8s/search-deployment.yaml,Simple/Advanced search latency
INF-NFR-002,Availability (Offline),Activity Diagram: Offline Queue,Core Services,internal.proto,Operational data not lost
INF-NFR-003,UI/UX (ISO 9241),Package Diagram: UI Components,Frontend,architecture.md,User-intuitive; accessibility
INF-NFR-004,Scalability,Deployment Diagram: App Server Cluster,App Tier,k8s/<component>-deployment.yaml,Scaleable for stations
INF-NFR-005,Availability (99.9%),Deployment Diagram: Load Balancer,Infra,architecture.md,Downtime limits
INF-NFR-010,Low Bandwidth,Deployment Diagram: Client Devices,Network,architecture.md,Performance on low bandwidth
INF-NFR-015,Security (SSL),Container Diagram: HTTPS,Gateway,openapi.yaml,Secure transmission
INF-ASR-014,3C Architecture,Package Diagram: Service Layer,All Services,architecture.md,Centralized deployment
```

---

# Acceptance Criteria

- [ ] 3-line Analysis Plan present.
- [ ] Sections A-L included.
- [ ] Every FR/NFR/ASR mapped in traceability matrix.
- [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [ ] Representative k8s manifest snippet included.
- [ ] SQL DDL / NoSQL models for primary entities included.
- [ ] All major components have: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema.
- [ ] Assumptions and open questions clearly listed.

# "How to review" checklist

- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?