# Architecturally Significant Requirements Results:
[ASR-001]: System Architecture
**Description**: The DigitalHome system shall consist of household devices, sensors and controllers for the devices, communication links between the components, and a computer system to manage the components.
**Architectural Impact**: This requirement influences the overall system architecture, including the selection of components, communication protocols, and system management.
**Quality Attributes Affected**: Performance, Reliability, Scalability
**Architectural Constraints**: The system must be able to manage a variety of devices and sensors, and must be able to communicate with them effectively.
**Rationale**: This requirement is architecturally significant because it defines the overall structure of the system and has a significant impact on the system's performance, reliability, and scalability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002, FR-003
- **Conflicts with:** None
---
[ASR-002]: Communication Protocol
**Description**: The DigitalHome Gateway device shall provide communication with all the DigitalHome devices and shall connect with a broadband Internet connection.
**Architectural Impact**: This requirement influences the selection of communication protocols and the design of the system's communication infrastructure.
**Quality Attributes Affected**: Performance, Reliability
**Architectural Constraints**: The system must be able to communicate with a variety of devices and must be able to connect to a broadband Internet connection.
**Rationale**: This requirement is architecturally significant because it defines the communication protocol used by the system and has a significant impact on the system's performance and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005
- **Conflicts with:** None
---
[ASR-003]: Data Storage
**Description**: User(id:UUID, name, email, hash), Plan(id, user_id, params...), Device(id, type, location...).
**Architectural Impact**: This requirement influences the design of the system's data storage infrastructure.
**Quality Attributes Affected**: Performance, Reliability
**Architectural Constraints**: The system must be able to store a variety of data, including plans and user information.
**Rationale**: This requirement is architecturally significant because it defines the data storage requirements of the system and has a significant impact on the system's performance and reliability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007
- **Conflicts with:** None
---
[ASR-004]: System Security
**Description**: The DigitalHome web system shall provide for authentication and information encryption through a recognized reliable and effective security technology, such as Transport Layer Security.
**Architectural Impact**: This requirement influences the design of the system's security infrastructure.
**Quality Attributes Affected**: Security
**Architectural Constraints**: The system must be able to provide secure authentication and encryption.
**Rationale**: This requirement is architecturally significant because it defines the security requirements of the system and has a significant impact on the system's security.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** None
---
[ASR-005]: System Backup and Recovery
**Description**: After each backup, verify checksum; every week, a restore is executed to test data integrity and reports results.
**Architectural Impact**: This requirement influences the design of the system's backup and recovery infrastructure.
**Quality Attributes Affected**: Reliability, Availability
**Architectural Constraints**: The system must be able to backup and recover system data.
**Rationale**: This requirement is architecturally significant because it defines the backup and recovery requirements of the system and has a significant impact on the system's reliability and availability.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** None