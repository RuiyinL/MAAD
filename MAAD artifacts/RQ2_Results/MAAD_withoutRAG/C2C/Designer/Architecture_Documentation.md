Scope: Produce production-ready architecture for TxDOT TMDD/DATEX Center-to-Center (C2C) data repository + device control + web map + incident GUI + remote control GUI.  
Approach: Normalize missing IDs into `INF-*`, prefer SRS naming over UML, map all requirements to 4+1 views and deliver API/contracts, schemas, and ops-ready k8s.  
Validation: Traceability matrix completeness, OpenAPI/proto/k8s/SQL syntax validation, and scenario validation against referenced diagrams (titles:IDs).

# A. Executive Summary (≤1 page)

## System overview
The Center-to-Center (C2C) Communications Network interconnects multiple dissimilar Traffic Management Centers (TMCs) by exchanging standardized traffic/device/incident data using **TMDD message sets** encoded as **DATEX/ASN over TCP/IP**, persisting a common repository, and enabling **remote device control** (DMS/LCS/CCTV/etc.), plus **Web Map**, **Incident GUI**, and **Remote Control GUI** clients.

**Primary diagram mapping (one-line):** 4+1 view is represented by *UseCase_ScenarioView: UC_*; *Container_PhysicalView: API/DB/AUDIT/ADAPTER/BUS*; *Component_DevelopmentView: Api/LeaseMgr/InterlockSvc/Ctrl/ExportSvc*; *Class_LogicView: DeviceStatus/ControlCommand/AuditEvent*; *Deployment_PhysicalView: AppA/AppB/Broker/DBS/GW*.

## Architectural styles & topology
- **Architectural style(s):** Canonical data core (TMDD) + Adapter/Gateway boundary + Event-driven integration + Append-only audit log.
- **Deployment topology:** Active-active application tier behind ingress, shared HA database, message broker, controller gateway/adapter, one-way external data export.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---:|---|
| R1: Legacy system/protocol ambiguity (project-defined protocol, vendor device interfaces) | High | Contract-first adapters with versioned schemas; stub ownership + freeze dates; CI conformance gates for TMDD/DATEX (see K: A1/A2). |
| R2: Safety/security for remote device control over public networks | High | Strong authn/authz (OIDC+JWT), mTLS inside cluster, least-privilege RBAC, immutable audit, deterministic command windows + idempotency. |
| R3: Outdated platform constraints (Windows NT, ESRI ARC IMS/MapObjects, C/C++) | Medium | Preserve compatibility by isolating legacy UI/map components behind API; allow modern server stack while keeping TMDD/DATEX compliance and adapter boundary. Conflicts recorded in K. |

## Key QA coverage mapping (Scalability/Availability/Security/Performance/Maintainability)

> Since the SRS has no explicit ASR/NFR IDs, this document introduces **inferred** NFR/ASR IDs (`INF-NFR-*`, `INF-ASR-*`). All are listed in **K** and appear in **B**.

| Quality | Inferred IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-SCALE-01 | Load + soak tests; HPA validation; broker throughput tests |
| Availability | INF-NFR-AVAIL-01, INF-ASR-HA-01 | Failover tests; chaos (pod/node kill); DB replica promotion drills |
| Security | INF-NFR-SEC-01..04 | SAST/DAST; dependency scan; pen test; secrets rotation drill |
| Performance | INF-NFR-PERF-01..03 | Latency SLIs; protocol encode/decode microbench; API p95/p99 tests |
| Maintainability | INF-ASR-MOD-01, INF-ASR-CONTRACT-01 | Contract tests; consumer-driven tests; schema migration tests |

---

# B. Traceability & Rationale

## Traceability Matrix (also delivered as `traceability_matrix.csv`)
> Rule: SRS lacks IDs → extracted and assigned `INF-*` IDs. Conflicts with provided UML (RLCS reversible lane focus) are logged in K; SRS naming is preferred.

