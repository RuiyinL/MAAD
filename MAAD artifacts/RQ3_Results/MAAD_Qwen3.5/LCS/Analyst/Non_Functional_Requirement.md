# Non-Functional Requirements Results:

[NFR-001]: System Availability
**Description:** The RLCS Application must be available 24 hours per day, 7 days per week, 365 days per year. If there is a failure, recovery time must be no greater than 10 minutes. SLI: (Total minutes - Unplanned outage minutes >5min) / Total minutes per trailing 12 months ≥ 99.95%; Alert when downtime event >5min occurs. Next action: Mandate SLI/alert/monitor plan, define owner for ops instrumentation.
**Quality Attributes**: Availability, Reliability
**Measurable Criteria (if provided):** 24/7/365 availability; Recovery time ≤ 10 minutes; Uptime ≥99.95% per 12-month trailing period; all downtime events >5 minutes count toward this SLO.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Degraded Mode/Failover Architecture)
- **Conflicts with:** None
---

[NFR-002]: Performance and Response Time
**Description:** Under <80% CPU/network utilization, response time for normal device status queries shall be ≤2 seconds; during safety screening, total delay ≤4 seconds; exceptions for failover events explicitly logged and excluded from SLO calculations. Total command propagation + safety screening must not exceed 4s; each hop must budget ≤1s for local validation; if exceeded, abort sequence and log error event 'latency_safety_violation'. Field devices shall receive respond to commands from the RLCS within 12 seconds of the command confirmation being issued by the operator. Next action: Add an explicit architectural latency budget for safety validation chain and test plan with abort/alert logic.
**Quality Attributes**: Performance, Latency
**Measurable Criteria (if provided):** Status update ≤ 2 seconds (<80% load); Command response ≤ 12 seconds; Safety screening total delay ≤4 seconds; Failover exceptions logged/excluded.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Hierarchical Control Topology)
- **Conflicts with:** ASR-002 (Multi-Layer Safety Screening may introduce latency)
---

[NFR-003]: Security and Access Control
**Description:** User security levels shall be assigned at the command level, device, mode. All password and integrity hashing shall use SHA-256 or stronger (FIPS 180-4 compliant); remove MD5 references. Minimum 12 characters; Rotation every 90 days; Audit log retention 365 days. Successful/failed logins audit-logged and retained for 365 days. Next action: Unify cryptographic standards and communicate mandatory control to developers and ops.
**Quality Attributes**: Security, Confidentiality
**Measurable Criteria (if provided):** Password encryption required (SHA-256+); Minimum 12 characters; Rotation every 90 days; Audit log retention 365 days.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (User Authentication)
- **Conflicts with:** None
---

[NFR-004]: Data Integrity and Verification
**Description:** The system shall will employ a one-way hash function as an aid to maintaining the integrity of the data and software in the field. Integrity check status (cv_integrity_status) shall be measured daily on each field controller; failures auto-alerted to ops and logged persistently in audit log. Next action: Define and document required metrics and alerting for all integrity checks.
**Quality Attributes**: Integrity, Security
**Measurable Criteria (if provided):** Integrity check frequency ≥ once per day; Metric cv_integrity_check; Alert on mismatch.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Non-Volatile Memory Integrity Check)
- **Conflicts with:** None
---

[NFR-005]: Maintainability and Technology Stack
**Description:** A commercial off-the-shelf database management system shall be used for this function. A commercial off-the-shelf reporting tool shall be used for this function. Wherever possible open systems standards for hardware, software, software development tools, and communications shall be used. Design/Technology Review checklist must confirm open standards for hardware/software unless exception signed by DoT arch/IT. Next action: Add maintainability/portability review item to design/arch signoff process.
**Quality Attributes**: Maintainability, Portability
**Measurable Criteria (if provided):** COTS DBMS required; COTS Reporting tool required; Open standards preferred.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Database Technology Stack)
- **Conflicts with:** None
---

[NFR-006]: Reliability and Stability
**Description:** The RLCS must demonstrate the ability to function continuously without needing to be reset or rebooted due to an RLCS error for at least 30 consecutive days. Metric: rlcs_process_uptime (seconds) polled every 60s; Alert SRE-002 if process uptime <30d without planned restart. Next action: Define monitoring probe, expected metric, and acceptance/alert on process restarts.
**Quality Attributes**: Reliability, Stability
**Measurable Criteria (if provided):** MTBF ≥ 30 days without reboot; Metric rlcs_process_uptime polled every 60s.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Degraded Mode/Failover Architecture)
- **Conflicts with:** None
---

[NFR-007]: Usability and Alarm Visibility
**Description:** When a device status has been overridden, on the screen it shall appear with different color from the normal and alarm status colors. The visual alarm shall include a change of color for the affected device. The alarm icon shall change to the normal status icon automatically when the alarm condition is removed.
**Quality Attributes**: Usability, Operability
**Measurable Criteria (if provided):** Distinct color coding for override/alarm/normal states.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002 (GUI Status Display)
- **Conflicts with:** None
---