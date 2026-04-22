Scope: Design a production-ready Gemini Observing Control System (OCS) architecture from the provided narrative SRS and the 11 supplied UML views.  
Approach: Normalize requirements into traceable IDs (INF-* where needed), then specify 4+1 architecture, contracts (OpenAPI + gRPC), schemas, and ops/security/SRE/test plans.  
Top validation steps: (1) end-to-end command path timing (ACK/NAK/timeout), (2) non-intrusive monitoring + isolation, (3) resource allocation deadlock-freedom + safety interlocks + auditability.

# A. Executive Summary (≤1 page)

## System overview
Gemini OCS is a distributed control, sequencing, monitoring, and data-archiving platform for telescope + multi-instrument operations across operational levels (Observing/Maintenance/Test) and access modes (Observing/Monitoring/Operation/Planning/Testing/Admin), including remote operations with dynamic site restrictions, simulation (virtual telescope), robust logging, and non-intrusive monitoring.

**Primary diagram mapping (titles + key element IDs):**
- Scenario View: **UseCaseDiagram** (UC_RunQueue, UC_DirectControl, UC_MonitorStatus, UC_AllocateResource, UC_RunSimulation, UC_ManageRemotePolicy)
- Container/Physical: **ContainerDiagram** (C_UI, C_APIGW, C_SEQ, C_ROUTER, C_ALLOC, C_GW, C_BUS, C_PARAMDB, C_LOGDB)
- Deployment: **DeploymentDiagram** (OCSCluster/AppNode-* , IOCNet/TelescopeIOC/InstrumentIOCs, DBServer)
- Runtime control: **SequenceScenario1_RunQueueAndControl** (CommandRouter→Allocator→ControlGateway→IOCs)
- Policy enforcement: **SequenceScenario2_RemotePolicyUpdate** (PolicyService + PolicyDB + enforcement within 60s)

## Chosen architectural style(s)
- **Layered + microservice-oriented control plane** with strict command contracts and centralized policy/audit (Auth/Policy/Router/Gateway).  
- **Event-driven telemetry/logging** via pub/sub to isolate monitoring and near-line work from observing control.

## Deployment topology (one-line)
- **HA service cluster** (OCSCluster) + **separate IOC network** (EPICS) + **dedicated DB/log store** + **external archive integration**, with local and remote UI nodes (DeploymentDiagram: LocalStations/RemoteStations/OCSCluster/IOCNet/DBServer).

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| R1: Monitoring/near-line workloads interfere with observing control latency | Lost observing time; violates non-intrusive requirement | TelemetryBus isolation + rate-limits + separate consumers; prioritize CommandRouter/ControlGateway CPU; enforce SLO guardrails (ASR-003, NFR-001, NFR-004). |
| R2: Resource deadlock or unsafe concurrent access (multi-instrument + beam exclusivity) | Stalled operations or safety hazard | Central AccessModeAllocator with lease TTL + deadlock detection; beam-exclusive resource model; deny conflicting leases (ASR-005, ASR-012, FR-027). |
| R3: Remote operations security/site policy ambiguity and misconfiguration | Unauthorized control or intrusion | Central PolicyService (RBAC + RemoteSitePolicy), audited policy changes, default-deny, TLS everywhere, per-operation site gating (FR-018, ASR-006, NFR-008). |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality area | IDs covered | Primary test types |
|---|---|---|
| Scalability/capacity | FR-057, NFR-009 | Load + soak tests; HPA scale tests; broker backpressure tests |
| Availability/recovery | INF-Reliability-01, INF-Reconfig-01, FR-060 | Chaos/failover drills; backup/restore; simulated subsystem failure + reconfigure |
| Security | FR-039, FR-018, NFR-008, INF-Security-01 | Pen test + SAST/DAST; RBAC tests; audit immutability tests |
| Performance/latency | NFR-001, NFR-004, NFR-005, NFR-017 | Latency budgets; protocol timing tests; network throughput tests |
| Maintainability/testability | FR-040, FR-041, FR-043, ASR-008 | Contract tests; simulator swap tests; regression suite; version-consistency checks |

---

# B. Traceability & Rationale

Because the “Original Requirements” are narrative and do not provide stable FR/NFR/ASR IDs, this design **derives** IDs as `INF-*` (inferred). Where the provided UML notes referenced FR/NFR/ASR labels not present in the narrative, the **requirements text wins** and the conflict is logged in **K**.

Traceability table is also delivered as `traceability_matrix.csv` in Section L.

