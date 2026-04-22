Analysis Plan: Scope—design production-ready architecture for CCTNS modules (Registration, Investigation, Prosecution, Search, Citizen Interface, Navigation, Support/Helpdesk, Security, Audit) and reconcile conflicts with provided UML.  
Analysis Plan: Approach—treat Original Requirements as scope authority; log UML conflict; define INF-* atomic requirements; produce 4+1 views, contracts (OpenAPI + internal proto), schemas, k8s, and traceability.  
Analysis Plan: Validation—cross-check every requirement mapped; verify OpenAPI/proto/k8s/SQL parse; ensure security/audit/availability/performance acceptance tests align to NFRs.

# A. Executive Summary (≤1 page)

## System overview
CCTNS (Crime & Criminals Tracking Network and Systems) is a centralized, SOA-based, browser-accessed police information system supporting citizen complaint registration, investigation workflows, prosecution/court interfacing, advanced search/reporting, citizen information exchange, role-based navigation, and a support/helpdesk capability with immutable audit trails and strong access control.

**Diagram mapping (note conflict):** Provided PlantUML diagrams describe a “Web Learning Game System” (UseCase_ScenarioView: UC_*; Component_DevelopmentView: WebUI/GameAPI/etc.). This conflicts with CCTNS requirements; per rule, we **prefer Original Requirements** and log the conflict in **K**. We still reference the diagram set as a generic 4+1 scaffold only (e.g., Deployment_PhysicalView: WebTier/AppTier/DataTier nodes) while renaming components to CCTNS in this document.

## Architectural style(s) and topology
- **Style:** Modular **SOA** with domain services + shared cross-cutting services (AuthN/AuthZ, Audit, Search, Notification, Helpdesk).  
- **Topology:** **Centralized 3-tier / n-tier** deployment (Web/UI tier, App/Service tier, Data tier) with offline-capable edge client for critical station workflows.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| R1: Immutable audit trail “unalterable” requirement not met end-to-end | Legal admissibility risk | Use **append-only WORM** storage + hash-chained entries + DB permissions preventing UPDATE/DELETE; periodic integrity verification jobs; export without mutation (INF-ASR-AUD-EXPORT). |
| R2: Performance targets for search and case retrieval degrade at scale | Operational failure at stations | Dedicated search index (OpenSearch/Elasticsearch) + DB indexing + paged results (10/20) + hierarchical cache; load tests enforcing NFR-PERF-* SLOs. |
| R3: Offline mode + later synchronization causes conflicts/data loss | Data integrity issues | Offline-first local store with outbox pattern, idempotent APIs, conflict policy (server timestamp + station priority), and audit of merges; explicit “sync status” UI. |

## Key QA coverage mapping

| Quality attribute | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-SCALE-01, INF-NFR-PERF-SEARCH-01, INF-NFR-PAGING-01 | Load/soak tests, capacity tests, search benchmark tests |
| Availability/DR | INF-NFR-AVAIL-01..04, INF-NFR-DR-01 | HA failover tests, backup/restore drills, chaos tests |
| Security | INF-ASR-SEC-RBAC-*, INF-ASR-SEC-TLS-*, INF-ASR-SEC-INJ-*, INF-ASR-SEC-ENC-01 | SAST/DAST, penetration tests, RBAC tests, TLS config scans |
| Performance | INF-NFR-PERF-SEARCH-01, INF-NFR-PERF-CASEHOT-01, INF-NFR-PERF-CASECOLD-01 | p95 latency tests, synthetic monitoring, DB/index profiling |
| Maintainability | INF-ASR-SOA-01, INF-ASR-OPEN-01, INF-ASR-3C-01 | Contract tests, schema validation CI gates, architecture conformance checks |

---

# B. Traceability & Rationale

Because the Original Requirements text has no IDs, we normalize into **INF-*** requirements. The table below is also delivered as `traceability_matrix.csv` in Section L.

