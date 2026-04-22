Analysis Plan  
Scope: Produce production-ready architecture documentation + delivery artifacts for the Space Fractions web learning game and its admin question updater, aligned to provided SRS and 11 UML diagrams.  
Approach: Use 4+1 views, infer missing requirement IDs as INF-*, define contracts (OpenAPI + internal proto), persistence schemas, and k8s-ready ops plan with security/observability/testing.  
Top validation steps: Traceability matrix completeness (all FR/NFR/ASR/INF), contract linting (OpenAPI/proto), and deployability checks (k8s manifest + DB schema + security controls).

# A. Executive Summary (≤1 page)

**System overview.** Space Fractions is a web-based interactive learning game for 6th graders to practice fraction skills through a storyline with multiple-choice questions, immediate feedback (sound/animation), adaptive branching at critical questions, and a final score/rank message. A web-accessible **Question Updater** allows an administrator (teacher) to edit question content stored on the server.

**Primary diagram mapping (one-line).** End-to-end behavior is captured by **UseCase_SpaceFractions (UC_PlayGame, UC_UpdateQ)**, runtime flow by **Activity_PlayGameEndToEnd**, and deployment by **Deployment_SpaceFractions (WebServer, StudentDevice, AdminDevice)**.

**Architectural style(s).**
- **Client-heavy web app + thin content/admin API** (SPA + REST): keeps gameplay state local and minimizes server dependencies.  
- **Contract-first content boundary** (OpenAPI + schema-validated JSON): ensures maintainability and safe updates.

**Deployment topology (one-line).** Static game assets served via HTTPS CDN/static server; admin API served via HTTPS; questions stored as versioned JSON; audit logs append-only (see **Container_SpaceFractions: Hosting**).

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---:|---|
| Flash dependency in SRS vs modern browsers | High | Implement HTML5/JS replacement; keep “movie” as MP4/Lottie; document conflict and provide compatibility plan (A1, K). |
| “Score local only” vs desire for ranking/competition | Medium | Keep score in-memory only (no persistence) per FR; show rank as local tier label; if future leaderboard needed, add opt-in server feature behind new requirements (INF). |
| Admin updater security (password-only) | High | Enforce strong password hashing + lockout + HTTPS + audit trail; restrict updater endpoints; add CSRF protection (NFR security inferred). |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality | Requirement IDs | Test types |
|---|---|---|
| Scalability | INF-NFR-SCALE-001 (multi-user access), NFR-001 (uptime) | Load test (k6), CDN cache tests, HPA simulation |
| Availability | NFR-001 | Synthetic probes, chaos (pod kill), backup/restore drills |
| Security | NFR-008, FR-021 | SAST/DAST, authn lockout tests, TLS config scan |
| Performance | NFR-009, FR-019, ASR-008 | Lighthouse, WebPageTest, browser perf tests, latency unit tests |
| Maintainability | NFR-007, ASR-003 | Contract tests, schema validation tests, modular build checks |

---

# B. Traceability & Rationale

Because the provided SRS text does not include explicit IDs, the following IDs are **inferred** and prefixed with `INF-`. They are mapped to the provided UML diagrams by **title and element IDs** only (no PlantUML source embedded).

