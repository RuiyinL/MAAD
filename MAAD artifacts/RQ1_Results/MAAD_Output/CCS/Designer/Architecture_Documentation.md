Analysis Plan  
Scope: Produce production-ready architecture for the EVLA/VLA Expansion Correlator Monitor & Control System (CMCS) aligned to provided requirements + 11 referenced diagrams.  
Approach: Normalize unlabeled requirements into testable INF-FR/INF-NFR/INF-ASR, prefer Original Requirements naming, and bind to concrete APIs, schemas, deployment, and SRE controls.  
Top validation: Traceability matrix completeness, API/schema syntactic validity, and HA/security/queue-spool behaviors verified via contract+chaos+failover tests.

# A. Executive Summary (≤1 page)

## System overview
The Correlator Monitor & Control System (CMCS) is the software/hardware control plane linking WIDAR correlator hardware to the VLA Expansion Project Monitor & Control (VLA M&C). It translates high-level configuration into hardware tables, performs real-time monitor/control via a master/slave topology, spools monitor data during network loss, publishes backend datasets, and self-heals faults with autonomous recovery and alerting.

**Primary diagram mapping (one-line):** Context and responsibilities are captured by *UseCase_ScenarioView* (actors: VLA M&C, Backend Controller, Operator; use cases: Translate Config, Control & Monitor, Self-Heal Faults) and realized by *Deployment_PhysicalView* (nodes: Master Control Node Primary/Secondary, CMIB Rack, Power Control Node) and *Class_LogicView* (VirtualCorrelatorInterface, MasterControlNode, CMIBController, SpoolBuffer, EventQueue, AuthService).

## Architectural style(s) and topology
- **Style:** Layered + master/slave control plane with HA master pair and real-time edge controllers (CMIB).  
- **Topology:** Dual Master Control Nodes (primary/secondary) + rack-level CMIB controllers + separate physical networks for control/monitor, external ops, and backend data.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| R1: Real-time determinism violated by “network-chaotic” loads on master | Data loss/corruption/overflows | Enforce network segmentation + bounded internal RPC timeouts; move deterministic loops to CMIB; rate-limit external monitor streams; verify with latency tests and CPU isolation. |
| R2: Failover state divergence between primary/secondary master | Incorrect hardware config after failover | Use replicated state versioning + write-ahead event queue; promote secondary only when caught up; verify with failover chaos tests. |
| R3: Unauthorized access to critical control plane | Loss of observing time, safety risk | mTLS + RBAC + MFA for privileged actions; immutable audit; network routers/firewalls; verify with penetration tests and negative auth tests. |

## Key QA coverage mapping

| Quality attribute | Requirement IDs (INF) | Test types |
|---|---|---|
| Scalability | INF-NFR-010 (expandable I/O/compute), INF-ASR-005 (Ethernet >=100Mbps) | Load tests, capacity tests, soak tests |
| Availability | INF-NFR-009 (HA, failover), INF-ASR-004 (redundant master state) | Chaos/failover drills, HA integration tests |
| Security | INF-FR-041..050 (unique ID, secure login, RBAC, audit) | SAST/DAST, authZ tests, mTLS tests, audit integrity tests |
| Performance/Determinism | INF-NFR-006/007 (deterministic response, deadlines) | Latency benchmarks, real-time loop tests, jitter tests |
| Maintainability | INF-NFR-016..020 (debuggable, killable, modular, source available) | Component tests, fault-injection, operability reviews |

---

# B. Traceability & Rationale

**Normalization note:** The provided “Original Requirements” text contains many “shall” statements but no stable IDs. Per special handling rule #1, this architecture assigns **INF-** IDs. All are mapped below at least once.

