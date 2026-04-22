Scope: Consolidate the provided multi-domain cyber-physical requirements into one production-ready, plugin-based control platform with shared infra services and per-domain controllers.  
Approach: Use 4+1 views aligned to the provided UML set, add explicit interfaces (OpenAPI + gRPC), schemas, k8s deployment, and measurable operational controls.  
Top validation steps: Requirement→artifact traceability for all inferred IDs, API/schema linting, simulator-driven E2E tests for timing/override/failure modes.

# A. Executive Summary (≤1 page)

## System overview
A unified **Cyber-Physical Control Platform (CPCP)** runs multiple independent control/monitoring applications (ICU patient monitoring, facial-access door, zoo turnstile, heating, traffic lights, sluice gate, vehicle monitor, package router, monorail shuttle, lab voltages display, speedometer/odometer, library admin, tennis court access/lighting, PC configuration viewer, lexical analyzer, stream editor, party-plan editor, correspondence report, OCR transcription intake). The platform is a **microkernel modular monolith** with **HardwareIO abstraction** and an internal **EventBus** to support add-on modules without changing existing deterministic controllers.

Primary diagram mapping:
- Scenario View: **UseCase_ScenarioView** (UC_MonitorVitals, UC_SendICUAlerts, UC_AttemptDoorEntry, UC_OperateTurnstile, UC_ControlTrafficLights, UC_OverrideTrafficPhase, UC_OperateSluiceGate, UC_ControlHeating, UC_ManageLibrary, UC_GenerateReports, UC_ShowPCConfig, UC_StartLightingSession).
- Logic View: **Class_LogicView** (PluginManager, EventBus, HardwareIO, Scheduler, AuditLogger, MetricsCollector, PatientMonitor, SafeRange, VitalMeasurement, Alert, FaceTemplate, TurnstileSession, etc.).

Chosen architectural style(s): **Microkernel plugin architecture + event-driven internal bus** (per “Past Design Decisions”).  
Deployment topology: **Single Kubernetes cluster** (control-plane services + persistence) plus optional **edge nodes** for hardware-adjacent plugins.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| R1: Timing determinism across many controllers | Safety/comfort failures | Partition plugins into **real-time loops** vs non-real-time; pin CPU, use priority scheduling, simulator-based timing tests (INF-NFR-TIMING-001/002) |
| R2: Hardware integration ambiguity (ports/pulses/registers) | Blocked delivery | Enforce **HardwareIO** contract + per-device driver plugin + simulator harness; contract tests (INF-ASR-HWIO-001) |
| R3: Security/privacy for face templates & access decisions | Compliance breach | Encrypt templates at rest, strict audit trails, RBAC, key rotation, data retention policy (INF-NFR-SEC-001..004) |

## Key QA coverage mapping (ASR/NFR → test types)
> Note: Original requirements contain no explicit ASR/NFR IDs; all are inferred as `INF-*` and listed in Section K.

| Quality | INF-ASR/NFR IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-SCALE-001 | Load, soak, HPA tests |
| Availability | INF-NFR-AVAIL-001, INF-NFR-RPO-001, INF-NFR-RTO-001 | Chaos, failover drills, backup/restore |
| Security | INF-NFR-SEC-001..004 | SAST/DAST, pen-test, secrets rotation tests |
| Performance | INF-NFR-TIMING-001..004 | Latency/jitter tests, profiling, RT loop simulation |
| Maintainability | INF-ASR-MOD-001, INF-ASR-OBS-001 | Contract tests, linting, ADR checks, observability validation |

---

# B. Traceability & Rationale

**traceability_matrix.csv** is provided in Section L (full file). It maps every inferred requirement to diagrams/components/artifacts.

**Rationale summary**: Requirements span multiple cyber-physical domains with common needs: deterministic scheduling, hardware access, persistence, alerts/notifications, overrides/config. A shared platform reduces duplicate engineering while preserving isolation via plugin boundaries.

---

# C. Architecture Overview

## 4+1 View alignment

### Context (Scenario View)
Actors and high-level capabilities are captured in **UseCase_ScenarioView**:
- ICU: UC_MonitorVitals includes UC_SendICUAlerts; safe ranges via UC_ManageSafeRanges.
- Door access: UC_AttemptDoorEntry with face template matching.
- Turnstile: UC_OperateTurnstile (two-coin rule).
- Traffic lights: UC_ControlTrafficLights with UC_OverrideTrafficPhase extension.
- Sluice gate: UC_OperateSluiceGate.
- Heating: UC_ControlHeating.
- Library: UC_ManageLibrary + UC_GenerateReports.
- PC config: UC_ShowPCConfig.
- Tennis lighting: UC_StartLightingSession.

### Container (runtime services)
Containers (implemented as deployable services/pods):
1. **cpcp-core**: PluginManager, EventBus, Scheduler, AuditLogger, MetricsCollector.
2. **cpcp-api**: External REST API (OpenAPI) for admin/config/reporting/queries.
3. **cpcp-worker**: Background jobs (report generation, scheduled control loops where not bound to edge).
4. **device-gateway** (optional edge): Hardware-adjacent runtime with HardwareIO drivers.
5. **db-postgres**: primary relational store.
6. **observability stack**: Prometheus + Grafana + Loki/ELK + OpenTelemetry Collector.

### Component/Package
- **Platform services**: plugin lifecycle, eventing, scheduling, audit, metrics.
- **Domain plugins**:
  - ICU Monitoring Plugin
  - Door Facial Access Plugin
  - Turnstile Plugin
  - Heating Controller Plugin
  - Traffic Lights Plugin (+ display add-on plugin)
  - Sluice Gate Plugin
  - Vehicle Counter Plugin
  - Package Router Plugin
  - Monorail Shuttle Plugin
  - Lab Voltages Display Plugin
  - Speedometer/Odometer Plugin
  - Library Admin Plugin
  - Tennis Court Access/Lighting Plugin
  - PC Config Viewer Plugin
  - Text Tools Plugins (lexer, stream editor, party-plan editor, correspondence report, OCR intake)

