# Functional Requirements Results:

[FR-001]: Capture and read ICU patient vital factors periodically  
**Description**: Each patient is monitored by an analog device which measures factors such as pulse, temperature, blood pressure, and skin resistance. The program reads these factors on a periodic basis (specified for each patient).  
**Rationale:** Describes system behavior for acquiring patient data on a schedule.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-002
---

[FR-002]: Store ICU patient factors in a database  
**Description**: The program reads these factors on a periodic basis (specified for each patient) and stores the factors in a database.  
**Rationale:** Defines a data persistence function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-003
- **Conflicts with:** NFR-004
---

[FR-003]: Maintain per-patient safe ranges for monitored factors  
**Description**: For each patient, safe ranges for each factor are also specified by medical staff.  
**Rationale:** Specifies configuration data that drives later decisions/alerts.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None specified
---

[FR-004]: Notify nurses’ station on out-of-range factor  
**Description**: If a factor falls outside a patient's safe range ... the nurses' station is notified.  
**Rationale:** Defines an alerting action triggered by monitored data.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003
- **Conflicts with:** None specified
---

[FR-005]: Notify nurses’ station on analog device failure  
**Description**: ... or if an analog device fails, the nurses' station is notified.  
**Rationale:** Defines fault detection/handling behavior and alerting.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None specified
---

[FR-006]: Capture face video stream for door admission attempts  
**Description**: The face of each successive person desiring admission is captured in a video stream.  
**Rationale:** Specifies an input acquisition function.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005
- **Conflicts with:** NFR-006
---

[FR-007]: Compare captured facial features against cleared-entry database  
**Description**: ... and the features are compared with entries in a database of the features of people who have been cleared for entry.  
**Rationale:** Defines core verification/matching behavior for access control.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, NFR-005
- **Conflicts with:** None specified
---

[FR-008]: Control secure door access based on facial recognition result  
**Description**: A secure door is to be controlled by a computer that recognises facial features.  
**Rationale:** States the controlling function of the system for physical access.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-007, NFR-005
- **Conflicts with:** None specified
---

[FR-009]: Operate zoo turnstile coin and barrier hardware via two computer ports  
**Description**: The zoo has bought a small turnstile system ... that can be connected to two ports of a small computer. Our job is to build the software to operate the turnstile system.  
**Rationale:** Specifies system behavior to interface with/operate attached hardware.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006
- **Conflicts with:** None specified
---

[FR-010]: Enforce payment rule: prevent entry without two coins  
**Description**: First, no visitor should be able to enter the zoo without having paid the entry price (which is two coins).  
**Rationale:** Defines a business rule controlling admission.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** FR-011
---

[FR-011]: Permit entry after payment of two coins  
**Description**: Second, any visitor who has paid the two coins should be allowed to enter.  
**Rationale:** Defines the complementary admission rule to FR-010.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009
- **Conflicts with:** FR-010
---

[FR-012]: Maintain room temperature to knob setting in heating system  
**Description**: The computer must regulate the behaviour of the system to maintain room temperatures as set on the control knobs.  
**Rationale:** Defines the main closed-loop control function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, FR-014, FR-015
- **Conflicts with:** FR-016
---

[FR-013]: Read room temperature sensors and control radiator valves  
**Description**: Each room has a temperature sensor and ... one on-off computer-controlled radiator valve.  
**Rationale:** Defines sensor input and actuator output functions needed for control.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006
- **Conflicts with:** None specified
---

[FR-014]: Support manual furnace on/off from control panel  
**Description**: There is a control panel at which the controller can be commanded manually to turn the furnace on or off.  
**Rationale:** Defines manual control interaction.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017
- **Conflicts with:** FR-012
---

[FR-015]: Display system state and malfunctions on heating control panel  
**Description**: ... the panel also provides a display that indicates the system state and any malfunction.  
**Rationale:** Specifies a user-facing status and fault reporting function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017
- **Conflicts with:** None specified
---

[FR-016]: Apply economy mode for unoccupied rooms (5° below setting)  
**Description**: For economy, the temperature of an unoccupied room should be 5 degrees below the knob setting.  
**Rationale:** Defines conditional control behavior based on occupancy.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-018, FR-012
- **Conflicts with:** FR-012
---

[FR-017]: Detect and report heating system malfunctions  
**Description**: ... display that indicates the system state and any malfunction.  
**Rationale:** Requires malfunction detection/reporting behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-015
- **Conflicts with:** None specified
---

[FR-018]: Use occupancy sensors to anticipate use and preheat 30 minutes before expected occupancy  
**Description**: The system should use information from the occupancy sensors to anticipate room use, starting to raise the temperature 30 minutes before occupancy is expected.  
**Rationale:** Defines predictive control behavior using occupancy input.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013, NFR-007
- **Conflicts with:** FR-014
---

