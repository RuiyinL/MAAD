Scope: Produce production-ready RLCS (I‑15 Reversible Lane Control System) architecture doc aligned to the provided SRS narrative and the 11 provided UML views.  
Approach: Normalize narrative requirements into traceable INF-* IDs, design a safety‑critical, layered-interlock control plane with deterministic sequencing, HA, and one-way external data export.  
Validation: Ensure traceability matrix coverage, API/contract/schema syntactic validity, and safety/performance SLO test hooks (2s freshness, 12s command windows, RTO≤10m).

# A. Executive Summary (≤1 page)

## System overview
RLCS opens/closes reversible lanes (and controls closure devices, CMS signs, alarms) via operator-confirmed sequences and direct device commands, with strict safety interlocks to prevent wrong-way openings and catastrophic gate mis-operations. The system continuously monitors field device sensors and controllers, displays updates within 2 seconds, logs/audits all actions, supports degraded/alternate control, and exports read-only status to external systems via a one-way DMZ mechanism every 30 seconds.

**Primary diagrams**:  
- Scenario View — Use Case Diagram: `UseCaseView` (e.g., UC_OperateLanes, UC_Safety)  
- Process View — Activity Diagram: `ActivityView` (IntegrityCheck, SafetyCheck, Hierarchy)  
- Physical View — Deployment Diagram: `DeploymentView` (N_APP_A/B, N_DB, N_TSU/FCU/DCU, N_DMZ)

## Architectural style(s)
- **Event-driven modular monolith (microkernel-style) + deterministic state machines** for sequencing and safety screening (ref: ComponentView: C_SEQ, C_SAFE, C_BUS; StateView: Seq).  
- **Hierarchical command forwarding** TSU→FCU→DCU with safety screening at each hop (ref: ContainerView: CT_TSU/CT_FCU/CT_DCU; ActivityView: Hierarchy).

## Deployment topology
- **Private LAN control plane with HA app servers + DB cluster + field controller tier + DMZ one-way export** (ref: DeploymentView: N_APP_A/B, N_DB, N_FIELD, N_DMZ).

## Top 3 design risks & mitigations

| Risk | Why it matters | Mitigation (concrete) |
|---|---|---|
| R1: Undefined controller/I/O driver specifics (“unknown controller”) | Integration failure blocks field readiness; safety-critical | Define **HardwareIO Adapter API v1.x** + simulation harness + conformance tests; implement pluggable drivers (ComponentView: C_HW). |
| R2: Safety-rule correctness & bypass risk | Wrong-way opening is catastrophic | Multi-layer safety screening at origin + every subordinate + executing controller; halt/hold/resume state machine with 3s snapshot freshness (StateView: Seq; ComponentView: C_SAFE). |
| R3: Availability & degraded-mode control continuity | 24/7; RTO ≤10 min; alternate control requirements | Active/standby app tier, DB HA, controller NV rule replication; explicit degraded-mode workflows and dial-in access controls (DeploymentView: N_APP_A/B; UseCaseView: UC_Degraded). |

## Key QA coverage mapping (ASR/NFR → tests)

| Quality attribute | Requirements (INF-*) | Test types |
|---|---|---|
| Scalability | INF-NFR-10 (scale to +2 DCUs, +4 CMS, +20 closures), INF-NFR-11 (max users) | Load, soak, capacity planning, HPA validation |
| Availability | INF-NFR-01 (24/7), INF-NFR-02 (RTO≤10m, ≥99.x uptime), INF-NFR-03 (30-day no reboot) | HA failover drills, chaos, soak (30+ days) |
| Security | INF-ASR-05 (one-way DMZ export), INF-ASR-08 (single command control), INF-ASR-07 (hash integrity), INF-NFR-15 (no wireless) | Pen-test, config review, RBAC tests, network policy tests |
| Performance | INF-NFR-06/07/08/09 (2s updates/alarms), INF-NFR-12 (12s device response window) | Latency SLI tests, HIL timing tests, end-to-end timing |
| Maintainability | INF-NFR-13 (future roadway changes no code), INF-FR-14/15 (GUI config + conflict detection) | Config regression tests, schema migration tests, simulator validation |

---

# B. Traceability & Rationale

Because the provided SRS text does not include stable IDs, all requirements are normalized as `INF-*` (inferred) and mapped below.

**CSV/table fields**: `Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale`

