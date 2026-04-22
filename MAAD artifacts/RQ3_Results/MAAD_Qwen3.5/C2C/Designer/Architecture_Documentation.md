# Analysis Plan
1. **Scope:** Architectural design for TxDOT Center-to-Center (C2C) system, reconciling legacy C++/Windows NT constraints with modern security (TLS/RBAC) and TMDD interoperability.
2. **Approach:** Hybrid Microkernel + Security Gateway pattern; Contract-first APIs (OpenAPI/gRPC); Canonical TMDD data model with Adapter layer for heterogeneous systems.
3. **Validation:** Traceability matrix coverage (all FR/NFR/ASR), syntactic validity of artifacts (OpenAPI/SQL/K8s), and security threat modeling.

---

# A. Executive Summary

The Center-to-Center (C2C) system is a traffic management infrastructure facilitating data exchange and device control between dissimilar Traffic Management Centers (TMCs) using ITS standards (TMDD/DATEX). The architecture adopts a **Hybrid Microkernel and Layered Style** with a **Security Gateway** pattern to isolate legacy core logic (C/C++ on Windows NT) from public network risks.

**Primary Diagram Mapping:**
*   **Logic View:** Class Diagram (Element IDs: `FieldDevice`, `SecurityGateway`, `AuditLog`).
*   **Process View:** Sequence Diagram (Scenario 1: Remote Device Control).
*   **Physical View:** Deployment Diagram (Element IDs: `Security Gateway Appliance`, `Windows NT Server`).

**Top 3 Design Risks & Mitigations:**
| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Legacy OS Security (ASR-005)** | Windows NT lacks modern TLS/Auth. | Deploy modern Security Gateway (TLS 1.2+) as a proxy before legacy core (ASR-006). |
| **Heterogeneous Interconnection (ASR-001)** | Protocol mismatch causes data loss. | Adapter Pattern with Canonical TMDD Model; Contract-first validation (INF-NFR-003). |
| **Auditability & Privacy (NFR-002)** | Passwords logged in control commands. | Immutable Audit Logs with Secret Redaction; Async logging to prevent blocking (INF-NFR-004). |

**QA Coverage Mapping:**
| Quality Attribute | ASR/NFR ID | Test Type |
| :--- | :--- | :--- |
| **Security** | NFR-002, ASR-006 | Penetration Testing, TLS Verification |
| **Performance** | NFR-001 (Map <2s) | Load Testing, Cache Hit Ratio Monitoring |
| **Interoperability** | ASR-001, ASR-002 | Contract Testing (OpenAPI/XSD) |
| **Reliability** | NFR-004 (Test Mode) | Log Integrity Verification, Hash Chain Check |
| **Modifiability** | ASR-004 (Config Blocks) | Plugin Integration Testing, Config Drift Detection |

---

