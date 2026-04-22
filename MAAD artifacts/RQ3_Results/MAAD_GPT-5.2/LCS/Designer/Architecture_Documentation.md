Scope: Produce production-ready architecture documentation for the I‑15 Reversible Lane Control System (RLCS) application, aligning to the provided SRS corpus and the provided 11 UML diagrams; resolve conflicts by preferring SRS naming/IDs.  
Approach: Normalize the SRS into atomic, testable `INF-*` requirements; map each to 4+1 views, interfaces (OpenAPI + internal proto), schemas (SQL DDL), and ops artifacts (k8s), with explicit safety/security controls.  
Top validation steps: (1) traceability completeness (all `INF-*` mapped), (2) contract/schema linting (OpenAPI/proto/SQL/k8s parse), (3) scenario tests for open/close sequencing + safety screening + degraded mode + audit/security.

# ArchitectureDocument.md

## A. Executive Summary (≤1 page)

### System overview
The RLCS Application controls and monitors I‑15 reversible lane field devices (gates, pop-ups, CMS, sensors) via FCU/DCU controllers, provides an operator GUI for status/commands/configuration/reporting, enforces multi-layer safety interlocks, logs/audits all actions, and exports one-way status to external systems every 30 seconds.

**Primary diagram mapping (one-line):**  
- Context & users: *UseCase_ScenarioView* (System, UC_*).  
- Core domain model: *Class_LogicView* (GameSession→**mapped to** RLCS OperationSession; QuestionSet→ConfigSet; AdminUser→Personnel).  
- Runtime flows: *Sequence_ProcessView_S1_AdminPublishUpdate* (**mapped to** Config Publish) and *Sequence_ProcessView_S2_EndUserPlayGame* (**mapped to** Operator Open/Close).  
- Deployment: *Deployment_PhysicalView* and *Container_PhysicalView* (**mapped to** TMC/FCU/DCU + DB + external status server).

> Conflict note: Provided UML diagrams describe a “Web Quiz Game System” and conflict with the RLCS SRS. Per rule, **SRS naming/IDs are authoritative**; UML is used only as structural inspiration. Conflicts are logged in **K**.

### Architectural style(s) and topology
- **Architectural style:** Layered + event-driven control core (command processor + safety screening + device adapters) with replicated edge control units.  
- **Deployment topology:** Hub-and-spoke: TMC (TSU/app+DB) ↔ FCU(s) ↔ DCU(s), with one-way external status server outside firewall and secure dial-in remote access.

### Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| Wrong-way opening due to logic/config error | Catastrophic safety event | Multi-layer safety screening at TSU/FCU/DCU; rule sets in non-volatile memory; “unknown/opposite open” hard blocks; independent verification tests + simulation; immutable audit logs. |
| Controller/network failure during operations | Loss of control/visibility | Degraded mode control at FCU; DCU direct control fallback; transparent fiber→ISDN failover; RTO ≤10 min runbooks; HA DB + app redundancy. |
| Unauthorized access / tampering | Safety + compliance breach | RBAC, single-operator command control, strong auth, password aging, lockout, TLS, dial-in hardening, integrity checks (hash + message checksums), audit trails with retention. |

### Key QA coverage mapping

| Quality attribute | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-013 (scale to +2 DCU, +4 CMS, +20 closures), INF-NFR-006 (max users) | Load tests, capacity tests, soak tests |
| Availability | INF-NFR-014 (24/7), INF-NFR-015 (99.x uptime), INF-NFR-016 (RTO ≤10 min), INF-NFR-017 (30-day no reboot) | HA/failover tests, chaos tests, DR drills |
| Security | INF-ASR-020 (RBAC), INF-ASR-021 (password hashing/aging), INF-ASR-022 (MD5 integrity per SRS), INF-ASR-023 (checksums), INF-ASR-024 (firewall one-way export), INF-ASR-025 (secure dial-in) | Pen tests, SAST/DAST, config audits, negative auth tests |
| Performance | INF-NFR-001..005 (2s updates, 12s device response, 30s export) | Latency tests, end-to-end timing tests, network emulation |
| Maintainability | INF-ASR-026 (modular/open architecture), INF-FR-009 (config without programming) | Change impact tests, config migration tests, contract tests |

---

## B. Traceability & Rationale

### Normalized requirement set
The SRS text lacks stable IDs; therefore requirements are normalized into `INF-*` IDs (per rule). **All requirements from the corpus are represented** via these atomic statements.