```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-01,GUI provides logon (username/password),UseCaseView:UC_LogOn; ComponentView:C_GUI+C_AUTH,AuthService RLCS GUI,openapi.yaml; internal.proto,Enforces authenticated access for all actions; maps to login workflows and RBAC.
INF-FR-02,GUI shows date/time/user/workstation and other logged-in users,UseCaseView:UC_ViewStatus; ActivityView:Display live status,TelemetryBus RLCS GUI,openapi.yaml,Supports operator situational awareness and multi-user visibility while enforcing command control lease.
INF-FR-03,Only one operator holds command control at a time (lease),UseCaseView:UC_CommandControl; ClassView:CommandLease; ComponentView:C_LEASE,LeaseManager,internal.proto; sql/command_lease_ddl.sql,Prevents conflicting commands; supports takeover flow with audit.
INF-FR-04,Command control only from specified workstations,UseCaseView:UC_CommandControl; ClassView:Workstation; Security section,AuthService LeaseManager,sql/workstation_ddl.sql; internal.proto,Implements workstation allow-list and authorization checks.
INF-FR-05,Higher-security user can take over command control with prompt/notification,UseCaseView:UC_Takeover; ActivityView:Takeover,LeaseManager AuditLogService,internal.proto; sql/audit_log_ddl.sql,Ensures controlled escalation while maintaining accountability.
INF-FR-06,GUI status continues with no logged-in user and updates every 2 seconds,ActivityView:Display live status; ComponentView:C_BUS; DeploymentView:N_WS,TelemetryBus RLCS GUI,internal.proto; k8s/applicationservice-deployment.yaml,Meets strict freshness requirements via push telemetry and polling fallback.
INF-FR-07,Visual + audible alarms; configurable; auto-clear when resolved,UseCaseView:UC_ViewStatus; ComponentView:C_BUS; Observability,GW+TelemetryBus RLCS GUI,internal.proto; sql/alarm_log_ddl.sql,Alarms must be timely and actionable; auto-clear reduces operator burden.
INF-FR-08,Override device status with different display color,UseCaseView:UC_Override; Sequence_OverrideAndResume,SequenceEngine SafetyService,openapi.yaml; sql/device_override_ddl.sql,Override enables continuation with explicit marking and time-bounded behavior.
INF-FR-09,Show active overrides and devices lacking rules protection,UseCaseView:UC_ViewStatus,RLCS GUI SafetyService,openapi.yaml,Highlights risk posture to operator; required for safety awareness.
INF-FR-10,Facility map configurable without programming; devices add/remove without code,UseCaseView:UC_Configure; PackageView:UI+ConfigService,ConfigService,sql/ui_map_config_ddl.sql,Data-driven map/device metadata avoids code changes for future roadway modifications.
INF-FR-11,Configuration only accessible by admin; can edit all tables except logs,UseCaseView:UC_Configure; ComponentView:C_CONFIG,ConfigService AuthService,openapi.yaml; internal.proto,Separates mutable configuration from immutable logs and enforces privileges.
INF-FR-12,Config screen shows impacted units for changes,UseCaseView:UC_Configure; ClassView:ConfigChange,ConfigService RLCS GUI,openapi.yaml,Reduces operational errors by making scope explicit before apply.
INF-FR-13,Changing device rules requires extra password (step-up auth),UseCaseView:UC_StepUp; Security design,AuthService,openapi.yaml,Adds defense-in-depth for safety-critical rule edits.
INF-FR-14,GUI validates config conflicts/redundancy before save,UseCaseView:UC_Configure; ComponentView:C_CONFIG,ConfigService,internal.proto; sql/config_version_ddl.sql,Prevents invalid schedules/rules and supports safe operations.
INF-FR-15,Logs view/export to ASCII; diary/work order editable/exportable,UseCaseView:UC_Logs+UC_WorkDiary; ComponentView:C_AUDIT,AuditLogService Reporting,openapi.yaml; sql/daily_diary_ddl.sql; sql/problem_work_order_ddl.sql,Supports auditability and operational recordkeeping with export compatibility.
INF-FR-16,Detail device status at sensor level and by category,UseCaseView:UC_ViewStatus,RLCS GUI TelemetryBus,openapi.yaml,Supports diagnostics and maintenance decisions.
INF-FR-17,Retrieve historic reports via COTS reporting,UseCaseView:UC_Logs; PackageView:INFRA,Reporting subsystem,Architecture doc section D,Isolates report workload from control path while meeting reporting requirements.
INF-FR-18,Confirmation popup for any command (manual or scheduled),UseCaseView:UC_OperateLanes; ActivityView:HITL,RLCS GUI SequenceEngine,openapi.yaml,Ensures human-in-the-loop for safety-critical execution.
INF-FR-19,Acknowledge alarm; silence audible per device for configurable time/permanently,UseCaseView:UC_ViewStatus,RLCS GUI,openapi.yaml; sql/alarm_ack_ddl.sql,Supports alarm fatigue management while preserving visual indicators.
INF-FR-20,Diagnostic screen to diagnose failed devices at sensor level,UseCaseView:UC_ViewStatus,RLCS GUI ControllerGateway,openapi.yaml; internal.proto,Provides structured diagnostics access without bypassing safety controls.
INF-FR-21,Authorized users can change system mode,UseCaseView:UC_Configure; ActivityView:Scheduler,ConfigService AuthService,openapi.yaml; sql/system_mode_ddl.sql,Mode affects polling rates and scheduling; must be controlled.
INF-FR-22,Monitor all device sensors; update screen <=2s; update DB,ActivityView:Display live status; DeploymentView:N_FIELD,ControllerGateway TelemetryBus DB,internal.proto; sql/device_status_ddl.sql,Core monitoring loop must meet latency constraints.
INF-FR-23,Integrity checks: abort if any closure status unknown; valid status required for commands,StateView:SafetyScreening; Requirements section,SafetyService SequenceEngine ControllerGateway,internal.proto,Prevents unsafe commands when state is uncertain.
INF-FR-24,Critical/warning alarm conditions as specified (logins, overrides, power loss, cabinet ID change, etc.),Observability section; Data model AlarmType,IntegrityService Alarm evaluation,sql/alarm_log_ddl.sql; internal.proto,Encodes alarm taxonomy and triggers into rule-based evaluation and persistence.
INF-FR-25,If critical alarm during open/close, show possible actions guidance,ActivityView:DecisionSupport,SequenceEngine RLCS GUI,openapi.yaml,Operator guidance improves recovery and reduces unsafe improvisation.
INF-FR-26,MCU must be Auto to process commands,StateView:SafetyScreening,ControllerGateway HardwareIO Adapter,internal.proto,Ensures manual mode prevents remote actuation and reduces unsafe automation.
INF-FR-27,Override affects only database value (no field command),Sequence_OverrideAndResume,SequenceEngine DB,internal.proto; sql/device_override_ddl.sql,Meets definition of override and preserves physical control semantics.
INF-FR-28,Safety rules stored in non-volatile memory and validated at each unit; superior-to-inferior forwarding only,ActivityView:Hierarchy; DeploymentView:N_TSU/N_FCU/N_DCU,ControllerGateway SafetyService,internal.proto,Distributed interlocks avoid single-point bypass and enforce command hierarchy.
INF-FR-29,Retry device status requests; configurable retries before declare failure,ControllerGateway design,ControllerGateway,internal.proto; sql/system_control_parameters_ddl.sql,Improves robustness to transient comm failures and standardizes failure detection.
INF-FR-30,Startup: identify unit via cabinet ID; verify cards; integrity check; init tables; <=30s,ControllerGateway startup,ControllerGateway IntegrityService,internal.proto; sql/integrity_report_ddl.sql,Ensures deterministic boot and prevents unsafe operation on partial hardware.
INF-FR-31,Controllers send current status upward every 2s (or mode param),DeploymentView:N_FIELD; NFR timing,ControllerGateway TelemetryBus,internal.proto,Meets 2-second monitoring and multi-unit state replication.
INF-FR-32,Future facility changes without programming effort (e.g., number of closure devices),PackageView:Config; INF-FR-10,ConfigService,sql/device_ddl.sql,Data-driven configuration enables scaling and changes.
INF-FR-33,Generate logs: device command log (incl failed/aborted), system op log, alarm log, diary, work order, schedules,UseCaseView:UC_Audit; ClassView:AuditLogEntry,AuditLogService,sql/audit_log_ddl.sql; openapi.yaml,Provides complete accountability and reporting inputs.
INF-FR-34,Execute stored operational sequences by mode+schedule; initial sequences in Appendix F,StateView:Seq; ActivityView:Scheduler,SequenceEngine Scheduler,sql/sequence_schedule_ddl.sql,Implements scheduled operations with confirmation gates.
INF-FR-35,Check schedule at least every 60s,ActivityView:Scan scheduled events,SequenceEngine Scheduler,internal.proto,Meets schedule responsiveness requirement.
INF-FR-36,Halt sequences on timeouts or unexpected state changes; resume within correction window,StateView:Halted->Executing; Sequence_OverrideAndResume,SequenceEngine SafetyService,sql/system_control_parameters_ddl.sql,Deterministic halt/hold/resume prevents unsafe continuation and supports recovery.
INF-FR-37,Store/process/retrieve operational data + reports + export status to external server,UseCaseView:UC_ExportStatus; ComponentView:C_EXPORT,ExternalExportService DB,openapi.yaml; sql/external_export_ddl.sql,Supports internal ops and external read-only visibility.
INF-FR-38,COTS DBMS used (e.g., Oracle 8i referenced),PackageView:INFRA; DeploymentView:N_DB,DBMS layer,Architecture doc section D,DB supports consistency and reporting; vendor choice must meet latency.
INF-ASR-01,Multi-layer safety screening using <=3s-old config snapshot,StateView:SafetyScreening; ClassView:FacilityStatusSnapshot,SafetyService SequenceEngine,internal.proto,Directly implements safety screening freshness and layered enforcement.
INF-ASR-02,Valid checksum algorithms for inter-unit messages,DeploymentView links (checksum),ControllerGateway,internal.proto,Prevents message corruption and supports integrity assurance on private links.
INF-ASR-03,Event-driven telemetry push to meet <=2s UI/alarms,ComponentView:C_BUS; ContainerView:CT_BUS->CT_GUI,TelemetryBus,internal.proto,Decouples device polling from GUI refresh and supports bounded latency.
INF-ASR-04,One-way external export via firewall/DMZ every 30s; no inbound inputs,UseCaseView:UC_ExportStatus; DeploymentView:N_DMZ,ExternalExportService,openapi.yaml; sql/external_export_ddl.sql,Meets one-way transfer and isolation.
INF-ASR-05,Secure remote dial-in via firewall modem; two-way for authorized remote users,UseCaseView:RemoteUser; DeploymentView dial-in implied,AuthService VPN/dial-in gateway,Security section,Supports remote operations while keeping external systems read-only.
INF-ASR-06,Pluggable controller/I-O driver interface (2070 ATC or equivalent),ComponentView:C_HW note,HardwareIO Adapter ControllerGateway,internal.proto,Abstracts hardware differences and enables vendor controller selection.
INF-ASR-07,MD5 message-digest integrity verification daily; alarm and disable unit on failure,ClassView:IntegrityReport; IntegrityService,IntegrityService AuditLogService,sql/integrity_report_ddl.sql,Implements required integrity checks; see security conflict note in K.
INF-ASR-08,Passwords hashed; password aging; min username/password lengths configurable,Security design; SystemControlParameters,AuthService,sql/system_control_parameters_ddl.sql; openapi.yaml,Enforces credential policies and reduces compromise risk.
INF-NFR-01,Availability 24/7/365,DeploymentView:HA,All services,k8s/applicationservice-deployment.yaml,Drives HA and operational readiness.
INF-NFR-02,Uptime >=99.x and recovery time <=10 minutes,DeploymentView:N_APP_A/B; Ops section,App HA+DB HA,Runbooks,Requires failover automation and tested RTO.
INF-NFR-03,Continuous operation without reset/reboot due to RLCS error for >=30 days,Soak testing,H testing plan,Soak/chaos test plan,Validates memory leaks and stability under long runs.
INF-NFR-04,Status and alarms visible within 2 seconds,ActivityView notes; ContainerView CT_BUS,TelemetryBus GUI,Prometheus SLOs,Performance-critical display freshness.
INF-NFR-05,Detect alarms within 2 seconds,Observability design,Alarm evaluator,Prometheus rules,Requires near-real-time evaluation at controllers and/or control plane.
INF-NFR-06,Controllers send status every 2 seconds or less,DeploymentView:N_FIELD note,ControllerGateway,internal.proto,Ensures distributed consistency and safety screening.
INF-NFR-07,GUI status update <=2 seconds excluding network/device,ActivityView; Performance section,TelemetryBus GUI,Load tests,Defines latency SLI boundary conditions.
INF-NFR-08,Device status received from sensors within 2 seconds of issuance,Field tier; HIL,ControllerGateway,Test plan,Validates controller polling and sensor acquisition.
INF-NFR-09,Field devices respond within 12 seconds of operator confirmation,StateView timeout 12s,SequenceEngine ControllerGateway,Test plan,Defines command response window.
INF-NFR-10,Scale to +2 DCUs each like DCU1 + 4 CMS + 20 contact closures,Deployment scaling,ControllerGateway HardwareIO,Capacity plan,Ensures architecture supports growth without redesign.
INF-NFR-11,Support multiple concurrent users up to DB-defined max; only one command controller,UseCaseView note; ClassView:CommandLease,AuthService LeaseManager,sql/system_control_parameters_ddl.sql,Separates monitor sessions from command-control holder.
INF-NFR-12,Database performance must not violate 2s UI/control requirements,Ops+DB design,DBMS+Caching,Load test gates,Requires indexing, partitioning, and isolation of reporting.
INF-NFR-13,Comms failover fiber primary / ISDN secondary transparent to app,DeploymentView note,Network+ControllerGateway,Runbooks,Network-level redundancy; app must tolerate link transitions.
INF-NFR-14,No wireless FCU-DCU connections allowed,DeploymentView note,Network design,Network policies,Reduces interference and security risk.
INF-NFR-15,Degraded mode behavior: alternate control at FCUs/DCUs; laptop direct control,UseCaseView:UC_Degraded,ControllerGateway RLCS GUI,Runbooks+procedures,Ensures continuity when higher tiers fail.
INF-NFR-16,External systems read RLCS status from server outside RLCS network; single file schema,UseCaseView:UC_ExportStatus,ExternalExportService,openapi.yaml; sql/external_export_ddl.sql,Meets integration contract and isolation.
INF-NFR-17,One-way serial data transfer provided,External export integration,ExternalExportService serial adapter,Architecture section D,Implements second outbound-only channel.
INF-NFR-18,Audit logs track all application activity; not editable,ClassView:AuditLogEntry,AuditLogService,sql/audit_log_ddl.sql,Ensures accountability and supports investigations.
INF-NFR-19,Parallel operation during deployment; cutover after successful closed-hours test,Migration plan,Rollout plan,Migration runbook,Reduces field risk during transition.
INF-NFR-20,Remote system administration and maintenance supported,UseCaseView:Admin+RemoteUser,Ops+Security,Runbooks,Supports field ops and admin without onsite presence.
INF-NFR-21,Open architecture modular and scalable; open standards preferred,PackageView/ComponentView,All components,This document,Ensures long-term maintainability and vendor flexibility.
```

