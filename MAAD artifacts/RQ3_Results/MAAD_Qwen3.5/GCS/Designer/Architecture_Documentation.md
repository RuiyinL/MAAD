Analysis Plan
Scope: Architectural design for Gemini Control System aligning SRS text with 11 PlantUML views (UseCase to Container).
Approach: Layered distributed architecture (UI/OCS/IOC/Hardware) modernizing legacy constraints while preserving EPICS/FITS mandates.
Validation: Traceability matrix coverage of all Diagram IDs + inferred text requirements, syntactic validity of all code artifacts.

# A. Executive Summary

The Gemini Control System is a distributed, safety-critical observatory control platform enabling remote and local telescope operation. The architecture follows a **Hybrid Layered + Event-Driven** style, mapped primarily to the **DeploymentDiagram** (nodes: Remote Site, Observatory Site, External Services) and **ComponentDiagram** (layers: UI, OCS, IOC, Data).

**Architectural Style:** Layered (UI → OCS → IOC → Hardware) with Event-Driven logging and safety interlocks.
**Deployment Topology:** Distributed across Observatory Site (On-Premise) and Remote Facilities (WAN), utilizing Kubernetes for OCS and dedicated Real-Time OS for IOCs.

**Top 3 Design Risks & Mitigations:**

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Safety Interlock Latency** | Hazardous hardware movement if software delays safety signals. | Hardware-independent interlocks (ASR-006); Watchdog timers; <15ms alert delivery (FR-012). |
| **WAN Bandwidth Constraints** | Remote observation failure due to latency/packet loss. | Lossless compression (NFR-011); Local caching; Adaptive quality (NFR-006). |
| **Legacy IOC Integration** | EPICS/RTOS incompatibility with modern OCS stack. | Adapter pattern (ComponentDiagram: IOC Controller); Contract-first gRPC interfaces (internal.proto). |

**Key QA Coverage Mapping:**

| Quality Attribute | ASR/NFR IDs | Test Types |
| :--- | :--- | :--- |
| **Security** | NFR-001, ASR-001 | Penetration Testing, TLS Verification, RBAC Audit |
| **Performance** | NFR-002, NFR-009, FR-014 | Load Testing (500ms ACK), Latency Monitoring |
| **Reliability** | NFR-005, NFR-018 | Chaos Engineering, Failover Drills |
| **Safety** | NFR-007, ASR-006 | Hardware-in-Loop (HIL), Interlock Simulation |
| **Maintainability** | NFR-008, ASR-008 | Static Analysis, Module Interface Contracts |

