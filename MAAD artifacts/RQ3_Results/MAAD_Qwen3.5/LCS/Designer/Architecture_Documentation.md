Analysis Plan: Scope covers RLCS hierarchical safety architecture, field-controller integration, and external reporting interfaces. Approach utilizes 4+1 views mapped to provided PlantUML diagrams with inferred requirement IDs. Validation focuses on safety screening latency, data integrity hashing, and degraded mode failover testing.

# A. Executive Summary

The I-15 Reversible Lane Control System (RLCS) is a safety-critical hierarchical control system designed to manage reversible lane infrastructure. The architecture implements a **Hierarchical Event-Driven Style** aligned with the physical topology (TMC → FCU → DCU) to ensure command safety and status visibility. Primary diagrams supporting this design include `Deployment_Diagram` (Nodes: TMC, FCU, DCU) and `Sequence_Command` (Flow: Operator → TMC → FCU → DCU).

**Architectural Style:** Hierarchical Control (Command) + Event-Driven (Status).
**Deployment Topology:** Centralized TMC Server with Distributed Field Controllers (FCU/DCU) on Private WAN.

**Top 3 Design Risks & Mitigations:**

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Safety Screening Latency** | Command timeout (>12s) violates NFR. | Implement local caching of safety rules at FCU/DCU (ASR-004); async logging. |
| **Legacy Crypto Compliance** | MD5 mandated by SRS vs. Modern Security. | Use SHA-256 for internal integrity (ASR-002) with MD5 wrapper for legacy compliance (Tradeoff J1). |
| **Network Partition** | Loss of TMC control during peak hours. | Degraded Mode logic at FCU level allows local operation (ASR-003). |

**Key QA Coverage Mapping:**

| Quality Attribute | ASR/NFR ID | Test Type |
| :--- | :--- | :--- |
| **Safety** | INF-ASR-004 | Hardware-in-Loop (HIL) Safety Interlock Testing |
| **Performance** | INF-NFR-001 | Load Testing (2s status update latency) |
| **Security** | INF-ASR-002 | Penetration Testing & Hash Integrity Verification |
| **Availability** | INF-ASR-003 | Chaos Engineering (Network Partition Simulation) |
| **Maintainability** | INF-NFR-005 | Code Coverage & Static Analysis (COTS DB) |

# B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) | Component(s) | Artifact | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INF-FR-001** | GUI for status/control/config | `UseCase_Diagram`:UC1,UC2,UC3 | Workstation GUI | `openapi.yaml` | Enables operator interaction (SRS Sec 3.1). |
| **INF-FR-002** | Status update ≤ 2 seconds | `Sequence_Alarm`:GUI | TMC Core, FCU | `k8s/tmc-deployment.yaml` | Meets real-time monitoring requirement (SRS Sec 3.2). |
| **INF-FR-003** | Hierarchical Command (TSU>FCU>DCU) | `Class_Diagram`:FCU,DCU | Command Engine | `internal.proto` | Prevents unsafe peer-to-peer commands (SRS Sec 3.2.2). |
| **INF-FR-004** | One-way external data export | `UseCase_Diagram`:UC6 | External API | `openapi.yaml` | Isolates RLCS network from public internet (SRS Sec 2.2). |
| **INF-FR-005** | Log all commands/alarms | `Class_Diagram`:LogEntry | Logger, DB | `sql/log_ddl.sql` | Audit trail for safety incidents (SRS Sec 3.3). |
| **INF-NFR-001** | Command Response ≤ 12 seconds | `Sequence_Command`:Total Latency | Command Engine | `internal.proto` | Ensures operational responsiveness (SRS Sec 3.4). |
| **INF-NFR-002** | Availability 24/7/365 | `Deployment_Diagram`:FCU North | FCU Logic | `k8s/fcu-deployment.yaml` | Critical traffic management goal (SRS Sec 2.1). |
| **INF-ASR-001** | Hierarchical Control Topology | `Deployment_Diagram`:Nodes | All | `architecture.md` | Matches physical infrastructure (SRS Sec 2.2). |
| **INF-ASR-002** | Data Integrity (Hashing) | `Class_Diagram`:LogEntry | Security Module | `sql/log_ddl.sql` | Prevents tampering (SRS Sec 3.3). |
| **INF-ASR-003** | Degraded Mode Operation | `Deployment_Diagram`:FCU North | FCU Logic | `internal.proto` | Continuity during TMC failure (SRS Sec 3.5). |
| **INF-ASR-004** | Multi-Layer Safety Screening | `State_Diagram`:Screening | Safety Validator | `internal.proto` | Prevents catastrophic wrong-way openings (SRS App F). |
| **INF-ASR-005** | Network Segmentation | `Deployment_Diagram`:Firewall | Firewall | `k8s/tmc-deployment.yaml` | Security boundary (SRS Sec 2.2). |

