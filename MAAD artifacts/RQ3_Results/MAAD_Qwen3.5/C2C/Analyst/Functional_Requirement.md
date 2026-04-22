# Functional Requirements Results:

[FR-001]: Network and Roadway Data Provision
**Description**: For each roadway network it maintains, the Center shall provide the network name and link data information. The Center shall provide the link information, including link identifier, link name and link type. The Center shall provide the node information, including node identifier, node name and node type description.

**Rationale:**  Describes specific data entities and attributes the system must expose to users or connected systems.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Interoperability), ASR-002 (Canonical Data Model)
- **Conflicts with:** None
---

[FR-002a]: Incident Record Management
**Description**: Derived from FR-002. The Center shall support the information about each incident, including network identifier, incident description and roadway. The Center shall support CRUD (Create, Read, Update, Delete) operations for incident records. Incident: {incident_id: UUID, network_id: string, description: string, roadway: string, created_ts: ISO8601 datetime, ...}, all creates/updates fail on missing required fields. Owner: Team-API; Next action: Document and attach incident object contract/schema to FR-002a.

**Rationale:**  Defines atomic behavior for incident data management, separated from lane closure and UI functions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Incident GUI), NFR-003 (Usability)
- **Conflicts with:** None
---

[FR-002b]: Lane Closure Record Management
**Description**: Derived from FR-002. The Center shall support the information about each lane closure, including network identifier, lane closure id, closure description. The Center shall support CRUD (Create, Read, Update, Delete) operations for lane closure records. LaneClosure: {closure_id: UUID, network_id: string, description: string, start_ts: ISO8601, end_ts: ISO8601, ...}. Reject request with HTTP 400 + error message if missing required field. Owner: Team-API; Next action: Document and attach lane closure schema to FR-002b.

**Rationale:**  Defines atomic behavior for lane closure data management, separated from incident and UI functions.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Incident GUI), NFR-003 (Usability)
- **Conflicts with:** None
---

[FR-002c]: Incident and Lane Closure GUI Functions
**Description**: Derived from FR-002. The Incident GUI shall allow the user to enter incident or lane closure information without the use of an Center. The GUI shall allow the data about an incident to be modified. The GUI shall allow a user to delete a previously entered incident or lane closure. The GUI shall provide a list of previously entered incidents and lane closures. GUI: on error, show accessible error message inline; prevent user data loss or commit of invalid record. Acceptance: GUI presents inline error message, ARIA-live alert, and preserves user input on error; verified by accessibility scan. Owner: Team-UX; Next action: Expand FR-002c with GUI error/accessibility acceptance test.

**Rationale:**  Defines UI-specific behaviors for incident and closure management, separated from data logic.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002a (Incident Record), FR-002b (Lane Closure Record)
- **Conflicts with:** None
---

[FR-003]: Field Device Status Monitoring
**Description**: Derived from FR-003. The Center shall provide status information for DMS, LCS, CCTV, Ramp Meter, HAR, Traffic Signal, ESS, HOV, Parking Lot, School Zone, Railroad Crossing, Reversible Lane, Dynamic Lane, Bus Stop/Location, Light/Commuter Stop/Location, Park and Ride Lot, and Vehicle Priority. Information includes identifiers, names, locations, status, and specific attributes. Data contracts shall be defined per device type (e.g., CCTV status response: { network_id: string, cctv_id: string, name: string, location: {lat: float, lon: float}, status: enum['active','inactive','fault'], last_update: ISO8601 }). For each device type, define a status schema including all required fields, units (where applicable), and data types. Owner: Team-API; Next action: Develop and publish API contracts/schemas for all device status types.

**Rationale:**  Describes the system's function to collect and expose status data from a wide variety of traffic management devices with explicit schema contracts.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001 (Heterogeneous System Interconnection), FR-008 (Data Collection), ASR-002 (Canonical Data Model)
- **Conflicts with:** None
---

