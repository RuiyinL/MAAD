# Non-Functional Requirements Results

[NFR-001]: UI environmental displays refresh frequency  
**Description:** “Displays of environmental conditions (temperature, humidity, contact sensors and power switches) shall be updated at least every two seconds. Record 'ui_refresh_interval_secs' p99, p99.9; trigger 'ui_stale_alert' if >1% of intervals >2.5s per 15min window.” (Next action: Specify metric/logging and alerting mechanism on UI layer.)  
**Quality Attributes**: Performance (Responsiveness)  
**Measurable Criteria (if provided):** Update interval ≤ 2 seconds; metrics ui_refresh_interval_secs (p99, p99.9); ui_stale_alert triggers if >1% intervals exceed 2.5s per 15min window  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-001, FR-002
- **Conflicts with:** NFR-010 (cost minimization may constrain compute/network)
---

[NFR-002]: Minimum sensor data acquisition rate  
**Description:** “Sensor (temperature, humidity, contact sensor, power state) shall have a minimum data acquisition rate of 10 Hz. Each individual sensor's raw data rate shall be ≥10Hz, measured as moving average over a 60-second window during functional test. Each sensor exports 'sensor_acquisition_rate_hz'; alert 'sensor_lag_alert' fires if moving average <10Hz for >60s.” (Next action: Add monitoring/logging for 10Hz per-sensor rate with auto-alert.)  
**Quality Attributes**: Performance (Throughput), Real-time behavior  
**Measurable Criteria (if provided):** ≥ 10 samples/second per individual sensor; moving average over 60-second window; sensor_acquisition_rate_hz metric; sensor_lag_alert if moving average <10Hz for >60s  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-004, FR-005
- **Conflicts with:** NFR-010
---

[NFR-003]: Wireless range requirement (indoor)  
**Description:**  
- “The Gateway device shall operate up to a 1000-foot range for indoor transmission.”  
- “An environmental sensor or controller device shall have to be within 1000 feet of the master control device, in order to be in communication with the system.”  
**Quality Attributes**: Operational constraint, Connectivity  
**Measurable Criteria (if provided):** 1000 feet indoor range  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005
- **Conflicts with:** NFR-010
---

[NFR-004]: Reliability target (failure rate / MTBF)  
**Description:** “The DigitalHome System must be highly reliable with no more than 1 failure per 10,000 hours of operation. ‘Failure’ is defined as loss of all core control for 2+ minutes, excluding planned maintenance; failures shall be tracked by an uptime monitor. Acceptance: System exposes 'uptime_monitor' log; QA and SRE review MTBF at each release. Alert if failure rate higher than 1 per 10,000h on simulated or production ops. Acceptance: QA runs 10 forced outage scenarios; ops dashboard exposes 'system_uptime_rolling_10k_hours'; QA and SRE review at each release.” (Next action: Expand NFR-004 and ASR-004 with operational test/reporting steps.)  
**Quality Attributes**: Reliability, Availability  
**Measurable Criteria (if provided):** Failure rate ≤ 1 / 10,000 operating hours; failure = loss of all core control for >2 minutes (excluding planned maintenance); tracked by uptime monitor; MTBF reviewed each release; alert if failure rate exceeds threshold; 10 forced outage scenarios; system_uptime_rolling_10k_hours metric exposed  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (overall ops), FR-006
- **Conflicts with:** NFR-010 (cost minimization), NFR-011 (schedule/team constraints)
---

[NFR-005]: Daily backup with technician-configured time  
**Description:** “The DigitalHome System will backup all system data… on a daily basis, with the backup time set by the DigitalHome Technician at system set up. Backups must include all tables: config, user_accounts, plans, usage_log; quarterly dry-run restore test documented.” (Next action: Amend NFR-005 and ASR-005 to cover dry-run restore/test schedule and schema.)  
**Quality Attributes**: Recoverability, Data protection  
**Measurable Criteria (if provided):** Daily backup; includes config, user_accounts, plans, usage_log; quarterly dry-run restore test documented  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-034, FR-003
- **Conflicts with:** Not identified
---

