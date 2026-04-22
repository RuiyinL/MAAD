# Functional Requirements Results:
[FR-001]: Provide Network Name and Link Data Information
**Description**: The Center shall provide a REST API endpoint GET /networks returning application/json: [{network_id: string, network_name: string, links: [{link_id: string, link_name: string, link_type: enum}]}].
**Rationale:** This requirement describes a specific behavior of the system, providing network name and link data information.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Provide Link Information
**Description**: The Center shall provide the link information, including link identifier, link name and link type.
**Rationale:** This requirement describes a specific behavior of the system, providing link information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-003]: Provide Node Information
**Description**: The Center shall provide the node information, including node identifier, node name and node type description.
**Rationale:** This requirement describes a specific behavior of the system, providing node information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-004]: Support Incident Information
**Description**: The Center shall support the information about each incident, including network identifier, incident description and roadway.
**Rationale:** This requirement describes a specific behavior of the system, supporting incident information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-005]: Support Lane Closure Information
**Description**: The Center shall support the information about each lane closure, including network identifier, lane closure id, closure description.
**Rationale:** This requirement describes a specific behavior of the system, supporting lane closure information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-006]: Provide DMS Status Information
**Description**: The Center shall provide the following status information about each DMS, including network identifier, DMS identifier, DMS name.
**Rationale:** This requirement describes a specific behavior of the system, providing DMS status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-007]: Support DMS Control
**Description**: To support DMS control in other centers, the Center shall be able to support the following device control command for a DMS, including network identifier, DMS identifier, username and Password.
**Rationale:** This requirement describes a specific behavior of the system, supporting DMS control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** None
---
[FR-008]: Provide LCS Status Information
**Description**: The Center shall support the following status information about each LCS, including network identifier, LCS identifier, LCS name, Location and Status.
**Rationale:** This requirement describes a specific behavior of the system, providing LCS status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-009]: Support LCS Control
**Description**: To support LCS control in other centers, the Center shall be able to support the following device control command for a LCS, including network identifier, LCS identifier, username and Password.
**Rationale:** This requirement describes a specific behavior of the system, supporting LCS control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** None
---
[FR-010]: Provide CCTV Status Information
**Description**: The Center shall provide the information status information about each CCTV, including network identifier, CCTV identifier, CCTV name, Location and Status.
**Rationale:** This requirement describes a specific behavior of the system, providing CCTV status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-011]: Support CCTV Control
**Description**: To support CCTV control in other centers, the Center shall be able to support the following CCTV control request, including network identifier, CCTV identifier, username, Password.
**Rationale:** This requirement describes a specific behavior of the system, supporting CCTV control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** None
---
[FR-012]: Support Video Snapshots
**Description**: To support video snapshots, the Center shall be able to support the status information, including network identifier, CCTV identifier, CCTV name and status.
**Rationale:** This requirement describes a specific behavior of the system, supporting video snapshots.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** None
---
[FR-013]: Support CCTV Switching
**Description**: To support CCTV switching in other centers, the Center shall be able to support the following CCTV switching command, including network identifier, username, Password and video channel input identifier.
**Rationale:** This requirement describes a specific behavior of the system, supporting CCTV switching.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** None
---
[FR-014]: Provide Ramp Meter Status Information
**Description**: The Center shall support the status information about each ramp meter, including network identifier, Ramp Meter identifier, Ramp Meter name, Location and Status.
**Rationale:** This requirement describes a specific behavior of the system, providing ramp meter status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-015]: Support Ramp Meter Control
**Description**: To support Ramp Meter control in other centers, the Center shall be able to support the following device control command for a ramp meter, including network identifier, Ramp Meter identifier, username, password and plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting ramp meter control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-014
- **Conflicts with:** None
---
[FR-016]: Provide HAR Status Information
**Description**: The Center shall support the following status information about each HAR, including network identifier, HAR identifier, HAR name, location and status.
**Rationale:** This requirement describes a specific behavior of the system, providing HAR status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-017]: Support HAR Control
**Description**: To support HAR control in other centers, the Center shall be able to support the following device control command for a HAR, including network identifier, HAR identifier, username, password and message.
**Rationale:** This requirement describes a specific behavior of the system, supporting HAR control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016
- **Conflicts with:** None
---
[FR-018]: Provide Traffic Signal Status Information
**Description**: The Center shall support the following status information about each Traffic Signal, including network identifier, traffic signal identifier, traffic signal name, location and status.
**Rationale:** This requirement describes a specific behavior of the system, providing traffic signal status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-019]: Support Traffic Signal Control
**Description**: To support Traffic Signal control in other centers, the Center shall be able to support the following device control command for a Traffic Signal, including network identifier, traffic signal identifier, username, password and traffic signal plan identifier.
**Rationale:** This requirement describes a specific behavior of the system, supporting traffic signal control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-018
- **Conflicts with:** None
---
[FR-020]: Provide ESS Status Information
**Description**: The Center shall support the following status information about each ESS, including network identifier, environmental sensor identifier, environment sensor name, type, location and status.
**Rationale:** This requirement describes a specific behavior of the system, providing ESS status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-021]: Provide HOV Status Information
**Description**: The Center shall support the following status information about each HOV, including network identifier, HOV identifier, HOV name, link identifier, status and plan.
**Rationale:** This requirement describes a specific behavior of the system, providing HOV status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-022]: Support HOV Lane Control
**Description**: To support HOV Lane control in other centers, the Center shall be able to support the following device control command for a HOV Lane, including network identifier, HOV Lane identifier, username, password and lane plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting HOV lane control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021
- **Conflicts with:** None
---
[FR-023]: Provide Parking Lot Status Information
**Description**: The Center shall support the following status information about each Parking Lot, including network identifier, parking lot identifier, parking lot name, location and status.
**Rationale:** This requirement describes a specific behavior of the system, providing parking lot status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-024]: Provide School Zone Status Information
**Description**: The Center shall support the following status information about each School Zone, including network identifier, link identifier, school zone identifier and school zone name.
**Rationale:** This requirement describes a specific behavior of the system, providing school zone status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-025]: Support School Zone Control
**Description**: To support School Zone control in other centers, the Center shall be able to support the following device control command for a School Zone, including network identifier, school zone identifier, username, password and plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting school zone control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-024
- **Conflicts with:** None
---
[FR-026]: Provide Railroad Crossing Status Information
**Description**: The Center shall support the following status information about each Railroad Crossing, including network identifier, link identifier, rail crossing identifier, rail crossing name, location and status.
**Rationale:** This requirement describes a specific behavior of the system, providing railroad crossing status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-027]: Provide Reversible Lane Status Information
**Description**: The Center shall support the following status information about each Reversible Lane, including network identifier, reversible lane identifier, reversible lane name, link identifier, indicator status and indicator failure state.
**Rationale:** This requirement describes a specific behavior of the system, providing reversible lane status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-028]: Support Reversible Lane Control
**Description**: To support Reversible Lane control in other centers, the Center shall be able to support the following device control command for a Reversible Lane, including network identifier, reversible lane identifier, username, password, plan and duration.
**Rationale:** This requirement describes a specific behavior of the system, supporting reversible lane control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-027
- **Conflicts with:** None
---
[FR-029]: Provide Dynamic Lane Status Information
**Description**: The Center shall support the following status information about each Dynamic Lane, including network identifier, link identifier, dynamic lane identifier, dynamic lane name and failure state.
**Rationale:** This requirement describes a specific behavior of the system, providing dynamic lane status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-030]: Support Dynamic Lane Control
**Description**: To support Dynamic Lane control in other centers, the Center shall be able to support the following device control command for a Dynamic Lane, including network identifier, dynamic lane identifier, username, password and lane plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting dynamic lane control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None
---
[FR-031]: Provide Bus Stop Status Information
**Description**: The Center shall support the following status information about each Bus Stop, including network identifier, link identifier, relative link location, name and location.
**Rationale:** This requirement describes a specific behavior of the system, providing bus stop status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-032]: Provide Bus Location Status Information
**Description**: The Center shall support the following status information about each Bus Location, including network identifier, link identifier, bus identifier, bus name, location and schedule adherence.
**Rationale:** This requirement describes a specific behavior of the system, providing bus location status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-033]: Provide Light/Commuter Stop Status Information
**Description**: The Center shall support the following status information about each Light/Commuter Stop, including network identifier, link identifier, commuter or light rail stop identifier, commuter or light rail stop name, location and routes.
**Rationale:** This requirement describes a specific behavior of the system, providing light/commuter stop status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-034]: Provide Light/Commuter Location Status Information
**Description**: The Center shall support the following status information about each Light/Commuter Location, including network identifier, link identifier, commuter or light rail identifier, commuter or light rail name, location and schedule adherence.
**Rationale:** This requirement describes a specific behavior of the system, providing light/commuter location status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-035]: Provide Park and Ride Lot Status Information
**Description**: The Center shall support the following status information about each Park and Ride Lot, including network identifier, park and ride lot identifier, park and ride lot name, location, status and capacity.
**Rationale:** This requirement describes a specific behavior of the system, providing park and ride lot status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-036]: Provide Vehicle Priority Status Information
**Description**: The Center shall support the following status information about each Vehicle Priority, including vehicle identifier, network identifier, link identifier and intersection identifier.
**Rationale:** This requirement describes a specific behavior of the system, providing vehicle priority status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-037]: Provide Network Device Status Information
**Description**: The Center shall support the following information about network device status, including network identifier, number of DMSs, number of LCSs, DMS status data, LCS status data and CCTV status data.
**Rationale:** This requirement describes a specific behavior of the system, providing network device status information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-038]: Support Command Timeframe Request
**Description**: The device status requestor and Center shall support the following information for command timeframe request, including network identifier and device type.
**Rationale:** This requirement describes a specific behavior of the system, supporting command timeframe request.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-037
- **Conflicts with:** None
---
[FR-039]: Support Command Timeframe Request with Additional Information
**Description**: The device status requestor and Center shall support the following information for command timeframe request, including network identifier, device type, days commands accepted and times commands accepted.
**Rationale:** This requirement describes a specific behavior of the system, supporting command timeframe request with additional information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-038
- **Conflicts with:** None
---
[FR-040]: Store TMDD Data Elements and Message Set Information
**Description**: The Data Collector shall be designed to support the storage of TMDD data elements and message set information.
**Rationale:** This requirement describes a specific behavior of the system, storing TMDD data elements and message set information.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-041]: Utilize TMDD Standard for Information Transmission
**Description**: The Center-to-Center Project shall utilize the TMDD standard (including message sets) to transmit information.
**Rationale:** This requirement describes a specific behavior of the system, utilizing TMDD standard for information transmission.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-040
- **Conflicts with:** None
---
[FR-042]: Generate Map with Traffic Conditions
**Description**: The Web Map application generates a map that can be displayed on an Internet WWW server, providing a graphical depiction of the traffic conditions.
**Rationale:** This requirement describes a specific behavior of the system, generating a map with traffic conditions.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-043]: Display Interstates and State Highways on Map
**Description**: The map shall display interstates and state highways on the graphical map.
**Rationale:** This requirement describes a specific behavior of the system, displaying interstates and state highways on map.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-044]: Allow Map User to Alter Magnification
**Description**: The map user shall be able to alter the current magnification (zoom level) of the map.
**Rationale:** This requirement describes a specific behavior of the system, allowing map user to alter magnification.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-045]: Allow Map User to Pan Map
**Description**: The map user shall be able to pan the map in each of the following directions: North, South, East or West.
**Rationale:** This requirement describes a specific behavior of the system, allowing map user to pan map.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-046]: Display Link Information with Color Coding
**Description**: Each link displayed on the map shall be color coded to provide a graphical depiction of speeds.
**Rationale:** This requirement describes a specific behavior of the system, displaying link information with color coding.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-047]: Provide Configuration File for Speed Values
**Description**: A configuration file shall be provided to specify specific speed values.
**Rationale:** This requirement describes a specific behavior of the system, providing configuration file for speed values.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-046
- **Conflicts with:** None
---
[FR-048]: Display Current Incidents on Map
**Description**: The map shall display the current incidents (as icons) known to the Center-to-Center Project.
**Rationale:** This requirement describes a specific behavior of the system, displaying current incidents on map.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-049]: Allow User to Click on Incident Icon for More Information
**Description**: The user shall be able to click on an incident icon to obtain further information about the incident.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to click on incident icon for more information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** None
---
[FR-050]: Display Incident Information in Tabular Format
**Description**: All current incidents shall be displayed in tabular format with the following information contained in the table.
**Rationale:** This requirement describes a specific behavior of the system, displaying incident information in tabular format.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** None
---
[FR-051]: Support Incident GUI
**Description**: Incident GUI shall support: (a) incident entry form with [field list], (b) lane closure entry form with [field list], both independent of Center selection.
**Rationale:** This requirement describes a specific behavior of the system, supporting incident GUI.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-048
- **Conflicts with:** None
---
[FR-052]: Allow User to Input Incident Information
**Description**: The Incident GUI shall allow the user to input the following information for each incident.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to input incident information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[FR-053]: Allow User to Input Lane Closure Information
**Description**: The Incident GUI shall allow the user to input the following information for each lane closure.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to input lane closure information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[FR-054]: Provide List of Previously Entered Incidents
**Description**: The GUI shall provide a list of previously entered incidents.
**Rationale:** This requirement describes a specific behavior of the system, providing list of previously entered incidents.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[FR-055]: Allow User to Modify Incident Information
**Description**: The GUI shall allow the data about an incident to be modified.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to modify incident information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-054
- **Conflicts with:** None
---
[FR-056]: Allow User to Delete Incident
**Description**: The GUI shall allow a user to delete a previously entered incident.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to delete incident.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-054
- **Conflicts with:** None
---
[FR-057]: Provide List of Previously Entered Lane Closures
**Description**: The GUI shall provide a list of previously entered lane closures.
**Rationale:** This requirement describes a specific behavior of the system, providing list of previously entered lane closures.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[FR-058]: DEPRECATED
**Description**: This requirement has been deprecated due to redundancy with FR-057.
**Rationale:** This requirement is no longer necessary.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** FR-057
---
[FR-059]: Support Remote Center Control GUI
**Description**: The remote Center Control GUI shall be designed to execute on a public network (e.g., Internet) and transmit equipment requests to the C-2-C software system.
**Rationale:** This requirement describes a specific behavior of the system, supporting remote center control GUI.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-060]: Prompt User for Login Information
**Description**: When the GUI application is initiated, the user shall be prompted for the following information, including User name and Password.
**Rationale:** This requirement describes a specific behavior of the system, prompting user for login information.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[FR-061]: Allow User to Select Network Identifier
**Description**: The user shall be provided with the capability to select a network identifier for a device command/control request.
**Rationale:** This requirement describes a specific behavior of the system, allowing user to select network identifier.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[FR-062]: Support DMS Control
**Description**: Once an Center is selected, the user shall be able to select a DMS from a list and provide the following information, including Target DMS, Message to be displayed and Beacons On/Off.
**Rationale:** This requirement describes a specific behavior of the system, supporting DMS control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-063]: Support LCS Control
**Description**: Once an Center is selected, the user shall be able to select a LCS from a list and provide the following information, including Target LCS and Assignment of lane arrows.
**Rationale:** This requirement describes a specific behavior of the system, supporting LCS control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-064]: Support CCTV Switching
**Description**: Once an Center is selected, the user shall be able to issue a CCTV switching command, including Source (input) and Destination port (output).
**Rationale:** This requirement describes a specific behavior of the system, supporting CCTV switching.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-065]: Support CCTV Control
**Description**: Once an Center is selected, the user shall be able to select a CCTV from a list and provide the following information.
**Rationale:** This requirement describes a specific behavior of the system, supporting CCTV control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-066]: Support Ramp Meter Control
**Description**: Once an Center is selected, the user shall be able to select a Ramp Meter from a list and provide the following information, including Target Ramp Meter and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting ramp meter control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-067]: Support HAR Control
**Description**: Once an Center is selected, the user shall be able to select a HAR from a list and provide the following information, including Target HAR and Text to be sent to the HAR.
**Rationale:** This requirement describes a specific behavior of the system, supporting HAR control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-068]: Support Traffic Signal Control
**Description**: Once an Center is selected, the user shall be able to select a Traffic Signal from a list and provide the following information, including Target Traffic Signal and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting traffic signal control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-069]: Support HOV Control
**Description**: Once an Center is selected, the user shall be able to select a HOV from a list and provide the following information, including Target HOV and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting HOV control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-070]: Support School Zone Control
**Description**: Once an Center is selected, the user shall be able to select a School Zone from a list and provide the following information, including Target School Zone and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting school zone control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-071]: Support Reversible Lane Control
**Description**: Once an Center is selected, the user shall be able to select a Reversible Lane from a list and provide the following information, including Target Reversible Lane and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting reversible lane control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-072]: Support Dynamic Lane Control
**Description**: Once an Center is selected, the user shall be able to select a Dynamic Lane from a list and provide the following information, including Target Dynamic Lane and Plan.
**Rationale:** This requirement describes a specific behavior of the system, supporting dynamic lane control.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-061
- **Conflicts with:** None
---
[FR-073]: Display Device Command/Control Status
**Description**: For each device command/control status request sent by the Remote GUI, the status returned from the network identifier will be displayed in a scrollable list on the GUI. Status must appear in UI within 3s of user command; if >5s, label as 'Delayed/Timeout'. Metric: device_status_latency histogram, alert if >3s for >0.1% of requests per hour.
**Rationale:** This requirement describes a specific behavior of the system, displaying device command/control status.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[FR-074]: Execute in Microsoft Windows NT Environment
**Description**: The Center-to-Center Server shall execute in a Microsoft Windows NT environment.
**Rationale:** This requirement describes a specific behavior of the system, executing in Microsoft Windows NT environment.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-075]: Utilize DATEX/ASN Runtime Library
**Description**: A DATEX/ASN runtime library shall be available on any computer communicating to the Center-to-Center project.
**Rationale:** This requirement describes a specific behavior of the system, utilizing DATEX/ASN runtime library.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-041
- **Conflicts with:** None
---
[FR-076]: Use ESRI's ARC Internet Map Server
**Description**: The web server application shall use ESRI's ARC Internet Map Server (ARC IMS) product for creating of map images.
**Rationale:** This requirement describes a specific behavior of the system, using ESRI's ARC Internet Map Server.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-042
- **Conflicts with:** None
---
[FR-077]: Implement Center-to-Center in C/C++
**Description**: At least 95% of implementation files (excluding 3rd-party libs) are C/C++.
**Rationale:** This requirement describes a specific behavior of the system, implementing Center-to-Center in C/C++.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-078]: Implement Web Interface in C/C++ and ESRI ARC IMS
**Description**: The Center-to-Center web interface shall be implemented using C/C++ and ESRI ARC IMS.
**Rationale:** This requirement describes a specific behavior of the system, implementing web interface in C/C++ and ESRI ARC IMS.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-076
- **Conflicts with:** None
---
[FR-079]: Implement Incident GUI in C/C++ and ESRI Map Objects
**Description**: Incident GUI shall operate on Windows 10/11, with startup time <5s and memory usage <512MB.
**Rationale:** This requirement describes a specific behavior of the system, implementing incident GUI in C/C++ and ESRI Map Objects.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-051
- **Conflicts with:** None
---
[FR-080]: Implement Remote Control GUI in C/C++ and ESRI Map Objects
**Description**: The Remote Control GUI shall be implemented using C/C++ and ESRI Map Objects.
**Rationale:** This requirement describes a specific behavior of the system, implementing remote control GUI in C/C++ and ESRI Map Objects.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-059
- **Conflicts with:** None
---
[FR-081]: Operate in Normal Mode
**Description**: The Center-to-Center shall be able to operate in normal mode, receiving data from all connected systems and combining the data into a single data store.
**Rationale:** This requirement describes a specific behavior of the system, operating in normal mode.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-082]: Operate in Test Mode
**Description**: The Center-to-Center shall be able to operate in test mode, performing normal mode operations and logging activities.
**Rationale:** This requirement describes a specific behavior of the system, operating in test mode.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-081
- **Conflicts with:** None