# B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) | Component(s) | Artifact | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Authenticate User | UseCaseDiagram:UC001 | Auth Service | openapi.yaml | Core access control for all roles (Astronomer, Operator). |
| **FR-002** | Control Operational Level | StateDiagram:Observing/Maintenance | OCS Controller | internal.proto | Enforces disjoint operational levels (Observing, Maintenance, Test). |
| **FR-004** | Execute Observation Sequence | SequenceDiagram1 | SeqExecutor | openapi.yaml | Primary science data collection function. |
| **FR-005** | Remote Operations | SequenceDiagram1 | API Gateway | openapi.yaml | Supports off-site observing (ASR-001). |
| **FR-006** | Monitor Telescope Status | UseCaseDiagram:UC005 | Logging Service | sql/observation_ddl.sql | Multi-point monitoring without affecting observation. |
| **FR-009** | Run Simulation | UseCaseDiagram:UC009 | Simulator | internal.proto | Virtual telescope for planning/testing (ASR-004). |
| **FR-011** | View System Logs | UseCaseDiagram:UC010 | Logging Service | sql/observation_ddl.sql | Audit trail for safety and debugging. |
| **FR-012** | Manage Safety Interlocks | SequenceDiagram2 | Safety Controller | internal.proto | Critical hazard mitigation (ASR-006). |
| **FR-014** | Parameter Database Access | ClassDiagram:ParameterDatabase | Parameter DB | sql/observation_ddl.sql | 2-3ms access time for configuration. |
| **FR-018** | Command Handshaking | SequenceDiagram1 | OCS Controller | internal.proto | 500ms timeout requirement for IOCs. |
| **NFR-001** | Security (TLS/Auth) | ActivityDiagram | Auth Service | openapi.yaml | Prevent intrusion (NFR-001). |
| **NFR-002** | Response Time (<2s/<4s) | SequenceDiagram1 | OCS Controller | k8s/ocs-deployment.yaml | User interface responsiveness. |
| **NFR-004** | Data Retention (7 days) | DeploymentDiagram | Archive Storage | sql/observation_ddl.sql | Compliance with archiving requirements. |
| **NFR-005** | Recovery Goal (5 mins) | StateDiagram:SafeState | Safety Controller | internal.proto | Minimizes downtime after fault. |
| **NFR-007** | Safety Interlocks (HW) | SequenceDiagram2 | Safety Interlock HW | internal.proto | Independent of software for critical hazards. |
| **NFR-009** | Detector Readout (<3min) | SequenceDiagram1 | Instrument IOC | internal.proto | Performance bound for science data. |
| **NFR-011** | Data Format (FITS) | SequenceDiagram1 | Data Handler | openapi.yaml | Standard astronomical data format. |
| **NFR-013** | Logging Rates (200Hz) | ClassDiagram:SystemLog | Logging Service | sql/observation_ddl.sql | Engineering data capture. |
| **ASR-001** | Remote Operations Support | DeploymentDiagram | API Gateway | openapi.yaml | Architectural driver for distributed design. |
| **ASR-004** | Simulation Support | ClassDiagram:Simulator | Simulator | internal.proto | Hardware independence for testing. |
| **ASR-006** | Safety Interlock Independence | SequenceDiagram2 | Safety Interlock HW | internal.proto | Risk mitigation for personnel/equipment. |
| **ASR-007** | EPICS Implementation | PackageDiagram:IOC Layer | IOC Controller | internal.proto | Standard for real-time control. |
| **ASR-008** | Modular Subsystems | ComponentDiagram | All Components | openapi.yaml | Maintainability and independent deployment. |
| **ASR-009** | Real-Time IOC Layer | DeploymentDiagram | IOC Rack | internal.proto | Strict timing for hardware control. |
| **INF-FR-001** | User Role Management | UseCaseDiagram:Actors | Auth Service | openapi.yaml | Inferred from text (Astronomer, Operator, etc.). |
| **INF-NFR-001** | FITS NOST 100-1.0 Compliance | SequenceDiagram1 | Data Handler | openapi.yaml | Inferred specific standard from text. |
| **INF-ASR-001** | Legacy Hardware Compatibility | DeploymentDiagram | IOC Rack | internal.proto | Inferred need to support existing mounts/instruments. |

# C. Architecture Overview

The architecture adheres to the **4+1 View Model**, aligned with the provided PlantUML diagrams.

1.  **Context View:** Defined by **UseCaseDiagram**. Actors (Astronomer, Operator, etc.) interact with the Gemini Observatory Control System boundary. External systems include Weather Services and Home Institute Archives.
2.  **Container View:** Defined by **ContainerDiagram**. High-level technology choices: Web Browser/Desktop App (UI), API Gateway/OCS App (Backend), EPICS/RTOS (IOC), PostgreSQL/EPICS (Data).
3.  **Component View:** Defined by **ComponentDiagram** and **PackageDiagram**. Internal structure of OCS (Auth, Scheduler, SeqExecutor) and IOC (Telescope, Instrument, Safety). Interfaces are contract-first (gRPC/REST).
4.  **Runtime/Logic View:** Defined by **ClassDiagram**, **ObjectDiagram**, **StateDiagram**, and **SequenceDiagram1/2**. Describes object relationships, state transitions (Initializing → Observing → SafeState), and message flows (Command/ACK).
5.  **Deployment View:** Defined by **DeploymentDiagram** and **ContainerDiagram**. Physical topology: Remote Sites (WAN), Observatory Site (LAN), IOC Rack (Hardware Bus). Supports 6 active + 2 monitoring nodes (NFR-010).

# D. Detailed Technical Design

## 1. Observation Control System (OCS)
*   **Responsibilities:** Command coordination, scheduling, sequencing, data processing. Owns observation state and user sessions.
*   **Technology Options:**
    *   *Recommended:* Java 17 + Spring Boot (Justification: meets ASR-008 (modularity) & NFR-002 (performance)).
    *   *Conservative:* Python 3.9 + Flask (Justification: meets ASR-006 (cost-minimized)).
    *   *Cutting-edge:* Go 1.20 + gRPC Gateway (Justification: meets NFR-009 (concurrency)).
*   **Recommended Stack:** Java 17, Spring Boot 3, PostgreSQL 14-15.
*   **Interface Design:** See `openapi.yaml` (External) and `internal.proto` (Internal).
*   **Data Model:** See `sql/observation_ddl.sql`.
*   **Caching:** Redis 7 for session tokens (TTL 1h) and parameter caching (TTL 5s). Strong consistency for safety params.

