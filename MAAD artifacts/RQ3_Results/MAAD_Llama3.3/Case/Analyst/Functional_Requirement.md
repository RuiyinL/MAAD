# Functional Requirements Results:
[FR-001]: Patient Monitoring
**Description**: Inputs: JSON object {patient_id: string, timestamp: RFC3339 datetime, pulse: int [0-250], temp: float [30.0-45.0], bp: {sys:int, dia:int}, skin_resist: float}. Output: Write record to [table: patient_vitals]. 
**Rationale:** This requirement describes a behavior of the system, specifically the input-output transformation of reading and storing patient data.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Notification of Nurses' Station
**Description**: When reading is out-of-range or device error, emit notification: JSON {patient_id, factor, value, threshold, timestamp, error_code: enum {DEVICE_FAIL, OUT_OF_RANGE}} via secure REST POST to nurses' station UI; must be acknowledged within 2 minutes. HTTP POST /alert { ... } returns 200 OK on receipt/ack, 500 on error.
**Rationale:** This requirement describes a function of the system, specifically the action of notifying the nurses' station in case of an emergency.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-003]: Secure Door Control
**Description**: System shall use ISO/IEC 19794-5-compliant face recognition; logs shall be stored as per schema {attempt_id, user_id, method: enum {face, admin_override}, timestamp, outcome}; after 3 failures, require two-factor admin override at local console.
**Rationale:** This requirement describes a function of the system, specifically the control of a secure door based on facial recognition.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-004]: Turnstile System Operation
**Description**: System shall only unlock when two consecutive ISO-coin-type-XYZ coins inserted within 10s and validated. If invalid, display red/error LED and log {'event':'invalid_coin','coin_id':string,'timestamp':datetime,'reason':string}.
**Rationale:** This requirement describes a behavior of the system, specifically the operation of the turnstile system.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-005]: Home Heating System Regulation
**Description**: Control command JSON {room_id, action:open|close|hold, timestamp}. Error handling for lost sensor/control connection.
**Rationale:** This requirement describes a function of the system, specifically the regulation of the home heating system.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-006]: Configuration Display
**Description**: User selects config category from menu; system displays {BIOS, RAM, disk, peripherals} as JSON table. User exits via ESC.
**Rationale:** This requirement describes a function of the system, specifically the display of configuration information.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-007]: Traffic Light Control
**Description**: Pulse signal spec: {unit_id:int, signal_type:R|G, duration_ms:int, timestamp}.
**Rationale:** This requirement describes a behavior of the system, specifically the control of traffic lights.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-008]: Speedometer and Odometer Control
**Description**: The computer must use the pulses from the car's rear wheel to set the current speed and total number of miles traveled in the two visible counters on the car fascia.
**Rationale:** This requirement describes a function of the system, specifically the control of the speedometer and odometer.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-009]: Library Administration
**Description**: Derived from FR-009. Manage library membership.
**Rationale:** This requirement describes a function of the system, specifically the administration of library membership.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-010]: Library Administration
**Description**: Derived from FR-009. Allow book borrowing/return.
**Rationale:** This requirement describes a function of the system, specifically the borrowing and returning of books.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[FR-011]: Library Administration
**Description**: Derived from FR-009. Track and impose fines for overdue books.
**Rationale:** This requirement describes a function of the system, specifically the tracking and imposition of fines for overdue books.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[FR-012]: Library Administration
**Description**: Derived from FR-009. Generate management reports.
**Rationale:** This requirement describes a function of the system, specifically the generation of management reports.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** None
---
[FR-013]: Indoor Court Management
**Description**: A computer system is needed to manage general and 'indoors' subscriptions, operate the lights, and manage billing and receipts for lighting.
**Rationale:** This requirement describes a function of the system, specifically the management of an indoor court.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-014]: Text Analysis
**Description**: A system is needed to analyze the language of a text, including the main text, frontispiece, general prologue, and marginal notes.
**Rationale:** This requirement describes a function of the system, specifically the analysis of a text.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-015]: Stream Editor
**Description**: A stream editor is to be built to support simple editing operations on ASCII text files.
**Rationale:** This requirement describes a function of the system, specifically the support of editing operations.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-016]: Lathe Controller
**Description**: An automatic lathe is a computer-controlled metal-working tool that makes metal parts by cutting or drilling.
**Rationale:** This requirement describes a function of the system, specifically the control of a lathe.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---