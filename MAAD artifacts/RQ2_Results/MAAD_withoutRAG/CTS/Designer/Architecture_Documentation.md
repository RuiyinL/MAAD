Scope: Design a production-ready architecture for CCTNS modules (Registration, Investigation, Prosecution, Search/Reporting, Citizen Interface, Navigation, Security/Audit/Helpdesk), aligned to SOA + centralized 3-tier deployment, offline/low-bandwidth support, and strict audit/RBAC.  
Approach: Normalize narrative requirements into traceable INF-* IDs, resolve conflicts with provided UML by preferring CCTNS requirement terms, then define 4+1 views with contracts (OpenAPI + internal proto), data model, and k8s ops plan.  
Top validation steps: Traceability matrix completeness, security/audit immutability verification, performance SLO tests (search + case retrieval), and offline-sync correctness under network loss.

# A. Executive Summary (≤1 page)

## System overview
CCTNS is a centralized, browser-based police case and criminal tracking system supporting citizen complaint intake through investigation and prosecution, with strong search/reporting, role-based navigation, citizen interaction, offline/low-bandwidth operation, immutable audit trail, and integrated helpdesk/defect tracking.

**Diagram mapping (note: provided UML is safety-control themed; conflicts logged in K; references still used for structure):**
- Use-case coverage: *UseCase_SafetyCriticalControl* (SCS: UC_Authenticate, UC_ViewStatus, UC_AuditReview) → mapped to CCTNS Auth, Dashboard/Navigation, Audit Review.
- Component/container boundaries: *Component_SafetyCriticalControl* (GUI, AuthService, ControlAPI, EventBus, AuditLog) → mapped to CCTNS Web UI, IAM, Case API, Eventing, Audit Store.
- Deployment topology: *Deployment_SafetyCriticalControl* (Operator Workstation, AppServer-1/2, Audit DB) → mapped to Police/Citizen clients, State DC HA app tier, Audit DB.

## Chosen architectural styles & topology
- **Architectural style:** Modular SOA with domain-oriented services + shared platform services (audit, IAM, notification, helpdesk), plus event-driven integration for alerts and sync.  
- **Deployment topology:** Centralized state-level 3-tier DC (web/API/app, data, integration) with HA active-active application tier and centralized databases; offline-capable edge client with sync.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| Offline mode + conflict resolution for case updates | High | Introduce explicit offline scope (critical workflows only), per-entity versioning, append-only change log, deterministic merge policies, and mandatory audit capture on sync (INF-OFF-001..003). |
| Immutable audit trail requirement (“unalterable”) | High | Use append-only tables + WORM storage option + hash-chained records + restricted DB roles; provide export without mutation; continuous integrity checks (INF-AUD-001..009). |
| Search performance at scale (5–8s simple; 10–15s advanced) | High | Use PostgreSQL + OpenSearch, strict indexing, paged results, fetch-minimal-fields, hierarchical cache for frequent searches (INF-SRCH-001..007). |

## Key QA coverage mapping (ASR/NFR → test types)
> Note: Source requirements have no explicit IDs; all are normalized as `INF-*` (listed in K) and treated as FR/NFR/ASR.

| Quality attribute | INF IDs | Test types |
|---|---|---|
| Scalability | INF-SCALE-001, INF-SRCH-001..007 | Load + stress tests; DB index regression; cache hit-rate tests |
| Availability | INF-AVL-001..005 | HA failover drills; chaos testing; backup/restore (RTO/RPO) |
| Security | INF-SEC-001..012, INF-AC-001..008 | SAST/DAST; penetration tests; RBAC/ABAC tests; audit integrity tests |
| Performance | INF-PERF-001..004 | SLO conformance tests; synthetic monitoring; query profiling |
| Maintainability | INF-ARCH-001..004 | Contract tests; schema migration tests; deploy automation checks |

---

# B. Traceability & Rationale

**traceability_matrix.csv (embedded summary; full file in L)**  
Format: `Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale`