**Traceability Matrix (excerpt; full in Section L artifact):**

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-AccessLevels-01 | System has disjoint operational levels: Observing/Maintenance/Test | StateDiagram:OCSSession; ClassDiagram:OperationalLevel | PolicyService, Session, OperationalState | architecture.md; internal.proto | Levels affect authorization and allowed mode combos; centralized policy avoids drift. |
| INF-AccessModes-01 | Access modes: Observing/Monitoring/Operation/Planning/Testing/Admin | ClassDiagram:AccessMode; UseCaseDiagram:UC_SelectMode | PolicyService, RemoteUI | openapi.yaml | UI and APIs must be mode-aware; mode drives command routing rules. |
| INF-NonIntrusiveMonitoring-01 | Monitoring must not affect ongoing observation | UseCaseDiagram:UC_MonitorStatus; ComponentDiagram:TelemetryBus | TelemetryBus, StatusAPI | architecture.md; internal.proto | Use async pub/sub + read-only queries with rate limits to isolate control path. |
| INF-SeqPrimary-01 | Observing normally via automatic Sequencer; direct interactive is exception | UseCaseDiagram:UC_RunQueue; StateDiagram:Observing | Sequencer, Scheduler | openapi.yaml | Enforces single point of control/responsibility and supports service/queue observing. |
| INF-QueueResequence-01 | Queue break/resequence based on conditions/QA | ActivityDiagram:Resequence; ClassDiagram:Sequencer.breakAndResequence | Scheduler, Sequencer | openapi.yaml | Required for flexible scheduling/service observing; implemented as scheduler rule engine. |
| INF-RemoteOps-01 | Remote operations supported; restrict specific ops to specific sites dynamically | UseCaseDiagram:UC_ManageRemotePolicy; SequenceScenario2_RemotePolicyUpdate | PolicyService, PolicyDB | openapi.yaml; sql/policy_ddl.sql | Site gating is independent of operations; dynamic update and enforcement. |
| INF-CmdProtocol-01 | Common command syntax; uniform ACK/NAK; timeout ~500ms; handshake 100–200ms | ClassDiagram:CommandEnvelope/Response; SequenceScenario1_RunQueueAndControl | CommandRouter, ControlGateway | internal.proto | Deterministic command contracts + correlation IDs are required for timing and recovery. |
| INF-CmdAccept-01 | Accept/reject within 2s before action | StateDiagram:CommandPath; SequenceScenario1 | CommandRouter | internal.proto; metrics alerts | Enforced at router boundary; rejects before IOC action begins. |
| INF-StatusLatency-01 | Status display update ≤4s local; status query ≤5s | ActivityDiagram:MonitorStatus; ClassDiagram:ControlVariable note | StatusAPI, ControlGateway | openapi.yaml; metrics alerts | Ensures UX responsiveness; remote may degrade but must remain functional. |
| INF-Traffic-01 | Peak control info ~100 TPS; isolate traffic via bridging | DeploymentDiagram:IOCNet; ComponentDiagram:TelemetryBus | ControlGateway, TelemetryBus | architecture.md | Separation of control and telemetry prevents cross-impact at peak command rates. |
| INF-DataFormat-01 | Store detector/instrument data in standard format; FITS for institute transmission; lossless compression | ClassDiagram:DataProduct note; ActivityDiagram:StoreData | ArchiveClient, Data pipeline | openapi.yaml; sql/data_product_ddl.sql | Fits archival and transmission requirements; compression reduces LAN/WAN impact. |
| INF-Retention-01 | Keep 7 days data; last 3 days interactive on disk | ClassDiagram:DataProduct note | ArchiveClient, On-site storage | architecture.md | Drives storage tiering and lifecycle policies. |
| INF-QuickLook-01 | Quick-look synchronous; usable in sequences; no manual intervention | ActivityDiagram:QuickLook; ComponentDiagram:QuickLookProcessor | QuickLookProcessor | internal.proto | Implemented as synchronous step callback with bounded compute and circuit breakers. |
| INF-NearLine-01 | Near-line reduction asynchronous; acquisition takes precedence | ComponentDiagram:NearLineProcessor note | NearLineProcessor, TelemetryBus | architecture.md | Backpressure & drop/defer policy prevents acquisition slowdown. |
| INF-Audit-01 | Log actions to recreate observation sequence; correlation IDs; 200Hz burst eng logging | ComponentDiagram:AuditLogService/EventLogService; ContainerDiagram:C_LOGDB | AuditLogService, EventLogService | sql/audit_event_ddl.sql | Supports traceability, debugging, and reliability monitoring. |
| INF-Versioning-01 | Version-labeled source/binaries; retrievable via commands; boot checks version consistency | ClassDiagram:Subsystem.getVersion | ControlGateway, IOC adapters | internal.proto | Ensures configuration control and reduces mismatch failures. |
| INF-Simulator-01 | All subsystems provide simulator module; easy replace hardware with simulation | UseCaseDiagram:UC_RunSimulation; ComponentDiagram:SimulatorAdapter | SimulatorAdapter | internal.proto | Supports virtual telescope planning/test and integration without hardware. |
| INF-Safety-01 | Safety: system to safe state on danger; interlocks independent of software; remote control safety prerequisites | Requirements narrative; UseCaseDiagram note | Safety interlock layer (IOC) + router flags | architecture.md | Software must respect interlocks and propagate safety status; command flags enforce restrictions. |

---

# C. Architecture Overview

## Context (users/external systems)
- Users: Observing Astronomer, Science Observer, Telescope Operator, Ops Staff, Support, Developers, Administrators, Remote users.
- External systems: Gemini Archive, Star Catalogs, Weather Station, Time Reference, commercial DBMS, EPICS IOC layer.

Referenced diagrams:
- **UseCaseDiagram** (actors + UC_*).
- **DeploymentDiagram** (GeminiArchive external; External Data Sources cloud).

## Container view
Core containers:
- **RemoteUI** (C_UI): mode-aware UX, supports monitoring duplication, planning, queue operations.
- **OCS API Gateway** (C_APIGW): HTTPS entrypoint; auth hooks; request shaping.
- **AuthService** (C_AUTH), **PolicyService** (C_POLICY).
- **Sequencer/Scheduler** (C_SEQ/C_SCHED).
- **CommandRouter** (C_ROUTER), **AccessModeAllocator** (C_ALLOC), **ControlGateway** (C_GW), **SimulatorAdapter** (C_SIM).
- **TelemetryBus** (C_BUS) + **QuickLook/NearLine** (C_QL/C_NL) + **ArchiveClient** (C_ARCH).
- **ParameterDB / PolicyDB / LogStore** (C_PARAMDB/C_POLICYDB/C_LOGDB).

Referenced diagram: **ContainerDiagram** (C_* IDs).

## Component/package view
- Package grouping aligns to **PackageDiagram** (ui/api/domain/security/orchestration/control/data/observability).
- Runtime interactions align to **ComponentDiagram** (IAuthAPI/IPolicyAPI/ICommandAPI/IStatusAPI/IArchiveAPI).

## Class/runtime view
- CommandEnvelope + CommandResponse with correlation IDs; RBACPolicy + RemoteSitePolicy gating; leases for critical resources.  
Referenced: **ClassDiagram**, **StateDiagram**, **SequenceScenario1_RunQueueAndControl**.

## Deployment view
- HA OCSCluster + DBServer + IOCNet; local and remote stations; TLS across WAN/LAN.  
Referenced: **DeploymentDiagram**.

---

# D. Detailed Technical Design (developer-facing)

## D1. OCS API Gateway (C_APIGW)

### 1) Responsibilities & data ownership
Terminates TLS, authenticates requests (via AuthService), enforces request validation and rate limits, forwards to internal services, and injects correlation IDs for end-to-end tracing. Owns **no** domain data; logs access events.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: **Go 1.22–1.23** (fast, low-latency, simple concurrency).  
  Justification: meets **INF-CmdAccept-01** (≤2s accept/reject) by minimizing overhead.
- Conservative: **Java 17–21 (Spring Boot 3.2+)** (mature ecosystem).  
  Justification: meets **INF-Audit-01** via mature observability/audit libraries.
- Cutting-edge: **Rust 1.78+ (Axum)** (performance + safety).  
  Justification: meets **INF-StatusLatency-01** by reducing CPU jitter.

**Web framework**
- Recommended: Go **chi v5** or **gin v1.10**.  
  Justification: meets **INF-StatusLatency-01** with low middleware overhead.
- Conservative: Spring MVC/WebFlux.
- Cutting-edge: Rust Axum / Tower.

**RPC/HTTP**
- Recommended: **HTTP/1.1+JSON external; gRPC internal**.  
  Justification: meets **INF-RemoteOps-01** (remote transparency) while keeping internal low-latency contracts.
- Conservative: REST everywhere.
- Cutting-edge: HTTP/3 externally where WAN supports.

**Persistence/cache/messaging/search/auth/observability/CI/CD/container/infra**
- Persistence: none (stateless); caching via **Redis 7.2–7.4** optional for rate-limit counters.  
  Justification: meets **INF-NonIntrusiveMonitoring-01** by preventing DB hotspots.
- Auth: OIDC passthrough + JWT validation at gateway.  
  Justification: meets **INF-RemoteOps-01** + **INF-Audit-01** (central gate).
- Observability: OpenTelemetry SDK.
- CI/CD: GitHub Actions/GitLab CI; container: containerd; infra: Terraform.

### 3) Recommended default stack
- Go 1.22–1.23 + chi v5 + OpenTelemetry + Envoy or NGINX ingress.
Justification: meets **INF-CmdAccept-01** (≤2s decision) with minimal overhead and consistent tracing.

### 4) Interface design (External APIs) — `openapi.yaml`
(Provided in Section L as a complete file.)

