Analysis Plan  
Scope: Production-ready architecture for TxDOT-style C2C network: TMDD/DATEX/ASN over TCP/IP, repository, map UI, incident GUI, remote control GUI, adapters, security, ops.  
Approach: 4+1 views aligned to provided 11 UML diagrams; microkernel + adapter/broker; contract-first APIs; SQL canonical store; Windows/ESRI constraints with Kubernetes-ready option.  
Top validation steps: Requirements→traceability matrix completeness; API/DDL/k8s syntax validation; security/audit controls + performance (2s status) verification against diagrams and inferred IDs.

# A. Executive Summary (≤1 page)

## System overview
The Center-to-Center (C2C) Communications Network interconnects dissimilar Traffic Management Centers (TMCs) by translating “system-specific” formats into ITS standards (TMDD message sets transmitted via DATEX/ASN over TCP/IP), storing canonical traffic data in a shared repository, and exposing capabilities for: (1) map visualization of speeds/incidents, (2) incident/lane-closure entry and management, and (3) remote device command/control with status feedback.

**Primary diagram mapping (one-line):** End-to-end behavior is captured by *UseCase_ScenarioView (UC_IssueDeviceCommand, UC_ViewMap, UC_EnterIncident)*, *Sequence_ProcessView_S1_IssueDeviceCommand*, *Sequence_ProcessView_S2_ViewMapAndIncidents*, and *Deployment_PhysicalView*.

## Architectural style(s) and deployment topology
- **Architectural style:** Microkernel runtime with plug-in adapters + broker, contract-enforced boundaries, canonical domain model (ref: *Package_DevelopmentView: pkg_kernel, pkg_integ*; *Component_DevelopmentView: MicrokernelRuntime, AdapterBroker*).  
- **Deployment topology:** DMZ API Gateway → App Tier services → Relational repository + ESRI map server + external peer/legacy centers (ref: *Deployment_PhysicalView: DMZ, AppTier, DB, EsriArcIMS, ExtSystems*).

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| Legacy platform constraints (Windows NT + ESRI ARC IMS/Map Objects + DATEX/ASN runtime) limit modernization | Security patching, TLS/mTLS support, CI/CD friction | Introduce “runtime gatekeeper” checks at startup; isolate legacy UI components; keep core services upgradeable; document supported version ranges and phased uplift plan (INF-PLAT-01). |
| Interoperability drift across centers (TMDD versions, vendor-specific fields) | Data loss, command failures | Contract-first schemas + version negotiation; adapter conformance tests; reject/ quarantine invalid payloads with explicit error codes (ref: *Class_LogicView: TMDDCodec.validateSchema/negotiateVersion*). |
| Remote command/control security (password fields, public network GUI) | Unauthorized control, credential leakage | mTLS for command endpoints, RBAC claims, secret redaction, immutable audit chain, lockout/MFA policy (ref: *State_LogicView_DeviceCommandLifecycle*, *Activity_ProcessView_RemoteDeviceCommand*). |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality attribute | ASR/NFR IDs | Test types |
|---|---|---|
| Scalability | INF-PERF-01 (ingest), INF-PERF-02 (map query) | Load + soak tests; DB index benchmarks; HPA tests |
| Availability | INF-AVAIL-01 (HA), ASR-006 (sync cadence) | Failover drills; chaos tests; backup/restore tests |
| Security | NFR-004 (auth policy), NFR-006 (mTLS/redaction), NFR-003 (TLS) | SAST/DAST; mTLS negative tests; RBAC tests; audit integrity tests |
| Performance | FR-070 (2s status display), NFR-010/011 (test-mode overhead) | Latency SLIs; profiling; log-overhead A/B tests |
| Maintainability | ASR-005 (building blocks), ASR-001/002 (heterogeneous integration) | Adapter contract tests; plugin lifecycle tests; upgrade tests |

---

# B. Traceability & Rationale

## Notes on requirement IDs
The provided “Original Requirements” text does not include explicit FR/NFR/ASR identifiers. Per special handling rule #1, IDs are inferred as `INF-###` and listed in Section K.