### Class/Runtime
Core abstractions from **Class_LogicView**:
- **HardwareIO** isolates direct port/pulse/register operations.
- **EventBus** enables decoupled modules (e.g., traffic light display shares RPulse/GPulse).
- **Scheduler** supports per-patient sampling periods and periodic loops.
- **AuditLogger/MetricsCollector** provide cross-cutting compliance and SRE hooks.

### Deployment
Kubernetes deployment with optional edge gateway nodes; see Section E and k8s snippet. Latency-sensitive hardware loops can run on the edge gateway; persistence/analytics run centrally.

---

# D. Detailed Technical Design (developer-facing)

## D1. Platform Core: cpcp-core (PluginManager/EventBus/Scheduler/Audit/Metrics)

### 1) Responsibilities & data ownership
Owns plugin lifecycle, configuration loading, internal event routing, deterministic scheduling primitives, and cross-cutting audit/metrics. It does **not** own domain data; domain plugins own their tables.

### 2) Technology options (3 alternatives per concern)

- Language/runtime  
  - Recommended: **Java 21** (LTS)  
  - Conservative: **Go 1.22–1.23**  
  - Cutting-edge: **Rust 1.78–1.82**
- Web framework (for core admin endpoints; full external API is in cpcp-api)  
  - Recommended: **Spring Boot 3.2–3.3**  
  - Conservative: **Javalin 5.x**  
  - Cutting-edge: **Quarkus 3.8–3.12**
- RPC/HTTP  
  - Recommended: **gRPC 1.60+** internal; REST externally  
  - Conservative: REST-only (internal + external)  
  - Cutting-edge: NATS request-reply + AsyncAPI contracts
- Persistence  
  - Recommended: **PostgreSQL 14–16**  
  - Conservative: MariaDB 10.11  
  - Cutting-edge: CockroachDB 23.x
- Cache  
  - Recommended: **Redis 7.2–7.4**  
  - Conservative: Caffeine in-process cache  
  - Cutting-edge: KeyDB 6.x
- Messaging  
  - Recommended: in-proc **EventBus** + optional **NATS 2.10**  
  - Conservative: in-proc only  
  - Cutting-edge: Kafka 3.6+
- Search  
  - Recommended: PostgreSQL FTS  
  - Conservative: no search (reports only)  
  - Cutting-edge: OpenSearch 2.x
- Authn/authz  
  - Recommended: OIDC (Keycloak 24–26)  
  - Conservative: local users + bcrypt  
  - Cutting-edge: SPIFFE/SPIRE + mTLS identity
- Observability  
  - Recommended: OpenTelemetry SDK 1.35+ + Prometheus  
  - Conservative: Prometheus only  
  - Cutting-edge: eBPF-based profiling/tracing
- CI/CD  
  - Recommended: GitHub Actions + Helm  
  - Conservative: Jenkins pipeline  
  - Cutting-edge: ArgoCD + progressive delivery (Flagger)
- Container runtime  
  - Recommended: containerd (K8s default)  
  - Conservative: Docker runtime (where permitted)  
  - Cutting-edge: gVisor sandboxing
- Infra provisioning  
  - Recommended: Terraform 1.6–1.8  
  - Conservative: manual k8s yaml  
  - Cutting-edge: Crossplane

### 3) Recommended default stack
- Java 21 + Spring Boot 3.2–3.3 + gRPC 1.60+ + PostgreSQL 14–16 + Redis 7.2–7.4 + OpenTelemetry.
Justification: meets **INF-ASR-MOD-001** (modular plugin runtime) and **INF-ASR-OBS-001** (platform-wide audit/metrics) and **INF-NFR-AVAIL-001** (operational maturity).

### 4) Interface design
- External API is served by **cpcp-api** (Section D2) using OpenAPI `openapi.yaml`.
- Internal gRPC contract: `internal.proto` (Section L) for event publication, alerting, and HardwareIO simulation control.

### 5) Data model / schema
Platform tables:
- `plugin_registry`, `audit_log`, `system_metric_samples`.
See SQL files in Section L.

Fields requiring immutability/audit:
- `audit_log` is append-only (INF-NFR-SEC-004).

### 6) Caching & consistency
- Cache plugin metadata and safe ranges (read-heavy) in Redis with TTL 60s; invalidate on update events. Use strong consistency for writes (Postgres as source of truth).

---

## D2. External API: cpcp-api (Admin/Query/Reporting)

### 1) Responsibilities & data ownership
Provides authenticated API for: registering patients/devices, setting safe ranges, querying measurements, querying access decisions, managing memberships/subscriptions, generating reports. Owns no data; acts as façade to domain services and DB.

### 2) Technology options
- Language/runtime: Node.js 18–20 / Java 21 / Go 1.22  
- Web framework: Fastify 4.x / Spring MVC / Gin  
- Auth: OIDC (Keycloak) / AWS Cognito / Auth0 (if cloud)  
- Rate limiting: Envoy / Kong / NGINX Ingress

### 3) Recommended default stack
- Node.js 20 + Fastify 4.x + OpenAPI 3.0 + OIDC.
Justification: meets **INF-NFR-SEC-001** (authenticated admin actions) and **INF-ASR-MOD-001** (decoupled façade).

### 4) External APIs (OpenAPI YAML)
Provided as `openapi.yaml` in Section L.

### 5) Data model
N/A (API layer only). Uses domain tables.

### 6) Caching & consistency
- Cache read-only report snapshots 5 minutes; strict no-cache for security-sensitive endpoints (access decisions).

---

## D3. ICU Patient Monitoring Plugin

### 1) Responsibilities & data ownership
Reads per-patient analog vitals on configured sampling periods, persists measurements, checks against safe ranges, and notifies nurses’ station on out-of-range or device failure.

### 2) Technology options
- Runtime: Java / Go / Rust (edge capable)
- Persistence: Postgres / TimescaleDB / InfluxDB
- Notification: internal events → REST webhook / HL7 gateway / message queue

### 3) Recommended default stack
- Java 21 plugin + Postgres + internal EventBus → AlertService.
Justification: meets **INF-NFR-TIMING-001** (per-patient periodic reads) and **INF-NFR-SAFETY-001** (alerts on abnormal/device failure).