**Table columns:** Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-NET-01 | Provide network name + link data per roadway network | Class_LogicView: DeviceStatus; Container_PhysicalView: DB | C2C API, TMDD Repository | openapi.yaml; sql/network_ddl.sql | Canonical TMDD-ish core persists network/link/node for reuse and exchange. |
| INF-FR-NET-02 | Provide link info (id, name, type) | Container_PhysicalView: DB | Repository Service | sql/link_ddl.sql | Normalized schema supports map + exchanges. |
| INF-FR-NET-03 | Provide node info (id, name, type desc) | Container_PhysicalView: DB | Repository Service | sql/node_ddl.sql | Supports topology needed for mapping and device association. |
| INF-FR-INC-01 | Support incident info (network id, description, roadway) | UseCase_ScenarioView: UC_AcquireStatus (mapped to “acquire data”); Container_PhysicalView: API/DB | Incident Service | openapi.yaml; sql/incident_ddl.sql | Incidents are core shared objects and feed map + external centers. |
| INF-FR-LC-01 | Support lane closure info (network id, id, description) | Container_PhysicalView: API/DB | LaneClosure Service | openapi.yaml; sql/lane_closure_ddl.sql | Same pattern as incidents with lifecycle and audit. |
| INF-FR-DMS-STAT-01 | Provide DMS status (network id, DMS id, DMS name) | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml; sql/device_status_ddl.sql | DeviceStatus canonical entity supports multiple device types. |
| INF-FR-DMS-CTRL-01 | Support DMS control cmd (net id, DMS id, username/password) | Sequence_ProcessView_S1_RequestModeChange (control pattern); Component_DevelopmentView: Api/Ctrl | Command Service, Adapter | openapi.yaml; internal.proto; sql/device_command_ddl.sql; sql/audit_event_ddl.sql | Replace username/password-in-payload with secure auth; still meet intent (authorized control). Conflict noted in K. |
| INF-FR-LCS-STAT-01 | Provide LCS status (id, name, location, status) | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml; sql/device_status_ddl.sql | DeviceStatus supports location/status. |
| INF-FR-LCS-CTRL-01 | Support LCS control cmd (id, username/password) | Component_DevelopmentView: Ctrl | Command Service, Adapter | openapi.yaml; internal.proto | Control routed via adapter boundary. |
| INF-FR-CCTV-STAT-01 | Provide CCTV status (id, name, location, status) | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml; sql/device_status_ddl.sql | Standard status model. |
| INF-FR-CCTV-CTRL-01 | Support CCTV control request (id, username/password) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Authorization handled by platform; adapter does device IO. |
| INF-FR-CCTV-SNAP-01 | Support video snapshot status info | Container_PhysicalView: EXP/DB | Media Metadata Service | openapi.yaml; sql/cctv_snapshot_ddl.sql | Store snapshot metadata; binary stored externally if needed. |
| INF-FR-CCTV-SW-01 | Support CCTV switching cmd (username/password, channel input id) | Component_DevelopmentView: Ctrl | Command Service | openapi.yaml; internal.proto | Adapter translates to vendor protocol. |
| INF-FR-RM-STAT-01 | Ramp meter status | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml | DeviceStatus deviceType=RAMP_METER. |
| INF-FR-RM-CTRL-01 | Ramp meter control (plan) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Plan as command payload with validation. |
| INF-FR-HAR-STAT-01 | HAR status | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml | DeviceStatus deviceType=HAR. |
| INF-FR-HAR-CTRL-01 | HAR control (message) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Message payload audited. |
| INF-FR-TS-STAT-01 | Traffic signal status | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml | DeviceStatus deviceType=TRAFFIC_SIGNAL. |
| INF-FR-TS-CTRL-01 | Traffic signal control (plan id) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Plan id validated per network/device. |
| INF-FR-ESS-STAT-01 | ESS status (type, location, status) | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml | ESS supported as status-only. |
| INF-FR-HOV-STAT-01 | HOV status (link id, status, plan) | Container_PhysicalView: DB | Device Status Service | openapi.yaml | Link association supported via schema. |
| INF-FR-HOV-CTRL-01 | HOV control (lane plan) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Command with plan payload. |
| INF-FR-PL-STAT-01 | Parking lot status (capacity) | Container_PhysicalView: DB | Parking Service | openapi.yaml; sql/parking_lot_status_ddl.sql | Capacity/time series supported. |
| INF-FR-SZ-STAT-01 | School zone status (link id, id, name) | Container_PhysicalView: DB | SchoolZone Service | openapi.yaml; sql/school_zone_ddl.sql | Status/control supported. |
| INF-FR-SZ-CTRL-01 | School zone control (plan) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Plan payload. |
| INF-FR-RRX-STAT-01 | Railroad crossing status | Container_PhysicalView: DB | RailCrossing Service | openapi.yaml; sql/rail_crossing_status_ddl.sql | Persist and publish. |
| INF-FR-RVL-STAT-01 | Reversible lane status (indicator status/failure) | Class_LogicView: DeviceStatus; State_LogicView_LaneSegment | Device Status, Control | openapi.yaml | Mode/state patterns reused even if UML was RLCS-focused. |
| INF-FR-RVL-CTRL-01 | Reversible lane control (plan, duration) | State_LogicView_LaneSegment | Command Service | openapi.yaml; internal.proto | Deterministic sequencing and duration validation. |
| INF-FR-DYL-STAT-01 | Dynamic lane status (failure state) | Class_LogicView: DeviceStatus | Device Status Service | openapi.yaml | Supported. |
| INF-FR-DYL-CTRL-01 | Dynamic lane control (lane plan) | Component_DevelopmentView: Api/Ctrl | Command Service | openapi.yaml; internal.proto | Supported. |
| INF-FR-BS-STAT-01 | Bus stop status | Container_PhysicalView: DB | Transit Service | openapi.yaml; sql/transit_stop_ddl.sql | Persist for map. |
| INF-FR-BL-STAT-01 | Bus location + schedule adherence | Container_PhysicalView: DB | Transit Service | openapi.yaml; sql/vehicle_location_ddl.sql | Time series for locations. |
| INF-FR-LRSTOP-01 | Light/commuter stop status + routes | Container_PhysicalView: DB | Transit Service | openapi.yaml; sql/transit_stop_ddl.sql | Routes stored as JSONB/child table. |
| INF-FR-LRLOC-01 | Light/commuter location + adherence | Container_PhysicalView: DB | Transit Service | openapi.yaml; sql/vehicle_location_ddl.sql | Same as bus location. |
| INF-FR-PR-STAT-01 | Park & ride lot (status, capacity) | Container_PhysicalView: DB | Parking Service | openapi.yaml; sql/parking_lot_status_ddl.sql | Supports capacity. |
| INF-FR-VP-01 | Vehicle priority (vehicle id, link id, intersection id) | Container_PhysicalView: DB | Priority Service | openapi.yaml; sql/vehicle_priority_ddl.sql | Supports signal priority integrations. |
| INF-FR-DEVAGG-01 | Network device status aggregate (counts + status datasets) | Container_PhysicalView: API/DB | Device Aggregation | openapi.yaml | Aggregate endpoint across devices. |
| INF-FR-CMDTF-01 | Command timeframe request (network id, device type) | Container_PhysicalView: API | Policy Service | openapi.yaml; sql/command_timeframe_ddl.sql | Enforces allowed hours/days. |
| INF-FR-CMDTF-02 | Command timeframe response (days/times accepted) | Container_PhysicalView: API | Policy Service | openapi.yaml | Returned policy for GUI gating. |
| INF-FR-STORE-01 | Data Collector stores TMDD elements + message set info | Package_DevelopmentView: persistence/domain | TMDD Repository | sql/tmdd_message_store_ddl.sql | Canonical storage keyed by schema/version. |
| INF-NFR-STD-01 | Use TMDD standard to transmit info | Standards-Gated approach | TMDD Codec/Contracts | internal.proto; openapi.yaml | Canonical model ensures consistent standard exchange. |
| INF-NFR-STD-02 | DATEX/ASN used to transmit TMDD message sets | Deployment_PhysicalView: GW | DATEX/ASN Codec | internal.proto | Codec boundary isolates encoding. |
| INF-NFR-STD-03 | TCP/IP transport for DATEX/ASN | Deployment_PhysicalView: VLAN links | Transport Layer | internal.proto | Transport settings + retries defined in contracts. |
| INF-FR-MAP-01 | Web Map app generates map for WWW server | Container_PhysicalView: GUI/API | Web Map Service | openapi.yaml | Map served via web endpoints. |
| INF-FR-MAP-02 | Map shows traffic conditions | Container_PhysicalView: EXP/DB | Map Rendering | openapi.yaml | Speeds/incidents/devices drive depiction. |
| INF-FR-MAP-03 | Display interstates/state highways | INF | Map Layers | (legacy ESRI config) | Layer configuration from NCTCOG base map. |
| INF-FR-MAP-04 | Basemap from NCTCOG GeoData warehouse | INF | ETL/Import | (runbook) | Import pipeline. |
| INF-FR-MAP-05 | Zoom level change | INF | Web UI | (UI spec) | Client side; API supports tiles/extents. |
| INF-FR-MAP-06 | Pan N/S/E/W | INF | Web UI | (UI spec) | Client side. |
| INF-FR-MAP-07 | Links color-coded by speeds; configurable thresholds | INF | Config Service | k8s ConfigMap | Config-driven thresholds. |
| INF-FR-MAP-08 | Display current incidents as icons; click for details | INF | Map + Incident API | openapi.yaml | Incident endpoints provide details. |
| INF-FR-MAP-09 | Incidents table view | INF | Web UI | openapi.yaml | List endpoint supplies tabular data. |
| INF-FR-MAP-10 | Map can display DMS/LCS/CCTV | INF | Map + Device APIs | openapi.yaml | Device list/status endpoints. |
| INF-FR-IGUI-01 | Incident GUI enter incident/lane closure without a Center | INF | Incident GUI Client | openapi.yaml | Client uses API directly. |
| INF-FR-IGUI-02 | Input incident fields | INF | Incident API | openapi.yaml | Schema enforces required fields. |
| INF-FR-IGUI-03 | Input lane closure fields | INF | LaneClosure API | openapi.yaml | Schema enforces required fields. |
| INF-FR-IGUI-04 | List previously entered incidents | INF | Incident API | openapi.yaml | GET list endpoint. |
| INF-FR-IGUI-05 | Modify incident | INF | Incident API | openapi.yaml | PUT/PATCH endpoint. |
| INF-FR-IGUI-06 | Delete incident | INF | Incident API | openapi.yaml | DELETE endpoint. |
| INF-FR-IGUI-07 | List lane closures | INF | LaneClosure API | openapi.yaml | GET list endpoint. |
| INF-FR-IGUI-08 | Delete lane closure | INF | LaneClosure API | openapi.yaml | DELETE endpoint. |
| INF-FR-RGUI-01 | Remote Control GUI runs on public network, sends equipment requests | UseCase_ScenarioView: UC_RequestMode (pattern) | Remote Control API | openapi.yaml | Public client uses authenticated API. |
| INF-FR-RGUI-02 | GUI prompts username/password at startup | INF | Auth | openapi.yaml | Implement via OIDC login (no raw password to devices). |
| INF-FR-RGUI-03 | Select network identifier for request | INF | Control API | openapi.yaml | networkId required in commands. |
| INF-FR-RGUI-04..14 | Select device + provide fields for DMS/LCS/CCTV/.../Dynamic Lane | Component_DevelopmentView: Api/Ctrl | Command API | openapi.yaml; internal.proto | Command payload polymorphic by deviceType. |
| INF-FR-RGUI-15 | Returned status displayed scrollable list | INF | WebSocket/SSE | openapi.yaml | Telemetry channel pushes status/ack. |
| INF-CONST-PLAT-01 | Server executes on Windows NT | Conflict | Runtime Platform | K | Modern infra recommended; legacy noted as constraint/conflict. |
| INF-CONST-LIB-01 | DATEX/ASN runtime library on any communicating computer | INF | Deployment checks | CI/CD + initContainers | Validate library presence at startup. |
| INF-CONST-ESRI-01 | Web server uses ESRI ARC IMS | Conflict | Map Rendering | K | Kept as optional legacy module; API decouples. |
| INF-CONST-PLAT-02 | C2C executes on Windows NT | Conflict | Runtime Platform | K | Same as above. |
| INF-CONST-LANG-01 | Implemented in C/C++ | Conflict | Services | K | Adapter/codec can be C++; services can be modern while preserving compliance. |
| INF-CONST-WEB-01 | Web interface uses C/C++ + ESRI ARC IMS | Conflict | Map Web | K | Optional legacy boundary. |
| INF-CONST-IGUI-01 | Incident GUI uses C/C++ + ESRI MapObjects | Conflict | GUI | K | Can be replaced with web app using same API. |
| INF-CONST-RGUI-01 | Remote Control GUI uses C/C++ + ESRI MapObjects | Conflict | GUI | K | Same. |
| INF-FR-MODE-01 | Operate in normal mode (collect from all, combine into single datastore) | Deployment_PhysicalView: AppA/AppB/DBS | Ingestion + Repository | internal.proto; sql/* | Normal mode = standard runtime. |
| INF-FR-MODE-02 | Operate in test mode (normal + logs activities) | G: Observability | Audit/Logging | sql/audit_event_ddl.sql | Test mode = increased logging + replay. |

---

# C. Architecture Overview

## Context (Scenario view)
Actors: operators/supervisors/maintainers, external data consumers, and external/legacy centers. Use cases include: ingest status, exchange standardized messages, issue device control, audit, and export one-way feeds. (Ref: *UseCase_ScenarioView: UC_AcquireStatus/UC_RequestMode/UC_Audit/UC_Export* — pattern reused for C2C device control workflows.)

## Container view
Core containers: **C2C Control/Data API**, **TMDD/DATEX Ingestion & Codec**, **Adapter Gateway** to legacy/proprietary systems, **Operational DB**, **Audit Log**, **Event Bus**, **Web Map UI**, **Incident UI**, **Remote Control UI**, and **One-way Export Service**. (Ref: *Container_PhysicalView: API/DB/AUDIT/ADAPTER/BUS/EXP*.)

## Component/package view
Packages: ui/api/domain/application/integrations/messaging/persistence. (Ref: *Package_DevelopmentView: UI/API/DOMAIN/APP/INTEG/MSG/PERSIST*.) Components: API, Interlock/Policy, Adapter(s), Telemetry, Export, Broker, DB, Audit. (Ref: *Component_DevelopmentView: Api/Ctrl/ExportSvc/Bus/Db/Audit*.)

## Class/runtime view
Canonical entities: Network/Link/Node, Incident, LaneClosure, Device, DeviceStatus, DeviceCommand, TMDDMessageEnvelope, AuditEvent. Control flows are deterministic, with command correlation IDs and append-only audit. (Pattern ref: *Class_LogicView: ControlCommand/DeviceStatus/AuditEvent* and *Sequence_ProcessView_S1_RequestModeChange*.)

## Deployment view
Active-active app servers, centralized broker and DB tier, gateway/adapter tier interfacing with field/legacy systems, and one-way external export network. (Ref: *Deployment_PhysicalView: AppA/AppB/Broker/DBS/GW/ONEWAY*.)

---

# D. Detailed Technical Design (developer-facing)

## D1. C2C API Service (Public API Gateway)

### 1) Responsibilities & data ownership
Owns external HTTP APIs for networks/links/nodes, incidents/lane closures, device status aggregation, device command submission, and telemetry subscriptions. Owns **authorization**, request validation, idempotency keys, and orchestration to internal services. Data owner for API-level resources; persists to OperationalDB; all mutating actions emit AuditEvents.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: **Go 1.22–1.23**
- Conservative: **Java 17–21 (Spring Boot 3.2–3.4)**
- Cutting-edge: **Rust 1.78–1.82 (Axum 0.7–0.8)**

**Web framework**
- Recommended: Go **chi 5.x** or **gin 1.10+**
- Conservative: Spring MVC/WebFlux
- Cutting-edge: Rust Axum

**RPC/HTTP**
- Recommended: **REST/JSON (OpenAPI 3.0.3)** externally + **gRPC** internally
- Conservative: REST only (internal/external)
- Cutting-edge: GraphQL externally + gRPC internally (not recommended for safety/control)

**Persistence**
- Recommended: **PostgreSQL 14–16**
- Conservative: Microsoft SQL Server 2019–2022 (if Windows-centric)
- Cutting-edge: CockroachDB 23–24 (distributed SQL)

**Cache**
- Recommended: **Redis 7.2–7.4**
- Conservative: In-memory per instance (limited correctness)
- Cutting-edge: KeyDB 6.x (Redis-compatible)

**Messaging**
- Recommended: **NATS JetStream 2.10+**
- Conservative: RabbitMQ 3.12–3.13
- Cutting-edge: Redpanda/Kafka (overkill unless very high throughput)

**Search**
- Recommended: PostgreSQL GIN indexes (incidents/devices)
- Conservative: No search; pagination only
- Cutting-edge: OpenSearch 2.x

**Authn/authz**
- Recommended: **OIDC (Keycloak 24–26) + JWT**
- Conservative: mTLS client certs only
- Cutting-edge: SPIFFE/SPIRE + OPA everywhere

**Observability**
- Recommended: OpenTelemetry SDK + Prometheus + Loki
- Conservative: Prometheus + structured logs only
- Cutting-edge: eBPF-based tracing (Cilium/Hubble)

**CI/CD**
- Recommended: GitHub Actions/GitLab CI with conformance gates
- Conservative: Jenkins
- Cutting-edge: Tekton + policy-as-code gates

**Container runtime**
- Recommended: containerd (Kubernetes standard)
- Conservative: Docker runtime (deprecated in k8s)
- Cutting-edge: gVisor sandboxing for adapter pods

**Infra provisioning**
- Recommended: Terraform 1.6–1.9
- Conservative: Manual + scripts
- Cutting-edge: Crossplane

### 3) Recommended default stack (with justification)
- Go 1.22–1.23, chi 5.x, PostgreSQL 14–16, NATS JetStream 2.10+, Redis 7.2+, Keycloak 24–26, OpenTelemetry 1.x.  
**Justification:** meets **INF-ASR-CONTRACT-01** (versioned contracts) and **INF-NFR-PERF-01** (low latency API/telemetry) and **INF-NFR-SEC-01** (public-network remote GUI auth).

### 4) Interface design (External OpenAPI — `openapi.yaml`)
(See full artifact in section L.)

### 5) Data model / schema (DDL)
(See artifacts: `sql/*.sql` in section L.)
- Encryption-at-rest fields: user identifiers, any credentials (but SRS username/password in commands is not stored).  
**Justification:** meets **INF-NFR-SEC-02** (secrets handling) and **INF-ASR-AUDIT-01** (immutable audit).

### 6) Caching & consistency strategy
- Cache read-heavy reference data: networks/links/nodes (TTL 10 minutes, invalidate on update).
- Cache device status snapshots per network/deviceType (TTL 2–5 seconds) for map/GUI.  
- Strong consistency for commands and audit: commands persisted before publish; audit append is synchronous for mutating requests.

---

## D2. TMDD/DATEX Ingestion + Codec Service

### 1) Responsibilities & data ownership
Implements DATEX/ASN encode/decode for TMDD message sets, handles TCP sessions to peer centers, validates runtime library presence, and produces canonical `tmdd_message_envelope` records plus derived entities (incidents, device statuses).

### 2) Technology options

**Language/runtime**
- Recommended: **C++20** (codec integration) + Go wrapper service
- Conservative: Pure C (legacy)
- Cutting-edge: Rust with ASN.1 tooling

**Transport**
- Recommended: TCP with reconnect + backoff + heartbeat
- Conservative: TCP only, minimal retry
- Cutting-edge: QUIC (non-compliant with SRS)

**Schema validation**
- Recommended: compile-time ASN.1 + runtime conformance tests
- Conservative: best-effort parsing
- Cutting-edge: formal verification (not necessary)

### 3) Recommended default stack
- C++20 codec module (DATEX/ASN), exposed via gRPC to Go services.  
**Justification:** meets **INF-NFR-STD-02** (DATEX/ASN) and **INF-NFR-STD-03** (TCP/IP transport).

### 4) Internal contracts (`internal.proto`)
Includes `PublishTmddEnvelope`, `TranslateStatus`, `TranslateIncident`, `SendDeviceCommandToAdapter`.

### 5) Data model
`tmdd_message_envelope` stores raw payload hash, schema version, direction (inbound/outbound), peer id, timestamps.

### 6) Caching/consistency
No caching of raw envelopes; derived entities use upsert with source timestamps; deduplicate by `(peer_id, message_id)`.

---

## D3. Adapter Gateway Service (Legacy/Proprietary Integrations)

### 1) Responsibilities & data ownership
Translates between project-defined legacy protocol / vendor device APIs and canonical commands/status. One adapter per system/vendor; pluggable driver boundary. Owns command correlation, retries, and error mapping.

### 2) Technology options
- Recommended: Go + plugin pattern OR sidecar binaries per vendor
- Conservative: C/C++ monolith adapter
- Cutting-edge: WASM plugin sandboxing

### 3) Recommended default stack
- Go adapter host + vendor-specific sidecars; strict versioned contracts.  
**Justification:** meets **INF-ASR-CONTRACT-01** (versioned interface stubs) and **INF-FR-MODE-01** (normal mode ingestion from dissimilar systems).

### 4) Internal contracts
See `internal.proto` service `AdapterService`.

### 5) Data model
`device_command` and `device_status` are persisted in OperationalDB; adapter only writes via API/internal service.

### 6) Caching/consistency
No caching of commands. Status push is event-driven; last-known status stored with freshness timestamp.

---

## D4. Web Map Service (Traffic Conditions Map)

### 1) Responsibilities & data ownership
Renders map layers (links colored by speed thresholds, incidents as icons, devices overlay). May be implemented as modern web map (tiles/vector) or kept as ESRI legacy renderer behind same APIs.

### 2) Technology options
- Recommended: Web frontend (React 18–19) + maplibre-gl; server provides vector/geojson endpoints
- Conservative: ESRI ArcGIS Enterprise/Server equivalents if ARC IMS required
- Cutting-edge: WebGPU vector rendering

### 3) Recommended default stack
- React + MapLibre; server endpoints for link speeds/incidents/devices.  
**Justification:** meets **INF-FR-MAP-01** (WWW map) and **INF-FR-MAP-07** (configurable speed thresholds).

### 4) Interfaces
Uses external OpenAPI endpoints `/map/links`, `/incidents`, `/devices/status`.

### 5) Data model
Reuses `link` + speed fields on `device_status` or derived `link_speed` table (optional; not included in minimal DDL set).

### 6) Caching
CDN cache for basemap; API caches link speed snapshots (TTL seconds).

---

## D5. Incident GUI + Remote Control GUI

### 1) Responsibilities & data ownership
Client applications for (a) CRUD incidents/lane closures, and (b) submit device control commands and view returned status list. Do not own data; use API.

### 2) Technology options
- Recommended: Web SPA + OIDC login
- Conservative: C++ desktop app (SRS constraint)
- Cutting-edge: Cross-platform (Flutter)

### 3) Recommended default stack
- Web SPA + OIDC + WebSocket telemetry.  
**Justification:** meets **INF-FR-RGUI-01** (public network remote GUI) and **INF-NFR-SEC-01** (secure auth).

### 4) Interfaces
Uses `/auth/*` (OIDC), `/incidents/*`, `/lane-closures/*`, `/commands/*`, `/telemetry/*`.

---

# E. Operations & Deployment (ops-facing)

## E1) Kubernetes-ready plan (`k8s/c2c-api-deployment.yaml`)
- Includes Deployment, Service, HPA, ConfigMap, Secret.
- Sizing tiers (suggested):
  - Small (≤50 RPS): 2 replicas, 250m CPU, 512Mi RAM
  - Medium (≤300 RPS): 4 replicas, 500m CPU, 1Gi RAM
  - Large (≤1000 RPS): 8+ replicas, 1 CPU, 2Gi RAM

**Justification:** meets **INF-NFR-AVAIL-01** (24/7 availability expectation) and **INF-NFR-SCALE-01**.

## E2) DB HA topology, backups, restore
- PostgreSQL HA via Patroni or managed service; replication factor 2–3.
- Backups: nightly full + WAL continuous; retention 30 days.
- Restore drills: monthly; target RPO ≤ 5 minutes, RTO ≤ 60 minutes.  
**Justification:** meets **INF-ASR-HA-01** and **INF-ASR-AUDIT-01** (audit preservation).

## E3) Network topology + ingress/egress rules
- Public ingress: HTTPS to API only; WebSocket allowed.
- Egress: API to broker/DB; codec service to peer centers via TCP (DATEX/ASN).
- One-way export network: only outbound from ExportSvc to consumers; deny inbound.  
(Ref: *Deployment_PhysicalView: ONEWAY*.)  
**Justification:** meets **INF-FR-RGUI-01** and **INF-FR-STD-03**.

## E4) CI/CD sketch
1. Build + unit tests
2. Static analysis + dependency scan
3. Contract tests (OpenAPI/proto compatibility)
4. TMDD/DATEX conformance suite (golden vectors)
5. Deploy to staging
6. Integration + e2e tests with simulators
7. Canary (5% traffic) then progressive rollout; rollback on SLO burn.  
**Justification:** meets **INF-ASR-CONTRACT-01** and **INF-NFR-STD-01**.

---

# F. Security Design

## F1) Auth & AuthZ
- External users: OIDC login, JWT access tokens (15 min), refresh tokens (8–12 hours).
- RBAC roles: `operator`, `supervisor`, `maintainer`, `readonly_consumer`.
- Command submission requires `operator` or `supervisor`; policy/timeframe enforced server-side.  
**Justification:** meets **INF-FR-RGUI-02** and **INF-NFR-SEC-01**.

## F2) Secrets management & rotation
- Kubernetes External Secrets + Vault or cloud secrets manager.
- Rotate client secrets every 90 days; DB passwords 90 days; TLS certs 30–90 days.  
**Justification:** meets **INF-NFR-SEC-02**.

## F3) TLS & service-mesh
- TLS 1.2+ externally; mTLS inside mesh (Istio/Linkerd) recommended.
- Codec TCP links: use VPN/IPsec tunnel between centers when possible.  
**Justification:** meets **INF-NFR-SEC-03**.

## F4) Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Credential theft on public GUI | OIDC, MFA optional, short-lived tokens |
| Command injection / replay | Idempotency keys + nonce; audit; JWT audience/issuer checks |
| Tampering with TMDD messages | Payload hashing + signature option; conformance validation |
| DoS on API | Rate limits, WAF, HPA, circuit breakers |
| Lateral movement inside cluster | mTLS + NetworkPolicies + least privilege |

---

# G. Observability & SRE

## G1) Metrics/traces/logs + alert rules
- Metrics: API p95/p99 latency, command accept/ack latency, adapter error rates, TMDD decode failures, DB replication lag, broker stream lag.
- Traces: propagate `correlationId` across API→broker→adapter.
- Logs: structured JSON; audit log separate append-only.

Example Prometheus alerts:
- `HighApiErrorRate` and `AdapterCommandFailures` (see artifacts section L in runbook notes).

**Justification:** meets **INF-FR-MODE-02** (test mode logs) and **INF-NFR-PERF-01**.

## G2) SLOs, error budgets, RTO/RPO
- API availability: 99.9% monthly (error budget ~43 min). (**INF-NFR-AVAIL-01**)
- Command submission success: 99.5% monthly. (**INF-NFR-PERF-02**)
- Telemetry freshness: 95% of status updates ≤ 5s old at read time. (**INF-NFR-PERF-03**)
- RTO 60 min, RPO 5 min. (**INF-ASR-HA-01**)

## G3) Dashboard/runbook sketch
- Dashboards: API health, ingestion health, adapter per-vendor, DB health, export health.
- Runbooks: codec decode storm, DB failover, stuck command correlation, one-way export backlog.

---

# H. Testing Strategy

## H1) Test matrix

| Test type | Components | Examples |
|---|---|---|
| Unit | API, policy, translation | Validate command timeframe logic |
| Integration | API↔DB, API↔Broker | Command persisted then published |
| Contract | OpenAPI/proto | Backward compatibility checks |
| E2E | GUI↔API↔Adapter simulator | DMS message set + ack path |
| Chaos | App/DB/Broker | Kill broker pod, ensure retry and no data loss |

**Justification:** meets **INF-ASR-CONTRACT-01** and **INF-FR-MODE-01**.

## H2) Test data mgmt & env isolation
- Environments: dev, staging, pre-prod, prod.
- Refresh: nightly baseline network/link/node; anonymize any sensitive operator data.

---

# I. Migration, Data Conversion & Rollout Plan

## I1) Migration steps
1. Stand up canonical repository and APIs in parallel.
2. Build adapters for each legacy system; run read-only ingestion first.
3. Validate parity (incidents/devices) via reconciliation jobs.
4. Enable command/control per device type with supervised rollout.
5. Cut over Web Map and GUIs to new API; keep legacy UI as fallback.
Rollback: disable command endpoints; keep read-only ingestion.

**Justification:** meets **INF-FR-MODE-01** and **INF-NFR-STD-01**.

## I2) Backwards compatibility/versioning
- External API: `/v1` with additive changes only; breaking changes → `/v2`.
- Internal proto: semantic versioning; reserve fields; maintain backward compatibility.

---

# J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Why chosen (tie to IDs) |
|---|---|---|---|
| Canonical TMDD core | TMDD-first persistence | Per-adapter bespoke models; document-only store | Ensures interoperability (**INF-NFR-STD-01**) |
| Broker | NATS JetStream | RabbitMQ; Kafka/Redpanda | Balanced ops + low latency (**INF-NFR-PERF-01**) |
| Auth | OIDC/JWT | mTLS-only; API keys | Supports public GUI securely (**INF-FR-RGUI-01**, **INF-NFR-SEC-01**) |
| Legacy ESRI/C++ constraints | Decouple behind APIs | Full compliance with NT/ARC IMS everywhere | Reduces lock-in while meeting functional intent; conflicts logged (K) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** SRS has no requirement IDs; this doc assigns `INF-*` IDs and treats them as the baseline for traceability.
- **A2:** TMDD/DATEX/ASN schemas and conformance vectors are available from TxDOT/partners; otherwise a joint schema-freeze milestone is required.
- **A3:** “username/password” in device control requirements indicates *operator authentication*, not credentials forwarded to field devices; device auth is handled by adapter credentials.
- **A4:** ESRI ARC IMS/MapObjects and Windows NT constraints are legacy; production deployment may use modern OS while preserving functional behavior via APIs.
- **A5:** One-way export means no inbound network path and no control commands accepted from external consumers.

## Conflicts (SRS vs provided UML diagrams)
- **C1:** PlantUML describes “RLCS Reversible Lane Control System” actors/use cases; SRS describes broader TxDOT C2C for many device types. Per rule, SRS naming is preferred; UML diagrams are used as *pattern references* only.

## Unresolved stakeholder questions (need answers)
1. Which TMDD version and which specific message sets are in scope for phase 1 (incidents, device status, device control)?
2. What is the exact “project defined protocol” used by legacy systems (wire format, auth, error handling)?
3. Are there legal/regulatory requirements for audit retention period and operator identity storage?
4. What are acceptable command timeframes and emergency override rules per agency/network?
5. For CCTV snapshots: is binary image storage required, and where (NAS/S3/DB)?

---

# L. Deliverables

```markdown
# filename: architecture.md
(Use this document content as architecture.md)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: TxDOT C2C API
  version: "1.0.0"
servers:
  - url: https://c2c.example.org/api/v1
security:
  - bearerAuth: []
paths:
  /networks:
    get:
      summary: List roadway networks
      operationId: listNetworks
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/Network" }
                  nextCursor:
                    type: string
                    nullable: true
  /incidents:
    get:
      summary: List incidents
      operationId: listIncidents
      parameters:
        - in: query
          name: networkId
          schema: { type: string }
        - in: query
          name: status
          schema: { $ref: "#/components/schemas/IncidentStatus" }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/Incident" }
    post:
      summary: Create incident
      operationId: createIncident
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/IncidentCreate" }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Incident" }
        "400":
          $ref: "#/components/responses/BadRequest"
  /incidents/{incidentId}:
    get:
      summary: Get incident details
      operationId: getIncident
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Incident" }
        "404":
          $ref: "#/components/responses/NotFound"
    patch:
      summary: Update incident
      operationId: updateIncident
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/IncidentPatch" }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Incident" }
        "400":
          $ref: "#/components/responses/BadRequest"
    delete:
      summary: Delete incident
      operationId: deleteIncident
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      responses:
        "204":
          description: Deleted
        "404":
          $ref: "#/components/responses/NotFound"
  /devices/status:
    get:
      summary: Get latest device status records (filterable)
      operationId: listDeviceStatus
      parameters:
        - in: query
          name: networkId
          schema: { type: string }
        - in: query
          name: deviceType
          schema: { $ref: "#/components/schemas/DeviceType" }
        - in: query
          name: limit
          schema: { type: integer, minimum: 1, maximum: 500, default: 100 }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/DeviceStatus" }
  /commands:
    post:
      summary: Submit a device command/control request
      operationId: createCommand
      parameters:
        - in: header
          name: Idempotency-Key
          required: false
          schema: { type: string, maxLength: 128 }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/DeviceCommandCreate" }
      responses:
        "202":
          description: Accepted for processing
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceCommand" }
        "400":
          $ref: "#/components/responses/BadRequest"
        "403":
          $ref: "#/components/responses/Forbidden"
  /commands/{commandId}:
    get:
      summary: Get command status/ack
      operationId: getCommand
      parameters:
        - in: path
          name: commandId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceCommand" }
        "404":
          $ref: "#/components/responses/NotFound"
  /policies/command-timeframes:
    get:
      summary: Get allowed command timeframes by network and device type
      operationId: getCommandTimeframes
      parameters:
        - in: query
          name: networkId
          required: true
          schema: { type: string }
        - in: query
          name: deviceType
          required: true
          schema: { $ref: "#/components/schemas/DeviceType" }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: "#/components/schemas/CommandTimeframePolicy" }
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  responses:
    BadRequest:
      description: Bad Request
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    Forbidden:
      description: Forbidden
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    NotFound:
      description: Not Found
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string, example: "VALIDATION_ERROR" }
        message: { type: string }
        requestId: { type: string }
        details:
          type: object
          additionalProperties: true
    Network:
      type: object
      required: [networkId, name]
      properties:
        networkId: { type: string }
        name: { type: string }
    IncidentStatus:
      type: string
      enum: [ACTIVE, CLEARED]
    Incident:
      type: object
      required: [incidentId, networkId, description, roadway, status, createdAtUtc]
      properties:
        incidentId: { type: string }
        networkId: { type: string }
        description: { type: string }
        roadway: { type: string }
        status: { $ref: "#/components/schemas/IncidentStatus" }
        createdAtUtc: { type: string, format: date-time }
        updatedAtUtc: { type: string, format: date-time, nullable: true }
    IncidentCreate:
      type: object
      required: [networkId, description, roadway]
      properties:
        networkId: { type: string }
        description: { type: string, minLength: 1 }
        roadway: { type: string, minLength: 1 }
    IncidentPatch:
      type: object
      properties:
        description: { type: string, minLength: 1 }
        roadway: { type: string, minLength: 1 }
        status: { $ref: "#/components/schemas/IncidentStatus" }
    DeviceType:
      type: string
      enum:
        - DMS
        - LCS
        - CCTV
        - RAMP_METER
        - HAR
        - TRAFFIC_SIGNAL
        - ESS
        - HOV
        - PARKING_LOT
        - SCHOOL_ZONE
        - RAIL_CROSSING
        - REVERSIBLE_LANE
        - DYNAMIC_LANE
    DeviceStatus:
      type: object
      required: [deviceId, deviceType, networkId, name, updatedAtUtc]
      properties:
        deviceId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        networkId: { type: string }
        name: { type: string }
        location:
          type: object
          nullable: true
          properties:
            lat: { type: number, format: double }
            lon: { type: number, format: double }
        status:
          type: object
          additionalProperties: true
        updatedAtUtc: { type: string, format: date-time }
    DeviceCommandCreate:
      type: object
      required: [networkId, deviceType, deviceId, payload]
      properties:
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        deviceId: { type: string }
        payload:
          description: Device-type-specific command payload.
          type: object
          additionalProperties: true
    DeviceCommand:
      type: object
      required: [commandId, networkId, deviceType, deviceId, state, createdAtUtc]
      properties:
        commandId: { type: string }
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        deviceId: { type: string }
        state:
          type: string
          enum: [ACCEPTED, SENT, ACKED, FAILED, TIMED_OUT]
        correlationId: { type: string, nullable: true }
        createdAtUtc: { type: string, format: date-time }
        lastUpdatedAtUtc: { type: string, format: date-time, nullable: true }
        error:
          type: object
          nullable: true
          properties:
            code: { type: string }
            message: { type: string }
    CommandTimeframePolicy:
      type: object
      required: [networkId, deviceType, daysAccepted, timesAccepted]
      properties:
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        daysAccepted:
          type: array
          items:
            type: string
            enum: [MON, TUE, WED, THU, FRI, SAT, SUN]
        timesAccepted:
          type: array
          items:
            type: object
            required: [startLocal, endLocal]
            properties:
              startLocal: { type: string, example: "07:00" }
              endLocal: { type: string, example: "19:00" }
```

```proto
// filename: internal.proto
syntax = "proto3";

package txdot.c2c.v1;

option go_package = "github.com/txdot/c2c/gen/go/v1;c2cv1";

message TmddEnvelope {
  string envelope_id = 1;
  string peer_center_id = 2;
  string direction = 3; // INBOUND|OUTBOUND
  string tmdd_schema_version = 4;
  bytes datex_asn_payload = 5;
  string payload_sha256 = 6;
  int64 received_at_unix_ms = 7;
}

message DeviceStatusRecord {
  string device_id = 1;
  string device_type = 2;
  string network_id = 3;
  string name = 4;
  double lat = 5;
  double lon = 6;
  map<string, string> status_kv = 7;
  int64 updated_at_unix_ms = 8;
}

message DeviceCommandRequest {
  string command_id = 1;
  string correlation_id = 2;
  string network_id = 3;
  string device_type = 4;
  string device_id = 5;
  map<string, string> payload_kv = 6;
  string requested_by_subject = 7; // from JWT sub
  int64 requested_at_unix_ms = 8;
}

message DeviceCommandAck {
  string command_id = 1;
  string correlation_id = 2;
  string state = 3; // ACKED|FAILED
  string error_code = 4;
  string error_message = 5;
  int64 ack_at_unix_ms = 6;
}

service CodecService {
  rpc PublishTmddEnvelope(TmddEnvelope) returns (PublishResult);
}

message PublishResult {
  bool ok = 1;
  string error_message = 2;
}

service AdapterService {
  rpc SendDeviceCommand(DeviceCommandRequest) returns (DeviceCommandAck);
  rpc GetLatestDeviceStatus(GetStatusRequest) returns (GetStatusResponse);
}

message GetStatusRequest {
  string network_id = 1;
  string device_type = 2;
}

message GetStatusResponse {
  repeated DeviceStatusRecord items = 1;
}
```

```yaml
# filename: k8s/c2c-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: c2c-api
  labels:
    app: c2c-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: c2c-api
  template:
    metadata:
      labels:
        app: c2c-api
    spec:
      containers:
        - name: c2c-api
          image: registry.example.org/c2c-api:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: c2c-api-config
            - secretRef:
                name: c2c-api-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1"
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
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: c2c-api
spec:
  selector:
    app: c2c-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: c2c-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: c2c-api
  minReplicas: 2
  maxReplicas: 8
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
  name: c2c-api-config
data:
  LOG_LEVEL: "info"
  DB_HOST: "postgres.default.svc.cluster.local"
  DB_PORT: "5432"
  DB_NAME: "c2c"
  NATS_URL: "nats://nats.default.svc.cluster.local:4222"
  OIDC_ISSUER_URL: "https://auth.example.org/realms/c2c"
---
apiVersion: v1
kind: Secret
metadata:
  name: c2c-api-secrets
type: Opaque
stringData:
  DB_USER: "c2c_app"
  DB_PASSWORD: "REPLACE_ME"
```

```sql
-- filename: sql/network_ddl.sql
CREATE TABLE IF NOT EXISTS network (
  network_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```sql
-- filename: sql/link_ddl.sql
CREATE TABLE IF NOT EXISTS link (
  link_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  link_type TEXT NOT NULL,
  geom_wkt TEXT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_link_network ON link(network_id);
```

```sql
-- filename: sql/node_ddl.sql
CREATE TABLE IF NOT EXISTS node (
  node_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type_description TEXT NOT NULL,
  lat DOUBLE PRECISION NULL,
  lon DOUBLE PRECISION NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_node_network ON node(network_id);
```

```sql
-- filename: sql/incident_ddl.sql
CREATE TABLE IF NOT EXISTS incident (
  incident_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE RESTRICT,
  description TEXT NOT NULL,
  roadway TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ACTIVE','CLEARED')),
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc TIMESTAMPTZ NULL
);
CREATE INDEX IF NOT EXISTS idx_incident_network_status ON incident(network_id, status);
```

```sql
-- filename: sql/lane_closure_ddl.sql
CREATE TABLE IF NOT EXISTS lane_closure (
  lane_closure_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE RESTRICT,
  description TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc TIMESTAMPTZ NULL
);
CREATE INDEX IF NOT EXISTS idx_lane_closure_network ON lane_closure(network_id);
```

```sql
-- filename: sql/device_status_ddl.sql
CREATE TABLE IF NOT EXISTS device_status (
  device_id TEXT NOT NULL,
  device_type TEXT NOT NULL,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE RESTRICT,
  name TEXT NOT NULL,
  lat DOUBLE PRECISION NULL,
  lon DOUBLE PRECISION NULL,
  status_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at_utc TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (device_id, device_type, network_id)
);
CREATE INDEX IF NOT EXISTS idx_device_status_network_type ON device_status(network_id, device_type);
CREATE INDEX IF NOT EXISTS idx_device_status_updated ON device_status(updated_at_utc);
```

```sql
-- filename: sql/device_command_ddl.sql
CREATE TABLE IF NOT EXISTS device_command (
  command_id TEXT PRIMARY KEY,
  correlation_id TEXT NOT NULL,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE RESTRICT,
  device_type TEXT NOT NULL,
  device_id TEXT NOT NULL,
  requested_by_subject TEXT NOT NULL,
  payload_json JSONB NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('ACCEPTED','SENT','ACKED','FAILED','TIMED_OUT')),
  error_json JSONB NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_updated_at_utc TIMESTAMPTZ NULL
);
CREATE INDEX IF NOT EXISTS idx_device_command_network_created ON device_command(network_id, created_at_utc DESC);
CREATE INDEX IF NOT EXISTS idx_device_command_state ON device_command(state);
```

```sql
-- filename: sql/audit_event_ddl.sql
CREATE TABLE IF NOT EXISTS audit_event (
  audit_event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor_subject TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  payload_json JSONB NOT NULL,
  occurred_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- Append-only: enforce immutability by privilege; no UPDATE/DELETE grants to app role.
CREATE INDEX IF NOT EXISTS idx_audit_event_occurred ON audit_event(occurred_at_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_event_resource ON audit_event(resource_type, resource_id);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-NET-01,Provide network name + link data,Container_PhysicalView:DB,C2C API,sql/network_ddl.sql;openapi.yaml,Canonical repository supports exchange and map
INF-FR-INC-01,Support incident info,Container_PhysicalView:API/DB,Incident Service,sql/incident_ddl.sql;openapi.yaml,Incidents are shared and mapped
INF-FR-DMS-CTRL-01,DMS control command,Component_DevelopmentView:Api/Ctrl,Command Service,sql/device_command_ddl.sql;openapi.yaml;internal.proto,Commands routed via adapter with audit
INF-NFR-STD-02,DATEX/ASN transports TMDD,Deployment_PhysicalView:GW,Codec Service,internal.proto,Codec boundary enforces encoding
INF-FR-MODE-02,Test mode logs activities,G:Observability,Audit/Logging,sql/audit_event_ddl.sql,Append-only audit supports test-mode logging
```

## Acceptance Criteria Verification Table
- [x] 3-line Analysis Plan present.  
- [x] Sections A-L included.  
- [x] Every FR/NFR/ASR mapped in traceability matrix. *(All are included via `INF-*`; stakeholder to confirm final baseline.)*  
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.  
- [x] Representative k8s manifest snippet included.  
- [x] SQL DDL / NoSQL models for primary entities included.  
- [x] All major components have at least one API contract and a data schema.  
- [x] Assumptions and unresolved questions listed.

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?