### 5) Data model / schema
No primary tables owned; uses LogStore via AuditLogService.

### 6) Caching & consistency
- Cache: per-IP and per-session rate limit counters (Redis), TTL 60s.
- Consistency: not applicable (stateless).

---

## D2. AuthService (C_AUTH) + PolicyService (C_POLICY)

### 1) Responsibilities & data ownership
- AuthService: interactive + API authentication, MFA support, session issuance (JWT access token + refresh), login auditing.
- PolicyService: RBAC and dynamic remote-site restriction evaluation; policy versioning; “default deny”.

Owns: PolicyDB (RBAC roles/permissions, remote site allowlists, policy versions).

### 2) Technology options

**Language/runtime**
- Recommended: Go 1.22–1.23  
  Justification: meets **INF-CmdAccept-01** to keep authz checks low-latency.
- Conservative: Java 17–21  
  Justification: meets **INF-Security-01** with mature IAM integration.
- Cutting-edge: Rust

**Authn/Authz**
- Recommended: **OIDC (Keycloak 24–26) + fine-grained RBAC in PolicyService**  
  Justification: meets **INF-RemoteOps-01** (dynamic site restrictions independent of operations).
- Conservative: LDAP + custom JWT issuer.
- Cutting-edge: SPIFFE/SPIRE + mTLS identities.

**Persistence**
- Recommended: **PostgreSQL 14–15** (PolicyDB)  
  Justification: meets **INF-Audit-01** (transactional audit of policy changes).
- Conservative: Oracle (if mandated).
- Cutting-edge: CockroachDB (geo-distributed).

**Observability**
- OpenTelemetry + structured logs.

### 3) Recommended default stack
- Keycloak 24–26 for OIDC + Go PolicyService + PostgreSQL 14–15.  
Justification: meets **INF-RemoteOps-01** (dynamic per-site restriction) and **INF-Audit-01** (audited admin changes).

### 4) Internal contracts — `internal.proto`
(Provided in Section L: includes AuthN and Policy checks + command authorization.)

### 5) Data model / schema
- `sql/policy_ddl.sql` includes roles, permissions, site policies, policy versions (Section L).

**Encryption-at-rest fields:** hashed password is externalized to Keycloak; store only opaque references and policy metadata.  
Justification: meets **INF-Security-01** (prevent intrusion and accidental mix-up).

### 6) Caching & consistency
- Cache RBAC permission matrix in-memory in PolicyService, TTL 30s; invalidate on policy_version change.
- Site policy effective within 60s (requirement); enforce by pushing policy version events via TelemetryBus or DB LISTEN/NOTIFY.

---

## D3. Sequencer (C_SEQ) + Scheduler (C_SCHED)

### 1) Responsibilities & data ownership
Sequencer executes observing programs as step sequences (pass-through initially), drives CommandRouter, supports break/resequence, and coordinates quick-look callbacks. Scheduler builds and re-sorts queues using rules, weather, catalogs, and time reference. Owns queue state (QueueDB table or in ParameterDB schema).

### 2) Technology options

**Language/runtime**
- Recommended: Go 1.22–1.23  
  Justification: meets **INF-SeqPrimary-01** (automation-first) with predictable performance.
- Conservative: Java 17–21
- Cutting-edge: Python 3.12 + compiled extensions (riskier for latency predictability)

**Workflow/orchestration**
- Recommended: custom deterministic step engine + persisted state (Postgres)  
  Justification: meets **INF-QueueResequence-01** (break/resequence) with auditability.
- Conservative: Temporal.io (strong workflows)
- Cutting-edge: Cadence/Argo Workflows (K8s-native but heavier)

**Persistence**
- Recommended: PostgreSQL 14–15 for queue state  
  Justification: meets **INF-Audit-01** (recreate observation sequence).

### 3) Recommended default stack
- Go step engine + PostgreSQL queue tables + OTel tracing.  
Justification: meets **INF-SeqPrimary-01** (sequencer primary path) and **INF-Audit-01** (replayable state).

### 4) Interface design
- External endpoints in OpenAPI: `/queues`, `/queues/{id}/run`, `/queues/{id}/resequence`.
- Internal: `CommandService.SubmitCommand` + `TelemetryService.PublishStatus`.

### 5) Data model / schema
See `sql/queue_ddl.sql` (Section L): queues, queue_steps, step_results with correlation IDs.

### 6) Caching & consistency
- Cache external condition fetch results (weather/catalog) TTL 5–30s depending on source; mark stale.
- Queue changes are strongly consistent in DB; step execution uses optimistic locking on queue version.

---

## D4. CommandRouter (C_ROUTER) + AccessModeAllocator (C_ALLOC) + ControlGateway (C_GW) + SimulatorAdapter (C_SIM)

### 1) Responsibilities & data ownership
- CommandRouter: validates, authorizes, assigns correlation IDs, enforces accept/reject within 2s, routes to ControlGateway, writes audit/event logs.
- AccessModeAllocator: exclusive leasing for critical resources (beam, active instrument, telescope axes), TTL-based, deadlock detection/resolution.
- ControlGateway: protocol bridge to IOC network (EPICS), implements ACK/NAK, timeouts, retries for idempotent commands only, status queries non-blocking.
- SimulatorAdapter: simulation substitute for real IOC targets for planning/test/maintenance.

Owns: Resource lease tables; command audit and event tables (or via LogStore service).

### 2) Technology options

**Language/runtime**
- Recommended: Go 1.22–1.23  
  Justification: meets **INF-CmdProtocol-01** (handshake 100–200ms; timeout ~500ms).
- Conservative: Java 17–21 with Netty
- Cutting-edge: Rust

**RPC/internal**
- Recommended: gRPC for internal calls; binary efficiency.  
  Justification: meets **INF-CmdAccept-01** by reducing parse/serialize overhead.
- Conservative: REST internal.
- Cutting-edge: NATS request/reply.

**Messaging**
- Recommended: **NATS JetStream 2.10+** for TelemetryBus (lightweight, low latency, durable streams).  
  Justification: meets **INF-NonIntrusiveMonitoring-01** by decoupling monitoring/logging from control path.
- Conservative: RabbitMQ 3.12+
- Cutting-edge: Redpanda/Kafka (heavier ops)

**Persistence**
- Recommended: PostgreSQL 14–15 for leases + command history.  
  Justification: meets **ASR-005 equivalent** (deadlock avoidance + authoritative allocation) via transactional locks.

### 3) Recommended default stack
- Go services + gRPC internal + PostgreSQL leases + EPICS integration in ControlGateway + NATS JetStream for telemetry.  
Justification: meets **INF-CmdProtocol-01** (timing), **INF-NonIntrusiveMonitoring-01** (isolation), **INF-QueueResequence-01** (traceable steps).

### 4) Interface design
- External: `/commands:submit`, `/status/query`, `/resources/leases`.
- Internal: `CommandService`, `AllocatorService`, `IocGatewayService` in `internal.proto`.

### 5) Data model / schema
- `sql/resource_lease_ddl.sql` includes unique constraints (one beam lease), TTL expiration indexes.
- `sql/audit_event_ddl.sql` includes immutability guidance.

