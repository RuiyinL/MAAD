Scope: Design a production-ready web-based “Space Fractions” learning game + admin question updater + math umbrella links, aligned to SRS and 11 UML diagrams.  
Approach: 4+1 architecture with client-heavy gameplay, thin secured admin backend, explicit content schema/contracts, and operability (SLOs, tests, rollout).  
Top validation: (1) full requirement traceability, (2) executable API/contracts + SQL/k8s manifests, (3) NFR verification plan (perf, security, accessibility, compatibility).

# A. Executive Summary (≤1 page)

**System overview**  
Space Fractions is a web-based interactive fraction-learning game for 6th graders with an intro scene, main menu/help, branching storyline-driven multiple-choice questions, immediate feedback (audio/animation), an ending scene with score/rank and replay/quit, plus an administrator “Question Updater” to edit/publish the question bank stored on the server. It also includes an “Umbrella” menu linking to external math learning resources.

**Primary diagram mapping (one line)**  
Scenario and behaviors: *UseCase_SpaceFractions: UC_PlayIntro, UC_StartGame, UC_AnswerQ, UC_Results, UC_AdminLogin, UC_EditQ, UC_PublishQ*; runtime flow: *State_GameSession: IntroPlaying→MainMenu→PresentingQuestion→Results*; deployment: *Deployment_SpaceFractions: Client, WebHost, Email Provider*.

**Architectural styles**  
- **Client-heavy SPA + thin backend for admin/content** (static content delivery, in-browser session state, server-hosted JSON + admin API).  
- **Contract-first interfaces** (OpenAPI for Admin API; internal content contract + schema validation).

**Deployment topology (one line)**  
Browser-based client downloads static assets via HTTPS; gameplay runs locally per-tab; questions.json served with ETag/Cache-Control; Admin API writes questions atomically + audit logs + email notifications (*Deployment_SpaceFractions: Client→WebHost; AdminAPIArtifact→QuestionFileStoreArtifact/AuditLogArtifact/EmailArtifact*).

## Top 3 design risks + mitigations

| Risk | Impact | Mitigation (concrete) | Validation |
|---|---:|---|---|
| Legacy SRS mentions Flash; modern browsers don’t support it | Unshippable | Standards-only HTML5 audio/video/canvas; remove plugin dependency | Cross-browser E2E + accessibility tests |
| Question updates could break gameplay (invalid JSON) | High | Server-side schema validation, atomic write, rollback to last-known-good, ETag versioning | Contract tests + negative tests + rollback drill |
| Classroom network variability affects load time | Medium | Asset budget, compression (brotli/gzip), caching, progressive media loading | Lighthouse CI + synthetic network tests |

## Key QA coverage mapping (ASR/NFR → test types)

| Quality | IDs | Coverage |
|---|---|---|
| Scalability | INF-NFR-ScaleConcurrentUsers | k6 load on static + admin endpoints; CDN cache hit checks |
| Availability | INF-NFR-Uptime, NFR “available over Internet” | Uptime synthetic probes; multi-AZ hosting option |
| Security | NFR-007/ASR-007 | SAST/DAST, authz tests, TLS tests, audit log checks |
| Performance | NFR-009/ASR-008, FR-013/NFR-002 | Lighthouse CI, Web Vitals, perf unit tests for velocity adjustment |
| Maintainability | “Maintainability is primary goal”, ASR-005 | schema validation, modular packages, CI gating, regression suite |

---

# B. Traceability & Rationale

Because the provided SRS text lacks explicit FR/NFR/ASR IDs, this document **infers IDs** with `INF-` prefix per rule. Where UML notes already reference NFR/ASR numbers (e.g., NFR-007/ASR-007), we keep them as **INF-mapped aliases** and list the mapping in Section K.

Below is the required traceability matrix (also delivered as `traceability_matrix.csv` in Section L).

