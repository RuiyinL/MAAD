# Functional Requirements Results

[FR-001A]: Web-ready device monitoring of home environment  
**Description**: “Derived from FR-001. The DigitalHome System shall allow a web-ready computer, cell phone or PDA to monitor a home's temperature, humidity, lights, security, and the state of small appliances.”  
**Rationale:** Describes user-facing system behavior (remote monitoring function).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-004, FR-005, FR-006, NFR-004, NFR-008
- **Conflicts with:** NFR-010
---

[FR-001B]: Web-ready device control of home environment  
**Description**: “Derived from FR-001. The DigitalHome System shall allow a web-ready computer, cell phone or PDA to control a home's temperature, humidity, lights, security, and the state of small appliances.”  
**Rationale:** Describes user-facing system behavior (remote control function).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-004, FR-005, FR-006, NFR-004, NFR-008
- **Conflicts with:** NFR-010
---

[FR-001]: Web-ready device monitoring and control of home environment (DEPRECATED)  
**Description**: “The DigitalHome System shall allow a web-ready computer, cell phone or PDA to control a home's temperature, humidity, lights, security, and the state of small appliances.” (Deprecated; split into FR-001A and FR-001B per Evaluator next_action: Refactor non-atomic FRs into one-action-per-FR.)  
**Rationale:** Describes user-facing system behavior (remote monitoring/control functions).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-004, FR-005, FR-006, NFR-004, NFR-008
- **Conflicts with:** NFR-010
---

[FR-002A]: Provide user interaction via personal web page on DigitalHome web server  
**Description**: “Derived from FR-002. The user communicates through a personal web page on the DigitalHome web server.”  
**Rationale:** Defines a required interaction mechanism/function (web-based UI).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-008
- **Conflicts with:** NFR-010
---

[FR-002B]: Provide user interaction via personal web page on local home server  
**Description**: “Derived from FR-002. The user communicates through a personal web page on a local home server.”  
**Rationale:** Defines a required interaction mechanism/function (web-based UI).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-008
- **Conflicts with:** NFR-010
---

[FR-002]: Provide user interaction via personal web page (web server or local home server) (DEPRECATED)  
**Description**: “The user communicates through a personal web page on the DigitalHome web server or on a local home server.” (Deprecated; split into FR-002A and FR-002B per Evaluator next_action: Refactor non-atomic FRs into one-action-per-FR.)  
**Rationale:** Defines a required interaction mechanism/function (web-based UI).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-008
- **Conflicts with:** NFR-010
---

[FR-003A]: Home web server establishment on home computer  
**Description**: “Derived from FR-003. A DigitalHome System shall have the capability to establish an individual home web server hosted on a home computer.”  
**Rationale:** Specifies a concrete system service/function (web server establishment).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-003B]: Home web server provides interaction and control of DigitalHome elements  
**Description**: “Derived from FR-003. The home web server will provide interaction with and control of the DigitalHome elements.”  
**Rationale:** Specifies a concrete system service/function (interaction/control).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-003C]: Home web server stores DigitalHome plans and data  
**Description**: “Derived from FR-003. The home web server will provide storage of DigitalHome plans and data.”  
**Rationale:** Specifies a concrete system service/function (data storage).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-003D]: Home web server establishes and maintains DigitalHome user accounts  
**Description**: “Derived from FR-003. The home web server will provide ability to establish and maintain DigitalHome User Accounts.”  
**Rationale:** Specifies a concrete system service/function (account management).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-003E]: Home web server provides backup service for account info, plans, and database  
**Description**: “Derived from FR-003. The home web server will provide backup service for user account information, user plans and a home database.”  
**Rationale:** Specifies a concrete system service/function (backup service).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-003]: Home web server provides interaction/control, storage, accounts, and backups (DEPRECATED)  
**Description**:  
- “A DigitalHome System shall have the capability to establish an individual home web server hosted on a home computer.”  
- “The home web server will provide interaction with and control of the DigitalHome elements.”  
- “The home web server will provide storage of DigitalHome plans and data.”  
- “The home web server will provide ability to establish and maintain DigitalHome User Accounts.”  
- “The home web server will provide backup service for user account information, user plans and a home database.”  
(Deprecated; split into FR-003A..FR-003E per Evaluator next_action: Refactor non-atomic FRs into one-action-per-FR.)  
**Rationale:** Specifies system services/functions delivered by the home web server.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019, FR-020, FR-021, FR-022, NFR-004, NFR-005
- **Conflicts with:** NFR-010
---

