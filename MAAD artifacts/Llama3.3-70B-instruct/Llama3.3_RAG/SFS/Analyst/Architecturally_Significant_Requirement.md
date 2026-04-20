# Architecturally Significant Requirements Results:
[ASR-001]: Web-Based Architecture
**Description**: The Space Fractions system must support the latest two versions of Chrome, Firefox, Edge, Safari on Windows, Mac, iOS, Android. Replace all references to 'Flash' with 'HTML5 (WebAssembly/Canvas/JS/CSS)' in SRS and dependencies.
**Architectural Impact**: This requirement influences the technology selection and component decomposition of the system, as it must be designed to run on a web browser.
**Quality Attributes Affected**: Performance, Security, Scalability
**Architectural Constraints**: The system must be designed to run on a web browser, using web-based technologies such as HTML, CSS, and JavaScript.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring it to be web-based.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-002]: Modern Web Standards
**Description**: The Space Fractions system must use open web standards (HTML5/JavaScript/CSS) throughout.
**Architectural Impact**: This requirement influences the technology selection and component decomposition of the system, as it must be designed to support modern web standards.
**Quality Attributes Affected**: Performance, Security
**Architectural Constraints**: The system must be designed to support modern web standards, which may impose limitations on the system's performance and security.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring it to support modern web standards.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-003]: Administrator Authentication
**Description**: Administrator passwords must be hashed via bcrypt (min 10 rounds); audit log data must be write-once and stored encrypted at rest (AES-256).
**Architectural Impact**: This requirement influences the security and data storage architecture of the system, as it must be designed to authenticate administrators and store custom fraction questions securely.
**Quality Attributes Affected**: Security, Scalability
**Architectural Constraints**: The system must be designed to authenticate administrators and store custom fraction questions securely, which may impose limitations on the system's security and scalability.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring it to authenticate administrators and store custom fraction questions securely.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-004]: Single-User Access
**Description**: Regular user session expires at 60m idle; admin session at 10m idle.
**Architectural Impact**: This requirement influences the scalability and concurrency architecture of the system, as it must be designed to support single-user access.
**Quality Attributes Affected**: Scalability, Concurrency
**Architectural Constraints**: The system must be designed to support single-user access, which may impose limitations on the system's scalability and concurrency.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring it to support single-user access.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[ASR-005]: Internet Accessibility
**Description**: The system is web-based only and does not support offline/local installation; all updates occur centrally.
**Architectural Impact**: This requirement influences the deployment and accessibility architecture of the system, as it must be designed to be accessible over the Internet.
**Quality Attributes Affected**: Availability, Accessibility
**Architectural Constraints**: The system must be designed to be accessible over the Internet, which may impose limitations on the system's availability and accessibility.
**Rationale**: This requirement is architecturally significant because it imposes a strong constraint on the design of the system, requiring it to be accessible over the Internet.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---