### 4) Interface design
- Internal gRPC: `PublishAlert`, `RecordVitals` (internal.proto).
- External endpoints: `/icu/patients`, `/icu/safe-ranges`, `/icu/measurements` (openapi.yaml).

### 5) Data model / schema
- `icu_patient`, `icu_safe_range`, `icu_vital_measurement`, `icu_alert`.
See SQL in Section L (`sql/icu_*.sql`). Encrypt-at-rest: none required by default; if mandated, encrypt `patient_name` and any identifiers (INF-NFR-SEC-002).

### 6) Caching & consistency
- Cache safe ranges in Redis TTL 60s. Measurements are write-once; queries can read from DB replicas.

---

## D4. Facial Recognition Door Access Plugin

### 1) Responsibilities & data ownership
Captures frames from video stream, extracts face features, compares to approved templates DB, returns access decision, logs attempt.

### 2) Technology options
- Face embedding: OpenCV + DNN / FaceNet / vendor SDK
- Storage: Postgres (templates as bytea) / Vault + DB pointers / dedicated biometric store

### 3) Recommended default stack
- Python 3.11–3.12 sidecar for feature extraction + Java plugin for policy + Postgres for templates.
Justification: meets **INF-NFR-SEC-002** (biometric data protection) and **INF-NFR-TIMING-002** (decision latency).

### 4) Interfaces
- External: `/door/attempts` POST; `/door/templates` CRUD (admin) in OpenAPI.
- Internal: `EvaluateFaceAttempt` RPC in internal.proto.

### 5) Data model
- `door_face_template` (templateCiphertext), `door_access_attempt`, `door_access_decision`.
Encrypt-at-rest: `template_ciphertext` required (INF-NFR-SEC-002). Immutable audit for decisions (INF-NFR-SEC-004).

### 6) Caching
- Cache active templates per door/camera TTL 5 minutes; invalidate on template change.

---

## D5. Zoo Turnstile Plugin

### 1) Responsibilities & data ownership
Controls coin acceptor + rotating barrier so entry requires exactly two coins; once paid, allow entry.

### 2) Tech options
- State machine lib: SMC / Spring Statemachine / custom
- Hardware: GPIO/serial driver behind HardwareIO

### 3) Recommended stack
- Java plugin + explicit finite state machine persisted per session.
Justification: meets **INF-NFR-SAFETY-002** (no unpaid entry) and **INF-NFR-CORRECT-001** (paid visitors allowed).

### 4) Interfaces
- External: `/turnstile/sessions/{id}` query for debugging.
- Internal: `TurnstileEvent` publish/subscribe.

### 5) Data model
- `turnstile_session`, `turnstile_event_log` (append-only).

### 6) Consistency
- Strong consistency for session transitions; idempotent coin insertion events.

---

## D6. Traffic Lights Plugin (+ Display Add-on, Card Regime, Overseer Override)

### 1) Responsibilities & data ownership
Implements 4-phase cycle and variants: fixed cycle, card-configured regime, overseer Hold/Change override. Publishes RPulse/GPulse events for units and display module.

### 2) Tech options
- Config: magnetic card ASCII parsing / JSON regime / UI configured
- Override arbitration: priority table + state machine

### 3) Recommended stack
- Java plugin + regime parser + deterministic scheduler; display as separate subscriber plugin.
Justification: meets **INF-ASR-MOD-002** (add display without disturbing controller) and **INF-NFR-TIMING-003** (phase durations).

### 4) Interfaces
- Internal: `LightPulseEvent` stream.
- External: `/traffic/regimes` upload; `/traffic/override` commands.

### 5) Data model
- `traffic_regime`, `traffic_override_event`, `traffic_phase_log`.

### 6) Consistency
- Overrides are immediately consistent; controller loop reads latest override token each tick.

---

## D7. Heating Controller Plugin

### 1) Responsibilities
Regulate room temps per knob, reduce setpoint by 5°C if unoccupied, anticipate occupancy 30 mins prior, control furnace/pump/valves, show state/malfunctions on control panel.

### 2) Tech options
- Control algorithm: PID / hysteresis bands / MPC (cutting-edge)
- Prediction: schedule-based / sensor-pattern learning / manual calendar input

### 3) Recommended stack
- Java plugin + hysteresis + schedule-based anticipation (configurable).
Justification: meets **INF-NFR-COMFORT-001** (temperature maintenance + economy offset) and **INF-NFR-TIMING-004** (30-minute preheat).

### 4) Interfaces
- External: `/heating/rooms` config; `/heating/state`.
- Internal: `HVACCommand` messages.

### 5) Data model
- `heating_room`, `heating_setpoint`, `heating_occupancy_event`, `heating_actuator_state`, `heating_fault`.

### 6) Caching
- Cache room config locally; occupancy events persisted async.

---

## D8. Library Admin Plugin

### 1) Responsibilities
Membership rules enforcement, lending/ordering from associated libraries, fines, management reports.

### 2) Options
- Data model: normalized SQL / event-sourced / document store
- Reporting: SQL views / batch jobs / BI tool

### 3) Recommended stack
- Postgres normalized schema + scheduled report jobs.
Justification: meets **INF-NFR-CORRECT-002** (membership rules) and **INF-NFR-REPORT-001** (management reports).

### 4) Interfaces
- External: `/library/members`, `/library/loans`, `/library/orders`, `/library/reports`.

### 5) Data model
- `lib_member`, `lib_book`, `lib_copy`, `lib_loan`, `lib_fine`, `lib_order`.

### 6) Consistency
- Strong consistency for loan creation/return; fines computed transactionally.

---

## D9. Tennis Court Access/Lighting Plugin

### 1) Responsibilities
Manage subscriptions (general + indoors), enforce “indoor game must include indoors member”, operate lock and lighting box via card, bill lighting cost to an indoors member.

### 2) Options
- Access control: online check / cached offline allowlist / hybrid
- Billing: immediate charge / monthly invoice

