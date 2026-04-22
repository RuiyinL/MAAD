# Non-Functional Requirements Results:
[NFR-001]: Prototype Environment Constraint  
**Description**: Simulated environment shall reproduce physical sensor timings within ±5% and match real device outputs within ±2%.  

**Quality Attributes**: Realism  

**Measurable Criteria (if provided)**: Defined simulation fidelity metrics (±5% timing variance, ±2% output accuracy).  
---  
[NFR-002]: Development Cost Minimization  
**Description**: The total cost of DigitalHome prototype components (sensors, controllers, gateway, server, tools) shall not exceed $5,000. Submit a BOM and cost report at project close.  

**Quality Attributes**: Cost Efficiency  

**Measurable Criteria (if provided)**: ≤$5,000 total component cost with BOM deliverable.  
---  
[NFR-003]: Gateway Transmission Range  
**Description**: The Gateway device shall operate up to a 1000-foot range for indoor transmission.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided)**: 1000 feet maximum range.  
---  
[NFR-004]: Daily Backup Schedule  
**Description**: The DigitalHome System will backup all system data on a daily basis.  

**Quality Attributes**: Reliability  

**Measurable Criteria (if provided)**: Daily backups with time configurable by technician.  
---  
[NFR-005]: Data Acquisition Rate  
**Description**: Sensor data acquisition: ≥10Hz per sensor, monitored in SRE logs, report if average rate <9Hz over any 1-hour window.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided)**: ≥10Hz sampling rate with alerting threshold.  
---  
[NFR-006]: UI Update Frequency  
**Description**: UI refresh rate: ≤2s, measured from event generation to visible update in frontend, 95th percentile; snapshot every 5 minutes.  

**Quality Attributes**: Performance  

**Measurable Criteria (if provided)**: ≤2 seconds refresh rate at 95th percentile.  
---  
[NFR-007]: Thermostat Sensitivity Range  
**Description**: The sensor part of the thermostat has a sensitivity range between 14ºF and 104ºF (-10ºC and 40ºC).  

**Quality Attributes**: Interoperability  

**Measurable Criteria (if provided)**: Operational range: 14–104°F/-10–40°C.  
---  
[NFR-008]: Standards Compliance  
**Description**: All requirements of ASHRAE 2010, sections 7/8/11; signed off by compliance officer in project review; test artifacts uploaded.  

**Quality Attributes**: Compliance  

**Measurable Criteria (if provided)**: Explicit sections and validation process.  
---  
[NFR-009]: Security Protocols  
**Description**: All auth events logged: {event_id, user_id, action, ip_addr, timestamp}, retention: 365d, rotation: 100MB.  

**Quality Attributes**: Security  

**Measurable Criteria (if provided)**: Structured auth logging with retention policy.  
---  
[NFR-010]: Failure Recovery  
**Description**: If the DigitalHome System fails, the recovery mechanism shall restore system data from the most recent backup.  

**Quality Attributes**: Reliability  

**Measurable Criteria (if provided)**: Recovery from last backup.  
---  
[NFR-011]: Error Handling  
**Description**: In pre-release usability test with ≥20 users, 90% must correctly resolve error using help text within one attempt; retain results as evidence. All usability test results (including failures) must be logged: {user_id, error, resolved,y/n, timestamp}, retained ≥2 years.  

**Quality Attributes**: Usability  

**Measurable Criteria (if provided)**: Usability success metric with evidence retention.  
---