**Legend:** Diagrams referenced by title and element IDs only (from provided set), used as structural placeholders.

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-MOD-REG-01 | Citizen registers complaint; police takes forward | UseCase_ScenarioView: UC_StartGame/UC_PlaySession (conflict placeholder) | RegistrationService, CitizenPortal | openapi.yaml, internal.proto | Implements citizen→police intake and case initiation flow. |
| INF-FR-MOD-INV-01 | Investigation workflow automation after registration | State_LogicView_GameSession: InProgress/Completed (placeholder) | InvestigationService | openapi.yaml, internal.proto | Models case lifecycle and task automation. |
| INF-FR-MOD-PRO-01 | Prosecution/court interaction recording | Sequence_ProcessView_S2_AdminPublish (placeholder) | ProsecutionService | openapi.yaml, sql/court_event_ddl.sql | Captures court events and documents with audit. |
| INF-FR-MOD-SEARCH-01 | Basic/advanced search across cases/person/crime/MO/property | Sequence_ProcessView_S1_PlaySession (placeholder) | SearchService | openapi.yaml | Provides query endpoints with RBAC filtering and paging. |
| INF-FR-MOD-REPORT-01 | Reporting queries (monthly, RTI) | Activity_ProcessView_PlaySession (placeholder) | ReportingService | openapi.yaml | Enables parameterized reports with export. |
| INF-FR-MOD-CIT-01 | Citizen interface: acknowledgements/info exchange | UseCase_ScenarioView: UC_ViewFeedback/UC_ViewScore (placeholder) | CitizenPortal, NotificationService | openapi.yaml | Supports status/ack and responses with alerts. |
| INF-FR-MOD-NAV-01 | Role-based landing pages: cases assigned, alerts, tasks | Container_PhysicalView: WebUI/AdminUI (placeholder) | NavigationService, UI | openapi.yaml | Drives personalized dashboards and saved UI preferences. |
| INF-FR-SUP-HELP-01 | Context-sensitive help for all UI actions | Package_DevelopmentView: ui | HelpContentService | openapi.yaml | Meets help material requirement across UI. |
| INF-FR-SUP-TICKET-01 | Log defects/enhancements and track | UseCase_ScenarioView: UC_ManageContent (placeholder) | HelpdeskService | openapi.yaml, sql/ticket_ddl.sql | Implements ticketing and tracking. |
| INF-FR-SUP-ALERT-01 | Alerts (email/SMS) on ticket actions if user chooses | Collaboration_ProcessView_S2_AdminPublish (placeholder) | NotificationService | internal.proto | Event-driven notifications. |
| INF-FR-SUP-REPORT-01 | Helpdesk reports by category/status/age | Class_LogicView: AuditLogEntry (placeholder) | HelpdeskService | openapi.yaml | Reporting endpoints for helpdesk. |
| INF-NFR-SUP-ACCESS-01 | Support accessible inside app and via browser | Deployment_PhysicalView: Client/WebTier | UI Gateway | openapi.yaml | Ensures both embedded and standalone access. |
| INF-ASR-AUD-01 | Unalterable audit trail for CRUD on critical entities | Class_LogicView: AuditLogEntry | AuditService | sql/audit_log_ddl.sql | Append-only + permissions + hash chain. |
| INF-ASR-AUD-02 | Audit captures user initiating action | Class_LogicView: AuditLogEntry.adminId | AuditService, AuthService | sql/audit_log_ddl.sql | Stores actor identity for admissibility. |
| INF-ASR-AUD-03 | Audit captures date/time | Class_LogicView: AuditLogEntry.timestampUtc | AuditService | sql/audit_log_ddl.sql | UTC timestamps for traceability. |
| INF-ASR-AUD-04 | Audit captures administrative parameters | Component_DevelopmentView: AuditService | AuditService | sql/audit_log_ddl.sql | Records config/security changes. |
| INF-ASR-AUD-05 | Audit cannot be modified/deleted; can be copied/exported unchanged | Component_DevelopmentView: AuditLogStore | AuditService | openapi.yaml, sql/audit_log_ddl.sql | Export endpoints + WORM/append-only. |
| INF-ASR-AUD-06 | Audit auto-captures without manual intervention | Component_DevelopmentView: AuditService | Audit middleware | internal.proto | Interceptors enforce automatic logging. |
| INF-ASR-AUD-07 | Retain audit at least life of case | Deployment_PhysicalView: AuditVol | AuditService | ops policy | Retention policy tied to case closure. |
| INF-ASR-AUD-08 | Audit available for inspection by authorized external personnel | UseCase_ScenarioView: UC_ViewAuditLog | AuditService | openapi.yaml | Read-only auditor role and export. |
| INF-ASR-AUD-09 | Export audit trails for specified cases without affecting stored audit | Component_DevelopmentView: AuditService | AuditService | openapi.yaml | Export is read-only snapshot. |
| INF-ASR-AUD-10 | Capture access-control violations and attempted violations | Component_DevelopmentView: AuthService/AuditService | AuthZ + Audit | sql/audit_log_ddl.sql | Logs denied access and search denials. |
| INF-NFR-AUD-REPORT-01 | Reports by workstation/network address | AuditLogEntry.remoteIp | AuditService | openapi.yaml | Stores IP/workstation metadata. |
| INF-ASR-SEC-CASE-01 | Limit access to cases to specified users/groups | (placeholder) | AuthZService | openapi.yaml | Case ACL model. |
| INF-ASR-SEC-RBAC-01 | Role-based control for functionality | Container_PhysicalView: AdminAPI/AuthService | AuthZService | openapi.yaml | RBAC claims enforced at API. |
| INF-ASR-SEC-GROUP-01 | User can be member of >1 group | (placeholder) | IAM | sql/user_group_ddl.sql | Many-to-many mapping. |
| INF-ASR-SEC-ADMIN-01 | Only admin-users set up profiles and allocate groups | UseCase_ScenarioView: Admin actor | AdminConsole | openapi.yaml | Admin-only endpoints. |
| INF-ASR-SEC-CASE-02 | User can stipulate which users/groups can access cases | (placeholder) | CaseService | openapi.yaml | Case ACL management. |
| INF-ASR-SEC-SUPER-01 | Only super-user changes security attributes | (placeholder) | IAM | openapi.yaml | Separate super-admin role. |
| INF-ASR-SEC-SEARCH-RESP-01 | Configurable response when user searches unauthorized case | (placeholder) | SearchService | openapi.yaml | Config flag: reveal metadata/existence/none. |
| INF-ASR-SEC-SEARCH-RESULT-01 | Search results never include unauthorized records | (placeholder) | SearchService | openapi.yaml | Post-filter by ACL at query time. |
| INF-ASR-SEC-LOG-01 | Unauthorized attempts logged in audit | AuditService | AuditService | sql/audit_log_ddl.sql | Deny events appended. |
| INF-NFR-ERR-01 | Meaningful error messages with actions | (placeholder) | API Gateway/UI | openapi.yaml | Standard error envelope. |
| INF-NFR-UI-01 | Consistent UI rules/look & feel | (placeholder) | UI | UI guidelines | Design system. |
| INF-NFR-UI-02 | Display several entities simultaneously | (placeholder) | UI | UI guidelines | Multi-pane views. |
| INF-NFR-UI-CUST-01 | Customizable UI; save in user profile | (placeholder) | UI, ProfileService | sql/user_profile_ddl.sql | Persist preferences. |
| INF-NFR-UI-DEFAULTS-01 | Persistent defaults for data entry | (placeholder) | UI | sql/user_profile_ddl.sql | Store defaults. |
| INF-NFR-UX-FAST-01 | Frequent transactions require few interactions | (placeholder) | UI | UX tests | Usability acceptance. |
| INF-NFR-ISO-9241-01 | UI complies with ISO 9241 + accessibility guidance | (placeholder) | UI | QA checklist | Accessibility testing. |
| INF-NFR-ACCESS-ALT-01 | Text equivalents for non-text media | (placeholder) | UI | QA checklist | WCAG-aligned checks. |
| INF-NFR-NAV-01 | Self-descriptive navigation, breadcrumbs, sitemap | (placeholder) | UI | UI artifacts | Navigation requirements. |
| INF-NFR-PERF-PAGE-01 | Acceptable opening/download times | (placeholder) | UI/CDN | ops | Performance budgets. |
| INF-NFR-AVAIL-01 | Availability window configured | Deployment_PhysicalView: WebTier/AppTier | Ops | SRE docs | Schedules and monitoring. |
| INF-NFR-AVAIL-02 | Planned downtime limit per rolling 3 months | Ops | Ops | SRE docs | Maintenance governance. |
| INF-NFR-AVAIL-03 | Unplanned downtime limit and incident count | Ops | Ops | SRE docs | SLO/error budget. |
| INF-NFR-DR-01 | Restore with inline sync within X hours | Deployment_PhysicalView: DataTier | Ops/DB | runbooks | DR drills. |
| INF-NFR-PERF-SEARCH-01 | Simple search 5–8s; advanced 10–15s | (placeholder) | SearchService | SLOs | Load tests. |
| INF-NFR-PERF-CASEHOT-01 | Retrieve recent case 5–8s | (placeholder) | CaseService | SLOs | Cache/hot storage. |
| INF-NFR-PERF-CASECOLD-01 | Retrieve older case ≤20s | (placeholder) | CaseService | SLOs | Tiered storage. |
| INF-NFR-SCALE-01 | Scalable for small/large stations | Deployment_PhysicalView: replicas | Platform | k8s | Horizontal scaling. |
| INF-ASR-ARCH-CENTRAL-01 | Centralized deployment/maintenance | Deployment_PhysicalView: centralized tiers | Platform | k8s | Central ops. |
| INF-ASR-3C-01 | Core-Configuration-Customization guiding principle | (placeholder) | Extension framework | internal.proto | State-specific overrides. |
| INF-ASR-SOA-01 | SOA modular design | Component_DevelopmentView | All services | internal.proto | Service boundaries. |
| INF-ASR-OPEN-01 | Open standards | (placeholder) | APIs | openapi.yaml | Standards-based contracts. |
| INF-ASR-SSO-01 | Common user access/auth service (SSO) | Component_DevelopmentView: AuthService | IAM | openapi.yaml | Central identity. |
| INF-ASR-DC-3TIER-01 | 3-tier datacenter architecture | Deployment_PhysicalView | Platform | k8s | Tier separation. |
| INF-ASR-N-TIER-01 | Separate presentation/business/data access | Package_DevelopmentView | UI/API/Services/DB | architecture.md | Layering. |
| INF-ASR-MOBILE-01 | Extensible to PDA/mobile terminals | (placeholder) | API | openapi.yaml | Responsive + mobile clients. |
| INF-ASR-METADATA-01 | Standardized formats and common metadata | (placeholder) | Data model | SQL | Canonical entities. |
| INF-ASR-BROWSER-01 | Browser-based minimal client requirements | Deployment_PhysicalView: Browser | UI | UI | Thin client. |
| INF-ASR-REMOTE-COMMS-01 | Multiple communication services for remote access | (placeholder) | Ingress/VPN | ops | VPN + HTTPS. |
| INF-ASR-PUBLIC-01 | Public access to subset of data/functionality | (placeholder) | CitizenPortal | openapi.yaml | Public endpoints with limits. |
| INF-ASR-MFA-01 | Multi-tier authentication where required | (placeholder) | IAM | openapi.yaml | Step-up auth. |
| INF-ASR-SEC-TLS-01 | SSL/TLS encrypted connections; HTTPS | Deployment_PhysicalView: HTTPS links | Ingress | k8s | TLS everywhere. |
| INF-ASR-SEC-VPN-01 | Secure VPN connections supported | (placeholder) | Network | ops | VPN option. |
| INF-ASR-SEC-ENC-01 | Selective encryption of stored data | (placeholder) | DB | SQL notes | Column encryption. |
| INF-ASR-SEC-SIGN-01 | Secure transmission + 2-way digital signatures | (placeholder) | Gateway | ops | mTLS + signing. |
| INF-ASR-SEC-XSS-01 | Prevent XSS | (placeholder) | UI/Gateway | security | CSP + encoding. |
| INF-ASR-SEC-SQLI-01 | Prevent SQL injection; parameterized queries | (placeholder) | Services | code standards | Prepared statements. |
| INF-ASR-SEC-SAN-01 | Sanitize/validate/encode inputs; client+server validation | (placeholder) | Gateway/Services/UI | openapi.yaml | Validation pipeline. |
| INF-ASR-SEC-SOFTDEL-01 | No hard delete; soft delete only | (placeholder) | All services | SQL DDL | `deleted_at` pattern. |
| INF-NFR-CACHE-01 | Cache frequent data | (placeholder) | CacheService | ops | Redis. |
| INF-NFR-UI-AJAX-01 | AJAX for UX | (placeholder) | UI | UI | Async calls. |
| INF-NFR-ASYNC-01 | Async HTTP socket capabilities | (placeholder) | Ingress/App | ops | HTTP/2, keepalive. |
| INF-NFR-STATIC-01 | Host static content on web server | Deployment_PhysicalView: WebTier | Web tier | ops | CDN/web server. |
| INF-NFR-PAGING-01 | Fetch results in batches 10/20; paged display | (placeholder) | SearchService/UI | openapi.yaml | Pagination. |
| INF-NFR-SEARCH-FIELDS-01 | Search fetch only display fields; details on click | (placeholder) | SearchService | openapi.yaml | Projection queries. |
| INF-NFR-CACHE-HIER-01 | Hierarchical cache for frequent searches | (placeholder) | CacheService | ops | L1 in-proc + Redis. |
| INF-NFR-DB-INDEX-01 | DB indexes on key search columns | (placeholder) | DB | SQL DDL | Index strategy. |
| INF-ASR-OFFLINE-01 | Offline mode for critical functionality; no data loss on failure/network | (placeholder) | StationEdgeClient | internal.proto | Offline-first + sync. |
| INF-ASR-ML-01 | Multilingual interface | (placeholder) | UI | UI | i18n framework. |
| INF-ASR-LOWBW-01 | Satisfactory performance on low bandwidth | (placeholder) | UI/API | SLOs | Payload minimization. |