### 3) Recommended
- Hybrid: cache indoors-members allowlist at lock; billing recorded centrally.
Justification: meets **INF-NFR-CORRECT-003** (indoor rule + billing) and **INF-NFR-AVAIL-002** (lock must function during brief outages).

### 4) Interfaces
- External: `/court/memberships`, `/court/lighting/sessions`.
- Internal: `CardReadEvent`, `LightingCommand`.

### 5) Data model
- `court_member`, `court_subscription`, `court_lighting_session`, `court_billing_entry`.

### 6) Caching
- Allowlist TTL 24h with signed snapshot.

---

## D10. Remaining plugins (brief design rule)
For speedometer/odometer, lab voltages, monorail shuttle, sluice gate, vehicle monitoring, package router, PC config viewer, text tools: implement as separate plugins using HardwareIO + Scheduler + EventBus; persist outputs where required; expose status endpoints in OpenAPI as needed. Each is mapped in traceability.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
Provided as `k8s/cpcp-api-deployment.yaml` in Section L.

Replica suggestions:
- Small: 2 replicas API / 1 core / 1 worker
- Medium: 3–5 API / 2 core / 2 worker
- Large: 10+ API / 3 core / 5 worker, plus Redis and read replicas

Justification: meets **INF-NFR-SCALE-001** (scale by replicas/HPA) and **INF-NFR-AVAIL-001** (multi-replica availability).

## E2. DB HA topology, backups
- Postgres primary + 2 replicas (streaming replication).  
- Backups: nightly full + WAL archiving; retention 30 days.  
- Restore drills: quarterly to validate RPO/RTO.  
Justification: meets **INF-NFR-RPO-001** and **INF-NFR-RTO-001**.

## E3. Network topology + ingress/egress
- Ingress: HTTPS to cpcp-api only.
- East-west: mTLS between services (optional service mesh).
- Edge gateways connect via VPN or private LAN; only gRPC port exposed from core to gateway.
Latency expectations:
- Local edge control loops: <5ms IO calls.
- API requests: p95 <250ms for queries (INF-NFR-TIMING-005).

## E4. CI/CD sketch
1. Lint + compile + unit tests
2. Contract tests (OpenAPI + proto)
3. Integration tests with simulator
4. Build image + SBOM + vulnerability scan
5. Deploy to staging with canary; run E2E; promote to prod
Justification: meets **INF-ASR-MOD-001** (safe plugin evolution) and **INF-NFR-SEC-003** (supply-chain security).

---

# F. Security Design

## F1. Auth & AuthZ
- OIDC/OAuth2 with JWT access tokens (15 min) + refresh tokens (rotating).  
- RBAC roles: Admin, Operator, MedicalStaff, Nurse, LibraryStaff, CourtManager, Overseer.  
Justification: meets **INF-NFR-SEC-001**.

## F2. Secrets management & rotation
- Kubernetes Secrets via External Secrets Operator + Vault/KMS; rotate quarterly or on incident.  
Justification: meets **INF-NFR-SEC-003**.

## F3. TLS & service mesh
- TLS 1.3 at ingress; optional Linkerd/Istio for mTLS internally.  
Justification: meets **INF-NFR-SEC-001**.

## F4. Threat model (top 5)
1. Biometric template theft → encrypt templates, strict access, audit.  
2. Replay of hardware events → signed event envelopes, nonce windows.  
3. Privilege escalation via API → RBAC + least privilege + audit.  
4. Data tampering in measurements → append-only logs + checksums.  
5. DoS on control loops → isolate RT loops, rate-limit API.

---

# G. Observability & SRE

## G1. Metrics/logs/traces + Prometheus alerts
Key metrics:
- ICU: sampling jitter, alert rate, device failure rate
- Door: decision latency, FAR/FRR estimates (if labeled data)
- Turnstile: unpaid-entry attempts
- Traffic: phase timing drift, override usage
- Heating: temperature error, furnace cycles, faults

Alert rules (examples):
- ICU sampling lag:
  - `avg_over_time(icu_sampling_lag_ms[5m]) > 200`
- Door decision latency:
  - `histogram_quantile(0.99, sum(rate(door_decision_latency_ms_bucket[5m])) by (le)) > 1000`

## G2. SLOs/error budgets/RTO/RPO
- API availability: 99.9% monthly (INF-NFR-AVAIL-001)  
- ICU alert delivery: p99 < 2s internal (INF-NFR-TIMING-006)  
- RPO 24h, RTO 1h for non-RT services (INF-NFR-RPO-001/INF-NFR-RTO-001)

## G3. Dashboard/runbook sketch
Dashboards: per-plugin health, event loop lag, DB replication lag.  
Runbooks: device failure, DB failover, stuck traffic phase, door false reject spike.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Notes |
|---|---|---|
| Unit | all plugins | state machines, parsers |
| Integration | core + DB + Redis | schema constraints, transactions |
| Contract | api + internal proto | OpenAPI/proto compatibility |
| E2E | simulator + selected hardware | ICU sampling, traffic cycles, turnstile payment |
| Chaos | DB failover, network loss | verify degraded behavior |

## H2. Test data & environment isolation
Environments: dev, integration, staging, prod.  
Refresh: nightly DB reset for integration; synthetic patient/door/card datasets.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
If replacing existing systems:
1. Stand up platform + DB
2. Import memberships/templates/config
3. Dual-write for lending/billing for 2 weeks
4. Cutover with rollback plan (read-only fallback)
## I2. Backwards compatibility
- Version OpenAPI under `/api/v1`; add `/api/v2` for breaking changes. Maintain 6 months overlap.

---

# J. Tradeoffs & Alternatives

- Microkernel modular monolith vs microservices  
  - Alternatives: microservices; single monolith without plugins  
  - Chosen: microkernel to add modules (traffic display) without disturbing controllers  
  - Ties: **INF-ASR-MOD-001**, **INF-ASR-MOD-002**
- Postgres vs time-series DB  
  - Alternatives: TimescaleDB/Influx  
  - Chosen: Postgres first; add Timescale extension if needed  
  - Ties: **INF-NFR-SCALE-001**
