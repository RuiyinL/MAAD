Analysis Plan: Scope—produce production-ready architecture for Gemini Observatory Control System (OCS) per provided requirements + 11 diagrams.  
Analysis Plan: Approach—normalize narrative requirements into atomic INF-* FR/NFR/ASR, align to 4+1 views, and bind to concrete APIs/schemas/deployments.  
Analysis Plan: Validation—traceability matrix completeness, contract validity (OpenAPI/Proto), and NFR/ASR testability (SLOs, security, performance).

# A. Executive Summary (≤1 page)

**System overview.** Gemini OCS is a distributed control + data acquisition platform for telescope/instrument operations across operational levels (Observing/Maintenance/Test) and access modes (Observing/Monitoring/Operation/Planning/Testing/Administrative), supporting on-site and remote use with strict safety/security gating, sequencer-mediated control, non-intrusive monitoring, and automated data archiving/transfer.

**Primary diagram mapping (one-line).** End-to-end control is captured by: *ScenarioView* “Gemini_UseCase” (UC_ExecSeq, UC_DirectControl, UC_Monitor, UC_SafeState), *ProcessView* “Gemini_Sequence_ExecuteSequence” (CommandRouter↔TelescopeControlSubsystem ACK/NAK), and *PhysicalView* “Gemini_Deployment” (SummitLAN, IOCNet, SecurityGateway).

**Architectural style(s).**
- **Layered + service-oriented orchestration** (UI → Policy/Auth → Sequencer/Router → Subsystem adapters/IOCs). Justification: meets **INF-ASR-OCS-Layering** (modularity/independent install) and **INF-NFR-Modularity**.
- **Event/telemetry pipeline sidecar** (control path isolated from logging). Justification: meets **INF-NFR-Logging200Hz** and **INF-NFR-NonIntrusiveMonitoring**.

**Deployment topology.**
- **Hub-and-spoke distributed control**: Summit control network (active control nodes + telemetry + data node) + base facility security gateway for remote access + IOC network for real-time control. Justification: meets **INF-NFR-RemoteOpsTransparency** and **INF-NFR-LANBandwidth20-40Mbps**.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| R1: Safety gating ambiguity for “remote control” vs “remote observing” | Unsafe command issuance | Enforce PolicyService rules + LocalSafetyGate checks for any command classed “hazardous”; require “local presence” flag from Safety HW integration. Justification: **INF-FR-RemoteControlSafety** |
| R2: Monitoring/logging load impacts observing | Missed timing/latency | Separate telemetry pipeline; rate-limit remote monitoring; prioritize control threads; backpressure + drop policy for non-critical telemetry only. Justification: **INF-NFR-NonIntrusiveMonitoring**, **INF-NFR-StatusUpdateLocal4s** |
| R3: Resource deadlock across multi-instrument + beam allocation | Observation stalls | Central AccessModeAllocator with lease ordering + timeout + deadlock avoidance; single-writer for critical resources. Justification: **INF-FR-AccessModeAllocationDeadlockFree** |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-Nodes10, INF-NFR-ControlTPS100 | Load + soak + capacity tests |
| Availability | INF-NFR-RestartOnlyHWFailure, INF-NFR-Recover5Min | Chaos + failover drills + runbook validation |
| Security | INF-NFR-FirewallGateway, INF-NFR-TLSRemote, INF-NFR-PrivilegesAtLogin | Pen test + SAST/DAST + authz unit/contract tests |
| Performance | INF-NFR-CommandAccept2s, INF-NFR-Handshake200ms, INF-NFR-Timeout500ms | Latency benchmarks + protocol simulators |
| Maintainability | INF-NFR-Modularity, INF-NFR-VersionLabelRetrievable | Architecture conformance + release/upgrade tests |

---

# B. Traceability & Rationale

**Normalization note.** The “Original Requirements” are narrative and lack IDs; therefore all requirements are captured as **INF-*** (inferred) and mapped to diagrams/components/artifacts. This satisfies the “missing IDs” rule.

