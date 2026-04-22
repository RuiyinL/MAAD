# Non-Functional Requirements Results

[NFR-001]: Use TMDD standard for information exchange
**Description:** “The Center-to-Center Project shall utilize the TMDD standard (including message sets) to transmit information.” Updated per evaluator: All exchanged traffic data must conform to TMDD v3.0 or higher as defined by [ref doc], with version negotiation at session start. [Next action: Set, document, and enforce specific TMDD standard version.]
  
**Quality Attributes**: Interoperability, Standards Compliance

**Measurable Criteria (if provided):** TMDD v3.0 or higher; version negotiation at session start

**Dependencies** / **Conflicts**:
- **Depends on:** FR-038, FR-071
- **Conflicts with:** NFR-002
---

[NFR-002]: Use DATEX/ASN to transmit TMDD message sets
**Description:** “DATEX/ASN shall be used to transmit the TMDD message sets.” Updated per evaluator: All TMDD message sets shall use DATEX/ASN v1.5 (or specified version), compatible with [reference implementation]. [Next action: Add concrete DATEX/ASN version and conformance requirement.]
  
**Quality Attributes**: Interoperability, Standards Compliance

**Measurable Criteria (if provided):** DATEX/ASN v1.5

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-003
---

[NFR-003]: Use TCP/IP transport for DATEX/ASN data
**Description:** “TCP/IP shall be used to transmit the DATEX/ASN data.” Updated per evaluator: All communication must be via TCP/IP (IPv4 and IPv6 supported), with all payloads secured via TLS 1.2+ on configurable ports. [Next action: Add explicit TCP/IP stack and security transport requirements.]
  
**Quality Attributes**: Interoperability, Portability

**Measurable Criteria (if provided):** IPv4 and IPv6 supported; TLS 1.2+; configurable ports

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002
- **Conflicts with:** NFR-009
---

[NFR-004]: Require username/password for device control requests
**Description:** “To support DMS control… including … username and Password.” (and similarly for LCS/CCTV switching/ramp meter/HAR/traffic signal/HOV/school zone/reversible lane/dynamic lane control) and “When the GUI application is initiated, the user shall be prompted for… User name and Password.” Updated per evaluator: Acceptance Criteria: (i) Attempts to register/login with passwords <12 chars are rejected and logged; (ii) After 5 failed login attempts per user, the account is locked for 30 min and auditable; (iii) All stored passwords must be verified as salted bcrypt/scrypt hashes in DB; (iv) If user profile has MFA_enabled=true, challenge is enforced on all non-session-auth requests; (v) Review team to provide explicit negative testcases for password and MFA, with pass/fail and findings. [Next action: Document and attach a detailed test plan and evidence for all NFR-004 controls.]
  
**Quality Attributes**: Security (Authentication), Safety

**Measurable Criteria (if provided):** Reject passwords <12 chars and log; lock after 5 failed attempts for 30 min; salted bcrypt/scrypt hashes; enforce MFA when MFA_enabled=true on all non-session-auth requests; explicit negative testcases with pass/fail and findings

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-007, FR-009, FR-011, FR-013, FR-015, FR-017, FR-020, FR-023, FR-026, FR-028, FR-057
- **Conflicts with:** NFR-005
---

[NFR-005]: Web map must be displayable on an Internet WWW server
**Description:** “The Web Map application generates a map that can be displayed on an Internet WWW server.” Updated per evaluator: Availability checked via pingdom/http synthetic every 5 min; failure if > 4.5 h/mo downtime. Initial map load time measured on cold page load at 95th percentile in CI and at live endpoint. [Next action: Document SRE test/monitor scripts and acceptance points.]
  
**Quality Attributes**: Deployability, Accessibility

**Measurable Criteria (if provided):** Synthetic availability check every 5 min; failure if >4.5 hours/month downtime; initial map load time measured on cold page load at 95th percentile in CI and at live endpoint

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-012
---

[NFR-006]: Data minimization/PII constraint for credentials in messages (implied risk)
**Description:** Requirements repeatedly include “username and Password” as part of device control command payload fields. Updated per evaluator: Define: (i) All messages with password fields must be exchanged only on validated mutual TLS v1.2+ APIs, verified in integration test; (ii) All audit logs/events are confirmed (test result evidence) to show only username (never password); (iii) Failed login, bad command, and network/serialization errors must be tested for absence of password value in logs. [Next action: Produce end-to-end test evidence for TLS enforcement and credential redaction in logs/error output.]
  
**Quality Attributes**: Security (Confidentiality), Privacy/Compliance

**Measurable Criteria (if provided):** Validated mutual TLS v1.2+ for all password-field messages (verified in integration test); audit logs/events show username only (never password) with test evidence; error conditions tested to confirm absence of password values in logs

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-007, FR-009, FR-011, FR-013, FR-015, FR-017, FR-020, FR-023, FR-026, FR-028
- **Conflicts with:** NFR-003
---

[NFR-007]: Basemap data source constraint (NCTCOG GeoData warehouse)
**Description:** “The basemap data shall be derived from the North Central Texas Council of Governments (NCTCOG) GeoData warehouse.”
  
**Quality Attributes**: Data Quality, Maintainability (external dependency)

**Measurable Criteria (if provided):** Not specified

**Dependencies** / **Conflicts**:
- **Depends on:** FR-041
- **Conflicts with:** NFR-013
---

[NFR-008]: Configuration-driven speed thresholds for link color coding
**Description:** “A configuration file shall be provided to specify specific speed values.” Updated per evaluator: Speed config in YAML (sample); CLI/API hot reload tested on all nodes; failures logged and rollback enabled. [Next action: Document config schema+reload plan.]
  
