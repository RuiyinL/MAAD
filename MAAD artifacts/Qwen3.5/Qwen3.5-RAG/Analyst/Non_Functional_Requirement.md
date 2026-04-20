# Non-Functional Requirements Results:
[NFR-001]: Platform Compatibility and Architecture
**Description:** The system shall run on any Internet-accessible computer with a web browser. While the SRS mentions Flash, the architectural decision mandates an HTML5/CSS/JavaScript-only architecture to ensure modern compatibility and remove plugin dependencies.

**Quality Attributes**: Portability, Compatibility, Maintainability

**Measurable Criteria (if provided):** Supported platforms: Chrome (last 2 versions), Firefox (last 2), Edge; cross-browser test suite must pass for all listed. (Overrides SRS Flash requirement per Architectural Decision).

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Web-Based Architecture)
- **Conflicts with:** SRS text "requires a web browser capable of running Flash movies" (Resolved by ADR).
---
[NFR-002]: Performance and Load Time
**Description:** The system assets (introductory movie, main menu, core logic) shall be downloadable and playable within a few minutes over a standard modem connection.

**Quality Attributes**: Performance, Efficiency

**Measurable Criteria (if provided):** Downloadable in approx. 1 minute with 56Kbps modem connection; Time-to-playable defined by 56Kbps simulation.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Web-Based Architecture)
- **Conflicts with:** None
---
[NFR-003]: Security and Authentication
**Description:** The system shall be as secure as the running web browser for general users. For administrators, the system shall enforce hardened authentication for the Question Updater.

**Quality Attributes**: Security, Integrity

**Measurable Criteria (if provided):** Admin passwords >=12 characters, salted hashing (bcrypt/Argon2), account lockout after 5 failures, HTTPS-only endpoints. Admin endpoints restrict to TLS 1.2+, password rotation every 180 days, incident response plan for failed auth/audit anomalies. Acceptance criteria: (a) All admin endpoints log every login, failed login, and question edit/change, with exportable logs reviewed monthly; (b) Incident Response drills completed and recorded at least twice yearly.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Administrator Question Updater), ASR-003 (Security Boundary)
- **Conflicts with:** SRS text "as secure as the web browser" (Refined by ADR).
---
[NFR-004]: Maintainability and Modifiability
**Description:** The system content (questions) shall be updatable by an administrator without requiring a system restart or code redeployment.

**Quality Attributes**: Maintainability, Modifiability

**Measurable Criteria (if provided):** Real-time updates via file save; Atomic file update semantics to prevent corruption. Maintainability acceptance: (a) 80% code coverage by automated tests; (b) All non-trivial functions/classes documented; (c) Cyclomatic complexity <10 for all modules; (d) Major content updatable without code changes.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Administrator Question Updater), ASR-002 (File-Based Content Management)
- **Conflicts with:** None
---
[NFR-005]: Usability and Accessibility
**Description:** The interface shall be effective for sixth-grade students, including those with low computer literacy (Alice) and those seeking competition (Bobby).

**Quality Attributes**: Usability, User Experience

**Measurable Criteria (if provided):** Input entirely via mouse clicks; Help section accessible from Main Menu; Feedback responsiveness within 500ms (per ADR standards). Usability acceptance: System must pass screen reader tests (axe or Accessibility Insights), and achieve a Flesch-Kincaid grade score ≤ 7 on all help/instruction text. All help/instruction screens must score Flesch-Kincaid Grade ≤7 (automatically computed per release), and all core screens must show 0 'serious'/'critical' errors per axe scan executed in CI.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002 (Main Menu), FR-004 (Answer Validation)
- **Conflicts with:** None
---
[NFR-006]: Availability and Reliability
**Description:** The system shall be available over the Internet via the S2S website. Reliability is ensured through testing.

**Quality Attributes**: Availability, Reliability

**Measurable Criteria (if provided):** Monthly uptime must be ≥ 99.5% as measured by automated probes every 60 seconds from at least 2 cloud regions. Extensive team testing required. Reliability acceptance: (a) ≥99% functional test suite pass rate per release; (b) ≤4 hours mean time to recover (MTTR) from critical failures; (c) Defect leakage rate < 1% per release.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Web-Based Architecture)
- **Conflicts with:** None
---