Scope: Produce production-ready architecture documentation for Space Fractions + Math Umbrella + Admin Question Updater, aligned to SRS and 11 provided UML diagrams.  
Approach: 4+1 views, contract-first APIs, versioned content schema, security/ops/testing coverage; resolve conflicts by preferring Original Requirements and logging assumptions/conflicts.  
Validation: Full traceability matrix (all FR/NFR/ASR), parsable OpenAPI + internal proto, valid k8s + SQL DDL snippets, and acceptance checklist verification table.

# ArchitectureDocument.md

## A. Executive Summary (≤1 page)

**System overview**  
Space Fractions is a web-based interactive learning system for 6th-grade fraction skills with storyline-driven multiple-choice questions, adaptive branching at critical points, immediate feedback (audio/animation), session-local scoring with end ranking/message, and an admin web tool to update the question bank stored on the server. A “Math Umbrella” web menu links to Space Fractions and external learning resources.

**Primary diagram mapping (one line)**  
Core behavior and structure are captured in: *Use Case* (UseCase: UC_*), *Class* (Class: GameApp/GameSession/QuestionBank/AdminUpdaterUI), *State* (State: GameSession states), *Sequence* (Sequence_S1_Gameplay, Sequence_S2_AdminUpdate), *Component* (Component: SpaceFractionsSPA/AdminBackendAPI/QuestionBankFileStore), *Deployment* (Deployment: StudentDevice/WebServer).

**Architectural style(s)**  
- **Client-heavy SPA + thin admin backend** (static content delivery; in-browser deterministic game engine; admin-only APIs).  
- **Contract-first content pipeline** (versioned JSON question bank validated on publish/load).

**Deployment topology (one line)**  
Single HTTPS web server (static assets + admin API + file store) with CDN optional; end-users run SPA in browser; admins use separate updater UI (ref: *Deployment* diagram: WebServer/StudentDevice/AdminDevice).

### Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| R1: SRS mentions Flash; modern browsers do not support it | Unshippable product | Adopt HTML5/JS/Canvas/WebAudio (Justification: meets NFR-003 compatibility + maintainability goal); log as requirement conflict (see K). |
| R2: “Real-time question updates” vs caching and bandwidth | Stale content or high load | Use versioned `qbank.json` + ETag + TTL reload ≤60s and show `version/lastSyncAt` in UI (Justification: meets maintainability + ASR-004 in diagrams). |
| R3: Admin updater security ambiguity | Content tampering | HTTPS-only, strong password policy, lockout, server-side sessions, audit log for privileged actions (Justification: meets NFR-008 security in UseCase note and diagrams). |

### Key QA coverage mapping

| Quality attribute | Requirement IDs | Primary tests |
|---|---|---|
| Scalability | INF-NFR-SCALE-001 (multi-user access via internet) | Load test static asset + `qbank.json` GET; CDN validation; admin API concurrency test |
| Availability | INF-NFR-AVAIL-001 (reliability via testing) | Synthetic monitoring; chaos test (kill admin pod) |
| Security | NFR-008, INF-NFR-SEC-001 | SAST/DAST, dependency scanning, authz tests, session tests, TLS config scan |
| Performance | NFR-006, INF-NFR-PERF-001 (fast load on modem), ASR-006 | Lighthouse/web-vitals, asset budget tests, gameplay latency tests |
| Maintainability | “Maintainability primary goal”, ASR-004, FR-013 | Contract tests for schema; migration tests; admin publish rollback tests |

---

## B. Traceability & Rationale

**Notes on IDs:** The provided SRS text does not include explicit FR/NFR/ASR numbering except what appears in diagrams (e.g., FR-002, FR-005, FR-012/013/014, NFR-006/008, ASR-001..006). Missing IDs are inferred as `INF-*` per rules and listed in K.

