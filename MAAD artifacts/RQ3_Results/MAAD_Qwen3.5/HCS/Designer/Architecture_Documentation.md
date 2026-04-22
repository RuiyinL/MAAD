Analysis Plan
Scope: DigitalHome Prototype (Smart Home Management System) covering Device Control, Security, Scheduling, and Reporting.
Approach: Modular Monolith with Hexagonal Architecture, Contract-First Design (OpenAPI/Proto), and SLO-driven Observability.
Validation: Traceability Matrix (Req→Artifact), SLO Verification (Latency/Availability), and Security Audit (TLS/Auth).

# DigitalHome System Architecture Document

## A. Executive Summary

The **DigitalHome System** is a local home server application designed to manage household devices (thermostats, humidistats, security sensors, power switches) via a web interface and a gateway device. This architecture supports the **DigitalHomeOwner Division's** goal of a 12-month prototype to validate business concepts.

*   **Primary Diagrams:** Deployment_Diagram (Physical), Component_Diagram (Logical), Class_Diagram (Data).
*   **Architectural Style:** Modular Monolith with Hexagonal (Ports & Adapters) Architecture.
*   **Deployment Topology:** Single-node Home Server (Docker/Kubernetes) with Local Database and RF Gateway.

### Top 3 Design Risks & Mitigations

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Gateway Communication Latency** | High latency may violate NFR-001 (2s display update). | Implement asynchronous event bus (Redis Pub/Sub) and push-based UI (SSE/WebSocket). |
| **Single Point of Failure (Home Server)** | System outage affects all home automation. | Daily automated backups (ASR-003) with RTO ≤ 10min; Heartbeat monitoring on Gateway. |
| **Security Breach (IoT/Web)** | Unauthorized access to home devices. | TLS 1.3 enforcement, RBAC (NFR-003), and Network Segmentation (IoT VLAN). |

### QA Coverage Mapping

| Quality Attribute | Requirements | Test Type |
| :--- | :--- | :--- |
| **Performance** | NFR-001 (2s update, 10Hz acquisition) | Load Testing, Latency Monitoring |
| **Reliability** | NFR-002 (1 failure/10k hrs), ASR-003 (Backup) | Chaos Engineering, Backup Restore Drills |
| **Security** | NFR-003 (TLS, Auth) | Penetration Testing, AuthZ Verification |
| **Maintainability** | NFR-005 (UML, OO), ASR-004 | Static Analysis, Code Coverage (>80%) |
| **Usability** | NFR-004 (Web UI, WCAG) | UX Testing, Accessibility Audit |

---

## B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) | Component(s) | Artifact | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | User Authentication & Account Mgmt | UseCase_Diagram:UC01 | Auth Service | `openapi.yaml` | Core access control for all users. |
| **FR-002** | Thermostat Control (60-80°F) | Class_Diagram:Thermostat | Device Control | `sql/device_ddl.sql` | Environmental regulation requirement. |
| **FR-003** | Humidistat Control (30-60%) | Class_Diagram:Humidistat | Device Control | `sql/device_ddl.sql` | Environmental regulation requirement. |
| **FR-004** | Security Sensors & Alarms | State_Diagram:SecuritySensor | Security Service | `internal.proto` | Critical safety function. |
| **FR-005** | Appliance Power Switches | Class_Diagram:PowerSwitch | Device Control | `internal.proto` | Remote on/off capability. |
| **FR-006** | Scheduling & Planning | Activity_Diagram | Scheduling Service | `openapi.yaml` | Automation logic for user convenience. |
| **FR-007** | Reporting (Temp/Humidity/Security) | Class_Diagram:Report | Reporting Service | `openapi.yaml` | Historical data analysis. |
| **FR-008** | Manual Override | Sequence_Diagram_TemperatureControl | Device Control | `internal.proto` | User priority over schedules. |
| **NFR-001** | Performance (2s update, 10Hz) | Component_Diagram:EventBus | Event Bus | `k8s/app-deployment.yaml` | Real-time responsiveness. |
| **NFR-002** | Reliability (1 failure/10k hrs) | Deployment_Diagram | Backup Service | `sql/backup_ddl.sql` | System stability. |
| **NFR-003** | Security (TLS, Audit) | Package_Diagram:Security Adapter | Auth Service | `openapi.yaml` | Data protection and compliance. |
| **NFR-004** | Usability (Web, WCAG) | UseCase_Diagram:User | Web UI | `openapi.yaml` | User experience standard. |
| **NFR-005** | Maintainability (UML, OO) | Package_Diagram | All Modules | `architecture.md` | Long-term code health. |
| **ASR-001** | Local Home Server | Deployment_Diagram:HomeServer | Infrastructure | `k8s/app-deployment.yaml` | Deployment constraint. |
| **ASR-002** | Gateway RF Communication | Component_Diagram:GatewayAdapter | Gateway Adapter | `internal.proto` | Hardware interface. |
| **ASR-003** | Backup & Recovery | Deployment_Diagram:BackupVolume | Backup Service | `sql/backup_ddl.sql` | Data durability. |
| **ASR-004** | OO Design (UML 2.0) | Class_Diagram | All Code | `architecture.md` | Development standard. |
| **ASR-005** | Simulated Environment | Package_Diagram:Simulation Adapter | Simulation Adapter | `internal.proto` | Testing constraint. |
| **ASR-006** | Cost Minimization | Deployment_Diagram | Infrastructure | `k8s/app-deployment.yaml` | Budget constraint. |
| **INF-001** | Session Timeout (15 min) | Activity_Diagram | Auth Service | `openapi.yaml` | Inferred from security best practices. |