[FR-004]: Gateway communicates with all devices and connects to broadband  
**Description**: “The DigitalHome Gateway device shall provide communication with all the DigitalHome devices and shall connect with a broadband Internet connection.”  
**Rationale:** Defines required device-communication behavior and connectivity function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-003, NFR-009
- **Conflicts with:** NFR-010
---

[FR-005]: Gateway RF module sends/receives wireless communications  
**Description**: “The Gateway shall contain an RF Module, which shall send and receive wireless communications between the Gateway and the other DigitalHome devices (sensors and controllers).”  
**Rationale:** Specifies a concrete functional capability (wireless send/receive).  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003, NFR-009
- **Conflicts with:** Not identified
---

[FR-006]: Read sensor values and save to home database; send controller values to devices  
**Description**: “Using wireless communication, sensor values can be read and saved in the home database. Controller values can be sent to controllers to change the DigitalHome environment.”  
**Rationale:** Describes core system processing (acquire, persist, and actuate).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005, FR-003, NFR-001, NFR-002
- **Conflicts with:** Not identified
---

[FR-007]: Thermostat monitoring and control from any location  
**Description**: “The DigitalHome programmable thermostat shall allow a user to monitor and control a home’s temperature from any location, using a web ready computer, cell phone, or PDA.”  
**Rationale:** Defines functional capability (remote thermostat management).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-004, FR-006
- **Conflicts with:** Not identified
---

[FR-008]: Read temperature at thermostat position  
**Description**: “A DigitalHome user shall be able to read the temperature at a thermostat position.”  
**Rationale:** Specifies a user-facing read function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-006
- **Conflicts with:** Not identified
---

[FR-009]: Set thermostat temperature with allowed range and increments  
**Description**: “A DigitalHome user shall be able to set the thermostat temperatures to between 60 °F and 80 °F, inclusive, at one degree increments.”  
**Rationale:** Specifies an input/control function with constraints.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** Not identified
---

[FR-010]: Support up to eight thermostats; individual and collective control  
**Description**:  
- “Up to eight thermostats shall be placed in rooms throughout the home.”  
- “The thermostats may be controlled individually or collectively…”  
**Rationale:** Defines system behavior and scaling of device management (control modes).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007, FR-006
- **Conflicts with:** Not identified
---

[FR-011]: Thermostat scheduling (up to 24 hourly settings/day for each day of week)  
**Description**: “For each thermostat, up to twenty-four one hour settings per day for every day of the week can be scheduled. The following order of precedence shall apply globally across all device/planning domains: Manual override > Planned value > Default value; upon manual setting, persist until the end of the current or next planned interval, then revert per plan.” (Next action: Amend FR-011 and all override-related FRs to uniformly state the global precedence rule.)  
**Rationale:** Defines a scheduling function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, FR-006
- **Conflicts with:** FR-012 (if precedence not defined consistently)
---

[FR-012]: Thermostat manual override persists until end of planned/default period  
**Description**: “If a thermostat device allows a user to make a manual temperature setting, the setting shall remain in effect until the end of the planned or default time period, at which time the planned or default setting will be used for the next time period. Manual device overrides shall take precedence over planned and default values, until the end of the next planned time period, at which point plan resumes.” (Next action: Amend all related FRs to state global order of precedence for settings.)  
**Rationale:** Defines behavioral rule for override and state persistence.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, FR-022
- **Conflicts with:** FR-023 (if override precedence differs)
---

[FR-013]: Thermostat communicates wirelessly with master control unit  
**Description**: “A thermostat unit shall communicate, through wireless signals, with the master control unit.”  
**Rationale:** Defines required communication behavior among components.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005
- **Conflicts with:** Not identified
---

[FR-014]: Support Fahrenheit and Celsius temperature values  
**Description**: “The system shall support Fahrenheit and Celsius temperature values. Each user can select preferred temperature units (°F/°C); units shall be stored in user profile and applied to all temperature displays and inputs. Acceptance: Setting persists across login/logoff. ‘units’ field in user profile is enum {'C','F'}, used for all temp input/output; default 'F'. Schema: user_profile {id: int, username: string, temp_units: enum<'C','F'>, ... }; persisted to user_accounts table.” (Next action: Add schema stub and data contract citation to FR-014 and implement in reporting/docs.)  
**Rationale:** Defines functional capability for units handling.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-009, FR-024
- **Conflicts with:** Not identified
---

[FR-015]: Humidistat monitoring and control from any location  
**Description**: “The DigitalHome programmable humidistat shall allow a user to monitor and control a home’s humidity from any location, using a web ready computer, cell phone, or PDA.”  
**Rationale:** Defines functional capability (remote humidity management).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-004, FR-006
- **Conflicts with:** Not identified
---