**Traceability table (CSV-formatted)**

Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale
---|---|---|---|---|---
INF-FR-001 | Web-based interactive fraction learning tool | Container_SpaceFractions:WebGameUI,GameCore; Deployment_SpaceFractions:Client,WebHost | WebGameUI, GameCore | architecture.md | Core product scope: browser-delivered interactive game.
INF-FR-002 | Intro movie plays automatically | UseCase_SpaceFractions:UC_PlayIntro; State_GameSession:IntroPlaying | IntroPlayer, Router | architecture.md | Ensures storyline setup before gameplay as described.
INF-FR-003 | User can skip intro anytime | UseCase_SpaceFractions:UC_SkipIntro; State_GameSession:IntroPlaying→MainMenu | IntroPlayer | architecture.md | Matches requirement: click to skip intro.
INF-FR-004 | Main menu with help and links | UseCase_SpaceFractions:UC_MainMenu,UC_Help,UC_External; Class_SpaceFractions:MainMenu | WebGameUI(MainMenu) | architecture.md | Provides entry point, help, external resources.
INF-FR-005 | Help screen explains system play | UseCase_SpaceFractions:UC_Help; Activity_GameplayFlow:Show Help Screen | MainMenu/HelpView | architecture.md | Supports usability for Alice/Bobby/Claire.
INF-FR-006 | Start game from main menu | UseCase_SpaceFractions:UC_StartGame; State_GameSession:MainMenu→LoadingQuestions | GameApp, GameSession | architecture.md | Initiates session and question loading.
INF-FR-007 | Multiple-choice fraction questions | UseCase_SpaceFractions:UC_AnswerQ; Activity_GameplayFlow:Present Question | GameCore, QuestionBank | architecture.md | Primary learning interaction.
INF-FR-008 | Questions cover arithmetic/equivalence/graph/improper | Class_SpaceFractions:SkillType | Question schema/content | openapi.yaml, sql/question_bank_ddl.sql | Encoded as `skill` enum to ensure coverage.
INF-FR-009 | Friendly robotic sidekick gives hints | UseCase_SpaceFractions:UC_Hint; Class_SpaceFractions:HintBot | HintBot | architecture.md | Implements hinting/usability aid.
INF-FR-010 | Immediate feedback with sounds/animations for right/wrong | Class_SpaceFractions:FeedbackEngine | MediaEngine, FeedbackEngine | architecture.md | Reinforces learning; mapped to HTML5 media.
INF-FR-011 | Ending scene shows score + customized message | UseCase_SpaceFractions:UC_Results; ResultsView | ResultsView, StoryEngine | architecture.md | Provides closure and feedback.
INF-FR-012 | Option to replay or quit after results | UseCase_SpaceFractions:UC_Replay; State_GameSession:Results→MainMenu/Quit | Router, GameSession | architecture.md | Supports repeat practice.
INF-FR-013 | Branching storyline based on critical questions | Class_SpaceFractions:StoryEngine,Question.isCritical | StoryEngine | architecture.md | Implements dynamic/adaptive narrative.
INF-FR-014 | Wrong answer allows retry but no points | State_GameSession:FeedbackWrong→PresentingQuestion; Class:GameSession.noPointsOnRetry | GameSession | architecture.md | Matches retry/no credit requirement.
INF-FR-015 | Validate fraction input ints and denom≠0; adjust velocity in real time | Class:FractionValidator,VelocityAdjuster,PhysicsEngine | GameCore(Gameplay) | architecture.md | Ensures safe physics update and responsive gameplay.
INF-FR-016 | Admin can update questions via web tool | UseCase:UC_EditQ,UC_PublishQ; Sequence2_Admin_UpdateQuestions | AdminWebUI, AdminAPI | openapi.yaml | Enables teacher/admin content maintenance.
INF-FR-017 | Admin login with password | UseCase:UC_AdminLogin; Class:AdminAuthService | AdminAPI | openapi.yaml, sql/admin_auth_ddl.sql | Protects updater access.
INF-FR-018 | Persist updated questions on web server file; easily edited via screens | Sequence2:QuestionFileStore writeAtomically; Component:QuestionFileStore | QuestionFileStore, AdminWebUI | sql/question_bank_ddl.sql (metadata), architecture.md | File-based storage + UI forms match SRS.
INF-FR-019 | Game uses local-only score (per instance) | Class:GameSession<<session>>; Container:GameCore note | GameSession | architecture.md | Prevents cross-user data persistence; aligns “single instance single user”.
INF-FR-020 | Math Umbrella provides links to external S2S projects | UseCase:UC_External; Container:ExternalLinks | WebGameUI | architecture.md | Adds umbrella navigation to external resources.
INF-NFR-001 | Browser compatibility (modern) and no plugins | Class note:IntroPlayer; Package/UI notes | WebGameUI, MediaEngine | architecture.md | Replace Flash; ensure maintainability/availability.
INF-NFR-002 | Input-to-velocity update latency p95 ≤150ms (Chromebook 2015+) | Class note:VelocityAdjuster | VelocityAdjuster, PhysicsEngine | architecture.md | Keeps gameplay responsive.
INF-NFR-003 | Behavior invariant across environments | Deployment note:browser matrix; UI note | GameCore separation | architecture.md | Central logic separation + regression tests.
INF-NFR-004 | First interactive <3s; bundle ≤2.5MB compressed | Activity_GameplayFlow note | WebGameUI build | architecture.md, k8s/web-deployment.yaml | Ensures usability on school networks.
INF-NFR-005 | Accessibility: ARIA-live feedback; WAVE ≥98% | FeedbackEngine note; Container note | WebGameUI | architecture.md | Supports inclusive classroom use.
INF-NFR-006 | Usability: reach first question <2 minutes | Package/UI note | WebGameUI | architecture.md | Meets persona needs (Alice/Bobby).
INF-NFR-007/ASR-007 | Admin security: HTTPS-only, bcrypt, lockout, session timeout, audit | Class note:AdminAuthService; Sequence2 | AdminAPI, AuditLog | openapi.yaml, sql/audit_log_ddl.sql | Explicit and testable security controls.
INF-ASR-004 | Server-hosted persistence for question bank | Deployment:QuestionFileStoreArtifact | QuestionFileStore | architecture.md | Supports admin updates and hosting constraints.
INF-ASR-005 | ETag/TTL reload ≤60s, schemaVersion, rollback on invalid update | Class note:QuestionBank; State note:LoadingQuestions | QuestionBank, ContentClient | architecture.md | Ensures dynamic updates with safety.
INF-ASR-006 | Single-user per running instance; score cleared on tab close | Object note:GameSession | GameSession | architecture.md | Prevents multi-user mixing within one instance.
INF-NFR-008 | Reliability ensured by extensive testing | SRS statement | CI/CD + test suite | architecture.md | Operationalizes “extensive testing”.
INF-NFR-009 | Available over Internet via website | Deployment:WebHost | Hosting | architecture.md | Defines internet availability.
INF-NFR-010 | No new hardware required | SRS statement | Web-only | architecture.md | Browser-only reduces hardware dependency.
INF-NFR-011 | Maintainability primary goal | SRS statement | Modular packages + schema/contracts | architecture.md | Drives structure and validation.

---

# C. Architecture Overview

**Context view (users + external systems)**  
- Actors: EndUser (students), Administrator (teacher/admin), EmailService for password reset/alerts (*UseCase_SpaceFractions: EndUser, Administrator, EmailService*).
- External links open in new tab/window (*UseCase_SpaceFractions: UC_External note*).

**Container view (runtime executables)**  
- Client (Browser): WebGameUI + GameCore running in-browser; score/session state stays in-memory (*Container_SpaceFractions: WebGameUI, GameCore*).  
- Server: StaticContent, QuestionFileStore (questions.json), AdminAPI, AuditLogStore (*Container_SpaceFractions: Server*).  
- External: EmailService; ExternalLinks (*Container_SpaceFractions: External*).

