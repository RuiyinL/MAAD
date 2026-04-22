# Non-Functional Requirements Results:
[NFR-001]: Control information throughput  
**Description:** Peak control information within system shall not exceed 100 transactions per second (TPS).  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided):** 100 TPS maximum  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006 (Command protocol)  
---  
[NFR-002]: Data storage capacity  
**Description:** System must retain 7 days of data from largest instrument with last 3 days interactively available.  

**Quality Attributes**: Capacity  

**Measurable Criteria (if provided):** 7 days retention, 3 days interactive access  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-007 (Data acquisition)  
---  
[NFR-003]: Response time constraints  
**Description:** Commands must be accepted/rejected within 2 seconds; status displays must update within 4 seconds locally. Command response: 99% of commands must respond within 2 seconds over a 7-day window, monitored via Prometheus query over API server logs, paged to SRE on breach. Status display update: within 4 seconds locally.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided):** Command response: 99% within 2s (7-day window); status update: 4s  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004 (Real-time constraints)  
---  
[NFR-004]: LAN bandwidth  
**Description:** LAN must support 20-40 Mbits/second transfer rate for astronomical data.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided):** 20-40 Mbits/s  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-007 (Data acquisition)  
---  
[NFR-005]: Concurrent node support  
**Description:** System must support six active control nodes plus two monitoring nodes without performance degradation.  

**Quality Attributes**: Scalability  

**Measurable Criteria (if provided):** 8 total nodes (6 active + 2 monitoring)  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001 (Distributed architecture)  
---  
[NFR-006]: Fault notification  
**Description:** Subsystems must notify users and log event within 10s of detecting a fault; log entry shall include timestamp, module ID, error code, and description. Structured log format; 'fault_notify_within_10s_pct' measured daily via log pipeline; SRE is paged if <99%.  

**Quality Attributes**: Reliability  

**Measurable Criteria (if provided):** Notification within 10s; structured log format; 99% SLO  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-008 (Fault recovery)  
---  
[NFR-007]: Recovery time objective  
**Description:** System must recover/reconfigure within 5 minutes from error onset. Recovery is achieved when non-faulted subsystems are fully operational and interface response is normal, all within 5 minutes; automatically measured and logged. Metric: 'error_to_ready_time' measured per incident; alert if exceeding 5 minutes.  

**Quality Attributes**: Reliability  

**Measurable Criteria (if provided):** 5 minutes with operational verification  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-008 (Fault recovery)  
---  
[NFR-008]: Database access time  
**Description:** Access times to online database must be 2-3ms per access.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided):** 2-3ms  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-007 (Centralized configuration)  
---  
[NFR-009]: Security protocols  
**Description:** Mutual TLS required at ingress; LDAP group 'gemini-astronomer', 'gemini-operator', etc. enforced via 'memberOf' attribute. Audit log: JSON line, with ISO8601, userID, action, IP. Log retention: min 1 year; failed logins result in HTTP 401 and warning audit log.  

**Quality Attributes**: Security  

**Measurable Criteria (if provided):** Mutual TLS + LDAP; audit logging; 1y retention  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001, ASR-002  
---  
[NFR-010]: Uniform user interface  
**Description:** User interfaces must maintain consistent "look and feel" across subsystems while reflecting access modes/levels. All UI modules must pass conformance test per Gemini UI Style Guide v1.0. Acceptance: UI module passes Gemini UI Style Guide v1.0 checklist (Appendix A) and tested by automated tool 'gemini-ui-conform'. UI Lead signs off checklist for release; any automated conformance test failure is a release blocker unless waiver is logged in JIRA.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided):** Style Guide conformance verification  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012 to FR-017  
---