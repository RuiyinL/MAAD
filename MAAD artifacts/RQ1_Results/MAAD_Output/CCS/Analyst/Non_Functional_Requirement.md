# Non-Functional Requirements Results

[NFR-001]: Master/Slave network topology constraint  
**Description:** “The Correlator Monitor and Control System will be designed and implemented as a Master/Slave network with one computer system coordinating the activities of a number of intelligent hardware control processors.”  
**Quality Attributes**: Architecture Constraint, Modifiability, Performance  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** None identified  
- **Conflicts with:** None identified  
---

[NFR-002]: Real-time load isolation between slave and master layers  
**Description:** “This topology will place the real-time computing requirements in the slave layer and the quasi real-time, network-chaotic loads into the master layer.”  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001  
- **Conflicts with:** None identified  
---

[NFR-003]: Redundancy and high modularity in critical areas  
**Description:** “‘Critical area’ = Master node, Power Control, each CMIB rack; each must show N+1 path in architecture diagram and included in failover test.” (Derived from NFR-003; Next action: Enumerate critical areas and tag with required redundancy; reference in design/spec.)  
**Quality Attributes**: Availability, Reliability, Modifiability  
**Measurable Criteria (if provided):** N+1 path required for listed critical areas; included in failover test  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-020  
---

[NFR-004]: Full observability with limits only by hardware/bandwidth/security  
**Description:** “Annex X, listing all non-observable fields and their latency, is included as an appendix and linked here; coverage is validated by SRE monitoring report every release.” (Derived from NFR-004; Next action: Draft Annex X and add its presence as an explicit deliverable in the NFR.)  
**Quality Attributes**: Operability/Observability, Security  
**Measurable Criteria (if provided):** Coverage validated by SRE monitoring report every release  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014  
- **Conflicts with:** NFR-014  
---

[NFR-005]: Timely and robust delivery to backend over secondary network  
**Description:** “Acceptance: Packet captures at both sender and backend show >99.99% of test packets meet latency/jitter/loss requirements.” (Derived from NFR-005; Next action: Add pre-defined network test methodology to requirement.)  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** >99.99% of test packets meet latency/jitter/loss requirements  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-003  
- **Conflicts with:** NFR-020  
---

[NFR-006]: Deterministic response to hardware inputs to avoid data loss/corruption/overflows  
**Description:** “Acceptance: Test harness submits burst of 10,000 events at 40 Mbps/channel, 99.99% processed in ≤5ms latency; logs must include latency histogram.” (Derived from NFR-006; Next action: Add test methods/criteria for performance measurements to requirement.)  
**Quality Attributes**: Real-time Performance, Reliability  
**Measurable Criteria (if provided):** Burst of 10,000 events at 40 Mbps/channel; 99.99% processed in ≤5 ms latency; latency histogram required  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-002  
- **Conflicts with:** NFR-020  
---

[NFR-007]: Meet all data processing deadlines and anticipated future requirements  
**Description:** “Acceptance: System must maintain at least 15% performance headroom above highest 99th percentile workload observed in past year.” (Derived from NFR-007; Next action: Set concrete, regularly revisited targets for capacity.)  
**Quality Attributes**: Performance, Scalability  
**Measurable Criteria (if provided):** ≥15% performance headroom above highest 99th percentile workload observed in past year  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006  
- **Conflicts with:** NFR-020  
---

[NFR-008]: Minimal interruption and autonomous return to service after watchdog reboot  
**Description:** “Restoration accepted if: all health checks pass, all control/status channels reopened, no data loss after recovery within 20 seconds.” (Derived from NFR-008; Next action: Update requirement to specify completeness criteria and add post-reboot test plan.)  
**Quality Attributes**: Availability, Reliability, Recoverability  
**Measurable Criteria (if provided):** All health checks pass; all control/status channels reopened; no data loss; within 20 seconds  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-020  
---

[NFR-009]: High availability / continued service under failures (general)  
**Description:** “System shall deliver ≥99.99% availability over any 365-day period; MTTR ≤30 minutes.” (Derived from NFR-009; Next action: Insert quantifiable uptime/reliability thresholds.)  
**Quality Attributes**: Availability, Reliability  
**Measurable Criteria (if provided):** Availability ≥99.99% over any 365-day period; MTTR ≤30 minutes  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003  
- **Conflicts with:** NFR-020  
---

[NFR-010]: Message conciseness and controllable content  
**Description:** “Error and status messages will be provided in a concise time/location referenced format… in a content controllable manner.”  
**Quality Attributes**: Operability, Maintainability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** None identified  
- **Conflicts with:** NFR-020  
---