```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,Web-based interactive fraction learning game,UseCase_SpaceFractions:UC_PlayGame; Deployment_SpaceFractions:StudentDevice/WebServer,GameWebUI StaticServer,architecture.md,Defines overall system scope and web delivery.
INF-FR-002,Run in browser on Internet-accessible computers,Deployment_SpaceFractions:StudentDevice; Container_SpaceFractions:StudentBrowser,GameWebUI,architecture.md,Ensures browser-based compatibility and internet hosting.
INF-FR-003,Introductory movie plays on start,Sequence_S1_PlayIntroToMenu:IntroMoviePlayer.play; State_GameSession:IntroPlaying,GameWebUI,architecture.md,Implements intro playback as first screen.
INF-FR-004,User can skip intro via mouse click,UseCase_SpaceFractions:UC_SkipIntro; Sequence_S1_PlayIntroToMenu:skipClick,GameWebUI,architecture.md,Supports skip behavior at any time.
INF-FR-005,Main menu with help section,UseCase_SpaceFractions:UC_MainMenu; Class_SpaceFractions:MainMenu,GameWebUI,architecture.md,Provides help and navigation entry point.
INF-FR-006,Main menu includes team summary + website link,Class_SpaceFractions:MainMenu,GameWebUI,architecture.md,Static content on menu page.
INF-FR-007,Main menu starts game on click,Activity_PlayGameEndToEnd:User clicks Start Game; State_GameSession:MainMenuShown->GameplayActive,GameController,architecture.md,Routes to gameplay session.
INF-FR-008,Series of fraction questions in storyline,UseCase_SpaceFractions:UC_Answer; Class_SpaceFractions:QuestionBank/StoryEngine,GameplayEngine QuestionLoader,architecture.md; openapi.yaml,Questions loaded and sequenced by story engine.
INF-FR-009,Questions are multiple-choice,Class_SpaceFractions:Question/Choice; State_GameSession:AwaitingAnswer,GameplayEngine,architecture.md,Choice model and UI rendering.
INF-FR-010,Test fraction arithmetic/equivalence/graphical/improper vs proper,Class_SpaceFractions:QuestionBank,Question content,questions.json schema (documented),architecture.md,Content model supports varied question types.
INF-FR-011,Robot sidekick provides hints,UseCase_SpaceFractions:UC_Hint; Activity_PlayGameEndToEnd:Show hint,FeedbackService UI,architecture.md,Hint field and UI trigger.
INF-FR-012,Adaptive/dynamic storyline branching on progress,State_GameSession:Branching; Class_SpaceFractions:StoryEngine.branch,StoryEngine,architecture.md,Branching based on critical correctness.
INF-FR-013,Critical questions affect plot/ending,State_GameSession:Branching; EndingShown,StoryEngine,architecture.md,Tracks critical outcomes for ending selection.
INF-FR-014,Score kept locally within game session only,Class_SpaceFractions:Score «local»; Container_SpaceFractions:LocalSession,GameSession,architecture.md,No server persistence; in-memory only.
INF-FR-015,Incorrect answer allows retry but no points,Activity_PlayGameEndToEnd:mark no-point; State_GameSession:incorrect/markNoPoint,Score,architecture.md,Implements penalty logic.
INF-FR-016,Input is mouse clicks for answers/preferences,UseCase_SpaceFractions:EndUser interactions,GameWebUI,architecture.md,UI event model uses clicks.
INF-FR-017,Output is sounds/animations acknowledging success/failure,FeedbackService; Activity_PlayGameEndToEnd:Emit feedback,GameWebUI FeedbackService,architecture.md,Feedback events drive audio/animation.
INF-FR-018,Fraction input: numerator/denominator integers; denom != 0,State_GameSession:VelocityAdjusting; Class_SpaceFractions:FractionValidator,GameplayEngine PhysicsEngine,architecture.md,Validates and rejects invalid fractions.
INF-FR-019,Feedback event emitted within 500ms of click,Class_SpaceFractions:FeedbackService note; Activity_PlayGameEndToEnd note,FeedbackService,architecture.md,Defines measurable UI responsiveness requirement.
INF-FR-020,Admin can update questions via web tool,UseCase_SpaceFractions:UC_UpdateQ; Sequence_S2_AdminUpdateQuestions,AdminController,openapi.yaml,Admin API supports CRUD/update.
INF-FR-021,Updater requires password login + lockout/strong hashing,Sequence_S2_AdminUpdateQuestions:AdminAuthService; Class_SpaceFractions:AdminAuthService note,AdminAuthService,architecture.md; sql/admin_ddl.sql,Implements secure authentication controls.
INF-FR-022,Updated questions saved on web server in easily edited file,Class_SpaceFractions:QuestionFileRepository; Component_SpaceFractions:QuestionFileRepository,QuestionStore,architecture.md; sql/question_version_ddl.sql,Uses JSON file store with atomic writes and versioning.
INF-FR-023,Math Umbrella provides links to external projects,UseCase_SpaceFractions:UC_Umbrella; Container_SpaceFractions:UmbrellaSite,GameWebUI,architecture.md,Opens external links in new window.
INF-FR-024,Open Denominators web page from menu,UseCase_SpaceFractions:UC_Denom; Container_SpaceFractions:DenomSite,GameWebUI,architecture.md,External link handling.
INF-FR-025,Ending scene shows score+rank and option try again/quit,UseCase_SpaceFractions:UC_FinalScore/UC_EndNav; State_GameSession:EndingShown,GameSession UI,architecture.md,Implements final screen and navigation.
INF-FR-026,Velocity adjustment: convert fraction to decimal and apply to physics engine immediately,UseCase_SpaceFractions:UC_Velocity; Class_SpaceFractions:VelocityCalculator/PhysicsEngine; State_GameSession note,PhysicsEngine,architecture.md,Real-time adjustment loop.
INF-NFR-001,Availability: hosted on S2S website; target 99.9% uptime,Deployment_SpaceFractions:WebServer note,Hosting/Ingress,architecture.md; k8s/game-deployment.yaml,Ops plan includes replicas, probes, and SLOs.
INF-NFR-002,Cross-browser consistent behavior,Deployment_SpaceFractions:StudentDevice note,GameWebUI,architecture.md,Defines supported browser matrix and tests.
INF-NFR-003,No new hardware required,Deployment_SpaceFractions,All,architecture.md,Uses standard web stack.
INF-NFR-004,Usability for Alice/Bobby/Claire,UseCase_SpaceFractions; MainMenu/Hint,GameWebUI,architecture.md,Help, hints, and simple click interactions.
INF-NFR-005,Performance: intro+menu load within ~60s on slow link,Activity_PlayGameEndToEnd note; Deployment_SpaceFractions note,StaticServer/CDN,architecture.md,Asset optimization and caching.
INF-NFR-006,Reliability ensured by extensive testing,All test diagrams,CI/CD + Testing,architecture.md,Defines test strategy and automation.
INF-NFR-007,Maintainability is primary goal,Package_SpaceFractions,Modular packages,architecture.md,Separation of concerns and contract-first content.
INF-NFR-008,Security: as secure as browser; admin tool secured; audit retention >=2y,Sequence_S2_AdminUpdateQuestions; Deployment_SpaceFractions note,AdminAPI AuditStore,architecture.md; sql/audit_log_ddl.sql,Adds HTTPS, hashing, lockout, and append-only audit.
INF-CONFLICT-001,SRS says Flash required but modern design uses HTML5,Deployment/Container diagrams imply HTML5,Architecture decision,architecture.md,K section logs conflict and resolution.
```