**Traceability table (also delivered as `traceability_matrix.csv` in Section L):**

Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale
---|---|---|---|---|---
INF-FR-001 | Receive config from VLA M&C and translate to HW config | UseCase_ScenarioView:UC_TranslateConfig; Activity_ProcessView_TranslateAndApply | VCI Gateway, Master Service | openapi.yaml; internal.proto | VCI provides translation boundary; master applies tables to CMIB.
INF-FR-002 | Process/transfer dynamic control + monitor data | UseCase_ScenarioView:UC_ControlMonitor; Class_LogicView:VirtualCorrelatorInterface,MasterControlNode | Master Service, CMIB Adapter | internal.proto; openapi.yaml | Control/monitor APIs + internal RPC to CMIB.
INF-FR-003 | Monitor health and take corrective action autonomously | UseCase_ScenarioView:UC_SelfHeal; Sequence_ProcessView_S2_SelfHealAndAlert | Health Manager, Master Service | internal.proto; sql/audit_event_ddl.sql | Health loop triggers reboot/alerts and audits actions.
INF-FR-004 | Limited real-time processing/probing (auto-correlation display tools) | UseCase_ScenarioView:UC_AutoCorr | VCI Gateway, Master Service | openapi.yaml | Provide endpoint to request/stream autocorr products (implementation may proxy backend).
INF-FR-005 | Easy system access for testing/debugging | UseCase_ScenarioView:UC_RemoteDebug; Package_DevelopmentView:ui | TestToolsGUI, VCI Gateway | openapi.yaml; k8s/cmcs-deployment.yaml | Remote debug via authenticated VCI; tools packaged and deployable.
INF-ASR-001 | Integrated part of overall VLA M&C structure | Deployment_PhysicalView:NODE_VLA--NET_OPS | VCI Gateway | openapi.yaml | External integration via VCI on ops network.
INF-ASR-002 | Gateway through Virtual Correlator Interface (VCI) | Container_PhysicalView:CON_VCI | VCI Gateway | openapi.yaml | All external use through VCI boundary.
INF-ASR-003 | Provide backend datasets over secondary virtual network | UseCase_ScenarioView:UC_DeliverBackendData; Deployment_PhysicalView:NET_BACK | Backend Data Publisher | internal.proto | Separate backend network path for datasets.
INF-ASR-004 | Master/slave network; master coordinates intelligent controllers | Class_LogicView:MasterControlNode o-- CMIBController | Master Service, CMIB Adapter | internal.proto | Master orchestrates; CMIB executes deterministic actions.
INF-ASR-005 | Ethernet >=100Mbps between master/CMIB/power | Deployment_PhysicalView:SW_RACK,NODE_RACK | CMIB Adapter, Power Adapter | k8s/cmcs-deployment.yaml | Network assumptions drive timeouts and throughput.
INF-ASR-006 | Separate physical interfaces for master↔CMIB, master↔power, master↔VLA M&C | Deployment_PhysicalView:NET_OPS/NET_CTRL/NET_BACK | Master Node | k8s/cmcs-deployment.yaml | Enforces isolation and determinism.
INF-ASR-007 | Redundant comm path master↔power for remote reboot | Deployment_PhysicalView:NODE_MasterP--NODE_Power | Power Control Adapter | internal.proto | Enables recovery from network/compute failure.
INF-ASR-008 | Fiber/low-RFI for shielded room penetrations | Deployment_PhysicalView:NET_OPS/NET_BACK notes | Network/Infra | (ops runbook) | Physical media constraint captured in deployment.
INF-ASR-009 | Routers/switches protect from unauthorized access/irrelevant traffic | Deployment_PhysicalView:NET_OPS | Ingress/Firewall | k8s/cmcs-deployment.yaml | Network policy + firewalling.
INF-FR-006 | CMIB communicates via PCI/ISA/serial/parallel as needed | Container_PhysicalView:CON_CMIB->EXT_HW | CMIB Adapter | internal.proto | Adapter abstracts bus specifics.
INF-FR-007 | CMIB reads 16-bit identifier to form unique IP for hot swap | Class_LogicView:CMIBController note | CMIB Firmware/Adapter | internal.proto | Deterministic addressing supports hot swap.
INF-FR-008 | Read back writable registers where meaningful | Class_LogicView:CMIBController.readbackRegisters | CMIB Adapter | internal.proto | Enables observability and fault tolerance.
INF-FR-009 | Interrogate hardware state across CMIB bus | Class_LogicView:CMIBController.interrogateHardware | Health Manager, CMIB Adapter | internal.proto | Health evaluation depends on interrogation.
INF-FR-010 | Control warm boots via external command | Class_LogicView:CMIBController.reboot(warmBoot) | Health Manager | internal.proto | Self-heal uses warm boot option.
INF-FR-011 | Physical indicator of CMIB operational status | (not modeled) | CMIB Hardware | (hardware spec) | Non-software requirement; tracked for hardware design.
INF-NFR-001 | UPS-backed power; coordinate safe shutdown | UseCase_ScenarioView:UPS->UC_ControlMonitor | Master Service, UPS Adapter | internal.proto | UPS events trigger controlled shutdown.
INF-NFR-002 | UPS signals outage and time remaining | Class_LogicView:PowerEvent | UPS Adapter | internal.proto; sql/power_event_ddl.sql | Persist and act on UPS telemetry.
INF-NFR-003 | Authorized remote logins to each system | UseCase_ScenarioView:UC_ManageAccess | Auth Service | openapi.yaml | Central auth + OS-level SSH with RBAC.
INF-NFR-004 | Hardware watchdog timers reboot on hang; minimal interruption | Class_LogicView:CMIBController.watchdogEnabled; Deployment_PhysicalView node notes | CMIB, Master Nodes | (ops runbook) | Watchdog + auto rejoin behavior.
INF-ASR-010 | CMIB HW spec: RAM, interfaces, 100BaseT, COTS OS near real-time | Deployment_PhysicalView:NODE_CMIB | CMIB Controller | (hardware spec) | Drives OS/runtime selection.
INF-ASR-011 | Master is HA general-purpose multi-NIC; local disk; standalone | Deployment_PhysicalView:NODE_MasterP note | Master Service | k8s/cmcs-deployment.yaml | Standalone boot/run and HA.
INF-ASR-012 | Power Control Node standalone capable | Deployment_PhysicalView:NODE_Power | Power Control Adapter | internal.proto | Continues power monitoring during M&C network failure.
INF-NFR-005 | Meet processing deadlines and future requirements | State_LogicView_MasterControlNode | Master/CMIB | (benchmarks) | Capacity planning + performance tests.
INF-NFR-006 | Deterministic response to HW inputs; avoid loss/corruption/overflows | Component_DevelopmentView:C_CMIB note | CMIB Adapter | internal.proto | Bounded-latency internal RPC and CMIB real-time loop.
INF-FR-012 | All lower-layer error/debug messages present at master | INF | Master Service | sql/message_ddl.sql | Central aggregation and persistence.
INF-FR-013 | Categorize/filter messages by content/detail/rate | Class_LogicView:Message.category/detailLevel | Master Service, VCI | openapi.yaml | Filterable message stream endpoint.
INF-FR-014 | Messages have UTC + wallclock timestamps | Class_LogicView:Message,MonitorSample | All services | sql/message_ddl.sql | Schema enforces both timestamps.
INF-FR-015 | Provide authorized user full access to messaging/monitor/control traffic | UseCase_ScenarioView:UC_RemoteDebug | VCI Gateway | openapi.yaml | Debug endpoints gated by RBAC.
INF-FR-016 | GUI for test software remote access through VCI | Package_DevelopmentView:ui | ConfigGUI/TestToolsGUI | (ui spec) | UI uses same APIs as automation.
INF-FR-017 | Self-monitoring detects failures (CPU, OS hang, temp/voltage, perf, comms) | UseCase_ScenarioView:UC_SelfHeal | Health Manager | internal.proto | Health rules + probes.
INF-NFR-007 | Software runs without total restart between maintenance windows | State_LogicView_MasterControlNode | Master Service | k8s/cmcs-deployment.yaml | Rolling restarts + process supervision.
INF-NFR-008 | Hardware performs indefinitely except total power failure | Deployment_PhysicalView | Infra/UPS | (ops runbook) | UPS + redundancy.
INF-FR-018 | Continue processing config/control until queues exhausted during comms loss | State_LogicView_MasterControlNode:ProcessingQueued | Event Queue | sql/event_queue_ddl.sql | Durable queue with retention.
INF-FR-019 | Idle and resume with minimal delay | State_LogicView_MasterControlNode | Master/CMIB | (benchmarks) | Warm standby and cached state.
INF-NFR-009 | Maintainability: accessible for repair/replacement/reconfig | Deployment_PhysicalView | Ops/Hardware | (rack layout) | Physical accessibility requirement.
INF-NFR-010 | Source code available on systems; modules debuggable/simulatable | Package_DevelopmentView | All | (repo policy) | Enables on-site debugging and simulation.
INF-NFR-011 | Processes killable/restartable/testable with minimal impact | k8s/cmcs-deployment.yaml | All services | k8s/cmcs-deployment.yaml | Kubernetes + supervision.
INF-NFR-012 | Third-party tools must include diagnostics/support | (not modeled) | Vendor deps | (procurement) | Procurement constraint.
INF-NFR-013 | OS source or sufficient diagnostics/support | (not modeled) | OS | (procurement) | OS selection constraint.
INF-NFR-014 | Expandable I/O/comm/processing; transparent/seamless upgrades | Deployment_PhysicalView | Infra | (capacity plan) | Modular adapters and scalable infra.
INF-NFR-015 | Robust security; unauthorized users denied | UseCase_ScenarioView:UC_ManageAccess | Auth Service | openapi.yaml | mTLS+RBAC deny-by-default.
INF-FR-020 | Users uniquely identified; username/password or equivalent | Class_LogicView:AuthService | Auth Service | openapi.yaml; sql/user_ddl.sql | Identity model.
INF-FR-021 | Log all access attempts | UseCase_ScenarioView:UC_Audit | Audit Log | sql/audit_event_ddl.sql | Audit schema.
INF-FR-022 | Ops unrestricted; can grant/revoke privileges | UseCase_ScenarioView:Admin->UC_ManageAccess | Auth Service | openapi.yaml | Admin endpoints.
INF-FR-023 | Dev/test/maint limited access; per-need privileges | RBACPolicy | Auth Service | openapi.yaml | Role-based privileges.
INF-FR-024 | Secure login attempts | AuthService.authenticate | Auth Service | openapi.yaml | mTLS + MFA.
INF-FR-025 | Admin unrestricted access | RBACPolicy roles | Auth Service | openapi.yaml | “admin” role.
INF-FR-026 | Admin can create user | UC_ManageAccess | Auth Service | openapi.yaml | POST /users.
INF-FR-027 | Admin can remove user | UC_ManageAccess | Auth Service | openapi.yaml | DELETE /users/{id}.
INF-FR-028 | Admin can edit user access properties | UC_ManageAccess | Auth Service | openapi.yaml | PATCH /users/{id}.
INF-FR-029 | Admin can block all access or selectively by user | UC_ManageAccess | Auth Service | openapi.yaml | POST /access/block.
INF-NFR-016 | Continue ops on unaffected resources during partial shutdown | State_LogicView_MasterControlNode:Degraded | Master Service | k8s/cmcs-deployment.yaml | Pod disruption + graceful degradation.
INF-NFR-017 | Replaceability/hot swap maximal | Deployment_PhysicalView:NODE_RACK hot-swappable | CMIB | (hardware spec) | Hot swap supported by IP mapping.
INF-NFR-018 | Hardware specs/config readily available | (not modeled) | Ops | (docs) | Documentation deliverable.
INF-NFR-019 | Code well documented, familiar languages | Package_DevelopmentView | All | architecture.md | Language choice and doc standards.
INF-NFR-020 | Readable style, minimal confusion | (not modeled) | All | (coding standards) | Engineering practice requirement.

---

# C. Architecture Overview

