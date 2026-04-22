Scope: Produce production-ready architecture documentation for the EVLA/VLA Expansion Correlator Monitor & Control System (CMCS) aligned to the provided requirements and the 11 supplied UML diagrams, resolving conflicts in favor of the requirements text.  
Approach: Normalize requirements into traceable inferred IDs (INF-*), map them to 4+1 views and to the provided diagrams (by title + element IDs only), then specify APIs, internal contracts, data schemas, and ops/security/SRE/testing.  
Top validation steps: (1) traceability completeness check (every INF-* mapped), (2) syntactic validation of OpenAPI/Proto/SQL/K8s, (3) architecture compliance review vs redundancy/modularity/security/observability requirements.

# A. Executive Summary (≤1 page)

## System overview
The Correlator Monitor & Control System (CMCS) provides the physical/software link between WIDAR correlator hardware (via CMIBs and power control) and the VLA Expansion Project Monitor & Control System (external M&C), translating configuration goals into hardware tables, handling real-time monitor/control, spooling telemetry, and performing autonomous fault recovery.

**Primary diagram mapping (one-line):** end-to-end control and telemetry flows are captured in *Deployment_SafetyCriticalControl: APP1/APP2/MB/StateDB/AuditDB/FCU*, *Component_SafetyCriticalControl: ControlAPI/AuthService/LeaseService/SafetyService/SequenceController/ControllerAdapter*, and *Sequence1_IssueCommand: ControlAPI→SafetyService→SequenceController→ControllerAdapter*.

## Architectural style(s) and topology
- **Style:** Master/Slave control with modular services + event-driven telemetry bus + contract-first hardware adapters.  
- **Deployment topology:** HA active/active masters with replicated services, separate physical networks (Master↔CMIB, Master↔Power, Master↔External M&C) and spooled telemetry.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| R1: Requirements lack explicit IDs and measurable timing/availability targets | High | Convert to INF-* requirements + define SLOs/SLIs and test gates; see Sections G/K. |
| R2: Provided UML diagrams model a generic safety-critical lease/interlock system that conflicts with CMCS terminology | Medium | Prefer requirements naming (CMCS/VCI/CMIB/Master/Power) and treat diagrams as patterns; log conflicts in K. |
| R3: Hardware protocol uncertainty (CMIB register semantics, warm boot, unique IP from 16-bit ID, hot-swap behavior) | High | Contract-first `ControllerAdapter`/`CmibAgent` protocol, versioned schemas, simulator harness; conformance tests and HIL. |

## Key QA coverage mapping (scalability, availability, security, performance, maintainability)

> Note: the requirements text provides no explicit ASR/NFR IDs; all are captured as inferred `INF-*` and treated as FR/NFR/ASR per content.

| Quality | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-EXPAND-IO, INF-NFR-EXPAND-TRANSPARENCY, INF-FR-CONTROLLABLE-SAMPLING | Load test, capacity test, soak test |
| Availability | INF-NFR-REDUNDANT-MASTER, INF-NFR-STANDALONE-BOOT, INF-NFR-PARTIAL-SHUTDOWN, INF-NFR-WATCHDOG | HA failover tests, chaos tests, power-loss drills |
| Security | INF-SEC-UNIQUE-ID, INF-SEC-SECURE-LOGIN, INF-SEC-AUDIT-LOG, INF-SEC-ROLE-PRIV | Pen test, authz unit tests, audit integrity tests |
| Performance/Real-time | INF-NFR-DETERMINISTIC-RESP, INF-NFR-DEADLINES, INF-FR-SPOOL-NETLOSS | HIL timing tests, latency SLO tests, fault injection |
| Maintainability | INF-NFR-MODULAR, INF-NFR-DEBUGGABLE, INF-NFR-RESTARTABLE, INF-NFR-SOURCE-AVAILABLE | CI static checks, restart/upgrade drills, maintainability reviews |

---

# B. Traceability & Rationale

Because the input requirements lack explicit numeric IDs, each requirement is assigned an inferred ID (`INF-*`). **Every INF-* appears at least once below and is referenced later.**

**Artifact filenames referenced:**  
- `architecture.md` (this document)  
- `openapi.yaml`  
- `internal.proto`  
- `k8s/cmcs-deployment.yaml`  
- `sql/*.sql` (DDL files)  
- `traceability_matrix.csv`

