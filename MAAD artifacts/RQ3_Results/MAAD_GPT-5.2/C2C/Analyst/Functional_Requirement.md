# Functional Requirements Results

[FR-001]: Provide roadway network metadata and topology
**Description**: “For each roadway network it maintains, the Center shall provide the network name and link data information. The Center shall provide the link information, including link identifier, link name and link type. The Center shall provide the node information, including node identifier, node name and node type description.”
  
**Rationale:** Describes system behavior to expose specific network/link/node data elements.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-002]: Support incident information exchange
**Description**: “The Center shall support the information about each incident, including network identifier, incident description and roadway.”
  
**Rationale:** Defines required data the system must store/exchange for incidents.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-003]: Support lane-closure information exchange
**Description**: “The Center shall support the information about each lane closure, including network identifier, lane closure id, closure description.”
  
**Rationale:** Defines required data the system must store/exchange for lane closures.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-004]: Provide DMS status information
**Description**: “The Center shall provide the following status information about each DMS, including network identifier, DMS identifier, DMS name.”
  
**Rationale:** Requires the system to expose DMS status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-005]: Support remote DMS control commands
**Description**: “To support DMS control in other centers, the Center shall be able to support the following device control command for a DMS, including network identifier, DMS identifier, username and Password.” Updated per evaluator: Example POST /api/dms/command { 'network_id': string, 'dms_id': string, 'username': string, 'password': string, 'command': {...} } [validation: 'password' required, min 12 chars, etc.]. [Next action: Draft and review DMS command schema (attach sample contract, validator).]
  
**Rationale:** Specifies a control function (command handling) and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-006]: Provide LCS status information
**Description**: “The Center shall support the following status information about each LCS, including network identifier, LCS identifier, LCS name, Location and Status.”
  
**Rationale:** Requires the system to expose LCS status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-007]: Support remote LCS control commands
**Description**: “To support LCS control in other centers, the Center shall be able to support the following device control command for a LCS, including network identifier, LCS identifier, username and Password.”
  
**Rationale:** Specifies a control function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-008]: Provide CCTV status information
**Description**: “The Center shall provide the information status information about each CCTV, including network identifier, CCTV identifier, CCTV name, Location and Status.”
  
**Rationale:** Requires the system to expose CCTV status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-009]: Support remote CCTV control requests
**Description**: “To support CCTV control in other centers, the Center shall be able to support the following CCTV control request, including network identifier, CCTV identifier, username, Password.” Updated per evaluator: Draft OpenAPI contract: POST /api/cctv/control {network_id:string, cctv_id:string, username:string, password:string, operation:string, ...} → Response: {status: enum['SUCCESS','FAILED'], error_message?:string}. [Next action: Develop schema/data contract for CCTV control request/response.]
  
**Rationale:** Defines a control request function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-010]: Support CCTV video snapshot status information
**Description**: “To support video snapshots, the Center shall be able to support the status information, including network identifier, CCTV identifier, CCTV name and status.”
  
**Rationale:** Defines a function to provide snapshot-related status data.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-011]: Support remote CCTV switching commands
**Description**: “To support CCTV switching in other centers, the Center shall be able to support the following CCTV switching command, including network identifier, username, Password and video channel input identifier.”
  
**Rationale:** Defines a switching command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-012]: Provide ramp meter status information
**Description**: “The Center shall support the status information about each ramp meter, including network identifier, Ramp Meter identifier, Ramp Meter name, Location and Status.”
  
**Rationale:** Requires the system to expose ramp meter status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-013]: Support remote ramp meter control commands
**Description**: “To support Ramp Meter control in other centers, the Center shall be able to support the following device control command for a ramp meter, including network identifier, Ramp Meter identifier, username, password and plan.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-014]: Provide HAR status information
**Description**: “The Center shall support the following status information about each HAR, including network identifier, HAR identifier, HAR name, location and status.”
  
**Rationale:** Requires the system to expose HAR status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-015]: Support remote HAR control commands
**Description**: “To support HAR control in other centers, the Center shall be able to support the following device control command for a HAR, including network identifier, HAR identifier, username, password and message.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-014, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-016]: Provide traffic signal status information
**Description**: “The Center shall support the following status information about each Traffic Signal, including network identifier,traffic signal identifier, traffic signal name,location and status.”
  
