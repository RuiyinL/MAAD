# Non-Functional Requirements Results

[NFR-001]: Command validation response time  
**Description:** “Every command must be accepted/rejected within 2 sec and before the corresponding action occurs.” Accept/reject response must be delivered to initiating user station within 2 s (99.9th percentile over 1-hour window); no command shall be executed unless positive acknowledgment is sent. (Next action: Add measurement definitions and clarify response time context.)  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** Accept/reject delivered to initiating user station within 2 seconds (99.9th percentile over 1-hour window); command execution must not begin unless positive acknowledgment is sent.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-044  
- **Conflicts with:** FR-051 (continuous monitoring load), FR-040 (logging overhead)  
---

[NFR-002]: Communications timeouts and ACK/NAK timing  
**Description:** “Timeouts must be supported at approximately 500 msec… Handshaking… within 100-200 msec…”  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** 500 ms timeout; 100–200 ms handshake.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003  
- **Conflicts with:** NFR-021 (WAN bandwidth/latency variability)  
---

[NFR-003]: Peak control throughput  
**Description:** “Peak control information within the system is expected to be 100 TPS.”  
**Quality Attributes**: Performance, Scalability  
**Measurable Criteria (if provided):** 100 transactions per second peak.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** FR-040 (high-rate logging), FR-051 (monitoring)  
---

[NFR-004]: Detector readout time constraints  
**Description:** “For focusing… maximum acceptable detector readout time is about 0.1 sec… For mosaicked… full readout… about 2 or 3 minutes.”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 0.1 s (partial) for focusing; 2–3 minutes full readout for large mosaics.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-001 (if readout blocks command validation)  
---

[NFR-005]: On-line database access latency and concurrency  
**Description:** “Access times to the database are to be in the range of 2-3 msec per access. Asynchronous writes are to be supported, allowing for concurrent operation.”  
**Quality Attributes**: Performance, Scalability  
**Measurable Criteria (if provided):** 2–3 ms per access; async writes supported.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-046  
- **Conflicts with:** FR-040 (logging volume)  
---

[NFR-006]: Privilege-based access control determined at login  
**Description:** “These privileges should be determined in a simple manner during logging into the system.” / “Access… restricted according to… level… modes… privileges…” All logins require minimum 12-character password; all privilege changes audited; session auto-logout after 30 min of inactivity. (Next action: Incorporate security controls and auditability.)  
**Quality Attributes**: Security, Safety, Usability  
**Measurable Criteria (if provided):** Minimum 12-character password; privilege changes audited; session auto-logout after 30 minutes inactivity.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019  
- **Conflicts with:** NFR-020 (transparency)  
---

[NFR-007]: Monitoring/testing/administrative must not affect ongoing observation performance  
**Description:** “Under no circumstances should monitoring affect the performance of an ongoing observation… Under no circumstances should testing affect… Under no circumstances should administrative access affect…” While observing, background tasks (monitoring, testing, admin) may consume no more than 5% of system CPU or add latency no more than 200 ms to foreground control/telemetry operations. Metric: background_cpu_pct_observing, alert if >5% for 30s; metric: foreground_latency_ms, alert if >200ms over 3s moving window. (Next action: Define CI/SRE test for CPU/latency headroom in observing mode.)  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** During observing, background tasks consume ≤5% CPU or add ≤200 ms latency to foreground control/telemetry operations; alert if background_cpu_pct_observing >5% for 30s; alert if foreground_latency_ms >200ms over 3s moving window.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-026  
- **Conflicts with:** NFR-003 (shared throughput), NFR-001  
---

[NFR-008]: Restart should be needed only on hardware failure  
**Description:** “The goal is to have restart conditions occur only on hardware failure.” Mean time between required system restart for non-hardware-caused reasons must exceed 180 days (excluding planned maintenance). (Next action: Define test metrics for system root-cause analysis.)  
**Quality Attributes**: Availability, Reliability  
**Measurable Criteria (if provided):** MTBR (non-hardware-caused) > 180 days, excluding planned maintenance.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042, FR-041  
- **Conflicts with:** None identified  
---