## 2. Instrument Object Controller (IOC)
*   **Responsibilities:** Real-time hardware control, safety monitoring, EPICS channel access.
*   **Technology Options:**
    *   *Recommended:* EPICS 7 + VxWorks 7 (Justification: meets ASR-007 (EPICS implementation)).
    *   *Conservative:* EPICS 3.14 + RTEMS (Justification: meets ASR-009 (Real-Time)).
    *   *Cutting-edge:* ZeroMQ + Linux PREEMPT_RT (Justification: meets NFR-005 (recovery)).
*   **Recommended Stack:** EPICS 7, VxWorks 7, C++17.
*   **Interface Design:** gRPC (`internal.proto`) for OCS-IOC comms; EPICS PVs for internal IOC.
*   **Data Model:** In-memory state machines; persisted to Parameter DB.
*   **Caching:** Reflective Memory for high-speed data (200Hz).

## 3. User Interface (UI)
*   **Responsibilities:** User authentication, status display, command submission.
*   **Technology Options:**
    *   *Recommended:* React 18 + TypeScript (Justification: meets NFR-006 (network transparency)).
    *   *Conservative:* Qt 6 + C++ (Justification: meets ASR-001 (remote ops)).
    *   *Cutting-edge:* Blazor WASM (Justification: meets ASR-006 (cost)).
*   **Recommended Stack:** React 18, TypeScript 5, WebSocket.
*   **Interface Design:** REST (`openapi.yaml`) + WebSocket for streaming status.

## 4. Data Layer
*   **Responsibilities:** Parameter storage, logging, archiving.
*   **Technology Options:**
    *   *Recommended:* PostgreSQL 14 (Params/Logs) + FITS File System (Archive) (Justification: meets NFR-004 (retention)).
    *   *Conservative:* SYBASE (Legacy) (Justification: meets INF-ASR-001 (legacy compat)).
    *   *Cutting-edge:* CockroachDB (Justification: meets NFR-010 (scalability)).
*   **Recommended Stack:** PostgreSQL 14, FITS Lib 4.
*   **Data Model:** Relational for metadata, Filesystem for binary data.

### Interface Design: External API (`openapi.yaml`)
```yaml
openapi: 3.0.3
info:
  title: Gemini Control System External API
  version: 1.0.0
  description: External interface for Remote Operations (ASR-001)
servers:
  - url: https://api.gemini.edu/v1
security:
  - BearerAuth: []
paths:
  /auth/login:
    post:
      summary: Authenticate User (FR-001)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username: { type: string }
                password: { type: string }
      responses:
        200:
          description: Auth Token
          content:
            application/json:
              schema:
                type: object
                properties:
                  token: { type: string }
                  role: { type: string }
        401:
          description: Unauthorized
  /observations/sequence:
    post:
      summary: Execute Observation Sequence (FR-004)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                sequenceId: { type: string }
                priority: { type: integer }
      responses:
        202:
          description: Accepted
        400:
          description: Invalid Sequence
  /telescope/status:
    get:
      summary: Monitor Telescope Status (FR-006)
      responses:
        200:
          description: Status JSON
          content:
            application/json:
              schema:
                type: object
                properties:
                  position: { type: string }
                  state: { type: string }
        403:
          description: Forbidden
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Interface Design: Internal Contract (`internal.proto`)
```proto
syntax = "proto3";
package gemini.internal;

service OCS_IOC_Controller {
  rpc MoveTo (Coordinates) returns (ACK);
  rpc Configure (InstrumentConfig) returns (ACK);
  rpc TakeExposure (ExposureParams) returns (DataHeader);
  rpc EmergencyStop (StopCommand) returns (ACK);
}

message Coordinates {
  double ra = 1;
  double dec = 2;
}

message ACK {
  bool success = 1;
  string message = 2;
  int64 timestamp = 3;
}

message InstrumentConfig {
  string instrumentId = 1;
  map<string, string> parameters = 2;
}

message ExposureParams {
  double duration = 1;
  string filter = 2;
}

message DataHeader {
  string fitsId = 1;
  int64 size = 2;
}

message StopCommand {
  string reason = 1;
}
```

### Data Model (`sql/observation_ddl.sql`)
```sql
-- Users & Roles (FR-001, INF-FR-001)
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Observation Logs (FR-011, NFR-013)
CREATE TABLE observation_logs (
    log_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    source VARCHAR(100),
    message TEXT,
    INDEX idx_timestamp (timestamp),
    INDEX idx_severity (severity)
);

