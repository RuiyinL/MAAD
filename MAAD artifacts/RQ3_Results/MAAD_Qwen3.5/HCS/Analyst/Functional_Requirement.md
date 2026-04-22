# Functional Requirements Results:

[FR-001]: User Authentication and Account Management
**Description**: The system shall establish a user account upon installation. The system shall provide authentication via the web interface. A Master user shall be able to add a user account. A DigitalHome Technician shall be capable of establishing user accounts. A role access table shall govern all user/admin privileges; system enforces unique email per account, password length ≥12, and logs all role elevation events. Acceptance criterion: A role-permissions matrix covering General, Master, and Technician users is defined; authentication includes user/password and optional MFA, with session timeout/revocation behavior documented. Audit log schema: {timestamp, user_id, action, ip_address, result}. Actor-permission matrix: tabular listing. Session timeout: 15-minute inactivity auto-logout; session revocation available per admin action. Next action: Define and document audit log, permission schema, and session rules.
**Rationale:** Describes specific user management behaviors and access control functions (login, account creation).
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003 (Security)
- **Conflicts with:** None identified
---

[FR-002]: Temperature Control and Monitoring
**Description**: The system shall allow a user to read the current temperature at a thermostat position and set the thermostat temperatures between 60 °F and 80 °F (inclusive, 1 degree increments). Up to eight thermostats shall be supported. For each thermostat, up to twenty-four one-hour settings per day for every day of the week can be scheduled.
**Rationale:** Describes the core function of monitoring and regulating temperature with specific operational parameters.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Gateway Communication), NFR-001 (Performance)
- **Conflicts with:** None identified
---

[FR-003]: Humidity Control and Monitoring
**Description**: The system shall allow a user to read the current humidity at a humidistat position and set the humidity level from 30% to 60% (inclusive, 1% increments). Up to eight humidistats shall be supported. For each humidistat, up to twenty-four one-hour settings per day for every day of the week can be scheduled.
**Rationale:** Describes the core function of monitoring and regulating humidity with specific operational parameters.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Gateway Communication), NFR-001 (Performance)
- **Conflicts with:** None identified
---

[FR-004]: Security Monitoring and Alarms
**Description**: The system shall manage up to fifty door and window contact sensors. When a security breach occurs (contact sensor set OPEN), the system shall activate both light and sound alarms.
**Rationale:** Describes the security monitoring behavior and reactive alarm activation.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Gateway Communication)
- **Conflicts with:** None identified
---

[FR-005]: Appliance and Power Management
**Description**: The system shall manage up to one hundred 115 volt, 10 amp power switches. The system shall provide information about the state of a power switch (OFF or ON) and change the state of a power switch (OFF to ON, or ON to OFF) via user request.
**Rationale:** Describes the function of controlling and monitoring appliance power states.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Gateway Communication)
- **Conflicts with:** None identified
---

[FR-006]: Environmental Planning and Scheduling
**Description**: The DigitalHome Planner shall provide the capability to direct the system to set various preset home parameters (temperature, humidity, security contacts, and on/off appliance/light status) for certain time periods. A user shall be able to create or modify a month plan that specifies for each day, for up to four daily time periods, the environmental parameter settings. Acceptance: If a user/manual override occurs, maintain that parameter until next plan period begins (15-minute minimum slot); logic tested in all device types. Next action: Expand override timing/priority rules and test cases.
**Rationale:** Describes the automation and scheduling logic function.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-004, FR-005
- **Conflicts with:** None identified
---

[FR-007]: Reporting and History
**Description**: For a given month and year, in the past two years, the system shall provide a report on the management and control of the home. The report shall contain daily average, maximum (with time), and minimum (with time) values of temperature and humidity, security breach times, and system downtime periods. Output schema: {day, thermostat_id, temp_avg, temp_max, temp_min, max_time, min_time, ...} as full JSON schema, plus matching CSV columns. Next action: Write/example output report schema in JSON and CSV.
**Rationale:** Describes the data aggregation and reporting function.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Maintainability/Storage)
- **Conflicts with:** None identified
---

[FR-008]: System Configuration and Maintenance
**Description**: A Master user and DigitalHome Technician shall be able to change the configuration of the system (e.g., change default parameter settings). The Technician shall be capable of starting and stopping operation of the DigitalHome System.
**Rationale:** Describes administrative functions for system setup and maintenance.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (User Authentication)
- **Conflicts with:** None identified
---

[FR-009]: Backup and Recovery Operations
**Description**: The system shall backup all system data (configuration, default parameter settings, planning, and usage data) on a daily basis. If the system fails, the recovery mechanism shall restore system data from the most recent backup.
**Rationale:** Describes the data protection and restoration function.
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Data Backup Architecture)
- **Conflicts with:** None identified
---

[FR-010]: Exception Handling
**Description**: All DigitalHome operations shall incorporate exception handling so that the system responds to a user with a clear, descriptive message when an error or an exceptional condition occurs. The system shall display user-friendly error messages for each class of error (authentication, input/data, communication, device offline), localized if needed; error scenario coverage must be validated during acceptance testing. Acceptance: Error messages available in English. Additional language support: [list] to be defined. Next action: Specify required localization scope per market.
**Rationale:** Describes the system's behavior during error conditions.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Usability)
- **Conflicts with:** None identified
---