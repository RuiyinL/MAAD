# Architecturally Significant Requirements Results:
[ASR-001]: Web-Based HTML5 Architecture
**Description**: The system shall be implemented as a web-based application using HTML5, CSS, and JavaScript, explicitly rejecting the SRS-mandated Flash plugin dependency to ensure long-term viability and deployment feasibility. NOTE: All references to Flash/plugin are superseded by ASR-001 and NFR-001 which exclusively mandate HTML5/JavaScript—no plugins.
**Architectural Impact:**  
- **Technology Selection:** Mandates HTML5 Canvas/DOM APIs over Flash/ActionScript.
- **Deployment:** Enables deployment on standard web servers without specialized media servers.
- **Compatibility:** Removes client-side plugin installation barriers.

**Quality Attributes Affected:**  
Portability, Maintainability, Deployability, Security

**Architectural Constraints:**  
- No browser plugins allowed.
- Must utilize modern browser APIs for audio/animation (replacing Flash movies).
- Acceptance criteria: Verified by automated headless browser testing that no plugin-related APIs or assets are loaded at runtime.

**Rationale:**  
Flash is obsolete and unsupported by modern browsers, creating a critical deployment blocker. This decision aligns with the "Legacy plugin purge" architectural decision to ensure the system is actually deployable and maintainable.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Platform Compatibility)
- **Conflicts with:** SRS text "requires a web browser capable of running Flash movies".
---
[ASR-002]: File-Based Content Management
**Description**: Question data shall be stored as UTF-8 JSON files on the web server, editable by the admin tool, rather than a database or compiled code.
**Architectural Impact:**  
- **Data Layer:** Simplifies persistence to file I/O; requires atomic write operations (temp-file + rename) to prevent corruption during updates.
- **Separation of Concerns:** Decouples content (questions) from code (game logic).
- **Concurrency:** Limits concurrent admin editing unless locking is implemented.

**Quality Attributes Affected:**  
Maintainability, Reliability, Modifiability

**Architectural Constraints:**  
- Server-side file system access required for the admin component.
- Atomic update semantics required for question files.
- Acceptance: After concurrent admin edits/failures in QA, 100% of question file versions validate as well-formed JSON.

**Rationale:**  
Supports the requirement for non-technical admins to update content without code changes. File-based storage reduces infrastructure complexity compared to a database for this scale, but requires strict write controls.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Administrator Question Updater), NFR-004 (Maintainability)
- **Conflicts with:** None
---
[ASR-003]: Security Boundary for Administration
**Description**: The administrative function (Question Updater) must be isolated behind an authentication boundary with specific security controls (HTTPS, hashed passwords, audit logging).
**Architectural Impact:**  
- **Security Architecture:** Requires implementation of an authentication mechanism (session management, password hashing).
- **Logging:** Requires an audit log subsystem to record admin actions (timestamp, admin ID, changes).
- **Network:** Enforces HTTPS for all admin traffic.

**Quality Attributes Affected:**  
Security, Integrity, Auditability

**Architectural Constraints:**  
- Admin endpoints must be HTTPS only.
- Passwords must be salted and hashed (no plain text).
- Audit log entry schema: {timestamp: ISO string, admin_id: string, action: string, details: object}; audit logs must be exported and backed up monthly, with retention policy enforced for 2 years.

**Rationale:**  
The ability to modify system content is a high-risk capability. Without proper authentication and logging, the system's educational integrity is compromised. This elevates the admin tool from a simple form to a secure subsystem.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Administrator Question Updater), NFR-003 (Security)
- **Conflicts with:** SRS text implying simple password protection ("asks for a password").
---
[ASR-004]: Client-Side State Management
**Description**: User scores and session state shall be maintained locally within the client system (browser memory/local storage) rather than on the server.
**Architectural Impact:**  
- **Data Flow:** Reduces server load and database requirements; no user account system needed.
- **Persistence:** Scores are lost when the session ends (no long-term user history).
- **Security:** Prevents server-side PII storage but exposes score data to client-side manipulation.

**Quality Attributes Affected:**  
Scalability, Security, Privacy

**Architectural Constraints:**  
- No persistent user database required.
- Score validation is client-side (vulnerable to cheating, accepted for this learning tool context).

**Rationale:**  
Aligns with the requirement "user's score must be kept as local data". Simplifies architecture by removing user management but accepts the trade-off of non-persistent scores and lower security integrity for gameplay data.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Scoring), FR-006 (Ending Scene)
- **Conflicts with:** None
---