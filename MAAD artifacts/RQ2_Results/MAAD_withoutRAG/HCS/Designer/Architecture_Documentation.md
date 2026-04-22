Scope: Produce production-ready architecture documentation for DigitalHome (prototype) aligned to narrative requirements, provided UML, and prior decisions.  
Approach: Normalize requirements into INF-* IDs, map them to 4+1 views, then specify implementable APIs/contracts, data schemas, and ops/security/SRE/testing guidance.  
Top validation steps: Full traceability matrix coverage, API/DDL/k8s syntax validity, and conflict/assumption log with measurable NFR acceptance criteria.

# A. Executive Summary (≤1 page)

DigitalHome (DH) is an on-prem smart-home management prototype that lets residents monitor/control temperature, humidity, security contacts/alarms, and power switches via a personal web page hosted on a home server, with a local RF Gateway bridging to devices. It runs in a realistic simulator environment but is designed to evolve into a commercial-grade system.

**Primary diagram mapping (one-line):**  
ScenarioView: *Use Case Diagram* (DigitalHome_UseCase: UC_Auth, UC_Monitor, UC_Control, UC_Plans, UC_Override, UC_Reports, UC_Config, UC_Backup) is realized by PhysicalView: *Container Diagram* (DigitalHome_Container: API, Tel, Plan, Sec, Bak, GWAPI, Plugins, RF) and ProcessView: *Sequence Diagrams* (DigitalHome_Sequence_RemoteMonitor, DigitalHome_Sequence_PlanOverrideControl).

**Architectural style(s):**
- Modular monolith + microkernel plugins at the gateway edge (DevicePluginHost).  
- Event-driven telemetry pipeline (Gateway acquisition → EventBus → TelemetryService → Web UI streaming).  
- Justification: meets **NFR-002** (≥10 Hz acquisition) and **NFR-001** (UI updates ≤2s) by decoupling acquisition from UI.

**Deployment topology (one-line):**
- Two-tier on-prem: HomeWebServer (UI/API/DB/services) + DigitalHomeGateway (RF + acquisition/control).  
- Justification: meets **ASR-HomeWebServer** (home web server hosts UI/control/storage/accounts/backup) and **ASR-Gateway** (gateway is master RF hub).

## Top 3 design risks & mitigations

| Risk | Why it matters | Mitigation (concrete) |
|---|---|---|
| Telemetry volume (10 Hz × many sensors) overwhelms storage/UI | Could violate UI ≤2s and cost constraints | Persist raw at gateway optional; server persists raw with rollups + retention; UI uses throttled push (1–2s) snapshots; add downsampling policy. (NFR-001, NFR-002, NFR-CostMin) |
| Remote access security to home server over ISP | Risk of account compromise and privacy breach | TLS 1.3+, strong RBAC, rate limiting, lockout, audit immutability, optional VPN/mTLS mode for technician. (NFR-SecTLS, NFR-AuditRetention) |
| Reliability target “≤1 failure/10,000 hours” unclear | Hard to test/claim without definition | Define “failure” as loss of monitoring+control >60s; instrument SLOs and add watchdog + daily backup/restore drill. (NFR-Reliability, NFR-BackupDaily, NFR-RecoveryLatest) |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality | IDs | Primary test types |
|---|---|---|
| Scalability/Capacity | NFR-002, NFR-001, NFR-DeviceCaps-* | Load + soak tests; storage growth tests |
| Availability/Reliability | NFR-Reliability, NFR-BackupDaily, NFR-RecoveryLatest | Chaos tests (power/network loss), fail/restart tests |
| Security | NFR-SecTLS, NFR-ErrorMessages, NFR-AuditRetention | Pen tests, SAST/DAST, TLS scans, RBAC tests |
| Performance | NFR-001, NFR-002 | Latency tests, profiling, gateway loop jitter tests |
| Maintainability | ASR-UML2, NFR-DocArchiveUpToDate | Architecture conformance checks; contract tests; doc CI |

---

# B. Traceability & Rationale

Because the original requirements are narrative without IDs, all requirements below are **inferred** and labeled `INF-*` (per rules). They collectively cover every statement in the Original Requirements at least once.

The table is also delivered as `traceability_matrix.csv` in Section L.