**Rationale:** Requires the system to expose traffic signal status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-017]: Support remote traffic signal control commands
**Description**: “To support Traffic Signal control in other centers, the Center shall be able to support the following device control command for a Traffic Signal, including network identifier, traffic signal identifier, username, password and traffic signal plan identifier.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-018]: Provide ESS status information
**Description**: “The Center shall support the following status information about each ESS, including network identifier, environmental sensor identifier, environment sensor name, type, location and status.”
  
**Rationale:** Requires the system to expose ESS status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-019]: Provide HOV lane status information
**Description**: “The Center shall support the following status information about each HOV, including network identifier, HOV identifier, HOV name, link identifier, status and plan.”
  
**Rationale:** Requires the system to expose HOV status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-020]: Support remote HOV lane control commands
**Description**: “To support HOV Lane control in other centers, the Center shall be able to support the following device control command for a HOV Lane, including network identifier, HOV Lane identifier, username, password and lane plan.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-021]: Provide parking lot status information
**Description**: “The Center shall support the following status information about each Parking Lot, including network identifier, parking lot identifier, parking lot name, location and status.”
  
**Rationale:** Requires the system to expose parking lot status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-022]: Provide school zone status information
**Description**: “The Center shall support the following status information about each School Zone, including network identifier, link identifier, school zone identifier and school zone name.”
  
**Rationale:** Requires the system to expose school zone status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-023]: Support remote school zone control commands
**Description**: “To support School Zone control in other centers, the Center shall be able to support the following device control command for a School Zone, including network identifier, school zone identifier, username, password and plan.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-024]: Provide railroad crossing status information
**Description**: “The Center shall support the following status information about each Railroad Crossing, including network identifier, link identifier, rail crossing identifier, rail crossing name, location and status.”
  
**Rationale:** Requires the system to expose railroad crossing status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-025]: Provide reversible lane status information
**Description**: “The Center shall support the following status information about each Reversible Lane, including network identifier, reversible lane identifier, reversible lane name, link identifier, indicator status and indicator failure state.”
  
**Rationale:** Requires the system to expose reversible lane status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-026]: Support remote reversible lane control commands
**Description**: “To support Reversible Lane control in other centers, the Center shall be able to support the following device control command for a Reversible Lane, including network identifier, reversible lane identifier, username, password, plan and duration.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-025, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-027]: Provide dynamic lane status information
**Description**: “The Center shall support the following status information about each Dynamic Lane, including network identifier, link identifier, dynamic lane identifier, dynamic lane name and failure state.”
  
**Rationale:** Requires the system to expose dynamic lane status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-028]: Support remote dynamic lane control commands
**Description**: “To support Dynamic Lane control in other centers, the Center shall be able to support the following device control command for a Dynamic Lane, including network identifier, dynamic lane identifier, username, password and lane plan.”
  
**Rationale:** Defines a control command function and required inputs.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-027, ASR-001, ASR-002
- **Conflicts with:** NFR-004
---

[FR-029]: Provide bus stop status information
**Description**: “The Center shall support the following status information about each Bus Stop, including network identifier, link identifier, relative link location, name and location.”
  
**Rationale:** Requires the system to expose bus stop status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-030]: Provide bus location status information
**Description**: “The Center shall support the following status information about each Bus Location, including network identifier, link identifier, bus identifier, bus name, location and schedule adherece.”
  
**Rationale:** Requires the system to expose bus location/status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-031]: Provide light/commuter rail stop status information
**Description**: “The Center shall support the following status information about each Light/Commuter Stop, including network identifier, link identifier, commuter or light rail stop identifier, commuter or light rail stop name, location and routes.”
  
**Rationale:** Requires the system to expose rail stop status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-032]: Provide light/commuter rail vehicle location status information
**Description**: “The Center shall support the following status information about each Light/Commuter Location, including network identifier, link identifier, commuter or light rail identifier, commuter or light rail name, location and schedule adherence.”
  
**Rationale:** Requires the system to expose rail vehicle location/status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-033]: Provide park-and-ride lot status information
**Description**: “The Center shall support the following status information about each Park and Ride Lot, including network identifier, park and ride lot identifier, park and ride lot name, location, status and capacity.”
  