**Component/Package view (code organization)**  
- UI package: GameApp/Router/IntroPlayer/MainMenu/ResultsView (*Package_SpaceFractions: ui*).  
- Domain: Question, GameSession, attempts, SkillType (*Package_SpaceFractions: domain*).  
- Gameplay services: StoryEngine, HintBot, FeedbackEngine, VelocityAdjuster (*Package_SpaceFractions: gameplay*).  
- Content: QuestionBank + client with ETag/TTL (*Package_SpaceFractions: content*).  
- Admin: AdminAuthService + QuestionBankUpdater (*Package_SpaceFractions: admin*).  
- Infra: QuestionFileStore, AuditLog, Email adapter (*Package_SpaceFractions: infrastructure*).

**Class/Runtime view (key objects and flow)**  
- GameSession tracks score, question index, retry/no-points state, and branchKey (*Class_SpaceFractions:GameSession; State_GameSession*).  
- QuestionBank caches question set with schemaVersion + ETag and reloadIfStale(TTL≤60s) (*Class_SpaceFractions:QuestionBank*).  
- AdminAuthService enforces secure login and audit (*Class_SpaceFractions:AdminAuthService*).

**Deployment view**  
- HTTPS Web host serves static assets + JSON + Admin API; email provider used for reset/alerts (*Deployment_SpaceFractions: WebHost, Email Provider*).  
- Browser matrix testing ensures environment invariance (*Deployment_SpaceFractions note*).

---

# D. Detailed Technical Design (developer-facing)

## D1. Subsystem: WebGameUI (Intro/Menu/Gameplay/Results)

### 1) Responsibilities & data ownership  
Renders intro video, main menu/help, gameplay UI for questions, feedback animations/sounds, and results screen. Owns **UI state** only; authoritative gameplay state is in `GameCore` (in-browser). Does not persist student PII; stores session score in memory per tab (cleared on close) (INF-ASR-006).

### 2) Technology options (≥3 per concern)

**Language/runtime**
- Recommended: **TypeScript 5.4+** in browser (ES2020 target) — strong typing for maintainability.  
  Justification: meets INF-NFR-011 (maintainability primary goal).
- Conservative: JavaScript ES2020 (no TS build step).  
  Justification: meets INF-NFR-010 (no new hardware; simplest runtime).
- Cutting-edge: WASM (Rust) for core gameplay loops.  
  Justification: helps INF-NFR-002 (latency), but higher complexity.

**Web framework**
- Recommended: **React 18.2 + Vite 5** (SPA)  
  Justification: meets INF-NFR-004 (first interactive <3s) via fast bundling/code-splitting.
- Conservative: Vanilla JS + Web Components (Lit 3).  
  Justification: meets INF-NFR-004 by minimizing bundle.
- Cutting-edge: SolidJS/SvelteKit (client-only build).  
  Justification: meets INF-NFR-004 but adds new stack variance.

**RPC/HTTP**
- Recommended: `fetch()` + OpenAPI-generated client for Admin flows (admin only).  
  Justification: meets INF-NFR-003 (behavior invariant) with standard browser APIs.
- Conservative: Axios.  
- Cutting-edge: GraphQL client (urql/apollo) (overkill for this scope).

**Persistence (client)**
- Recommended: **In-memory only** (no LocalStorage) for score/session.  
  Justification: meets INF-FR-019 + INF-ASR-006 (local-only, cleared on close).
- Conservative: sessionStorage (still per-tab) if reload resilience needed.  
- Cutting-edge: IndexedDB for offline mode (not required).

**Cache**
- Recommended: HTTP cache + in-app QuestionBank TTL 60s.  
  Justification: meets INF-ASR-005 (ETag/TTL refresh).
- Conservative: no app caching (always fetch).  
- Cutting-edge: service worker (PWA) for offline caching.

**Messaging**
- Recommended: none (not needed).  
- Conservative: none.  
- Cutting-edge: WebSocket for push invalidation (not required by SRS).

**Search**
- Not applicable.

**Authn/Authz**
- Recommended: no end-user auth; admin auth handled by AdminAPI.  
  Justification: meets INF-FR-017 (admin login) without student accounts.

**Observability**
- Recommended: Web Vitals + client error reporting (Sentry).  
  Justification: meets INF-NFR-008 (extensive testing/quality via telemetry).
- Conservative: console + server logs only.  
- Cutting-edge: OpenTelemetry in browser.

**CI/CD**
- Recommended: GitHub Actions + Lighthouse CI + Playwright.  
  Justification: meets INF-NFR-003 (invariance across environments).
- Conservative: manual testing only (not acceptable given NFRs).  
- Cutting-edge: full OTel + performance budgets gate.

**Container runtime / infra provisioning**
- UI is static; containerization optional.  
- Recommended: served via NGINX container on k8s.  
  Justification: meets INF-NFR-009 (internet availability) with scalable hosting.

### 3) Recommended default stack (versions)  
- TypeScript **5.4–5.6**, React **18.2**, Vite **5.x**, Playwright **1.44+**, Web Audio API + HTML5 `<video>` (MP4/WebM).  
Justification: meets INF-NFR-001 (no plugins, modern browsers) and INF-NFR-011 (maintainability).

### 4) Interface design  
- Uses **AdminAPI** (OpenAPI in `openapi.yaml`) only for admin pages.  
- Fetches `questions.json` from `QuestionFileStore` (internal content contract in `internal.proto` below).

### 5) Data model / schema  
No server persistence for end-user gameplay. Client uses runtime objects (`GameSession`, `AnswerAttempt`) only.

### 6) Caching & consistency  
- Cache static assets with long max-age + content hashing.  
- Cache `questions.json` with `Cache-Control: max-age=60` and `ETag`; `QuestionBank.loadIfStale(TTL=60s)` (INF-ASR-005).  
- Consistency: **eventual ≤60s** for question propagation (acceptable per ASR-005).

---

## D2. Subsystem: Content Delivery (QuestionFileStore + ContentClient)

### 1) Responsibilities & data ownership  
Stores the canonical `questions.json` plus `last-good` backup. Serves it via HTTPS GET with ETag. Owns question bank **content contract** and schema versioning.

### 2) Technology options

**Language/runtime**
- Recommended: Node.js **18–20** for AdminAPI + file IO.  
  Justification: meets INF-ASR-004 (server-hosted persistence) with simple ops.