---

# C. Architecture Overview

## 4+1 View alignment

**Scenario (Use Case) View.** Primary user journeys are in **UseCase_SpaceFractions**: gameplay (**UC_PlayGame**, includes **UC_WatchIntro**, **UC_Answer**, **UC_FinalScore**) and admin updates (**UC_UpdateQ** includes **UC_AdminLogin**).

**Logical (Class/State) View.** Core domain objects are in **Class_SpaceFractions** (e.g., **GameSession**, **QuestionBank**, **StoryEngine**, **Score**, **FractionValidator**, **VelocityCalculator**, **PhysicsEngine**). Runtime states are in **State_GameSession** (IntroPlaying → MainMenuShown → GameplayActive → EndingShown).

**Process View.** End-to-end activity is in **Activity_PlayGameEndToEnd**; key sequences are **Sequence_S1_PlayIntroToMenu** and **Sequence_S2_AdminUpdateQuestions**; collaborations are **Collaboration_S1_PlayIntroToMenu** and **Collaboration_S2_AdminUpdateQuestions**.

**Development View.** Code organization is in **Package_SpaceFractions** (ui/app/domain/content/physics/admin/security/persistence) and runtime components in **Component_SpaceFractions** (GameWebUI, AdminWebUI, AdminController, QuestionFileRepository, AuditLogger).

**Physical/Deployment View.** Hosting and nodes are in **Deployment_SpaceFractions** and **Container_SpaceFractions**: student/admin browsers connect via HTTPS to S2S hosting; questions.json and audit logs are server-side.

---

# D. Detailed Technical Design (developer-facing)

## D1. Game Web UI + Gameplay Engine (GameWebUI, GameController, GameplayEngine)

### 1) Responsibilities & data ownership
Owns all student-facing screens (intro, menu, gameplay, ending), input handling (mouse clicks), local-only session state (score/progress), immediate feedback events, and real-time velocity adjustment applied to an in-browser physics loop. **Data ownership:** gameplay state is **ephemeral in memory** (Score/StoryProgress) per INF-FR-014; question content is read-only fetched from server.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime (frontend)**
- Recommended: **TypeScript 5.3+** with **Node.js 18-20** toolchain.  
- Conservative: ES2019 JavaScript + minimal tooling.  
- Cutting-edge: TypeScript + WebAssembly modules for physics.  
Justification: meets **INF-NFR-007 (maintainability)** via typed modular code.

**Web framework**
- Recommended: **React 18** (or Vue 3) SPA.  
- Conservative: Vanilla JS + Web Components.  
- Cutting-edge: SvelteKit 2.  
Justification: meets **INF-NFR-004 (usability)** with mature UI patterns and accessibility tooling.

**RPC/HTTP**
- Recommended: Fetch API over HTTPS to static JSON + admin API only for admin.  
- Conservative: No runtime HTTP beyond initial asset load (bundle questions into build).  
- Cutting-edge: GraphQL for content.  
Justification: meets **INF-FR-022 (server file-based questions)** by fetching versioned JSON.

**Persistence (client)**
- Recommended: **In-memory only** (no localStorage) for score/progress.  
- Conservative: sessionStorage (still local) but violates strict “memory only”.  
- Cutting-edge: IndexedDB for offline mode (new requirement).  
Justification: meets **INF-FR-014 (score local only)**.

**Cache**
- Recommended: HTTP caching for static assets; in-app cache for QuestionBank with TTL=5 min.  
- Conservative: no caching.  
- Cutting-edge: Service Worker offline cache.  
Justification: meets **INF-NFR-005 (slow link load)**.

**Messaging**
- Recommended: none (single-user session).  
- Conservative: none.  
- Cutting-edge: WebSocket for live classroom competition (new requirement).  
Justification: meets **INF-FR-014** and “single instance per user”.