[NFR-009]: Robustness via retries, range/validity checking, and non-lost commands  
**Description:** “Retry procedures must be embodied… to achieve recovery on-line… range checking and validity checking… protocol… predictable… commands cannot get lost and replies have to come back reliably.” No more than 1 unacknowledged command failure per 10^7 issued; failure triggers auto-retry; log retry attempts. (Next action: Define reliability/command-loss metric and alert threshold.)  
**Quality Attributes**: Reliability, Safety  
**Measurable Criteria (if provided):** ≤1 unacknowledged command failure per 10^7 commands issued; auto-retry on failure; retry attempts logged.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-044, FR-050  
- **Conflicts with:** NFR-001 (extra checking/retries add latency)  
---

[NFR-010]: Data retention capacity on system disks  
**Description:** “System data capacity… retaining 7 days of data… last 3 days… available interactively from hard disk…” System will raise an alert if less than 7 days of observation data remain on disk, or if 3 most recent days are not accessible interactively. (Next action: Add SRE alert/monitor criteria.)  
**Quality Attributes**: Capacity, Availability  
**Measurable Criteria (if provided):** 7 days retained; last 3 days interactive; alert if <7 days remain or if last 3 days not interactively accessible.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-036  
- **Conflicts with:** NFR-001 (if storage management impacts responsiveness)  
---

[NFR-011]: LAN transfer rate requirement  
**Description:** “The LAN must support a transfer rate of 20-40 Mbits/second.”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 20–40 Mbps.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-021 (WAN limitations)  
---

[NFR-012]: Safety interlocks independent of software; safe-state capability  
**Description:** “Safety protection… must be independent of the software… mechanical hard stops… interlocks… watch dogs… software shall be able to bring… quickly to a safe state…” System software must initiate safe-state transition within 2 seconds after hazard notification; confirm safe state within 10 seconds. (Next action: Add measurable timing to all safety transition/response requirements.)  
**Quality Attributes**: Safety, Reliability  
**Measurable Criteria (if provided):** Initiate safe-state transition within 2 seconds after hazard notification; confirm safe state within 10 seconds.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-049  
- **Conflicts with:** FR-054 (dynamic reconfiguration may be constrained)  
---

[NFR-013]: Hazard interlock classification (passive/active/software)  
**Description:** “All hazards capable of causing death… passively interlocked… injury/severe damage… actively interlocked… All other hazards may be interlocked via software.” Table: hazard_type, mitigation, required interlock/safety response; e.g., 'death', 'mechanical hard-stop', function_name. (Next action: Draft hazard mitigation map and trace to code/tests.)  
**Quality Attributes**: Safety, Compliance  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-012  
- **Conflicts with:** None identified  
---

[NFR-014]: Documentation, versioning, change logs, and formal release discipline  
**Description:** “All Gemini software is to be fully documented… External documentation must include Unix-style man pages… developers should maintain accurate change logs… formal release system… checkable on-line… version labeled…” Release check: All new features have accompanying man page; changelog updated and reviewed at release; automated doc build passes. (Next action: Implement doc/test checklist for releases.)  
**Quality Attributes**: Maintainability, Supportability  
**Measurable Criteria (if provided):** Release check: all new features have accompanying man page; changelog updated and reviewed at release; automated doc build passes.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-047  
- **Conflicts with:** None identified  
---

[NFR-015]: Use COTS/standards where feasible; integrate existing external software  
**Description:** “Commercial packages… and standards are to be used whenever feasible. Existing external software will be integrated…” COTS/standards shall be used when integration cost is less than 20% higher than equivalent in-house solution; evaluate at design review with 3 costed alternatives. (Next action: Add procurement/governance controls for evaluating COTS/standards adoption.)  
**Quality Attributes**: Maintainability, Cost, Interoperability  
**Measurable Criteria (if provided):** Use COTS/standards when integration cost is <20% higher than equivalent in-house solution; evaluate at design review with 3 costed alternatives.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007  
- **Conflicts with:** NFR-016 (modularity may be harder with COTS)  
---

[NFR-016]: Strict modularity and interface-defined environments  
**Description:** “Software must be strictly modular… each module’s environment is strictly defined by its interface… No module can rely upon information outside of this interface.”  
**Quality Attributes**: Modifiability, Maintainability  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003  
- **Conflicts with:** NFR-001 (extra indirection may add latency)  
---

[NFR-017]: Failure containment (no cascading failures)  
**Description:** “Failure conditions should not cascade… failure of one subsystem should not affect other… including communication links.” During subsystem fault injection (planned outage or communications fail), dependent subsystem error rates must remain at baseline and no more than 1 loss of service in others per 1,000 faults injected. (Next action: Add/define fault-injection test plan and pass/fail criteria for containment.)  
**Quality Attributes**: Reliability, Resilience  
**Measurable Criteria (if provided):** During fault injection, dependent subsystem error rates remain at baseline; ≤1 loss of service in other subsystems per 1,000 faults injected.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-016  
- **Conflicts with:** None identified  
---

