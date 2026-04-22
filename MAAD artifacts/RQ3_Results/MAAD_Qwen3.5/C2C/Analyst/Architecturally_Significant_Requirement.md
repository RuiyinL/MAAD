# Architecturally Significant Requirements Results:

[ASR-001]: Heterogeneous System Interconnection
**Description**: The Center-to-Center infrastructure must interconnect several dissimilar traffic management systems. In order to create the Center-to-Center infrastructure, interfaces to the existing systems will be created. The data from these interfaces will communicate with the existing system in a "system specific" format. Acceptance: At least 3 concurrent unique interface protocols supported, full integration test coverage for all. Owner: Team-Integration; Next action: Expand ASR-001 with protocol testability acceptance metrics.

**Architectural Impact:**  
Drives the need for an integration layer capable of protocol translation. Requires an Adapter/Broker pattern to isolate system-specific formats from the canonical core. Impacts component decomposition by necessitating pluggable adapters for each dissimilar TMC system.

**Quality Attributes Affected:**  
Interoperability, Modifiability, Integration

**Architectural Constraints:**  
Must support multiple concurrent "system specific" interface protocols alongside the standard ITS protocol. At least 3 concurrent unique interface protocols supported.

**Rationale:**  
High risk due to heterogeneity. Directly influences the integration architecture (Microkernel + Adapter) as noted in reference knowledge to localize protocol translation and preserve modifiability.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Canonical Data Model)
- **Conflicts with:** None
---

[ASR-002]: Standards-Based Canonical Data Model
**Description**: The Center-to-Center project will be implemented using the evolving ITS Traffic Management Data Dictionary (TMDD) standard, the message sets associated with TMDD... The Center-to-Center Project shall utilize the TMDD standard (including message sets) to transmit information. DATEX/ASN shall be used to transmit the TMDD message sets. TCP/IP shall be used to transmit the DATEX/ASN data.

**Architectural Impact:**  
Mandates a canonical internal domain model aligned with TMDD. Requires specific codec components for DATEX/ASN encoding/decoding. Dictates the communication stack (TCP/IP). Enforces contract-first interface design.

**Quality Attributes Affected:**  
Interoperability, Scalability, Standards Compliance

**Architectural Constraints:**  
Must implement TMDD schema validation. Must support DATEX/ASN runtime library. Must use TCP/IP transport.

**Rationale:**  
Strong constraint on design and technology. Ensures reusability and future extension (Statewide baseline). Drives the decision for a canonical model and codec boundary.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Data Collection)
- **Conflicts with:** ASR-001 (Requires translation from system-specific formats)
---

[ASR-003]: Hierarchical Repository Federation
**Description**: This would allow a "local" common repository to be created by "linking" individual partners, a "regional" common repository to be created by "linking" local common repositories and a "statewide" common repository to be created by "linking" regional common repositories.

**Architectural Impact:**  
Requires a data architecture supporting federation or synchronization across tiers (Local->Regional->Statewide). Influences database schema (indexed canonical entities) and synchronization policy (batched pull, conflict resolution).

**Quality Attributes Affected:**  
Scalability, Availability, Data Consistency

**Architectural Constraints:**  
Database must support replication or federation mechanisms. Network topology must support hierarchical linking.

**Rationale:**  
High business value (Statewide baseline). Introduces complexity in data consistency and sync. Drives the repository-centric requirement and synchronization policy.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Data Collection), ASR-002 (Canonical Data Model)
- **Conflicts with:** None
---

[ASR-004]: Configurable Building Blocks
**Description**: The Center-to-Center infrastructure is being created using a series of building blocks. These building blocks allow the software to be utilized in a number of configurations (by simply altering the configuration parameters of the software). The software is being designed so that multiple instances of a building block can be deployed by simply "configuring" the building block of operation within a specific agency. Acceptance: All building block instances differentiate only by config file/environment variable—no recompilation needed. Owner: Team-DevOps; Next action: Document acceptance/test for configuration-driven deployment model.

**Architectural Impact:**  
Demands a modular, component-based architecture (Microkernel). Configuration must be externalized (config files/parameters) rather than hard-coded. Supports multi-instance deployment.

**Quality Attributes Affected:**  
Modifiability, Deployability, Reusability

**Architectural Constraints:**  
Software components must be stateless or configuration-driven. Deployment mechanism must support instance differentiation via config. No recompilation needed for agency-specific deployment.