**Rationale:** Requires the system to expose park-and-ride status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-034]: Provide vehicle priority status information
**Description**: “The Center shall support the following status information about each Vehicle Priority, including vehicle identifier, network identifier, link identifier and intersection identifier.”
  
**Rationale:** Requires the system to expose vehicle priority status fields.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-035]: Provide aggregated network device status summary
**Description**: “The Center shall support the following information about network device status, including network identifier, number of DMSs, number of LCSs, DMS status data, LCS status data and CCTV status data.”
  
**Rationale:** Defines a function to provide a consolidated device status view.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-006, FR-008, ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-036]: Support device command timeframe request (device type)
**Description**: “The device status requestor and Center shall support the following information for command timeframe request, including network identifier and device type.” Updated per evaluator: Request: {network_id: string, device_type: string}; Response: {network_id: string, device_type: string, days: [string], times: [string]}. [Next action: Attach example data contracts for command timeframe APIs.]
  
**Rationale:** Defines an interaction to request command timeframe parameters.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-037]: Support device command timeframe response (days/times accepted)
**Description**: “The device status requestor and Center shall support the following information for command timeframe request, including network identifier, device type, days commands accepted and times commands accepted.”
  
**Rationale:** Defines required response content for timeframe constraints.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-036, ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-038]: Store TMDD data elements and message set information
**Description**: “The Data Collector shall be designed to support the storage of TMDD data elements and message set information.”
  
**Rationale:** Defines a data storage function for TMDD elements/messages.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-001, ASR-002
- **Conflicts with:** NFR-006
---

[FR-039]: Generate and serve a web map depicting traffic conditions
**Description**: “The Web Map application generates a map that can be displayed on an Internet WWW server. The map provides a graphical depiction of the traffic conditions.” Updated per evaluator: Simulate 100 concurrent users via [tool] on supported browsers; P95 map load time ≤4s from CI/CD pipeline at each build. [Next action: Add loadtest script and build integration.]
  
**Rationale:** Defines a user-facing function to generate and publish map output.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005
- **Conflicts with:** NFR-005
---

[FR-040]: Display interstates and state highways on the map
**Description**: “The map shall display interstates and state highways on the graphical map.”
  
**Rationale:** Defines required map content.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-005
---

[FR-041]: Use NCTCOG GeoData warehouse as basemap source
**Description**: “The basemap data shall be derived from the North Central Texas Council of Governments (NCTCOG) GeoData warehouse.”
  
**Rationale:** Defines a required data source used by the map function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-007
---

[FR-042]: Support map zoom
**Description**: “The map user shall be able to alter the current magnification (zoom level) of the map.”
  
**Rationale:** Defines an interactive map function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-005
---

[FR-043]: Support map panning (N/S/E/W)
**Description**: “The map user shall be able to pan the map in each of the following directions: North, South, East or West.”
  
**Rationale:** Defines an interactive map function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-039
- **Conflicts with:** NFR-005
---

[FR-044]: Color-code links by speed using configurable thresholds
**Description**: “Each link displayed on the map shall be color coded to provide a graphical depiction of speeds. A configuration file shall be provided to specify specific speed values.”
  
**Rationale:** Defines a visualization function and its configuration mechanism.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-039
- **Conflicts with:** NFR-008
---

[FR-045]: Display current incidents as icons and allow drill-down
**Description**: “The map shall display the current incidents (as icons) known to the Center-to-Center Project. The user shall be able to click on an incident icon to obtain further information about the incident.” Updated per evaluator: Drill-down dialog displays {type, description, geo, timestamp, impact} only if session includes 'IncidentViewer' claim; add unit/integration tests covering RBAC path. [Next action: Define and document incident info payload, UI dialog fields, and access roles.]
  
**Rationale:** Defines map overlay behavior and user interaction.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-039
- **Conflicts with:** NFR-005
---

[FR-046]: Display current incidents in a table
**Description**: “All current incidents shall be displayed in tabular format with the following information contained in the table.”
  
**Rationale:** Defines a UI function to present incident data in tabular form.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-039
- **Conflicts with:** NFR-005
---