[NFR-011]: Message categorization and filterability (content/detail/rate)  
**Description:** “All system error and debug messages shall be categorized… such that message traffic can be filtered as to content, detail, and message rate.”  
**Quality Attributes**: Operability, Maintainability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-010  
- **Conflicts with:** NFR-020  
---

[NFR-012]: Dual timestamping (UTC and wall clock) with type-specific semantics  
**Description:** “All messages… shall have both UTC and wall clock time stamp information… Error messages… discovery time, control messages… generation time.”  
**Quality Attributes**: Traceability, Operability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-010  
- **Conflicts with:** NFR-020  
---

[NFR-013]: Standalone boot/run capability without external communications (Master)  
**Description:** “The Master… shall have all required disk and file system facilities installed locally such that the EVLA Correlator Monitor and Control System can boot and run in a stand-alone configuration… CMIBs… boot, configure, and run without any communication outside of the correlator Monitor and Control System network.”  
**Quality Attributes**: Resilience, Availability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004  
- **Conflicts with:** NFR-020  
---

[NFR-014]: Robust security mechanism preventing unauthorized access  
**Description:** “Privileged session actions require two-factor authentication; audit log entries must include action type, timestamp, actor, and outcome; all sensitive data at rest is encrypted with AES-256 or stronger. Provide a NIST 800-53 mapping spreadsheet.” (Derived from NFR-014; Next action: Decompose each security control and define measurable acceptance criteria for each; add to requirements list.)  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Two-factor authentication required for privileged session actions; audit log fields include action type/timestamp/actor/outcome; AES-256+ encryption at rest for sensitive data; NIST 800-53 mapping spreadsheet provided  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-015  
- **Conflicts with:** NFR-004, FR-005  
---

[NFR-015]: Secure login and authentication/authorization; unique identification  
**Description:** “Acceptance: All logins use mutual TLS or SSH, passwords stored as PBKDF2/bcrypt hashes, sessions auto-expire after 8 hours.” (Derived from NFR-015; Next action: Rewrite to specify minimum authentication transport, credential storage, and session policy.)  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Mutual TLS or SSH for logins; PBKDF2/bcrypt password storage; session expiry 8 hours  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014  
- **Conflicts with:** FR-005  
---

[NFR-016]: Maintainability via modularization for fault detection/repair  
**Description:** “Acceptance: Module architecture doc must list all direct imports with graph diagram; codebase must have 95%+ line and public interface coverage by unit tests tagged 'boundary'.” (Derived from NFR-016; Next action: Draft and insert measurable test protocol and tooling owner for interface coverage.)  
**Quality Attributes**: Maintainability, Modifiability  
**Measurable Criteria (if provided):** Module architecture doc lists all direct imports with graph diagram; ≥95% line and public interface coverage by unit tests tagged “boundary”  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003  
- **Conflicts with:** NFR-020  
---

[NFR-017]: Hardware accessibility for maintenance/repair/replacement  
**Description:** “All system processing and interconnect hardware shall be readily accessible for maintenance, repair, replacement and reconfiguration…”  
**Quality Attributes**: Maintainability, Serviceability  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** None identified  
---

[NFR-018]: Source code availability and debuggability/testability of modules/processes  
**Description:** “Acceptance: Minimum 90% line and branch coverage on public API modules; all interface inputs simulated with edge and error cases; coverage reported for each release.” (Derived from NFR-018; Next action: Amend requirement to specify code/test coverage percent and report granularity.)  
**Quality Attributes**: Maintainability, Testability  
**Measurable Criteria (if provided):** ≥90% line and branch coverage on public API modules; edge/error case simulation for all interface inputs; coverage reported each release  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** None identified  
---

[NFR-019]: Expandability/reconfigurability/replaceability of I/O, comms, processing hardware  
**Description:** “Acceptance: Slot for expansion card or external link in all core hardware.” (Derived from NFR-019; Next action: Add measurable expansion requirements or explicit proxy.)  
**Quality Attributes**: Scalability, Modifiability  
**Measurable Criteria (if provided):** Expansion slot or external link present in all core hardware  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** NFR-020  
---

[NFR-020]: Technology constraints for networking and physical media (Ethernet, fiber, etc.)  
**Description:** “All critical physical connections must support field upgrade to ≥1 Gbps Ethernet or equivalent speed.” (Derived from NFR-020; Next action: Clarify requirement as minimum or add expansion clause.)  
**Quality Attributes**: Constraint, Interoperability, Performance  
**Measurable Criteria (if provided):** Field upgrade support to ≥1 Gbps Ethernet (or equivalent) for all critical physical connections  
**Dependencies** / **Conflicts**:  
- **Depends on:** None identified  
- **Conflicts with:** NFR-019 (future expandability may be constrained by fixed interfaces)  
---