[FR-019]: Display PC installed components configuration on request  
**Description**: A program is to be developed to display the configuration of currently installed components – BIOS, RAM and disk storage, peripheral devices, etc – in a PC. The program operates when the PC user enters a request at the keyboard.  
**Rationale:** Describes a user-triggered reporting function.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021
- **Conflicts with:** None specified
---

[FR-020]: Display current assignment of IRQs and I/O ports  
**Description**: The program must also display the current assignment of IRQs and input-output ports.  
**Rationale:** Specific reporting behavior for hardware resource mapping.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019
- **Conflicts with:** None specified
---

[FR-021]: Allow user to select reported information and terminate execution  
**Description**: The user can select the information to be reported, and can terminate execution of the program.  
**Rationale:** Defines user interaction flows and options.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-019
- **Conflicts with:** None specified
---

[FR-022]: Control one-way roadworks light units via pulses and guises  
**Description**: The computer controls the lights by emitting Pulses and Guises, to which the units respond by turning the lights on and off. Each unit has a Stop light and a Go light.  
**Rationale:** Defines actuator control behavior with specified signal mechanism.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006
- **Conflicts with:** FR-024, FR-025
---

[FR-023]: Execute fixed 4-phase timing cycle for roadworks lights  
**Description**: The regime for the lights repeats a fixed cycle of four phases: 50s both Stop; 120s one Stop other Go; 50s both Stop; 120s swapped; repeat.  
**Rationale:** Defines exact control sequencing and timing behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, NFR-001
- **Conflicts with:** FR-024, FR-025, FR-026
---

[FR-024]: Provide add-on display module showing Stop/Go states using shared RPulse/GPulse events  
**Description**: The one-way traffic light system now needs a little display ... add the display ... as a separate module. The new module will share the RPulse and GPulse events of the existing system.  
**Rationale:** Defines an extension function and integration mechanism.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, ASR-007
- **Conflicts with:** None specified
---

[FR-025]: Support regime configuration via magnetic card reader (ASCII-encoded regime)  
**Description**: In a new design ... incorporated a magnetic card reader. The regime is encoded on the card as a simple ASCII text. The computer reads the card and controls the lights accordingly.  
**Rationale:** Defines a configuration input and resulting control behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, NFR-008
- **Conflicts with:** FR-023
---

[FR-026]: Support traffic overseer override via Hold/Change buttons  
**Description**: ... traffic overseer ... can override ... equipped with two buttons marked 'Hold' and Change'. The overseer can extend the current phase ... Hold ... or curtail it ... Change.  
**Rationale:** Defines manual override control inputs and behaviors.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-022, ASR-008
- **Conflicts with:** FR-023, FR-025
---

[FR-027]: Compute and display car speed and total miles using wheel pulses  
**Description**: One rear wheel generates pulses ... computer can detect these pulses and must use them to set the current speed and total number of miles travelled in the two visible counters.  
**Rationale:** Input processing and output display update behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009, NFR-001
- **Conflicts with:** None specified
---

[FR-028]: Share counter registers between computer and visible display  
**Description**: The underlying registers of the counters are shared by the computer and the visible display.  
**Rationale:** Specifies interaction pattern between control logic and hardware display.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009
- **Conflicts with:** None specified
---

[FR-029]: Administer lending library memberships and borrowing privileges  
**Description**: A system is needed to administer a lending library. Membership is required for borrowing books, but not for reading them on the library premises.  
**Rationale:** Defines membership and privilege behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-034
- **Conflicts with:** None specified
---

[FR-030]: Support ordering books and obtaining them from associated libraries  
**Description**: Books may be ordered and can be obtained from associated libraries.  
**Rationale:** Defines inter-library ordering and fulfillment behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-031]: Assess fines for overdue books  
**Description**: Overdue books incur fines.  
**Rationale:** Defines penalty computation/assignment behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-032A]: Generate overdue books listing report  
**Description**: Derived from FR-032. System generates overdue books listing (schema: {title: String, borrower: String, due_date: Date (YYYY-MM-DD), fine: Currency (USD)}), triggered daily at 3am; sample output file appended. [Next action: Supply schema and a test-cased sample report.]  
**Rationale:** Defines a specific report output with fields and trigger.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-032B]: Generate inventory report  
**Description**: Derived from FR-032. System generates inventory report. Fields: {book_id: String, title: String, status: Enum[Available, Borrowed], location: String}. [Next action: Document inventory report schema/fields.]  
**Rationale:** Defines a distinct management report function (inventory).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-032C]: Generate borrower history report  
**Description**: Derived from FR-032. System generates borrower history report. Fields: {borrower: String, book_id: String, title: String, borrow_date: Date, return_date: Date, fine: Currency}. [Next action: Add field/type/schema and example output for borrower history.]  
**Rationale:** Defines a distinct management report function (borrower history).  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-033]: Enforce library membership acquisition and exercise rules  
**Description**: It is required to restrict the way library membership is acquired and exercised. The membership rules must be enforced ... privileges and obligations ... enrolling, resigning, paying fees, and similar matters.  
**Rationale:** Defines rule enforcement behavior across membership lifecycle.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-029
- **Conflicts with:** None specified
---