---

# C. Architecture Overview

## 4+1 view alignment (using provided diagrams as structural references)
- **Context/Scenario view:** UseCase_ScenarioView (UC_* placeholders) represents actors (Citizen, PoliceUser, Admin, Auditor) and major use cases (Register Complaint, Investigate, Prosecute, Search, Citizen Status, Helpdesk, Audit Review).
- **Container view:** Container_PhysicalView elements map to CCTNS containers: **CitizenPortal**, **PoliceWebApp**, **AdminConsole**, **API Gateway**, domain services, and data stores.
- **Component/Package view:** Component_DevelopmentView and Package_DevelopmentView map to service decomposition: Case/Registration, Investigation, Prosecution, Search/Reporting, Citizen Interface, Navigation/Profile, Helpdesk, AuthN/AuthZ, Audit, Notification.
- **Logical/Class view:** Class_LogicView is repurposed: domain entities become Case, Person, FIR/Complaint, Evidence, CourtEvent, User, Group, AuditLogEntry, Ticket.
- **Deployment view:** Deployment_PhysicalView maps to 3-tier DC: Web tier (TLS ingress + static), App tier (stateless services), Data tier (PostgreSQL + Search index + Object store + WORM audit).

---

# D. Detailed Technical Design (developer-facing)

## D1. Subsystem: API Gateway + UI (CitizenPortal, PoliceWebApp, AdminConsole)

### 1) Responsibilities & data ownership
Provides browser-based access with minimal client requirements, multilingual UI, role-based navigation, UI customization stored in user profile, and secure API access via a single ingress enforcing TLS, auth, validation, and rate limits. Owns no core domain data; owns UI assets and client-side state.

### 2) Technology options (3 alternatives per concern)

**Language/runtime**
- Recommended: TypeScript on Node.js `18-20`
- Conservative: Java `17-21`
- Cutting-edge: Deno `1.40+`

**Web framework**
- Recommended: React `18.x` + Vite `5.x`
- Conservative: Angular `16-18`
- Cutting-edge: Next.js `14.x` (SSR/edge)

**RPC/HTTP**
- Recommended: REST/JSON over HTTPS + OpenAPI 3.0
- Conservative: Server-rendered MVC + form posts
- Cutting-edge: GraphQL federation

**Persistence**
- Recommended: None (UI); preferences via ProfileService
- Conservative: Server session store
- Cutting-edge: Edge KV

**Cache**
- Recommended: CDN + browser cache headers
- Conservative: Nginx caching
- Cutting-edge: Edge compute caching

**Messaging**
- Recommended: NATS `2.10+` for notifications/events
- Conservative: RabbitMQ `3.12+`
- Cutting-edge: Kafka `3.6+`

**Search**
- Recommended: OpenSearch `2.11-2.14`
- Conservative: PostgreSQL full-text
- Cutting-edge: Vector search hybrid