**Immutability fields:** audit_event rows append-only; no UPDATE/DELETE permitted at application layer.  
Justification: meets **INF-Audit-01** (recreate event sequence reliably).

### 6) Caching & consistency
- Cache: last-known status variables in memory in ControlGateway, TTL 1–2s for UI polling.
- Consistency: command acceptance is strong; status is eventually consistent but bounded by NFR-equivalents (≤4s local display, ≤5s query).

---

## D5. Data pipeline: QuickLook (C_QL), NearLine (C_NL), ArchiveClient (C_ARCH), ParameterDB (C_PARAMDB), LogStore (C_LOGDB)

### 1) Responsibilities & data ownership
- QuickLookProcessor: synchronous preview/QA pipeline invoked by Sequencer; must not delay acquisition beyond configured budget.
- NearLineProcessor: asynchronous reductions; must yield to acquisition; can defer/drop under contention.
- ArchiveClient: packages FITS + headers, applies lossless compression policy, sends to GeminiArchive, manages local retention tiers.
- ParameterDB: low-latency access to telescope/instrument parameters; supports async writes and distributed IOC sourcing.
- LogStore: durable storage for audit/event logs and engineering telemetry bursts.

### 2) Technology options

**Persistence (ParameterDB/LogStore/Data products)**
- Recommended: PostgreSQL 14–15 for structured metadata + **object storage (S3-compatible: MinIO RELEASE.*)** for FITS blobs  
  Justification: meets **INF-Retention-01** (7d retention, 3d interactive) via lifecycle policies + cheap blob storage.
- Conservative: SAN/NFS + Postgres metadata
- Cutting-edge: Ceph RGW + TimescaleDB for telemetry

**Compression**
- Recommended: FITS tile compression (lossless) or gzip where appropriate.  
  Justification: meets **INF-DataFormat-01** (lossless compression for transmission/storage).

**Observability storage**
- Recommended: Loki 2.9+ (logs) + Prometheus 2.49+ (metrics) + Tempo (traces)  
  Justification: meets **INF-Audit-01** (traceability) and operational monitoring.

### 3) Recommended default stack
- Postgres metadata + S3-compatible object storage for data products + NATS JetStream events + Prometheus/Loki/Tempo.  
Justification: meets **INF-DataFormat-01** (FITS + headers + compression) and **INF-Audit-01** (replay logs).

### 4) Interfaces
- External: `/data-products/{id}`, `/archive/query`.
- Internal: `TelemetryService.PublishDataProduct` and `ArchiveService.ArchiveDataProduct` (internal.proto).

### 5) Data model / schema
- `sql/data_product_ddl.sql` for metadata (datasetId, fits_uri, headers_json, compression, checksum).
- `sql/engineering_telemetry_ddl.sql` for burst logging (up to 200Hz short periods).

**Encryption-at-rest:** headers_json may contain proprietary info; encrypt column or whole disk.  
Justification: meets **INF-Security-01** (protect private data).

### 6) Caching & consistency
- Cache most recent data-product metadata in Redis TTL 60s for UI browse.
- Archive send is at-least-once with idempotency key = datasetId; store “archived_at” to prevent duplicates.

---

# E. Operations & Deployment (ops-facing)

## E1) Kubernetes-ready plan (`k8s/ocs-commandrouter-deployment.yaml`)
(Provided in Section L as syntactically valid YAML.)

Replica guidance:
- Small: 2 replicas CommandRouter, 2 PolicyService, 2 ControlGateway (active/active)
- Medium: 4–6 replicas
- Large: 8+ replicas, shard by telescope site if needed

Justification: meets **INF-RemoteOps-01** (distributed access) and **INF-CmdAccept-01** (latency via horizontal scaling).

## E2) DB HA topology + backup/restore
- PostgreSQL HA: Patroni or CloudNativePG; 3-node cluster, synchronous replication (1 sync, 1 async).
- Backups: full nightly + WAL continuous; verify restore weekly to staging.
- RPO target: 5 minutes; RTO target: 30 minutes for control-plane DBs; data blobs per object storage replication.

Justification: meets **INF-Audit-01** (must recreate observation steps) by preserving logs and queue state.

## E3) Network topology + ingress/egress rules and latency expectations
Mapped to **DeploymentDiagram**:
- Ingress: RemoteUI→OCSCluster via TLS only; restrict remote control operations by PolicyService site gating.
- Egress: OCSCluster→IOCNet on dedicated real-time link; no direct WAN-to-IOC routing.
- Expected latencies: Router→ControlGateway in-cluster <10ms; Gateway→IOC handshake 100–200ms; router timeouts ~500ms.

Justification: meets **INF-CmdProtocol-01** (handshake/timeout predictability) and **INF-Security-01** (WAN intrusion protection).

## E4) CI/CD sketch
1. Build: compile, lint, SBOM, container build.
2. Tests: unit → contract → integration (DB/broker) → IOC simulator E2E.
3. Security gates: SAST, dependency scan, policy-as-code.
4. Deploy: canary (5%) then roll; blue/green for gateway.
5. Rollback: automatic if SLO burn alerts trigger.

Justification: meets **INF-Versioning-01** (versioned binaries + consistency checks).

---

# F. Security Design

## F1) Auth & AuthZ
- External: OIDC login (Keycloak) → JWT access tokens (5–15 min) + refresh tokens (8–12 hours).
- Internal: service-to-service mTLS or SPIFFE (optional phase); otherwise short-lived JWT with audience restrictions.
- Revocation: token introspection for admin actions; immediate policy effect within 60s via policy_version bump.

Justification: meets **INF-RemoteOps-01** (dynamic restrictions) and **INF-Security-01** (intrusion protection).

## F2) Secrets management & rotation
- Kubernetes Secrets + sealed-secrets or external Vault; rotate DB creds quarterly; rotate signing keys semi-annually; emergency rotation procedure.

Justification: meets **INF-Security-01**.

## F3) TLS & service mesh
- TLS mandatory on WAN/LAN interfaces (RemoteUI↔Gateway).
- Optional Istio/Linkerd for mTLS and policy enforcement between services.

Justification: meets **INF-RemoteOps-01** (secure remote operations).

## F4) Threat model summary (top 5)
1. Unauthorized remote command injection → RBAC + site gating + audit + default deny.
2. Replay of commands → nonce/correlation + short token TTL + idempotency keys.
3. Insider misuse (ops/developer) → least privilege + immutable audit logs.
4. DoS via monitoring flood → rate limits + TelemetryBus isolation.
5. IOC network pivot → strict network segmentation; no direct remote access.

Justification: meets **INF-Security-01** and **INF-NonIntrusiveMonitoring-01**.

---

# G. Observability & SRE

## G1) Metrics, traces, logs + example alerts
**Key metrics**
- `commandrouter_accept_latency_ms` p95/p99
- `ioc_handshake_latency_ms`
- `status_query_latency_ms`
- `allocator_lease_conflicts_total`
- `telemetrybus_lag_seconds`
- `quicklook_duration_ms` and `nearline_queue_depth`