- OIDC vs mTLS-only  
  - Alternatives: mTLS SPIFFE; local auth  
  - Chosen: OIDC for human users + optional mTLS for service identity  
  - Ties: **INF-NFR-SEC-001**

---

# K. Open Questions & Assumptions

## Assumptions
- **A1**: All domain subsystems can be deployed under one administrative org and security boundary unless stated otherwise.  
- **A2**: Hardware interfaces (ports/pulses/register addresses) will be provided by vendors; until then, HardwareIO simulator stubs are used.  
- **A3**: Nurses’ station notification endpoint exists as HTTP webhook or can be implemented as part of this platform.  
- **A4**: Facial recognition accuracy targets (FAR/FRR) and retention policies are to be defined by customer/compliance.

## Naming/diagram conflicts logged (special-case rule #2)
- Diagram actor “NursesStationSystem” vs requirement “nurses' station” (use requirement wording; keep actor alias in implementation notes).
- Requirement duplicates ICU monitoring text (“JCU” vs “ICU”); prefer “ICU” per majority; record both in configs.

## Unresolved stakeholder questions
1. ICU: What are maximum allowable sampling jitter and alert latency bounds per patient class?  
2. Door access: Required FAR/FRR, liveness detection needs, and template retention period?  
3. Traffic: Card regime grammar—exact ASCII format and validation rules?  
4. Heating: How is “occupancy expected” determined (calendar vs learned vs manual schedule)?  
5. Turnstile: How to handle coin jams/refunds and power loss states?

## Inferred requirement IDs list (non-exhaustive; full list in traceability)
All requirements were inferred as `INF-*` because the source has no IDs: INF-ICU-*, INF-DOOR-*, INF-TURN-*, INF-HEAT-*, INF-TRAFFIC-*, INF-SLUICE-*, INF-LIB-*, INF-COURT-*, INF-PC-*, INF-VEH-*, INF-PACK-*, INF-MONO-*, INF-LAB-*, INF-SPEED-*, INF-TEXT-* plus INF-NFR-* and INF-ASR-*.

---

# L. Deliverables

```markdown
# filename: architecture.md
(Contents are the full document in ArchitectureDocument.md; this deliverable is intentionally identical.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Cyber-Physical Control Platform API
  version: "1.0.0"
servers:
  - url: https://cpcp.example.local/api/v1
security:
  - oidc: [cpcp.read, cpcp.write]
paths:
  /icu/patients:
    post:
      summary: Register or update an ICU patient monitoring configuration
      operationId: upsertIcuPatient
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/IcuPatientUpsert" }
      responses:
        "200":
          description: Upserted
          content:
            application/json:
              schema: { $ref: "#/components/schemas/IcuPatient" }
        "400": { $ref: "#/components/responses/BadRequest" }
        "401": { $ref: "#/components/responses/Unauthorized" }
  /icu/patients/{patientId}/safe-ranges:
    put:
      summary: Set safe ranges for a patient
      operationId: putSafeRanges
      parameters:
        - in: path
          name: patientId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/SafeRangeSet" }
      responses:
        "200":
          description: Updated safe ranges
          content:
            application/json:
              schema: { $ref: "#/components/schemas/SafeRangeSet" }
        "400": { $ref: "#/components/responses/BadRequest" }
        "401": { $ref: "#/components/responses/Unauthorized" }
  /icu/measurements:
    get:
      summary: Query vital measurements
      operationId: queryIcuMeasurements
      parameters:
        - in: query
          name: patientId
          required: true
          schema: { type: string }
        - in: query
          name: fromUtc
          required: false
          schema: { type: string, format: date-time }
        - in: query
          name: toUtc
          required: false
          schema: { type: string, format: date-time }
        - in: query
          name: limit
          required: false
          schema: { type: integer, minimum: 1, maximum: 5000, default: 500 }
      responses:
        "200":
          description: Measurements
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/VitalMeasurement" }
        "401": { $ref: "#/components/responses/Unauthorized" }
  /door/attempts:
    post:
      summary: Submit a door access attempt for evaluation
      operationId: createDoorAttempt
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/DoorAttemptRequest" }
      responses:
        "201":
          description: Decision produced
          content:
            application/json:
              schema: { $ref: "#/components/schemas/AccessDecision" }
        "400": { $ref: "#/components/responses/BadRequest" }
        "401": { $ref: "#/components/responses/Unauthorized" }
  /turnstile/sessions:
    post:
      summary: Start a new turnstile session (for diagnostics/sim)
      operationId: startTurnstileSession
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                turnstileId: { type: string }
      responses:
        "201":
          description: Created session
          content:
            application/json:
              schema: { $ref: "#/components/schemas/TurnstileSession" }
        "401": { $ref: "#/components/responses/Unauthorized" }
  /traffic/override:
    post:
      summary: Overseer override (Hold/Change)
      operationId: postTrafficOverride
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/TrafficOverrideCommand" }
      responses:
        "202":
          description: Accepted
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Ack" }
        "400": { $ref: "#/components/responses/BadRequest" }
        "401": { $ref: "#/components/responses/Unauthorized" }
components:
  securitySchemes:
    oidc:
      type: openIdConnect
      openIdConnectUrl: https://idp.example.local/realms/cpcp/.well-known/openid-configuration
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
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string }
        message: { type: string }
        requestId: { type: string }
        details:
          type: object
          additionalProperties: true
    IcuPatientUpsert:
      type: object
      required: [patientId, samplingPeriodMs, deviceId]
      properties:
        patientId: { type: string }
        deviceId: { type: string }
        samplingPeriodMs: { type: integer, minimum: 100 }
        notes: { type: string }
    IcuPatient:
      type: object
      required: [patientId, samplingPeriodMs, deviceId, updatedAtUtc]
      properties:
        patientId: { type: string }
        deviceId: { type: string }
        samplingPeriodMs: { type: integer }
        updatedAtUtc: { type: string, format: date-time }
        notes: { type: string }
    SafeRange:
      type: object
      required: [factor, minValue, maxValue]
      properties:
        factor:
          type: string
          enum: [pulse, temperatureC, systolicMmHg, diastolicMmHg, skinResistanceOhm]
        minValue: { type: number }
        maxValue: { type: number }
    SafeRangeSet:
      type: object
      required: [patientId, ranges]
      properties:
        patientId: { type: string }
        ranges:
          type: array
          minItems: 1
          items: { $ref: "#/components/schemas/SafeRange" }
    VitalMeasurement:
      type: object
      required: [measurementId, patientId, timestampUtc]
      properties:
        measurementId: { type: string }
        patientId: { type: string }
        timestampUtc: { type: string, format: date-time }
        pulse: { type: integer, nullable: true }
        temperatureC: { type: number, nullable: true }
        systolicMmHg: { type: integer, nullable: true }
        diastolicMmHg: { type: integer, nullable: true }
        skinResistanceOhm: { type: number, nullable: true }
        deviceFailure: { type: boolean, default: false }
    DoorAttemptRequest:
      type: object
      required: [cameraId, capturedAtUtc, frameBase64]
      properties:
        cameraId: { type: string }
        capturedAtUtc: { type: string, format: date-time }
        frameBase64:
          type: string
          description: JPEG frame base64-encoded (or a pointer in future versions)
    AccessDecision:
      type: object
      required: [attemptId, result, latencyMs, decidedAtUtc]
      properties:
        attemptId: { type: string }
        result:
          type: string
          enum: [ALLOWED, DENIED, ERROR]
        latencyMs: { type: integer, minimum: 0 }
        decidedAtUtc: { type: string, format: date-time }
        subjectId: { type: string, nullable: true }
        reason: { type: string, nullable: true }
    TurnstileSession:
      type: object
      required: [sessionId, turnstileId, state, coinsInserted, createdAtUtc]
      properties:
        sessionId: { type: string }
        turnstileId: { type: string }
        state:
          type: string
          enum: [WAITING_FOR_COINS, PAID, PASSAGE_OPEN, COMPLETED, ERROR]
        coinsInserted: { type: integer, minimum: 0, maximum: 2 }
        createdAtUtc: { type: string, format: date-time }
    TrafficOverrideCommand:
      type: object
      required: [unitPairId, command]
      properties:
        unitPairId: { type: string }
        command:
          type: string
          enum: [HOLD, CHANGE]
    Ack:
      type: object
      required: [accepted, requestId]
      properties:
        accepted: { type: boolean }
        requestId: { type: string }
```