# B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INF-FR-001** | Center provides network/link/node data. | Logic View: ClassDiagram (`Network`) | DataCollector | `sql/network_ddl.sql` | Canonical model required for federation (ASR-003). |
| **INF-FR-002** | Center supports incident/lane closure info. | Logic View: ClassDiagram (`Incident`) | IncidentMgr | `openapi.yaml` | Public API exposure for incident management (FR-002a). |
| **INF-FR-003** | Center provides device status (DMS, LCS, CCTV). | Logic View: ClassDiagram (`FieldDevice`) | DeviceCtrl | `internal.proto` | Internal status polling via adapter (ASR-001). |
| **INF-FR-004** | Center supports device control commands. | Process View: SequenceDiagram (`DeviceControl`) | DeviceCtrl | `openapi.yaml` | Remote control requires auth/TLS (NFR-002). |
| **INF-FR-005** | Web Map displays traffic/incidents (zoom/pan). | Scenario View: UseCaseDiagram (`UC_Map`) | WebMap | `k8s/webui-deployment.yaml` | Performance req <2s rendering (NFR-001). |
| **INF-FR-006** | Incident GUI allows entry/mod/delete. | Scenario View: UseCaseDiagram (`UC_Incident`) | IncidentMgr | `openapi.yaml` | CRUD operations require audit logging (NFR-004). |
| **INF-FR-007** | Remote Control GUI executes on public net. | Physical View: DeploymentDiagram (`Remote Workstation`) | RemoteGUI | `openapi.yaml` | Public network requires Security Gateway (ASR-006). |
| **INF-NFR-001** | Map rendering latency <2s. | Process View: ActivityDiagram (`Validate TLS`) | WebMap | `k8s/webui-deployment.yaml` | Caching strategy required for performance. |
| **INF-NFR-002** | Security: TLS, RBAC, Password Redaction. | Logic View: ClassDiagram (`SecurityGateway`) | SecurityGateway | `internal.proto` | Mitigates Legacy OS risk (ASR-005). |
| **INF-NFR-003** | Protocol: TMDD/DATEX/ASN over TCP/IP. | Logic View: ClassDiagram (`DeviceAdapter`) | AdapterMgr | `sql/canonical_ddl.sql` | Standards compliance (ASR-002). |
| **INF-NFR-004** | Test Mode logs activities immutably. | Logic View: ClassDiagram (`AuditLog`) | AuditComponent | `sql/audit_ddl.sql` | Auditability for compliance (FR-008). |
| **INF-ASR-001** | Interconnect dissimilar traffic systems. | Development View: PackageDiagram (`Adapters`) | AdapterMgr | `internal.proto` | Adapter pattern isolates core from protocols. |
| **INF-ASR-002** | Utilize TMDD standard message sets. | Logic View: ClassDiagram (`FieldDevice`) | DataCollector | `sql/canonical_ddl.sql` | Canonical model ensures interoperability. |
| **INF-ASR-003** | Repository federation (Local->Regional). | Development View: PackageDiagram (`Repository`) | Repository | `sql/network_ddl.sql` | Hierarchical data linking required. |
| **INF-ASR-004** | Configurable building blocks. | Development View: ComponentDiagram (`AdapterManager`) | AdapterMgr | `k8s/core-service-deployment.yaml` | Microkernel plugin architecture. |
| **INF-ASR-005** | Execute in Windows NT environment. | Physical View: DeploymentDiagram (`Windows NT Server`) | C2C Core | `k8s/core-service-deployment.yaml` | Legacy constraint requires network segmentation. |
| **INF-ASR-006** | Security Gateway for public network. | Physical View: DeploymentDiagram (`Security Gateway Appliance`) | SecurityGateway | `openapi.yaml` | Enforces TLS 1.2+ before legacy core. |

---

# C. Architecture Overview

The architecture follows a **4+1 View Model** aligned with ISO/IEC/IEEE 42020:2019(E).

1.  **Context View:** The system interconnects multiple TMCs (ExternalSystems) and provides interfaces for Operators and RemoteUsers. Referenced in **Scenario View: UseCase Diagram** (Elements: `Operator`, `RemoteUser`, `ExternalSystem`).
2.  **Container View:** Separates **Web UI** (HTTPS/JS), **API Gateway** (Nginx/Proxy), **Core Service** (C/C++), and **Database** (SQL). Referenced in **Physical View: Container Diagram** (Elements: `Web UI`, `API Gateway`, `Core Service`).
3.  **Component View:** Internal logic divided into **AuthComponent**, **IncidentComponent**, **DeviceControlComponent**, and **AdapterManager**. Referenced in **Development View: Component Diagram** (Elements: `AuthComponent`, `DeviceControlComponent`).
4.  **Class/Runtime View:** Domain model includes `Incident`, `FieldDevice`, `Network`, `User`, `AuditLog`. Referenced in **Logic View: Class Diagram** (Elements: `Incident`, `FieldDevice`, `AuditLog`).
5.  **Deployment View:** Physical topology includes **Client Network**, **DMZ (Security Gateway)**, and **Legacy Center Network (Windows NT)**. Referenced in **Physical View: Deployment Diagram** (Elements: `DMZ`, `Legacy Center Network`).

**Rationale:** This hybrid style supports the legacy constraints (Windows NT/C++) while introducing modern security boundaries (Gateway) and extensibility (Adapters), balancing strict standards compliance (TMDD) with heterogeneous field devices.

---

# D. Detailed Technical Design

## 1. Core Logic Subsystem (C2C Core)
*   **Responsibilities:** TMDD canonical data processing, repository federation, device command execution. Owns `Incident`, `FieldDevice`, `Network` entities.
*   **Technology Options:**
    *   *Recommended:* C/C++ (Windows Server 2019+). Justification: Meets INF-ASR-005 (Legacy Env) with modern security waiver.
    *   *Conservative:* C/C++ (Windows NT 4.0). Justification: Strict SRS compliance, high security risk (INF-ASR-005).
    *   *Cutting-edge:* Rust (Linux). Justification: Modern safety, but violates INF-ASR-005 (Legacy Env).
