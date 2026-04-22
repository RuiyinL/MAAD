# Functional Requirements Results:
[FR-001]: Patient Monitoring Data Acquisition  
**Description**: The program shall read patient factors (pulse, temperature, blood pressure, skin resistance) from analog devices periodically, with the period specified per patient.  

**Rationale:** Describes a core system behavior (data acquisition) triggered by time intervals.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-002]: Patient Data Storage  
**Description**: The program shall store patient factors in a database.  

**Rationale:** Specifies a data-handling function (persisting measurements).  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001  
- **Conflicts with:** None  
---  

[FR-003]: Safe Range Configuration  
**Description**: Medical staff shall specify safe ranges for each patient's physiological factors.  

**Rationale:** Defines a user-driven configuration task.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-004]: Anomaly Notification  
**Description**: Notify nurses' station using HL7 ORU^R01 with fields {patient_id, factor, value, safe_range, timestamp, device_status}. Retry up to 3 times if NACK received; escalate to audible alarm if not delivered in 2 seconds.  

**Rationale:** Describes an alerting behavior triggered by specific conditions with explicit payload definition.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001, FR-003  
- **Conflicts with:** None  
---  

[FR-005]: Facial Recognition Access Control  
**Description**: The system shall, upon face capture, compute a 128-float feature vector using FaceNet, compare to authorized vectors, grant access if any authorized cosine distance ≤0.72, otherwise deny and log the event. Log format: {user_id, timestamp, match_score, access_granted}.  

**Rationale:** Specifies an authentication workflow (capture→compare→authorize) with explicit outcomes.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-006]: Turnstile Payment Enforcement  
**Description**: The system shall prevent zoo entry unless two coins are paid and shall grant entry upon payment.  

**Rationale:** Defines access control logic based on payment verification.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-007]: Room Temperature Regulation  
**Description**: The system shall maintain room temperatures as set on control knobs, reducing temperatures by 5 degrees in unoccupied rooms.  

**Rationale:** Describes real-time environmental control behavior.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-008]: Occupancy-Based Temperature Adjustment  
**Description**: The system shall raise room temperatures 30 minutes before expected occupancy using sensor data.  

**Rationale:** Specifies predictive control based on sensor inputs.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-007  
- **Conflicts with:** None  
---  

[FR-009]: PC Configuration Display  
**Description**: The program shall, upon user request, display: (1) current configuration of BIOS, RAM, disks, and peripherals as a table [Component, Status]; (2) IRQ and I/O port assignments as a table [IRQ/Port, Assigned Device]. Accept request as user command from keyboard.  

**Rationale:** Defines an on-demand information retrieval and presentation function with explicit output formats.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-010]: Traffic Light Cycle Control  
**Description**: The system shall cycle traffic lights through four phases: 50s both Stop, 120s Stop/Go, 50s both Stop, 120s Go/Stop.  

**Rationale:** Specifies a timed sequence of hardware operations.  

**Dependencies** / **极速赛车开奖直播开奖结果🔸我该如何进行极速赛车开奖直播开奖结果🔸Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-011]: Vehicle Speed/Distance Calculation  
**Description**: The system shall compute current speed and total miles traveled using wheel-rotation pulses and update visible counters.  

**Rationale:** Describes real-time metric computation from hardware inputs.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-012]: Sluice Gate Periodic Operation  
**Description**: The system shall hold a sluice gate fully open for 10 minutes every 3 hours and keep it closed otherwise.  

**Rationale:** Defines a time-based mechanical control sequence.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-013]: Vehicle Classification Reporting  
**Description**: The system shall generate hourly traffic reports with vehicle type (motorbike/car/commercial), time/date per vehicle, and cumulative totals.  

**Rationale:** Specifies data aggregation and reporting based on sensor patterns.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-014]: Package Routing Control  
**Description**: The system shall route packages to destination bins by setting switches when no package is present and report misroutes.  

**Rationale:** Describes material handling logic with error notification.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---  

[FR-015]: Shuttle Movement Control  
**Description**: The system shall move a shuttle between airport areas, stopping for 60 seconds at each end, while adhering to speed/acceleration limits.  

**Rationale:** Defines a motion control sequence with timing constraints.  

**Dependencies** / **Conflicts**:  
- **Depends on:** None  
- **Conflicts with:** None  
---