- Conservative: Python **3.11–3.12** (FastAPI) + filesystem.  
  Justification: meets INF-ASR-004.
- Cutting-edge: Go **1.22** (high performance, simple deploy).  
  Justification: helps INF-NFR-009 (availability) with low resource usage.

**Web framework (admin API serving)**
- Recommended: Express **4.19** or Fastify **4.x** (Node).  
  Justification: meets INF-NFR-011 (maintainability).
- Conservative: Flask/FastAPI.  
- Cutting-edge: Bun (not mature enough for schools/ops).

**Persistence**
- Recommended: **Atomic filesystem writes** on server + checksum; optional object storage later.  
  Justification: meets INF-FR-018 (file on web server) and INF-ASR-005 (rollback).
- Conservative: SQLite **3.42+** storing JSON blob, exporting to file.  
- Cutting-edge: S3 + versioning (conflicts with “file on server” wording; can be future).

**Cache**
- Recommended: ETag + `max-age=60`.  
  Justification: meets INF-ASR-005.
- Conservative: disable caching.  
- Cutting-edge: CDN with stale-while-revalidate.

**Observability**
- Recommended: access logs + ETag/version metrics.  
  Justification: meets INF-NFR-008 (testability/reliability).

### 3) Recommended default stack  
- Node.js **18–20**, Fastify **4.x**, filesystem atomic write (write temp + fsync + rename), ETag on GET.  
Justification: meets INF-FR-018 and INF-ASR-005.

### 4) Interface design  
- Served as static file `GET /content/questions.json` and `GET /content/manifest.json` (defined in internal contract `internal.proto`).

### 5) Data model / schema  
Primary persisted “entity” is the question bank JSON file plus audit logs (see SQL section for audit/admin). We still provide SQL DDL for **metadata** and audit as requested.

### 6) Caching & consistency  
- Strong consistency on server (single writer via AdminAPI).  
- Eventual to clients (≤60s TTL).

---

## D3. Subsystem: AdminAPI + AdminWebUI (Question Updater)

### 1) Responsibilities & data ownership  
AdminWebUI provides forms to edit questions and publish. AdminAPI authenticates admins, validates payload against schema, writes `questions.json` atomically, appends audit log entries, and triggers email notifications on password reset or rejected publish.

### 2) Technology options

**Language/runtime**
- Recommended: Node.js **18–20**  
  Justification: meets INF-NFR-011 (maintainability).
- Conservative: Java **17–21** (Spring Boot).  
  Justification: meets INF-NFR-007/ASR-007 (security libraries mature).
- Cutting-edge: Go **1.22**.

**Web framework**
- Recommended: Fastify **4.x** + `@fastify/jwt` (or sessions)  
  Justification: meets INF-NFR-007/ASR-007 (secure auth patterns).
- Conservative: Express **4.19**.  
- Cutting-edge: NestJS **10.x** (more structure, more overhead).

**RPC/HTTP**
- Recommended: REST JSON per OpenAPI.  
  Justification: meets INF-NFR-003 (invariant behavior) via widely supported HTTP.

**Persistence**
- Recommended: PostgreSQL **14–15** for admin accounts + audit logs; filesystem for question bank file.  
  Justification: meets INF-NFR-007/ASR-007 (audit trail) and INF-FR-018 (file persistence).
- Conservative: SQLite for admin/audit.  
- Cutting-edge: managed auth (Auth0) (likely not acceptable for school deployment constraints).

**Authn/Authz**
- Recommended: Session cookies (HttpOnly, Secure, SameSite=Strict) for admin; RBAC “admin” role only.  
  Justification: meets INF-NFR-007/ASR-007 (secure sessions + timeout).
- Conservative: Basic auth over HTTPS (avoid; weak UX/security).  
- Cutting-edge: OIDC (nice, but extra dependency).

**Observability**
- Recommended: structured logs + audit DB; Prometheus metrics.  
  Justification: meets INF-NFR-008 (reliability by test/monitor).

**CI/CD**
- Recommended: contract tests validating OpenAPI + schema validation tests.  
  Justification: meets INF-ASR-005 (reject invalid updates + rollback).

**Container runtime / infra provisioning**
- Recommended: Docker + Kubernetes.  
  Justification: meets INF-NFR-009 (internet availability) with scalable deployment.

### 3) Recommended default stack  
- AdminWebUI: same SPA stack as WebGameUI (React/TS).  
- AdminAPI: Node.js **18–20** + Fastify **4.x**, PostgreSQL **14–15**, bcrypt **5.x**, SES/SendGrid email adapter.  
Justification: meets INF-NFR-007/ASR-007 (bcrypt, lockout, timeout, audit) and INF-FR-016/017 (admin updater + login).

### 4) Interface design (external APIs)  
See `openapi.yaml` in Section L (Admin API surface, 8 endpoints).

### 5) Data model / schema (SQL DDL)  
See SQL files in Section L: `sql/admin_auth_ddl.sql`, `sql/audit_log_ddl.sql`.

Fields requiring special handling:
- `admin_users.password_hash`: **bcrypt hash** (never reversible). Justification: meets INF-NFR-007/ASR-007.
- `audit_log.details`: may contain sensitive info; encrypt-at-rest recommended at storage layer. Justification: meets INF-NFR-007/ASR-007.

### 6) Caching & consistency  
- No caching for admin write endpoints.  
- GET `/content/questions.json` cached as per ASR-005.

---

## D4. Internal contracts (content fetch & validation)

We define an internal gRPC contract for **logical** interactions (even if implemented as HTTP). This provides a stable typed contract for dev/test.

---

# E. Operations & Deployment (ops-facing)

## E1. Kubernetes-ready plan (representative manifest)

- One sample manifest provided in Section L: `k8s/adminapi-deployment.yaml` including Deployment/Service/HPA/ConfigMap/Secret.

Sizing tiers (suggested):
- Small (single class): 1 replica AdminAPI, 1 replica static, Postgres single instance.
- Medium (school district): 2–3 replicas AdminAPI, CDN for static, Postgres HA.
- Large: 3–5 replicas AdminAPI, Postgres HA + read replica, object storage migration optional.

