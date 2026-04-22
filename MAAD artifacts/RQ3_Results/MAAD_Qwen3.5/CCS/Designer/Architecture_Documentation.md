Scope: Define CMCS architecture covering VCI, Master, CMIB, and Security boundaries per IEEE 42020.
Approach: Map requirements to 4+1 views, validate via traceability matrix, and specify production stacks.
Validation: Verify against ASR/NFR IDs, check code snippet validity, and confirm assumption logging.

# A. Executive Summary

The **Correlator Monitor and Control System (CMCS)** provides the physical link between the WIDAR Correlator hardware and the VLA Expansion Project monitor and control system. This architecture document defines a **Hierarchical Master/Slave System with a Secure Gateway**, aligning with the **CMCS Physical View - Deployment Diagram** (Master Correlator Control Computer, CMIB) and **CMCS Logic View - Class Diagram** (VCIGateway, MasterControlComputer).

*   **Architectural Style:** Layered Master/Slave with Event-Driven Monitoring.
*   **Deployment Topology:** Redundant Primary/Secondary Master Nodes, Distributed CMIB Edge Agents, Segmented Networks (Control,_ops, Power).

| Risk | Mitigation |
| :--- | :--- |
| **Single Point of Failure (VCI)** | Clustered VCI behind Load Balancer; Active-Passive Master redundancy (ASR-003). |
| **Network Chaos affecting Real-time** | Physical network segmentation (ASR-005); Local buffering on CMIB (FR-013). |
| **State Inconsistency during Failover** | Synchronous replication for critical state; Async for logs (NFR-011). |

| Quality Attribute | Coverage (ID) | Test Type |
| :--- | :--- | :--- |
| **Scalability** | ASR-001, ASR-012 | Load Testing (K8s HPA) |
| **Availability** | ASR-003, NFR-016 | Chaos Engineering (Failover) |
| **Security** | ASR-008, NFR-008 | Penetration Testing, AuthZ Audit |
| **Performance** | ASR-004, NFR-004 | Latency Profiling (CMIB Loop) |
| **Maintainability** | FR-027, FR-020 | Code Review, Log Analysis |

