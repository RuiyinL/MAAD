# Functional Requirements Results:
[FR-001]: Remote Device Control via Web  
**Description**: The DigitalHome System shall allow a web-ready computer, cell phone or PDA to control a home's temperature, humidity, lights, security, and the state of small appliances.  

**Rationale:** Describes user interaction behavior through web-enabled devices to manage household components.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002  
---  
[FR-002]: Web Server as Central Communication Hub  
**Description**: The communication center of the DigitalHome system shall be a DigitalHome home web server, through which a user shall be able极速飞艇168开奖官网结果 to monitor and control home devices and systems.  

**Rationale:** Defines the primary component for user-system interaction.  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001  
---  
[FR-003]: Gateway Wireless Communication  
**Description**: Each DigitalHome shall contain a master control device (the DigitalHome Gateway Device) that connects to the home’s broadband Internet connection and uses wireless communication to send and receive communication between the DigitalHome system and the home devices and systems.  

**Rationale:** Specifies function of the Gateway device enabling connectivity.  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-002  
---  
[FR-004]: Environmental Sensor/Controller Integration  
**Description**: The DigitalHome shall be equipped with various environmental controllers and sensors (temperature controller-sensors: thermostats, humidity controller-sensors: humidistats, contact sensors, security sound and light alarms, and power switches).  

**Rationale:** Enumerates device types handled by the system.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005, FR-007  
---  
[FR-005]: Thermostat Monitoring and Control  
**Description**: A DigitalHome user shall be able to read the temperature at a thermostat position and set the thermostat temperatures to between 60 °F and 80 °F, inclusive, at one degree increments.  

**Rationale:** Describes a specific interaction with temperature sensors/controllers.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
---  
[FR-006]: Thermostat Scheduling  
**Description**: Users can schedule up to 24 hourly settings per day per thermostat, each from 60-80°F.  

**Rationale:** Defines time-based automation behavior for temperature control.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005  
---  
[FR-015]: Thermostat Override Behavior  
**Description**: When user issues manual override, system must set temp/humidity immediately and persist setting until next scheduled time period boundary (per FR-006). Acceptance test: Set override, advance simulated clock, verify setting reverts at next period.  

**Rationale:** Defines measurable override behavior with test criteria.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-005  
---  
[FR-007]: Humidity Monitoring and Control  
**Description**: A DigitalHome user shall be able to read the humidity at a humidistat position and set the humidity level for a humidistat, from 30% to 60%, inclusive at 1% increments.  

**Rationale:** Describes interaction with humidity sensors/controllers.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
---  
[FR-008]: Security Alarm Activation  
**Description**: When a security breach occurs and a contact sensor is set OPEN, the alarm system shall be activated.  

**Rationale:** Specifies system response to security events.  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006  
---  
[FR-009]: Appliance State Management  
**Description**: The system shall be able to provide information about the state of a power switch (OFF or ON) and change the state of a power switch, in turn changing the state of an appliance. UI change event must include: {switch_id, previous_state, new_state, user_id, timestamp}; hardware state must match within ≤2s (measured via log correlation). If hardware state mismatches after UI event, system logs error, displays user alert, and retries once.  

**Rationale:** Defines control functions with error handling for state mismatches.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
---  
[FR-010]: Configuration Management by Master User  
**Description**: Master user may update only: {thermostat_default, humidity_default, ...}; changes rejected with ACCESS_DENIED if field not permitted; error output: {code, message, attempted_field}.  

**Rationale:** Specifies administrative functions with validation and error contract.  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-003  
---  
[FR-011]: Environmental Parameter Planning  
**Description**: For a given month and year, a user shall be able to create or modify a month plan that specifies for each day, for up to four daily time periods, environmental parameter settings (temperature, humidity, contact sensors and power switches). { day: YYYY-MM-DD, periods: [ { start_time: HH:MM, end_time: HH:MM, params: { temp: int [60-80], humidity: int [30-60], contacts: [OPEN|CLOSED], power: [ON|OFF] } } ] }. API will return {success: bool, errors:[{field,message}]} for all invalid plan input.  

**Rationale:** Describes planning capabilities with validation error contract.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006, FR-007  
---  
[FR-012]: Historical Reporting  
**Description**: For a given month and year in the past two years, DigitalHome shall provide a report containing daily average/maximum/minimum values of temperature/humidity and security breach timestamps. Reports must be downloadable in JSON and CSV; each call returns ≤1000 records; errors schema: {code,msg}.  

**Rationale:** Defines reporting functionality with output format and error handling.  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-005  
---  
[FR-013]: Account Management  
**Description**: The home web server shall establish and maintain DigitalHome User Accounts. User schema includes user_id, email, hashed_pw, roles[]; error response always {code,field,msg}.  

**Rationale:** Details user lifecycle management with schema and error contract.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002  
---  
[FR-014]: Backup Service Provision  
**Description**: The home web server shall provide backup service for user account information, user plans, and a home database. Backups must be restorable for any snapshot; quarterly restore test simulates failure -> restore within 10 minutes or alert SRE.  

**Rationale:** Specifies data backup behavior with RTO and validation protocol.  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-004  
---