---

## C. Architecture Overview

The architecture follows the **4+1 View Model**, realized through the provided PlantUML diagrams.

1.  **Context View:** The system interacts with **General Users**, **Master Users**, **Technicians**, and **External IoT Devices** (via Gateway). (Ref: `UseCase_Diagram`)
2.  **Container View:** The system is a **Web Application** (UI + API), **Business Logic Service**, **Gateway Service**, **Database**, and **Backup Service**. (Ref: `Container_Diagram`)
3.  **Component View:** Internal components include **Device Control**, **Scheduling**, **Reporting**, **Authentication**, and **Gateway Adapter**. (Ref: `Component_Diagram`, `Package_Diagram`)
4.  **Runtime/Logic View:** Objects like `Thermostat`, `User`, `SchedulePlan` interact via Services and Repositories. (Ref: `Class_Diagram`, `Object_Diagram`, `State_Diagram`)
5.  **Deployment View:** Hosted on a **Home Computer** (Docker/K8s), connecting to **Gateway Device** (RF) and **User Devices** (Browser). (Ref: `Deployment_Diagram`)

**Key Architectural Decisions:**
*   **Modular Monolith:** Reduces operational complexity for the prototype (ASR-006) while maintaining module boundaries for future extraction (ASR-001).
*   **Hexagonal Architecture:** Isolates core logic from infrastructure (Database, Gateway, Web) to support testing and technology swaps (NFR-005).
*   **Event-Driven UI:** Server-Sent Events (SSE) ensure real-time updates (NFR-001) without heavy polling.

---

## D. Detailed Technical Design

### 1. Web Application (UI & API)
*   **Responsibilities:** User authentication, dashboard display, command issuance, report rendering.
*   **Technology Options:**
    1.  **Recommended:** React 18 + Vite + TypeScript. (Justification: Meets NFR-004 for modern UX, strong ecosystem).
    2.  **Conservative:** Angular 16 + TypeScript. (Justification: Enterprise standard, steeper learning curve).
    3.  **Cutting-edge:** SvelteKit + WebAssembly. (Justification: High performance, smaller bundle, less mature ecosystem).
*   **Recommended Stack:** React 18, Node.js 20 LTS. Justification: Meets NFR-004 (Usability) and ASR-004 (OO/Component-based).

### 2. Business Logic Service (Backend)
*   **Responsibilities:** Device state management, scheduling logic, security rules, reporting aggregation.
*   **Technology Options:**
    1.  **Recommended:** Java 17 + Spring Boot 3. (Justification: Meets ASR-004 (OO), ASR-006 (Standard), strong enterprise support).
    2.  **Conservative:** Python 3.11 + Django. (Justification: Fast dev, but GIL may limit 10Hz throughput).
    3.  **Cutting-edge:** Go 1.21 + Gin. (Justification: High performance, but less OO-focused than Java).
*   **Recommended Stack:** Java 17, Spring Boot 3.1. Justification: Meets ASR-004 (OO Design) and NFR-005 (Maintainability).

### 3. Persistence (Database)
*   **Responsibilities:** Store device states, user accounts, schedules, audit logs, backups.
*   **Technology Options:**
    1.  **Recommended:** PostgreSQL 15. (Justification: Meets ASR-003 (Backup/Reliability), ACID compliance).
    2.  **Conservative:** MySQL 8. (Justification: Widely supported, less advanced JSON handling).
    3.  **Cutting-edge:** CockroachDB. (Justification: Distributed SQL, overkill for single-node prototype).