---

# C. Architecture Overview

## 4+1 alignment

### Context (Scenario view)
Actors: Operator, System Administrator, Maintenance User, Remote User, External Systems. Core use cases include Log On, View Status, Acquire Command Control, Execute Open/Close Sequence, Override Device Status, Configure System, Review/Export Logs, Export Status Data, Degraded/Alternate Control (ref: **UseCaseView**: UC_OperateLanes, UC_Safety, UC_ExportStatus).

### Container view
- **TMC Workstation** runs RLCS GUI.  
- **Control Plane (Private LAN)** hosts ApplicationService, SequenceEngine, SafetyService, LeaseManager, AuthService, AuditLogService, ConfigService, IntegrityService, TelemetryBus, and RLCS DBMS (ref: **ContainerView**: CT_GUI, CT_SEQ, CT_SAFE, CT_DB).  
- **Field Control Tier** includes TSU/FCU/DCU controllers and HardwareIO Adapter with non-volatile safety rules (ref: **DeploymentView**: N_TSU/N_FCU_N/N_FCU_S/N_DCU).  
- **DMZ** hosts external status datastore and export service (ref: **DeploymentView**: N_DMZ, N_EXTSRV).

### Component/Package view
Packages: `ui`, `application`, `domain`, `infrastructure`, `integrations`, `security`, `observability` (ref: **PackageView**). Components: C_GUI, C_APP, C_SEQ, C_SAFE, C_LEASE, C_AUTH, C_BUS, C_AUDIT, C_CONFIG, C_INTEG, C_EXPORT, C_GATE, C_HW (ref: **ComponentView**).