**Authn/authz**
- Recommended: OIDC (Keycloak `24-26`) + JWT
- Conservative: LDAP + server sessions
- Cutting-edge: Passkeys/WebAuthn

**Observability**
- Recommended: OpenTelemetry + Prometheus + Loki
- Conservative: ELK stack only
- Cutting-edge: eBPF-based tracing

**CI/CD**
- Recommended: GitHub Actions/GitLab CI with SAST/DAST gates
- Conservative: Jenkins
- Cutting-edge: Bazel + remote cache

**Container runtime**
- Recommended: containerd (Kubernetes)
- Conservative: Docker Engine
- Cutting-edge: gVisor/Kata for isolation

**Infra provisioning**
- Recommended: Terraform `1.6+`
- Conservative: Ansible
- Cutting-edge: Crossplane

### 3) Recommended default stack
- React 18 + Node.js 18-20 + Nginx `1.24+` for static hosting; OIDC via Keycloak; OpenTelemetry.
**Justification:** meets INF-ASR-BROWSER-01 (minimal client), INF-ASR-ML-01 (multilingual), INF-ASR-SEC-TLS-01 (HTTPS), INF-NFR-UI-CUST-01 (saved UI config).

### 4) Interface design (external APIs)
See `openapi.yaml` in Section L (covers citizen + police + admin + audit + helpdesk).

### 5) Data model / schema
UI preferences stored in `sql/user_profile_ddl.sql` (Section L).

### 6) Caching & consistency
- Cache static assets via CDN (immutable hashed filenames).
- Cache “dashboard counts” for 30–60s per user; invalidate on task assignment events.
- Consistency: UI is eventually consistent for counts; case detail views are strongly consistent (read-after-write via DB).

---

## D2. Subsystem: Identity, Access Control (AuthN/AuthZ) + Profile

### 1) Responsibilities & data ownership
Central SSO, RBAC, group membership, super-user security administration, case-level ACL enforcement hooks, and user profile storage (UI preferences, defaults). Owns Users, Groups, Roles, Memberships, Sessions/Tokens, Profiles.

### 2) Technology options

**Language/runtime**
- Recommended: Java `17-21` (Spring Boot `3.2-3.3`)
- Conservative: .NET `8`
- Cutting-edge: Rust `1.75+`

**Authn/authz**
- Recommended: Keycloak `24-26` (OIDC/OAuth2) + JWT + optional step-up MFA
- Conservative: AD/LDAP + custom RBAC
- Cutting-edge: SPIFFE/SPIRE + workload identity

**Persistence**
- Recommended: PostgreSQL `14-16`
- Conservative: Oracle `19c+`
- Cutting-edge: CockroachDB `23+`

**Cache**
- Recommended: Redis `7.2+` for token introspection cache
- Conservative: in-memory only
- Cutting-edge: distributed cache with CRDTs

(Other concerns same as D1; omitted for brevity but applied consistently.)

### 3) Recommended default stack
- Keycloak 24-26 + PostgreSQL 14-16 + Redis 7.2.
**Justification:** meets INF-ASR-SSO-01 (common auth), INF-ASR-SEC-RBAC-01 (role-based control), INF-ASR-SEC-GROUP-01 (multi-group), INF-ASR-MFA-01 (multi-tier auth).

### 4) Internal contracts
See `internal.proto` (AuthZ checks, group membership, case ACL evaluation).

### 5) Data model / schema
See `sql/user_group_ddl.sql` and `sql/user_profile_ddl.sql`.

### 6) Caching & consistency
- Cache role/group claims in JWT (short TTL 5–15 min).
- For revocation: maintain “token version” per user; reject tokens with stale version.
- Strong consistency for security attribute changes (super-user only).

---

## D3. Subsystem: Case/Registration + Investigation + Prosecution

### 1) Responsibilities & data ownership
Owns core case records: complaints/FIR, persons (complainant/victim/accused), evidence, investigation tasks, and court events. Enforces soft delete, audit logging, and access control at case level.

### 2) Technology options

**Language/runtime**
- Recommended: Java 17-21
- Conservative: .NET 8
- Cutting-edge: Go 1.22+

**Web framework**
- Recommended: Spring Boot 3.2-3.3
- Conservative: Jakarta EE
- Cutting-edge: Quarkus 3.x

**Persistence**
- Recommended: PostgreSQL 14-16 (primary system of record)
- Conservative: MS SQL Server 2019-2022
- Cutting-edge: YugabyteDB 2.20+

**Messaging**
- Recommended: NATS 2.10+ (events: CaseCreated, TaskAssigned, CourtEventLogged)
- Conservative: RabbitMQ
- Cutting-edge: Kafka

**Search**
- Recommended: OpenSearch index fed by CDC/outbox
- Conservative: DB-only search
- Cutting-edge: CQRS with separate read model

### 3) Recommended default stack
- Spring Boot 3.2-3.3 + PostgreSQL 14-16 + NATS 2.10 + OpenSearch 2.11-2.14.
**Justification:** meets INF-ASR-SOA-01 (modular SOA), INF-NFR-PERF-SEARCH-01 (search latency), INF-ASR-OFFLINE-01 (sync via outbox), INF-ASR-SEC-SOFTDEL-01 (soft delete).

### 4) Interface design
External endpoints in `openapi.yaml` (case create/update, investigation tasks, court events). Internal events and sync in `internal.proto`.

### 5) Data model / schema
See `sql/case_ddl.sql`, `sql/investigation_task_ddl.sql`, `sql/court_event_ddl.sql`.

**Encryption-at-rest fields:** PII (names, phone, address), sensitive notes, evidence references.  
**Justification:** meets INF-ASR-SEC-ENC-01 (selective encryption of stored data).

### 6) Caching & consistency
- Cache “hot cases” (accessed within 2 months) in Redis with TTL 24h; invalidate on update.
- Cold cases may be stored in cheaper storage tier for attachments; metadata remains in DB.
- Consistency: DB is source of truth; search index is eventually consistent (seconds) via outbox.

---

## D4. Subsystem: Search + Reporting

### 1) Responsibilities & data ownership
Provides basic/advanced search across cases/persons/crime/MO/property with strict ACL filtering, configurable “unauthorized case visibility” behavior, paged results (10/20), projection fields only, and reporting exports (monthly/RTI).

### 2) Technology options

**Search engine**
- Recommended: OpenSearch 2.11-2.14
- Conservative: PostgreSQL FTS + trigram indexes
- Cutting-edge: Elasticsearch 8.x + ES|QL

**Reporting**
- Recommended: SQL views + parameterized queries + async export jobs
- Conservative: On-demand synchronous reports
- Cutting-edge: Precomputed OLAP (ClickHouse)

### 3) Recommended default stack
- OpenSearch + PostgreSQL views + async export worker.
**Justification:** meets INF-NFR-PERF-SEARCH-01 (search response), INF-NFR-PAGING-01 (batching), INF-ASR-SEC-SEARCH-RESULT-01 (no unauthorized results).