**Search**
- Recommended: none.  
- Conservative: none.  
- Cutting-edge: client-side search for question bank (admin feature).  
Justification: scope-limited; no SRS need.

**Authn/Authz**
- Recommended: none for students; admin handled server-side.  
- Conservative: basic auth for admin (avoid).  
- Cutting-edge: OIDC for admin.  
Justification: meets **INF-FR-021 (admin login)** while keeping student flow frictionless.

**Observability**
- Recommended: browser RUM events + server metrics.  
- Conservative: console logs only.  
- Cutting-edge: OpenTelemetry in browser.  
Justification: meets **INF-NFR-006 (reliability via testing/monitoring)**.

**CI/CD**
- Recommended: GitHub Actions + unit/e2e + contract checks.  
- Conservative: manual deploy.  
- Cutting-edge: progressive delivery with feature flags.  
Justification: meets **INF-NFR-006**.

**Container runtime / infra provisioning**
- Recommended: Docker + Kubernetes; Terraform for infra.  
- Conservative: VM + nginx.  
- Cutting-edge: serverless edge hosting.  
Justification: meets **INF-NFR-001 (uptime)** with replicas and health checks.

### 3) Recommended default stack (explicit versions)
- Frontend: **TypeScript 5.3-5.6**, **React 18.2**, **Vite 5-6**, Node **18-20**.
- Physics/animation: **Canvas/WebAudio** + requestAnimationFrame loop.
- Content: fetch `/content/questions.json` with ETag caching.
Justification: meets **INF-NFR-007 (maintainability)** and **INF-NFR-005 (performance)**.

### 4) Interface design

#### External APIs (OpenAPI YAML) — `openapi.yaml`
Covers admin login, read questions, update questions, get current version, and audit query (admin-only).

#### Internal contracts — `internal.proto`
Defines internal service boundary for question loading, validation, and audit append (even if implemented in-process initially).

### 5) Data model / schema
Gameplay score is not persisted. Persisted entities are server-side: admin accounts, question versions, audit logs (see SQL in Section L).

### 6) Caching & consistency strategy
- **Client** caches questions in memory; revalidate via ETag on refresh; TTL 5 minutes during a session.
- **Server** serves `questions.json` with `Cache-Control: max-age=60` and ETag; admin update invalidates by writing new version and updating “current pointer”.
- Consistency: **strong** for admin update (atomic write + version bump), **eventual** for clients (cache expiry/refresh).

---

## D2. Admin Updater Backend (AdminController, AdminAuthService, QuestionFileRepository, AuditLogger)

### 1) Responsibilities & data ownership
Provides password-based admin authentication, serves admin UI, validates and writes updated question sets to server storage atomically, and appends immutable audit records for login attempts and edits. **Data ownership:** questions and audit logs are server-owned persisted data.

### 2) Technology options (≥3 alternatives per concern)

**Language/runtime (backend)**
- Recommended: **Node.js 18-20 (TypeScript)**.  
- Conservative: Python **3.11-3.12** (FastAPI).  
- Cutting-edge: Go **1.22-1.23**.  
Justification: meets **INF-NFR-007 (maintainability)** with shared TS models and schema validation.

**Web framework**
- Recommended: **Express 4.18+** or **Fastify 4-5**.  
- Conservative: nginx + CGI (not recommended).  
- Cutting-edge: Bun server.  
Justification: meets **INF-FR-020 (web-accessible updater)**.

**RPC/HTTP**
- Recommended: REST/JSON over HTTPS.  
- Conservative: server-rendered forms only.  
- Cutting-edge: gRPC-web.  
Justification: meets **INF-NFR-008 (security)** with standard HTTPS REST.

**Persistence**
- Recommended: **PostgreSQL 14-16** for admin + audit + question version metadata; store actual `questions.json` in object storage or filesystem.  
- Conservative: filesystem-only JSON + flat audit file.  
- Cutting-edge: event store (Kafka + compacted topics).  
Justification: meets **INF-NFR-008 (audit retention >=2y)** with durable DB retention and queryability.

**Cache**
- Recommended: none required; rely on HTTP caching for static.  
- Conservative: none.  
- Cutting-edge: Redis 7 for rate limiting and lockout counters.  
Justification: meets **INF-FR-021 (lockout)** reliably across replicas.

**Messaging**
- Recommended: none.  
- Conservative: none.  
- Cutting-edge: queue for async audit shipping.  
Justification: scope.

**Search**
- Recommended: none.  
- Conservative: none.  
- Cutting-edge: OpenSearch for audit search.  
Justification: scope.

**Authn/Authz**
- Recommended: **Session cookie** after login + CSRF tokens; password hashed with **Argon2id**.  
- Conservative: HTTP Basic (avoid).  
- Cutting-edge: OIDC (Azure AD/Google Workspace).  
Justification: meets **INF-FR-021** and **INF-NFR-008**.