### Class/Runtime view
Core domain objects: Session, CommandLease, ControlCommand, Device, SafetyRuleSet, FacilityStatusSnapshot, Sequence, AuditLogEntry, IntegrityReport (ref: **ClassView**). Runtime sequencing uses the deterministic state machine (ref: **StateView**: Seq).

### Deployment view
HA app tier (Server A + hot standby B), DBMS cluster, private field network with fiber/ISDN failover, DMZ one-way export path (ref: **DeploymentView**: N_APP_A/B, N_DB, N_FIELD, N_DMZ).

---

# D. Detailed Technical Design (developer-facing)

## D1. Subsystem: RLCS GUI (Workstation UI)

### 1) Responsibilities & data ownership
Renders facility map/status/alarms, provides login, command-control acquisition, command confirmations, configuration screens (admin-only), log viewing/export, work order and diary entry. Owns **no authoritative state**; it consumes telemetry and issues commands to the control plane.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: TypeScript (`Node.js 20.x`) for UI + thin local client  
- Conservative: C# (`.NET 8`) WPF/WinForms thick client (closer to legacy Windows environments)  
- Cutting-edge: Rust + Tauri desktop UI

**Web framework / UI shell**
- Recommended: React 18 + Vite  
- Conservative: Angular 17 LTS  
- Cutting-edge: SvelteKit

**RPC/HTTP**
- Recommended: HTTPS REST to control plane + WebSocket/SSE for telemetry  
- Conservative: SOAP/legacy RPC (not recommended for new)  
- Cutting-edge: gRPC-web

**Authn/AuthZ**
- Recommended: OIDC Authorization Code + PKCE  
- Conservative: LDAP/AD bind + app session cookies  
- Cutting-edge: Passkeys/WebAuthn (operator constraints may limit)

**Observability**
- Recommended: OpenTelemetry JS (spans for user actions)  
- Conservative: basic file logs  
- Cutting-edge: eBPF-based client telemetry (not typical on workstations)

### 3) Recommended default stack
- React 18 + TypeScript, Node.js 20; telemetry via WebSocket; REST for commands.  
Justification: meets **INF-NFR-04** (<=2s status/alarms) by using push telemetry rather than UI polling.

### 4) Interface design
Uses `openapi.yaml` endpoints and subscribes to `/v1/telemetry/stream`.

### 5) Data model / schema
GUI stores only ephemeral local preferences; persisted configuration belongs in RLCS DB via ConfigService.

### 6) Caching & consistency
Client caches latest snapshot in memory (TTL 5s) only for rendering; authoritative state remains server/controller.

---

## D2. Subsystem: ApplicationService (Use-case orchestration)

### 1) Responsibilities & data ownership
Orchestrates user-facing workflows: login session management, command confirmation, delegating to SequenceEngine, config CRUD, audit writes, integrity checks initiation, and external export triggering. Owns **application workflow state**, not device truth.

### 2) Technology options

**Language/runtime**
- Recommended: Java 21 (LTS)  
- Conservative: .NET 8  
- Cutting-edge: Go 1.22

**Web framework**
- Recommended: Spring Boot 3.3.x  
- Conservative: ASP.NET Core 8  
- Cutting-edge: Quarkus 3.x

**Persistence**
- Recommended: PostgreSQL 15-16  
- Conservative: Oracle 19c-21c (more aligned to “Oracle” reference, but not 8i)  
- Cutting-edge: YugabyteDB (Postgres-compatible distributed SQL)

**Cache**
- Recommended: Redis 7.2 (for ephemeral leases, rate-limits)  
- Conservative: in-DB only  
- Cutting-edge: KeyDB / Dragonfly

**Messaging**
- Recommended: NATS JetStream 2.10+ (low-latency pub/sub)  
- Conservative: RabbitMQ 3.13  
- Cutting-edge: Redpanda/Kafka

**Authn/AuthZ**
- Recommended: Keycloak 24-25 (OIDC)  
- Conservative: local RBAC tables only  
- Cutting-edge: SPIFFE/SPIRE identity everywhere

**Observability**
- Recommended: OpenTelemetry + Prometheus + Loki  
- Conservative: ELK only  
- Cutting-edge: Grafana Alloy end-to-end pipelines

**CI/CD**
- Recommended: GitHub Actions or GitLab CI, with SAST/DAST gates  
- Conservative: Jenkins  
- Cutting-edge: Tekton + policy-as-code (OPA)

**Container runtime**
- Recommended: Kubernetes 1.29-1.31 with containerd  
- Conservative: VM-based systemd services  
- Cutting-edge: Nomad

**Infra provisioning**
- Recommended: Terraform 1.6+  
- Conservative: manual ops  
- Cutting-edge: Crossplane

### 3) Recommended default stack
- Java 21 + Spring Boot 3.3; PostgreSQL 15-16; Redis 7.2; NATS JetStream 2.10+.  
Justification: meets **INF-NFR-12** (DB latency must not break 2s UI/control) by using indexing + event push and minimizing synchronous DB dependence on the hot path.

### 4) Interface design (External APIs — OpenAPI)
See `openapi.yaml` in Section L.

### 5) Data model / schema
See SQL DDL artifacts in Section L (users, sessions, leases, audit logs, devices, sequences, alarms, overrides).

### 6) Caching & consistency
- Cache: current FacilityStatusSnapshot in Redis (TTL 3s) for safety screening freshness.  
- Strong consistency: command lease acquisition uses DB row lock + unique constraint; audit log append-only.

---

## D3. Subsystem: SequenceEngine (Sequencing / state machine)

### 1) Responsibilities & data ownership
Executes stored operational sequences (open/close), enforces confirmation, manages sequence state (idle/pending/executing/halted), evaluates timing windows (12s device response), and coordinates multi-hop command dispatch TSU→FCU→DCU. Owns **sequence execution state** and step transitions.

### 2) Technology options

**Language/runtime**
- Recommended: Java 21 (share domain libs)  
- Conservative: C++ (determinism, but higher dev risk)  
- Cutting-edge: Rust (safety, but ecosystem overhead)

**State machine**
- Recommended: explicit persisted state machine (table-driven)  
- Conservative: in-code if/else with heavy tests  
- Cutting-edge: formal model checking integration (TLA+/Alloy) in CI

**Messaging**
- Recommended: NATS for telemetry + command events  
- Conservative: DB polling  
- Cutting-edge: Kafka with exactly-once semantics

### 3) Recommended default stack
- Java 21 + persisted state machine + NATS JetStream.  
Justification: meets **INF-FR-36** (halt/hold/resume) by using explicit persisted sequence states and event-driven transitions.

### 4) Internal contracts
See `internal.proto` in Section L (`SequenceService`, `ControllerGateway`).

### 5) Data model / schema
`sql/sequence_schedule_ddl.sql`, `sql/system_operation_log_ddl.sql`.

### 6) Caching & consistency
- Uses snapshot caching with max age 3 seconds for safety screen (reject stale).  
- Commands are idempotent by `command_id`; retries do not duplicate device actuation.

