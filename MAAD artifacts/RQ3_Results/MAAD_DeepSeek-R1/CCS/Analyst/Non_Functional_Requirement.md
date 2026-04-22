# Non-Functional Requirements Results:
[NFR-001]: Deterministic Response  
**Description:** The system shall respond to hardware inputs within 2ms (99.99% of operations) with zero missed/corrupted data per hour during normal operations.  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** Response ≤2ms (99.99%), zero data loss/corruption per hour  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-003  
---

[NFR-002]: Fault Isolation Guidance  
**Description:** Repair time measured during 24x7 support; guidance rendered as GUI checklist ≤10s post-isolation.  
**Quality Attributes**: Maintainability  
**Measurable Criteria (if provided):** Fault isolation ≤1 min, repair ≤5 min  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---

[NFR-003]: Critical Event Logging  
**Description:** Log events include: event_type, correlator_id, state, UTC_timestamp, user_id.  
**Quality Attributes**: Maintainability, Usability  
**Measurable Criteria (if provided):** Log latency≤1s, retention=30 days  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-006  
---

[NFR-004]: Measured Hardware Expandability  
**Description:** Hardware shall be expandable to at least double initial throughput with ≤30 min downtime per expansion event.  
**Quality Attributes**: Scalability  
**Measurable Criteria (if provided):** 2x throughput, ≤30 min downtime  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-007  
---

[NFR-005]: Validated Code Coverage  
**Description:** Maintain >90% branch coverage in CI builds, measured with 'gcovr' during simulation-mode tests.  
**Quality Attributes**: Maintainability  
**Measurable Criteria (if provided):** >90% branch coverage via gcovr  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-011  
---