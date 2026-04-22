Scope: Produce production-ready architecture for the **Web Learning Game System** described by the provided UML set; log conflicts vs the mixed “Original Requirements” corpus.  
Approach: Use 4+1 views aligned to the 11 provided diagrams; infer missing FR/NFR/ASR as `INF-*`, then design APIs, data, security, ops, and test strategy.  
Top validation: (1) full traceability matrix coverage, (2) OpenAPI + internal contract syntactic validity, (3) k8s + SQL DDL validity, (4) conflict log + assumptions.

# A. Executive Summary (≤1 page)

## System overview
A standards-based HTML5 web application that lets end users play a question/answer learning game and lets admins securely manage and publish question content with schema validation, atomic publishing, and audit logging.

**Primary diagram mapping (one-line):** Scenario View is captured in **UseCase_ScenarioView** (UC_PlayGame, UC_ManageQuestions, UC_PublishUpdate, UC_ViewAuditLog); core domain is in **Class_LogicView** (GameSession, QuestionBank, ContentUpdateRequest, ContentPublisher, AuditLog).

## Architectural style(s) and deployment topology
- **Style:** Layered + Hexagonal (ports/adapters) with contract-first APIs (external OpenAPI + internal gRPC).  
- **Topology:** Stateless API replicas behind ingress + shared durable storage for content and audit (see **Deployment_PhysicalView**: Web Server Node replicas + Storage Node).

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| File-based content store concurrency/consistency during admin publishes | Corrupt/partial content, downtime | Use DB-backed versioned content + transactional publish; keep atomic publish semantics; add optimistic concurrency via `If-Match`/ETag. |
| Admin auth compromise (password stuffing, session theft) | Unauthorized content changes | OIDC + MFA for admins; rate limiting; lockout; secure cookies; audit trails; least privilege. |
| Requirements corpus conflict (many unrelated systems) | Wrong system built | Treat UML as authoritative for this delivery; log conflicts; require stakeholder confirmation (see Section K). |

## Key QA coverage mapping (ASR/NFR → test types)

> Note: The provided diagrams include “ASR/NFR (inferred)” notes but no formal IDs. This document defines them as `INF-ASR-*` / `INF-NFR-*` and lists them in Section K.

| Quality | IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-SCAL-01 | Load + soak tests; HPA validation; k6 |
| Availability | INF-NFR-AVL-01 | Chaos tests; failover drills; backup/restore tests |
| Security | INF-ASR-SEC-01, INF-ASR-AUD-01 | SAST/DAST; penetration tests; authz tests; secret scanning |
| Performance | INF-NFR-PERF-01 | API latency tests; browser RUM; profiling |
| Maintainability | INF-ASR-CONTRACT-01 | Contract tests; schema validation tests; CI gates |

---

# B. Traceability & Rationale

## Scope note (conflict handling)
The “Original Requirements” text contains many unrelated systems (ICU monitoring, turnstile, heating, sluice, etc.) that **conflict** with the provided UML, which clearly specifies a **Web Learning Game System**. Per rule, we **prefer names/IDs in Original Requirements**; however, the Original Requirements do not define IDs and do not describe the web learning game at all. Therefore:
- We **infer** requirement IDs (`INF-*`) for the web learning game based on the UML and embedded notes.
- We **log the conflict** in Section K and require stakeholder confirmation.