**Rationale:**  
Enables cost-effective extension and reuse across agencies. Directly supports the "building block" design strategy and multi-instance deployment.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008 (Operational Modes)
- **Conflicts with:** None
---

[ASR-005]: Legacy Platform and Technology Stack
**Description**: Derived from ASR-005. The Center-to-Center Server shall execute in a Microsoft Windows NT environment. The Center-to-Center shall be implemented in the C/C++ programming language. The web server application shall use ESRI's ARC Internet Map Server (ARC IMS) product... The Incident GUI shall be implemented using C/C++ and ESRI Map Objects. Legacy system operation is permitted only with approved security waiver and enumerated mitigation plan; otherwise, migration to a supported OS is required within 12 months. A platform security waiver and legacy risk mitigation plan must be approved by TxDOT IT Security; plan must address lack of OS vendor support, propose full migration schedule to supported OS within 12 months. Operation on Windows NT requires: (1) signed security waiver by TxDOT IT Security, (2) deployment of proxy/gateway enforcing TLS 1.2+ and NIST password policies, and (3) approved migration plan within 12 months. Operation on Windows NT is permitted only with a signed risk waiver, proxy-controlled external interface enforcing TLS 1.2+, and published migration roadmap to a vendor-supported OS within 12 months; see NIST 800-53/TxDOT IT policy. Owner: Security Team; Next action: Security Team to prepare formal risk waiver and documented migration plan.

**Architectural Impact:**  
Locks the technology stack to legacy standards (Windows NT, C/C++, ESRI ARC IMS). Requires specific runtime libraries (DATEX/ASN, ESRI). Impacts security posture (Windows NT EOL) and modernization strategy. Requires explicit security and support exception process.

**Quality Attributes Affected:**  
Portability, Security, Maintainability

**Architectural Constraints:**  
Must run on Windows NT (with waiver). Must use C/C++. Must integrate with ESRI ARC IMS/Map Objects. Migration to supported OS required within 12 months if waiver not granted. Requires proxy/gateway for TLS 1.2+ enforcement. Signed risk waiver required.

**Rationale:**  
High risk due to legacy constraints (Windows NT EOL). Conflicts with modern security/supportability. Requires explicit legacy exception policy and migration plan as per reference knowledge.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Web Map), FR-006 (Remote GUI)
- **Conflicts with:** NFR-002 (Security - Legacy OS limitations), ASR-006 (Public Network Security)
---

[ASR-006]: Public Network Security for Command Control
**Description**: Derived from ASR-006. The remote Center Control GUI shall be designed to execute on a public network (e.g., Internet) and transmit equipment requests to the C-2-C software system. To support device control... including username and Password. If legacy Windows NT does not support modern TLS, all remote access must be via proxied/segregated network boundary with modern appliance enforcing TLS 1.2+. If Windows NT cannot host modern encryption, a secure front-end (VPN or proxy with TLS 1.2+) must terminate all public commands and segment legacy hosts. All public control traffic must terminate at a modern, supported security gateway appliance enforcing TLS 1.2+ and RBAC, with backend host network-segmented and not directly exposed. Acceptance: 100% of public network device control traffic terminates at FIPS 140-2 compliant TLS 1.2+ gateway, with complete audit log and quarterly pen test. Owner: Security Team; Next action: Document and implement gateway/proxy architecture, validate in penetration testing.

**Architectural Impact:**  
Requires a Security Gateway or API Gateway to enforce TLS/mTLS for public network traffic. Necessitates RBAC for command issuance. Requires audit logging with secret redaction (passwords must not be logged). Requires compensating controls (proxy/VPN) if legacy platform lacks encryption support. Mandates secure gateway between public network and legacy host.

**Quality Attributes Affected:**  
Security, Integrity, Confidentiality

**Architectural Constraints:**  
Must enforce encryption (TLS 1.2+) on public interfaces. Must implement authentication/authorization before command execution. Must use proxy/VPN if host OS is incapable. Backend host must be network-segmented and not directly exposed. FIPS 140-2 compliant gateway required. Quarterly pen test required.

**Rationale:**  
High risk (Public network + Device Control). Passwords in command payloads require strict security controls (mTLS, RBAC, redaction) to prevent unauthorized infrastructure control. Documents conflict with legacy platform.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Device Control), FR-006 (Remote GUI), NFR-002 (Security)
- **Conflicts with:** ASR-005 (Legacy Platform may lack modern TLS support)
---