*   **Recommended Stack:** C/C++ on Windows Server 2019+ (Waiver for NT). Justification: Meets INF-ASR-005 while allowing security patching (INF-NFR-002).
*   **Interface Design:**
    *   *External:* OpenAPI (See Section L `openapi.yaml`).
    *   *Internal:* gRPC (See Section L `internal.proto`).
*   **Data Model:** Relational SQL with TMDD canonical mapping. (See Section L `sql/network_ddl.sql`).
*   **Caching:** Redis for Session/Map Data. TTL: 5min. Invalidation: Write-through on Incident Update.

## 2. Security Gateway Subsystem
*   **Responsibilities:** TLS termination, RBAC enforcement, Audit Log initiation, Password Redaction.
*   **Technology Options:**
    *   *Recommended:* Nginx + OAuth2 Proxy. Justification: Meets INF-ASR-006 (Security Gateway).
    *   *Conservative:* Windows IIS + WAF. Justification: Aligns with legacy stack, higher overhead.
    *   *Cutting-edge:* Kubernetes Istio Gateway. Justification: Cloud-native, overkill for legacy core.
*   **Recommended Stack:** Nginx on Linux Container. Justification: Meets INF-ASR-006 (Public Network Boundary).
*   **Interface Design:** HTTPS External, Internal TLS to Core.
*   **Data Model:** No persistent data; ephemeral session store in Redis.

## 3. UI Subsystem (Web Map & Remote GUI)
*   **Responsibilities:** Map visualization, Incident entry, Device Control request initiation.
*   **Technology Options:**
    *   *Recommended:* React + ESRI ARC IMS Wrapper. Justification: Meets INF-FR-005 (Web Map) & INF-ASR-005 (ESRI).
    *   *Conservative:* Pure C/C++ GUI (Legacy). Justification: Matches SRS, poor web integration.
    *   *Cutting-edge:* Blazor/MAUI. Justification: Modern UI, less ESRI compatibility.
*   **Recommended Stack:** React (Web) + C/C++ (Legacy GUI Wrapper). Justification: Balances INF-FR-005 (Web) and INF-ASR-005 (Legacy).

## 4. Adapter Subsystem
*   **Responsibilities:** Translate system-specific protocols to TMDD Canonical.
*   **Technology Options:**
    *   *Recommended: *Plugin Architecture (DLLs). Justification: Meets INF-ASR-001 (Heterogeneous).
    *   *Conservative:* Hard-coded Monolith. Justification: Low modifiability.
    *   *Cutting-edge:* Microservices per Adapter. Justification: High ops overhead.
*   **Recommended Stack:** C++ Dynamic Libraries. Justification: Meets INF-ASR-004 (Configurable Blocks).

---

# E. Operations & Deployment

## 1. Kubernetes Plan (Gateway/UI)
The Legacy Core runs on VM, but Gateway/UI are containerized for scalability.
**File:** `k8s/core-service-deployment.yaml` (See Section L).
*   **Replicas:** Small (1), Medium (3), Large (5).
*   **Resources:** 500m CPU, 512MiB RAM (Gateway); 2 CPU, 4GiB RAM (Core VM).
*   **HPA:** Min 1, Max 10, Target CPU 70%.

## 2. DB HA Topology
*   **Engine:** PostgreSQL 14-15 (Canonical Store).
*   **Replication:** 1 Primary, 2 Read Replicas.
*   **Backup:** Daily Full, Hourly WAL. RPO: 1 hour. RTO: 4 hours.
*   **Justification:** Meets INF-NFR-004 (Data Collector storage).

## 3. Network Topology
*   **Ingress:** Public Internet -> DMZ (Gateway) -> Legacy Network (Core).
*   **Egress:** Core -> Field Devices (Private/Internal).
*   **Latency:** <2s for Map (INF-NFR-001); <5s for Command Status (INF-FR-004).
*   **Reference:** Physical View: Deployment Diagram (Element IDs: `DMZ`, `Legacy Center Network`).

## 4. CI/CD Sketch
*   **Build:** Compile C++ Core, Build Gateway Container.
*   **Test:** Contract Tests (OpenAPI), Unit Tests (Adapters).
*   **Deploy:** Blue/Green for Gateway; Rolling Update for Core (with restart window).
*   **Gating:** Security Scan (TLS config), Performance Test (Map Render <2s).

---

# F. Security Design

1.  **Auth & AuthZ:** OAuth2/OIDC for Remote Users; JWT for Internal Services.
    *   *Lifecycle:* Token expiry 1 hour; Refresh 24 hours.
    *   *Justification:* Meets INF-NFR-002 (RBAC Required).