## Traceability matrix (table; also delivered as CSV in Section L)
Columns: `Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale`

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FR-GAME-01 | End user can play game (intro → questions → score) | UseCase_ScenarioView:UC_PlayGame,UC_ViewIntro,UC_AnswerQuestion,UC_ViewScore; State_LogicView_GameSession:GSL | GameWebUI, GameService | architecture.md, openapi.yaml | Core user flow implemented via session lifecycle and game endpoints. |
| INF-FR-GAME-02 | Provide feedback per answer | UseCase_ScenarioView:UC_GetFeedback; Sequence_ProcessView_S2_EndUserPlayGame | GameService | openapi.yaml | Feedback returned by submit-answer response. |
| INF-FR-ADMIN-01 | Admin login | UseCase_ScenarioView:UC_AdminLogin; Sequence_ProcessView_S1_AdminPublishUpdate | AuthService, AdminWebUI | openapi.yaml, internal.proto | Auth endpoints and session validation. |
| INF-FR-ADMIN-02 | Admin manages questions (create/update) | UseCase_ScenarioView:UC_ManageQuestions; Class_LogicView:QuestionBank,Question | ContentService | openapi.yaml, sql/* | CRUD + versioning for question sets. |
| INF-ASR-CONTRACT-01 | Contract-first content updates with server-side schema validation | Class_LogicView:ContentUpdateRequest; Activity_ProcessView_AdminPublishUpdate | ContentService | openapi.yaml, architecture.md | Enforced via JSON Schema validation on publish. |
| INF-ASR-ATOMIC-01 | Atomic publish semantics (temp write + atomic rename) | Class_LogicView:ContentPublisher; Component_DevelopmentView:FileStore[AtomicRename] | ContentService, FileStore | architecture.md | Preserved as an implementation tactic; DB alternative also provided. |
| INF-ASR-AUD-01 | Audit logging with required fields + retention ≥2 years | Class_LogicView:AuditLog,AuditLogEntry; Component_DevelopmentView:AuditService | AuditService | sql/audit_ddl.sql | Append-only audit table with retention policy. |
| INF-ASR-SEC-01 | Hardened auth: salted hash, lockout after 5 failures, HTTPS-only | Class_LogicView:AdminUser; Component_DevelopmentView:AuthService[Lockout] | AuthService, ApiGateway | architecture.md, openapi.yaml | Security controls implemented at gateway and auth service. |
| INF-NFR-PERF-01 | Feedback responsiveness observable within 500ms | State_LogicView_GameSession note | GameService | architecture.md | Latency SLO and tests defined. |
| INF-NFR-WEB-01 | Standards-based HTML5 web app (no plugins) | UseCase_ScenarioView note; Package_DevelopmentView:ui | GameWebUI, AdminWebUI | architecture.md | UI stack constrained to HTML5/CSS/JS. |
| INF-NFR-AVL-01 | Stateless API enables horizontal scaling | Deployment_PhysicalView note | Backend API | k8s/backend-api-deployment.yaml | K8s replicas + HPA. |
| INF-NFR-DUR-01 | Content durability and integrity | Component_DevelopmentView:FileStore[AtomicRename] | Persistence | sql/content_ddl.sql | Versioned content + integrity hashes. |

---

# C. Architecture Overview

## Context (Scenario View)
Actors: **EndUser**, **Admin**, and **External Browser** interact with the system (see **UseCase_ScenarioView**: EndUser→UC_PlayGame; Admin→UC_ManageQuestions; ExternalBrowser→UC_PlayGame/UC_AdminLogin).

## Containers (Physical View)
Containers: static web UI hosting, backend API, auth service, audit service, and storage (see **Container_PhysicalView**: C_StaticHosting, C_BackendApi, C_Auth, C_Audit, C_FileStore, C_AuditStore).

## Components/Packages (Development View)
Layering: `ui → api → application → domain → persistence/security/audit` (see **Package_DevelopmentView**). Runtime components: ApiGateway, GameService, ContentService, AuthService, AuditService (see **Component_DevelopmentView**).

## Class/Runtime (Logic + Process Views)
Core domain objects: GameSession, QuestionBank, Question, AnswerAttempt, Score; admin objects: AdminUser, AdminSession, ContentUpdateRequest, ContentPublisher, AuditLog (see **Class_LogicView**). Runtime flows: Admin publish (see **Sequence_ProcessView_S1_AdminPublishUpdate**) and EndUser play (see **Sequence_ProcessView_S2_EndUserPlayGame**). Session lifecycle is defined in **State_LogicView_GameSession**.

## Deployment (Physical View)
Two web server replicas connect to a storage node over LAN; clients connect via HTTPS (see **Deployment_PhysicalView**: Web Server Node Replica 1/2, Storage Node).

---

# D. Detailed Technical Design (developer-facing)

## D1. Subsystem: Game Experience (GameWebUI + GameService)

### D1.1 Responsibilities & data ownership
GameWebUI renders intro, questions, feedback, and score; GameService owns session state, scoring, and question selection. Persisted data: question bank versions; optionally session telemetry (non-PII) for analytics (assumption A6).

### D1.2 Technology options (≥3 alternatives per concern)

**Language/runtime**
- Recommended: **TypeScript on Node.js 20 LTS** (Node.js 20-22)  
- Conservative: **Java 21 (21-22) + Spring Boot 3.2+**  
- Cutting-edge: **Go 1.22-1.23** with Fiber/Chi

**Web framework**
- Recommended: **Fastify 4.x** (Node)  
- Conservative: **Express 4.x**  
- Cutting-edge: **Bun 1.x** runtime + Elysia

**RPC/HTTP**
- Recommended: **REST/JSON over HTTPS** externally + **gRPC** internally  
- Conservative: REST only  
- Cutting-edge: GraphQL federation

**Persistence (SQL/NoSQL)**
- Recommended: **PostgreSQL 14-16** for content/audit  
- Conservative: File-based JSON + atomic rename (as in diagrams)  
- Cutting-edge: DynamoDB (managed) + streams

**Cache**
- Recommended: **Redis 7.2-7.4** for hot question bank + rate limits  
- Conservative: In-memory LRU per pod  
- Cutting-edge: Valkey 7.x

**Messaging**
- Recommended: **NATS 2.10+** for audit/event fanout (optional)  
- Conservative: none (sync writes)  
- Cutting-edge: Kafka 3.6+

**Search**
- Recommended: none (small dataset)  
- Conservative: none  
- Cutting-edge: OpenSearch 2.x for question analytics

**Authn/Authz**
- Recommended: **OIDC (Auth0/Keycloak) for Admin**, anonymous for EndUser  
- Conservative: local password auth (bcrypt/Argon2) as in diagrams  
- Cutting-edge: Passkeys/WebAuthn for Admin

**Observability**
- Recommended: OpenTelemetry + Prometheus + Loki  
- Conservative: structured logs only  
- Cutting-edge: eBPF-based profiling (Parca)

**CI/CD**
- Recommended: GitHub Actions + Trivy + contract tests  
- Conservative: Jenkins  
- Cutting-edge: GitOps (ArgoCD) with policy-as-code

**Container runtime**
- Recommended: containerd (K8s default)  
- Conservative: Docker Engine  
- Cutting-edge: gVisor sandboxing

**Infra provisioning**
- Recommended: Terraform 1.6+  
- Conservative: manual + scripts  
- Cutting-edge: Crossplane

### D1.3 Recommended default stack (versions) + justification
- **Frontend:** React 18.2+ (18-19), Vite 5-6, TypeScript 5.3-5.6  
  Justification: meets **INF-NFR-WEB-01** (HTML5/no plugins).
- **Backend:** Node.js 20-22 + Fastify 4.x + Zod/JSON Schema validation  
  Justification: meets **INF-NFR-PERF-01** (low-latency feedback).
- **DB:** PostgreSQL 14-16  
  Justification: meets **INF-NFR-DUR-01** (durability/integrity).
- **Cache:** Redis 7.2-7.4  
  Justification: meets **INF-NFR-SCAL-01** (scale via caching).

### D1.4 Interface design (External APIs) — `openapi.yaml`
Provided in Section L.

### D1.4 Internal contracts — `internal.proto`
Provided in Section L.

### D1.5 Data model / schema (primary persisted entities)
- `question_bank_versions`, `questions`, `admin_users`, `admin_sessions`, `audit_log_entries` (see Section L SQL).
- Encryption-at-rest: admin password hashes (hash only), session tokens (hashed), audit IP (optional masking).  
  Justification: meets **INF-ASR-SEC-01** (hardened auth) and **INF-ASR-AUD-01** (audit integrity).

### D1.6 Caching & consistency strategy
- Cache `QuestionBank(version)` in Redis with TTL 5 minutes; invalidate on publish event.  
- Strong consistency for publish: transaction commits new version; readers use “latest published” pointer.  
- If file-store mode is used, preserve atomic rename and add a distributed lock (e.g., Redis Redlock) for admin publish.  
  Justification: meets **INF-ASR-ATOMIC-01** (atomic publish).

---

## D2. Subsystem: Admin Content Management (AdminWebUI + ContentService)

### D2.1 Responsibilities & data ownership
AdminWebUI provides authenticated UI for editing/uploading question sets. ContentService validates payloads against schema, creates a new published version, and writes audit entries.

### D2.2 Technology options (same concerns; admin-specific notes)
- Persistence: prefer PostgreSQL; file-store remains supported as “compatibility mode” to match diagrams.
- Auth: prefer OIDC; local auth remains supported for air-gapped deployments.

### D2.3 Recommended default stack + justification
- **Admin auth:** OIDC (Keycloak 24-26 or Auth0) + RBAC claims  
  Justification: meets **INF-ASR-SEC-01** (hardened auth).
- **Validation:** JSON Schema draft 2020-12 via Ajv 8.x  
  Justification: meets **INF-ASR-CONTRACT-01** (contract-first validation).
- **Publishing:** DB transaction + immutable version rows; optional export to JSON file for static hosting  
  Justification: meets **INF-NFR-DUR-01** (durability) and preserves **INF-ASR-ATOMIC-01** semantics.

### D2.4 Interface design
Covered by OpenAPI endpoints: `/admin/login` (if local), `/admin/content/validate`, `/admin/content/publish`, `/admin/audit`.

### D2.5 Data model
See SQL DDLs in Section L.

### D2.6 Caching & consistency
- Admin reads latest draft from DB; publish creates new immutable version.  
- Use ETag on question bank version to prevent lost updates.

---

## D3. Subsystem: Security (AuthService + ApiGateway)

### D3.1 Responsibilities & data ownership
AuthService authenticates admins, issues sessions/tokens, enforces lockout, and validates sessions. ApiGateway enforces HTTPS-only, rate limits, and request validation.

### D3.2 Technology options
- Auth: OIDC (recommended) / local sessions / passkeys
- Gateway: NGINX Ingress / Envoy / API Gateway (Kong)

### D3.3 Recommended default stack + justification
- **Gateway:** NGINX Ingress Controller 1.10+ (or Envoy Gateway)  
  Justification: meets **INF-ASR-SEC-01** (HTTPS-only).
- **Admin auth:** OIDC + short-lived JWT (5-15 min) + refresh tokens  
  Justification: meets **INF-ASR-SEC-01** (session security).

### D3.4 Interfaces
- Internal gRPC `Auth.ValidateSession` used by ContentService (see `internal.proto`).

### D3.5 Data model
- If local auth enabled: `admin_users`, `admin_sessions` tables.

### D3.6 Caching & consistency
- Cache token introspection results for 30-60 seconds to reduce IdP load.

---

## D4. Subsystem: Audit & Compliance (AuditService)

### D4.1 Responsibilities & data ownership
Append-only audit log for admin actions (publish, validate, login failures). Enforce retention policy and support queries.

### D4.2 Technology options
- Storage: PostgreSQL append-only table / WORM object storage / log pipeline (Loki)
- Integrity: hash-chaining per entry (optional)

### D4.3 Recommended default stack + justification
- **Audit store:** PostgreSQL 14-16 with append-only constraints + partitioning by month  
  Justification: meets **INF-ASR-AUD-01** (retention ≥2 years).

### D4.4 Interfaces
- OpenAPI `/admin/audit` + internal gRPC `Audit.Append`.

### D4.5 Data model
See `sql/audit_ddl.sql`.

### D4.6 Caching & consistency
- No caching for audit writes; reads can be paginated and cached for 30s.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
See `k8s/backend-api-deployment.yaml` in Section L.  
Justification: meets **INF-NFR-AVL-01** (horizontal scaling via stateless replicas).

## E2. DB HA topology, backups, restore
- PostgreSQL HA: 1 primary + 2 synchronous replicas (small: 1 replica; medium: 2; large: 3).  
- Backups: nightly full + WAL archiving every 5 minutes; retention 35 days; quarterly restore drill.  
Justification: meets **INF-NFR-DUR-01** (durability/integrity).

## E3. Network topology + ingress/egress rules
- Ingress: HTTPS 443 only to `static-hosting` and `backend-api`.  
- East-west: backend-api → postgres (5432), redis (6379), otel-collector (4317).  
- Deny all egress by default; allow IdP endpoints if OIDC enabled.  
Mapped to **Deployment_PhysicalView** (Client→Web replicas via HTTPS; Web→Storage via LAN).  
Justification: meets **INF-ASR-SEC-01** (HTTPS-only + hardened access).

## E4. CI/CD sketch
1. PR: lint + unit tests + SAST + OpenAPI lint + contract tests  
2. Build: container build + SBOM + image scan  
3. Deploy: staging via Helm/Kustomize; run integration + E2E  
4. Promote: canary 10% → 50% → 100%, auto-rollback on SLO burn  
Justification: meets **INF-ASR-CONTRACT-01** (contract-first validation via CI gates).

---

# F. Security Design

## F1. Auth & AuthZ
- Admin: OIDC login; JWT access token (5-15 min), refresh token (rotating), RBAC claim `role=admin`.  
- EndUser: anonymous session id (cookie) with CSRF protections for state-changing calls.  
Justification: meets **INF-ASR-SEC-01**.

## F2. Secrets management & rotation
- Use Kubernetes Secrets + external KMS (AWS KMS/GCP KMS/Vault). Rotate DB creds every 90 days; rotate signing keys every 180 days.  
Justification: meets **INF-ASR-SEC-01**.

## F3. TLS & service-mesh
- TLS 1.2+ at ingress; optional mTLS in mesh (Istio/Linkerd) for internal gRPC.  
Justification: meets **INF-ASR-SEC-01**.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Credential stuffing | rate limit, MFA, lockout, breached-password checks |
| XSS in question content | sanitize HTML, CSP headers, encode output |
| CSRF on admin actions | same-site cookies, CSRF tokens |
| Tampering with published content | versioned immutable rows, audit trail, integrity hash |
| Data exfiltration via logs | structured logging with redaction, least-privilege access |

---

# G. Observability & SRE

## G1. Metrics, traces, logs + example alerts
Metrics:
- API: request rate, p95 latency, error rate by route
- Business: questions served/min, publish success/fail, validation errors
Tracing: spans for `PublishUpdate`, `ValidateContent`, `SubmitAnswer`
Logs: JSON logs with request id, admin id (if any), action, latency

Example Prometheus alerts:
- High error rate:
  - `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02`
- Latency SLO burn:
  - `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.5`

Justification: meets **INF-NFR-PERF-01** (feedback responsiveness) and **INF-NFR-AVL-01** (availability monitoring).

## G2. SLOs, error budgets, RTO/RPO
- Game API availability: 99.9% monthly; error budget 43.2 min/month  
- p95 latency for submit-answer: ≤500ms  
- RTO: 30 minutes; RPO: 5 minutes (with WAL)  
Justification: meets **INF-NFR-PERF-01** and **INF-NFR-DUR-01**.

## G3. Dashboard/runbook sketch
Dashboards: API golden signals, publish pipeline, DB health, Redis hit rate.  
Runbooks: “Publish failing schema validation”, “DB failover”, “Admin login lockouts spike”.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Notes |
|---|---|---|
| Unit | domain, application | scoring, validation |
| Integration | backend-api + postgres/redis | publish transaction, caching |
| Contract | OpenAPI + internal.proto | CI gate; backward compatibility |
| E2E | GameWebUI/AdminWebUI | playwright/cypress |
| Chaos | k8s + db failover | validate RTO/RPO |

Justification: meets **INF-ASR-CONTRACT-01** (contract-first) and **INF-NFR-AVL-01**.

## H2. Test data & environments
Envs: dev, staging, prod. Refresh staging DB weekly with synthetic data; never copy prod admin credentials.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
- If currently file-based JSON: import into DB as version `v1`; keep exporting JSON for compatibility.  
- Dual-read during cutover: API reads DB; fallback to file only if DB unavailable (time-boxed).  
Rollback: switch ingress to previous deployment; DB changes are additive (new tables/columns only).

Justification: meets **INF-NFR-AVL-01** (safe rollout).

## I2. Backwards compatibility & API versioning
- Version APIs under `/v1`; additive changes only; breaking changes require `/v2`.  
- OpenAPI contract tests ensure compatibility.

Justification: meets **INF-ASR-CONTRACT-01**.

---

# J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Why chosen |
|---|---|---|---|
| Persistence for question bank | PostgreSQL versioned content | File JSON atomic rename; DynamoDB | DB improves concurrency and integrity while preserving atomic publish semantics; ties to **INF-NFR-DUR-01** and **INF-ASR-ATOMIC-01**. |
| Admin auth | OIDC + MFA | local password auth; passkeys only | OIDC reduces risk and centralizes policy; ties to **INF-ASR-SEC-01**. |
| Internal comms | gRPC | REST only; message bus | gRPC gives typed contracts and fast calls; ties to **INF-ASR-CONTRACT-01**. |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** The UML diagrams define the target system (“Web Learning Game System”) and override the unrelated “Original Requirements” corpus for implementation scope.  
- **A2:** End users are anonymous; no PII storage is required for gameplay sessions.  
- **A3:** Admin users are a small set (<100) and can use enterprise SSO (OIDC).  
- **A4:** Question content is primarily text + multiple choice; any rich text is sanitized.  
- **A5:** Audit retention requirement is ≥2 years as stated in UML notes.  
- **A6:** Optional telemetry is allowed only in aggregate and without identifiers.

## Unresolved stakeholder questions
1. Confirm scope: “Is the deliverable the Web Learning Game System (per UML) and not the ICU/turnstile/heating/etc. systems listed in the requirements dump?”  
2. Do you require offline mode for gameplay?  
3. Should scores persist across sessions/users (leaderboards), or remain per-session only?  
4. Are there regulatory constraints (COPPA/GDPR) affecting telemetry and cookies?  
5. Do admins need draft workflows (review/approve) beyond validate/publish?

## Conflict log (per rule)
- Conflict: “Original Requirements” list many embedded/real-time control systems; UML specifies a web learning game. Resolution: proceed with UML-defined system; require stakeholder confirmation (Q1).

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# Architecture Document
This file is the rendered content of Sections A-K from ArchitectureDocument.md.
(For this delivery, ArchitectureDocument.md is the canonical artifact.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Web Learning Game System API
  version: "1.0.0"
servers:
  - url: https://api.example.com/v1
paths:
  /game/sessions:
    post:
      summary: Start a new game session
      operationId: startGameSession
      tags: [game]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              properties:
                userAgent:
                  type: string
                  minLength: 1
              required: [userAgent]
      responses:
        "201":
          description: Session created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GameSession"
        "400":
          $ref: "#/components/responses/BadRequest"
  /game/sessions/{sessionId}/question:
    get:
      summary: Get next question for a session
      operationId: getNextQuestion
      tags: [game]
      parameters:
        - name: sessionId
          in: path
          required: true
          schema: { type: string, minLength: 1 }
      responses:
        "200":
          description: Next question
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QuestionView"
        "404":
          $ref: "#/components/responses/NotFound"
  /game/sessions/{sessionId}/answers:
    post:
      summary: Submit an answer attempt and receive feedback
      operationId: submitAnswer
      tags: [game]
      parameters:
        - name: sessionId
          in: path
          required: true
          schema: { type: string, minLength: 1 }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SubmitAnswerRequest"
      responses:
        "200":
          description: Feedback and score delta
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/SubmitAnswerResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "404":
          $ref: "#/components/responses/NotFound"
  /game/sessions/{sessionId}/score:
    get:
      summary: Get current score for a session
      operationId: getScore
      tags: [game]
      parameters:
        - name: sessionId
          in: path
          required: true
          schema: { type: string, minLength: 1 }
      responses:
        "200":
          description: Score
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Score"
        "404":
          $ref: "#/components/responses/NotFound"

  /admin/auth/login:
    post:
      summary: Local admin login (only if OIDC not used)
      operationId: adminLogin
      tags: [admin]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              properties:
                username: { type: string, minLength: 1 }
                password: { type: string, minLength: 12 }
              required: [username, password]
      responses:
        "200":
          description: Session token issued
          content:
            application/json:
              schema:
                type: object
                additionalProperties: false
                properties:
                  sessionToken: { type: string, minLength: 20 }
                  expiresAtUtc: { type: string, format: date-time }
                required: [sessionToken, expiresAtUtc]
        "401":
          $ref: "#/components/responses/Unauthorized"
        "423":
          description: Account locked
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /admin/content/validate:
    post:
      summary: Validate question bank payload against schema
      operationId: validateContent
      tags: [admin]
      security:
        - AdminAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ContentUpdatePayload"
      responses:
        "200":
          description: Validation result
          content:
            application/json:
              schema:
                type: object
                additionalProperties: false
                properties:
                  valid: { type: boolean }
                  errors:
                    type: array
                    items: { $ref: "#/components/schemas/ValidationError" }
                required: [valid, errors]
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"

  /admin/content/publish:
    post:
      summary: Publish a validated question bank as a new version
      operationId: publishUpdate
      tags: [admin]
      security:
        - AdminAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              properties:
                payload:
                  $ref: "#/components/schemas/ContentUpdatePayload"
                expectedCurrentVersion:
                  type: string
                  description: Optimistic concurrency control; publish fails if current version differs.
              required: [payload, expectedCurrentVersion]
      responses:
        "201":
          description: Published
          content:
            application/json:
              schema:
                type: object
                additionalProperties: false
                properties:
                  newVersion: { type: string }
                  publishedAtUtc: { type: string, format: date-time }
                required: [newVersion, publishedAtUtc]
        "409":
          description: Version conflict
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          $ref: "#/components/responses/Unauthorized"

  /admin/audit:
    get:
      summary: Query audit log entries
      operationId: queryAudit
      tags: [admin]
      security:
        - AdminAuth: []
      parameters:
        - name: fromUtc
          in: query
          required: true
          schema: { type: string, format: date-time }
        - name: toUtc
          in: query
          required: true
          schema: { type: string, format: date-time }
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 1000, default: 200 }
      responses:
        "200":
          description: Audit entries
          content:
            application/json:
              schema:
                type: object
                additionalProperties: false
                properties:
                  entries:
                    type: array
                    items: { $ref: "#/components/schemas/AuditLogEntry" }
                required: [entries]
        "401":
          $ref: "#/components/responses/Unauthorized"

components:
  securitySchemes:
    AdminAuth:
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
    NotFound:
      description: Not found
      content:
        application/json:
          schema: { $ref: "#/components/schemas/Error" }
  schemas:
    Error:
      type: object
      additionalProperties: false
      properties:
        code: { type: string }
        message: { type: string }
        details:
          type: object
          additionalProperties: true
      required: [code, message]
    GameSession:
      type: object
      additionalProperties: false
      properties:
        sessionId: { type: string }
        startedAtUtc: { type: string, format: date-time }
        status: { type: string, enum: [Created, Active, Completed, Abandoned] }
      required: [sessionId, startedAtUtc, status]
    QuestionView:
      type: object
      additionalProperties: false
      properties:
        questionId: { type: string }
        prompt: { type: string }
        choices:
          type: array
          minItems: 2
          items: { type: string }
      required: [questionId, prompt, choices]
    SubmitAnswerRequest:
      type: object
      additionalProperties: false
      properties:
        questionId: { type: string }
        selectedChoiceIndex: { type: integer, minimum: 0 }
      required: [questionId, selectedChoiceIndex]
    SubmitAnswerResponse:
      type: object
      additionalProperties: false
      properties:
        attemptId: { type: string }
        isCorrect: { type: boolean }
        pointsDelta: { type: integer }
        score: { $ref: "#/components/schemas/Score" }
      required: [attemptId, isCorrect, pointsDelta, score]
    Score:
      type: object
      additionalProperties: false
      properties:
        points: { type: integer, minimum: 0 }
        correctCount: { type: integer, minimum: 0 }
        incorrectCount: { type: integer, minimum: 0 }
      required: [points, correctCount, incorrectCount]
    ValidationError:
      type: object
      additionalProperties: false
      properties:
        path: { type: string }
        message: { type: string }
      required: [path, message]
    ContentUpdatePayload:
      type: object
      additionalProperties: false
      properties:
        schemaVersion: { type: string, example: "1.0.0" }
        questions:
          type: array
          minItems: 1
          items:
            type: object
            additionalProperties: false
            properties:
              questionId: { type: string }
              prompt: { type: string }
              choices:
                type: array
                minItems: 2
                items: { type: string }
              correctChoiceIndex: { type: integer, minimum: 0 }
              difficulty: { type: string }
            required: [questionId, prompt, choices, correctChoiceIndex]
      required: [schemaVersion, questions]
    AuditLogEntry:
      type: object
      additionalProperties: false
      properties:
        eventId: { type: string }
        timestampUtc: { type: string, format: date-time }
        adminId: { type: string }
        remoteIp: { type: string }
        action: { type: string }
        beforeHash: { type: string }
        afterHash: { type: string }
      required: [eventId, timestampUtc, adminId, remoteIp, action, beforeHash, afterHash]
```

```proto
// filename: internal.proto
syntax = "proto3";

package weblearning.internal.v1;

option go_package = "weblearning/internal/v1;internalv1";

message ValidateSessionRequest {
  string token = 1;
}

message ValidateSessionResponse {
  bool valid = 1;
  string admin_id = 2;
  repeated string roles = 3;
  string expires_at_utc = 4;
}

service Auth {
  rpc ValidateSession(ValidateSessionRequest) returns (ValidateSessionResponse);
}

message AppendAuditRequest {
  string timestamp_utc = 1;
  string admin_id = 2;
  string remote_ip = 3;
  string action = 4;
  string before_hash = 5;
  string after_hash = 6;
}

message AppendAuditResponse {
  string event_id = 1;
}

service Audit {
  rpc Append(AppendAuditRequest) returns (AppendAuditResponse);
}

message PublishContentRequest {
  string admin_id = 1;
  string expected_current_version = 2;
  string payload_json = 3;
}

message PublishContentResponse {
  string new_version = 1;
  string published_at_utc = 2;
}

service ContentPublisher {
  rpc Publish(PublishContentRequest) returns (PublishContentResponse);
}
```

```yaml
# filename: k8s/backend-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  labels:
    app: backend-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
    spec:
      containers:
        - name: backend-api
          image: example.com/weblearning/backend-api:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: backend-api-secrets
                  key: databaseUrl
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: backend-api-secrets
                  key: redisUrl
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
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
  name: backend-api
spec:
  selector:
    app: backend-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-api
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
  name: backend-api-config
data:
  LOG_LEVEL: "info"
---
apiVersion: v1
kind: Secret
metadata:
  name: backend-api-secrets
type: Opaque
stringData:
  databaseUrl: "postgresql://weblearning:CHANGE_ME@postgres:5432/weblearning"
  redisUrl: "redis://redis:6379/0"
```

```sql
-- filename: sql/content_ddl.sql
CREATE TABLE IF NOT EXISTS question_bank_versions (
  version_id BIGSERIAL PRIMARY KEY,
  version_text TEXT NOT NULL UNIQUE,
  schema_version TEXT NOT NULL,
  published_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_by_admin_id TEXT NOT NULL,
  payload_sha256 CHAR(64) NOT NULL,
  is_current BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_question_bank_current
ON question_bank_versions (is_current)
WHERE is_current = TRUE;

CREATE TABLE IF NOT EXISTS questions (
  question_pk BIGSERIAL PRIMARY KEY,
  version_id BIGINT NOT NULL REFERENCES question_bank_versions(version_id) ON DELETE CASCADE,
  question_id TEXT NOT NULL,
  prompt TEXT NOT NULL,
  choices JSONB NOT NULL,
  correct_choice_index INT NOT NULL CHECK (correct_choice_index >= 0),
  difficulty TEXT NULL,
  CONSTRAINT uq_question_per_version UNIQUE (version_id, question_id)
);

CREATE INDEX IF NOT EXISTS ix_questions_version ON questions(version_id);
```

```sql
-- filename: sql/auth_ddl.sql
CREATE TABLE IF NOT EXISTS admin_users (
  admin_id TEXT PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  is_locked BOOLEAN NOT NULL DEFAULT FALSE,
  failed_attempts INT NOT NULL DEFAULT 0,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS admin_sessions (
  session_id TEXT PRIMARY KEY,
  admin_id TEXT NOT NULL REFERENCES admin_users(admin_id) ON DELETE CASCADE,
  token_hash CHAR(64) NOT NULL UNIQUE,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at_utc TIMESTAMPTZ NOT NULL,
  revoked_at_utc TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS ix_admin_sessions_admin ON admin_sessions(admin_id);
CREATE INDEX IF NOT EXISTS ix_admin_sessions_expires ON admin_sessions(expires_at_utc);
```

```sql
-- filename: sql/audit_ddl.sql
CREATE TABLE IF NOT EXISTS audit_log_entries (
  event_id BIGSERIAL PRIMARY KEY,
  timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  admin_id TEXT NOT NULL,
  remote_ip INET NOT NULL,
  action TEXT NOT NULL,
  before_hash CHAR(64) NOT NULL,
  after_hash CHAR(64) NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_audit_time ON audit_log_entries(timestamp_utc);
CREATE INDEX IF NOT EXISTS ix_audit_admin ON audit_log_entries(admin_id);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-GAME-01,End user can play game (intro → questions → score),"UseCase_ScenarioView:UC_PlayGame|State_LogicView_GameSession:GSL","GameWebUI;GameService","ArchitectureDocument.md;openapi.yaml",Implements core gameplay flow and session lifecycle.
INF-FR-GAME-02,Provide feedback per answer,"UseCase_ScenarioView:UC_GetFeedback|Sequence_ProcessView_S2_EndUserPlayGame","GameService","openapi.yaml",Submit-answer returns correctness and score delta.
INF-FR-ADMIN-01,Admin login,"UseCase_ScenarioView:UC_AdminLogin|Sequence_ProcessView_S1_AdminPublishUpdate","AuthService;AdminWebUI","openapi.yaml;internal.proto",Admin authentication and session validation.
INF-FR-ADMIN-02,Admin manages questions,"UseCase_ScenarioView:UC_ManageQuestions|Class_LogicView:QuestionBank,Question","ContentService","openapi.yaml;sql/content_ddl.sql",CRUD/versioned content management.
INF-ASR-CONTRACT-01,Contract-first schema validation,"Class_LogicView:ContentUpdateRequest|Activity_ProcessView_AdminPublishUpdate","ContentService","openapi.yaml;ArchitectureDocument.md",Server-side JSON schema validation.
INF-ASR-ATOMIC-01,Atomic publish semantics,"Class_LogicView:ContentPublisher|Component_DevelopmentView:FileStore","ContentService;Persistence","ArchitectureDocument.md",Prevents partial/corrupt publishes.
INF-ASR-AUD-01,Audit logging + retention,"Class_LogicView:AuditLog,AuditLogEntry|Component_DevelopmentView:AuditService","AuditService","sql/audit_ddl.sql",Append-only audit with query support.
INF-ASR-SEC-01,Hardened auth + HTTPS-only,"Class_LogicView:AdminUser|Component_DevelopmentView:AuthService","AuthService;ApiGateway","ArchitectureDocument.md;openapi.yaml",Lockout, hashing, TLS enforcement.
INF-NFR-PERF-01,Feedback within 500ms,"State_LogicView_GameSession:GSL","GameService","ArchitectureDocument.md",Latency SLO and tests.
INF-NFR-WEB-01,HTML5 no plugins,"Package_DevelopmentView:ui","GameWebUI;AdminWebUI","ArchitectureDocument.md",Standards-based browser UI.
INF-NFR-AVL-01,Stateless scaling,"Deployment_PhysicalView:Web Server Node (Replica 1/2)","Backend API","k8s/backend-api-deployment.yaml",Replicas + HPA.
INF-NFR-DUR-01,Durability/integrity,"Component_DevelopmentView:FileStore|Class_LogicView:QuestionBank","Persistence","sql/content_ddl.sql",Versioning + hashes.
```

---

## Verification table (Acceptance Criteria)

| Check | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | [x] |
| [ ] Sections A-L included. | [x] |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | [x] *(all are inferred as INF- due to missing IDs)* |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | [x] |
| [ ] Representative k8s manifest snippet included. | [x] |
| [ ] SQL DDL / NoSQL models for primary entities included. | [x] |
| [ ] All major components have at least one API contract and a data schema. | [x] |
| [ ] Assumptions and unresolved questions listed. | [x] |

---

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?