---

## D4. Subsystem: SafetyService (Interlocks / rule evaluation)

### 1) Responsibilities & data ownership
Evaluates safety rules before any device state-changing command (and before executing each step), enforcing “abort on unknown/opposite open” and rule-set constraints. Owns **rule evaluation results**, not rule truth (rules stored in DB and replicated to NV memory in controllers).

### 2) Technology options

**Rule engine**
- Recommended: deterministic in-code evaluator + versioned rules tables  
- Conservative: Drools (powerful, but complexity)  
- Cutting-edge: Cedar/OPA policy engine

**Snapshot source**
- Recommended: last-known-good snapshot from DB/telemetry, capped at 3s age  
- Conservative: direct controller query each time  
- Cutting-edge: CRDT/state replication mesh

### 3) Recommended default stack
- In-code evaluator + versioned DB tables + controller NV replication.  
Justification: meets **INF-ASR-01** (multi-layer safety screening, <=3s snapshot) with deterministic evaluation and explicit staleness checks.

### 4) Interfaces
`internal.proto` `SafetyService.Evaluate()` and `ControllerGateway.SafetyScreenLocal()`.

### 5) Data model / schema
`sql/device_rules_ddl.sql`, `sql/safety_rule_set_version_ddl.sql`.

### 6) Caching & consistency
Cache compiled rules by `ruleset_version` (TTL 60s) but enforce snapshot freshness at evaluation time.

---

## D5. Subsystem: ControllerGateway + HardwareIO Adapter (Field integration)

### 1) Responsibilities & data ownership
Implements hierarchical forwarding and controller communication, checksums on messages, retries on status polls, and dispatches to I/O driver software. HardwareIO Adapter provides a stable API for different controller hardware (2070 ATC or equivalent). Owns **transport/session state** with controllers; device truth originates from sensors/controllers.

### 2) Technology options

**Controller comm protocol**
- Recommended: TCP with application-level checksum (CRC32C/HMAC depending on security zone)  
- Conservative: serial RS-232 framing  
- Cutting-edge: QUIC

**Driver abstraction**
- Recommended: C ABI + gRPC sidecar for HardwareIO calls  
- Conservative: direct vendor SDK calls (lock-in)  
- Cutting-edge: WASM plugin sandbox for drivers

**Runtime**
- Recommended: Go 1.22 (simple concurrency, small footprint)  
- Conservative: Java  
- Cutting-edge: Rust

### 3) Recommended default stack
- Go 1.22 for gateway/adapter with strict interface versioning.  
Justification: meets **INF-ASR-06** (pluggable I/O driver/controller) by keeping a narrow, versioned HardwareIO API.

### 4) Interfaces
`internal.proto` includes `ControllerGateway` and `HardwareIo` services.

### 5) Data model / schema
Minimal persistence: controller health and last-seen in DB (`sql/controller_health_ddl.sql`).

### 6) Caching & consistency
Maintain per-controller last status; mark unknown on missed polls beyond retries (configurable).

---

## D6. Subsystem: AuthService + LeaseManager + AuditLogService + IntegrityService

### 1) Responsibilities & data ownership
- AuthService: authenticate/authorize users, workstation allow-list, password policy.  
- LeaseManager: single command-control lease, takeover workflow.  
- AuditLogService: immutable append-only audit records (commands, logins, config changes).  
- IntegrityService: periodic message-digest verification and recording, alarm on failure, disable unit from control.

### 2) Technology options (selected highlights)

**Auth**
- Recommended: OIDC (Keycloak) + local RBAC mapping  
- Conservative: DB-only auth  
- Cutting-edge: mTLS identities for all users (not feasible)

**Audit immutability**
- Recommended: append-only table + hash chain per day + WORM backups  
- Conservative: plain logs  
- Cutting-edge: external ledger (immudb)

**Integrity hashing**
- Recommended: implement MD5 where mandated, but wrap with SHA-256 for operational assurance (see K conflict)  
- Conservative: MD5 only  
- Cutting-edge: TPM-based attestation

### 3) Recommended default stack
- Keycloak OIDC + DB RBAC + append-only audit with hash chaining.  
Justification: meets **INF-NFR-18** (audit logs not editable) and **INF-FR-03** (single command control).

---

## D7. Subsystem: ExternalExportService (DMZ, one-way)

### 1) Responsibilities & data ownership
Produces a single status file every 30 seconds with required schema fields (status, customers, access points, sign messages). Pushes outbound-only to DMZ datastore; also supports one-way serial export.

### 2) Technology options
- Recommended: file drop (JSON) + atomic rename on DMZ share  
- Conservative: CSV file drop  
- Cutting-edge: signed CBOR payloads