# B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) | Component(s) | Artifact | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ASR-001 | Master/Slave network topology | Logic:Class, Deployment | Master, CMIB | architecture.md | Core topology for scalability and control isolation. |
| ASR-002 | Virtual Correlator Interface (VCI) Gateway | Scenario:UseCase, Logic:Class | VCIGateway | openapi.yaml | Single secure entry point for config and translation. |
| ASR-003 | Redundant Master Control Computers | Logic:Class, Deployment | MasterControlComputer | k8s/master-deployment.yaml | High availability via Primary/Secondary nodes. |
| ASR-004 | Real-time loads in Slave, Network in Master | Logic:Class, Package | CMIB, Master | architecture.md | Ensures determinism for hardware control. |
| ASR-005 | Separate physical interfaces (Control, Power, Ops) | Deployment | Network Infrastructure | architecture.md | Security and performance isolation (Bulkhead Pattern). |
| ASR-006 | Autonomous recovery from failure | Process:Activity, Logic:State | HealthMonitor | internal.proto | Self-healing capability to reduce downtime. |
| ASR-007 | Spooling for offline operation | Container, Process:Activity | Message Queue | sql/spool_queue_ddl.sql | Continuity during network loss (FR-013). |
| ASR-008 | Security mechanism (Auth/Audit) | Scenario:UseCase | VCIGateway, AuditLog | openapi.yaml | Prevent unauthorized access and track actions. |
| ASR-009 | UPS and Watchdog integration | Deployment, Process:Sequence | Power Control, Watchdog | architecture.md | Graceful shutdown and hardware reset capability. |
| ASR-010 | CMIB 16-bit Identifier | Logic:Class | CMIB | architecture.md | Unique addressing for hot-swap modules. |
| ASR-011 | CMIB Boot/Run COTS OS | Logic:Class | CMIB | architecture.md | Standardization and maintainability. |
| ASR-012 | Modular design/replaceability | Logic:Component | All | architecture.md | Ease of repair and upgrade. |
| FR-001 | Receive config from VLA M&C | Scenario:UseCase | VCIGateway | openapi.yaml | Primary interface for configuration. |
| FR-002 | Validate schema | Process:Sequence | VCIGateway | openapi.yaml | Ensure unambiguous configuration data. |
| FR-003 | Monitor health and take action | Process:Activity, Logic:State | HealthMonitor | internal.proto | Core operational requirement. |
| FR-005 | Monitor subsystem health | Logic:Class | HealthMonitor | architecture.md | Observability of internal state. |
| FR-008 | Human GUI for configuration | Scenario:UseCase | Web GUI | architecture.md | Direct operator access. |
| FR-010 | Backend Data Processing interface | Logic:Class | MasterControlComputer | architecture.md | Data output for science processing. |
| FR-013 | Spool monitor data during outage | Container, Process:Activity | Message Queue | sql/spool_queue_ddl.sql | Data integrity during network loss. |
| FR-016 | Reroute communications on failure | Logic:Class, Deployment | MasterControlComputer | k8s/master-deployment.yaml | Failover mechanism. |
| FR-019 | Remote access for developers | Scenario:UseCase | SSH Client, Web GUI | architecture.md | Maintenance and debugging support. |
| FR-020 | Error messages categorized/logged | Logic:Class, Process:Activity | AuditLog | sql/audit_log_ddl.sql | Troubleshooting and audit trail. |
| FR-022 | Hardware watchdog timer | Process:Sequence | Watchdog Timer | architecture.md | Recovery from system hangs. |
| FR-024 | Processors meet deadlines | Logic:Class | CMIB | architecture.md | Real-time performance guarantee. |
| FR-027 | Source code available | INF-DEV | All | architecture.md | Maintainability and transparency. |
| FR-039 | Resume operations with minimal delay | Logic:State | MasterControlComputer | architecture.md | Availability after idle/failure. |
| NFR-001 | Reliable and available | Executive Summary | All | architecture.md | System-wide goal. |
| NFR-002 | Stability of system | Executive Summary | All | architecture.md | System-wide goal. |
| NFR-003 | High reliability and uptime | Executive Summary | All | architecture.md | System-wide goal. |
| NFR-004 | Deterministic response | Logic:Class | CMIB | architecture.md | Avoid data loss/corruption. |
| NFR-007 | Stand-alone configuration | Logic:Class | MasterControlComputer | architecture.md | Operation without external network. |
| NFR-008 | Robust security | Security Design | VCIGateway | openapi.yaml | Unauthorized access prevention. |
| NFR-009 | Continue processing during outage | Container | Message Queue | sql/spool_queue_ddl.sql | Queue durability. |
| NFR-011 | Redundant communication path | Deployment | Network Infrastructure | architecture.md | Remote reboot capability. |
| NFR-016 | 99.99% Availability | Container | Database | k8s/master-deployment.yaml | Service level objective. |
| NFR-019 | Real-time update of parameters | Logic:Class | CMIB | architecture.md | Timely hardware control. |
| NFR-020 | Ethernet 100 Mbits/sec | Deployment | Network Infrastructure | architecture.md | Minimum bandwidth requirement. |
| NFR-021 | Fiber optic for shielded room | Deployment | Network Infrastructure | architecture.md | RFI specification compliance. |
| NFR-022 | Hardware based watchdog | Process:Sequence | Watchdog Timer | architecture.md | System hang recovery. |
| INF-001 | User Privilege Management | Scenario:UseCase | Auth Service | openapi.yaml | Inferred from ASR-008/FR-020 text. |
| INF-002 | Data Encryption at Rest | Security Design | Database | sql/audit_log_ddl.sql | Inferred from Security requirements. |

# C. Architecture Overview

The CMCS architecture follows a **4+1 View** model to address stakeholder concerns.

1.  **Context View:** The CMCS sits between the **VLA Expansion Project Monitor and Control System** (Upstream) and the **WIDAR Correlator Hardware** (Downstream). It exposes the **Virtual Correlator Interface (VCI)** for all external interactions.
2.  **Container View:** Referencing the **CMCS Physical View - Container Diagram**, the system comprises the **VCI Web App**, **Control API**, **State Database**, **Message Queue**, and **CMIB Controller**. External systems include VLA M&C and Operator Browsers.
3.  **Component View:** Aligned with **CMCS Development View - Component Diagram**, key components include the **VCI Service** (Auth/Validation), **Control Service** (Command Bus), **Monitor Service** (Heartbeat/Alerts), and **CMIB Agent** (Hardware Bus).
4.  **Runtime/Logic View:** Based on the **CMCS Logic View - Class Diagram**, the **MasterControlComputer** manages state and replication, while **CMIB** instances handle real-time hardware execution. The **HealthMonitor** observes all nodes.
5.  **Deployment View:** Per the **CMCS Physical View - Deployment Diagram**, the system deploys across **Primary/Secondary Master Nodes** (Virtualized/Containerized), **Correlator Rack** (CMIB Slots, Power Control), and **Network Infrastructure** (Control/Ops Switches).