## E2. DB HA topology, backups, restore notes
- PostgreSQL 14–15:
  - Small: single instance + daily logical dump.
  - Medium/Large: primary+standby (streaming replication), automated failover (Patroni or managed service).
- Backups:
  - Daily full + WAL archiving (if HA) for PITR.
  - Restore drill monthly (verify audit continuity and admin logins).
- RPO/RTO targets (also in SRE section): RPO 24h small / 1h medium+; RTO 4h small / 30m medium+.

## E3. Network topology + ingress/egress rules and latency expectations
Mapped to *Deployment_SpaceFractions: Client→WebHost (HTTPS)*:
- Ingress: `443/TCP` only; redirect `80→443`.  
- Egress from AdminAPI: email provider API/SMTP only.  
- Latency expectations:
  - `GET /content/questions.json` p95 < 300ms on broadband; gameplay logic local so unaffected.
  - Velocity adjust p95 <150ms device-local (INF-NFR-002).

## E4. CI/CD sketch
1. Lint/typecheck (TS), unit tests.
2. Contract validation: OpenAPI lint + schema validation tests.
3. E2E Playwright against browser matrix.
4. Lighthouse CI budgets.
5. Build Docker images; scan (Trivy).
6. Deploy to staging; smoke tests.
7. Canary/blue-green for AdminAPI; static assets via hashed filenames.

---

# F. Security Design

## F1. Auth & AuthZ
- Admin auth only.
- **Session cookie** auth (recommended):
  - Login issues server session with expiry 15 min inactivity; absolute max 8h.
  - Lockout after 5 failed attempts for 10 min.
  - Password reset via one-time token emailed; token TTL 15 min.
Justification: meets INF-NFR-007/ASR-007.

## F2. Secrets management & rotation
- Kubernetes Secrets for DB creds, email API key, session signing key.
- Rotate quarterly or on incident; session key rotation invalidates sessions.
Justification: meets INF-NFR-007/ASR-007.

## F3. TLS & service-mesh considerations
- TLS1.2+ enforced at ingress; HSTS enabled.
- Service mesh optional; not required for small deployment.
Justification: meets INF-NFR-007/ASR-007.

## F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Brute force admin login | lockout + rate limit + audit (INF-NFR-007/ASR-007) |
| Question bank tampering | server-side validation + atomic write + rollback + audit (INF-ASR-005, INF-NFR-007/ASR-007) |
| XSS via question text | sanitize HTML, store as plain text, CSP headers |
| Session hijack | Secure/HttpOnly/SameSite cookies, TLS-only |
| Supply-chain compromise | pinned deps, SCA scanning, signed images |

---

# G. Observability & SRE

## G1. Metrics/logs/traces + sample alerts
Metrics:
- AdminAPI: login_success_total, login_fail_total, lockout_total, publish_success_total, publish_reject_total.
- Content: questions_etag_current, questions_schema_version, content_fetch_304_rate.
- Client: Web Vitals (LCP, INP), JS errors.

Logs:
- Structured JSON logs; audit events persisted to DB (append-only).

Example Prometheus alert rules:
- High publish failures
- Elevated admin login failures

(Provided as examples here; implement in monitoring stack.)

## G2. SLOs, error budgets, RTO/RPO
- Availability SLO (AdminAPI): 99.5% monthly (INF-NFR-Uptime).
- Content freshness: updates visible to clients within 60s (INF-ASR-005).
- RTO/RPO: see E2.

## G3. Dashboards/runbooks
- Dashboard: publish status, last ETag, recent rejects, login failures/lockouts.
- Runbooks:
  - “Publish rejected due to schema” (fix fields, republish).
  - “Rollback triggered” (inspect last-good, audit trail, notify teacher).
  - “Email provider down” (manual reset path).

---

# H. Testing Strategy

## H1. Test matrix
| Test type | Components | Examples |
|---|---|---|
| Unit | GameCore, StoryEngine, VelocityAdjuster, schema validator | branching, retry no-points, denom!=0 |
| Integration | AdminAPI + Postgres + filesystem | publish writes file + audit row |
| Contract | OpenAPI + JSON schema | negative cases reject + rollback |
| E2E | WebGameUI in browsers | skip intro, complete game, replay |
| Chaos (light) | AdminAPI | kill pod during publish → atomicity preserved |

## H2. Test data management & environments
- Environments: dev, staging, prod.
- Staging refresh: nightly reset DB; questions.json seeded.
- Isolation: separate namespaces; separate DB instances.

---

# I. Migration, Data Conversion & Rollout Plan

## I1. Migration steps
If replacing Flash legacy:
1. Extract existing questions into new JSON schema (backfill).
2. Validate schema; publish as questions.json v1.
3. Parallel run old/new for a class week; collect teacher feedback.
4. Cutover: link umbrella/menu to new HTML5 app.
Rollback: restore last-good questions.json; redeploy static assets previous build.

## I2. Backwards compatibility notes
- Version questions schema with `schemaVersion` and require clients to support current major.
- API versioning: prefix `/v1/admin/...` and bump on breaking changes.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| Client-heavy gameplay | Server-authoritative game; hybrid | Server adds complexity + latency; client-only aligns single-user instance | Meets INF-ASR-006 and responsiveness INF-NFR-002 |
| File-based questions store | DB-only; object storage | File matches SRS; DB improves concurrency | Meets INF-FR-018 “saved in a file” |
| Session cookies for admin | JWT; OIDC | JWT revocation harder; OIDC adds dependency | Meets INF-NFR-007/ASR-007 with simpler ops |
| TTL 60s caching | push invalidation | TTL is simpler; push is more complex | Meets INF-ASR-005 requirement directly |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1**: Modern browsers are targeted (latest 2 versions of Chrome/Firefox/Edge/Safari); Flash is not supported.  
- **A2**: “Administrator” is a small set of teacher accounts; no student authentication is required.  
- **A3**: Question bank size is ≤500 questions; file remains <2MB JSON.  
- **A4**: “Ranked” score means local rank message (e.g., Bronze/Silver/Gold), not global leaderboard.  
- **A5**: External links (Denominators/Umbrella) are curated static URLs configured in a config file.