[FR-034]: Control sluice gate on fixed schedule (open 10 min per 3 hours)  
**Description**: ... gate should be held in the fully open position for ten minutes in every three hours and otherwise kept in the fully closed position.  
**Rationale:** Specifies time-based control behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-035, FR-036, NFR-001
- **Conflicts with:** FR-037
---

[FR-035]: Drive sluice motor via clockwise/anticlockwise/on/off pulses  
**Description**: The screws are driven by a small motor, which can be controlled by clockwise, anticlockwise, on and off pulses. The connection ... consists of four pulse lines for motor control.  
**Rationale:** Defines actuator command behaviors and interface.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006
- **Conflicts with:** None specified
---

[FR-036]: Read sluice gate top/bottom travel sensors to detect fully open/shut  
**Description**: There are sensors at the top and bottom of the gate travel ... The connection ... consists of ... two status lines for the gate sensors.  
**Rationale:** Defines sensor input acquisition for control/state.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006
- **Conflicts with:** None specified
---

[FR-037]: Provide operator-commanded sluice gate raise/lower mode  
**Description**: A computer system is needed to raise and lower the sluice gate in response to the commands of an operator ... and a status line for each class of operator command.  
**Rationale:** Specifies an interactive control mode responding to operator commands.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-035, FR-036, ASR-008
- **Conflicts with:** FR-034
---

[FR-038]: Monitor narrow one-way street traffic using four sensor tubes and clock  
**Description**: The traffic ... is to be monitored. Four sensor tubes ... connected to a computer equipped with a time-of-day clock.  
**Rationale:** Defines sensor-based monitoring and time stamping capability.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** None specified
---

[FR-039]: Classify passing vehicles by sensor activation patterns  
**Description**: When a car passes ... pattern ... A motorbike will activate only one lower sensor and one upper sensor ... vehicle types to be distinguished are motorbikes, cars and commercial delivery vehicles with three or more axles.  
**Rationale:** Defines classification logic based on sensor sequence.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-038
- **Conflicts with:** None specified
---

[FR-040]: Produce traffic report with per-vehicle lines and hourly cumulative totals  
**Description**: The report has a line for each passing vehicle, showing the date and time, and the vehicle type; it also has a cumulative total for each type, printed hourly.  
**Rationale:** Defines reporting outputs and periodic aggregation.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-038, FR-039
- **Conflicts with:** None specified
---

[FR-041]: Provide command-line editor to maintain party plan (parties, guests, invitations)  
**Description**: They want a simple editor ... party plan ... list of parties, a list of guests, and a note of who's invited to each party. The editor will accept command-line text input ... DOS or Unix style ... creating and editing it.  
**Rationale:** Defines CRUD editing functionality and interface style.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-009
- **Conflicts with:** None specified
---

[FR-042]: Generate correspondent communication report (counts and lengths)  
**Description**: The report contains a line for each ... correspondent's name, how many days the report covers, the number of messages received from the correspondent and their maximum and average lengths, and the same information for the messages sent to the correspondent by Fred. ‘Maximum and average lengths’ are calculated in characters, per correspondent, over the report interval (default: last 7 days). Report row: {name: string, days: int, rec_count: int, rec_max_len: int, rec_avg_len: float, sent_count: int, sent_max_len: int, sent_avg_len: float}. [Next action: Attach schema/field list to the requirement.]  
**Rationale:** Defines report generation and required computed metrics.  
**Dependencies** / **Conflicts**:
- **Depends on:** None specified
- **Conflicts with:** None specified
---

[FR-043]: Control package router switches to route packages to destination bins  
**Description**: ... build the controlling computer ... route packages to their destination bins by setting the switches appropriately ... switches that the computer can flip (when no package is present between the incoming and outgoing pipes).  
**Rationale:** Defines real-time control behavior for routing via actuated switches.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-010, NFR-001
- **Conflicts with:** None specified
---

