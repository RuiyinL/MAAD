# Architecturally Significant Requirements Results:

[ASR-001]: Service Oriented Architecture (SOA)
**Description**: The CCTNS system should be implemented using Service Oriented Architecture (SOA) and have a modular design. The functional architecture is composed of 4 major components based on SOA principles. Each of the components contains multiple services as defined by Service Definition.

**Architectural Impact:**  
- Requires service-based component decomposition
- Necessitates service registry/discovery mechanisms
- Demands standardized service interfaces and contracts
- Influences technology selection toward SOA-compatible frameworks
- Affects deployment and scaling strategies

**Quality Attributes Affected:**  
Scalability, Modifiability, Interoperability, Maintainability

**Architectural Constraints:**  
- Must implement SOA principles
- Four major component architecture
- Service-based communication patterns
- Modular design with clear service boundaries

**Rationale:**  
This requirement fundamentally shapes the entire system architecture, affecting component design, communication patterns, technology choices, and deployment strategies. SOA introduces significant architectural complexity but enables modularity and scalability.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[ASR-002]: Unalterable Audit Trail Architecture
**Description**: The CCTNS system must keep an unalterable audit trail capable of automatically capturing and storing information about all the actions (create/read/update/delete) that are taken upon the critical entities in the CCTNS system. The word "unalterable" is to mean that the audit trail data cannot be modified in any way or deleted by any user. Once the audit trail functionality has been activated, the CCTNS system must track events without manual intervention. Each audit record is signed with previous hash, and log export includes cryptographic verification metadata. Retained 7 years after case closure.

**Architectural Impact:**  
- Requires append-only logging architecture
- Necessitates cryptographic integrity mechanisms (hash chains, digital signatures)
- Demands separate audit storage from operational data
- Requires tamper-evident storage solutions
- Influences database design (cannot use soft deletes for audit records)

**Quality Attributes Affected:**  
Security, Compliance, Data Integrity, Reliability

**Architectural Constraints:**  
- Append-only audit log storage
- Cryptographic integrity verification (hash chain)
- Automatic capture without manual intervention
- Separate audit trail storage from operational data
- Cannot modify or delete audit records
- 7-year retention post-case closure

**Rationale:**  
This is a high-risk, compliance-critical requirement that significantly impacts data architecture, storage design, and security mechanisms. Legal admissibility of evidence depends on this capability, making it architecturally significant.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013, FR-014 (Audit Trail Capture)
- **Conflicts with:** None identified
---

[ASR-003]: Centralized 3-Tier Deployment Architecture
**Description**: The CCTNS system should be developed for a centralized deployment and maintenance. The CCTNS system should be developed to be deployed in a 3-tier datacenter architecture. The CCTNS system should be designed to have a n-tier architecture with the presentation logic separated from the business logic that is again separated from the data-access logic. If offline required, CCTNS client logic must persist all in-flight registration & search data locally, with encrypted sync guaranteed within 30m reconnection window; otherwise, all operations must require central connection.

**Architectural Impact:**  
- Requires physical separation of presentation, business, and data tiers
- Demands centralized infrastructure at state level
- Influences network architecture and connectivity requirements
- Affects disaster recovery and backup strategies
- Requires load balancing and clustering for scalability
- Requires local persistence layer for offline-capable clients

**Quality Attributes Affected:**  
Scalability, Maintainability, Availability, Security

**Architectural Constraints:**  
- 3-tier datacenter architecture mandatory
- Centralized deployment at state level
- Clear separation: presentation logic, business logic, data-access logic
- State-level configuration and customization
- Local encrypted cache for offline operations with 30-minute sync window

**Rationale:**  
This requirement dictates the physical and logical deployment architecture, affecting infrastructure costs, network design, maintenance procedures, and scalability approaches. It represents a major architectural commitment. Reconciled with NFR-010 to support offline operations via local persistence.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** NFR-010 (Offline Operation - reconciled via local persistence with encrypted sync)
---

[ASR-004]: Browser-Based Access with Minimal Client Requirements
**Description**: The CCTNS system should be designed for access through browser-based systems and must impose minimal requirements on the client device.

**Architectural Impact:**  
- Requires web-based presentation layer
- Limits client-side processing and storage
- Demands server-side rendering or thin-client architecture
- Influences technology choices (HTML5, JavaScript frameworks)
- Affects offline capability design

**Quality Attributes Affected:**  
Portability, Usability, Maintainability

**Architectural Constraints:**  
- Browser-based access only
- Minimal client device requirements
- Web technology stack required
- Server-side processing emphasis

**Rationale:**  
This requirement constrains the presentation architecture significantly, affecting technology choices, user experience design, and offline capability. It impacts all user-facing components.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-014 (Browser Compatibility), NFR-028 (Minimal Client Requirements)
- **Conflicts with:** NFR-010 (Offline Operation - browser limitations)
---