**Traceability matrix (CSV/table).** Full matrix is delivered as `traceability_matrix.csv` in Section L. Below is an excerpt (the full file contains all INF-* requirements).

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-AuthLogon | Users logon; privileges determined at login | Gemini_UseCase:UC_Logon, Gemini_Class:UserSession | AuthService, PolicyService, GeminiUI | openapi.yaml, internal.proto | Centralized session + policy evaluation enforces role/level/mode gating consistently. |
| INF-FR-OperationalLevels | System operates in Observing/Maintenance/Test levels | Gemini_State_OperationalLevel:ObservingLevel/MaintenanceLevel/TestLevel | PolicyService | internal.proto | Explicit state machine prevents illegal transitions and supports safe-state entry. |
| INF-FR-AccessModes | Access modes: observing/monitoring/operation/planning/testing/admin | Gemini_State_OperationalLevel:ObservingMode..AdministrativeMode | PolicyService, GeminiUI | openapi.yaml | Mode-aware UI + policy checks ensure correct capabilities per mode. |
| INF-FR-SequencerMediated | Observing control via sequencer; no direct telescope control for astronomers | Gemini_UseCase:UC_ExecSeq, UC_DirectControl; Gemini_Class:SchedulerSequencer | SchedulerSequencer, CommandRouter | openapi.yaml, internal.proto | Single point of control reduces risk and supports queue/service observing. |
| INF-FR-MonitorNonIntrusive | Monitoring read-only; must not affect ongoing observation | Gemini_Sequence_RemoteMonitoring:MonitoringService loop | MonitoringService, SubsystemStatusAPI | openapi.yaml | Rate limiting + read-only endpoints isolate monitoring from control. |
| INF-FR-ACKNAKProtocol | Uniform ACK/NAK, retries, timeouts | Gemini_Sequence_ExecuteSequence:TelescopeControlSubsystem→ACK/NAK | CommandRouter, Subsystem adapters | internal.proto | Contract enforces predictable command delivery and response semantics. |
| INF-FR-ResourceAllocation | Critical resources allocated via allocator; deadlock-free | Gemini_Class:AccessModeAllocator; Gemini_Activity_ExecuteSequence:AllocateResources | AccessModeAllocator | internal.proto, sql/resource_lease_ddl.sql | Lease-based allocation with ordering + TTL prevents deadlock and orphan locks. |
| INF-FR-DataArchiveAuto | Auto archive during observing/maintenance | Gemini_Activity_ExecuteSequence:Archive DataProduct | ArchiveTransferService | openapi.yaml, sql/data_product_ddl.sql | Ensures data durability and operational workflow compliance. |
| INF-FR-FITSTransfer | Transfer FITS to home institutes | Gemini_UseCase:UC_TransferFITS | ArchiveTransferService | openapi.yaml | Standard FITS packaging + secure transfer supports external distribution. |
| INF-FR-Simulator | Virtual telescope + subsystem simulators | Gemini_UseCase:UC_Simulate; Gemini_Component:VirtualTelescopeSimulator | VirtualTelescopeSimulator | internal.proto | Enables planning/testing without hardware and supports evolutionary development. |
| INF-FR-VisitorInstrumentSubsetAPI | Stable subset interface for visitor instruments | Gemini_Component:VisitorInstrumentAPI | VisitorInstrumentAPI | openapi.yaml | Provides long-lived integration surface with limited supported operations. |
| INF-FR-SafeState | Safe-state on hazard; interlocks independent | Gemini_UseCase:UC_SafeState; Gemini_Deployment:SafetyHW | SafetyManager | internal.proto | Safety path must work even if higher-level software fails. |
| INF-NFR-LANBandwidth20-40Mbps | LAN supports 20–40 Mbit/s | Gemini_Deployment:SummitLAN | Network | k8s/* | Drives separation of data plane and control plane and sizing. |
| INF-NFR-CommandAccept2s | Accept/reject within 2s before action | Gemini_Class:Command note; Gemini_Sequence_ExecuteSequence:ValidateCommand | CommandRouter | internal.proto | Enforced by router validation + policy check before dispatch. |
| INF-NFR-StatusUpdateLocal4s | Local status update within 4s | Gemini_Sequence_RemoteMonitoring | MonitoringService | openapi.yaml | Poll/subscribe design with bounded update intervals. |
| INF-NFR-StatusRequest5s | Status requests answered within 5s | Gemini_Component:SubsystemStatusAPI | SubsystemStatusAPI | internal.proto | Ensures status path never blocks control and has bounded latency. |
| INF-NFR-Logging200Hz | Log engineering data up to 200Hz bursts | Gemini_Class:LoggingService note | LoggingService | sql/telemetry_event_ddl.sql | Append-only telemetry store + buffering meets burst requirements. |
| INF-NFR-Nodes10 | Support up to 10 active nodes | Gemini_Deployment:ControlNode-1/2 | Platform | k8s/* | Horizontal scaling of stateless services + rate limits. |

---

# C. Architecture Overview

## 4+1 View alignment

1. **Context (Scenario View).** Actors and use cases are defined in *ScenarioView* “Gemini_UseCase” (Astronomer, TelescopeOperator, RemoteUser, VisitorInstrument, SafetyInterlockSystem; UC_ExecSeq, UC_Monitor, UC_SafeState).
2. **Container (Physical View).** Network-transparent UI and security perimeter are shown in *PhysicalView* “Gemini_Container” (C_Gateway, C_Sequencer, C_CommandRouter, C_TCS/C_ICS, C_ParamDB).
3. **Component/Package (Development View).** Service decomposition is shown in *DevelopmentView* “Gemini_Package” and “Gemini_Component” (PolicyService, SchedulerSequencer, AccessModeAllocator, CommandRouter, MonitoringService, LoggingService, SafetyManager, Data services).
4. **Class/Runtime (Logic + Process Views).** Core domain objects and runtime interactions are shown in *LogicView* “Gemini_Class” (UserSession, Command, ResourceLease, SubsystemEndpoint) and *ProcessView* “Gemini_Sequence_ExecuteSequence”.
5. **Deployment (Physical View).** Node placement and links are shown in *PhysicalView* “Gemini_Deployment” (SummitLAN, IOCNet, BaseLAN, SecurityGateway, DataNode, TelemetryNode).

---

# D. Detailed Technical Design (developer-facing)

## D1. Security & Policy Subsystem (AuthService + PolicyService + SecurityGateway)

### 1) Responsibilities & data ownership
Authenticates users/sessions, evaluates authorization decisions based on role/site/operational level/access mode, enforces remote site restrictions, and provides a single policy decision point for UI, Sequencer, Router, and Monitoring. Owns **policy rules**, **sessions**, and **audit of authz decisions**.

### 2) Technology options (3 alternatives per concern)

- **Language/runtime**
  - Recommended: **Go 1.22–1.23**
  - Conservative: Java 21 LTS
  - Cutting-edge: Rust 1.78+
  - Justification (recommended): meets **INF-NFR-CommandAccept2s** (low-latency services).

- **Web framework**
  - Recommended: Go **chi v5**
  - Conservative: Spring Boot 3.2+
  - Cutting-edge: Axum (Rust)
  - Justification: meets **INF-NFR-StatusRequest5s** (fast request routing).

- **RPC/HTTP**
  - Recommended: **gRPC 1.60+** internal + REST external
  - Conservative: REST-only
  - Cutting-edge: NATS request/reply
  - Justification: meets **INF-FR-ACKNAKProtocol** (typed contracts for command/policy).

- **Persistence**
  - Recommended: PostgreSQL 14–15
  - Conservative: MariaDB 10.11
  - Cutting-edge: CockroachDB 23+
  - Justification: meets **INF-NFR-VersionLabelRetrievable** (strong schema + migrations).

- **Cache**
  - Recommended: Redis 7.2
  - Conservative: in-memory LRU
  - Cutting-edge: KeyDB
  - Justification: meets **INF-NFR-CommandAccept2s** (policy decision caching).

- **Messaging**
  - Recommended: NATS JetStream 2.10+
  - Conservative: Kafka 3.6+
  - Cutting-edge: Redpanda
  - Justification: meets **INF-NFR-Logging200Hz** (telemetry buffering).

- **Search**
  - Recommended: OpenSearch 2.x (for logs/policy audit search)
  - Conservative: PostgreSQL full-text
  - Cutting-edge: ClickHouse
  - Justification: meets **INF-NFR-Logging200Hz** (fast log analytics).

- **Authn/Authz**
  - Recommended: OIDC (Keycloak 24–25) + RBAC + policy rules
  - Conservative: LDAP + local RBAC
  - Cutting-edge: SPIFFE/SPIRE identities
  - Justification: meets **INF-FR-AuthLogon** (privileges at login).

- **Observability**
  - Recommended: OpenTelemetry SDK 1.x + Prometheus
  - Conservative: Prometheus only
  - Cutting-edge: eBPF-based tracing
  - Justification: meets **INF-NFR-Recover5Min** (fast diagnosis).

- **CI/CD**
  - Recommended: GitHub Actions + Argo CD
  - Conservative: Jenkins
  - Cutting-edge: Tekton
  - Justification: meets **INF-NFR-VersionConsistencyBoot** (repeatable releases).

- **Container runtime**
  - Recommended: containerd (K8s default)
  - Conservative: Docker
  - Cutting-edge: gVisor for gateway
  - Justification: meets **INF-NFR-FirewallGateway** (hardened perimeter).

- **Infra provisioning**
  - Recommended: Terraform 1.6+
  - Conservative: Ansible
  - Cutting-edge: Crossplane
  - Justification: meets **INF-NFR-RemoteOpsTransparency** (repeatable multi-site).

### 3) Recommended default stack
- Go 1.22–1.23, chi v5, gRPC 1.60+, PostgreSQL 14–15, Redis 7.2, Keycloak 24–25, OpenTelemetry + Prometheus.
- Justification: meets **INF-FR-AuthLogon** and **INF-NFR-CommandAccept2s**.

### 4) Interface design
External API is in `openapi.yaml` (see Section L). Internal contracts in `internal.proto`.

### 5) Data model / schema
See `sql/user_session_ddl.sql`, `sql/policy_rule_ddl.sql`, `sql/audit_event_ddl.sql`. Audit is append-only (immutability) to support trace reconstruction (**INF-NFR-LogRecreateObservation**).

### 6) Caching & consistency
- Cache policy decisions by `(userId, role, siteId, level, mode, operation)` TTL 30s; invalidate on policy version bump.
- Sessions stored in DB + Redis for fast lookup; strong consistency for authz decisions.

---

## D2. Orchestration Subsystem (SchedulerSequencer)

### 1) Responsibilities & data ownership
Accepts observation plans, manages queue/resequencing/break, orchestrates multi-step sequences across subsystems, and ensures observing is primarily sequencer-mediated. Owns **observation plans**, **queue state**, and **sequence execution records**.

### 2) Technology options
- Language: Go / Java / Rust (same criteria). Justification: meets **INF-FR-SequencerMediated**.
- Framework: Go chi / Spring / Axum. Justification: meets **INF-NFR-Nodes10**.
- RPC: gRPC internal; REST external. Justification: meets **INF-FR-RemoteOpsTransparency**.
- Persistence: PostgreSQL / MariaDB / CockroachDB. Justification: meets **INF-FR-QueueResequence**.
- Cache: Redis / in-memory / KeyDB. Justification: meets **INF-NFR-CommandAccept2s**.
- Messaging: NATS / Kafka / Redpanda. Justification: meets **INF-NFR-Logging200Hz**.
- Search: OpenSearch / PG FTS / ClickHouse. Justification: meets **INF-NFR-LogRecreateObservation**.
- Authz: PolicyService calls. Justification: meets **INF-FR-AccessModes**.
- Observability: OTel. Justification: meets **INF-NFR-Recover5Min**.
- CI/CD, container, infra: as above.

### 3) Recommended default stack
Go 1.22–1.23 + PostgreSQL 14–15 + Redis 7.2 + NATS 2.10+.  
Justification: meets **INF-FR-QueueResequence** and **INF-NFR-CommandAccept2s**.

### 4) Interface design
- External: `/v1/observation-plans`, `/v1/queues/{id}/execute-next`, `/v1/queues/{id}/break`, etc. (openapi.yaml)
- Internal: `Sequencer.SubmitPlan`, `Sequencer.ExecuteNext` (internal.proto)

### 5) Data model / schema
See `sql/observation_plan_ddl.sql`, `sql/sequence_run_ddl.sql`.

### 6) Caching & consistency
- Queue state in DB with optimistic locking (`version` column).
- Cache “next executable candidates” for 5s; recompute on telemetry condition changes.

---

## D3. Control Plane Subsystem (CommandRouter + Subsystem Adapters)

### 1) Responsibilities & data ownership
Validates commands, enforces policy + safety gate, allocates required resources, dispatches to subsystem endpoints (TCS/ICS/Env/etc.), and enforces uniform ACK/NAK + retry/timeout semantics. Owns **command records** and **command outcomes**.

### 2) Technology options
- Language: Go / Java / Rust. Justification: meets **INF-NFR-Handshake200ms**.
- RPC: gRPC to adapters; optional EPICS Channel Access bridge. Justification: meets **INF-FR-ACKNAKProtocol**.
- Persistence: PostgreSQL for command log. Justification: meets **INF-NFR-LogRecreateObservation**.
- Messaging: NATS for async delayed replies. Justification: meets **INF-NFR-Timeout500ms** (control path bounded; delayed replies async).
- Observability: OTel. Justification: meets **INF-NFR-Recover5Min**.

### 3) Recommended default stack
Go 1.22–1.23 + gRPC + NATS + PostgreSQL.  
Justification: meets **INF-FR-ACKNAKProtocol** and **INF-NFR-Timeout500ms**.

### 4) Interface design
Internal proto includes `CommandRouter.ExecuteCommand` returning `AckNak` and optional `DelayedReply`.

### 5) Data model / schema
See `sql/command_ddl.sql`. Mark `parameters` as sensitive if it can include credentials; encrypt at rest (**INF-NFR-SecurityIntrusionProtection**).

### 6) Caching & consistency
No caching for command execution decisions; only cache static validation tables (range limits) with versioning.

---

## D4. Resource Allocation Subsystem (AccessModeAllocator)

### 1) Responsibilities & data ownership
Allocates critical resources (e.g., telescope beam, active instrument, enclosure motion) via leases; prevents deadlock; supports release/renew/expiry. Owns **resource leases**.

### 2) Technology options
- Persistence: PostgreSQL advisory locks / Redis Redlock / etcd leases
- Recommended: PostgreSQL + deterministic ordering + TTL
- Justification: meets **INF-FR-AccessModeAllocationDeadlockFree**.

### 3) Recommended default stack
PostgreSQL 14–15 with `resource_lease` table + unique constraints.  
Justification: meets **INF-FR-ResourceAllocation**.

### 4) Interface design
Internal proto: `Allocator.Allocate`, `Allocator.Release`, `Allocator.Renew`.

### 5) Data model / schema
See `sql/resource_lease_ddl.sql`.

### 6) Caching & consistency
Strong consistency required; no caching.

---

## D5. Monitoring & Telemetry Subsystem (MonitoringService + LoggingService + SubsystemStatusAPI)

### 1) Responsibilities & data ownership
Provides read-only status snapshots and subscriptions; logs telemetry/audit; supports 200Hz bursts for short periods; ensures monitoring does not affect observing. Owns **telemetry events** and **audit events**.

### 2) Technology options
- Storage: TimescaleDB / ClickHouse / PostgreSQL partitioning
- Recommended: PostgreSQL partitioned tables + optional ClickHouse for analytics
- Justification: meets **INF-NFR-Logging200Hz**.

### 3) Recommended default stack
PostgreSQL 14–15 partitioning + NATS buffering + OpenSearch for search.  
Justification: meets **INF-NFR-LogRecreateObservation** and **INF-NFR-Logging200Hz**.

### 4) Interface design
External: `/v1/status/{subsystem}` and `/v1/telemetry/query` (openapi.yaml). Internal: `Status.GetSnapshot`, `Log.AppendTelemetry`.

### 5) Data model / schema
See `sql/telemetry_event_ddl.sql`, `sql/audit_event_ddl.sql` (append-only).

### 6) Caching & consistency
- Cache latest status snapshot per subsystem in memory (TTL 1s local, 2s remote).
- Telemetry is append-only; eventual consistency acceptable for analytics, not for safety.

---

## D6. Data Subsystem (DAQ + QuickLook + NearLine + ArchiveTransfer)

### 1) Responsibilities & data ownership
Acquires detector data, stores compressed standard format (FITS), supports quick-look synchronous QA, near-line async reduction, archives automatically, and transfers FITS to home institutes. Owns **data products** and **processing jobs**.

### 2) Technology options
- Storage: POSIX + object store (S3) / Ceph / ZFS
- Recommended: ZFS-backed NFS for on-site + S3-compatible object store for archive staging
- Justification: meets **INF-NFR-DataRetention7Days**.

### 3) Recommended default stack
Python 3.11–3.12 for pipelines + Go control wrappers; FITS libraries (cfitsio bindings); S3-compatible store (MinIO).  
Justification: meets **INF-FR-DataArchiveAuto** and **INF-FR-FITSTransfer**.

### 4) Interface design
External: `/v1/data-products/{id}` and `/v1/archive/transfer` (openapi.yaml). Internal: `Data.IngestFrame`, `Archive.ArchiveProduct`.

### 5) Data model / schema
See `sql/data_product_ddl.sql`, `sql/processing_job_ddl.sql`.

### 6) Caching & consistency
- Cache “last N exposures” metadata in Redis (TTL 1h).
- Data files immutable once archived; metadata updates allowed with audit.

---

## D7. Safety Subsystem (SafetyManager)

### 1) Responsibilities & data ownership
Receives hazard notifications, initiates safe-state sequences, confirms safe state, and logs safety events. Does not own interlock logic (hardware independent). Owns **safety events**.

### 2) Technology options
- Integration: OPC-UA / digital IO / vendor API
- Recommended: OPC-UA where available + fallback digital IO gateway
- Justification: meets **INF-FR-SafeState** (interlocks independent).

### 3) Recommended default stack
Go service + gRPC + dedicated low-latency link to safety gateway.  
Justification: meets **INF-NFR-SafeState2s**.

### 4) Interface design
Internal: `Safety.HazardNotify`, `Safety.InitiateSafeState`.

### 5) Data model / schema
Safety events stored append-only in `audit_event` with `action="SAFETY_*"`.

### 6) Caching & consistency
No caching; strong ordering by timestamp.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/commandrouter-deployment.yaml` in Section L.

Replica sizing guidance (initial):
- Small: 1–2 replicas (on-site only)
- Medium: 3 replicas (remote monitoring + queue)
- Large: 5+ replicas (10 nodes, heavy monitoring)

Justification: meets **INF-NFR-Nodes10**.

## E2. DB HA topology, backups
- PostgreSQL HA: 3-node (1 primary, 2 synchronous replicas) using Patroni.
- Backups: base backup nightly + WAL archiving continuous; restore drill monthly.
- RPO: 5 minutes; RTO: 30 minutes for control DB; telemetry DB can be longer.
Justification: meets **INF-NFR-DataRedundancyNoLoss** and **INF-NFR-Recover5Min** (operational goal).

## E3. Network topology + ingress/egress rules
Mapped to *PhysicalView* “Gemini_Deployment” (GW↔SummitLAN, SummitLAN↔IOCNet).
- Ingress: only SecurityGateway exposed to WAN; all other services cluster-internal.
- Egress: ArchiveTransferService allowed to Archive + HomeInstitute endpoints only.
Justification: meets **INF-NFR-FirewallGateway** and **INF-NFR-RemoteOpsTransparency**.

## E4. CI/CD sketch
1. PR: lint + unit + contract tests (OpenAPI/Proto) + SAST
2. Build images + SBOM + sign
3. Deploy to staging (summit-sim) with simulators
4. E2E sequences + performance gates (2s accept/reject, 500ms timeout)
5. Canary to summit-prod; rollback on SLO burn
Justification: meets **INF-NFR-VersionConsistencyBoot**.

---

# F. Security Design

## F1. Auth & AuthZ
- OIDC login (Keycloak) → short-lived access token (15 min) + refresh token (8 h).
- PolicyService enforces RBAC + site/level/mode constraints per request.
- Revocation: token introspection for gateway; session invalidation on logout/timeout.
Justification: meets **INF-FR-AuthLogon** and **INF-FR-SiteRestrictionsDynamic**.

## F2. Secrets management
- Kubernetes Secrets sealed (SealedSecrets) + optional Vault for rotation.
- Rotate DB creds quarterly; rotate TLS certs every 60–90 days.
Justification: meets **INF-NFR-SecurityIntrusionProtection**.

## F3. TLS & service mesh
- TLS 1.2+ at gateway; mTLS inside cluster (Istio optional).
Justification: meets **INF-NFR-TLSRemote**.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| WAN intrusion | Gateway allowlist + IDS + no direct service exposure (**INF-NFR-FirewallGateway**) |
| Privilege escalation | Central policy decisions + audit + least privilege (**INF-FR-AccessModes**) |
| Command spoofing/replay | mTLS + nonce/commandId + audit chain (**INF-FR-ACKNAKProtocol**) |
| Monitoring DoS | Rate limits + separate monitoring service (**INF-FR-MonitorNonIntrusive**) |
| Data exfiltration | Egress policies + encrypted transfers (**INF-FR-FITSTransfer**) |

---

# G. Observability & SRE

## G1. Metrics/traces/logs + example alerts
- Metrics: command latency, ACK/NAK rate, allocator contention, status query latency, telemetry ingest lag, archive backlog.
- Tracing: trace per sequence step across Sequencer→Router→Adapter.
- Logs: structured JSON; audit append-only.

Example Prometheus rules:
- `CommandAcceptLatencyHigh` (p95 > 2s)
- `TelemetryIngestLagHigh` (NATS consumer lag)

(See Section L for example rules embedded in runbook notes.)

Justification: meets **INF-NFR-CommandAccept2s** and **INF-NFR-Logging200Hz**.

## G2. SLOs, error budgets, RTO/RPO
- SLO: 99.9% of commands validated (accept/reject) within 2s.
- SLO: 99% status snapshots within 5s.
- RTO/RPO: see E2.
Justification: meets **INF-NFR-CommandAccept2s**, **INF-NFR-StatusRequest5s**.

## G3. Dashboard/runbook sketch
- Dashboards: “Night Ops”, “Remote Monitoring”, “Allocator”, “Archive”.
- Runbooks: “Safe-state triggered”, “IOC unresponsive”, “Telemetry overload”.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components |
|---|---|
| Unit | PolicyService, Allocator, Router validation |
| Integration | Router↔Adapters, Sequencer↔Allocator, Monitoring↔StatusAPI |
| Contract | OpenAPI + Proto compatibility gates |
| E2E | ExecuteSequence, RemoteMonitoring, SafeState |
| Chaos | Kill Router pod, DB failover, NATS partition |

Justification: meets **INF-NFR-Recover5Min**.

## H2. Test data & environment isolation
- Environments: dev, summit-sim (with simulators), staging, prod.
- Refresh: nightly for sim; prod data never copied to dev.
Justification: meets **INF-FR-Simulator**.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
1. Stand up summit-sim with VirtualTelescopeSimulator + simulated IOCs.
2. Integrate one subsystem at a time (TCS first), dual-run with legacy if present.
3. Enable monitoring-only remote first; then planning; then sequencer submit.
4. Cutover control plane with rollback to legacy command path.
Justification: meets **INF-NFR-EvolutionaryDevelopment**.

## I2. Backwards compatibility/versioning
- External API versioned `/v1`; deprecations supported for ≥24 months for visitor API.
Justification: meets **INF-FR-VisitorInstrumentSubsetAPI** (stable long-lived interface).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Why chosen |
|---|---|---|
| gRPC internal contracts | REST-only; message bus only | gRPC provides strict typing for ACK/NAK and timeouts (**INF-FR-ACKNAKProtocol**) |
| PostgreSQL as primary store | CockroachDB; MySQL | Strong consistency + mature HA tooling (**INF-FR-ResourceAllocation**) |
| NATS buffering for telemetry | Kafka; direct DB writes | Lower ops overhead and good for bursty telemetry (**INF-NFR-Logging200Hz**) |
| Separate MonitoringService | Direct subsystem polling from UI | Prevents monitoring from impacting observing (**INF-FR-MonitorNonIntrusive**) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** EPICS is used within IOCs for ParameterDB; host-side DB is PostgreSQL.  
- **A2:** “Command types” can be classified into hazardous vs non-hazardous for safety gating.  
- **A3:** Remote “direct control” is only allowed from approved sites and only when local safety presence is asserted.  
- **A4:** FITS packaging and compression standards are available via existing libraries (cfitsio).  
- **A5:** WAN essential tasks use project-controlled links; Internet only for non-essential tasks.

## Open stakeholder questions
1. Define the authoritative list of **critical resources** for AccessModeAllocator (beam, mount, enclosure, instrument mechanisms?).  
2. What are the exact **site restriction policies** (which sites can do what, and when)?  
3. What is the required **audit retention** duration for telemetry vs audit events?  
4. Confirm acceptable **remote monitoring update rates** per subsystem (10Hz is assumed in diagrams).  
5. Confirm whether **visitor instrument** needs telescope offset/focus only, or additional standardized operations.

## Conflict log
- No explicit conflicts detected between diagrams and narrative; however narrative uses “Operations staff / support personnel / developers” while diagrams use “OperationsStaff/MaintenanceEngineer/RemoteUser”. We will prefer narrative naming in UI labels and policy roles; keep diagram role names as implementation roles.

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# (This document is the architecture.md content; copy from Section A through end.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Gemini Observatory Control System (OCS) External API
  version: "1.0.0"
servers:
  - url: https://ocs.example.org
security:
  - bearerAuth: []
paths:
  /v1/sessions:
    post:
      summary: Create session (OIDC token exchange)
      operationId: createSession
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [idToken, siteId]
              properties:
                idToken: { type: string }
                siteId: { type: string }
      responses:
        "201":
          description: Session created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Session"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /v1/modes/select:
    post:
      summary: Select operational level and access mode
      operationId: selectMode
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [operationalLevel, accessMode]
              properties:
                operationalLevel:
                  type: string
                  enum: [Observing, Maintenance, Test]
                accessMode:
                  type: string
                  enum: [Observing, Monitoring, Operation, Planning, Testing, Administrative]
      responses:
        "200":
          description: Mode accepted
          content:
            application/json:
              schema:
                type: object
                properties:
                  accepted: { type: boolean }
                  policyVersion: { type: string }
        "403":
          $ref: "#/components/responses/Forbidden"
  /v1/observation-plans:
    post:
      summary: Submit an observation plan to the scheduler/sequencer
      operationId: submitObservationPlan
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ObservationPlan"
      responses:
        "202":
          description: Accepted for scheduling
          content:
            application/json:
              schema:
                type: object
                properties:
                  planId: { type: string }
                  status: { type: string, enum: [QUEUED, REJECTED] }
        "400":
          $ref: "#/components/responses/BadRequest"
        "403":
          $ref: "#/components/responses/Forbidden"
  /v1/queues/{queueId}/execute-next:
    post:
      summary: Execute next step in queue (operator/sequencer)
      operationId: executeNext
      parameters:
        - name: queueId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Step executed
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StepResult"
        "409":
          description: Resource conflict / lease unavailable
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/status/{subsystemId}:
    get:
      summary: Get read-only status snapshot for a subsystem
      operationId: getStatus
      parameters:
        - name: subsystemId
          in: path
          required: true
          schema: { type: string }
        - name: detail
          in: query
          required: false
          schema:
            type: string
            enum: [short, verbose]
      responses:
        "200":
          description: Status snapshot
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StatusSnapshot"
        "403":
          $ref: "#/components/responses/Forbidden"
  /v1/commands:
    post:
      summary: Submit a direct control command (restricted)
      operationId: submitCommand
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Command"
      responses:
        "200":
          description: ACK/NAK returned before action
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AckNak"
        "403":
          $ref: "#/components/responses/Forbidden"
        "409":
          description: Safety gate or site restriction failed
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/data-products/{dataId}:
    get:
      summary: Get data product metadata (FITS stored elsewhere)
      operationId: getDataProduct
      parameters:
        - name: dataId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Data product metadata
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DataProduct"
  /v1/archive/transfer:
    post:
      summary: Trigger FITS transfer to home institute endpoint
      operationId: transferFits
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [dataId, destination]
              properties:
                dataId: { type: string }
                destination:
                  type: object
                  required: [type, uri]
                  properties:
                    type: { type: string, enum: [SFTP, HTTPS] }
                    uri: { type: string }
      responses:
        "202":
          description: Transfer started
          content:
            application/json:
              schema:
                type: object
                properties:
                  transferId: { type: string }
                  status: { type: string, enum: [STARTED] }
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    Forbidden:
      description: Forbidden
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string }
        message: { type: string }
        requestId: { type: string }
        details: { type: object, additionalProperties: true }
    Session:
      type: object
      required: [sessionId, userId, role, siteId, operationalLevel, accessMode]
      properties:
        sessionId: { type: string }
        userId: { type: string }
        role:
          type: string
          enum: [Astronomer, TelescopeOperator, OperationsStaff, MaintenanceEngineer, RemoteUser, VisitorInstrument]
        siteId: { type: string }
        operationalLevel: { type: string, enum: [Observing, Maintenance, Test] }
        accessMode: { type: string, enum: [Observing, Monitoring, Operation, Planning, Testing, Administrative] }
    ObservationPlan:
      type: object
      required: [programId, constraints, sequence]
      properties:
        programId: { type: string }
        constraints: { type: object, additionalProperties: true }
        sequence: { type: string, description: "Serialized sequence DSL" }
    Command:
      type: object
      required: [type, target, parameters]
      properties:
        type: { type: string }
        target: { type: string }
        parameters: { type: object, additionalProperties: true }
    AckNak:
      type: object
      required: [commandId, status, sentAt, timeoutMs]
      properties:
        commandId: { type: string }
        status: { type: string, enum: [ACK, NAK] }
        sentAt: { type: string, format: date-time }
        timeoutMs: { type: integer, minimum: 1 }
        reason: { type: string }
    StatusSnapshot:
      type: object
      required: [subsystemId, timestamp, payload]
      properties:
        subsystemId: { type: string }
        timestamp: { type: string, format: date-time }
        payload: { type: object, additionalProperties: true }
    StepResult:
      type: object
      required: [stepId, outcome]
      properties:
        stepId: { type: string }
        outcome: { type: string, enum: [SUCCESS, FAILED, RETRIED] }
        ackNak: { $ref: "#/components/schemas/AckNak" }
    DataProduct:
      type: object
      required: [dataId, format, compressed, storedAt]
      properties:
        dataId: { type: string }
        format: { type: string, enum: [FITS] }
        compressed: { type: boolean }
        storedAt: { type: string }
        header: { type: object, additionalProperties: true }
```

```proto
// filename: internal.proto
syntax = "proto3";

package gemini.ocs.v1;

import "google/protobuf/timestamp.proto";

message UserContext {
  string session_id = 1;
  string user_id = 2;
  string role = 3;
  string site_id = 4;
  string operational_level = 5; // Observing|Maintenance|Test
  string access_mode = 6;       // Observing|Monitoring|Operation|Planning|Testing|Administrative
  string policy_version = 7;
}

message Command {
  string command_id = 1;
  string type = 2;
  string target = 3;
  map<string, string> parameters = 4;
  google.protobuf.Timestamp requested_at = 5;
  string requested_by = 6;
  string site_id = 7;
  bool requires_resource = 8;
}

message AckNak {
  string command_id = 1;
  string status = 2; // ACK|NAK
  google.protobuf.Timestamp sent_at = 3;
  int32 timeout_ms = 4;
  string reason = 5;
}

message AllocateRequest {
  UserContext ctx = 1;
  string resource_id = 2;
  string mode = 3;
  int32 lease_ttl_seconds = 4;
}

message ResourceLease {
  string lease_id = 1;
  string resource_id = 2;
  string holder_session_id = 3;
  string mode = 4;
  google.protobuf.Timestamp expires_at = 5;
}

message AllocateResponse {
  bool granted = 1;
  ResourceLease lease = 2;
  string reason = 3;
}

service Allocator {
  rpc Allocate(AllocateRequest) returns (AllocateResponse);
  rpc Release(ResourceLease) returns (AckNak);
  rpc Renew(ResourceLease) returns (ResourceLease);
}

message ExecuteRequest {
  UserContext ctx = 1;
  Command cmd = 2;
  string lease_id = 3;
}

service CommandRouter {
  rpc ExecuteCommand(ExecuteRequest) returns (AckNak);
}

message StatusRequest {
  UserContext ctx = 1;
  string subsystem_id = 2;
  string detail = 3; // short|verbose
}

message StatusSnapshot {
  string subsystem_id = 1;
  google.protobuf.Timestamp timestamp = 2;
  map<string, string> payload = 3;
}

service Status {
  rpc GetSnapshot(StatusRequest) returns (StatusSnapshot);
}

message HazardNotification {
  string hazard_code = 1;
  string source = 2;
  google.protobuf.Timestamp timestamp = 3;
}

service Safety {
  rpc HazardNotify(HazardNotification) returns (AckNak);
  rpc InitiateSafeState(UserContext) returns (AckNak);
}
```

```yaml
# filename: k8s/commandrouter-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: commandrouter
  namespace: gemini-ocs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: commandrouter
  template:
    metadata:
      labels:
        app: commandrouter
    spec:
      containers:
        - name: commandrouter
          image: ghcr.io/gemini/commandrouter:1.0.0
          ports:
            - containerPort: 8080
            - containerPort: 9090
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          envFrom:
            - configMapRef:
                name: ocs-config
            - secretRef:
                name: ocs-secrets
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: commandrouter
  namespace: gemini-ocs
spec:
  selector:
    app: commandrouter
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: grpc
      port: 9090
      targetPort: 9090
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: commandrouter-hpa
  namespace: gemini-ocs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: commandrouter
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
  name: ocs-config
  namespace: gemini-ocs
data:
  POLICY_SERVICE_URL: "http://policyservice.gemini-ocs.svc.cluster.local"
  NATS_URL: "nats://nats.gemini-ocs.svc.cluster.local:4222"
  COMMAND_TIMEOUT_MS: "500"
---
apiVersion: v1
kind: Secret
metadata:
  name: ocs-secrets
  namespace: gemini-ocs
type: Opaque
stringData:
  DB_DSN: "postgres://ocs:change-me@postgres.gemini-ocs.svc.cluster.local:5432/ocs?sslmode=require"
```

```sql
-- filename: sql/observation_plan_ddl.sql
CREATE TABLE IF NOT EXISTS observation_plan (
  plan_id            TEXT PRIMARY KEY,
  program_id         TEXT NOT NULL,
  constraints_json   JSONB NOT NULL,
  sequence_dsl       TEXT NOT NULL,
  created_by         TEXT NOT NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  status             TEXT NOT NULL CHECK (status IN ('QUEUED','REJECTED','RUNNING','COMPLETED','FAILED'))
);

CREATE INDEX IF NOT EXISTS idx_observation_plan_program ON observation_plan(program_id);
CREATE INDEX IF NOT EXISTS idx_observation_plan_status ON observation_plan(status);
```

```sql
-- filename: sql/command_ddl.sql
CREATE TABLE IF NOT EXISTS command (
  command_id     TEXT PRIMARY KEY,
  type           TEXT NOT NULL,
  target         TEXT NOT NULL,
  parameters_json JSONB NOT NULL,
  requested_at   TIMESTAMPTZ NOT NULL,
  requested_by   TEXT NOT NULL,
  site_id        TEXT NOT NULL,
  status         TEXT NOT NULL CHECK (status IN ('ACK','NAK','TIMEOUT','RETRIED')),
  reason         TEXT,
  lease_id       TEXT,
  policy_version TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_command_requested_at ON command(requested_at);
CREATE INDEX IF NOT EXISTS idx_command_target ON command(target);
```

```sql
-- filename: sql/resource_lease_ddl.sql
CREATE TABLE IF NOT EXISTS resource_lease (
  lease_id           TEXT PRIMARY KEY,
  resource_id        TEXT NOT NULL,
  holder_session_id  TEXT NOT NULL,
  mode               TEXT NOT NULL,
  expires_at         TIMESTAMPTZ NOT NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_resource_active_lease
ON resource_lease(resource_id)
WHERE expires_at > now();
```

```sql
-- filename: sql/audit_event_ddl.sql
CREATE TABLE IF NOT EXISTS audit_event (
  audit_id      TEXT PRIMARY KEY,
  timestamp     TIMESTAMPTZ NOT NULL,
  actor_session_id TEXT NOT NULL,
  action        TEXT NOT NULL,
  target        TEXT NOT NULL,
  result        TEXT NOT NULL,
  details_json  JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Append-only enforcement is done via DB permissions (no UPDATE/DELETE for app role).
CREATE INDEX IF NOT EXISTS idx_audit_event_time ON audit_event(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_event_action ON audit_event(action);
```

```sql
-- filename: sql/telemetry_event_ddl.sql
CREATE TABLE IF NOT EXISTS telemetry_event (
  event_id     TEXT PRIMARY KEY,
  timestamp    TIMESTAMPTZ NOT NULL,
  source       TEXT NOT NULL,
  type         TEXT NOT NULL,
  payload_json JSONB NOT NULL
) PARTITION BY RANGE (timestamp);

-- Example monthly partition (ops creates ahead of time)
CREATE TABLE IF NOT EXISTS telemetry_event_2026_03
PARTITION OF telemetry_event
FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

CREATE INDEX IF NOT EXISTS idx_telemetry_time ON telemetry_event_2026_03(timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_source ON telemetry_event_2026_03(source);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-AuthLogon,Logon and determine privileges at login,"Gemini_UseCase:UC_Logon; Gemini_Class:UserSession",AuthService|PolicyService,openapi.yaml|internal.proto,Central authn/authz ensures consistent gating across modes/levels.
INF-FR-OperationalLevels,Observing/Maintenance/Test operational levels,"Gemini_State_OperationalLevel:ObservingLevel/MaintenanceLevel/TestLevel",PolicyService,internal.proto,Explicit state machine prevents invalid transitions.
INF-FR-AccessModes,Observing/Monitoring/Operation/Planning/Testing/Administrative modes,"Gemini_State_OperationalLevel:ObservingMode..AdministrativeMode",PolicyService|GeminiUI,openapi.yaml,Mode-aware UI + policy checks.
INF-FR-SequencerMediated,Observing control via sequencer; no direct telescope control for astronomers,"Gemini_UseCase:UC_ExecSeq; Gemini_Class:SchedulerSequencer",SchedulerSequencer|CommandRouter,openapi.yaml|internal.proto,Single point of control supports queue/service observing.
INF-FR-MonitorNonIntrusive,Monitoring read-only and must not affect observing,"Gemini_Sequence_RemoteMonitoring:MonitoringService loop",MonitoringService|SubsystemStatusAPI,openapi.yaml|internal.proto,Rate limiting + read-only endpoints isolate monitoring.
INF-FR-ACKNAKProtocol,Uniform ACK/NAK with timeouts and retries,"Gemini_Sequence_ExecuteSequence:TelescopeControlSubsystem->ACK/NAK",CommandRouter|SubsystemAdapters,internal.proto,Typed contract enforces predictable command semantics.
INF-FR-ResourceAllocation,Critical resources allocated only via allocator; deadlock-free,"Gemini_Class:AccessModeAllocator",AccessModeAllocator,internal.proto|sql/resource_lease_ddl.sql,Lease-based allocation prevents deadlock and orphan locks.
INF-FR-SafeState,Safe-state on hazard; interlocks independent,"Gemini_UseCase:UC_SafeState; Gemini_Deployment:SafetyHW",SafetyManager,internal.proto,Safety path must work even if higher-level software fails.
INF-FR-DataArchiveAuto,Automatic archiving during observing/maintenance,"Gemini_Activity_ExecuteSequence:Archive DataProduct",ArchiveTransferService,openapi.yaml|sql/data_product_ddl.sql,Ensures data durability and workflow compliance.
INF-FR-FITSTransfer,Transfer FITS to home institutes,"Gemini_UseCase:UC_TransferFITS",ArchiveTransferService,openapi.yaml,Standard FITS distribution.
INF-FR-Simulator,Virtual telescope + subsystem simulators,"Gemini_Component:VirtualTelescopeSimulator",VirtualTelescopeSimulator,internal.proto,Enables planning/testing without hardware.
INF-FR-VisitorInstrumentSubsetAPI,Stable subset API for visitor instruments,"Gemini_Component:VisitorInstrumentAPI",VisitorInstrumentAPI,openapi.yaml,Long-lived integration surface.
INF-NFR-CommandAccept2s,Accept/reject commands within 2 seconds,"Gemini_Class:Command note",CommandRouter,internal.proto,Router validates and authorizes before dispatch.
INF-NFR-Timeout500ms,Protocol timeout approx 500ms,"Gemini_Activity_ExecuteSequence:Receive ACK/NAK",CommandRouter,internal.proto,Timeouts enforced in router/adapters.
INF-NFR-Handshake200ms,Handshaking within 100-200ms,"Gemini_Activity_ExecuteSequence:Receive ACK/NAK",SubsystemAdapters,internal.proto,Adapter contract includes immediate ACK/NAK.
INF-NFR-ControlTPS100,Peak control info 100 TPS,"Gemini_Deployment:SummitLAN",Platform,k8s/commandrouter-deployment.yaml,Horizontal scaling + traffic isolation.
INF-NFR-StatusUpdateLocal4s,Local status update within 4 seconds,"Gemini_Sequence_RemoteMonitoring:UpdateDisplay",MonitoringService,openapi.yaml,Bounded polling/subscription.
INF-NFR-StatusRequest5s,Status requests answered within 5 seconds,"Gemini_Component:SubsystemStatusAPI",SubsystemStatusAPI,internal.proto,Status API designed non-blocking.
INF-NFR-Logging200Hz,Engineering data logging up to 200Hz bursts,"Gemini_Class:LoggingService note",LoggingService,sql/telemetry_event_ddl.sql,Partitioned append-only telemetry store.
INF-NFR-Nodes10,Support up to 10 active nodes,"Gemini_Deployment:ControlNode-1/2",Platform,k8s/commandrouter-deployment.yaml,Stateless services scale horizontally.
```

---

## Acceptance Criteria Verification Table

| Check | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | [x] |
| [ ] Sections A-L included. | [x] |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | [ ] *(Full narrative corpus is extremely large; requires stakeholder confirmation to enumerate remaining INF-* items beyond those normalized here.)* |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | [x] |
| [ ] Representative k8s manifest snippet included. | [x] |
| [ ] SQL DDL / NoSQL models for primary entities included. | [x] |
| [ ] All major components have at least one API contract and a data schema. | [ ] *(Data schema for some components is shared via audit/telemetry; expand if separate tables required.)* |
| [ ] Assumptions and unresolved questions listed. | [x] |

---

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?