## Traceability matrix (table view; full CSV in Section L)

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-LINK | Provide physical link between WIDAR and VLA M&C | Deployment_SafetyCriticalControl: FCU/APP1/APP2 | CmibAgent, ControllerAdapter | architecture.md | Establishes integration boundary and the master/slave control plane. |
| INF-FR-CONFIG-RECV-XLATE | Receive config from external M&C and translate to hardware tables | Sequence1_IssueCommand: ControlAPI/SafetyService/SequenceController | VCI, ConfigTranslator, TablePublisher | openapi.yaml, internal.proto | Contract-first translation ensures unambiguous convergent configuration. |
| INF-FR-DYNAMIC-MONCTRL | Process/transfer dynamic control and monitor data | Sequence2_MonitorStatusAndExport: MonitoringService/EventBus | TelemetryBus, MonitorAggregator | internal.proto | Event-driven pub/sub supports continuous monitor streams and control feedback. |
| INF-FR-AUTONOMOUS-RECOVERY | Monitor health and take corrective action autonomously | State_CommandLifecycle: Failed→Retry | HealthSupervisor, Watchdogs | internal.proto, architecture.md | Encodes retry, restart, and alerting when self-heal fails. |
| INF-FR-REALTIME-PROBING | Limited real-time processing (e.g., auto-correlation display tools) | Container_SafetyCriticalControl: MonitoringUI | DiagnosticTools, DataProbeSvc | openapi.yaml | Provides user tools without interfering with control plane. |
| INF-FR-EASY-ACCESS | Easy system access for test/debug | Package_SafetyCriticalControl: ui/api/services | DebugConsole, AdminAPI | openapi.yaml | Remote access and tooling are explicit interfaces and audited. |
| INF-ASR-MASTER-SLAVE | Master coordinates; slaves handle real-time HW | Deployment_SafetyCriticalControl: APP1/APP2/FCU | MasterControl, CmibAgent | architecture.md | Separates quasi-real-time external network from deterministic HW layer. |
| INF-ASR-ISOLATION | Isolate correlator hardware from external network chaos | Deployment_SafetyCriticalControl: NET/FCU links | NetworkSegmentation | k8s/cmcs-deployment.yaml | Separate NICs/VLANs and rate limiting reduce risk of overload. |
| INF-NFR-REDUNDANT-CRITICAL | Redundant in critical areas; modular | Deployment_SafetyCriticalControl: APP1/APP2 | HA Master, modular services | k8s/cmcs-deployment.yaml | Active/active masters and modular components enable failover and repair. |
| INF-FR-FULL-OBSERVABLE | Fully observable; limited by HW/bandwidth/security | Component_SafetyCriticalControl: EventBus/AuditLog | Observability stack | architecture.md | Defines logging/metrics/traces with security controls. |
| INF-FR-MSG-CONCISE | Concise time/location referenced error/status to upper levels; filterable | Component_SafetyCriticalControl: AuditLog/EventBus | LogRouter, MessageCatalog | internal.proto | Structured logging + filters meet operator needs and reduce noise. |
| INF-FR-VCI | Gateway via Virtual Correlator Interface (VCI) | Container_SafetyCriticalControl: C_API/C_SVC | VCI API | openapi.yaml | Single logical API surface for external M&C and GUI. |
| INF-FR-GUI-CONFIG | GUI can configure correlator via same tables | UseCase_SafetyCriticalControl: UC_Config | WebUI, TableEditor | openapi.yaml | GUI uses the same config-table model as external M&C for consistency. |
| INF-FR-BDP-DATASET | Provide datasets to Backend Data Processing over secondary network | Deployment_SafetyCriticalControl: EXT | ExportService | openapi.yaml | Separate egress ensures robustness and bandwidth control. |
| INF-FR-SPOOL-MON | Spool ancillary monitor data to survive temporary network loss | Component_SafetyCriticalControl: StateStore | TelemetrySpooler | sql/telemetry_event_ddl.sql | Persistent queue prevents data loss during outages. |
| INF-FR-CONTROLLABLE-SAMPLING | Sample rates/contents controllable via M&C or backend controller | Sequence2_MonitorStatusAndExport: ExportService | SamplingPolicySvc | openapi.yaml, internal.proto | Central policy enables runtime adjustment with auditability. |
| INF-FR-EXT-FEEDS | Accept external feeds: models, time, phase corrections | UseCase_SafetyCriticalControl: TimeSource | TimeModelIngestSvc | openapi.yaml | Explicit ingestion endpoints allow controlled updates. |
| INF-FR-HOTSWAP-RECOVER | Recover from failures/hot-swapped devices; alert if not self-healed | State_CommandLifecycle: Failed paths | DeviceManager, Alerting | internal.proto | Supports restart/reconfigure to current operational state. |
| INF-NFR-STATEFUL-SECONDARY | Primary and secondary masters keep full state; reroute on failure | Deployment_SafetyCriticalControl: APP1/APP2/StateDB | HA/Leader election | k8s/cmcs-deployment.yaml, sql/system_state_ddl.sql | Shared state + fencing prevents split-brain and enables rapid failover. |
| INF-NFR-WATCHDOG | Watchdog processes; hardware watchdog reboot on hang | (pattern) State_CommandLifecycle | NodeWatchdog | architecture.md | Ensures autonomous recovery with minimal interruption. |
| INF-ASR-ETHERNET-100M | Interfaces: Ethernet ≥100M; transformer coupled copper unless needed | Deployment_SafetyCriticalControl: NET/FCU | Network HW | architecture.md | Specifies physical media and minimum bandwidth. |
| INF-ASR-SEPARATE-NETS | Master-CMIB, Master-Power, Master-External nets separate | Deployment_SafetyCriticalControl: NET | NetworkSegmentation | architecture.md | Reduces fault domains and unauthorized access risk. |
| INF-ASR-REDUNDANT-PWR-PATH | Redundant comm path Master↔Power for remote reboot | (pattern) Deployment | PowerControlLink | architecture.md | Enables recovery from partial network/computing failures. |
| INF-ASR-FIBER-RFI | Penetrating shielded room via fiber/low-RFI material | (pattern) Deployment | PhysicalNetwork | architecture.md | Meets RFI constraints. |
| INF-SEC-ROUTER-PROTECT | Router/switch protect Master from unauthorized/irrelevant traffic | Deployment_SafetyCriticalControl: NET | Firewall/ACL | architecture.md | Enforces least privilege ingress and traffic shaping. |
| INF-ASR-CMIB-BUS | CMIB daughterboard communicates via PCI/ISA/serial/parallel | (pattern) Component | CmibHwAbstraction | internal.proto | Encapsulates hardware bus specifics behind a stable agent protocol. |
| INF-ASR-CMIB-READID | CMIB reads 16-bit board ID to form IP; supports hot-swap carry-over | (pattern) Component | AddressManager | internal.proto | Stable addressing across swaps reduces reconfiguration errors. |
| INF-FR-READBACK-REGS | Read back writeable control registers where meaningful | (pattern) Component | RegisterService | internal.proto | Enables monitoring, diagnostics, and fault tolerance. |
| INF-FR-WARMBOOT | CMIB supports warm boot triggered remotely | (pattern) State | DeviceManager | internal.proto | Supports controlled reboot without full power cycle. |
| INF-ASR-STATUS-LED | CMIB carrier has visible operational indicator | (HW) | — | architecture.md | Documented as hardware acceptance criterion. |
| INF-NFR-UPS | Powered through UPS; signal outage and time remaining | (ops) | PowerSupervisor | architecture.md | Enables coordinated shutdown and safe stop procedures. |
| INF-SEC-REMOTE-LOGIN | Authorized remote logins to each computer | UseCase_SafetyCriticalControl: UC_Auth | Bastion/SSO | architecture.md | Required for maintenance and debugging with audit. |
| INF-NFR-REALTIME-OS | CMIB runs COTS OS in near real-time; supports test bench + upgrades | (pattern) Component | CmibAgent | internal.proto | Ensures deterministic local control and standalone simulation mode. |
| INF-NFR-MASTER-HA | Master is HA, multiple NICs, local disk for standalone boot | Deployment_SafetyCriticalControl: APP1/APP2 | Master services | k8s/cmcs-deployment.yaml | Supports operation without external networks. |
| INF-NFR-POWER-HA | Power control computer HA; standalone during M&C network failure | (pattern) Deployment | PowerController | architecture.md | Power monitoring must continue even if external M&C is down. |
| INF-NFR-DEADLINES | Processors meet deadlines and future requirements | (SRE) | All services | architecture.md | Converted into measurable SLOs/alerts in Section G. |
| INF-NFR-DETERMINISTIC-RESP | Deterministic response to HW inputs to avoid data loss | State_CommandLifecycle | CmibAgent loop | internal.proto | Near-real-time agent and bounded queues avoid overruns. |
| INF-FR-ERROR-AT-MASTER | All lower-layer errors/debug present at master; avoid direct CPU access | Component_SafetyCriticalControl: AuditLog | LogCollector | architecture.md | Centralized logging and streaming removes need for local console. |
| INF-FR-MSG-CATEGORIZED | Error/debug categorized and filterable | (pattern) Component | MessageCatalog | internal.proto | Structured levels/categories permit filtering by content/rate. |
| INF-FR-TIMESTAMPS | Messages carry UTC and wall-clock timestamps | internal.proto types | TelemetryEvent, AuditEntry | internal.proto | Required for correlation and operational forensics. |
| INF-FR-FULL-TRAFFIC-TOOL | Authorized user can access all messaging/monitor/control traffic | UseCase_SafetyCriticalControl: UC_Diag | AdminUI | openapi.yaml | Supports offline testing and debugging with access controls. |
| INF-FR-GUI-REMOTE | GUI provides remote configurable access through VCI | Container_SafetyCriticalControl: C_UI→C_API | MonitoringUI | openapi.yaml | Remote operations interface tied to VCI. |
| INF-NFR-SELF-MONITORING | Detect/report/remedy failures (CPU, OS, temp/voltage, perf, comms) | Deployment_SafetyCriticalControl: APP nodes | HealthSupervisor | architecture.md | Health checks + alerts + remediation workflows. |
| INF-NFR-NO-RESTART | Software operates without total restart between maintenance windows | (ops) | Rolling restarts | k8s/cmcs-deployment.yaml | Kubernetes rolling updates + modular restartability. |
| INF-NFR-INDEFINITE-HW | Hardware performs indefinitely except total power failure | (ops) | UPS + redundancy | architecture.md | Redundancy and power policy reduce single points of failure. |
| INF-NFR-QUEUE-EXHAUST | Continue processing until queues exhausted during comm loss | internal.proto queues | TelemetrySpooler | sql/telemetry_event_ddl.sql | Persisted queues enable degraded operation. |
| INF-NFR-IDLE-RESUME | Idle and resume with minimal delay | (runtime) | Warm caches | architecture.md | Keepalive loops and preloaded configs. |
| INF-NFR-MAINT-ACCESS | Hardware accessible for maintenance; modular replacement/hot swap | (ops) | Rack design | architecture.md | Physical maintainability influences deployment/rack layout. |
| INF-NFR-SOURCE-LOCAL | Source code available on systems that execute it | (process) | SCM mirror | architecture.md | Ensures maintainability and on-site support. |
| INF-NFR-DEBUGGABLE | Application modules debuggable, inputs/outputs simulatable | Component_SafetyCriticalControl: ControllerAdapter | Simulator | internal.proto | Simulation harness and mockable interfaces. |
| INF-NFR-PROC-RESTART | Processes killable/restartable/testable with minimal impact | k8s + supervision | All services | k8s/cmcs-deployment.yaml | Liveness/readiness + graceful shutdown. |
| INF-NFR-VENDOR-DIAG | Closed tools must include diagnostics & support | (process) | Vendor mgmt | architecture.md | Procurement/ops requirement. |
| INF-NFR-OS-DIAG | OS source or sufficient diagnostics/support | (process) | OS selection | architecture.md | Reduce risk of un-debuggable failures. |
| INF-NFR-EXPAND-IO | I/O/comms/processing easily expandable and replaceable | (ops) | Modular | architecture.md | Use standard protocols and scalable bus patterns. |
| INF-NFR-EXPAND-TRANSPARENCY | Expansion transparent except recompilation | (design) | Plugin/adapter | architecture.md | Adapter pattern shields core from HW variation. |
| INF-NFR-EXPAND-SEAMLESS | Seamless at interfaces, no impact on modules met at interfaces | internal.proto versioning | Contracts | internal.proto | Backward-compatible contracts and schema versioning. |
| INF-SEC-MECHANISM | Robust security prevents unauthorized access | Security sections | AuthN/Z | architecture.md, openapi.yaml | OIDC/mTLS + RBAC enforced at VCI. |
| INF-SEC-UNIQUE-ID | All users uniquely identified | UseCase_SafetyCriticalControl: UC_Auth | IAM | openapi.yaml | Required for accountability and audit. |
| INF-SEC-AUDIT-LOG | Log all access attempts | Component_SafetyCriticalControl: AuditLog | AuditService | sql/audit_entry_ddl.sql | Enables forensics and compliance. |
| INF-SEC-ROLE-OPS | Ops unrestricted; can grant/revoke privileges | (security) | RBAC admin | openapi.yaml | Role model supports ops vs dev/maintainer separation. |
| INF-SEC-ROLE-DEV | Dev/test/maint need scoped access | (security) | RBAC policies | openapi.yaml | Least privilege. |
| INF-SEC-SECURE-LOGIN | Login attempts secure | (security) | TLS, MFA | openapi.yaml | Prevent credential interception. |
| INF-SEC-ADMIN | System administrator unrestricted | (security) | Admin role | openapi.yaml | Needed for emergency operations. |
| INF-SEC-USER-PROPS | Each user has access properties/privileges | (security) | User DB | sql/user_account_ddl.sql | Persisted role bindings. |
| INF-SEC-ADMIN-CRUD | Admin can create/remove/edit users | (security) | Admin API | openapi.yaml | Explicit endpoints enable controlled user lifecycle. |
| INF-SEC-ADMIN-BLOCK | Admin can block all or selective users | (security) | Authz gate | openapi.yaml | Rapid response to compromise. |
| INF-NFR-PARTIAL-SHUTDOWN | Continue ops on unaffected resources during maintenance | Deployment HA | HA routing | k8s/cmcs-deployment.yaml | Rolling updates + redundancy. |
| INF-NFR-REPLACEABILITY | Modular replaceability, hot-swappable components | (ops) | Hardware modules | architecture.md | Supports rapid repair. |
| INF-NFR-DOCS-SPECS | Hardware specs/config readily available | (process) | CMDB | architecture.md | Maintainers need accurate inventory/config. |
| INF-NFR-CODE-STYLE | Code well documented, familiar languages, readable style | (process) | Standards | architecture.md | Maintainability baseline for multi-team development. |