[NFR-021]: Network segmentation via separate physical interfaces  
**Description:** “Acceptance: Network firewalls block unapproved traffic between physical network segments; test plan required.” (Derived from NFR-021; Next action: Add network traffic isolation acceptance test to requirement.)  
**Quality Attributes**: Security, Performance, Reliability  
**Measurable Criteria (if provided):** Firewalls block unapproved inter-segment traffic; test plan required  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-020  
- **Conflicts with:** NFR-019  
---

[NFR-022]: Use routers/switches to protect from unauthorized access and irrelevant traffic  
**Description:** “Network routers/switches shall be employed… to protect the Master… from unauthorized access and irrelevant network traffic.”  
**Quality Attributes**: Security, Performance  
**Measurable Criteria (if provided):** Not specified  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-014, NFR-020  
- **Conflicts with:** None identified  
---

[NFR-023]: UPS-backed power and coordinated safe shutdown on prolonged outage  
**Description:** “Test: All critical nodes at full CPU+I/O utilization, UPS supports ≥15 min runtime, shutdown completed before battery reaches 10%.” (Derived from NFR-023; Next action: Add a target test scenario (hardware, load, duration, shutdown protocol) to requirement.)  
**Quality Attributes**: Reliability, Safety/Integrity  
**Measurable Criteria (if provided):** ≥15 minutes runtime; shutdown completed before battery reaches 10% (under full CPU+I/O utilization on all critical nodes)  
**Dependencies** / **Conflicts**:  
- **Depends on:** None identified  
- **Conflicts with:** NFR-020  
---

[NFR-024]: Self-monitoring capability across specified abnormal conditions  
**Description:** “For processor hardware failure, system must detect and take remediation action within 30 sec of event; miss threshold triggers a critical alert.” (Derived from NFR-024; Next action: Specify detection and remediation windows for each failure type in requirement.)  
**Quality Attributes**: Reliability, Availability, Operability  
**Measurable Criteria (if provided):** Detect and remediate processor hardware failure within 30 seconds; miss triggers critical alert  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-020  
---

[NFR-025]: Software operates without total restart between maintenance windows  
**Description:** “Acceptance: System-under-test runs for 30 days; any process restart logged and reviewed; total OS reboot not permitted during period.” (Derived from NFR-025; Next action: Clarify types of restart counted and establish monitoring/logging to support validation.)  
**Quality Attributes**: Reliability, Availability  
**Measurable Criteria (if provided):** 30-day run; process restarts logged/reviewed; no total OS reboot during period  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-020  
---

[NFR-026]: Hardware operates indefinitely without complete loss of service (except total power failure)  
**Description:** “Quarterly hardware failure report logged/archived for all components, including exception cases.” (Derived from NFR-026; Next action: Add reporting mechanism and periodic analysis to requirement.)  
**Quality Attributes**: Availability, Reliability  
**Measurable Criteria (if provided):** Quarterly hardware failure report logged/archived for all components (including exceptions)  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-023  
- **Conflicts with:** NFR-020  
---

[NFR-027]: Continue operations on unaffected resources during partial shutdowns  
**Description:** “List: Heartbeats, state-of-health, reboot control = core functions; at least 1 node running at all times.” (Derived from NFR-027; Next action: Add mapping table and reference to requirement.)  
**Quality Attributes**: Availability, Maintainability  
**Measurable Criteria (if provided):** Core functions defined as heartbeats/state-of-health/reboot control; ≥1 node running at all times  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003, NFR-016  
- **Conflicts with:** NFR-020  
---

[NFR-028]: Replaceability and maximal practical use of hot-swappable components  
**Description:** “Acceptance: ≥90% critical components on BOM are hot-swappable and are demonstrated in annual test; design doc lists exceptions with rationale.” (Derived from NFR-028; Next action: Set demonstrable target and point to verification owner.)  
**Quality Attributes**: Maintainability, Availability  
**Measurable Criteria (if provided):** ≥90% critical BOM components hot-swappable; annual demonstration test; exceptions documented with rationale  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-016  
- **Conflicts with:** NFR-020  
---

[NFR-029]: Documentation and familiar languages; readable coding style  
**Description:** “Acceptance: 100% modules pass PEP8 (or Google) check, doc coverage ≥90% as measured by Sphinx/doxygen/linter.” (Derived from NFR-029; Next action: Reference code style/coverage standard.)  
**Quality Attributes**: Maintainability  
**Measurable Criteria (if provided):** 100% modules pass PEP8 (or Google) check; documentation coverage ≥90% (Sphinx/doxygen/linter)  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-018  
- **Conflicts with:** None identified  
---