*   **Recommended Stack:** PostgreSQL 15. Justification: Meets ASR-003 (Data Durability) and NFR-003 (Audit capabilities).

### 4. Gateway Adapter (IoT Communication)
*   **Responsibilities:** Translate RF signals to internal events, manage device polling (10Hz).
*   **Technology Options:**
    1.  **Recommended:** Python 3.11 + AsyncIO. (Justification: Great for I/O bound tasks, hardware libs).
    2.  **Conservative:** C++ + Boost.Asio. (Justification: High performance, higher complexity).
    3.  **Cutting-edge:** Rust + Tokio. (Justification: Memory safety, steep learning curve).
*   **Recommended Stack:** Python 3.11. Justification: Meets ASR-002 (Gateway Integration) and minimizes dev time.

### Interface Design

#### External API (OpenAPI)
*   **Filename:** `openapi.yaml`
*   **Description:** Public REST API for Web UI and Mobile Clients.
*   **See Section L for full specification.**

#### Internal Contract (gRPC)
*   **Filename:** `internal.proto`
*   **Description:** Communication between Business Logic and Gateway Adapter/Simulator.
*   **See Section L for full specification.**

### Data Model / Schema
*   **Primary Entities:** `users`, `devices`, `device_states`, `schedules`, `audit_logs`.
*   **Encryption:** `password_hash` (bcrypt), `audit_logs` (WORM storage).
*   **See Section L for `sql/schema.sql`.**

### Caching & Consistency
*   **Strategy:** Redis for Session Store and Device State Cache.
*   **TTL:** Session (15 mins per INF-001), Device State (5 seconds).
*   **Consistency:** Strong consistency for Commands (SQL), Eventual for UI Updates (Redis Pub/Sub). Justification: Meets NFR-001 (Performance).

---

## E. Operations & Deployment

### 1. Kubernetes Plan
*   **Runtime:** K3s (Lightweight Kubernetes for Home Server). Justification: Meets ASR-006 (Cost/Resource constraints).
*   **Manifest:** See Section L (`k8s/app-deployment.yaml`).
*   **Replicas:** 1 (Stateful), HPA based on CPU > 70%.

### 2. Database HA & Backup
*   **Topology:** Single Node (Prototype), WAL Archiving enabled.
*   **Backup:** Daily `pg_dump` to local volume + Remote S3 (if configured).
*   **RTO/RPO:** RTO ≤ 10 min, RPO ≤ 24 hours (per ASR-003).

### 3. Network Topology
*   **Ingress:** Nginx Ingress Controller (TLS Termination).
*   **Egress:** Restricted to NTP and Update Server (per Deployment_Diagram).
*   **Latency:** < 100ms internal, < 2s End-to-End (NFR-001).

### 4. CI/CD Sketch
1.  **Build:** Maven (Java) + npm (React).
2.  **Test:** Unit (JUnit), Contract (Pact), Integration (TestContainers).
3.  **Deploy:** Helm Chart to Home Server.
4.  **Gate:** Security Scan (OWASP), SLO Check.

---

## F. Security Design

1.  **Auth & AuthZ:**
    *   **Protocol:** OAuth2/OIDC (Keycloak embedded or Spring Security).
    *   **Tokens:** JWT (Short-lived), Refresh Tokens (Rotated).
    *   **RBAC:** Roles: `GENERAL`, `MASTER`, `TECHNICIAN` (per Class_Diagram).
2.  **Secrets Management:**
    *   Kubernetes Secrets (encrypted at rest).
    *   Rotation: Every 90 days or on breach.
3.  **TLS:**
    *   TLS 1.3 enforced on all external interfaces (NFR-003).
    *   mTLS for internal service-to-service (optional for prototype, recommended for commercial).
4.  **Threat Model:**
    *   *Threat:* Unauthorized Device Control. *Mitigation:* AuthZ checks on every command.
    *   *Threat:* Data Tampering. *Mitigation:* Audit Logs (Immutable).
    *   *Threat:* Replay Attack. *Mitigation:* Nonce/Timestamp in RF commands.
    *   *Threat:* Credential Theft. *Mitigation:* bcrypt hashing, Account Lockout (5 attempts).
    *   *Threat:* Gateway Spoofing. *Mitigation:* Pre-shared Keys (PSK) for RF.