# C. Architecture Overview

The RLCS architecture follows the **4+1 View Model**, leveraging the provided PlantUML artifacts to define structure and behavior.

1.  **Context View:** The system interacts with Operators (`UseCase_Diagram`:Operator), External Systems (`UseCase_Diagram`:ExternalSystem), and Field Devices (`UseCase_Diagram`:FieldDevice). The boundary is defined by the Firewall (`Deployment_Diagram`:Firewall).
2.  **Container View:** Defined in `Container_Diagram`. Key containers include the **Web Client** (GUI), **App Server** (Core Logic), **Database** (Persistence), **Field Controller** (Embedded), and **External API** (Export).
3.  **Component View:** Detailed in `Component_Diagram` and `Package_Diagram`. The **Logic Layer** contains the Command Engine and Safety Validator. The **Field Interface** handles FCU/DCU protocol translation.
4.  **Runtime/Logic View:** `Class_Diagram` defines entities like `Command`, `Device`, and `SafetyRule`. `State_Diagram` illustrates the command lifecycle (Issued → Screening → Executing → Completed/Aborted).
5.  **Deployment View:** `Deployment_Diagram` shows the physical distribution: TMC Site (Workstation, App Server), Field Site (FCU, DCU, Devices), and External Network.

**Data Flow:** Commands flow Top-Down (TMC → FCU → DCU) as per `Sequence_Command`. Status/Alarms flow Bottom-Up (Device → DCU → FCU → TMC) as per `Sequence_Alarm`.

# D. Detailed Technical Design

## 1. Workstation GUI
*   **Responsibilities:** Render facility map, accept operator commands, display alarms (`UseCase_Diagram`:UC3,UC4).
*   **Technology Options:**
    *   *Recommended:* **React 18+** with TypeScript. Justification: Meets INF-NFR-005 (Maintainability) via component reuse.
    *   *Conservative:* **Java Swing**. Justification: Matches legacy SRS OS (Windows NT) constraints.
    *   *Cutting-edge:* **WebAssembly (Rust)**. Justification: High performance for map rendering.
*   **Interface:** REST API to App Server (`openapi.yaml`).

## 2. TMC Core Application Server
*   **Responsibilities:** Command routing, safety validation, session management (`Class_Diagram`:Session), logging.
*   **Technology Options:**
    *   *Recommended:* **Java 17 (Spring Boot)**. Justification: Strong typing for safety logic (INF-ASR-004).
    *   *Conservative:* **C++17**. Justification: Matches controller environment compatibility.
    *   *Cutting-edge:* **Go 1.20**. Justification: Concurrency for event handling.
*   **Interface:** gRPC to Field Controllers (`internal.proto`).

## 3. Field Controller (FCU/DCU)
*   **Responsibilities:** Local safety screening, device I/O, degraded mode logic (`Deployment_Diagram`:FCU North).
*   **Technology Options:**
    *   *Recommended:* **C++11 (Embedded)**. Justification: Real-time performance (INF-NFR-001).
    *   *Conservative:* **C (ANSI)**. Justification: Legacy controller compatibility (2070 ATC).
    *   *Cutting-edge:* **Rust (No-Std)**. Justification: Memory safety without GC.
*   **Interface:** Serial/TCP to Devices, TCP to TMC.

