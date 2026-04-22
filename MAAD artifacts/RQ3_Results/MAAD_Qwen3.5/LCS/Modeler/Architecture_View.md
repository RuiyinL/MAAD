## Architecture Summary & Quality-Attribute Analysis

The proposed architecture for the Reversible Lane Control System (RLCS) is a **Hierarchical Event-Driven Architecture** with a strong emphasis on **Defense-in-Depth Safety**. The system is structured around the physical topology (TMC → FCU → DCU) to satisfy ASR-001, ensuring commands flow strictly top-down. Status updates flow bottom-up via an event mechanism to meet FR-002 and NFR-002 (2-second update rate).

**Key Quality Attributes & Trade-offs:**
1.  **Safety (Critical):** Addressed by ASR-002 (Multi-Layer Safety Screening). Every command is validated at TMC, FCU, and DCU.
    *   *Trade-off:* Increased latency. Mitigated by strict latency budgets (≤4s total) and abort mechanisms (NFR-002).
2.  **Availability:** Addressed by ASR-003 (Degraded Mode). Field units (FCU/DCU) possess local logic and non-volatile memory (ASR-004) to operate independently if TMC fails.
    *   *Trade-off:* Complexity in state synchronization between central and field units.
3.  **Security:** Addressed by ASR-005 (Network Segmentation) and NFR-003 (SHA-256). A firewall separates the private RLCS network from external systems.
    *   *Trade-off:* Restricted external access (one-way data export only).
4.  **Performance:** NFR-002 mandates ≤2s status updates and ≤12s command response.
    *   *Risk:* Multi-layer screening consumes time. Tactics include optimized local validation and asynchronous logging.
5.  **Maintainability:** NFR-005 mandates COTS DB and Reporting. A layered architecture isolates persistence logic.

## Architectural Style & Rationale

**Primary Style: Hierarchical Control**
*   **Justification:** Directly implements ASR-001 (TSU > FCU > DCU). Prevents peer-to-peer unsafe commands. Matches physical infrastructure.
*   **Requirements:** ASR-001, FR-003, FR-009.

**Secondary Style: Event-Driven**
*   **Justification:** Required for real-time status updates (FR-002, FR-007) and Alarm Notifications (NFR-002 latency). Decouples field devices from the GUI.
*   **Requirements:** FR-002, FR-007, NFR-002.

**Tertiary Style: Layered (N-Tier)**
*   **Justification:** Supports NFR-005 (COTS DB, Reporting) and separation of concerns (GUI, Logic, Data).
*   **Requirements:** NFR-005, FR-008.

**Interaction:** The Hierarchical style governs the command path (Safety), while the Event-Driven style governs the status path (Performance/Usability). The Layered style organizes the software within the TMC nodes.

## Architecture Patterns & Tactics

**Patterns:**
1.  **Model-View-Controller (MVC):** Used in the Workstation GUI (FR-001, FR-002). Separates user input from status display.
2.  **Repository:** Manages access to the COTS Database (FR-005, NFR-005). Ensures data integrity and immutability of logs.
3.  **Broker/Proxy:** Field Controllers (FCU) act as brokers between TMC and DCUs (ASR-001).
4.  **Leader Election (Leasing):** Implements Single Operator Command Control (ASR-006). Only one active session holds the "command lease".

**Tactics:**
1.  **Replication (Availability):** Safety rules and config replicated to Non-Volatile Memory in FCU/DCU (ASR-003, ASR-004).
2.  **Heartbeat/Watchdog (Reliability):** Monitors process uptime (NFR-006) and device connectivity (FR-010).
3.  **Cryptographic Hashing (Security):** SHA-256 for integrity checks and passwords (NFR-003, ASR-004).
4.  **Firewall/DMZ (Security):** Enforces one-way data export (ASR-005, FR-006).
5.  **Timeout/Abort (Safety):** Commands abort if safety screening exceeds 4s (ASR-002).

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCase_Diagram
actor "Operator" as Operator
actor "SystemAdmin" as Admin
actor "ExternalSystem" as External
actor "FieldDevice" as Device

