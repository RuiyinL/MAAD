# Architecturally Significant Requirements Results:
[ASR-001]: Service-Oriented Architecture
**Description**: The CCTNS system should be implemented using Service Oriented Architecture (SOA) and have a modular design.
**Architectural Impact**: This requirement influences the overall architecture of the system, requiring a modular and service-oriented design.
**Quality Attributes Affected**: Scalability, Maintainability, Performance
**Architectural Constraints**: The system must be designed as a collection of services that can be easily integrated and modified.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring a modular and service-oriented architecture.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-002]: Centralized Deployment
**Description**: Centralized at State DC, with off-site (district/region) DR/failover. Management by Govt. IT; audit yearly.
**Architectural Impact**: This requirement influences the deployment and maintenance strategy of the system, requiring a centralized approach.
**Quality Attributes Affected**: Scalability, Maintainability, Performance
**Architectural Constraints**: The system must be designed to be deployed and maintained from a central location.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the deployment and maintenance strategy of the system.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001
- **Conflicts with:** None
---
[ASR-003]: Security and Access Control
**Description**: All at-rest sensitive data must use AES-256-GCM via FIPS 140-2 validated modules; keys rotated every 90 days, tracked in audit trail; tested quarterly.
**Architectural Impact**: This requirement influences the security and access control mechanisms of the system, requiring a robust and secure design.
**Quality Attributes Affected**: Security, Performance
**Architectural Constraints**: The system must be designed to prevent cross-site scripting and utilize parameterized queries.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the security and access control mechanisms of the system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[ASR-004]: Audit Trail
**Description**: Metric: audit_chain_integrity_pass_rate, Window: weekly, Alert: violation_detected > 0 this window.
**Architectural Impact**: This requirement influences the auditing and logging mechanisms of the system, requiring a robust and secure design.
**Quality Attributes Affected**: Security, Performance
**Architectural Constraints**: The system must be designed to maintain an unalterable audit trail.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the auditing and logging mechanisms of the system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** None
---
[ASR-005]: Scalability and Performance
**Description**: The CCTNS system be scaleable and must not have any features which would preclude use in small or large police stations, with varying numbers of cases handled.
**Architectural Impact**: This requirement influences the scalability and performance of the system, requiring a design that can handle varying workloads.
**Quality Attributes Affected**: Scalability, Performance
**Architectural Constraints**: The system must be designed to be scalable and performant.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the scalability and performance of the system.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001
- **Conflicts with:** None
---