---

## G. Observability & SRE

1.  **Metrics:**
    *   `http_request_duration_seconds` (Latency)
    *   `device_command_total` (Usage)
    *   `system_uptime_seconds` (Reliability)
2.  **Alerts (Prometheus):**
    *   `alert: HighLatency expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2`
    *   `alert: DeviceOffline expr: time() - device_last_seen_timestamp > 60`
3.  **SLOs:**
    *   **Availability:** 99.0% (Prototype).
    *   **Latency:** 95% of UI updates < 2s.
    *   **Error Rate:** < 1% of requests.
4.  **Runbooks:**
    *   *Gateway Disconnect:* Check RF module power, restart Gateway Service.
    *   *DB Disk Full:* Clear old audit logs (>1 year), expand volume.

---

## H. Testing Strategy

| Test Type | Scope | Tools | Frequency |
| :--- | :--- | :--- | :--- |
| **Unit** | Classes/Methods | JUnit, Jest | On Commit |
| **Integration** | Module Interactions | TestContainers | On Merge |
| **Contract** | API Compatibility | Pact, OpenAPI Validator | On PR |
| **E2E** | User Flows | Cypress, Selenium | Nightly |
| **Chaos** | Resilience | Chaos Mesh | Monthly |

*   **Data Management:** Synthetic data generation for Privacy.
*   **Environments:** Dev (Local), Staging (Simulated Gateway), Prod (Home Server).

---

## I. Migration, Data Conversion & Rollout Plan

1.  **Migration:** Greenfield project. No legacy data migration required.
2.  **Rollout:**
    *   Phase 1: Simulator Only (Dev).
    *   Phase 2: Single Home Pilot (Prototype).
    *   Phase 3: Commercial Release (Future).
3.  **Backwards Compatibility:** API Versioning (`/api/v1/`) enforced in OpenAPI.
4.  **Rollback:** Helm Rollback to previous revision if Health Check fails.

---

## J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros | Cons | Choice Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Microservices | Scalability, Isolation | High Ops Cost, Complexity | **Modular Monolith** fits 5-engineer team & ASR-006 (Cost). |
| **DB** | NoSQL (MongoDB) | Flexible Schema | Weak Transactions | **PostgreSQL** ensures ACID for Scheduling/Security (ASR-003). |
| **UI Update** | Polling | Simple | High Latency, Load | **SSE/WebSocket** meets NFR-001 (2s update). |
| **Language** | Python (Backend) | Fast Dev | Slower Execution | **Java** preferred for OO/Enterprise alignment (ASR-004). |

---

## K. Open Questions & Assumptions

### Assumptions
*   **A1:** The "Home Computer" has a minimum of 4GB RAM and 2 CPU Cores available for the server.
*   **A2:** The RF Gateway device firmware supports the defined internal proto contract.
*   **A3:** Internet connection is stable enough for initial authentication and alerts (ISP dependency).
*   **A4:** "1 failure per 10,000 hours" is interpreted as MTBF for the software process, excluding hardware.
*   **A5:** Users have basic web literacy (per Original Requirements).

### Unresolved Questions
1.  **Q1:** What is the specific RF protocol (Z-Wave, Zigbee, Proprietary)? *Suggestion: Define in Gateway Adapter Spec.*
2.  **Q2:** Are there legal compliance requirements for Security Alarm data (e.g., local law enforcement integration)? *Suggestion: Consult Legal.*
3.  **Q3:** What is the maximum retention period for Audit Logs beyond the 1-year NFR? *Suggestion: Confirm with Compliance.*

---

## L. Deliverables

### 1. `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: DigitalHome API
  version: 1.0.0
  description: External API for DigitalHome System
servers:
  - url: /api/v1
paths:
  /auth/login:
    post:
      summary: User Login
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string }
                password: { type: string }
      responses:
        200:
          description: JWT Token
        401:
          description: Invalid Credentials
  /devices/{deviceId}/state:
    get:
      summary: Get Device State
      parameters:
        - in: path
          name: deviceId
          schema: { type: string }
      responses:
        200:
          description: Device State
          content:
            application/json:
              schema:
                type: object
                properties:
                  value: { type: number }
                  unit: { type: string }
    put:
      summary: Set Device State
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                targetValue: { type: number }
      responses:
        200: { description: OK }
        400: { description: Invalid Range }
  /schedules:
    post:
      summary: Create Schedule
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                deviceId: { type: string }
                timeSlot: { type: string }
                action: { type: string }
      responses:
        201: { description: Created }
  /reports/monthly:
    get:
      summary: Get Monthly Report
      parameters:
        - in: query
          name: month
          schema: { type: string }
      responses:
        200:
          description: Report Data
          content:
            application/json:
              schema:
                type: object
