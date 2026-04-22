# Architecturally Significant Requirements Results

[ASR-001]: Web-based deployment over Internet (S2S website)  
**Description**: “The product will be a web-based, interactive system.” / “The Space Fractions system will be available over the Internet via the S2S website.”  
**Architectural Impact:**  
Forces a browser-delivered architecture (client-side runtime + web server hosting), impacts hosting, content delivery, and external-link handling.  
**Quality Attributes Affected:** Portability, Availability, Deployability, Security  
**Architectural Constraints:** Must be accessible via the World Wide Web; hosted and delivered from S2S website infrastructure.  
**Rationale:** Strong deployment constraint that shapes system context, interfaces, and operational model.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-003
---

[ASR-002]: Standards-based (HTML5) client delivery; no Flash/plugins  
**Description**: Derived from ASR-002. “All interactive features, animations, and audio must be implemented with HTML5, CSS, and JavaScript and execute without plugins in the last two Chrome, Firefox, Safari, Edge.” Next action: Edit SRS and all requirements docs to eliminate Flash/plugin wording; update downstream test/UX/asset design docs.  
**Architectural Impact:**  
Constrains client technology stack and content format to standards-based web delivery (HTML5/CSS/JavaScript), influencing UI composition, asset pipeline, and compatibility strategy.  
**Quality Attributes Affected:** Compatibility, Portability, Maintainability, Security  
**Architectural Constraints:** All interactive features, animations, and audio must be implemented with HTML5/CSS/JavaScript; no plugins; supported in last two versions of Chrome, Firefox, Safari, Edge.  
**Rationale:** Hard technology constraint with broad impact and long-term risk mitigation (deployment/security/maintainability).  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001
- **Conflicts with:** NFR-006, NFR-007
---

[ASR-003]: Web-accessible admin question updating with server-side file persistence  
**Description**: Derived from ASR-003. “JSON schema for question file: {\"id\":\"string\",\"prompt\":\"string\",\"choices\":[\"string\"],\"answer\":\"string\",\"hint\":\"string\"}” Next action: Add schema to requirements doc; reference it in API/design/test plans.  
**Architectural Impact:**  
Requires an admin subsystem (separate UI + server endpoint), a persistent content store (file on server), and a runtime content-loading mechanism so gameplay reads updated questions. Drives separation between content and code and defines a content update workflow.  
**Quality Attributes Affected:** Maintainability, Modifiability, Security, Integrity  
**Architectural Constraints:** Question data must be stored as UTF-8 JSON files on server with defined schema; edits must be schema-validated; updates must be written to a temp file and atomically renamed over the old file on successful schema validation.  
**Rationale:** Introduces cross-cutting content management and persistence concerns that shape module boundaries and data flow.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020, FR-022, NFR-007
- **Conflicts with:** NFR-008
---

[ASR-004]: Password-gated administrator access  
**Description**: “She navigates to the updater page, which asks for a password. Upon correct submission of her password…”  
**Architectural Impact:**  
Requires an authentication mechanism for admin functions (credential handling, session management, and protection of update endpoints).  
**Quality Attributes Affected:** Security, Privacy, Integrity  
**Architectural Constraints:** Admin updater must require password authentication before allowing edits.  
**Rationale:** Security is cross-cutting and affects admin UI, server endpoints, and storage/handling of credentials.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, ASR-003
- **Conflicts with:** NFR-008
---

[ASR-005]: Local score storage within the system instance  
**Description**: “The user's score must be kept as local data within the Space Fractions system so that the results may be given at the end…”  
**Architectural Impact:**  
Constrains state management approach (client-local state vs server persistence), influences session lifecycle, replay behavior, and data privacy boundaries.  
**Quality Attributes Affected:** Privacy, Reliability, Maintainability  
**Architectural Constraints:** Score data must be stored locally within the running system instance (not specified as server-side).  
**Rationale:** State placement is an architectural decision affecting component responsibilities and data flow.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, FR-013
- **Conflicts with:** Not specified
---

[ASR-006]: Single-user per instance with multi-user access via Internet distribution  
**Description**: “Only one person can use a single instance… However… will reside on the Internet so more than one user can access the product and download its content for use on their computer.”  
**Architectural Impact:**  
Defines concurrency model: no shared multi-user session per instance, but supports multiple independent instances via distribution. Impacts whether server needs per-user state, and how content is packaged/cached.  
**Quality Attributes Affected:** Scalability, Concurrency, Deployability  
**Architectural Constraints:** Enforce single-user usage per running instance; allow multiple users to access/download content over Internet.  
**Rationale:** Strongly shapes runtime topology and state isolation assumptions.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001
- **Conflicts with:** Not specified
---

[ASR-007]: Performance constraints for modem-based loading/play  
**Description**: “movies… downloaded in approximately one minute with a modem connection… main system can be played within a few minutes with a regular modem connection…”  
**Architectural Impact:**  
Drives asset sizing, compression, streaming strategy (Flash partial download), and overall content delivery approach to meet low-bandwidth constraints.  
**Quality Attributes Affected:** Performance, Responsiveness, User Experience  
**Architectural Constraints:** Intro+menu assets sized to download ~1 minute over modem; gameplay should be usable within a few minutes over modem.  
**Rationale:** Non-trivial performance targets that influence packaging and delivery architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002, ASR-001
- **Conflicts with:** Not specified
---

[ASR-008]: Real-time velocity adjustment from fraction input applied to physics engine  
**Description**: “output timing is immediate… applied to the game's physics engine to update the spaceship's speed in real-time.”  
**Architectural Impact:**  
Requires a tight coupling/interaction between input validation, fraction-to-decimal computation, and the physics update loop; influences event handling and timing model to keep gameplay responsive.  
**Quality Attributes Affected:** Performance, Responsiveness, Correctness  
**Architectural Constraints:** Velocity adjustment must be computed and applied immediately in real time to the physics engine.  
**Rationale:** Timing-sensitive behavior affects core runtime design and integration between gameplay logic and physics.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017
- **Conflicts with:** Not specified
---