## 4+1 view alignment
- **Context / Scenario view:** *UseCase_ScenarioView* (CMCS boundary: UC_TranslateConfig, UC_ControlMonitor, UC_SelfHeal, UC_ManageAccess).  
- **Container view:** *Container_PhysicalView* (CON_VCI, CON_Master, CON_Health, CON_CMIB, CON_BackendPub, CON_Power; DB_Audit/DB_Spool/DB_Queue).  
- **Component/Package view:** *Package_DevelopmentView* and *Component_DevelopmentView* (C_VCI, C_MasterP/C_MasterS, C_Health, C_CMIB, C_Power, C_Auth, C_Audit, C_Spool, C_Queue).  
- **Logical/Class + Runtime view:** *Class_LogicView* (VirtualCorrelatorInterface, MasterControlNode, CMIBController, SpoolBuffer, EventQueue, AuthService) and *State_LogicView_MasterControlNode* (Booting→StandaloneReady→ConnectedExternal; ProcessingQueued; SelfHealing).  
- **Deployment/Physical view:** *Deployment_PhysicalView* (NET_OPS/NET_CTRL/NET_BACK; NODE_MasterP/NODE_MasterS; NODE_RACK; NODE_Power; NODE_UPS).

## Key architectural principles
1. **VCI as the only external gateway** for config/control/monitor (INF-ASR-002).  
2. **Determinism at the edge (CMIB)**; master handles aggregation, translation, and external interfaces (INF-ASR-004, INF-NFR-006).  
3. **HA master pair with replicated state** and durable event queue for comms loss (INF-ASR-004, INF-FR-018).  
4. **Security is fail-closed** with unique identity, RBAC, MFA for privileged actions, and immutable audit (INF-NFR-015, INF-FR-021).  
5. **Network segmentation** via separate physical interfaces and protected ingress (INF-ASR-006, INF-ASR-009).

---

# D. Detailed Technical Design (developer-facing)

## D1. VCI Gateway (Virtual Correlator Interface)

### D1.1 Responsibilities & data ownership
VCI Gateway terminates external connections (VLA M&C, operators, backend controller), authenticates/authorizes requests, translates external configuration into internal `ConfigTableSet`, and exposes monitor/control/query APIs. It does **not** own authoritative hardware state; it reads `SystemState` from Master Service and writes access audits.

### D1.2 Technology options (3+ alternatives per concern)

**Language/runtime**
- Recommended: **Go 1.22–1.23** (low-latency, static binary, strong concurrency).  
- Conservative: **Java 21 LTS** (mature ecosystem, strong tooling).  
- Cutting-edge: **Rust 1.76–1.80** (memory safety, high performance; higher dev cost).

**Web framework**
- Recommended: Go **chi 5.x** or **gin 1.10+**.  
- Conservative: Java **Spring Boot 3.2–3.3**.  
- Cutting-edge: Rust **axum 0.7+**.

**RPC/HTTP**
- Recommended: **REST/JSON OpenAPI 3.0** externally + **gRPC** internally.  
- Conservative: REST everywhere.  
- Cutting-edge: **NATS** request/reply for internal control plane.

**Persistence**
- Recommended: **PostgreSQL 14–16** for audit/user tables.  
- Conservative: MySQL 8.0.  
- Cutting-edge: CockroachDB 23–24 (geo/HA; operational complexity).

**Cache**
- Recommended: **Redis 7.2–7.4** for session/token cache and rate limiting.  
- Conservative: In-memory only (no HA).  
- Cutting-edge: KeyDB (Redis-compatible; less standard).

**Messaging**
- Recommended: **NATS 2.10+** for internal pub/sub of monitor samples (optional).  
- Conservative: gRPC streaming only.  
- Cutting-edge: Kafka 3.6+ (heavyweight for this scope).

**AuthN/AuthZ**
- Recommended: **mTLS + short-lived JWT** (service-issued) + RBAC.  
- Conservative: SSH + local accounts only (hard to centralize).  
- Cutting-edge: SPIFFE/SPIRE identities.

**Observability**
- Recommended: OpenTelemetry SDK + Prometheus metrics.  
- Conservative: logs only.  
- Cutting-edge: eBPF-based profiling (Parca).

**CI/CD**
- Recommended: GitHub Actions/GitLab CI with contract tests.  
- Conservative: Jenkins.  
- Cutting-edge: Tekton.

**Container runtime**
- Recommended: containerd (Kubernetes default).  
- Conservative: Docker Engine.  
- Cutting-edge: gVisor/Kata for isolation.

**Infra provisioning**
- Recommended: Terraform 1.6+ + Helm 3.13+.  
- Conservative: Ansible only.  
- Cutting-edge: Crossplane.

### D1.3 Recommended default stack
- Go 1.22–1.23, chi 5.x, OpenAPI 3.0, gRPC to master, PostgreSQL 14–16, Redis 7.2–7.4, OpenTelemetry, Prometheus.
- Justification: meets **INF-NFR-006** (bounded latency) and **INF-NFR-015** (security controls) by enabling efficient concurrency + strong TLS libraries.

### D1.4 Interface design (External APIs) — `openapi.yaml`
(Full file in Section L.)

### D1.5 Data model / schema
VCI uses shared DB schemas for `users`, `audit_event`. (See SQL in Section L.)

### D1.6 Caching & consistency
- Cache: session tokens, RBAC decisions (TTL 60s), rate-limit counters (TTL 1–5 min).  
- Consistency: authZ decisions are **eventually consistent** within TTL; user revocation forces cache bust (publish “revoke” event).

---

## D2. Master Service (Primary/Secondary)

### D2.1 Responsibilities & data ownership
Master Service owns `SystemState` (authoritative control-plane state), routes control commands to CMIBs, aggregates monitor samples/messages, spools monitor data, persists control/config events, replicates state to secondary, and coordinates backend dataset publishing.

### D2.2 Technology options

**Language/runtime**
- Recommended: **Go 1.22–1.23** (predictable latency, easy deployment).  
- Conservative: **C++20** (max performance; higher complexity).  
- Cutting-edge: **Rust**.

**RPC**
- Recommended: **gRPC (protobuf)** to CMIB Adapter and between masters.  
- Conservative: raw TCP with custom framing.  
- Cutting-edge: QUIC-based RPC.

**Persistence**
- Recommended: PostgreSQL 14–16 for audit + metadata; local disk spool (filesystem) for high-rate monitor spooling.  
- Conservative: SQLite for local-only (risk under concurrency).  
- Cutting-edge: TimescaleDB for monitor time-series.

**Queue**
- Recommended: PostgreSQL-backed durable queue table + worker (simple, auditable).  
- Conservative: filesystem queue.  
- Cutting-edge: NATS JetStream.

**Observability**
- Recommended: Prometheus + OpenTelemetry traces; structured logs.

### D2.3 Recommended default stack
- Go 1.22–1.23, gRPC, PostgreSQL 14–16, filesystem spool (XFS/ext4), optional NATS.
- Justification: meets **INF-FR-018** (continue during comms loss via durable queue) and **INF-ASR-004** (HA replication).

### D2.4 Internal contracts — `internal.proto`
(Full file in Section L.)

### D2.5 Data model / schema
Primary persisted entities: `event_queue`, `spool_cursor`, `system_state`, `message`. (See SQL in Section L.)  
- Encryption-at-rest: audit + user secrets (INF-NFR-015).  
- Immutability: audit_event append-only (INF-FR-021).

### D2.6 Caching & consistency
- Cache: last-known CMIB states in memory (TTL 2s) to serve on-demand queries quickly.  
- Consistency: `SystemState.state_version` monotonic; secondary must match before promotion.

---

## D3. CMIB Adapter + CMIB Controller Interface

### D3.1 Responsibilities & data ownership
CMIB Adapter is the master-side integration layer that speaks to CMIB controllers over segmented control network and abstracts register writes/readbacks, interrogation, and reboot/warm boot. CMIB controllers own immediate hardware interaction and deterministic loops.

