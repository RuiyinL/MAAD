# Non-Functional Requirements Results (NFRs)

[NFR-001]: Command acceptance/handshake timing requirements  
**Description:** “Timeouts must be supported at approximately 500 msec. Handshaking of commands between IOCs must occur within 100-200 msec…” and “Every command must be accepted/rejected within 2 sec and before the corresponding action occurs.”  
**Quality Attributes**: Performance, Real-time responsiveness  
**Measurable Criteria (if provided):** 500 ms timeouts; IOC handshake 100–200 ms; command accept/reject ≤ 2 s.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-033  
- **Conflicts with:** NFR-014 (logging overhead), NFR-008 (security checks latency)  
---

[NFR-002]: Peak control throughput  
**Description:** “Peak control information within the system is expected to be 100 TPS.”  
**Quality Attributes**: Performance, Scalability  
**Measurable Criteria (if provided):** 100 transactions per second (TPS).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-033  
- **Conflicts with:** NFR-014  
---

[NFR-003]: Non-interference with ongoing observations  
**Description:** “Under no circumstances should monitoring/testing/administrative access affect the performance of an ongoing observation.” Updated per evaluator: Acceptance: During 1h at max load, monitoring/test/admin ops increase median and p95 observing command latency ≤ 2% vs baseline. Metric: obs_cmd_latency_pct_change; window=1h; alert threshold >2% increase. Owner: Team-SRE; Next action: Add SLO metric and test procedure for 2% impact clause.  
**Quality Attributes**: Performance isolation, Reliability  
**Measurable Criteria (if provided):** obs_cmd_latency_pct_change measured over 1h window; median and p95 latency increase ≤ 2% vs baseline under max load; alert if >2% increase.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, FR-008, FR-009  
- **Conflicts with:** FR-063, FR-045 (if compute contention)  
---

[NFR-004]: Status update responsiveness  
**Description:** “Status display update must be within 4 sec at the local stations… Requests… for status information must be answered within 5 sec…” Updated per evaluator: Define metric 'ui_status_update_latency' (10-minute average and 99th percentile); acceptance: raise alert if more than 1% of status display updates exceed 4s (local) or status requests exceed 5s in a 1h window. Owner: Team-SRE; Next action: Add metric definition and alerting to NFR-004.  
**Quality Attributes**: Performance, Usability  
**Measurable Criteria (if provided):** ui_status_update_latency metric (10-minute avg and 99th percentile); alert if >1% of local updates >4s or status requests >5s in 1h window.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-051  
- **Conflicts with:** NFR-014  
---

[NFR-005]: LAN throughput for data transfer  
**Description:** “The LAN must support a transfer rate of 20-40 Mbits/second.”  
**Quality Attributes**: Performance, Capacity  
**Measurable Criteria (if provided):** 20–40 Mbit/s.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-034, FR-036  
- **Conflicts with:** —  
---

[NFR-006]: Compression constraints for transmission  
**Description:** “may be compressed using a loss-less compression technique for transmission…” and “high-quality transmission… can only be assisted with loss-less compression.” Updated per evaluator: Acceptance: SRE script verifies all config entries governing transmission compression = 'lossless', and CI pipeline asserts data output matches input (hash check) after compress/decompress round-trip. Owner: Team-SRE; Next action: Add monitoring or unit tests to enforce lossless compression.  
**Quality Attributes**: Data integrity, Performance  
**Measurable Criteria (if provided):** Config enforcement check: compression='lossless' for governed transmission paths; CI hash-equality check after compress/decompress round-trip.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-034, FR-038  
- **Conflicts with:** —  
---

[NFR-007]: On-site data retention capacity  
**Description:** “capable of retaining 7 days of data… last 3 days… available interactively from hard disk…”  
**Quality Attributes**: Capacity, Availability  
**Measurable Criteria (if provided):** Retain 7 days; last 3 days interactive on disk.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-036  
- **Conflicts with:** —  
---