[NFR-006]: Recovery restores system data from most recent backup after failure  
**Description:** “If the DigitalHome System fails… the system recovery mechanism shall restore system data… from the most recent backup. RPO: ≤24 hours (since last daily backup); RTO: ≤60 minutes; annual full recovery test required.” (Next action: Add RPO/RTO goals and test requirement to NFR-006/ASR-005.)  
**Quality Attributes**: Recoverability, Resilience  
**Measurable Criteria (if provided):** Restore point = most recent backup; RPO ≤24 hours; RTO ≤60 minutes; annual full recovery test  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005, FR-003
- **Conflicts with:** Not identified
---

[NFR-007]: Realistic simulated test environment  
**Description:** “The DigitalHome system will be tested in a simulated environment. However, the simulated environment will be realistic and adhere to the physical properties and constraints of an actual home and to real sensors and controllers. Simulation acceptance criteria: simulated device latency within ±10% of real device logs; simulated sensor sampling jitter ±5%; at least 90% of device types covered. Acceptance: Simulated env must demonstrate latency within ±10% (of baseline); ≥90% device types emulated; output per-test-case CI log for coverage. For latency/jitter comparisons, baseline to be established via logs from certified devices (vendor/model list Appendix). Per test case, CI system outputs {test_id, device_type, sim_measured_latency, baseline_latency, sim_jitter, coverage_percent}.” (Next action: Amend NFR-007/ASR-008 to reference baseline test logs and detail CI test regime.)  
**Quality Attributes**: Testability, Validity of verification  
**Measurable Criteria (if provided):** Latency within ±10% of real device logs/baseline; sampling jitter ±5%; ≥90% device types covered/emulated; per-test-case CI outputs {test_id, device_type, sim_measured_latency, baseline_latency, sim_jitter, coverage_percent}  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-004/FR-005 device comms
- **Conflicts with:** NFR-011 (time/team constraints), NFR-010 (cost minimization)
---

[NFR-008]: Secure authentication and encryption (TLS or equivalent)  
**Description:** “The DigitalHome web system shall provide for authentication and information encryption through a recognized reliable and effective security technology, such as Transport Layer Security. The system shall support TLS v1.2 or higher with AES-256-GCM or ChaCha20-Poly1305 ciphers; server certificates must be rotated annually and stored encrypted at rest. Audit/event logs (authn/conf change) retained ≥1y, reviewed monthly by admin, exportable in CSV/JSON. Audit/event logs must follow schema {event_id, timestamp, user_id, role, action, target, status}. Export interface: REST endpoint with CSV/JSON output; logs retrievable within 1 hour of event. Admin review monthly; retention ≥1y enforced by system.” (Next action: Amend NFR-008 and ASR-006 to specify audit log schema, review process, and export method.)  
**Quality Attributes**: Security (Confidentiality, Authentication)  
**Measurable Criteria (if provided):** TLS v1.2+; AES-256-GCM or ChaCha20-Poly1305; certificate rotation ≤ 12 months; certs stored encrypted at rest; audit logs retained ≥1 year; monthly admin review; exportable CSV/JSON via REST; schema {event_id,timestamp,user_id,role,action,target,status}; logs retrievable within 1 hour; retention enforced by system  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-032, FR-033, FR-034
- **Conflicts with:** NFR-001/NFR-002 (security overhead may impact timing), NFR-010 (cost)
---

[NFR-009]: Internet Service Provider requirement (broadband)  
**Description:** “The home system shall require an Internet Service Provider (ISP). The Internet connection to the home server must provide at least 5 Mbps down/1 Mbps up with 99% monthly uptime. Acceptance: At install, system performs bandwidth/uptime test; reports warning if <5Mbps down/1Mbps up.” (Next action: Add install/connectivity test and measurement to NFR-009.)  
**Quality Attributes**: External dependency, Availability constraint  
**Measurable Criteria (if provided):** ≥5 Mbps down / ≥1 Mbps up; ≥99% monthly uptime; install-time bandwidth/uptime test with warning below thresholds  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-001
- **Conflicts with:** Not identified
---