```

### 2. `internal.proto`
```proto
syntax = "proto3";
package digitalhome.internal;

service GatewayService {
  rpc SendCommand (DeviceCommand) returns (CommandResponse);
  rpc SubscribeToDeviceEvents (DeviceSubscription) returns (stream DeviceEvent);
}

message DeviceCommand {
  string deviceId = 1;
  string commandType = 2; // e.g., SET_TEMP, TOGGLE_SWITCH
  string value = 3;
}

message CommandResponse {
  bool success = 1;
  string message = 2;
}

message DeviceEvent {
  string deviceId = 1;
  string eventType = 2; // e.g., STATE_CHANGE, BREACH
  string value = 3;
  int64 timestamp = 4;
}

message DeviceSubscription {
  string deviceId = 1;
}
```

### 3. `k8s/app-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: digitalhome-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: digitalhome
  template:
    metadata:
      labels:
        app: digitalhome
    spec:
      containers:
      - name: app
        image: digitalhome/app:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "prod"
---
apiVersion: v1
kind: Service
metadata:
  name: digitalhome-service
spec:
  selector:
    app: digitalhome
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

### 4. `sql/schema.sql`
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- GENERAL, MASTER, TECHNICIAN
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE devices (
    device_id UUID PRIMARY KEY,
    device_type VARCHAR(50) NOT NULL, -- THERMOSTAT, HUMIDISTAT, etc.
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'ONLINE'
);

CREATE TABLE device_states (
    state_id UUID PRIMARY KEY,
    device_id UUID REFERENCES devices(device_id),
    current_value NUMERIC,
    target_value NUMERIC,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45)
);
-- Index for performance on reports
CREATE INDEX idx_device_states_updated ON device_states(updated_at);
```

### 5. `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact,Rationale
FR-001,User Authentication,UseCase_Diagram:UC01,Auth Service,openapi.yaml,Core access control
FR-002,Thermostat Control,Class_Diagram:Thermostat,Device Control,sql/schema.sql,Env regulation
FR-003,Humidistat Control,Class_Diagram:Humidistat,Device Control,sql/schema.sql,Env regulation
FR-004,Security Sensors,State_Diagram:SecuritySensor,Security Service,internal.proto,Safety function
FR-005,Power Switches,Class_Diagram:PowerSwitch,Device Control,internal.proto,Remote control
FR-006,Scheduling,Activity_Diagram,Scheduling Service,openapi.yaml,Automation
FR-007,Reporting,Class_Diagram:Report,Reporting Service,openapi.yaml,Historical analysis
FR-008,Manual Override,Sequence_Diagram,Device Control,internal.proto,User priority
NFR-001,Performance (2s),Component_Diagram,Event Bus,k8s/app-deployment.yaml,Real-time
NFR-002,Reliability,Deployment_Diagram,Backup Service,sql/schema.sql,Stability
NFR-003,Security (TLS),Package_Diagram,Auth Service,openapi.yaml,Protection
NFR-004,Usability,UseCase_Diagram,Web UI,openapi.yaml,UX Standard
NFR-005,Maintainability,Package_Diagram,All Modules,architecture.md,Code Health
ASR-001,Local Server,Deployment_Diagram,Infrastructure,k8s/app-deployment.yaml,Deployment
ASR-002,Gateway RF,Component_Diagram,Gateway Adapter,internal.proto,Hardware Interface
ASR-003,Backup,Deployment_Diagram,Backup Service,sql/schema.sql,Durability
ASR-004,OO Design,Class_Diagram,All Code,architecture.md,Standard
ASR-005,Simulation,Package_Diagram,Simulation Adapter,internal.proto,Testing
ASR-006,Cost,Deployment_Diagram,Infrastructure,k8s/app-deployment.yaml,Budget
INF-001,Session Timeout,Activity_Diagram,Auth Service,openapi.yaml,Security Best Practice
```

---

### How to Review
- [ ] All FR/NFR/ASR present in traceability matrix?
- [ ] OpenAPI + internal API contract included and valid?
- [ ] Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- [ ] k8s snippet present and syntactically valid?
- [ ] SQL DDLs provided for persisted entities?
- [ ] Assumptions and open questions clearly listed?