# Architecturally Significant Requirements Results:

[ASR-001]: Distributed System Architecture for Remote Operations
**Description**: All software should be developed to permit remote operations. The remote operations software must be considered from the beginning in the Gemini software design to avoid redesign later. The common layers of software shall cope from the beginning with a distributed environment. Network transport: must support TCP/IP v4/v6, TLS1.2+; min 100 concurrent sessions, average round-trip time per packet <150ms under 95th percentile site link. Minimum baseline protocols (e.g., support TCP/IP v4/v6, TLS1.2+, ISDN fallback) shall be specified; expected request volume patterns for sizing shall be listed. Acceptance: For restricted operation at siteX, submit test control command from forbidden site→NAK; allowed site→ACK. All attempts logged and restriction tested per month. Owner: Security Team; Next action: write restriction config and test cases.

**Architectural Impact:**
- Requires distributed system architecture with client-server or peer-to-peer communication patterns
- Necessitates network abstraction layer that is transparent to local/remote operations
- Impacts all software layers from user interface to IOC control
- Requires WAN-capable communication protocols (TCP/IP, ISDN, Internet)

**Quality Attributes Affected:**
- Performance (network latency impact)
- Security (remote access protection)
- Availability (distributed failure modes)
- Scalability (multiple remote sites)

**Architectural Constraints:**
- Must implement network-transparent communication from initial design
- Requires homogeneous LAN/WAN interfaces based on standards
- Must support dynamic restriction of operations to specific remote sites
- Common software layers must handle distributed environment
- Must support TCP/IP v4/v6, TLS1.2+
- Min 100 concurrent sessions
- Average round-trip time per packet <150ms under 95th percentile site link

**Rationale:**
This is architecturally significant because it fundamentally shapes the entire system architecture. Building remote operations capability from the beginning versus retrofitting later represents a major architectural decision with significant cost and risk implications. It affects communication patterns, security architecture, and all software layers.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-001, NFR-006
- **Conflicts with:** None
---

[ASR-002]: Multi-Instrument Parallel Access Architecture
**Description**: Parallel access to all mounted instruments shall be provided, though only one instrument has access to the telescope beam. Inactive instruments shall be able to take calibration exposures in parallel, prepare for exposure in hot standby, and work at all operation levels without adversely impacting the active instrument.

**Architectural Impact:**
- Requires instrument management subsystem with resource allocation and arbitration
- Necessitates isolation mechanisms between active and inactive instruments
- Impacts command routing and resource locking architecture
- Requires concurrent operation support in control software

**Quality Attributes Affected:**
- Performance (parallel operation efficiency)
- Reliability (isolation of failures)
- Safety (beam access control)

**Architectural Constraints:**
- Must implement instrument resource allocation system
- Requires isolation between active and inactive instrument operations
- Must support hot standby mode for inactive instruments
- Cannot allow inactive instrument actions to impact active instrument

**Rationale:**
This is architecturally significant because it requires careful design of resource management, concurrency control, and isolation mechanisms. The multi-instrument context is fundamental to Gemini's operation and affects core control architecture decisions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, NFR-018
- **Conflicts with:** None
---

[ASR-003]: Standardized Interface Architecture for Instruments
**Description**: The Gemini Telescopes view all instruments as operating as servers, responding to commands from upper levels. Visitor instruments must be capable of operating in this mode. The visitor instrument interface must be stable and long-lived (1-2 years between uses). Acceptance: Visitor instrument interface spec (OpenAPI) published w/ version in repo; compatibility suite runs before each change; schema review per release cycle. Owner: API Owner; Next action: create/publish interface schema and review cadence.

**Architectural Impact:**
- Requires server-based instrument control architecture
- Necessitates stable, versioned interface contracts for visitor instruments
- Impacts integration strategy for external/visitor instrumentation
- Requires interface subset strategy (subset of Gemini facilities for visitors)

**Quality Attributes Affected:**
- Maintainability (interface stability)
- Interoperability (visitor instrument support)
- Security (access control for external instruments)

**Architectural Constraints:**
- Must implement server-based command/response pattern for all instruments
- Visitor interface must be stable long-term (1-2 years)
- Visitor interface should be subset of existing instrumentation interface
- Cannot require coordinated motions beyond simple raster scans for visitors
- Visitor instrument interface spec (OpenAPI) published with version in repo
- Compatibility suite runs before each change
- Schema review per release cycle