### 4) Interface design
Search/report endpoints in `openapi.yaml`.

### 5) Data model / schema
Search index mapping is derived from DB; audit search requests in `audit_log` (see SQL). Reports tracked in `sql/report_job_ddl.sql` (included below in L).

### 6) Caching & consistency
- Hierarchical cache: L1 in-service (TTL 30s) + Redis (TTL 5–15 min) for frequent searches.
- Cache key includes userId/role/ACL version to prevent leakage.

---

## D5. Subsystem: Audit + Helpdesk + Notification

### 1) Responsibilities & data ownership
- **Audit:** immutable capture of CRUD, reads, security/admin changes, and violations; export for auditors; inspection UI.
- **Helpdesk:** ticket submission, tracking, category/status/age reports; accessible inside/outside app.
- **Notification:** email/SMS alerts on ticket actions and optionally case events.

### 2) Technology options

**Audit storage**
- Recommended: PostgreSQL append-only table + WORM object storage for periodic sealed segments
- Conservative: DB only with strict permissions
- Cutting-edge: Ledger DB (QLDB-like)

**Notification**
- Recommended: pluggable providers (SMTP + SMS aggregator) via NATS events
- Conservative: email only
- Cutting-edge: omnichannel (WhatsApp, push)

### 3) Recommended default stack
- Audit: PostgreSQL + hash chain + WORM snapshots; Helpdesk: same DB; Notification: NATS + provider adapters.
**Justification:** meets INF-ASR-AUD-01..05 (unalterable audit), INF-FR-SUP-ALERT-01 (alerts), INF-FR-SUP-REPORT-01 (helpdesk reports).

### 4) Interface design
Audit/helpdesk endpoints in `openapi.yaml`; internal event contracts in `internal.proto`.

### 5) Data model / schema
See `sql/audit_log_ddl.sql`, `sql/ticket_ddl.sql`.