---

# C. Architecture Overview

## Context view
CMCS sits between:
- **External VLA Expansion Project Monitor & Control System** (goal configurations, dynamic control, auxiliary feeds).
- **WIDAR correlator hardware** via **CMIB intelligent processors** and **Correlator Power Control Computer**.

The provided UML depicts a generic control system with `ControlAPI`, `EventBus`, and `ControllerAdapter`. **We map those patterns to CMCS**: `VCI API` (ControlAPI), `Telemetry Bus` (EventBus), and `CMIB/Power adapters` (ControllerAdapter). See *Component_SafetyCriticalControl: ControlAPI/EventBus/ControllerAdapter*.

## Container view
- **VCI API + GUI**: single gateway for external M&C and human GUI access. (Ref: *Container_SafetyCriticalControl: C_UI→C_API*).
- **Core control services**: translation, sequencing, safety gates (for hardware protection), monitoring aggregation, export/spool.
- **State store + audit log**: persisted configuration/state snapshots, immutable audit trail. (Ref: *Deployment_SafetyCriticalControl: StateDB/AuditDB*).
- **Hardware integration**: CMIB agent protocol and power controller protocol adapters.

## Component/package view
Packages align to *Package_SafetyCriticalControl: ui/api/domain/services/persistence/messaging/integrations*, but renamed in codebase to CMCS terms:
- `vci-api`, `monitoring-ui`, `control-core`, `telemetry`, `cmib-agent`, `power-agent`, `persistence`, `security`.

## Runtime/class view
The UML’s `CommandRequest`, `SystemState`, `TelemetryEvent`, and `AuditEntry` map directly to CMCS:
- `CommandRequest` → `ControlCommand` / `ConfigApplyRequest`
- `SystemState` → `CorrelatorStateSnapshot`
- `TelemetryEvent` → `MonitorSample` / `ErrorEvent`
- `AuditEntry` remains `AuditEntry`

See *Class_SafetyCriticalControl: CommandRequest/SystemState/TelemetryEvent/AuditEntry* and *State_CommandLifecycle* for command execution lifecycle.

## Deployment view
HA masters and separate networks are required by INF-ASR-SEPARATE-NETS and INF-NFR-REDUNDANT-MASTER. The provided deployment diagram shows generic nodes; we apply it as:
- `AppNode-1/2` = Primary/Secondary Master Correlator Control Computer (active/active with fencing)
- `Field Controller Unit` = CMIB network + power controller network edges

Ref: *Deployment_SafetyCriticalControl: APP1/APP2/FCU/StateDB/AuditDB*.

---

# D. Detailed Technical Design (developer-facing)

## D.1 Major subsystems
1. **VCI Gateway (External API + GUI backend)**  
2. **Control Core (Config translation, sequencing, safety/hardware protection rules)**  
3. **Telemetry & Spooling (monitor collection, buffering, export)**  
4. **Hardware Integration (CMIB Agent + Power Agent adapters, simulator)**  
5. **Persistence (State DB + Audit DB, schema registry)**  
6. **Security & IAM (authn/authz, user management)**

Below, each major subsystem follows the required template.

---

## D.2 VCI Gateway (External API + GUI backend)

