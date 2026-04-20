# Non-Functional Requirements Results

[NFR-001]: Web-Based Availability (Internet-Accessible)
**Description:** “The product will be a web-based, interactive system… The Space Fractions system will be available over the Internet via the S2S website… will reside on the Internet so more than one user can access the product and download its content for use on their computer…”
  
**Quality Attributes**: Portability, Availability, Deployability

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** Not specified
- **Conflicts with:** FR-015 (single-user-per-instance nuance requires careful state handling)
---

[NFR-002]: No New Hardware Required
**Description:** “The Space Fractions system does not require any new hardware.”
  
**Quality Attributes**: Constraints, Deployability

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** Not specified
---

[NFR-003]: Browser Compatibility (Modern Standards-Based Stack; No Plugins)
**Description:** Source SRS: “requires a web browser capable of running Flash movies.” Semantic memory decision: “re-baselined to a standards-based web stack (HTML5/JS/CSS/SVG/Canvas/WebAudio; no plugins)… browser targets (latest 2 versions of Chrome/Firefox/Edge/Safari on Windows/macOS).”
  
**Quality Attributes**: Compatibility, Maintainability, Portability

**Measurable Criteria (if provided):** “latest 2 versions of Chrome/Firefox/Edge/Safari on Windows/macOS” (from prior architectural decision)

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** (Original SRS Flash runtime requirement)
---

[NFR-004]: Usability for Sixth-Grade Students (Mouse-Driven, Clear Navigation)
**Description:** “Input will consist entirely of mouse clicks… The information and interface will be effective so that Bobby will easily recognize what to do… and Alice will have no problems navigating through the help section… Claire will be assured that the students will know what to do…”
  
**Quality Attributes**: Usability, Accessibility (informal)

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-004
- **Conflicts with:** Not specified
---

[NFR-005]: Environment-Independent Behavior
**Description:** “Various environments may yield different interfaces, but the behavior of the program will be the same.”
  
**Quality Attributes**: Portability, Reliability (behavioral consistency)

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** Not specified
---

[NFR-006]: Responsive Gameplay for Velocity Adjustment
**Description:** “The output timing is immediate, ensuring responsive gameplay… update the spaceship’s speed in real-time.”
  
**Quality Attributes**: Performance, Responsiveness

**Measurable Criteria (if provided):** “immediate” / “real-time” (no numeric threshold specified)

**Dependencies** / **Conflicts**:
- **Depends on:** FR-011
- **Conflicts with:** FR-013 (if frequent content reloads degrade responsiveness)
---

[NFR-007]: Admin Access Control (Password-Protected Updater)
**Description:** “She navigates to the updater page, which asks for a password. Upon correct submission…”
  
**Quality Attributes**: Security

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012
- **Conflicts with:** Not specified
---

[NFR-008]: Secure Transport and Credential Handling (Explicit Controls)
**Description:** All administrative and player data must be transmitted over HTTPS. Admin authentication must enforce passwords of at least 12 characters and support account lockout after 5 failed attempts. [Owner: Not specified; Next action: Add measurable security controls and define test/monitoring strategy.]
  
**Quality Attributes**: Security, Privacy, Compliance/Assurance

**Measurable Criteria (if provided):** HTTPS-only; admin passwords >=12 characters; lockout after 5 failed attempts

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013
- **Conflicts with:** Not specified
---

[NFR-009]: Maintainability / Modifiability of Question Content
**Description:** “Maintainability is a primary goal… questions… updated by an administrator… saved in a file… easily edited through simplified administrative screens.”
  
**Quality Attributes**: Maintainability, Modifiability

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013
- **Conflicts with:** Not specified
---

[NFR-010]: Download/Startup Performance on Modem Connection
**Description:** “Introductory and main menu movies… downloaded in approximately one minute with a modem connection… main system can be played within a few minutes… Flash movies do not have to be fully downloaded to play…”
  
**Quality Attributes**: Performance, Efficiency

**Measurable Criteria (if provided):** ~1 minute (intro+menu assets) on modem; “few minutes” to play (not precisely defined)

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003
- **Conflicts with:** FR-008 (branching media size could increase load time)
---

[NFR-011]: Reliability via Testing
**Description:** “Reliability will be ensured by extensive testing by the team members and mentors, if available.”
  
**Quality Attributes**: Reliability, Quality Assurance

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005
- **Conflicts with:** Not specified
---