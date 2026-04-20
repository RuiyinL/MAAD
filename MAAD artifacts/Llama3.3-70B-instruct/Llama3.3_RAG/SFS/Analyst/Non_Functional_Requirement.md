# Non-Functional Requirements Results:
[NFR-001]: Security
**Description:** All data in transit must use TLS 1.2+; administrator authentication must require at least an 8-character password with symbols and numbers. The system must limit admin login attempts to 5 per 15 mins, session auto-expiry at 10m idle. All audit logs must be encrypted at rest using AES-256.
**Quality Attributes**: Security
**Measurable Criteria (if provided):** TLS 1.2+, 8-character password with symbols and numbers, 5 attempts per 15 minutes
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-002]: Reliability
**Description:** 99% unit test coverage; mean time between failures (MTBF) > 6 months; unplanned downtime less than 1 hour/month. Alert if 'unit_test_coverage' <99% on merge; MTBF violation reported if incidents/6mo > 1.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):** 99% unit test coverage, MTBF > 6 months, unplanned downtime less than 1 hour/month
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-003]: Maintainability
**Description:** Code merged to 'main' requires complexity report <10 and approval by two users not author.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):** Complexity report <10, approved by two users
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-004]: Performance
**Description:** Initial load time must be < 2 seconds over typical school Wi-Fi (100 kB/s); response to user input < 250 ms. Acceptance: Load time measured via Lighthouse on 100 kB/s throttled connection, Chrome (last 2 versions), for initial full load.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** Initial load time < 2 seconds, response to user input < 250 ms
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-005]: Usability
**Description:** At least 90% of surveyed sixth graders must complete onboarding with zero external help; System Usability Scale (SUS) score ≥ 80. Acceptance: At least 90% of randomly selected 6th graders can complete from intro screen to first completed challenge without teacher/peer input.
**Quality Attributes**: Usability
**Measurable Criteria (if provided):** 90% completion rate, SUS score ≥ 80
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---