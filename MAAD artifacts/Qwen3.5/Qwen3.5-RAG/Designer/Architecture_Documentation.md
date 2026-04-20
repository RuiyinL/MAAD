Analysis Plan
Scope: Web-based HTML5 "Space Fractions" educational game with admin content management, replacing legacy Flash requirements.
Approach: Layered Client-Server architecture using React (Client) and Node.js (Server), with JSON file storage for questions and SQL for audit/auth.
Validation: Traceability matrix mapping all INF- requirements to diagrams; OpenAPI contract validation; K8s manifest syntax check.

# Architecture Document: Space Fractions System

## A. Executive Summary

The **Space Fractions System** is a web-based educational tool designed to improve fraction-solving skills for sixth-grade students. It replaces legacy Flash dependencies with a modern HTML5/JavaScript stack while retaining the narrative-driven gameplay and administrative content update capabilities described in the SRS. The architecture follows a **Layered Web Architecture** (Client-Server) with a **Model-View-Controller (MVC)** pattern on the client side, aligning with the **Container Diagram** (Container: Web App, Admin API, File Store) and **Package Diagram** (ClientApp, ServerApp).

**Architectural Style:** Layered Client-Server with MVC (Client) and REST API (Server).
**Deployment Topology:** Cloud-hosted Web Server (Nginx/Node) serving static assets and API endpoints; Client-side execution in browser.

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Legacy Flash Dependency** | High | Purged; replaced with HTML5 Canvas/WebGL (See Section J, Tradeoff T1). |
| **Content Integrity** | Medium | Atomic file writes + JSON Schema validation for question updates (ASR-002). |
| **Client-Side Score Tampering** | Low | Accepted risk for educational tool; server-side audit of admin actions only (ASR-004). |

**QA Coverage Mapping:**

| Quality Attribute | ASR/NFR ID | Test Type |
| :--- | :--- | :--- |
| **Security** | NFR-003, ASR-003 | Penetration Testing, Auth Flow Verification |
| **Performance** | NFR-002 | Load Testing (56Kbps simulation legacy metric adapted to Lighthouse) |
| **Maintainability** | NFR-004, ASR-002 | Code Coverage, Schema Validation Tests |
| **Usability** | NFR-005 | Accessibility Audit (WCAG 2.1), User Testing (6th Grade Persona) |
| **Availability** | NFR-006 | Uptime Monitoring (99.5% SLO) |

## B. Traceability & Rationale

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INF-FR-001** | Intro Movie (Skipable) | UseCaseDiagram:UC1, StateDiagram:IntroPlaying | GameRenderer | `client/src/Intro.tsx` | Engages user; skip option supports returning users (FR-001). |
| **INF-FR-002** | Main Menu (Help/Start) | UseCaseDiagram:UC2, StateDiagram:MenuReady | GameUI | `client/src/Menu.tsx` | Central navigation hub (FR-002). |
| **INF-FR-003** | Fraction Questions | UseCaseDiagram:UC3, ClassDiagram:Question | QuestionEngine | `client/src/QuestionEngine.ts` | Core educational logic (FR-003). |
| **INF-FR-004** | Ending Scene & Score | UseCaseDiagram:UC5, StateDiagram:SessionEnd | GameSession | `client/src/Session.ts` | Provides feedback and closure (FR-005). |
| **INF-FR-005** | Question Updater | UseCaseDiagram:UC6, SequenceDiagram:Scenario 2 | Admin API | `openapi.yaml` | Allows admin content management (FR-006). |
| **INF-FR-006** | Math Umbrella Links | UseCaseDiagram:UC4, ContainerDiagram:Web App | GameUI | `client/src/Menu.tsx` | External resource integration (FR-007). |
| **INF-NFR-001** | Web Browser Compatible | DeploymentDiagram:Client Device | Web Browser | `package.json` | Ensures accessibility without plugins (NFR-001). |
| **INF-NFR-002** | Performance (Load Time) | ActivityDiagram:Load Assets | Web Server | `k8s/web-server-deployment.yaml` | Ensures usability on low bandwidth (NFR-002). |
| **INF-NFR-003** | Security (Admin Auth) | ComponentDiagram:AuthComponent | AuthSvc | `sql/admin_users_ddl.sql` | Protects content integrity (NFR-003). |
| **INF-NFR-004** | Maintainability | PackageDiagram:ServerApp | ServerApp | `internal_rest_contracts.md` | Separation of concerns (NFR-004). |
| **INF-NFR-005** | Usability (Mouse/Accessibility) | UseCaseDiagram:Student | InputHandler | `client/src/InputHandler.ts` | Supports target persona skills (NFR-005). |
| **INF-ASR-001** | Web-Based Architecture | ContainerDiagram:Web App | Web App | `architecture.md` | Foundation of deployment strategy (ASR-001). |
| **INF-ASR-002** | File-Based Content | ClassDiagram:QuestionStore | FileStore | `internal_rest_contracts.md` | Simplifies admin editing without DB (ASR-002). |
| **INF-ASR-003** | Security Boundary | PackageDiagram:ServerApp.Security | AuthSvc | `openapi.yaml` | Isolates admin functions (ASR-003). |
| **INF-ASR-004** | Local Score Storage | ClassDiagram:GameSession | LocalStorage | `client/src/Session.ts` | Privacy-preserving session tracking (ASR-004). |