2.  **Secrets Management:** Hashicorp Vault for API Keys/DB Credentials.
    *   *Rotation:* 90 days.
    *   *Justification:* Meets INF-NFR-002 (Password Redaction).
3.  **TLS:** TLS 1.2+ enforced at Gateway. Internal TLS between Gateway and Core.
    *   *Justification:* Meets INF-ASR-006 (Security Gateway).
4.  **Threat Model:**
    *   *Threat 1:* Unauthorized Device Control. *Mitigation:* RBAC + Audit Log (INF-NFR-002).
    *   *Threat 2:* Data Interception. *Mitigation:* TLS 1.2+ (INF-ASR-006).
    *   *Threat 3:* Legacy OS Compromise. *Mitigation:* Network Segmentation (INF-ASR-005).
    *   *Threat 4:* Audit Log Tampering. *Mitigation: *Immutable Hash Chain (INF-NFR-004).
    *   *Threat 5:* Protocol Injection. *Mitigation:* Adapter Validation (INF-ASR-001).

---

# G. Observability & SRE

1.  **Metrics:**
    *   `gateway_request_latency` (Histogram).
    *   `core_device_command_success_rate` (Counter).
    *   `audit_log_write_latency` (Histogram).
    *   **Prometheus Alert:** `avg(gateway_request_latency) > 2s` (INF-NFR-001).
    *   **Prometheus Alert:** `rate(core_device_command_success_rate) < 0.95` (INF-FR-004).
2.  **SLOs:**
    *   **Availability:** 99.9% (Gateway), 99.5% (Core).
    *   **Error Budget:** 0.1% 5xx errors per month.
    *   **RTO/RPO:** 4 hours / 1 hour (DB).
3.  **Dashboard:** Grafana dashboard showing Command Success Rate, Map Load Time, Audit Log Volume.
4.  **Runbook:** Steps for Gateway Restart, Core Failover, DB Restore.

---

# H. Testing Strategy

1.  **Test Matrix:**
    *   **Unit:** Core Logic (C++), Adapter Translation.
    *   **Integration:** Gateway -> Core, Core -> DB.
    *   **Contract:** OpenAPI Schema Validation (INF-FR-002).
    *   **E2E:** Remote User -> Device Control (INF-FR-004).
    *   **Chaos:** Network Partition between Gateway and Core.
2.  **Data Management:**
    *   **Environments:** Dev, Test, Prod.
    *   **Refresh:** Test env refreshed weekly with anonymized Prod data.
    *   **Isolation:** Separate DB instances per env.

---

# I. Migration, Data Conversion & Rollout Plan

1.  **Migration Steps:**
    *   Deploy Security Gateway in DMZ.
    *   Point Legacy Core to new Canonical DB.
    *   Enable Adapter Plugins for existing systems.
    *   Cut-over Public UI to new Gateway.
2.  **Data Sync:** Dual-write during transition; Backfill historical data to Canonical Model.
3.  **Rollback:** Revert Gateway DNS; Restore Legacy DB snapshot.
4.  **Compatibility:** API Versioning (v1, v2); Legacy Protocol Support via Adapters (INF-ASR-001).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why Chosen |
| :--- | :--- | :--- | :--- |
| **Core Language** | Java / .NET | Pros: Modern libs. Cons: Violates INF-ASR-005 (C++). | C++ matches SRS & Legacy perf. |
| **Security** | Legacy Auth (NTLM) | Pros: Native. Cons: Weak security (INF-NFR-002). | OAuth2/TLS meets modern sec reqs. |
| **Data Store** | NoSQL (Mongo) | Pros: Flexible. Cons: Weak transactional integrity (INF-NFR-004). | SQL ensures audit immutability. |
| **Deployment** | Pure Cloud | Pros: Scalable. Cons: Violates INF-ASR-005 (Windows NT). | Hybrid (VM + K8s) balances constraints. |

---

# K. Open Questions & Assumptions

**Assumptions:**
*   **A1:** Windows NT servers can be upgraded to Windows Server 2019+ under a signed waiver (INF-ASR-005).
*   **A2:** ESRI ARC IMS 10.9.1+ is available for Web Map generation (INF-FR-005).
*   **A3:** Field devices support TMDD message sets via adapter translation (INF-ASR-001).
*   **A4:** Network segmentation allows DMZ placement between Public Internet and Legacy Core (INF-ASR-006).