rectangle "RLCS System" {
  usecase "Authenticate User" as UC1
  usecase "Control Device" as UC2
  usecase "View Status" as UC3
  usecase "Acknowledge Alarm" as UC4
  usecase "Configure System" as UC5
  usecase "Export Status" as UC6
  usecase "View Logs" as UC7
  usecase "Manage Session" as UC8
}

Operator --> UC1
Operator --> UC2
Operator --> UC3
Operator --> UC4
Operator --> UC8

Admin --> UC1
Admin --> UC5
Admin --> UC7

External <-- UC6 : One-Way JSON

UC2 ..> UC1 : <<include>>
UC5 ..> UC1 : <<include>>
UC4 ..> UC3 : <<extend>>

note right of UC2
  Safety Validated
  Multi-Layer
end note

note left of UC6
  RFC-8259 JSON
  30s Interval
end note
}
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml Class_Diagram
class User {
  +id: int
  +username: string
  +passwordHash: string
  +role: Enum
  +login()
  +logout()
}

class Session {
  +id: int
  +userId: int
  +startTime: Timestamp
  +hasCommandControl: boolean
  +acquireControl()
  +releaseControl()
}

class Command {
  +id: int
  +type: Enum
  +targetDeviceId: int
  +status: Enum
  +timestamp: Timestamp
  +validate()
  +execute()
}

class Device {
  +id: int
  +type: Enum
  +status: Enum
  +location: string
  +updateStatus()
}

class SafetyRule {
  +id: int
  +condition: string
  +action: string
  +isViolated(cmd: Command): boolean
}

class LogEntry «immutable» {
  +id: int
  +type: Enum
  +message: string
  +timestamp: Timestamp
  +operatorId: int
}

class Config {
  +key: string
  +value: string
  +lastModified: Timestamp
}

class Alarm {
  +id: int
  +severity: Enum
  +isActive: boolean
  +acknowledge()
}

class FCU {
  +id: int
  +location: string
  +validateCommand(): boolean
}

class DCU {
  +id: int
  +parentId: int
  +executeCommand(): boolean
}

User "1" -- "0..*" Session
Session "1" -- "0..*" Command
Command "1" -- "1" Device
Command "1" -- "0..*" SafetyRule
Device "1" -- "0..*" LogEntry
FCU "1" -- "1..*" DCU
DCU "1" -- "1..*" Device

note right of LogEntry
  Append Only
  SHA-256 Integrity
end note

note left of Session
  Single Operator
  Leasing Mechanism
end note
@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml Object_Diagram
object op1 : User [Authenticate] {
  id := 101
  username := "J Doe"
  role := OPERATOR
}

object sess1 : Session [ManageSession] {
  id := 5001
  hasCommandControl := true
}

object cmd1 : Command [ControlDevice] {
  id := 9001
  type := OPEN_GATE
  status := VALIDATED
}

object dev1 : Device [ControlDevice] {
  id := 201
  status := CLOSED
  location := "I-15 NB"
}

object alarm1 : Alarm [AcknowledgeAlarm] {
  id := 301
  severity := CRITICAL
  isActive := true
}

op1 --> sess1
sess1 --> cmd1
cmd1 --> dev1
dev1 --> alarm1

note right of cmd1
  Scenario 1: 
  Command Execution
end note

note left of alarm1
  Scenario 2: 
  Alarm Notification
end note
@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml State_Diagram
[*] --> Issued : Operator Request

state "Safety Screening" as Screening {
  state "TMC Validate" as TMC
  state "FCU Validate" as FCU
  state "DCU Validate" as DCU
  TMC --> FCU : Pass
  FCU --> DCU : Pass
}

Issued --> Screening : Start
Screening --> Executing : All Pass
Screening --> Aborted : Fail/Timeout

Executing --> Completed : Device ACK
Executing --> Aborted : Device NACK