**Rationale:**
This is architecturally significant because it defines the fundamental instrument integration pattern. The server-based architecture with stable interfaces for visitor instruments represents a major architectural decision affecting all instrument control subsystems and external integration.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-008
- **Conflicts with:** None
---

[ASR-004]: Virtual Telescope Simulation Architecture
**Description**: All hardware subsystems must provide a software simulation module that responds in reasonable fashion to commands directed at that hardware. The simulation cannot require any hardware specific to the application. Support of Gemini and visitor instruments would benefit by a Gemini observatory simulator.

**Architectural Impact:**
- Requires simulation layer for all subsystems
- Necessitates hardware abstraction to enable simulation
- Impacts testing and development architecture (can test without hardware)
- Requires virtual telescope environment integration

**Quality Attributes Affected:**
- Maintainability (testing without hardware)
- Portability (hardware-independent simulation)
- Reliability (development and validation)

**Architectural Constraints:**
- Every subsystem must include simulator module
- Simulation must work without hardware-specific requirements
- Must integrate with virtual telescope environment
- Simulation required for science planning, maintenance, and testing

**Rationale:**
This is architecturally significant because it requires building simulation capability into every subsystem from the beginning. This affects subsystem design patterns, testing architecture, and enables hardware-independent development - a major architectural commitment.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, NFR-017
- **Conflicts with:** None
---

[ASR-005]: Hierarchical Logging and Event Architecture
**Description**: System logging information must include all important events with timestamps. Engineering data logging at up to 200 Hz for short periods. Long-term logging at 1 Hz or less into common format (SYBASE). Errors and alarms must be distinguished with appropriate tracing to source.

**Architectural Impact:**
- Requires multi-tier logging architecture (high-frequency vs long-term)
- Necessitates time synchronization across distributed system
- Impacts database architecture (relational DBMS for logs)
- Requires event classification system (errors vs alarms)

**Quality Attributes Affected:**
- Reliability (fault tracking)
- Maintainability (debugging support)
- Performance (logging overhead)

**Architectural Constraints:**
- Must support 200 Hz logging for short periods
- Long-term logging must use common format (SYBASE)
- All events must be timestamped and indexed
- Must distinguish between errors (command failures) and alarms (asynchronous failures)

**Rationale:**
This is architecturally significant because logging architecture affects all subsystems and requires careful design for performance (200 Hz logging), storage management, and event correlation across distributed components.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, NFR-012, NFR-013
- **Conflicts with:** None
---

[ASR-006]: Safety-Critical Interlock Architecture
**Description**: Safety protection must be independent of software where implemented. All hazards capable of causing death and/or loss of irreplaceable equipment shall be passively interlocked. All hazards capable of causing injury and/or severe damage shall be actively interlocked. Interlock must not depend on any software for reliable operation.

**Architectural Impact:**
- Requires hardware-based safety interlock system separate from control software
- Necessitates safety monitoring architecture with independent failure detection
- Impacts system shutdown and safe state architecture
- Requires multi-layer safety (mechanical, electrical, software)

**Quality Attributes Affected:**
- Safety (primary concern)
- Reliability (independent failure modes)
- Availability (safe state transitions)

**Architectural Constraints:**
- Critical hazards must have software-independent interlocks
- Must implement passive interlocks for death/irreplaceable equipment hazards
- Must implement active interlocks for injury/severe damage hazards
- System must bring to safe state upon danger detection

**Rationale:**
This is architecturally significant because safety requirements mandate hardware-software separation for critical interlocks. This fundamentally affects system architecture, requiring independent safety monitoring and control paths that cannot rely on software alone.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, NFR-007
- **Conflicts with:** None
---

[ASR-007]: Distributed Database Architecture
**Description**: Telescope and instrument parameters are distributed in databases across the IOCs. The internal (within IOC) implementation must be based on EPICS. Implementation within host workstation is TBD. Database must support remote access and distributed data with 2-3 msec access times. Action: Host database implementation (e.g. PostgreSQL) must be selected by design freeze date D; interface schema published N days prior. Owner: Architect; Next action: assign owner/timeline for host DB tech/contract.

**Architectural Impact:**
- Requires distributed database architecture across IOCs and workstations
- Necessitates EPICS for IOC-level data management
- Impacts data consistency and synchronization strategies
- Requires performance optimization for 2-3 msec access times

**Quality Attributes Affected:**
- Performance (access time requirements)
- Reliability (distributed data consistency)
- Maintainability (table-driven applications)