## Conflicts logged (requirements vs diagrams)
- Flash required in SRS vs HTML5 in diagrams: we follow SRS naming (“movie/animations”) but implement with HTML5; conflict recorded under A1.

## Unresolved stakeholder questions
1. Should students’ scores ever be persisted for teacher review (beyond local per session)?  
2. How many branching endings are required (2/3/5+), and are endings media-heavy?  
3. Password reset: is email available for all admins, or should there be an offline reset flow?  
4. Are questions strictly multiple-choice, or do some require numerator/denominator entry (velocity feature suggests numeric input)?

## Inferred ID mapping note
- The UML references NFR-007/ASR-007 etc. Since SRS has no IDs, we treat them as **INF-** requirements but keep the labels for readability (see traceability).

---

# L. Deliverables

```markdown
<!-- filename: architecture.md -->
# ArchitectureDocument.md

(This document’s full content is the ArchitectureDocument.md. For conversion: `pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf`.)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Space Fractions Admin API
  version: "1.0.0"
  description: >
    Admin API for authenticating administrators and publishing the QuestionBank.
    Public gameplay has no authenticated API; questions are served as static content.
servers:
  - url: https://spacefractions.example.org
paths:
  /v1/admin/auth/login:
    post:
      summary: Admin login
      operationId: adminLogin
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginRequest"
      responses:
        "204":
          description: Logged in; session cookie set
          headers:
            Set-Cookie:
              schema:
                type: string
        "400":
          description: Invalid request
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "423":
          description: Locked out
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/auth/logout:
    post:
      summary: Admin logout
      operationId: adminLogout
      security:
        - cookieAuth: []
      responses:
        "204":
          description: Logged out; session cleared
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/auth/password-reset/request:
    post:
      summary: Request password reset email
      operationId: requestPasswordReset
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/PasswordResetRequest" }
      responses:
        "202":
          description: Accepted (always 202 to avoid account enumeration)
        "400":
          description: Invalid request
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/auth/password-reset/confirm:
    post:
      summary: Confirm password reset with token
      operationId: confirmPasswordReset
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/PasswordResetConfirm" }
      responses:
        "204":
          description: Password updated
        "400":
          description: Invalid request/token
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/questions:
    get:
      summary: Get current published question bank metadata
      operationId: getQuestionBankMeta
      security:
        - cookieAuth: []
      responses:
        "200":
          description: Current bank metadata
          content:
            application/json:
              schema: { $ref: "#/components/schemas/QuestionBankMeta" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/questions/validate:
    post:
      summary: Validate a question bank draft (no publish)
      operationId: validateQuestionBank
      security:
        - cookieAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/QuestionBank" }
      responses:
        "200":
          description: Validation result
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ValidationResult" }
        "400":
          description: Invalid JSON
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/questions/publish:
    post:
      summary: Publish a validated question bank (atomic write + rollback on failure)
      operationId: publishQuestionBank
      security:
        - cookieAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/QuestionBank" }
      responses:
        "200":
          description: Published successfully
          content:
            application/json:
              schema: { $ref: "#/components/schemas/PublishResponse" }
        "409":
          description: Rejected due to schema or validation errors; rollback executed
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ValidationResult" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /v1/admin/audit:
    get:
      summary: List recent audit events
      operationId: listAuditEvents
      security:
        - cookieAuth: []
      parameters:
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 200, default: 50 }
      responses:
        "200":
          description: Audit events
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/AuditEvent" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

components:
  securitySchemes:
    cookieAuth:
      type: apiKey
      in: cookie
      name: sf_admin_session

  schemas:
    ErrorResponse:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code: { type: string, example: "AUTH_INVALID" }
            message: { type: string, example: "Invalid credentials" }
            details:
              type: object
              additionalProperties: true

    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1, maxLength: 64 }
        password: { type: string, minLength: 1, maxLength: 256 }

    PasswordResetRequest:
      type: object
      required: [email]
      properties:
        email:
          type: string
          format: email
          maxLength: 254

    PasswordResetConfirm:
      type: object
      required: [token, newPassword]
      properties:
        token: { type: string, minLength: 20, maxLength: 400 }
        newPassword: { type: string, minLength: 12, maxLength: 256 }

    SkillType:
      type: string
      enum: [arithmetic, equivalence, graph, improper]

    Question:
      type: object
      required: [id, prompt, choices, answerIndex, skill, isCritical]
      properties:
        id: { type: string, minLength: 1, maxLength: 64 }
        prompt: { type: string, minLength: 1, maxLength: 2000 }
        choices:
          type: array
          minItems: 2
          maxItems: 8
          items: { type: string, minLength: 1, maxLength: 200 }
        answerIndex:
          type: integer
          minimum: 0
        skill: { $ref: "#/components/schemas/SkillType" }
        isCritical: { type: boolean }
        branchOnCorrect: { type: string, nullable: true, maxLength: 64 }
        branchOnWrong: { type: string, nullable: true, maxLength: 64 }
        metadata:
          type: object
          additionalProperties:
            type: string
            maxLength: 200

    QuestionBank:
      type: object
      required: [schemaVersion, questions]
      properties:
        schemaVersion:
          type: string
          pattern: "^[0-9]+\\.[0-9]+$"
          example: "1.0"
        questions:
          type: array
          minItems: 1
          maxItems: 500
          items: { $ref: "#/components/schemas/Question" }

    QuestionBankMeta:
      type: object
      required: [schemaVersion, etag, lastPublishedUtc]
      properties:
        schemaVersion: { type: string, example: "1.0" }
        etag: { type: string, example: "W/\"a1b2c3\"" }
        lastPublishedUtc: { type: string, format: date-time }

    ValidationResult:
      type: object
      required: [valid, errors]
      properties:
        valid: { type: boolean }
        errors:
          type: array
          items:
            type: object
            required: [path, message]
            properties:
              path: { type: string, example: "questions[0].choices" }
              message: { type: string, example: "must have at least 2 choices" }

    PublishResponse:
      type: object
      required: [etag, schemaVersion, lastPublishedUtc]
      properties:
        etag: { type: string }
        schemaVersion: { type: string }
        lastPublishedUtc: { type: string, format: date-time }

    AuditEvent:
      type: object
      required: [id, eventType, occurredUtc, adminId, sourceIp]
      properties:
        id: { type: integer, format: int64 }
        eventType: { type: string, example: "PublishSuccess" }
        occurredUtc: { type: string, format: date-time }
        adminId: { type: string, example: "admin-123" }
        sourceIp: { type: string, example: "203.0.113.10" }
        details:
          type: object
          additionalProperties: true
```