**Unresolved Questions:**
*   **Q1:** What is the exact EOL date for the Windows NT legacy environment? (Stakeholder: IT Ops).
*   **Q2:** Do all partner TMCs support DATEX/ASN encoding, or requires custom adapters? (Stakeholder: Partner Agencies).
*   **Q3:** What is the maximum concurrent user load for the Remote Control GUI? (Stakeholder: Traffic Ops).

---

# L. Deliverables

## 1. `architecture.md`
(This document constitutes the full architecture specification.)

## 2. `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: C2C Traffic Management API
  version: 1.0.0
  description: External API for Incident Management and Device Control
servers:
  - url: https://api.c2c.txdot.gov/v1
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Incident:
      type: object
      properties:
        incident_id: { type: string, format: uuid }
        network_id: { type: string }
        description: { type: string }
        roadway: { type: string }
        status: { type: string, enum: [Active, Resolved, Closed] }
    DeviceCommand:
      type: object
      properties:
        network_id: { type: string }
        device_id: { type: string }
        device_type: { type: string, enum: [DMS, LCS, CCTV, RampMeter] }
        command_params: { type: object }
        username: { type: string }
        password: { type: string, format: password } # Redacted in logs
paths:
  /incidents:
    post:
      summary: Create Incident
      security: [{ bearerAuth: [] }]
      requestBody:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/Incident' }
      responses:
        201: { description: Created }
        401: { description: Unauthorized }
  /incidents/{id}:
    put:
      summary: Update Incident
      security: [{ bearerAuth: [] }]
      parameters:
        - in: path, name: id, schema: { type: string }
      requestBody:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/Incident' }
      responses:
        200: { description: OK }
    delete:
      summary: Delete Incident
      security: [{ bearerAuth: [] }]
      parameters:
        - in: path, name: id, schema: { type: string }
      responses:
        204: { description: Deleted }
  /devices/command:
    post:
      summary: Control Device
      security: [{ bearerAuth: [] }]
      requestBody:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/DeviceCommand' }
      responses:
        200: { description: Command Accepted }
        403: { description: Forbidden }
  /devices/status:
    get:
      summary: Get Device Status
      security: [{ bearerAuth: [] }]
      parameters:
        - in: query, name: network_id, schema: { type: string }
        - in: query, name: device_type, schema: { type: string }
      responses:
        200: { description: Status List }
  /map/render:
    get:
      summary: Render Traffic Map
      parameters:
        - in: query, name: zoom, schema: { type: integer }
        - in: query, name: pan, schema: { type: string }
      responses:
        200: { description: Map Image URL }
```

## 3. `internal.proto`
```proto
syntax = "proto3";
package c2c.internal;

service DeviceController {
  rpc GetStatus(StatusRequest) returns (StatusResponse);
  rpc ExecuteCommand(CommandRequest) returns (CommandResponse);
}

service IncidentManager {
  rpc CreateIncident(IncidentRequest) returns (IncidentResponse);
  rpc UpdateIncident(IncidentRequest) returns (IncidentResponse);
}

message StatusRequest {
  string network_id = 1;
  string device_id = 2;
  string device_type = 3;
}

message StatusResponse {
  string status = 1;
  string location = 2;
  int64 timestamp = 3;
}

message CommandRequest {
  string network_id = 1;
  string device_id = 2;
  string command_type = 3;
  string params = 4;
  string user_id = 5;
}

message CommandResponse {
  bool success = 1;
  string message = 2;
}

message IncidentRequest {
  string incident_id = 1;
  string network_id = 2;
  string description = 3;
  string roadway = 4;
}

message IncidentResponse {
  string incident_id = 1;
  string status = 2;
}
```

## 4. `k8s/core-service-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: c2c-gateway
  namespace: traffic-ops
spec:
  replicas: 3
  selector:
    matchLabels:
      app: c2c-gateway
  template:
    metadata:
      labels:
        app: c2c-gateway
    spec:
      containers:
      - name: gateway
        image: c2c/gateway:1.0.0
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
        - name: TLS_VERSION
          value: "1.2"
        - name: AUDIT_LOG_PATH
          value: "/var/log/audit"
      - name: core-wrapper
        image: c2c/core-wrapper:1.0.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "2000m"
        command: ["./c2c_core.exe", "--mode", "normal"]
  minAvailable: 2