[NFR-018]: Essential tasks must use project-controlled resources (leased lines); internet only for non-essential  
**Description:** “Due to the uncertain future of the Internet, only non-essential tasks may employ it. All essential tasks… must take place on resources controlled by the project (such as leased lines).”  
**Quality Attributes**: Reliability, Security  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** FR-022 (remote operations), FR-037 (data transmission)  
---

[NFR-019]: Network architecture should be hierarchical (OSI-like); peer-to-peer only for proven performance need  
**Description:** “Clear hierarchical model… e.g. ISO/OSI… Peer-to-peer connectivity should only be used to overcome a demonstrated performance problem.” Peer-to-peer linkage requires documented case where OSI stack adds >500ms to control path latency under production load, reviewed by architect. (Next action: Set performance baseline for permitted architecture deviations.)  
**Quality Attributes**: Maintainability, Performance  
**Measurable Criteria (if provided):** Peer-to-peer allowed only with documented case OSI stack adds >500ms to control path latency under production load and reviewed by architect.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-002 (may require bypass for timing)  
---

[NFR-020]: Functional transparency for local vs remote use; minimize bandwidth impact  
**Description:** “System shall be totally transparent to local or remote use… design should minimize the impact of link bandwidth on transparency.”  
**Quality Attributes**: Usability, Performance  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022  
- **Conflicts with:** FR-023 (site restrictions), NFR-021 (WAN limits)  
---

[NFR-021]: Remote performance depends on WAN bandwidth; hardware assumed sufficient; use standard protocols  
**Description:** “Hardware… specified with sufficient bandwidth… take advantage of… ISDN, TCP/IP, Internet, etc… speed of the link will determine the perceived transparency…” Remote control command round-trip latency shall not exceed 10s in 99% of cases on the specified WAN link; minimum sustained throughput for remote data access shall be 5 Mbps. (Next action: Add explicit metrics for remote operation latency and bandwidth.)  
**Quality Attributes**: Performance, Interoperability  
**Measurable Criteria (if provided):** Remote control command round-trip latency ≤10s in 99% of cases on specified WAN link; minimum sustained throughput for remote data access ≥5 Mbps.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-020  
---

[NFR-022]: Control nodes scalability without appreciable degradation  
**Description:** “Allow simultaneous operation of up to six active control nodes and up to two more monitoring nodes… capable of coping with the load of 10 active nodes…” System must maintain ≥95% of single-node performance (response times, throughput) with 6 active + 2 monitoring nodes, and ≥80% with 10 active nodes. Response time at 6-node load must remain within 105% of single-node 99th percentile latency; throughput ≥95% of single-node; error rate ≤1/10,000 commands. (Next action: Refine and separate out required performance metrics for scalability.)  
**Quality Attributes**: Scalability, Performance  
**Measurable Criteria (if provided):** With 6 active + 2 monitoring nodes: response time within 105% of single-node 99th percentile latency; throughput ≥95% of single-node; error rate ≤1/10,000 commands. With 10 active nodes: ≥80% of single-node performance (response times, throughput).  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-001, NFR-003  
---

[NFR-023]: Status display update timing  
**Description:** “Status display update must be within 4 sec at the local stations… Requests… for status… answered within 5 sec…” Remote station update must complete within 8 seconds under normal bandwidth; locally, status update within 4 seconds. (Next action: Expand coverage to include remote operation or clarify scope.)  
**Quality Attributes**: Performance, Usability  
**Measurable Criteria (if provided):** Local status display update within 4 seconds; remote station update within 8 seconds under normal bandwidth; status request response within 5 seconds.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020, FR-021  
- **Conflicts with:** NFR-007 (non-intrusive monitoring)  
---

[NFR-024]: Engineering data logging rates and formats  
**Description:** “Possible to log engineering data at up to 200 Hz… Long-term logging… 1 Hz or less… common format (baselined as SYBASE).”  
**Quality Attributes**: Observability, Performance  
**Measurable Criteria (if provided):** 200 Hz short periods; ≤1 Hz long-term; format baselined as SYBASE.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-040  
- **Conflicts with:** NFR-003 (throughput), NFR-001 (latency)  
---

