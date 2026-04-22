# Non-Functional Requirements Results

[NFR-001]: Web-based availability over the Internet  
**Description:** Derived from NFR-001. “99.9% uptime means no more than 43.8 minutes downtime per 30 days, as measured by 60s probes, excluding pre-announced maintenance.” Next action: Add precise uptime metric and test measurement plan to the requirements.  
**Quality Attributes**: Portability, Accessibility, Deployment/Operational Constraint  
**Measurable Criteria (if provided):** 99.9% uptime monthly = ≤43.8 minutes downtime per 30 days; measured by 60s probes; excludes pre-announced maintenance (duration not specified here)  
**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** Not specified
---

[NFR-002]: Requires HTML5-compatible web browser (no plugins)  
**Description:** Derived from NFR-002. “Requires HTML5-compatible web browser; all interactive media and animations implemented using standard web technologies (HTML5, CSS, JavaScript); must run correctly in latest Chrome, Firefox, Safari, and Edge.” Next action: Remove Flash dependency from all requirements; update architecture and test plans to require only web standards.  
**Quality Attributes**: Compatibility, Technology Constraint  
**Measurable Criteria (if provided):** Must run correctly in latest Chrome, Firefox, Safari, and Edge; no plugins (Flash removed)  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-006
---

[NFR-003]: Single-user per browser session (concurrent sessions permitted)  
**Description:** Derived from NFR-003. “Each browser session shall present a single-user interface; concurrent sessions by multiple users on the server are permitted.” Next action: Clarify in both SRS and technical notes how single-user assumption is implemented.  
**Quality Attributes**: Concurrency/Capacity Constraint  
**Measurable Criteria (if provided):** Single user per browser session; concurrent sessions permitted (no numeric limit specified)  
**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** NFR-001
---

[NFR-004]: Usability for sixth graders; intuitive navigation and help  
**Description:** Derived from NFR-004. “Acceptance: ≥90% of 20 representative sixth-graders (school pilot, n=20) complete all core flows unassisted (≤1 prompt allowed).” Next action: Add detailed usability acceptance protocol to requirements/usability section.  
**Quality Attributes**: Usability, Learnability, Accessibility (interaction simplicity)  
**Measurable Criteria (if provided):** ≥90% of n=20 representative sixth-graders complete core flows unassisted; ≤1 prompt allowed  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-009
- **Conflicts with:** Not specified
---

[NFR-005]: Consistent behavior across browser environments  
**Description:** Derived from NFR-005. “Measure pixel bounding box of menu buttons and Q&A panels; automated regression test on Chrome, Firefox, Safari, Edge (most recent+prior version) on Win10/macOS/iPadOS. Report any layout/RT deviation >5%.” Next action: Supply test matrix/table and automated test acceptance criteria in requirements appendix.  
**Quality Attributes**: Portability, Consistency  
**Measurable Criteria (if provided):** Layout measured by pixel bounding boxes of menu buttons and Q&A panels; browsers: Chrome/Firefox/Safari/Edge (most recent+prior); platforms: Win10/macOS/iPadOS; report deviations >5%  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002
- **Conflicts with:** Not specified
---

[NFR-006]: No new hardware required  
**Description:** Derived from NFR-006. “‘Supported on devices with at least 1GB RAM, running latest 2 versions of Chrome/Firefox/Safari/Edge on Windows 10+, macOS 11+, or iPadOS 16+.’” Next action: Add supported platform matrix in appendix or NFR-006 table.  
**Quality Attributes**: Deployment Constraint, Cost Constraint  
**Measurable Criteria (if provided):** ≥1GB RAM; latest 2 versions of Chrome/Firefox/Safari/Edge; Windows 10+, macOS 11+, iPadOS 16+  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-002 (may indirectly constrain device/browser choices)
---

[NFR-007]: Maintainability is a primary goal  
**Description:** Derived from NFR-007. “‘System can be rebuilt/tested on Windows 10 and Ubuntu 22.04 using documented open-source tools; code adheres to PEP8/ESLint without critical errors.’” Next action: Add maintainability acceptance tests/criteria to NFR-007 and cross-reference in architecture documentation.  
**Quality Attributes**: Maintainability, Modifiability  
**Measurable Criteria (if provided):** Rebuild/test on Windows 10 and Ubuntu 22.04 using documented open-source tools; PEP8/ESLint with no critical errors  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022
- **Conflicts with:** NFR-002 (Flash constraint may reduce maintainability long-term)
---

[NFR-008]: Security controls for admin operations (HTTPS, strong auth, audit, compliance)  
**Description:** Derived from NFR-008. “Audit log entries must contain: {\"timestamp_utc\":string, \"admin_id\":string, \"remote_ip\":string, \"field_changed\":string, \"before\":string, \"after\":string}. Logs stored for ≥2 years. COPPA compliance confirmed by annual legal review.” Next action: Append audit log format; define compliance test case in QA and deployment processes.  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Audit log schema fields specified; retention ≥2 years; COPPA compliance confirmed by annual legal review  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, NFR-001
- **Conflicts with:** FR-021 (password-based admin access implies additional security needs not specified)
---

[NFR-009]: Performance—download/playability over modem connection  
**Description:** Derived from NFR-009. “Using Chrome DevTools (56Kbps simulation), loading /game delivers intro animation and menu screen in ≤60s total; all asset files listed in table X in the appendix.” Next action: Add asset table, simulation protocol, pass/fail thresholds to SRS and SRE acceptance checklist.  
**Quality Attributes**: Performance (startup/load time), Efficiency  
**Measurable Criteria (if provided):** 56Kbps simulation in Chrome DevTools; /game delivers intro+menu ≤60s; asset files listed in appendix table X  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002
- **Conflicts with:** Not specified
---

[NFR-010]: Reliability via extensive testing  
**Description:** Derived from NFR-010. “System must achieve ≥90% automated test coverage and ≤2 open severity-1 defects prior to general release. Severity-1 defect: blocks core gameplay, causes data loss/corruption, or presents security vulnerability exploitable by users.” Next action: Add glossary or append formal severity table to NFR-010 and QA documents.  
**Quality Attributes**: Reliability, Quality Assurance Process Constraint  
**Measurable Criteria (if provided):** ≥90% automated test coverage; ≤2 open severity-1 defects prior to general release; severity-1 definition included  
**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** Not specified
---