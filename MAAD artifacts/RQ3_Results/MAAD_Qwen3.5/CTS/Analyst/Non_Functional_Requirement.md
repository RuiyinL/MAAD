# Non-Functional Requirements Results:

[NFR-001]: Search Performance - Simple Search
**Description:** The CCTNS system must be able to perform a simple search within 5-8 seconds regardless of the storage capacity or number of cases in the CCTNS system. It does not include retrieving the records themselves. Metric: search_simple_time_p95 <8s, measured at browser by SRE synthetic bot, alert if >8s in 3 checks.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** 5-8 seconds for simple search. Metric: search_simple_time_p95 <8s.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Search Optimization), ASR-009 (Database Indexing)
- **Conflicts with:** None identified
---

[NFR-002]: Search Performance - Advanced Search
**Description:** The CCTNS system must be able to perform an advanced search (multiple search criteria) within 10-15 seconds regardless of the storage capacity or number of cases in the CCTNS system. Metric: search_advanced_time_p95 <15s, measured at browser by SRE synthetic bot.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** 10-15 seconds for advanced search. Metric: search_advanced_time_p95 <15s.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Search Optimization), ASR-009 (Database Indexing)
- **Conflicts with:** None identified
---

[NFR-003]: Case Retrieval Performance - Recent Cases
**Description:** The CCTNS system must be able to retrieve and display within 5-8 seconds the case which has been accessed within the previous 2 months, regardless of storage capacity or number of cases in the CCTNS system. Metric: case_retrieve_recent_p95 <8s, measured at browser by SRE synthetic bot.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** 5-8 seconds for cases accessed within 2 months. Metric: case_retrieve_recent_p95 <8s.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Caching Strategy)
- **Conflicts with:** None identified
---

[NFR-004]: Case Retrieval Performance - Older Cases
**Description:** The CCTNS system must be able to retrieve and display within 20 seconds the case which has not been accessed within the previous 2 months, regardless of storage capacity or number of cases in the CCTNS system. Metric: case_retrieve_old_p95 <20s, measured at browser by SRE synthetic bot.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** 20 seconds for cases not accessed within 2 months. Metric: case_retrieve_old_p95 <20s.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Caching Strategy)
- **Conflicts with:** None identified
---

[NFR-005]: System Availability
**Description:** The CCTNS system must be available at least 99.9% of the time, 24x7, with no more than 8 hours planned downtime per rolling three month period. Downtime counted if SRE agent cannot complete login+search in 1 minute; automated alert if downtime >4 hours/quarter.

**Quality Attributes**: Availability

**Measurable Criteria (if provided):** 99.9% availability, 24x7, max 8 hours planned downtime per rolling three month period. Downtime measurement: SRE agent login+search <1 min.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Centralized Deployment)
- **Conflicts with:** None identified
---

[NFR-006]: Unplanned Downtime Limit
**Description:** Unplanned downtime for the CCTNS system must not exceed 4 hours per rolling three month period. The number of incidents of unplanned downtime must not exceed 2 per rolling three month period. Downtime counted if SRE agent cannot complete login+search in 1 minute.

**Quality Attributes**: Reliability, Availability

**Measurable Criteria (if provided):** Max 4 hours unplanned downtime, max 2 incidents per rolling three month period.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Centralized Deployment)
- **Conflicts with:** None identified
---

[NFR-007]: System Recovery Time
**Description:** Restoration of CCTNS, with all data resync, must complete within 8 hours of a hardware/software incident. RTO proof via failover/simulation.

**Quality Attributes**: Reliability, Recoverability

**Measurable Criteria (if provided):** 8 hours RTO including data resync.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Centralized Deployment)
- **Conflicts with:** None identified
---

[NFR-008]: Scalability
**Description:** The CCTNS system be scaleable and must not have any features which would preclude use in small or large police stations, with varying numbers of cases handled. System shall support 10,000 concurrent users making search/registration requests at 1 req/user/min with <1% error, <12s response. Acceptance: Pass core regression suite on 1, 100, 10,000 user environments.

**Quality Attributes**: Scalability

**Measurable Criteria (if provided):** 10,000 concurrent users, 10 million records, <1% error rate, <12s response at 1 req/user/min. Acceptance: Pass core regression suite on 1, 100, 10,000 user environments.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (SOA Architecture), ASR-010 (Scalability Design)
- **Conflicts with:** None identified
---

[NFR-009]: Multilingual Support
**Description:** The CCTNS system should support multilingual interface. The CCTNS system must support at least Hindi and English in all user interface elements and help content, with coverage exceeding 99% of all UI labels and error messages. Metric: multilingual_coverage_pct >=99% (count all UI strings/localized labels).

**Quality Attributes**: Usability, Portability

