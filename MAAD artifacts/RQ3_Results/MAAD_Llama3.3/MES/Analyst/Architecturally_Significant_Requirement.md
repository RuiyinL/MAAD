# Architecturally Significant Requirements Results:
[ASR-001]: Modular Pipeline Architecture
**Description**: The APAF system shall acquire, process, and distribute telemetry data using a modular pipeline architecture. Pipeline modules: acquire (input: ESOC XML), process (output: IDFS XML), distribute (output: PDS package).
**Architectural Impact**: The requirement influences the technology selection, component decomposition, and data communication patterns.
**Quality Attributes Affected**: Performance, Scalability, Reliability
**Architectural Constraints**: The system must use a modular pipeline architecture.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design and has a high impact on the system's performance, scalability, and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003
- **Conflicts with:** None
---
[ASR-002]: Data Contract-First Approach
**Description**: Each telemetry and IDFS data object must have an associated XML Schema 1.1 definition with unique version number and example instance provided.
**Architectural Impact**: The requirement influences the data communication patterns, scalability strategies, and cross-cutting concerns.
**Quality Attributes Affected**: Interoperability, Data Integrity
**Architectural Constraints**: The system must use a contract-first approach for data integration.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design and has a high impact on the system's interoperability and data integrity.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003
- **Conflicts with:** None
---
[ASR-003]: RBAC and Audit Logging
**Description**: The APAF system shall implement RBAC with roles: admin, ASPERA-3 Co-I, public; audit logs shall record all authentication and data access attempts, be tamper-evident, and retained for at least 3 years. Acceptance Criterion: All audit logs must be stored in a WORM (Write Once Read Many) system or validated by cryptographic hash chain with quarterly audit reports.
**Architectural Impact**: The requirement influences the security, scalability, and cross-cutting concerns.
**Quality Attributes Affected**: Security, Compliance
**Architectural Constraints**: The system must enforce RBAC and maintain audit logs.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design and has a high impact on the system's security and compliance.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-002
- **Conflicts with:** None
---
[ASR-004]: PDS Compliance and Submission
**Description**: The APAF system shall provide ASPERA-3 data to NASA PDS in PDS-compliant form and within 6 months after acquisition.
**Architectural Impact**: The requirement influences the data communication patterns, scalability strategies, and cross-cutting concerns.
**Quality Attributes Affected**: Compliance, Performance
**Architectural Constraints**: The system must provide ASPERA-3 data to NASA PDS in PDS-compliant form and within 6 months after acquisition.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design and has a high impact on the system's compliance and performance.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, NFR-006, NFR-007
- **Conflicts with:** None