**Quality Attributes**: Maintainability, Configurability

**Measurable Criteria (if provided):** YAML format; CLI/API hot reload tested on all nodes; failures logged; rollback enabled

**Dependencies** / **Conflicts**:
- **Depends on:** FR-044
- **Conflicts with:** NFR-014
---

[NFR-009]: Remote control GUI operates over a public network
**Description:** “The remote Center Control GUI shall be designed to execute on a public network (e.g., Internet) and transmit equipment requests to the C-2-C software system.” Updated per evaluator: Remote GUI uptime is measured weekly; automatic alert if <98% uptime in past 4 weeks; quarterly scan with {scanner-tool}. [Next action: Specify monitoring, scanning, and reporting process for remote GUI endpoints.]
  
**Quality Attributes**: Security, Reliability

**Measurable Criteria (if provided):** Weekly uptime measurement; alert if <98% uptime in past 4 weeks; quarterly vulnerability scan with {scanner-tool}

**Dependencies** / **Conflicts**:
- **Depends on:** FR-056
- **Conflicts with:** NFR-003
---

[NFR-010]: Test mode must log activities
**Description:** “In this mode, the Center-to-Center performs normal mode operations and also logs activities.” Updated per evaluator: Retention checked monthly by scheduled script; restricted to [role list]; log event: {timestamp, type, user_id, action, ...}. [Next action: Define and circulate a full logging/audit event type and retention checklist.]
  
**Quality Attributes**: Auditability, Supportability

**Measurable Criteria (if provided):** Monthly retention check by scheduled script; access restricted to [role list]; log event fields include {timestamp, type, user_id, action, ...}

**Dependencies** / **Conflicts**:
- **Depends on:** FR-072
- **Conflicts with:** NFR-011
---

[NFR-011]: Logging overhead constraint (implied)
**Description:** Test mode adds logging on top of normal operations (“performs normal mode operations and also logs activities”). Updated per evaluator: Acceptance: Measured query latency under 1000 events/min ingest with/without test mode; pass if test mode median latency is ≤10% greater vs normal mode. [Next action: Design performance acceptance script and publish results template.]
  
**Quality Attributes**: Performance, Capacity

**Measurable Criteria (if provided):** Under 1000 events/min ingest, test mode median query latency ≤10% greater than normal mode

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-010, FR-071
- **Conflicts with:** NFR-010
---

[NFR-012]: Server platform constraint: Microsoft Windows NT
**Description:** “The Center-to-Center Server shall execute in a Microsoft Windows NT environment.” and “The Center-to-Center shall execute in a Microsoft Windows NT environment.” Updated per evaluator: The system shall be certified on Windows Server 2019+; Windows NT 4.0 SP6a permitted for legacy deployments only with signed waiver, EOL 12/2025. [Next action: Document formal migration/deprecation plan and risk escalation cycle.]
  
**Quality Attributes**: Portability (constraint), Deployability

**Measurable Criteria (if provided):** Windows Server 2019+ certification; Windows NT 4.0 SP6a legacy-only with signed waiver; EOL 12/2025

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004
- **Conflicts with:** NFR-005
---

[NFR-013]: Runtime dependency: DATEX/ASN runtime library required
**Description:** “A DATEX/ASN runtime library shall be available on any computer communicating to the Center-to-Center project.” Updated per evaluator: All deployments must provide DATEX/ASN runtime v1.7.0, compatible with [API spec]. [Next action: Document and enforce version and interface constraints for runtime library.]
  
**Quality Attributes**: Deployability, Interoperability

**Measurable Criteria (if provided):** DATEX/ASN runtime v1.7.0; compatible with [API spec]

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, NFR-003
- **Conflicts with:** NFR-015
---

[NFR-014]: Web server mapping technology constraint: ESRI ARC IMS
**Description:** “The web server application shall use ESRI's ARC Internet Map Server (ARC IMS) product for creating of map images.” Updated per evaluator: ESRI ARC IMS 10.2 with [component list], support and license required for [named features]. [Next action: Catalog all required ESRI product features/components.]
  
**Quality Attributes**: Maintainability (vendor constraint), Deployability

**Measurable Criteria (if provided):** ESRI ARC IMS 10.2; required components: [component list]; support and license required for [named features]

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-012
---

[NFR-015]: Implementation language constraint: C/C++
**Description:** “The Center-to-Center shall be implemented in the C/C++ programming language.” Updated per evaluator: Core modules must be implemented in C/C++, but future adapters (e.g., REST API) may use .NET/Java. [Next action: Document rationale for this constraint and any exceptions.]
  
**Quality Attributes**: Maintainability (constraint), Portability (constraint)

**Measurable Criteria (if provided):** Core modules in C/C++; adapters/wrappers may use .NET/Java

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-012
- **Conflicts with:** NFR-016
---

[NFR-016]: UI implementation technology constraints (ESRI components + C/C++)
**Description:** “The Center-to-Center web interface shall be implemented using C/C++ and ESRI ARC IMS. The Incident GUI shall be implemented using C/C++ and ESRI Map Objects. The Remote Control GUI shall be implemented using C/C++ and ESRI Map Objects.” Updated per evaluator: The Incident GUI must use ESRI Map Objects v2.4+. [Next action: Add supported UI technology version(s) and update as per vendor life-cycle.]
  
**Quality Attributes**: Maintainability (vendor constraint), Deployability

**Measurable Criteria (if provided):** ESRI Map Objects v2.4+ (Incident GUI)

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014, NFR-015
- **Conflicts with:** NFR-012
---