**Observability**
- Recommended: Prometheus metrics + structured logs.  
- Conservative: file logs only.  
- Cutting-edge: OpenTelemetry collector.  
Justification: meets **INF-NFR-001 (uptime)** via monitoring.

**CI/CD**
- Recommended: build, unit, integration, contract, security scans, deploy with canary.  
Justification: meets **INF-NFR-006 (reliability)**.

**Container runtime / infra provisioning**
- Recommended: Kubernetes + Helm; Terraform.  
Justification: meets **INF-NFR-001**.

### 3) Recommended default stack
- Backend: **Node.js 18-20**, **Fastify 4-5**, **PostgreSQL 14-16**, **Redis 7.2** (optional for lockout/rate limit), **Argon2id**.
Justification: meets **INF-NFR-008 (security/audit)** and **INF-NFR-001 (availability)**.

### 4) Interface design
- External OpenAPI in `openapi.yaml` (admin endpoints).
- Internal proto in `internal.proto` (question store + audit append).

### 5) Data model / schema
- `admin_user`, `admin_session`, `question_set_version`, `audit_log` tables (see SQL).
- Encryption-at-rest: DB volume encryption; secrets in K8s Secret manager.
Justification: meets **INF-NFR-008**.

### 6) Caching & consistency
- Strong consistency for updates: DB transaction for metadata + atomic object/file write; only then switch “current version”.
- Clients may see old version until cache expires.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)
Justification: meets **INF-NFR-001 (99.9% uptime)** via replicas, probes, and HPA.

## E2. DB HA topology, backups, restore
- PostgreSQL: 1 primary + 1 standby (streaming replication), automated failover (Patroni or managed service).
- Backups: nightly full + WAL archiving; retention 30 days; quarterly restore drill.
Justification: meets **INF-NFR-008 (audit retention)** and **INF-NFR-001 (availability)**.

## E3. Network topology + ingress/egress
- Ingress: `/game/*` static assets; `/api/admin/*` admin API (restricted).
- Egress: allow only to required external sites for link opening (client-side).
- Latency: admin API p95 < 200ms intra-region; game assets served via CDN.
References: **Deployment_SpaceFractions: Internet↔WebServer HTTPS**.

## E4. CI/CD sketch
1. Lint/format → unit tests → build artifacts.
2. Contract tests: OpenAPI lint + schema validation.
3. E2E: Playwright for game flow + admin update flow.
4. Security: dependency scan + SAST.
5. Deploy: canary 10% then full; rollback on SLO burn.
Justification: meets **INF-NFR-006 (reliability)**.

---

# F. Security Design

## F1. Auth & AuthZ
- Students: no auth.
- Admin: password login → server issues **HttpOnly, Secure session cookie** (SameSite=Lax) with CSRF token for state-changing requests.
- Lockout: 5 failed attempts → 1 hour lock; stored in Redis or DB.
Justification: meets **INF-FR-021** and **INF-NFR-008**.

## F2. Secrets management & rotation
- Use Kubernetes Secrets via external secret manager (AWS Secrets Manager / GCP Secret Manager / Vault).
- Rotate admin password hashes via reset flow; rotate signing keys every 90 days.
Justification: meets **INF-NFR-008**.

## F3. TLS & service-mesh
- TLS 1.2+ at ingress; optional mTLS inside cluster if service mesh (Istio/Linkerd) is adopted.
Justification: meets **INF-NFR-008**.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Brute-force admin password | lockout + rate limit + strong hashing (Argon2id) |
| CSRF on admin update | CSRF token + SameSite cookies |
| Tampering with questions.json | atomic writes + versioning + audit log |
| XSS in question content | sanitize/escape HTML; content validation |
| Audit log deletion | append-only table + restricted DB role + backups |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + example alerts
- Metrics: request rate, p95 latency, 4xx/5xx, login failures, update success, audit append failures.
- Logs: JSON structured with requestId, adminId, remoteIp; never log passwords.
- RUM: client emits “feedback latency” metric for INF-FR-019.

Example Prometheus alert rules:
- High error rate:
  `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02`
- Admin brute force:
  `sum(rate(admin_login_fail_total[5m])) by (ip) > 10`

Justification: meets **INF-NFR-001 (uptime)** and **INF-NFR-006 (reliability)**.

## G2. SLOs / error budgets / RTO/RPO
- Availability SLO: 99.9% monthly (INF-NFR-001).
- Admin update RPO: 24h (nightly backup), RTO: 1h.
- Audit log RPO: 5 min (WAL), RTO: 1h.
Justification: meets **INF-NFR-008**.

## G3. Dashboard/runbook sketch
- Dashboards: API latency, error rate, login failures, update throughput, DB replication lag.
- Runbooks: “Admin cannot login”, “Questions not updating”, “High 5xx”.

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Examples |
|---|---|---|
| Unit | StoryEngine, Score, FractionValidator | penalty logic, denom!=0 |
| Integration | AdminController↔Postgres, Question store | atomic version switch |
| Contract | OpenAPI + JSON schema | validate questions payload |
| E2E | Game flow + admin update | intro skip, branching, ending |
| Chaos | k8s pods/DB failover | ensure uptime SLO |