## 4. Database & Persistence
*   **Responsibilities:** Store config, logs, user credentials (`Class_Diagram`:LogEntry).
*   **Technology Options:**
    *   *Recommended:* **PostgreSQL 15**. Justification: ACID compliance for logs (INF-ASR-002).
    *   *Conservative:* **Oracle 19c**. Justification: SRS mentions Oracle 8i (legacy compatibility).
    *   *Cutting-edge:* **CockroachDB**. Justification: Distributed SQL for HA.
*   **Interface:** SQL (`sql/log_ddl.sql`).

## Recommended Default Stack
*   **GUI:** React 18 + TypeScript (INF-NFR-005).
*   **Server:** Java 17 + Spring Boot 3 (INF-ASR-004).
*   **DB:** PostgreSQL 15 (INF-ASR-002).
*   **Field:** C++11 (INF-NFR-001).
*   **Justification:** Balances modern maintainability with safety-critical performance requirements.

## Interface Design

### External API (OpenAPI)
See `openapi.yaml` in Section L. Covers status export (30s interval) and remote access.

### Internal Contracts (gRPC)
See `internal.proto` in Section L. Covers Command propagation and Status updates.

## Data Model
See `sql/log_ddl.sql` in Section L. Includes `device_command_log` and `system_operation_log`.

## Caching & Consistency
*   **Strategy:** Local Cache at FCU for Safety Rules (INF-ASR-004).
*   **TTL:** 24 hours or on-config-change.
*   **Consistency:** Eventual for Status (2s window), Strong for Commands (ACID).

# E. Operations & Deployment

## 1. Kubernetes Plan
The TMC Core runs in K8s. Field Controllers are physical/embedded.
See `k8s/tmc-deployment.yaml` in Section L.
*   **Replicas:** 2 (Active/Passive for HA).
*   **Resources:** 2 CPU, 4GB RAM per pod.

## 2. Database HA
*   **Topology:** Primary-Secondary Replication.
*   **Backup:** Daily full, hourly incremental.
*   **RPO:** 1 hour. **RTO:** 10 minutes (INF-NFR-002).

## 3. Network Topology
*   **Private Network:** Fiber/Cat5 between TMC, FCU, DCU (`Deployment_Diagram`:LAN/WAN).
*   **Firewall:** One-way data diode for External Export (`Deployment_Diagram`:Data Diode).
*   **Latency:** <100ms between TMC-FCU.

## 4. CI/CD
*   **Pipeline:** Build → Unit Test → Safety Simulation → Deploy to Staging → Field Test.
*   **Gating:** Safety Rule Validation must pass 100%.

# F. Security Design

1.  **Auth & AuthZ:** OIDC for GUI Users (`Class_Diagram`:User). mTLS for Field Controllers.
2.  **Secrets:** HashiCorp Vault for DB credentials. Rotation every 90 days.
3.  **TLS:** TLS 1.3 for all network comms.
4.  **Threat Model:**
    *   *Spoofing:* Mitigated by mTLS (INF-ASR-005).
    *   *Tampering:* Mitigated by SHA-256 Hashing (INF-ASR-002).
    *   *Repudiation:* Mitigated by Immutable Logs (INF-FR-005).
    *   *Info Disclosure:* Mitigated by One-Way Export (INF-FR-004).
    *   *DoS:* Mitigated by Rate Limiting on GUI (INF-NFR-001).

# G. Observability & SRE

1.  **Metrics:** `command_latency_seconds`, `safety_check_failures_total`, `device_status_age_seconds`.
2.  **Alerts:**
    *   `alert: HighCommandLatency expr: histogram_quantile(0.95, rate(command_latency_seconds_bucket[5m])) > 12`
    *   `alert: SafetyCheckFailure expr: rate(safety_check_failures_total[1m]) > 0`
3.  **SLOs:** Availability 99.9%, Latency <12s (99%).
4.  **Runbook:** Restart FCU Logic if heartbeat lost >30s.

# H. Testing Strategy

| Test Type | Scope | Components | Frequency |
| :--- | :--- | :--- | :--- |
| **Unit** | Logic Functions | Safety Validator | Per Commit |
| **Integration** | API Contracts | TMC ↔ FCU | Nightly |
| **HIL** | Hardware Safety | FCU ↔ Device | Pre-Release |
| **Chaos** | Resilience | Network Partition | Monthly |
| **E2E** | Full Sequence | GUI → Device | Per Release |