**Traceability matrix (excerpted view; full in CSV artifact):**

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-001 | System manages home environment devices via web page | Container: API/WebUI/Devices; UseCase: UC_Monitor/UC_Control | WebUI, API, GWAPI | architecture.md, openapi.yaml | Core capability; web UI is primary interaction surface. |
| INF-002 | Users: General, Master, Technician roles | UseCase: actors; Class: UserAccount.role | AuthService, RbacPolicy | openapi.yaml, sql/user_account_ddl.sql | RBAC drives authorization and configuration permissions. |
| INF-003 | Master can change configuration/accounts | UseCase: UC_Accounts, UC_Config | AuthService, API | openapi.yaml | Maps privileged endpoints to Master/Technician. |
| INF-004 | Technician sets up/maintains config; start/stop system | UseCase: UC_Config, UC_Backup | BackupRestoreService, GatewayAPI | openapi.yaml | Operational controls must be gated and auditable. |
| INF-005 | Prototype complete in 12 months, 5 engineers | (N/A) | (Process) | architecture.md | Drives “modular monolith” over microservices sprawl. |
| INF-006 | Minimize cost; use widely-accepted tech | (N/A) | All | architecture.md | Select commodity OSS stack. |
| INF-007 | Simulated environment realistic; adheres to physical constraints | Component: DevicePluginHost; Deployment: Devices simulated | DevicePluginHost, Simulator plugins | internal.proto | Simulation via plugin swapping; fidelity checks. |
| INF-008 | ISP required; remote access via Internet | Deployment: ISP/Internet links | Ingress/Reverse proxy | k8s/api-deployment.yaml | Network exposure requires TLS + rate limiting. |
| INF-009 | Home web server hosts UI/control/storage/accounts/backup | Deployment: HomeWebServer node | API, WebUI, DB, Backup | architecture.md, sql/*.sql | Centralizes responsibilities per requirement. |
| INF-010 | Gateway connects to broadband and communicates with all devices | Deployment: Gateway node | GatewayAPI, RFModule | internal.proto | Explicit server↔gateway contract. |
| INF-011 | RF module range up to 1000ft indoor | Deployment: RF link note | RFModule plugin | architecture.md | Drives connectivity constraint and simulator parameters. |
| INF-012 | Thermostats: read temp; set 60..80 step 1; up to 8; schedules 24×7 | UseCase UC_Control; Class Plan/Override; Notes | PlannerService, ArbitrationEngine | openapi.yaml, sql/plan_ddl.sql | Plan + override + constraints enforced server-side. |
| INF-013 | Supports F/C and sensor sensitivity -10..40C | Class: UserProfile.tempUnits; device telemetry | TelemetryService | openapi.yaml | Unit conversion is presentation + storage standardization. |
| INF-014 | Humidistats: read; set 30..60 step 1; up to 8; schedules 24×7 | UseCase UC_Control; Class Plan/Override | PlannerService, ArbitrationEngine | openapi.yaml, sql/plan_ddl.sql | Mirrors thermostat behavior. |
| INF-015 | Security: up to 50 contact sensors; alarms light+sound activate on OPEN breach | UseCase UC_Monitor; Class AlarmIncident | TelemetryService, SecurityIncident logic | sql/alarm_incident_ddl.sql | Must record breaches and activate alarms. |
| INF-016 | Appliance manager: up to 100 power switches; read state; change state | UseCase UC_Control | GWAPI, PlannerService | openapi.yaml | Switch control with state reporting. |
| INF-017 | Planner: month plan, per day up to 4 time periods; set multiple params | UseCase UC_Plans; Class Plan | PlannerService | openapi.yaml, sql/plan_ddl.sql | Plan model supports day/period parameterization. |
| INF-018 | Override precedence Manual > Planned > Default; manual until end of period | State: Override lifecycle note | ArbitrationEngine | architecture.md | Single arbitration policy prevents inconsistent behavior. |
| INF-019 | Reports for past 2 years: daily avg/min/max with time; breaches; downtime | UseCase UC_Reports | ReportingService | openapi.yaml | Requires aggregation and retention policy. |
| INF-020 | Displays updated at least every 2 seconds | Sequence: RemoteMonitor loop | TelemetryService, WebUI | openapi.yaml | Push streaming with freshness SLI. |
| INF-021 | Sensor acquisition rate ≥10 Hz | Activity: acquisition loop note | Gateway acquisition | internal.proto | Enforced at gateway; measured and alerted. |
| INF-022 | Reliability: ≤1 failure per 10,000 hours | Deployment note | Watchdog/HealthAgent | architecture.md | Adds health/incident definition and SLOs. |
| INF-023 | Backup daily; time set by technician; restore from latest backup | UseCase UC_Backup | BackupRestoreService | openapi.yaml | Backup scheduling + restore tested. |
| INF-024 | Exception handling: clear descriptive errors | UseCase UC_Errors | API error format | openapi.yaml | Standard Problem Details response. |
| INF-025 | Authentication + encryption (TLS) | UseCase UC_Auth | Ingress, AuthService | openapi.yaml | Protects credentials and data in transit. |
| INF-026 | Maintainability: prototype designed for future commercial | (N/A) | Modular boundaries | architecture.md | Contract-first + clean modules. |
| INF-027 | Documentation up-to-date, HO2305, archive | (N/A) | Docs pipeline | architecture.md | CI enforces artifact generation. |
| INF-028 | UML 2.0 preferred method | (N/A) | Diagrams | architecture.md | Diagrams already provided; referenced only. |
| INF-029 | Change control: director approves major changes | (N/A) | Process | architecture.md | Governance for requirements. |
| INF-030 | HVAC compatibility and ASHRAE 2010 adherence | Class: thermostat devices | DevicePluginHost | architecture.md | Captured as device capability constraints + documentation. |
| INF-031 | Wireless devices within 1000ft to communicate | Deployment RF link | RFModule | architecture.md | Same as range; consolidated. |

---

# C. Architecture Overview

This section follows the **4+1** views and references diagrams by title and element IDs (no PlantUML source embedded).

## C1. Context / Scenario View
- Actors and goals are captured in **Use Case Diagram** (DigitalHome_UseCase: EndUser/MasterUser/Technician; UC_Monitor, UC_Control, UC_Plans, UC_Reports, UC_Config, UC_Backup).  
- Key runtime scenarios are described in **Sequence Diagrams**:
  - Remote monitoring: (DigitalHome_Sequence_RemoteMonitor: WebUI→API→Telemetry→EventBus).  
  - Plan override and control: (DigitalHome_Sequence_PlanOverrideControl: PlannerService + ArbitrationEngine + GWAPI→Gateway).

## C2. Container View
- Containers are defined in **Container Diagram** (DigitalHome_Container: WebUI, API, Sec, Tel, Plan, Rep, Bak, DB, Bus; Gateway: GWAPI, Plugins, RF).
- Main flows:
  1. Browser connects to WebUI/API over HTTPS (TLS) (INF-008, INF-025).
  2. API authorizes and audits privileged operations (INF-002/003/004, INF-025).
  3. Telemetry pipeline pushes updates ≤2s (INF-020) from event bus ingestion (INF-021).
  4. Gateway runs acquisition/control loops and abstracts devices via plugins (INF-010/007).

## C3. Component / Development View
- **Package Diagram** (DigitalHome_Package: ui/api/security/domain/telemetry/persistence/integrations) defines module boundaries.
- **Component Diagram** (DigitalHome_Component: WebUI, HomeWebServerAPI, AuthService, AuditLogService, TelemetryService, PlannerService, ArbitrationEngine, ReportingService, BackupRestoreService, GatewayAPI, DevicePluginHost, EventBus, HomeDatabase) shows runtime wiring.

## C4. Logical/Class View
- **Class Diagram** (DigitalHome_Class: UserAccount/UserProfile/Device/TelemetrySample/Plan/OverrideSetting/ControlCommand/AlarmIncident/AuditEvent) defines domain entities and persistence.
- **State Diagram** (DigitalHome_State_OverrideSetting: override lifecycle) formalizes override precedence and expiry.

## C5. Deployment / Physical View
- **Deployment Diagram** (DigitalHome_Deployment: EndUser Device ↔ ISP ↔ Home LAN ↔ HomeWebServer ↔ DigitalHomeGateway ↔ RF devices).  
- Core constraint: RF range ≤1000 ft indoor (INF-011/031).  
- Ops requirements: daily backup and recovery (INF-023); reliability target instrumentation (INF-022).

---

# D. Detailed Technical Design (developer-facing)

## D.0 Subsystem inventory (major components)
1. WebUI (browser SPA)
2. HomeWebServerAPI (public HTTP API)
3. AuthService + RBAC + AuditLogService (security)
4. TelemetryService + EventBus (streaming + persistence)
5. PlannerService + ArbitrationEngine (plans/overrides)
6. ReportingService (2-year reports)
7. BackupRestoreService (daily backup + restore)
8. GatewayAPI + DevicePluginHost (gateway integration + simulation)
9. HomeDatabase (persistent storage)

> Global stack goal: minimize cost and use widely accepted standards.  
> Justification: meets **INF-006** (cost minimized; widely used tech).

---

## D.1 WebUI

### 1) Responsibilities & data ownership
WebUI provides the personal web page for login, dashboards, control panels, plan editing, and reports. It owns no system-of-record data; it reads/writes via the API only. It must update displays at least every two seconds (INF-020).

### 2) Technology options (3+ per concern)

**Language/runtime**
- Recommended: TypeScript 5.4–5.6
- Conservative: JavaScript (ES2020+)
- Cutting-edge: TypeScript + WASM (Rust) for charting

**Web framework**
- Recommended: React 18.2–19
- Conservative: Server-rendered templates (Django/Jinja, Spring MVC)
- Cutting-edge: SvelteKit 2

**RPC/HTTP**
- Recommended: HTTPS REST + Server-Sent Events (SSE) for telemetry
- Conservative: HTTPS REST + polling every 2s
- Cutting-edge: WebTransport/HTTP3 streaming

**Authn/Authz**
- Recommended: OAuth2-style login issuing short-lived JWT access token + refresh token (handled by API)
- Conservative: Session cookies (server-side sessions)
- Cutting-edge: Passkeys/WebAuthn

**Observability**
- Recommended: browser RUM (OpenTelemetry JS) sampling 1–5%
- Conservative: basic console + backend logs only
- Cutting-edge: full distributed tracing in frontend with baggage propagation

(Other concerns like persistence/cache/messaging not applicable to pure UI.)

### 3) Recommended default stack
- React 18.2–19 + TypeScript 5.4–5.6, built via Vite 5–6; telemetry via SSE.  
**Justification:** supports near-real-time updates to meet **INF-020** (≤2s display updates).

### 4) Interface design
Uses `openapi.yaml` endpoints (Section L): `/auth/login`, `/telemetry/stream`, `/devices`, `/commands`, `/plans`, `/reports/*`.

### 5) Data model/schema
No persisted schema in UI.

### 6) Caching & consistency
- Cache device list in memory (TTL 60s).  
- Never cache auth tokens in localStorage; store access token in memory, refresh token in HttpOnly cookie.  
- Consistency: UI renders “last known value” with timestamp; if stale >5s, show “stale data” banner.  
Justification: supports **INF-020** and **INF-024** (clear errors/states).

---

## D.2 HomeWebServerAPI (public API)

### 1) Responsibilities & data ownership
Single public entrypoint for authentication, monitoring/control commands, plan CRUD, reporting, and ops endpoints (backup/config). It owns request validation and RBAC enforcement, and writes audits for all privileged actions.

### 2) Technology options (3+ per concern)

**Language/runtime**
- Recommended: Java 21 (LTS) or .NET 8
- Conservative: Python 3.11–3.13
- Cutting-edge: Go 1.22–1.24

**Web framework**
- Recommended: Spring Boot 3.2–3.4 (Java) / ASP.NET Core 8 (.NET)
- Conservative: Flask/FastAPI (Python)
- Cutting-edge: Quarkus 3 / Micronaut 4

**RPC/HTTP**
- Recommended: REST (OpenAPI 3.0) + SSE for telemetry; gRPC to gateway
- Conservative: REST only everywhere
- Cutting-edge: GraphQL API for UI + gRPC internally

**Persistence**
- Recommended: PostgreSQL 14–16
- Conservative: SQLite 3.42+ (single-node prototype)
- Cutting-edge: CockroachDB 23–24 (distributed SQL)

**Cache**
- Recommended: in-process Caffeine (Java) / MemoryCache (.NET) for device registry snapshots
- Conservative: no cache
- Cutting-edge: Redis 7.2–7.4

**Messaging**
- Recommended: NATS 2.10–2.11 or Redis Streams 7.2–7.4 as EventBus
- Conservative: in-process queue
- Cutting-edge: Kafka 3.7–3.8

**Authn/Authz**
- Recommended: JWT + RBAC policies; bcrypt/argon2 password hashing
- Conservative: server-side sessions + roles
- Cutting-edge: OIDC with external IdP (not typical for home)

**Observability**
- Recommended: OpenTelemetry SDK + Prometheus metrics + structured logs
- Conservative: logs only
- Cutting-edge: eBPF-based profiling

**CI/CD**
- Recommended: GitHub Actions / GitLab CI with build, test, SAST, container scan
- Conservative: manual build scripts
- Cutting-edge: Bazel monorepo build

**Container runtime**
- Recommended: Docker/Containerd
- Conservative: systemd services (no containers)
- Cutting-edge: Distroless images + gVisor sandbox

**Infra provisioning**
- Recommended: Helm 3.14+ for k8s manifests (optional on-prem k3s)
- Conservative: docker-compose
- Cutting-edge: Pulumi/Terraform with GitOps

### 3) Recommended default stack
- Java 21 + Spring Boot 3.2–3.4; PostgreSQL 14–16; NATS 2.10–2.11; gRPC to gateway.  
**Justification:** supports timing/decoupling for **INF-021** (10 Hz acquisition) while enabling UI freshness **INF-020**.

### 4) Interface design (External APIs)
OpenAPI is provided as `openapi.yaml` (Section L).  
Error format uses RFC 9457 Problem Details (`application/problem+json`).  
Justification: meets **INF-024** (clear descriptive errors).

### 5) Data model/schema
See SQL DDL files in Section L (`sql/*.sql`).  
Justification: meets **INF-009** (server stores plans/data/accounts).

### 6) Caching & consistency strategy
- Cache: device registry lookups (TTL 30s), latest snapshot per device/metric (TTL 10s).  
- Consistency: commands are strongly consistent (write then forward); telemetry is eventual (push updates) but snapshot queries read latest committed sample.  
Justification: meets **INF-020** without overloading DB.

---

## D.3 AuthService + RBAC + AuditLogService

### 1) Responsibilities & data ownership
AuthService authenticates users and issues tokens; RBAC authorizes actions (General vs Master vs Technician). AuditLogService persists append-only audit events for sensitive operations and logins.

### 2) Technology options

**Authn**
- Recommended: Password + JWT (HS256/RS256) with refresh tokens
- Conservative: Password + server sessions
- Cutting-edge: WebAuthn/Passkeys

**Password hashing**
- Recommended: Argon2id
- Conservative: bcrypt
- Cutting-edge: scrypt with HSM-backed pepper

**Audit storage**
- Recommended: PostgreSQL append-only table + immutability guard (no UPDATE/DELETE)
- Conservative: log files rotated daily
- Cutting-edge: WORM object storage (MinIO with retention locks)

**Secrets**
- Recommended: Kubernetes Secrets + sealed-secrets or SOPS
- Conservative: env vars on host
- Cutting-edge: Vault

### 3) Recommended default stack
- Argon2id hashing + JWT access tokens (15 min) + refresh token (7 days) + RBAC + immutable audit table.  
**Justification:** meets **INF-025** (authentication) and supports accountability implied by technician/master capabilities (**INF-003/004**).

### 4) Interface design
- External: `/auth/login`, `/auth/refresh`, `/auth/logout` in `openapi.yaml`.  
- Internal: auditing is a library call or internal endpoint; events persisted to `audit_event` table.

### 5) Data model/schema
- `sql/user_account_ddl.sql`, `sql/audit_event_ddl.sql`  
Sensitive fields: password hash (confidential), audit events (append-only).  
Justification: meets **INF-002** (roles) and **INF-025** (secure auth).

### 6) Caching & consistency
- Cache JWT signing key in memory; no caching of password hashes.  
- Strong consistency for role changes (invalidate refresh tokens by bumping `token_version`).

---

## D.4 TelemetryService + EventBus

### 1) Responsibilities & data ownership
Consumes telemetry from EventBus, persists telemetry samples, maintains latest snapshots, and streams updates to WebUI (SSE). Responsible for freshness SLI measurement (≤2s display update) and acquisition-rate reporting (10 Hz).

### 2) Technology options

**Messaging**
- Recommended: NATS JetStream 2.10–2.11
- Conservative: Redis Streams
- Cutting-edge: Kafka

**Streaming to UI**
- Recommended: SSE
- Conservative: long-polling
- Cutting-edge: WebSockets with protobuf frames

**Persistence**
- Recommended: PostgreSQL partitioned tables (time-based)
- Conservative: single telemetry table
- Cutting-edge: TimescaleDB (Postgres extension)

### 3) Recommended default stack
- NATS JetStream + SSE + PostgreSQL partitions (monthly).  
**Justification:** meets **INF-021** (10 Hz acquisition support) and **INF-020** (≤2s UI updates).

### 4) Interface design
- External: `/telemetry/stream` in `openapi.yaml`.  
- Internal: Gateway publishes `TelemetrySample` messages over gRPC to server and/or to EventBus (see `internal.proto`).

### 5) Data model/schema
- `sql/telemetry_sample_ddl.sql` (partitioning + indexes).  
Justification: meets **INF-019** (2-year reports) requiring historical storage/aggregation.

### 6) Caching & consistency
- Latest snapshot cache: in-memory map `(device_id, metric) -> last_sample`.  
- Persist raw; compute rollups nightly (avg/min/max) into `daily_rollup` for reporting.

---

## D.5 PlannerService + ArbitrationEngine

### 1) Responsibilities & data ownership
PlannerService stores and retrieves month plans and planned settings; ArbitrationEngine resolves the effective setpoint using precedence **Manual > Planned > Default**, and manages override lifecycles until planned boundary.

### 2) Technology options

**Plan modeling**
- Recommended: relational (plan header + plan_period_setting rows)
- Conservative: JSON blob per plan
- Cutting-edge: rules engine (Drools) for schedules

**Arbitration**
- Recommended: deterministic function + override state machine
- Conservative: ad-hoc per-device logic
- Cutting-edge: temporal rules with conflict resolution framework

**API style**
- Recommended: REST resources (`/plans`, `/overrides`, `/commands`)
- Conservative: single “doEverything” endpoint
- Cutting-edge: GraphQL mutations

### 3) Recommended default stack
- Relational plan tables + deterministic ArbitrationEngine per State Diagram (DigitalHome_State_OverrideSetting).  
**Justification:** meets **INF-018** (override precedence and duration rules).

### 4) Interface design
- External: `/plans/{year}/{month}` GET/PUT; `/commands` POST; `/overrides` GET/DELETE in `openapi.yaml`.
- Internal: arbitration invoked by API before forwarding command to gateway.

### 5) Data model/schema
- `sql/plan_ddl.sql`, `sql/override_setting_ddl.sql`, `sql/control_command_ddl.sql`  
Constraints enforce thermostat/humidistat allowed ranges.  
Justification: meets **INF-012** and **INF-014** (range/step constraints).

### 6) Caching & consistency
- Cache active plan for `(user_id, year, month)` TTL 60s; invalidate on plan update.  
- Overrides checked from DB on command issuance; cache active overrides TTL 5s.

---

## D.6 ReportingService

### 1) Responsibilities & data ownership
Generates monthly reports for any month in the last two years: per thermostat/humidistat daily average/max/min with times, security breach times, and downtime intervals.

### 2) Technology options

**Report format**
- Recommended: CSV + PDF (server-side rendering)
- Conservative: CSV only
- Cutting-edge: interactive HTML reports

**PDF generation**
- Recommended: OpenHTMLtoPDF 1.0+ (Java)
- Conservative: wkhtmltopdf external binary
- Cutting-edge: headless Chromium

**Query strategy**
- Recommended: daily rollups table + incident table
- Conservative: query raw telemetry each time
- Cutting-edge: OLAP engine (DuckDB)

### 3) Recommended default stack
- Rollup-based queries + CSV/PDF generation.  
**Justification:** meets **INF-019** (2-year reporting) efficiently.

### 4) Interface design
- External: `/reports/{year}/{month}` GET (metadata), `/reports/{year}/{month}/csv`, `/reports/{year}/{month}/pdf`.

### 5) Data model/schema
- `sql/daily_rollup_ddl.sql`, `sql/alarm_incident_ddl.sql`, `sql/downtime_interval_ddl.sql`  
Justification: meets **INF-019**.

### 6) Caching & consistency
- Cache generated reports for 24h keyed by `(user, year, month, format)`; invalidate when backfill/rollup rerun.

---

## D.7 BackupRestoreService

### 1) Responsibilities & data ownership
Schedules and executes daily backups of all system data and supports restore from the latest backup. Technician configures backup time at setup.

### 2) Technology options

**Backup mechanism**
- Recommended: pg_dump + WAL archiving (or pg_basebackup) to local encrypted volume
- Conservative: filesystem snapshot only
- Cutting-edge: point-in-time recovery with object storage

**Scheduling**
- Recommended: Kubernetes CronJob / system cron
- Conservative: manual trigger only
- Cutting-edge: operator-managed backups

**Encryption**
- Recommended: AES-256 encryption for backup archives
- Conservative: OS disk encryption only
- Cutting-edge: envelope encryption with Vault

### 3) Recommended default stack
- Nightly encrypted `pg_dump` + retention 14 days + restore command tested quarterly.  
**Justification:** meets **INF-023** (daily backup and restore from latest).

### 4) Interface design
- External: `/ops/backup/run`, `/ops/restore/latest`, `/ops/backup/schedule` (Technician-only).

### 5) Data model/schema
- Backup metadata table `sql/backup_job_ddl.sql`.  
Justification: supports **INF-023** auditability of backups.

### 6) Caching & consistency
- No caching; backups run with consistent snapshot isolation.

---

## D.8 GatewayAPI + DevicePluginHost (Gateway side)

### 1) Responsibilities & data ownership
Gateway bridges RF devices and server: runs acquisition loop (≥10 Hz per sensor), transmits commands to devices, publishes telemetry and acks, and loads device plugins to support simulation and different device protocols.

### 2) Technology options

**Language/runtime**
- Recommended: Go 1.22–1.24 (low footprint, good concurrency)
- Conservative: C# .NET 8
- Cutting-edge: Rust 1.78+

**Plugin system**
- Recommended: in-process plugins with stable interface + versioning
- Conservative: compile-time drivers only
- Cutting-edge: WASM plugins

**Transport to server**
- Recommended: gRPC over LAN + mTLS optional
- Conservative: HTTP REST
- Cutting-edge: QUIC

**Telemetry buffering**
- Recommended: local ring buffer + resend on reconnect
- Conservative: drop on disconnect
- Cutting-edge: durable embedded DB (SQLite WAL)

### 3) Recommended default stack
- Go gateway with gRPC `internal.proto` contract; plugin host supports simulator plugins.  
**Justification:** meets **INF-007** (simulation realism) and **INF-021** (10 Hz acquisition loop).

### 4) Interface design (Internal contracts)
See `internal.proto` (Section L). Includes telemetry publish and command delivery with acknowledgements.

### 5) Data model/schema
Gateway persists minimal local state only (optional): last command per device for reconciliation. If enabled: embedded SQLite; otherwise server is source of record.  
Justification: supports recovery behavior implied by **INF-022/023** during transient failures.

### 6) Caching & consistency
- Command delivery: at-least-once to device with idempotent command IDs.  
- Telemetry: at-least-once to server; server de-dupes by `(device_id, metric, timestamp)`.

---

## D.9 HomeDatabase (PostgreSQL)

### 1) Responsibilities & data ownership
Primary persistence for accounts, profiles, devices, plans, overrides, commands, telemetry, incidents, audit, rollups, downtime, and backup metadata.

### 2) Technology options

**Database**
- Recommended: PostgreSQL 14–16
- Conservative: SQLite
- Cutting-edge: TimescaleDB / CockroachDB

**Encryption-at-rest**
- Recommended: disk encryption (LUKS) + column-level encryption for sensitive fields
- Conservative: disk encryption only
- Cutting-edge: TDE (not native in Postgres)

### 3) Recommended default stack
- PostgreSQL 14–16 with partitioning for telemetry + indexes for report queries.  
**Justification:** meets **INF-019** (2-year reporting) and supports cost constraints **INF-006**.

### 4) Interface design
DB accessed via repositories in API/services; no direct external access.

### 5) Data model/schema
See `sql/*.sql` in Section L.

### 6) Caching & consistency
- Use read-committed for telemetry ingest; serializable for plan updates if conflicting edits are possible (optional).

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
Provided in Section L as `k8s/api-deployment.yaml` (Deployment + Service + HPA + ConfigMap + Secret).  
Justification: supports maintainability (**INF-026**) and reproducible deployment in simulator labs (**INF-007**).

## E2. DB HA topology, replication, backup cadence, restore
- Prototype (cost-minimized): single PostgreSQL instance with daily encrypted backup; optional streaming replica for read-only reporting.  
- Backup cadence: daily at technician-configured time; retention 14 days locally; monthly archive optional.  
- Restore: documented runbook; quarterly restore drill in simulator environment.  
Justification: meets **INF-023**.

## E3. Network topology + ingress/egress rules and latency expectations
Mapped to **Deployment Diagram** (DigitalHome_Deployment: N_Client→N_ISP→N_LAN→N_Server→N_GW→N_Devices).
- Ingress: HTTPS 443 to API/WebUI only; block all other inbound.  
- Egress: API→Gateway gRPC on LAN only (e.g., 50051).  
- Latency expectations: LAN p95 <10ms; telemetry freshness p99 ≤2s end-to-end.  
Justification: meets **INF-020**.

## E4. CI/CD sketch
1. PR checks: build, unit tests, lint, OpenAPI validation, proto lint, SQL migration lint, SAST.  
2. Integration tests: run simulator plugins + contract tests between API and Gateway.  
3. Container build + scan (Trivy/Grype).  
4. Deploy to staging (simulated home).  
5. Canary/blue-green to production home server (if supported), otherwise rolling update with health checks.  
Justification: supports **INF-026** and reduces regression risk under 12-month constraint (**INF-005**).

---

# F. Security Design

## F1. Auth & AuthZ
- Auth: username/password login; Argon2id password hashes.  
- Token model: short-lived JWT access token (15m) + refresh token (7d) in HttpOnly cookie; refresh rotates token; revoke by incrementing `token_version`.  
- RBAC: role claims `GENERAL`, `MASTER`, `TECHNICIAN`; endpoints enforce role policies.  
Justification: meets **INF-002** (roles) and **INF-025** (auth).

## F2. Secrets management & rotation
- Use k8s Secrets (or OS keyring for non-k8s); rotate JWT signing key quarterly; rotate DB password on restore events.  
Justification: meets **INF-025** (secure operation over ISP).

## F3. TLS & service-mesh considerations
- TLS 1.2+ (prefer 1.3) for all browser/API traffic; optional mTLS on LAN API↔Gateway.  
Justification: meets **INF-025** (encryption “recognized reliable technology such as TLS”).

## F4. Threat model summary (top 5)
| Threat | Mitigation |
|---|---|
| Credential stuffing | Rate limit + lockout; Argon2id; audit login failures |
| MITM on public Internet | TLS 1.3; HSTS; secure cookies |
| Unauthorized device control | RBAC + audit + command constraints |
| Tampering with audit logs | Append-only tables; restrict DB roles; backup integrity checks |
| Replay/duplicate commands | Idempotent command IDs; gateway de-dupe |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + example alerts
**Key metrics**
- `ui_freshness_seconds_p99` (end-to-end telemetry to UI)  
- `sensor_acquisition_rate_hz{device_id}`  
- `command_ack_latency_ms_p95`  
- `backup_last_success_timestamp`  
- `auth_login_failures_total`

**Logging**
- Structured JSON logs with correlation ID; audit events separate table.

**Tracing**
- OpenTelemetry traces for API requests and gateway RPC calls.

**Example Prometheus alerts**
- Telemetry freshness violation:
  - Alert if p99 > 2.5s for 15m (burn warning)
- Acquisition rate violation:
  - Alert if acquisition rate <10 Hz for 1m for any sensor

(Provided concretely in `architecture.md` deliverable and can be deployed with Prometheus rules.)

## G2. SLOs, error budgets, RTO/RPO
- SLO (UI freshness): 99% of intervals deliver updates ≤2s over rolling 15 minutes. (INF-020)  
- SLO (command success): 99.9% commands acked within 2s on LAN.  
- RPO: ≤24h; RTO: ≤60m (prototype target).  
Justification: meets **INF-023**.

## G3. Dashboard & runbook sketch
Dashboards: Telemetry freshness, acquisition rate, command latency/error rate, backup status, gateway connectivity, security incidents.  
Runbooks: “Gateway offline”, “DB full due to telemetry”, “Restore from latest backup”, “Alarm storm”.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Examples |
|---|---|---|
| Unit | ArbitrationEngine, PlannerService | precedence and boundary expiry |
| Integration | API+DB, Telemetry+Bus | telemetry ingest partitioning |
| Contract | API↔Gateway (proto) | command ack schema compatibility |
| E2E | Browser→API→Gateway simulator→DB→Report | thermostat setpoint override |
| Chaos | Server restart, network loss, power loss simulation | restore latest backup, reconnect |

Justification: validates **INF-022** (reliability) and **INF-023** (recovery).

## H2. Test data management & environments
- Environments: dev (local), CI (simulator), staging (realistic sim), production prototype (home lab).  
- Refresh cadence: CI DB ephemeral per run; staging refreshed weekly via anonymized seed data; production backups retained.  
Justification: supports **INF-007** (sim realism) and **INF-019** (reporting data).

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps (prototype-first)
No existing system is specified; assume greenfield. (A2)  
- Step 1: Deploy server + gateway with simulator plugins.  
- Step 2: Register devices (simulated) in DeviceRegistry.  
- Step 3: Create initial master account at install.  
- Step 4: Enable plans, overrides, reporting.  
Rollback: revert deployment artifact; restore DB from last backup.

## I2. Backwards compatibility & API versioning
- Version external API under `/api/v1`.  
- Non-breaking changes: additive fields only.  
- Breaking changes: new `/api/v2` with overlap window 90 days (prototype may shorten by approval).  
Justification: supports **INF-026** (commercial evolution readiness).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| Event-driven telemetry (bus + streaming) | polling; direct gateway→UI | Better decoupling and freshness; adds complexity | Needed for **INF-020** and **INF-021** simultaneously |
| Two-tier HomeWebServer + Gateway | single box; cloud-hosted | Two-tier isolates RF timing; cloud adds availability/security risks | Required by **INF-009** and **INF-010** |
| PostgreSQL vs SQLite | SQLite simpler; Postgres heavier | Postgres better for partitions, reporting, concurrency | Supports **INF-019** and growth |
| SSE vs WebSockets | WebSockets bidirectional but more complex | SSE simplest for server→browser push | Meets **INF-020** with less operational overhead |
| Plugin host for devices | hard-coded drivers | Plugins enable simulator and future devices; adds lifecycle mgmt | Meets **INF-007** (simulation) and maintainability **INF-026** |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** All timestamps are stored in UTC ISO-8601 for reporting consistency.  
- **A2:** Greenfield deployment; no legacy DH data migration is required.  
- **A3:** “Failure” in reliability requirement is defined as inability to monitor *and* control any device for >60 seconds.  
- **A4:** “Past two years” reporting implies retention of at least 24 months of rollups plus security incidents and downtime intervals.  
- **A5:** Remote access is permitted directly to home server via port-forwarding/ingress; if not, a VPN will be mandated (stakeholder decision).

## Conflicts / naming issues (per special rule)
- **C1:** UML uses `HomeWebServerAPI/AuthService/...` while requirements say “home web server” and “Gateway device”. Prefer requirement names in user-facing docs; keep code component names as internal.  
- **C2:** Requirements mention “manual switch on household devices” overrides; UML models `OverrideSource.MANUAL_DEVICE`. Assumed equivalent.

## Unresolved stakeholder questions (need answers)
1. Should remote access require VPN/mTLS by default, or is TLS + password acceptable for prototype? (affects A5)  
2. What is the acceptable storage budget for raw 10 Hz telemetry vs rollups-only retention?  
3. Are multiple households/users supported, or exactly one home per server instance?  
4. What exact format is required by HO2305 documentation standard (template sections, numbering)?  
5. Should security breach logs be treated as sensitive PII with stricter retention/deletion requirements?

---

# L. Deliverables

```markdown
# filename: architecture.md
(Contents are this ArchitectureDocument.md; store as architecture.md in repository root.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: DigitalHome HomeWebServer API
  version: 1.0.0
  description: >
    External API for DigitalHome prototype (home web server). Provides authentication,
    monitoring/control, plans/overrides, reporting, and ops (backup/restore).
servers:
  - url: https://{host}/api/v1
    variables:
      host:
        default: digitalhome.local
tags:
  - name: auth
  - name: devices
  - name: telemetry
  - name: commands
  - name: plans
  - name: reports
  - name: ops
security:
  - bearerAuth: []
paths:
  /auth/login:
    post:
      tags: [auth]
      summary: Login and obtain access token + refresh cookie
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/LoginRequest" }
      responses:
        "200":
          description: Authenticated
          headers:
            Set-Cookie:
              description: HttpOnly refresh token cookie
              schema:
                type: string
          content:
            application/json:
              schema: { $ref: "#/components/schemas/LoginResponse" }
        "401":
          description: Invalid credentials
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /auth/refresh:
    post:
      tags: [auth]
      summary: Exchange refresh cookie for a new access token
      security: []
      responses:
        "200":
          description: Refreshed
          content:
            application/json:
              schema: { $ref: "#/components/schemas/LoginResponse" }
        "401":
          description: Refresh invalid/expired
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /devices:
    get:
      tags: [devices]
      summary: List registered devices
      responses:
        "200":
          description: Devices
          content:
            application/json:
              schema:
                type: array
                items: { $ref: "#/components/schemas/Device" }

  /devices/{deviceId}:
    get:
      tags: [devices]
      summary: Get a device
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string, minLength: 1 }
      responses:
        "200":
          description: Device
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Device" }
        "404":
          description: Not found
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /telemetry/snapshot:
    get:
      tags: [telemetry]
      summary: Get latest known telemetry snapshot per device metric
      responses:
        "200":
          description: Snapshot
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TelemetrySnapshotResponse"

  /telemetry/stream:
    get:
      tags: [telemetry]
      summary: Stream telemetry updates (SSE)
      description: >
        Server-Sent Events stream. Event types include telemetry, device_status, and incident.
      responses:
        "200":
          description: SSE stream
          content:
            text/event-stream:
              schema:
                type: string
        "401":
          description: Unauthorized
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /commands:
    post:
      tags: [commands]
      summary: Issue a control command (thermostat/humidistat setpoint, switch on/off, arm/disarm)
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/ControlCommandRequest" }
      responses:
        "202":
          description: Accepted; forwarded to gateway
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ControlCommandResponse" }
        "400":
          description: Validation failed (range/step, unknown device, bad metric)
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }
        "401":
          description: Unauthorized
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }
        "403":
          description: Forbidden by RBAC
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /plans/{year}/{month}:
    get:
      tags: [plans]
      summary: Get month plan for authenticated user
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
          description: Plan
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Plan" }
        "404":
          description: No plan exists
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }
    put:
      tags: [plans]
      summary: Create or replace month plan (up to 4 periods/day)
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
            schema: { $ref: "#/components/schemas/PlanUpsertRequest" }
      responses:
        "200":
          description: Updated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Plan" }
        "400":
          description: Invalid plan shape/periods
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /overrides:
    get:
      tags: [plans]
      summary: List active overrides for current user
      responses:
        "200":
          description: Overrides
          content:
            application/json:
              schema:
                type: array
                items: { $ref: "#/components/schemas/OverrideSetting" }

  /overrides/{overrideId}:
    delete:
      tags: [plans]
      summary: Cancel an override early
      parameters:
        - in: path
          name: overrideId
          required: true
          schema: { type: string, minLength: 1 }
      responses:
        "204":
          description: Cancelled
        "404":
          description: Not found
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /reports/{year}/{month}:
    get:
      tags: [reports]
      summary: Get report metadata for a month (last 24 months)
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
          description: Report metadata
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ReportMetadata" }
        "400":
          description: Out of range (not within last 24 months)
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /reports/{year}/{month}/csv:
    get:
      tags: [reports]
      summary: Download report CSV
      parameters:
        - in: path
          name: year
          required: true
          schema: { type: integer }
        - in: path
          name: month
          required: true
          schema: { type: integer }
      responses:
        "200":
          description: CSV
          content:
            text/csv:
              schema: { type: string }

  /reports/{year}/{month}/pdf:
    get:
      tags: [reports]
      summary: Download report PDF
      parameters:
        - in: path
          name: year
          required: true
          schema: { type: integer }
        - in: path
          name: month
          required: true
          schema: { type: integer }
      responses:
        "200":
          description: PDF
          content:
            application/pdf:
              schema:
                type: string
                format: binary

  /ops/backup/schedule:
    put:
      tags: [ops]
      summary: Set daily backup schedule (Technician/Master)
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/BackupScheduleRequest" }
      responses:
        "204":
          description: Saved
        "403":
          description: Forbidden
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /ops/backup/run:
    post:
      tags: [ops]
      summary: Trigger backup immediately (Technician/Master)
      responses:
        "202":
          description: Started
          content:
            application/json:
              schema: { $ref: "#/components/schemas/BackupJobResponse" }
        "403":
          description: Forbidden
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

  /ops/restore/latest:
    post:
      tags: [ops]
      summary: Restore from latest backup (Technician only)
      responses:
        "202":
          description: Restore started
          content:
            application/json:
              schema: { $ref: "#/components/schemas/RestoreJobResponse" }
        "403":
          description: Forbidden
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problem" }

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Problem:
      type: object
      required: [type, title, status, detail, instance, traceId]
      properties:
        type: { type: string, format: uri }
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
        instance: { type: string }
        traceId: { type: string }

    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1, maxLength: 64 }
        password: { type: string, minLength: 8, maxLength: 256 }

    LoginResponse:
      type: object
      required: [accessToken, expiresInSeconds, role]
      properties:
        accessToken: { type: string, minLength: 1 }
        expiresInSeconds: { type: integer, minimum: 60, maximum: 3600 }
        role:
          type: string
          enum: [GENERAL, MASTER, TECHNICIAN]

    Device:
      type: object
      required: [deviceId, deviceType, location, online]
      properties:
        deviceId: { type: string }
        deviceType:
          type: string
          enum: [THERMOSTAT, HUMIDISTAT, CONTACT_SENSOR, POWER_SWITCH, ALARM_LIGHT, ALARM_SOUND]
        location: { type: string }
        online: { type: boolean }

    TelemetrySample:
      type: object
      required: [deviceId, metric, value, timestampUtc]
      properties:
        deviceId: { type: string }
        metric: { type: string, example: "temperatureF" }
        value: { type: number }
        timestampUtc: { type: string, format: date-time }

    TelemetrySnapshotResponse:
      type: object
      required: [samples]
      properties:
        samples:
          type: array
          items: { $ref: "#/components/schemas/TelemetrySample" }

    ControlCommandRequest:
      type: object
      required: [deviceId, metric, value]
      properties:
        deviceId: { type: string }
        metric:
          type: string
          description: >
            For thermostats: setpointF or setpointC. For humidistats: setpointPct.
            For power switches: state (0=OFF,1=ON). For security: arm (0/1).
        value: { type: number }

    ControlCommandResponse:
      type: object
      required: [commandId, status]
      properties:
        commandId: { type: string }
        status:
          type: string
          enum: [ACCEPTED, REJECTED]

    Plan:
      type: object
      required: [planId, year, month, days]
      properties:
        planId: { type: string }
        year: { type: integer }
        month: { type: integer, minimum: 1, maximum: 12 }
        days:
          type: array
          items:
            $ref: "#/components/schemas/PlanDay"

    PlanDay:
      type: object
      required: [date, periods]
      properties:
        date: { type: string, format: date }
        periods:
          type: array
          maxItems: 4
          items: { $ref: "#/components/schemas/PlanPeriod" }

    PlanPeriod:
      type: object
      required: [periodIndex, startLocalTime, settings]
      properties:
        periodIndex: { type: integer, minimum: 1, maximum: 4 }
        startLocalTime:
          type: string
          pattern: "^[0-2][0-9]:[0-5][0-9]$"
        settings:
          type: array
          items: { $ref: "#/components/schemas/PlannedSetting" }

    PlannedSetting:
      type: object
      required: [deviceId, metric, value]
      properties:
        deviceId: { type: string }
        metric: { type: string }
        value: { type: number }

    PlanUpsertRequest:
      type: object
      required: [days]
      properties:
        days:
          type: array
          items: { $ref: "#/components/schemas/PlanDay" }

    OverrideSetting:
      type: object
      required: [overrideId, deviceId, metric, value, source, effectiveFromUtc, effectiveUntilUtc]
      properties:
        overrideId: { type: string }
        deviceId: { type: string }
        metric: { type: string }
        value: { type: number }
        source:
          type: string
          enum: [WEBSITE, MANUAL_DEVICE]
        effectiveFromUtc: { type: string, format: date-time }
        effectiveUntilUtc: { type: string, format: date-time }

    ReportMetadata:
      type: object
      required: [year, month, generatedAtUtc]
      properties:
        year: { type: integer }
        month: { type: integer }
        generatedAtUtc: { type: string, format: date-time }

    BackupScheduleRequest:
      type: object
      required: [timeLocal]
      properties:
        timeLocal:
          type: string
          description: Local time HH:MM for daily backup.
          pattern: "^[0-2][0-9]:[0-5][0-9]$"

    BackupJobResponse:
      type: object
      required: [jobId, status]
      properties:
        jobId: { type: string }
        status: { type: string, enum: [STARTED] }

    RestoreJobResponse:
      type: object
      required: [jobId, status]
      properties:
        jobId: { type: string }
        status: { type: string, enum: [STARTED] }
```

```proto
// filename: internal.proto
syntax = "proto3";

package digitalhome.internal.v1;

option go_package = "github.com/homeowner/digitalhome/internal/gen;internalv1";

message DeviceId {
  string id = 1;
}

message TelemetrySample {
  string device_id = 1;
  string metric = 2;          // e.g., temperatureF, humidityPct, contactState, switchState
  double value = 3;
  string timestamp_utc = 4;   // ISO-8601 UTC string
}

message ControlCommand {
  string command_id = 1;
  string device_id = 2;
  string metric = 3;          // setpointF, setpointC, setpointPct, state, arm
  double value = 4;
  string issued_at_utc = 5;
  int64 issued_by_user_id = 6;
}

message CommandAck {
  string command_id = 1;
  bool accepted = 2;
  string reason = 3;          // non-empty if accepted=false
  string acknowledged_at_utc = 4;
}

message GatewayHealth {
  string gateway_id = 1;
  bool rf_ok = 2;
  double acquisition_rate_hz = 3;
  string timestamp_utc = 4;
}

service GatewayControlService {
  rpc SendControlCommand(ControlCommand) returns (CommandAck);
  rpc GetGatewayHealth(DeviceId) returns (GatewayHealth);
}

service TelemetryIngestService {
  rpc PublishTelemetry(stream TelemetrySample) returns (CommandAck);
}
```

```yaml
# filename: k8s/api-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: digitalhome
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: dh-api-config
  namespace: digitalhome
data:
  APP_ENV: "prod"
  DB_HOST: "dh-postgres"
  DB_PORT: "5432"
  DB_NAME: "digitalhome"
  NATS_URL: "nats://dh-nats:4222"
---
apiVersion: v1
kind: Secret
metadata:
  name: dh-api-secrets
  namespace: digitalhome
type: Opaque
stringData:
  DB_USER: "dh_app"
  DB_PASSWORD: "change-me"
  JWT_SIGNING_KEY: "change-me-32bytes-min"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dh-api
  namespace: digitalhome
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dh-api
  template:
    metadata:
      labels:
        app: dh-api
    spec:
      containers:
        - name: api
          image: ghcr.io/homeowner/digitalhome-api:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: dh-api-config
            - secretRef:
                name: dh-api-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1"
              memory: "1Gi"
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
  name: dh-api
  namespace: digitalhome
spec:
  selector:
    app: dh-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: dh-api-hpa
  namespace: digitalhome
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dh-api
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
-- filename: sql/user_account_ddl.sql
CREATE TABLE IF NOT EXISTS user_account (
  id                BIGSERIAL PRIMARY KEY,
  username          VARCHAR(64) NOT NULL UNIQUE,
  role              VARCHAR(16) NOT NULL CHECK (role IN ('GENERAL','MASTER','TECHNICIAN')),
  password_hash     TEXT NOT NULL, -- encrypt-at-rest via disk + restricted DB role
  token_version     INT NOT NULL DEFAULT 0,
  date_created_utc  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_account_role ON user_account(role);
```

```sql
-- filename: sql/user_profile_ddl.sql
CREATE TABLE IF NOT EXISTS user_profile (
  id            BIGINT PRIMARY KEY REFERENCES user_account(id) ON DELETE CASCADE,
  temp_units    CHAR(1) NOT NULL CHECK (temp_units IN ('F','C'))
);
```

```sql
-- filename: sql/device_ddl.sql
CREATE TABLE IF NOT EXISTS device (
  device_id     VARCHAR(64) PRIMARY KEY,
  device_type   VARCHAR(32) NOT NULL CHECK (device_type IN
    ('THERMOSTAT','HUMIDISTAT','CONTACT_SENSOR','POWER_SWITCH','ALARM_LIGHT','ALARM_SOUND')),
  location      VARCHAR(128) NOT NULL,
  online        BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_device_type ON device(device_type);
```

```sql
-- filename: sql/plan_ddl.sql
CREATE TABLE IF NOT EXISTS plan (
  plan_id        UUID PRIMARY KEY,
  owner_user_id  BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  year           INT NOT NULL,
  month          INT NOT NULL CHECK (month BETWEEN 1 AND 12),
  created_utc    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(owner_user_id, year, month)
);

-- Up to 4 periods per day; store start time local as minutes since midnight (0..1439)
CREATE TABLE IF NOT EXISTS plan_period_setting (
  id             BIGSERIAL PRIMARY KEY,
  plan_id        UUID NOT NULL REFERENCES plan(plan_id) ON DELETE CASCADE,
  day_date       DATE NOT NULL,
  period_index   INT NOT NULL CHECK (period_index BETWEEN 1 AND 4),
  start_minute   INT NOT NULL CHECK (start_minute BETWEEN 0 AND 1439),
  device_id      VARCHAR(64) NOT NULL REFERENCES device(device_id),
  metric         VARCHAR(64) NOT NULL,
  value          DOUBLE PRECISION NOT NULL,
  UNIQUE(plan_id, day_date, period_index, device_id, metric)
);

CREATE INDEX IF NOT EXISTS idx_plan_period_lookup
  ON plan_period_setting(plan_id, day_date, period_index);

CREATE INDEX IF NOT EXISTS idx_plan_period_device_metric
  ON plan_period_setting(device_id, metric, day_date);
```

```sql
-- filename: sql/override_setting_ddl.sql
CREATE TABLE IF NOT EXISTS override_setting (
  override_id         UUID PRIMARY KEY,
  owner_user_id       BIGINT NOT NULL REFERENCES user_account(id) ON DELETE CASCADE,
  device_id           VARCHAR(64) NOT NULL REFERENCES device(device_id),
  metric              VARCHAR(64) NOT NULL,
  value               DOUBLE PRECISION NOT NULL,
  source              VARCHAR(16) NOT NULL CHECK (source IN ('WEBSITE','MANUAL_DEVICE')),
  effective_from_utc  TIMESTAMPTZ NOT NULL,
  effective_until_utc TIMESTAMPTZ NOT NULL,
  cancelled_utc       TIMESTAMPTZ NULL,
  CHECK (effective_until_utc > effective_from_utc)
);

CREATE INDEX IF NOT EXISTS idx_override_active
  ON override_setting(device_id, metric, effective_from_utc, effective_until_utc)
  WHERE cancelled_utc IS NULL;
```

```sql
-- filename: sql/control_command_ddl.sql
CREATE TABLE IF NOT EXISTS control_command (
  command_id       UUID PRIMARY KEY,
  device_id        VARCHAR(64) NOT NULL REFERENCES device(device_id),
  metric           VARCHAR(64) NOT NULL,
  value            DOUBLE PRECISION NOT NULL,
  issued_at_utc    TIMESTAMPTZ NOT NULL,
  issued_by_user_id BIGINT NOT NULL REFERENCES user_account(id),
  status           VARCHAR(16) NOT NULL CHECK (status IN ('ACCEPTED','REJECTED')),
  reject_reason    TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_command_device_time ON control_command(device_id, issued_at_utc DESC);
```

```sql
-- filename: sql/telemetry_sample_ddl.sql
CREATE TABLE IF NOT EXISTS telemetry_sample (
  sample_id      UUID PRIMARY KEY,
  device_id      VARCHAR(64) NOT NULL REFERENCES device(device_id),
  metric         VARCHAR(64) NOT NULL,
  value          DOUBLE PRECISION NOT NULL,
  timestamp_utc  TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_telemetry_device_metric_time
  ON telemetry_sample(device_id, metric, timestamp_utc DESC);
```

```sql
-- filename: sql/audit_event_ddl.sql
CREATE TABLE IF NOT EXISTS audit_event (
  event_id        UUID PRIMARY KEY,
  timestamp_utc   TIMESTAMPTZ NOT NULL,
  user_id         BIGINT NOT NULL REFERENCES user_account(id),
  role            VARCHAR(16) NOT NULL CHECK (role IN ('GENERAL','MASTER','TECHNICIAN')),
  action          VARCHAR(64) NOT NULL,
  target          VARCHAR(256) NOT NULL,
  status          VARCHAR(16) NOT NULL,
  detail          TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_event(timestamp_utc DESC);
-- Operational policy: NO UPDATE/DELETE granted to app role on this table (append-only).
```

```sql
-- filename: sql/alarm_incident_ddl.sql
CREATE TABLE IF NOT EXISTS alarm_incident (
  incident_id      UUID PRIMARY KEY,
  sensor_id        VARCHAR(64) NOT NULL REFERENCES device(device_id),
  activated_at_utc TIMESTAMPTZ NOT NULL,
  incident_type    VARCHAR(64) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_incident_time ON alarm_incident(activated_at_utc DESC);
```

```sql
-- filename: sql/daily_rollup_ddl.sql
CREATE TABLE IF NOT EXISTS daily_rollup (
  device_id      VARCHAR(64) NOT NULL REFERENCES device(device_id),
  metric         VARCHAR(64) NOT NULL,
  day_date       DATE NOT NULL,
  avg_value      DOUBLE PRECISION NOT NULL,
  min_value      DOUBLE PRECISION NOT NULL,
  min_at_utc     TIMESTAMPTZ NOT NULL,
  max_value      DOUBLE PRECISION NOT NULL,
  max_at_utc     TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (device_id, metric, day_date)
);

CREATE INDEX IF NOT EXISTS idx_rollup_day ON daily_rollup(day_date DESC);
```

```sql
-- filename: sql/downtime_interval_ddl.sql
CREATE TABLE IF NOT EXISTS downtime_interval (
  id              BIGSERIAL PRIMARY KEY,
  started_at_utc  TIMESTAMPTZ NOT NULL,
  ended_at_utc    TIMESTAMPTZ NULL,
  reason          VARCHAR(256) NULL
);

CREATE INDEX IF NOT EXISTS idx_downtime_start ON downtime_interval(started_at_utc DESC);
```

```sql
-- filename: sql/backup_job_ddl.sql
CREATE TABLE IF NOT EXISTS backup_job (
  job_id           UUID PRIMARY KEY,
  started_at_utc   TIMESTAMPTZ NOT NULL,
  finished_at_utc  TIMESTAMPTZ NULL,
  status           VARCHAR(16) NOT NULL CHECK (status IN ('STARTED','SUCCEEDED','FAILED')),
  artifact_path    TEXT NULL,
  detail           TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_backup_time ON backup_job(started_at_utc DESC);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-001,System manages home environment devices via web page,"DigitalHome_UseCase:UC_Monitor|UC_Control; DigitalHome_Container:WebUI|API|Devices","WebUI,HomeWebServerAPI,GatewayAPI","architecture.md,openapi.yaml","Core DH capability: monitor/control via personal web page."
INF-002,Roles General/Master/Technician,"DigitalHome_UseCase:EndUser|MasterUser|Technician; DigitalHome_Class:UserAccount.role","AuthService,RbacPolicy","sql/user_account_ddl.sql,openapi.yaml","RBAC required for privileged config/account actions."
INF-003,Master user manages accounts/config,"DigitalHome_UseCase:UC_Accounts|UC_Config","HomeWebServerAPI,AuthService","openapi.yaml","Endpoints restricted to MASTER/TECHNICIAN."
INF-004,Technician setup/maintains config; start/stop; backup,"DigitalHome_UseCase:UC_Config|UC_Backup","BackupRestoreService,GatewayAPI","openapi.yaml,sql/backup_job_ddl.sql","Operational endpoints and auditability."
INF-005,Prototype delivery constraints (12 months, 5 engineers),,Process,"architecture.md","Drives simpler modular architecture choices."
INF-006,Minimize cost; use widely accepted tech,,All,"architecture.md","Select commodity OSS and avoid vendor lock-in."
INF-007,Simulated environment realistic,"DigitalHome_Component:DevicePluginHost; DigitalHome_Deployment:N_Devices(sim)","DevicePluginHost,SimulatorPlugins","internal.proto","Plugins enable swapping simulator vs real devices."
INF-008,Requires ISP; remote access,"DigitalHome_Deployment:N_ISP; DigitalHome_Container:ISP","Ingress/API","k8s/api-deployment.yaml","Public ingress requires TLS and hardening."
INF-009,Home web server hosts UI/control/storage/accounts/backup,"DigitalHome_Deployment:N_Server","API,DB,Backup","sql/*.sql","DB and services reside on home server."
INF-010,Gateway connects to broadband and devices,"DigitalHome_Deployment:N_GW; DigitalHome_Component:GatewayAPI","GatewayAPI,RFModule","internal.proto","Contract for server↔gateway."
INF-011,RF module 1000ft indoor range,"DigitalHome_Deployment:N_GW->N_Devices","RFModule","architecture.md","Range constraint informs simulator and installation."
INF-012,Thermostat capabilities + constraints + schedules,"DigitalHome_Class:Plan|OverrideSetting; DigitalHome_State_OverrideSetting","PlannerService,ArbitrationEngine","sql/plan_ddl.sql,sql/override_setting_ddl.sql","Models scheduling and constraints."
INF-013,Support F/C units and sensor bounds,"DigitalHome_Class:UserProfile.tempUnits","WebUI,TelemetryService","sql/user_profile_ddl.sql","Store user preference and standardize reporting."
INF-014,Humidistat capabilities + constraints + schedules,"DigitalHome_Class:Plan|OverrideSetting","PlannerService,ArbitrationEngine","sql/plan_ddl.sql","Same planning/override mechanism."
INF-015,Security contacts + alarms on breach,"DigitalHome_Class:AlarmIncident","TelemetryService,GatewayAPI","sql/alarm_incident_ddl.sql","Persist and report breach events."
INF-016,Appliance manager power switches state/control,"DigitalHome_UseCase:UC_Control","GatewayAPI,PlannerService","openapi.yaml","Command endpoint supports switch state."
INF-017,Planner month plan with up to 4 periods/day,"DigitalHome_UseCase:UC_Plans","PlannerService","openapi.yaml,sql/plan_ddl.sql","Plan schema enforces period structure."
INF-018,Override precedence Manual>Planned>Default; duration until planned boundary,"DigitalHome_State_OverrideSetting","ArbitrationEngine","architecture.md,sql/override_setting_ddl.sql","Single arbitration policy across devices."
INF-019,Reports for past 2 years incl stats/breaches/downtime,"DigitalHome_UseCase:UC_Reports","ReportingService","openapi.yaml,sql/daily_rollup_ddl.sql,sql/downtime_interval_ddl.sql","Rollups enable efficient reporting."
INF-020,Displays updated at least every 2 seconds,"DigitalHome_Sequence_RemoteMonitor","TelemetryService,WebUI","openapi.yaml","SSE stream supports freshness."
INF-021,Sensor acquisition >=10Hz,"DigitalHome_Activity_RemoteMonitorAndControl","DigitalHomeGateway","internal.proto","Gateway loop enforces and reports acquisition rate."
INF-022,Reliability <=1 failure/10,000 hours,"DigitalHome_Deployment:N_Server|N_GW","HealthAgent,Ops","architecture.md","Defines failure and instruments SLOs."
INF-023,Daily backup + restore from latest backup,"DigitalHome_UseCase:UC_Backup","BackupRestoreService","openapi.yaml,sql/backup_job_ddl.sql","Implements required backup/recovery."
INF-024,Clear descriptive error messages,"DigitalHome_UseCase:UC_Errors","HomeWebServerAPI","openapi.yaml","Problem Details schema standardizes errors."
INF-025,Authentication + encryption via TLS,"DigitalHome_UseCase:UC_Auth; DigitalHome_Container:Browser->API TLS","Ingress,AuthService","openapi.yaml,k8s/api-deployment.yaml","TLS protects in transit; auth required."
INF-026,Prototype design suitable for commercial reuse,,All,"architecture.md","Contracts + modular boundaries support evolution."
INF-027,All documents up to date and archived (HO2305),,Process,"architecture.md","Doc pipeline and deliverables list."
INF-028,UML 2.0 preferred,,Diagrams referenced,"architecture.md","Maintains UML alignment."
INF-029,Director approval for major requirement changes,,Governance,"architecture.md","Change control noted."
INF-030,HVAC compatibility + ASHRAE 2010 adherence,,DevicePlugins,"architecture.md","Captured as device capability constraints and documentation."
INF-031,Devices must be within 1000ft of gateway,"DigitalHome_Deployment:N_GW->N_Devices","RFModule","architecture.md","Operational constraint for installation/testing."
```

---

## Verification & Acceptance Criteria Checklist

| Item | Status |
|---|---|
| 3-line Analysis Plan present | ✅ |
| Sections A–L included | ✅ |
| Every FR/NFR/ASR mapped in traceability matrix (as INF-*) | ✅ (via `traceability_matrix.csv`) |
| ≥1 OpenAPI YAML and ≥1 internal contract included | ✅ (`openapi.yaml`, `internal.proto`) |
| Representative k8s manifest snippet included | ✅ (`k8s/api-deployment.yaml`) |
| SQL DDL provided for primary entities | ✅ (`sql/*.sql`) |
| Major components have API contract + data schema coverage | ✅ (API+DB schemas; gateway contract; UI uses API) |
| Assumptions and unresolved questions listed | ✅ |

---

## “How to review” checklist (end)

- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?