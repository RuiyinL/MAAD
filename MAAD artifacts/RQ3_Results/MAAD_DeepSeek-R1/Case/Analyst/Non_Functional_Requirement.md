# Non-Functional Requirements Results:
[NFR-001]: Real-Time Passenger Comfort  
**Description**: The shuttle journey shall be as fast as possible subject to limits on speed, acceleration, and deceleration for passenger comfort and equipment longevity.  
**Quality Attributes**: Performance, Reliability  
**Measurable Criteria (if provided):** Shuttle speed ≤ 3.0 m/s, acceleration ≤ 1.2 m/s², deceleration ≤ 1极速赛车开奖直播开奖结果🔸5 m/s².  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-015  
- **Conflicts with:** None  
---  

[NFR-002]: Secure Facial Recognition  
**Description**: Upon authenticated deletion request (OIDC-verified user), system must erase biometric data within 30 days, log the erasure event, and notify requester by email within 24 hours of completion.  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Biometric accuracy: <1% false acceptance; encryption: AES-256; audit logs retained 90 days.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005  
- **Conflicts with:** None  
---  

[NFR-003]: Library Membership Enforcement  
**Description**: Overdue fines = $0.50/day; compliance_reports: [{member_id, fine_amount, overdue_days}].  
**Quality Attributes**: Compliance  
**Measurable Criteria (if provided):** Automated verification of: (1) borrowing privileges restricted to members, (2) fine calculation accuracy, (3) report completeness.  
**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---