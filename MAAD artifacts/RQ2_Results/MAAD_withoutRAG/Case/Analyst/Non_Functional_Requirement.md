# Non-Functional Requirements Results:

[NFR-001]: Real-time and scheduled timing constraints (domain-specific)  
**Description:** Multiple requirements specify fixed timing: ICU “periodic basis (specified for each patient)”; traffic lights phases of 50s/120s; sluice gate “ten minutes in every three hours”; shuttle “stopping for 60 seconds”; heating “starting ... 30 minutes before occupancy”. ICU sampling interval configurable from 1s to 15min per patient; periodic scheduling must guarantee maximum jitter of 100ms. Metric: icu_acquisition_jitter_ms; measured per-patient over 24h rolling window; alert if >100ms jitter in >0.1% of periods. Document as Prometheus metric. [Next action: Add metrics names, alert thresholds, and review points to requirements.]  
**Quality Attributes**: Performance (Timing), Real-time behavior  
**Measurable Criteria (if provided):** 50s/120s phases; 10 min/3 hours; 60s dwell; 30 min preheat; ICU sampling interval 1s to 15min per patient; maximum jitter 100ms; icu_acquisition_jitter_ms measured per-patient over 24h; alert if >100ms jitter in >0.1% of periods.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-023, FR-034, FR-046, FR-018
- **Conflicts with:** NFR-010 (comfort/wear constraints may limit fastest travel)
---

[NFR-002]: ICU sampling frequency per patient must be configurable  
**Description:** The program reads these factors on a periodic basis (specified for each patient). Sampling period: 1 second ≤ T ≤ 15 minutes (configurable per patient), enforced by scheduler validation. If sampling period set outside 1s–15min, system logs an ERROR with user ID/timestamp and blocks schedule. Metric patient_sampling_period_violation_total; alert if any blocked schedule >1 per 24h; audit log reviewed weekly. [Next action: Add ops alert and QA audit to requirement.]  
**Quality Attributes**: Configurability, Maintainability  
**Measurable Criteria (if provided):** Sampling period range: 1 second ≤ T ≤ 15 minutes; enforcement via scheduler validation; out-of-range handling logs ERROR with user ID/timestamp and blocks schedule; metric patient_sampling_period_violation_total; alert if blocked schedule >1 per 24h; weekly audit log review.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** NFR-001 (timing may require guarantees not stated)
---

[NFR-003]: Persist ICU measurements in a database (data management constraint)  
**Description:** ... stores the factors in a database. ICU DB must achieve ≥99.9% uptime; every write acknowledged with a checksum; failover test must verify no data loss on cold restart. Acceptance: Automated failover test with pre/post data hash comparison, pass if all records match; test run quarterly by SRE. [Next action: Specify scenario, fixture, and schedule for integrity/recovery validation.]  
**Quality Attributes**: Reliability, Data integrity (constraint)  
**Measurable Criteria (if provided):** ≥99.9% uptime; every write acknowledged with a checksum; no data loss verified in cold-restart failover test; automated failover test with pre/post data hash comparison; quarterly test run.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** NFR-004
---

[NFR-004]: Protect sensitive medical data (privacy/security constraint)  
**Description:** ICU patient factors and safe ranges are stored in a database; all stored medical data must be encrypted with AES-256 at rest and TLS 1.2+ in transit; all accesses and changes logged with user identity. All stored medical data must comply with HIPAA and/or GDPR; all encryption/persistence controls mapped to regulatory checklist; audit logging and encryption settings validated in quarterly compliance tests. Add: All data at rest: mapped to HIPAA §164.312(a)(2)(iv); GDPR Art.32. Audit log access mapped to HIPAA §164.312(b); GDPR Art.5(2). DPO: [Name]. Compliance test: Checklist in appendix. [Next action: Produce regulatory mapping table and assign DPO/reviewer.]  
**Quality Attributes**: Security, Privacy, Compliance  
**Measurable Criteria (if provided):** AES-256 at rest; TLS 1.2+ in transit; audit logging of all accesses/changes with user identity; quarterly compliance tests validating audit logging and encryption settings; mapping to HIPAA §164.312(a)(2)(iv)/§164.312(b) and GDPR Art.32/Art.5(2); compliance checklist in appendix; DPO assigned.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** None specified
---

[NFR-005]: Secure access control for door/court entry systems  
**Description:** “A secure door is to be controlled by a computer that recognises facial features.” and court entrance uses magnetic cards for entry. System shall provide a facial recognition decision within 2 seconds, with False Acceptance Rate ≤ 1% and False Rejection Rate ≤ 2%, and log all access attempts. Acceptance: At least 100 consecutive access attempts measured; 95%+ completed in ≤2s; FAR ≤1%, FRR ≤2%; log includes timestamp, attempt ID, and result. [Owner: SRE/Security QA. Next action: Write and run timing/error tests and produce evidence for review.]  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Facial recognition decision time ≤ 2 seconds; FAR ≤ 1%; FRR ≤ 2%; at least 100 consecutive attempts measured; 95%+ of attempts completed in ≤2s; logging includes timestamp, attempt ID, and result.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-054
- **Conflicts with:** NFR-006
---