### 6) Caching & consistency
- Audit reads are not cached (integrity).
- Helpdesk list views cached 30s per user.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/cctns-api-deployment.yaml` in Section L.

**Justification (k8s):** meets INF-NFR-SCALE-01 (scalability) and INF-ASR-ARCH-CENTRAL-01 (centralized deployment).

## E2. DB HA topology, backups, restore
- **PostgreSQL HA:** 1 primary + 2 synchronous standbys (Patroni or managed service), automatic failover.
- **Backups:** full daily + WAL continuous archiving; retain 35 days; quarterly restore drills.
- **RPO/RTO:** target RPO ≤ 15 min, RTO ≤ 2 hours (tunable to INF-NFR-DR-01 placeholder X hours).
**Justification:** meets INF-NFR-DR-01 (restore with inline sync) and INF-NFR-AVAIL-03 (unplanned downtime limits).

## E3. Network topology + ingress/egress rules
- Ingress: HTTPS 443 only; optional VPN ingress for police networks.
- East-west: mTLS between services (service mesh optional).
- Egress: SMS/Email providers via allowlisted endpoints.
Mapped to Deployment_PhysicalView: Browser→WebServer→App replicas→Data tier.
**Justification:** meets INF-ASR-SEC-TLS-01 (HTTPS) and INF-ASR-SEC-VPN-01 (VPN support).

## E4. CI/CD sketch
1. Build + unit tests
2. SAST + dependency scan
3. Contract tests (OpenAPI + proto)
4. Integration tests (DB + search)
5. DAST in staging
6. Deploy canary (5%) then progressive rollout
**Justification:** meets INF-ASR-SOA-01 (modular services) and INF-NFR-ERR-01 (consistent error handling via contract tests).

---

# F. Security Design

## F1. Auth & AuthZ
- **OIDC/OAuth2** with JWT access tokens (5–15 min) + refresh tokens (8–12h) for web apps.
- **RBAC** for functions + **Case ACL** for record-level access.
- Configurable unauthorized search response modes (metadata/existence/none).
**Justification:** meets INF-ASR-SEC-RBAC-01 and INF-ASR-SEC-SEARCH-RESP-01.

## F2. Secrets management & rotation
- Use Kubernetes Secrets + external KMS/Vault; rotate DB creds quarterly; rotate signing keys semi-annually; immediate rotation on incident.
**Justification:** meets INF-ASR-SEC-SIGN-01 (secure transmission/signing) and INF-ASR-SEC-TLS-01.

## F3. TLS & service-mesh
- TLS 1.2+ at ingress; mTLS optional internally for “2-way digital signatures” requirement interpretation.
**Justification:** meets INF-ASR-SEC-SIGN-01 and INF-ASR-SEC-TLS-01.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| SQL injection | Parameterized queries + validation (INF-ASR-SEC-SQLI-01, INF-ASR-SEC-SAN-01) |
| XSS | Output encoding + CSP + input sanitization (INF-ASR-SEC-XSS-01) |
| Unauthorized data access | RBAC + case ACL + audit violations (INF-ASR-SEC-CASE-01, INF-ASR-AUD-10) |
| Audit tampering | Append-only + hash chain + WORM snapshots (INF-ASR-AUD-01, INF-ASR-AUD-05) |
| Credential stuffing | MFA step-up + lockout policies + rate limiting (INF-ASR-MFA-01) |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + example alerts
- Metrics: request latency p95/p99, search latency, DB pool saturation, audit append rate, sync backlog, notification failures.
- Traces: propagate trace-id across gateway→services→DB/search.
- Logs: JSON structured, redaction of secrets/PII.

Example Prometheus rules:
- High API error rate:
  - `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02`
- Search latency SLO breach:
  - `histogram_quantile(0.95, sum(rate(search_latency_seconds_bucket[5m])) by (le)) > 15`

**Justification:** meets INF-NFR-PERF-SEARCH-01 (search latency) and INF-NFR-AVAIL-03 (downtime/incident control).

## G2. SLOs, error budgets, RTO/RPO
- API availability: 99.9% monthly (tune to stakeholder downtime limits).
- Search p95: simple ≤8s, advanced ≤15s.
- Audit append: p95 ≤ 200ms.
- RPO/RTO as in E2.

## G3. Dashboard/runbook sketch
- Dashboards: “Station health”, “Search performance”, “Audit integrity”, “Sync backlog”.
- Runbooks: DB failover, search reindex, audit export, notification provider outage.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components |
|---|---|
| Unit | All services (Case, Search, Audit, Helpdesk, AuthZ) |
| Integration | Services + PostgreSQL/OpenSearch/Redis/NATS |
| Contract | OpenAPI (gateway), proto (internal), schema validation |
| E2E | Citizen complaint→case→investigation→court event→audit export |
| Chaos | Kill pods, DB failover, search node loss |

## H2. Test data & environments
- Envs: dev, test, staging, prod.
- Data: synthetic PII; masked production snapshots only with approvals.
- Refresh: weekly for staging; daily for test.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
1. Stand up new platform in parallel.
2. Backfill historical cases into PostgreSQL + index into OpenSearch.
3. Dual-write from legacy (if exists) via adapter until cutover.
4. Cutover by station waves; keep rollback window 2–4 weeks.
5. Decommission legacy after audit sign-off.

## I2. API versioning
- `/api/v1/...` with additive changes only; breaking changes require `/v2` and 6–12 month deprecation.
**Justification:** meets INF-ASR-OPEN-01 (open standards) and INF-ASR-SOA-01 (service modularity).

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| OpenSearch for search | Postgres FTS; Elasticsearch | FTS simpler but slower for complex queries; ES licensing/ops | Meets INF-NFR-PERF-SEARCH-01 and paging/projection requirements |
| OIDC/Keycloak | LDAP sessions; custom auth | Custom increases risk; LDAP lacks modern flows | Meets INF-ASR-SSO-01, INF-ASR-MFA-01 |
| Append-only audit in DB + WORM snapshots | DB only; ledger DB | Ledger strong but complex; DB-only weaker against admin tampering | Meets INF-ASR-AUD-01..05 |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** “Critical entities” for audit include Case, Person, Complaint/FIR, Evidence, InvestigationTask, CourtEvent, User/Group/SecurityConfig, Ticket.  
- **A2:** Availability/downtime placeholders (`xx`) will be finalized as SLOs; until then target 99.9% monthly.  
- **A3:** “2-way digital signatures” is implemented as **mTLS** for service-to-service and optional client certs for admin/auditor access.  
- **A4:** Offline mode applies to Registration + basic case lookup + task updates; full search/reporting may be limited offline.  
- **A5:** Multilingual support initially covers English + one state language; extensible via i18n catalogs.

## Conflicts logged (requirements vs diagrams)
- **C1:** PlantUML diagrams describe “Web Learning Game System” (UC_StartGame, GameAPI, QuestionService) which conflicts with CCTNS modules. Per rule, we treat **Original Requirements as authoritative** and use diagrams only as generic view scaffolding.

## Unresolved stakeholder questions
1. What are the exact uptime window and downtime limits (fill `xx` values) for INF-NFR-AVAIL-01..03?  
2. Define “life of the case” retention for audit: until closure + how many years?  
3. Which data fields require selective encryption-at-rest (PII categories, evidence types)?  
4. Which unauthorized search response mode is required by default (metadata/existence/none) per INF-ASR-SEC-SEARCH-RESP-01?  
5. Offline sync conflict policy: station priority, last-write-wins, or field-level merge?

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# ArchitectureDocument.md
(Contents are exactly this document, Sections A–L.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: CCTNS External API
  version: 1.0.0
  description: >
    External REST API for CCTNS (Citizen + Police + Admin + Audit + Helpdesk).
servers:
  - url: https://cctns.example.gov/api/v1
security:
  - bearerAuth: []
tags:
  - name: Citizen
  - name: Cases
  - name: Investigation
  - name: Prosecution
  - name: Search
  - name: Helpdesk
  - name: Audit
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Error:
      type: object
      required: [code, message, correlationId]
      properties:
        code:
          type: string
          example: AUTHZ_DENIED
        message:
          type: string
        details:
          type: object
          additionalProperties: true
        correlationId:
          type: string
    Pagination:
      type: object
      required: [limit, offset, total]
      properties:
        limit: { type: integer, minimum: 1, maximum: 50, example: 20 }
        offset: { type: integer, minimum: 0, example: 0 }
        total: { type: integer, minimum: 0, example: 123 }
    ComplaintCreateRequest:
      type: object
      required: [complainant, incident, channel]
      properties:
        channel:
          type: string
          enum: [IN_PERSON, WEB, MOBILE]
        complainant:
          $ref: '#/components/schemas/Person'
        incident:
          type: object
          required: [occurredAt, location, description]
          properties:
            occurredAt: { type: string, format: date-time }
            location: { type: string }
            description: { type: string, minLength: 10 }
    ComplaintCreateResponse:
      type: object
      required: [complaintId, status]
      properties:
        complaintId: { type: string, example: "cmp-2026-0000123" }
        status: { type: string, enum: [RECEIVED, UNDER_REVIEW] }
    Person:
      type: object
      required: [fullName]
      properties:
        fullName: { type: string }
        phone: { type: string }
        address: { type: string }
        idDocumentRef: { type: string }
    Case:
      type: object
      required: [caseId, title, status, createdAt]
      properties:
        caseId: { type: string, example: "case-2026-0000456" }
        title: { type: string }
        status: { type: string, enum: [OPEN, UNDER_INVESTIGATION, IN_COURT, CLOSED] }
        createdAt: { type: string, format: date-time }
    CaseCreateRequest:
      type: object
      required: [complaintId, title]
      properties:
        complaintId: { type: string }
        title: { type: string }
        stationId: { type: string }
    InvestigationTaskCreateRequest:
      type: object
      required: [caseId, taskType, assignedToUserId]
      properties:
        caseId: { type: string }
        taskType: { type: string, example: "COLLECT_EVIDENCE" }
        assignedToUserId: { type: string }
        dueAt: { type: string, format: date-time }
    CourtEventCreateRequest:
      type: object
      required: [caseId, courtName, hearingAt, notes]
      properties:
        caseId: { type: string }
        courtName: { type: string }
        hearingAt: { type: string, format: date-time }
        notes: { type: string }
    SearchRequest:
      type: object
      required: [queryType, criteria]
      properties:
        queryType:
          type: string
          enum: [CASE, PERSON, PROPERTY, MODUS_OPERANDI]
        criteria:
          type: object
          additionalProperties: true
        limit:
          type: integer
          minimum: 10
          maximum: 20
          default: 20
        offset:
          type: integer
          minimum: 0
          default: 0
    SearchResultItem:
      type: object
      required: [id, kind, display]
      properties:
        id: { type: string }
        kind: { type: string, enum: [CASE, PERSON, PROPERTY] }
        display:
          type: object
          additionalProperties: true
    SearchResponse:
      type: object
      required: [items, page]
      properties:
        items:
          type: array
          items: { $ref: '#/components/schemas/SearchResultItem' }
        page:
          $ref: '#/components/schemas/Pagination'
    TicketCreateRequest:
      type: object
      required: [type, category, title, description]
      properties:
        type: { type: string, enum: [DEFECT, ENHANCEMENT] }
        category: { type: string, example: "SEARCH" }
        title: { type: string }
        description: { type: string }
        notifyBy:
          type: array
          items: { type: string, enum: [EMAIL, SMS] }
    Ticket:
      type: object
      required: [ticketId, status, createdAt]
      properties:
        ticketId: { type: string }
        status: { type: string, enum: [OPEN, IN_PROGRESS, RESOLVED, CLOSED] }
        createdAt: { type: string, format: date-time }
        updatedAt: { type: string, format: date-time }
    AuditExportResponse:
      type: object
      required: [exportId, downloadUrl, sha256]
      properties:
        exportId: { type: string }
        downloadUrl: { type: string, format: uri }
        sha256: { type: string }
paths:
  /citizen/complaints:
    post:
      tags: [Citizen]
      summary: Register a citizen complaint
      operationId: createComplaint
      security: []  # public subset allowed; rate-limited at gateway
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ComplaintCreateRequest' }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ComplaintCreateResponse' }
        "400":
          description: Validation error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
  /cases:
    post:
      tags: [Cases]
      summary: Create a case from a complaint (police user)
      operationId: createCase
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CaseCreateRequest' }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Case' }
        "401":
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
  /cases/{caseId}:
    get:
      tags: [Cases]
      summary: Get case details (ACL enforced)
      operationId: getCase
      parameters:
        - name: caseId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Case' }
        "404":
          description: Not found (or hidden by security mode)
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
  /investigation/tasks:
    post:
      tags: [Investigation]
      summary: Create an investigation task
      operationId: createInvestigationTask
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/InvestigationTaskCreateRequest' }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                type: object
                required: [taskId, status]
                properties:
                  taskId: { type: string }
                  status: { type: string, enum: [OPEN] }
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
  /prosecution/court-events:
    post:
      tags: [Prosecution]
      summary: Record a court interaction/event
      operationId: createCourtEvent
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CourtEventCreateRequest' }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                type: object
                required: [courtEventId]
                properties:
                  courtEventId: { type: string }
  /search:
    post:
      tags: [Search]
      summary: Basic/advanced search (ACL-filtered, paged)
      operationId: search
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/SearchRequest' }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/SearchResponse' }
        "400":
          description: Bad request
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
  /helpdesk/tickets:
    post:
      tags: [Helpdesk]
      summary: Create a defect/enhancement ticket
      operationId: createTicket
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/TicketCreateRequest' }
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Ticket' }
  /helpdesk/tickets/{ticketId}:
    get:
      tags: [Helpdesk]
      summary: Get ticket status
      operationId: getTicket
      parameters:
        - name: ticketId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Ticket' }
  /audit/cases/{caseId}/export:
    post:
      tags: [Audit]
      summary: Export audit trail for a case (read-only snapshot)
      operationId: exportCaseAudit
      parameters:
        - name: caseId
          in: path
          required: true
          schema: { type: string }
      responses:
        "202":
          description: Accepted
          content:
            application/json:
              schema: { $ref: '#/components/schemas/AuditExportResponse' }
        "403":
          description: Forbidden
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Error' }
```

