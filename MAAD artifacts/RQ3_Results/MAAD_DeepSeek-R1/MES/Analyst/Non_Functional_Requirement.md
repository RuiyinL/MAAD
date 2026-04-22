# Non-Functional Requirements Results:
[NFR-001]: Daily Processing Timeliness  
**Description:** The APAF system shall automatically process telemetry data on a daily basis. Processing considered complete when all files have Validated and Stored status by 03:00 UTC and ProcessingLog written. Alert if any file missing at cutoff. [Next action: Detail processing exit/state, update acceptance/test plan.]  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** Processing completed by 03:00 UTC daily with >99% success.  
**Dependencies** / **Conflicts**:  
---  
[NFR-002]: ASPERA-3 IDFS Distribution Timeliness  
**Description:** ASPERA-3 IDFS data shall be provided to Co-I’s within 24 hours of acquisition if error-free.  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 24-hour distribution window.  
**Dependencies** / **Conflicts**:  
---  
[NFR-003]: MEX OA IDFS Distribution Timeliness  
**Description:** MEX OA IDFS data shall be provided to Co-I’s within 24 hours of acquisition if error-free.  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 24-hour distribution window.  
**Dependencies** / **Conflicts**:  
---  
[NFR-004]: Intermediate Files Distribution Timeliness  
**Description:** Intermediate files shall be provided to Co-I’s within 24 hours of acquisition if error-free.  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 24-hour distribution window.  
**Dependencies** / **Conflicts**:  
---  
[NFR-005]: PDS Submission Timeliness  
**Description:** ASPERA-3 data shall be provided to NASA PDS within 6 months after acquisition.  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** 6-month submission deadline.  
**Dependencies** / **Conflicts**:  
---  
[NFR-006]: Safety Compliance  
**Description:** The APAF data system will not impose hazards to personnel, property, or the environment. Test acceptance: FMEA worksheet attached; all identified mitigations in tracking doc; incident log in central repo, summary delivered quarterly to compliance. [Next action: Refine acceptance and control plan per compliance/ops input.]  
**Quality Attributes**: Safety  
**Measurable Criteria (if provided):** FMEA hazard class ≤3, all mitigations implemented, NDA signed for traceable incident log.  
**Dependencies** / **Conflicts**:  
---