**Measurable Criteria (if provided):** Hindi and English supported, 99% coverage of UI labels and error messages. Metric: multilingual_coverage_pct >=99%.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[NFR-010]: Offline Operation
**Description:** The CCTNS system should work even in an offline mode with the critical functionality. The CCTNS system should be designed in manner that operational data is not lost in case of any failure of equipment or communication network. Registration and search must operate offline for up to 48h, with all unsynced data queued and synced within 30m of reconnection; define test cases for data merge conflicts. Acceptance: Any sync conflict logged and reported to user/admin, with auto-resolve documented.

**Quality Attributes**: Reliability, Availability

**Measurable Criteria (if provided):** Offline operation for Registration/Search up to 48 hours, sync within 30 minutes.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Centralized Deployment)
- **Conflicts with:** NFR-001, NFR-002 (Performance requirements may conflict with offline sync), ASR-003 (Centralized Deployment - reconciled via local persistence with encrypted sync)
---

[NFR-011]: Low-Bandwidth Performance
**Description:** The CCTNS system should be designed to have satisfactory performance even in Police Stations connected on low-bandwidth. At 256 kbps bandwidth, system must return search results in <= 12 seconds. Registration of a complaint must complete within 20 seconds at 256 kbps.

**Quality Attributes**: Performance, Portability

**Measurable Criteria (if provided):** 256 kbps bandwidth, search results <= 12 seconds, registration <= 20 seconds.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-010 (Scalability Design)
- **Conflicts with:** None identified
---

[NFR-012]: ISO 9241 Compliance
**Description:** The user interfaces of the CCTNS system should comply with Standard ISO 9241. ICT accessibility: ISO 9241-20 shall be the standard for guidance on ICT accessibility. Software accessibility ISO 9241-171 shall be the standard for guidance on software accessibility. System UIs must pass 'ISO 9241-171 Accessibility' QA checklist (include citation) and record results in accessibility conformance report. Metric: iso_9241_audit_pass == true for each major release, with attached conformance report.

**Quality Attributes**: Usability, Accessibility

**Measurable Criteria (if provided):** ISO 9241, ISO 9241-20, ISO 9241-171 compliance with QA checklist and conformance report.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[NFR-013]: Screen Text Legibility
**Description:** Text presented on the pages should be readable taking into account the expected display characteristics and spatial arrangement. ISO 9241-303 shall be consulted for screen text legibility requirements. QA provides completed ISO 9241-303 checklist for each release.

**Quality Attributes**: Usability, Accessibility

**Measurable Criteria (if provided):** ISO 9241-303 compliance with QA checklist per release.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[NFR-014]: Browser Compatibility
**Description:** The CCTNS system should run on multiple browsers. Support: Chrome ≥108, Edge ≥108, Safari ≥15, Firefox ≥108. All functional smoke tests pass in CI for each major release. Acceptance: browser_smoke_matrix must pass for all browsers, result posted to release notes.

**Quality Attributes**: Portability, Compatibility

**Measurable Criteria (if provided):** Chrome ≥108, Edge ≥108, Safari ≥15, Firefox ≥108 with CI smoke tests.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Browser-based Access)
- **Conflicts with:** None identified
---

[NFR-015]: SSL/TLS Encryption
**Description:** The CCTNS system should support SSL encrypted connections. The CCTNS system should use HTTPS as the communication protocol, i.e, HTTP over an encrypted secure socket layer (SSL). All connections must use TLS 1.2 or higher with 2048-bit RSA or 256-bit ECC; reject self-signed or expired certs. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** TLS 1.2+, 2048-bit RSA or 256-bit ECC, no self-signed/expired certs. SAST/DAST 0 Critical/High.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-016]: Cross-Site Scripting Prevention
**Description:** The CCTNS system should ensure high standards of security and access control through preventing cross-site scripting. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** XSS prevention required. SAST/DAST 0 Critical/High.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-017]: SQL Injection Prevention
**Description:** The CCTNS system should ensure high standards of security and access control through preventing SQL Injection. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** SQL Injection prevention required. SAST/DAST 0 Critical/High.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-018]: Input Validation and Sanitization
**Description:** The CCTNS system should ensure high standards of security and access control through sanitizing the user-inputs, validating the incoming data or user request, encoding the incoming data or user request, and validating the data both at the client and server. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** Input validation and sanitization required. SAST/DAST 0 Critical/High.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-019]: Data Encryption at Rest
**Description:** The CCTNS system should support selective encryption of the stored data. Case narrative and personal identifiers must be encrypted at rest with AES-256 using per-tenant key management. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release; DLP log—no unencrypted export.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** AES-256 encryption for case narrative and personal identifiers with per-tenant key management.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-020]: Network Security
**Description:** The CCTNS system should ensure secure transmission of data over the network and utilize SSL and 2-way digital signatures. The CCTNS system should support secure virtual private network connections. System passes: (1) external user connects via site-to-site IPSec VPN; (2) all data in transmission is digitally signed and verifiable by recipient. Acceptance: SAST/DAST scan results—0 Critical or High findings allowed per release.

**Quality Attributes**: Security

**Measurable Criteria (if provided):** IPSec VPN connectivity, digital signature verification for all transmitted data.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---