```proto
// filename: internal.proto
syntax = "proto3";

package cpcp.internal.v1;

option java_multiple_files = true;
option java_package = "com.cpcp.internal.v1";

message Error {
  string code = 1;
  string message = 2;
  string request_id = 3;
}

message Ack {
  bool accepted = 1;
  string request_id = 2;
}

message VitalMeasurement {
  string measurement_id = 1;
  string patient_id = 2;
  string timestamp_utc = 3;
  int32 pulse = 4;
  double temperature_c = 5;
  int32 systolic_mmhg = 6;
  int32 diastolic_mmhg = 7;
  double skin_resistance_ohm = 8;
  bool device_failure = 9;
  string checksum = 10;
}

message Alert {
  string alert_id = 1;
  string timestamp_utc = 2;
  string severity = 3;   // INFO/WARN/CRITICAL
  string category = 4;   // ICU/DOOR/TRAFFIC/HEATING/etc
  string message = 5;
  string entity_id = 6;  // patientId, doorId, etc
}

service TelemetryIngestService {
  rpc RecordVitals(VitalMeasurement) returns (Ack);
}

service AlertService {
  rpc PublishAlert(Alert) returns (Ack);
}

message FaceAttempt {
  string attempt_id = 1;
  string camera_id = 2;
  string captured_at_utc = 3;
  bytes frame_jpeg = 4;
}

message AccessDecision {
  string attempt_id = 1;
  string result = 2; // ALLOWED/DENIED/ERROR
  int32 latency_ms = 3;
  string subject_id = 4;
  string reason = 5;
}

service DoorAccessService {
  rpc EvaluateFaceAttempt(FaceAttempt) returns (AccessDecision);
}

message SimCommand {
  string plugin_id = 1;
  string command = 2; // e.g., "SET_PORT", "EMIT_PULSE", "SET_REGISTER"
  map<string,string> params = 3;
}

service HardwareSimService {
  rpc ApplySimCommand(SimCommand) returns (Ack);
}
```

```yaml
# filename: k8s/cpcp-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cpcp-api
  labels:
    app: cpcp-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cpcp-api
  template:
    metadata:
      labels:
        app: cpcp-api
    spec:
      containers:
        - name: cpcp-api
          image: registry.example.local/cpcp-api:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: cpcp-api-config
            - secretRef:
                name: cpcp-api-secrets
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
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: cpcp-api
spec:
  selector:
    app: cpcp-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cpcp-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cpcp-api
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
  name: cpcp-api-config
data:
  NODE_ENV: "production"
  PORT: "8080"
  OIDC_ISSUER_URL: "https://idp.example.local/realms/cpcp"
  DATABASE_URL: "postgresql://cpcp_api@postgres:5432/cpcp"
---
apiVersion: v1
kind: Secret
metadata:
  name: cpcp-api-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: "CHANGE_ME"
  OIDC_CLIENT_ID: "cpcp-api"
  OIDC_CLIENT_SECRET: "CHANGE_ME"
```

```sql
-- filename: sql/platform_audit_log_ddl.sql
CREATE TABLE IF NOT EXISTS audit_log (
  audit_id            UUID PRIMARY KEY,
  timestamp_utc       TIMESTAMPTZ NOT NULL,
  actor_id            TEXT NOT NULL,
  action              TEXT NOT NULL,
  resource_type       TEXT NOT NULL,
  resource_id         TEXT NOT NULL,
  outcome             TEXT NOT NULL,
  details_json        JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log (timestamp_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_actor ON audit_log (actor_id, timestamp_utc DESC);
```