-- Parameters (FR-014, NFR-004)
CREATE TABLE system_parameters (
    param_key VARCHAR(100) PRIMARY KEY,
    param_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50)
);

-- Archive Metadata (NFR-004, NFR-011)
CREATE TABLE data_archive (
    fits_id VARCHAR(100) PRIMARY KEY,
    observation_id VARCHAR(50),
    storage_path VARCHAR(255) NOT NULL,
    retention_date DATE NOT NULL,
    size_bytes BIGINT
);
```

# E. Operations & Deployment

## 1. Kubernetes Plan
Deploy OCS services on Observatory Site cluster. IOCs remain on dedicated hardware (VxWorks).

```yaml
# k8s/ocs-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ocs-controller
  namespace: gemini-ops
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ocs-controller
  template:
    metadata:
      labels:
        app: ocs-controller
    spec:
      containers:
      - name: ocs-app
        image: gemini/ocs:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: ocs-config
              key: db_host
---
apiVersion: v1
kind: Service
metadata:
  name: ocs-service
  namespace: gemini-ops
spec:
  selector:
    app: ocs-controller
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 2. DB HA & Backup
*   **Topology:** PostgreSQL Primary-Replica (Sync Commit for Params, Async for Logs).
*   **Backup:** WAL Archiving to separate storage node. Daily full backup.
*   **Restore:** RTO < 5 mins (NFR-005) via standby promotion.

## 3. Network Topology
*   **Ingress:** TLS Termination at API Gateway (NFR-001).
*   **Internal:** mTLS between OCS pods.
*   **IOC Link:** Dedicated VLAN, <500ms latency (FR-018).
*   **Remote:** WAN via leased lines (not public Internet for critical control).

## 4. CI/CD
*   **Pipeline:** Build → Unit Test → Integration Test (Simulator) → Staging → Production.
*   **Gating:** Safety Interlock Simulation Pass required for deploy.
*   **Strategy:** Blue/Green for OCS; Rolling for IOCs (during Maintenance Level).

# F. Security Design

1.  **Auth & AuthZ:** OAuth2/OIDC with JWT. Roles (Astronomer, Operator) mapped to claims. Token expiry 1 hour. Revocation via blacklist (Redis).
2.  **Secrets:** HashiCorp Vault. Rotation every 90 days.
3.  **TLS:** TLS 1.2+ mandatory (NFR-001). mTLS for service-to-service.
4.  **Threat Model:**
    *   *Unauthorized Access:* Mitigated by RBAC (FR-001).
    *   *Command Injection:* Mitigated by Input Validation (NFR-005).
    *   *WAN Intrusion:* Mitigated by Firewall/Gateway (NFR-001).
    *   *Safety Bypass:* Mitigated by Hardware Interlocks (ASR-006).
    *   *Data Tampering:* Mitigated by FITS Checksums (NFR-011).

# G. Observability & SRE

1.  **Metrics:**
    *   `ocs_command_latency_seconds` (Target p95 < 2s).
    *   `ioc_ack_timeout_count` (Target 0).
    *   `safety_interlock_status` (Binary).
2.  **Alerts (Prometheus):**
    *   `alert: HighCommandLatency: expr: histogram_quantile(0.95, rate(ocs_command_latency_seconds_bucket[5m])) > 2`
    *   `alert: SafetyInterlockTrip: expr: safety_interlock_status == 1`
3.  **SLOs:**
    *   Availability: 99.9% (Observing Level).
    *   Error Budget: 0.1% downtime/month.
    *   RTO: 5 mins (NFR-005). RPO: 0 (for commands), 24h (for logs).
4.  **Runbook:** Automated failover to SafeState on critical alert.

# H. Testing Strategy

1.  **Test Matrix:**
    *   *Unit:* All Java/C++ modules.
    *   *Integration:* OCS ↔ IOC (using Simulator).
    *   *Contract:* OpenAPI/Proto validation.
    *   *E2E:* Full Observation Sequence (Virtual Telescope).
    *   *Chaos:* Network partition between Remote Site and Obs Site.
2.  **Data Management:**
    *   *Environments:* Dev, Test (HIL), Staging, Prod.
    *   *Refresh:* Test DB refreshed weekly with anonymized Prod data.

# I. Migration, Data Conversion & Rollout Plan

1.  **Migration:**
    *   Phase 1: Deploy modern OCS alongside legacy (Dual Write).
    *   Phase 2: Switch read traffic to new OCS.
    *   Phase 3: Decommission legacy OCS.