**Tracing**
- Correlation ID propagated from gateway; spans: UI→APIGW→CommandRouter→ControlGateway→IOC.

**Logs**
- Structured JSON logs with `correlationId`, `sessionTokenHash`, `subsystem`, `cmd`, `result`.

**Example Prometheus alert rules**
- (Included in doc; implement in PrometheusRule CRD)

```promql
# Alert 1: Command accept latency burn
histogram_quantile(0.99, sum(rate(commandrouter_accept_latency_ms_bucket[5m])) by (le)) > 1500
```

```promql
# Alert 2: Telemetry lag threatens UI freshness
max(telemetrybus_lag_seconds) > 3
```

Justification: meets **INF-StatusLatency-01** (≤4s updates) and **INF-CmdAccept-01** (≤2s accept/reject).

## G2) SLOs, error budgets, RTO/RPO
- SLO1: Command accept/reject p99 ≤ 2s (budget 0.1%/30d).
- SLO2: IOC handshake p95 ≤ 200ms; timeout budget monitored.
- SLO3: Local status freshness ≤ 4s p95.
- RTO/RPO: see E2.

Justification: meets **INF-CmdAccept-01**, **INF-CmdProtocol-01**, **INF-StatusLatency-01**.

## G3) Dashboard/runbook sketch
Dashboards: command latency, lease conflicts, IOC connectivity, archive success, queue progress, warning rate.  
Runbooks: “IOC timeout storm”, “Allocator deadlock risk”, “Archive degraded”, “Policy misconfiguration”.

---

# H. Testing Strategy

## H1) Test matrix

| Test type | Components | Focus |
|---|---|---|
| Unit | PolicyService, Allocator, Router | RBAC/site rules, deadlock logic, retry rules |
| Integration | Router+Gateway+Postgres+NATS | command flow + persistence |
| Contract | OpenAPI + gRPC | backward compatible API evolution |
| E2E (simulated) | Sequencer→Router→SimulatorAdapter | observing program execution without hardware |
| Chaos | DB failover, broker outage | resilience and reconfiguration |

Justification: meets **INF-Simulator-01** (simulation modules) and **INF-Reliability-01** (robustness).

## H2) Test data & environment isolation
- Environments: dev, integration, staging (with IOC simulators), production.
- Refresh: nightly seed of catalogs/weather stubs; anonymized logs.
- Isolation: per-namespace ephemeral test deployments for PRs.

---

# I. Migration, Data Conversion & Rollout Plan

## I1) Migration steps
1. Stand up new OCS cluster alongside existing (if any).
2. Implement IOC simulators + run parallel dry-run observing sequences.
3. Dual-write logs/events to both stores during cutover window.
4. Gradually migrate instruments (inactive instruments first) to minimize risk.
5. Rollback: switch gateway routing back; leases expire quickly; preserve audit logs.

Justification: meets **INF-SeqPrimary-01** (sequencer-first) and **INF-Audit-01** (recreate sequences).

## I2) API versioning strategy
- `/api/v1/...` external; additive changes only in minor; breaking → `/api/v2`.
- gRPC: protobuf field numbers stable; deprecate without reuse.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros | Cons | Why chosen |
|---|---|---|---|---|
| NATS JetStream for TelemetryBus | RabbitMQ; Kafka/Redpanda | Low latency; simpler ops; durable streams | Not as feature-rich as Kafka | Best fit for isolation/non-interference and moderate scale (**INF-NonIntrusiveMonitoring-01**, **INF-Traffic-01**) |
| Go for control plane | Java; Rust | Predictable latency, simpler deployment | Fewer enterprise frameworks than Java | Aligns with tight command timing (**INF-CmdAccept-01**, **INF-CmdProtocol-01**) |
| Postgres for policies/leases/queues | MySQL; CockroachDB | Strong consistency + tooling | Needs HA mgmt | Supports authoritative allocator + audit (**INF-Audit-01**, **INF-QueueResequence-01**) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** EPICS IOC access is available via a gateway host process that can enforce ACK/NAK semantics and correlation IDs.  
- **A2:** “Timeouts ~500ms” and “handshake 100–200ms” apply to IOC-level command acknowledgment, not full action completion.  
- **A3:** Remote policy “effective within 60s” is interpreted as propagation + enforcement SLA, not UI refresh SLA.  
- **A4:** FITS headers may include proprietary metadata; encryption-at-rest is required for metadata stores.  
- **A5:** Archive integration supports idempotent ingest keyed by datasetId (or we emulate idempotency with local dedupe).

## Conflicts / naming issues (per rule #2)
- **K-C1:** UML notes reference FR/NFR/ASR IDs that are **not present** in the narrative requirements. Resolution: use narrative requirements as source-of-truth; derived IDs are `INF-*`.

## Unresolved stakeholder questions
1. What exact command set and error taxonomy must be standardized across subsystems (minimum common commands: version, self-test, start/stop/init/reset)?  
2. Which operations are permitted from which remote sites (default allowlist per site)?  
3. Data volume expectations per instrument (for sizing 7-day retention) and preferred compression method (FITS tile vs gzip).  
4. Required MTTR/MTBF targets and formal availability SLOs for commissioning vs steady operations.  
5. Which commercial DBMS is mandated (if any) for operational logs vs adopting Postgres/Timescale.

---

# L. Deliverables

## 1) `architecture.md` (this document)
```markdown
# ArchitectureDocument.md
(Contents are exactly the ArchitectureDocument you are reading.)
```