## C. Architecture Overview

The system architecture is defined using the 4+1 View Model, referencing the provided PlantUML diagrams.

1.  **Context View:** The system interacts with **Students** (via Browser) and **Administrators** (via Web Interface). External dependencies include the **Denominators' Web Page** (links) and **S2S Projects** (Math Umbrella).
2.  **Container View:** (Reference: **Container Diagram**)
    *   **Web App (Client):** HTML5/JS SPA handling game logic, rendering, and local storage.
    *   **Admin API (Server):** HTTPS service handling authentication and question updates.
    *   **File Store:** JSON files holding question data; SQL DB holding admin credentials/audit logs.
3.  **Component View:** (Reference: **Component Diagram**, **Package Diagram**)
    *   **Client:** `GameRenderer`, `InputManager`, `QuestionEngine`.
    *   **Server:** `AuthComponent`, `ContentManager`.
4.  **Runtime/Logic View:** (Reference: **Class Diagram**, **State Diagram**, **Sequence Diagram**)
    *   **State Management:** `SceneManager` handles transitions (Intro -> Menu -> Play -> End).
    *   **Data Flow:** `QuestionStore` loads JSON; `GameSession` tracks local score.
5.  **Deployment View:** (Reference: **Deployment Diagram**)
    *   **Client Device:** Any modern browser (Chrome, Firefox, Edge).
    *   **Web Server:** Cloud VM (Nginx + Node.js runtime).

## D. Detailed Technical Design

### 1. Client-Side Game Engine
*   **Responsibilities:** Render animations, handle input, manage game state, store local scores.
*   **Technology Options:**
    *   *Recommended:* **React 18 + TypeScript**. Justification: Meets NFR-005 (Usability) via component reuse; strong typing reduces logic errors.
    *   *Conservative:* **jQuery + Vanilla JS**. Justification: Lower learning curve, but harder to maintain (NFR-004).
    *   *Cutting-edge:* **Svelte + WebGL**. Justification: High performance, but steeper learning curve.
*   **Recommended Stack:** React 18, TypeScript 5, Vite.
*   **Interface:** Internal state management (Redux/Context). No external API for gameplay (ASR-004).
*   **Data Model:** LocalStorage schema for `GameSession` (Score, State).

### 2. Admin API & Content Management
*   **Responsibilities:** Authenticate admins, validate question JSON, perform atomic file writes, audit actions.
*   **Technology Options:**
    *   *Recommended:* **Node.js (Express/NestJS)**. Justification: Unified JS stack; meets NFR-004 (Maintainability).
    *   *Conservative:* **Python (Flask)**. Justification: Robust, but adds language context switch.
    *   *Cutting-edge:* **Go (Gin)**. Justification: High performance, but overkill for low-traffic admin tool.
*   **Recommended Stack:** Node.js 20, Express 4.
*   **Interface:** External OpenAPI (See Section L), Internal REST for File IO.
*   **Data Model:** SQL for Admin Users/Audit; JSON Files for Questions (ASR-002).