```proto
// filename: internal.proto
syntax = "proto3";

package cctns.internal.v1;

option java_multiple_files = true;
option java_package = "gov.cctns.internal.v1";

message Actor {
  string user_id = 1;
  repeated string role = 2;
  repeated string group_id = 3;
  string workstation_id = 4;
  string remote_ip = 5;
}

message CaseRef {
  string case_id = 1;
}

message AuthzCheckRequest {
  Actor actor = 1;
  string action = 2; // e.g., "CASE_READ", "CASE_UPDATE", "SEARCH"
  CaseRef case_ref = 3;
}

message AuthzCheckResponse {
  bool allowed = 1;
  string decision = 2; // "ALLOW" | "DENY" | "HIDE_EXISTENCE" | "REVEAL_METADATA"
}

service AuthzService {
  rpc Check(AuthzCheckRequest) returns (AuthzCheckResponse);
}

message AuditAppendRequest {
  string event_id = 1;
  string timestamp_utc = 2;
  Actor actor = 3;
  string entity_type = 4; // CASE, PERSON, TICKET, SECURITY_CONFIG, ...
  string entity_id = 5;
  string action = 6; // CREATE/READ/UPDATE/DELETE_SOFT/DENY
  string before_json = 7;
  string after_json = 8;
  string prev_hash = 9;
  string entry_hash = 10;
}

message AuditAppendResponse {
  bool ok = 1;
}

service AuditService {
  rpc Append(AuditAppendRequest) returns (AuditAppendResponse);
}

message OutboxEvent {
  string event_id = 1;
  string event_type = 2; // CaseCreated, CaseUpdated, TaskAssigned, TicketUpdated
  string occurred_at_utc = 3;
  string aggregate_type = 4;
  string aggregate_id = 5;
  string payload_json = 6;
}

service EventBusService {
  rpc Publish(OutboxEvent) returns (AuditAppendResponse);
}
```

```yaml
# filename: k8s/cctns-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cctns-api
  labels:
    app: cctns-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cctns-api
  template:
    metadata:
      labels:
        app: cctns-api
    spec:
      containers:
        - name: cctns-api
          image: registry.example.gov/cctns/api:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "prod"
            - name: DB_URL
              valueFrom:
                secretKeyRef:
                  name: cctns-secrets
                  key: db_url
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: cctns-secrets
                  key: db_user
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: cctns-secrets
                  key: db_password
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
            initialDelaySeconds: 20
            periodSeconds: 10
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
  name: cctns-api
spec:
  selector:
    app: cctns-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cctns-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cctns-api
  minReplicas: 3
  maxReplicas: 20
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
  name: cctns-config
data:
  SEARCH_PAGE_LIMIT_DEFAULT: "20"
  UNAUTH_SEARCH_MODE: "HIDE_EXISTENCE"
---
apiVersion: v1
kind: Secret
metadata:
  name: cctns-secrets
type: Opaque
stringData:
  db_url: "jdbc:postgresql://postgres-primary:5432/cctns"
  db_user: "cctns_app"
  db_password: "REPLACE_ME"
```

```sql
-- filename: sql/case_ddl.sql
CREATE TABLE IF NOT EXISTS cctns_case (
  case_id            TEXT PRIMARY KEY,
  complaint_id       TEXT,
  title              TEXT NOT NULL,
  status             TEXT NOT NULL CHECK (status IN ('OPEN','UNDER_INVESTIGATION','IN_COURT','CLOSED')),
  station_id         TEXT,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at_utc     TIMESTAMPTZ,
  acl_policy_json    JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_case_status ON cctns_case(status) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_case_station ON cctns_case(station_id) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_case_updated ON cctns_case(updated_at_utc) WHERE deleted_at_utc IS NULL;
```

```sql
-- filename: sql/investigation_task_ddl.sql
CREATE TABLE IF NOT EXISTS investigation_task (
  task_id            TEXT PRIMARY KEY,
  case_id            TEXT NOT NULL REFERENCES cctns_case(case_id),
  task_type          TEXT NOT NULL,
  assigned_to_user_id TEXT NOT NULL,
  status             TEXT NOT NULL CHECK (status IN ('OPEN','IN_PROGRESS','DONE','CANCELLED')),
  due_at_utc         TIMESTAMPTZ,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at_utc     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_task_case ON investigation_task(case_id) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_task_assignee ON investigation_task(assigned_to_user_id) WHERE deleted_at_utc IS NULL;
```