Aborted --> [*] : Log Error
Completed --> [*] : Log Success

note right of Screening
  Max Latency 4s
  ASR-002
end note

note left of Aborted
  Notify Operator
  < 2s
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml Activity_Diagram
start
:Operator Issues Command;
partition "Security" {
  :Verify Session Lease;
  if (Valid Lease?) then (Yes)
    :Hash Command (SHA-256);
  else (No)
    :Reject Command;
    stop
  endif
}
partition "TMC Safety" {
  :Validate Local Rules;
  if (Safe?) then (Yes)
    :Forward to FCU;
  else (No)
    :Abort & Log;
    stop
  endif
}
partition "FCU Safety" {
  :Validate Subordinate Rules;
  if (Safe?) then (Yes)
    :Forward to DCU;
  else (No)
    :Abort & Log;
    stop
  endif
}
partition "DCU Execution" {
  :Check Device Status;
  if (Known?) then (Yes)
    :Activate Device;
  else (No)
    :Abort & Log;
    stop
  endif
}
:Send Acknowledgement;
:Write Immutable Log;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram 

```plantuml
@startuml Sequence_Command
participant "Operator" as Op
participant "TMC Server" as TMC
participant "FCU" as FCU
participant "DCU" as DCU
participant "Device" as Dev

Op -> TMC : Issue Command
activate TMC
TMC -> TMC : Safety Check (Local)
TMC -> FCU : Forward Command
activate FCU
FCU -> FCU : Safety Check (Field)
FCU -> DCU : Forward Command
activate DCU
DCU -> DCU : Safety Check (Device)
DCU -> Dev : Execute
activate Dev
Dev --> DCU : ACK
DCU --> FCU : ACK
FCU --> TMC : ACK
TMC --> Op : Confirm
note right of TMC: Total Latency ≤ 4s
deactivate TMC
deactivate FCU
deactivate DCU
deactivate Dev
@enduml
```

```plantuml
@startuml Sequence_Alarm
participant "Device" as Dev
participant "DCU" as DCU
participant "FCU" as FCU
participant "TMC Server" as TMC
participant "GUI" as GUI

Dev --> DCU : Fault Detected
activate DCU
DCU -> FCU : Alarm Event
activate FCU
FCU -> TMC : Alarm Event
activate TMC
TMC -> TMC : Log Alarm
TMC -> GUI : Display Alarm (≤2s)
activate GUI
GUI -> GUI : Audible Alert
GUI --> TMC : Acknowledge
TMC --> FCU : Silence
FCU --> DCU : Silence
deactivate DCU
deactivate FCU
deactivate TMC
deactivate GUI
note left of GUI: NFR-002 Latency
@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml Collaboration_Command
object "Operator" as Op
object "TMC Server" as TMC
object "FCU" as FCU
object "DCU" as DCU
object "Device" as Dev

Op -- TMC : 1
TMC -- FCU : 2
FCU -- DCU : 3
DCU -- Dev : 4

Op -> TMC : 1.1 Issue Command
TMC -> TMC : 1.2 Validate
TMC -> FCU : 2.1 Forward
FCU -> FCU : 2.2 Validate
FCU -> DCU : 3.1 Forward
DCU -> DCU : 3.2 Validate
DCU -> Dev : 4.1 Execute
Dev --> DCU : 4.2 ACK
DCU --> FCU : 3.3 ACK
FCU --> TMC : 2.3 ACK
TMC --> Op : 1.3 Confirm

note bottom: Scenario 1: Command Execution
@enduml
```