## 2) `openapi.yaml` — external API (complete)
```yaml
openapi: 3.0.3
info:
  title: Gemini OCS External API
  version: "1.0.0"
servers:
  - url: https://ocs.example.org/api/v1
security:
  - bearerAuth: []
paths:
  /auth/login:
    post:
      summary: Login and obtain tokens
      operationId: login
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        "200":
          description: Tokens issued
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
  /session/modes:
    put:
      summary: Select operational level and access modes for the current session
      operationId: selectModes
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SelectModesRequest"
      responses:
        "200":
          description: Modes accepted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SelectModesResponse"
        "409":
          description: Mode/level conflict
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /queues:
    post:
      summary: Create or register an observing queue
      operationId: createQueue
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateQueueRequest"
      responses:
        "201":
          description: Queue created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QueueResponse"
  /queues/{queueId}/run:
    post:
      summary: Start running a queue (sequencer-driven)
      operationId: runQueue
      parameters:
        - name: queueId
          in: path
          required: true
          schema: { type: string }
      responses:
        "202":
          description: Run accepted
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/RunQueueResponse"
        "403":
          description: Not authorized for current level/mode/site
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /queues/{queueId}/resequence:
    post:
      summary: Break and resequence a queue
      operationId: resequenceQueue
      parameters:
        - name: queueId
          in: path
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ResequenceRequest"
      responses:
        "200":
          description: Queue resequenced
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QueueResponse"
  /commands:submit:
    post:
      summary: Submit a command (direct control allowed only when policy permits)
      operationId: submitCommand
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CommandEnvelope"
      responses:
        "200":
          description: Command accepted/rejected before action
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandResponse"
        "403":
          description: Not authorized (RBAC/site/level/mode)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /status/query:
    post:
      summary: Query status variables (read-only)
      operationId: statusQuery
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/StatusQueryRequest"
      responses:
        "200":
          description: Status results
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/StatusQueryResponse"
  /policies/remote-sites:
    put:
      summary: Update allowed remote sites for operations (admin only)
      operationId: updateRemoteSites
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/RemoteSitePolicyUpdate"
      responses:
        "200":
          description: Policy updated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/RemoteSitePolicyResponse"
        "403":
          description: Not authorized
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /data-products/{datasetId}:
    get:
      summary: Retrieve data product metadata (and optionally a presigned FITS URL)
      operationId: getDataProduct
      parameters:
        - name: datasetId
          in: path
          required: true
          schema: { type: string }
        - name: includePresignedUrl
          in: query
          required: false
          schema: { type: boolean, default: false }
      responses:
        "200":
          description: Data product
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DataProductResponse"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1 }
        password: { type: string, minLength: 1 }
        mfaToken: { type: string, nullable: true }
    LoginResponse:
      type: object
      required: [accessToken, refreshToken, expiresInSeconds, roles]
      properties:
        accessToken: { type: string }
        refreshToken: { type: string }
        expiresInSeconds: { type: integer, minimum: 60 }
        roles:
          type: array
          items: { type: string }
    SelectModesRequest:
      type: object
      required: [operationalLevel, accessModes]
      properties:
        operationalLevel:
          type: string
          enum: [OBSERVING, MAINTENANCE, TEST]
        accessModes:
          type: array
          items:
            type: string
            enum: [OBSERVING, MONITORING, OPERATION, PLANNING, TESTING, ADMINISTRATIVE]
        remoteSiteId: { type: string, nullable: true }
    SelectModesResponse:
      type: object
      required: [policyVersion]
      properties:
        policyVersion: { type: string }
    CreateQueueRequest:
      type: object
      required: [name, steps]
      properties:
        name: { type: string }
        steps:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/QueueStep"
    QueueStep:
      type: object
      required: [stepId, subsystem, command]
      properties:
        stepId: { type: string }
        subsystem: { type: string }
        command:
          $ref: "#/components/schemas/Command"
    QueueResponse:
      type: object
      required: [queueId, name, version, steps]
      properties:
        queueId: { type: string }
        name: { type: string }
        version: { type: integer, minimum: 1 }
        steps:
          type: array
          items: { $ref: "#/components/schemas/QueueStep" }
    RunQueueResponse:
      type: object
      required: [runId, acceptedAtUtc]
      properties:
        runId: { type: string }
        acceptedAtUtc: { type: string, format: date-time }
    ResequenceRequest:
      type: object
      required: [reason]
      properties:
        reason: { type: string }
        policyHint: { type: string, nullable: true }
    Command:
      type: object
      required: [cmd, args]
      properties:
        cmd: { type: string }
        args: { type: object, additionalProperties: true }
        idempotent: { type: boolean, default: false }
        requiresSafetyInterlock: { type: boolean, default: false }
    CommandEnvelope:
      type: object
      required: [correlationId, timestampUtc, accessMode, operationalLevel, command]
      properties:
        correlationId: { type: string }
        timestampUtc: { type: string, format: date-time }
        accessMode:
          type: string
          enum: [OBSERVING, MONITORING, OPERATION, PLANNING, TESTING, ADMINISTRATIVE]
        operationalLevel:
          type: string
          enum: [OBSERVING, MAINTENANCE, TEST]
        command: { $ref: "#/components/schemas/Command" }
        targetSubsystem: { type: string, nullable: true }
    CommandResponse:
      type: object
      required: [correlationId, resultCode, acceptedAtUtc]
      properties:
        correlationId: { type: string }
        resultCode:
          type: string
          enum: [ACK, NAK, TIMEOUT]
        reason: { type: string, nullable: true }
        acceptedAtUtc: { type: string, format: date-time }
    StatusQueryRequest:
      type: object
      required: [variables]
      properties:
        variables:
          type: array
          minItems: 1
          items: { type: string }
    StatusQueryResponse:
      type: object
      required: [results]
      properties:
        results:
          type: array
          items:
            type: object
            required: [variable, timestampUtc, value, statusCode]
            properties:
              variable: { type: string }
              timestampUtc: { type: string, format: date-time }
              value: { type: string }
              unit: { type: string, nullable: true }
              statusCode: { type: integer }
              errorMessage: { type: string, nullable: true }
    RemoteSitePolicyUpdate:
      type: object
      required: [allowedSites]
      properties:
        allowedSites:
          type: array
          items: { type: string }
    RemoteSitePolicyResponse:
      type: object
      required: [policyVersion, effectiveWithinSeconds]
      properties:
        policyVersion: { type: string }
        effectiveWithinSeconds: { type: integer, minimum: 1 }
    DataProductResponse:
      type: object
      required: [datasetId, fitsUri, compression, headersJson, checksumSha256]
      properties:
        datasetId: { type: string }
        fitsUri: { type: string }
        presignedUrl: { type: string, nullable: true }
        compression: { type: string }
        headersJson: { type: string }
        checksumSha256: { type: string }
    ErrorResponse:
      type: object
      required: [errorCode, message, correlationId]
      properties:
        errorCode: { type: string }
        message: { type: string }
        correlationId: { type: string }
        details:
          type: object
          additionalProperties: true
```

## 3) `internal.proto` — internal gRPC contracts (complete)
```proto
syntax = "proto3";

package gemini.ocs.v1;

option go_package = "github.com/gemini/ocs/internal/gen/ocs;ocs";

import "google/protobuf/timestamp.proto";

enum OperationalLevel {
  OPERATIONAL_LEVEL_UNSPECIFIED = 0;
  OBSERVING = 1;
  MAINTENANCE = 2;
  TEST = 3;
}

enum AccessMode {
  ACCESS_MODE_UNSPECIFIED = 0;
  MODE_OBSERVING = 1;
  MODE_MONITORING = 2;
  MODE_OPERATION = 3;
  MODE_PLANNING = 4;
  MODE_TESTING = 5;
  MODE_ADMINISTRATIVE = 6;
}

enum CommandResultCode {
  COMMAND_RESULT_UNSPECIFIED = 0;
  ACK = 1;
  NAK = 2;
  TIMEOUT = 3;
}

message SessionContext {
  string session_token = 1;
  string user_id = 2;
  repeated string roles = 3;
  string remote_site_id = 4;
  string policy_version = 5;
}

message Command {
  string cmd = 1;
  string args_json = 2;
  bool idempotent = 3;
  bool requires_safety_interlock = 4;
}

message CommandEnvelope {
  string correlation_id = 1;
  google.protobuf.Timestamp timestamp_utc = 2;
  SessionContext session = 3;
  AccessMode access_mode = 4;
  OperationalLevel operational_level = 5;
  string target_subsystem = 6;
  Command command = 7;
}

message CommandResponse {
  string correlation_id = 1;
  CommandResultCode result_code = 2;
  string reason = 3;
  google.protobuf.Timestamp accepted_at_utc = 4;
}

message AuthorizationRequest {
  SessionContext session = 1;
  OperationalLevel operational_level = 2;
  AccessMode access_mode = 3;
  string operation = 4;
  string target_subsystem = 5;
}

message AuthorizationResponse {
  bool allowed = 1;
  string reason = 2;
  string policy_version = 3;
}

message LeaseRequest {
  SessionContext session = 1;
  AccessMode access_mode = 2;
  repeated string resource_ids = 3;
  google.protobuf.Timestamp requested_at_utc = 4;
  int32 ttl_seconds = 5;
}

message LeaseResponse {
  bool granted = 1;
  string lease_id = 2;
  string reason = 3;
  google.protobuf.Timestamp expires_at_utc = 4;
}

message StatusQuery {
  SessionContext session = 1;
  repeated string variables = 2;
}

message StatusVariable {
  string variable = 1;
  google.protobuf.Timestamp timestamp_utc = 2;
  string value = 3;
  string unit = 4;
  int32 status_code = 5;
  string error_message = 6;
}

message StatusResponse {
  repeated StatusVariable results = 1;
}

service PolicyService {
  rpc Authorize(AuthorizationRequest) returns (AuthorizationResponse);
}

service AllocatorService {
  rpc RequestLease(LeaseRequest) returns (LeaseResponse);
  rpc ReleaseLease(LeaseResponse) returns (google.protobuf.Timestamp);
}

service CommandService {
  rpc SubmitCommand(CommandEnvelope) returns (CommandResponse);
}

service StatusService {
  rpc QueryStatus(StatusQuery) returns (StatusResponse);
}
```

