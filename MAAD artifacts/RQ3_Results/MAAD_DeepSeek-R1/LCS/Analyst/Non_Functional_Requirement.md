# Non-Functional Requirements Results:
[NFR-001]: Continuous Availability  
**Description**: Total yearly uptime must be ≥99.99%, unless otherwise documented by contract or local reg.  
**Quality Attributes**: Reliability, Availability  
**Measurable Criteria**: ≥99.99% yearly uptime  
**Dependencies / Conflicts**:  
- **Depends on:** ASR-001  
---  

[NFR-002]: Data Integrity Verification  
**Description**: Replace all references to MD5 with 'SHA-256 or better is required for all cryptographic functions, including integrity and password storage.'  
**Quality Attributes**: Security, Integrity  
**Measurable Criteria**: SHA-256+ cryptographic enforcement  
**Dependencies / Conflicts**:  
- **Depends on:** ASR-002  
---  

[NFR-003]: Database Performance  
**Description**: If >50 events/min or >20 users, set system state=DEGRADED, log to SIEM, show GUI warning with mitigation instructions.  
**Quality Attributes**: Performance  
**Measurable Criteria**: Degrade strategy for overload conditions  
**Dependencies / Conflicts**:  
- **Depends on:** FR-003  
---  

[NFR-004]: Real-time Monitoring Latency  
**Description**: Acceptance: test with 10 events/min, up to 20 users, confirm field-to-GUI latency ≤2s, log delays and alert on >2.2s.  
**Quality Attributes**: Performance  
**Measurable Criteria**: Latency test protocol  
**Dependencies / Conflicts**:  
- **Conflicts with:** NFR-003 under overload  
---  

[NFR-005]: Password Security  
**Description**: All passwords are migrated to SHA-256 on first successful login; lockout after 5 failed logins in 10 minutes; legacy MD5 hashes must be upgraded.  
**Quality Attributes**: Security  
**Measurable Criteria**: Password migration, lockout policy, hash upgrade  
**Dependencies / Conflicts**:  
- **Depends on:** FR-002  
---