[FR-016]: Read humidity at humidistat position  
**Description**: “A DigitalHome user shall be able to read the humidity at a humidistat position.”  
**Rationale:** Specifies a user-facing read function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015, FR-006
- **Conflicts with:** Not identified
---

[FR-017]: Set humidity with allowed range and increments  
**Description**: “A DigitalHome user shall be able to set the humidity level for a humidistat, from 30% to 60%, inclusive a 1% increments.”  
**Rationale:** Specifies a control function with constraints.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015
- **Conflicts with:** Not identified
---

[FR-018]: Support up to eight humidistats and scheduling (24 hourly settings/day)  
**Description**:  
- “Up to eight humidistats shall be placed in rooms throughout the home.”  
- “For each humidistat, up to twenty-four one hour settings per day for every day of the week can be scheduled.”  
(Next action: Amend all related FRs to state global order of precedence for settings.)  
**Rationale:** Defines scaling and scheduling behavior for humidistats.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015, FR-022
- **Conflicts with:** FR-012/FR-023 if override precedence is inconsistent
---

[FR-019]: Humidistat manual override persists until end of planned/default period  
**Description**: “If a humdistat device allows a user to make a manual temperature setting, the setting shall remain in effect until the end of the planned or default time period, at which time the planned or default setting will be used for the next time period. Manual device overrides shall take precedence over planned and default values, until the end of the next planned time period, at which point plan resumes.” (Next action: Amend all related FRs to state global order of precedence for settings.)  
**Rationale:** Defines behavioral rule for overrides.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-018, FR-022
- **Conflicts with:** FR-023 (if global override precedence differs)
---

[FR-020]: Humidistats communicate wirelessly via master control unit  
**Description**: “A DigitalHome system shall use wireless signals to communicate, through the master control unit, with the humidistats.”  
**Rationale:** Defines required device communication behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005
- **Conflicts with:** Not identified
---

[FR-021]: Manage up to fifty door/window contact sensors  
**Description**: “A DigitalHome system shall be able to manage up to fifty door and window contact sensors.”  
**Rationale:** Specifies a concrete management capability and supported scale.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-006
- **Conflicts with:** Not identified
---

[FR-022]: Activate light and sound alarms on security breach  
**Description**:  
- “A DigitalHome system shall be able to activate both light and sound alarms: one sound alarm and one light alarm subsystem, with multiple lights.”  
- “When a security breach occurs and a contact sensor is set OPEN, the alarm system shall be activated.”  
**Rationale:** Defines event-driven security behavior (detect -> alarm).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, FR-006
- **Conflicts with:** FR-023 (if plans can disable alarms without clear precedence)
---

[FR-023]: Appliance and lighting management (turn on/off)  
**Description**: “The DigitalHome programmable Appliance Manager shall provide for management of a home’s small appliances, including lighting units, by allowing a user to turn them on or off as desired.”  
**Rationale:** Specifies a user-facing control function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-006
- **Conflicts with:** Not identified
---

[FR-024]: Manage up to one hundred power switches and report/change power state  
**Description**:  
- “The Appliance Manager shall be able to manage up to one hundred 115 volt, 10 amp power switches.”  
- “The system shall be able to provide information about the state of a power switch (OFF or ON)…”  
- “The system shall be able to change the state of a power switch…”  
**Rationale:** Defines device management functions (query state, command state) at a specified scale.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-023, FR-006
- **Conflicts with:** Not identified
---

[FR-025]: Power switch manual change persists until end of planned/default period  
**Description**: “If a user changes the state of power switch device manually, the device shall remain in that state until the end of the planned or default time period, at which time the planned or default setting will be used for the next time period. Manual device overrides shall take precedence over planned and default values, until the end of the next planned time period, at which point plan resumes.” (Next action: Amend all related FRs to state global order of precedence for settings.)  
**Rationale:** Defines functional override behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-024, FR-026
- **Conflicts with:** FR-027 (if override precedence differs)
---

[FR-026]: DigitalHome Planner creates/modifies month plans (4 daily periods/day)  
**Description**: “For a given month and year, a user shall be able to create or modify a month plan that specifies for each day, for up to four daily time periods, the environmental parameter settings (temperature, humidity, contact sensors and power switches).”  
**Rationale:** Defines planning function and associated data structure.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-006
- **Conflicts with:** Not identified
---