[NFR-021]: Soft Delete Requirement
**Description:** The CCTNS system should ensure high standards of security and access control through do not allow hard delete and perform only soft tagging the row for deletion. All deletions must update a 'deleted_at' timestamp without removing the row. Deleted rows retained at least 7 years. Acceptance: daily jobs verify all deleted rows or audit trails retained >=7 years or case end+7y.

**Quality Attributes**: Security, Data Integrity

**Measurable Criteria (if provided):** Soft delete with deleted_at timestamp, 7-year retention for deleted rows.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Unalterable Audit Trail)
- **Conflicts with:** None identified
---

[NFR-022]: Error Message Clarity
**Description:** All error messages produced by the CCTNS system must be meaningful, so that they can be appropriately acted upon by the users who are likely to see them. Users expect error messages to be in the same language as the user interface.

**Quality Attributes**: Usability

**Measurable Criteria (if provided):** Meaningful, actionable error messages in UI language

**Dependencies** / **Conflicts**:
- **Depends on:** FR-023 (Error Message Display)
- **Conflicts with:** None identified
---

[NFR-023]: User Interface Consistency
**Description:** The CCTNS system must employ a single set of user interface rules, or a small number of sets to provide a familiar and common look and feel for the application. Acceptance: system_ui_rule_sets <=3, enforced in config.

**Quality Attributes**: Usability

**Measurable Criteria (if provided):** Single or small number of UI rule sets. Max 3 sets.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[NFR-024]: Navigation Self-Descriptiveness
**Description:** Navigation should be designed to help users understand where they are, where they have been and where they can go next. Each presentation segment (page or window) should provide the user with a clear and sufficient indication of where he or she is in the navigation structure. Metric: iso_9241_audit_pass == true for each major release, with attached conformance report.

**Quality Attributes**: Usability

**Measurable Criteria (if provided):** ISO 9241-110 compliance.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Role-Based Navigation)
- **Conflicts with:** None identified
---

[NFR-025]: Page Load Time
**Description:** Application pages should be designed and implemented so that there are acceptable opening times and download times for the expected range of technical contexts of use (e.g. bandwidth between the application and the user). This is particularly important for frequently accessed pages or pages that are important for user navigation and exploration, such as the home page. Home and main navigation pages must load <3 seconds at 2 Mbps; other pages <5 seconds. Metric: home_page_load_p90_ms, measured at browser via Synthetic SRE bot, alert if >3000ms for 3 checks in a row. Acceptance: home_page_load_p90_ms <3000ms, alert if over 3x.

**Quality Attributes**: Performance

**Measurable Criteria (if provided):** Home/nav pages <3 seconds at 2 Mbps; other pages <5 seconds. SRE alert: p90 >3000ms for 3 consecutive checks.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-010 (Scalability Design), NFR-011 (Low-Bandwidth Performance)
- **Conflicts with:** None identified
---

[NFR-026]: Audit Trail Retention
**Description:** The CCTNS system must maintain the audit trail for as long as required, which will be at least for the life of the case to which it refers. Acceptance: daily jobs verify all deleted rows or audit trails retained >=7 years or case end+7y.

**Quality Attributes**: Security, Compliance

**Measurable Criteria (if provided):** Minimum: life of the case. Daily retention check.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Unalterable Audit Trail)
- **Conflicts with:** None identified
---

[NFR-027]: Audit Trail Accessibility
**Description:** The CCTNS system must ensure that audit trail data is available for inspection on request, so that a specific event can be identified and all related data made accessible, and that this can be achieved by authorised external personnel who have little or no familiarity with the CCTNS system.

**Quality Attributes**: Security, Compliance, Usability

**Measurable Criteria (if provided):** Available for inspection by authorized external personnel

**Dependencies** / **Conflicts**:
- **Depends on:** FR-015 (Audit Trail Export)
- **Conflicts with:** None identified
---

[NFR-028]: Minimal Client Requirements
**Description:** The CCTNS system should be designed for access through browser-based systems and must impose minimal requirements on the client device.

**Quality Attributes**: Portability, Usability

**Measurable Criteria (if provided):** Minimal client device requirements

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Browser-based Access)
- **Conflicts with:** None identified
---

[NFR-029]: Multiple Communication Services
**Description:** The CCTNS system must support multiple types of communication services for remote access.

**Quality Attributes**: Portability, Compatibility

**Measurable Criteria (if provided):** Multiple communication service types

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Communication Services)
- **Conflicts with:** None identified
---

[NFR-030]: Public Access Capability
**Description:** The CCTNS system should have capability to support public access to a subset of data and functionality. Public interface allows read-only search on case summaries (no PII), up to 100 requests/hour per IP.

**Quality Attributes**: Security, Accessibility

**Measurable Criteria (if provided):** Read-only case summaries (no PII), 100 requests/hour per IP rate limit.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control), ASR-011 (Security Architecture)
- **Conflicts with:** None identified
---