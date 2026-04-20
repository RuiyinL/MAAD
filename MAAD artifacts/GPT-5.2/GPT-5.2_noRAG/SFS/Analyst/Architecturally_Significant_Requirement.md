# Architecturally Significant Requirements Results

[ASR-001]: Standards-Based Web Architecture (Replace Flash/Plugins)
**Description**: The Space Fractions system shall use HTML5 and JavaScript to deliver interactive content and animations, ensuring compatibility with all modern browsers. [Owner: Not specified; Next action: Revise architecture and implementation stack to eliminate all Flash dependencies.]
  
**Architectural Impact:**  
- Forces client technology selection (HTML5/JS rendering, audio, animation).
- Drives rewrite of media/animation pipeline and UI components (intro, feedback, menus).
- Impacts test strategy (cross-browser matrix) and asset delivery.

**Quality Attributes Affected:**  
Compatibility, Maintainability, Portability, Security

**Architectural Constraints:**  
- Must run without browser plugins.
- Must support current mainstream browsers (per defined matrix).

**Rationale:**  
Technology choice is a dominant constraint affecting nearly every component; Flash is obsolete and conflicts with maintainability/compatibility goals.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003
- **Conflicts with:** (Original SRS Flash dependency)
---

[ASR-002]: Client-Heavy App with Local Session State for Scoring (Single-User-per-Instance)
**Description**: “Only one person can use a single instance… The user’s score must be kept as local data within the Space Fractions system… so that the results may be given at the end… more than one user can access the product and download its content for use on their computer.”
  
**Architectural Impact:**
- Drives where state lives (in-browser session memory vs server persistence).
- Enables scalable static hosting for many concurrent users while preventing cross-user score leakage.

**Quality Attributes Affected:**
Scalability, Privacy, Reliability

**Architectural Constraints:**
- Score/state must be session-scoped on the client; no shared/global score state across users by default.

**Rationale:**
State placement and concurrency model materially affect architecture and security boundaries.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-015, NFR-001
- **Conflicts with:** Any future requirement to store user progress centrally (not specified)
---

[ASR-003]: Environment-Invariant Behavior Across Browsers
**Description**: “Various environments may yield different interfaces, but the behavior of the program will be the same.”
  
**Architectural Impact:**
- Encourages separation of core game logic (validation/scoring/branching) from presentation layer.
- Requires cross-browser regression testing and deterministic logic.

**Quality Attributes Affected:**
Portability, Reliability, Testability

**Architectural Constraints:**
- Core rules/logic must be implemented in a platform-consistent layer with repeatable outputs.

**Rationale:**
Cross-environment behavioral invariance is cross-cutting and requires explicit architectural layering and testing discipline.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003, NFR-005
- **Conflicts with:** Not specified
---

[ASR-004]: Admin Question Updater + Server-Side Content Persistence Contract
**Description**: “A component accessible over the World Wide Web will allow the series of fraction questions to be updated by an administrator… This information must be saved in a file on the web server… easily edited through simplified administrative screens… the system sequence can dynamically read and incorporate [updates] into the gameplay.”
  
**Architectural Impact:**
- Requires a backend/admin subsystem distinct from the game client.
- Requires a defined content format/schema and validation to prevent runtime failures.
- Requires atomic writes/versioning and safe read patterns for the live game.

**Quality Attributes Affected:**
Maintainability, Modifiability, Reliability, Security

**Architectural Constraints:**
- Web-accessible admin interface.
- Server-side persistent storage for question bank (file-based per SRS).
- Runtime-readable question data by the gameplay component.

**Rationale:**
Introduces a major subsystem boundary (admin vs gameplay) and a durable data contract affecting runtime behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013, NFR-007, NFR-009
- **Conflicts with:** Not specified
---

[ASR-005]: Secure Administrative Operations (Auth + HTTPS + Auditability)
**Description**: SRS: “updater page… asks for a password” and “secure as the web browser.” Applied decision: “HTTPS-only… bcrypt/Argon2… server-side sessions… audit logging… session expiry… lockout/rate limiting…”
  
**Architectural Impact:**
- Adds cross-cutting security services: authentication, session management, transport security.
- Requires audit logging around privileged content changes.

**Quality Attributes Affected:**
Security, Integrity, Accountability

**Architectural Constraints:**
- Admin endpoints must require authentication.
- Transport must be encrypted (HTTPS).
- Credential storage must be hashed; privileged actions should be logged.

**Rationale:**
Security for administrative modification is high-risk and affects multiple components (UI, backend, storage).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013, NFR-007, NFR-008
- **Conflicts with:** Not specified
---

[ASR-006]: Bandwidth/Load-Time Constraints for Media-Rich Web Delivery
**Description**: “Introductory and main menu movies… downloaded in approximately one minute with a modem connection… main system can be played within a few minutes… Flash movies do not have to be fully downloaded to play…”
  
**Architectural Impact:**
- Drives asset size budgets, compression, and progressive loading/streaming strategies.
- Influences how animations/audio are packaged and delivered in the standards-based stack.

**Quality Attributes Affected:**
Performance, User Experience

**Architectural Constraints:**
- Must support low-bandwidth startup/playability expectations (as stated) via progressive delivery.

**Rationale:**
Performance constraints shape front-end delivery architecture and content pipeline.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-010, ASR-001
- **Conflicts with:** FR-008 (increased branching media can violate load budgets)
---