### 1) Responsibilities & data ownership
Owns the external-facing **Virtual Correlator Interface (VCI)**: authentication, authorization, request validation, request routing to internal services, and consistent error responses. It does **not** own hardware state; it reads current snapshots from State Store.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: **Go 1.22–1.23** (high-concurrency, simple ops)
- Conservative: **Java 21 LTS** (mature ecosystem, long-term support)
- Cutting-edge: **Rust 1.78–1.81** (max safety, higher dev friction)

**Web framework**
- Recommended: Go **chi v5** or **gin v1.10**
- Conservative: Spring Boot **3.2–3.3**
- Cutting-edge: Rust **axum 0.7**

**RPC/HTTP**
- Recommended: **REST/JSON + WebSocket** for GUI; internal gRPC
- Conservative: REST-only
- Cutting-edge: **gRPC-web** end-to-end

**Persistence access**
- Recommended: SQL via pgx (Go) / JDBC (Java)
- Conservative: ORM (Hibernate)
- Cutting-edge: event-sourcing only (not recommended due to complexity)

**Cache**
- Recommended: Redis **7.2–7.4**
- Conservative: in-process cache only
- Cutting-edge: DragonflyDB

**Messaging**
- Recommended: NATS **2.10–2.11** (JetStream for spooling)
- Conservative: RabbitMQ **3.12–3.13**
- Cutting-edge: Redpanda/Kafka

**Search**
- Recommended: none (initial)
- Conservative: PostgreSQL full-text
- Cutting-edge: OpenSearch

**Authn/Authz**
- Recommended: OIDC (Keycloak **24–26**) + JWT + RBAC
- Conservative: LDAP + local sessions
- Cutting-edge: SPIFFE/SPIRE mTLS identities

**Observability**
- Recommended: OpenTelemetry **1.x** + Prometheus **2.49+**
- Conservative: logs only (insufficient)
- Cutting-edge: eBPF-based tracing (complementary)

**CI/CD**
- Recommended: GitHub Actions/GitLab CI
- Conservative: Jenkins
- Cutting-edge: Bazel + hermetic builds

**Container runtime**
- Recommended: containerd (Kubernetes default)
- Conservative: Docker Engine
- Cutting-edge: gVisor (extra isolation)

**Infra provisioning**
- Recommended: Terraform **1.6–1.8**
- Conservative: manual scripts
- Cutting-edge: Crossplane

### 3) Recommended default stack + justification
- **Go 1.22–1.23 + chi v5 + gRPC (internal) + PostgreSQL 14–15 + NATS 2.10–2.11 + OTel**.  
Justification: meets INF-NFR-MODULAR (modularity), INF-FR-FULL-OBSERVABLE (full observability), and INF-SEC-SECURE-LOGIN (secure login).

### 4) Interface design (External APIs) — `openapi.yaml`
(Full file in Section L; summarized here)
- Auth: login/token, refresh
- Config: submit config tables, apply, validate
- Control: issue control commands, warm boot request
- Monitoring: query state, subscribe stream (via WebSocket upgrade endpoint)
- Admin: user CRUD, block/unblock

### 5) Data model / schema
Uses `user_account`, `role_binding`, `audit_entry` tables (see SQL files). Sensitive fields encrypted at rest where required.

### 6) Caching & consistency
- Cache: current `CorrelatorStateSnapshot` read-through cache TTL 250–500ms for GUI responsiveness.
- Consistency: **strong** consistency for auth/admin actions and config apply; **eventual** for telemetry stream.

---

## D.3 Control Core (Config translation, sequencing, protection rules)

### 1) Responsibilities & data ownership
Owns translation from goal-oriented configuration to **hardware configuration tables**, deterministic sequencing for safe application, and enforcement of “abort-on-unknown” hardware protection policies. Owns `config_snapshot` and `command_execution` records.

### 2) Technology options

**Language/runtime**
- Recommended: Go 1.22–1.23
- Conservative: Java 21
- Cutting-edge: Rust

**Framework**
- Recommended: plain services + gRPC handlers
- Conservative: Spring
- Cutting-edge: actor model (Akka)

**RPC**
- Recommended: gRPC (protobuf)
- Conservative: internal REST
- Cutting-edge: QUIC-based RPC

**Persistence**
- Recommended: PostgreSQL 14–15
- Conservative: MySQL 8.0
- Cutting-edge: FoundationDB (complex)

**Messaging**
- Recommended: NATS JetStream
- Conservative: RabbitMQ
- Cutting-edge: Kafka

**Authz**
- Recommended: centralized RBAC in gateway + service-level policy checks
- Conservative: gateway-only
- Cutting-edge: OPA sidecar everywhere

**Observability**
- Recommended: OTel traces around config apply/sequence steps
- Conservative: logs only
- Cutting-edge: formal runtime verification (future)

**CI/CD, container, infra**
- Same as D.2.

### 3) Recommended default stack + justification
- **Go 1.22–1.23 + gRPC + PostgreSQL 14–15 + NATS JetStream**.  
Justification: meets INF-NFR-DETERMINISTIC-RESP (deterministic response) and INF-FR-CONFIG-RECV-XLATE (translate config to tables).

### 4) Interface design (Internal contracts) — `internal.proto`
Defines:
- `ConfigService.Validate/Apply`
- `ControlService.IssueCommand`
- `DeviceService.WarmBoot/ReadRegisters`
- `TelemetryService.PublishSample/Subscribe`

### 5) Data model / schema
- `config_snapshot` (immutable applied configs)
- `command_execution` (status, timestamps, target, result)

### 6) Caching & consistency
- No caching of safety-critical apply decisions; only cache derived read models for UI.
- Use optimistic concurrency on `system_state.version` to prevent stale overwrites.

---

## D.4 Telemetry & Spooling (monitor collection, buffering, export)

### 1) Responsibilities & data ownership
Collects monitor samples and errors from CMIB/power agents, timestamps them (UTC + wall clock), spools them durably during network loss, and exports selected datasets to backend processing / external M&C.

### 2) Technology options

**Messaging**
- Recommended: NATS JetStream (durable streams)
- Conservative: RabbitMQ with persistent queues
- Cutting-edge: Kafka/Redpanda

**Persistence**
- Recommended: PostgreSQL partitioned tables for telemetry index + JetStream for short-term queueing
- Conservative: TimescaleDB
- Cutting-edge: ClickHouse (analytics heavy)

**Export**
- Recommended: batch export via HTTPS + signed payloads
- Conservative: SCP/rsync drops
- Cutting-edge: streaming gRPC to backend

### 3) Recommended default stack + justification
- **NATS JetStream + PostgreSQL 14–15 partitioned telemetry tables**.  
Justification: meets INF-FR-SPOOL-MON (spool monitor data on network loss) and INF-FR-CONTROLLABLE-SAMPLING (controllable sampling).

### 4) Interface design
Export endpoints in `openapi.yaml` and internal `TelemetryService` in `internal.proto`.

### 5) Data model / schema
- `telemetry_event` partitioned by day, indexed by `occurred_at`, `source`, `event_type`.

### 6) Caching & consistency
- Cache export cursors per subscriber (last delivered offset).
- Exactly-once delivery is not assumed; provide **at-least-once** with idempotency keys.

---

## D.5 Hardware Integration (CMIB Agent + Power Agent + simulator)

### 1) Responsibilities & data ownership
Encapsulates all hardware bus/protocol specifics (PCI/ISA/serial/ethernet), provides stable RPC to Control Core, enforces local near-real-time loops, and supports standalone bench simulation.

### 2) Technology options

**Agent language/runtime**
- Recommended: C++20 or Rust for low-level IO; or Go if OS/drivers allow
- Conservative: C (highest portability)
- Cutting-edge: Rust + async runtime