[FR-027]: Override planned values via website or manual switches  
**Description**: “A user shall be able to override planned parameter values, through the DigitalHome website, or if available, through manual switches on household devices. Manual override takes precedence until the end of the current or next planned interval, then reverts to planned; planned overrides default. Acceptance: Manual > Planned > Default, manual applies through next scheduled transition, proven in system tests. All manual/planned/default value overrides for connected devices must follow the global precedence rule as defined in FR-011.” (Next action: Update all affected FRs to cross-reference the canonical override rule in FR-027/FR-011.)  
**Rationale:** Specifies a system behavior for handling overrides.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-026, FR-011, FR-018, FR-025
- **Conflicts with:** Not identified (but precedence among manual/plan/default must be consistent across domains)
---

[FR-028]: Provide month report for past two years  
**Description**: “For a given month and year, in the past two years, DigitalHome shall be able to provide a report on the management and control of the home. Monthly reports shall be delivered as CSV and PDF. Acceptance: Monthly report includes for each monitored parameter: field names, types, sample CSV and PDF structure.” (Next action: Add schemas/examples to FR-028-031 and document in reporting design.)  
**Rationale:** Defines reporting function over stored historical data.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-006, NFR-006
- **Conflicts with:** NFR-008 (if storage/retention not sufficient)
---

[FR-029]: Month report includes temperature/humidity daily avg/max/min with time per device  
**Description**: “The month report shall contain daily average, maximum (with time) and minimum (with time) values of temperature and humidity for each thermostat and humidistat, respectively. Report fields shall include daily average/min/max temperature per thermostat (timestamped) and daily average/min/max humidity per humidistat (timestamped). Acceptance: Report includes (for each thermostat/humidistat): device_id, date, avg, min, max, min_time, max_time; all timestamps in UTC (ISO 8601).” (Next action: Create canonical schema and add to FR-029/FR-028.)  
**Rationale:** Specifies required content/outputs of reporting.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-028, FR-008, FR-016
- **Conflicts with:** Not identified
---

[FR-030]: Month report includes security breach day/time (alarm activations)  
**Description**: “The month report shall provide the day and time for which any security breaches occurred, that is, when the security alarms were activated. Alarm incidents shall be included with type and date/time.” (Next action: Document concrete schema and format for reports.)  
**Rationale:** Specifies required reporting output for security events.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-028, FR-022
- **Conflicts with:** Not identified
---

[FR-031]: Month report includes periods when system not in operation  
**Description**: “The month report shall provide a section that indicates the periods of time when the DigitalHome System was not in operation. Downtime periods shall be included as UTC intervals.” (Next action: Document concrete schema and format for reports.)  
**Rationale:** Defines reporting behavior based on operational status tracking.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-028, NFR-004
- **Conflicts with:** Not identified
---

[FR-032]: Establish general user accounts upon installation  
**Description**: “Upon installation, a DigitalHome user account shall be established. All changes to user roles/configuration must be auditable and reported in a monthly security log summary. 'user_accounts' table includes id, username, role, date_created; provisioning events logged in security log.” (Next action: Add schema/log examples to FR-032.)  
**Rationale:** Specifies an account provisioning function at installation time.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-033
- **Conflicts with:** Not identified
---

[FR-033]: Master user can change system configuration (accounts, defaults)  
**Description**: “A Master user will be designated, who shall be able to change the configuration of the system… add a user account or change the default parameter settings. All changes to user roles/configuration must be auditable and reported in a monthly security log summary.” (Next action: Expand admin functionality requirements with audit/logging.)  
**Rationale:** Defines privileged configuration management functions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-008
- **Conflicts with:** Not identified
---

[FR-034]: Technician can configure system and start/stop system operation  
**Description**: “A DigitalHome Technician… capable of setting up and making changes in the configuration of the system… and starting and stopping operation of the DigitalHome System. All changes to user roles/configuration must be auditable and reported in a monthly security log summary.” (Next action: Expand admin functionality requirements with audit/logging.)  
**Rationale:** Defines administrative operational functions.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-031, NFR-008
- **Conflicts with:** Not identified
---

[FR-035]: Exception handling with clear descriptive user messages  
**Description**: “All DigitalHome operations shall incorporate exception handling so that the system responds to a user with a clear, descriptive message when an error or an exceptional condition occurs. Acceptance: All error codes/messages reviewed; coverage report shows 95%+ error scenarios exercise descriptive feedback. All error scenarios return codes per digitalhome-error-catalog v1. Test: coverage report proves ≥95% code paths exercised for descriptive error.” (Next action: Amend FR-035 with error catalog, coverage metric, and test evidencing.)  
**Rationale:** Specifies runtime behavior in error cases (observable function to users).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** Not identified
---