[ASR-005]: Multi-Channel Communication Services
**Description**: The CCTNS system must support multiple types of communication services for remote access. The solution should send alerts (e.g., email, SMS) to the user if the user chooses to whenever any action has been taken on the alert.

**Architectural Impact:**  
- Requires messaging/integration layer for multiple channels
- Demands email and SMS gateway integrations
- Influences notification architecture design
- Requires async communication patterns
- Affects reliability and delivery guarantee mechanisms

**Quality Attributes Affected:**  
Interoperability, Reliability, Usability

**Architectural Constraints:**  
- Multiple communication channel support (email, SMS, etc.)
- Gateway integration required
- Async notification architecture
- Delivery tracking capability

**Rationale:**  
This requirement introduces integration complexity with external systems (email servers, SMS gateways) and affects the overall communication architecture. It impacts reliability and delivery guarantee strategies.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010 (Alert Notification System)
- **Conflicts with:** None identified
---

[ASR-006]: Role-Based Access Control (RBAC) Architecture
**Description**: The CCTNS system should provide for role-based control for the functionality within the CCTNS system. The CCTNS system must allow a user to be a member of more than one group. The CCTNS system must allow only admin-users to set up user profiles and allocate users to groups.

**Architectural Impact:**  
- Requires centralized authentication/authorization service
- Demands RBAC model implementation across all components
- Influences database design for user/group/role relationships
- Affects all service interfaces (authentication required)
- Requires session management architecture

**Quality Attributes Affected:**  
Security, Maintainability, Scalability

**Architectural Constraints:**  
- RBAC model mandatory
- Multi-group membership support
- Admin-only user management
- Common User Access and Authentication Service (Single Sign-On)

**Rationale:**  
This is a cross-cutting concern that affects every component and service. Security architecture depends on this, and it impacts user experience, database design, and service communication patterns.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, FR-017, FR-018, FR-019 (Access Control Functions)
- **Conflicts with:** None identified
---

[ASR-007]: Hierarchical Caching Strategy
**Description**: A hierarchical cache should be configured and used for caching of results of most frequently used searches. The CCTNS system should ensure high scalability and performance through using of cache for storing frequent data.

**Architectural Impact:**  
- Requires cache layer in architecture (e.g., Redis, Memcached)
- Demands cache invalidation strategy
- Affects data consistency design
- Influences performance optimization approach
- Requires cache coherence mechanisms

**Quality Attributes Affected:**  
Performance, Scalability

**Architectural Constraints:**  
- Hierarchical cache implementation required
- Cache frequent search results
- Cache invalidation strategy needed
- Must support NFR-003, NFR-004 performance requirements

**Rationale:**  
This requirement is critical for meeting performance SLAs. Cache architecture decisions affect data consistency, scalability approach, and infrastructure requirements. Trade-offs between performance and consistency must be managed.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002, NFR-003, NFR-004 (Performance Requirements)
- **Conflicts with:** None identified
---

[ASR-008]: Search Optimization Architecture
**Description**: Database Indexes should be applied on the key columns used for searching. The search results should be fetched from the database in batches of 10 or 20 maximum as configured within the application. The search should fetch only the fields that need to be displayed to the user. Only when the user clicks on a particular record to view its further details should a query be fired to fetch the additional details for this particular record only. GET /cases?limit=20&offset=0, returns {results:[], total:int, has_more:bool}.

**Architectural Impact:**  
- Requires database indexing strategy
- Demands pagination implementation at data layer
- Influences query optimization approach
- Requires lazy-loading pattern for details
- Affects API design (list vs. detail endpoints)

**Quality Attributes Affected:**  
Performance, Scalability

**Architectural Constraints:**  
- Database indexing on search columns mandatory
- Batch/paged retrieval (10-20 records max)
- Lazy-loading for record details
- Field-level query optimization
- REST API contract: limit/offset pagination with total count

**Rationale:**  
This requirement directly addresses performance SLAs for search operations. It affects database design, API architecture, and data retrieval patterns. Critical for scalability with large case volumes.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002 (Search Performance)
- **Conflicts with:** None identified
---

[ASR-009]: Multi-Tier Authentication and Security
**Description**: The CCTNS system should support multi-tier authentication where required. The CCTNS system should be built on a common User Access and Authentication Service to ensure Single-Sign on for the end-user.

**Architectural Impact:**  
- Requires centralized authentication service
- Demands SSO implementation (e.g., SAML, OAuth)
- Influences session management architecture
- Affects all service-to-service communication
- Requires security token/certificate management

**Quality Attributes Affected:**  
Security, Usability, Maintainability

**Architectural Constraints:**  
- Common authentication service mandatory
- Single Sign-On required
- Multi-tier authentication support
- Security token management

**Rationale:**  
Security architecture depends on this requirement. It affects user experience, service communication patterns, and infrastructure design. Single point of authentication is a critical architectural decision.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (RBAC Architecture), NFR-015, NFR-020 (Security)
- **Conflicts with:** None identified
---