### Traceability matrix (also delivered as `traceability_matrix.csv` in Section L)

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| FR-001 | Web-based interactive learning tool for fractions | Container: SPA/Umbrella; Deployment: StudentDevice | SpaceFractionsSPA, MathUmbrellaWeb | architecture.md | SPA delivers interactive experience in browser with minimal install. |
| FR-002 | Intro movie plays; click to skip | UseCase: UC_PlayIntro/UC_SkipIntro; State: IntroPlaying; Activity: PlayIntro/SkipIntro | MenuController, SpaceFractionsSPA | architecture.md | Implements autoplay intro with click-to-skip event handling. |
| FR-003 | Main menu with help + links | UseCase: UC_LaunchMenu/UC_ViewHelp; Activity: ShowMainMenu | MathUmbrellaWeb, MenuController | architecture.md | Menu provides navigation and help for usability. |
| FR-004 | Series of fraction questions in storyline | UseCase: UC_AnswerQuestion; Sequence_S1_Gameplay loop; State: InQuestion | GameSession, QuestionBank | architecture.md | QuestionBank drives storyline sequence with branching. |
| FR-005 | Incorrect answer => retry; no points | State: IncorrectFeedback→Retry/lockPoints; Activity: LockPointsForQuestion | GameSession, ScoreBoard | architecture.md | Enforces learning through retry while preventing point farming. |
| FR-006 | Output feedback via sounds/animations | Activity: PlayCorrect/Incorrect; Class: FeedbackAnimator | RenderAudioUI, FeedbackAnimator | architecture.md | Audio/visual feedback via WebAudio/Canvas. |
| FR-007 | Sidekick assistant gives hints/usability help | UseCase: UC_GetHint; Class: SidekickAssistant | SidekickAssistant, UI | architecture.md | Provides contextual hints without altering scoring rules. |
| FR-008 | Branching storyline at critical questions | Class: Question.critical + BranchRule; State: BranchDecision | GameEngine, QuestionBank | architecture.md | Declarative branch rules in content enable adaptive story. |
| FR-009 | Ending scene shows score/rank + replay/exit | UseCase: UC_ViewResults/UC_ReplayExit; State: Results/EndingScene | GameSession, ScoreBoard | architecture.md | Score summarized at end; user chooses replay or exit. |
| FR-010 | Score is computed and ranked with custom message | Class: ScoreBoard.computeRank/composeMessage | GameEngine | architecture.md | Deterministic scoring + rank mapping. |
| FR-011 | Single user per running instance; many can access online | Deployment: StudentDevice; note ASR-002 | SpaceFractionsSPA | architecture.md | Session-local in-memory state; stateless hosting supports many users. |
| FR-012 | Admin updater accessible via web; password gate | UseCase: UC_AdminLogin; Sequence_S2_AdminUpdate | AdminUpdaterWeb, AdminBackendAPI | openapi.yaml, internal.proto | Dedicated admin UI + secure auth endpoint. |
| FR-013 | Admin edits questions; saved to server file; easy screens | UseCase: UC_EditQuestion/UC_PublishQuestions; Component: QuestionBankFileStore | AdminBackendAPI, QuestionBankFileStore | sql/*.sql, openapi.yaml | File-based question store with atomic publish; UI forms for editing. |
| FR-014 | External resources open in separate window/tab | UseCase note UC_OpenExternal; Container: openSeparateWindow | MathUmbrellaWeb | architecture.md | Ensures game context remains open while browsing resources. |
| FR-015 | Inputs are mouse clicks for answers/preferences | SRS text; Activity: GetAnswer(mouse click) | SpaceFractionsSPA | architecture.md | UI restricted to click interactions for accessibility. |
| FR-016 | Fraction input: numerator/denominator validated; denom!=0 | Class: FractionInputValidator; Activity: ValidateFractionInput | GameEngine | architecture.md | Enforces integer validation and denominator constraints. |
| FR-017 | Convert fraction to decimal & apply velocity adjustment | Class: FractionConverter/PhysicsEngine; Activity: ApplyVelocityDelta | GameEngine, PhysicsEngine | architecture.md | Real-time physics update based on fraction conversion. |
| FR-018 | Invalid fraction shows error and requests new input | Activity: ShowErrorMessage; Class: ValidationResult | UI, GameEngine | architecture.md | Immediate user feedback maintains flow. |
| NFR-003 | Runs on any internet-accessible computer; modern browser support | Deployment note NFR-003; Activity note ASR-001/NFR-003 | SpaceFractionsSPA | architecture.md | Standards-based SPA supports broad device/browser matrix. |
| NFR-004 | Usability: simple mouse-driven UI for 6th graders | Package: ui note | UI | architecture.md | Menu/help and click-only interactions reduce friction. |
| NFR-006 | Real-time velocity update | Class note PhysicsEngine; Activity note | PhysicsEngine | architecture.md | In-browser compute avoids network round-trip latency. |
| NFR-007 | Reliability ensured by extensive testing | SRS; Testing strategy | All | architecture.md | Automated tests + monitoring provide measurable reliability. |
| NFR-008 | Security: HTTPS, pw>=12, lockout after 5 | UseCase note UC_AdminLogin; Component notes | AuthSessionService, AdminBackendAPI | openapi.yaml, internal.proto | Explicit controls replace “secure as browser” ambiguity. |
| NFR-010 | Bandwidth/load-time constraints (modem friendly) | Container note ASR-006/NFR-010 | StaticAssetHost, SPA | architecture.md | Progressive loading and asset budgets meet slow network constraints. |
| ASR-001 | No plugins; HTML5 migration | Activity note ASR-001 | SpaceFractionsSPA | architecture.md | Removes Flash dependency; improves maintainability/compatibility. |
| ASR-002 | Score/state session-local | UseCase note UC_ViewResults; Deployment note | GameEngine | architecture.md | Prevents cross-user leakage; supports privacy. |
| ASR-003 | Behavior invariant across environments | Package note domain | GameEngine | architecture.md | Deterministic logic separated from rendering; regression across browsers. |
| ASR-004 | Versioned JSON schema; ETag+TTL reload ≤60s; atomic write | Class note QuestionBank; Component note ContentLoader | ContentLoader, QuestionBankRepository | internal.proto, sql/*.sql | Ensures modifiability and bounded staleness. |
| ASR-005 | Secure auth/session; hashing; audit | Component notes AdminBackendAPI/AuthSessionService | AuthSessionService, AuditLogService | sql/*.sql, openapi.yaml | Meets admin security and accountability. |
| ASR-006 | Progressive loading/media constraints | Container note SPA | StaticAssetHost, SPA | architecture.md | Keeps initial load time low; streams media. |
| INF-FR-UMB-001 | Umbrella menu lists projects by topic (fractions/decimals/percents) | UseCase: UC_LaunchMenu/UC_OpenProject | MathUmbrellaWeb | architecture.md | Simple static menu page with categorized links. |
| INF-FR-EXT-001 | Link to Denominators web page from menu | SRS main menu text | MathUmbrellaWeb | architecture.md | Treated as external resource link. |
| INF-NFR-AVAIL-001 | Availability/reliability target unspecified; must be “reliable” | SRS reliability statement | WebServer | architecture.md | Define SLOs and monitoring to operationalize. |
| INF-NFR-SCALE-001 | Many users can access online concurrently | SRS “reside on the Internet” | StaticAssetHost | architecture.md | Static hosting + CDN enables horizontal scale. |
| INF-NFR-PERF-001 | Intro/menu downloads ~1 minute on modem; playable quickly | SRS download constraints | StaticAssetHost | architecture.md | Enforce asset size budgets and compression. |
| INF-NFR-SEC-001 | “Secure as the browser” replaced with explicit policy | SRS security statement | AdminBackendAPI/Auth | architecture.md | Convert vague statement into testable controls (NFR-008). |
| INF-FR-AUD-001 | Audit privileged admin events (publish) | Sequence_S2 + Class: AuditLogger | AuditLogService | sql/audit_log_ddl.sql | Enables accountability and incident investigation. |

---

## C. Architecture Overview

### Context view
Actors: **EndUser (students)** and **Admin (teacher)**. EndUser uses Math Umbrella to launch Space Fractions and open external resources; Admin logs in to updater to edit/publish questions (ref: *Use Case* diagram: EndUser/Admin with UC_*).

### Container view
- **MathUmbrellaWeb**: static menu page; opens SpaceFractions in separate tab/window (ref: *Container* diagram: Umbrella → SPA).  
- **SpaceFractionsSPA**: in-browser game UI (intro/menu/gameplay/results).  
- **GameEngine (in-browser)**: deterministic scoring/branching/validation; session-local state (ref: *Container* diagram: Engine; *Class*: GameSession/ScoreBoard).  
- **AdminUpdaterWeb**: admin UI for editing questions.  
- **WebServer**: serves static assets + `qbank.json`; hosts AdminBackendAPI + AuthSessionService + AuditLogService; persists question bank to file store (ref: *Container* + *Deployment* diagrams).

### Component/Package view
Packages: `ui`, `domain`, `content`, `admin`, `security`, `observability`, `infrastructure` (ref: *Package* diagram). Key components: SpaceFractionsSPA, GameEngine, ContentLoader, AdminBackendAPI, AuthSessionService, AuditLogService, QuestionBankFileStore (ref: *Component* diagram).

### Class/runtime view
Runtime flow: GameApp boots → intro → main menu → loads QuestionBank with caching → GameSession loops questions with hint and feedback → branch decisions → results and replay/exit (ref: *State* diagram “GameSession”; *Activity* diagram; *Sequence_S1_Gameplay*). Admin flow: login → edit → validate → atomic publish → audit log (ref: *Sequence_S2_AdminUpdate*).

### Deployment view
Browser clients connect via HTTPS to WebServer. Static assets and question bank delivered via caching headers (ETag). Admin operations use HTTPS POST to admin API; question bank stored on disk (ref: *Deployment* diagram).

---

## D. Detailed Technical Design (developer-facing)

### D1. Subsystem: EndUser Web Experience (MathUmbrellaWeb + SpaceFractionsSPA)

#### 1) Responsibilities & data ownership
Renders intro/menu/help/gameplay/results, handles mouse-click interactions, plays audio/animations, and maintains **session-local** gameplay state (current question, attempts, score). Owns no server-side user data (Justification: meets ASR-002 session-local state).

#### 2) Technology options (≥3 per concern)

**Language/runtime (frontend)**
- Recommended: TypeScript 5.x on Node.js toolchain 18–20 (build-time). Compatibility: modern evergreen browsers.  
- Conservative: ES2020 JavaScript + JSDoc types. Compatibility: broad but less safe.  
- Cutting-edge: WebAssembly (Rust) for game logic. Compatibility: modern browsers; higher complexity.

**Web framework**
- Recommended: React 18 + Vite 5/6. Compatibility: Chrome/Edge/Firefox/Safari latest-2.  
- Conservative: Vanilla + Web Components (Lit 3).  
- Cutting-edge: Svelte 5 or SolidJS.

**RPC/HTTP**
- Recommended: Fetch API + REST for admin and content GET; no runtime dependency.  
- Conservative: Axios wrapper.  
- Cutting-edge: GraphQL client for content (overkill).

**Persistence (client)**
- Recommended: In-memory state + optional `sessionStorage` for crash-recovery toggle.  
- Conservative: `localStorage` (but violates session-local intent if persisted).  
- Cutting-edge: IndexedDB with structured versioning.

**Cache**
- Recommended: HTTP cache + Service Worker (optional) for offline-ish behavior.  
- Conservative: Browser HTTP cache only.  
- Cutting-edge: App-managed cache with Cache Storage + background sync.

**Messaging**
- Recommended: None (single-user local loop).  
- Conservative: Web Worker messages for heavy compute.  
- Cutting-edge: SharedWorker for multi-tab (not needed; conflicts with “single instance”).

**Search**
- Recommended: None.  
- Conservative: Client-side search for question bank (not required).  
- Cutting-edge: WASM search index.

**Authn/Authz**
- Recommended: No end-user auth; admin auth handled separately.  
- Conservative: Basic Auth for admin (discouraged).  
- Cutting-edge: OIDC login for admin.

**Observability**
- Recommended: Web-vitals + lightweight client error reporting (Sentry 7/8).  
- Conservative: Console logs only (not acceptable for production).  
- Cutting-edge: OpenTelemetry JS in browser.

**CI/CD**
- Recommended: GitHub Actions with lint/test/build and artifact upload.  
- Conservative: Manual build.  
- Cutting-edge: Bazel monorepo.

**Container runtime / infra provisioning**
- Not applicable to pure static SPA; see server subsystem.

#### 3) Recommended default stack (+ justification)
- **TypeScript 5.4–5.6, React 18.2, Vite 5–6, Canvas/WebAudio, Fetch API**.  
Justification: meets ASR-001 (no plugins) and NFR-003 (browser compatibility).

#### 4) Interface design
EndUser surface is static hosting + `GET /content/qbank.json` (see OpenAPI, D2).

#### 5) Data model / schema
No end-user persistent server entities (Justification: meets ASR-002).

#### 6) Caching & consistency
- Cache static assets with long max-age + content hashes.  
- Cache `qbank.json` with `ETag` and `Cache-Control: max-age=60`.  
- Client `ContentLoader` reloadIfStale with TTL ≤60s (ref: *Class* QuestionBank note; *Component* ContentLoader).

---

### D2. Subsystem: Content Delivery & Question Bank (ContentLoader + QuestionBankFileStore)

#### 1) Responsibilities & data ownership
Owns the **versioned question bank** content contract. Serves `qbank.json` to SPAs with caching headers; stores the canonical file on server disk; validates schema on publish and (optionally) on read. (Justification: meets ASR-004 versioned schema + atomic write.)

#### 2) Technology options

**Language/runtime (backend)**
- Recommended: Node.js 20 LTS (TypeScript) with Fastify 4/5.  
- Conservative: Python 3.11–3.13 with Flask/FastAPI.  
- Cutting-edge: Go 1.22–1.24 with Chi/Fiber.

**Web framework**
- Recommended: Fastify (high throughput, schema support).  
- Conservative: Express.  
- Cutting-edge: Bun server.

**Persistence**
- Recommended: File-based JSON on disk + atomic rename writes.  
- Conservative: SQLite 3.45+ file DB.  
- Cutting-edge: Postgres 14–16 or S3/object store + versioning.

**Cache**
- Recommended: ETag computed from file hash + `max-age=60`.  
- Conservative: No caching (higher bandwidth).  
- Cutting-edge: Redis 7 cache with pub/sub invalidation.

**Observability**
- Recommended: Structured logs (pino) + Prometheus metrics endpoint.  
- Conservative: Plain logs.  
- Cutting-edge: Full OpenTelemetry tracing.

#### 3) Recommended default stack (+ justification)
- **Node.js 20 + Fastify + file-backed `qbank.json` with atomic publish + ETag + Cache-Control max-age=60**.  
Justification: meets ASR-004 (versioned JSON + TTL/ETag) and INF-NFR-PERF-001 (bandwidth-aware caching).

#### 4) Interface design (External APIs: OpenAPI YAML)
Provided in Section L as `openapi.yaml` (covers `GET /content/qbank.json`, admin auth, edit/publish flows, audit read).

#### 5) Data model / schema (server-side)
Persisted entities (even if file-based) are modeled for operability and audit:
- `question_bank_versions` (metadata)
- `admin_users`
- `admin_sessions`
- `audit_log`

SQL DDL in Section L (`sql/*.sql`). Even if question content stays in a file, metadata/audit benefits from SQL (recommended). If pure-file-only is desired, keep DDL as “future-ready”.

Fields requiring special handling:
- Password hash: encryption-at-rest via platform/disk + hashing (ASR-005, NFR-008).
- Audit log: append-only/immutable semantics (INF-FR-AUD-001).

#### 6) Caching & consistency
- EndUser reads are **eventually consistent ≤60s** (TTL-based).  
- Admin publish is **strong** for the single server: atomic write ensures readers see either old or new full file, never partial (ASR-004).  
- If multi-replica later: move file to shared object store or DB and propagate via CDN purge.

---

### D3. Subsystem: Game Engine (in-browser domain logic)

#### 1) Responsibilities & data ownership
Implements deterministic rules: question evaluation, retry/point lock, scoring/ranking/message, branching at critical points, fraction validation and velocity adjustment application through PhysicsEngine abstraction. Owns session-local state only. (Justification: meets ASR-003 deterministic behavior + ASR-002 local state.)

#### 2) Technology options

**Language/runtime**
- Recommended: TypeScript shared with SPA.  
- Conservative: JavaScript module.  
- Cutting-edge: Rust→WASM.

**Persistence**
- Recommended: none (in-memory).  
- Conservative: sessionStorage.  
- Cutting-edge: IndexedDB.

**Caching**
- Recommended: cache current question + prefetch next media assets.  
- Conservative: no prefetch.  
- Cutting-edge: predictive prefetch based on branch probabilities.

**Observability**
- Recommended: client event counters (attempts, completion rate) sampled; privacy-safe.  
- Conservative: no metrics.  
- Cutting-edge: full event stream (not required; privacy risk).

#### 3) Recommended default stack (+ justification)
- **TypeScript game engine module with pure functions for scoring/branching + adapter interfaces for rendering/physics**.  
Justification: meets ASR-003 (environment-invariant behavior) and NFR-006 (real-time physics updates locally).

#### 4) Internal contracts
Use internal `.proto` for conceptual contracts between UI and engine (even if in-process) and between admin backend and repository for clarity; provided as `internal.proto` in Section L.

#### 5) Data model / schema
Question JSON schema (served content) example (documented here; validated in admin publish):
- `version`, `generatedAt`, `startQuestionId`, `questions[]` with `id,prompt,choices,correctIndex,critical,branchRules,inputMode,fractionInput`.

(We keep canonical schema in OpenAPI under `QuestionBank`.)

#### 6) Caching & consistency
Engine caches loaded bank in memory; `reloadIfStale` checks TTL and ETag.

---

### D4. Subsystem: Admin Updater (AdminUpdaterWeb + AdminBackendAPI + Auth + Audit)

#### 1) Responsibilities & data ownership
Admin UI provides forms to edit questions and publish new bank versions. Backend authenticates admin, enforces lockout/session expiry, validates schema, writes question bank atomically, and appends audit events. (Justification: meets FR-012/FR-013 and NFR-008/ASR-005.)

#### 2) Technology options

**Authn/Authz**
- Recommended: Session cookies (HttpOnly, Secure, SameSite=Strict) + server session store (SQLite/Postgres).  
- Conservative: HTTP Basic Auth (insufficient controls).  
- Cutting-edge: OIDC (Google/Microsoft) with MFA.

**Persistence**
- Recommended: Postgres 14–16 for admin users/sessions/audit + file store for qbank.  
- Conservative: SQLite for admin data + file store for qbank.  
- Cutting-edge: Managed auth (Auth0) + object store versioning.

**Observability**
- Recommended: audit log + security metrics (failed logins, lockouts).  
- Conservative: audit file only.  
- Cutting-edge: SIEM integration.

**CI/CD**
- Recommended: build, unit/integration tests, container scan, deploy with canary.  
- Conservative: manual deploy.  
- Cutting-edge: GitOps with ArgoCD.

#### 3) Recommended default stack (+ justification)
- **Fastify backend + server-side sessions + Argon2id hashing + audit log append-only + atomic file publish**.  
Justification: meets NFR-008 and ASR-005 (secure auth + audit).

#### 4) Interface design
External OpenAPI in `openapi.yaml`. Key endpoints:
- `POST /admin/auth/login`
- `POST /admin/auth/logout`
- `GET /admin/questions`
- `PUT /admin/questions/{id}`
- `POST /admin/publish`
- `GET /content/qbank.json`

#### 5) Data model / schema
See SQL DDLs in Section L:
- `admin_users`, `admin_sessions`, `audit_log`, `question_bank_versions`.

#### 6) Caching & consistency
- Admin endpoints: `Cache-Control: no-store`.  
- Publish triggers new `ETag` for `qbank.json` and version bump; clients observe within ≤60s due to caching policy (ASR-004).

---

## E. Operations & Deployment (ops-facing)

### E1. Kubernetes-ready plan (representative manifest)
See `k8s/web-deployment.yaml` in Section L (Deployment + Service + HPA + ConfigMap + Secret).  
Justification for Kubernetes option: supports INF-NFR-SCALE-001 (many concurrent users) and INF-NFR-AVAIL-001 (operational reliability).

Suggested replicas (stateless web):
- Small: 1–2 replicas
- Medium: 3–5 replicas
- Large: 6–12 replicas + CDN

### E2. DB HA topology, backups, restore
- **Recommended**: Postgres 14–16 managed (or Patroni) with 1 primary + 1 replica; PITR enabled.  
  - Backups: daily full + continuous WAL; retain 30 days.  
  - Restore drill: monthly; verify admin login and audit query.  
Justification: supports ASR-005 auditability and NFR-008 secure admin operation continuity.

If SQLite chosen: run single-writer with scheduled backups; accept reduced HA.

### E3. Network topology + ingress/egress rules
- Ingress: HTTPS 443 only to web service (ref: *Deployment* diagram: StudentDevice→WebServer HTTPS).  
- Egress: optional to error reporting endpoint (if enabled).  
- Latency expectations: EndUser gameplay logic local; only initial asset/qbank fetch on network.  
Justification: meets NFR-006 (real-time updates local) and NFR-003 (web accessible).

### E4. CI/CD sketch
1. PR: lint, typecheck, unit tests; build SPA; build backend; schema validation tests.  
2. Security: dependency scan, SAST, container scan; TLS lint.  
3. Deploy to staging; run E2E (Playwright) across browser matrix.  
4. Prod: canary 10% → 50% → 100%; rollback on alert.  
Justification: supports NFR-007 reliability and maintainability goal.

---

## F. Security Design

### F1. Auth & AuthZ
- **Admin-only authentication** using **server-side sessions** with cookie: `HttpOnly; Secure; SameSite=Strict`.  
- Passwords stored as **Argon2id** hash; password policy: length ≥12; lockout after 5 failed attempts for 15 minutes.  
- Role model: `ADMIN` only (scope for future `TEACHER/EDITOR`).  
Justification: meets NFR-008 and ASR-005.

Token lifecycle:
- Session TTL: 15 minutes inactivity; absolute 8 hours.
- Revocation: logout deletes session; admin disable invalidates all sessions.

### F2. Secrets management & rotation
- Kubernetes Secret or cloud secret manager for `SESSION_SECRET`, `DATABASE_URL`.  
- Rotation: quarterly or on incident; support dual secrets during rotation.  
Justification: supports NFR-008.

### F3. TLS & service-mesh
- TLS 1.2+ enforced at ingress; HSTS enabled.  
- Service mesh optional; not required for single service, but permitted for mTLS internally if split later.  
Justification: meets NFR-008.

### F4. Threat model (top 5)
| Threat | Mitigation |
|---|---|
| Credential stuffing on admin login | Rate limit + lockout + strong password policy (NFR-008). |
| XSS in question content | Server-side schema validation + output encoding; CSP headers. |
| Tampering with question bank file | Admin-only publish; atomic writes; audit logs (ASR-004/ASR-005). |
| Session hijack | Secure cookies + SameSite + TLS + session expiry (NFR-008). |
| Supply chain vulnerabilities | Dependency scanning + pinned versions + SCA gates (NFR-007). |

---

## G. Observability & SRE

### G1. Metrics, traces, logs
**Backend metrics (Prometheus):**
- `http_requests_total{route,code}`
- `admin_login_fail_total`
- `admin_lockout_total`
- `qbank_publish_total`
- `qbank_current_version` (gauge)
- `qbank_file_write_errors_total`

**Client metrics (sampled, privacy-safe):**
- completion rate, average attempts per question, hint usage frequency.

**Logs**
- Structured JSON logs on backend; audit log persisted separately (append-only semantics).

**Example Prometheus alert rules**
- High 5xx rate:
  - `sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02`
- Publish failures:
  - `increase(qbank_file_write_errors_total[15m]) > 0`

### G2. SLOs, error budgets, RTO/RPO
- SLO (static content availability): 99.9% monthly (INF-NFR-AVAIL-001).  
- SLO (admin publish success): 99.5% monthly.  
- RTO: 4 hours (restore service).  
- RPO: 24 hours for admin DB; question bank file additionally stored in object storage backup nightly.  
Justification: operationalizes reliability and maintainability goals.

### G3. Dashboard/runbook sketch
Dashboards:
- Traffic + latency + error rate
- Admin auth failures/lockouts
- Current qbank version + last publish time
Runbooks:
- “Admin can’t login” (check lockout, DB connectivity)
- “qbank stale” (check cache headers, ETag changes, CDN config)
- “publish failing” (disk full, permissions, atomic rename failure)

---

## H. Testing Strategy

### H1. Test matrix

| Test type | Components | Examples |
|---|---|---|
| Unit | GameEngine, validators | scoring rules, retry lock, fraction denom!=0 |
| Integration | AdminBackendAPI + FileStore | publish writes atomic, ETag changes |
| Contract | OpenAPI + internal.proto | schema validation, error format conformance |
| E2E | SPA + backend (staging) | playthrough flows, branching, results, replay |
| Chaos | backend | kill pod during publish (ensure atomicity) |

### H2. Test data & environment isolation
Environments: `dev` (local), `staging`, `prod`.  
- Staging refresh cadence: nightly reset of DB + sample qbank.  
- Prod data: audit retained 90 days; no end-user PII stored.

---

## I. Migration, Data Conversion & Rollout Plan

### I1. Migration steps (Flash → HTML5 replacement)
1. Extract existing questions/story assets into new `qbank.json` schema.  
2. Implement SPA intro/menu/gameplay with parity acceptance tests.  
3. Release admin updater for content maintenance.  
4. Parallel run: host legacy content read-only for short window; redirect to new SPA.  
5. Rollback: keep previous `qbank.json` version and allow instant revert by repointing symlink/version.  
Justification: meets maintainability goal and NFR-003 compatibility.

### I2. Backwards compatibility and API versioning
- Version OpenAPI at `/api/v1`.  
- `qbank.json` includes `schemaVersion` to allow forward-compatible loaders.  
- Breaking changes: new `/v2` endpoint and dual-serve for 30 days.

---

## J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros | Cons | Why chosen (tie to IDs) |
|---|---|---|---|---|
| Replace Flash with HTML5 | Keep Flash; Use WebView wrapper | Runs in modern browsers; maintainable | Stakeholder sign-off needed | Chosen due to ASR-001 + NFR-003 compatibility. |
| File-based qbank store | DB-backed questions; S3 object store | Simple, easy edit, atomic rename | Harder in multi-replica | Matches FR-013 and ASR-004. |
| Session cookies vs JWT | JWT; OIDC | Cookies simplest; less token leakage | Requires server session store | Meets NFR-008 lockout/session rules and ASR-005 audit. |
| TTL/ETag cache vs push invalidation | WebSocket push; CDN purge on publish | Simple, bounded bandwidth | Eventual consistency up to 60s | Meets ASR-004 TTL<=60s and modem constraints. |

---

## K. Open Questions & Assumptions

### Assumptions
- **A1:** EndUser does not require login; no student identity or persistent progress is stored server-side.  
- **A2:** “Real-time updates” for question content means propagation to clients within **≤60 seconds**, not instantaneous push.  
- **A3:** Admin user base is small (single teacher or small set); RBAC beyond `ADMIN` is out of scope.  
- **A4:** Question bank is modest in size (≤500 questions; ≤5 MB uncompressed) to meet modem-era constraints.  
- **A5:** Audio/animation assets are either embedded with the SPA build or referenced by URL in the question bank and are cacheable.

### Conflicts logged (rules: prefer Original Requirements naming/IDs)
- **C1:** SRS requires “Flash-supporting browser”, but architecture/diagrams adopt HTML5/JS (ASR-001). Preferred: deliver HTML5; record as modernization conflict.

### Unresolved stakeholder questions (suggested phrasing)
1. Should scores/ranks be saved for teacher review (leaderboard) or remain session-local only (ASR-002)?  
2. What exact scoring formula and rank thresholds are desired (ScoreBoard)?  
3. How many “critical questions” and what branching depth is expected (content authoring constraints)?  
4. Should external resources open in a new tab always, or configurable for pop-up blockers (FR-014)?  
5. Who manages admin accounts (single shared password vs per-teacher accounts)?

### Inferred requirement IDs (due to missing IDs in SRS)
- INF-FR-UMB-001, INF-FR-EXT-001, INF-NFR-AVAIL-001, INF-NFR-SCALE-001, INF-NFR-PERF-001, INF-NFR-SEC-001, INF-FR-AUD-001, INF-NFR-PERF-002 (asset budget enforcement implicit).

---

## L. Deliverables

```markdown
<!-- filename: architecture.md -->
(Use the full content of this ArchitectureDocument.md)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Space Fractions API
  version: "1.0.0"
  description: |
    Public content API and admin updater API for Space Fractions.
    End-user gameplay is client-side; server provides question bank content and admin publishing.
servers:
  - url: https://spacefractions.example.org
paths:
  /content/qbank.json:
    get:
      summary: Get current question bank (versioned)
      operationId: getQuestionBank
      responses:
        "200":
          description: Question bank JSON
          headers:
            ETag:
              schema: { type: string }
            Cache-Control:
              schema: { type: string }
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QuestionBank"
        "304":
          description: Not modified
        "500":
          description: Server error
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/auth/login:
    post:
      summary: Admin login (creates session cookie)
      operationId: adminLogin
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/AdminLoginRequest" }
      responses:
        "200":
          description: Login OK
          headers:
            Set-Cookie:
              schema: { type: string }
          content:
            application/json:
              schema: { $ref: "#/components/schemas/AdminLoginResponse" }
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "423":
          description: Locked (too many failed attempts)
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/auth/logout:
    post:
      summary: Admin logout (revokes session)
      operationId: adminLogout
      security:
        - cookieAuth: []
      responses:
        "204":
          description: Logged out
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/questions:
    get:
      summary: List questions (metadata + prompts)
      operationId: listQuestions
      security:
        - cookieAuth: []
      responses:
        "200":
          description: List of questions
          content:
            application/json:
              schema:
                type: object
                required: [version, questions]
                properties:
                  version: { type: string }
                  questions:
                    type: array
                    items: { $ref: "#/components/schemas/Question" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/questions/{id}:
    put:
      summary: Upsert a question in a draft workspace (server-side draft)
      operationId: upsertQuestion
      security:
        - cookieAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, minLength: 1 }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/Question" }
      responses:
        "200":
          description: Saved to draft
          content:
            application/json:
              schema:
                type: object
                required: [draftVersion, question]
                properties:
                  draftVersion: { type: string }
                  question: { $ref: "#/components/schemas/Question" }
        "400":
          description: Schema/validation error
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/publish:
    post:
      summary: Publish current draft as new question bank version (atomic)
      operationId: publishQuestionBank
      security:
        - cookieAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [changeNote]
              properties:
                changeNote:
                  type: string
                  minLength: 1
      responses:
        "200":
          description: Publish OK
          content:
            application/json:
              schema:
                type: object
                required: [version, etag, publishedAt]
                properties:
                  version: { type: string }
                  etag: { type: string }
                  publishedAt: { type: string, format: date-time }
        "400":
          description: Draft invalid
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "401":
          description: Not authenticated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }
        "500":
          description: Publish failed
          content:
            application/json:
              schema: { $ref: "#/components/schemas/ErrorResponse" }

  /api/v1/admin/audit:
    get:
      summary: Get recent audit events
      operationId: listAuditEvents
      security:
        - cookieAuth: []
      parameters:
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 500, default: 100 }
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
            code:
              type: string
              example: AUTH_INVALID
            message:
              type: string
              example: Invalid username or password.
            details:
              type: object
              additionalProperties: true

    AdminLoginRequest:
      type: object
      required: [username, password]
      properties:
        username: { type: string, minLength: 1 }
        password: { type: string, minLength: 1 }

    AdminLoginResponse:
      type: object
      required: [adminId, username]
      properties:
        adminId: { type: string }
        username: { type: string }

    AuditEvent:
      type: object
      required: [id, occurredAt, adminId, eventType, sourceIp]
      properties:
        id: { type: string }
        occurredAt: { type: string, format: date-time }
        adminId: { type: string }
        eventType:
          type: string
          enum: [LOGIN_OK, LOGIN_FAIL, LOCKOUT, PUBLISH_OK, PUBLISH_FAIL, QUESTION_UPSERT]
        sourceIp: { type: string }
        metadata:
          type: object
          additionalProperties: true

    QuestionBank:
      type: object
      required: [schemaVersion, version, generatedAt, startQuestionId, questions]
      properties:
        schemaVersion:
          type: integer
          enum: [1]
        version:
          type: string
          description: Monotonic content version (e.g., yyyy.mm.dd-build)
        generatedAt:
          type: string
          format: date-time
        startQuestionId:
          type: string
        questions:
          type: array
          items: { $ref: "#/components/schemas/Question" }

    Question:
      type: object
      required: [id, prompt, choices, correctIndex, critical, inputMode]
      properties:
        id:
          type: string
          pattern: "^[A-Za-z0-9._-]{1,64}$"
        prompt:
          type: string
          minLength: 1
        choices:
          type: array
          minItems: 2
          maxItems: 6
          items: { type: string }
        correctIndex:
          type: integer
          minimum: 0
        critical:
          type: boolean
        inputMode:
          type: string
          enum: [multipleChoice, fractionInput]
        branchRules:
          type: array
          items: { $ref: "#/components/schemas/BranchRule" }
        media:
          type: object
          additionalProperties: false
          properties:
            imageUrl: { type: string }
            audioUrl: { type: string }

    BranchRule:
      type: object
      required: [condition, nextQuestionId]
      properties:
        condition:
          type: string
          description: e.g., "correct==true" or "criticalFail==true"
        nextQuestionId:
          type: string
```

```proto
// filename: internal.proto
syntax = "proto3";

package spacefractions.internal.v1;

// Internal contracts. Some interactions are in-process (SPA->Engine),
// but the message types are defined for deterministic testing and future split.

message ValidationError {
  string code = 1;        // e.g., "DENOM_ZERO", "NOT_INTEGER"
  string message = 2;
}

message FractionInput {
  int32 numerator = 1;
  int32 denominator = 2;
}

message VelocityAdjustment {
  double delta = 1;
  double newVelocity = 2;
}

message BranchRule {
  string condition = 1;
  string nextQuestionId = 2;
}

message Question {
  string id = 1;
  string prompt = 2;
  repeated string choices = 3;
  int32 correctIndex = 4;
  bool critical = 5;
  string inputMode = 6; // "multipleChoice" | "fractionInput"
  repeated BranchRule branchRules = 7;
}

message ScoreSnapshot {
  int32 correctCount = 1;
  int32 totalQuestions = 2;
  int32 scorePoints = 3;
  string rank = 4;
  string message = 5;
}

message SubmitAnswerRequest {
  string sessionId = 1;
  string questionId = 2;
  int32 choiceIndex = 3;
}

message SubmitAnswerResponse {
  bool correct = 1;
  bool pointsAwarded = 2;
  string nextQuestionId = 3; // empty if last
  ScoreSnapshot score = 4;
}

message PublishRequest {
  string adminId = 1;
  string changeNote = 2;
}

message PublishResponse {
  string version = 1;
  string etag = 2;
  string publishedAt = 3; // RFC3339
}

service ContentRepositoryService {
  rpc Publish(PublishRequest) returns (PublishResponse);
}
```

```yaml
# filename: k8s/web-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: spacefractions
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: sf-config
  namespace: spacefractions
data:
  NODE_ENV: "production"
  QBANK_PATH: "/data/qbank.json"
  CACHE_MAX_AGE_SECONDS: "60"
---
apiVersion: v1
kind: Secret
metadata:
  name: sf-secrets
  namespace: spacefractions
type: Opaque
stringData:
  SESSION_SECRET: "CHANGE_ME_IN_PROD"
  DATABASE_URL: "postgres://sf_admin:CHANGE_ME@postgres.spacefractions.svc.cluster.local:5432/sf"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sf-web
  namespace: spacefractions
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sf-web
  template:
    metadata:
      labels:
        app: sf-web
    spec:
      containers:
        - name: web
          image: ghcr.io/example/spacefractions-web:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: sf-config
            - secretRef:
                name: sf-secrets
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          volumeMounts:
            - name: qbank-data
              mountPath: /data
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 20
      volumes:
        - name: qbank-data
          persistentVolumeClaim:
            claimName: sf-qbank-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: sf-qbank-pvc
  namespace: spacefractions
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Service
metadata:
  name: sf-web
  namespace: spacefractions
spec:
  selector:
    app: sf-web
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sf-web-hpa
  namespace: spacefractions
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sf-web
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```sql
-- filename: sql/admin_users_ddl.sql
CREATE TABLE IF NOT EXISTS admin_users (
  id              UUID PRIMARY KEY,
  username        TEXT NOT NULL UNIQUE,
  password_hash   TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  disabled_at     TIMESTAMPTZ NULL,
  last_login_at   TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username);
```

```sql
-- filename: sql/admin_sessions_ddl.sql
CREATE TABLE IF NOT EXISTS admin_sessions (
  id            UUID PRIMARY KEY,
  admin_user_id UUID NOT NULL REFERENCES admin_users(id),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at    TIMESTAMPTZ NOT NULL,
  revoked_at    TIMESTAMPTZ NULL,
  source_ip     INET NULL,
  user_agent    TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_admin_sessions_admin_user_id ON admin_sessions(admin_user_id);
CREATE INDEX IF NOT EXISTS idx_admin_sessions_expires_at ON admin_sessions(expires_at);
```

```sql
-- filename: sql/audit_log_ddl.sql
CREATE TABLE IF NOT EXISTS audit_log (
  id          UUID PRIMARY KEY,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  admin_user_id UUID NULL REFERENCES admin_users(id),
  event_type  TEXT NOT NULL,
  source_ip   INET NULL,
  metadata    JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_audit_log_occurred_at ON audit_log(occurred_at);
CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
```

```sql
-- filename: sql/question_bank_versions_ddl.sql
CREATE TABLE IF NOT EXISTS question_bank_versions (
  version       TEXT PRIMARY KEY,
  etag          TEXT NOT NULL,
  published_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_by  UUID NULL REFERENCES admin_users(id),
  change_note   TEXT NOT NULL
);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
FR-001,Web-based interactive learning tool,Container: SPA/Umbrella; Deployment: StudentDevice,SpaceFractionsSPA; MathUmbrellaWeb,architecture.md,Delivers interactive learning in browser
FR-002,Intro autoplay + click-to-skip,UseCase: UC_PlayIntro/UC_SkipIntro; State: IntroPlaying,MenuController; SpaceFractionsSPA,architecture.md,Implements intro flow and skip event
FR-003,Main menu with help + links,UseCase: UC_ViewHelp; Activity: ShowMainMenu,MathUmbrellaWeb; MenuController,architecture.md,Ensures navigation and instructions
FR-004,Question sequence in storyline,Sequence_S1_Gameplay loop; State: InQuestion,GameSession; QuestionBank,architecture.md,Content-driven progression
FR-005,Incorrect => retry no points,State: IncorrectFeedback; Activity: LockPointsForQuestion,GameSession; ScoreBoard,architecture.md,Learning-friendly scoring
FR-006,Sounds/animations feedback,Class: FeedbackAnimator,RenderAudioUI,architecture.md,Immediate reinforcement
FR-007,Sidekick hints,UseCase: UC_GetHint; Class: SidekickAssistant,SidekickAssistant,architecture.md,Guidance for usability/learning
FR-008,Branching critical points,Class: BranchRule; State: BranchDecision,GameEngine; QuestionBank,architecture.md,Adaptive narrative
FR-009,Ending scene with replay/exit,UseCase: UC_ViewResults/UC_ReplayExit,GameSession; ScoreBoard,architecture.md,Session conclusion
FR-010,Score ranked with message,Class: ScoreBoard methods,GameEngine,architecture.md,Deterministic rank/message
FR-011,Single user per instance; many online,Deployment note ASR-002,SpaceFractionsSPA,architecture.md,Local session state + stateless hosting
FR-012,Admin web updater with password,UseCase: UC_AdminLogin; Sequence_S2_AdminUpdate,AdminUpdaterWeb; AdminBackendAPI,openapi.yaml,Secure admin entrypoint
FR-013,Edit/publish questions saved to server file,Component: QuestionBankFileStore; Sequence_S2,AdminBackendAPI; QuestionBankFileStore,openapi.yaml; sql/question_bank_versions_ddl.sql,Atomic publish + persistence
FR-014,External resources open separately,UseCase note UC_OpenExternal,MathUmbrellaWeb,architecture.md,Maintains game context
FR-015,Mouse-only input,Activity: GetAnswer(mouse click),SpaceFractionsSPA,architecture.md,Simplifies interaction
FR-016,Fraction validation denom!=0,Class: FractionInputValidator,GameEngine,architecture.md,Prevents invalid physics update
FR-017,Fraction to decimal velocity adjust,Class: FractionConverter/PhysicsEngine,PhysicsEngine,architecture.md,Implements learning mechanic
FR-018,Invalid input error message,Activity: ShowErrorMessage,UI,architecture.md,User guidance
NFR-003,Browser compatibility,Deployment note NFR-003,SpaceFractionsSPA,architecture.md,Supports broad access
NFR-004,Usability mouse-driven,Package: ui note,UI,architecture.md,Child-friendly UX
NFR-006,Real-time velocity update,Class note PhysicsEngine,PhysicsEngine,architecture.md,Low-latency local compute
NFR-007,Reliability via testing,SRS statement,All,architecture.md,Automated tests/monitoring
NFR-008,HTTPS pw>=12 lockout 5,UseCase note UC_AdminLogin,AuthSessionService,openapi.yaml; sql/admin_users_ddl.sql,Explicit security controls
NFR-010,Load-time/bandwidth constraints,Container note ASR-006/NFR-010,StaticAssetHost; SPA,architecture.md,Progressive load and caching
ASR-001,No plugins HTML5,Activity note ASR-001,SpaceFractionsSPA,architecture.md,Removes Flash dependency
ASR-002,Session-local score/state,UseCase note UC_ViewResults,GameEngine,architecture.md,Prevents cross-user leakage
ASR-003,Deterministic invariant behavior,Package note domain,GameEngine,architecture.md,Consistent logic across browsers
ASR-004,Versioned JSON schema + TTL/ETag + atomic write,Component note ContentLoader,ContentLoader; QuestionBankRepository,openapi.yaml; sql/question_bank_versions_ddl.sql,Updatable content with bounded staleness
ASR-005,Secure auth/session + audit,Component note AdminBackendAPI,AuthSessionService; AuditLogService,sql/audit_log_ddl.sql; sql/admin_sessions_ddl.sql,Accountability and secure admin ops
ASR-006,Progressive loading/media constraints,Container note SPA,StaticAssetHost; SPA,architecture.md,Meets slow-network constraints
INF-FR-UMB-001,Umbrella categorized links,UseCase: UC_LaunchMenu/UC_OpenProject,MathUmbrellaWeb,architecture.md,Topic hub
INF-FR-EXT-001,Denominators web page link,SRS menu text,MathUmbrellaWeb,architecture.md,External resource integration
INF-NFR-AVAIL-001,Availability target implied,SRS reliability statement,WebServer,architecture.md,Define SLOs and monitoring
INF-NFR-SCALE-001,Many concurrent users,SRS internet access,StaticAssetHost,architecture.md,Stateless scale + CDN
INF-NFR-PERF-001,Modem-friendly downloads,SRS download constraints,StaticAssetHost,architecture.md,Asset budgets + compression
INF-NFR-SEC-001,Replace vague security with explicit,SRS security text,AuthSessionService,architecture.md,Testable controls
INF-FR-AUD-001,Audit privileged publish,Sequence_S2_AdminUpdate: AuditLogger,AuditLogService,sql/audit_log_ddl.sql,Forensics and governance
```

---

## Verification / Acceptance Criteria Checklist

| Item | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | Yes |
| [ ] Sections A-L included. | Yes |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | Yes (including inferred INF-*) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | Yes (`openapi.yaml`, `internal.proto`) |
| [ ] Representative k8s manifest snippet included. | Yes (`k8s/web-deployment.yaml`) |
| [ ] SQL DDL / NoSQL models for primary entities included. | Yes (`sql/*.sql`) |
| [ ] All major components have at least one API contract and a data schema. | Yes (OpenAPI schemas + proto + SQL) |
| [ ] Assumptions and unresolved questions listed. | Yes (Section K) |

---

## How to review (checklist)
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?