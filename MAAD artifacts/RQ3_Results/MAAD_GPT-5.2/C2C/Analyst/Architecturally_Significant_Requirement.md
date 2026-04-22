# Architecturally Significant Requirements Results

[ASR-001]: Interconnect dissimilar traffic management systems via interfaces/adapters
**Description**: “The Center-to-Center infrastructure must interconnect several dissimilar traffic management systems. In order to create the Center-to-Center infrastructure, interfaces to the existing systems will be created. The data from these interfaces will communicate with the existing system in a ‘system specific’ format.” Updated per evaluator: All new system adapters must implement the IExternalTrafficSystemAdapter interface defined in [InterfaceSpec-v1], mapping legacy fields to TMDD/ITS canonical types. [Next action: Produce interface contract stub/template per integration.]
  
**Architectural Impact:**  
Drives an integration architecture with adapter/translator components per legacy system, clear boundary contracts, and a broker/canonical model to normalize “system specific” formats into shared representations.

**Quality Attributes Affected:** Interoperability, Maintainability, Modifiability

**Architectural Constraints:** Must support multiple heterogeneous external systems; must include interface components that handle system-specific formats.

**Rationale:** High architectural impact due to cross-system integration and ongoing evolution of multiple external dependencies.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002, NFR-003
- **Conflicts with:** NFR-012
---

[ASR-002]: Standards-based “cloud” canonical data exchange with project-defined protocol at boundary
**Description**: “Any data that is passed into the ‘cloud’… will be based on the ITS standards. Systems will interface to the ‘cloud’ using a project defined protocol. New systems that are deployed (based on the ITS standards) will not utilize the project defined protocol but will be moved ‘into’ the cloud…”
  
**Architectural Impact:**  
Requires a canonical “inside-the-cloud” data model (ITS/TMDD) and a boundary protocol layer for legacy systems; implies dual-path integration (legacy via project protocol vs native ITS systems).

**Quality Attributes Affected:** Interoperability, Evolvability, Maintainability

**Architectural Constraints:** Internal exchange must be ITS-standards-based; boundary must support a project-defined protocol for non-ITS systems.

**Rationale:** Establishes core architectural separation between canonical domain and edge integration, affecting all interfaces and data flows.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, NFR-001
- **Conflicts with:** NFR-002
---

[ASR-003]: Repository-centric architecture with multi-source ingest into a single datastore
**Description**: “This Center-to-Center infrastructure implements a repository for traffic data…” and “In this mode the Center-to-Center receives data from all connected systems, including the Incident GUI, and combines the data into a single data store (database).” Updated per evaluator: The central traffic repository shall be relational (PostgreSQL/MySQL); schema must include TMDD canonical fields, indexed by network_id, device_id, timestamp. [Next action: Produce draft schema and performance load estimation.]
  
**Architectural Impact:**  
Forces a central data store (schema, indexing, concurrency, ingest pipelines) and integration patterns for multiple producers/consumers; impacts data consistency, synchronization, and query patterns.

**Quality Attributes Affected:** Scalability, Performance, Reliability, Maintainability

**Architectural Constraints:** Must include a shared repository/database; must support ingest from multiple connected systems.

**Rationale:** Central repository is a primary architectural driver and a potential bottleneck/high-risk component.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-038, FR-071
- **Conflicts with:** NFR-011
---

[ASR-004]: Protocol stack constraint: TMDD over DATEX/ASN over TCP/IP
**Description**: “The Center-to-Center Project shall utilize the TMDD standard (including message sets) to transmit information. DATEX/ASN shall be used to transmit the TMDD message sets. TCP/IP shall be used to transmit the DATEX/ASN data.”
  
**Architectural Impact:**  
Constrains communication layers, serialization/encoding, runtime libraries, and interface components; impacts error handling, versioning, and interoperability testing.

**Quality Attributes Affected:** Interoperability, Portability (constraint), Maintainability

**Architectural Constraints:** Must implement the specified protocol layering and associated runtime dependencies.

**Rationale:** Strong technology/protocol constraint that shapes integration, libraries, and deployment topology.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002, NFR-003, NFR-013
- **Conflicts with:** NFR-009
---