[FR-047]: Map display capability for DMS/LCS/CCTV
**Description**: “The map shall be capable of displaying the following for a DMS. The map shall be capable of displaying the following for a LCS. The map shall be capable of displaying the following for a CCTV.”
  
**Rationale:** Defines required map overlay capabilities for device types (details not specified in source text).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-006, FR-008, FR-039
- **Conflicts with:** NFR-005
---

[FR-048]: Incident GUI supports entry of incident/lane-closure data without a Center
**Description**: “The Incident GUI shall allow the user to enter incident or lane closure information without the use of an Center.” Updated per evaluator: Incident form: fields and types, required/optional, and corresponding success/failure cases; example: {incident_type: enum, location: {lat,lng}, description: string, timestamp: RFC3339, ...}. [Next action: Define form field spec and validation matrix for incident input form.]
  
**Rationale:** Defines a user function for data entry independent of a center system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003
- **Conflicts with:** NFR-004
---

[FR-049]: Incident GUI supports incident data input
**Description**: “The Incident GUI shall allow the user to input the following information for each incident.”
  
**Rationale:** Defines a data entry function (specific fields not provided in source text).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** NFR-005
---

[FR-050]: Incident GUI supports lane-closure data input
**Description**: “The Incident GUI shall allow the user to input the following information for each lane closure.”
  
**Rationale:** Defines a data entry function (specific fields not provided in source text).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** NFR-005
---

[FR-051]: Incident GUI lists previously entered incidents
**Description**: “The GUI shall provide a list of previously entered incidents.”
  
**Rationale:** Defines a retrieval/display function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-049
- **Conflicts with:** NFR-005
---

[FR-052]: Incident GUI allows modification of incident data
**Description**: “The GUI shall allow the data about an incident to be modified.”
  
**Rationale:** Defines an update/edit function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** NFR-004
---

[FR-053]: Incident GUI allows deletion of incidents
**Description**: “The GUI shall allow a user to delete a previously entered incident.” Updated per evaluator: Acceptance: Attempted delete by non-'IncidentAdmin': access denied; attempted delete by 'IncidentAdmin': allowed, and audit log entry created with user_id, deleted_id, and timestamp. [Next action: Define/attach incident deletion authorization and audit requirements.]
  
**Rationale:** Defines a delete function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** NFR-004
---

[FR-054]: Incident GUI lists previously entered lane closures
**Description**: “The GUI shall provide a list of previously entered lane closures.”
  
**Rationale:** Defines a retrieval/display function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-050
- **Conflicts with:** NFR-005
---

[FR-055]: Incident GUI allows deletion of lane closures
**Description**: “The GUI shall allow a user to delete a previously entered lane closure.”
  
**Rationale:** Defines a delete function.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-054
- **Conflicts with:** NFR-004
---

[FR-056]: Remote Center Control GUI transmits equipment requests over a public network
**Description**: “The remote Center Control GUI shall be designed to execute on a public network (e.g., Internet) and transmit equipment requests to the C-2-C software system.”
  
**Rationale:** Defines a remote-control function and its operational context (public network).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-057, NFR-004, ASR-004
- **Conflicts with:** NFR-009
---

[FR-057]: Remote Control GUI prompts for username/password at startup
**Description**: “When the GUI application is initiated, the user shall be prompted for the following information, including User name and Password.” Updated per evaluator: GUI login must only occur over HTTPS/TLS-secured channels. [Next action: Update UI auth flow to enforce encrypted transport.]
  
**Rationale:** Defines an authentication-related UI behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** NFR-005
---

[FR-058]: Remote Control GUI allows selection of network identifier for device requests
**Description**: “The user shall be provided with the capability to select a network identifier for a device command/control request.”
  
**Rationale:** Defines a user function to scope commands to a network.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-056
- **Conflicts with:** NFR-005
---

[FR-059]: Remote Control GUI supports DMS command entry
**Description**: “Once an Center is selected, the user shall be able to select a DMS from a list and provide the following information, including Target DMS, Message to be displayed and Beacons On/Off.”
  
**Rationale:** Defines a user workflow to issue DMS commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-060]: Remote Control GUI supports LCS command entry
**Description**: “Once an Center is selected, the user shall be able to select a LCS from a list and provide the following information, including Target LCS and Assignment of lane arrows.”
  
