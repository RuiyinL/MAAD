# Functional Requirements Results:
[FR-001]: Monitor Patient Vitals Periodically
**Description**: The system shall read patient factors (pulse, temperature, blood pressure, skin resistance) from analog devices on a periodic basis specified for each patient and store the factors in a database. Each factor reading: { patient_id: string, timestamp: ISO8601, pulse: int, temperature: float, blood_pressure: [int,int], skin_resistance: float } stored per-sample with configurable period in seconds. Data contract: temperature: float, °C, valid 25-45; pulse: int, 0-250 bpm; blood_pressure: [systolic:int, diastolic:int], 30-250/30-150; skin_resistance: float, in Ohms. JSON schema for per-sample vital explicitly noted. Schedule config format: {patient_id, period_seconds}. Storage model: DB table per-sample. [Next Action: Author: Add sample data schema with units/types, clarify sample trigger and DB structure.]

**Rationale:** Describes the core data acquisition and storage behavior of the patient monitoring system.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Performance), ASR-001 (Real-Time Scheduling)
- **Conflicts with:** None
---
[FR-002]: Alert on Safety Violation or Device Failure
**Description**: If a patient factor falls outside the specified safe range, or if an analog device fails, the system shall notify the nurses' station. Upon out-of-range factor or failure: display alert <alert_id> at nurse station within 3 seconds; alert content = { patient_id, factor, value, timestamp }. Acceptance criteria: The system shall log alert delivery and require nurse station user acknowledgment within 3 seconds of an out-of-range reading or device failure. Acceptance: System simulates factor out-of-range, alert received+acknowledged at station UI within 3 seconds; log entry written. Alert channel = HTTP API call to nurse station IP. [Next Action: Add explicit UI/API and simulated scenario test to requirements.]

**Rationale:** Describes the critical safety behavior and exception handling of the monitoring system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-002 (Safety)
- **Conflicts with:** None
---
[FR-003]: Control Traffic Light Cycle
**Description**: The system shall control traffic light units by emitting pulses to repeat a fixed cycle of phases (Stop/Stop, Stop/Go, Stop/Stop, Go/Stop) with specified durations. System state: while override active ('Hold'/'Change'), default cycle is completely suspended; manual override lockout after 10 minutes to prevent indefinite hold. Table defining all system states (Idle, Running, Override), inputs (Timer, Hold, Change), transition rules, and timeouts. [Next Action: Draft state transition diagram with input events.]

**Rationale:** Describes the primary control behavior of the traffic light system.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Hardware Interface)
- **Conflicts with:** FR-005 (Overseer Override)
---
[FR-004]: Configure Traffic Regime via Magnetic Card
**Description**: The system shall read a magnetic card containing an ASCII-encoded light regime and control the lights according to the encoded regime instead of the factory preset.

**Rationale:** Describes the configuration mechanism allowing flexibility in traffic light behavior.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (External Configuration)
- **Conflicts with:** None
---
[FR-005]: Overseer Traffic Light Override
**Description**: The system shall allow a traffic overseer to extend the current light phase by pressing a 'Hold' button or curtail it by pressing a 'Change' button. Overseer actions via 'Hold' or 'Change' temporarily suspend the default cycle; system resumes cycle after intervention ends. Manual override state takes precedence during activation. Manual override suspends default timer while active; returns to timer state after release or timeout. Override precedence: Manual override state takes precedence during activation. Post-override auto-resume policy: Returns to timer state after release or timeout. [Next Action: Document override priority and resumption logic.]

**Rationale:** Describes the manual intervention capability for the traffic system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003
- **Conflicts with:** FR-003 (Default Cycle)
---
[FR-006]: Regulate Home Heating Temperature
**Description**: The computer shall regulate the system to maintain room temperatures as set on control knobs, using oil-burning furnace and pump control.