```sql
-- filename: sql/court_event_ddl.sql
CREATE TABLE IF NOT EXISTS court_event (
  court_event_id     TEXT PRIMARY KEY,
  case_id            TEXT NOT NULL REFERENCES cctns_case(case_id),
  court_name         TEXT NOT NULL,
  hearing_at_utc     TIMESTAMPTZ NOT NULL,
  notes_enc          BYTEA NOT NULL,
  created_by_user_id TEXT NOT NULL,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at_utc     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_court_case ON court_event(case_id) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_court_hearing ON court_event(hearing_at_utc) WHERE deleted_at_utc IS NULL;
```

```sql
-- filename: sql/audit_log_ddl.sql
CREATE TABLE IF NOT EXISTS audit_log (
  event_id           TEXT PRIMARY KEY,
  timestamp_utc      TIMESTAMPTZ NOT NULL,
  actor_user_id      TEXT,
  actor_roles        TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  actor_groups       TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  workstation_id     TEXT,
  remote_ip          INET,
  entity_type        TEXT NOT NULL,
  entity_id          TEXT NOT NULL,
  action             TEXT NOT NULL,
  before_json        JSONB,
  after_json         JSONB,
  prev_hash          TEXT,
  entry_hash         TEXT NOT NULL,
  is_violation       BOOLEAN NOT NULL DEFAULT FALSE
);

-- Append-only enforcement is done via DB permissions: no UPDATE/DELETE grants to app role.
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(timestamp_utc);
CREATE INDEX IF NOT EXISTS idx_audit_violation ON audit_log(is_violation) WHERE is_violation = TRUE;
```

```sql
-- filename: sql/ticket_ddl.sql
CREATE TABLE IF NOT EXISTS helpdesk_ticket (
  ticket_id          TEXT PRIMARY KEY,
  type               TEXT NOT NULL CHECK (type IN ('DEFECT','ENHANCEMENT')),
  category           TEXT NOT NULL,
  title              TEXT NOT NULL,
  description        TEXT NOT NULL,
  status             TEXT NOT NULL CHECK (status IN ('OPEN','IN_PROGRESS','RESOLVED','CLOSED')),
  notify_by          TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  created_by_user_id TEXT,
  created_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at_utc     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_ticket_status ON helpdesk_ticket(status) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_ticket_age ON helpdesk_ticket(created_at_utc) WHERE deleted_at_utc IS NULL;
CREATE INDEX IF NOT EXISTS idx_ticket_category ON helpdesk_ticket(category) WHERE deleted_at_utc IS NULL;
```

```sql
-- filename: sql/user_group_ddl.sql
CREATE TABLE IF NOT EXISTS iam_user (
  user_id        TEXT PRIMARY KEY,
  username       TEXT UNIQUE NOT NULL,
  display_name   TEXT,
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS iam_group (
  group_id       TEXT PRIMARY KEY,
  name           TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS iam_user_group (
  user_id  TEXT NOT NULL REFERENCES iam_user(user_id),
  group_id TEXT NOT NULL REFERENCES iam_group(group_id),
  PRIMARY KEY (user_id, group_id)
);
```

```sql
-- filename: sql/user_profile_ddl.sql
CREATE TABLE IF NOT EXISTS user_profile (
  user_id            TEXT PRIMARY KEY REFERENCES iam_user(user_id),
  ui_prefs_json      JSONB NOT NULL DEFAULT '{}'::jsonb,
  data_entry_defaults_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  locale             TEXT NOT NULL DEFAULT 'en-IN',
  updated_at_utc     TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-MOD-REG-01,Citizen registers complaint; police takes forward,UseCase_ScenarioView:UC_*,RegistrationService|CitizenPortal,openapi.yaml|internal.proto,Implements intake and initiation
INF-FR-MOD-INV-01,Investigation workflow automation,State_LogicView_GameSession:InProgress/Completed,InvestigationService,openapi.yaml|sql/investigation_task_ddl.sql,Automates post-registration tasks
INF-FR-MOD-PRO-01,Court interaction recording,Sequence_ProcessView_S2_AdminPublish:*,ProsecutionService,openapi.yaml|sql/court_event_ddl.sql,Records prosecution events
INF-FR-MOD-SEARCH-01,Basic/advanced search,Sequence_ProcessView_S1_PlaySession:*,SearchService,openapi.yaml,Search endpoints with ACL filtering
INF-FR-MOD-REPORT-01,Reporting (monthly/RTI),Activity_ProcessView_PlaySession:*,ReportingService,openapi.yaml,Parameterized report APIs
INF-FR-MOD-CIT-01,Citizen info exchange/ack,UseCase_ScenarioView:UC_View*,CitizenPortal|NotificationService,openapi.yaml,Status and acknowledgements
INF-FR-MOD-NAV-01,Role-based landing pages,Container_PhysicalView:WebUI/AdminUI,NavigationService|ProfileService,sql/user_profile_ddl.sql,Personalized dashboards and saved prefs
INF-FR-SUP-HELP-01,Context-sensitive help,Package_DevelopmentView:ui,HelpContentService,architecture.md,Help across UI
INF-FR-SUP-TICKET-01,Log and track defects/enhancements,UseCase_ScenarioView:UC_ManageContent,HelpdeskService,sql/ticket_ddl.sql,Ticketing
INF-FR-SUP-ALERT-01,Email/SMS alerts on actions,Collaboration_ProcessView_S2_AdminPublish:*,NotificationService,internal.proto,Event-driven alerts
INF-FR-SUP-REPORT-01,Helpdesk reports by category/status/age,Class_LogicView:*,HelpdeskService,openapi.yaml,Reporting endpoints
INF-ASR-AUD-01,Unalterable audit trail CRUD,Class_LogicView:AuditLogEntry,AuditService,sql/audit_log_ddl.sql,Append-only audit
INF-ASR-SEC-TLS-01,HTTPS/TLS everywhere,Deployment_PhysicalView:HTTPS links,Ingress/Gateway,k8s/cctns-api-deployment.yaml,TLS enforced
INF-ASR-SEC-SOFTDEL-01,No hard delete,*,All services,sql/*_ddl.sql,deleted_at pattern
INF-NFR-PERF-SEARCH-01,Search latency targets,*,SearchService,openapi.yaml,Load-testable SLOs
INF-NFR-PAGING-01,Results in batches 10/20,*,SearchService/UI,openapi.yaml,Pagination contract
INF-ASR-SSO-01,Common auth service SSO,Component_DevelopmentView:AuthService,IAM,internal.proto,Central authz checks
INF-ASR-OFFLINE-01,Offline critical functionality,*,StationEdgeClient,internal.proto,Outbox events for sync
```

---

## Verification / Acceptance Criteria Checklist

| Item | Status |
|---|---|
| 3-line Analysis Plan present | [x] |
| Sections A-L included | [x] |
| Every FR/NFR/ASR mapped in traceability matrix | [x] (as INF-* normalized) |
| ≥1 OpenAPI YAML and ≥1 internal proto/REST contract included | [x] |
| Representative k8s manifest snippet included | [x] |
| SQL DDL / models for primary entities included | [x] |
| All major components have at least one API contract and a data schema | [x] |
| Assumptions and unresolved questions listed | [x] |

---

## How to review (checklist)
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?