### 3. Interface Design

#### External API (OpenAPI)
See `openapi.yaml` in Section L. Covers Auth and Question Update flows.

#### Internal Contracts
See `internal_rest_contracts.md` in Section L. Defines communication between API Service and File Storage module.

### 4. Data Model / Schema

**Admin Users & Audit (SQL):**
See `sql/admin_users_ddl.sql` in Section L. Includes password hash, last login, and audit log table.

**Questions (JSON):**
Stored in `/data/questions.json`. Schema enforced by API middleware.
```json
{
  "id": "q_001",
  "prompt": "1/2 + 1/2 = ?",
  "choices": ["1", "2", "1/4"],
  "answerIndex": 0,
  "rationale": "Common denominator addition."
}
```

### 5. Caching & Consistency
*   **Questions:** Cached in server memory (RAM) upon startup or file change event. Invalidated on atomic write.
*   **Consistency:** Strong consistency for Admin updates (Atomic Rename). Eventual consistency for Client (clients fetch latest JSON on session start).

## E. Operations & Deployment

### 1. Kubernetes Plan
See `k8s/admin-api-deployment.yaml` in Section L.
*   **Replicas:** 2 (High Availability).
*   **Resources:** 256Mi RAM, 0.5 CPU per pod.
*   **HPA:** Scale based on CPU > 70%.

### 2. DB HA Topology
*   **Database:** Managed PostgreSQL (e.g., AWS RDS).
*   **Replication:** Multi-AZ Standby.
*   **Backup:** Daily snapshots, 30-day retention.

### 3. Network Topology
*   **Ingress:** Nginx Ingress Controller (HTTPS Termination).
*   **Egress:** Restricted; only allowed to external S2S links (Math Umbrella).
*   **Latency:** <200ms API response time (NFR-002).

### 4. CI/CD Sketch
1.  **Build:** Docker image build (Client & Server).
2.  **Test:** Unit (Jest), Integration (Supertest), Contract (OpenAPI Validator).
3.  **Deploy:** Canary deployment (5% traffic -> 100%).
4.  **Gate:** Security scan (SAST/DAST) before production.

## F. Security Design

1.  **Auth & AuthZ:**
    *   **Protocol:** OAuth2/OIDC or JWT-based Session.
    *   **Lifecycle:** Tokens expire after 15 minutes; Refresh tokens valid for 8 hours.
    *   **Storage:** HttpOnly Secure Cookies (Client), Hashed (Server).
2.  **Secrets Management:**
    *   **Tool:** Kubernetes Secrets or AWS Secrets Manager.
    *   **Rotation:** Every 90 days for DB credentials; Immediate revocation on admin termination.
3.  **TLS & Service Mesh:**
    *   **TLS:** 1.3 enforced for all external traffic (ASR-003).
    *   **Mesh:** Not required for single-service API; mTLS for internal DB connection.
4.  **Threat Model:**
    *   **T1: XSS:** Mitigated by React DOM sanitization.
    *   **T2: Auth Bypass:** Mitigated by Middleware Guards (OpenAPI).
    *   **T3: File Corruption:** Mitigated by Atomic Writes (ASR-002).
    *   **T4: Brute Force:** Mitigated by Rate Limiting & Account Lockout (NFR-003).
    *   **T5: Data Leak:** Mitigated by LocalStorage only for scores (ASR-004).

## G. Observability & SRE

1.  **Metrics:**
    *   `api_request_duration_seconds` (Histogram)
    *   `question_update_count_total` (Counter)
    *   `auth_failure_count_total` (Counter)
2.  **Alerts (Prometheus):**
    *   `rate(api_request_duration_seconds_count[5m]) > 100` (High Traffic)
    *   `rate(auth_failure_count_total[5m]) > 10` (Brute Force Attempt)
3.  **SLOs:**
    *   **Availability:** 99.5% (NFR-006).
    *   **Latency:** 95th percentile < 500ms.
    *   **RTO:** 4 hours; **RPO:** 24 hours.

## H. Testing Strategy