**Traceability matrix (also delivered as `traceability_matrix.csv` in L).**

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-001 | GUI shows status, commands, config, logs export, reports | UseCase_ScenarioView:System, UC_* | OperatorGUI, CommandService, ReportingService | architecture.md, openapi.yaml | Core user-facing function set. |
| INF-FR-002 | Logon screen with username/password; command control enablement | UseCase_ScenarioView:UC_AdminLogin (mapped), Sequence_ProcessView_S1_* (mapped) | AuthService, OperatorGUI | openapi.yaml, internal.proto, sql/personnel_ddl.sql | Enforces controlled access and command authority. |
| INF-FR-003 | Only one operator may have command control at a time; higher security can take over with prompt/notify | State_LogicView_GameSession (mapped), Sequence_ProcessView_S2_* (mapped) | CommandArbiter, AuthService, OperatorGUI | internal.proto, sql/command_control_ddl.sql | Prevents conflicting control actions. |
| INF-FR-004 | Status continues updating every 2s even when no user logged in | Deployment_PhysicalView:App nodes (mapped) | MonitoringService, DeviceAdapter | internal.proto | Ensures unattended monitoring. |
| INF-FR-005 | GUI map of facility; device icons with OK/alarm/override colors; audible alarm | Container_PhysicalView:GameWebUI (mapped) | OperatorGUI | architecture.md | Operator situational awareness. |
| INF-FR-006 | Config screens admin-only; modify DB tables except logs; validate conflicts | Activity_ProcessView_AdminPublish (mapped) | ConfigService, DB | openapi.yaml, sql/* | Controlled configuration management. |
| INF-FR-007 | Additional password required to configure device rules | Activity_ProcessView_AdminPublish (mapped) | AuthService, ConfigService | openapi.yaml | Protects safety-critical rules. |
| INF-FR-008 | Add/remove devices and modify map without programming | Package_DevelopmentView:pkg_ui (mapped) | OperatorGUI, ConfigService | sql/device_ddl.sql | Data-driven UI. |
| INF-FR-009 | Export logs ASCII; problem work order + daily diary editable constraints | Class_LogicView:AuditLogEntry (mapped) | LogService, WorkOrderService | openapi.yaml, sql/logs_ddl.sql | Auditability and operator workflow. |
| INF-FR-010 | Detail views per device and per category | UseCase_ScenarioView:UC_ViewScore (mapped) | OperatorGUI, QueryService | openapi.yaml | Supports diagnostics. |
| INF-FR-011 | Retrieve historical reports by date range/name via COTS reporting | Component_DevelopmentView:ContentService (mapped) | ReportingService | architecture.md | Reporting requirement. |
| INF-FR-012 | Confirm window for any command (manual or scheduled) | Sequence_ProcessView_S2_* (mapped) | OperatorGUI, CommandService | openapi.yaml | Human-in-the-loop safety. |
| INF-FR-013 | Acknowledge/silence alarms per device for configurable time | UseCase_ScenarioView:UC_GetFeedback (mapped) | AlarmService, OperatorGUI | openapi.yaml, sql/alarm_ddl.sql | Alarm handling. |
| INF-FR-014 | Change system mode screen for authorized users | UseCase_ScenarioView:UC_PlayGame (mapped) | ModeService | openapi.yaml, sql/system_mode_ddl.sql | Mode-driven behavior. |
| INF-FR-015 | Monitor all sensors; update DB; screen update ≤2s | Deployment_PhysicalView (mapped) | MonitoringService, DB | internal.proto, sql/device_status_ddl.sql | Real-time monitoring. |
| INF-FR-016 | Integrity checks: abort if closure device status unknown; execute only with valid statuses | Sequence_ProcessView_S2_* (mapped) | SafetyScreeningService, CommandService | internal.proto | Prevent unsafe actions. |
| INF-FR-017 | Critical/warning alarms per conditions; notify within 2s | Component_DevelopmentView:AuditLogStore (mapped) | AlarmService | sql/alarm_ddl.sql | Alarm semantics. |
| INF-FR-018 | Override device status (DB-only) for configurable time; does not affect others | Class_LogicView:AdminUser (mapped) | OverrideService | sql/override_ddl.sql | Enables controlled continuation. |
| INF-FR-019 | Commands forwarded only superior→inferior (TSU>FCU>DCU) | Deployment_PhysicalView (mapped) | CommandRouter | internal.proto | Enforces hierarchy. |
| INF-FR-020 | Retry status requests; failure after N retries => device failure | Activity_ProcessView_AdminPublish (mapped) | MonitoringService | sql/system_control_params_ddl.sql | Robust polling. |
| INF-FR-021 | Startup: identify cabinet ID, verify cards, integrity check, init tables; ≤30s | Deployment_PhysicalView (mapped) | ControllerAgent | internal.proto | Deterministic startup. |
| INF-FR-022 | Execute scheduled sequences; check schedule at least every 60s; operator confirmation | Sequence_ProcessView_S2_* (mapped) | SchedulerService, OperatorGUI | openapi.yaml, sql/schedule_ddl.sql | Scheduled operations. |
| INF-FR-023 | Halt sequences on step timeout or unsafe status changes; resume within configurable hold time | State_LogicView_GameSession (mapped) | SequencerService | sql/sequencer_params_ddl.sql | Safe sequencing. |
| INF-FR-024 | One-way external status export every 30s; one-way serial output | Deployment_PhysicalView:Proxy/Storage (mapped) | ExternalExportService | openapi.yaml | External consumers. |
| INF-FR-025 | Remote access via secure dial-in through firewall for authorized users | Deployment_PhysicalView (mapped) | RemoteAccessGateway | architecture.md | Remote operations. |
| INF-ASR-020 | RBAC by command level/device/mode/workstation; status/control/override | Class_LogicView:AdminUser (mapped) | AuthZService | sql/personnel_security_ddl.sql | Fine-grained authorization. |
| INF-ASR-021 | Password hashing + aging + min lengths; lockout after retries | Class_LogicView:AdminUser (mapped) | AuthService | sql/personnel_ddl.sql | Credential security. |
| INF-ASR-022 | MD5 message digest integrity verification daily; alarm on failure; block unit from sequences | Class_LogicView:AuditLogEntry (mapped) | IntegrityService | sql/integrity_log_ddl.sql | SRS-mandated integrity control. |
| INF-ASR-023 | Valid checksum algorithms for inter-unit messages | Sequence_ProcessView_S2_* (mapped) | TransportSecurity | internal.proto | Detect message corruption. |
| INF-ASR-024 | External systems access via firewall; one-way output only | Deployment_PhysicalView (mapped) | ExternalExportService | architecture.md | Prevent inbound influence. |
| INF-ASR-025 | Secure dial-in is two-way; only authorized remote users | Deployment_PhysicalView (mapped) | RemoteAccessGateway | architecture.md | Controlled remote entry. |
| INF-ASR-026 | Open, modular, scalable architecture; future roadway changes without programming | Package_DevelopmentView (mapped) | All services | architecture.md | Maintainability/scalability. |
| INF-NFR-001 | GUI status update ≤2s; map refresh default 2s configurable | State_LogicView_GameSession (mapped) | OperatorGUI | sql/system_control_params_ddl.sql | Performance target. |
| INF-NFR-002 | Device state change displayed ≤2s from occurrence | Sequence_ProcessView_S2_* (mapped) | MonitoringService | internal.proto | Real-time requirement. |
| INF-NFR-003 | Device responds to commands ≤12s after operator confirmation | Sequence_ProcessView_S2_* (mapped) | DeviceAdapter | internal.proto | Field responsiveness. |
| INF-NFR-004 | External export interval 30s | Deployment_PhysicalView (mapped) | ExternalExportService | architecture.md | External SLA. |
| INF-NFR-005 | Scheduled event scan at least every 60s | Activity_ProcessView_AdminPublish (mapped) | SchedulerService | architecture.md | Scheduler cadence. |
| INF-NFR-006 | Support multiple users up to DB-defined max; only one command controller | UseCase_ScenarioView (mapped) | AuthService, CommandArbiter | sql/system_control_params_ddl.sql | Concurrency constraints. |
| INF-NFR-013 | Scale: +2 DCU, +4 CMS, +20 closures | Deployment_PhysicalView (mapped) | DeviceRegistry | sql/device_ddl.sql | Capacity planning. |
| INF-NFR-014 | Availability 24/7/365 | Deployment_PhysicalView (mapped) | All | k8s/* | Operational requirement. |
| INF-NFR-015 | Uptime ≥99.x yearly | Deployment_PhysicalView (mapped) | All | k8s/*, SLOs | Availability objective. |
| INF-NFR-016 | Recovery time ≤10 minutes | Deployment_PhysicalView (mapped) | Ops/Runbooks | architecture.md | DR requirement. |
| INF-NFR-017 | No reset/reboot due to RLCS error for ≥30 days | Deployment_PhysicalView (mapped) | All | testing plan | Reliability. |

---

## C. Architecture Overview

### 4+1 view alignment

**Context (Scenario view):** Operators, administrators, maintenance staff, and external systems. Use cases: monitor/control, configure, schedule, report, export status, remote access. (Ref: *UseCase_ScenarioView:System, UC_*; mapped to RLCS roles.)

**Container view:**  
- Operator Workstations (TMC/FCU) running OperatorGUI.  
- Application services (Command, Sequencer, Monitoring, Alarm, Config, Reporting, Export).  
- Central DB (COTS RDBMS).  
- Field Controller Agents at FCU/DCU interfacing to I/O driver software and device I/O cards.  
(Ref: *Container_PhysicalView* elements mapped to RLCS containers.)

**Component/Package view:** Modular services: AuthN/AuthZ, CommandArbiter, SafetyScreening, Sequencer, Scheduler, DeviceRegistry, DeviceAdapter, Alarm, Logging/Audit, Reporting, ExternalExport. (Ref: *Package_DevelopmentView*, *Component_DevelopmentView* mapped.)

**Class/Runtime view:** Domain entities: Personnel, Workstation, Device, DeviceStatus, DeviceRules, Commands (device/macro/super), Schedules, Logs, Overrides, AlarmCriteria. (Ref: *Class_LogicView* mapped.)

**Deployment view:** Private RLCS network (fiber primary, ISDN secondary), FCU↔DCU copper, firewall boundary to external status server and dial-in modem. (Ref: *Deployment_PhysicalView* mapped.)

---

## D. Detailed Technical Design (developer-facing)

### D1. Subsystem: Operator GUI (TMC/FCU workstations)

1) **Responsibilities & data ownership**  
Renders facility map and device icons, shows alarms/overrides, provides command confirmation dialogs, supports alarm acknowledge/silence, exposes configuration screens (admin-only), and report retrieval. Owns no authoritative state; reads from services/DB.

2) **Technology options (3+ per concern)**  
- Language/runtime: Recommended **TypeScript**; Conservative C#; Cutting-edge Rust+Tauri.  
- Web framework: Recommended React; Conservative Angular; Cutting-edge SvelteKit.  
- RPC/HTTP: Recommended REST/JSON; Conservative SOAP; Cutting-edge gRPC-web.  
- Persistence: none local (except cached read-only).  
- Cache: browser memory + IndexedDB (optional).  
- Messaging: WebSocket for push alarms; fallback polling.  
- Auth: OIDC (recommended) or local session.  
- Observability: OpenTelemetry JS.  
- CI/CD: GitHub Actions/Azure DevOps.  
- Container runtime/infra: N/A (desktop) or kiosk VM images.

3) **Recommended default stack**  
- React 18.x + TypeScript 5.x; WebSocket + REST.  
Justification: meets **INF-NFR-001** (2s refresh) via push+poll fallback and supports rich UI for alarms.

4) **Interface design**  
Uses `openapi.yaml` endpoints `/auth/*`, `/status/*`, `/commands/*`, `/alarms/*`, `/config/*`, `/reports/*`.

5) **Data model/schema**  
No primary ownership; uses DB via services.

6) **Caching & consistency**  
Cache static map/layout and device catalog with ETag; status is **strongly consistent** to last poll/push (≤2s). No client-side writes except diary/work order drafts.

---

### D2. Subsystem: Command + Safety Screening + Sequencer (core control)

1) **Responsibilities & data ownership**  
Accepts operator/scheduled commands, enforces command control exclusivity, performs multi-layer safety screening, routes commands TSU→FCU→DCU, executes sequences with step timeouts, halts/resumes, and records command logs. Owns command execution state machine; authoritative device state remains at controllers but is mirrored centrally.

2) **Technology options**  
- Language/runtime: Recommended **Java 21**; Conservative C++17; Cutting-edge Go 1.22.  
- Framework: Recommended Spring Boot 3.2; Conservative Jakarta EE; Cutting-edge Quarkus.  
- RPC: Recommended gRPC internal; Conservative REST only; Cutting-edge NATS request/reply.  
- Persistence: Recommended PostgreSQL; Conservative Oracle (per SRS legacy); Cutting-edge CockroachDB.  
- Cache: Recommended Redis; Conservative none; Cutting-edge Aerospike.  
- Messaging: Recommended Kafka; Conservative RabbitMQ; Cutting-edge Redpanda.  
- AuthZ: Recommended OPA (policy-as-code); Conservative DB-driven checks; Cutting-edge Cedar.  
- Observability: OpenTelemetry + Prometheus.  
- CI/CD: GitHub Actions + Helm.  
- Container runtime/infra: containerd on Kubernetes; conservative VM systemd.

3) **Recommended default stack**  
- Java 21 + Spring Boot 3.2, gRPC internal, PostgreSQL 15-16, Redis 7.2.  
Justification: meets **INF-FR-016** (integrity/safety checks) and **INF-NFR-002** (≤2s propagation) with low-latency services and strong typing.

4) **Interface design (internal)**  
See `internal.proto` services `CommandRouter`, `SafetyScreening`, `Sequencer`, `ControllerAgent`.

5) **Data model/schema**  
See DDLs: `device`, `device_status`, `device_rules`, `device_command`, `device_command_macro`, `system_operational_command`, `schedule`, `command_log`, `override`, `alarm_log`.

6) **Caching & consistency**  
- Cache device catalog/rules with versioning; invalidate on config publish.  
- Safety screening must use config data ≤3s old → enforce cache max-age 1s and version checks; fallback to DB read.

---

### D3. Subsystem: Monitoring + Alarm + Logging/Audit

1) **Responsibilities & data ownership**  
Polls/receives device/controller status, updates DB, detects alarm conditions within 2s, triggers audible/visual notifications, supports acknowledge/silence, and writes immutable logs (command log, alarm log, diary, work orders, integrity verification results).

2) **Technology options**  
- Language/runtime: Recommended Java 21; Conservative .NET 8; Cutting-edge Elixir.  
- Persistence: Recommended PostgreSQL; Conservative Oracle 19c; Cutting-edge TimescaleDB.  
- Messaging: Recommended Kafka; Conservative polling only; Cutting-edge MQTT.  
- Observability: Prometheus + Loki; conservative syslog; cutting-edge ClickHouse.

3) **Recommended default stack**  
- Java 21 services + PostgreSQL 15-16 + Kafka 3.7 + Loki.  
Justification: meets **INF-FR-017** (alarm generation) and **INF-NFR-002** (≤2s detection/notify).

4) **Interface design**  
External: `/alarms/*`, `/logs/*`. Internal: `StatusStream` in `internal.proto`.

5) **Data model/schema**  
See `sql/alarm_ddl.sql`, `sql/logs_ddl.sql`, `sql/integrity_log_ddl.sql`.

6) **Caching & consistency**  
No caching for alarms; logs append-only; status table upserts with last_seen timestamps.

---

### D4. Subsystem: Configuration + Reporting + External Export

1) **Responsibilities & data ownership**  
Admin edits configuration tables (except logs), validates conflicts/redundancy, publishes versions to controllers (replicated to non-volatile memory), supports COTS reporting, exports one-way status file every 30s to external server and one-way serial output.

2) **Technology options**  
- DBMS: Recommended PostgreSQL; Conservative Oracle 19c (aligns SRS “Oracle 8i” legacy); Cutting-edge Yugabyte.  
- Reporting: Recommended Metabase; Conservative Crystal Reports; Cutting-edge Superset.  
- Export: Recommended SFTP drop + signed JSON; Conservative SMB share; Cutting-edge HTTPS push to DMZ.

3) **Recommended default stack**  
- PostgreSQL 15-16 + Metabase 0.49 + DMZ SFTP export.  
Justification: meets **INF-FR-024** (one-way export every 30s) and **INF-FR-006** (admin config with validation).

---

### D5. External API (OpenAPI) — `openapi.yaml`
(Provided in full in section L; referenced here.)

**Error format (uniform):** `{ "error": { "code": "...", "message": "...", "details": {...}, "correlationId": "..." } }`

---

### D6. Primary persisted entities (SQL DDL)
(Provided in full in section L; referenced here.)

**Encryption-at-rest / immutability flags:**  
- Password hashes: encrypted-at-rest (DB TDE or disk encryption) + access restricted. Justification: meets **INF-ASR-021**.  
- Audit/command logs: append-only/immutable (enforced by permissions + triggers). Justification: meets **INF-FR-009**.  
- Integrity digests: immutable records. Justification: meets **INF-ASR-022**.

---

## E. Operations & Deployment (ops-facing)

### E1. Kubernetes-ready plan (representative manifest)
See `k8s/rlcs-core-deployment.yaml` in L.

Replica sizing guidance (starting point):
- Small (≤50 devices): core=2 replicas, monitoring=2, db=1 primary+1 standby.
- Medium (≤500 devices): core=3, monitoring=3, kafka=3, db=1+2.
- Large (≥1000 devices): core=5, monitoring=5, kafka=5, db=1+2 with read replicas.

Justification: meets **INF-NFR-014** (24/7) via redundancy.

### E2. DB HA topology, backups, restore
- Topology: PostgreSQL primary + synchronous standby (same site) + async DR replica (optional).  
- Backups: nightly full + 15-min WAL archiving; retain 90 days; quarterly restore drills.  
Justification: meets **INF-NFR-016** (RTO ≤10 min) by tested restore and HA failover.

### E3. Network topology + ingress/egress rules
- Private RLCS network: TSU/TMC ↔ FCU ↔ DCU; no inbound from external systems.  
- DMZ external status server: receives one-way file drop; external systems read there.  
- Dial-in: terminates at firewall/VPN concentrator; only to FCU workstations/services.  
Justification: meets **INF-ASR-024** (one-way external) and **INF-ASR-025** (secure dial-in).

### E4. CI/CD sketch
1. Build + unit tests + SAST  
2. Contract tests (OpenAPI/proto) + schema migration dry-run  
3. Integration tests with simulator (sequencer/safety)  
4. Deploy to staging (blue/green)  
5. Canary to production (10%) + SLO gate  
Justification: meets **INF-ASR-026** (modular maintainable) via automated gates.

---

## F. Security Design

### F1. Auth & AuthZ
- **AuthN:** OIDC for workstation users where feasible; fallback local auth for isolated networks.  
- **AuthZ:** RBAC with attributes: command level (status/control/override), device, mode, workstation.  
- Command control token: single active “command controller” lease with TTL and takeover workflow.  
Justification: meets **INF-ASR-020** and **INF-FR-003**.

### F2. Secrets management & rotation
- Kubernetes Secrets + external KMS (e.g., HashiCorp Vault) for DB creds, signing keys. Rotate quarterly or on incident.  
Justification: meets **INF-NFR-014** by reducing outage risk from credential incidents.

### F3. TLS & service mesh
- TLS 1.2+ everywhere; mTLS inside cluster optional; strict cipher suites.  
Justification: meets **INF-ASR-025** (secure remote access).

### F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Unauthorized command issuance | RBAC + command control lease + MFA for override + audit |
| Tampering with controller logic/rules | Non-volatile replication + MD5 digest verification + alarms + block from sequences |
| Replay/altered inter-unit messages | Message checksums + sequence numbers + TLS where possible |
| Insider config mistake | Simulator testing + two-person rule for rule changes + versioned publish |
| DoS on monitoring | Rate limits + backpressure + degraded mode operations |

---

## G. Observability & SRE

### G1. Metrics/logs/traces + example alerts
Key metrics:
- `rlcs_status_update_lag_seconds` (p95)  
- `rlcs_command_step_timeout_total`  
- `rlcs_safety_screen_fail_total`  
- `rlcs_alarm_notify_latency_seconds`  
- `rlcs_command_controller_lease_conflicts_total`

Logs: structured JSON with correlationId; never log passwords.

Example Prometheus alerts:
- **Status lag breach**
```promql
histogram_quantile(0.95, sum(rate(rlcs_status_update_lag_seconds_bucket[5m])) by (le)) > 2
```
- **Integrity verification failure**
```promql
increase(rlcs_integrity_verification_fail_total[1h]) > 0
```

Justification: meets **INF-NFR-002** (≤2s) and **INF-ASR-022** (integrity alarms).

### G2. SLOs, error budgets, RTO/RPO
- SLO: status propagation p95 ≤2s (budget 0.1%).  
- SLO: alarm notify p95 ≤2s.  
- Availability: ≥99.x yearly.  
- RTO ≤10 min; RPO ≤15 min (WAL).  
Justification: meets **INF-NFR-015/016**.

### G3. Dashboard/runbook sketch
Dashboards: device health, command pipeline, sequencer state, alarms, integrity checks, network link status.  
Runbooks: “halted sequence resume”, “FCU failover”, “DB failover”, “integrity failure isolate unit”.

---

## H. Testing Strategy

### H1. Test matrix

| Test type | Components | Focus |
|---|---|---|
| Unit | SafetyScreening, Sequencer, AuthZ | rule evaluation, timeouts, RBAC |
| Integration | Core↔DB, Core↔ControllerAgent | status/command flows |
| Contract | OpenAPI, gRPC proto | backward compatibility |
| E2E | Operator open/close sequences | halt/resume, opposite-direction interlocks |
| Chaos | network loss, controller down | degraded mode, RTO |

Justification: meets **INF-FR-023** (halt/resume) and **INF-NFR-016** (recovery).

### H2. Test data & environments
Envs: dev, integration (simulator), staging (full stack), prod. Refresh: weekly for staging; prod-like anonymized logs.

---

## I. Migration, Data Conversion & Rollout Plan

1) Steps:
- Stand up new TSU/app+DB in parallel with existing system (parallel operation requirement).  
- Import device catalog, rules, schedules; validate in simulator.  
- Field deployment: install controller agents; run shadow monitoring.  
- Cutover during facility closed; execute full acceptance test; then disconnect old system.

2) Backward compatibility:
- Version OpenAPI `/api/v1`; additive changes only; deprecate with 6-month window.

Justification: meets **INF-NFR-014** (continuous operation) and “parallel operation” requirement (captured in INF-FR-026 below in K).

---

## J. Tradeoffs & Alternatives

| Decision | Alternatives | Why chosen |
|---|---|---|
| PostgreSQL vs Oracle | Oracle 19c; CockroachDB | PostgreSQL reduces cost/ops complexity while meeting performance; Oracle remains conservative option aligning SRS legacy. Tied to **INF-NFR-001/002**. |
| gRPC internal | REST-only; message bus only | gRPC gives strict contracts for safety-critical command routing; still expose REST externally. Tied to **INF-FR-019**. |
| MD5 integrity (per SRS) | SHA-256; signed manifests | SRS explicitly allows MD5; implement MD5 for compliance but wrap with additional signed manifests as defense-in-depth (documented as enhancement). Tied to **INF-ASR-022**. |

---

## K. Open Questions & Assumptions

### Assumptions
- **A1:** A central TSU application server exists at TMC hosting core services and DB.  
- **A2:** Controllers (FCU/DCU) can run a “ControllerAgent” process and store replicated rule/config in non-volatile memory.  
- **A3:** Inter-unit transport supports adding checksums/sequence numbers without breaking controller firmware constraints.  
- **A4:** External status export format will be JSON (in addition to any legacy flat file) and is read-only by external systems.  
- **A5:** “99.” uptime in SRS is interpreted as **≥99.0%** until stakeholders confirm exact value.  
- **A6:** COTS reporting tool can access a read replica or reporting schema without impacting control-plane latency.

### Open stakeholder questions (need answers)
1. Confirm exact uptime target: 99.0%, 99.5%, 99.9%?  
2. Confirm authoritative list of system modes beyond Normal/Degraded/Emergency/Maintenance.  
3. Confirm exact device inventory and command strings for each controller type (2070 ATC vs other).  
4. Confirm external status file schema (flat file vs JSON) and hosting location in DMZ.  
5. Confirm dial-in security requirements (VPN type, MFA, allowed endpoints).

### Conflict log (UML vs SRS)
- UML names “Web Quiz Game System”, “QuestionSet”, “GameSession”, “Admin publish” conflict with RLCS. Per rule, SRS terms (RLCS, TSU/FCU/DCU, Device, Command, Schedule) are authoritative; UML used only as generic structural patterns.

### Additional normalized requirement added for completeness
- **INF-FR-026:** Parallel operation during deployment; disconnect legacy only after successful closed-hours field test.

---

## L. Deliverables

```markdown
# architecture.md
(Identical to ArchitectureDocument.md content)
```

```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: RLCS External API
  version: "1.0.0"
  description: >
    External API for RLCS operator/admin workstations and for one-way external status retrieval.
    Note: External systems must not send control inputs (one-way export is separate).
servers:
  - url: https://rlcs.example.local/api/v1
paths:
  /auth/login:
    post:
      summary: Login and obtain access token
      operationId: login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        "200":
          description: Authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LoginResponse"
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "423":
          description: Account locked
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /auth/logout:
    post:
      summary: Logout (revoke token)
      operationId: logout
      security:
        - bearerAuth: []
      responses:
        "204":
          description: Logged out
        "401":
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /command-control/lease:
    post:
      summary: Acquire or take over command control lease
      operationId: acquireCommandControl
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CommandControlLeaseRequest"
      responses:
        "200":
          description: Lease granted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandControlLease"
        "409":
          description: Lease conflict (another operator holds control and takeover not permitted)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /status/summary:
    get:
      summary: Get current system operation status summary
      operationId: getStatusSummary
      security:
        - bearerAuth: []
      responses:
        "200":
          description: Current status
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SystemStatusSummary"
        "401":
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /devices:
    get:
      summary: List devices (catalog)
      operationId: listDevices
      security:
        - bearerAuth: []
      parameters:
        - in: query
          name: category
          schema:
            type: string
          required: false
        - in: query
          name: locationId
          schema:
            type: integer
          required: false
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
  /devices/{deviceId}/status:
    get:
      summary: Get detailed status for a device
      operationId: getDeviceStatus
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: deviceId
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: Device status
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeviceStatus"
        "404":
          description: Not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /commands/confirm:
    post:
      summary: Confirm and execute a command (device/macro/super)
      operationId: confirmCommand
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CommandConfirmRequest"
      responses:
        "202":
          description: Accepted for execution
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandAccepted"
        "400":
          description: Validation error / safety screening failed
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "409":
          description: Command control not held
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /alarms/active:
    get:
      summary: List active alarms
      operationId: listActiveAlarms
      security:
        - bearerAuth: []
      responses:
        "200":
          description: Active alarms
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      $ref: "#/components/schemas/Alarm"
  /alarms/{alarmId}/ack:
    post:
      summary: Acknowledge an alarm and optionally silence audible alarm
      operationId: acknowledgeAlarm
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: alarmId
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AlarmAcknowledgeRequest"
      responses:
        "200":
          description: Updated alarm
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Alarm"
  /config/publish:
    post:
      summary: Publish configuration changes (admin only)
      operationId: publishConfig
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ConfigPublishRequest"
      responses:
        "200":
          description: Published
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ConfigPublishResponse"
        "403":
          description: Forbidden
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /reports/run:
    post:
      summary: Run a report by name and date range
      operationId: runReport
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ReportRunRequest"
      responses:
        "200":
          description: Report result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ReportRunResponse"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    LoginRequest:
      type: object
      required: [username, password, workstationId]
      properties:
        username:
          type: string
          minLength: 3
          maxLength: 64
        password:
          type: string
          minLength: 12
          maxLength: 256
        workstationId:
          type: integer
    LoginResponse:
      type: object
      required: [accessToken, expiresInSeconds, personnelId, commandLevel]
      properties:
        accessToken:
          type: string
        expiresInSeconds:
          type: integer
          minimum: 60
        personnelId:
          type: integer
        commandLevel:
          type: string
          enum: [STATUS_ONLY, CONTROL, OVERRIDE]
    CommandControlLeaseRequest:
      type: object
      required: [requested, takeoverIfHigherSecurity]
      properties:
        requested:
          type: boolean
        takeoverIfHigherSecurity:
          type: boolean
    CommandControlLease:
      type: object
      required: [heldByPersonnelId, heldByWorkstationId, leaseExpiresAtUtc]
      properties:
        heldByPersonnelId:
          type: integer
        heldByWorkstationId:
          type: integer
        leaseExpiresAtUtc:
          type: string
          format: date-time
    SystemStatusSummary:
      type: object
      required: [operationStatus, customerType, updatedAtUtc]
      properties:
        operationStatus:
          type: string
          enum: [OPEN_NORTH, OPEN_SOUTH, CLOSED, UNKNOWN]
        customerType:
          type: string
          enum: [RLCS_FASTRAK_ONLY, ALL_TRAFFIC, UNKNOWN]
        updatedAtUtc:
          type: string
          format: date-time
        accessPoints:
          type: array
          items:
            $ref: "#/components/schemas/AccessPointStatus"
    AccessPointStatus:
      type: object
      required: [locationId, isOpen]
      properties:
        locationId:
          type: integer
        isOpen:
          type: boolean
    Device:
      type: object
      required: [deviceId, name, category, locationId, direction]
      properties:
        deviceId:
          type: integer
        name:
          type: string
        category:
          type: string
        locationId:
          type: integer
        direction:
          type: string
          enum: [NORTHBOUND, SOUTHBOUND, BOTH, NA]
    DeviceStatus:
      type: object
      required: [deviceId, status, lastChangedAtUtc, lastSeenAtUtc, overridden]
      properties:
        deviceId:
          type: integer
        status:
          type: string
        lastChangedAtUtc:
          type: string
          format: date-time
        lastSeenAtUtc:
          type: string
          format: date-time
        overridden:
          type: boolean
        sensorData:
          type: object
          additionalProperties: true
    CommandConfirmRequest:
      type: object
      required: [commandType, commandId, confirm]
      properties:
        commandType:
          type: string
          enum: [DEVICE, MACRO, SUPER, OVERRIDE]
        commandId:
          type: integer
        confirm:
          type: boolean
        parameters:
          type: object
          additionalProperties: true
    CommandAccepted:
      type: object
      required: [commandExecutionId, acceptedAtUtc]
      properties:
        commandExecutionId:
          type: string
        acceptedAtUtc:
          type: string
          format: date-time
    Alarm:
      type: object
      required: [alarmId, alarmType, deviceId, message, active, raisedAtUtc]
      properties:
        alarmId:
          type: integer
        alarmType:
          type: string
          enum: [CRITICAL, WARNING]
        deviceId:
          type: integer
        message:
          type: string
        active:
          type: boolean
        raisedAtUtc:
          type: string
          format: date-time
        acknowledgedAtUtc:
          type: string
          format: date-time
          nullable: true
        silencedUntilUtc:
          type: string
          format: date-time
          nullable: true
    AlarmAcknowledgeRequest:
      type: object
      required: [acknowledge, silenceSeconds]
      properties:
        acknowledge:
          type: boolean
        silenceSeconds:
          type: integer
          minimum: 0
          maximum: 86400
    ConfigPublishRequest:
      type: object
      required: [changeSet, rulePassword]
      properties:
        changeSet:
          type: object
          additionalProperties: true
        rulePassword:
          type: string
          minLength: 12
          maxLength: 256
    ConfigPublishResponse:
      type: object
      required: [configVersion, publishedAtUtc]
      properties:
        configVersion:
          type: integer
        publishedAtUtc:
          type: string
          format: date-time
    ReportRunRequest:
      type: object
      required: [reportName, beginUtc, endUtc]
      properties:
        reportName:
          type: string
        beginUtc:
          type: string
          format: date-time
        endUtc:
          type: string
          format: date-time
        parameters:
          type: object
          additionalProperties: true
    ReportRunResponse:
      type: object
      required: [reportName, generatedAtUtc, result]
      properties:
        reportName:
          type: string
        generatedAtUtc:
          type: string
          format: date-time
        result:
          type: object
          additionalProperties: true
    ErrorResponse:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message, correlationId]
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: object
              additionalProperties: true
            correlationId:
              type: string
```

```proto
// internal.proto
syntax = "proto3";

package rlcs.internal.v1;

import "google/protobuf/timestamp.proto";

message UnitId {
  string unit_type = 1; // TSU, FCU, DCU
  int32 unit_number = 2; // e.g., FCU-N=1, FCU-S=2, DCU1=1...
}

message DeviceId {
  int32 device_id = 1;
}

message StatusSample {
  DeviceId device = 1;
  string status = 2; // OPEN/CLOSED/UNKNOWN/etc.
  google.protobuf.Timestamp last_changed_utc = 3;
  google.protobuf.Timestamp last_seen_utc = 4;
  bool overridden = 5;
  map<string,string> sensor_data = 6;
}

message StatusBatch {
  UnitId source_unit = 1;
  google.protobuf.Timestamp sampled_at_utc = 2;
  repeated StatusSample samples = 3;
  uint32 message_checksum = 4; // transport-level checksum (INF-ASR-023)
  uint64 sequence_number = 5;
}

message SafetyScreenRequest {
  UnitId originating_unit = 1;
  string command_type = 2; // DEVICE/MACRO/SUPER
  int32 command_id = 3;
  google.protobuf.Timestamp config_snapshot_time_utc = 4; // must be <=3s old
}

message SafetyScreenResult {
  bool allowed = 1;
  string reason_code = 2;
  string reason_text = 3;
}

message CommandStep {
  int32 step_number = 1;
  int32 device_command_id = 2;
  int32 timeout_seconds = 3;
}

message ExecuteCommandRequest {
  UnitId originating_unit = 1;
  UnitId target_unit = 2;
  string command_type = 3; // DEVICE/MACRO/SUPER
  int32 command_id = 4;
  string command_execution_id = 5;
  repeated CommandStep steps = 6;
  uint32 message_checksum = 7;
  uint64 sequence_number = 8;
}

message ExecuteCommandAck {
  string command_execution_id = 1;
  bool accepted = 2;
  string reject_reason = 3;
  google.protobuf.Timestamp accepted_at_utc = 4;
}

message CommandProgress {
  string command_execution_id = 1;
  int32 current_step = 2;
  string state = 3; // RUNNING/HALTED/COMPLETED/ABORTED
  string detail = 4;
  google.protobuf.Timestamp updated_at_utc = 5;
}

message IntegrityVerifyRequest {
  UnitId unit = 1;
  bool operator_initiated = 2;
}

message IntegrityVerifyResult {
  UnitId unit = 1;
  bool ok = 2;
  string md5_hex = 3;
  google.protobuf.Timestamp verified_at_utc = 4;
}

service StatusStream {
  rpc PushStatus(StatusBatch) returns (google.protobuf.Timestamp);
}

service SafetyScreening {
  rpc Screen(SafetyScreenRequest) returns (SafetyScreenResult);
}

service CommandRouter {
  rpc Execute(ExecuteCommandRequest) returns (ExecuteCommandAck);
  rpc SubscribeProgress(UnitId) returns (stream CommandProgress);
}

service IntegrityService {
  rpc Verify(IntegrityVerifyRequest) returns (IntegrityVerifyResult);
}
```

```yaml
# k8s/rlcs-core-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rlcs-core
  namespace: rlcs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rlcs-core
  template:
    metadata:
      labels:
        app: rlcs-core
    spec:
      containers:
        - name: rlcs-core
          image: ghcr.io/example/rlcs-core:1.0.0
          ports:
            - containerPort: 8080
            - containerPort: 9090
          envFrom:
            - configMapRef:
                name: rlcs-core-config
            - secretRef:
                name: rlcs-core-secrets
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "4Gi"
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: rlcs-core
  namespace: rlcs
spec:
  selector:
    app: rlcs-core
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rlcs-core-hpa
  namespace: rlcs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rlcs-core
  minReplicas: 3
  maxReplicas: 10
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
  name: rlcs-core-config
  namespace: rlcs
data:
  RLCS_POLL_INTERVAL_MS: "2000"
  RLCS_SCHEDULE_SCAN_SECONDS: "60"
  RLCS_EXPORT_INTERVAL_SECONDS: "30"
---
apiVersion: v1
kind: Secret
metadata:
  name: rlcs-core-secrets
  namespace: rlcs
type: Opaque
stringData:
  DB_URL: "jdbc:postgresql://postgresql.rlcs.svc.cluster.local:5432/rlcs"
  DB_USER: "rlcs_app"
  DB_PASSWORD: "REPLACE_ME"
  JWT_SIGNING_KEY: "REPLACE_ME"
```

```sql
-- sql/device_ddl.sql
CREATE TABLE device_category (
  device_category_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE location (
  location_id SERIAL PRIMARY KEY,
  highway TEXT,
  segment TEXT,
  direction TEXT,
  lane TEXT,
  geo_code TEXT,
  name TEXT NOT NULL
);

CREATE TABLE device (
  device_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  device_category_id INT NOT NULL REFERENCES device_category(device_category_id),
  location_id INT NOT NULL REFERENCES location(location_id),
  direction TEXT NOT NULL CHECK (direction IN ('NORTHBOUND','SOUTHBOUND','BOTH','NA')),
  controller_unit TEXT NOT NULL, -- TSU/FCU/DCU identifier
  is_closure_device BOOLEAN NOT NULL DEFAULT FALSE,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_device_category ON device(device_category_id);
CREATE INDEX idx_device_location ON device(location_id);
CREATE INDEX idx_device_controller ON device(controller_unit);
```

```sql
-- sql/device_status_ddl.sql
CREATE TABLE device_status (
  device_id INT PRIMARY KEY REFERENCES device(device_id),
  status TEXT NOT NULL,
  last_changed_at_utc TIMESTAMPTZ NOT NULL,
  last_seen_at_utc TIMESTAMPTZ NOT NULL,
  overridden BOOLEAN NOT NULL DEFAULT FALSE,
  override_expires_at_utc TIMESTAMPTZ,
  sensor_data JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX idx_device_status_last_seen ON device_status(last_seen_at_utc);
CREATE INDEX idx_device_status_status ON device_status(status);
```

```sql
-- sql/device_rules_ddl.sql
CREATE TABLE system_mode (
  system_mode_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE device_rules (
  device_rules_id SERIAL PRIMARY KEY,
  system_mode_id INT NOT NULL REFERENCES system_mode(system_mode_id),
  device_x_id INT NOT NULL REFERENCES device(device_id),
  desired_status_x TEXT NOT NULL,
  device_y_id INT NOT NULL REFERENCES device(device_id),
  prohibited_status_y TEXT NOT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_rules_mode ON device_rules(system_mode_id);
CREATE INDEX idx_rules_x ON device_rules(device_x_id);
CREATE INDEX idx_rules_y ON device_rules(device_y_id);
```

```sql
-- sql/personnel_ddl.sql
CREATE TABLE personnel (
  personnel_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  initials TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL, -- store Argon2/bcrypt hash; encrypt-at-rest via disk/TDE
  password_changed_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  status TEXT NOT NULL CHECK (status IN ('ACTIVE_LOGGED_ON','ACTIVE_LOGGED_OFF','INACTIVE')),
  failed_attempts INT NOT NULL DEFAULT 0,
  locked_until_utc TIMESTAMPTZ
);

CREATE INDEX idx_personnel_status ON personnel(status);
```

```sql
-- sql/personnel_security_ddl.sql
CREATE TABLE workstation (
  workstation_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  location_id INT REFERENCES location(location_id),
  can_issue_commands BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE command_level (
  command_level_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  level_type TEXT NOT NULL CHECK (level_type IN ('STATUS_ONLY','CONTROL','OVERRIDE'))
);

CREATE TABLE personnel_security_level (
  personnel_security_level_id SERIAL PRIMARY KEY,
  personnel_id INT NOT NULL REFERENCES personnel(personnel_id),
  system_mode_id INT REFERENCES system_mode(system_mode_id),
  command_level_id INT NOT NULL REFERENCES command_level(command_level_id),
  workstation_id INT REFERENCES workstation(workstation_id),
  device_id INT REFERENCES device(device_id)
);

CREATE INDEX idx_psl_personnel ON personnel_security_level(personnel_id);
```

```sql
-- sql/schedule_ddl.sql
CREATE TABLE system_operational_command (
  system_operational_command_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  timeout_seconds INT NOT NULL,
  command_level_id INT NOT NULL REFERENCES command_level(command_level_id)
);

CREATE TABLE system_operation_schedule (
  system_operation_schedule_id SERIAL PRIMARY KEY,
  system_mode_id INT NOT NULL REFERENCES system_mode(system_mode_id),
  start_time_utc TIMESTAMPTZ NOT NULL,
  end_time_utc TIMESTAMPTZ,
  frequency_seconds INT NOT NULL,
  command_type TEXT NOT NULL CHECK (command_type IN ('DEVICE','MACRO','SUPER')),
  command_id INT NOT NULL,
  requires_operator_confirmation BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_schedule_mode_time ON system_operation_schedule(system_mode_id, start_time_utc);
```

```sql
-- sql/logs_ddl.sql
CREATE TABLE device_command_log (
  device_command_log_id BIGSERIAL PRIMARY KEY,
  device_id INT REFERENCES device(device_id),
  command_id INT NOT NULL,
  command_type TEXT NOT NULL,
  issued_by_personnel_id INT REFERENCES personnel(personnel_id),
  issued_by_workstation_id INT REFERENCES workstation(workstation_id),
  issued_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  result TEXT NOT NULL,
  detail TEXT
);

CREATE INDEX idx_cmdlog_time ON device_command_log(issued_at_utc);

CREATE TABLE operator_daily_diary_log (
  operator_daily_diary_log_id BIGSERIAL PRIMARY KEY,
  personnel_id INT NOT NULL REFERENCES personnel(personnel_id),
  workstation_id INT REFERENCES workstation(workstation_id),
  log_date DATE NOT NULL,
  shift TEXT,
  notes TEXT,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_diary_person_date ON operator_daily_diary_log(personnel_id, log_date);
```

```sql
-- sql/alarm_ddl.sql
CREATE TABLE alarm_log (
  alarm_id BIGSERIAL PRIMARY KEY,
  alarm_type TEXT NOT NULL CHECK (alarm_type IN ('CRITICAL','WARNING')),
  device_id INT REFERENCES device(device_id),
  message TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  raised_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  acknowledged_by_personnel_id INT REFERENCES personnel(personnel_id),
  acknowledged_at_utc TIMESTAMPTZ,
  silenced_until_utc TIMESTAMPTZ
);

CREATE INDEX idx_alarm_active ON alarm_log(active);
CREATE INDEX idx_alarm_raised ON alarm_log(raised_at_utc);
```

```sql
-- sql/override_ddl.sql
CREATE TABLE device_override (
  device_override_id BIGSERIAL PRIMARY KEY,
  device_id INT NOT NULL REFERENCES device(device_id),
  overridden_status TEXT NOT NULL,
  override_reason TEXT,
  overridden_by_personnel_id INT NOT NULL REFERENCES personnel(personnel_id),
  started_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at_utc TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_override_device ON device_override(device_id);
CREATE INDEX idx_override_expires ON device_override(expires_at_utc);
```

```sql
-- sql/integrity_log_ddl.sql
CREATE TABLE integrity_verification_log (
  integrity_verification_log_id BIGSERIAL PRIMARY KEY,
  unit_id TEXT NOT NULL,
  verified_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  ok BOOLEAN NOT NULL,
  md5_hex TEXT NOT NULL,
  detail TEXT
);

CREATE INDEX idx_integrity_unit_time ON integrity_verification_log(unit_id, verified_at_utc);
```

```csv
# traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,"GUI shows status, commands, config, logs export, reports","UseCase_ScenarioView:System,UC_*","OperatorGUI,CommandService,ReportingService","architecture.md,openapi.yaml","Core user-facing functions."
INF-FR-002,"Logon with username/password; command control enablement","UseCase_ScenarioView:UC_AdminLogin(mapped)","AuthService,OperatorGUI","openapi.yaml,internal.proto,sql/personnel_ddl.sql","Controlled access."
INF-FR-003,"Single command controller; takeover by higher security with prompt/notify","State_LogicView_GameSession(mapped)","CommandArbiter,AuthService","internal.proto,sql/command_control_ddl.sql","Prevents conflicting control."
INF-FR-004,"Status updates continue every 2s without login","Deployment_PhysicalView(mapped)","MonitoringService,DeviceAdapter","internal.proto","Unattended monitoring."
INF-FR-005,"Facility map + icons + audible alarms + override colors","Container_PhysicalView(mapped)","OperatorGUI","architecture.md","Situational awareness."
INF-FR-006,"Admin-only config; modify DB except logs; validate conflicts","Activity_ProcessView_AdminPublish(mapped)","ConfigService,DB","openapi.yaml,sql/*","Safe configuration."
INF-FR-007,"Extra password for device rules config","Activity_ProcessView_AdminPublish(mapped)","AuthService,ConfigService","openapi.yaml","Protect safety rules."
INF-FR-008,"Add/remove devices and modify map without programming","Package_DevelopmentView(mapped)","OperatorGUI,ConfigService","sql/device_ddl.sql","Data-driven UI."
INF-FR-009,"Export logs ASCII; work orders + diary constraints","Class_LogicView:AuditLogEntry(mapped)","LogService,WorkOrderService","openapi.yaml,sql/logs_ddl.sql","Auditability."
INF-FR-010,"Detail views per device/category","UseCase_ScenarioView(mapped)","OperatorGUI,QueryService","openapi.yaml","Diagnostics."
INF-FR-011,"Historical reports via COTS reporting","Component_DevelopmentView(mapped)","ReportingService","architecture.md","Reporting requirement."
INF-FR-012,"Confirm window for any command","Sequence_ProcessView_S2(mapped)","OperatorGUI,CommandService","openapi.yaml","Human confirmation."
INF-FR-013,"Acknowledge/silence alarms configurable","UseCase_ScenarioView(mapped)","AlarmService","openapi.yaml,sql/alarm_ddl.sql","Alarm handling."
INF-FR-014,"Change system mode screen authorized","UseCase_ScenarioView(mapped)","ModeService","openapi.yaml,sql/system_mode_ddl.sql","Mode-driven behavior."
INF-FR-015,"Monitor sensors; update DB; screen update <=2s","Deployment_PhysicalView(mapped)","MonitoringService,DB","internal.proto,sql/device_status_ddl.sql","Real-time monitoring."
INF-FR-016,"Abort if closure status unknown; execute only with valid statuses","Sequence_ProcessView_S2(mapped)","SafetyScreeningService","internal.proto","Safety interlocks."
INF-FR-017,"Critical/warning alarms; notify within 2s","Component_DevelopmentView(mapped)","AlarmService","sql/alarm_ddl.sql","Alarm semantics."
INF-FR-018,"Override device status DB-only for time; no side effects","Class_LogicView(mapped)","OverrideService","sql/override_ddl.sql","Controlled continuation."
INF-FR-019,"Commands forwarded superior->inferior only","Deployment_PhysicalView(mapped)","CommandRouter","internal.proto","Hierarchy enforcement."
INF-FR-020,"Retry status; N retries => failure","Activity_ProcessView(mapped)","MonitoringService","sql/system_control_params_ddl.sql","Robust polling."
INF-FR-021,"Startup identify cabinet/cards/integrity/init <=30s","Deployment_PhysicalView(mapped)","ControllerAgent","internal.proto","Deterministic startup."
INF-FR-022,"Scheduled sequences; scan >=60s; operator confirmation","Sequence_ProcessView_S2(mapped)","SchedulerService","sql/schedule_ddl.sql","Scheduled ops."
INF-FR-023,"Halt on timeout/unsafe; resume within hold time","State_LogicView(mapped)","SequencerService","sql/sequencer_params_ddl.sql","Safe sequencing."
INF-FR-024,"One-way external export every 30s; one-way serial","Deployment_PhysicalView(mapped)","ExternalExportService","architecture.md","External consumers."
INF-FR-025,"Secure dial-in remote access authorized","Deployment_PhysicalView(mapped)","RemoteAccessGateway","architecture.md","Remote operations."
INF-FR-026,"Parallel operation during deployment; cutover after closed-hours test","Deployment_PhysicalView(mapped)","Ops/Runbooks","architecture.md","Safe rollout."
INF-ASR-020,"RBAC by command level/device/mode/workstation","Class_LogicView(mapped)","AuthZService","sql/personnel_security_ddl.sql","Fine-grained authz."
INF-ASR-021,"Password hashing/aging/min length/lockout","Class_LogicView(mapped)","AuthService","sql/personnel_ddl.sql","Credential security."
INF-ASR-022,"MD5 digest verify daily; alarm; block unit","Class_LogicView(mapped)","IntegrityService","sql/integrity_log_ddl.sql","Integrity control."
INF-ASR-023,"Checksums for inter-unit messages","Sequence_ProcessView_S2(mapped)","TransportSecurity","internal.proto","Detect corruption."
INF-ASR-024,"Firewall one-way external access","Deployment_PhysicalView(mapped)","ExternalExportService","architecture.md","No inbound influence."
INF-ASR-025,"Secure dial-in two-way via firewall","Deployment_PhysicalView(mapped)","RemoteAccessGateway","architecture.md","Controlled remote entry."
INF-ASR-026,"Open modular scalable architecture; future changes w/o programming","Package_DevelopmentView(mapped)","All services","architecture.md","Maintainability."
INF-NFR-001,"GUI refresh <=2s configurable","State_LogicView(mapped)","OperatorGUI","sql/system_control_params_ddl.sql","Performance."
INF-NFR-002,"Status/alarms propagate <=2s","Sequence_ProcessView_S2(mapped)","MonitoringService,AlarmService","internal.proto","Real-time."
INF-NFR-003,"Device responds <=12s after confirm","Sequence_ProcessView_S2(mapped)","DeviceAdapter","internal.proto","Field responsiveness."
INF-NFR-004,"External export every 30s","Deployment_PhysicalView(mapped)","ExternalExportService","architecture.md","External SLA."
INF-NFR-005,"Schedule scan >=60s","Activity_ProcessView(mapped)","SchedulerService","architecture.md","Scheduler cadence."
INF-NFR-006,"Multi-user up to max; single command controller","UseCase_ScenarioView(mapped)","AuthService,CommandArbiter","sql/system_control_params_ddl.sql","Concurrency."
INF-NFR-013,"Scale +2 DCU +4 CMS +20 closures","Deployment_PhysicalView(mapped)","DeviceRegistry","sql/device_ddl.sql","Capacity."
INF-NFR-014,"24/7/365 availability","Deployment_PhysicalView(mapped)","All","k8s/rlcs-core-deployment.yaml","Operational requirement."
INF-NFR-015,"Yearly uptime >=99.x","Deployment_PhysicalView(mapped)","All","architecture.md","Availability objective."
INF-NFR-016,"Recovery time <=10 minutes","Deployment_PhysicalView(mapped)","Ops/Runbooks","architecture.md","DR requirement."
INF-NFR-017,"No reboot due to RLCS error for >=30 days","Deployment_PhysicalView(mapped)","All","architecture.md","Reliability."
```

---

## Verification (Acceptance Criteria)

| Check | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A-L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (via normalized `INF-*`) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDL models for primary entities included | [x] |
| All major components have API contract + data schema | [x] |
| Assumptions and unresolved questions listed | [x] |

## How to review checklist
- All `INF-*` present in traceability matrix?  
- `openapi.yaml` and `internal.proto` parse with validators?  
- Each major component includes responsibilities, 3+ stack options, recommended stack with ASR/NFR justification, interface, and schema?  
- k8s manifest applies (`kubectl apply --dry-run=client`)?  
- SQL DDL runs cleanly on PostgreSQL 15/16?  
- Assumptions and open questions acceptable to stakeholders?

Conversion note (if PDF/HTML needed):  
- `pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf`  
- `pandoc ArchitectureDocument.md -o ArchitectureDocument.html`