# Architecturally Significant Requirements Results:
[ASR-001]: Interconnection of Heterogeneous TMC Systems
**Description**: The system shall provide a documented plugin API in C and/or C++ for adapter modules supporting XML/CSV parse, including versioning and isolation mechanism.
**Architectural Impact**: This requirement influences the architecture by requiring a flexible and modular design to accommodate different systems.
**Quality Attributes Affected**: Interoperability, Scalability, Maintainability
**Architectural Constraints**: The system must be able to communicate with different systems using various protocols and data formats.
**Rationale**: This requirement is architecturally significant because it requires a high degree of flexibility and modularity in the system design.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[ASR-002]: Use of ITS Standards
**Description**: System shall adopt TMDD v3.0 as of project launch, with annual review for version upgrades ensuring 1 year backward compatibility.
**Architectural Impact**: This requirement influences the architecture by requiring the use of standard data formats and protocols.
**Quality Attributes Affected**: Interoperability, Scalability, Maintainability
**Architectural Constraints**: The system must be designed to use the TMDD standard and other ITS data elements and message sets.
**Rationale**: This requirement is architecturally significant because it requires the use of standard data formats and protocols, which can impact the system's interoperability and scalability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-041
- **Conflicts with:** None
---
[ASR-003]: Deployable Building Blocks
**Description**: Append schema JSON/YAML for building block parameters.
**Architectural Impact**: This requirement influences the architecture by requiring a modular and configurable design.
**Quality Attributes Affected**: Scalability, Maintainability, Flexibility
**Architectural Constraints**: The system must be designed to allow for multiple instances of building blocks to be deployed and configured.
**Rationale**: This requirement is architecturally significant because it requires a high degree of modularity and configurability in the system design.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[ASR-004]: Security and Authentication
**Description**: Sessions shall expire after 30 mins inactivity; audit logs record: userID, auth method, request, status, IP, timestamp.
**Architectural Impact**: This requirement influences the architecture by requiring secure communication and authentication mechanisms.
**Quality Attributes Affected**: Security, Availability
**Architectural Constraints**: The system must be designed to ensure secure communication and authentication.
**Rationale**: This requirement is architecturally significant because it requires secure communication and authentication mechanisms, which can impact the system's security and availability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[ASR-005]: Data Storage and Management
**Description**: The Data Collector shall be designed to support the storage of TMDD data elements and message set information.
**Architectural Impact**: This requirement influences the architecture by requiring a data storage and management system.
**Quality Attributes Affected**: Scalability, Maintainability, Performance
**Architectural Constraints**: The system must be designed to store and manage large amounts of data.
**Rationale**: This requirement is architecturally significant because it requires a data storage and management system, which can impact the system's scalability, maintainability, and performance.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-040
- **Conflicts with:** None
---
[ASR-006]: System Integration
**Description**: The Center-to-Center infrastructure implements a repository for traffic data and provides a mechanism to exchange device control information between TMCs.
**Architectural Impact**: This requirement influences the architecture by requiring system integration and data exchange mechanisms.
**Quality Attributes Affected**: Interoperability, Scalability, Maintainability
**Architectural Constraints**: The system must be designed to integrate with other systems and exchange data.
**Rationale**: This requirement is architecturally significant because it requires system integration and data exchange mechanisms, which can impact the system's interoperability, scalability, and maintainability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None