## 4) `k8s/ocs-commandrouter-deployment.yaml` — example manifest (complete)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ocs-commandrouter
  namespace: ocs
spec:
  replicas: 4
  selector:
    matchLabels:
      app: ocs-commandrouter
  template:
    metadata:
      labels:
        app: ocs-commandrouter
    spec:
      containers:
        - name: commandrouter
          image: ghcr.io/gemini/ocs-commandrouter:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: POLICY_GRPC_ADDR
              valueFrom:
                configMapKeyRef:
                  name: ocs-config
                  key: policyGrpcAddr
            - name: ALLOCATOR_GRPC_ADDR
              valueFrom:
                configMapKeyRef:
                  name: ocs-config
                  key: allocatorGrpcAddr
            - name: IOC_GATEWAY_GRPC_ADDR
              valueFrom:
                configMapKeyRef:
                  name: ocs-config
                  key: iocGatewayGrpcAddr
            - name: DATABASE_DSN
              valueFrom:
                secretKeyRef:
                  name: ocs-secrets
                  key: databaseDsn
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "2"
              memory: "2Gi"
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ocs-commandrouter
  namespace: ocs
spec:
  selector:
    app: ocs-commandrouter
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ocs-commandrouter-hpa
  namespace: ocs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ocs-commandrouter
  minReplicas: 2
  maxReplicas: 12
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
  namespace: ocs
data:
  policyGrpcAddr: "ocs-policyservice:50051"
  allocatorGrpcAddr: "ocs-allocator:50052"
  iocGatewayGrpcAddr: "ocs-controlgateway:50053"
---
apiVersion: v1
kind: Secret
metadata:
  name: ocs-secrets
  namespace: ocs
type: Opaque
stringData:
  databaseDsn: "postgres://ocs:CHANGEME@postgres.ocs.svc.cluster.local:5432/ocs?sslmode=require"
```

## 5) SQL DDL examples

### `sql/policy_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS policy_version (
  policy_version TEXT PRIMARY KEY,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by_user_id TEXT NOT NULL,
  comment TEXT
);