## Traceability matrix (CSV/table)
(Also delivered as `traceability_matrix.csv` in Section L.)

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-001 | Provide network name and link data per roadway network | Class_LogicView: Network/Topology/Link/Node | TrafficRepository, MapService | sql/network_ddl.sql; sql/link_ddl.sql; openapi.yaml | Canonical topology entities enable map rendering and cross-center sharing. |
| INF-002 | Provide link info: id, name, type | Class_LogicView: Link | MapService, TrafficRepository | sql/link_ddl.sql; openapi.yaml | Link attributes are required for basemap overlay and speed coloring. |
| INF-003 | Provide node info: id, name, type description | Class_LogicView: Node | TrafficRepository | sql/node_ddl.sql | Nodes support topology completeness and future routing/analytics. |
| INF-004 | Support incident info: network id, description, roadway | Class_LogicView: Incident; Sequence_ProcessView_S2_ViewMapAndIncidents | IncidentService, TrafficRepository | sql/incident_ddl.sql; openapi.yaml | Incidents are stored and served to map and tables. |
| INF-005 | Support lane closure info: network id, id, description | Class_LogicView: LaneClosure | IncidentService, TrafficRepository | sql/lane_closure_ddl.sql; openapi.yaml | Lane closures are managed similarly to incidents with separate lifecycle. |
| INF-006 | DMS status: network id, DMS id, DMS name | Class_LogicView: DMS; UseCase_ScenarioView: UC_ViewDeviceStatus | DeviceStatusService, Adapters | sql/device_ddl.sql; openapi.yaml | Device status is normalized into Device table with subtype fields. |
| INF-007 | DMS control command includes network id, DMS id, username/password | Sequence_ProcessView_S1_IssueDeviceCommand; State_LogicView_DeviceCommandLifecycle | DeviceCommandService, SecurityGateway, Adapters | sql/device_command_ddl.sql; openapi.yaml | Commands are validated, authorized, audited, and routed to adapters. |
| INF-008 | LCS status: id, name, location, status | Class_LogicView: LCS | DeviceStatusService | sql/device_ddl.sql | LCS is a Device subtype with lane assignment metadata. |
| INF-009 | LCS control includes username/password | Sequence_ProcessView_S1_IssueDeviceCommand | DeviceCommandService, SecurityGateway | openapi.yaml | Same command pipeline; deviceType=LCS. |
| INF-010 | CCTV status: id, name, location, status | Class_LogicView: CCTV | DeviceStatusService | sql/device_ddl.sql | CCTV status supports map display and remote selection. |
| INF-011 | CCTV control request includes username/password | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Unified command endpoint supports CCTV operations. |
| INF-012 | Video snapshots status: CCTV id/name/status | UseCase_ScenarioView: UC_ViewDeviceStatus | DeviceStatusService | openapi.yaml | Snapshot metadata is exposed as status extension. |
| INF-013 | CCTV switching command includes video channel input id + credentials | Class_LogicView: CCTV.videoChannelInputId; Sequence S1 | DeviceCommandService, Adapters | openapi.yaml; internal.proto | Switching modeled as operation with payload. |
| INF-014 | Ramp meter status and control (plan) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceStatusService, DeviceCommandService | openapi.yaml; sql/device_ddl.sql | Plan-based control is represented in command payload schema. |
| INF-015 | HAR status and control (message) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | HAR message is a command payload variant. |
| INF-016 | Traffic signal status and control (plan id) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Signal plan selection is a command payload variant. |
| INF-017 | ESS status | Class_LogicView: Device (ESS as type) | DeviceStatusService | sql/device_ddl.sql | ESS stored as deviceType=ESS with type field. |
| INF-018 | HOV status and control (plan) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | HOV plan is a command payload variant. |
| INF-019 | Parking lot status and capacity | Class_LogicView: Device (ParkingLot as type) | DeviceStatusService | sql/device_ddl.sql | Capacity stored in device_ext JSON. |
| INF-020 | School zone status and control (plan) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | School zone plan is a command payload variant. |
| INF-021 | Railroad crossing status | Class_LogicView: Device (RailCrossing as type) | DeviceStatusService | sql/device_ddl.sql | Crossing status stored as deviceType=RAIL_CROSSING. |
| INF-022 | Reversible lane status and control (plan, duration) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Duration included in payload schema. |
| INF-023 | Dynamic lane status and control (lane plan) | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Dynamic lane plan included in payload schema. |
| INF-024 | Bus stop status | Class_LogicView: Device (BusStop as type) | DeviceStatusService | sql/device_ddl.sql | Transit assets stored as deviceType=BUS_STOP. |
| INF-025 | Bus location status + schedule adherence | Class_LogicView: Device (BusLocation as type) | DeviceStatusService | sql/device_ddl.sql | Location + adherence stored in device_ext JSON. |
| INF-026 | Light/commuter stop status + routes | Class_LogicView: Device (RailStop as type) | DeviceStatusService | sql/device_ddl.sql | Routes stored in device_ext JSON array. |
| INF-027 | Light/commuter location status + schedule adherence | Class_LogicView: Device (RailVehicle as type) | DeviceStatusService | sql/device_ddl.sql | Vehicle location stored as deviceType=RAIL_VEHICLE. |
| INF-028 | Park and ride lot status + capacity | Class_LogicView: Device (ParkRide as type) | DeviceStatusService | sql/device_ddl.sql | Capacity stored in device_ext JSON. |
| INF-029 | Vehicle priority status (vehicle id, link, intersection) | Class_LogicView: Device (VehiclePriority as type) | DeviceStatusService | sql/device_ddl.sql | Priority events stored as deviceType=VEHICLE_PRIORITY. |
| INF-030 | Network device status summary (counts + status data) | UseCase_ScenarioView: UC_ViewDeviceStatus | DeviceStatusService | openapi.yaml | Summary endpoint aggregates by deviceType and status. |
| INF-031 | Command timeframe request: network id + device type | Class_LogicView: CommandTimeframe | DeviceCommandService | sql/command_timeframe_ddl.sql; openapi.yaml | Timeframe rules enforce when commands are accepted. |
| INF-032 | Command timeframe response includes days/times accepted | Class_LogicView: CommandTimeframe.daysAccepted/timesAccepted | DeviceCommandService | openapi.yaml | Returned to GUI to guide operator and validation. |
| INF-033 | Data Collector stores TMDD data elements/message sets | Package_DevelopmentView: pkg_persist/pkg_domain | TrafficRepository | sql/*; internal.proto | Canonical storage supports TMDD message persistence and replay. |
| INF-034 | Use TMDD standard message sets | Class_LogicView: TMDDCodec | TMDDCodec, Adapters | internal.proto | Codec enforces TMDD schema and version negotiation. |
| INF-035 | DATEX/ASN used to transmit TMDD message sets | Component_DevelopmentView: TMDDCodec | TMDDCodec | internal.proto | Encoding/decoding boundary is centralized in codec. |
| INF-036 | TCP/IP used to transmit DATEX/ASN | Deployment_PhysicalView: AppTier→ExtSystems | Adapters | internal.proto | Transport is TCP/IP with TLS; adapter owns socket lifecycle. |
| INF-037 | Web Map app generates map for Internet WWW server | Deployment_PhysicalView: Browser/DMZ | WebMapUI, MapService | openapi.yaml | Web UI consumes map overlay APIs and renders via ESRI. |
| INF-038 | Map shows traffic conditions graphically | Sequence_ProcessView_S2_ViewMapAndIncidents | MapService, MapRenderService | openapi.yaml | Link speeds + thresholds produce colored overlays. |
| INF-039 | Map displays interstates and state highways | Sequence S2; Deployment: NCTCOG | NCTCOGGeoDataClient, ESRI | openapi.yaml | Basemap source provides road layers. |
| INF-040 | Basemap derived from NCTCOG GeoData warehouse | UseCase_ScenarioView: NCTCOGGeoData→UC_ViewMap | NCTCOGGeoDataClient | openapi.yaml | Basemap client fetches tiles/features from NCTCOG. |
| INF-041 | Map user can zoom | UseCase_ScenarioView: UC_ViewMap | WebMapUI | openapi.yaml | Viewport/zoom parameters supported by map endpoint. |
| INF-042 | Map user can pan N/S/E/W | UseCase_ScenarioView: UC_ViewMap | WebMapUI | openapi.yaml | Viewport bounding box supports panning. |
| INF-043 | Links color-coded by speeds | Sequence S2: MapRenderService.colorCodeLinks | MapRenderService | openapi.yaml | Speed thresholds config drives styling. |
| INF-044 | Config file specifies speed values | Sequence S2: thresholdsYaml | MapService | architecture.md | ConfigMap-mounted YAML used by MapRenderService. |
| INF-045 | Map displays current incidents as icons | Sequence S2: renderMap(incidentIcons) | MapService | openapi.yaml | Incidents returned as geo points for icon overlay. |
| INF-046 | Click incident icon for more info | Sequence S2: incidentDrilldown | IncidentService, SecurityGateway | openapi.yaml | Drilldown endpoint returns details with RBAC. |
| INF-047 | Incidents displayed in tabular format | UseCase_ScenarioView: UC_ViewIncidents | IncidentService | openapi.yaml | List endpoint supports table rendering. |
| INF-048 | Map can display DMS/LCS/CCTV | UseCase_ScenarioView: UC_ViewMap includes UC_ViewDeviceStatus | DeviceStatusService | openapi.yaml | Device status endpoint supports map overlays. |
| INF-049 | Incident GUI allows entry without a Center | UseCase_ScenarioView: UC_EnterIncident | IncidentGUI, IncidentService | openapi.yaml | GUI posts directly to C2C API. |
| INF-050 | Incident GUI inputs incident fields | Class_LogicView: Incident | IncidentService | sql/incident_ddl.sql; openapi.yaml | Schema enforces required fields. |
| INF-051 | Incident GUI inputs lane closure fields | Class_LogicView: LaneClosure | IncidentService | sql/lane_closure_ddl.sql; openapi.yaml | Separate endpoint and table. |
| INF-052 | GUI lists previously entered incidents | UseCase_ScenarioView: UC_ViewIncidents | IncidentService | openapi.yaml | List endpoint supports pagination/filtering. |
| INF-053 | GUI modifies incident | UseCase_ScenarioView: UC_ModifyIncident | IncidentService | openapi.yaml | PUT/PATCH endpoint updates incident. |
| INF-054 | GUI deletes incident | UseCase_ScenarioView: UC_DeleteIncident | IncidentService, SecurityGateway | openapi.yaml | Delete requires elevated claim. |
| INF-055 | GUI lists lane closures | UseCase_ScenarioView: UC_ViewIncidents | IncidentService | openapi.yaml | Lane closure list endpoint. |
| INF-056 | GUI deletes lane closure | UseCase_ScenarioView: UC_EnterLaneClosure/UC_DeleteIncident (admin) | IncidentService | openapi.yaml | Delete endpoint for lane closures. |
| INF-057 | Remote Center Control GUI runs on public network | Deployment_PhysicalView: RemotePC via Internet | RemoteControlGUI, APIGateway | openapi.yaml | Public ingress requires TLS and hardened auth. |
| INF-058 | Remote GUI prompts username/password at start | Activity_ProcessView_RemoteDeviceCommand | AuthService | openapi.yaml | Login endpoint issues session token. |
| INF-059 | User selects network identifier for command | Activity_ProcessView_RemoteDeviceCommand | DeviceCommandService | openapi.yaml | networkId is required in command request. |
| INF-060 | Select DMS and provide message + beacons | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Payload schema supports DMS message + beacons. |
| INF-061 | Select LCS and lane arrows assignment | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Payload schema supports lane assignment. |
| INF-062 | Issue CCTV switching command source/destination | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Payload schema supports switching fields. |
| INF-063 | Select CCTV and provide info | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | CCTV operations modeled as command operations. |
| INF-064 | Select ramp meter and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Plan field in payload. |
| INF-065 | Select HAR and text | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Message field in payload. |
| INF-066 | Select traffic signal and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Plan id in payload. |
| INF-067 | Select HOV and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Plan in payload. |
| INF-068 | Select school zone and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Plan in payload. |
| INF-069 | Select reversible lane and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Plan in payload. |
| INF-070 | Select dynamic lane and plan | UseCase_ScenarioView: UC_IssueDeviceCommand | DeviceCommandService | openapi.yaml | Lane plan in payload. |
| INF-071 | Display command/control status in scrollable list | UseCase_ScenarioView: UC_ViewDeviceStatus; Sequence S1 | RemoteControlGUI | openapi.yaml | Command response includes status and is queryable. |
| INF-072 | C2C Server executes in Microsoft Windows NT environment | Deployment_PhysicalView: AppTier Windows | All services | architecture.md | Platform constraint drives build/runtime choices. |
| INF-073 | DATEX/ASN runtime library available on any communicating computer | Deployment_PhysicalView: Codec artifact | TMDDCodec, Adapters | architecture.md | Gatekeeper checks runtime presence. |
| INF-074 | Web server uses ESRI ARC IMS for map images | Deployment_PhysicalView: EsriArcIMS | MapRenderService | architecture.md | ESRI constraint dictates map rendering integration. |
| INF-075 | C2C implemented in C/C++ | Package_DevelopmentView note | Core services, adapters | architecture.md | Language constraint drives implementation and libraries. |
| INF-076 | Web interface implemented using C/C++ and ESRI ARC IMS | Package_DevelopmentView: pkg_ui | WebMapUI, MapService | architecture.md | UI integration must match ESRI stack. |
| INF-077 | Incident GUI implemented using C/C++ and ESRI Map Objects | Package_DevelopmentView: pkg_ui | IncidentGUI | architecture.md | Desktop GUI constraint. |
| INF-078 | Remote Control GUI implemented using C/C++ and ESRI Map Objects | Package_DevelopmentView: pkg_ui | RemoteControlGUI | architecture.md | Desktop GUI constraint. |
| INF-079 | Normal mode: receive from all systems and combine into single datastore | Deployment_PhysicalView; Component_DevelopmentView: TrafficRepositoryDB | MicrokernelRuntime, Adapters, Repository | internal.proto; sql/* | Ingest pipeline writes canonical store. |
| INF-080 | Test mode: normal mode + logs activities | Activity_ProcessView_RemoteDeviceCommand; Deployment note | Observability stack | architecture.md | Test-mode toggles verbose logging with bounded overhead. |
| INF-SEC-001 | TLS 1.2+ for external interfaces (inferred from diagrams) | Component_DevelopmentView note: APIGateway | APIGateway | openapi.yaml; k8s/* | Transport security is required for public network access. |
| INF-SEC-002 | mTLS for password-field endpoints (inferred from diagrams) | State_LogicView_DeviceCommandLifecycle note | APIGateway, SecurityGateway | openapi.yaml | Prevent credential interception and enforce client identity. |
| INF-SEC-003 | Password policy + lockout + MFA (inferred from diagrams) | Activity_ProcessView_RemoteDeviceCommand | AuthService | openapi.yaml; sql/user_account_ddl.sql | Meets operator authentication requirements for public network GUI. |
| INF-AUD-001 | Immutable hash-chained audit log (inferred from diagrams) | Class_LogicView: AuditEvent | AuditLog, TrafficRepository | sql/audit_event_ddl.sql | Ensures non-repudiation and tamper evidence. |
| INF-SYNC-001 | Repository sync local→regional→statewide (inferred) | UseCase_ScenarioView: UC_SyncRepositories | SyncService (future) | internal.proto | Supports scalable federation of repositories. |

---

# C. Architecture Overview

## 4+1 view alignment

### Scenario (Use Case) view
Key user/system interactions are defined in *UseCase_ScenarioView*:
- Map viewing and incident drilldown: `UC_ViewMap`, `UC_ViewIncidents`, `UC_IncidentDrilldown`
- Incident/lane closure entry and management: `UC_EnterIncident`, `UC_EnterLaneClosure`, `UC_ModifyIncident`, `UC_DeleteIncident`
- Remote device command/control and status: `UC_IssueDeviceCommand`, `UC_ViewDeviceStatus`
- Cross-center sync: `UC_SyncRepositories`
- Security: `UC_AuthenticateUser`, `UC_AuthorizeAction`

### Logical view (domain + retained data)
The canonical model is shown in *Class_LogicView*:
- Topology: `Network`, `Topology`, `Link`, `Node`
- Events: `Incident`, `LaneClosure`
- Devices: `Device` with subtypes `DMS`, `LCS`, `CCTV` (and additional device types represented via `deviceType` + extension fields)
- Control: `DeviceCommand`, `CommandTimeframe`
- Security/audit: `UserAccount`, `AuthSession`, `AuditEvent`
- Integration boundary: `IExternalTrafficSystemAdapter`, `TMDDCodec`, `SecurityGateway`

### Process view (runtime behavior)
- Remote command flow: *Activity_ProcessView_RemoteDeviceCommand* and *Sequence_ProcessView_S1_IssueDeviceCommand*.
- Map + incident drilldown: *Sequence_ProcessView_S2_ViewMapAndIncidents*.
- Command lifecycle: *State_LogicView_DeviceCommandLifecycle*.

### Development view (code organization)
- *Package_DevelopmentView* defines module boundaries: `ui`, `api`, `kernel`, `domain`, `persistence`, `integration`, `security`.
- *Component_DevelopmentView* defines deployable components and interfaces: `APIGateway`, `AuthService`, `IncidentService`, `DeviceStatusService`, `DeviceCommandService`, `MapService`, `MicrokernelRuntime`, `AdapterBroker`, `TMDDCodec`, `TrafficRepositoryDB`, `AuditLog`.

### Physical/Deployment view
- *Deployment_PhysicalView* and *Container_PhysicalView* define: public clients → DMZ gateway → app tier services → DB + ESRI map server + external systems over TMDD/DATEX/ASN/TCP/IP.

---

# D. Detailed Technical Design (developer-facing)

## D1. API Gateway (DMZ Reverse Proxy)

### 1) Responsibilities & data ownership
Terminates external TLS, enforces mTLS on sensitive endpoints, rate-limits, routes requests to internal services, and standardizes error responses. Owns no business data.

### 2) Technology options (3+ per concern)
- **Language/runtime**
  - Recommended: NGINX 1.24+ or Envoy 1.29+ (native)  
  - Conservative: IIS ARR (Windows-native)  
  - Cutting-edge: Cilium Gateway API (K8s-native)
- **Web framework**
  - Recommended: N/A (proxy config)  
  - Conservative: IIS modules  
  - Cutting-edge: WASM filters (Envoy)
- **RPC/HTTP**
  - Recommended: HTTP/1.1 + HTTP/2 upstream  
  - Conservative: HTTP/1.1 only  
  - Cutting-edge: gRPC-web for browser clients
- **Persistence**
  - Recommended: none  
  - Conservative: none  
  - Cutting-edge: none
- **Cache**
  - Recommended: proxy cache for basemap/tiles (if allowed)  
  - Conservative: no cache  
  - Cutting-edge: CDN integration
- **Messaging**
  - Recommended: none  
  - Conservative: none  
  - Cutting-edge: none
- **Search**
  - Recommended: none  
  - Conservative: none  
  - Cutting-edge: none
- **Authn/Authz**
  - Recommended: validate JWT access tokens; enforce mTLS for `/commands`  
  - Conservative: session cookies (server-side)  
  - Cutting-edge: SPIFFE/SPIRE identities
- **Observability**
  - Recommended: access logs + OpenTelemetry tracing headers pass-through  
  - Conservative: access logs only  
  - Cutting-edge: eBPF L7 metrics
- **CI/CD**
  - Recommended: config lint + integration tests  
  - Conservative: manual change control  
  - Cutting-edge: GitOps (Argo CD)
- **Container runtime**
  - Recommended: containerd 1.7+  
  - Conservative: Windows containers (if IIS)  
  - Cutting-edge: gVisor (Linux-only)
- **Infra provisioning**
  - Recommended: Terraform 1.6+  
  - Conservative: manual VM provisioning  
  - Cutting-edge: Crossplane

### 3) Recommended default stack
- **Envoy 1.29–1.31** in DMZ, with mTLS client cert validation for command endpoints.  
Justification: meets INF-SEC-001 (TLS 1.2+) and INF-SEC-002 (mTLS for password-field endpoints).

### 4) Interface design
See `openapi.yaml` (Section L) for external API surface.

### 5) Data model / schema
None.

### 6) Caching & consistency
Cache only non-sensitive GET responses (e.g., map overlays) with short TTL (5–15s) to reduce load; never cache auth or command endpoints.

---

## D2. AuthService + SecurityGateway

### 1) Responsibilities & data ownership
Authenticates users (RemoteControlOperator, IncidentOperator/Admin), issues tokens/sessions, enforces password policy, lockout, optional MFA, and RBAC claims. Owns `UserAccount`, `AuthSession`, and writes `AuditEvent` for auth events.

### 2) Technology options
- **Language/runtime**
  - Recommended: C++17 (MSVC 2019/2022) service  
  - Conservative: C (Win32 service)  
  - Cutting-edge: Rust 1.75+ (if allowed)
- **Web framework**
  - Recommended: cpp-httplib 0.15+ or Boost.Beast 1.83+  
  - Conservative: ISAPI/IIS native module  
  - Cutting-edge: gRPC C++ 1.60+
- **RPC/HTTP**
  - Recommended: REST over HTTPS  
  - Conservative: SOAP (legacy)  
  - Cutting-edge: gRPC with mTLS
- **Persistence**
  - Recommended: PostgreSQL 14–15  
  - Conservative: SQL Server 2019 (Windows-aligned)  
  - Cutting-edge: CockroachDB 23+ (multi-region)
- **Cache**
  - Recommended: Redis 7.2+ for token revocation list (optional)  
  - Conservative: in-DB revocation table  
  - Cutting-edge: OPA sidecar cache
- **Messaging**
  - Recommended: none (sync)  
  - Conservative: none  
  - Cutting-edge: NATS for auth events
- **Search**
  - Recommended: none  
  - Conservative: none  
  - Cutting-edge: none
- **Authn/Authz**
  - Recommended: JWT access tokens + refresh tokens; RBAC claims  
  - Conservative: server-side sessions only  
  - Cutting-edge: OIDC provider integration (Keycloak 24+)
- **Observability**
  - Recommended: structured logs + audit events + metrics (login failures)  
  - Conservative: Windows Event Log only  
  - Cutting-edge: full OTel traces
- **CI/CD**
  - Recommended: unit tests + SAST + dependency scanning  
  - Conservative: manual builds  
  - Cutting-edge: supply-chain signing (SLSA)
- **Container runtime**
  - Recommended: Linux containers (if decoupled) or Windows service on VM  
  - Conservative: VM only  
  - Cutting-edge: K8s with Windows nodes
- **Infra provisioning**
  - Recommended: Terraform + Ansible  
  - Conservative: manual  
  - Cutting-edge: GitOps

### 3) Recommended default stack
- **C++17 + Boost.Beast + PostgreSQL 14–15 + JWT (RS256) + optional TOTP MFA**.  
Justification: meets INF-072 (Windows NT environment constraint) and INF-SEC-003 (password/lockout/MFA).

### 4) Interface design
Covered in `openapi.yaml` (`/auth/login`, `/auth/refresh`, `/auth/logout`).

### 5) Data model / schema
See `sql/user_account_ddl.sql`, `sql/auth_session_ddl.sql`, `sql/audit_event_ddl.sql`.

### 6) Caching & consistency
Cache public keys/JWKS in gateway; store refresh token hashes in DB; revocation is strongly consistent (DB transaction).

---

## D3. IncidentService (Incidents + Lane Closures)

### 1) Responsibilities & data ownership
CRUD for incidents and lane closures, list/query for map and tables, and RBAC enforcement for delete/modify. Owns `Incident` and `LaneClosure` records.

### 2) Technology options
- **Language/runtime**
  - Recommended: C++17  
  - Conservative: C  
  - Cutting-edge: Go 1.22+
- **Web framework**
  - Recommended: Pistache 0.0.5+ or Boost.Beast  
  - Conservative: CGI/IIS  
  - Cutting-edge: gRPC
- **RPC/HTTP**
  - Recommended: REST JSON  
  - Conservative: XML  
  - Cutting-edge: gRPC + JSON transcoding
- **Persistence**
  - Recommended: PostgreSQL 14–15  
  - Conservative: SQL Server 2019  
  - Cutting-edge: PostgreSQL + PostGIS 3.3+ (if geo queries needed)
- **Cache**
  - Recommended: Redis for “current incidents” list (TTL 2–5s)  
  - Conservative: DB only  
  - Cutting-edge: materialized views
- **Messaging**
  - Recommended: optional outbox table for sync to peers  
  - Conservative: none  
  - Cutting-edge: Kafka 3.7+
- **Search**
  - Recommended: DB indexes + trigram (optional)  
  - Conservative: none  
  - Cutting-edge: OpenSearch 2.x
- **Authn/Authz**
  - Recommended: JWT + RBAC claims (`IncidentOperator`, `IncidentAdmin`)  
  - Conservative: basic auth  
  - Cutting-edge: OPA policies
- **Observability**
  - Recommended: request metrics + audit on write operations  
  - Conservative: logs only  
  - Cutting-edge: distributed tracing
- **CI/CD**
  - Recommended: contract tests against `openapi.yaml`  
  - Conservative: manual  
  - Cutting-edge: consumer-driven contracts
- **Container runtime / Infra**
  - Same as above services.

### 3) Recommended default stack
- **C++17 REST service + PostgreSQL 14–15 + Redis 7.2 (optional)**.  
Justification: meets INF-004/INF-005 (incident/lane closure support) and INF-079 (single datastore in normal mode).

### 4) Interface design
Covered in `openapi.yaml` (`/incidents`, `/lane-closures`).

### 5) Data model / schema
See `sql/incident_ddl.sql`, `sql/lane_closure_ddl.sql`.

### 6) Caching & consistency
Cache “current incidents” and “current lane closures” for map rendering; invalidate on write via publish/notify (DB NOTIFY) or short TTL.

---

## D4. DeviceStatusService

### 1) Responsibilities & data ownership
Provides device inventories and current status (DMS/LCS/CCTV/etc.), plus aggregated network device status summaries. Owns `Device` snapshots in repository; may also proxy live status via adapters.

### 2) Technology options
- **Language/runtime:** C++17 / C / Go  
- **RPC/HTTP:** REST JSON / XML / gRPC  
- **Persistence:** PostgreSQL / SQL Server / TimescaleDB 2.14+ (time-series)  
- **Cache:** Redis / in-memory / none  
- **Messaging:** NATS / none / Kafka  
- **Search:** DB indexes / OpenSearch / none  
- **Authn/Authz:** JWT / mTLS-only / OPA  
- **Observability:** Prometheus metrics / Windows perf counters / OTel

### 3) Recommended default stack
- **C++17 REST + PostgreSQL 14–15 + Redis 7.2 (optional)**.  
Justification: meets INF-030 (network device status summary) and INF-048 (map display of devices).

### 4) Interface design
Covered in `openapi.yaml` (`/devices`, `/networks/{networkId}/device-status-summary`).

### 5) Data model / schema
See `sql/device_ddl.sql`.

### 6) Caching & consistency
- Cache device lists per networkId/deviceType (TTL 5–15s).
- Status consistency: “last-write-wins by timestamp” for ingested snapshots; optionally provide `sourceTimestamp` and `ingestedAt`.

---

## D5. DeviceCommandService

### 1) Responsibilities & data ownership
Validates, authorizes, time-window checks, persists, audits, encodes TMDD/DATEX/ASN payloads, routes to correct adapter, and returns status within the 2-second reply window when possible. Owns `DeviceCommand` and `CommandTimeframe`.

### 2) Technology options
- **Language/runtime:** C++17 / C / Rust  
- **RPC/HTTP:** REST JSON / SOAP / gRPC  
- **Persistence:** PostgreSQL / SQL Server / MySQL 8.0  
- **Cache:** Redis for timeframe rules / DB only / in-memory  
- **Messaging:** synchronous adapter call / async queue (RabbitMQ 3.13) / Kafka  
- **Search:** none / OpenSearch / DB only  
- **Authn/Authz:** JWT + RBAC + mTLS / mTLS-only / OIDC  
- **Observability:** metrics + audit / logs only / full tracing

### 3) Recommended default stack
- **C++17 REST + PostgreSQL 14–15 + synchronous adapter routing; optional async outbox for retries**.  
Justification: meets INF-070 (status display) and INF-031/INF-032 (command timeframe enforcement).

### 4) Interface design
Covered in `openapi.yaml` (`/commands`, `/commands/{commandId}`) and internal adapter contract in `internal.proto`.

### 5) Data model / schema
See `sql/device_command_ddl.sql`, `sql/command_timeframe_ddl.sql`.

### 6) Caching & consistency
Cache `CommandTimeframe` per (networkId, deviceType) TTL 60s; commands are strongly consistent writes; status updates are append/update with optimistic concurrency.

---

## D6. Integration: MicrokernelRuntime + AdapterBroker + Adapter Plugins + TMDDCodec

### 1) Responsibilities & data ownership
Loads adapter plugins per agency/system, negotiates TMDD versions, validates schemas, translates between system-specific formats and canonical model, and manages TCP/IP sessions to external centers/systems. Owns no primary data; writes ingested snapshots/events to repository via internal API.

### 2) Technology options
- **Language/runtime**
  - Recommended: C++17 plugin ABI boundary (stable C interface)  
  - Conservative: static linking per adapter  
  - Cutting-edge: WASM plugins
- **RPC/HTTP**
  - Recommended: internal gRPC (C++) between core and broker  
  - Conservative: internal REST  
  - Cutting-edge: message bus
- **Persistence**
  - Recommended: none (writes via repository service)  
  - Conservative: local spool files  
  - Cutting-edge: embedded RocksDB
- **Messaging**
  - Recommended: direct calls + optional outbox for retries  
  - Conservative: none  
  - Cutting-edge: NATS JetStream
- **Authn/Authz**
  - Recommended: mTLS to peers + per-peer cert pinning  
  - Conservative: TLS only  
  - Cutting-edge: SPIFFE identities
- **Observability**
  - Recommended: per-adapter metrics (decode errors, negotiation failures)  
  - Conservative: logs only  
  - Cutting-edge: full traces across adapters

### 3) Recommended default stack
- **C++17 microkernel + C ABI plugin adapters + TMDD/DATEX/ASN runtime library (vendor-provided) + TCP sockets with TLS 1.2+**.  
Justification: meets INF-034/INF-035/INF-036 (TMDD/DATEX/ASN/TCP-IP) and INF-073 (DATEX runtime availability).

### 4) Internal contracts (`internal.proto`)
See Section L.

### 5) Data model / schema
Adapters do not own tables; they write via internal service calls. (Optional spool table can be added later; not required by SRS.)

### 6) Caching & consistency
Cache negotiated TMDD version per peer session; invalidate on reconnect. Ingest is eventually consistent across peers; local repository is source of truth.

---

## D7. MapService + ESRI ARC IMS integration

### 1) Responsibilities & data ownership
Fetches basemap layers from NCTCOG source (via ESRI), overlays link speed colors and incident/device icons, and serves map metadata to WebMapUI. Owns no primary data; reads from repository.

### 2) Technology options
- **Language/runtime**
  - Recommended: C++17 service calling ESRI ARC IMS APIs  
  - Conservative: ESRI-only server-side scripts  
  - Cutting-edge: separate tile server (Mapbox/GeoServer) (likely incompatible)
- **Web framework**
  - Recommended: REST endpoints returning overlay JSON + image URLs  
  - Conservative: server-rendered HTML  
  - Cutting-edge: vector tiles
- **Persistence**
  - Recommended: none  
  - Conservative: none  
  - Cutting-edge: cache store
- **Cache**
  - Recommended: cache overlay computations (TTL 2–5s)  
  - Conservative: none  
  - Cutting-edge: CDN
- **Authn/Authz**
  - Recommended: anonymous for base map; auth for drilldown if required  
  - Conservative: all anonymous  
  - Cutting-edge: fine-grained ABAC

### 3) Recommended default stack
- **ESRI ARC IMS 10.2 integration + C++ overlay service + thresholds YAML config**.  
Justification: meets INF-074 (ARC IMS) and INF-044 (speed config file).

### 4) Interface design
Covered in `openapi.yaml` (`/map/overlay`, `/map/config/speed-thresholds`).

### 5) Data model / schema
No new tables; uses `link` speeds and `incident` tables.

### 6) Caching & consistency
Overlay cache TTL 2–5s; basemap caching per ESRI capabilities. Consistency is “near-real-time” based on latest ingested speeds/incidents.

---

## D8. Persistence: TrafficRepositoryDB + AuditLog

### 1) Responsibilities & data ownership
Stores canonical topology, incidents, lane closures, devices, commands, timeframes, users/sessions, and immutable audit events. Owns all persisted data.

### 2) Technology options
- **Persistence (SQL/NoSQL)**
  - Recommended: PostgreSQL 14–15  
  - Conservative: SQL Server 2019  
  - Cutting-edge: YugabyteDB 2.20+
- **Search**
  - Recommended: DB indexes  
  - Conservative: none  
  - Cutting-edge: OpenSearch
- **Encryption-at-rest**
  - Recommended: disk-level (BitLocker/LUKS) + column encryption for secrets  
  - Conservative: disk-level only  
  - Cutting-edge: HSM-backed TDE
- **HA**
  - Recommended: streaming replication + automatic failover  
  - Conservative: single primary + backups  
  - Cutting-edge: multi-primary

### 3) Recommended default stack
- **PostgreSQL 14–15 with streaming replication and strict indexing on (network_id, device_id, timestamp)**.  
Justification: meets INF-079 (single datastore) and INF-033 (store TMDD data elements/message sets).

### 4) Interface design
Exposed via services; not directly public.

### 5) Data model / schema
See SQL DDL artifacts in Section L.

### 6) Caching & consistency
DB is source of truth; Redis optional for hot reads. Audit events are append-only and hash-chained.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
Even if initial deployment is Windows VM-based (INF-072), provide a Kubernetes-ready reference for future portability (INF-PLAT-01).

See `k8s/c2c-core-deployment.yaml` in Section L.

## E2. DB HA topology, backups, restore
- **Topology:** 1 primary + 1 synchronous standby (same DC) + 1 asynchronous replica (DR site).  
  Justification: meets INF-AVAIL-01 (inferred HA requirement for critical repository).
- **Backups:** nightly full + 15-minute WAL archiving; retain 35 days; quarterly restore drills.  
  Justification: meets INF-079 (single datastore) by ensuring recoverability.
- **Restore notes:** restore to new primary, re-point services via DNS; verify audit hash chain integrity post-restore.

## E3. Network topology + ingress/egress rules
Mapped to *Deployment_PhysicalView*:
- **Ingress (Internet→DMZ):** allow 443/TCP only; enforce TLS 1.2+.  
  Justification: meets INF-SEC-001.
- **DMZ→AppTier:** allow 443/TCP internal TLS; deny all else.  
- **AppTier→DB:** allow 5432/TCP (PostgreSQL) only on private subnet.  
- **AppTier→External Systems:** allow configured TCP ports for TMDD/DATEX/ASN sessions; require TLS and peer allowlist.  
  Justification: meets INF-036.
- **Latency expectations:** command ack path should return within 2s of adapter reply (INF-070); enforce timeouts and circuit breakers.

## E4. CI/CD sketch
1. Build (C/C++): compile, run unit tests, static analysis (clang-tidy), dependency scan.  
2. Contract tests: validate `openapi.yaml` and `internal.proto`; run adapter schema conformance tests.  
3. Integration tests: spin up DB + services; run E2E flows (issue command, view map overlay).  
4. Security gates: SAST + secret scan; mTLS negative tests.  
5. Deploy: blue/green for API + services; canary 5% traffic; rollback on SLO burn.  
Justification: meets INF-080 (test mode logging) by ensuring test-mode behaviors are validated pre-prod.

---

# F. Security Design

## F1. Auth & AuthZ choice
- **External API:** OAuth2-like JWT bearer tokens (access + refresh) for GUIs; **mTLS required** for `/commands` and any endpoint carrying credentials to external centers.  
  Justification: meets INF-SEC-002 (mTLS) and INF-058 (username/password prompt).
- **Token lifecycle:** access token 15 minutes; refresh token 8 hours; refresh token stored hashed; revoke on logout/lockout.
- **RBAC claims:** `DeviceController`, `IncidentOperator`, `IncidentAdmin`, `IncidentViewer`.

## F2. Secrets management & rotation
- Store DB credentials and signing keys in K8s Secrets or Windows DPAPI-protected store; rotate quarterly or on incident; enforce least privilege.  
Justification: meets INF-SEC-003 (credential protection).

## F3. TLS & service-mesh
- TLS 1.2+ everywhere; prefer TLS 1.3 where supported.  
- Optional service mesh (Linkerd/Istio) for mTLS east-west if Kubernetes is used.  
Justification: meets INF-SEC-001.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Credential interception from public network GUI | TLS 1.2+, mTLS for command endpoints, no password logging (INF-SEC-002) |
| Unauthorized device control | RBAC claims + audit + timeframe enforcement (INF-031/032) |
| Payload tampering / schema confusion | TMDD schema validation + version negotiation (INF-034) |
| Replay of commands | nonce/idempotency key + commandId uniqueness + short token TTL |
| Audit log tampering | hash-chained append-only audit events (INF-AUD-001) |

---

# G. Observability & SRE

## G1. Metrics, traces, logs + example alerts
**Key metrics**
- Auth: login_failures_total, account_lockouts_total
- Commands: command_requests_total{deviceType}, command_latency_ms, command_failures_total, adapter_timeouts_total
- Map: overlay_latency_ms, incidents_query_latency_ms
- Integration: tmdd_decode_errors_total, version_negotiation_failures_total

**Logging**
- Structured JSON logs; redact secrets; correlate with `requestId` and `commandId`.

**Tracing**
- Propagate W3C traceparent from gateway to services; span per adapter call.

**Example Prometheus alert rules**
- High command failure rate:
  - `rate(c2c_command_failures_total[5m]) / rate(c2c_command_requests_total[5m]) > 0.05`
- Adapter timeouts:
  - `rate(c2c_adapter_timeouts_total[5m]) > 1`

## G2. SLOs, error budgets, RTO/RPO
- **SLO-1 Command response:** 99% of command submissions receive a response within 2s of adapter reply (INF-070).  
- **SLO-2 Map overlay:** 95% overlay requests < 1s (INF-PERF-02).  
- **RTO:** 1 hour; **RPO:** 15 minutes (aligned to WAL backups).  
Justification: meets INF-079 (single datastore) by bounding recovery.

## G3. Dashboard/runbook sketch
- Dashboards: command success rate by deviceType; adapter negotiation failures; DB replication lag; map overlay latency.
- Runbooks: “Adapter down”, “DB failover”, “mTLS cert expired”, “Audit chain verification failed”.

---

# H. Testing Strategy

## H1. Test matrix

| Test type | Components | Examples |
|---|---|---|
| Unit | AuthService, IncidentService, DeviceCommandService, TMDDCodec | password policy, schema validation, timeframe logic |
| Integration | Services + DB | incident CRUD, command persistence, audit append |
| Contract | Gateway + services; adapters | OpenAPI validation; `internal.proto` compatibility; TMDD schema conformance |
| E2E | GUI→API→Adapter (mock) | issue DMS command; view status; map overlay + drilldown |
| Chaos | DB failover; adapter disconnect | ensure retries, circuit breaker, no data corruption |

## H2. Test data management & environment isolation
- Environments: dev, test, staging, prod (4).  
- Refresh cadence: nightly anonymized snapshot for test; synthetic TMDD payload generator for adapters.  
- Isolation: per-env DB; per-env signing keys; separate mTLS CA.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
1. Stand up repository + services in parallel (“shadow mode”).  
2. Implement adapters for each legacy system; ingest status/events into canonical store.  
3. Validate map overlays and incident lists against legacy outputs.  
4. Enable remote command/control in “observe-only” mode (no-op adapter) then controlled pilot.  
5. Cutover per networkId/center; keep rollback by switching routing back to legacy.

**Data-sync strategy:** dual-ingest (legacy + new) until parity; last-write-wins by timestamp for conflicts.  
Justification: meets INF-079 (combine data into single datastore).

## I2. Backwards compatibility & API versioning
- External API versioning via `/v1/...`; additive changes only within v1; breaking changes require `/v2`.  
- Deprecation window: 180 days for public endpoints.  
Justification: meets INF-057 (public network GUI) by ensuring stable interfaces.

---

# J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Why chosen (tie to IDs) |
|---|---|---|---|
| Microkernel + adapters | Yes | Monolith; ESB | Meets INF-001..INF-036 interoperability and INF-079 multi-source ingest with isolated translations. |
| PostgreSQL | Yes | SQL Server; MySQL | Strong indexing + replication; fits canonical repository needs (INF-033, INF-079). |
| JWT + mTLS for commands | Yes | mTLS-only; OIDC external IdP | Balances GUI usability with strong command security (INF-SEC-002, INF-058). |
| REST external API | Yes | SOAP; gRPC-web | Simpler for web/desktop clients; contract-first via OpenAPI (INF-037, INF-049). |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** “Microsoft Windows NT environment” is interpreted as Windows Server 2019+ for production hardening while maintaining functional compatibility expectations.  
- **A2:** ESRI ARC IMS 10.2 and ESRI Map Objects versions are available and licensable for all required servers/clients.  
- **A3:** TMDD version is at least v3.0 and schemas are obtainable for validation.  
- **A4:** External centers/legacy systems can support TLS 1.2+ for TMDD/DATEX/ASN transport; if not, a secured tunnel (VPN) will be used.  
- **A5:** All device types beyond DMS/LCS/CCTV are represented as `deviceType` + `device_ext` JSON until full subtype modeling is required.  
- **A6:** Incident “tabular format fields” not enumerated in SRS will minimally include id, description, roadway, timestamp, impact, status.

## Unresolved stakeholder questions (need input)
1. What exact TMDD message set versions and ASN.1 modules are mandated per partner center?  
2. What are the authoritative lists for `networkId` values and device inventories (source of truth)?  
3. What are the required incident table columns and any PII constraints?  
4. What is the required command acceptance timeframe policy governance (who configures `CommandTimeframe`)?  
5. Are there regulatory requirements for audit retention duration and cryptographic signing (beyond hash chaining)?

## Conflicts / naming issues logged
- **C1:** Diagrams reference “Windows Server 2019+” while SRS says “Windows NT”. Preference given to SRS naming; implementation assumes A1.  
- **C2:** Diagrams include NFR/ASR IDs not present in SRS; treated as inferred `INF-SEC-*`, `INF-AVAIL-*`, `INF-PERF-*` and listed here.

## Inferred requirement IDs list (non-exhaustive categories)
- INF-SEC-001/002/003, INF-AUD-001, INF-AVAIL-01, INF-PERF-01/02, INF-PLAT-01, INF-SYNC-001.

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# ArchitectureDocument.md

(Contents are the full document from Sections A–L, as provided in this response.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Center-to-Center (C2C) External API
  version: "1.0.0"
  description: >
    External REST API for C2C: auth, incidents/lane closures, device status, commands, and map overlays.
servers:
  - url: https://c2c.example.gov/v1
tags:
  - name: auth
  - name: incidents
  - name: devices
  - name: commands
  - name: map
security:
  - bearerAuth: []
paths:
  /auth/login:
    post:
      tags: [auth]
      summary: Login and obtain access/refresh tokens
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
            examples:
              ex:
                value: { "username": "remote.operator", "password": "correct horse battery staple" }
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
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "423":
          description: Account locked
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /auth/refresh:
    post:
      tags: [auth]
      summary: Refresh access token
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/RefreshRequest" }
      responses:
        "200":
          description: New access token
          content:
            application/json:
              schema: { $ref: "#/components/schemas/RefreshResponse" }
        "401":
          description: Invalid refresh token
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /auth/logout:
    post:
      tags: [auth]
      summary: Revoke refresh token
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/LogoutRequest" }
      responses:
        "204":
          description: Logged out
        "400":
          description: Bad request
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /incidents:
    get:
      tags: [incidents]
      summary: List incidents (for map/table)
      parameters:
        - in: query
          name: networkId
          required: true
          schema: { type: string }
        - in: query
          name: limit
          required: false
          schema: { type: integer, minimum: 1, maximum: 500, default: 100 }
        - in: query
          name: cursor
          required: false
          schema: { type: string }
      responses:
        "200":
          description: Incident list
          content:
            application/json:
              schema: { $ref: "#/components/schemas/IncidentListResponse" }
        "401":
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
    post:
      tags: [incidents]
      summary: Create incident
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/IncidentCreateRequest" }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: "#/components/schemas/IncidentResponse" }
        "400":
          description: Validation error
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "401":
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /incidents/{incidentId}:
    get:
      tags: [incidents]
      summary: Get incident details (drilldown)
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Incident details
          content:
            application/json:
              schema: { $ref: "#/components/schemas/IncidentResponse" }
        "403":
          description: Forbidden (missing IncidentViewer claim)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "404":
          description: Not found
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
    put:
      tags: [incidents]
      summary: Update incident
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/IncidentUpdateRequest" }
      responses:
        "200":
          description: Updated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/IncidentResponse" }
        "400":
          description: Validation error
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
    delete:
      tags: [incidents]
      summary: Delete incident (IncidentAdmin)
      parameters:
        - in: path
          name: incidentId
          required: true
          schema: { type: string }
      responses:
        "204":
          description: Deleted
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /lane-closures:
    get:
      tags: [incidents]
      summary: List lane closures
      parameters:
        - in: query
          name: networkId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Lane closure list
          content:
            application/json:
              schema: { $ref: "#/components/schemas/LaneClosureListResponse" }
    post:
      tags: [incidents]
      summary: Create lane closure
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/LaneClosureCreateRequest" }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: "#/components/schemas/LaneClosureResponse" }

  /lane-closures/{laneClosureId}:
    delete:
      tags: [incidents]
      summary: Delete lane closure
      parameters:
        - in: path
          name: laneClosureId
          required: true
          schema: { type: string }
      responses:
        "204":
          description: Deleted
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /devices:
    get:
      tags: [devices]
      summary: List devices by network and type
      parameters:
        - in: query
          name: networkId
          required: true
          schema: { type: string }
        - in: query
          name: deviceType
          required: false
          schema:
            $ref: "#/components/schemas/DeviceType"
      responses:
        "200":
          description: Device list
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceListResponse" }

  /networks/{networkId}/device-status-summary:
    get:
      tags: [devices]
      summary: Aggregated device status summary for a network
      parameters:
        - in: path
          name: networkId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Summary
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceStatusSummaryResponse" }

  /commands/timeframes:
    get:
      tags: [commands]
      summary: Get command acceptance timeframe for a network and device type
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
          description: Timeframe
          content:
            application/json:
              schema: { $ref: "#/components/schemas/CommandTimeframeResponse" }

  /commands:
    post:
      tags: [commands]
      summary: Issue a device command (mTLS required)
      description: >
        Requires bearer token and mTLS at the gateway. Payload supports multiple device operations.
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/DeviceCommandCreateRequest" }
      responses:
        "202":
          description: Accepted (PENDING)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceCommandResponse" }
        "400":
          description: Validation error (schema/timeframe)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "403":
          description: Forbidden (missing DeviceController claim)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /commands/{commandId}:
    get:
      tags: [commands]
      summary: Get command status
      parameters:
        - in: path
          name: commandId
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Status
          content:
            application/json:
              schema: { $ref: "#/components/schemas/DeviceCommandResponse" }
        "404":
          description: Not found
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /map/overlay:
    get:
      tags: [map]
      summary: Get map overlay data (links colored by speed + incident/device icons)
      parameters:
        - in: query
          name: networkId
          required: true
          schema: { type: string }
        - in: query
          name: bbox
          required: true
          description: "minLon,minLat,maxLon,maxLat"
          schema:
            type: string
            pattern: "^-?\\d+(\\.\\d+)?,-?\\d+(\\.\\d+)?,-?\\d+(\\.\\d+)?,-?\\d+(\\.\\d+)?$"
        - in: query
          name: zoom
          required: true
          schema: { type: integer, minimum: 0, maximum: 22 }
      responses:
        "200":
          description: Overlay payload
          content:
            application/json:
              schema: { $ref: "#/components/schemas/MapOverlayResponse" }

  /map/config/speed-thresholds:
    get:
      tags: [map]
      summary: Get configured speed thresholds used for link coloring
      responses:
        "200":
          description: Thresholds
          content:
            application/json:
              schema: { $ref: "#/components/schemas/SpeedThresholdsResponse" }

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    ErrorResponse:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message, requestId]
          properties:
            code: { type: string, example: "C2C-VALIDATION-001" }
            message: { type: string }
            requestId: { type: string }
            details:
              type: object
              additionalProperties: true

    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1 }
        password: { type: string, minLength: 12, format: password }

    LoginResponse:
      type: object
      required: [accessToken, refreshToken, expiresInSeconds, claims]
      properties:
        accessToken: { type: string }
        refreshToken: { type: string }
        expiresInSeconds: { type: integer, example: 900 }
        claims:
          type: array
          items: { type: string }

    RefreshRequest:
      type: object
      required: [refreshToken]
      properties:
        refreshToken: { type: string }

    RefreshResponse:
      type: object
      required: [accessToken, expiresInSeconds]
      properties:
        accessToken: { type: string }
        expiresInSeconds: { type: integer }

    LogoutRequest:
      type: object
      required: [refreshToken]
      properties:
        refreshToken: { type: string }

    Incident:
      type: object
      required: [incidentId, networkId, description, roadway, timestamp]
      properties:
        incidentId: { type: string }
        networkId: { type: string }
        description: { type: string }
        roadway: { type: string }
        geo:
          type: string
          description: "lat,lon"
        timestamp:
          type: string
          format: date-time
        impact:
          type: string
          enum: [MINOR, MODERATE, MAJOR, UNKNOWN]
        status:
          type: string
          enum: [ACTIVE, CLEARED, UNKNOWN]

    IncidentCreateRequest:
      type: object
      required: [networkId, description, roadway, timestamp]
      properties:
        networkId: { type: string }
        description: { type: string, minLength: 1 }
        roadway: { type: string, minLength: 1 }
        geo: { type: string }
        timestamp: { type: string, format: date-time }
        impact:
          type: string
          enum: [MINOR, MODERATE, MAJOR, UNKNOWN]

    IncidentUpdateRequest:
      type: object
      required: [description, roadway, timestamp]
      properties:
        description: { type: string, minLength: 1 }
        roadway: { type: string, minLength: 1 }
        geo: { type: string }
        timestamp: { type: string, format: date-time }
        impact:
          type: string
          enum: [MINOR, MODERATE, MAJOR, UNKNOWN]
        status:
          type: string
          enum: [ACTIVE, CLEARED, UNKNOWN]

    IncidentResponse:
      type: object
      required: [incident]
      properties:
        incident: { $ref: "#/components/schemas/Incident" }

    IncidentListResponse:
      type: object
      required: [items]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/Incident" }
        nextCursor:
          type: string
          nullable: true

    LaneClosure:
      type: object
      required: [laneClosureId, networkId, description]
      properties:
        laneClosureId: { type: string }
        networkId: { type: string }
        description: { type: string }

    LaneClosureCreateRequest:
      type: object
      required: [networkId, description]
      properties:
        networkId: { type: string }
        description: { type: string, minLength: 1 }

    LaneClosureResponse:
      type: object
      required: [laneClosure]
      properties:
        laneClosure: { $ref: "#/components/schemas/LaneClosure" }

    LaneClosureListResponse:
      type: object
      required: [items]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/LaneClosure" }

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
        - BUS_STOP
        - BUS_LOCATION
        - RAIL_STOP
        - RAIL_VEHICLE
        - PARK_AND_RIDE
        - VEHICLE_PRIORITY
        - UNKNOWN

    Device:
      type: object
      required: [deviceId, networkId, deviceType, name, status]
      properties:
        deviceId: { type: string }
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        name: { type: string }
        location: { type: string }
        status: { type: string }
        ext:
          type: object
          additionalProperties: true

    DeviceListResponse:
      type: object
      required: [items]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/Device" }

    DeviceStatusSummaryResponse:
      type: object
      required: [networkId, countsByType, countsByStatus]
      properties:
        networkId: { type: string }
        countsByType:
          type: object
          additionalProperties: { type: integer }
        countsByStatus:
          type: object
          additionalProperties: { type: integer }

    CommandTimeframeResponse:
      type: object
      required: [networkId, deviceType, daysAccepted, timesAccepted]
      properties:
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        daysAccepted:
          type: array
          items: { type: string, example: "MON" }
        timesAccepted:
          type: array
          items: { type: string, example: "08:00-18:00" }

    DeviceCommandStatus:
      type: string
      enum: [DRAFT, REJECTED, PENDING, SUCCESS, FAILED]

    DeviceCommandCreateRequest:
      type: object
      required: [networkId, deviceType, deviceId, operation, payload]
      properties:
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        deviceId: { type: string }
        operation:
          type: string
          example: "DISPLAY_MESSAGE"
        payload:
          type: object
          additionalProperties: true
        idempotencyKey:
          type: string
          description: "Client-provided key to prevent duplicate submissions"

    DeviceCommand:
      type: object
      required: [commandId, networkId, deviceType, deviceId, operation, requestedBy, requestedAt, status]
      properties:
        commandId: { type: string }
        networkId: { type: string }
        deviceType: { $ref: "#/components/schemas/DeviceType" }
        deviceId: { type: string }
        operation: { type: string }
        payload:
          type: object
          additionalProperties: true
        requestedBy: { type: string }
        requestedAt: { type: string, format: date-time }
        status: { $ref: "#/components/schemas/DeviceCommandStatus" }
        errorMessage: { type: string, nullable: true }

    DeviceCommandResponse:
      type: object
      required: [command]
      properties:
        command: { $ref: "#/components/schemas/DeviceCommand" }

    MapOverlayResponse:
      type: object
      required: [networkId, links, incidents, devices]
      properties:
        networkId: { type: string }
        links:
          type: array
          items:
            type: object
            required: [linkId, speedKph, color]
            properties:
              linkId: { type: string }
              speedKph: { type: integer }
              color: { type: string, example: "#FF0000" }
        incidents:
          type: array
          items:
            type: object
            required: [incidentId, geo, icon]
            properties:
              incidentId: { type: string }
              geo: { type: string }
              icon: { type: string }
        devices:
          type: array
          items:
            type: object
            required: [deviceId, deviceType, geo, icon]
            properties:
              deviceId: { type: string }
              deviceType: { $ref: "#/components/schemas/DeviceType" }
              geo: { type: string }
              icon: { type: string }

    SpeedThresholdsResponse:
      type: object
      required: [thresholds]
      properties:
        thresholds:
          type: array
          items:
            type: object
            required: [minKph, color]
            properties:
              minKph: { type: integer }
              color: { type: string }
```

```proto
// filename: internal.proto
syntax = "proto3";

package c2c.internal.v1;

option go_package = "c2c/internal/v1;internalv1";

// Internal contract between core services and adapter broker/plugins.
// Focus: command routing + status ingest + TMDD/DATEXASN payload transport.

message AdapterKey {
  string network_id = 1;
  string device_type = 2; // e.g., "DMS", "CCTV"
}

message TmddEnvelope {
  string tmdd_version = 1;     // negotiated version, e.g., "3.1"
  bytes datex_asn_payload = 2; // encoded ASN.1 bytes
  string correlation_id = 3;   // commandId or ingest batch id
}

message CommandRequest {
  string command_id = 1;
  string network_id = 2;
  string device_type = 3;
  string device_id = 4;
  string operation = 5;
  string requested_by = 6;
  int64 requested_at_unix_ms = 7;
  map<string, string> metadata = 8;
  TmddEnvelope envelope = 9;
}

message CommandAck {
  string command_id = 1;
  string status = 2; // "PENDING" | "SUCCESS" | "FAILED"
  string error_message = 3;
  int64 received_at_unix_ms = 4;
}

message DeviceSnapshot {
  string network_id = 1;
  string device_type = 2;
  string device_id = 3;
  string name = 4;
  string location = 5;
  string status = 6;
  int64 source_timestamp_unix_ms = 7;
  map<string, string> ext = 8;
}

message IncidentSnapshot {
  string network_id = 1;
  string incident_id = 2;
  string description = 3;
  string roadway = 4;
  string geo = 5;
  int64 source_timestamp_unix_ms = 6;
  string impact = 7;
}

message IngestBatch {
  string batch_id = 1;
  repeated DeviceSnapshot devices = 2;
  repeated IncidentSnapshot incidents = 3;
}

message IngestAck {
  string batch_id = 1;
  int32 accepted_devices = 2;
  int32 accepted_incidents = 3;
  string error_message = 4;
}

service AdapterBrokerService {
  rpc PushCommand(CommandRequest) returns (CommandAck);
  rpc IngestSnapshots(IngestBatch) returns (IngestAck);
}
```

```yaml
# filename: k8s/c2c-core-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: c2c-core
  labels:
    app: c2c-core
spec:
  replicas: 2
  selector:
    matchLabels:
      app: c2c-core
  template:
    metadata:
      labels:
        app: c2c-core
    spec:
      containers:
        - name: c2c-core
          image: registry.example.gov/c2c/core:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "2"
              memory: "2Gi"
          env:
            - name: C2C_MODE
              valueFrom:
                configMapKeyRef:
                  name: c2c-config
                  key: mode
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: c2c-secrets
                  key: database_url
            - name: JWT_PRIVATE_KEY_PEM
              valueFrom:
                secretKeyRef:
                  name: c2c-secrets
                  key: jwt_private_key_pem
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: c2c-core
spec:
  selector:
    app: c2c-core
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: c2c-core-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: c2c-core
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
  name: c2c-config
data:
  mode: "normal"
  speed_thresholds.yaml: |
    thresholds:
      - minKph: 0
        color: "#FF0000"
      - minKph: 40
        color: "#FFA500"
      - minKph: 70
        color: "#00FF00"
---
apiVersion: v1
kind: Secret
metadata:
  name: c2c-secrets
type: Opaque
stringData:
  database_url: "postgresql://c2c_user:REDACTED@postgres.c2c.svc.cluster.local:5432/c2c"
  jwt_private_key_pem: |
    -----BEGIN PRIVATE KEY-----
    REPLACE_WITH_REAL_KEY
    -----END PRIVATE KEY-----
```

```sql
-- filename: sql/network_ddl.sql
CREATE TABLE IF NOT EXISTS network (
  network_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_network_name ON network (name);
```

```sql
-- filename: sql/link_ddl.sql
CREATE TABLE IF NOT EXISTS link (
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  link_id TEXT NOT NULL,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  speed_kph INTEGER,
  speed_timestamp TIMESTAMPTZ,
  PRIMARY KEY (network_id, link_id)
);

CREATE INDEX IF NOT EXISTS idx_link_network_type ON link (network_id, type);
CREATE INDEX IF NOT EXISTS idx_link_speed_timestamp ON link (network_id, speed_timestamp DESC);
```

```sql
-- filename: sql/node_ddl.sql
CREATE TABLE IF NOT EXISTS node (
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  node_id TEXT NOT NULL,
  name TEXT NOT NULL,
  type_description TEXT NOT NULL,
  PRIMARY KEY (network_id, node_id)
);

CREATE INDEX IF NOT EXISTS idx_node_network ON node (network_id);
```

```sql
-- filename: sql/incident_ddl.sql
CREATE TABLE IF NOT EXISTS incident (
  incident_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  roadway TEXT NOT NULL,
  geo TEXT,
  impact TEXT NOT NULL DEFAULT 'UNKNOWN',
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  source_timestamp TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_incident_network_time ON incident (network_id, source_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_incident_status ON incident (status);
```

```sql
-- filename: sql/lane_closure_ddl.sql
CREATE TABLE IF NOT EXISTS lane_closure (
  lane_closure_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  source_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_lane_closure_network_time ON lane_closure (network_id, source_timestamp DESC);
```

```sql
-- filename: sql/device_ddl.sql
CREATE TABLE IF NOT EXISTS device (
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  device_id TEXT NOT NULL,
  device_type TEXT NOT NULL,
  name TEXT NOT NULL,
  location TEXT,
  status TEXT NOT NULL,
  source_timestamp TIMESTAMPTZ,
  device_ext JSONB NOT NULL DEFAULT '{}'::jsonb,
  PRIMARY KEY (network_id, device_id)
);

CREATE INDEX IF NOT EXISTS idx_device_network_type ON device (network_id, device_type);
CREATE INDEX IF NOT EXISTS idx_device_status ON device (status);
CREATE INDEX IF NOT EXISTS idx_device_source_timestamp ON device (network_id, source_timestamp DESC);
```

```sql
-- filename: sql/command_timeframe_ddl.sql
CREATE TABLE IF NOT EXISTS command_timeframe (
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  device_type TEXT NOT NULL,
  days_accepted TEXT[] NOT NULL,
  times_accepted TEXT[] NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (network_id, device_type)
);
```

```sql
-- filename: sql/device_command_ddl.sql
CREATE TABLE IF NOT EXISTS device_command (
  command_id TEXT PRIMARY KEY,
  network_id TEXT NOT NULL REFERENCES network(network_id) ON DELETE CASCADE,
  device_type TEXT NOT NULL,
  device_id TEXT NOT NULL,
  operation TEXT NOT NULL,
  payload JSONB NOT NULL,
  requested_by TEXT NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL,
  error_message TEXT,
  idempotency_key TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_device_command_idempotency
  ON device_command (network_id, requested_by, idempotency_key)
  WHERE idempotency_key IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_device_command_network_time
  ON device_command (network_id, requested_at DESC);

CREATE INDEX IF NOT EXISTS idx_device_command_status
  ON device_command (status);
```

```sql
-- filename: sql/user_account_ddl.sql
CREATE TABLE IF NOT EXISTS user_account (
  user_id TEXT PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL, -- store bcrypt/scrypt hash; never store plaintext
  mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  locked_until TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_user_account_username ON user_account (username);
```

```sql
-- filename: sql/auth_session_ddl.sql
CREATE TABLE IF NOT EXISTS auth_session (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES user_account(user_id) ON DELETE CASCADE,
  issued_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  claims TEXT[] NOT NULL,
  refresh_token_hash TEXT NOT NULL,
  revoked_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_auth_session_user ON auth_session (user_id, expires_at DESC);
CREATE INDEX IF NOT EXISTS idx_auth_session_revoked ON auth_session (revoked_at);
```

```sql
-- filename: sql/audit_event_ddl.sql
CREATE TABLE IF NOT EXISTS audit_event (
  event_id TEXT PRIMARY KEY,
  timestamp TIMESTAMPTZ NOT NULL,
  type TEXT NOT NULL,
  user_id TEXT,
  action TEXT NOT NULL,
  target_id TEXT,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  hash_prev TEXT NOT NULL,
  hash_this TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_event_time ON audit_event (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_event_user ON audit_event (user_id, timestamp DESC);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-001,Provide network name and link data per roadway network,"Class_LogicView:Network/Topology/Link/Node","TrafficRepository,MapService","sql/network_ddl.sql;sql/link_ddl.sql;openapi.yaml","Canonical topology supports map and sharing."
INF-004,Support incident info,"Class_LogicView:Incident;Sequence_ProcessView_S2_ViewMapAndIncidents","IncidentService,TrafficRepository","sql/incident_ddl.sql;openapi.yaml","Incidents stored and served to map/table."
INF-005,Support lane closure info,"Class_LogicView:LaneClosure","IncidentService,TrafficRepository","sql/lane_closure_ddl.sql;openapi.yaml","Lane closures managed and displayed."
INF-030,Network device status summary,"UseCase_ScenarioView:UC_ViewDeviceStatus","DeviceStatusService","openapi.yaml","Aggregated endpoint supports summary requirement."
INF-031,Command timeframe request,"Class_LogicView:CommandTimeframe","DeviceCommandService","sql/command_timeframe_ddl.sql;openapi.yaml","Timeframe rules enforce acceptance windows."
INF-034,Use TMDD standard message sets,"Class_LogicView:TMDDCodec","TMDDCodec,Adapters","internal.proto","Codec enforces standard encoding/validation."
INF-035,DATEX/ASN used to transmit TMDD,"Component_DevelopmentView:TMDDCodec","TMDDCodec","internal.proto","Centralized DATEX/ASN encoding boundary."
INF-036,TCP/IP used to transmit DATEX/ASN,"Deployment_PhysicalView:AppTier->ExtSystems","Adapters","internal.proto","Adapters own TCP transport."
INF-070,Display command status within 2s of reply,"State_LogicView_DeviceCommandLifecycle","DeviceCommandService,RemoteControlGUI","openapi.yaml","Command status returned and queryable."
INF-072,Execute in Microsoft Windows NT environment,"Deployment_PhysicalView:AppTier Windows","All services","architecture.md","Platform constraint drives runtime choices."
INF-073,DATEX/ASN runtime library available,"Deployment_PhysicalView:Codec artifact","TMDDCodec,Adapters","architecture.md","Gatekeeper checks runtime presence."
INF-074,Use ESRI ARC IMS for map images,"Deployment_PhysicalView:EsriArcIMS","MapRenderService","architecture.md","ESRI constraint dictates map rendering."
INF-079,Normal mode combine data into single datastore,"Component_DevelopmentView:TrafficRepositoryDB","MicrokernelRuntime,Repository","sql/*;internal.proto","Ingest pipeline writes canonical store."
INF-080,Test mode logs activities,"Activity_ProcessView_RemoteDeviceCommand","Observability stack","architecture.md","Test-mode toggles verbose logging."
INF-SEC-001,TLS 1.2+ for external interfaces,"Component_DevelopmentView:APIGateway","APIGateway","openapi.yaml;k8s/c2c-core-deployment.yaml","Transport security for public access."
INF-SEC-002,mTLS for password-field endpoints,"State_LogicView_DeviceCommandLifecycle","APIGateway,SecurityGateway","openapi.yaml","Hardens command/control endpoints."
INF-AUD-001,Immutable hash-chained audit log,"Class_LogicView:AuditEvent","AuditLog,TrafficRepository","sql/audit_event_ddl.sql","Tamper-evident audit trail."
```

---

## Verification & Acceptance Criteria Checklist

| Item | Verification |
|---|---|
| [x] 3-line Analysis Plan present. | Present at top (exactly 3 lines). |
| [x] Sections A-L included. | A through L headings included. |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | SRS lacked IDs; all statements were assigned INF- IDs; stakeholder to confirm no missed lines. |
| [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | `openapi.yaml` and `internal.proto` included. |
| [x] Representative k8s manifest snippet included. | `k8s/c2c-core-deployment.yaml` included. |
| [x] SQL DDL / NoSQL models for primary entities included. | SQL DDLs included. |
| [x] All major components have at least one API contract and a data schema. | Covered via OpenAPI + SQL; adapters via proto. |
| [x] Assumptions and unresolved questions listed. | Section K included. |

---

## How to review checklist
- All FR/NFR/ASR present in traceability matrix? (Here: all inferred `INF-*` requirements; confirm none missing from SRS text.)  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?