# Architecturally Significant Requirements Results:
[ASR-001]: Daily Batch Processing Constraint  
**Description**: The APAF system shall acquire telemetry data and automatically process it on a daily basis.  
**Architectural Impact:**  
Mandates a batch-oriented pipeline architecture with scheduling capabilities. Requires idempotent processing steps and fault recovery to handle daily cycles.  
**Quality Attributes Affected:**  
Performance, Reliability  
**Architectural Constraints:**  
Must implement scheduled batch processing with defined completion windows (e.g., 01:00–03:00 UTC).  
**Rationale:**  
High impact due to strict timing constraints dictating system decomposition (modular pipelines) and state management.  
**Dependencies** / **Conflicts**:  
Depends on FR-001  
---  
[ASR-002]: 24-Hour Conditional Distribution  
**Description**: Electronically distributed data/products must be delivered to Co-I’s within 24 hours if error-free.  
**Architectural Impact:**  
Drives event-driven workflows with validation gates, retry mechanisms, and real-time alerting. Necessitates explicit SLAs for pipeline stages.  
**Quality Attributes Affected:**  
Performance, Reliability  
**Architectural Constraints:**  
Requires quarantine mechanisms for error handling and state tracking (e.g., Created → Validated → Distributed). Distribution occurs only if integrity and schema checks pass all pipeline steps. Acceptance: For ≥99% of cases, transition from Validated to Distributed state within 24 hours logged. SLA breach triggers PagerDuty alert.  
**Rationale:**  
Architecturally significant due to end-to-end timeliness requirements influencing communication patterns and error recovery strategies.  
**Dependencies** / **Conflicts**:  
Depends on FR-016, FR-017, FR-018  
---  
[ASR-003]: Local Archival for Reprocessing  
**Description**: Telemetry, IDFS datasets, and intermediate files must be stored locally for reprocessing/availability.  
**Architectural Impact:**  
Demands scalable storage subsystems and versioned data contracts. Influences component interactions (e.g., ingest → archive → reprocess).  
**Quality Attributes Affected:**  
Reliability, Maintainability  
**Architectural Constraints:**  
Mandates: Data held ≥5 years; backup daily; restore test quarterly; schema version metadata present. Acceptance: SRE logs show daily backup with ≥99% success; quarterly restore test report entered into OpsLog; retention monitoring alert if any file >5y old is deleted.  
**Rationale:**  
High impact due to storage scalability requirements and cross-cutting data lifecycle management.  
**Dependencies** / **Conflicts**:  
Depends on FR-005, FR-006, FR-007  
---  
[ASR-004]: Dual-Mode Web Dissemination  
**Description**: Public displays of current data vs. password-protected team displays for full analysis.  
**Architectural Impact:**  
Enforces RBAC, audit logging, and strict session management. Requires decoupling data processing from presentation layers.  
**Quality Attributes Affected:**  
Security, Usability  
**Architectural Constraints:**  
Must implement: All restricted endpoints require RBAC with MFA (TOTP). Session timeout 30 min. Audit log (ISO 27001-compliant) retained ≥180 days. Acceptance: All login events logged to AuditLog, session inactivity timeout at 30 min verified quarterly, MFA (TOTP) required for all RBAC-protected endpoints.  
**Rationale:**  
Cross-cutting security concerns affecting UI, API design, and data access layers.  
**Dependencies** / **Conflicts**:  
Depends on FR-008, FR-009, FR-010, FR-015  
---  
[ASR-005]: Built-in Error Handling  
**Description**: The system shall implement built-in error handling for data integrity.  
**Architectural Impact:**  
Requires centralized error tracking, quarantine states, and validation services at pipeline stages.  
**Quality Attributes Affected:**  
Reliability, Integrity  
**Architectural Constraints:**  
Mandates SchemaValidationService and Quarantine+Alerting components. Acceptance: ≥99.9% errors processed by SchemaValidationService routed to quarantine within 2 min. Alert issued for alert_time_p95 >2 min (24h rolling window).  
**Rationale:**  
High-risk cross-cutting concern impacting data flow design and operational monitoring.  
**Dependencies** / **Conflicts**:  
Depends on FR-011  
---  
[ASR-006]: PDS Submission Deadline  
**Description**: ASPERA-3 data must be submitted to PDS within 6 months after acquisition.  
**Architectural Impact:**  
Drives asynchronous validation workflows and long-running process management. Requires versioned schema compliance.  
**Quality Attributes Affected:**  
Performance, Compliance  
**Architectural Constraints:**  
Must support states like PDSReady → PDSSubmitted with versioned schema references. Acceptance: >99% of datasets have PDSSubmitted timestamp within 6 months of PDSReady. Compliance checker log attached to submission artifact.  
**Rationale:**  
Architecturally significant due to extended timelines requiring checkpointing and compliance checks.  
**Dependencies** / **Conflicts**:  
Depends on FR-022  
---