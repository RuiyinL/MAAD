# Non-Functional Requirements Results:

[NFR-001]: Interoperability and Standards Compliance
**Description:** The Center-to-Center project will be implemented using the evolving ITS Traffic Management Data Dictionary (TMDD) standard, the message sets associated with TMDD, other ITS Data Elements and Message Sets. Any data that is passed into the "cloud" will be based on the ITS standards. System must pass TMDD v3.x Interoperability Testing Suite with ≥ 95% of message exchanges validated against TMDD schema. Interoperability: ≥ 99% of cross-agency message exchanges shall conform to TMDD schema and protocol, measured weekly. Log and report TMDD schema conformance stats weekly; auto-alert to Integration Lead if <99% for 2 weeks.

**Quality Attributes**: Interoperability, Compatibility

**Measurable Criteria (if provided):**  System must pass TMDD v3.x Interoperability Testing Suite with ≥ 95% of message exchanges validated against TMDD schema; ≥ 99% of cross-agency message exchanges shall conform to TMDD schema and protocol, measured weekly; auto-alert to Integration Lead if <99% for 2 weeks.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Canonical Data Model)
- **Conflicts with:** FR-003 (System specific formats require translation)
---

[NFR-002]: Security and Authentication
**Description:** To support device control in other centers, the Center shall be able to support device control commands including username and Password. The remote Center Control GUI shall prompt for User name and Password upon initiation. Systems will interface to the "cloud" using a project defined protocol. All device control commands must be transmitted over TLS 1.2+; passwords are never logged; RBAC must restrict command actions and all credentials must adhere to NIST SP 800-63 password standards. Security: 100% commands over TLS 1.2+; passwords ≥ 12 chars per NIST 800-63, 100% of failed login attempts are logged and alerted on over a 30-day rolling window. If running on unsupported OS, device control must be restricted to private/VPN or routed through a compliant API gateway with complete audit logging. All remote commands originating/terminating on Windows NT hosts must be proxied through a modern API gateway with TLS 1.2+ and audit logging; no device control is directly exposed.

**Quality Attributes**: Security, Authentication

**Measurable Criteria (if provided):**  100% commands over TLS 1.2+; passwords ≥ 12 chars per NIST 800-63, 100% of failed login attempts are logged and alerted on over a 30-day rolling window; passwords never logged; unsupported OS requires proxy/gateway routing; no device control directly exposed on Windows NT.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Device Control), FR-006 (Remote GUI), ASR-006 (Public Network Security)
- **Conflicts with:** ASR-005 (Legacy Platform limitations)
---

[NFR-003]: Usability and Interaction
**Description:** The map user shall be able to alter the current magnification (zoom level) of the map. The map user shall be able to pan the map in each of the following directions: North, South, East or West. The user shall be able to click on an incident icon to obtain further information. Map operations (pan, zoom, click) respond in ≤ 1 sec in 95% of cases; incident info is accessible per WCAG 2.1 AA. Web map and GUIs reviewed annually against WCAG 2.1 AA; all violations remediated within 90 days.

**Quality Attributes**: Usability, User Experience

**Measurable Criteria (if provided):**  Map operations (pan, zoom, click) respond in ≤ 1 sec in 95% of cases; incident info and all interactive controls must be accessible per WCAG 2.1 AA; annual review with violations remediated within 90 days.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Web Map Visualization)
- **Conflicts with:** None
---

[NFR-004]: Reliability and Auditability
**Description:** In test mode, the Center-to-Center performs normal mode operations and also logs activities. The use of ITS standards will create a system that is reusable for other ITS application areas. In test mode, all user/device actions logged with timestamps, logs retained for ≥ 1 year, and retrievable for audit within 12 hours. All logs in test mode must be retrievable within 12 hours (or 1 business day, but not both).

**Quality Attributes**: Reliability, Maintainability, Reusability

**Measurable Criteria (if provided):**  In test mode, all user/device actions logged with timestamps, logs retained for ≥ 1 year, and retrievable for audit within 12 hours.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008 (Operational Modes)
- **Conflicts with:** None
---