**Architectural Constraints:**
- IOC database implementation must use EPICS
- Must support 2-3 msec access times
- Must support remote access and distributed data
- Must support asynchronous writes for concurrent operation
- Host database implementation (e.g. PostgreSQL) must be selected by design freeze date D
- Interface schema published N days prior

**Rationale:**
This is architecturally significant because database architecture affects all control operations, parameter management, and system configuration. The EPICS requirement for IOCs and distributed data support represents major technology and design decisions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, NFR-002
- **Conflicts with:** None
---

[ASR-008]: Modular Subsystem Architecture with Defined Interfaces
**Description**: The software must be strictly modular - functionality of a subsystem should correspond to that which belongs to that subsystem only. No module can rely upon information outside of its defined interface. Each module's environment is strictly defined by its interface to other components. Acceptance: Each installed module presents API schema, and automated test/linter assures no dependency on internals of other modules. Explicit module interface contracts, code scanning for cross-module reference violations, and interface spec acceptance shall be mandated. Acceptance: All modules publish interface definition (OpenAPI spec), ABI/API checks run at build and test in CI/CD. Interface declaration in defined IDL or OpenAPI format shall be mandated; ABI/API compatibility check shall be automated as part of CI. Acceptance: All modules checked by 'interface-lint' in CI/CD for API/ABI contract correctness and cross-module reference scan. Owner: Dev Lead; Next action: define interface/contract CI pipeline and lint criteria.

**Quality Attributes Affected:**
- Maintainability (independent subsystem maintenance)
- Reliability (no undesired interactions)
- Portability (module independence)

**Architectural Constraints:**
- Modules must not rely on information outside defined interfaces
- Subsystems must be installable and maintainable independently
- Must prevent undesired interactions between subsystems
- Interface size between modules must be minimized
- Each installed module must present API schema
- Automated test/linter must assure no dependency on internals of other modules
- All modules must publish interface definition (OpenAPI spec)
- ABI/API checks must run at build and test in CI/CD
- All modules checked by 'interface-lint' in CI/CD for API/ABI contract correctness and cross-module reference scan

**Rationale:**
This is architecturally significant because it defines the fundamental decomposition strategy for the entire system. Strict modularity with defined interfaces affects all architectural decisions, integration patterns, and maintenance strategies.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-008, NFR-018
- **Conflicts with:** None
---

[ASR-009]: Real-Time Control at IOC Level
**Description**: Strict real-time control is restricted to the IOC layer. Real-time support is required at the IOC level. The upper levels (User-interface and OCS) are assumed to not require a real-time operating environment but must provide sufficient performance for human interaction and communications.

**Architectural Impact:**
- Requires real-time operating environment at IOC layer
- Necessitates separation between real-time and non-real-time components
- Impacts communication architecture between IOC and upper levels
- Requires performance guarantees for IOC operations

**Quality Attributes Affected:**
- Performance (real-time deadlines)
- Reliability (deterministic IOC behavior)
- Safety (time-critical control)

**Architectural Constraints:**
- IOC layer must have real-time operating environment
- Upper levels (UI, OCS) do not require real-time OS
- Must separate real-time from non-real-time processing
- IOC must meet timing requirements for hardware control

**Rationale:**
This is architecturally significant because it defines the real-time boundary in the system architecture. This affects technology selection (RTOS for IOCs), component placement, and communication patterns between real-time and non-real-time components.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002, NFR-009
- **Conflicts with:** None
---

[ASR-010]: Network Architecture with Redundancy and Hierarchy
**Description**: The LAN shall be supplemented with Local Time Bus, digital reflective memory bus, and analog event-based bus. Network redundancy should be considered for reliability and security. A clear hierarchical model must be implemented supporting separation of logical and physical layers (ISO/OSI model).

**Architectural Impact:**
- Requires multi-bus network architecture (LAN + Time Bus + Memory Bus + Event Bus)
- Necessitates hierarchical network model (ISO/OSI)
- Impacts communication protocol selection
- Requires redundancy design for control information

**Quality Attributes Affected:**
- Reliability (network redundancy)
- Performance (specialized buses for timing/events)
- Security (network isolation)

**Architectural Constraints:**
- Must implement LAN plus specialized buses (Time, Memory, Event)
- Must follow hierarchical network model (ISO/OSI)
- Must consider network redundancy for control information
- LAN/WAN interfaces must be homogeneous and standards-based

**Rationale:**
This is architecturally significant because network architecture affects all communication in the distributed system. The multi-bus approach with hierarchical model and redundancy requirements represents major infrastructure decisions affecting reliability, performance, and maintainability.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003, NFR-006
- **Conflicts with:** None
---