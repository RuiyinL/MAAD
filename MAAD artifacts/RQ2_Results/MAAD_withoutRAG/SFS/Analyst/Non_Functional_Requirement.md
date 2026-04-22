# Non-Functional Requirements Results

[NFR-001]: Supported browsers and no-plugin runtime constraint  
**Description:** (Derived from NFR-001) All multimedia content must function using only HTML5/JavaScript/SVG and work on Chrome, Firefox, Edge, Safari (latest 2 versions). No Flash or plugin dependencies permitted. Owner: Architect/PO; Next action: Update all FR/ASR/NFR and SRS text to remove Flash/plugin references and define HTML5-only technology stack.  

**Quality Attributes**: Compatibility/Portability; Technology Constraint  

**Measurable Criteria (if provided):** HTML5/JavaScript/SVG only; Chrome/Firefox/Edge/Safari latest 2 versions; no Flash/plugins  

**Dependencies** / **Conflicts**:
- **Depends on:** None specified
- **Conflicts with:** NFR-011 (Maintainability goal), NFR-003 (run on any Internet-accessible computer—Flash may not be available)
---

[NFR-002]: Quantified gameplay responsiveness for velocity adjustment  
**Description:** (Derived from NFR-002) “The output timing is immediate, ensuring responsive gameplay… update the spaceship's speed in real-time.” Test case: for 100 gameplay input→velocity updates on 2015+ Chromebook, 95% must complete in ≤150ms; failures generate alert and block deploy. Owner: PO/QA; Next action: Configure performance-monitoring test suite for critical game flows.  

**Quality Attributes**: Performance/Responsiveness  

**Measurable Criteria (if provided):** n=100 runs on 2015+ Chromebook; 95th percentile ≤150ms; failures alert and block deploy  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013
- **Conflicts with:** None specified
---

[NFR-003]: Web-based availability and internet accessibility with uptime target  
**Description:** (Derived from NFR-003) “The product will be a web-based, interactive system.” / “The Space Fractions system will run on any Internet-accessible computer…” / “The Space Fractions system will be available over the Internet via the S2S website.” HTTP 200 uptime of 99.5% measured via external probe every 30s; outages >3min trigger Slack/email alert to SRE and open ticket. Owner: SRE; Next action: Document monitoring/alerting protocol for SRE and specify in deployment checklist.  

**Quality Attributes**: Accessibility/Portability/Deployment Constraint  

**Measurable Criteria (if provided):** External probe every 30s; uptime (HTTP 200) ≥99.5%; outages >3 minutes trigger alert + ticket  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (in original SRS), or modern equivalent platform constraint
- **Conflicts with:** None specified
---

[NFR-004]: No new hardware required  
**Description:** (Derived from NFR-004) “The Space Fractions system does not require any new hardware.” Build verification matrix must pass on 3+ different hardware models (PC, Chromebook, iPad) with supported browsers. Owner: SRE/QA; Next action: Add compatibility testplan for hardware diversity.  

**Quality Attributes**: Operational Constraint/Deployability  

**Measurable Criteria (if provided):** Build verification matrix passes on ≥3 hardware models (PC, Chromebook, iPad) with supported browsers  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** None specified
---

[NFR-005]: Cross-browser behavioral invariance with regression acceptance criterion  
**Description:** (Derived from NFR-005) “various environments may yield different interfaces, but the behavior of the program will be the same.” Selenium regression suite runs on release and weekly; any story/score divergence blocks release, with tracking in QA dashboard. Owner: QA; Next action: Automate browser matrix management and link regression alerts to release pipeline.  

**Quality Attributes**: Portability/Consistency/Correctness  

**Measurable Criteria (if provided):** Regression runs weekly and on release; any divergence blocks release; tracked in QA dashboard  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** FR-006 (adaptive storylines increase cross-environment verification complexity; not a direct contradiction)
---