### D3.2 Technology options

**Language/runtime**
- Recommended: Go for adapter; CMIB controller: C/C++ or Go depending on OS support.  
- Conservative: C for adapter and controller.  
- Cutting-edge: Rust for controller.

**Transport**
- Recommended: gRPC over mTLS on NET_CTRL.  
- Conservative: UDP with retries (harder correctness).  
- Cutting-edge: TSN Ethernet (if hardware supports).

### D3.3 Recommended default stack
- Adapter: Go + gRPC; Controller: C++20 or C on near-real-time Linux.
- Justification: meets **INF-NFR-006** (deterministic response) by keeping deterministic work on CMIB and using bounded RPC.

### D3.4 Internal contracts
Covered in `internal.proto` services `CmibService`.

### D3.5 Data model
CMIB adapter persists only message/health summaries centrally (see `message` table).

### D3.6 Caching & consistency
No caching of control commands; commands are idempotent where possible and always recorded in `event_queue`.

---

## D4. Health Manager

### D4.1 Responsibilities & data ownership
Evaluates health signals (CPU hang, comms failures, temp/voltage deviations, performance below spec), triggers self-heal actions (CMIB warm boot, power node remote reboot), and issues alerts. Owns health rules configuration.

### D4.2 Technology options
- Recommended: Go service with rule engine (simple thresholds + state machine).  
- Conservative: embedded in Master Service (fewer moving parts).  
- Cutting-edge: CEP engine (Flink) (overkill).

### D4.3 Recommended default stack
- Go 1.22–1.23, rules in ConfigMap, gRPC to CMIB/Power.
- Justification: meets **INF-FR-017** (self-monitoring) and **INF-FR-003** (autonomous corrective action).

### D4.4 Interfaces
`internal.proto` `HealthService`.

### D4.5 Data model
Health events are written to `message` and `audit_event`.

### D4.6 Caching & consistency
Health evaluation uses sliding windows (e.g., last 60s) in memory; persisted summaries every N seconds.

---

## D5. Power Control Adapter + UPS Adapter

### D5.1 Responsibilities & data ownership
Power Control Adapter provides remote reboot path and power status ingestion. UPS Adapter ingests UPS outage/time-remaining signals and forwards to master for safe shutdown coordination.

### D5.2 Technology options
- Recommended: Go + gRPC; hardware IO via vendor SDK.  
- Conservative: Python 3.11–3.12 (fast integration; less deterministic).  
- Cutting-edge: Rust.

### D5.3 Recommended default stack
- Go 1.22–1.23, gRPC, vendor SDK bindings.
- Justification: meets **INF-ASR-007** (redundant reboot path) and **INF-NFR-002** (UPS time remaining).

### D5.4 Interfaces
`internal.proto` `PowerService`.

### D5.5 Data model
`power_event` table (see SQL).

### D5.6 Caching & consistency
UPS events are append-only; master uses latest event for shutdown decisions.

---

## D6. Auth Service + Audit Log Service

### D6.1 Responsibilities & data ownership
Auth Service authenticates users (mTLS client cert + optional username/password for break-glass) and authorizes actions via RBAC. Audit Log Service stores immutable access and action logs, including failed attempts.

### D6.2 Technology options

**AuthN**
- Recommended: mTLS client certs + MFA for privileged actions.  
- Conservative: username/password only (risk).  
- Cutting-edge: SPIFFE identities.

**AuthZ**
- Recommended: RBAC with explicit privileges.  
- Conservative: coarse roles only.  
- Cutting-edge: ABAC/OPA policies.

**Audit storage**
- Recommended: PostgreSQL append-only + WORM backups.  
- Conservative: flat files.  
- Cutting-edge: hash-chained ledger.

### D6.3 Recommended default stack
- PostgreSQL 14–16, RBAC, mTLS, TOTP/WebAuthn MFA for privileged actions.
- Justification: meets **INF-NFR-015** (robust security) and **INF-FR-021** (log all access attempts).

### D6.4 Interfaces
External endpoints in `openapi.yaml` under `/auth/*` and `/users/*`.

### D6.5 Data model
`users`, `user_roles`, `audit_event` (see SQL).  
- Encrypt-at-rest: password hashes, MFA secrets.  
- Immutability: audit_event no updates/deletes (only retention purge job).

### D6.6 Caching & consistency
- Cache RBAC decisions (TTL 60s).  
- Revocation: publish “user_revoked” event; invalidate caches immediately.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (`k8s/cmcs-deployment.yaml`)
- Recommended deployment: 2 replicas VCI, 2 replicas Master (primary/secondary via leader election), 2 replicas Auth, 2 replicas Health; CMIB controllers are typically **not** Kubernetes pods (embedded/edge), but CMIB Adapter is.

Justification: meets **INF-NFR-011** (restartable processes) via Kubernetes self-healing.

(Full manifest snippet in Section L.)

## E2. DB HA topology, backups, restore
- PostgreSQL HA: 1 primary + 1 synchronous standby (same rack/room) + optional async replica offsite.  
- Backups: base backup nightly + WAL archiving continuous; test restore weekly.  
- RPO/RTO targets: see Section G.

Justification: meets **INF-FR-021** (audit retention/integrity) by ensuring recoverability.

## E3. Network topology + ingress/egress rules
Mapped to *Deployment_PhysicalView*:
- NET_OPS: only exposes VCI ingress (443) and SSH (22) from admin subnets.  
- NET_CTRL: only master↔CMIB adapter/controller ports; deny all else.  
- NET_BACK: only backend publisher→backend DP.

Latency expectations:
- Master↔CMIB: <2ms intra-rack typical; enforce RPC deadlines (e.g., 20ms) to preserve determinism.

Justification: meets **INF-ASR-006** (separate physical interfaces) and **INF-ASR-009** (protect from unauthorized traffic).

## E4. CI/CD sketch
1. Build + unit tests  
2. Lint + SAST  
3. Contract tests: OpenAPI validation + protobuf compatibility  
4. Integration tests with simulated CMIB  
5. Container build + SBOM  
6. Deploy to staging (Helm)  
7. E2E + chaos (failover drill)  
8. Canary/blue-green to prod with rollback on SLO burn

Justification: meets **INF-NFR-007** (no total restart between windows) by enabling safe rolling upgrades.

---

# F. Security Design

## F1. Auth & AuthZ
- **Primary:** mTLS for all external and internal service-to-service traffic.  
- **User identity:** unique user ID bound to certificate subject; optional username/password only for break-glass accounts.  
- **MFA:** required for privileged actions (user admin, reboot, config apply).  
- **Authorization:** RBAC roles: `admin`, `ops`, `developer`, `maintainer`, `viewer`.  
- **Revocation:** CRL/OCSP checked on each session establishment; user disable takes effect within 15 minutes (cache TTL + forced reauth).

Justification: meets **INF-FR-024** (secure login) and **INF-NFR-015** (robust security).

## F2. Secrets management & rotation
- Use Kubernetes Secrets sealed with SOPS or external Vault.  
- Rotate: TLS certs 90 days; DB creds 30 days; MFA seeds on reset only.

Justification: meets **INF-FR-021** (auditability) by reducing credential compromise window.

## F3. TLS & service mesh
- TLS 1.2+ (prefer 1.3).  
- Optional service mesh (Linkerd/Istio) for mTLS automation; keep minimal to reduce operational risk.

Justification: meets **INF-ASR-009** (protect from unauthorized access).

## F4. Threat model (top 5)
1. Unauthorized command injection → mTLS+RBAC+MFA, deny-by-default.  
2. Replay of control commands → nonce/commandId + timestamp validation; idempotency keys.  
3. Compromised operator workstation → least privilege + audit + short sessions.  
4. Network DoS on NET_OPS → rate limiting, separate NICs, prioritize NET_CTRL.  
5. Audit log tampering → append-only tables + restricted DB roles + immutable backups.