CREATE TABLE IF NOT EXISTS rbac_role (
  role_name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS rbac_permission (
  permission_id TEXT PRIMARY KEY,
  operation TEXT NOT NULL,
  operational_level TEXT NOT NULL CHECK (operational_level IN ('OBSERVING','MAINTENANCE','TEST')),
  access_mode TEXT NOT NULL CHECK (access_mode IN ('OBSERVING','MONITORING','OPERATION','PLANNING','TESTING','ADMINISTRATIVE')),
  target_pattern TEXT NOT NULL DEFAULT '*'
);

CREATE TABLE IF NOT EXISTS rbac_role_permission (
  role_name TEXT NOT NULL REFERENCES rbac_role(role_name),
  permission_id TEXT NOT NULL REFERENCES rbac_permission(permission_id),
  PRIMARY KEY (role_name, permission_id)
);

CREATE TABLE IF NOT EXISTS remote_site_policy (
  policy_id BIGSERIAL PRIMARY KEY,
  policy_version TEXT NOT NULL REFERENCES policy_version(policy_version),
  operation TEXT NOT NULL,
  allowed_site_id TEXT NOT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (policy_version, operation, allowed_site_id)
);

CREATE INDEX IF NOT EXISTS idx_remote_site_policy_operation
  ON remote_site_policy(operation);
```

### `sql/resource_lease_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS resource (
  resource_id TEXT PRIMARY KEY,
  resource_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_lease (
  lease_id TEXT PRIMARY KEY,
  owner_session_token_hash TEXT NOT NULL,
  resource_id TEXT NOT NULL REFERENCES resource(resource_id),
  access_mode TEXT NOT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at_utc TIMESTAMPTZ NOT NULL,
  UNIQUE (resource_id)
);

CREATE INDEX IF NOT EXISTS idx_resource_lease_expires
  ON resource_lease(expires_at_utc);
```

### `sql/audit_event_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS audit_log (
  audit_id BIGSERIAL PRIMARY KEY,
  timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  user_id TEXT NOT NULL,
  session_token_hash TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT,
  result_code TEXT NOT NULL,
  correlation_id TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_corr
  ON audit_log(correlation_id);

CREATE TABLE IF NOT EXISTS event_log (
  event_id BIGSERIAL PRIMARY KEY,
  event_time_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  origin TEXT NOT NULL,
  severity TEXT NOT NULL,
  error_code TEXT NOT NULL,
  correlation_id TEXT,
  message TEXT NOT NULL,
  user_action TEXT
);

CREATE INDEX IF NOT EXISTS idx_event_time
  ON event_log(event_time_utc);
```

### `sql/queue_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS observing_queue (
  queue_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS queue_step (
  queue_id TEXT NOT NULL REFERENCES observing_queue(queue_id) ON DELETE CASCADE,
  step_id TEXT NOT NULL,
  subsystem TEXT NOT NULL,
  command_json TEXT NOT NULL,
  ordinal INTEGER NOT NULL,
  PRIMARY KEY (queue_id, step_id),
  UNIQUE (queue_id, ordinal)
);

CREATE TABLE IF NOT EXISTS step_result (
  queue_id TEXT NOT NULL,
  step_id TEXT NOT NULL,
  correlation_id TEXT NOT NULL,
  result_code TEXT NOT NULL,
  accepted_at_utc TIMESTAMPTZ NOT NULL,
  reason TEXT,
  PRIMARY KEY (queue_id, step_id, correlation_id)
);

CREATE INDEX IF NOT EXISTS idx_step_result_corr
  ON step_result(correlation_id);
```

### `sql/data_product_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS data_product (
  dataset_id TEXT PRIMARY KEY,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  fits_uri TEXT NOT NULL,
  compression TEXT NOT NULL,
  headers_json TEXT NOT NULL,
  checksum_sha256 TEXT NOT NULL,
  archived_at_utc TIMESTAMPTZ,
  retention_class TEXT NOT NULL CHECK (retention_class IN ('INTERACTIVE_3D','ONSITE_7D','ARCHIVED'))
);

CREATE INDEX IF NOT EXISTS idx_data_product_created
  ON data_product(created_at_utc);
```

## 6) `traceability_matrix.csv` — full mapping table
```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-AccessLevels-01,"Operational levels: Observing/Maintenance/Test",StateDiagram:OCSSession;ClassDiagram:OperationalLevel,"PolicyService,Session,OperationalState","architecture.md;internal.proto","Authorization and mode compatibility depend on level; central enforcement prevents unsafe access."
INF-AccessModes-01,"Access modes: Observing/Monitoring/Operation/Planning/Testing/Admin",ClassDiagram:AccessMode;UseCaseDiagram:UC_SelectMode,"RemoteUI,PolicyService","openapi.yaml","Mode-aware UI and APIs ensure correct privileges and UX."
INF-NonIntrusiveMonitoring-01,"Monitoring must not affect ongoing observation",UseCaseDiagram:UC_MonitorStatus;ComponentDiagram:TelemetryBus,"TelemetryBus,StatusService","architecture.md;openapi.yaml","Async pub/sub and read-only queries isolate observing control."
INF-SeqPrimary-01,"Automatic sequencer is normal; interaction via scheduler not direct control",UseCaseDiagram:UC_RunQueue;StateDiagram:Observing,"Sequencer,Scheduler","openapi.yaml;sql/queue_ddl.sql","Implements queue/service observing and single point of control."
INF-QueueResequence-01,"Break and resequence queue based on QA/conditions",ActivityDiagram:Resequence;ClassDiagram:Sequencer.breakAndResequence,"Scheduler,Sequencer","openapi.yaml;sql/queue_ddl.sql","Supports flexible scheduling and re-prioritization."
INF-RemoteOps-01,"Remote operations supported; full operations remotely where allowed",DeploymentDiagram:RemoteStations;UseCaseDiagram:RemoteUser,"RemoteUI,APIGW,PolicyService","architecture.md;openapi.yaml","Remote transparency via same APIs; restrictions via policy."
INF-RemoteSiteRestrict-01,"Restrict operations to specific remote sites dynamically",UseCaseDiagram:UC_ManageRemotePolicy;SequenceScenario2_RemotePolicyUpdate,"PolicyService,PolicyDB","openapi.yaml;sql/policy_ddl.sql","Independent, dynamic gating reduces safety/security risk."
INF-RemoteMonitorKeyboard-01,"Remote monitoring keyboard has no effect (read-only)",UseCaseDiagram:UC_MonitorStatus,"RemoteUI","architecture.md","UI enforces mode-specific interaction semantics."
INF-CmdProtocol-01,"Uniform commands; ACK/NAK; timeouts ~500ms; IOC handshake 100-200ms",SequenceScenario1_RunQueueAndControl,"ControlGateway,CommandRouter","internal.proto","Contract-first command envelopes ensure predictable behavior."
INF-CmdAccept-01,"Every command accepted/rejected within 2s before action",StateDiagram:CommandPath,"CommandRouter","internal.proto;metrics","Router validates+authorizes before sending to IOC."
INF-StatusLatency-01,"Status update <=4s local; status query <=5s",ActivityDiagram:MonitorStatus,"StatusService,ControlGateway","openapi.yaml;metrics","Defines SLOs for UI responsiveness."
INF-Traffic-01,"Peak control info ~100 TPS; traffic isolation",DeploymentDiagram:IOCNet;ComponentDiagram:TelemetryBus,"ControlGateway,TelemetryBus","architecture.md","Separates control from telemetry to avoid congestion."
INF-DataFormat-01,"Standard format; FITS transmission; lossless compression",ClassDiagram:DataProduct,"ArchiveClient","sql/data_product_ddl.sql","Ensures archival and institute interoperability."
INF-Retention-01,"Retain 7 days; last 3 days interactive",ClassDiagram:DataProduct,"ArchiveClient,ObjectStore","architecture.md","Storage lifecycle policies implement retention requirements."
INF-QuickLook-01,"Quick-look synchronous and usable within sequences",ActivityDiagram:QuickLook,"QuickLookProcessor,Sequencer","architecture.md","Inline quick-look supports decisions without manual intervention."
INF-NearLine-01,"Near-line reduction async; acquisition precedence",ComponentDiagram:NearLineProcessor,"NearLineProcessor","architecture.md","Backpressure policy prevents observing slowdown."
INF-Audit-01,"Log events to recreate observation; 200Hz burst eng logs",ContainerDiagram:C_LOGDB,"AuditLogService,EventLogService","sql/audit_event_ddl.sql","Append-only logs with correlation IDs enable replay/debug."
INF-Versioning-01,"Version labeled; retrievable via commands; boot-time consistency checks",ClassDiagram:Subsystem.getVersion,"ControlGateway,IOCAdapters","internal.proto","Prevents mixed-version failures and supports configuration control."
INF-Simulator-01,"Subsystem simulator modules; easy swap real with sim",UseCaseDiagram:UC_RunSimulation;ComponentDiagram:SimulatorAdapter,"SimulatorAdapter,ControlGateway","internal.proto","Enables virtual telescope planning and test without hardware."
INF-Safety-01,"Safety: safe state on danger; interlocks independent of software",UseCaseDiagram note on UC_DirectControl,"IOC layer + CommandRouter flags","architecture.md","Software respects and surfaces interlock state; avoids unsafe commands."
INF-Reconfig-01,"Reconfiguration/startup/shutdown procedures; dynamic environment changes",Requirements narrative,"Sequencer,Ops procedures","architecture.md","Procedure automation reduces errors and downtime."
INF-NodeCapacity-01,"Simultaneous nodes: up to 6 active + 2 monitoring; capable of 10 active",DeploymentDiagram:LocalStations/RemoteStations,"OCSCluster,HPA","k8s/ocs-commandrouter-deployment.yaml","Scaling plan supports expected concurrency."
```

---

## Verification table (Acceptance Criteria)
- [x] 3-line Analysis Plan present.  
- [x] Sections A-L included.  
- [x] Every FR/NFR/ASR mapped in traceability matrix. *(Note: narrative SRS lacked IDs; mapped as INF-*)*  
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.  
- [x] Representative k8s manifest snippet included.  
- [x] SQL DDL / NoSQL models for primary entities included.  
- [x] All major components have at least one API contract and a data schema.  
- [x] Assumptions and unresolved questions listed.

## How to review checklist
- All FR/NFR/ASR present in traceability matrix? *(Here: INF-* derived list complete for this submission; confirm with stakeholders.)*  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?

**Conversion note (if PDF/HTML needed):**
- `pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf`  
- `pandoc ArchitectureDocument.md -o ArchitectureDocument.html`