[NFR-006]: Usability success-rate/time metric for target users  
**Description:** (Derived from NFR-006) “The information and interface will be effective so that Bobby will easily recognize what to do… Alice will have no problems navigating through the help section… Claire will be assured that the students will know what to do from this main screen.” ≥85% of all users, including those using keyboard/screen reader, must reach Q1 in <2min; if not, redesign UI/hints and retest. Owner: PO/UX; Next action: Expand usability NFRs to include accessibility, broader user base, and explicit improvement trigger.  

**Quality Attributes**: Usability/Learnability  

**Measurable Criteria (if provided):** ≥85% of all users (including keyboard/screen reader users) reach Q1 in <2 minutes; if unmet then redesign + retest  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-004, FR-017
- **Conflicts with:** None specified
---

[NFR-007]: Admin/editor security controls (HTTPS + password hashing)  
**Description:** (Derived from NFR-007) “The Space Fractions system will be as secure as the web browser that will run the product.” Admin subsystem must use HTTPS, store all passwords hashed with bcrypt, provide lockout for 10 minutes after 5 failed logins, timeout sessions after 15min of inactivity, and log all admin access attempts and changes. Owner: Security/PO; Next action: Update NFR-007 and related FRs to list all required technical controls and document enforcement in admin user stories.  

**Quality Attributes**: Security  

**Measurable Criteria (if provided):** HTTPS-only; bcrypt password hashing; lockout 10 minutes after 5 failed logins; session timeout 15 minutes inactivity; log all admin access attempts and changes  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003
- **Conflicts with:** FR-016 (admin password protection needs explicit security controls beyond “as secure as browser”)
---

[NFR-008]: Single-user per running instance; multi-user access via Internet distribution  
**Description:** “Only one person can use a single instance of the Space Fractions system. However, the Space Fractions system will reside on the Internet so more than one user can access the product and download its content for use on their computer.”  

**Quality Attributes**: Concurrency/Scalability (usage constraint)  

**Measurable Criteria (if provided):** Not specified  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** None specified
---

[NFR-009]: Main menu interactivity load-time target on modern connection  
**Description:** (Derived from NFR-009) “introductory and main menu movies… downloaded in approximately one minute with a modem connection.” / “main system can be played within a few minutes with a regular modem connection… Flash movies do not have to be fully downloaded to play.” Main game bundle (JS/CSS/critical assets) ≤2.5MB compressed; first-interactive measured in Lighthouse on each deploy (<3sec, 10Mbps, 2015+ HW). Owner: Tech Lead; Next action: Add asset-size guidance to build/deploy checklist and automate performance audits.  

**Quality Attributes**: Performance (load time), Network efficiency  

**Measurable Criteria (if provided):** Main bundle ≤2.5MB compressed; Lighthouse first-interactive <3 seconds on 10Mbps and 2015+ hardware on each deploy  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-003
- **Conflicts with:** None specified
---

[NFR-010]: Maintainability metrics (test coverage + content deploy time)  
**Description:** (Derived from NFR-010) “Maintainability is a primary goal for this project.” At least 80% statement/branch/test coverage for UI, admin, and data layer, as measured by CI pipeline on each release candidate. Owner: PO/dev; Next action: Update SRS/requirements to specify maintainability criteria in testable terms, referencing code coverage checks.  

**Quality Attributes**: Maintainability/Modifiability  

**Measurable Criteria (if provided):** ≥80% statement/branch/test coverage for UI/admin/data layer measured by CI on each release candidate  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-018
- **Conflicts with:** NFR-001 (Flash dependency undermines maintainability)
---

[NFR-011]: Reliability ensured by extensive testing  
**Description:** (Derived from NFR-011) “Reliability will be ensured by extensive testing by the team members and mentors, if available.” Zero P0 blocking bugs for 30 days post-release and ≥99% pass on nightly QA for release qualification. Owner: QA; Next action: Add reliability KPIs/metrics and reporting cadence to NFR-011.  

**Quality Attributes**: Reliability  

**Measurable Criteria (if provided):** Zero P0 blocking bugs for 30 days post-release; nightly QA pass rate ≥99% for release qualification  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-013, FR-018
- **Conflicts with:** None specified
---