**Rationale:** Describes the core control loop behavior of the heating system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Occupancy Logic)
- **Conflicts with:** None
---
[FR-007]: Implement Occupancy-Based Energy Saving
**Description**: The system shall set the temperature of an unoccupied room to 5 degrees below the knob setting and raise the temperature 30 minutes before occupancy is expected based on occupancy sensors. Acceptance: At least 95% of predicted occupancy events result in the room temperature rising to within 2°C of knob setting within 30 minutes of predicted use. Document prediction algorithm stub and test: For 100 occupancy events, 95% show temp increase within 2°C in 30 min; record prediction input sources for audit. [Next Action: Provide stub schema for occupancy model/inputs and list concrete test scenario.]

**Rationale:** Describes the energy optimization logic based on sensor input.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** None
---
[FR-008]: Control Sluice Gate Motor
**Description**: The system shall control the sluice gate motor using clockwise, anticlockwise, on, and off pulses based on operator commands or a fixed timer (open 10 mins every 3 hours).

**Rationale:** Describes the actuation behavior of the irrigation system.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Hardware Interface)
- **Conflicts with:** None
---
[FR-009a-1]: Manage Library Membership Enrollment
**Description**: The system shall enroll members. Stub schemas for membership record {member_id, name, enrollment_date, status}. Derived from FR-009a. [Next Action: Break into atomic requirements per action.]

**Rationale:** Describes the membership enrollment logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-009a-2]: Manage Library Membership Resignation
**Description**: The system shall resign members. Stub schemas for membership record {member_id, resignation_date, status}. Derived from FR-009a. [Next Action: Break into atomic requirements per action.]

**Rationale:** Describes the membership resignation logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009a-1
- **Conflicts with:** None
---
[FR-009a-3]: Manage Library Membership Fees
**Description**: The system shall pay fees for members. Stub schemas for membership record {member_id, fee_amount, payment_date}. Derived from FR-009a. [Next Action: Break into atomic requirements per action.]

**Rationale:** Describes the membership fee payment logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009a-1
- **Conflicts with:** None
---
[FR-009b-1]: Manage Library Borrowing
**Description**: The system shall allow borrowing for members. Loan schema {loan_id, member_id, book_id, borrow_date, due_date, return_date?}. Derived from FR-009b. [Next Action: Decompose to borrow/return and specify I/O contract.]

**Rationale:** Describes the lending borrow logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009a-1
- **Conflicts with:** None
---
[FR-009b-2]: Manage Library Returning
**Description**: The system shall allow returning for members. Loan schema {loan_id, member_id, book_id, return_date}. Derived from FR-009b. [Next Action: Decompose to borrow/return and specify I/O contract.]

**Rationale:** Describes the lending return logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009b-1
- **Conflicts with:** None
---
[FR-009c]: Detect Overdue Books
**Description**: The system shall track overdue books. Stub schemas for loan record. Derived from FR-009. Acceptance: For every loan not returned by due_date, status is flagged as 'overdue' with timestamp. Data format: {loan_id, due_date, status, timestamp}. [Next Action: Create test case and data field for overdue event.]

**Rationale:** Describes the overdue detection logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009b-1
- **Conflicts with:** None
---
[FR-009d]: Process Library Fines
**Description**: The system shall incur fines for overdue books. Stub schemas for fine record. Derived from FR-009. Loan overdue by >0 days auto-incurs fine entry {fine_id, loan_id, amount, date_assessed, paid:boolean}. [Next Action: Add atomic fine logic and stub schema.]

**Rationale:** Describes the fine processing logic of the library administration system.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009c
- **Conflicts with:** None
---
[FR-010]: Configure Automatic Lathe via Floppy Disk
**Description**: The system shall read dimensions/shape of bushes from one floppy disk file and lathe properties from a second floppy disk file to control the cutting tool accordingly.

**Rationale:** Describes the data-driven configuration behavior of the lathe controller.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (External Configuration)
- **Conflicts with:** None
---