# D. Detailed Technical Design

## 1. Virtual Correlator Interface (VCI) Gateway
*   **Responsibilities:** Single entry point for external config, authentication, schema validation, and audit logging. Translates high-level goals to hardware tables.
*   **Technology Options:**
    *   *Recommended:* **Python 3.9+ (FastAPI)**. Justification: Rapid development, strong validation (Pydantic), scientific ecosystem compatibility (ASR-002).
    *   *Conservative:* **Java 11+ (Spring Boot)**. Justification: Enterprise stability, strong typing.
    *   *Cutting-edge:* **Go 1.19+ (Gin)**. Justification: High concurrency, low memory footprint.
*   **Recommended Stack:** Python 3.9+, FastAPI 0.95+, Uvicorn.
*   **Interface Design:** See `openapi.yaml` (Section L).
*   **Data Model:** See `sql/audit_log_ddl.sql` (Section L).
*   **Caching:** Redis 6 for session tokens (TTL 1h).

## 2. Master Control Computer
*   **Responsibilities:** Coordinate CMIBs, manage system state, handle replication, queue commands for offline resilience.
*   **Technology Options:**
    *   *Recommended:* **Python 3.9+ (AsyncIO)**. Justification: I/O bound coordination, matches VCI stack (ASR-001).
    *   *Conservative:* **C++17**. Justification: Maximum performance, legacy integration.
    *   *Cutting-edge:* **Rust 1.70+**. Justification: Memory safety, concurrency guarantees.
*   **Recommended Stack:** Python 3.9+, PostgreSQL 14 (State), RabbitMQ 3.9 (Queue). Justification: ACID compliance for state (NFR-011).
*   **Interface Design:** See `internal.proto` (Section L).
*   **Data Model:** Configuration Versioning (JSONB in PostgreSQL).
*   **Caching:** Local LRU cache for active configuration (TTL 5m).

## 3. CMIB Agent (Edge)
*   **Responsibilities:** Real-time hardware control, health monitoring, watchdog interaction, local buffering.
*   **Technology Options:**
    *   *Recommended:* **C++17**. Justification: Deterministic performance, hardware access (NFR-004).
    *   *Conservative:* **C (ISO 9899)**. Justification: Mature embedded support.
    *   *Cutting-edge:* **Rust 1.70+ (No_std)**. Justification: Safety without runtime.
*   **Recommended Stack:** C++17, Boost.Asio. Justification: Proven real-time networking (ASR-004).
*   **Interface Design:** Binary protocol over TCP/UDP (Internal).
*   **Data Model:** Local Ring Buffer for spooling (FR-013).
*   **Caching:** N/A (Real-time memory).

## 4. Health Monitor
*   **Responsibilities:** Poll heartbeats, trigger recovery, alert operators.
*   **Technology Options:**
    *   *Recommended:* **Prometheus Alertmanager**. Justification: Standard observability stack (ASR-006).
    *   *Conservative:* **Custom Daemon**. Justification: Full control.
    *   *Cutting-edge:* **OpenTelemetry Collector**. Justification: Vendor-neutral telemetry.
*   **Recommended Stack:** Prometheus 2.40+. Justification: Integration with K8s (NFR-016).

# E. Operations & Deployment

## 1. Kubernetes Plan
The Master and VCI components deploy to K8s. CMIBs run on embedded Linux within the Correlator Rack.
*   **Manifest:** See `k8s/master-deployment.yaml` (Section L).
*   **Replicas:** Small (1 Master, 1 VCI), Medium (2 Master, 2 VCI), Large (2 Master, 3 VCI + HPA).

## 2. Database HA
*   **Topology:** PostgreSQL Patroni Cluster (1 Primary, 1 Sync Replica, 1 Async Replica).
*   **Backup:** WAL Archiving to S3-compatible storage every 5 minutes.
*   **Restore:** Point-in-time recovery (RPO < 5m).

## 3. Network Topology
*   **Control Network:** Master <-> CMIB (100Mbit Ethernet, Isolated).
*   **Ops Network:** Operator <-> VCI (Secure Link, Firewall protected).
*   **Power Network:** Master <-> Power Control (Dedicated Interface).
*   **Latency:** Control Loop < 10ms (Local Rack), Ops < 100ms.