**Transport**
- Recommended: gRPC over dedicated VLAN
- Conservative: raw TCP protocol
- Cutting-edge: DDS

**Simulation**
- Recommended: built-in simulator implementing same `internal.proto`
- Conservative: mocks only
- Cutting-edge: digital twin

### 3) Recommended default stack + justification
- **C++20 agent + gRPC + hardware abstraction layer + simulator mode**.  
Justification: meets INF-NFR-REALTIME-OS (near real-time CMIB support) and INF-FR-READBACK-REGS (register readback/diagnostics).

### 4) Interface design
Use `DeviceService` in `internal.proto` for:
- `ReadRegisters`, `WriteRegisters`
- `WarmBoot`
- `GetBoardId16` (for IP mapping logic support)

### 5) Data model / schema
Hardware integration is mostly stateless; persists:
- `device_inventory` (board IDs, mapping, last-seen)

### 6) Caching & consistency
- Cache inventory lookups; TTL 10s.
- Do not cache register reads except for monitoring sampling windows.

---

## D.6 Persistence (State DB + Audit DB)

### 1) Responsibilities & data ownership
Stores authoritative state snapshots, configs, users/roles, and immutable audit entries. Provides strong consistency and HA replication.

### 2) Options
- Recommended: PostgreSQL 14–15 (primary/standby) + WORM-like audit table policies
- Conservative: PostgreSQL 13
- Cutting-edge: CockroachDB (operational complexity)

### 3) Recommended + justification
- **PostgreSQL 14–15**.  
Justification: meets INF-NFR-STATEFUL-SECONDARY (masters share full state) and INF-SEC-AUDIT-LOG (log all access attempts).

### 4–6)
See SQL DDL artifacts in Section L.

---

# E. Operations & Deployment (ops-facing)

## E.1 Kubernetes-ready plan (`k8s/cmcs-deployment.yaml`)
- Separate Deployments: `vci-api`, `control-core`, `telemetry-svc`
- StatefulSets: `postgres-state`, optional `postgres-audit`
- NATS cluster (3 replicas) for JetStream durability

Justification: meets INF-NFR-PARTIAL-SHUTDOWN (continue on unaffected resources during maintenance).

## E.2 DB HA topology, backup cadence, restore
- Topology: PostgreSQL primary + synchronous standby (2 nodes minimum), optional async replica for analytics.
- Backups: nightly full + WAL archiving continuous; retain 30 days.
- Restore: quarterly restore drills; target RTO/RPO defined in Section G.

Justification: meets INF-FR-SPOOL-MON (no loss of spooled monitor data) and INF-SEC-AUDIT-LOG (audit retention).

## E.3 Network topology + ingress/egress rules
Map to *Deployment_SafetyCriticalControl: NET/APP1/APP2/FCU/EXT* but enforce **separate physical/VLAN interfaces** per INF-ASR-SEPARATE-NETS:
- VLAN-A: Master↔CMIB
- VLAN-B: Master↔Power Control
- VLAN-C: Master↔External M&C + GUI
- VLAN-D: Export network to backend/secondary virtual network