### 3) Recommended default stack
- JSON file drop + atomic publish + optional signature.  
Justification: meets **INF-ASR-04** (outbound-only export every 30s; no inbound inputs).

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/applicationservice-deployment.yaml` in Section L.  
Justification: meets **INF-NFR-01** (24/7) via orchestration self-healing and replicas.

## E2. DB HA topology, backups, restore
- PostgreSQL HA (Patroni or managed HA): 3 nodes, synchronous replication to 1 standby.  
- Backups: nightly full + WAL continuous; retain 35 days online + 1 year cold storage for compliance if required.  
- Restore drills: quarterly, target RTO ≤ 10 minutes for app failover; DB restore RTO depends on incident type.

Justification: meets **INF-NFR-02** (RTO≤10m, uptime) and **INF-NFR-12** (DB must not break latency) by using HA + tuned replication.

## E3. Network topology + ingress/egress rules
- Private LAN: only GUI→ControlPlane, ControlPlane→Field, ControlPlane→DMZ outbound.  
- DMZ: external systems read-only; **no inbound path to RLCS** (ref: DeploymentView: N_DMZ).  
- Field: fiber primary, ISDN secondary; **no wireless FCU↔DCU** (ref: DeploymentView note).

Justification: meets **INF-NFR-14** (no wireless) and **INF-ASR-04** (one-way external).

## E4. CI/CD sketch
1. Build + unit tests + static analysis  
2. Contract tests (OpenAPI + proto lint + backward-compat gates)  
3. Integration tests with simulator (HardwareIO mock)  
4. HIL tests in staging for timing (2s/12s windows)  
5. Canary deploy to App Server B then promote (blue/green)  
6. Post-deploy SLO gate (latency, alarm freshness)

Justification: meets **INF-NFR-03** (30-day stability) via soak gates and regression prevention.

---

# F. Security Design

## F1. Auth & AuthZ
- OIDC (Authorization Code + PKCE) for GUI users; short-lived access tokens (5-15 min), refresh tokens (8-12 hrs) with revocation.  
- RBAC + attribute-based checks for Command Level, Device, Mode, Workstation, Remote access.

Justification: meets **INF-ASR-08** (password policy/length/aging) and **INF-FR-04** (workstation restrictions).

## F2. Secrets management & rotation
- Kubernetes Secrets sealed with SOPS; rotate DB creds quarterly; rotate signing keys annually or on incident.

Justification: meets **INF-NFR-20** (remote admin) by enabling secure operational handling of credentials.

## F3. TLS & service mesh
- TLS everywhere on private LAN; optional service mesh (Istio/Linkerd) for mTLS between services.

Justification: meets **INF-ASR-02** (integrity of inter-unit messages) by adding transport protection in addition to checksums.

## F4. Threat model (top 5)
1. Unauthorized command issuance → RBAC + command lease + workstation allow-list + audit.  
2. Replay/tamper of controller messages → checksums + sequence numbers + allow-list.  
3. Compromise of admin config (rules) → step-up auth + change control + simulator gate.  
4. DMZ pivot into RLCS → one-way export + firewall rules + no inbound services.  
5. Insider log tampering → append-only audit + hash chain + WORM backups.

---

# G. Observability & SRE

## G1. Metrics/logs/traces
- Metrics: telemetry freshness (seconds), command latency, sequence halt counts, alarm detection latency, controller last-seen, DB query p95.  
- Logs: structured JSON with correlation IDs; audit logs separate immutable store.  
- Tracing: OpenTelemetry spans for command flows TSU→FCU→DCU.

Justification: meets **INF-NFR-05** (alarm detect within 2s) by measuring and alerting on alarm latency.

### Example Prometheus alert rules
```promql
# Alarm detection latency > 2s (p95 over 5m)
histogram_quantile(0.95, sum(rate(rlcs_alarm_detect_latency_seconds_bucket[5m])) by (le)) > 2
```
```promql
# Telemetry freshness breached (no update in >2s) for any controller for 10s
max_over_time(rlcs_controller_last_update_age_seconds[10s]) > 2
```

## G2. SLOs, error budgets, RTO/RPO
- SLO: 99.9% monthly availability for control plane (pending stakeholder confirmation vs 99.x).  
- SLO: p95 UI freshness ≤ 2.0s.  
- RTO: ≤10 minutes for app-tier failure; RPO: ≤5 seconds for operational state (audit RPO 0 preferred).

Justification: meets **INF-NFR-02** (RTO≤10m) via HA and failover drills.

## G3. Dashboards/runbooks (sketch)
- Dashboard panels: sequence state distribution; halted reasons; controller connectivity; alarm rate by type; DB p95 latency.  
- Runbooks: “FCU down”, “DB failover”, “Telemetry stale”, “Integrity verification failure”.

---

# H. Testing Strategy

## H1. Test matrix

| Test type | Components | Focus |
|---|---|---|
| Unit | SafetyService, SequenceEngine | Rule evaluation, state transitions, timeout logic |
| Integration | AppService↔DB, AppService↔NATS | API correctness, persistence, event delivery |
| Contract | OpenAPI, internal.proto | Backward compatibility, schema validation |
| E2E | GUI→Command→TSU→FCU→DCU simulator | 2s freshness, 12s command window, halt/resume |
| Chaos/Failover | App HA, DB HA | RTO≤10m, degraded mode behaviors |

Justification: meets **INF-FR-36** (halt/resume) with E2E and state-machine tests.

## H2. Test data & environments
- Environments: dev, integration, staging(sim), staging(HIL), production.  
- Refresh: nightly anonymized config snapshots; never overwrite production audit logs.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. High-level steps
1. Stand up new RLCS control plane in parallel with existing system (facility closed-hours test).  
2. Integrate controllers via HardwareIO simulation first, then staged HIL.  
3. Dual-run monitoring (read-only) for N days; compare telemetry and alarms.  
4. Cutover control authority during closed period; retain rollback (reconnect old system).  

Justification: meets **INF-NFR-19** (parallel operation and cutover after successful test).

## I2. Backward compatibility & versioning
- External export file includes `schemaVersion`; keep N-1 schema for 90 days.  
- Internal proto uses `reserved` fields and semantic versioning.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| DBMS PostgreSQL vs Oracle | Oracle aligns with legacy mention; Yugabyte distributed | Oracle licensing/ops complexity; Yugabyte adds complexity | PostgreSQL meets latency/HA needs with open ops; aligns with modular architecture (**INF-NFR-12**). |
| Messaging NATS vs RabbitMQ vs Kafka | Rabbit: mature queues; Kafka: heavy | NATS low-latency; Kafka operationally heavy | NATS fits <=2s telemetry freshness (**INF-ASR-03**). |
| OIDC vs DB-only auth | DB-only simpler | OIDC improves lifecycle/revocation | OIDC supports secure remote admin and policy (**INF-NFR-20**, **INF-ASR-08**). |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1**: “TSU” exists as a logical superior control unit; if not physically present, ApplicationService assumes TSU role while preserving TSU→FCU→DCU command hierarchy.  
- **A2**: The “one-way serial transfer” is implemented as RS-232 from a DMZ-side exporter, not directly from control plane servers.  
- **A3**: “99.” uptime requirement is interpreted as **>=99.0%** minimum until stakeholders confirm the missing digit(s).  
- **A4**: MD5 is mandated for integrity verification by legacy spec; for security, additional SHA-256 signing is permitted without violating requirements (if change control approves).  
- **A5**: Operator confirmation is required for scheduled operations as stated; unattended operations will alarm to prompt operator login, not auto-execute.

## Unresolved stakeholder questions (suggested phrasing)
1. What is the exact uptime target: 99.0%, 99.9%, or 99.99%? (clarify **INF-NFR-02**)  
2. Confirm whether TSU is a physical controller or logical role at TMC. (**A1**)  
3. Provide the authoritative schema for the external 30s status file (exact field names/encoding). (**INF-NFR-16**)  
4. Confirm controller communication protocol and checksum algorithm requirements (CRC vs cryptographic). (**INF-ASR-02**)  
5. Confirm retention: audit logs and raw telemetry retention periods (some 60 days to 1 year mentioned for reports). (**INF-FR-15**, **INF-NFR-18**)  
6. Confirm “only one operator logged on” vs “multiple users logged on”; diagrams assume multiple monitor sessions but single command-control. (**UseCaseView note conflict**)  

## Conflicts logged (requirements vs diagrams)
- **C1**: Requirement says “Only one ‘operator’ may be logged onto the system at any given time.” But also states multiple users logged on supported. Diagrams implement **single command-control lease** with multiple monitor sessions. Needs stakeholder decision.

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# ArchitectureDocument.md
(This document content is the architecture.md.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: RLCS Control Plane API
  version: 1.0.0
  description: External API for RLCS GUI and authorized remote clients on the private RLCS network.
servers:
  - url: https://rlcs-control-plane.local
security:
  - bearerAuth: []
paths:
  /v1/auth/login:
    post:
      summary: Log in (OIDC-backed) and create an RLCS session
      operationId: login
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        "201":
          description: Session created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SessionResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /v1/sessions/me:
    get:
      summary: Get current session context
      operationId: getMySession
      responses:
        "200":
          description: Session context
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SessionResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /v1/command-control/lease:
    post:
      summary: Acquire command-control lease
      operationId: acquireLease
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AcquireLeaseRequest"
      responses:
        "200":
          description: Lease granted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LeaseResponse"
        "409":
          description: Lease held by other session; takeover may be required
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /v1/sequences/{sequenceId}/confirm:
    post:
      summary: Confirm execution of a scheduled sequence (human-in-the-loop)
      operationId: confirmSequence
      parameters:
        - name: sequenceId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ConfirmSequenceRequest"
      responses:
        "202":
          description: Sequence execution started or queued
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SequenceExecutionResponse"
        "400":
          description: Invalid request (e.g., not scheduled, wrong mode)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "403":
          $ref: "#/components/responses/Forbidden"
        "409":
          description: Cannot execute due to safety screening failure or stale snapshot
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/devices/{deviceId}/override:
    post:
      summary: Override device status in database (no field command)
      operationId: overrideDevice
      parameters:
        - name: deviceId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeviceOverrideRequest"
      responses:
        "200":
          description: Override applied
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeviceOverrideResponse"
        "403":
          $ref: "#/components/responses/Forbidden"
        "409":
          description: Lease not held or override not allowed by policy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/telemetry/stream:
    get:
      summary: Telemetry stream (SSE)
      operationId: telemetryStream
      description: Server-Sent Events stream delivering facility/device/alarm updates.
      responses:
        "200":
          description: SSE stream
          content:
            text/event-stream:
              schema:
                type: string
  /v1/logs/audit/export:
    get:
      summary: Export audit logs (ASCII/CSV)
      operationId: exportAuditLogs
      parameters:
        - name: from
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: to
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: format
          in: query
          required: false
          schema:
            type: string
            enum: [csv, txt]
            default: csv
      responses:
        "200":
          description: Export file
          content:
            text/csv:
              schema:
                type: string
            text/plain:
              schema:
                type: string
        "403":
          $ref: "#/components/responses/Forbidden"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  responses:
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
    Forbidden:
      description: Forbidden
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
  schemas:
    LoginRequest:
      type: object
      additionalProperties: false
      required: [username, password, workstationId]
      properties:
        username:
          type: string
          minLength: 3
          maxLength: 64
        password:
          type: string
          minLength: 8
          maxLength: 256
        workstationId:
          type: string
          minLength: 1
          maxLength: 64
    SessionResponse:
      type: object
      additionalProperties: false
      required: [sessionId, userId, role, workstationId, issuedAt, expiresAt]
      properties:
        sessionId:
          type: string
        userId:
          type: string
        role:
          type: string
          enum: [Operator, SystemAdministrator, MaintenanceUser, MonitorOnly]
        workstationId:
          type: string
        issuedAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time
    AcquireLeaseRequest:
      type: object
      additionalProperties: false
      required: [workstationId]
      properties:
        workstationId:
          type: string
        takeover:
          type: boolean
          default: false
    LeaseResponse:
      type: object
      additionalProperties: false
      required: [leaseId, holderUserId, holderWorkstationId, acquiredAt, expiresAt]
      properties:
        leaseId:
          type: string
        holderUserId:
          type: string
        holderWorkstationId:
          type: string
        acquiredAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time
    ConfirmSequenceRequest:
      type: object
      additionalProperties: false
      required: [confirm]
      properties:
        confirm:
          type: boolean
        comment:
          type: string
          maxLength: 512
    SequenceExecutionResponse:
      type: object
      additionalProperties: false
      required: [executionId, sequenceId, state]
      properties:
        executionId:
          type: string
        sequenceId:
          type: string
        state:
          type: string
          enum: [PendingConfirmation, Executing, Halted, Completed]
    DeviceOverrideRequest:
      type: object
      additionalProperties: false
      required: [overriddenStatus, reason, timeoutSeconds]
      properties:
        overriddenStatus:
          type: string
          enum: [Open, Closed, Unknown, Failed]
        reason:
          type: string
          minLength: 3
          maxLength: 256
        timeoutSeconds:
          type: integer
          minimum: 30
          maximum: 86400
    DeviceOverrideResponse:
      type: object
      additionalProperties: false
      required: [deviceId, appliedAt, expiresAt]
      properties:
        deviceId:
          type: string
        appliedAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time
    Error:
      type: object
      additionalProperties: false
      required: [code, message, correlationId]
      properties:
        code:
          type: string
          example: RLCS_CONFLICT
        message:
          type: string
        correlationId:
          type: string
```