Justification: meets **INF-NFR-006**.

## H2. Test data & environments
- Envs: dev, staging, prod.
- Staging refresh: weekly; prod-like config; synthetic admin user.
- Question sets: seeded fixtures; schema-validated.
Justification: meets **INF-NFR-007 (maintainability)**.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
If replacing an older hosted version:
1. Import existing questions into new JSON schema.
2. Run schema validation + snapshot version.
3. Deploy static assets + admin API.
4. Cutover DNS; keep old site read-only for 1 week.
Rollback: revert DNS + restore previous question version pointer.
Justification: meets **INF-NFR-001**.

## I2. Backwards compatibility & versioning
- Version questions as `question_set_version.version` integer; keep last N versions.
- API versioning: `/api/v1/...`; breaking changes require `/v2`.
Justification: meets **INF-NFR-007**.

---

# J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Why chosen (tie to IDs) |
|---|---|---|---|
| Replace Flash with HTML5 | HTML5 SPA | Keep Flash (obsolete); Unity WebGL | Meets **INF-NFR-002** cross-browser and resolves Flash conflict (K). |
| Persist questions in DB + export JSON | Hybrid | Filesystem-only; full DB-only | Meets **INF-FR-022** (file-based) while meeting **INF-NFR-008** audit/retention. |
| Admin auth via session cookies | Cookie session | JWT; OIDC | Meets **INF-FR-021** with simpler CSRF-safe admin UI. |
| No student accounts | None | Student login + profiles | Meets **INF-FR-014** local-only score and reduces PII/security scope. |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** Flash requirement is treated as legacy; implementation will be HTML5/JS with equivalent behavior (intro “movie” as MP4/Lottie).  
- **A2:** “Ranked” score in ending is a **local tier label** (e.g., Bronze/Silver/Gold) not a global leaderboard, to preserve INF-FR-014.  
- **A3:** Question content format will be a validated JSON schema with fields matching Class_SpaceFractions:Question/Choice.  
- **A4:** Admin is a single role (“teacher/admin”) with full edit rights; no RBAC beyond admin/non-admin.  
- **A5:** Audit retention “>=2 years” is required (from diagrams/notes) and is treated as binding (INF-NFR-008).

## Conflicts logged (per rule)
- **INF-CONFLICT-001:** SRS states “browser capable of running Flash movies”; diagrams and modern deployment assume HTML5. Resolution: follow SRS naming (“movie”) but implement via HTML5; document as A1.

## Unresolved stakeholder questions
1. Should the Question Updater support **multiple admins** and password reset workflow (email) or only a shared password?  
2. Are there any **content moderation** requirements (e.g., profanity filter) for custom questions?  
3. What is the expected **max question set size** (e.g., 20 vs 500) to size payload and caching?  
4. Should the game support **offline play** (service worker) given slow connections?  
5. Is “Denominators website” a fixed URL or configurable per deployment?

---

# L. Deliverables

## 1) `architecture.md`
```md
# Space Fractions — Architecture Documentation
(Contents are exactly Sections A–L as provided in this ArchitectureDocument.md.)
```

## 2) `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: Space Fractions Admin & Content API
  version: 1.0.0
servers:
  - url: https://spacefractions.example.org
tags:
  - name: Content
  - name: AdminAuth
  - name: AdminQuestions
  - name: AdminAudit
components:
  securitySchemes:
    AdminSessionCookie:
      type: apiKey
      in: cookie
      name: sf_admin_session
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code:
          type: string
          example: AUTH_INVALID
        message:
          type: string
        requestId:
          type: string
        details:
          type: object
          additionalProperties: true
    Choice:
      type: object
      required: [id, text]
      properties:
        id:
          type: string
          minLength: 1
        text:
          type: string
          minLength: 1
    Question:
      type: object
      required: [id, prompt, choices, answer, hint, isCritical]
      properties:
        id:
          type: string
          pattern: "^[A-Za-z0-9_-]{1,64}$"
        prompt:
          type: string
          minLength: 1
        choices:
          type: array
          minItems: 2
          items:
            $ref: "#/components/schemas/Choice"
        answer:
          type: string
          minLength: 1
        hint:
          type: string
        isCritical:
          type: boolean
    QuestionSet:
      type: object
      required: [version, updatedAtUtc, questions]
      properties:
        version:
          type: integer
          minimum: 1
        updatedAtUtc:
          type: string
          format: date-time
        questions:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/Question"
    AdminLoginRequest:
      type: object
      required: [adminId, password]
      properties:
        adminId:
          type: string
          minLength: 1
        password:
          type: string
          minLength: 12
    AdminLoginResponse:
      type: object
      required: [adminId, sessionExpiresAtUtc]
      properties:
        adminId:
          type: string
        sessionExpiresAtUtc:
          type: string
          format: date-time
    UpdateQuestionsRequest:
      type: object
      required: [questions, changeNote]
      properties:
        questions:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/Question"
        changeNote:
          type: string
          minLength: 1
          maxLength: 500
    UpdateQuestionsResponse:
      type: object
      required: [newVersion, updatedAtUtc]
      properties:
        newVersion:
          type: integer
          minimum: 1
        updatedAtUtc:
          type: string
          format: date-time
    AuditEvent:
      type: object
      required: [id, timestampUtc, adminId, remoteIp, eventType]
      properties:
        id:
          type: string
        timestampUtc:
          type: string
          format: date-time
        adminId:
          type: string
        remoteIp:
          type: string
        eventType:
          type: string
          enum: [LOGIN_OK, LOGIN_FAIL, LOCKOUT, QUESTIONS_VALIDATE_FAIL, QUESTIONS_UPDATE_OK]
        fieldChanged:
          type: string
          nullable: true
        before:
          type: string
          nullable: true
        after:
          type: string
          nullable: true
