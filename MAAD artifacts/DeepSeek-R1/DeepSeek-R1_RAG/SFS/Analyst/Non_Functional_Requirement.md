# Non-Functional Requirements Results:
[NFR-001]: Target User Usability  
**Description**: At least 95% of sixth-grade test users are able to navigate main menu and complete one question without external assistance within 2 minutes.  
**Quality Attributes**: Usability  
**Measurable Criteria (if provided):** 95% success rate within 2 minutes  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002  
---  

[NFR-002]: Content Load Performance  
**Description**: System must load playable content within 5 seconds over a 10Mbps connection (90th percentile of sessions).  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** ≤5 seconds load time at 90th percentile  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---  

[NFR-003]: Security Controls  
**Description**: All user/admin authentication flows must use TLS 1.2+; password hashes must use bcrypt with 12 rounds; unsuccessful admin logins are logged to server-side storage. Passwords must be ≥12 characters with uppercase/lowercase/numeric/special complexity; admin reset flows must validate identity and enforce complexity.  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** TLS 1.2+, bcrypt-12 hashing, login attempt logging, ≥12 char complexity  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004, ASR-007  
---  

[NFR-004]: Global Availability  
**Description**: The system must demonstrate ≥99% HTTP(S) accessibility from at least 3 global regions (Americas, EMEA, APAC) measured via synthetic checks over a 30-day period. Metric: website.available; measured via external synthetic checks every 5 min; ≥99% success rate from target geos.  
**Quality Attributes**: Availability  
**Measurable Criteria (if provided):** ≥99% accessibility from 3 regions  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-002  
---  

[NFR-005]: Reliability Targets  
**Description**: Acceptance: End-user HTTP(S) endpoint delivers 99% uptime over any rolling 30-day window; alert triggered on >10 minutes consecutive downtime. Metric: website.available; checked every 5min; alert >10min downtime or <99% in 30-day window.  
**Quality Attributes**: Reliability  
**Measurable Criteria (if provided):** 99% uptime with alerting  
**Dependencies** / **Conflicts**:  
---  

[NFR-006]: Maintainability Metrics  
**Description**: Source code maintains average cyclomatic complexity below 10; at least 80% line coverage in automated tests.  
**Quality Attributes**: Maintainability  
**Measurable Criteria (if provided):** CC<10, coverage≥80%  
**Dependencies** / **Conflicts**:  
---  

[NFR-007]: Concurrency Model  
**Description**: Only one active user session per browser instance; system supports unlimited concurrent users globally (stateless web).  
**Quality Attributes**: Concurrency  
**Measurable Criteria (if provided):** Single session per instance  
**Dependencies** / **Conflicts**:  
---