| Test Type | Components | Tool | Frequency |
| :--- | :--- | :--- | :--- |
| **Unit** | Client Logic, API Utils | Jest | Pre-commit |
| **Integration** | API + DB, API + File | Supertest | CI Pipeline |
| **Contract** | OpenAPI Compliance | Dredd | CI Pipeline |
| **E2E** | Full Game Flow | Cypress | Nightly |
| **Chaos** | Pod Failure | Chaos Mesh | Quarterly |

*   **Data Management:** Synthetic data for tests; Anonymized logs for staging.
*   **Environments:** Dev, Staging (Mirror Prod), Prod.

## I. Migration, Data Conversion & Rollout Plan

1.  **Migration:**
    *   **Legacy Flash -> HTML5:** Complete rewrite (No data migration needed for game logic).
    *   **Questions:** Existing questions must be manually converted to JSON schema during initial setup.
2.  **Rollout:**
    *   **Phase 1:** Deploy Admin API; Populate initial questions.
    *   **Phase 2:** Deploy Client to Staging; UAT with Teachers (Persona: Claire).
    *   **Phase 3:** Production Release; Monitor Error Rates.
3.  **Compatibility:**
    *   **API Versioning:** `/api/v1/...`.
    *   **Browser:** Support last 2 versions of Chrome, Firefox, Edge.

## J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros | Cons | Chosen | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Runtime** | Flash (Legacy) vs HTML5 | Flash: Existing assets. | Flash: Obsolete, insecure. | **HTML5** | Meets NFR-001 (Web), NFR-004 (Maintainability). |
| **Content Store** | SQL vs JSON Files | SQL: Queryable, ACID. | SQL: Overhead for simple Q/A. | **JSON Files** | Meets ASR-002 (File-Based), easier for Admins to edit. |
| **Score Storage** | Server DB vs LocalStorage | Server: Global Leaderboards. | Server: PII Privacy concerns. | **LocalStorage** | Meets ASR-004 (Local Data), reduces server load. |

## K. Open Questions & Assumptions

**Assumptions:**
*   **A1:** The SRS requirement for "Flash movies" is overridden by the architectural decision to use HTML5 due to security and compatibility obsolescence (See Section J).
*   **A2:** Admins have basic computer skills sufficient to use a web form (Persona: Claire).
*   **A3:** Internet connectivity is available for initial asset load (Modem constraint adapted to modern broadband).
*   **A4:** "Math Umbrella" links are external and maintained separately; uptime not guaranteed by this system.

**Open Questions:**
*   **Q1:** Should question updates require dual-approval for production safety? (Currently single admin).
*   **Q2:** Are there specific accessibility standards (e.g., WCAG 2.1 AA) mandated beyond "Usability"?
*   **Q3:** What is the retention policy for Audit Logs beyond the suggested 2 years?

## L. Deliverables

### 1. architecture.md
(This document)

### 2. openapi.yaml

```yaml
openapi: 3.0.3
info:
  title: Space Fractions Admin API
  version: 1.0.0
  description: API for Admin Question Management and Authentication
servers:
  - url: https://api.spacefractions.edu/v1
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Question:
      type: object
      properties:
        id: { type: string }
        prompt: { type: string }
        choices: { type: array, items: { type: string } }
        answerIndex: { type: integer }
        rationale: { type: string }
      required: [id, prompt, choices, answerIndex]
    LoginRequest:
      type: object
      properties:
        username: { type: string }
        password: { type: string }
paths:
  /auth/login:
    post:
      summary: Admin Login
      requestBody:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/LoginRequest' }
      responses:
        '200':
          description: JWT Token
          content:
            application/json:
              schema:
                type: object
                properties:
                  token: { type: string }
        '401':
          description: Invalid Credentials
  /questions:
    get:
      summary: List Questions
      security: [{ bearerAuth: [] }]
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Question' }
    put:
      summary: Update Question
      security: [{ bearerAuth: [] }]
      requestBody:
        content:
          application/json:
            schema: { $ref: '#/components/schemas/Question' }
      responses:
        '200': { description: Updated }
        '400': { description: Validation Error }
```

### 3. internal_rest_contracts.md