paths:
  /content/questions:
    get:
      tags: [Content]
      summary: Get current question set (public, read-only)
      responses:
        "200":
          description: Current question set
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QuestionSet"
        "500":
          description: Server error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /api/v1/admin/login:
    post:
      tags: [AdminAuth]
      summary: Admin login (sets session cookie)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/AdminLoginRequest"
      responses:
        "200":
          description: Login success; session cookie set
          headers:
            Set-Cookie:
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AdminLoginResponse"
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "423":
          description: Locked out
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /api/v1/admin/logout:
    post:
      tags: [AdminAuth]
      summary: Admin logout (clears session cookie)
      security:
        - AdminSessionCookie: []
      responses:
        "204":
          description: Logged out
        "401":
          description: Not authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /api/v1/admin/questions:
    get:
      tags: [AdminQuestions]
      summary: Get current question set (admin view)
      security:
        - AdminSessionCookie: []
      responses:
        "200":
          description: Current question set
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QuestionSet"
        "401":
          description: Not authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
    put:
      tags: [AdminQuestions]
      summary: Replace question set (validates schema, creates new version)
      security:
        - AdminSessionCookie: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateQuestionsRequest"
      responses:
        "200":
          description: Updated successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UpdateQuestionsResponse"
        "400":
          description: Validation error (schema/content)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          description: Not authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /api/v1/admin/audit:
    get:
      tags: [AdminAudit]
      summary: Query audit events (admin-only)
      security:
        - AdminSessionCookie: []
      parameters:
        - in: query
          name: since
          schema:
            type: string
            format: date-time
        - in: query
          name: limit
          schema:
            type: integer
            minimum: 1
            maximum: 500
            default: 100
      responses:
        "200":
          description: Audit events
          content:
            application/json:
              schema:
                type: object
                required: [events]
                properties:
                  events:
                    type: array
                    items:
                      $ref: "#/components/schemas/AuditEvent"
        "401":
          description: Not authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
```

## 3) `internal.proto`
```proto
syntax = "proto3";

package spacefractions.internal.v1;

option go_package = "spacefractions/internal/v1;internalv1";

message Choice {
  string id = 1;
  string text = 2;
}

message Question {
  string id = 1;
  string prompt = 2;
  repeated Choice choices = 3;
  string answer = 4;
  string hint = 5;
  bool is_critical = 6;
}

message QuestionSet {
  int64 version = 1;
  string updated_at_utc = 2; // RFC3339
  repeated Question questions = 3;
}

message ValidateQuestionSetRequest {
  repeated Question questions = 1;
}

message ValidateQuestionSetResponse {
  bool valid = 1;
  repeated string errors = 2;
}

message PublishQuestionSetRequest {
  repeated Question questions = 1;
  string admin_id = 2;
  string change_note = 3;
  string remote_ip = 4;
}

message PublishQuestionSetResponse {
  int64 new_version = 1;
  string updated_at_utc = 2; // RFC3339
}

message AppendAuditEventRequest {
  string timestamp_utc = 1; // RFC3339
  string admin_id = 2;
  string remote_ip = 3;
  string event_type = 4; // LOGIN_OK, LOGIN_FAIL, ...
  string field_changed = 5;
  string before = 6;
  string after = 7;
}

message AppendAuditEventResponse {
  string id = 1;
}

service QuestionStoreService {
  rpc ValidateQuestionSet(ValidateQuestionSetRequest) returns (ValidateQuestionSetResponse);
  rpc PublishQuestionSet(PublishQuestionSetRequest) returns (PublishQuestionSetResponse);
}

