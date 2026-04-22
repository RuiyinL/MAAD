# Architecturally Significant Requirements Results

[ASR-001]: Web-based interactive system deployable over the Internet  
**Description**: “The product will be a web-based, interactive system.” / “The Space Fractions system will be available over the Internet via the S2S website.”  
**Architectural Impact:**  
- Forces a browser-delivered application architecture (client runtime, HTTP(S) delivery, static assets).  
- Drives deployment model (web hosting, routing, CDN considerations) and cross-browser compatibility testing.  

**Quality Attributes Affected:** Portability, Availability, Deployability, Usability  

**Architectural Constraints:** Must be accessible via standard web delivery over the Internet (no local-only install assumption).  

**Rationale:** Strong platform/deployment constraint affecting most design decisions.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** None specified
---

[ASR-002]: Client runtime/technology dependency for media execution (modern web standards)  
**Description**: (Derived from ASR-002) Introductory movie, animation, and all sound must use MP4/WebM/OGG (for video), MP3/WAV (sound), Canvas/SVG for animation, and UI playground must be built in ReactJS, Vue, or comparable, with no plugin dependencies. Owner: Architect; Next action: Hold architecture sign-off until all requirements reference only modern web technologies in alignment with NFR-001.  
**Architectural Impact:**  
- Constrains UI rendering, animation/audio pipeline, asset packaging, and browser support strategy.  
- Impacts maintainability and compatibility; may require technology substitution to remain deployable.  

**Quality Attributes Affected:** Compatibility, Security, Maintainability, Portability  

**Architectural Constraints:** Must use HTML5 video/audio formats and Canvas/SVG for animation; UI implemented in a modern JS framework (React/Vue or comparable); no plugins.  

**Rationale:** Technology constraint is a primary architectural driver and a high-risk constraint.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-010, NFR-003
---

[ASR-003]: Environment-invariant behavior across browsers/configurations  
**Description**: “various environments may yield different interfaces, but the behavior of the program will be the same.”  
**Architectural Impact:**  
- Encourages separation of core game logic (scoring, branching, validation) from presentation.  
- Requires cross-browser determinism strategy (shared logic module, regression tests, avoiding undefined browser behaviors).  

**Quality Attributes Affected:** Portability, Correctness, Reliability  

**Architectural Constraints:** Core behavior must be consistent across supported environments despite UI differences.  

**Rationale:** Cross-cutting correctness/portability requirement influencing code structure and test strategy.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003, NFR-005
- **Conflicts with:** None specified
---

[ASR-004]: Admin-updatable question bank via web interface with server-side file persistence  
**Description**: “a component accessible over the World Wide Web will allow the series of fraction questions to be updated by an administrator…” / “must be saved in a file on the web server… easily edited through simplified administrative screens.”  
**Architectural Impact:**  
- Requires an admin subsystem, authentication, server-side persistence mechanism, and a content contract readable by the game.  
- Introduces backend endpoints/pages and storage format decisions (file vs DB), plus validation and compatibility concerns.  

**Quality Attributes Affected:** Maintainability, Modifiability, Security, Reliability  

**Architectural Constraints:** Must persist question data to a server-hosted file and support remote admin edits via web UI.  

**Rationale:** Adds a privileged management plane and persistence/read-path that shapes system decomposition.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017, FR-018, NFR-010
- **Conflicts with:** None specified
---

[ASR-005]: Dynamic incorporation of updated questions during runtime (no restart) with rollback on invalid update  
**Description**: (Derived from ASR-005) “system sequence can dynamically read and incorporate… real-time updates… without the need for system restarts or interruptions.” Each questions.json file includes schemaVersion; updates failing validation atomically rollback to last-good file; admin notified by email/log. Owner: DevOps/QA; Next action: Add schema version/rollback/alert spec in admin subsystem.  
**Architectural Impact:**  
- Requires runtime content loading strategy (cache control, polling/refresh, versioning) and backward-compatible content schema.  
- Adds failure-mode handling when content is partially updated or invalid.  

**Quality Attributes Affected:** Availability, Reliability, Performance, Maintainability  

**Architectural Constraints:** Content updates must become visible to gameplay without restarting the system; invalid updates must be rejected with fallback to prior valid version and admin alerting; question file must include schemaVersion.  

**Rationale:** Non-trivial runtime update capability impacts client/server communication and content lifecycle.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-018
- **Conflicts with:** NFR-009 (bandwidth/load-time expectations may be impacted by frequent refresh)
---

[ASR-006]: Session-local score storage (no stated server persistence for player results)  
**Description**: “The user's score must be kept as local data within the Space Fractions system so that the results may be given at the end…” / “Only one person can use a single instance…”  
**Architectural Impact:**  
- Drives state management to the client session (in-memory/local state) rather than centralized server storage.  
- Influences privacy and scalability (stateless server delivery for gameplay).  

**Quality Attributes Affected:** Scalability, Privacy, Reliability  

**Architectural Constraints:** Player score/progress is maintained locally within the running instance for end-of-game feedback.  

**Rationale:** State placement is a core architectural decision affecting backend needs and concurrency behavior.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, NFR-008
- **Conflicts with:** None specified
---

[ASR-007]: Password-protected administrative access  
**Description**: (Derived from ASR-007) “She navigates to the updater page, which asks for a password. Upon correct submission…” All admin authentication must meet: min-8-char bcrypt-hashed password, lockout after 5 failures, session timeout (15m inactivity), audit trail with timestamp/IP for logins and edits. Comply with GDPR if applicable. Owner: Security/Architect; Next action: Define acceptance criteria for security controls and integrate into admin API doc and test plan.  
**Architectural Impact:**  
- Requires authentication mechanism, credential storage/verification approach, and protection of admin endpoints.  
- Drives cross-cutting security controls (sessions, rate limiting, logging) even if not fully specified in SRS.  

**Quality Attributes Affected:** Security, Integrity, Accountability  

**Architectural Constraints:** Admin updater must be access-controlled via password authentication; must implement bcrypt hashing, lockout, session timeout, and audit trail (timestamp/IP); GDPR compliance if applicable.  

**Rationale:** Privileged access is high risk and cross-cutting; affects backend design and threat model.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-018, NFR-007
- **Conflicts with:** None specified
---

[ASR-008]: Performance expectations for low-bandwidth clients (modem) and progressive playback  
**Description**: (Derived from ASR-008) All assets must support first-interactive ≤3s over 10Mbps cable broadband on 2015+ Chromebook/iPad. Owner: Tech Lead; Next action: Modernize scenario and document test cases for representative user.  
**Architectural Impact:**  
- Constrains asset sizes, loading strategy (streaming/progressive loading), and initial critical-path bundle design.  
- Impacts media encoding, caching strategy, and perceived performance optimization.  

**Quality Attributes Affected:** Performance, Usability, Accessibility  

**Architectural Constraints:** All assets must support first-interactive ≤3 seconds over 10Mbps cable broadband on 2015+ Chromebook/iPad.  

**Rationale:** Non-default network/performance constraint shapes asset pipeline and client loading architecture.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-009, NFR-003
- **Conflicts with:** ASR-005 (frequent dynamic updates could increase bandwidth)
---