[ASR-010]: Scalability and Performance Design Patterns
**Description**: The CCTNS system should ensure high scalability and performance through using of AJAX based technology to improve user experience, leveraging Asynchronous HTTP socket capabilities of web server for scalability and performance, hosting all the static content (documents, images) on the web server, and displaying of records on the screen in batches/paged manner.

**Architectural Impact:**  
- Requires AJAX-enabled frontend framework
- Demands asynchronous communication patterns
- Influences web server selection and configuration
- Requires static content delivery strategy (CDN or web server)
- Affects frontend-backend interaction design

**Quality Attributes Affected:**  
Performance, Scalability, Usability

**Architectural Constraints:**  
- AJAX-based technology required
- Asynchronous HTTP capabilities
- Static content on web server
- Paged display implementation

**Rationale:**  
This requirement dictates frontend architecture and communication patterns. It affects technology selection, user experience design, and server infrastructure requirements.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002, NFR-003, NFR-004 (Performance Requirements)
- **Conflicts with:** None identified
---

[ASR-011]: Security Architecture - Input Validation and Protection
**Description**: The CCTNS system should ensure high standards of security and access control through preventing cross-site scripting, preventing SQL Injection, utilizing parameterized queries, sanitizing the user-inputs, validating the incoming data or user request, validating the data both at the client and server, and encoding the incoming data or user request.

**Architectural Impact:**  
- Requires security middleware/filters at all tiers
- Demands parameterized query enforcement at data layer
- Influences framework selection (security features)
- Requires centralized input validation layer
- Affects all data entry points

**Quality Attributes Affected:**  
Security, Reliability

**Architectural Constraints:**  
- Parameterized queries mandatory
- Client and server-side validation
- XSS and SQL Injection prevention
- Input sanitization at all entry points
- Data encoding required

**Rationale:**  
Security is a cross-cutting concern affecting all components. This requirement mandates specific security patterns and technologies throughout the architecture. Critical for system integrity and compliance.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-015, NFR-016, NFR-017, NFR-018 (Security Requirements)
- **Conflicts with:** None identified
---

[ASR-012]: Open Standards and Technology Constraints
**Description**: The CCTNS system should be developed on Open Standards. The proposed functional architecture is modeled around centralized deployment to facilitate ease of maintenance and leverage advancement in open standards and web technologies. The CCTNS system should adopt standardized formats and common metadata elements.

**Architectural Impact:**  
- Requires open standard protocols (HTTP, HTTPS, XML/JSON, etc.)
- Influences technology selection (open source preferred)
- Demands standardized data formats
- Affects vendor lock-in considerations
- Requires standards compliance verification

**Quality Attributes Affected:**  
Interoperability, Maintainability, Portability

**Architectural Constraints:**  
- Open standards mandatory
- Standardized formats required
- Common metadata elements
- Web technology stack

**Rationale:**  
This requirement constrains technology choices and affects long-term maintainability and vendor independence. It impacts integration strategies and technology roadmap decisions.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[ASR-013]: Mobile and PDA Extensibility
**Description**: The CCTNS system should be extensible to provide access to the interfaces through PDA's and mobile data terminals.

**Architectural Impact:**  
- Requires responsive design architecture
- Demands mobile-optimized API design
- Influences screen layout strategy
- Affects offline synchronization design
- Requires mobile device considerations in security

**Quality Attributes Affected:**  
Portability, Usability, Scalability

**Architectural Constraints:**  
- Mobile device support required
- PDA compatibility needed
- Responsive design implementation
- Mobile-optimized interfaces

**Rationale:**  
This requirement affects presentation architecture and API design. It introduces mobile-specific considerations for security, performance, and user experience that must be addressed in the base architecture.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Browser-based Access)
- **Conflicts with:** None identified
---

[ASR-014]: Core-Configuration-Customization (3C) Architecture
**Description**: The 3 C's (Core-Configuration-Customization) forms the guiding principle for the architecture. The core services, support layer and security and access control components can be deployed as standard components with necessary configuration changes. The customization layer can override and add to the core services based on the specific state requirements and can be plugged with the core services. The deployment of the application will be at state level and will be configured and customized as per the state specific extensions.

**Architectural Impact:**  
- Requires layered architecture with clear separation
- Demands plugin/extension mechanism
- Influences configuration management design
- Affects deployment and versioning strategy
- Requires configuration vs. customization boundaries

**Quality Attributes Affected:**  
Modifiability, Maintainability, Scalability

**Architectural Constraints:**  
- 3-layer architecture (Core, Configuration, Customization)
- Plugin-based customization mechanism
- State-level deployment
- Configurable core components

**Rationale:**  
This is a fundamental architectural principle that affects component design, deployment strategy, and maintenance approach. It enables multi-state deployment with customization while maintaining upgradability.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (SOA Architecture), ASR-003 (Centralized Deployment)
- **Conflicts with:** None identified
---