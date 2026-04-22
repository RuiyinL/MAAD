# Architecturally Significant Requirements Results:
[ASR-001]: System Architecture with Supported COTS Software
**Description**: At go-live and annually, vendor SHALL produce an SBOM that lists all COTS/OS/database/software components, all confirmed under support, with documented upgrade path for every platform module.

**Architectural Impact**: This requirement influences the technology selection and component decomposition of the system.

**Quality Attributes Affected**: Performance, Security, Scalability

**Architectural Constraints**: The system must use supported COTS software and operating systems.

**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system and involves major trade-offs between performance, security, and scalability.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** None
---

[ASR-002]: Data Integrity with NIST-Approved Hash Function
**Description**: The system must use a NIST-approved hash (e.g., SHA-256); implementation must support algorithm upgrade with minimal rework.

**Architectural Impact**: This requirement influences the data storage and communication patterns of the system.

**Quality Attributes Affected**: Security, Reliability

**Architectural Constraints**: The system must use a NIST-approved hash function to maintain data integrity.

**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system and involves major trade-offs between security and reliability.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-002
- **Conflicts with:** None
---

[ASR-003]: Scalability with Defined Test Process
**Description**: Acceptance: Under simulated load of two additional DCUs, four additional CMSs, and twenty contact closures, average response time for device status/control commands must not exceed 110% of baseline (measured on reference hardware, n=1000 samples per function, with load characteristics documented in test plan ASP-TC-SCAL-001).

**Architectural Impact**: This requirement influences the scalability strategy of the system.

**Quality Attributes Affected**: Performance, Scalability

**Architectural Constraints**: The system must be able to scale up to a maximum of two additional DCU controllers.

**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system and involves major trade-offs between performance and scalability.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** None
---