[FR-044]: Obey operator commands for package routing system  
**Description**: ... controlling computer to obey the operator's commands ...  
**Rationale:** Defines interactive command handling.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008
- **Conflicts with:** None specified
---

[FR-045]: Detect and report misrouted packages with message display  
**Description**: A misrouted package may be routed to any bin, an appropriate message being displayed ... and ... report misrouted packages.  
**Rationale:** Defines exception handling and operator feedback.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-043
- **Conflicts with:** None specified
---

[FR-046]: Control airport shuttle to shuttle continuously between two rest positions and dwell 60s  
**Description**: ... control the shuttle ... moves continually backwards and forwards ... stopping for 60 seconds in each area to allow passengers to embark and disembark.  
**Rationale:** Defines required motion pattern and dwell timing.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-047, NFR-001
- **Conflicts with:** NFR-010
---

[FR-047]: Read position sensor (0..9999) and set motor/brake states directly  
**Description**: The control computer has direct access to the position sensor state and can set the motor and brake states directly.  
**Rationale:** Defines key IO functions for closed-loop control.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009
- **Conflicts with:** None specified
---

[FR-048]: Optimize shuttle journey time subject to comfort/wear limits  
**Description**: The journey should be as fast as possible, subject to certain limits on the speed, acceleration and deceleration ... comfortable ride ... avoid excessive wear.  
**Rationale:** Defines control objective with constraints.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-046, FR-047, NFR-010
- **Conflicts with:** FR-046
---

[FR-049]: Display 32 measured lab voltages as columns and compute average  
**Description**: The computer must maintain a display showing the 32 voltages as columns side by side on the screen. It must also display the average voltage over all the points.  
**Rationale:** Defines continuous visualization and computed summary.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-050, NFR-001
- **Conflicts with:** None specified
---

[FR-050]: Read A/D register values for 32 measurement points (1–32)  
**Description**: ... voltages are measured at 32 points ... communicated ... by analog-digital devices. The devices convert the voltages into register values that are directly accessible to the computer ... identified by integer values 1-32.  
**Rationale:** Defines hardware input acquisition and addressing.  
**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009
- **Conflicts with:** None specified
---

[FR-051]: Perform lexical analysis and output token records (type and value)  
**Description**: The lexical analyser must recognise tokens ... integers, floating-point numbers, identifiers, comments and so on - and produce an output stream in which each token appears as a separate record with a field for the token type and a field for the token value.  
**Rationale:** Specifies transformation from input text to token stream.  
**Dependencies** / **Conflicts**:
- **Depends on:** None specified
- **Conflicts with:** None specified
---

[FR-052]: Stream editor to execute ordered global find-and-replace operations from command file  
**Description**: A stream editor ... operations ... given in a command file ... each operation being a simple global find-and-replace ... performed in the order in which they appear in the command file.  
**Rationale:** Defines batch processing function with deterministic ordering.  
**Dependencies** / **Conflicts**:
- **Depends on:** None specified
- **Conflicts with:** None specified
---

[FR-053]: Tennis club: manage subscriptions (general and indoors) and rules for indoor game eligibility  
**Description**: 'Indoors' members pay ... An indoor game must include at least one indoors member. A computer system is needed: to manage general and 'indoors' subscriptions.  
**Rationale:** Defines membership management and eligibility rule enforcement.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-054, FR-055
- **Conflicts with:** None specified
---

[FR-054]: Control court entrance lock using member magnetic cards  
**Description**: 'Indoors' members are issued with magnetic cards. The court entrance lock ... can read these cards. To use the indoor court a member inserts the card into the lock and gains entry.  
**Rationale:** Defines physical access control function with card input.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005
- **Conflicts with:** None specified
---

[FR-055]: Control lighting via control box; accept desired playing time; switch lights on for that duration  
**Description**: ... card is inserted into the lighting control box and the desired playing time is entered. The lights then come on and remain on for that length of time.  
**Rationale:** Defines timed actuator control behavior.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-056, NFR-001
- **Conflicts with:** None specified
---

[FR-056]: Bill lighting cost to an indoors member included in the game; manage billing and receipts  
**Description**: The lighting cost is billed to an 'indoors' member included in the game ... manage the billing and receipts for lighting.  
**Rationale:** Defines billing allocation and financial record handling.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-053, FR-055
- **Conflicts with:** None specified
---

[FR-057]: Enter full text of rare book by keyboard for analysis (all parts)  
**Description**: ... every part of the text of the whole book must be communicated to the computer by keyboard.  
**Rationale:** Defines data entry/acquisition function due to OCR limitation.  
**Dependencies** / **Conflicts**:
- **Depends on:** None specified
- **Conflicts with:** None specified
---