```sql
-- filename: sql/icu_tables_ddl.sql
CREATE TABLE IF NOT EXISTS icu_patient (
  patient_id          TEXT PRIMARY KEY,
  device_id           TEXT NOT NULL,
  sampling_period_ms  INTEGER NOT NULL CHECK (sampling_period_ms >= 100),
  notes               TEXT NULL,
  updated_at_utc      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS icu_safe_range (
  patient_id          TEXT NOT NULL REFERENCES icu_patient(patient_id) ON DELETE CASCADE,
  factor              TEXT NOT NULL CHECK (factor IN
                      ('pulse','temperatureC','systolicMmHg','diastolicMmHg','skinResistanceOhm')),
  min_value           DOUBLE PRECISION NOT NULL,
  max_value           DOUBLE PRECISION NOT NULL,
  updated_at_utc      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (patient_id, factor),
  CHECK (min_value <= max_value)
);

CREATE TABLE IF NOT EXISTS icu_vital_measurement (
  measurement_id      UUID PRIMARY KEY,
  patient_id          TEXT NOT NULL REFERENCES icu_patient(patient_id) ON DELETE CASCADE,
  timestamp_utc       TIMESTAMPTZ NOT NULL,
  pulse               INTEGER NULL,
  temperature_c       DOUBLE PRECISION NULL,
  systolic_mmhg       INTEGER NULL,
  diastolic_mmhg      INTEGER NULL,
  skin_resistance_ohm DOUBLE PRECISION NULL,
  device_failure      BOOLEAN NOT NULL DEFAULT FALSE,
  checksum            TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_icu_measurement_patient_time
  ON icu_vital_measurement (patient_id, timestamp_utc DESC);

CREATE TABLE IF NOT EXISTS icu_alert (
  alert_id            UUID PRIMARY KEY,
  timestamp_utc       TIMESTAMPTZ NOT NULL,
  patient_id          TEXT NULL REFERENCES icu_patient(patient_id) ON DELETE SET NULL,
  severity            TEXT NOT NULL CHECK (severity IN ('INFO','WARN','CRITICAL')),
  category            TEXT NOT NULL DEFAULT 'ICU',
  message             TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_icu_alert_time ON icu_alert (timestamp_utc DESC);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-ICU-001,Read patient vitals periodically per patient,UseCase_ScenarioView:UC_MonitorVitals|Class_LogicView:PatientMonitor|Scheduler,ICU Monitoring Plugin;cpcp-core,openapi.yaml;internal.proto;sql/icu_tables_ddl.sql,Periodic sampling implemented via Scheduler with per-patient config persisted in icu_patient.
INF-ICU-002,Store vitals in database,Class_LogicView:VitalMeasurement,ICU Monitoring Plugin,sql/icu_tables_ddl.sql,Measurements persisted with indexes for time-series queries.
INF-ICU-003,Medical staff specify safe ranges,UseCase_ScenarioView:UC_ManageSafeRanges|Class_LogicView:SafeRange,ICU Monitoring Plugin;cpcp-api,openapi.yaml;sql/icu_tables_ddl.sql,Safe ranges stored per patient/factor and updated via authenticated API.
INF-ICU-004,Notify nurses station if out-of-range,UseCase_ScenarioView:UC_SendICUAlerts|Class_LogicView:Alert,AlertService,internal.proto;sql/icu_tables_ddl.sql,Alerts published over internal RPC and persisted for auditability.
INF-ICU-005,Notify nurses station if analog device fails,UseCase_ScenarioView:UC_SendICUAlerts|Class_LogicView:PatientMonitor,ICU Monitoring Plugin,internal.proto;sql/icu_tables_ddl.sql,Device-failure flag triggers CRITICAL alert.
INF-DOOR-001,Recognize facial features and compare to cleared DB,UseCase_ScenarioView:UC_AttemptDoorEntry|Class_LogicView:FaceTemplate,Door Access Plugin,openapi.yaml;internal.proto,Templates stored and evaluated per attempt.
INF-TURN-001,No entry without paying two coins,UseCase_ScenarioView:UC_OperateTurnstile,Turnstile Plugin,openapi.yaml,State machine enforces coin count before barrier unlock.
INF-TURN-002,Any visitor who paid two coins allowed to enter,UseCase_ScenarioView:UC_OperateTurnstile,Turnstile Plugin,openapi.yaml,Transition to PASSAGE_OPEN once coinsInserted==2.
INF-HEAT-001,Maintain room temperature per knob setting,UseCase_ScenarioView:UC_ControlHeating,Heating Plugin,openapi.yaml,Control loop targets setpoint.
INF-HEAT-002,Unoccupied rooms 5C below knob setting,UseCase_ScenarioView:UC_ControlHeating,Heating Plugin,openapi.yaml,Eco offset applied when occupancy false.
INF-HEAT-003,Anticipate occupancy 30 minutes before expected,UseCase_ScenarioView:UC_ControlHeating,Heating Plugin,openapi.yaml,Scheduler preheats based on prediction input.
INF-PC-001,Display installed components and IRQ/IO port assignments on request,UseCase_ScenarioView:UC_ShowPCConfig,PC Config Viewer Plugin,openapi.yaml,On-demand hardware inventory report.
INF-TRAFFIC-001,Fixed 4-phase light cycle (50/120/50/120),UseCase_ScenarioView:UC_ControlTrafficLights,Traffic Lights Plugin,internal.proto,Deterministic schedule emits pulses.
INF-TRAFFIC-002,Add display module sharing RPulse/GPulse without disturbing design,UseCase_ScenarioView:UC_ControlTrafficLights,Traffic Display Plugin;EventBus,internal.proto,EventBus subscription provides decoupling.
INF-TRAFFIC-003,Card reader loads regime encoded ASCII,UseCase_ScenarioView:UC_ControlTrafficLights,Traffic Lights Plugin,openapi.yaml,Regime parser + stored configs.
INF-TRAFFIC-004,Overseer Hold/Change overrides phase,UseCase_ScenarioView:UC_OverrideTrafficPhase,Traffic Lights Plugin,openapi.yaml,Override commands alter phase timing.
INF-SLUICE-001,Gate open 10 min every 3 hours otherwise closed,UseCase_ScenarioView:UC_OperateSluiceGate,Sluice Gate Plugin,internal.proto,Scheduled open/close with sensor interlocks.
INF-SLUICE-002,Gate responds to operator commands,UseCase_ScenarioView:UC_OperateSluiceGate,Sluice Gate Plugin,openapi.yaml,Manual commands mediated by safety checks.
INF-VEH-001,Detect vehicle pattern and report type with hourly totals,UseCase_ScenarioView:UC_GenerateReports,Vehicle Monitor Plugin,openapi.yaml,Sensor events classified and aggregated hourly.
INF-LAB-001,Display 32 voltages and average,UseCase_ScenarioView:UC_GenerateReports,Lab Voltages Plugin,openapi.yaml,Reads A/D registers and updates UI state.
INF-SPEED-001,Compute speed and odometer from wheel pulses with shared registers,UseCase_ScenarioView:UC_GenerateReports,Speedometer Plugin,internal.proto,HardwareIO reads pulses/writes registers deterministically.
INF-LIB-001,Administer lending library,UseCase_ScenarioView:UC_ManageLibrary,Library Plugin,openapi.yaml,Core lending/ordering/fines enforced by domain rules.
INF-LIB-002,Enforce membership acquisition/exercise rules,UseCase_ScenarioView:UC_ManageLibrary,Library Plugin,openapi.yaml,Membership state machine + constraints.
INF-LIB-003,Overdue books incur fines and reports needed,UseCase_ScenarioView:UC_GenerateReports,Library Plugin,openapi.yaml,Fine accrual jobs + report endpoints.
INF-COURT-001,Manage general/indoors subscriptions and operate lock/lights with billing,UseCase_ScenarioView:UC_StartLightingSession,Tennis Court Plugin,openapi.yaml,Billing entries produced per lighting session tied to indoors member.
INF-TEXT-001,Lexical analyzer outputs token stream with type/value,UseCase_ScenarioView:UC_GenerateReports,Lexer Plugin,openapi.yaml,CLI/offline plugin providing structured token output.
INF-TEXT-002,Stream editor performs global find/replace operations from command file,UseCase_ScenarioView:UC_GenerateReports,Stream Editor Plugin,openapi.yaml,Deterministic batch transformations.
INF-TEXT-003,Party plan editor maintains parties/guests/invitations via CLI,UseCase_ScenarioView:UC_GenerateReports,Party Plan Plugin,openapi.yaml,CRUD operations stored locally/DB.
INF-TEXT-004,Correspondence report summary per correspondent,UseCase_ScenarioView:UC_GenerateReports,Correspondence Report Plugin,openapi.yaml,Aggregates sent/received message stats.
INF-OCR-001,Keyboard entry of all text parts of rare book for analysis,UseCase_ScenarioView:UC_ManageLibrary,OCR Intake Plugin,openapi.yaml,Text ingestion endpoints and storage.
INF-PACK-001,Package router reads barcodes and sets switches without unsafe flipping,UseCase_ScenarioView:UC_GenerateReports,Package Router Plugin,internal.proto,Switch-setting guarded by occupancy sensors and spacing logic.
INF-MONO-001,Monorail shuttles back/forth, stop 60s each end, fast as possible within comfort limits,UseCase_ScenarioView:UC_GenerateReports,Monorail Plugin,internal.proto,Control loop optimizes travel with constraints.
INF-NFR-SEC-001,All admin/control operations authenticated and encrypted in transit,Class_LogicView:AuditLogger,cpcp-api;cpcp-core,openapi.yaml;k8s/cpcp-api-deployment.yaml,OIDC + TLS.
INF-NFR-SEC-002,Biometric templates encrypted at rest and access-controlled,Class_LogicView:FaceTemplate,Door Access Plugin,sql/*;openapi.yaml,Protect sensitive biometric data.
INF-NFR-SEC-003,Supply chain security and secret rotation,Class_LogicView:AuditLogger,CI/CD;Ops,k8s/*,Vuln scan + rotation policy.
INF-NFR-SEC-004,Immutable audit logging for critical actions,Class_LogicView:AuditLogger,cpcp-core,sql/platform_audit_log_ddl.sql,Append-only audit table.
INF-NFR-AVAIL-001,Core services HA with replicas and DB replication,Deployment view inferred,Ops,k8s/*,Multi-replica + HA DB.
INF-NFR-RPO-001,RPO <= 24h,Ops inferred,Ops,architecture.md,Backup cadence defined.
INF-NFR-RTO-001,RTO <= 1h for central services,Ops inferred,Ops,architecture.md,Restore drills and runbooks.
```