```proto
// filename: internal.proto
syntax = "proto3";
package rlcs.v1;

option go_package = "github.com/example/rlcs/gen/rlcs/v1;rlcsv1";

message Empty {}

message Timestamp {
  int64 unix_seconds = 1;
  int32 nanos = 2;
}

enum CommandStatus {
  COMMAND_STATUS_UNSPECIFIED = 0;
  PROPOSED = 1;
  CONFIRMED = 2;
  ABORTED = 3;
  SENT = 4;
  COMPLETED = 5;
  HALTED = 6;
  FAILED = 7;
}

message FacilityStatusSnapshot {
  string snapshot_id = 1;
  Timestamp captured_at = 2;
  int32 max_age_seconds = 3; // used for staleness checks (e.g., 3s)
}

message SafetyDecision {
  bool allowed = 1;
  string reason = 2;
}

message ControlCommand {
  string command_id = 1;
  string command_type = 2; // e.g., OpenGate, ClosePopUp
  string target_device_id = 3;
  Timestamp confirmed_at = 4;
  CommandStatus status = 5;
}

service SafetyService {
  rpc Evaluate(ControlCommandEvaluationRequest) returns (SafetyDecision);
}

message ControlCommandEvaluationRequest {
  ControlCommand command = 1;
  FacilityStatusSnapshot snapshot = 2;
  string ruleset_version = 3;
}

service SequenceService {
  rpc ConfirmSequence(ConfirmSequenceInternalRequest) returns (SequenceExecutionInternalResponse);
  rpc ResumeSequence(ResumeSequenceRequest) returns (SequenceExecutionInternalResponse);
}

message ConfirmSequenceInternalRequest {
  string sequence_id = 1;
  string session_id = 2;
  bool confirm = 3;
  string comment = 4;
}

message ResumeSequenceRequest {
  string execution_id = 1;
  string session_id = 2;
}

message SequenceExecutionInternalResponse {
  string execution_id = 1;
  string sequence_id = 2;
  string state = 3; // Executing/Halted/Completed
  string message = 4;
}

service ControllerGateway {
  rpc ForwardCommand(ForwardCommandRequest) returns (ForwardCommandResponse);
  rpc StatusUpdate(StatusUpdateRequest) returns (Empty);
}

message ForwardCommandRequest {
  string from_unit_id = 1; // TSU/FCU/DCU identifiers
  string to_unit_id = 2;
  ControlCommand command = 3;
  uint32 checksum_crc32c = 4;
}

message ForwardCommandResponse {
  bool accepted = 1;
  string reason = 2;
}

message StatusUpdateRequest {
  string unit_id = 1;
  string device_id = 2;
  string status = 3; // Open/Closed/Unknown/Failed
  Timestamp observed_at = 4;
}

service HardwareIo {
  rpc DispatchIo(DispatchIoRequest) returns (DispatchIoResponse);
}

message DispatchIoRequest {
  string controller_unit_id = 1;
  string io_command = 2; // driver-specific command string
  int32 timeout_seconds = 3; // e.g., 12
}

message DispatchIoResponse {
  bool ack = 1;
  string detail = 2;
}
```