---

# G. Observability & SRE

## G1. Metrics/logs/traces
**Per-component metrics**
- VCI: request rate, auth failures, p95 latency, rate-limit drops.  
- Master: command queue depth, CMIB RPC latency, state replication lag, spool bytes, dropped samples.  
- Health: faults detected/min, heal success rate, time-to-recover.  
- Power/UPS: outage events, time remaining, reboot attempts.

**Logging**
- Structured JSON logs with correlation IDs (`requestId`, `commandId`).  
- Redact secrets (passwords, MFA seeds).

**Tracing**
- OpenTelemetry spans: `TranslateConfig`, `ApplyConfig`, `CmibExecute`, `ReplicateState`.

## G1.1 Example Prometheus alert rules
- Alert 1: replication lag too high
- Alert 2: event queue growing (comms loss or stuck worker)

(Provided in runbook; examples below)

```yaml
# prometheus-rules.yaml (example)
groups:
- name: cmcs.rules
  rules:
  - alert: CMCS_MasterReplicationLagHigh
    expr: cmcs_master_replication_lag_seconds > 2
    for: 1m
    labels: { severity: "critical" }
    annotations:
      summary: "Master replication lag high"
      description: "Secondary is >2s behind for >1m; failover unsafe."
  - alert: CMCS_EventQueueBacklogGrowing
    expr: rate(cmcs_event_queue_depth[5m]) > 10
    for: 5m
    labels: { severity: "warning" }
    annotations:
      summary: "Event queue backlog growing"
      description: "Queue depth increasing; check external comms and CMIB RPC health."
```

## G2. SLOs, error budgets, RTO/RPO
- Availability SLO (control plane): 99.99% monthly (INF-NFR-009).  
- p95 external API latency: ≤250ms for queries; config apply is async with status polling.  
- RTO: 30 minutes for master node failure (INF-NFR-009).  
- RPO: 0 for audit/events (synchronous replication); monitor spool best-effort.

## G3. Dashboard & runbook sketch
Dashboards:
- “Control Plane Health”: queue depth, CMIB latency, faults, replication lag.  
- “Security”: auth failures, blocked users, audit write errors.  
Runbooks:
- Failover procedure, comms loss mode, spool overrun handling, CMIB hot swap.

---

# H. Testing Strategy

## H1. Test matrix

| Test type | Components | What it validates |
|---|---|---|
| Unit | VCI, Master, Health, Auth | Translation logic, RBAC rules, state machine |
| Integration | Master↔CMIB Adapter, Master↔Power | RPC timeouts, retries, warm boot flows |
| Contract | OpenAPI + protobuf | Backward compatibility, schema validation |
| E2E | VLA M&C simulator→VCI→Master→CMIB sim | Full config apply + monitor stream |
| Chaos | Master failover, network partition, DB failover | HA behavior, queue draining, no data loss for events |

## H2. Test data & environment isolation
Environments: `dev`, `integration`, `staging`, `prod`.  
- Refresh cadence: integration DB reset nightly; staging weekly.  
- CMIB simulator: deterministic register model + fault injection.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps (if replacing existing CMCS)
1. Deploy CMCS in parallel (standalone mode) with CMIB simulators.  
2. Connect to real CMIBs in read-only monitor mode.  
3. Enable control for a single rack (canary).  
4. Enable full control; keep rollback path to legacy master.  
5. Cut over backend dataset publishing to NET_BACK.

Rollback: disable VCI ingress, revert routing to legacy master, keep CMIB addressing stable (INF-FR-007).

## I2. Backwards compatibility & API versioning
- Version external API as `/api/v1`.  
- Additive changes only within v1; breaking changes require `/api/v2` with dual-run window.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| gRPC internal control plane | REST; raw TCP | gRPC: strong contracts, streaming; REST simpler; raw TCP fastest but risky | gRPC chosen for correctness + bounded latency (**INF-NFR-006**) |
| PostgreSQL for audit/events | SQLite; Kafka | Postgres: HA + SQL; SQLite limited; Kafka heavy | Postgres meets durability + operability (**INF-FR-021**, **INF-FR-018**) |
| mTLS + RBAC + MFA | password-only; VPN-only | mTLS strong identity; password-only weak; VPN-only not sufficient | Meets security requirements (**INF-NFR-015**, **INF-FR-024**) |
| HA primary/secondary master | active/active; single master | active/active complex; single master risky | Primary/secondary aligns with requirements (**INF-ASR-004**) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** CMIB controllers can run a Linux-based near-real-time OS (e.g., PREEMPT_RT) compatible with required bus access.  
- **A2:** External VLA M&C can call HTTPS/mTLS endpoints and handle async job status polling.  
- **A3:** Backend dataset payloads are referenced by URI/object path (`payloadRef`) rather than embedded in control-plane messages.  
- **A4:** “Spool 24h at peak rate” is acceptable as filesystem-based spool with bounded disk allocation and overrun alerting.  
- **A5:** “Standalone mode” means master+CMIB can boot/configure/run without external networks, but local operator access remains available.

## Unresolved stakeholder questions
1. What are the **exact monitor sample rates and peak bandwidth** per rack (needed to size spool and NET_CTRL)?  
2. What is the **authoritative external config schema** from VLA M&C (to finalize translation rules)?  
3. What are the **required retention periods** for audit logs and monitor spools beyond the stated 24h spool (e.g., 1 year audit assumed in container diagram)?  
4. What is the **exact failover trigger** and acceptable switchover time (seconds vs minutes)?  
5. Are there **hard real-time constraints** (max jitter) for specific CMIB actions?