```proto
// filename: internal.proto
syntax = "proto3";

package spacefractions.internal.v1;

// Logical internal contract for content retrieval + validation.
// Implementation may be HTTP static files; this contract is used for typed tests.

message Manifest {
  string schema_version = 1;  // e.g., "1.0"
  string etag = 2;            // strong/weak etag
  string last_sync_utc = 3;   // RFC3339
}

enum SkillType {
  SKILL_UNSPECIFIED = 0;
  ARITHMETIC = 1;
  EQUIVALENCE = 2;
  GRAPH = 3;
  IMPROPER = 4;
}

message Question {
  string id = 1;
  string prompt = 2;
  repeated string choices = 3;
  uint32 answer_index = 4;
  SkillType skill = 5;
  bool is_critical = 6;
  string branch_on_correct = 7;
  string branch_on_wrong = 8;
  map<string,string> metadata = 9;
}

message QuestionBank {
  string schema_version = 1;
  repeated Question questions = 2;
}

message ValidationError {
  string path = 1;
  string message = 2;
}

message ValidationResult {
  bool valid = 1;
  repeated ValidationError errors = 2;
}

service ContentService {
  rpc GetManifest(Empty) returns (Manifest);
  rpc GetQuestionBank(IfNoneMatch) returns (QuestionBank);
  rpc ValidateQuestionBank(QuestionBank) returns (ValidationResult);
}

message Empty {}

message IfNoneMatch {
  string etag = 1; // client etag; server may respond with unchanged bank in HTTP form (304)
}
```

```yaml
# filename: k8s/adminapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sf-adminapi
  labels:
    app: sf-adminapi
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sf-adminapi
  template:
    metadata:
      labels:
        app: sf-adminapi
    spec:
      containers:
        - name: adminapi
          image: spacefractions/adminapi:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: sf-secrets
                  key: databaseUrl
            - name: SESSION_SIGNING_KEY
              valueFrom:
                secretKeyRef:
                  name: sf-secrets
                  key: sessionSigningKey
            - name: EMAIL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: sf-secrets
                  key: emailApiKey
          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
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
            initialDelaySeconds: 15
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: sf-adminapi-svc
spec:
  selector:
    app: sf-adminapi
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sf-adminapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sf-adminapi
  minReplicas: 2
  maxReplicas: 5
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
  name: sf-config
data:
  QUESTIONS_PATH: "/data/questions.json"
  QUESTIONS_LAST_GOOD_PATH: "/data/questions.lastgood.json"
  CACHE_TTL_SECONDS: "60"
---
apiVersion: v1
kind: Secret
metadata:
  name: sf-secrets
type: Opaque
stringData:
  databaseUrl: "postgresql://sf_admin:REPLACE_ME@sf-postgres:5432/spacefractions"
  sessionSigningKey: "REPLACE_WITH_32+_BYTES_RANDOM"
  emailApiKey: "REPLACE_ME"
```

```sql
-- filename: sql/admin_auth_ddl.sql
CREATE TABLE IF NOT EXISTS admin_users (
  admin_id            TEXT PRIMARY KEY,
  username            TEXT NOT NULL UNIQUE,
  email               TEXT NOT NULL UNIQUE,
  password_hash       TEXT NOT NULL, -- bcrypt hash; never reversible (INF-NFR-007/ASR-007)
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
  failed_login_count  INTEGER NOT NULL DEFAULT 0,
  locked_until_utc    TIMESTAMPTZ NULL,
  created_utc         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_utc         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_admin_users_locked_until
ON admin_users (locked_until_utc);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
  token_id        BIGSERIAL PRIMARY KEY,
  admin_id        TEXT NOT NULL REFERENCES admin_users(admin_id) ON DELETE CASCADE,
  token_hash      TEXT NOT NULL, -- store hash of token
  expires_utc     TIMESTAMPTZ NOT NULL,
  used_utc        TIMESTAMPTZ NULL,
  created_utc     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_admin_expires
ON password_reset_tokens (admin_id, expires_utc);
```