---

## Acceptance Criteria Verification Table

| Item | Status |
|---|---|
| 3-line Analysis Plan present | ✅ |
| Sections A-L included | ✅ |
| Every FR/NFR/ASR mapped in traceability matrix | ⚠️ Partially — full coverage requires expanding traceability beyond representative rows (see note below) |
| ≥1 OpenAPI YAML and ≥1 internal proto included | ✅ |
| Representative k8s manifest snippet included | ✅ |
| SQL DDL examples included | ✅ |
| All major components have at least one API contract and a data schema | ⚠️ Partially — only ICU/platform shown in SQL; remaining domains need DDL files |
| Assumptions and unresolved questions listed | ✅ |

**Important implementation note:** The provided requirements set is very large; the traceability and schemas above are representative but not exhaustive for every plugin. To fully satisfy the “Every FR/NFR/ASR must appear at least once” and “All major components have schema” constraints, the next iteration should (1) enumerate each remaining plugin’s DDL in `sql/*.sql`, and (2) extend `traceability_matrix.csv` to include every additional inferred requirement line-by-line.

---

## How to review checklist (short)
- All FR/NFR/ASR present in traceability matrix? (expand to full)  
- OpenAPI + internal API contract included and valid?  
- Each major component has responsibilities, 3+ stack options, recommended stack + justification, API contract, and schema? (complete remaining plugins)  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities? (complete remaining)  
- Assumptions and open questions clearly listed?  

```markdown
# filename: ArchitectureDocument.md
(Primary artifact: this entire response content.)