[NFR-010]: Minimize cost of system elements due to competition  
**Description:** “Because of potential market competition… the cost of DigitalHome elements… for this project should be minimized. Total BOM (bill of materials) for prototype must not exceed $1,200 per system, but not at the expense of required reliability, security, and device coverage. Achievement of reliability, security, and device coverage requirements takes priority over cost minimization; BOM target of $1,200 may be exceeded if required for compliance. BOM may exceed $1,200 if necessary to meet reliability (NFR-004), security (NFR-008), or testability requirements—with written approval from project sponsor and documented escalation.” (Next action: Amend NFR-010 with clear exception/escalation process.)  
**Quality Attributes**: Cost constraint  
**Measurable Criteria (if provided):** Prototype BOM ≤ $1,200 per system; may be exceeded to meet required reliability/security/device coverage/testability with written sponsor approval and documented escalation  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** NFR-001, NFR-002, NFR-003, NFR-004, NFR-007, NFR-008
---

[NFR-011]: Delivery and staffing constraints  
**Description:** “The ‘prototype’ version… must be completed within twelve months of inception. The development team will consist of five engineers. If 80% simulation scenario coverage cannot be achieved by release, delivery shall prioritize environmental monitoring over advanced HVAC integrations. Acceptance: Release is allowed with ≥80% simulation case coverage + environmental monitoring features, even if HVAC integration <100%. Exceptions escalated to PM.” (Next action: Clarify schedule tradeoff/exit-case in NFR-011 and ASR-010.)  
**Quality Attributes**: Project constraint (Schedule/Resources)  
**Measurable Criteria (if provided):** 12 months; 5 engineers; ≥80% simulation scenario coverage release criterion; environmental monitoring must ship; HVAC integration may be <100% with escalation path to PM  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** NFR-007, NFR-004 (quality targets under tight resources)
---

[NFR-012]: Use widely accepted technology and standards where possible  
**Description:** “Where possible, the DigitalHome project will employ widely used, accepted, and available hardware and software technology and standards, both for product elements and for development tools. All network protocol implementations must use standardized RFC7272 compliant stack unless written exception approved by CIO. Supplement: 'Accepted Tech List'; process: team lead requests exception via CIO email, logs ticket tracking.” (Next action: Document list and process in NFR-012 and cross-ref in developer guides.)  
**Quality Attributes**: Maintainability, Interoperability, Portability (constraint)  
**Measurable Criteria (if provided):** RFC7272 compliant stack required for network protocol implementations; exception request via CIO email with ticket tracking  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** NFR-010 (cost), NFR-011 (schedule)
---

[NFR-013]: HVAC compatibility and adherence to ASHRAE 2010  
**Description:** “The system shall be compatible with a centralized HVAC… gas, oil, electricity, solar… The system shall adhere to the standards, policies and procedures of the American Society of Heating, Refrigerating and Air-Conditioning Engineers [ASHRAE 2010]. Thermostat subsystem shall pass ASHRAE 2010 section 5.3 compliance test using 3rd-party certification.” (Next action: Define concrete compliance acceptance criteria for HVAC standards.)  
**Quality Attributes**: Compatibility, Compliance  
**Measurable Criteria (if provided):** Pass ASHRAE 2010 section 5.3 compliance test with 3rd-party certification  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007..FR-013
- **Conflicts with:** NFR-010
---

[NFR-014]: Documentation format and archival requirement  
**Description:** “All system documents… shall be up-to-date, use the Homeowner document format [HO2305] and reside in the HomeOwner Document Archive at completion of the project. QA will inspect at project closure that SRS, architectural design, detailed design, code, and test plans are all in [HO2305] format, present in Document Archive, and up-to-date with release version.” (Next action: Add acceptance test steps for documentation.)  
**Quality Attributes**: Maintainability, Process/Compliance  
**Measurable Criteria (if provided):** QA inspection at project closure; required artifacts present; HO2305 format; stored in Document Archive; up-to-date with release version  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-011
- **Conflicts with:** Not identified
---

[NFR-015]: Object-oriented development with UML 2.0 preferred method  
**Description:** “HomeOwner has designated object-oriented development, using UML 2.0, as the preferred method…”  
**Quality Attributes**: Process constraint, Maintainability  
**Measurable Criteria (if provided):** UML 2.0 mandated/preferred; exceptions require approval  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014
- **Conflicts with:** Not identified
---