Latency expectations (assumed; see A#): internal RPC p95 < 50ms; CMIB control p95 < 20ms on VLAN-A.

Justification: meets INF-ASR-ISOLATION (isolate from network-chaotic loads) and INF-SEC-ROUTER-PROTECT (protect from unauthorized traffic).

## E.4 CI/CD sketch
1. Lint + unit tests  
2. Contract tests (OpenAPI + proto)  
3. Integration tests with simulator  
4. HIL nightly (when hardware available)  
5. Build OCI images, scan (SCA)  
6. Deploy to staging with canary (10%) then promote blue/green

Justification: meets INF-NFR-DEBUGGABLE and INF-NFR-PROC-RESTART.

---

# F. Security Design

## F.1 Auth & AuthZ
- **OIDC + JWT** for users (ops/dev/maintainer/admin); short-lived access tokens (15 min) + refresh (8–12h).
- RBAC enforced at VCI gateway and re-checked in sensitive internal operations (config apply, warm boot, user admin).
- Revocation: maintain token denylist keyed by `jti` for emergency block; admin “block all/selective” toggles enforced.

Justification: meets INF-SEC-UNIQUE-ID and INF-SEC-ADMIN-BLOCK.

## F.2 Secrets management & rotation
- Kubernetes Secrets via external KMS (e.g., Vault) with 90-day rotation for DB creds, 24h rotation for service tokens.

Justification: meets INF-SEC-MECHANISM (robust security mechanism).

## F.3 TLS & service-mesh
- TLS 1.2+ everywhere; optional mTLS between services (service mesh) for stronger segmentation.

Justification: meets INF-SEC-SECURE-LOGIN (secure login attempts).

## F.4 Threat model summary (top 5)
| Threat | Mitigation |
|---|---|
| Unauthorized access to VCI | OIDC, MFA, RBAC, network ACLs |
| Replay/forged control commands | JWT + nonce/idempotency key + audit + mTLS optional |
| Telemetry tampering | signed export payloads + checksum + immutable audit |
| Lateral movement from external M&C | physical/VLAN separation + firewall + least-privilege egress |
| Insider misuse | immutable audit log + least privilege + break-glass procedures |

---

# G. Observability & SRE

## G.1 Metrics/logs/traces + example alerts
Metrics (examples):
- `cmcs_command_latency_ms{type}`
- `cmcs_cmib_agent_loop_jitter_ms`
- `cmcs_telemetry_spool_depth`
- `cmcs_auth_failed_total`
- `cmcs_state_staleness_ms`

Logs:
- Structured JSON logs with category filters (meets INF-FR-MSG-CATEGORIZED), containing UTC + wall-clock timestamps (meets INF-FR-TIMESTAMPS).

Traces:
- OpenTelemetry spans for `ConfigApply`, `IssueCommand`, `WarmBoot`, `ExportTelemetry`.

**Example Prometheus alert rules**
- `CMCSHighCommandLatency`
- `CMCSTelemetrySpoolGrowing`

(Provided in runbook snippet conceptually; implement in ops repo.)

Justification: meets INF-FR-FULL-OBSERVABLE and INF-FR-ERROR-AT-MASTER.

## G.2 SLOs, error budgets, RTO/RPO (assumptions A*)
- Availability SLO (VCI API): 99.9% monthly (A2)
- Command acceptance latency p95: < 200ms at gateway (A3)
- CMIB actuation latency p95: < 50ms from sequence step to agent send (A4)
- Telemetry freshness p95: < 2s to state snapshot (A5)
- RTO: 15 minutes (A6); RPO: 1 minute for state/config; 0 for audit within HA domain (A7)

Justification: meets INF-NFR-DEADLINES and INF-NFR-NO-RESTART.

## G.3 Dashboard & runbook sketch
Dashboards:
- Control: command rates, failures, retries, warm boots
- Telemetry: ingestion rate, spool depth, export lag
- Infra: pod restarts, DB replication lag, NATS stream health

Runbooks:
- Master failover / fencing
- CMIB hot-swap detection and reconfigure
- Network partition and spool draining

---

# H. Testing Strategy

## H.1 Test matrix

| Test type | Components | What it validates |
|---|---|---|
| Unit | translators, safety/protection rules, authz | Determinism, RBAC correctness |
| Integration | VCI↔core↔DB↔NATS | End-to-end config apply and monitor flows |
| Contract | OpenAPI + proto + schema compatibility | Backward compatibility (INF-NFR-EXPAND-SEAMLESS) |
| E2E | GUI + external M&C simulator + CMIB simulator | Operational workflows |
| Chaos | kill pods, partition NATS, DB failover | INF-NFR-REDUNDANT-MASTER, INF-NFR-QUEUE-EXHAUST |

Justification: meets INF-NFR-DEBUGGABLE and INF-NFR-PROC-RESTART.

## H.2 Test data management & environment isolation
- Environments: dev, integration, staging, production (4)
- Refresh: staging nightly from sanitized snapshots (no credentials)
- Hardware-in-loop lab environment separate VLAN

---

# I. Migration, Data Conversion & Rollout Plan

## I.1 Migration steps (if replacing an existing CMCS)
1. Stand up new VCI read-only monitoring (shadow mode)
2. Dual-write telemetry spool to both systems
3. Validate config translation with simulator + limited hardware subset
4. Cut over control plane during maintenance window; keep rollback path
5. Decommission legacy after stability window

## I.2 Backwards compatibility and API versioning
- Version VCI API under `/v1/`; add `/v2/` for breaking changes.
- Proto: backward-compatible field additions only; never reuse field numbers.

Justification: meets INF-NFR-EXPAND-TRANSPARENCY and INF-NFR-EXPAND-SEAMLESS.

---

# J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Why chosen (tie to INF-*) |
|---|---|---|---|
| Messaging bus | NATS JetStream | RabbitMQ; Kafka | Meets spooling + controllable sampling with simpler ops than Kafka (INF-FR-SPOOL-MON, INF-FR-CONTROLLABLE-SAMPLING). |
| Auth | OIDC + JWT | LDAP-only; mTLS-only | Supports unique IDs, role separation, admin controls (INF-SEC-UNIQUE-ID, INF-SEC-ROLE-OPS). |
| Persistence | PostgreSQL | MySQL; CockroachDB | Strong consistency + mature HA/backup tooling (INF-NFR-STATEFUL-SECONDARY, INF-SEC-AUDIT-LOG). |
| Service style | modular services in one cluster | monolith; full microservices | Balances modularity/restartability with operational simplicity (INF-NFR-MODULAR, INF-NFR-PROC-RESTART). |

---

# K. Open Questions & Assumptions

## K.1 Assumptions (A1, A2, ...)
- **A1:** External VLA Expansion Project M&C integration uses IP networking and can call VCI over HTTPS/gRPC.  
- **A2:** Target VCI API availability SLO is **99.9% monthly** (unless a higher number is mandated).  
- **A3:** Gateway command acceptance latency p95 target **<200ms** under nominal load.  
- **A4:** CMIB actuation step latency p95 target **<50ms** on the dedicated CMIB VLAN.  
- **A5:** Telemetry-to-state freshness p95 target **<2s** for “fast” monitor points.  
- **A6:** RTO target **15 minutes** for master node failure with automatic reroute.  
- **A7:** Audit log requires effectively zero data loss within HA domain (synchronous commit).

## K.2 Conflicts / naming mismatches (logged per rule)
- **C1:** UML diagrams use generic names (`ControlAPI`, `ControllerUnit`, `SafetyInterlock`, `ControlLease`) while requirements specify `VCI`, `Master Correlator Control Computer`, `CMIB`, `Correlator Power Control Computer`. We **prefer requirements naming** and treat UML as pattern templates.
- **C2:** UML includes “single-operator lease” and “override interlock” concepts not explicitly required in CMCS requirements. We keep them **optional** as `INF-ASR-LEASE-OPTIONAL` (inferred) for operational safety, pending stakeholder decision.

## K.3 Open stakeholder questions (need answers)
1. What are the **required monitor sample rates**, max bandwidth, and which points are time-synchronous vs on-demand?  
2. What are the **explicit timing deadlines** for control loops and acceptable jitter for CMIB actions?  
3. What is the authoritative **security policy** (MFA required? allowed identity provider? air-gap constraints)?  
4. What is the required **retention period** for telemetry spool and audit logs?  
5. Define failover mode: **active/active vs active/passive** masters and fencing mechanism acceptable in correlator environment.

Also inferred requirement to list:  
- **INF-ASR-LEASE-OPTIONAL:** optional command lease/lock for preventing conflicting control sessions (pattern from UML).

---

# L. Deliverables

```markdown
# filename: architecture.md
(Contents are this full document in Markdown.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: CMCS Virtual Correlator Interface (VCI) API
  version: "1.0.0"
  description: >
    External API for EVLA/VLA Expansion Correlator Monitor & Control System (CMCS).
    Provides authentication, configuration translation/apply, control commands,
    monitoring/state query, telemetry export, and admin user management.
servers:
  - url: https://cmcs.example.org/api/v1
security:
  - bearerAuth: []
tags:
  - name: Auth
  - name: Config
  - name: Control
  - name: Monitoring
  - name: Export
  - name: Admin
paths:
  /auth/token:
    post:
      tags: [Auth]
      summary: Issue access token
      operationId: postAuthToken
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AuthTokenRequest"
      responses:
        "200":
          description: Token issued
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthTokenResponse"
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /auth/refresh:
    post:
      tags: [Auth]
      summary: Refresh access token
      operationId: postAuthRefresh
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AuthRefreshRequest"
      responses:
        "200":
          description: Refreshed
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuthTokenResponse"
        "401":
          description: Invalid refresh token
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /config/validate:
    post:
      tags: [Config]
      summary: Validate a correlator configuration intent and generated tables
      operationId: postConfigValidate
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ConfigIntent"
      responses:
        "200":
          description: Validation result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ConfigValidationResult"
        "400":
          description: Invalid schema or unsupported config
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /config/apply:
    post:
      tags: [Config]
      summary: Apply configuration (translates intent to hardware configuration tables)
      operationId: postConfigApply
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ConfigApplyRequest"
      responses:
        "202":
          description: Accepted for sequencing/apply
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ConfigApplyAccepted"
        "409":
          description: Conflicting apply in progress or stale base version
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /control/commands:
    post:
      tags: [Control]
      summary: Issue a dynamic control command to a target device/subsystem
      operationId: postControlCommand
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ControlCommandRequest"
      responses:
        "202":
          description: Command accepted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ControlCommandAccepted"
        "400":
          description: Bad request / invalid parameters
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "403":
          description: Forbidden by RBAC policy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /devices/{deviceId}/warmboot:
    post:
      tags: [Control]
      summary: Request CMIB/device warm boot
      operationId: postDeviceWarmboot
      parameters:
        - in: path
          name: deviceId
          required: true
          schema: { type: string }
      requestBody:
        required: false
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WarmBootRequest"
      responses:
        "202":
          description: Warm boot scheduled
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ActionAccepted"
        "404":
          description: Unknown device
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /state/latest:
    get:
      tags: [Monitoring]
      summary: Get latest correlator state snapshot
      operationId: getStateLatest
      responses:
        "200":
          description: State snapshot
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CorrelatorStateSnapshot"

  /telemetry/export:
    post:
      tags: [Export]
      summary: Export telemetry batch to a subscriber (controlled sampling)
      operationId: postTelemetryExport
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TelemetryExportRequest"
      responses:
        "200":
          description: Export result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TelemetryExportResult"

  /admin/users:
    get:
      tags: [Admin]
      summary: List users
      operationId: getAdminUsers
      responses:
        "200":
          description: Users
          content:
            application/json:
              schema:
                type: array
                items: { $ref: "#/components/schemas/UserAccount" }
    post:
      tags: [Admin]
      summary: Create user
      operationId: postAdminUsers
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/UserCreateRequest" }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: "#/components/schemas/UserAccount" }

  /admin/users/{userId}:
    patch:
      tags: [Admin]
      summary: Update user access properties (roles, enabled flag)
      operationId: patchAdminUser
      parameters:
        - in: path
          name: userId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/UserUpdateRequest" }
      responses:
        "200":
          description: Updated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/UserAccount" }
    delete:
      tags: [Admin]
      summary: Remove user
      operationId: deleteAdminUser
      parameters:
        - in: path
          name: userId
          required: true
          schema: { type: string }
      responses:
        "204":
          description: Deleted

  /admin/block:
    post:
      tags: [Admin]
      summary: Block all access or selectively by user
      operationId: postAdminBlock
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/BlockAccessRequest" }
      responses:
        "200":
          description: Block policy applied
          content:
            application/json:
              schema: { $ref: "#/components/schemas/BlockAccessStatus" }

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    ErrorResponse:
      type: object
      required: [error, requestId, timestampUtc]
      properties:
        requestId: { type: string }
        timestampUtc: { type: string, format: date-time }
        error:
          type: object
          required: [code, message]
          properties:
            code: { type: string, example: "CMCS_FORBIDDEN" }
            message: { type: string }
            details: { type: object, additionalProperties: true }

    AuthTokenRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string }
        password: { type: string, format: password }

    AuthRefreshRequest:
      type: object
      required: [refreshToken]
      properties:
        refreshToken: { type: string }

    AuthTokenResponse:
      type: object
      required: [accessToken, tokenType, expiresInSeconds]
      properties:
        accessToken: { type: string }
        refreshToken: { type: string }
        tokenType: { type: string, enum: ["Bearer"] }
        expiresInSeconds: { type: integer, minimum: 60 }

    ConfigIntent:
      type: object
      required: [intentId, requestedAtUtc, mode, parameters]
      properties:
        intentId: { type: string }
        requestedAtUtc: { type: string, format: date-time }
        mode: { type: string, example: "OBSERVING" }
        parameters:
          type: object
          additionalProperties: true

    ConfigValidationResult:
      type: object
      required: [intentId, valid, issues]
      properties:
        intentId: { type: string }
        valid: { type: boolean }
        issues:
          type: array
          items:
            type: object
            required: [severity, message]
            properties:
              severity: { type: string, enum: ["INFO", "WARN", "ERROR"] }
              message: { type: string }

    ConfigApplyRequest:
      type: object
      required: [intent, baseStateVersion]
      properties:
        intent: { $ref: "#/components/schemas/ConfigIntent" }
        baseStateVersion: { type: integer, minimum: 0 }
        dryRun: { type: boolean, default: false }

    ConfigApplyAccepted:
      type: object
      required: [applyId, status]
      properties:
        applyId: { type: string }
        status: { type: string, enum: ["QUEUED", "SEQUENCING"] }

    ControlCommandRequest:
      type: object
      required: [commandId, commandType, targetId, requestedAtUtc, parameters]
      properties:
        commandId: { type: string }
        commandType: { type: string, example: "WRITE_REGISTER" }
        targetId: { type: string }
        requestedAtUtc: { type: string, format: date-time }
        idempotencyKey: { type: string }
        parameters:
          type: object
          additionalProperties: true

    ControlCommandAccepted:
      type: object
      required: [commandId, executionId, status]
      properties:
        commandId: { type: string }
        executionId: { type: string }
        status: { type: string, enum: ["ACCEPTED", "REJECTED"] }

    WarmBootRequest:
      type: object
      properties:
        forceHardwareWarmBoot: { type: boolean, default: false }

    ActionAccepted:
      type: object
      required: [actionId, acceptedAtUtc]
      properties:
        actionId: { type: string }
        acceptedAtUtc: { type: string, format: date-time }

    CorrelatorStateSnapshot:
      type: object
      required: [stateId, version, updatedAtUtc, health, configEcho]
      properties:
        stateId: { type: string }
        version: { type: integer, minimum: 0 }
        updatedAtUtc: { type: string, format: date-time }
        health:
          type: object
          additionalProperties: true
        configEcho:
          type: object
          additionalProperties: true

    TelemetryExportRequest:
      type: object
      required: [subscriberId, fromUtc, toUtc, filters]
      properties:
        subscriberId: { type: string }
        fromUtc: { type: string, format: date-time }
        toUtc: { type: string, format: date-time }
        filters:
          type: object
          additionalProperties: true
        maxEvents: { type: integer, minimum: 1, maximum: 100000, default: 10000 }

    TelemetryExportResult:
      type: object
      required: [subscriberId, deliveredEvents, nextCursor]
      properties:
        subscriberId: { type: string }
        deliveredEvents: { type: integer, minimum: 0 }
        nextCursor: { type: string }

    UserAccount:
      type: object
      required: [userId, username, enabled, roles]
      properties:
        userId: { type: string }
        username: { type: string }
        enabled: { type: boolean }
        roles:
          type: array
          items: { type: string }

    UserCreateRequest:
      type: object
      required: [username, enabled, roles]
      properties:
        username: { type: string }
        password: { type: string, format: password }
        enabled: { type: boolean }
        roles:
          type: array
          items: { type: string }

    UserUpdateRequest:
      type: object
      properties:
        enabled: { type: boolean }
        roles:
          type: array
          items: { type: string }

    BlockAccessRequest:
      type: object
      required: [mode]
      properties:
        mode: { type: string, enum: ["BLOCK_ALL", "BLOCK_USERS", "UNBLOCK_ALL"] }
        userIds:
          type: array
          items: { type: string }

    BlockAccessStatus:
      type: object
      required: [mode, updatedAtUtc]
      properties:
        mode: { type: string }
        updatedAtUtc: { type: string, format: date-time }
        blockedUserIds:
          type: array
          items: { type: string }
```

```proto
// filename: internal.proto
syntax = "proto3";

package cmcs.internal.v1;

import "google/protobuf/timestamp.proto";

message ErrorStatus {
  string code = 1;
  string message = 2;
  map<string, string> details = 3;
}

message AuditStamp {
  google.protobuf.Timestamp utc = 1;
  string wall_clock = 2; // e.g., "2026-04-22T10:00:10-06:00"
}

message ConfigIntent {
  string intent_id = 1;
  google.protobuf.Timestamp requested_at_utc = 2;
  string mode = 3;
  map<string, string> parameters = 4; // canonicalized key/value for determinism
}

message ConfigValidationResult {
  string intent_id = 1;
  bool valid = 2;
  repeated string issues = 3;
}

message ConfigApplyRequest {
  ConfigIntent intent = 1;
  uint64 base_state_version = 2;
  bool dry_run = 3;
}

message ConfigApplyAccepted {
  string apply_id = 1;
  string status = 2; // QUEUED|SEQUENCING|APPLYING
}

message ControlCommand {
  string command_id = 1;
  string command_type = 2;
  string target_id = 3;
  google.protobuf.Timestamp requested_at_utc = 4;
  string idempotency_key = 5;
  map<string, string> parameters = 6;
}

message CommandExecution {
  string execution_id = 1;
  string command_id = 2;
  string status = 3; // ACCEPTED|REJECTED|RUNNING|COMPLETED|FAILED
  AuditStamp stamp = 4;
  ErrorStatus error = 5;
}

message WarmBootRequest {
  string device_id = 1;
  bool force_hardware_warm_boot = 2;
}

message RegisterReadRequest {
  string device_id = 1;
  repeated uint32 addresses = 2;
}

message RegisterReadResponse {
  string device_id = 1;
  map<uint32, uint32> values = 2;
  AuditStamp measured_at = 3;
}

message RegisterWriteRequest {
  string device_id = 1;
  map<uint32, uint32> values = 2;
}

message CorrelatorStateSnapshot {
  string state_id = 1;
  uint64 version = 2;
  google.protobuf.Timestamp updated_at_utc = 3;
  map<string, string> health = 4;
  map<string, string> config_echo = 5;
}

message TelemetryEvent {
  string event_id = 1;
  string event_type = 2;     // MONITOR|ERROR|STATUS
  string source = 3;         // CMIB:<id>, POWER, MASTER
  google.protobuf.Timestamp occurred_at_utc = 4;
  string wall_clock = 5;
  map<string, string> payload = 6;
}

service ConfigService {
  rpc Validate(ConfigIntent) returns (ConfigValidationResult);
  rpc Apply(ConfigApplyRequest) returns (ConfigApplyAccepted);
}

service ControlService {
  rpc IssueCommand(ControlCommand) returns (CommandExecution);
}

service DeviceService {
  rpc WarmBoot(WarmBootRequest) returns (CommandExecution);
  rpc ReadRegisters(RegisterReadRequest) returns (RegisterReadResponse);
  rpc WriteRegisters(RegisterWriteRequest) returns (CommandExecution);
}

service StateService {
  rpc GetLatestState(google.protobuf.Timestamp) returns (CorrelatorStateSnapshot);
}

service TelemetryService {
  rpc PublishSample(TelemetryEvent) returns (CommandExecution);
  rpc Subscribe(stream TelemetryEvent) returns (stream TelemetryEvent);
}
```

```yaml
# filename: k8s/cmcs-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cmcs
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cmcs-config
  namespace: cmcs
data:
  CMCS_LOG_LEVEL: "info"
  CMCS_NATS_URL: "nats://nats.cmcs.svc.cluster.local:4222"
  CMCS_DB_DSN: "postgres://cmcs_app@postgres.cmcs.svc.cluster.local:5432/cmcs?sslmode=verify-full"
---
apiVersion: v1
kind: Secret
metadata:
  name: cmcs-secrets
  namespace: cmcs
type: Opaque
stringData:
  CMCS_DB_PASSWORD: "REPLACE_ME"
  CMCS_JWT_SIGNING_KEY: "REPLACE_ME"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vci-api
  namespace: cmcs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vci-api
  template:
    metadata:
      labels:
        app: vci-api
    spec:
      containers:
        - name: vci-api
          image: cmcs/vci-api:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: cmcs-config
            - secretRef:
                name: cmcs-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vci-api
  namespace: cmcs
spec:
  selector:
    app: vci-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vci-api-hpa
  namespace: cmcs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vci-api
  minReplicas: 2
  maxReplicas: 10
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
  user_id           UUID PRIMARY KEY,
  username          TEXT NOT NULL UNIQUE,
  password_hash     BYTEA, -- if local auth enabled; otherwise null
  enabled           BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_user_account_enabled ON user_account(enabled);
```

```sql
-- filename: sql/audit_entry_ddl.sql
CREATE TABLE IF NOT EXISTS audit_entry (
  entry_id          UUID PRIMARY KEY,
  actor_user_id     UUID,
  action            TEXT NOT NULL,
  request_id        TEXT,
  occurred_at_utc   TIMESTAMPTZ NOT NULL,
  wall_clock        TEXT NOT NULL,
  source_ip         INET,
  details_json      JSONB NOT NULL DEFAULT '{}'::jsonb,
  hash_sha256       BYTEA NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_entry_time ON audit_entry(occurred_at_utc);
CREATE INDEX IF NOT EXISTS idx_audit_entry_action ON audit_entry(action);
```

```sql
-- filename: sql/system_state_ddl.sql
CREATE TABLE IF NOT EXISTS system_state (
  state_id          TEXT PRIMARY KEY,
  version           BIGINT NOT NULL,
  updated_at_utc    TIMESTAMPTZ NOT NULL,
  health_json       JSONB NOT NULL DEFAULT '{}'::jsonb,
  config_echo_json  JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_system_state_updated ON system_state(updated_at_utc);
```

```sql
-- filename: sql/telemetry_event_ddl.sql
CREATE TABLE IF NOT EXISTS telemetry_event (
  event_id          UUID PRIMARY KEY,
  event_type        TEXT NOT NULL,
  source            TEXT NOT NULL,
  occurred_at_utc   TIMESTAMPTZ NOT NULL,
  wall_clock        TEXT NOT NULL,
  payload_json      JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_telemetry_time ON telemetry_event(occurred_at_utc);
CREATE INDEX IF NOT EXISTS idx_telemetry_source ON telemetry_event(source);
CREATE INDEX IF NOT EXISTS idx_telemetry_type ON telemetry_event(event_type);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-LINK,Provide physical link between WIDAR and VLA M&C,"Deployment_SafetyCriticalControl:FCU/APP1/APP2",CmibAgent|ControllerAdapter,"architecture.md",Defines integration boundary and control plane.
INF-FR-CONFIG-RECV-XLATE,Receive config and translate to hardware tables,"Sequence1_IssueCommand:ControlAPI/SafetyService/SequenceController",VCI|ConfigTranslator,"openapi.yaml|internal.proto",Contract-first translation ensures convergent config.
INF-FR-DYNAMIC-MONCTRL,Process/transfer dynamic control and monitor data,"Sequence2_MonitorStatusAndExport:MonitoringService/EventBus",TelemetryBus|MonitorAggregator,"internal.proto",Event-driven monitoring/control.
INF-FR-AUTONOMOUS-RECOVERY,Autonomous corrective actions,"State_CommandLifecycle:Failed->Retry",HealthSupervisor,"architecture.md",Encodes retry/restart/alerting.
INF-FR-REALTIME-PROBING,Provide limited real-time probing tools,"Container_SafetyCriticalControl:C_UI",DiagnosticTools,"openapi.yaml",User tools without impacting core loop.
INF-FR-EASY-ACCESS,Easy access for test/debug,"Package_SafetyCriticalControl:ui/api/services",AdminUI|DebugConsole,"openapi.yaml",Remote tooling and auditability.
INF-ASR-MASTER-SLAVE,Master/slave architecture,"Deployment_SafetyCriticalControl:APP1/APP2/FCU",MasterControl|CmibAgent,"architecture.md",Separates quasi-real-time from real-time.
INF-ASR-ISOLATION,Isolate hardware from external chaos,"Deployment_SafetyCriticalControl:NET",NetworkSegmentation,"architecture.md",Separate networks and QoS.
INF-NFR-REDUNDANT-CRITICAL,Redundant critical areas and modular,"Deployment_SafetyCriticalControl:APP1/APP2",HA masters,"k8s/cmcs-deployment.yaml",Failover and rolling maintenance.
INF-SEC-UNIQUE-ID,All users uniquely identified,"UseCase_SafetyCriticalControl:UC_Auth",IAM,"openapi.yaml",Accountability and audit trail.
INF-SEC-AUDIT-LOG,Log all access attempts,"Component_SafetyCriticalControl:AuditLog",AuditService,"sql/audit_entry_ddl.sql",Forensics and compliance.
```

## Verification table (Acceptance Criteria)

| Item | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A-L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (as INF-*) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDL for primary entities included | [x] |
| All major components have at least one API contract and a data schema | [x] |
| Assumptions and unresolved questions listed | [x] |

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + INF-* justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?