**Rationale:** Defines a user workflow to issue LCS commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-061]: Remote Control GUI supports CCTV switching command entry
**Description**: “Once an Center is selected, the user shall be able to issue a CCTV switching command, including Source (input) and Destination port (output).”
  
**Rationale:** Defines a user workflow to issue CCTV switching commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-062]: Remote Control GUI supports CCTV control entry
**Description**: “Once an Center is selected, the user shall be able to select a CCTV from a list and provide the following information.”
  
**Rationale:** Defines a user workflow to issue CCTV control (details not specified in source text).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-063]: Remote Control GUI supports ramp meter command entry
**Description**: “Once an Center is selected, the user shall be able to select a Ramp Meter from a list and provide the following information, including Target Ramp Meter and Plan.”
  
**Rationale:** Defines a user workflow to issue ramp meter commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-064]: Remote Control GUI supports HAR command entry
**Description**: “Once an Center is selected, the user shall be able to select a HAR from a list and provide the following information, including Target HAR and Text to be sent to the HAR.”
  
**Rationale:** Defines a user workflow to issue HAR commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-015, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-065]: Remote Control GUI supports traffic signal command entry
**Description**: “Once an Center is selected, the user shall be able to select a Traffic Signal from a list and provide the following information, including Target Traffic Signal and Plan.”
  
**Rationale:** Defines a user workflow to issue traffic signal commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-017, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-066]: Remote Control GUI supports HOV command entry
**Description**: “Once an Center is selected, the user shall be able to select a HOV from a list and provide the following information, including Target HOV and Plan.”
  
**Rationale:** Defines a user workflow to issue HOV commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-020, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-067]: Remote Control GUI supports school zone command entry
**Description**: “Once an Center is selected, the user shall be able to select a School Zone from a list and provide the following information, including Target School Zone and Plan.”
  
**Rationale:** Defines a user workflow to issue school zone commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-023, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-068]: Remote Control GUI supports reversible lane command entry
**Description**: “Once an Center is selected, the user shall be able to select a Reversible Lane from a list and provide the following information, including Target Reversible Lane and Plan.”
  
**Rationale:** Defines a user workflow to issue reversible lane commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-026, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-069]: Remote Control GUI supports dynamic lane command entry
**Description**: “Once an Center is selected, the user shall be able to select a Dynamic Lane from a list and provide the following information, including Target Dynamic Lane and Plan.”
  
**Rationale:** Defines a user workflow to issue dynamic lane commands.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-028, FR-056, FR-058
- **Conflicts with:** NFR-004
---

[FR-070]: Display returned command/control status in a scrollable list
**Description**: “For each device command/control status request sent by the Remote GUI, the status returned from the network identifier will be displayed in a scrollable list on the GUI.” Updated per evaluator: All command/control status responses must display 'SUCCESS', 'FAILED', 'PENDING', or detailed error message in the GUI within 2 seconds of reply. [Next action: Document/display all possible statuses and their semantics.]
  
**Rationale:** Defines UI behavior for presenting responses.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-056, FR-059, FR-060, FR-061, FR-062, FR-063, FR-064, FR-065, FR-066, FR-067, FR-068, FR-069
- **Conflicts with:** NFR-005
---

[FR-071]: Operate in normal mode with multi-source ingest into a single datastore
**Description**: “The Center-to-Center shall be able to operate in normal mode. In this mode the Center-to-Center receives data from all connected systems, including the Incident GUI, and combines the data into a single data store (database).” Updated per evaluator: CI must execute loadtest ingesting 30K events in 6 minutes from ≥5 sources, and measure response with latency metrics and pass/fail variance. [Next action: Complete load/SLO test plan and acceptance gate.]
  
**Rationale:** Defines an operational mode and required data processing behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-038, FR-048, ASR-003
- **Conflicts with:** NFR-006
---

[FR-072]: Operate in test mode with activity logging
**Description**: “The Center-to-Center shall be able to operate in test mode. In this mode, the Center-to-Center performs normal mode operations and also logs activities.”
  
**Rationale:** Defines an operational mode and additional behavior (logging).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-071, NFR-010
- **Conflicts with:** NFR-011
---