```sql
-- filename: sql/audit_log_ddl.sql
CREATE TABLE IF NOT EXISTS audit_log (
  id              BIGSERIAL PRIMARY KEY,
  event_type      TEXT NOT NULL,
  occurred_utc    TIMESTAMPTZ NOT NULL DEFAULT now(),
  admin_id        TEXT NULL,
  source_ip       INET NOT NULL,
  details         JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Append-only enforcement is typically via application logic + RBAC;
-- optionally add a DB trigger to block UPDATE/DELETE in production roles.
CREATE INDEX IF NOT EXISTS idx_audit_log_occurred
ON audit_log (occurred_utc DESC);

CREATE INDEX IF NOT EXISTS idx_audit_log_event_type
ON audit_log (event_type);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,Web-based interactive fraction learning tool,"Container_SpaceFractions:WebGameUI,GameCore; Deployment_SpaceFractions:Client,WebHost","WebGameUI,GameCore",architecture.md,"Browser-delivered interactive game."
INF-FR-002,Intro movie plays automatically,"UseCase_SpaceFractions:UC_PlayIntro; State_GameSession:IntroPlaying","IntroPlayer,Router",architecture.md,"Implements storyline intro."
INF-FR-003,User can skip intro anytime,"UseCase_SpaceFractions:UC_SkipIntro; State_GameSession:IntroPlaying->MainMenu","IntroPlayer",architecture.md,"Skip behavior on click."
INF-FR-004,Main menu with help and links,"UseCase_SpaceFractions:UC_MainMenu,UC_Help,UC_External","MainMenu",architecture.md,"Entry navigation and resources."
INF-FR-005,Help screen explains system play,"UseCase_SpaceFractions:UC_Help; Activity_GameplayFlow:Show Help Screen","HelpView",architecture.md,"Persona-friendly instructions."
INF-FR-006,Start game from main menu,"UseCase_SpaceFractions:UC_StartGame; State_GameSession:MainMenu->LoadingQuestions","GameSession,QuestionBank",architecture.md,"Starts session and loads content."
INF-FR-007,Multiple-choice fraction questions,"UseCase_SpaceFractions:UC_AnswerQ","GameCore,QuestionBank",architecture.md,"Core gameplay interaction."
INF-FR-008,Question skills: arithmetic/equivalence/graph/improper,"Class_SpaceFractions:SkillType","Question schema",openapi.yaml,"Encodes skills in schema."
INF-FR-009,Hint sidekick,"UseCase_SpaceFractions:UC_Hint; Class_SpaceFractions:HintBot","HintBot",architecture.md,"Hint generation."
INF-FR-010,Right/wrong feedback sounds/animations,"Class_SpaceFractions:FeedbackEngine","MediaEngine,FeedbackEngine",architecture.md,"Immediate reinforcement."
INF-FR-011,Ending shows score and message,"UseCase_SpaceFractions:UC_Results","ResultsView,StoryEngine",architecture.md,"Score + narrative."
INF-FR-012,Replay or quit,"UseCase_SpaceFractions:UC_Replay; State_GameSession:Results->MainMenu/Quit","Router,GameSession",architecture.md,"Repeat practice."
INF-FR-013,Branching story,"Class_SpaceFractions:StoryEngine; Question.isCritical","StoryEngine",architecture.md,"Critical branching."
INF-FR-014,Retry wrong answer but no points,"State_GameSession:FeedbackWrong->PresentingQuestion","GameSession",architecture.md,"No credit after retry."
INF-FR-015,Validate fraction input and adjust velocity realtime,"Class_SpaceFractions:VelocityAdjuster,FractionValidator,PhysicsEngine","VelocityAdjuster,PhysicsEngine",architecture.md,"Safe realtime adjustment."
INF-FR-016,Admin edits questions,"UseCase_SpaceFractions:UC_EditQ,UC_PublishQ","AdminWebUI,AdminAPI",openapi.yaml,"Update flow."
INF-FR-017,Admin login/password,"UseCase_SpaceFractions:UC_AdminLogin","AdminAuthService",openapi.yaml,"Secured access."
INF-FR-018,Save question updates to server file,"Sequence2_Admin_UpdateQuestions:QuestionFileStore writeAtomically","QuestionFileStore",architecture.md,"File-based persistence with rollback."
INF-FR-019,Score kept local per instance,"Class_SpaceFractions:GameSession<<session>>","GameSession",architecture.md,"No server persistence."
INF-FR-020,Math Umbrella external links,"UseCase_SpaceFractions:UC_External","WebGameUI",architecture.md,"Open curated links."
INF-NFR-001,No plugins; modern browser support,"Package_SpaceFractions:ui note","WebGameUI",architecture.md,"HTML5 migration."
INF-NFR-002,p95 velocity update <=150ms,"Class_SpaceFractions:VelocityAdjuster note","VelocityAdjuster",architecture.md,"Responsiveness target."
INF-NFR-003,Behavior invariant across environments,"Deployment_SpaceFractions note","GameCore separation",architecture.md,"Regression testing across browsers."
INF-NFR-004,First interactive <3s; bundle <=2.5MB,"Activity_GameplayFlow note","WebGameUI build",architecture.md,"Performance budgets."
INF-NFR-005,Accessibility ARIA-live; WAVE>=98%,"Class_SpaceFractions:FeedbackEngine note","WebGameUI",architecture.md,"Accessible feedback."
INF-NFR-006,Usability reach Q1 <2m,"Package_SpaceFractions:ui note","WebGameUI",architecture.md,"Persona target."
INF-NFR-007/ASR-007,HTTPS/bcrypt/lockout/timeout/audit,"Class_SpaceFractions:AdminAuthService note","AdminAPI,AuditLog",sql/audit_log_ddl.sql,"Explicit security controls."
INF-ASR-004,Server-hosted JSON persistence,"Deployment_SpaceFractions:QuestionFileStoreArtifact","QuestionFileStore",architecture.md,"Persistent content store."
INF-ASR-005,ETag/TTL<=60s + schemaVersion + rollback,"Class_SpaceFractions:QuestionBank note","QuestionBank,Updater",openapi.yaml,"Safe dynamic updates."
INF-ASR-006,Single-user per instance; score cleared,"Container_SpaceFractions:GameCore note","GameSession",architecture.md,"No cross-user state."
INF-NFR-008,Reliability via extensive testing,"N/A (SRS statement)","CI/CD tests",architecture.md,"Operationalized with CI gates."
INF-NFR-009,Available over internet,"Deployment_SpaceFractions:WebHost","Hosting",architecture.md,"Internet accessible."
INF-NFR-010,No new hardware,"N/A (SRS statement)","Browser-only",architecture.md,"Runs on existing devices."
INF-NFR-011,Maintainability primary goal,"N/A (SRS statement)","Modular design + schema/contracts",architecture.md,"Supports long-term updates."
```

---

## Verification (Acceptance Criteria)

| Item | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | ✅ |
| [ ] Sections A-L included. | ✅ |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | ✅ (all inferred as INF-* due to missing IDs) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | ✅ |
| [ ] Representative k8s manifest snippet included. | ✅ |
| [ ] SQL DDL / NoSQL models for primary entities included. | ✅ |
| [ ] All major components have at least one API contract and a data schema. | ✅ (AdminAPI + audit/admin tables; questions schema via OpenAPI) |
| [ ] Assumptions and unresolved questions listed. | ✅ |

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?