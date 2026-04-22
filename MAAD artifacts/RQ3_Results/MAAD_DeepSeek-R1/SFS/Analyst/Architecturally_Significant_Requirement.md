# Architecturally Significant Requirements Results:
[ASR-001]: HTML5 Runtime Requirement  
**Description**: The system must render all movies and interactivity via HTML5 technologies; Flash must not be required.  
**Architectural Impact:**  
Mandates HTML5/CSS/JavaScript stack for rendering. Affects component design (browser-native UI), deployment (no plugins), and security (modern standards compliance).  
**Quality Attributes Affected:**  
Compatibility, Security, Maintainability  
**Architectural Constraints:**  
Client-side must use standards-based web technologies; server must deliver HTML5 content.  
**Rationale:**  
High-impact constraint dictating modern technology stack with cross-cutting security/maintainability implications.  
**Dependencies** / **Conflicts**:  
- **Conflicts with:** Original Flash dependency  
---  

[ASR-002]: Web Deployment  
**Description**: Available over Internet via S2S website.  
**Architectural Impact:**  
Requires client-server architecture with web hosting. Influences component decomposition (browser client, web server), communication (HTTP), and scalability strategies (stateless interactions).  
**Quality Attributes Affected:**  
Availability, Accessibility  
**Architectural Constraints:**  
Must deploy via web server; client requires internet connectivity.  
**Rationale:**  
Defines fundamental deployment model with availability trade-offs.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---  

[ASR-003]: Local Score Storage  
**Description**: User scores stored locally within system for end-of-session results.  
**Architectural Impact:**  
Eliminates server-side storage needs but prevents cross-device persistence. Affects data flow (client-only scoring), component design (local storage handlers), and analytics capabilities.  
**Quality Attributes Affected:**  
Data Persistence, Usability  
**Architectural Constraints:**  
Scores must persist client-side without server synchronization.  
**Rationale:**  
Imposes data-locality constraint with architectural trade-offs (simplicity vs. analytics limitations).  
**Dependencies** / **Conflicts**:  
---  

[ASR-004]: Atomic Question File Updates  
**Description**: Updates to question files must use a JSON schema v1.0 (see Appendix A). Each update writes to a temp file, validated against the schema, and atomically replaces the prior file. Admin access must require session authentication and actions logged.  
**Architectural Impact:**  
Requires server file I/O subsystem with atomic operations. Drives component decomposition (validation service, audit logger), data contracts (JSON schema), and security layers (authentication).  
**Quality Attributes Affected:**  
Maintainability, Security, Data Integrity  
**Architectural Constraints:**  
Must implement atomic file writes with schema validation and audit logging.  
**Rationale:**  
High-risk requirement (file writes + validation) affecting security boundaries and modifiability.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-002  
---  

[ASR-005]: Accessible Input Methods  
**Description**: All UI elements must be reachable and usable by keyboard (tab/enter/arrow keys) and have ARIA labels for screenreaders.  
**Architectural Impact:**  
Constrains UI to accessible design patterns. Affects component design (keyboard handlers, semantic HTML), testing matrix (accessibility audits), and compliance strategies.  
**Quality Attributes Affected:**  
Usability, Accessibility  
**Architectural Constraints:**  
UI must support WCAG 2.1 AA compliance via keyboard navigation and ARIA.  
**Rationale:**  
Cross-cutting constraint influencing UI component design and legal compliance.  
**Dependencies** / **Conflicts**:  
---  

[ASR-006]: Controlled External Integration  
**Description**: System is standalone except for permitted outbound browser link navigation to educational resources.  
**Architectural Impact:**  
Enforces strict integration boundaries. Limits external dependencies to hyperlinks only, promoting modular isolation while allowing educational resource access.  
**Quality Attributes Affected:**  
Portability, Maintainability  
**Architectural Constraints:**  
No external software dependencies beyond browser standards; hyperlinks exempted.  
**Rationale:**  
Clarifies architectural boundary constraints while resolving conflict with resource linking.  
**Dependencies** / **Conflicts**:  
---  

[ASR-007]: Hardened Admin Authentication  
**Description**: Admin passwords are stored as salted bcrypt hashes; all admin interactions over HTTPS; failed login attempts over 5/minute IP-blocked; admin sessions expire after 30 min idle.  
**Architectural Impact:**  
Necessitates authentication subsystem with security controls. Drives security components (credential hashing, TLS enforcement, rate limiting), session management, and audit logging.  
**Quality Attributes Affected:**  
Security  
**Architectural Constraints:**  
Must implement password hashing, TLS, brute-force protection, and session expiration.  
**Rationale:**  
Security-critical requirement with cross-cutting architectural implications.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004  
---