[FR-004]: Field Device Remote Control
**Description**: Derived from FR-004. To support control in other centers, the Center shall be able to support device control commands for DMS, LCS, CCTV, Ramp Meter, HAR, Traffic Signal, HOV, School Zone, Reversible Lane, and Dynamic Lane. Commands include network identifier, device identifier, username, password, and specific control parameters. Device control command endpoint shall accept JSON body {network_id, device_id, command, username, password}; on auth fail, returns HTTP 401. Encrypted channel required. Precondition of user RBAC check. Add contract definitions for control endpoints: e.g., POST /api/device/control { network_id, device_id, username, password, command: {param1, param2...} }, returns {status, error_message, timestamp}. Schema: {network_id: string, device_id: string, username: string, password: string, command: object, timestamp: ISO8601}. Response: {status: enum, error_message: string, timestamp: ISO8601}. Acceptance: Device control endpoint enforces RBAC, strong password (≥12 chars), and all POST/PUTs over TLS 1.2+. Pen test 2x/year. Owner: Team-API; Next action: Expand FR-004 with explicit security acceptance criteria and test plan; Publish and version API contracts for device control endpoints.

**Rationale:**  Defines the system's ability to issue actionable commands to external devices, requiring authentication parameters, explicit API contracts, and security controls.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Remote Control GUI), NFR-002 (Security), ASR-006 (Public Network Security)
- **Conflicts with:** None
---

[FR-005]: Web Map Visualization
**Description**: Derived from FR-005. The Web Map application generates a map that can be displayed on an Internet WWW server. The map shall display interstates and state highways. The map user shall be able to alter the current magnification (zoom level) and pan the map (North, South, East, West). Each link displayed on the map shall be color coded to provide a graphical depiction of speeds. The map shall display current incidents (as icons) and device status (DMS, LCS, CCTV). Map renders within 2s on supported browsers (>95% browser coverage). Acceptance: Supports 100 concurrent users, ≥1000 simultaneous incident/device icons, renders correctly on latest Chrome/Edge/Firefox and previous two major versions; error banner displayed on fetch/data errors. Acceptance: Automated a11y scan on every release; zero high-severity issues before deploy; all WCAG 2.1 AA violations fixed in 30 days. Owner: Team-UX; Next action: Expand acceptance criteria as above; Add measurable, automatable accessibility testing to FR-005.

**Rationale:**  Describes the visual output and interaction capabilities of the web mapping component with measurable performance criteria.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Technology Stack - ESRI), FR-001 (Network Data), NFR-003 (Usability)
- **Conflicts with:** None
---

[FR-006]: Remote Center Control GUI
**Description**: The remote Center Control GUI shall be designed to execute on a public network and transmit equipment requests to the C-2-C software system. When initiated, the user shall be prompted for User name and Password. The user shall be provided with the capability to select a network identifier, select a device (DMS, LCS, CCTV, etc.), and provide control information. Status returned from the network identifier will be displayed in a scrollable list.

**Rationale:**  Describes the interface and workflow for remote operators to authenticate and control devices.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Device Control), NFR-002 (Security)
- **Conflicts with:** None
---

[FR-007]: Data Collection and Storage
**Description**: The Data Collector shall be designed to support the storage of TMDD data elements and message set information. In normal mode, the Center-to-Center receives data from all connected systems and combines the data into a single data store (database). Storage model: canonical schema for TMDD v3.0, with future extension/migration plan; all tables/fields versioned. Owner: Team-Data; Next action: Provide and version data model/schema for TMDD message/data store.

**Rationale:**  Defines the data ingestion and persistence behavior of the system.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Repository Federation), ASR-002 (Canonical Data Model)
- **Conflicts with:** None
---

[FR-008]: Operational Modes
**Description**: The Center-to-Center shall be able to operate in normal mode (receive data, combine into data store). The Center-to-Center shall be able to operate in test mode (perform normal mode operations and also log activities). Acceptance: Switching between modes is logged and all expected data/logs available within defined SLA. Owner: Team-Ops; Next action: Define operational mode test plan for FR-008.

**Rationale:**  Describes distinct operational states affecting data processing and logging behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Reliability/Audit)
- **Conflicts with:** None
---