# Architecture Summary & Quality-Attribute Analysis

## Proposed Architecture Summary

The Gemini Observatory Control System requires a **Distributed Layered Architecture with Event-Driven Elements**. The system is organized into four primary layers:

1. **User Interface Layer** - Remote/local operator consoles, web interfaces
2. **Observation Control System (OCS) Layer** - Command coordination, scheduling, sequencing
3. **Instrument Object Controller (IOC) Layer** - Real-time hardware control, EPICS-based
4. **Hardware/Safety Layer** - Physical instruments, detectors, safety interlocks

This architecture supports distributed remote operations (ASR-001), real-time control at IOC level (ASR-009), and modular subsystem independence (ASR-008).

## Quality Attribute Analysis

| Quality Attribute | Key Requirements | Architectural Risks | Trade-offs |
|------------------|------------------|---------------------|------------|
| **Security** | NFR-001, ASR-001 | Remote access increases attack surface | TLS overhead vs. security |
| **Performance** | NFR-002, NFR-003, NFR-009 | Network latency for remote ops | Local caching vs. data freshness |
| **Reliability** | NFR-005, NFR-018 | Distributed failure modes | Redundancy vs. complexity |
| **Safety** | NFR-007, ASR-006 | Software-independent interlocks required | Hardware cost vs. risk mitigation |
| **Maintainability** | NFR-008, ASR-008 | Module interface governance | Strict contracts vs. flexibility |
| **Scalability** | NFR-010 | 10 active nodes max | Fixed capacity vs. growth |

## Recommended Architecture Style

**Hybrid: Layered + Event-Driven + Distributed**

**Justification:**
- **Layered**: Matches the natural hierarchy (UI → OCS → IOC → Hardware) per ASR-009
- **Event-Driven**: Supports logging (ASR-005), safety alerts (ASR-006), and monitoring (FR-006)
- **Distributed**: Required for remote operations (ASR-001, FR-005)

---

## Architecture Patterns & Tactics

| Pattern/Tactic | Purpose | Addresses |
|---------------|---------|-----------|
| **Broker Pattern** | Message routing between distributed components | ASR-001, FR-018 |
| **Repository Pattern** | Parameter database access | FR-014, ASR-007 |
| **State Pattern** | Operational level management | FR-002, FR-003 |
| **Observer Pattern** | Multi-point monitoring | FR-006, NFR-018 |
| **Circuit Breaker** | Fault isolation | NFR-018, NFR-005 |
| **Hardware Abstraction** | Simulation support | FR-009, ASR-004, NFR-017 |
| **RBAC** | Role-based access control | FR-001, NFR-001 |
| **Publisher-Subscriber** | Logging and events | ASR-005, FR-011 |

---

## ScenarioView

### 1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCaseDiagram
left to right direction
skinparam packageStyle rectangle

actor "Astronomer" as Astronomer
actor "Science Observer" as ScienceObserver
actor "Telescope Operator" as TelescopeOperator
actor "Support Personnel" as SupportPersonnel
actor "Administrator" as Administrator
actor "Developer" as Developer

rectangle "Gemini Observatory Control System" {
    usecase "Authenticate User" as UC001
    usecase "Manage Access Roles" as UC002
    usecase "Control Operational Level" as UC003
    usecase "Execute Observation Sequence" as UC004
    usecase "Monitor Telescope Status" as UC005
    usecase "Control Instruments" as UC006
    usecase "Configure System" as UC007
    usecase "Access Data Archive" as UC008
    usecase "Run Simulation" as UC009
    usecase "View System Logs" as UC010
    usecase "Manage Safety Interlocks" as UC011
    usecase "Schedule Observations" as UC012
}

Astronomer --> UC001
Astronomer --> UC004
Astronomer --> UC005
Astronomer --> UC008
Astronomer --> UC009

ScienceObserver --> UC001
ScienceObserver --> UC004
ScienceObserver --> UC005
ScienceObserver --> UC008

TelescopeOperator --> UC001
TelescopeOperator --> UC003
TelescopeOperator --> UC004
TelescopeOperator --> UC005
TelescopeOperator --> UC006
TelescopeOperator --> UC012

SupportPersonnel --> UC001
SupportPersonnel --> UC005
SupportPersonnel --> UC007
SupportPersonnel --> UC010

