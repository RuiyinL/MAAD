# Non-Functional Requirements Results:
[NFR-001]: Performance Requirement for Map Display
**Description:** The map shall display interstates and state highways within 2 seconds of request under 95% of typical operational load.
**Quality Attributes**: Performance
**Measurable Criteria (if provided):** 2 seconds, 95% of typical operational load
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[NFR-002]: Security Requirement for Remote Control
**Description:** The Remote Center Control GUI shall require two-factor authentication; all traffic must use TLS 1.2 or higher; all access attempts are logged with userID, timestamp, IP. After 5 failed login attempts, account disabled for 15min. Auth/audit logs must be retained for at least 90 days.
**Quality Attributes**: Security
**Measurable Criteria (if provided):** Two-factor authentication, TLS 1.2 or higher, 5 failed login attempts, 15min account disable, 90 days log retention
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[NFR-003]: Usability Requirement for Incident GUI
**Description:** 80% of users shall be able to enter incident or lane closure information within 60 seconds after 30 minutes of system training.
**Quality Attributes**: Usability
**Measurable Criteria (if provided):** 80% of users, 60 seconds, 30 minutes of system training
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[NFR-004]: Maintainability Requirement for Center-to-Center
**Description:** Cyclomatic complexity ≤10 per method as measured by 'lizard' tool; coverage via gcov XML summary.
**Quality Attributes**: Maintainability
**Measurable Criteria (if provided):** Cyclomatic complexity ≤10, 'lizard' tool, gcov XML summary
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-005]: Portability Requirement for Web Interface
**Description:** The web interface shall support Microsoft Edge and Google Chrome with 100% functional parity as verified in regression testing.
**Quality Attributes**: Portability
**Measurable Criteria (if provided):** Microsoft Edge, Google Chrome, 100% functional parity
**Dependencies** / **Conflicts**:
- **Depends on:** FR-076
- **Conflicts with:** None
---
[NFR-006]: Scalability Requirement for Center-to-Center
**Description:** Log: concurrent_tmc_sessions, message_rate, avg_response_time per 5min; alert if degradation >10%.
**Quality Attributes**: Scalability
**Measurable Criteria (if provided):** concurrent_tmc_sessions, message_rate, avg_response_time, 5min window, >10% degradation alert
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[NFR-007]: Availability Requirement for Center-to-Center
**Description:** Center-to-Center shall achieve at least 99.5% availability per calendar month, measured as maximum 3.65 hours downtime/month.
**Quality Attributes**: Availability
**Measurable Criteria (if provided):** 99.5% availability, 3.65 hours downtime/month
**Dependencies** / **Conflicts**:
- **Depends on:** FR-081
- **Conflicts with:** None
---
[NFR-008]: Reliability Requirement for Device Control
**Description:** For 99.9% of device command/control status requests, status shall be returned and displayed within 3 seconds.
**Quality Attributes**: Reliability
**Measurable Criteria (if provided):** 99.9% of device command/control status requests, 3 seconds
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None