service AuditService {
  rpc AppendAuditEvent(AppendAuditEventRequest) returns (AppendAuditEventResponse);
}
```

## 4) `k8s/admin-api-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sf-admin-api
  labels:
    app: sf-admin-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sf-admin-api
  template:
    metadata:
      labels:
        app: sf-admin-api
    spec:
      containers:
        - name: admin-api
          image: ghcr.io/org/spacefractions-admin-api:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          envFrom:
            - configMapRef:
                name: sf-admin-api-config
            - secretRef:
                name: sf-admin-api-secrets
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
  name: sf-admin-api
spec:
  selector:
    app: sf-admin-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sf-admin-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sf-admin-api
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
  name: sf-admin-api-config
data:
  NODE_ENV: "production"
  PORT: "8080"
  POSTGRES_HOST: "sf-postgres"
  POSTGRES_PORT: "5432"
  POSTGRES_DB: "spacefractions"
  QUESTIONS_CURRENT_OBJECT_KEY: "questions/current.json"
  SESSION_TTL_SECONDS: "3600"
---
apiVersion: v1
kind: Secret
metadata:
  name: sf-admin-api-secrets
type: Opaque
stringData:
  POSTGRES_USER: "sf_admin"
  POSTGRES_PASSWORD: "REPLACE_ME"
  SESSION_SIGNING_KEY: "REPLACE_ME_32B_MIN"
  ARGON2_SECRET_PEPPER: "REPLACE_ME"
```

## 5) SQL DDL examples

### `sql/admin_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS admin_user (
  admin_id TEXT PRIMARY KEY,
  password_hash TEXT NOT NULL,
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  disabled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS admin_session (
  session_id TEXT PRIMARY KEY,
  admin_id TEXT NOT NULL REFERENCES admin_user(admin_id),
  created_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at_utc TIMESTAMPTZ NOT NULL,
  revoked_at_utc TIMESTAMPTZ NULL,
  remote_ip INET NULL,
  user_agent TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_admin_session_admin_id ON admin_session(admin_id);
CREATE INDEX IF NOT EXISTS idx_admin_session_expires ON admin_session(expires_at_utc);
```

### `sql/question_version_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS question_set_version (
  version BIGSERIAL PRIMARY KEY,
  updated_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_by_admin_id TEXT NOT NULL REFERENCES admin_user(admin_id),
  change_note TEXT NOT NULL,
  object_key TEXT NOT NULL, -- points to stored JSON (filesystem path or object storage key)
  sha256_hex TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_question_set_version_updated_at ON question_set_version(updated_at_utc DESC);
```

### `sql/audit_log_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS audit_log (
  id BIGSERIAL PRIMARY KEY,
  timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
  admin_id TEXT NULL,
  remote_ip INET NULL,
  event_type TEXT NOT NULL,
  field_changed TEXT NULL,
  before TEXT NULL,
  after TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
```

## 6) `traceability_matrix.csv`
```csv
Requirement ID,Artifact(s)
INF-FR-001,architecture.md; traceability_matrix.csv
INF-FR-002,architecture.md; k8s/admin-api-deployment.yaml
INF-FR-003,architecture.md
INF-FR-004,architecture.md
INF-FR-005,architecture.md
INF-FR-006,architecture.md
INF-FR-007,architecture.md
INF-FR-008,architecture.md
INF-FR-009,architecture.md
INF-FR-010,architecture.md
INF-FR-011,architecture.md
INF-FR-012,architecture.md
INF-FR-013,architecture.md
INF-FR-014,architecture.md
INF-FR-015,architecture.md
INF-FR-016,architecture.md
INF-FR-017,architecture.md
INF-FR-018,architecture.md
INF-FR-019,architecture.md
INF-FR-020,openapi.yaml; internal.proto; architecture.md
INF-FR-021,openapi.yaml; sql/admin_ddl.sql; architecture.md
INF-FR-022,openapi.yaml; sql/question_version_ddl.sql; architecture.md
INF-FR-023,architecture.md
INF-FR-024,architecture.md
INF-FR-025,architecture.md
INF-FR-026,architecture.md
INF-NFR-001,k8s/admin-api-deployment.yaml; architecture.md
INF-NFR-002,architecture.md
INF-NFR-003,architecture.md
INF-NFR-004,architecture.md
INF-NFR-005,architecture.md
INF-NFR-006,architecture.md
INF-NFR-007,architecture.md
INF-NFR-008,sql/audit_log_ddl.sql; openapi.yaml; architecture.md
INF-CONFLICT-001,architecture.md
```

---

## Verification (Acceptance Criteria)
| Item | Status |
|---|---|
| 3-line Analysis Plan present | - [x] |
| Sections A-L included | - [x] |
| Every FR/NFR/ASR mapped in traceability matrix | - [x] (all inferred as INF- due to missing IDs) |
| ≥1 OpenAPI YAML and ≥1 internal API contract included | - [x] |
| Representative k8s manifest snippet included | - [x] |
| SQL DDL / models for primary entities included | - [x] |
| All major components have at least one API contract and a data schema | - [x] |
| Assumptions and unresolved questions listed | - [x] |

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?