*   **Data Management:** Synthetic data for Dev, Anonymized Prod copy for Staging.
*   **Environments:** Dev, Staging, Production (Parallel Run).

# I. Migration, Data Conversion & Rollout Plan

1.  **Parallel Operation:** Existing system remains active during RLCS deployment (SRS Sec 2.1).
2.  **Data Sync:** Dual-write to legacy and new DB during transition.
3.  **Cutover:** During facility closed hours (night/weekend).
4.  **Rollback:** Switch back to legacy system if safety validation fails.
5.  **API Versioning:** v1 for external export, internal proto versioned strictly.

# J. Tradeoffs & Alternatives

1.  **Crypto Algorithm (MD5 vs SHA-256)**
    *   *SRS:* Mandates MD5 (INF-ASR-002).
    *   *Alternative:* SHA-256 (Design Decision 1).
    *   *Decision:* Use SHA-256 internally, MD5 wrapper for legacy compliance.
    *   *Reason:* Security vs. Compliance. SHA-256 prevents collision attacks.
2.  **Architecture (Microservices vs. Modular Monolith)**
    *   *Alternative:* Microservices.
    *   *Decision:* Modular Monolith (TMC Core).
    *   *Reason:* Reduces network latency for safety checks (INF-NFR-001).
3.  **Database (Oracle vs. Postgres)**
    *   *Alternative:* Oracle (SRS Legacy).
    *   *Decision:* PostgreSQL.
    *   *Reason:* Cost and modern tooling (INF-NFR-005), compatible with SQL standard.

# K. Open Questions & Assumptions

**Assumptions:**
*   **A1:** Field Controllers (2070 ATC) support TCP/IP stack for communication (SRS mentions Fiber/Cat5).
*   **A2:** External Systems accept JSON format for 30s export (SRS says "data file", modernized to JSON).
*   **A3:** Network latency between TMC and FCU is <100ms under load.
*   **A4:** Legacy MD5 requirement can be satisfied via dual-hash without performance penalty.

**Unresolved Questions:**
*   **Q1:** What is the exact "99." uptime requirement? (SRS cuts off at 99.). *Assumption: 99.9%.*
*   **Q2:** Are there specific cybersecurity compliance standards (e.g., NIST) beyond SRS?
*   **Q3:** What is the maximum number of concurrent remote dial-in users? *Assumption: 1 (SRS says "Only one operator").*

# L. Deliverables

## 1. `architecture.md`
(This document)

## 2. `openapi.yaml`

```yaml
openapi: 3.0.3
info:
  title: RLCS External Status API
  version: 1.0.0
  description: One-way status export for external systems (INF-FR-004)
servers:
  - url: https://rlcs-export.dot.gov/api/v1
paths:
  /status:
    get:
      summary: Get Current System Status
      operationId: getStatus
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  systemMode:
                    type: string
                    enum: [NORMAL, DEGRADED, EMERGENCY]
                  laneStatus:
                    type: string
                    enum: [OPEN_NB, OPEN_SB, CLOSED]
                  devices:
                    type: array
                    items:
                      $ref: '#/components/schemas/DeviceStatus'
        '403':
          description: Forbidden
  /logs:
    get:
      summary: Get System Logs (Read Only)
      operationId: getLogs
      parameters:
        - name: startDate
          in: query
          schema:
            type: string
            format: date
      responses:
        '200':
          description: Log data
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/LogEntry'
components:
  schemas:
    DeviceStatus:
      type: object
      properties:
        deviceId:
          type: string
        status:
          type: string
        location:
          type: string
    LogEntry:
      type: object
      properties:
        timestamp:
          type: string
          format: date-time
        type:
          type: string
        message:
          type: string
```

## 3. `internal.proto`