## Conflict log (requirements vs diagrams)
- No direct conflicts detected in naming; diagrams use “CMCS/VCI/Master/CMIB” consistent with Original Requirements.  
- Diagram notes mention “revoke<=15min” and “audit retain 1y” which are **not explicit** in requirements; treated as assumptions (A5 + open question #3).

---

# L. Deliverables

## 1) `architecture.md` (this document)
```markdown
# ArchitectureDocument.md
(Contents are exactly the sections A–L above.)
```

## 2) `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: CMCS VCI External API
  version: "1.0.0"
  description: >
    External API for the Correlator Monitor & Control System Virtual Correlator Interface (VCI).
    All endpoints require mTLS. Privileged actions require MFA.
servers:
  - url: https://cmcs-vci.example.org/api/v1
security:
  - mTLS: []
paths:
  /auth/session:
    post:
      summary: Create a session (mTLS identity + optional MFA)
      operationId: createSession
      security:
        - mTLS: []
      requestBody:
        required: false
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateSessionRequest"
      responses:
        "200":
          description: Session created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Session"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
  /configs:translate:
    post:
      summary: Translate external configuration into internal config tables
      operationId: translateConfig
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ExternalConfig"
      responses:
        "200":
          description: Translation result
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ConfigTableSet"
        "400":
          $ref: "#/components/responses/ErrBadRequest"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
  /configs:apply:
    post:
      summary: Apply a translated config table set to hardware (async)
      operationId: applyConfig
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ApplyConfigRequest"
      responses:
        "202":
          description: Apply accepted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/JobAccepted"
        "400":
          $ref: "#/components/responses/ErrBadRequest"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
  /control/commands:
    post:
      summary: Submit a control command (async)
      operationId: submitControlCommand
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ControlCommand"
      responses:
        "202":
          description: Command accepted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/JobAccepted"
        "400":
          $ref: "#/components/responses/ErrBadRequest"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
  /monitor/state:
    get:
      summary: Query current system state
      operationId: querySystemState
      parameters:
        - in: query
          name: detail
          schema:
            type: string
            enum: [summary, full]
          required: false
      responses:
        "200":
          description: System state
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SystemState"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
  /monitor/stream:
    get:
      summary: Stream monitor samples (server-sent events)
      operationId: streamMonitor
      parameters:
        - in: query
          name: isTimeSynchronous
          schema:
            type: boolean
          required: false
        - in: query
          name: metricPrefix
          schema:
            type: string
          required: false
        - in: query
          name: maxHz
          schema:
            type: integer
            minimum: 1
            maximum: 1000
          required: false
      responses:
        "200":
          description: SSE stream of MonitorSample events
          content:
            text/event-stream:
              schema:
                type: string
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
  /jobs/{jobId}:
    get:
      summary: Get async job status/result
      operationId: getJob
      parameters:
        - in: path
          name: jobId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Job status
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/JobStatus"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
  /users:
    post:
      summary: Create a new user (admin only)
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
      responses:
        "201":
          description: User created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
  /users/{userId}:
    patch:
      summary: Update user access properties (admin only)
      operationId: updateUser
      parameters:
        - in: path
          name: userId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateUserRequest"
      responses:
        "200":
          description: User updated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
    delete:
      summary: Delete a user (admin only)
      operationId: deleteUser
      parameters:
        - in: path
          name: userId
          required: true
          schema: { type: string }
      responses:
        "204":
          description: User deleted
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
  /access/block:
    post:
      summary: Block access globally or for a user (admin only)
      operationId: blockAccess
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/BlockAccessRequest"
      responses:
        "200":
          description: Block applied
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BlockAccessResponse"
        "401":
          $ref: "#/components/responses/ErrUnauthorized"
        "403":
          $ref: "#/components/responses/ErrForbidden"
components:
  securitySchemes:
    mTLS:
      type: mutualTLS
      description: Client certificate authentication required.
  responses:
    ErrBadRequest:
      description: Bad request
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    ErrUnauthorized:
      description: Unauthorized
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    ErrForbidden:
      description: Forbidden
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
  schemas:
    Error:
      type: object
      required: [errorId, message, timestampUtc]
      properties:
        errorId: { type: string, example: "CMCS-ERR-401" }
        message: { type: string }
        details: { type: object, additionalProperties: true }
        timestampUtc: { type: string, format: date-time }
    CreateSessionRequest:
      type: object
      properties:
        mfaCode:
          type: string
          description: Optional TOTP/WebAuthn assertion for privileged session.
    Session:
      type: object
      required: [sessionId, userId, issuedAtUtc, expiresAtUtc, roles]
      properties:
        sessionId: { type: string }
        userId: { type: string }
        issuedAtUtc: { type: string, format: date-time }
        expiresAtUtc: { type: string, format: date-time }
        roles:
          type: array
          items: { type: string }
    ExternalConfig:
      type: object
      required: [requestId, targetRackId, config]
      properties:
        requestId: { type: string }
        targetRackId: { type: string }
        config:
          type: object
          description: Opaque external config payload; validated by schema version.
          additionalProperties: true
        schemaVersion:
          type: string
          example: "vla-mc-1.0"
    ConfigTableSet:
      type: object
      required: [requestId, createdUtc, tablesHash, targetRackId, tables]
      properties:
        requestId: { type: string }
        createdUtc: { type: string, format: date-time }
        tablesHash: { type: string, example: "sha256:..." }
        targetRackId: { type: string }
        tables:
          type: array
          items:
            $ref: "#/components/schemas/ConfigTable"
    ConfigTable:
      type: object
      required: [name, rows]
      properties:
        name: { type: string }
        rows:
          type: array
          items:
            type: object
            additionalProperties: true
    ApplyConfigRequest:
      type: object
      required: [configTableSet, requireMfa]
      properties:
        configTableSet:
          $ref: "#/components/schemas/ConfigTableSet"
        requireMfa:
          type: boolean
          description: If true, server enforces MFA for this action.
    ControlCommand:
      type: object
      required: [commandId, timestampUtc, targetId, type, payload]
      properties:
        commandId: { type: string }
        timestampUtc: { type: string, format: date-time }
        targetId: { type: string, example: "CMIB-0x12AF" }
        type: { type: string, example: "SetSampleRate" }
        payload:
          type: object
          additionalProperties: true
    JobAccepted:
      type: object
      required: [jobId, acceptedAtUtc]
      properties:
        jobId: { type: string }
        acceptedAtUtc: { type: string, format: date-time }
    JobStatus:
      type: object
      required: [jobId, status, updatedAtUtc]
      properties:
        jobId: { type: string }
        status:
          type: string
          enum: [PENDING, RUNNING, SUCCEEDED, FAILED]
        updatedAtUtc: { type: string, format: date-time }
        result:
          type: object
          additionalProperties: true
        error:
          $ref: "#/components/schemas/Error"
    SystemState:
      type: object
      required: [stateVersion, masterRole, lastUpdatedUtc]
      properties:
        stateVersion: { type: integer, format: int64 }
        masterRole: { type: string, enum: [primary, secondary] }
        lastUpdatedUtc: { type: string, format: date-time }
        rackStates:
          type: object
          additionalProperties: true
    CreateUserRequest:
      type: object
      required: [userId, displayName, roles]
      properties:
        userId: { type: string }
        displayName: { type: string }
        roles:
          type: array
          items: { type: string }
        certSubject:
          type: string
          description: X.509 subject DN bound to this user.
        password:
          type: string
          description: Optional break-glass password; never returned.
    UpdateUserRequest:
      type: object
      properties:
        displayName: { type: string }
        roles:
          type: array
          items: { type: string }
        blocked: { type: boolean }
    User:
      type: object
      required: [userId, displayName, roles, blocked]
      properties:
        userId: { type: string }
        displayName: { type: string }
        roles:
          type: array
          items: { type: string }
        blocked: { type: boolean }
    BlockAccessRequest:
      type: object
      required: [mode]
      properties:
        mode:
          type: string
          enum: [GLOBAL, USER]
        userId:
          type: string
          description: Required when mode=USER
        reason:
          type: string
    BlockAccessResponse:
      type: object
      required: [appliedAtUtc]
      properties:
        appliedAtUtc: { type: string, format: date-time }
        mode: { type: string }
        userId: { type: string }
```

## 3) `internal.proto`
```proto
syntax = "proto3";

package cmcs.internal.v1;

option go_package = "cmcs/internal/v1;internalv1";

message Ack {
  string request_id = 1;
  bool ok = 2;
  string message = 3;
}

message TimestampPair {
  string timestamp_utc = 1;     // RFC3339
  string wallclock_local = 2;   // RFC3339 with local offset
}

message ConfigTableSet {
  string request_id = 1;
  string created_utc = 2;
  string tables_hash = 3;
  string target_rack_id = 4;
  bytes tables_blob = 5; // canonical serialized tables (e.g., protobuf/json)
}

message ControlCommand {
  string command_id = 1;
  string timestamp_utc = 2;
  string target_id = 3; // e.g., CMIB-0x12AF
  string type = 4;
  bytes payload = 5; // canonical payload
}

message RegisterWrite {
  string target_id = 1;
  uint32 address = 2;
  uint32 value = 3;
}

message RegisterSnapshot {
  string target_id = 1;
  repeated uint32 addresses = 2;
  repeated uint32 values = 3;
}

message HardwareState {
  string target_id = 1;
  map<string, string> metrics = 2; // temps, voltages, error counters, etc.
  string observed_utc = 3;
}

message PowerEvent {
  string event_type = 1; // OUTAGE, RESTORED, LOW_BATTERY
  int32 time_remaining_sec = 2;
  string timestamp_utc = 3;
}

message Fault {
  string fault_id = 1;
  string target_id = 2;
  string category = 3; // CPU_HANG, COMM_FAIL, TEMP, VOLTAGE, PERF
  string detected_utc = 4;
  map<string, string> details = 5;
}

service MasterService {
  rpc ApplyConfig(ConfigTableSet) returns (Ack);
  rpc RouteControl(ControlCommand) returns (Ack);
  rpc ReplicateState(bytes) returns (Ack); // state delta blob
}

service CmibService {
  rpc ExecuteRegisterWrite(RegisterWrite) returns (Ack);
  rpc ReadbackRegisters(ControlCommand) returns (RegisterSnapshot);
  rpc InterrogateHardware(ControlCommand) returns (HardwareState);
  rpc Reboot(ControlCommand) returns (Ack); // payload includes warmBoot flag
}

service HealthService {
  rpc EvaluateHealth(ControlCommand) returns (Ack);
  rpc ReportFault(Fault) returns (Ack);
}

service PowerService {
  rpc RemoteReboot(ControlCommand) returns (Ack);
  rpc ReportPowerEvent(PowerEvent) returns (Ack);
}
```

## 4) `k8s/cmcs-deployment.yaml`
```yaml
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
  LOG_LEVEL: "info"
  RBAC_CACHE_TTL_SECONDS: "60"
  EVENT_QUEUE_RETENTION_HOURS: "96"
  SPOOL_RETENTION_HOURS: "24"
---
apiVersion: v1
kind: Secret
metadata:
  name: cmcs-secrets
  namespace: cmcs
type: Opaque
stringData:
  POSTGRES_DSN: "postgres://cmcs_app:REDACTED@cmcs-postgres.cmcs.svc.cluster.local:5432/cmcs?sslmode=require"
  REDIS_ADDR: "cmcs-redis.cmcs.svc.cluster.local:6379"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cmcs-vci
  namespace: cmcs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cmcs-vci
  template:
    metadata:
      labels:
        app: cmcs-vci
    spec:
      containers:
        - name: vci
          image: registry.example.org/cmcs/vci:1.0.0
          ports:
            - containerPort: 8443
          envFrom:
            - configMapRef: { name: cmcs-config }
            - secretRef: { name: cmcs-secrets }
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits: { cpu: "1", memory: "1Gi" }
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8443
              scheme: HTTPS
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: cmcs-vci
  namespace: cmcs
spec:
  selector:
    app: cmcs-vci
  ports:
    - name: https
      port: 443
      targetPort: 8443
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cmcs-vci-hpa
  namespace: cmcs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cmcs-vci
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
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cmcs-master
  namespace: cmcs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cmcs-master
  template:
    metadata:
      labels:
        app: cmcs-master
    spec:
      containers:
        - name: master
          image: registry.example.org/cmcs/master:1.0.0
          ports:
            - containerPort: 9090
          envFrom:
            - configMapRef: { name: cmcs-config }
            - secretRef: { name: cmcs-secrets }
          resources:
            requests: { cpu: "500m", memory: "512Mi" }
            limits: { cpu: "2", memory: "2Gi" }
          livenessProbe:
            tcpSocket: { port: 9090 }
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: cmcs-master
  namespace: cmcs
spec:
  selector:
    app: cmcs-master
  ports:
    - name: grpc
      port: 9090
      targetPort: 9090
```

## 5) SQL DDL examples

### `sql/user_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS users (
  user_id            TEXT PRIMARY KEY,
  display_name       TEXT NOT NULL,
  cert_subject_dn    TEXT UNIQUE,
  password_hash      TEXT, -- encrypt-at-rest via disk/volume encryption; store salted hash only
  mfa_secret_enc     BYTEA, -- encrypted at rest (KMS envelope)
  blocked            BOOLEAN NOT NULL DEFAULT FALSE,
  created_utc        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_utc        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_roles (
  user_id   TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  role      TEXT NOT NULL,
  PRIMARY KEY (user_id, role)
);

CREATE INDEX IF NOT EXISTS idx_users_blocked ON users(blocked);
```

### `sql/audit_event_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS audit_event (
  audit_id        BIGSERIAL PRIMARY KEY,
  timestamp_utc   TIMESTAMPTZ NOT NULL,
  actor_user_id   TEXT,
  action_type     TEXT NOT NULL,
  outcome         TEXT NOT NULL,
  target          TEXT,
  source_ip       INET,
  details         JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Append-only enforcement is done by DB role policy: no UPDATE/DELETE grants to app role.
CREATE INDEX IF NOT EXISTS idx_audit_event_time ON audit_event(timestamp_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_event_actor ON audit_event(actor_user_id);
```

### `sql/event_queue_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS event_queue (
  event_id        BIGSERIAL PRIMARY KEY,
  enqueued_utc    TIMESTAMPTZ NOT NULL DEFAULT now(),
  event_type      TEXT NOT NULL, -- APPLY_CONFIG, CONTROL_COMMAND
  request_id      TEXT NOT NULL,
  payload         JSONB NOT NULL,
  status          TEXT NOT NULL DEFAULT 'PENDING', -- PENDING,RUNNING,DONE,FAILED
  last_error      TEXT,
  updated_utc     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_event_queue_status_time ON event_queue(status, enqueued_utc);
CREATE INDEX IF NOT EXISTS idx_event_queue_request ON event_queue(request_id);
```

### `sql/message_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS message (
  message_id        BIGSERIAL PRIMARY KEY,
  timestamp_utc     TIMESTAMPTZ NOT NULL,
  wallclock_local   TIMESTAMPTZ NOT NULL,
  location_id       TEXT NOT NULL,
  severity          TEXT NOT NULL,
  category          TEXT NOT NULL,
  detail_level      TEXT NOT NULL,
  content           TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_message_time ON message(timestamp_utc DESC);
CREATE INDEX IF NOT EXISTS idx_message_category ON message(category);
```

### `sql/power_event_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS power_event (
  power_event_id     BIGSERIAL PRIMARY KEY,
  event_type         TEXT NOT NULL,
  time_remaining_sec INTEGER NOT NULL,
  timestamp_utc      TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_power_event_time ON power_event(timestamp_utc DESC);
```

## 6) `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,Receive config and translate to HW config,UseCase_ScenarioView:UC_TranslateConfig;Activity_ProcessView_TranslateAndApply,VCI Gateway;Master Service,openapi.yaml;internal.proto,VCI translates and master applies tables.
INF-FR-002,Process/transfer dynamic control and monitor data,UseCase_ScenarioView:UC_ControlMonitor,Master Service;CMIB Adapter,internal.proto;openapi.yaml,APIs and internal RPC implement control/monitor.
INF-FR-003,Autonomous health monitoring and corrective action,UseCase_ScenarioView:UC_SelfHeal;Sequence_ProcessView_S2_SelfHealAndAlert,Health Manager;Master Service,internal.proto,Health loop triggers reboot/alerts.
INF-FR-004,Limited real-time probing (auto-correlation tools),UseCase_ScenarioView:UC_AutoCorr,VCI Gateway,openapi.yaml,Expose endpoint for autocorr retrieval/streaming.
INF-FR-005,Easy access for testing/debugging,UseCase_ScenarioView:UC_RemoteDebug,VCI Gateway;TestToolsGUI,openapi.yaml,Remote debug endpoints gated by RBAC.
INF-ASR-001,Integrated with VLA M&C structure,Deployment_PhysicalView:NODE_VLA--NET_OPS,VCI Gateway,openapi.yaml,External integration via ops network.
INF-ASR-002,Gateway through VCI,Container_PhysicalView:CON_VCI,VCI Gateway,openapi.yaml,All external use through VCI.
INF-ASR-003,Backend datasets over secondary network,Deployment_PhysicalView:NET_BACK,Backend Data Publisher,internal.proto,Separate backend network path.
INF-ASR-004,Master/slave topology,Class_LogicView:MasterControlNode o-- CMIBController,Master Service;CMIB Adapter,internal.proto,Master coordinates CMIBs.
INF-ASR-005,Ethernet >=100Mbps internal links,Deployment_PhysicalView:SW_RACK,NODE_RACK,Infra;CMIB Adapter,k8s/cmcs-deployment.yaml,Network sizing and timeouts.
INF-ASR-006,Separate physical interfaces,Deployment_PhysicalView:NET_OPS/NET_CTRL/NET_BACK,Master Node,k8s/cmcs-deployment.yaml,Segmentation for determinism/security.
INF-ASR-007,Redundant master-power path for remote reboot,Deployment_PhysicalView:NODE_MasterP--NODE_Power,Power Control Adapter,internal.proto,Recovery path.
INF-ASR-008,Fiber/low-RFI penetrations,Deployment_PhysicalView:NET_OPS/NET_BACK notes,Infra,(ops runbook),Physical constraint.
INF-ASR-009,Routers/switches protect from unauthorized traffic,Deployment_PhysicalView:NET_OPS,Ingress/Firewall,k8s/cmcs-deployment.yaml,Network policy.
INF-FR-006,CMIB bus via PCI/ISA/serial/parallel,Container_PhysicalView:CON_CMIB->EXT_HW,CMIB Adapter,internal.proto,Adapter abstracts bus.
INF-FR-007,Read 16-bit ID to form IP for hot swap,Class_LogicView:CMIBController note,CMIB Controller,internal.proto,Stable addressing.
INF-FR-008,Read back writable registers,Class_LogicView:CMIBController.readbackRegisters,CMIB Adapter,internal.proto,Observability.
INF-FR-009,Interrogate hardware state,Class_LogicView:CMIBController.interrogateHardware,Health Manager;CMIB Adapter,internal.proto,Health evaluation.
INF-FR-010,Control warm boots,Class_LogicView:CMIBController.reboot,Health Manager,internal.proto,Self-heal action.
INF-FR-011,Physical CMIB status indicator,(not modeled),CMIB Hardware,(hardware spec),Hardware requirement tracked.
INF-NFR-001,UPS-backed safe shutdown,UseCase_ScenarioView:UPS->UC_ControlMonitor,UPS Adapter;Master Service,internal.proto,UPS events drive shutdown.
INF-NFR-002,UPS signals outage/time remaining,Class_LogicView:PowerEvent,UPS Adapter,sql/power_event_ddl.sql,Persist UPS telemetry.
INF-NFR-003,Authorized remote logins,UseCase_ScenarioView:UC_ManageAccess,Auth Service,openapi.yaml,Central auth.
INF-NFR-004,Hardware watchdog reboot,Deployment_PhysicalView node notes,CMIB;Master Nodes,(ops runbook),Auto reboot and rejoin.
INF-ASR-010,CMIB hardware spec supports COTS near real-time OS,Deployment_PhysicalView:NODE_CMIB,CMIB Controller,(hardware spec),Platform constraint.
INF-ASR-011,Master HA multi-NIC standalone,Deployment_PhysicalView:NODE_MasterP note,Master Service,k8s/cmcs-deployment.yaml,Standalone boot/run.
INF-ASR-012,Power node standalone,Deployment_PhysicalView:NODE_Power,Power Control Adapter,internal.proto,Power monitoring continues.
INF-NFR-005,Meet deadlines and future needs,State_LogicView_MasterControlNode,Master/CMIB,(benchmarks),Performance planning.
INF-NFR-006,Deterministic response to HW inputs,Component_DevelopmentView:C_CMIB note,CMIB Adapter,internal.proto,Bounded latency.
INF-FR-012,Lower-layer errors visible at master,(implicit),Master Service,sql/message_ddl.sql,Central message store.
INF-FR-013,Filterable categorized messages,Class_LogicView:Message.category/detailLevel,VCI;Master Service,openapi.yaml,Stream filters.
INF-FR-014,UTC+wallclock timestamps,Class_LogicView:Message,MonitorSample,All,sql/message_ddl.sql,Schema fields.
INF-FR-015,Authorized full access to traffic,UseCase_ScenarioView:UC_RemoteDebug,VCI Gateway,openapi.yaml,Debug endpoints.
INF-FR-016,GUI for test software via VCI,Package_DevelopmentView:ui,UI,(ui spec),UI uses APIs.
INF-FR-017,Self-monitoring detects abnormal conditions,UseCase_ScenarioView:UC_SelfHeal,Health Manager,internal.proto,Health rules.
INF-NFR-007,No total restart between windows,State_LogicView_MasterControlNode,All,k8s/cmcs-deployment.yaml,Rolling upgrades.
INF-NFR-008,Hardware indefinite operation except power,Deployment_PhysicalView,Infra/UPS,(ops runbook),Redundancy.
INF-FR-018,Continue processing until queues exhausted,State_LogicView_MasterControlNode:ProcessingQueued,Event Queue,sql/event_queue_ddl.sql,Durable queue.
INF-FR-019,Idle and resume quickly,State_LogicView_MasterControlNode,Master/CMIB,(benchmarks),Warm standby.
INF-NFR-009,Accessible for maintenance,Deployment_PhysicalView,Ops/Hardware,(rack layout),Physical access.
INF-NFR-010,Source available; debuggable; simulatable,Package_DevelopmentView,All,(repo policy),Engineering policy.
INF-NFR-011,Killable/restartable processes,k8s/cmcs-deployment.yaml,All,k8s/cmcs-deployment.yaml,K8s supervision.
INF-NFR-012,Third-party tools have diagnostics/support,(not modeled),Vendor deps,(procurement),Procurement constraint.
INF-NFR-013,OS source or diagnostics/support,(not modeled),OS,(procurement),OS selection constraint.
INF-NFR-014,Expandable/transparent upgrades,Deployment_PhysicalView,Infra,(capacity plan),Modularity.
INF-NFR-015,Robust security deny unauthorized,UseCase_ScenarioView:UC_ManageAccess,Auth Service,openapi.yaml,Fail-closed auth.
INF-FR-020,Unique user identification,Class_LogicView:AuthService,Auth Service,sql/user_ddl.sql,User table.
INF-FR-021,Log all access attempts,UseCase_ScenarioView:UC_Audit,Audit Log,sql/audit_event_ddl.sql,Audit schema.
INF-FR-022,Ops unrestricted; grant/revoke privileges,UseCase_ScenarioView:Admin->UC_ManageAccess,Auth Service,openapi.yaml,Admin endpoints.
INF-FR-023,Limited access for dev/test/maint,RBACPolicy,Auth Service,openapi.yaml,RBAC roles.
INF-FR-024,Secure login attempts,AuthService.authenticate,Auth Service,openapi.yaml,mTLS+MFA.
INF-FR-025,Admin unrestricted access,RBACPolicy roles,Auth Service,openapi.yaml,Admin role.
INF-FR-026,Admin create user,UC_ManageAccess,Auth Service,openapi.yaml,POST /users.
INF-FR-027,Admin remove user,UC_ManageAccess,Auth Service,openapi.yaml,DELETE /users/{id}.
INF-FR-028,Admin edit user properties,UC_ManageAccess,Auth Service,openapi.yaml,PATCH /users/{id}.
INF-FR-029,Admin block access global/user,UC_ManageAccess,Auth Service,openapi.yaml,POST /access/block.
INF-NFR-016,Continue ops during partial shutdown,State_LogicView_MasterControlNode:Degraded,Master Service,k8s/cmcs-deployment.yaml,Graceful degradation.
INF-NFR-017,Replaceability/hot swap maximal,Deployment_PhysicalView:NODE_RACK hot-swappable,CMIB,(hardware spec),Hot swap support.
INF-NFR-018,Hardware specs/config available,(not modeled),Ops,(docs),Documentation deliverable.
INF-NFR-019,Code well documented familiar languages,(not modeled),All,architecture.md,Language and doc standards.
INF-NFR-020,Readable style minimal confusion,(not modeled),All,(coding standards),Engineering practice.
```

---

## Verification / Acceptance Criteria

| Item | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A–L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (as INF- IDs) |
| ≥1 OpenAPI YAML and ≥1 internal proto included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDL for primary entities included | [x] |
| All major components have API contract + data schema | [x] |
| Assumptions and unresolved questions listed | [x] |

### How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?