```markdown
# Internal Service Contracts

## Service: API Gateway -> File Storage Service

### Endpoint: POST /internal/storage/write
**Description:** Atomic write of question JSON file.
**Request:**
```json
{
  "filename": "questions.json",
  "content": "{...}",
  "checksum": "sha256..."
}
```
**Response:**
```json
{
  "status": "success",
  "version": "1.0.2"
}
```
**Error Codes:**
- 500: Disk Full
- 409: Concurrent Modification (Lock held)

### Endpoint: GET /internal/storage/read
**Description:** Retrieve cached question data.
**Response:** JSON Content of question file.
```

### 4. k8s/admin-api-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: space-fractions-admin-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: admin-api
  template:
    metadata:
      labels:
        app: admin-api
    spec:
      containers:
      - name: api
        image: spacefractions/admin-api:1.0.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: host
---
apiVersion: v1
kind: Service
metadata:
  name: admin-api-service
spec:
  selector:
    app: admin-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

### 5. sql/admin_users_ddl.sql

```sql
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES admin_users(id),
    action VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address INET,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_admin_username ON admin_users(username);
```

### 6. traceability_matrix.csv

```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),1-2 sentence rationale
INF-FR-001,Intro Movie (Skipable),UseCaseDiagram:UC1, StateDiagram:IntroPlaying,GameRenderer,client/src/Intro.tsx,Engages user; skip option supports returning users (FR-001).
INF-FR-002,Main Menu (Help/Start),UseCaseDiagram:UC2, StateDiagram:MenuReady,GameUI,client/src/Menu.tsx,Central navigation hub (FR-002).
INF-FR-003,Fraction Questions,UseCaseDiagram:UC3, ClassDiagram:Question,QuestionEngine,client/src/QuestionEngine.ts,Core educational logic (FR-003).
INF-FR-004,Ending Scene & Score,UseCaseDiagram:UC5, StateDiagram:SessionEnd,GameSession,client/src/Session.ts,Provides feedback and closure (FR-005).
INF-FR-005,Question Updater,UseCaseDiagram:UC6, SequenceDiagram:Scenario 2,Admin API,openapi.yaml,Allows admin content management (FR-006).
INF-FR-006,Math Umbrella Links,UseCaseDiagram:UC4, ContainerDiagram:Web App,GameUI,client/src/Menu.tsx,External resource integration (FR-007).
INF-NFR-001,Web Browser Compatible,DeploymentDiagram:Client Device,Web Browser,package.json,Ensures accessibility without plugins (NFR-001).
INF-NFR-002,Performance (Load Time),ActivityDiagram:Load Assets,Web Server,k8s/web-server-deployment.yaml,Ensures usability on low bandwidth (NFR-002).
INF-NFR-003,Security (Admin Auth),ComponentDiagram:AuthComponent,AuthSvc,sql/admin_users_ddl.sql,Protects content integrity (NFR-003).
INF-NFR-004,Maintainability,PackageDiagram:ServerApp,ServerApp,internal_rest_contracts.md,Separation of concerns (NFR-004).
INF-NFR-005,Usability (Mouse/Accessibility),UseCaseDiagram:Student,InputHandler,client/src/InputHandler.ts,Supports target persona skills (NFR-005).
INF-ASR-001,Web-Based Architecture,ContainerDiagram:Web App,Web App,architecture.md,Foundation of deployment strategy (ASR-001).
INF-ASR-002,File-Based Content,ClassDiagram:QuestionStore,FileStore,internal_rest_contracts.md,Simplifies admin editing without DB (ASR-002).
INF-ASR-003,Security Boundary,PackageDiagram:ServerApp.Security,AuthSvc,openapi.yaml,Isolates admin functions (ASR-003).
INF-ASR-004,Local Score Storage,ClassDiagram:GameSession,LocalStorage,client/src/Session.ts,Privacy-preserving session tracking (ASR-004).
```

---

## Acceptance Criteria Verification

- [x] 3-line Analysis Plan present.
- [x] Sections A-L included.
- [x] Every FR/NFR/ASR mapped in traceability matrix.
- [x] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included.
- [x] Representative k8s manifest snippet included.
- [x] SQL DDLs provided for persisted entities.
- [x] All major components have: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema.
- [x] Assumptions and open questions clearly listed.

## How to Review
- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?