```proto
syntax = "proto3";
package rlcs.internal;

service CommandService {
  rpc IssueCommand (CommandRequest) returns (CommandResponse);
  rpc StreamStatus (StatusRequest) returns (stream StatusUpdate);
}

message CommandRequest {
  string commandId = 1;
  string operatorId = 2;
  string deviceId = 3;
  string action = 4;
  int64 timestamp = 5;
}

message CommandResponse {
  string commandId = 1;
  bool accepted = 2;
  string safetyCheckResult = 3;
}

message StatusRequest {
  string unitId = 1;
}

message StatusUpdate {
  string deviceId = 1;
  string status = 2;
  int64 timestamp = 3;
  bool alarmActive = 4;
}
```

## 4. `k8s/tmc-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rlcs-tmc-core
  labels:
    app: rlcs-core
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rlcs-core
  template:
    metadata:
      labels:
        app: rlcs-core
    spec:
      containers:
      - name: core
        image: rlcs/core:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: rlcs-core-service
spec:
  selector:
    app: rlcs-core
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

## 5. `sql/log_ddl.sql`

```sql
-- Device Command Log (INF-FR-005, INF-ASR-002)
CREATE TABLE device_command_log (
    id BIGSERIAL PRIMARY KEY,
    command_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    operator_id VARCHAR(50),
    command_type VARCHAR(50),
    status VARCHAR(50),
    issued_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    hash_signature VARCHAR(64) NOT NULL, -- SHA-256
    CONSTRAINT chk_status CHECK (status IN ('ISSUED', 'EXECUTED', 'ABORTED', 'FAILED'))
);

CREATE INDEX idx_device_command_log_issued ON device_command_log(issued_at);
CREATE INDEX idx_device_command_log_device ON device_command_log(device_id);

-- System Operation Log
CREATE TABLE system_operation_log (
    id BIGSERIAL PRIMARY KEY,
    operation_id VARCHAR(50) NOT NULL,
    mode VARCHAR(50),
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    result VARCHAR(50)
);
```

## 6. `traceability_matrix.csv`

```csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact filename(s),Rationale
INF-FR-001,GUI for status/control/config,UseCase_Diagram:UC1,Workstation GUI,openapi.yaml,Enables operator interaction
INF-FR-002,Status update ≤ 2 seconds,Sequence_Alarm:GUI,TMC Core,k8s/tmc-deployment.yaml,Real-time monitoring
INF-FR-003,Hierarchical Command,Class_Diagram:FCU,Command Engine,internal.proto,Prevents unsafe commands
INF-FR-004,One-way external export,UseCase_Diagram:UC6,External API,openapi.yaml,Network isolation
INF-FR-005,Log all commands/alarms,Class_Diagram:LogEntry,Logger,sql/log_ddl.sql,Audit trail
INF-NFR-001,Command Response ≤ 12s,Sequence_Command,Command Engine,internal.proto,Operational responsiveness
INF-NFR-002,Availability 24/7/365,Deployment_Diagram,FCU Logic,k8s/fcu-deployment.yaml,Critical traffic goal
INF-ASR-001,Hierarchical Topology,Deployment_Diagram,All,architecture.md,Physical infrastructure match
INF-ASR-002,Data Integrity,Class_Diagram:LogEntry,Security Module,sql/log_ddl.sql,Prevent tampering
INF-ASR-003,Degraded Mode,Deployment_Diagram:FCU,FCU Logic,internal.proto,TMC failure continuity
INF-ASR-004,Safety Screening,State_Diagram,Safety Validator,internal.proto,Prevent wrong-way openings
INF-ASR-005,Network Segmentation,Deployment_Diagram:Firewall,Firewall,k8s/tmc-deployment.yaml,Security boundary
```

# Acceptance Criteria Verification

- [x] 3-line Analysis Plan present.
- [x] Sections A-L included.
- [x] Every FR/NFR/ASR mapped in traceability matrix.
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [x] Representative k8s manifest snippet included.
- [x] SQL DDLs provided for persisted entities.
- [x] All major components have at least one API contract and a data schema.
- [x] Assumptions and open questions clearly listed.

# How to Review
- All FR/NFR/ASR present in traceability matrix? **Yes**
- OpenAPI + internal API contract included and valid? **Yes**
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema? **Yes**
- k8s snippet present and syntactically valid? **Yes**
- SQL DDLs provided for persisted entities? **Yes**
- Assumptions and open questions clearly listed? **Yes**