[NFR-008]: Security via privileges/levels and protection from interference/intrusion  
**Description:** “Access… restricted…” “Privileges… determined… during logging in…” “Security of operation shall be considered…” “Security must be provided… prevent accidental mix-up… prevent intrusion from the wide area network…” Updated per evaluator: Test plan covers: password policy enforcement (reject weak, accept strong), failed login attempts log, connection TLS established, audit log entry on every access and admin action. Owner: Team-Sec; Next action: Map each security feature to one or more acceptance criteria/tests/metrics.  
**Quality Attributes**: Security, Safety, Integrity  
**Measurable Criteria (if provided):** Password policy enforcement test (reject weak/accept strong); failed login attempts logged; TLS established for connections; audit log entry on every access and admin action.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-039  
- **Conflicts with:** NFR-001 (latency), NFR-010 (ease of use vs restrictions)  
---

[NFR-009]: Multi-node capacity without appreciable performance degradation  
**Description:** “allow simultaneous operation of up to six active control nodes and up to two more monitoring nodes… without appreciable degradation… capable… 10 active nodes…”  
**Quality Attributes**: Scalability, Performance  
**Measurable Criteria (if provided):** 6 active + 2 monitoring without appreciable degradation; capability up to 10 active nodes.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-057  
- **Conflicts with:** —  
---

[NFR-010]: Usability and human engineering of UIs; uniformity across subsystems  
**Description:** “interface… simple, safe, and convenient… simple to learn and secure…” and “user interfaces… should be uniform across all subsystems… different access levels should present different ‘look-and-feels’.” Updated per evaluator: Add: Acceptance: SUS survey of ≥10 users mixing astronomers/operators, SUS instrument as specified in annex A, with results documented in /QA/usability/. Owner: Team-UX; Next action: Attach usability test plan and sample survey instrument to repo.  
**Quality Attributes**: Usability, Human factors  
**Measurable Criteria (if provided):** SUS survey with n ≥ 10 users mixing astronomers/operators; SUS instrument per annex A; results archived at /QA/usability/.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003  
- **Conflicts with:** NFR-008 (security constraints may reduce simplicity)  
---

[NFR-011]: Reliability, recoverability, and reconfiguration objectives  
**Description:** “retry procedures… achieve recovery on-line…” “reconfigure… continue observing… given failure of a single non-critical subsystem.” “goal for recover and/or reconfiguration is 5 minutes… to observing again.” Updated per evaluator: Acceptance: Automated incident record logs {err_time, resumed_time}, and SRE report checks distribution; raise alert if >5min on >0.5% of cases/mo. Metric: recovery_time_minutes (from error/event log to resumed observation). Owner: Team-SRE; Next action: Add incident+recovery time monitoring to SRE dashboard.  
**Quality Attributes**: Reliability, Availability, Resilience  
**Measurable Criteria (if provided):** recovery_time_minutes metric; alert if recovery_time_minutes > 5 minutes in >0.5% of monthly incidents; incident record includes {err_time, resumed_time}.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-042, FR-064  
- **Conflicts with:** —  
---

[NFR-012]: Safety and independent interlocks  
**Description:** “Safety protection… must be independent of the software… mechanical hard stops… interlocks… watch dogs.” “software… bring… quickly to a safe state…”  
**Quality Attributes**: Safety  
**Measurable Criteria (if provided):** Not specified (categorical interlock rules provided).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-054  
- **Conflicts with:** FR-064 (retries), FR-013 (direct interactive operation)  
---

[NFR-013]: Logging for traceability of observations  
**Description:** “sufficient information… to recreate the sequence of events… properly timestamped and indexed.” Updated per evaluator: Acceptance: Log API entry must contain: {timestamp, user_id, subsystem, action, result_code}; SRE test: retrieve random log entries ≥1 year old to verify fields and write immutability. Owner: Team-SRE; Next action: Publish observation/audit log API/schema and immutability verification procedure.  
**Quality Attributes**: Auditability, Maintainability, Operability  
**Measurable Criteria (if provided):** Log entry schema includes {timestamp, user_id, subsystem, action, result_code}; retention/immutability verified by retrieving random entries ≥1 year old.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-062  
- **Conflicts with:** NFR-003, NFR-001 (overhead)  
---