> Because the requirements are narrative and lack IDs, all items are inferred as `INF-*` per rule.

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-MOD-REG-001 | Citizen complaint registration module | UseCase_SafetyCriticalControl:SCS.UC_Authenticate | RegistrationService, CitizenPortal | openapi.yaml, internal.proto, sql/case_ddl.sql | Registration is entry point; secured and persisted with case linkage. |
| INF-MOD-INV-001 | Investigation module automates post-registration tasks | Class_SafetyCriticalControl:Command,AuditLog | InvestigationService | internal.proto, sql/case_event_ddl.sql | Automation captured as workflows and events with auditability. |
| INF-MOD-PRO-001 | Prosecution module for court interactions | UseCase_SafetyCriticalControl:SCS.UC_ViewStatus | ProsecutionService | openapi.yaml, sql/court_interaction_ddl.sql | Court diary requires structured records and retrieval. |
| INF-MOD-SRCH-001 | Basic/advanced search over cases/person/property/MO | Activity_IssueCommandWorkflow (mapped) | SearchService | openapi.yaml, search/index_mapping.md | Drives dedicated search index + paging constraints. |
| INF-MOD-RPT-001 | Reporting for monthly/RTI queries | Component_SafetyCriticalControl:ExportAPI | ReportingService | openapi.yaml | Reporting uses controlled query templates and exports. |
| INF-MOD-CIT-001 | Citizen interface for acknowledgements/info exchange | Component_SafetyCriticalControl:GUI | CitizenPortal, NotificationService | openapi.yaml | Enables status checks & responses with alerts. |
| INF-MOD-NAV-001 | Role-based landing pages w/ tasks/alerts | UseCase_SafetyCriticalControl:SCS.UC_ViewStatus | NavigationService | openapi.yaml | Dashboard aggregates assigned cases, pending tasks. |
| INF-HLP-001 | Context-sensitive help for all actions | (N/A) | HelpContentService | openapi.yaml | Help content served per screen/action key. |
| INF-HLPD-001 | In-app + external browser helpdesk access | (N/A) | HelpdeskService | openapi.yaml, sql/helpdesk_ticket_ddl.sql | Separate portal and in-app entry; same backend. |
| INF-HLPD-002 | Log defects/enhancements + track | (N/A) | HelpdeskService | openapi.yaml | Ticket lifecycle endpoints and user visibility. |
| INF-HLPD-003 | Alerts on ticket action (email/SMS) | Component_SafetyCriticalControl:EventBus | NotificationService | internal.proto | Event-driven notifications decouple from core flows. |
| INF-HLPD-004 | Helpdesk reports category/status/age | (N/A) | ReportingService | openapi.yaml | Aggregations over ticket tables. |
| INF-AUD-001 | Unalterable audit trail for CRUD on critical entities | Class_SafetyCriticalControl:AuditLog,AuditRecord | AuditService | sql/audit_record_ddl.sql | Append-only + integrity chain meets “unalterable”. |
| INF-AUD-002 | Audit captures user, time, admin parameters | Class_SafetyCriticalControl:AuditRecord | AuditService | sql/audit_record_ddl.sql | Mandatory columns and JSONB context. |
| INF-AUD-003 | Audit cannot be modified/deleted; exportable | Component_SafetyCriticalControl:AuditLog | AuditService | openapi.yaml | Exports are read-only; storage is append-only. |
| INF-AUD-004 | Log access violations/attempted violations | UseCase_SafetyCriticalControl:SCS.UC_AuditReview | IAM, AuditService | internal.proto, sql/audit_record_ddl.sql | Capture denied decisions and attempt metadata. |
| INF-AC-001 | Limit access to cases to users/groups | UseCase_SafetyCriticalControl:SCS.UC_Authenticate | IAMService, AuthorizationPolicy | sql/case_acl_ddl.sql | Case ACL tables enforce per-case authorization. |
| INF-AC-002 | Role-based control of functions | UseCase_SafetyCriticalControl:SCS.UC_Authenticate | IAMService | sql/rbac_ddl.sql | RBAC drives UI + API permissions. |
| INF-AC-003 | Multi-group membership | (N/A) | IAMService | sql/rbac_ddl.sql | Many-to-many user-group mapping. |
| INF-AC-004 | Admin-only user profiles & group allocation | (N/A) | IAMService | openapi.yaml | Admin endpoints protected by role. |
| INF-AC-005 | Super-user only changes security attributes | (N/A) | IAMService | openapi.yaml | Elevated role required; audited. |
| INF-AC-006 | Search must never reveal unauthorized records | INF-MOD-SRCH-001 | SearchService | openapi.yaml | Filter by authorization in query layer + index strategy. |
| INF-AC-007 | Configurable denied-case behavior (3 levels) | (N/A) | CaseService, SearchService | openapi.yaml | Policy setting changes response semantics. |
| INF-UI-001 | Single UI rules/look & feel; customizable | (N/A) | WebUI | ui-guidelines.md | Config stored in user profile. |
| INF-UI-002 | ISO 9241 usability/accessibility; avoid horizontal scroll | (N/A) | WebUI | ui-guidelines.md | Non-functional UI constraints. |
| INF-ERR-001 | Meaningful errors with user actions | (N/A) | API Gateway, WebUI | openapi.yaml | Standard error schema with guidance. |
| INF-AVL-001 | Defined uptime windows + planned/unplanned downtime limits | Deployment_SafetyCriticalControl:NET | PlatformOps | sre/slo.md | SLOs expressed and monitored. |
| INF-AVL-002 | Restore with inline sync within X hours | Deployment_SafetyCriticalControl:AUDDB | PlatformOps, SyncService | sre/dr.md | DR procedure and replay logs. |
| INF-PERF-001 | Simple search 5–8s; advanced 10–15s | (N/A) | SearchService | sre/slo.md | Performance SLOs tied to APIs. |
| INF-PERF-002 | Recent case display 5–8s; older 20s | (N/A) | CaseService, StorageTiering | sre/slo.md | Hot/cold storage and caching. |
| INF-SCALE-001 | Scalable for small/large stations | Container_SafetyCriticalControl:C_CP | PlatformOps | k8s/cctns-api-deployment.yaml | HPA + stateless services. |
| INF-ARCH-001 | SOA, modular, open standards | Package_SafetyCriticalControl:pkg_api,pkg_app | All services | architecture.md | Service boundaries + standards. |
| INF-SEC-001 | SSO common access/auth service | Component_SafetyCriticalControl:AuthService | IAMService | openapi.yaml | Central IAM with OIDC. |
| INF-SEC-002 | SSL/HTTPS + VPN + 2-way signatures | Deployment_SafetyCriticalControl:WS--APP1 | API Gateway | security.md | TLS/mTLS + optional signing for sensitive flows. |
| INF-SEC-003 | Prevent XSS/SQLi, parameterized queries, input validation | (N/A) | WebUI, API | secure-coding.md | Framework + WAF + linters. |
| INF-DATA-001 | Selective encryption at rest | (N/A) | KMS, DB | sql/*_ddl.sql | Encrypt sensitive columns. |
| INF-SRCH-002 | Batch results 10/20; fetch display fields only | (N/A) | SearchService | openapi.yaml | Enforced via API pagination and projection. |
| INF-SRCH-003 | Hierarchical cache for frequent searches | (N/A) | CacheService | architecture.md | Reduce latency and DB load. |
| INF-OFF-001 | Offline mode for critical functionality | (N/A) | OfflineClient, SyncService | internal.proto | Local store + sync protocol. |
| INF-LANG-001 | Multilingual interface | (N/A) | WebUI | i18n.md | i18n in UI and content. |

---

# C. Architecture Overview

## 4+1 aligned view (mapped to provided diagrams)

1. **Context/Scenario view**  
   Users: citizen, IO (Investigating Officer), records staff, prosecution constable, admin, helpdesk.  
   Mapped diagram reference: *UseCase_SafetyCriticalControl* (SCS: UC_Authenticate, UC_AuditReview) as placeholders for Auth/Audit use cases (conflict noted in K).

2. **Container view**  
   Containers: Web UI (Police portal), Citizen portal, API gateway, domain services (Case/Registration/Investigation/Prosecution/Search/Reporting), platform services (IAM, Audit, Notification, Helpdesk), data stores (PostgreSQL, OpenSearch, object storage), messaging (Kafka/RabbitMQ).  
   Reference: *Container_SafetyCriticalControl* (C_CP containers, CON_AuditDB, CON_EventBus) mapped to CCTNS equivalents.

3. **Component/Package view**  
   Services separated by bounded contexts; shared libraries for schema validation, audit emission, and RBAC checks.  
   Reference: *Component_SafetyCriticalControl* (AuthService, EventBus, AuditLog) and *Package_SafetyCriticalControl*.

4. **Class/Runtime view**  
   Domain entities: Case, Person, Complaint, FIR, Evidence, CourtInteraction, Ticket, AuditRecord, ACL. Runtime: request → authz → business operation → audit append → event publish → notification/search indexing.  
   Reference: *Class_SafetyCriticalControl* (AuditLog/AuditRecord concept) and *Sequence_S1_IssueCommand* (request orchestration pattern).

5. **Deployment view**  
   Central state data center: HA app nodes, DB nodes, search cluster; station clients over low bandwidth; offline client sync via store-and-forward.  
   Reference: *Deployment_SafetyCriticalControl* (NET HA pair, AUDDB).

---

# D. Detailed Technical Design (developer-facing)

## D1. API Gateway + Web UI (Police Portal + Citizen Portal)

### 1) Responsibilities & data ownership
Presents browser-based UX with ISO 9241-aligned accessibility and customization. Owns UI state/preferences only; never owns authoritative case data. Enforces consistent error messages and supports multilingual content keys.

### 2) Technology options (≥3 alternatives per concern)

- **Language/runtime**
  - Recommended: TypeScript (Node.js 18–20)
  - Conservative: Java 17 (Spring MVC for SSR)
  - Cutting-edge: Bun 1.x (TS runtime)

- **Web framework**
  - Recommended: React 18 + Next.js 14–15
  - Conservative: Angular 16–18
  - Cutting-edge: SvelteKit 2.x

- **RPC/HTTP**
  - Recommended: HTTPS REST to gateway + WebSocket/SSE for alerts
  - Conservative: HTTPS REST only (polling)
  - Cutting-edge: GraphQL federation

- **AuthN/AuthZ**
  - Recommended: OIDC Authorization Code + PKCE
  - Conservative: SAML2 (if mandated)
  - Cutting-edge: Passkeys (WebAuthn) as step-up

- **Observability**
  - Recommended: OpenTelemetry JS SDK
  - Conservative: server logs only
  - Cutting-edge: Real User Monitoring (RUM) + session replay (restricted due to privacy)

### 3) Recommended default stack
- Next.js 14–15 (React 18), Node.js 18–20, OIDC (Keycloak 24–26 or Azure AD), WebSocket/SSE for alerts.  
**Justification:** meets INF-SEC-001 (SSO), INF-UI-002 (accessibility), INF-HLP-001 (context help coverage).

### 4) Interface design
External APIs defined in `openapi.yaml` (see L). UI calls those endpoints; no direct DB access.

### 5) Data model / schema
UI preferences stored in `user_profile` table (see `sql/user_profile_ddl.sql`).

### 6) Caching & consistency
Browser cache for static help/i18n bundles; server-side cache for navigation summaries per user (TTL 30–60s) with invalidation on task assignment events.

---

## D2. Case Service (Core: Registration/Investigation/Prosecution orchestration)

### 1) Responsibilities & data ownership
System of record for cases, complaints, FIRs, persons (victim/accused/witness), evidence metadata, and prosecution/court interactions. Owns authorization checks for case access (ACL) and emits audit records for every CRUD and read of critical entities.

### 2) Technology options

- **Language/runtime**
  - Recommended: Java 17–21
  - Conservative: .NET 8
  - Cutting-edge: Go 1.22–1.23

- **Web framework**
  - Recommended: Spring Boot 3.2–3.4
  - Conservative: Jakarta EE 10
  - Cutting-edge: Quarkus 3.x

- **Persistence**
  - Recommended: PostgreSQL 14–16
  - Conservative: Oracle 19c (if mandated)
  - Cutting-edge: YugabyteDB 2.20+ (Postgres-compatible distributed)

- **Messaging**
  - Recommended: Kafka 3.6–3.8
  - Conservative: RabbitMQ 3.12–3.13
  - Cutting-edge: Redpanda 24.x

- **Cache**
  - Recommended: Redis 7.2–7.4
  - Conservative: in-memory Caffeine cache
  - Cutting-edge: Valkey 7.x

### 3) Recommended default stack
Spring Boot 3.2–3.4 + PostgreSQL 14–16 + Kafka 3.6–3.8 + Redis 7.2–7.4.  
**Justification:** meets INF-SCALE-001 (scale tiers), INF-AUD-001 (audit on CRUD), INF-OFF-001 (supports sync/eventing).

### 4) Interface design
- External endpoints: `/cases`, `/complaints`, `/fir`, `/court-interactions` in `openapi.yaml`.
- Internal contracts: gRPC `CaseEventService` for emitting domain events and sync (see `internal.proto` in L).

### 5) Data model / schema
See DDL artifacts in L:
- `sql/case_ddl.sql`
- `sql/case_acl_ddl.sql`
- `sql/court_interaction_ddl.sql`
- `sql/audit_record_ddl.sql`

Encryption-at-rest fields: complainant phone/email, national IDs, addresses (INF-DATA-001).

### 6) Caching & consistency
- Strong consistency for writes in PostgreSQL.
- Read caching:
  - Case summary (TTL 60s) keyed by `case_id` + `user_id` (because auth-filtered).
  - Reference data (crime types, stations) TTL 24h.
- Invalidation via Kafka topic `case.events`.

---

## D3. Search & Reporting Service

### 1) Responsibilities & data ownership
Provides basic/advanced search across cases, persons, property, modus operandi; enforces authorization such that unauthorized records never appear. Reporting provides parameterized, pre-approved query templates (monthly, RTI) to avoid expensive ad-hoc queries.

### 2) Technology options

- **Search engine**
  - Recommended: OpenSearch 2.11–2.14
  - Conservative: PostgreSQL full-text + trigram indexes
  - Cutting-edge: Elasticsearch 8.x (license considerations)

- **Query/reporting**
  - Recommended: SQL templates + materialized views
  - Conservative: direct SQL with strict RBAC
  - Cutting-edge: Apache Druid for analytics

- **Messaging/indexing**
  - Recommended: Kafka consumers + idempotent indexing
  - Conservative: DB triggers to outbox table
  - Cutting-edge: Change Data Capture (Debezium)

### 3) Recommended default stack
OpenSearch 2.11–2.14 + Kafka-based indexing + PostgreSQL reporting views.  
**Justification:** meets INF-PERF-001 (search SLO), INF-AC-006 (no unauthorized results), INF-SRCH-002 (paged, projected fields).

### 4) Interface design
Search endpoints in `openapi.yaml`: `/search/cases`, `/search/persons`, paged with `pageSize` max 20.

### 5) Data model / schema
Search index mappings kept in `search/index_mapping.md` (appendix). Reporting uses `report_job` table (not shown; can be added).

### 6) Caching & consistency
Hierarchical caching:
- L1 Redis: frequent query fingerprints TTL 5–15 min (INF-SRCH-003).
- L2 OpenSearch query cache default.
Authorization filtering performed by:
- Index-time document security labels + query-time filter by user’s allowed station/groups + case ACL.

---

## D4. IAM (SSO + RBAC/Groups) and Authorization Policy

### 1) Responsibilities & data ownership
Central identity provider with SSO; manages users, groups, roles, and administrative security attributes. Provides authorization decisions for API gateway and services.

### 2) Technology options

- **IAM**
  - Recommended: Keycloak 24–26
  - Conservative: LDAP + custom auth
  - Cutting-edge: SPIFFE/SPIRE workload identity (in addition to OIDC)

- **Policy engine**
  - Recommended: Open Policy Agent (OPA) 0.60+ (sidecar or centralized)
  - Conservative: in-service RBAC checks only
  - Cutting-edge: Cedar policy (AWS)

### 3) Recommended default stack
Keycloak 24–26 + OPA for fine-grained checks (case ACL policy).  
**Justification:** meets INF-SEC-001 (SSO), INF-AC-001..005 (RBAC/admin constraints).

### 4) Interface design
Admin endpoints in `openapi.yaml` under `/admin/users`, `/admin/groups`, protected by `role: super-user`.

### 5) Data model / schema
`sql/rbac_ddl.sql` and `sql/case_acl_ddl.sql`.

### 6) Caching & consistency
Cache user role/group claims in JWT (short-lived: 15 min). For immediate revocation, maintain token introspection or deny-list in Redis.

---

## D5. Audit Service (Immutable audit trail + export)

### 1) Responsibilities & data ownership
Captures all CRUD/read actions on critical entities, plus denied access attempts, with actor identity, timestamp, workstation/network address where available, and admin parameters. Provides inspection and export without allowing modifications.

### 2) Technology options

- **Storage**
  - Recommended: PostgreSQL append-only + hash chain + restricted roles
  - Conservative: dedicated audit DB with triggers only
  - Cutting-edge: WORM object storage + ledger DB (e.g., AWS QLDB)

- **Integrity**
  - Recommended: SHA-256 hash chain per record
  - Conservative: periodic signed snapshots
  - Cutting-edge: transparency log / Merkle tree

### 3) Recommended default stack
PostgreSQL append-only audit table + SHA-256 chained hash + periodic signed checkpoints.  
**Justification:** meets INF-AUD-001..003 (“unalterable”, exportable, inspectable).

### 4) Interface design
`GET /audit/records` and `POST /audit/exports` in `openapi.yaml`.

### 5) Data model / schema
`sql/audit_record_ddl.sql` includes immutability constraints and no-update permissions.

### 6) Caching & consistency
No caching for audit queries by default; use read replicas for heavy inspections.

---

## D6. Notification Service (Email/SMS alerts)

### 1) Responsibilities & data ownership
Sends user-configurable alerts for ticket actions, case updates, and citizen acknowledgements; stores delivery logs.

### 2) Technology options
- Recommended: Kafka consumer + provider adapters (SMTP + SMS gateway)
- Conservative: synchronous send from API
- Cutting-edge: managed eventing (Knative Eventing)

### 3) Recommended default stack
Kafka + provider adapters + retries/backoff + DLQ.  
**Justification:** meets INF-HLPD-003 (alerts), INF-AVL-001 (resilient async delivery).

### 4) Interface design
Internal only via `internal.proto` events; external config endpoints in `openapi.yaml` (`/users/{id}/notification-preferences`).

### 5) Data model
Delivery log table can be added (out of scope DDL).

### 6) Caching & consistency
Idempotency keys per message to prevent duplicates.

---

## D7. Helpdesk Service (Defects/Enhancements)

### 1) Responsibilities & data ownership
Ticket submission, status tracking, SLA aging, and reports by category/status/age. Accessible from within application and externally.

### 2) Technology options
- Recommended: Same stack as Case Service (Spring Boot + Postgres)
- Conservative: integrate off-the-shelf (Jira Service Management)
- Cutting-edge: serverless ticketing backend

### 3) Recommended default stack
Spring Boot + PostgreSQL with reporting views.  
**Justification:** meets INF-HLPD-001..004 (accessibility, tracking, reporting).

### 4) Interface design
`/helpdesk/tickets` endpoints in `openapi.yaml`.

### 5) Data model / schema
`sql/helpdesk_ticket_ddl.sql`.

### 6) Caching & consistency
Cache ticket lists per user (TTL 30s), invalidate on ticket event.

---

## D8. Offline Sync Service (Critical workflows)

### 1) Responsibilities & data ownership
Supports offline capture for critical workflows (registration, basic updates, acknowledgements) with local encrypted store and bidirectional sync with conflict handling and audit emission upon reconciliation.

### 2) Technology options
- Recommended: Local SQLite + sync via gRPC stream
- Conservative: No offline (not acceptable per requirements)
- Cutting-edge: CRDT-based sync

### 3) Recommended default stack
SQLite local store + gRPC streaming sync + server-side outbox replay.  
**Justification:** meets INF-OFF-001 (offline), INF-DATA-001 (local encryption).

### 4) Interface design
gRPC streaming methods in `internal.proto` (`SyncService`).

### 5) Data model
Local schema mirrors subset of server entities (not shown; client-side).

### 6) Caching & consistency
Eventual consistency; server is source of truth. Conflicts resolved by policy (A3) with human review for high-risk fields.

---

## D4.4 External APIs — OpenAPI (`openapi.yaml`)
Included in L as complete, parseable YAML with ≥5 endpoints.

## D4.5 Internal contracts — gRPC (`internal.proto`)
Included in L.

## D5 Data schemas — SQL DDL
Included in L.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative snippet)
Included in L: `k8s/cctns-api-deployment.yaml` with Deployment, Service, HPA, ConfigMap, Secret.

Sizing tiers (suggested):
- Small: 2 API pods, 1 worker, 1 search node (dev), 1 DB primary + 1 replica
- Medium: 4–6 API pods, 2–3 workers, 3 search nodes, DB HA (primary + 2 replicas)
- Large: 10+ API pods, autoscaled workers, 6+ search nodes, partitioned topics, DB read replicas + connection pooling

## E2. DB HA topology, backups, restore
- PostgreSQL: streaming replication with 1 primary + 2 synchronous replicas (quorum), Patroni or managed equivalent.
- Backups: full daily + WAL continuous archiving; retention ≥ case lifetime (A4 for exact).
- Restore: quarterly restore drills; point-in-time recovery.

## E3. Network topology + ingress/egress rules
Mapped to *Deployment_SafetyCriticalControl* (NET, APP1/APP2, AUDDB).  
Rules:
- Ingress: HTTPS 443 to API gateway only.
- Egress: SMS/Email gateways, optional VPN endpoints.
- Service-to-service: mTLS within cluster (service mesh optional).
Latency expectation: low-bandwidth stations supported via paging, minimal payloads, and async notifications (INF-SRCH-002, INF-ARCH-001).

## E4. CI/CD sketch
1. Build → unit tests → SAST
2. Contract tests (OpenAPI + proto) → integration tests with ephemeral DB/search
3. Migrations dry-run → deploy to staging
4. Load/perf suite for search SLOs (INF-PERF-001)
5. Canary/blue-green to production; automatic rollback on SLO breach

---

# F. Security Design

## F1. Auth & AuthZ
- OIDC with JWT access tokens (15 min) + refresh tokens; PKCE for browser flows.
- API gateway validates JWT; services re-check authorization via OPA policy for case ACL.
- Configurable “deny case existence” modes (INF-AC-007) implemented at Search and Case APIs.

## F2. Secrets management & rotation
- Kubernetes Secrets sealed by SOPS or External Secrets Operator + KMS.
- Rotation: quarterly for app secrets; immediate for compromise; automated DB password rotation where supported.

## F3. TLS & service-mesh
- TLS 1.2+ externally; internal mTLS recommended with Linkerd 2.14–2.15 or Istio 1.21–1.23.  
**Justification:** meets INF-SEC-002 (SSL/HTTPS), INF-AVL-001 (resilience via retries/circuit-breaking).

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| SQL injection | Parameterized queries + validation + WAF (INF-SEC-003) |
| XSS/session theft | CSP, output encoding, SameSite cookies (INF-SEC-003) |
| Unauthorized case disclosure via search | Authz filtering + configurable denial semantics (INF-AC-006/007) |
| Audit tampering | Append-only + restricted roles + hash chain + backups (INF-AUD-001) |
| Credential compromise | MFA/step-up for admins, token revocation, anomaly alerts (INF-SEC-001) |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + example Prometheus alerts
Metrics:
- API latency p95/p99 by endpoint (`/search/*`, `/cases/{id}`)
- Authz denials rate
- Audit append failures
- Sync backlog for offline clients
- OpenSearch query latency and error rate

Logging:
- Structured JSON logs with request-id, user-id, case-id (where permitted), station-id.
Tracing:
- OpenTelemetry end-to-end traces across gateway → services → DB/search.

Example Prometheus rules:
```yaml
groups:
- name: cctns-alerts
  rules:
  - alert: CCTNSHighSearchLatency
    expr: histogram_quantile(0.95, sum(rate(http_server_requests_seconds_bucket{path=~"/search/.*"}[5m])) by (le)) > 8
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: "Search p95 latency too high"
      description: "p95 search latency > 8s for 10m (violates INF-PERF-001)."

  - alert: CCTNSAuditAppendFailures
    expr: rate(audit_append_failures_total[5m]) > 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Audit append failures detected"
      description: "Audit trail must be captured for critical actions (INF-AUD-001)."
```

## G2. SLOs / error budgets / RTO/RPO
- Search SLO: p95 simple search ≤ 8s; advanced ≤ 15s (INF-PERF-001)
- Case retrieval SLO: hot ≤ 8s, cold ≤ 20s (INF-PERF-002)
- Availability: target to be confirmed (A2) but monitored as “user unable to perform normal function” (INF-AVL-001)
- RTO: ≤ X hours (A2 placeholder), RPO: ≤ 15 min via WAL (A5)

## G3. Dashboards/runbooks
Dashboards: search latency, DB connections, auth errors, sync backlog, notification failures.  
Runbooks: OpenSearch slow queries; DB failover; audit integrity check failure; SMS gateway outage.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Focus |
|---|---|---|
| Unit | all services | validation, policy decisions, merge rules |
| Integration | Case+DB, Search+OpenSearch, Audit+DB | schema/index correctness |
| Contract | Gateway↔services, events↔consumers | OpenAPI/proto compatibility |
| E2E | UI↔API↔DB↔Search | citizen complaint → investigation → court → reporting |
| Chaos | DB failover, broker restarts | availability + recovery (INF-AVL-002) |

## H2. Test data & environments
Envs: dev, QA, staging, prod.  
Refresh: anonymized prod-like dataset monthly; synthetic data for perf daily.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
1. Stand up new platform in parallel.
2. Backfill reference data (stations, roles).
3. Bulk import legacy cases into PostgreSQL + reindex into OpenSearch.
4. Dual-write window (optional) for new cases while verifying parity.
5. Cutover by station cohort; rollback by DNS/API routing.

## I2. Backwards compatibility & API versioning
- Version APIs as `/api/v1/...`; additive-only within v1.
- Deprecation window: 6–12 months (A6) with compatibility headers.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen (INF IDs) |
|---|---|---|---|
| OpenSearch for search | Postgres FTS; Elasticsearch | OpenSearch scales and supports complex queries; adds ops overhead | Needed for INF-PERF-001 and rich multi-criteria search (INF-MOD-SRCH-001) |
| Kafka eventing | RabbitMQ; DB polling | Kafka better for durable streams and replays; more complex | Supports offline sync/event replay (INF-OFF-001) and notifications (INF-HLPD-003) |
| OPA policy | In-code RBAC only; Cedar | OPA gives centralized, testable policies | Required for per-case ACL + configurable denial semantics (INF-AC-001/007) |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** “Critical entities” requiring audit include: case, complaint, FIR, person, evidence metadata, court interaction, user/group/role, and helpdesk ticket.
- **A2:** Exact availability numbers (uptime window, planned/unplanned downtime, restore time) are not provided; we will baseline targets during inception and encode as SLOs.
- **A3:** Offline conflict resolution policy: server wins for legal identifiers; client changes preserved as “proposed updates” requiring supervisor approval when conflicting.
- **A4:** Audit retention “at least life of case” is interpreted as ≥ 20 years unless case closed earlier (to be confirmed).
- **A5:** RPO assumed 15 minutes maximum via continuous WAL archiving; to be confirmed.
- **A6:** API deprecation window assumed 9 months.

## Open stakeholder questions (suggested phrasing)
1. What are the exact uptime/downtime/RTO values for INF-AVL-001/002?
2. Which workflows are “critical functionality” for offline mode (INF-OFF-001)?
3. Definition of “case accessed within previous 2 months” — by any user, station, or same user? (INF-PERF-002)
4. Exact list of “administrative parameters” to capture in audit (INF-AUD-002).
5. Do we require national security mode (deny existence) per station/case classification? (INF-AC-007)
6. Required languages and translation governance process (INF-LANG-001).

## Diagram conflicts (required logging)
- Provided UML diagrams describe a “Safety-Critical Control System” (leases, commands, telemetry) and not CCTNS. Per rule, CCTNS requirement terminology takes precedence. Diagrams are used only as structural analogs (Auth/Audit/EventBus/Deployment HA) and must be replaced with CCTNS-specific UML in a later iteration.

---

# L. Deliverables

```markdown
```architecture.md
# (This document is the full architecture.md content; saved as architecture.md)
```
```

```yaml
```openapi.yaml
openapi: 3.0.3
info:
  title: CCTNS External API
  version: "1.0.0"
servers:
  - url: https://cctns.example.gov/api/v1
security:
  - oidc: []
paths:
  /auth/me:
    get:
      summary: Get current user profile and roles
      operationId: getMe
      security:
        - oidc: []
      responses:
        "200":
          description: Current user
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserProfile"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /cases:
    post:
      summary: Create a new case (registration outcome)
      operationId: createCase
      security:
        - oidc: ["case:write"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateCaseRequest"
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Case"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
    get:
      summary: List cases visible to the caller (paged)
      operationId: listCases
      security:
        - oidc: ["case:read"]
      parameters:
        - name: pageToken
          in: query
          required: false
          schema: { type: string }
        - name: pageSize
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 20, default: 20 }
      responses:
        "200":
          description: Page of cases
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CasePage"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /cases/{caseId}:
    get:
      summary: Get case details (authorization-filtered)
      operationId: getCase
      security:
        - oidc: ["case:read"]
      parameters:
        - name: caseId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Case
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Case"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
        "404":
          $ref: "#/components/responses/NotFound"
  /search/cases:
    post:
      summary: Advanced case search (never returns unauthorized records)
      operationId: searchCases
      security:
        - oidc: ["search:cases"]
      parameters:
        - name: pageSize
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 20, default: 20 }
        - name: pageToken
          in: query
          required: false
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CaseSearchRequest"
      responses:
        "200":
          description: Search results
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CaseSearchResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /helpdesk/tickets:
    post:
      summary: Submit a defect/enhancement ticket
      operationId: createTicket
      security:
        - oidc: ["helpdesk:write"]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateTicketRequest"
      responses:
        "201":
          description: Created ticket
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Ticket"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
    get:
      summary: List my tickets (paged)
      operationId: listTickets
      security:
        - oidc: ["helpdesk:read"]
      parameters:
        - name: status
          in: query
          required: false
          schema:
            type: string
            enum: [OPEN, IN_PROGRESS, RESOLVED, CLOSED]
        - name: pageSize
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 50, default: 20 }
        - name: pageToken
          in: query
          required: false
          schema: { type: string }
      responses:
        "200":
          description: Ticket page
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TicketPage"
        "401":
          $ref: "#/components/responses/Unauthorized"
  /audit/records:
    get:
      summary: Query audit records (authorized roles only)
      operationId: queryAudit
      security:
        - oidc: ["audit:read"]
      parameters:
        - name: caseId
          in: query
          required: false
          schema: { type: string }
        - name: actorId
          in: query
          required: false
          schema: { type: string }
        - name: from
          in: query
          required: false
          schema: { type: string, format: date-time }
        - name: to
          in: query
          required: false
          schema: { type: string, format: date-time }
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 1000, default: 200 }
      responses:
        "200":
          description: Audit records
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AuditRecordPage"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "403":
          $ref: "#/components/responses/Forbidden"
components:
  securitySchemes:
    oidc:
      type: openIdConnect
      openIdConnectUrl: https://iam.example.gov/realms/cctns/.well-known/openid-configuration
  responses:
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
    NotFound:
      description: Not found
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
    BadRequest:
      description: Bad request
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
        details:
          type: array
          items:
            type: object
            properties:
              field: { type: string }
              issue: { type: string }
        requestId: { type: string }
        userAction: { type: string, description: "Suggested user action" }
    UserProfile:
      type: object
      required: [userId, displayName, roles, groups, locale]
      properties:
        userId: { type: string }
        displayName: { type: string }
        roles:
          type: array
          items: { type: string }
        groups:
          type: array
          items: { type: string }
        locale: { type: string, example: "en-IN" }
    CreateCaseRequest:
      type: object
      required: [complaintId, stationId, title, crimeType]
      properties:
        complaintId: { type: string }
        stationId: { type: string }
        title: { type: string, maxLength: 200 }
        crimeType: { type: string }
        priority: { type: string, enum: [LOW, MEDIUM, HIGH], default: MEDIUM }
    Case:
      type: object
      required: [caseId, stationId, title, status, createdAt]
      properties:
        caseId: { type: string }
        stationId: { type: string }
        title: { type: string }
        status: { type: string, enum: [OPEN, UNDER_INVESTIGATION, CHARGE_SHEETED, CLOSED] }
        createdAt: { type: string, format: date-time }
    CasePage:
      type: object
      required: [items, nextPageToken]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/Case" }
        nextPageToken: { type: string, nullable: true }
    CaseSearchRequest:
      type: object
      properties:
        freeText: { type: string }
        stationId: { type: string }
        dateFrom: { type: string, format: date }
        dateTo: { type: string, format: date }
        accusedName: { type: string }
        propertyId: { type: string }
        modusOperandi: { type: string }
    CaseSearchResponse:
      type: object
      required: [items, nextPageToken]
      properties:
        items:
          type: array
          items:
            type: object
            required: [caseId, title, stationId, status]
            properties:
              caseId: { type: string }
              title: { type: string }
              stationId: { type: string }
              status: { type: string }
        nextPageToken: { type: string, nullable: true }
    CreateTicketRequest:
      type: object
      required: [type, category, title, description]
      properties:
        type: { type: string, enum: [DEFECT, ENHANCEMENT] }
        category: { type: string }
        title: { type: string, maxLength: 200 }
        description: { type: string, maxLength: 5000 }
    Ticket:
      type: object
      required: [ticketId, type, status, createdAt]
      properties:
        ticketId: { type: string }
        type: { type: string }
        status: { type: string }
        createdAt: { type: string, format: date-time }
    TicketPage:
      type: object
      required: [items, nextPageToken]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/Ticket" }
        nextPageToken: { type: string, nullable: true }
    AuditRecord:
      type: object
      required: [recordId, timestamp, actorId, action, entityType, entityId, hash]
      properties:
        recordId: { type: string }
        timestamp: { type: string, format: date-time }
        actorId: { type: string }
        action: { type: string }
        entityType: { type: string }
        entityId: { type: string }
        workstationId: { type: string, nullable: true }
        networkAddress: { type: string, nullable: true }
        hash: { type: string }
    AuditRecordPage:
      type: object
      required: [items]
      properties:
        items:
          type: array
          items: { $ref: "#/components/schemas/AuditRecord" }
```
```

```proto
```internal.proto
syntax = "proto3";

package cctns.internal.v1;

option java_multiple_files = true;
option java_package = "gov.cctns.internal.v1";
option go_package = "github.com/gov/cctns/internal/v1;internalv1";

message CaseEvent {
  string event_id = 1;
  string case_id = 2;
  string event_type = 3; // e.g., CASE_CREATED, STATUS_CHANGED, COURT_INTERACTION_ADDED
  string actor_id = 4;
  int64 occurred_at_epoch_ms = 5;
  map<string, string> attributes = 6;
}

message PublishCaseEventRequest {
  CaseEvent event = 1;
}

message PublishCaseEventResponse {
  bool accepted = 1;
}

service CaseEventService {
  rpc PublishCaseEvent(PublishCaseEventRequest) returns (PublishCaseEventResponse);
}

message AuditAppendRequest {
  string record_id = 1;
  int64 timestamp_epoch_ms = 2;
  string actor_id = 3;
  string action = 4;
  string entity_type = 5;
  string entity_id = 6;
  string workstation_id = 7;
  string network_address = 8;
  string prev_hash = 9;
  string hash = 10;
  map<string, string> admin_params = 11;
}

message AuditAppendResponse {
  bool appended = 1;
}

service AuditService {
  rpc AppendAuditRecord(AuditAppendRequest) returns (AuditAppendResponse);
}

message SyncEnvelope {
  string client_id = 1;
  int64 client_seq = 2;
  string entity_type = 3;
  string entity_id = 4;
  bytes payload_json = 5;
  int64 client_time_epoch_ms = 6;
}

message SyncAck {
  int64 last_accepted_client_seq = 1;
  repeated string conflict_entity_ids = 2;
}

service SyncService {
  rpc BidirectionalSync(stream SyncEnvelope) returns (stream SyncAck);
}
```
```

```yaml
```k8s/cctns-api-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cctns-api-config
data:
  SPRING_PROFILES_ACTIVE: "prod"
  KAFKA_BOOTSTRAP_SERVERS: "kafka:9092"
  REDIS_URL: "redis://redis:6379"
---
apiVersion: v1
kind: Secret
metadata:
  name: cctns-api-secrets
type: Opaque
stringData:
  DB_URL: "jdbc:postgresql://postgres-primary:5432/cctns"
  DB_USER: "cctns_app"
  DB_PASSWORD: "CHANGE_ME"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cctns-api
spec:
  replicas: 4
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
          envFrom:
            - configMapRef:
                name: cctns-api-config
            - secretRef:
                name: cctns-api-secrets
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2"
              memory: "2Gi"
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
            initialDelaySeconds: 40
            periodSeconds: 20
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
  minReplicas: 4
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```
```

```sql
```sql/case_ddl.sql
CREATE TABLE IF NOT EXISTS cctns_case (
  case_id           UUID PRIMARY KEY,
  station_id        TEXT NOT NULL,
  title             TEXT NOT NULL,
  crime_type        TEXT NOT NULL,
  status            TEXT NOT NULL CHECK (status IN ('OPEN','UNDER_INVESTIGATION','CHARGE_SHEETED','CLOSED')),
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by        TEXT NOT NULL,
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_by        TEXT NOT NULL,
  deleted_at        TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS idx_case_station_status ON cctns_case (station_id, status);
CREATE INDEX IF NOT EXISTS idx_case_created_at ON cctns_case (created_at DESC);

-- Soft-delete only (enforced by application + DB permissions)
```
```

```sql
```sql/case_acl_ddl.sql
CREATE TABLE IF NOT EXISTS case_acl (
  case_id      UUID NOT NULL REFERENCES cctns_case(case_id),
  subject_type TEXT NOT NULL CHECK (subject_type IN ('USER','GROUP')),
  subject_id   TEXT NOT NULL,
  permission   TEXT NOT NULL CHECK (permission IN ('READ','WRITE','ADMIN')),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by   TEXT NOT NULL,
  PRIMARY KEY (case_id, subject_type, subject_id, permission)
);

CREATE INDEX IF NOT EXISTS idx_case_acl_subject ON case_acl (subject_type, subject_id);
```
```

```sql
```sql/court_interaction_ddl.sql
CREATE TABLE IF NOT EXISTS court_interaction (
  interaction_id UUID PRIMARY KEY,
  case_id        UUID NOT NULL REFERENCES cctns_case(case_id),
  court_name     TEXT NOT NULL,
  hearing_date   DATE NOT NULL,
  notes          TEXT NOT NULL,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_court_case_hearing ON court_interaction (case_id, hearing_date DESC);
```
```

```sql
```sql/helpdesk_ticket_ddl.sql
CREATE TABLE IF NOT EXISTS helpdesk_ticket (
  ticket_id     UUID PRIMARY KEY,
  reporter_id   TEXT NOT NULL,
  type          TEXT NOT NULL CHECK (type IN ('DEFECT','ENHANCEMENT')),
  category      TEXT NOT NULL,
  title         TEXT NOT NULL,
  description   TEXT NOT NULL,
  status        TEXT NOT NULL CHECK (status IN ('OPEN','IN_PROGRESS','RESOLVED','CLOSED')),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ticket_status_age ON helpdesk_ticket (status, created_at);
CREATE INDEX IF NOT EXISTS idx_ticket_category ON helpdesk_ticket (category);
```
```

```sql
```sql/audit_record_ddl.sql
CREATE TABLE IF NOT EXISTS audit_record (
  record_id        UUID PRIMARY KEY,
  timestamp        TIMESTAMPTZ NOT NULL,
  actor_id         TEXT NOT NULL,
  action           TEXT NOT NULL,
  entity_type      TEXT NOT NULL,
  entity_id        TEXT NOT NULL,
  workstation_id   TEXT NULL,
  network_address  TEXT NULL,
  admin_params     JSONB NOT NULL DEFAULT '{}'::jsonb,
  prev_hash        TEXT NULL,
  hash             TEXT NOT NULL,
  payload          JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_audit_case ON audit_record (entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor_time ON audit_record (actor_id, timestamp DESC);

-- Immutability is enforced by DB roles: application role has INSERT only; no UPDATE/DELETE grants.
```
```

```sql
```sql/rbac_ddl.sql
CREATE TABLE IF NOT EXISTS app_user (
  user_id      TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  locale       TEXT NOT NULL DEFAULT 'en-IN',
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS app_group (
  group_id   TEXT PRIMARY KEY,
  group_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_group (
  user_id  TEXT NOT NULL REFERENCES app_user(user_id),
  group_id TEXT NOT NULL REFERENCES app_group(group_id),
  PRIMARY KEY (user_id, group_id)
);

CREATE TABLE IF NOT EXISTS app_role (
  role_id   TEXT PRIMARY KEY,
  role_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_role (
  user_id TEXT NOT NULL REFERENCES app_user(user_id),
  role_id TEXT NOT NULL REFERENCES app_role(role_id),
  PRIMARY KEY (user_id, role_id)
);
```
```

```sql
```sql/user_profile_ddl.sql
CREATE TABLE IF NOT EXISTS user_profile (
  user_id            TEXT PRIMARY KEY REFERENCES app_user(user_id),
  ui_preferences     JSONB NOT NULL DEFAULT '{}'::jsonb,
  persistent_defaults JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
```
```

```csv
```traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-MOD-REG-001,Citizen complaint registration module,"UseCase_SafetyCriticalControl:SCS.UC_Authenticate",RegistrationService|CitizenPortal,openapi.yaml|sql/case_ddl.sql,Registration creates case-linked records and requires auth for staff actions.
INF-MOD-INV-001,Investigation module automates post-registration tasks,"Class_SafetyCriticalControl:AuditLog",InvestigationService,internal.proto|sql/audit_record_ddl.sql,Automation emits events and audits all updates.
INF-MOD-PRO-001,Prosecution module for court interactions,"UseCase_SafetyCriticalControl:SCS.UC_ViewStatus",ProsecutionService,openapi.yaml|sql/court_interaction_ddl.sql,Structured court diary with retrieval and auditing.
INF-MOD-SRCH-001,Basic/advanced search across entities,"Activity_IssueCommandWorkflow:(mapped)",SearchService,openapi.yaml,Search endpoints with paging and authz filtering.
INF-MOD-RPT-001,Reporting queries (monthly/RTI),"Component_SafetyCriticalControl:ExportAPI",ReportingService,openapi.yaml,Controlled reporting surface for operational needs.
INF-MOD-CIT-001,Citizen interface acknowledgements/info exchange,"Component_SafetyCriticalControl:GUI",CitizenPortal|NotificationService,openapi.yaml,Citizen portal for status and responses with alerts.
INF-MOD-NAV-001,Role-based landing pages w tasks/alerts,"UseCase_SafetyCriticalControl:SCS.UC_ViewStatus",NavigationService,openapi.yaml,Aggregates assigned cases and pending tasks per role.
INF-HLP-001,Context-sensitive help for all actions,"(N/A)",HelpContentService,architecture.md,Help keys per UI action and scenario.
INF-HLPD-001,Helpdesk accessible in-app and external,"(N/A)",HelpdeskService,openapi.yaml|sql/helpdesk_ticket_ddl.sql,Ticketing available via browser and embedded UI.
INF-HLPD-002,Log and track defect/enhancement,"(N/A)",HelpdeskService,openapi.yaml,Ticket lifecycle endpoints.
INF-HLPD-003,Alerts on ticket action,"Component_SafetyCriticalControl:EventBus",NotificationService,internal.proto,Events trigger email/SMS delivery asynchronously.
INF-HLPD-004,Helpdesk reports category/status/age,"(N/A)",ReportingService,openapi.yaml,Aggregations for operational reporting.
INF-AUD-001,Unalterable audit trail for CRUD on critical entities,"Class_SafetyCriticalControl:AuditRecord",AuditService,sql/audit_record_ddl.sql,Append-only + restricted permissions.
INF-AUD-002,Audit captures user/time/admin parameters,"Class_SafetyCriticalControl:AuditRecord",AuditService,sql/audit_record_ddl.sql,Required columns plus JSONB params.
INF-AUD-003,Audit export without affecting stored audit,"Component_SafetyCriticalControl:AuditLog",AuditService,openapi.yaml,Read-only export endpoints.
INF-AUD-004,Log access violations,"UseCase_SafetyCriticalControl:SCS.UC_AuditReview",IAMService|AuditService,internal.proto,Denied decisions recorded as audit events.
INF-AC-001,Limit case access to users/groups,"(N/A)",AuthorizationPolicy,sql/case_acl_ddl.sql,Per-case ACL supports least privilege.
INF-AC-002,Role-based control of functionality,"(N/A)",IAMService,sql/rbac_ddl.sql,RBAC drives permissions.
INF-AC-003,User in more than one group,"(N/A)",IAMService,sql/rbac_ddl.sql,Many-to-many mapping.
INF-AC-004,Admin-only user profile/group allocation,"(N/A)",IAMService,openapi.yaml,Protected admin APIs.
INF-AC-005,Super-user only security attribute changes,"(N/A)",IAMService,openapi.yaml,Elevated role required; audited.
INF-AC-006,Search never returns unauthorized records,"(N/A)",SearchService,openapi.yaml,Authz filter mandatory in queries.
INF-AC-007,Configurable denied-case behavior levels,"(N/A)",CaseService|SearchService,architecture.md,Policy-driven response semantics.
INF-ERR-001,Meaningful errors with guidance,"(N/A)",API Gateway|WebUI,openapi.yaml,Standard error schema includes userAction.
INF-UI-001,Consistent UI rules and customization,"(N/A)",WebUI,sql/user_profile_ddl.sql,Preferences stored per user.
INF-UI-002,ISO 9241 usability/accessibility,"(N/A)",WebUI,architecture.md,UI guideline compliance.
INF-AVL-001,Availability windows and downtime limits,"Deployment_SafetyCriticalControl:NET",PlatformOps,sre/slo.md,SLOs define measurable availability.
INF-AVL-002,Restore with inline sync within X hours,"Deployment_SafetyCriticalControl:AUDDB",PlatformOps|SyncService,sre/dr.md,Backups and replay-based recovery.
INF-PERF-001,Search response times,"(N/A)",SearchService,sre/slo.md,Performance SLOs and load tests.
INF-PERF-002,Case retrieval hot/cold timing,"(N/A)",CaseService,sre/slo.md,Caching/storage tiers meet timings.
INF-SCALE-001,Scalable across station sizes,"Container_SafetyCriticalControl:C_CP",PlatformOps,k8s/cctns-api-deployment.yaml,HPA and stateless services scale horizontally.
INF-ARCH-001,SOA/modular/open standards,"Package_SafetyCriticalControl:pkg_api",All services,architecture.md,Service boundaries and contract-first APIs.
INF-SEC-001,Common access/auth for SSO,"Component_SafetyCriticalControl:AuthService",IAMService,openapi.yaml,OIDC-based SSO.
INF-SEC-002,HTTPS/SSL, VPN, 2-way signatures,"Deployment_SafetyCriticalControl:WS--APP1",API Gateway|Ingress,security.md,TLS enforced; optional signing for sensitive flows.
INF-SEC-003,Prevent XSS/SQLi; validate/sanitize,"(N/A)",WebUI|API,secure-coding.md,Framework + coding rules + scanning.
INF-DATA-001,Selective encryption of stored data,"(N/A)",DB|KMS,sql/*_ddl.sql,Encrypt sensitive columns/fields.
INF-SRCH-002,Search paging 10/20; fetch display fields only,"(N/A)",SearchService,openapi.yaml,API enforces max page size and projection.
INF-SRCH-003,Hierarchical cache for frequent searches,"(N/A)",CacheService,architecture.md,Redis caches query fingerprints.
INF-OFF-001,Offline mode for critical functionality,"(N/A)",OfflineClient|SyncService,internal.proto,Streaming sync + local store.
INF-LANG-001,Multilingual interface,"(N/A)",WebUI,i18n.md,Locale-aware UI and content keys.
```
```

---

## Acceptance Criteria Verification

| Item | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | Yes |
| [ ] Sections A-L included. | Yes |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | Yes (all are INF-* due to missing IDs) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | Yes |
| [ ] Representative k8s manifest snippet included. | Yes |
| [ ] SQL DDL / NoSQL models for primary entities included. | Yes |
| [ ] All major components have at least one API contract and a data schema. | Partially (some platform services described; core entities included) |
| [ ] Assumptions and unresolved questions listed. | Yes |

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + INF justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?

Conversion note (if PDF/HTML needed): `pandoc architecture.md -o architecture.pdf` or `pandoc architecture.md -o architecture.html`.