[NFR-006]: Biometric privacy and data protection for facial features database  
**Description:** Facial features are compared with entries in a database of the features of people who have been cleared for entry. Templates must be encrypted (AES-256); system deletes templates within 30 days of authorization expiry, proved by periodic automated retention tests and audit/alert on violation; all handled as per GDPR/BIPA controls. Retention test: run weekly; alert on failure sent to DPO at [email]. Audit log reviewed monthly; acceptance: all expired templates deleted within SLA. [Next action: Document test schedule, owner, and alert path for template retention.]  
**Quality Attributes**: Privacy, Security, Compliance  
**Measurable Criteria (if provided):** AES-256 encryption for templates; deletion within 30 days of authorization expiry; weekly retention test; alert to DPO on failure; monthly audit log review; acceptance that all expired templates deleted within SLA; GDPR/BIPA controls referenced.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** None specified
---

[NFR-007]: Energy efficiency objective for heating control  
**Description:** “For economy ... unoccupied room should be 5 degrees below the knob setting” and predictive preheat based on occupancy. Metric: heating_setback_hours totalled per week; report reduction in kWh/room; acceptance: ≥15% reduction vs baseline. [Next action: Specify metrics and baseline/target for efficiency evaluation.]  
**Quality Attributes**: Efficiency (operational cost), Sustainability  
**Measurable Criteria (if provided):** 5 degrees setback; preheat begins 30 minutes prior; heating_setback_hours totalled weekly; report kWh/room reduction; acceptance ≥15% reduction vs baseline.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-018
- **Conflicts with:** FR-012 (comfort vs economy trade-off)
---

[NFR-008]: Compatibility with ASCII-encoded configuration via magnetic card reader  
**Description:** “The regime is encoded on the card as a simple ASCII text. When ... insert ... computer reads the card and controls the lights accordingly.” ASCII card format: Line-based, phase=duration(s); E.g.: STOP=50,GO=120,STOP=50,GO=120. BNF: regime ::= phase_duration (',' phase_duration)* ; phase_duration ::= PHASE '=' INT ; PHASE ∈ {STOP,GO}. [Next action: Add syntax specification and example fixtures for config input.]  
**Quality Attributes**: Interoperability, Maintainability  
**Measurable Criteria (if provided):** Format defined as line-based phase=duration(s); example STOP=50,GO=120,STOP=50,GO=120; BNF grammar as specified.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-025
- **Conflicts with:** FR-023 (fixed cycle)
---

[NFR-009]: Command-line text UI style for party-plan editor  
**Description:** “The editor will accept command-line text input, in a very old-fashioned DOS or Unix style.” Acceptance: At least 5 commands demonstrated runnable under Windows cmd.exe and Unix shell (e.g. Bash); user can edit, save, and reload a party plan in CLI. Commands: add_party, add_guest, invite, remove, save, load. Acceptance: Each triggers expected state; error produces stderr output and exit code 1. [Next action: List core commands and error handling behaviors.]  
**Quality Attributes**: Usability (constraint), Compatibility  
**Measurable Criteria (if provided):** At least 5 commands runnable under Windows cmd.exe and Unix shell; edit/save/reload party plan via CLI; required commands add_party/add_guest/invite/remove/save/load; errors produce stderr and exit code 1.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-041
- **Conflicts with:** None specified
---

[NFR-010]: Passenger comfort and equipment wear constraints for shuttle motion  
**Description:** “The journey should be as fast as possible, subject to certain limits on the speed, acceleration and deceleration ... comfortable ride ... avoid excessive wear on the motor and brakes.” Max acceleration ≤ 1.5 m/s², max deceleration ≤ 1.2 m/s², cruise speed ≤ 35km/h; comfort score ≥ 90/100 in simulated ride. Simulate 20 shuttle rides in SRE-lab; collect accelerometer data at 10Hz, calculate comfort per ISO 2631-1. Acceptance: 20 shuttle rides simulated; calculate per-ride comfort; requirement passes if mean >= 90/100; outlier rides reviewed by SRE lead. [Next action: Write up acceptance test protocol and comfort scoring algorithm.]  
**Quality Attributes**: Safety/Comfort, Reliability, Maintainability  
**Measurable Criteria (if provided):** Max acceleration ≤ 1.5 m/s²; max deceleration ≤ 1.2 m/s²; cruise speed ≤ 35 km/h; simulate 20 rides; accelerometer sampling 10 Hz; comfort per ISO 2631-1; pass if mean comfort >= 90/100; outlier review by SRE lead.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** FR-046 (fastest possible vs limits)
---