[NFR-014]: Fault/event logging with traceability to source  
**Description:** “notification… electronically logged… error logging should provide enough information to trace… source… in equipment and in event sequence.” Updated per evaluator: Every fault/event log must include event time (UTC ISO8601), originating subsystem/component, event severity, error code/reference, user/action (if applicable), and CorrelationID. Owner: Team-SRE; Next action: Add event schema/table and mandatory log field list.  
**Quality Attributes**: Diagnosability, Maintainability  
**Measurable Criteria (if provided):** Mandatory fields: event time (UTC ISO8601), subsystem/component, severity, error code/reference, user/action (if applicable), CorrelationID.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, FR-062  
- **Conflicts with:** NFR-003 (if verbose at runtime)  
---

[NFR-015]: Engineering logging rate capability  
**Description:** “log engineering data at up to 200 Hz rates for short periods… Long-term logging… 1 Hz or less…” Updated per evaluator: System shall expose an 'eng_log_write_rate' metric reporting average to 95th percentile over a 60s window; alert if dropped entries exceed 0.1% in any 5-minute rolling window. Owner: Team-SRE; Next action: Add log write rate metric, measurement point, and alert policy.  
**Quality Attributes**: Performance, Observability  
**Measurable Criteria (if provided):** Metric 'eng_log_write_rate' (avg..p95 over 60s); dropped entries ≤ 0.1% per 5-minute rolling window (alert if exceeded).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-063  
- **Conflicts with:** NFR-003  
---

[NFR-016]: Time synchronization support  
**Description:** “synchronization with the Time Reference System… is also necessary.”  
**Quality Attributes**: Correctness, Consistency  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-052  
- **Conflicts with:** —  
---

[NFR-017]: Online database performance and concurrency  
**Description:** “Access times to the database are to be in the range of 2-3 msec per access. Asynchronous writes are to be supported… Time-access critical information is available in memory. The database must support both remote access and distributed data.” Updated per evaluator: Database shall log 'db_access_latency_ms' per operation; if over 3ms in >1% of cases per hour, a performance alert is raised. Owner: Team-SRE; Next action: Document database latency/uptime monitoring and actionable alert rule.  
**Quality Attributes**: Performance, Scalability  
**Measurable Criteria (if provided):** 2–3 ms per access; metric 'db_access_latency_ms' per operation; alert threshold: >3 ms in >1% calls per hour.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-065  
- **Conflicts with:** —  
---

[NFR-018]: Use standards and commercial/public-domain software where feasible; integrate existing software  
**Description:** “Commercial packages… and standards are to be used whenever feasible. Existing external software will be integrated…”  
**Quality Attributes**: Maintainability, Cost effectiveness, Interoperability  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-049  
- **Conflicts with:** NFR-021 (stable interfaces vs evolving packages)  
---

[NFR-019]: Version labeling and retrievability; online version control availability  
**Description:** “All Gemini software must be version labeled… retrievable… via control commands.” and “On-line version control must be implemented… available to recover/restore versions at all times.”  
**Quality Attributes**: Maintainability, Traceability  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-058  
- **Conflicts with:** —  
---

[NFR-020]: Portability and hardware independence for non-hardware-control software; portable UI toolkit  
**Description:** “All software which does not directly control specific hardware must be written as machine independent, portable code.” and “user interface tools… based on standards… portable across different… platforms (Portable User Interface Toolkit).” Updated per evaluator: Acceptance: See /build/platform-matrix.md; verify green build across all rows nightly. Owner: Team-DevOps; Next action: Publish platform list and add multi-target build/test jobs to CI.  
**Quality Attributes**: Portability, Maintainability  
**Measurable Criteria (if provided):** Nightly CI build must be green across all rows in /build/platform-matrix.md.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-059  
- **Conflicts with:** NFR-001 (performance vs portability tradeoffs)  
---

[NFR-021]: Stable, long-lived visitor instrument interface  
**Description:** “It is important that the visitor instrument interface be stable and long-lived…” Updated per evaluator: Deprecation notices published on project website and emailed to integrators at least 12 months in advance. Rollback instructions included in migration docs. Owner: Team-API; Next action: Draft/process documentation for interface deprecation and notification.  
**Quality Attributes**: Compatibility, Maintainability  
**Measurable Criteria (if provided):** Deprecation notices published on project website and emailed ≥ 12 months before change; rollback instructions included in migration docs.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-060  
- **Conflicts with:** NFR-018 (evolving internal standards)  
---