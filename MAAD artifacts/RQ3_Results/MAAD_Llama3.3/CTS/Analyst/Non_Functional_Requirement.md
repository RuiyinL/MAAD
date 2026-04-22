# Non-Functional Requirements Results:
[NFR-001]: User-Friendliness
**Description**: Acceptance: 95% of user interface actions have context-sensitive help; help must appear within 2s and be rated at least 4/5 by usability test group.
**Quality Attributes**: Usability
**Measurable Criteria (if provided)**: 95% of user interface actions have context-sensitive help; help must appear within 2s and be rated at least 4/5 by usability test group.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-002]: Performance
**Description**: Retrieve case details in <8s (P95); page load <3s P95 under peak load; 0 error budget for observed SLO breaches in production.
**Quality Attributes**: Performance
**Measurable Criteria (if provided)**: Retrieve case details in <8s (P95); page load <3s P95 under peak load; 0 error budget for observed SLO breaches in production.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** None
---
[NFR-003]: Security
**Description**: Acceptance: CVSS 9+ findings = 0, others tracked, fix SLA: critical 24h, report must be attached to release ticket.
**Quality Attributes**: Security
**Measurable Criteria (if provided)**: CVSS 9+ findings = 0, others tracked, fix SLA: critical 24h, report must be attached to release ticket.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[NFR-004]: Availability
**Description**: System must be available 24x7x365 except for scheduled maintenance, which is limited to 2 hours per calendar quarter, with total unplanned downtime not exceeding 120 minutes per calendar quarter. Measurement is from first user impact to full service restoration.
**Quality Attributes**: Availability
**Measurable Criteria (if provided)**: System must be available 24x7x365 except for scheduled maintenance, which is limited to 2 hours per calendar quarter, with total unplanned downtime not exceeding 120 minutes per calendar quarter. Measurement is from first user impact to full service restoration.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-005]: Scalability
**Description**: Scalability test: 100 queries/sec, P95 latency <2s, in production-like env; 'active user' is any logged-in user performing >=1 trans per 10min.
**Quality Attributes**: Scalability
**Measurable Criteria (if provided)**: Scalability test: 100 queries/sec, P95 latency <2s, in production-like env; 'active user' is any logged-in user performing >=1 trans per 10min.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-006]: Accessibility
**Description**: All UI content must meet WCAG 2.1 AA for each supported language; compliance confirmed by external audit each major release.
**Quality Attributes**: Accessibility
**Measurable Criteria (if provided)**: All UI content must meet WCAG 2.1 AA for each supported language; compliance confirmed by external audit each major release.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-007]: Data Integrity
**Description**: All user-visible errors must return {code, message, action}; 90%+ of testers must report error is actionable during validation.
**Quality Attributes**: Data Integrity
**Measurable Criteria (if provided)**: All user-visible errors must return {code, message, action}; 90%+ of testers must report error is actionable during validation.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-008]: Maintainability
**Description**: Each config/release event is logged and weekly test restores performed for all critical configs.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided)**: Each config/release event is logged and weekly test restores performed for all critical configs.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---