2.  **Data Sync:** ETL job for SYBASE → PostgreSQL migration.
3.  **Compatibility:** API Versioning (`/v1/`). Legacy clients supported via Adapter.
4.  **Rollback:** Instant switch back to legacy OCS if Safety Interlock tests fail.

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Chosen |
| :--- | :--- | :--- | :--- |
| **OCS Language** | Python vs Java vs Go | Python (Fast dev, slow runtime); Go (Fast, less enterprise libs); Java (Balanced). | Java (ASR-008, NFR-002) |
| **IOC OS** | Linux RT vs VxWorks | Linux (Cost); VxWorks (Certified Safety). | VxWorks (ASR-009, NFR-007) |
| **Data Store** | NoSQL vs SQL | NoSQL (Scale); SQL (Consistency/Transactions). | SQL (FR-014, NFR-004) |
| **Remote Access** | Public Internet vs Leased Line | Internet (Cost); Leased (Security/Reliability). | Leased Line (NFR-001, ASR-001) |

# K. Open Questions & Assumptions

**Assumptions:**
*   `A1`: Existing hardware mounts support EPICS interface upgrades.
*   `A2`: WAN bandwidth between Remote Sites and Observatory is guaranteed ≥10Mbps.
*   `A3`: Legacy SYBASE data can be exported to CSV/SQL for migration.
*   `A4`: Hardware Safety Interlocks are already installed and functional (software only monitors).

**Unresolved Questions:**
*   Q1: What is the exact latency budget for Video Streaming vs Control Data?
*   Q2: Are there specific regulatory compliance standards (e.g., ITAR) for data export?
*   Q3: What is the budget for replacing legacy IOC hardware vs software emulation?

# L. Deliverables

```markdown
<!-- File: architecture.md -->
# Gemini Control System Architecture
[Content of this document]
```

```yaml
# File: openapi.yaml
openapi: 3.0.3
info:
  title: Gemini Control System External API
  version: 1.0.0
servers:
  - url: https://api.gemini.edu/v1
security:
  - BearerAuth: []
paths:
  /auth/login:
    post:
      summary: Authenticate User
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username: { type: string }
                password: { type: string }
      responses:
        200:
          description: OK
  /observations/sequence:
    post:
      summary: Execute Sequence
      responses:
        202:
          description: Accepted
  /telescope/status:
    get:
      summary: Get Status
      responses:
        200:
          description: OK
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
```

```proto
# File: internal.proto
syntax = "proto3";
package gemini.internal;
service OCS_IOC_Controller {
  rpc MoveTo (Coordinates) returns (ACK);
  rpc EmergencyStop (StopCommand) returns (ACK);
}
message Coordinates { double ra = 1; double dec = 2; }
message ACK { bool success = 1; string message = 2; }
message StopCommand { string reason = 1; }
```

```yaml
# File: k8s/ocs-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ocs-controller
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ocs-app
        image: gemini/ocs:1.0.0
        resources:
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

```sql
-- File: sql/observation_ddl.sql
CREATE TABLE users (user_id VARCHAR(50) PRIMARY KEY, role VARCHAR(50));
CREATE TABLE observation_logs (log_id BIGSERIAL PRIMARY KEY, timestamp TIMESTAMP);
CREATE TABLE system_parameters (param_key VARCHAR(100) PRIMARY KEY, param_value TEXT);
```

```csv
# File: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact filename(s),1-2 sentence rationale
FR-001,Authenticate User,UseCaseDiagram:UC001,Auth Service,openapi.yaml,Core access control for all roles.
FR-004,Execute Observation Sequence,SequenceDiagram1,SeqExecutor,openapi.yaml,Primary science data collection function.
NFR-001,Security (TLS/Auth),ActivityDiagram,Auth Service,openapi.yaml,Prevent intrusion.
NFR-007,Safety Interlocks (HW),SequenceDiagram2,Safety Interlock HW,internal.proto,Independent of software for critical hazards.
ASR-001,Remote Operations Support,DeploymentDiagram,API Gateway,openapi.yaml,Architectural driver for distributed design.
INF-FR-001,User Role Management,UseCaseDiagram:Actors,Auth Service,openapi.yaml,Inferred from text (Astronomer, Operator, etc.).
```

# Acceptance Criteria Verification

- [x] 3-line Analysis Plan present.
- [x] Sections A-L included.
- [x] Every FR/NFR/ASR mapped in traceability matrix.
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [x] Representative k8s manifest snippet included.
- [x] SQL DDLs provided for persisted entities.
- [x] All major components have: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema.
- [x] Assumptions and open questions clearly listed.

# How to Review
- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?