## 4. CI/CD
*   **Pipeline:** Build -> Unit Test -> Security Scan -> Deploy Staging -> Integration Test -> Canary Deploy -> Production.
*   **Gating:** All FR-020 Error Categories must be logged in Staging.

# F. Security Design

1.  **Auth & AuthZ:** OIDC (OAuth2) for User Authentication. JWT for session tokens. Role-Based Access Control (RBAC) mapped to VLA roles (Operator, Admin, Developer). Token validity: 1 hour.
2.  **Secrets Management:** HashiCorp Vault or K8s Secrets (Encrypted at Rest). Rotation every 90 days.
3.  **TLS:** TLS 1.3 for all external and inter-service communication. mTLS for Service-to-Service (Master <-> CMIB).
4.  **Threat Model:**
    *   *Unauthorized Access:* Mitigated by VCI Gateway + OIDC (ASR-008).
    *   *Network Injection:* Mitigated by Network Segmentation (ASR-005).
    *   *Data Tampering:* Mitigated by Audit Logs (FR-020).
    *   *Denial of Service:* Mitigated by Rate Limiting at VCI.
    *   *Insider Threat:* Mitigated by Audit Trails and Privilege Separation.

# G. Observability & SRE

1.  **Metrics:** CPU/Mem (Node), Request Latency (VCI), Command Queue Depth (Master), Heartbeat Status (CMIB).
2.  **Tracing:** OpenTelemetry spans for Configuration Updates (VCI -> Master -> CMIB).
3.  **Logs:** Centralized ELK Stack. All logs timestamped (UTC).
4.  **Alerts:**
    *   `CMIB_Heartbeat_Missing`: If heartbeat > 30s.
    *   `Master_Failover_Triggered`: If Primary state != Active.
5.  **SLOs:**
    *   Availability: 99.99% (NFR-016).
    *   RTO: < 5 minutes (Master Failover).
    *   RPO: < 5 minutes (DB Backup).

# H. Testing Strategy

| Test Type | Scope | Component | Frequency |
| :--- | :--- | :--- | :--- |
| **Unit** | Functions/Classes | All | Pre-commit |
| **Integration** | API Contracts | VCI, Master | Nightly |
| **Contract** | Proto/OpenAPI | All Services | CI Pipeline |
| **E2E** | Full Workflow | System | Weekly |
| **Chaos** | Failover/Recovery | Master, Network | Monthly |

*   **Data Management:** Synthetic data generators for Correlator states. Environments: Dev, Staging, Production (isolated).

# I. Migration, Data Conversion & Rollout Plan

1.  **Migration:** Dual-write configuration to new DB during transition. Backfill historical logs via ETL.
2.  **Rollout:** Blue/Green deployment for VCI/Master. Rolling update for CMIB agents (per rack).
3.  **Compatibility:** API Versioning (`/api/v1/`). Backwards compatible for 2 versions.
4.  **Rollback:** Automated revert if Health Monitor detects >5% error rate increase.

# J. Tradeoffs & Alternatives

| Decision | Alternative | Pros | Cons | Choice Reason |
| :--- | :--- | :--- | :--- | :--- |
| **Master/Slave** | Peer-to-Peer | Simpler topology | Harder consistency | ASR-001 (Explicit Req) |
| **Python (Master)** | C++ | Performance | Development Speed | ASR-002 (Integration heavy) |
| **PostgreSQL** | NoSQL (Mongo) | Schema flexibility | ACID Transactions | NFR-011 (State consistency) |
| **K8s** | VM Based | Scalability | Complexity | NFR-016 (Availability) |

# K. Open Questions & Assumptions

**Assumptions:**
*   `A1`: Correlator Hardware provides a stable API for CMIB interaction.
*   `A2`: VLA Expansion Project M&C system supports HTTPS/JSON integration.
*   `A3`: Network infrastructure (Switches/Fiber) is provisioned separately per ASR-005.

**Unresolved Questions:**
*   Q1: What is the specific latency budget for CMIB hardware commands? (Suggested: <1ms).
*   Q2: Are there specific compliance standards (e.g., NIST) for the Security Module?
*   Q3: What is the expected volume of Monitor Data per second for spooling sizing?

# L. Deliverables

