# Non-Functional Requirements Results:
[NFR-001]: Performance
**Description:** SLI: user_response_latency_sec (P95 ≤2s, 5min rolling); alert if >2s in >5% of requests.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):**  P95 ≤2s, 5min rolling
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-002]: Security
**Description:** Audit storage: AES-256-GCM, keys rotated yearly, GDPR-compliant deletion workflow for audit logs.
**Quality Attributes**: Security
**Measurable Criteria (if provided):**  AES-256-GCM, yearly key rotation
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003
- **Conflicts with:** None
---
[NFR-003]: Usability
**Description:** 'Acknowledge' = UI button click, event logged to DB; measurement window = time since alert visible to acknowledgment click.
**Quality Attributes**: Usability
**Measurable Criteria (if provided):**  UI button click, event logged to DB
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-004]: Reliability
**Description:** SLI: system_uptime, system_mttr; monitor in ops dashboard, alert at <99.95%; MTTR >30min.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):**  system_uptime, system_mttr
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-005]: Maintainability
**Description:** 80%+ unit+integration test coverage per main modules; WIP break glass for <80%.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):**  80%+ test coverage
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-006]: Availability
**Description:** SLI: system_availability; alert on drop below 99.95% or >5min outage.
**Quality Attributes**: Availability
**Measurable Criteria (if provided):**  99.95% availability
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[NFR-007]: Scalability
**Description:** Test with 500 simulated/pseudo-patient devices, measure mean response time, fail if increase >1%.
**Quality Attributes**: Scalability
**Measurable Criteria (if provided):**  500 concurrent patients, <1% increase in response time
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---