[ASR-005]: Configurable building-block deployment with multi-instance reuse
**Description**: “The Center-to-Center infrastructure is being created using a series of building blocks. These building blocks allow the software to be utilized in a number of configurations (by simply altering the configuration parameters of the software). The software is being designed so that multiple instances of a building block can be deployed by simply ‘configuring’ the building block…”
  
**Architectural Impact:**  
Requires modular componentization, configuration-driven behavior, instance isolation, and deployment descriptors; suggests plug-in/microkernel or component framework.

**Quality Attributes Affected:** Modifiability, Reusability, Deployability

**Architectural Constraints:** Must support multiple deployable instances of components via configuration parameters (not code changes).

**Rationale:** Cross-cutting structural requirement affecting packaging, configuration management, and runtime composition.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008
- **Conflicts with:** NFR-012
---

[ASR-006]: Hierarchical linking of repositories (local → regional → statewide)
**Description**: “This would allow a ‘local’ common repository to be created by ‘linking’ individual partners, a ‘regional’ common repository to be created by ‘linking’ local common repositories and a ‘statewide’ common repository to be created by ‘linking’ regional common repositories.” Updated per evaluator: Regional repo must sync to parent every 10 min, batch size 1000, with last-write-wins timestamp rule and audit log. [Next action: Detail repo replication/sync protocol.]
  
**Architectural Impact:**  
Introduces federation/replication or synchronization across tiers; impacts data governance, conflict resolution, latency, and network topology.

**Quality Attributes Affected:** Scalability, Availability, Interoperability, Maintainability

**Architectural Constraints:** Must support linking repositories across multiple aggregation levels.

**Rationale:** Major scalability and distribution driver with significant architectural trade-offs.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003, ASR-004
- **Conflicts with:** NFR-011
---

[ASR-007]: Platform and vendor technology constraints (Windows NT + ESRI + C/C++)
**Description**: “The Center-to-Center Server shall execute in a Microsoft Windows NT environment… The web server application shall use ESRI's ARC Internet Map Server (ARC IMS)… The Center-to-Center shall be implemented in the C/C++ programming language… The Incident GUI… C/C++ and ESRI Map Objects… The Remote Control GUI… C/C++ and ESRI Map Objects.” Updated per evaluator: All new deployments must default to Win2019+; legacy support for NT/ESRI by exception only; set roadmap for full phaseout. [Next action: Hold architecture/IT standards review to align platform constraints.]
  
**Architectural Impact:**  
Constrains runtime environment, build toolchain, UI/mapping subsystem design, deployment packaging, and integration with ESRI components; limits portability and influences component boundaries (native code, COM/SDK integration patterns).

**Quality Attributes Affected:** Portability (constraint), Maintainability, Deployability

**Architectural Constraints:** Must run on Windows NT; must use ESRI ARC IMS for web map images; must implement in C/C++; GUIs must use ESRI Map Objects.

**Rationale:** Hard technology constraints with broad impact across all layers and components.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-012, NFR-014, NFR-015, NFR-016
- **Conflicts with:** NFR-005
---

[ASR-008]: Remote device control over public networks with authentication fields
**Description**: “The remote Center Control GUI shall be designed to execute on a public network (e.g., Internet) and transmit equipment requests…” and multiple control command requirements include “username and Password.” Updated per evaluator: All credential-related API endpoints must provide automated TLS config proof (config/scan evidence), and annual penetration test demonstrating no credential leakage. [Next action: Specify endpoint compliance evidence package (TLS scan, breach reporting workflow).]
  
**Architectural Impact:**  
Requires end-to-end security architecture (authentication, authorization, secure transport, credential handling), plus audit/logging and command validation; affects all device-control endpoints and UI flows.

**Quality Attributes Affected:** Security, Safety, Reliability

**Architectural Constraints:** Must support authenticated remote command/control over public networks; command messages include credential fields as specified.

**Rationale:** High-risk, cross-cutting security requirement affecting many components and interfaces.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-056, FR-057, NFR-004, NFR-009
- **Conflicts with:** NFR-006
---