```plantuml
@startuml Collaboration_Alarm
object "Device" as Dev
object "DCU" as DCU
object "FCU" as FCU
object "TMC Server" as TMC
object "GUI" as GUI

Dev -- DCU : 1
DCU -- FCU : 2
FCU -- TMC : 3
TMC -- GUI : 4

Dev --> DCU : 1.1 Fault
DCU -> FCU : 2.1 Alarm
FCU -> TMC : 3.1 Alarm
TMC -> TMC : 3.2 Log
TMC -> GUI : 4.1 Display
GUI --> TMC : 4.2 Ack
TMC -> FCU : 3.3 Silence
FCU -> DCU : 2.3 Silence

note bottom: Scenario 2: Alarm Notification
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml Package_Diagram
package "UI Layer" {
  [Workstation GUI]
}
package "Logic Layer" {
  [Command Engine]
  [Safety Validator]
  [Session Manager]
}
package "Persistence Layer" {
  [Log Repository]
  [Config Repository]
}
package "Field Interface" {
  [FCU Proxy]
  [DCU Protocol]
}
package "Security" {
  [Auth Module]
  [Crypto Util]
}

"UI Layer" --> "Logic Layer"
"Logic Layer" --> "Persistence Layer"
"Logic Layer" --> "Field Interface"
"Logic Layer" --> "Security"
"Field Interface" --> "Security"

note right of "Logic Layer"
  Multi-Layer Safety
  ASR-002
end note
note left of "Security"
  SHA-256
  NFR-003
end note
@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml Component_Diagram
component "AuthComponent" {
  port "Login" as P1
  port "Validate" as P2
}
component "CommandEngine" {
  port "Issue" as P3
  port "Route" as P4
}
component "SafetyValidator" {
  port "Check" as P5
}
component "Logger" {
  port "Write" as P6
}
component "DBAdapter" {
  port "Query" as P7
}
component "FieldProxy" {
  port "Send" as P8
  port "Receive" as P9
}

P1 --> AuthComponent
AuthComponent --> CommandEngine : Session Valid
CommandEngine --> SafetyValidator : Pre-Check
SafetyValidator --> FieldProxy : Safe Command
FieldProxy --> Logger : Audit Trail
Logger --> DBAdapter : Persist
DBAdapter --> Logger : Confirm

note right of SafetyValidator
  Implements ASR-002
  Distributed Logic
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml Deployment_Diagram
node "TMC Site" {
  node "Workstation" {
    component "GUI Client"
  }
  node "App Server" {
    component "TMC Core"
    component "Database"
  }
}
node "Firewall" {
  component "Data Diode"
}
node "External Network" {
  component "External Receiver"
}
node "Field Site North" {
  node "FCU North" {
    component "FCU Logic"
  }
  node "DCU 1-5" {
    component "DCU Logic"
  }
  node "Devices" {
    component "Gate/Sensor"
  }
}

"Workstation" -- "App Server" : LAN
"App Server" -- "Firewall" : Secure Link
"Firewall" -- "External Network" : One-Way
"App Server" -- "FCU North" : WAN (Private)
"FCU North" -- "DCU 1-5" : Serial/Ethernet
"DCU 1-5" -- "Devices" : I/O

note right of "FCU North"
  Degraded Mode
  ASR-003
end note
note left of "Firewall"
  Network Segmentation
  ASR-005
end note
@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml Container_Diagram
rectangle "System Boundary" {
  container "Web Client" "HTML/JS" "Operator Interface" {
    component "Status Display"
    component "Command Panel"
  }
  container "App Server" "Java/C++" "Core Logic & Routing" {
    component "Safety Engine"
    component "Session Mgr"
  }
  container "Database" "Oracle/Postgres" "Persistence & Logs" {
    component "Log Tables"
    component "Config Tables"
  }
  container "Field Controller" "Embedded" "FCU/DCU Logic" {
    component "Local Safety"
    component "Device Driver"
  }
  container "External API" "JSON/HTTPS" "Data Export" {
    component "Status Publisher"
  }
}

"Web Client" --> "App Server" : HTTPS
"App Server" --> "Database" : SQL
"App Server" --> "Field Controller" : TCP/Serial
"App Server" --> "External API" : Push JSON

note right of "Field Controller"
  Non-Volatile Memory
  ASR-004
end note
note left of "External API"
  RFC-8259 JSON
  FR-006
end note
@enduml
```