Administrator --> UC001
Administrator --> UC002
Administrator --> UC007
Administrator --> UC010
Administrator --> UC011

Developer --> UC001
Developer --> UC007
Developer --> UC009
Developer --> UC010

UC004 ..> UC001 : <<include>>
UC005 ..> UC001 : <<include>>
UC006 ..> UC001 : <<include>>
UC007 ..> UC001 : <<include>>
UC008 ..> UC001 : <<include>>
UC011 ..> UC003 : <<extend>>

note right of UC011
  Safety interlocks
  independent of software
  (ASR-006, NFR-007)
end note

note left of UC009
  Virtual telescope
  simulation mode
  (FR-009, ASR-004)
end note

@enduml
```

---

## LogicView

### 2. Class — Logic View: Class Diagram

```plantuml
@startuml ClassDiagram
left to right direction
skinparam classAttributeIconSize 0

class User {
    -userId: String
    -username: String
    -role: UserRole
    -sessionToken: String
    +login(credentials): AuthToken
    +logout(): void
    +getPermissions(): List<Permission>
}

class UserRole {
    -roleName: String
    -privileges: List<Privilege>
    +hasAccess(subsystem): boolean
    +getAccessMode(): AccessMode
}

class AccessMode {
    -modeName: String
    -capabilities: List<Capability>
    +isEnabled(feature): boolean
}

class OperationalLevel {
    -levelName: String
    -allowedModes: List<AccessMode>
    +transition(newLevel): boolean
    +getCurrentLevel(): OperationalLevel
}

class Instrument {
    -instrumentId: String
    -instrumentType: String
    -status: InstrumentStatus
    -isMounted: boolean
    +getStatus(): InstrumentStatus
    +configure(config): void
    +takeExposure(params): Data
}

class Telescope {
    -telescopeId: String
    -position: Coordinates
    -focus: Double
    -currentInstrument: Instrument
    +moveTo(coords): void
    +setFocus(value): void
    +getBeamAccess(): Instrument
}

class ObservationSequence {
    -sequenceId: String
    -steps: List<ObservationStep>
    -priority: Integer
    -weatherConstraints: WeatherRule
    +execute(): void
    +pause(): void
    +resume(): void
}

class DataAcquisition {
    -detectorId: String
    -compressionMethod: String
    -format: DataFormat
    +acquireData(): FITSData
    +compress(data): byte[]
    +store(data, location): void
}

class «persisted» ParameterDatabase {
    -dbName: String
    -accessLatency: Long
    +getParameter(name): Value
    +setParameter(name, value): void
    +getAtomic(name): Value
}

class SafetyInterlock {
    -interlockId: String
    -hazardLevel: HazardLevel
    -isHardwareBased: boolean
    -status: InterlockStatus
    +check(): boolean
    +engage(): void
    +getStatus(): InterlockStatus
}

class SystemLog {
    -logId: String
    -timestamp: DateTime
    -eventType: EventType
    -severity: LogSeverity
    -source: String
    +log(event): void
    +getLogs(filter): List<SystemLog>
    +flushBuffer(): void
}

class Simulator {
    -simulatedComponent: String
    -simulationMode: SimMode
    +executeCommand(cmd): Response
    +getSimulatedData(): Data
    +validateAgainstHardware(): boolean
}

User "1" -- "1" UserRole : has
UserRole "1" -- "1..*" AccessMode : grants
OperationalLevel "1" -- "1..*" AccessMode : allows
Telescope "1" -- "0..*" Instrument : mounts
ObservationSequence "1" -- "1" Telescope : controls
DataAcquisition "1" -- "1" Instrument : reads from
ParameterDatabase "1" -- "1..*" Telescope : configures
ParameterDatabase "1" -- "1..*" Instrument : configures
SafetyInterlock "1" -- "1" Telescope : protects
SafetyInterlock "1" -- "1..*" Instrument : protects
SystemLog "1" -- "1..*" User : tracks
SystemLog "1" -- "1..*" Instrument : monitors
Simulator "1" -- "1" Instrument : simulates
Simulator "1" -- "1" Telescope : simulates

note right of SafetyInterlock
  Hardware-independent
  for critical hazards
  (ASR-006, NFR-007)
end note

note left of ParameterDatabase
  2-3ms access time
  EPICS at IOC level
  (FR-014, ASR-007)
end note

note right of SystemLog
  200Hz short-term
  1Hz long-term
  (NFR-013, ASR-005)
end note

@enduml
```

---

### 3. Object — Logic View: Object Diagram

```plantuml
@startuml ObjectDiagram
left to right direction

object user1 : User [AuthenticateUser] {
    userId = "USR-001"
    username = "astro_jones"
    role = "Astronomer"
    sessionToken = "tok_abc123"
}

object role1 : UserRole [AuthenticateUser] {
    roleName = "Astronomer"
    privileges = ["OBSERVE", "MONITOR", "DATA_ACCESS"]
}

object mode1 : AccessMode [AuthenticateUser] {
    modeName = "Observing"
    capabilities = ["ExecuteSequence", "MonitorStatus"]
}

object telescope1 : Telescope [ExecuteObservation] {
    telescopeId = "GEMINI-N"
    position = "RA:12h30m DEC:+45°"
    focus = 15.2
    currentInstrument = "instrument1"
}

object instrument1 : Instrument [ExecuteObservation] {
    instrumentId = "NIRI-01"
    instrumentType = "Near-Infrared"
    status = "READY"
    isMounted = true
}

object sequence1 : ObservationSequence [ExecuteObservation] {
    sequenceId = "SEQ-2024-001"
    priority = 1
    weatherConstraints = "CLEAR"
}

object interlock1 : SafetyInterlock [ExecuteObservation] {
    interlockId = "SAFE-001"
    hazardLevel = "CRITICAL"
    isHardwareBased = true
    status = "ENGAGED"
}

object db1 : ParameterDatabase [ExecuteObservation] {
    dbName = "TELEMETRY_DB"
    accessLatency = 2
}

user1 --> role1 : has
role1 --> mode1 : grants
telescope1 --> instrument1 : mounts
sequence1 --> telescope1 : controls
interlock1 --> telescope1 : protects
db1 --> telescope1 : configures
db1 --> instrument1 : configures

note right of interlock1
  Hardware interlock
  engaged for safety
end note

note left of db1
  Access latency: 2ms
  within SLO
end note

@enduml
```

---

### 4. State — Logic View: State Diagram

```plantuml
@startuml StateDiagram
left to right direction
skinparam state {
    BackgroundColor white
    BorderColor black
}

[*] --> Initializing : System Boot

state Initializing {
    [*] --> HardwareCheck
    HardwareCheck --> SoftwareCheck : Hardware OK
    SoftwareCheck --> VersionVerify : Software OK
    VersionVerify --> ConfigLoad : Version OK
    ConfigLoad --> [*] : Config Loaded
}

Initializing --> Standby : All Checks Pass
Initializing --> SafeState : Check Failed

Standby --> Observing : Start Observation
Standby --> Maintenance : Enter Maintenance
Standby --> Testing : Enter Test Mode

Observing --> Standby : Observation Complete
Observing --> SafeState : Safety Alert
Observing --> Maintenance : Manual Override

Maintenance --> Standby : Maintenance Complete
Maintenance --> SafeState : Safety Alert

Testing --> Standby : Test Complete
Testing --> SafeState : Safety Alert

SafeState --> [*] : System Shutdown
SafeState --> Standby : Safety Cleared

state SafeState {
    [*] --> ActuatorsDisabled
    ActuatorsDisabled --> InterlocksEngaged
    InterlocksEngaged --> AlarmsIssued
    AlarmsIssued --> [*]
}

note right of SafeState
  Recovery goal: 5 minutes
  (NFR-005)
  Hardware interlocks
  independent of software
  (ASR-006)
end note

note left of Observing
  Primary operation mode
  Queue-based sequencing
  (FR-004)
end note

note bottom of Initializing
  Version control check
  at boot time
  (FR-015)
end note

@enduml
```

---

## ProcessView

### 5. Activity — Process View: Activity Diagram

```plantuml
@startuml ActivityDiagram
left to right direction
skinparam activity {
    BackgroundColor white
    BorderColor black
}

start

:User Login;
note right: TLS1.2+ required
(NFR-001)

partition "Authentication" {
    :Validate Credentials;
    if (Valid?) then (yes)
        :Generate Auth Token;
        :Assign Role & Privileges;
    else (no)
        :Log Failed Attempt;
        if (Attempts >= 5?) then (yes)
            :Lock Account;
            :Alert Security;
        else (no)
            :Return Error;
        endif
        stop
    endif
}

:Select Operational Level;
note right: Observing/Maintenance/Test
(FR-002)

partition "Safety Check" {
    :Check Hardware Interlocks;
    note right: Independent of software
    (ASR-006)
    if (All Safe?) then (yes)
        :Clear for Operation;
    else (no)
        :Enter Safe State;
        :Issue Alarms;
        stop
    endif
}

partition "Observation Execution" {
    :Load Observation Sequence;
    :Verify Instrument Availability;
    fork
        :Configure Telescope;
        :Set Instrument Parameters;
    fork again
        :Monitor Weather;
        :Track Schedule Priority;
    end fork
    
    :Execute Exposure;
    note right: <3min readout
    (NFR-009)
    
    :Acquire Data;
    :Compress (Lossless);
    note right: FITS format
    (NFR-011)
    
    :Store to Archive;
    note right: 7 days retention
    (NFR-004)
}

:Log All Events;
note right: 200Hz short-term
(NFR-013)

:Update Status Display;
note right: <4 sec update
(NFR-002)

if (Sequence Complete?) then (yes)
    :Notify User;
    :Archive Final Data;
else (no)
    :Continue Next Step;
endif

stop

@enduml
```

---

### 6. Sequence — Process View: Sequence Diagram

```plantuml
@startuml SequenceDiagram1
title Sequence: Remote Observation Execution (FR-004, FR-005, ASR-001)
left to right direction
skinparam sequence {
    LifeLineBorderColor black
    LifeLineBackgroundColor white
}

actor "Remote Astronomer" as Astronomer
participant "UI Client" as UIClient
participant "Auth Service" as AuthService
participant "OCS Controller" as OCS
participant "Instrument IOC" as InstrumentIOC
participant "Telescope IOC" as TelescopeIOC
participant "Parameter DB" as ParamDB
participant "Data Archive" as Archive

Astronomer -> UIClient : Login(credentials)
UIClient -> AuthService : Authenticate(username, password)
AuthService --> UIClient : AuthToken + Role
note right: TLS1.2+ (NFR-001)

Astronomer -> UIClient : Submit Observation Sequence
UIClient -> OCS : ExecuteSequence(seqId, token)
OCS -> AuthService : ValidateToken(token)
AuthService --> OCS : Role=Astronomer, Privileges=[...]

OCS -> ParamDB : GetParameters(telescope, instrument)
note right: <3ms access (FR-014)
ParamDB --> OCS : Parameters

OCS -> TelescopeIOC : MoveTo(coordinates)
TelescopeIOC --> OCS : ACK (<500ms)
note right: 500ms timeout (FR-018)

OCS -> InstrumentIOC : Configure(exposureParams)
InstrumentIOC --> OCS : ACK

OCS -> InstrumentIOC : TakeExposure()
InstrumentIOC --> OCS : Exposure Complete
note right: <3min readout (NFR-009)

OCS -> InstrumentIOC : GetData()
InstrumentIOC --> OCS : FITS Data

OCS -> OCS : Compress(Lossless)
note right: FITS format (NFR-011)

OCS -> Archive : Store(data, metadata)
Archive --> OCS : Storage Confirmed
note right: 7 days retention (NFR-004)

OCS --> UIClient : Sequence Progress Update
note right: <4 sec update (NFR-002)
UIClient --> Astronomer : Display Status

Astronomer -> UIClient : Request Quick-Look Data
UIClient -> OCS : GetQuickLook(exposureId)
OCS --> UIClient : Processed Data
note right: Within exposure sequence (FR-019)

@enduml
```

---

```plantuml
@startuml SequenceDiagram2
title Sequence: Safety Interlock Activation (FR-012, NFR-007, ASR-006)
left to right direction
skinparam sequence {
    LifeLineBorderColor black
    LifeLineBackgroundColor white
}

participant "Hardware Sensor" as Sensor
participant "Safety Interlock HW" as SafetyHW
participant "Safety Monitor SW" as SafetySW
participant "OCS Controller" as OCS
participant "Instrument IOC" as InstrumentIOC
participant "Telescope IOC" as TelescopeIOC
participant "System Log" as SysLog
participant "Ops Console" as Console

Sensor -> SafetyHW : Hazard Detected
note right: Hardware-independent\n(ASR-006)
SafetyHW -> SafetyHW : Engage Interlock

SafetyHW -> SafetySW : Interlock Status Change
SafetySW -> OCS : SafetyAlert(hazardId, severity)
note right: <15 sec delivery (FR-012)

OCS -> TelescopeIOC : EmergencyStop()
TelescopeIOC --> OCS : ACK

OCS -> InstrumentIOC : EmergencyStop()
InstrumentIOC --> OCS : ACK

OCS -> SysLog : LogEvent(SAFETY_ALERT, hazardId)
note right: Timestamp + source (FR-011)
SysLog --> OCS : Logged

OCS -> Console : Display Alarm(alarmId, message)
note right: All ops consoles (FR-012)
Console --> OCS : Alarm Acknowledged

OCS -> OCS : Enter Safe State
note right: <5 min recovery (NFR-005)

OCS -> SysLog : LogEvent(SAFE_STATE_ENTRY)
SysLog --> OCS : Logged

SafetyHW -> SafetyHW : Test Interlock (periodic)
note right: Every 168h (NFR-007)
SafetyHW -> SysLog : Log Test Result

alt Test Failed
    SafetyHW -> SafetyHW : Hard Shutdown
    SafetyHW -> SysLog : Log Interlock Failure
else Test Passed
    SafetyHW -> SysLog : Log Interlock OK
end

@enduml
```

---

### 7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml CollaborationDiagram1
title Collaboration: Remote Observation Execution
left to right direction
skinparam sequence {
    LifeLineBorderColor black
    LifeLineBackgroundColor white
}

object "1:Astronomer" as Astronomer
object "2:UIClient" as UIClient
object "3:AuthService" as AuthService
object "4:OCS" as OCS
object "5:ParamDB" as ParamDB
object "6:TelescopeIOC" as TelescopeIOC
object "7:InstrumentIOC" as InstrumentIOC
object "8:Archive" as Archive

Astronomer -- UIClient : Network
UIClient -- AuthService : TLS
UIClient -- OCS : Network
OCS -- ParamDB : LAN (<3ms)
OCS -- TelescopeIOC : LAN (500ms)
OCS -- InstrumentIOC : LAN (500ms)
OCS -- Archive : LAN

1 --> 2 : 1: Login(credentials)
2 --> 3 : 2: Authenticate()
3 --> 2 : 3: AuthToken
2 --> 4 : 4: ExecuteSequence(seqId)
4 --> 3 : 5: ValidateToken()
4 --> 5 : 6: GetParameters()
5 --> 4 : 7: Parameters
4 --> 6 : 8: MoveTo(coords)
6 --> 4 : 9: ACK
4 --> 7 : 10: Configure()
7 --> 4 : 11: ACK
4 --> 7 : 12: TakeExposure()
7 --> 4 : 13: Exposure Complete
4 --> 7 : 14: GetData()
7 --> 4 : 15: FITS Data
4 --> 8 : 16: Store(data)
8 --> 4 : 17: Confirmed
4 --> 2 : 18: Status Update
2 --> 1 : 19: Display Status

note bottom
  Scenario: Remote Observation Execution
  References: FR-004, FR-005, ASR-001
  Performance: <4 sec status update (NFR-002)
end note

@enduml
```

---

```plantuml
@startuml CollaborationDiagram2
title Collaboration: Safety Interlock Activation
left to right direction
skinparam sequence {
    LifeLineBorderColor black
    LifeLineBackgroundColor white
}

object "1:Sensor" as Sensor
object "2:SafetyHW" as SafetyHW
object "3:SafetySW" as SafetySW
object "4:OCS" as OCS
object "5:TelescopeIOC" as TelescopeIOC
object "6:InstrumentIOC" as InstrumentIOC
object "7:SysLog" as SysLog
object "8:Console" as Console

Sensor -- SafetyHW : Hardware
SafetyHW -- SafetySW : Signal
SafetySW -- OCS : Network
OCS -- TelescopeIOC : LAN
OCS -- InstrumentIOC : LAN
OCS -- SysLog : LAN
OCS -- Console : Network

1 --> 2 : 1: Hazard Detected
2 --> 2 : 2: Engage Interlock
2 --> 3 : 3: Status Change
3 --> 4 : 4: SafetyAlert()
4 --> 5 : 5: EmergencyStop()
5 --> 4 : 6: ACK
4 --> 6 : 7: EmergencyStop()
6 --> 4 : 8: ACK
4 --> 7 : 9: LogEvent(SAFETY)
7 --> 4 : 10: Logged
4 --> 8 : 11: Display Alarm()
8 --> 4 : 12: Acknowledged
4 --> 4 : 13: Enter Safe State
4 --> 7 : 14: LogEvent(SAFE_STATE)

note bottom
  Scenario: Safety Interlock Activation
  References: FR-012, NFR-007, ASR-006
  Timing: <15 sec alert delivery (FR-012)
  Recovery: <5 min to observing (NFR-005)
end note

@enduml
```

---

## DevelopmentView

### 8. Package — Development View: Package Diagram

```plantuml
@startuml PackageDiagram
left to right direction
skinparam package {
    BackgroundColor white
    BorderColor black
}

package "UI Layer" <<User Interface>> {
    [Web Client] as WebUI
    [Desktop Client] as DesktopUI
    [Mobile Client] as MobileUI
}

package "OCS Layer" <<Observation Control>> {
    [Authentication Service] as AuthService
    [Scheduling Service] as ScheduleService
    [Sequence Executor] as SeqExecutor
    [Data Processor] as DataProcessor
}

package "IOC Layer" <<Real-Time Control>> {
    [Telescope IOC] as TelescopeIOC
    [Instrument IOC] as InstrumentIOC
    [Detector IOC] as DetectorIOC
    [Safety Monitor] as SafetyMonitor
}

package "Data Layer" <<Persistence>> {
    [Parameter DB] as ParamDB
    [Log DB] as LogDB
    [Archive Storage] as ArchiveStorage
}

package "Integration Layer" <<External>> {
    [Remote API Gateway] as APIGateway
    [Weather Service] as WeatherService
    [Archive Interface] as ArchiveInterface
}

WebUI --> AuthService : HTTPS/TLS
DesktopUI --> AuthService : HTTPS/TLS
MobileUI --> AuthService : HTTPS/TLS

AuthService --> ParamDB : Query
ScheduleService --> ParamDB : Query
ScheduleService --> WeatherService : Get Forecast
SeqExecutor --> TelescopeIOC : Command
SeqExecutor --> InstrumentIOC : Command
SeqExecutor --> DataProcessor : Process

DataProcessor --> ArchiveStorage : Store
DataProcessor --> LogDB : Log

TelescopeIOC --> ParamDB : Read/Write
InstrumentIOC --> ParamDB : Read/Write
DetectorIOC --> ParamDB : Read/Write
SafetyMonitor --> TelescopeIOC : Emergency Stop
SafetyMonitor --> InstrumentIOC : Emergency Stop

APIGateway --> AuthService : Auth
APIGateway --> SeqExecutor : Commands

note right of "IOC Layer"
  Real-time OS required
  EPICS implementation
  (ASR-009, ASR-007)
end note

note left of "Data Layer"
  2-3ms access time
  7 days retention
  (FR-014, NFR-004)
end note

note bottom of "Integration Layer"
  Remote operations support
  Network transparent
  (ASR-001, NFR-006)
end note

@enduml
```

---

### 9. Component — Development View: Component Diagram

```plantuml
@startuml ComponentDiagram
left to right direction
skinparam component {
    BackgroundColor white
    BorderColor black
}

component "AuthComponent" <<Authentication>> {
    [Login Handler] as LoginHandler
    [Token Manager] as TokenManager
    [Role Validator] as RoleValidator
}

component "OCS Controller" <<Command Control>> {
    [Command Router] as CmdRouter
    [Sequence Manager] as SeqManager
    [Scheduler] as Scheduler
}

component "Instrument Manager" <<Resource Mgmt>> {
    [Instrument Registry] as InstRegistry
    [Beam Arbitrator] as BeamArb
    [Calibration Handler] as CalibHandler
}

component "Data Handler" <<Acquisition>> {
    [FITS Encoder] as FITSEncoder
    [Compressor] as Compressor
    [Archive Writer] as ArchiveWriter
}

component "Safety Controller" <<Safety>> {
    [Interlock Monitor] as InterlockMon
    [Emergency Handler] as EmergHandler
    [Alarm Manager] as AlarmMgr
}

component "Logging Service" <<Logging>> {
    [Event Logger] as EventLogger
    [Buffer Manager] as BufferMgr
    [Log Retention] as LogRetention
}

component "Simulator" <<Simulation>> {
    [Hardware Simulator] as HWSim
    [Virtual Telescope] as VirtTel
    [Test Validator] as TestVal
}

component "Parameter DB" <<EPICS>> {
    [IOC Channel] as IOCChannel
    [Host DB] as HostDB
    [Sync Manager] as SyncMgr
}

LoginHandler --> TokenManager : Generate
TokenManager --> RoleValidator : Validate
CmdRouter --> SeqManager : Route
SeqManager --> Scheduler : Query
SeqManager --> BeamArb : Request Access
BeamArb --> InstRegistry : Check Status
InstRegistry --> CalibHandler : Coordinate

FITSEncoder --> Compressor : Compress
Compressor --> ArchiveWriter : Write
InterlockMon --> EmergHandler : Trigger
EmergHandler --> AlarmMgr : Notify

EventLogger --> BufferMgr : Buffer (200Hz)
BufferMgr --> LogRetention : Flush

HWSim --> VirtTel : Simulate
TestVal --> HWSim : Validate

CmdRouter --> IOCChannel : Command
IOCChannel --> HostDB : Sync

note right of Safety Controller
  Hardware-independent
  interlocks for critical hazards
  (ASR-006, NFR-007)
end note

note left of Parameter DB
  EPICS at IOC level
  2-3ms access latency
  (ASR-007, FR-014)
end note

note bottom of Simulator
  No hardware required
  Pass 100% test suite
  (FR-009, ASR-004)
end note

@enduml
```

---

## PhysicalView

### 10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml DeploymentDiagram
left to right direction
skinparam node {
    BackgroundColor white
    BorderColor black
}

node "Remote Site A" <<Facility>> as SiteA {
    node "Operator Workstation" <<Windows/Linux>> as WorkstationA {
        component "Desktop Client" as ClientA
    }
    node "Monitoring Station" <<Linux>> as MonitorA {
        component "Web Client" as WebA
    }
}

node "Remote Site B" <<Facility>> as SiteB {
    node "Operator Workstation" <<Windows/Linux>> as WorkstationB {
        component "Desktop Client" as ClientB
    }
}

node "Observatory Site" <<Primary>> as ObsSite {
    node "OCS Server Cluster" <<High Availability>> {
        component "OCS Controller" as OCS
        component "Auth Service" as Auth
        component "Scheduler" as Scheduler
    }
    
    node "Application Server" <<Linux>> {
        component "Data Processor" as DataProc
        component "Logging Service" as LogSvc
    }
    
    node "Database Server" <<Redundant>> {
        database "Parameter DB (EPICS)" as ParamDB
        database "Log DB (SYBASE)" as LogDB
    }
    
    node "Archive Storage" <<7-day Retention>> {
        component "Archive Service" as Archive
        artifact "FITS Files" as FITS
    }
    
    node "IOC Rack" <<Real-Time OS>> {
        component "Telescope IOC" as TelIOC
        component "Instrument IOC-1" as InstIOC1
        component "Instrument IOC-2" as InstIOC2
        component "Safety Monitor" as SafetyMon
    }
    
    node "Hardware Layer" <<Physical>> {
        component "Telescope" as Telescope
        component "Instrument-1" as Instrument1
        component "Instrument-2" as Instrument2
        component "Safety Interlocks (HW)" as SafetyHW
    }
}

node "External Services" <<Cloud>> {
    component "Weather Service" as Weather
    component "Home Institute Archive" as HomeArchive
}

WorkstationA -- WorkstationB : WAN (TLS1.2+)
WorkstationA -- OCS : WAN <150ms RTT
WorkstationB -- OCS : WAN <150ms RTT
MonitorA -- OCS : WAN

OCS -- DataProc : LAN (20-40 Mbit/s)
DataProc -- ParamDB : LAN <3ms
DataProc -- LogDB : LAN
DataProc -- Archive : LAN

OCS -- TelIOC : LAN <500ms
OCS -- InstIOC1 : LAN <500ms
OCS -- InstIOC2 : LAN <500ms

TelIOC -- Telescope : Hardware Bus
InstIOC1 -- Instrument1 : Hardware Bus
InstIOC2 -- Instrument2 : Hardware Bus
SafetyMon -- SafetyHW : Hardware (Independent)

OCS -- Weather : Internet
Archive -- HomeArchive : Internet <20 sec

note right of "IOC Rack"
  Real-time control layer
  EPICS implementation
  (ASR-009)
  6 active + 2 monitoring nodes
  (NFR-010)
end note

note left of "Database Server"
  2-3ms access time
  Distributed across IOCs
  (ASR-007, FR-014)
end note

note bottom of "Hardware Layer"
  Safety interlocks
  independent of software
  (ASR-006, NFR-007)
end note

@enduml
```

---

### 11. Container — Physical View: Container Diagram

```plantuml
@startuml ContainerDiagram
left to right direction
skinparam container {
    BackgroundColor white
    BorderColor black
}

rectangle "Remote Operations" <<External>> {
    container "Web Browser" <<HTML5/JavaScript>> as WebBrowser {
        Responsibility: Remote UI access
        Technology: HTTPS, WebSocket
        Scale: 100 concurrent sessions (ASR-001)
    }
    
    container "Desktop Application" <<Qt/C++>> as DesktopApp {
        Responsibility: Full operator console
        Technology: TLS1.2+, Local cache
        Scale: Multi-site deployment
    }
}

rectangle "Observatory Backend" <<On-Premise>> {
    container "API Gateway" <<Nginx/Node>> as APIGateway {
        Responsibility: Request routing, auth proxy
        Technology: TLS termination, rate limiting
        Security: TLS1.2+, 100 sessions min (ASR-001)
    }
    
    container "OCS Application" <<Java/Python>> as OCSApp {
        Responsibility: Observation coordination
        Technology: Message queue, async processing
        Performance: <2s command response (NFR-002)
    }
    
    container "Auth Service" <<Java>> as AuthSvc {
        Responsibility: Authentication, RBAC
        Technology: JWT, OAuth2
        Security: 180-day audit log (NFR-001)
    }
    
    container "Data Processor" <<Python/C>> as DataProc {
        Responsibility: FITS encoding, compression
        Technology: Lossless compression
        Performance: <20 sec transmission (NFR-011)
    }
    
    container "Parameter Database" <<EPICS/PostgreSQL>> as ParamDB {
        Responsibility: System parameters
        Technology: EPICS channels, SQL
        Performance: 2-3ms access (FR-014)
        Capacity: 10 active nodes (NFR-010)
    }
    
    container "Log Database" <<SYBASE>> as LogDB {
        Responsibility: Event logging
        Technology: Relational DBMS
        Performance: 200Hz short-term (NFR-013)
        Retention: 30 days minimum
    }
    
    container "Archive Storage" <<File System>> as Archive {
        Responsibility: Data retention
        Technology: FITS format, compression
        Capacity: 7 days (NFR-004)
        Interactive: 3 days on disk
    }
    
    container "IOC Controller" <<EPICS RTOS>> as IOC {
        Responsibility: Real-time hardware control
        Technology: EPICS, RTOS
        Performance: 500ms timeout (FR-018)
        Readout: 0.1s focus, 3min full (NFR-009)
    }
}

rectangle "External Services" <<Cloud>> {
    container "Weather API" <<REST>> as WeatherAPI {
        Responsibility: Weather data
        Integration: Scheduling decisions
    }
    
    container "Home Institute" <<FTP/HTTPS>> as HomeInst {
        Responsibility: Data transfer
        Performance: <20 sec (NFR-011)
        Format: FITS NOST 100-1.0
    }
}

WebBrowser --> APIGateway : HTTPS/WSS
DesktopApp --> APIGateway : TLS1.2+

APIGateway --> AuthSvc : Validate Token
APIGateway --> OCSApp : Route Commands

OCSApp --> ParamDB : Read/Write Params
OCSApp --> LogDB : Log Events
OCSApp --> DataProc : Process Data
OCSApp --> IOC : Hardware Commands

DataProc --> Archive : Store FITS
DataProc --> HomeInst : Transfer Data

OCSApp --> WeatherAPI : Query Forecast
AuthSvc --> LogDB : Audit Log (180 days)

note right of "API Gateway"
  Network transparency
  Remote operations support
  (ASR-001, NFR-006)
end note

note left of "IOC Controller"
  Real-time boundary
  Hardware abstraction
  (ASR-009, ASR-004)
end note

note bottom of "Archive Storage"
  7 days total retention
  3 days interactive
  (NFR-004)
end note

@enduml
```