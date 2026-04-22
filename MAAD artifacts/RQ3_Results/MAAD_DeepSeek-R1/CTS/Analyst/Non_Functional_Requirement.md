# Non-Functional Requirements Results:
[NFR-001]: Context-Sensitive Help Usability  
**Description:** Acceptance if 100% of user interface actions have a help link taking user to detailed, context-specific documentation.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** 100% coverage of UI actions  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-014  
- **Conflicts with:**   
---

[NFR-002]: Error Message Clarity  
**Description:** Acceptance if all system error messages are reviewed against a template: [problem description], [user action], and pass usability testing by at least 3 end users.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** Template compliance and usability validation  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-014  
- **Conflicts with:**   
---

[NFR-003]: UI Consistency  
**Description:** UI must fully comply with [document url or ID], owned by [role], and published at [location].  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** Guideline compliance  

**Dependencies** / **Conflicts**:  
- **Depends on:**   
- **Conflicts with:**   
---

[NFR-004]: UI Customization  
**Description:** User UI layout is saved to the central user profile store, persisted and synced at each login/logout; settings follow users to any workstation.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** Centralized profile persistence  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005  
- **Conflicts with:**   
---

[NFR-005]: Accessibility Compliance  
**Description:** Acceptance if all UI components satisfy ISO 9241-171 section 9 and pass W3C WCAG 2.1 Level AA checks on Chrome, Edge, and Firefox.  

**Quality Attributes**: Accessibility  

**Measurable Criteria (if provided):** ISO 9241-171 compliance + WCAG 2.1 AA  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001  
- **Conflicts with:**   
---

[NFR-006]: Navigation Efficiency  
**Description:** Acceptance if registration can be completed within 5 steps and case search within 3 steps from landing page, as validated by usability testing.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** Max step counts for key workflows  

**Dependencies** / **Conflicts**:  
- **Depends on:**   
- **Conflicts with:**   
---

[NFR-007]: Input Validation & Sanitization  
**Description:** Acceptance if code passes OWASP ASVS Level 2 input validation and ZAP/DAST scan shows no critical findings.  

**Quality Attributes**: Security  

**Measurable Criteria (if provided):** OWASP ASVS Level 2 compliance  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-009  
- **Conflicts with:**   
---

[NFR-008]: Connection Security  
**Description:** All endpoints use HTTPS w/ TLS 1.2+ (PCI compliant ciphers, A grade on SSL Labs); VPN requires IPsec/IKEv2; two-way signatures implemented with X.509 PKI.  

**Quality Attributes**: Security  

**Measurable Criteria (if provided):** TLS 1.2+ protocols  

**Dependencies** / **Conflicts**:  
- **Depends on:**   
- **Conflicts with:**   
---

[NFR-009]: Availability Targets  
**Description:** Central availability measured by hourly synthetic login and CRUD check on /api/cases; branch by local ping + check for offline transaction acceptance. 99.9% online (≤4h quarterly); 99% offline (≥99% op hours/branch).  

**Quality Attributes**: Availability  

**Measurable Criteria (if provided):** Online: ≤4h downtime/quarter; Offline: ≥99% station uptime  

**Dependencies** / **Conflicts**:  
- **Depends on:**   
- **Conflicts with:** NFR-011 (offline mode)  
---

[NFR-010]: Query Performance  
**Description:** Measure search performance using /api/caseSearch with synthetic users running hourly (24/7). If P95 search time >10s for >3 intervals in 72h, SRE alert triggered.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided):** Automated hourly measurement  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
- **Conflicts with:** NFR-011 (offline mode)  
---