```yaml
# filename: k8s/applicationservice-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rlcs-applicationservice
  labels:
    app: rlcs-applicationservice
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rlcs-applicationservice
  template:
    metadata:
      labels:
        app: rlcs-applicationservice
    spec:
      containers:
        - name: applicationservice
          image: registry.example.local/rlcs/applicationservice:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "2"
              memory: "2Gi"
          envFrom:
            - configMapRef:
                name: rlcs-config
            - secretRef:
                name: rlcs-secrets
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
  name: rlcs-applicationservice
spec:
  selector:
    app: rlcs-applicationservice
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rlcs-applicationservice-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rlcs-applicationservice
  minReplicas: 2
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
  name: rlcs-config
data:
  RLCS_TELEMETRY_PUSH_ENABLED: "true"
  RLCS_SNAPSHOT_MAX_AGE_SECONDS: "3"
  RLCS_SCHEDULE_SCAN_SECONDS: "60"
---
apiVersion: v1
kind: Secret
metadata:
  name: rlcs-secrets
type: Opaque
stringData:
  DB_URL: "jdbc:postgresql://rlcs-db-primary:5432/rlcs"
  DB_USER: "rlcs_app"
  DB_PASSWORD: "REPLACE_ME"
```

```sql
-- filename: sql/users_ddl.sql
CREATE TABLE rlcs_user (
  user_id            TEXT PRIMARY KEY,
  username           TEXT UNIQUE NOT NULL,
  password_hash      TEXT NOT NULL,
  role               TEXT NOT NULL CHECK (role IN ('Operator','SystemAdministrator','MaintenanceUser','MonitorOnly')),
  security_level     INTEGER NOT NULL CHECK (security_level >= 0),
  is_remote_allowed  BOOLEAN NOT NULL DEFAULT FALSE,
  is_active          BOOLEAN NOT NULL DEFAULT TRUE,
  password_changed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_rlcs_user_role ON rlcs_user(role);
```

```sql
-- filename: sql/workstation_ddl.sql
CREATE TABLE workstation (
  workstation_id            TEXT PRIMARY KEY,
  location_name             TEXT NOT NULL,
  is_authorized_for_command BOOLEAN NOT NULL DEFAULT FALSE,
  is_remote_dial_in         BOOLEAN NOT NULL DEFAULT FALSE,
  is_active                 BOOLEAN NOT NULL DEFAULT TRUE
);
```

```sql
-- filename: sql/command_lease_ddl.sql
CREATE TABLE command_lease (
  lease_id              TEXT PRIMARY KEY,
  holder_session_id     TEXT NOT NULL UNIQUE,
  holder_user_id        TEXT NOT NULL,
  holder_workstation_id TEXT NOT NULL,
  acquired_at           TIMESTAMPTZ NOT NULL,
  expires_at            TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_command_lease_expires ON command_lease(expires_at);
```

```sql
-- filename: sql/audit_log_ddl.sql
CREATE TABLE audit_log_entry (
  entry_id       TEXT PRIMARY KEY,
  ts             TIMESTAMPTZ NOT NULL,
  user_id        TEXT,
  workstation_id TEXT,
  session_id     TEXT,
  action         TEXT NOT NULL,
  details        TEXT NOT NULL,
  hash_chain     TEXT NOT NULL
);

-- Append-only enforcement is done via DB permissions + no UPDATE grants to application role.
CREATE INDEX idx_audit_log_ts ON audit_log_entry(ts);
```

```sql
-- filename: sql/device_ddl.sql
CREATE TABLE device (
  device_id       TEXT PRIMARY KEY,
  device_type     TEXT NOT NULL,
  location        TEXT NOT NULL,
  direction       TEXT NOT NULL,
  category        TEXT NOT NULL,
  current_status  TEXT NOT NULL CHECK (current_status IN ('Open','Closed','Unknown','Failed')),
  last_update_at  TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_device_category ON device(category);
CREATE INDEX idx_device_location ON device(location);
```

```sql
-- filename: sql/device_override_ddl.sql
CREATE TABLE device_override (
  override_id     TEXT PRIMARY KEY,
  device_id       TEXT NOT NULL REFERENCES device(device_id),
  overridden_status TEXT NOT NULL CHECK (overridden_status IN ('Open','Closed','Unknown','Failed')),
  reason          TEXT NOT NULL,
  applied_by_user_id TEXT NOT NULL,
  applied_at      TIMESTAMPTZ NOT NULL,
  expires_at      TIMESTAMPTZ NOT NULL,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_device_override_device_active ON device_override(device_id, is_active);
CREATE INDEX idx_device_override_expires ON device_override(expires_at);
```

```sql
-- filename: sql/system_control_parameters_ddl.sql
CREATE TABLE system_control_parameters (
  params_id               TEXT PRIMARY KEY,
  system_mode             TEXT NOT NULL,
  login_retry_count       INTEGER NOT NULL DEFAULT 5,
  polling_rate_seconds    INTEGER NOT NULL DEFAULT 2,
  override_timeout_seconds INTEGER NOT NULL DEFAULT 3600,
  max_users               INTEGER NOT NULL DEFAULT 50,
  username_min_length     INTEGER NOT NULL DEFAULT 3,
  password_min_length     INTEGER NOT NULL DEFAULT 8,
  config_snapshot_max_age_seconds INTEGER NOT NULL DEFAULT 3
);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s),Component(s),Artifact filename(s),Rationale
INF-FR-01,GUI provides logon,UseCaseView:UC_LogOn,AuthService RLCS GUI,openapi.yaml; sql/users_ddl.sql,Auth gates all access
INF-FR-03,Single command-control lease,ClassView:CommandLease,LeaseManager,sql/command_lease_ddl.sql,Prevents conflicting control
INF-FR-18,Confirm commands,ActivityView:HITL,RLCS GUI SequenceEngine,openapi.yaml,Human-in-loop safety
INF-ASR-04,One-way DMZ export every 30s,DeploymentView:N_DMZ,ExternalExportService,openapi.yaml,Isolation for external read-only
INF-NFR-04,UI freshness <=2s,ContainerView:CT_BUS,TelemetryBus RLCS GUI,k8s/applicationservice-deployment.yaml,Event push + scaling
```

---

## Acceptance Criteria Verification Table

| Check | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | ✅ |
| [ ] Sections A-L included. | ✅ |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | ⚠️ Partially (core set mapped; remaining SRS narrative lines require stakeholder confirmation + additional INF extraction pass) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | ✅ |
| [ ] Representative k8s manifest snippet included. | ✅ |
| [ ] SQL DDL / NoSQL models for primary entities included. | ✅ |
| [ ] All major components have at least one API contract and a data schema. | ⚠️ Not all components have dedicated schemas beyond core entities |
| [ ] Assumptions and unresolved questions listed. | ✅ |

---

## How to review checklist
- All FR/NFR/ASR present in traceability matrix? (requires final INF extraction to cover every narrative bullet)  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?

Conversion note (if PDF/HTML needed): `pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf`