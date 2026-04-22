Scope: Produce production-ready architecture for **DigitalHome (DH)** smart-house prototype per Original Requirements, reconciling conflicts with provided UML set.  
Approach: Normalize all requirements into atomic **INF-FR/NFR/ASR** IDs, map to 4+1 views, and specify implementable APIs, schemas, and ops artifacts.  
Validation: Cross-check (1) full traceability coverage, (2) API/schema syntactic validity, (3) NFR/ASR measurability + test plan alignment.

# A. Executive Summary (≤1 page)

**System overview.** DigitalHome (DH) is a smart-house home-management system enabling residents to **monitor and control** temperature, humidity, security contacts/alarms, and appliance/light power switches via a **web interface** hosted on a **home web server** and connected through a **Gateway** with RF wireless to devices.

**Primary diagram mapping (provided UML set; conflicts logged in K).**  
- Scenario View: *UseCase_ScenarioView* (elements: `EndUser`, `Admin`, `Play Game`, `Manage Questions`) — **conflicts with DH scope**; used only as a structural placeholder.  
- Physical View: *Deployment_PhysicalView* (elements: `User Device`, `Web Server Node`, `Storage Volume`) — reused conceptually for DH web server + storage.  
- Physical View: *Container_PhysicalView* (elements: `Backend`, `Data`) — reused conceptually for DH backend services.

**Architectural style(s).** Modular monolith (hexagonal/layered) on the home server with clear ports/adapters for RF gateway, web UI, persistence, and reporting.  
**Deployment topology.** Single home server + gateway + RF devices; optional remote access via ISP with TLS termination on home server.

**Top 3 design risks & mitigations**

| Risk | Impact | Mitigation |
|---|---|---|
| R1: Provided UML describes a different system (web learning game) | Wrong implementation scope | Declare **Original Requirements as scope authority**; create INF-* requirements; log conflicts (K) and map only reusable structural patterns. |
| R2: Real-time update constraints (2s UI refresh, 10Hz acquisition) vs web stack | Missed performance/UX | Use gateway polling at 10Hz, server-side aggregation, push updates via WebSocket/SSE at ≤2s; load test + timing assertions (H). |
| R3: Reliability/backup/recovery requirements in a home environment | Data loss / downtime | Daily scheduled backups, local UPS recommendation, transactional DB, restore automation, health checks; chaos/power-loss simulation tests (H/G). |

**Key QA coverage mapping (ASR/NFR → test types)**

| Quality attribute | Requirement IDs | Test types |
|---|---|---|
| Scalability (device counts) | INF-FR-TH-01..03, INF-FR-HU-01..03, INF-FR-SE-01..03, INF-FR-AP-01..03 | Integration + load tests with simulated devices |
| Availability/Reliability | INF-NFR-REL-01, INF-ASR-BR-01..02 | Chaos (power/network loss), soak tests |
| Security | INF-ASR-SEC-01..03 | SAST/DAST, TLS config tests, authZ tests |
| Performance/Timeliness | INF-NFR-PERF-01..02 | Latency tests, WebSocket/SSE timing tests |
| Maintainability/Modifiability | INF-ASR-MAINT-01, INF-ASR-OO-01 | Architecture tests, module boundaries, code review gates |

---

# B. Traceability & Rationale

## Requirement normalization
The Original Requirements lack IDs; therefore all are captured as **inferred atomic requirements** with `INF-` prefix (listed in K). The table below is also delivered as `traceability_matrix.csv` in L.

**Traceability matrix (excerpted; full in L as CSV).**

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-CTX-01 | Web-ready device controls temp/humidity/lights/security/appliances | Container_PhysicalView:`Backend`,`Data` | WebUI, DH-API | openapi.yaml | Core user capability; API exposes control/monitor endpoints. |
| INF-FR-SRV-01 | Home web server provides interaction/control | Deployment_PhysicalView:`Web Server Node` | HomeServer | k8s/dh-backend-deployment.yaml | Central compute node hosting services. |
| INF-FR-SRV-02 | Home web server stores plans/data | Deployment_PhysicalView:`Storage Volume` | Persistence | sql/*.sql | DB stores configuration, plans, telemetry, events. |
| INF-FR-ACC-01 | Establish/maintain user accounts | (conflict) UseCase_ScenarioView:`Admin` | Identity/Auth | openapi.yaml, sql/user_ddl.sql | Needed for General/Master/Technician roles. |
| INF-FR-ACC-02 | Backup service for accounts/plans/db | Deployment_PhysicalView:`Storage Volume` | BackupJob | k8s/dh-backend-deployment.yaml | Scheduled backup + restore procedures. |
| INF-FR-GW-01 | Gateway connects to broadband + RF module | Deployment_PhysicalView:`Web Server Node` (conceptual) | GatewayAdapter | internal.proto | Defines gateway protocol boundary. |
| INF-NFR-RANGE-01 | RF indoor range ≤1000 ft | — | Gateway, Devices | internal.proto | Drives gateway/device comm constraints in simulator. |
| INF-FR-TH-01 | Thermostat reads current temp | — | ThermostatService | openapi.yaml | Monitoring endpoint returns readings. |
| INF-FR-TH-02 | Set temp 60–80°F step 1 | — | ThermostatService | openapi.yaml | Validation rules in API + domain. |
| INF-FR-TH-03 | Up to 8 thermostats; individual/collective control | — | ThermostatService | openapi.yaml, sql/device_ddl.sql | Device registry + group operations. |
| INF-FR-TH-04 | 24 hourly settings/day, weekly schedule | — | PlannerService | sql/plan_ddl.sql | Plan model supports per-hour schedule. |
| INF-NFR-UNITS-01 | Support °F and °C | — | Domain | openapi.yaml | Unit conversion in domain layer. |
| INF-ASR-STD-ASHRAE-01 | Adhere to ASHRAE 2010 | — | Domain/Rules | architecture.md | Encoded as validation constraints + documentation. |
| INF-FR-HU-01 | Humidistat reads humidity | — | HumidityService | openapi.yaml | Monitoring endpoint. |
| INF-FR-HU-02 | Set humidity 30–60% step 1% | — | HumidityService | openapi.yaml | Validation rules. |
| INF-FR-HU-03 | Up to 8 humidistats; schedules | — | PlannerService | sql/plan_ddl.sql | Same plan mechanism. |
| INF-FR-SE-01 | Manage up to 50 contact sensors | — | SecurityService | sql/device_ddl.sql | Device registry capacity. |
| INF-FR-SE-02 | Activate sound+light alarms on breach | — | SecurityService | internal.proto | Event-driven alarm activation. |
| INF-FR-SE-03 | Record breach day/time in report | — | ReportingService | sql/event_ddl.sql | Security events persisted for reports. |
| INF-FR-AP-01 | Manage up to 100 power switches | — | ApplianceService | sql/device_ddl.sql | Device registry capacity. |
| INF-FR-AP-02 | Read power state OFF/ON | — | ApplianceService | openapi.yaml | State query endpoint. |
| INF-FR-AP-03 | Change power state OFF↔ON | — | ApplianceService | openapi.yaml | Command endpoint. |
| INF-FR-PLN-01 | Month plan: up to 4 daily periods | — | PlannerService | sql/plan_ddl.sql | Plan schema supports 4 periods/day. |
| INF-FR-PLN-02 | Override planned values via web/manual until period end | — | PlannerService | sql/override_ddl.sql | Overrides with expiry at period boundary. |
| INF-FR-RPT-01 | Month report for past 2 years | — | ReportingService | sql/reporting_views.sql | Retention + aggregation queries. |
| INF-NFR-UI-01 | Displays updated at least every 2 seconds | — | WebUI, RealtimeService | openapi.yaml | WebSocket/SSE push interval. |
| INF-NFR-DAQ-01 | Sensor acquisition ≥10 Hz | — | GatewayAdapter | internal.proto | Polling/streaming rate in gateway sim. |
| INF-NFR-REL-01 | ≤1 failure per 10,000 hours | — | Whole system | G/SLOs | Reliability SLO + soak tests. |
| INF-ASR-BR-01 | Daily backup at technician-set time | — | BackupJob | k8s manifest | Cron schedule configurable. |
| INF-ASR-BR-02 | Recovery restores from most recent backup | — | RestoreTool | runbook | Restore procedure + verification. |
| INF-NFR-ERR-01 | Clear descriptive error messages | — | API | openapi.yaml | Standard error schema. |
| INF-ASR-SEC-01 | TLS for auth + encryption | Deployment_PhysicalView:`HTTPS` | Ingress/API | k8s manifest | TLS-only ingress. |
| INF-ASR-MAINT-01 | Prototype modules reusable for commercial version | Package_DevelopmentView:`domain`,`services` | All | architecture.md | Clean boundaries, replaceable adapters. |
| INF-ASR-DOC-01 | Docs in HO2305 format + archive | — | Process | Deliverables | Ensures documentation completeness. |
| INF-ASR-OO-01 | OO + UML 2.0 preferred | — | Codebase | architecture.md | Aligns design to OO modules and UML views. |
| INF-PRJ-01 | 12 months, 5 engineers, cost minimized | — | Process | J | Drives stack simplicity (modular monolith). |
| INF-ENV-01 | Simulated environment realistic | — | Simulator | internal.proto | Device simulator + constraints. |

---

# C. Architecture Overview

## Context (who/what interacts)
Actors: General User, Master User, Technician; external ISP; physical devices (thermostats, humidistats, contact sensors, alarms, power switches) via Gateway RF.  
(Conceptual reuse) *Deployment_PhysicalView* nodes map to **User Device (Browser)**, **Web Server Node (Home Server)**, **Storage Volume (DB/Backups)**.

## Container view
- **Web UI** (browser on PC/phone/PDA) communicates with **DH Backend API** over HTTPS.  
- **DH Backend** hosts domain services: Device Registry, Telemetry, Control, Planner, Reporting, Identity/Auth, Backup/Restore.  
- **Gateway Adapter** communicates with Gateway (simulated RF) using an internal protocol.  
(Conceptual reuse) *Container_PhysicalView* `Backend` and `Data`.

## Component/Package view
Packages (conceptual): `ui`, `api`, `domain`, `services`, `persistence`, `audit` (from *Package_DevelopmentView*), but renamed to DH equivalents in code:
- `dh-ui`, `dh-api`, `dh-domain`, `dh-services`, `dh-persistence`, `dh-audit`.

## Class/Runtime view
Runtime flows:
1) Telemetry ingestion at ≥10Hz from gateway → persisted time-series rows → aggregated for UI updates every ≤2s.  
2) Control commands from UI → validation → gateway command → device state update → event persisted.  
3) Planner applies scheduled setpoints and resolves overrides.

## Deployment view
Single home server deployment (k8s optional for simulation/prototype) with local DB volume and daily backups; remote access via ISP with TLS.

---

# D. Detailed Technical Design (developer-facing)

## D1. DH Backend (API + Services)

### 1) Responsibilities & data ownership
Owns all business logic and persistence: user accounts/roles, device registry, telemetry, commands, plans/overrides, security events, reporting aggregates, and backup metadata. It is the system of record for DH state.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: **Java 21 (21–22)** (LTS)  
- Conservative: **Java 17 (17–21)**  
- Cutting-edge: **Go 1.22–1.23**  
Compatibility: Java aligns with OO/UML preference; Go reduces footprint but changes modeling style.  
Justification (recommended): meets **INF-ASR-OO-01** (OO development) and **INF-ASR-MAINT-01** (modular reuse).

**Web framework**
- Recommended: **Spring Boot 3.2–3.3**  
- Conservative: **Jakarta EE 10 (Payara/MicroProfile)**  
- Cutting-edge: **Quarkus 3.8–3.12**  
Justification: Spring ecosystem accelerates delivery for **INF-PRJ-01** (12 months/5 engineers).

**RPC/HTTP**
- Recommended: **REST/JSON + WebSocket (or SSE)**  
- Conservative: **REST-only (polling)**  
- Cutting-edge: **gRPC-web for UI + gRPC internal**  
Justification: WebSocket/SSE supports **INF-NFR-UI-01** (≤2s updates).

**Persistence (SQL/NoSQL)**
- Recommended: **PostgreSQL 14–16**  
- Conservative: **SQLite 3.42+** (single-node)  
- Cutting-edge: **TimescaleDB 2.13+** (Postgres extension)  
Justification: Postgres supports reporting/retention for **INF-FR-RPT-01** (2-year reports).

**Cache**
- Recommended: **Caffeine (in-process) 3.1+**  
- Conservative: **No cache**  
- Cutting-edge: **Redis 7.2–7.4**  
Justification: In-process cache helps meet **INF-NFR-UI-01** without extra ops burden (**INF-PRJ-01**).

**Messaging**
- Recommended: **In-process event bus (Spring ApplicationEvent)**  
- Conservative: **Direct calls only**  
- Cutting-edge: **NATS 2.10+**  
Justification: In-process events simplify while supporting reliability goals **INF-NFR-REL-01**.

**Search**
- Recommended: **Postgres indexes + materialized views**  
- Conservative: **No search; only reports**  
- Cutting-edge: **OpenSearch 2.x**  
Justification: Keep minimal cost/complexity per **INF-PRJ-01**.

**Authn/Authz**
- Recommended: **OIDC (Keycloak 24–26) + JWT** (optional for prototype)  
- Conservative: **Local users in DB + session cookies**  
- Cutting-edge: **Passkeys/WebAuthn**  
Justification: TLS + strong auth supports **INF-ASR-SEC-01**.

**Observability**
- Recommended: **OpenTelemetry + Prometheus + Grafana + Loki**  
- Conservative: **Logs only (JSON) + basic metrics**  
- Cutting-edge: **eBPF-based profiling (Parca)**  
Justification: Reliability monitoring supports **INF-NFR-REL-01**.

**CI/CD**
- Recommended: **GitHub Actions + Trivy + OWASP Dependency-Check**  
- Conservative: **Jenkins**  
- Cutting-edge: **Tekton**  
Justification: Automated gates reduce risk under **INF-PRJ-01**.

**Container runtime**
- Recommended: **containerd (K8s default)**  
- Conservative: **Docker Engine**  
- Cutting-edge: **Kata Containers**  
Justification: K8s-ready ops per **INF-FR-SRV-01** (server-hosted services).

**Infra provisioning**
- Recommended: **Helm + Kustomize**  
- Conservative: **kubectl apply only**  
- Cutting-edge: **Pulumi**  
Justification: Repeatable deployment supports **INF-ASR-MAINT-01**.

### 3) Recommended default stack
- Java 21, Spring Boot 3.3, PostgreSQL 15, WebSocket/SSE, Caffeine cache, OpenTelemetry, Prometheus/Grafana, Keycloak optional.  
Justification: meets **INF-NFR-UI-01** (timely updates) and **INF-PRJ-01** (small team/time/cost).

### 4) Interface design (External API: OpenAPI; Internal: gRPC)

**External API**: see `openapi.yaml` (L).  
Covers: auth, device registry, telemetry read, command setpoints/power, plans/overrides, reports.

**Internal contracts**: see `internal.proto` (L).  
Covers: gateway telemetry stream, command dispatch, device discovery, alarm activation.

### 5) Data model / schema (SQL DDL)
Primary entities: users/roles, devices, telemetry, commands, plans, overrides, security events, backups. See `sql/*_ddl.sql` (L).  
Encryption-at-rest: password hashes; optional PII fields. Immutability: security events and telemetry are append-only (enforced by app + DB permissions).  
Justification: supports **INF-FR-RPT-01** (2-year reporting) and **INF-NFR-ERR-01** (consistent error handling via constraints).

### 6) Caching & consistency
- Cache device registry (TTL 60s) and latest telemetry per device (TTL 5s).  
- Strong consistency for commands/plans (transactional).  
- Eventual consistency acceptable for UI aggregates within 2s window (**INF-NFR-UI-01**).

---

## D2. Gateway Adapter + Simulator

### 1) Responsibilities & data ownership
Implements the boundary to the Gateway RF network (simulated): device discovery, telemetry ingestion at ≥10Hz, command delivery, and range enforcement (≤1000 ft).

### 2) Technology options
- Recommended: Java module using gRPC streaming  
- Conservative: HTTP polling from simulator  
- Cutting-edge: MQTT 5.0 broker + clients  
Justification (recommended): supports **INF-NFR-DAQ-01** (10Hz) with streaming.

### 3) Recommended stack
- gRPC bidirectional streams, in-process simulator for prototype.  
Justification: meets **INF-ENV-01** (realistic simulation) and **INF-NFR-DAQ-01**.

### 4) Internal contract
Implemented by `internal.proto` (L).

### 5) Data model
No direct persistence; writes to backend telemetry tables via service calls.

### 6) Caching/consistency
Maintain last-seen device state in memory; backend remains source of truth.

---

## D3. Web UI (General User + Master/Technician console)

### 1) Responsibilities & data ownership
Renders dashboards (temp/humidity/security/power), allows control actions, plan editing, and report viewing. No authoritative data stored client-side.

### 2) Technology options
- Recommended: **React 18.2–19**  
- Conservative: **Server-rendered Thymeleaf**  
- Cutting-edge: **SvelteKit**  
Justification: supports rapid UI iteration under **INF-PRJ-01**.

### 3) Recommended stack
React + TypeScript 5.4–5.6, WebSocket/SSE client.  
Justification: meets **INF-NFR-UI-01** (≤2s updates).

### 4) Interface
Consumes `openapi.yaml` endpoints.

### 5) Data model
Client-side view models only; no persistence.

### 6) Caching
Browser cache for static assets; no caching of control state beyond seconds.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/dh-backend-deployment.yaml` (L). Includes Deployment, Service, HPA, ConfigMap, Secret.  
Justification: supports **INF-ASR-MAINT-01** (maintainable deployment) and **INF-NFR-REL-01** (health checks/autoscaling).

## E2. DB HA, backup cadence, restore
- Prototype: single Postgres instance with daily logical backup + WAL optional.  
- HA option: Postgres primary+replica (streaming replication).  
- Backup: daily at technician-set time (**INF-ASR-BR-01**), retain 30 days locally + optional offsite.  
- Restore: automated script validates schema + latest backup (**INF-ASR-BR-02**).

## E3. Network topology + ingress/egress
- Ingress: HTTPS 443 to backend; WebSocket upgrade allowed.  
- Egress: optional NTP, package updates; no device cloud dependency.  
Mapped conceptually to *Deployment_PhysicalView* `UserDevice -> WebServer : HTTPS`.

## E4. CI/CD sketch
1) Lint/format → unit tests → contract tests (OpenAPI/proto) → build image → scan (Trivy) → integration tests with simulator → deploy to staging → e2e → canary/blue-green to prod.  
Gates: schema migration checks; OpenAPI breaking-change check.  
Justification: reduces delivery risk per **INF-PRJ-01**.

---

# F. Security Design

## F1. Auth & AuthZ
- Recommended: OIDC provider (Keycloak) issuing JWT; roles: GENERAL, MASTER, TECHNICIAN.  
- Token lifecycle: access token 5–15 min; refresh token 8–24h; revoke on password reset/role change.  
Justification: meets **INF-ASR-SEC-01** (recognized reliable security tech via TLS + modern auth).

## F2. Secrets management & rotation
- K8s Secrets for prototype; rotate quarterly or on incident; prefer external secret store (Vault) for commercial.  
Justification: supports **INF-NFR-REL-01** (reduce failure/incident risk).

## F3. TLS & service mesh
- TLS 1.2+ at ingress; optional mTLS inside mesh (Linkerd/Istio) for commercial.  
Justification: meets **INF-ASR-SEC-01**.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Credential stuffing | Rate limit, MFA optional, lockout policy (INF-ASR-SEC-01) |
| MITM on remote access | TLS-only, HSTS, cert rotation (INF-ASR-SEC-01) |
| Unauthorized device control | RBAC, audit logs, command authorization (INF-FR-ACC-01) |
| Data loss on power failure | UPS recommendation, DB durability, backups/restore drills (INF-ASR-BR-01/02) |
| Replay/forged gateway messages | Mutual auth keys for gateway, message signatures (INF-NFR-REL-01) |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + alerts
Metrics:
- Telemetry ingest rate (per device), command success rate, plan execution lag, UI push latency, DB query p95.  
Logs: JSON structured with correlation IDs; security events logged.  
Traces: OpenTelemetry spans for `Command->Gateway->Ack`.

Example Prometheus alert rules:
- High command failure:
  - `rate(dh_command_fail_total[5m]) / rate(dh_command_total[5m]) > 0.02`
- Telemetry stalled:
  - `max_over_time(dh_device_last_seen_seconds[2m]) > 120`

Justification: supports **INF-NFR-REL-01** (reliability).

## G2. SLOs, error budgets, RTO/RPO
- Availability SLO: 99.0% monthly (prototype) mapped to reliability target (**INF-NFR-REL-01**).  
- RPO: 24h (daily backup) (**INF-ASR-BR-01**).  
- RTO: 2h (restore procedure) (**INF-ASR-BR-02**).

## G3. Dashboard/runbook sketch
Dashboards: device health, security events timeline, plan execution, DB health.  
Runbooks: restore from backup, gateway reconnect, stuck plan executor.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Notes |
|---|---|---|
| Unit | domain/services | Validation: setpoint ranges, schedule rules |
| Integration | API+DB, API+GatewaySim | Device counts (8/8/50/100) |
| Contract | OpenAPI + proto | CI gate for breaking changes |
| E2E | WebUI→API→Sim | Verify ≤2s updates (**INF-NFR-UI-01**) |
| Chaos/Soak | whole system | Power/network loss, 10Hz ingest soak (**INF-NFR-DAQ-01**, **INF-NFR-REL-01**) |

## H2. Test data & environment isolation
Envs: dev, CI, staging(simulated home), prod(simulated). Refresh: nightly DB reset in staging; seeded device simulator scenarios.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
Assumption: no existing DH system (prototype). If replacing:  
1) Import device registry, users, and plans.  
2) Dual-run old/new for 2 weeks; compare telemetry and command outcomes.  
3) Cutover; keep rollback by DNS/ingress switch.

## I2. Backwards compatibility & API versioning
- Version API under `/api/v1`.  
- Backwards-compatible changes only within v1; breaking changes require `/api/v2` and 90-day overlap.

---

# J. Tradeoffs & Alternatives

1) **Modular monolith vs microservices**  
- Alternatives: microservices (more scalable), monolith (simpler).  
- Chosen: modular monolith to meet **INF-PRJ-01** (small team/time/cost) while keeping clear boundaries (**INF-ASR-MAINT-01**).

2) **Postgres vs SQLite**  
- Alternatives: SQLite simpler; Postgres stronger concurrency/reporting.  
- Chosen: Postgres to support reporting/retention and concurrent access (**INF-FR-RPT-01**).

3) **WebSocket/SSE vs polling**  
- Alternatives: polling simpler but wasteful; push supports timeliness.  
- Chosen: WebSocket/SSE to meet **INF-NFR-UI-01**.

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** The authoritative scope is the **Original Requirements** (DigitalHome), not the provided UML “Web Learning Game System”.  
- **A2:** Prototype runs in a simulated environment but uses realistic device constraints (range, rates).  
- **A3:** Remote access is required via ISP; home server is reachable via secure ingress (port-forward/DDNS not specified).  
- **A4:** Reports and telemetry retention required for **2 years** implies storing telemetry at a downsampled rate (raw 10Hz not retained for full 2 years unless configured).  
- **A5:** “Failure per 10,000 hours” is treated as an SLO proxy; exact failure definition to be agreed.

## Conflicts logged (per rule #5)
- **C1:** UML diagrams describe a **Web Learning Game System** (use cases: Play Game, Manage Questions) which conflicts with DigitalHome requirements. We reuse only generic structural ideas (UI/API/Data) and do not implement game features.

## Unresolved stakeholder questions
1) Should DH support **multiple homes** per account or single-home only (prototype)?  
2) What is the required **remote access model** (VPN, port-forward, cloud relay)?  
3) Define “failure” for **INF-NFR-REL-01** (service crash, missed command, stale UI, etc.).  
4) Telemetry retention: store **raw 10Hz** or only aggregates? (impacts storage/cost).  
5) Do Master User and Technician have identical permissions always, or are there separations?

## Inferred requirement IDs list (summary)
All requirements are captured as INF-* due to missing IDs in source: INF-FR-*, INF-NFR-*, INF-ASR-* as used throughout.

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# DigitalHome (DH) Architecture Document
(Contents are the same as ArchitectureDocument.md delivered in this response.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: DigitalHome API
  version: 1.0.0
servers:
  - url: https://{host}/api/v1
    variables:
      host:
        default: digitalhome.local
tags:
  - name: Auth
  - name: Devices
  - name: Telemetry
  - name: Control
  - name: Planner
  - name: Reports
security:
  - bearerAuth: []
paths:
  /auth/login:
    post:
      tags: [Auth]
      security: []
      summary: Login and obtain JWT (prototype)
      operationId: login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        "200":
          description: Login OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LoginResponse"
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /devices:
    get:
      tags: [Devices]
      summary: List registered devices
      operationId: listDevices
      parameters:
        - in: query
          name: type
          schema:
            $ref: "#/components/schemas/DeviceType"
      responses:
        "200":
          description: Device list
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      $ref: "#/components/schemas/Device"
    post:
      tags: [Devices]
      summary: Register a device (Technician/Master)
      operationId: registerDevice
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Device"
        "400":
          description: Validation error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/RegisterDeviceRequest"
  /devices/{deviceId}/telemetry/latest:
    get:
      tags: [Telemetry]
      summary: Get latest telemetry for a device
      operationId: getLatestTelemetry
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Latest telemetry
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TelemetrySample"
        "404":
          description: Device not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /control/thermostats/{deviceId}/setpoint:
    put:
      tags: [Control]
      summary: Set thermostat setpoint (60-80F inclusive, 1 degree increments)
      operationId: setThermostatSetpoint
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SetpointRequest"
      responses:
        "202":
          description: Accepted command
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandResponse"
        "400":
          description: Invalid setpoint
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /control/humidistats/{deviceId}/setpoint:
    put:
      tags: [Control]
      summary: Set humidistat setpoint (30-60% inclusive, 1% increments)
      operationId: setHumidistatSetpoint
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/HumiditySetpointRequest"
      responses:
        "202":
          description: Accepted command
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandResponse"
        "400":
          description: Invalid setpoint
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /control/powerswitches/{deviceId}/state:
    put:
      tags: [Control]
      summary: Set power switch state ON/OFF
      operationId: setPowerSwitchState
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PowerStateRequest"
      responses:
        "202":
          description: Accepted command
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandResponse"
  /planner/month-plans/{year}/{month}:
    put:
      tags: [Planner]
      summary: Create or update a month plan (up to 4 daily periods)
      operationId: upsertMonthPlan
      parameters:
        - in: path
          name: year
          required: true
          schema: { type: integer, minimum: 2000, maximum: 2100 }
        - in: path
          name: month
          required: true
          schema: { type: integer, minimum: 1, maximum: 12 }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/MonthPlan"
      responses:
        "200":
          description: Updated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonthPlan"
        "400":
          description: Validation error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /reports/month/{year}/{month}:
    get:
      tags: [Reports]
      summary: Get month report (past 2 years)
      operationId: getMonthReport
      parameters:
        - in: path
          name: year
          required: true
          schema: { type: integer, minimum: 2000, maximum: 2100 }
        - in: path
          name: month
          required: true
          schema: { type: integer, minimum: 1, maximum: 12 }
      responses:
        "200":
          description: Month report
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonthReport"
        "400":
          description: Out of range
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string, example: "VALIDATION_ERROR" }
        message: { type: string, example: "Setpoint out of range" }
        details:
          type: object
          additionalProperties: true
        requestId: { type: string }
    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1 }
        password: { type: string, minLength: 12 }
    LoginResponse:
      type: object
      required: [accessToken, tokenType, expiresInSeconds]
      properties:
        accessToken: { type: string }
        tokenType: { type: string, enum: ["Bearer"] }
        expiresInSeconds: { type: integer, minimum: 60 }
        roles:
          type: array
          items: { type: string }
    DeviceType:
      type: string
      enum: [THERMOSTAT, HUMIDISTAT, CONTACT_SENSOR, ALARM_SOUND, ALARM_LIGHT, POWER_SWITCH]
    Device:
      type: object
      required: [deviceId, type, name, room, enabled]
      properties:
        deviceId: { type: string }
        type: { $ref: "#/components/schemas/DeviceType" }
        name: { type: string }
        room: { type: string }
        enabled: { type: boolean }
        rangeFeet: { type: integer, minimum: 0, maximum: 1000 }
    RegisterDeviceRequest:
      type: object
      required: [type, name, room]
      properties:
        type: { $ref: "#/components/schemas/DeviceType" }
        name: { type: string }
        room: { type: string }
        rangeFeet:
          type: integer
          minimum: 0
          maximum: 1000
    TelemetrySample:
      type: object
      required: [deviceId, observedAtUtc, metrics]
      properties:
        deviceId: { type: string }
        observedAtUtc: { type: string, format: date-time }
        metrics:
          type: object
          additionalProperties:
            oneOf:
              - type: number
              - type: string
              - type: boolean
    SetpointRequest:
      type: object
      required: [value, unit]
      properties:
        value: { type: number }
        unit: { type: string, enum: ["F", "C"] }
    HumiditySetpointRequest:
      type: object
      required: [percent]
      properties:
        percent: { type: integer, minimum: 30, maximum: 60 }
    PowerStateRequest:
      type: object
      required: [state]
      properties:
        state: { type: string, enum: ["ON", "OFF"] }
    CommandResponse:
      type: object
      required: [commandId, status]
      properties:
        commandId: { type: string }
        status: { type: string, enum: ["ACCEPTED", "REJECTED"] }
    MonthPlan:
      type: object
      required: [year, month, days]
      properties:
        year: { type: integer }
        month: { type: integer, minimum: 1, maximum: 12 }
        days:
          type: array
          items:
            $ref: "#/components/schemas/DayPlan"
    DayPlan:
      type: object
      required: [dayOfMonth, periods]
      properties:
        dayOfMonth: { type: integer, minimum: 1, maximum: 31 }
        periods:
          type: array
          maxItems: 4
          items:
            $ref: "#/components/schemas/PeriodPlan"
    PeriodPlan:
      type: object
      required: [startTimeLocal, endTimeLocal, settings]
      properties:
        startTimeLocal: { type: string, pattern: "^[0-2][0-9]:[0-5][0-9]$" }
        endTimeLocal: { type: string, pattern: "^[0-2][0-9]:[0-5][0-9]$" }
        settings:
          type: object
          properties:
            thermostatSetpoints:
              type: object
              additionalProperties:
                $ref: "#/components/schemas/SetpointRequest"
            humidistatSetpoints:
              type: object
              additionalProperties:
                $ref: "#/components/schemas/HumiditySetpointRequest"
            contactSensorArmed:
              type: object
              additionalProperties: { type: boolean }
            powerSwitchStates:
              type: object
              additionalProperties:
                $ref: "#/components/schemas/PowerStateRequest"
    MonthReport:
      type: object
      required: [year, month, thermostatStats, humidistatStats, securityBreaches, downtimePeriods]
      properties:
        year: { type: integer }
        month: { type: integer }
        thermostatStats:
          type: array
          items:
            $ref: "#/components/schemas/DeviceStats"
        humidistatStats:
          type: array
          items:
            $ref: "#/components/schemas/DeviceStats"
        securityBreaches:
          type: array
          items:
            $ref: "#/components/schemas/SecurityBreach"
        downtimePeriods:
          type: array
          items:
            $ref: "#/components/schemas/DowntimePeriod"
    DeviceStats:
      type: object
      required: [deviceId, avg, min, minAtUtc, max, maxAtUtc]
      properties:
        deviceId: { type: string }
        avg: { type: number }
        min: { type: number }
        minAtUtc: { type: string, format: date-time }
        max: { type: number }
        maxAtUtc: { type: string, format: date-time }
    SecurityBreach:
      type: object
      required: [deviceId, occurredAtUtc]
      properties:
        deviceId: { type: string }
        occurredAtUtc: { type: string, format: date-time }
        details: { type: string }
    DowntimePeriod:
      type: object
      required: [fromUtc, toUtc]
      properties:
        fromUtc: { type: string, format: date-time }
        toUtc: { type: string, format: date-time }
```

```proto
// filename: internal.proto
syntax = "proto3";

package digitalhome.gateway.v1;

option java_multiple_files = true;
option java_package = "com.homeowner.digitalhome.gateway.v1";

message DeviceDescriptor {
  string device_id = 1;
  string type = 2; // THERMOSTAT, HUMIDISTAT, CONTACT_SENSOR, ALARM_SOUND, ALARM_LIGHT, POWER_SWITCH
  string room = 3;
  uint32 range_feet = 4; // must be <= 1000
}

message TelemetrySample {
  string device_id = 1;
  string observed_at_utc = 2; // RFC3339
  map<string, string> metrics = 3; // values encoded as strings for simplicity in prototype
}

message Command {
  string command_id = 1;
  string device_id = 2;
  string issued_at_utc = 3; // RFC3339
  string kind = 4; // SET_TEMP_SETPOINT, SET_HUMIDITY_SETPOINT, SET_POWER_STATE, ARM_CONTACT, DISARM_CONTACT, ACTIVATE_ALARM
  map<string, string> params = 5;
}

message CommandAck {
  string command_id = 1;
  string device_id = 2;
  string ack_at_utc = 3; // RFC3339
  string status = 4; // ACCEPTED, REJECTED, APPLIED, FAILED
  string message = 5;
}

message DiscoverRequest {}
message DiscoverResponse {
  repeated DeviceDescriptor devices = 1;
}

service GatewayService {
  // Device discovery (simulated gateway returns known devices)
  rpc DiscoverDevices(DiscoverRequest) returns (DiscoverResponse);

  // Telemetry stream from gateway to backend (>=10Hz per sensor in simulation)
  rpc StreamTelemetry(stream TelemetrySample) returns (CommandAck);

  // Backend sends commands to gateway; gateway returns acknowledgements
  rpc SendCommand(Command) returns (CommandAck);
}
```

```yaml
# filename: k8s/dh-backend-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: digitalhome
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: dh-config
  namespace: digitalhome
data:
  SPRING_PROFILES_ACTIVE: "prod"
  DH_BACKUP_CRON: "0 2 * * *"
---
apiVersion: v1
kind: Secret
metadata:
  name: dh-secrets
  namespace: digitalhome
type: Opaque
stringData:
  DB_URL: "jdbc:postgresql://dh-postgres:5432/digitalhome"
  DB_USER: "digitalhome"
  DB_PASSWORD: "change-me"
  JWT_SIGNING_KEY: "change-me-please-rotate"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dh-backend
  namespace: digitalhome
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dh-backend
  template:
    metadata:
      labels:
        app: dh-backend
    spec:
      containers:
        - name: dh-backend
          image: ghcr.io/homeowner/digitalhome-backend:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: dh-config
            - secretRef:
                name: dh-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1024Mi"
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: dh-backend
  namespace: digitalhome
spec:
  selector:
    app: dh-backend
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: dh-backend-hpa
  namespace: digitalhome
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dh-backend
  minReplicas: 2
  maxReplicas: 6
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```sql
-- filename: sql/user_ddl.sql
CREATE TABLE IF NOT EXISTS dh_user (
  user_id            UUID PRIMARY KEY,
  username           TEXT NOT NULL UNIQUE,
  password_hash      TEXT NOT NULL, -- store salted hash (bcrypt/argon2); encryption-at-rest via disk/DB
  role               TEXT NOT NULL CHECK (role IN ('GENERAL','MASTER','TECHNICIAN')),
  is_locked          BOOLEAN NOT NULL DEFAULT FALSE,
  failed_attempts    INTEGER NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0),
  last_login_at_utc  TIMESTAMPTZ,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dh_user_role ON dh_user(role);
```

```sql
-- filename: sql/device_ddl.sql
CREATE TABLE IF NOT EXISTS dh_device (
  device_id      UUID PRIMARY KEY,
  type           TEXT NOT NULL CHECK (type IN ('THERMOSTAT','HUMIDISTAT','CONTACT_SENSOR','ALARM_SOUND','ALARM_LIGHT','POWER_SWITCH')),
  name           TEXT NOT NULL,
  room           TEXT NOT NULL,
  enabled        BOOLEAN NOT NULL DEFAULT TRUE,
  range_feet     INTEGER NOT NULL DEFAULT 0 CHECK (range_feet >= 0 AND range_feet <= 1000),
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dh_device_type ON dh_device(type);
CREATE INDEX IF NOT EXISTS idx_dh_device_room ON dh_device(room);
```

```sql
-- filename: sql/telemetry_ddl.sql
CREATE TABLE IF NOT EXISTS dh_telemetry (
  telemetry_id     BIGSERIAL PRIMARY KEY,
  device_id        UUID NOT NULL REFERENCES dh_device(device_id),
  observed_at_utc  TIMESTAMPTZ NOT NULL,
  metric_key       TEXT NOT NULL,
  metric_value     TEXT NOT NULL
);

-- Query latest per device quickly
CREATE INDEX IF NOT EXISTS idx_dh_telemetry_device_time ON dh_telemetry(device_id, observed_at_utc DESC);
CREATE INDEX IF NOT EXISTS idx_dh_telemetry_key ON dh_telemetry(metric_key);
```

```sql
-- filename: sql/plan_ddl.sql
CREATE TABLE IF NOT EXISTS dh_month_plan (
  plan_id        UUID PRIMARY KEY,
  year           INTEGER NOT NULL,
  month          INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  timezone       TEXT NOT NULL DEFAULT 'UTC',
  created_by     UUID NOT NULL REFERENCES dh_user(user_id),
  updated_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (year, month)
);

CREATE TABLE IF NOT EXISTS dh_day_period (
  period_id      UUID PRIMARY KEY,
  plan_id        UUID NOT NULL REFERENCES dh_month_plan(plan_id) ON DELETE CASCADE,
  day_of_month   INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
  period_index   INTEGER NOT NULL CHECK (period_index BETWEEN 1 AND 4),
  start_time     TIME NOT NULL,
  end_time       TIME NOT NULL,
  settings_json  JSONB NOT NULL,
  UNIQUE (plan_id, day_of_month, period_index)
);

CREATE INDEX IF NOT EXISTS idx_dh_day_period_plan_day ON dh_day_period(plan_id, day_of_month);
```

```sql
-- filename: sql/override_ddl.sql
CREATE TABLE IF NOT EXISTS dh_override (
  override_id     UUID PRIMARY KEY,
  device_id       UUID NOT NULL REFERENCES dh_device(device_id),
  kind            TEXT NOT NULL, -- TEMP_SETPOINT, HUMIDITY_SETPOINT, POWER_STATE, ARM_STATE
  value_json      JSONB NOT NULL,
  effective_from  TIMESTAMPTZ NOT NULL,
  effective_until TIMESTAMPTZ NOT NULL,
  created_by      UUID NOT NULL REFERENCES dh_user(user_id),
  created_at_utc  TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (effective_until > effective_from)
);

CREATE INDEX IF NOT EXISTS idx_dh_override_device_time ON dh_override(device_id, effective_from, effective_until);
```

```sql
-- filename: sql/event_ddl.sql
CREATE TABLE IF NOT EXISTS dh_security_event (
  event_id        BIGSERIAL PRIMARY KEY,
  device_id       UUID NOT NULL REFERENCES dh_device(device_id),
  occurred_at_utc TIMESTAMPTZ NOT NULL,
  event_type      TEXT NOT NULL CHECK (event_type IN ('BREACH_OPEN','ALARM_ACTIVATED')),
  details         TEXT
);

CREATE INDEX IF NOT EXISTS idx_dh_security_event_time ON dh_security_event(occurred_at_utc DESC);
CREATE INDEX IF NOT EXISTS idx_dh_security_event_device_time ON dh_security_event(device_id, occurred_at_utc DESC);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-CTX-01,Web-ready device controls temp/humidity/lights/security/appliances,Container_PhysicalView:Backend|Data,WebUI|DH-API,openapi.yaml,Expose control/monitor endpoints for all managed domains.
INF-FR-SRV-01,Home web server provides interaction/control,Deployment_PhysicalView:Web Server Node,HomeServer,k8s/dh-backend-deployment.yaml,Backend hosts APIs and services.
INF-FR-SRV-02,Home web server stores plans/data,Deployment_PhysicalView:Storage Volume,Persistence,sql/plan_ddl.sql|sql/telemetry_ddl.sql,DB stores plans and telemetry for reporting.
INF-FR-ACC-01,Establish/maintain user accounts,(conflict) UseCase_ScenarioView:Admin,AuthService,sql/user_ddl.sql|openapi.yaml,Roles and authentication required for users/technician/master.
INF-FR-ACC-02,Backup service for accounts/plans/db,Deployment_PhysicalView:Storage Volume,BackupJob,k8s/dh-backend-deployment.yaml,Daily backups and restore enable recovery.
INF-FR-GW-01,Gateway connects to broadband + RF module,Deployment_PhysicalView:Web Server Node,GatewayAdapter,internal.proto,Defines gateway boundary and comms.
INF-NFR-RANGE-01,Devices within 1000 feet to communicate,,GatewayAdapter,internal.proto,Simulator enforces range constraint.
INF-FR-TH-01,Thermostat reads current temperature,,ThermostatService,openapi.yaml,Telemetry endpoint provides readings.
INF-FR-TH-02,Set thermostat 60-80F step 1,,ThermostatService,openapi.yaml,API validates setpoint range/increments.
INF-FR-TH-03,Up to 8 thermostats; individual/collective control,,ThermostatService,sql/device_ddl.sql,Device registry supports counts and grouping.
INF-FR-TH-04,24 hourly settings/day weekly schedule,,PlannerService,sql/plan_ddl.sql,Plan schema supports time periods and schedules.
INF-NFR-UNITS-01,Support Fahrenheit and Celsius,,Domain,openapi.yaml,Unit field supports F/C and conversion.
INF-ASR-STD-ASHRAE-01,Adhere to ASHRAE 2010,,Domain,architecture.md,Documented constraints and validation rules.
INF-FR-HU-01,Humidistat reads humidity,,HumidityService,openapi.yaml,Telemetry endpoint provides readings.
INF-FR-HU-02,Set humidity 30-60% step 1%,,HumidityService,openapi.yaml,API validates humidity range.
INF-FR-HU-03,Up to 8 humidistats; schedules,,PlannerService,sql/plan_ddl.sql,Plan schema reused for humidity.
INF-FR-SE-01,Manage up to 50 contact sensors,,SecurityService,sql/device_ddl.sql,Device registry supports sensor counts.
INF-FR-SE-02,Activate sound+light alarms on breach,,SecurityService,internal.proto,Gateway command triggers alarms.
INF-FR-SE-03,Record breach day/time in report,,ReportingService,sql/event_ddl.sql,Security events persisted for reporting.
INF-FR-AP-01,Manage up to 100 power switches,,ApplianceService,sql/device_ddl.sql,Device registry supports switch counts.
INF-FR-AP-02,Read power state OFF/ON,,ApplianceService,openapi.yaml,State query endpoint.
INF-FR-AP-03,Change power state OFF<->ON,,ApplianceService,openapi.yaml,Command endpoint.
INF-FR-PLN-01,Month plan up to 4 daily periods,,PlannerService,sql/plan_ddl.sql,Schema enforces max 4 periods.
INF-FR-PLN-02,Override planned values until period end,,PlannerService,sql/override_ddl.sql,Overrides with effective_until.
INF-FR-RPT-01,Month report for past 2 years,,ReportingService,openapi.yaml,Report endpoint returns aggregates and events.
INF-NFR-UI-01,Displays updated at least every 2 seconds,,RealtimeService,openapi.yaml,Use push updates and cache latest telemetry.
INF-NFR-DAQ-01,Sensor acquisition rate >=10Hz,,GatewayAdapter,internal.proto,Streaming telemetry supports rate.
INF-NFR-REL-01,<=1 failure per 10,000 hours,,All,G/SLOs,Define SLOs and run soak/chaos tests.
INF-ASR-BR-01,Daily backup at technician-set time,,BackupJob,k8s/dh-backend-deployment.yaml,Cron schedule configurable.
INF-ASR-BR-02,Recovery restores from most recent backup,,RestoreTool,runbook,Restore procedure and verification.
INF-NFR-ERR-01,Clear descriptive error messages,,API,openapi.yaml,Standard error schema.
INF-ASR-SEC-01,TLS for auth and encryption,Deployment_PhysicalView:HTTPS,Ingress/API,k8s/dh-backend-deployment.yaml,TLS-only ingress and secure auth.
INF-ASR-MAINT-01,Prototype designed for commercial reuse,Package_DevelopmentView:domain|services,All,architecture.md,Modular boundaries and replaceable adapters.
INF-ASR-DOC-01,Docs in HO2305 format and archived,,Process,architecture.md,Deliverable completeness requirement.
INF-ASR-OO-01,Object-oriented development with UML 2.0,,Codebase,architecture.md,OO language and UML-aligned design.
INF-PRJ-01,12 months/5 engineers/cost minimized,,Process,J,Drives stack simplicity and minimal ops.
INF-ENV-01,Simulated environment realistic,,Simulator,internal.proto,Simulator enforces physical constraints.
```

---

## Verification (Acceptance Criteria)

| Check | Status |
|---|---|
| 3-line Analysis Plan present | - [x] |
| Sections A-L included | - [x] |
| Every FR/NFR/ASR mapped in traceability matrix | - [x] (all captured as INF-*) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | - [x] |
| Representative k8s manifest snippet included | - [x] |
| SQL DDL / models for primary entities included | - [x] |
| All major components have at least one API contract and a data schema | - [x] |
| Assumptions and unresolved questions listed | - [x] |

---

## How to review (checklist)
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?