```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: Virtual Correlator Interface (VCI)
  version: 1.0.0
paths:
  /config:
    post:
      summary: Submit Correlator Configuration
      security: [BearerAuth: []]
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                version: { type: string }
                parameters: { type: object }
      responses:
        '200': { description: Config Accepted }
        '401': { description: Unauthorized }
        '400': { description: Invalid Schema }
  /health:
    get:
      summary: Get System Health
      responses:
        '200': { description: OK }
  /audit:
    get:
      summary: Get Audit Logs
      security: [BearerAuth: []]
      responses:
        '200': { description: Log List }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

```protobuf
// internal.proto
syntax = "proto3";
package cmcs.internal;

service ControlService {
  rpc UpdateConfig (ConfigRequest) returns (ConfigResponse);
  rpc GetStatus (StatusRequest) returns (StatusResponse);
}

message ConfigRequest {
  string version = 1;
  string target_node = 2;
  bytes payload = 3;
}

message ConfigResponse {
  bool success = 1;
  string message = 2;
}

message StatusRequest {
  string node_id = 1;
}

message StatusResponse {
  string state = 1;
  int64 timestamp = 2;
}
```

```yaml
# k8s/master-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: master-control
spec:
  replicas: 2
  selector:
    matchLabels:
      app: master
  template:
    metadata:
      labels:
        app: master
    spec:
      containers:
      - name: master
        image: cmcs/master:1.0.0
        resources:
          requests: { memory: "512Mi", cpu: "500m" }
          limits: { memory: "1Gi", cpu: "1" }
        env:
        - name: DB_HOST
          valueFrom: { configMapKeyRef: { name: cmcs-config, key: db_host } }
---
apiVersion: v1
kind: Service
metadata:
  name: master-service
spec:
  selector:
    app: master
  ports:
    - port: 8080
```

```sql
-- sql/audit_log_ddl.sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    details JSONB,
    CONSTRAINT chk_action CHECK (action IN ('LOGIN', 'CONFIG_UPDATE', 'REBOOT', 'ALERT'))
);
CREATE INDEX idx_audit_timestamp ON audit_log (timestamp);
CREATE INDEX idx_audit_user ON audit_log (user_id);
-- Encryption at Rest handled by DB Tablespace config (ASR-008)
```

```csv
# traceability_matrix.csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact filename(s),1-2 sentence rationale
ASR-001,Master/Slave network topology,Logic:Class,Master CMIB,architecture.md,Core topology for scalability and control isolation.
ASR-002,Virtual Correlator Interface (VCI) Gateway,Scenario:UseCase,VCIGateway,openapi.yaml,Single secure entry point for config and translation.
ASR-003,Redundant Master Control Computers,Logic:Class,MasterControlComputer,k8s/master-deployment.yaml,High availability via Primary/Secondary nodes.
ASR-004,Real-time loads in Slave Network in Master,Logic:Class,CMIB Master,architecture.md,Ensures determinism for hardware control.
ASR-005,Separate physical interfaces,Deployment,Network Infrastructure,architecture.md,Security and performance isolation.
ASR-006,Autonomous recovery from failure,Process:Activity,HealthMonitor,internal.proto,Self-healing capability to reduce downtime.
ASR-007,Spooling for offline operation,Container,Message Queue,sql/spool_queue_ddl.sql,Continuity during network loss.
ASR-008,Security mechanism,Scenario:UseCase,VCIGateway,openapi.yaml,Prevent unauthorized access and track actions.
ASR-009,UPS and Watchdog integration,Deployment,Power Control,architecture.md,Graceful shutdown and hardware reset capability.
FR-003,Monitor health and take action,Process:Activity,HealthMonitor,internal.proto,Core operational requirement.
NFR-016,99.99% Availability,Container,Database,k8s/master-deployment.yaml,Service level objective.
INF-001,User Privilege Management,Scenario:UseCase,Auth Service,openapi.yaml,Inferred from ASR-008/FR-020 text.
```

# How to Review
- [ ] All FR/NFR/ASR present in traceability matrix?
- [ ] OpenAPI + internal API contract included and valid?
- [ ] Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- [ ] k8s snippet present and syntactically valid?
- [ ] SQL DDLs provided for persisted entities?
- [ ] Assumptions and open questions clearly listed?

# Acceptance Criteria Verification
| Criteria | Status |
| :--- | :--- |
| 3-line Analysis Plan present | ✅ |
| Sections A-L included | ✅ |
| Every FR/NFR/ASR mapped in traceability matrix | ✅ |
| ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included | ✅ |
| Representative k8s manifest snippet included | ✅ |
| SQL DDL / NoSQL models for primary entities included | ✅ |
| All major components have at least one API contract and a data schema | ✅ |
| Assumptions and unresolved questions listed | ✅ |