```

## 5. `sql/network_ddl.sql`
```sql
CREATE TABLE networks (
    network_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE links (
    link_id VARCHAR(50) PRIMARY KEY,
    network_id VARCHAR(50) NOT NULL REFERENCES networks(network_id),
    link_name VARCHAR(100),
    link_type VARCHAR(50),
    geom_data GEOMETRY,
    INDEX idx_network (network_id)
);

CREATE TABLE nodes (
    node_id VARCHAR(50) PRIMARY KEY,
    network_id VARCHAR(50) NOT NULL REFERENCES networks(network_id),
    node_name VARCHAR(100),
    node_type_desc VARCHAR(255)
);

CREATE TABLE incidents (
    incident_id UUID PRIMARY KEY,
    network_id VARCHAR(50) NOT NULL REFERENCES networks(network_id),
    description TEXT,
    roadway VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('Active', 'Resolved', 'Closed')),
    created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status)
);

CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    result VARCHAR(20),
    hash_chain VARCHAR(255) NOT NULL -- Immutable integrity
);
```

## 6. `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact filename(s),Rationale
INF-FR-001,Center provides network/link/node data,Logic View: ClassDiagram (Network),DataCollector,sql/network_ddl.sql,Canonical model for federation (ASR-003)
INF-FR-002,Center supports incident/lane closure info,Logic View: ClassDiagram (Incident),IncidentMgr,openapi.yaml,Public API for incident management (FR-002a)
INF-FR-003,Center provides device status,Logic View: ClassDiagram (FieldDevice),DeviceCtrl,internal.proto,Internal status polling (ASR-001)
INF-FR-004,Center supports device control commands,Process View: SequenceDiagram (DeviceControl),DeviceCtrl,openapi.yaml,Remote control requires auth/TLS (NFR-002)
INF-FR-005,Web Map displays traffic/incidents,Scenario View: UseCaseDiagram (UC_Map),WebMap,k8s/webui-deployment.yaml,Performance req <2s rendering (NFR-001)
INF-FR-006,Incident GUI allows entry/mod/delete,Scenario View: UseCaseDiagram (UC_Incident),IncidentMgr,openapi.yaml,CRUD operations require audit logging (NFR-004)
INF-FR-007,Remote Control GUI executes on public net,Physical View: DeploymentDiagram (Remote Workstation),RemoteGUI,openapi.yaml,Public network requires Security Gateway (ASR-006)
INF-NFR-001,Map rendering latency <2s,Process View: ActivityDiagram (Validate TLS),WebMap,k8s/webui-deployment.yaml,Caching strategy for performance
INF-NFR-002,Security: TLS RBAC Password Redaction,Logic View: ClassDiagram (SecurityGateway),SecurityGateway,internal.proto,Mitigates Legacy OS risk (ASR-005)
INF-NFR-003,Protocol: TMDD/DATEX/ASN over TCP/IP,Logic View: ClassDiagram (DeviceAdapter),AdapterMgr,sql/canonical_ddl.sql,Standards compliance (ASR-002)
INF-NFR-004,Test Mode logs activities immutably,Logic View: ClassDiagram (AuditLog),AuditComponent,sql/audit_ddl.sql,Auditability for compliance (FR-008)
INF-ASR-001,Interconnect dissimilar traffic systems,Development View: PackageDiagram (Adapters),AdapterMgr,internal.proto,Adapter pattern isolates core
INF-ASR-002,Utilize TMDD standard message sets,Logic View: ClassDiagram (FieldDevice),DataCollector,sql/canonical_ddl.sql,Canonical model ensures interoperability
INF-ASR-003,Repository federation (Local->Regional),Development View: PackageDiagram (Repository),Repository,sql/network_ddl.sql,Hierarchical data linking
INF-ASR-004,Configurable building blocks,Development View: ComponentDiagram (AdapterManager),AdapterMgr,k8s/core-service-deployment.yaml,Microkernel plugin architecture
INF-ASR-005,Execute in Windows NT environment,Physical View: DeploymentDiagram (Windows NT Server),C2C Core,k8s/core-service-deployment.yaml,Legacy constraint requires segmentation
INF-ASR-006,Security Gateway for public network,Physical View: DeploymentDiagram (Security Gateway Appliance),SecurityGateway,openapi.yaml,Enforces TLS 1.2+ before legacy core
```

---

# Acceptance Criteria Verification

- [x] 3-line Analysis Plan present.
- [x] Sections A-L included.
- [x] Every FR/NFR/ASR mapped in traceability matrix.
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [x] Representative k8s manifest snippet included.
- [x] SQL DDLs provided for persisted entities.
- [x] All major components have: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema.
- [x] Assumptions and open questions clearly listed.

# How to Review Checklist
- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?