[NFR-025]: Recovery/reconfiguration time objective  
**Description:** “The goal for recover and/or reconfiguration is 5 minutes from onset of the error condition to observing again.” For non-safety-critical faults, the maximum time from confirmed error detection to start of next science exposure shall not exceed 5 minutes (95% of cases measured over a month). Table: error_code, detection_event, recovery_start, recovery_end; 95% of recoveries from event X to science exposure restart under 5 minutes. (Next action: Publish error scenario/recovery test suite and definition for timing window.)  
**Quality Attributes**: Availability, Resilience  
**Measurable Criteria (if provided):** For non-safety-critical faults, ≤5 minutes from confirmed error detection to start of next science exposure in 95% of cases measured over a month; define timing window via table: error_code, detection_event, recovery_start, recovery_end.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042, FR-054  
- **Conflicts with:** NFR-012 (safety may require longer)  
---

[NFR-026]: UI uniformity across subsystems; different look-and-feel per access level  
**Description:** “User interfaces for different access levels should be uniform across all subsystems, though different access levels should present different ‘look-and-feels’.” All user interfaces for a given access level must use the standard Gemini UI toolkit and pass the UI Conformance Checklist at each release. Append 'UI Conformance Checklist v1.0' (e.g., uniform color/font/widget usage, interactive sample UI tests) as req doc attachment. Append 'UI Conformance Checklist v1.0' to requirements; add release-gate test referencing this doc. (Next action: Create/publish checklist and retrofit into release process.)  
**Quality Attributes**: Usability, Maintainability  
**Measurable Criteria (if provided):** Use standard Gemini UI toolkit; pass UI Conformance Checklist at each release; UI Conformance Checklist v1.0 appended as requirements attachment; release-gate test references UI Conformance Checklist v1.0.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002  
- **Conflicts with:** NFR-015 (COTS UI constraints)  
---

[NFR-027]: UI toolkit portability and network transparency  
**Description:** “User interface tools shall be based on standards… portable across different computer hardware platforms… should also be network transparent so that it does not matter where it is being run.” UI toolkit shall run with no changes on Linux, Windows, Mac OS (at time of release). (Next action: Specify platform list and test scenario.)  
**Quality Attributes**: Portability, Usability  
**Measurable Criteria (if provided):** Runs with no changes on Linux, Windows, Mac OS (at time of release).  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005  
- **Conflicts with:** NFR-001 (thin clients vs latency)  
---

[NFR-028]: Real-time support required at IOC level; upper levels not real-time  
**Description:** “Strict real-time control is restricted to the IOC layer… upper levels… assumed to not require a real-time operating environment… Real-time support is required at the IOC level.” IOC control loop latency must not exceed 10ms end-to-end with jitter <1ms (95% of cycles). (Next action: Add quantifiable real-time performance target for IOC software.)  
**Quality Attributes**: Performance, Safety  
**Measurable Criteria (if provided):** IOC control loop latency ≤10ms end-to-end; jitter <1ms for 95% of cycles.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004  
- **Conflicts with:** None identified  
---

[NFR-029]: Security against command mix-up and WAN intrusion; firewall acceptable  
**Description:** “Security must be provided… prevent accidental mix-up… and to prevent intrusion from the wide area network… acceptable… network gateway acting as a firewall.” Firewall must block all non-whitelisted traffic; intrusion detection events trigger alert within 1 min; penetration tests run quarterly and results logged. (Next action: Mandate security audit, IDS, and test schedule.)  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Block all non-whitelisted traffic; IDS alert within 1 minute of intrusion detection event; quarterly penetration tests with results logged.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-023, NFR-006  
- **Conflicts with:** NFR-020 (transparency)  
---

[NFR-030]: Encrypted channels for remote command/data and remote DB access  
**Description:** All remote command and data exchanges must use TLS 1.2+; all database access by remote clients must require encryption. All TLS endpoints must enable only NIST- or EC- ciphersuites with a minimum of 2048-bit keys; reviewed annually. (Next action: Update NFR to reference acceptable cipher suites and audit schedule.)  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** TLS 1.2+ for all remote command/data exchanges; encryption required for all remote client database access; only NIST- or EC- ciphersuites enabled with minimum 2048-bit keys; reviewed annually.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-013, NFR-029  
- **Conflicts with:** None identified  
---