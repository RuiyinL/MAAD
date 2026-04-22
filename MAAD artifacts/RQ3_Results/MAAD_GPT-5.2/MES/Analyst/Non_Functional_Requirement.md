# Non-Functional Requirements Results

[NFR-001]: Daily automated processing cadence  
**Description:** “...to automatically process the data on a daily basis.” Updated per evaluator: “Processing job must complete between 01:00 and 03:00 UTC each day; failures must alert SRE within 10 min.” (Next action: Set/clarify daily processing time window.)  
**Quality Attributes**: Performance / Operational constraint (Scheduling)  
**Measurable Criteria (if provided):** Processing completes between 01:00 and 03:00 UTC daily; failures alert SRE within 10 minutes  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003
- **Conflicts with:** Not identified  
---

[NFR-002]: Password protection for science-analysis web displays until data is public  
**Description:** “The web-based displays defined by the ASPERA-3 team to be used for science analysis shall be password protected until the ASPERA-3 data is made public…” Updated per evaluator: “Auth logs retained at least 180 days; MFA required for team accounts; transition to public requires signoff by PI logged to audit trail.” (Next action: Define authentication flows, log retention, and publication approval process.)  
**Quality Attributes**: Security / Privacy  
**Measurable Criteria (if provided):** Auth logs retained ≥ 180 days; MFA required for team accounts; PI signoff required and logged for transition to public  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** Not identified  
---

[NFR-003]: Web server access control for pertinent team members  
**Description:** “The APAF system web server shall be password protected where appropriate to allow only pertinent ASPERA-3 team members access.” Updated per evaluator: “Passwords must be at least 12 chars, rotated every 90 days; accounts deactivated within 72 hours of team member departure.” (Next action: Draft credential, password, and access provisioning standards.)  
**Quality Attributes**: Security / Privacy  
**Measurable Criteria (if provided):** Password length ≥ 12 characters; rotation every 90 days; account deactivation within 72 hours of departure  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-009
- **Conflicts with:** Not identified  
---

[NFR-004]: Built-in error handling for data integrity  
**Description:** “The APAF ground data system shall have built-in error handling for better data integrity.” Updated per evaluator: “The system shall detect: (1) checksum mismatch, (2) missing file, (3) schema nonconformance; in each case, alert SRE within 10 minutes, place artifact in quarantine, and log event to [error_audit_log], reviewable within 1 hour.” (Next action: Update the requirement to enumerate error types and describe alerting, quarantine, and logging, with measurable SLAs.)  
**Quality Attributes**: Reliability / Data Integrity  
**Measurable Criteria (if provided):** Detect checksum mismatch, missing file, schema nonconformance; alert SRE within 10 minutes; quarantine artifact; log to [error_audit_log]; reviewable within 1 hour  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-010, FR-013
- **Conflicts with:** Not identified  
---

[NFR-005]: Delivery timeliness for electronically distributed ASPERA-3 IDFS data  
**Description:** “ASPERA-3 IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ASPERA-3 telemetry as long as the transmission and processing are error-free…” Updated per evaluator: “If transmission or processing errors occur, notify recipients within 2 hours and attempt automated retry up to 3 times; successful delivery measured as confirmation receipt from all Co-Is within 24±2 hours after telemetry acquisition.” (Next action: Redefine NFR to include error detection/reporting/testable exception handling.)  
**Quality Attributes**: Performance (Timeliness) / Service Level  
**Measurable Criteria (if provided):** Notify within 2 hours on errors; automated retry up to 3 times; confirmation receipt from all Co-Is within 24±2 hours after telemetry acquisition  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-010
- **Conflicts with:** Not identified  
---

[NFR-006]: Delivery timeliness for electronically distributed MEX OA IDFS data  
**Description:** “MEX OA IDFS data that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring MEX OA telemetry as long as the transmission and processing are error-free…”  
**Quality Attributes**: Performance (Timeliness) / Service Level  
**Measurable Criteria (if provided):** ≤ 24 hours from telemetry acquisition (conditional)  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003, FR-010
- **Conflicts with:** Not identified  
---

[NFR-007]: Delivery timeliness for electronically distributed intermediate cleaned-up telemetry files  
**Description:** “Any APAF-generated intermediate files… that are electronically distributed shall be provided to the ASPERA-3 Co-I’s within 24 hours of acquiring ASPERA-3 and MEX OA telemetry as long as the transmission and processing are error-free…”  
**Quality Attributes**: Performance (Timeliness) / Service Level  
**Measurable Criteria (if provided):** ≤ 24 hours from telemetry acquisition (conditional)  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-004, FR-010
- **Conflicts with:** Not identified  
---

[NFR-008]: PDS submission deadline  
**Description:** “ASPERA-3 data shall be provided to NASA PDS no later than 6 months after acquisition.”  
**Quality Attributes**: Compliance / Timeliness  
**Measurable Criteria (if provided):** ≤ 6 months after acquisition  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-014, FR-015
- **Conflicts with:** Not identified  
---

[NFR-009]: No hazards to personnel, property, or environment  
**Description:** “The APAF data system will not impose hazards to personnel, property, or the environment.” Updated per evaluator: “System must pass annual organizational IT safety audit and have zero open severity-1 findings regarding safety to personnel/property/environment.” (Next action: Anchor NFR to specific testable/certifiable process or metric.)  
**Quality Attributes**: Safety  
**Measurable Criteria (if provided):** Pass annual organizational IT safety audit; zero open severity-1 safety findings  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** Not identified  
---

[NFR-010]: Requirement identifiers must be project-unique  
**Description:** “Each requirement shall be: assigned a project-unique identifier.” Updated per evaluator: “Requirement IDs allocated and managed in central requirements tracking system; verified on SDD handoff.” (Next action: Establish/document requirement ID management system.)  
**Quality Attributes**: Maintainability / Traceability (Process constraint)  
**Measurable Criteria (if provided):** Verified on SDD handoff (central tracking system details not specified)  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** Not identified  
---

[NFR-011]: No training required due to sufficient operational documentation  
**Description:** “...installation and operations procedures… in enough detail where there are no training-related requirements for users and operators…” Updated per evaluator: “Acceptance: 3 randomly selected operators can perform installation and basic operations by following the documentation, with <1 critical support request.” (Next action: Define a documentation acceptance test or usability proxy.)  
**Quality Attributes**: Usability / Operability  
**Measurable Criteria (if provided):** 3 randomly selected operators complete installation and basic operations using documentation; <1 critical support request  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019
- **Conflicts with:** Not identified  
---

[NFR-012]: Consideration of software quality factors during development  
**Description:** “Some of the software quality factors that will be considered when developing the APAF data system include: reliability, maintainability, availability, flexibility, portability, testability, and usability.” Updated per evaluator: “Availability: Uptime ≥ 99.7% as measured by [service_monitor]; maintainability: all critical defects resolved in <7 days, reported monthly.” (Next action: Define targets and measurement points for quality factors.)  
**Quality Attributes**: Reliability, Maintainability, Availability, Flexibility, Portability, Testability, Usability  
**Measurable Criteria (if provided):** Uptime ≥ 99.7% measured by [service_monitor]; critical defects resolved in <7 days; reported monthly  
**Dependencies** / **Conflicts**:
- **Depends on:** Not identified
- **Conflicts with:** Not identified  
---