## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SafetyCriticalControl
left to right direction
skinparam packageStyle rectangle

actor Operator
actor Supervisor
actor Maintainer
actor "ControllerUnit" as ControllerUnit <<external system>>
actor "TelemetrySubscriber" as TelemetrySubscriber <<external system>>
actor "TimeSource" as TimeSource <<external system>>

rectangle "Control System" as System {
  usecase "Authenticate\n[Authenticate]" as UC_Auth
  usecase "Acquire Control Lease\n[AcquireLease]" as UC_Lease
  usecase "Issue Command\n[IssueCommand]" as UC_Command
  usecase "Validate Safety\n[ValidateSafety]" as UC_Safety
  usecase "Execute Sequence\n[ExecuteSequence]" as UC_Sequence
  usecase "Monitor Status\n[MonitorStatus]" as UC_Monitor
  usecase "Acknowledge Alarm\n[AckAlarm]" as UC_Ack
  usecase "Export Telemetry\n[ExportTelemetry]" as UC_Export
  usecase "Configure System\n[ConfigureSystem]" as UC_Config
  usecase "Run Diagnostics\n[RunDiagnostics]" as UC_Diag
  usecase "Override Interlock\n[OverrideInterlock]" as UC_Override
}

Operator --> UC_Auth
Operator --> UC_Lease
Operator --> UC_Command
Operator --> UC_Monitor
Operator --> UC_Ack

Supervisor --> UC_Override
Supervisor --> UC_Monitor

Maintainer --> UC_Config
Maintainer --> UC_Diag

ControllerUnit --> UC_Sequence
ControllerUnit --> UC_Monitor

TelemetrySubscriber --> UC_Export
TimeSource --> UC_Monitor

UC_Command .> UC_Lease : <<include>>
UC_Command .> UC_Safety : <<include>>
UC_Command .> UC_Sequence : <<include>>
UC_Monitor .> UC_Export : <<extend>>

UC_Override .> UC_Safety : <<extend>>

note bottom of System
assumption: Requirements artifacts (FR/NFR/ASR) were not provided; modeled a safety-critical
event-driven control system per semantic memory decisions: single-operator lease, layered interlocks,
deterministic sequencing, immutable audit, contract-first controller I/O and telemetry export.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_SafetyCriticalControl
skinparam classAttributeIconSize 0

class Operator {
  +operatorId: String
  +name: String
  +role: String
  +authenticate()
  +requestLease()
  +issueCommand()
  +ackAlarm()
}

class ControlLease <<immutable>> {
  +leaseId: String
  +holderOperatorId: String
  +issuedAt: DateTime
  +expiresAt: DateTime
  +isActive(): boolean
}

class CommandRequest <<immutable>> {
  +commandId: String
  +commandType: String
  +targetId: String
  +requestedAt: DateTime
  +parametersJson: String
  +validate()
}

class SafetyInterlock {
  +interlockId: String
  +layer: String
  +evaluate(cmd: CommandRequest, state: SystemState): SafetyDecision
  +abort(reason: String)
}

class SafetyDecision <<immutable>> {
  +allowed: boolean
  +reason: String
  +timestamp: DateTime
}

class SequenceController {
  +sequenceId: String
  +mode: String
  +startSequence(cmd: CommandRequest)
  +advanceTick()
  +halt()
  +resume()
}

class SystemState <<persisted>> {
  +stateId: String
  +laneDirection: String
  +barrierState: String
  +deviceHealth: String
  +lastUpdateAt: DateTime
  +isStale(maxAgeMs: long): boolean
}

class TelemetryEvent <<immutable>> {
  +eventId: String
  +eventType: String
  +source: String
  +occurredAt: DateTime
  +payloadJson: String
}

class EventBus {
  +publish(evt: TelemetryEvent)
  +subscribe(topic: String)
}

class AuditLog <<persisted>> {
  +append(entry: AuditEntry)
  +queryByTimeRange()
}

class AuditEntry <<immutable>> {
  +entryId: String
  +actorId: String
  +action: String
  +timestamp: DateTime
  +hash: String
}

class ControllerAdapter {
  +protocolVersion: String
  +sendCommand(cmd: CommandRequest)
  +readStatus(): DeviceStatusFrame
}

class DeviceStatusFrame <<immutable>> {
  +frameVersion: String
  +deviceId: String
  +statusCode: String
  +measuredAt: DateTime
  +checksum: String
}

class DataContractRegistry <<persisted>> {
  +getSchema(name: String, version: String): String
  +registerSchema()
}

Operator "1" --> "0..1" ControlLease : holds >
Operator "1" --> "0..*" CommandRequest : creates >
SequenceController "1" --> "0..*" CommandRequest : executes >
SafetyInterlock "1..*" --> "1" SequenceController : guards >
SafetyInterlock --> SafetyDecision : produces >
SequenceController --> ControllerAdapter : uses >
ControllerAdapter --> DeviceStatusFrame : reads >
SystemState "1" o-- "0..*" DeviceStatusFrame : derivedFrom
EventBus "1" --> "0..*" TelemetryEvent : carries >
TelemetryEvent --> SystemState : updates >
AuditLog "1" o-- "0..*" AuditEntry : stores >
CommandRequest --> AuditEntry : audited >
ControlLease --> AuditEntry : audited >
DataContractRegistry --> ControllerAdapter : constrains >

note right of SafetyInterlock
Layered interlocks:
- originating unit (UI/API)
- subordinate screening
- executing controller
Abort on unknown/opposite-direction unsafe states.
end note

note right of ControlLease
Single-operator command/control via lease/lock.
Lease expiration prevents stale control authority.
end note

note bottom of ControllerAdapter
Contract-first integration:
versioned command/status frames, checksums, timing constraints.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SafetyCriticalControl
skinparam classAttributeIconSize 0

object op1 as "op1:Operator [IssueCommand]" {
  operatorId = "OP-17"
  name = "A. Rivera"
  role = "Operator"
}

object lease1 as "lease1:ControlLease [AcquireLease]" {
  leaseId = "L-2026-04-22-0007"
  holderOperatorId = "OP-17"
  issuedAt = "2026-04-22T10:00:00Z"
  expiresAt = "2026-04-22T10:05:00Z"
}

object cmd1 as "cmd1:CommandRequest [IssueCommand]" {
  commandId = "C-8891"
  commandType = "SetLaneDirection"
  targetId = "LaneSegment-3"
  requestedAt = "2026-04-22T10:00:10Z"
  parametersJson = "{direction:'NORTHBOUND'}"
}

object state1 as "state1:SystemState [MonitorStatus]" {
  stateId = "S-rt"
  laneDirection = "HOLD"
  barrierState = "CLOSED"
  deviceHealth = "OK"
  lastUpdateAt = "2026-04-22T10:00:09Z"
}

object si1 as "si1:SafetyInterlock [ValidateSafety]" {
  interlockId = "SI-ORIGIN"
  layer = "Originating"
}

object sc1 as "sc1:SequenceController [ExecuteSequence]" {
  sequenceId = "SEQ-42"
  mode = "Deterministic"
}

object ad1 as "ad1:ControllerAdapter [ExecuteSequence]" {
  protocolVersion = "v1.0"
}

op1 --> lease1 : holds
op1 --> cmd1 : creates
cmd1 --> si1 : evaluatedBy
si1 --> sc1 : guards
sc1 --> ad1 : uses
state1 <-- ad1 : readsStatus

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_CommandLifecycle
hide empty description

state "CommandLifecycle" as CL {
  [*] --> Draft : CreateCommand
  Draft --> LeaseChecked : AcquireLease
  LeaseChecked --> Rejected : [leaseInvalid] / audit("LeaseDenied")
  LeaseChecked --> SafetyChecking : [leaseValid] / audit("LeaseOK")

  SafetyChecking --> Rejected : [unsafe] / audit("SafetyAbort")
  SafetyChecking --> Sequencing : [safe] / startSequence()

  Sequencing --> Executing : SlotReady
  Executing --> Completed : ControllerAck / audit("Executed")
  Executing --> Failed : TimeoutOrNack / audit("ExecFailed")

  Failed --> SafetyChecking : Retry [retryAllowed] / backoff()
  Failed --> Rejected : [retryExceeded] / raiseAlarm()

  Completed --> [*]
  Rejected --> [*]
}

note right of CL
Deterministic sequencing and abort-on-unknown policy.
assumption: command timeout/retry windows are defined as SLOs but not provided.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_IssueCommandWorkflow
start
:Authenticate [SecurityCheck];
:Acquire Control Lease [LeaseLock];

if (Lease active?) then (yes)
  :Compose Command;
  :Validate Command Syntax;
  :Fetch Latest SystemState;
  if (State stale?) then (yes)
    :Abort & Raise Alarm;
    :Audit "StaleStateAbort";
    stop
  else (no)
    :Run Layered Safety Interlocks;
    if (Safe?) then (yes)
      :Audit "CommandAccepted";
      fork
        :Publish CommandRequested event;
      fork again
        :Start Deterministic Sequence;
      end fork
      :Send Command to ControllerAdapter;
      :Wait for Controller Ack/Status;
      if (Ack OK?) then (yes)
        :Publish TelemetryEvent;
        :Update SystemState;
        :Audit "CommandExecuted";
        stop
      else (no)
        :Audit "CommandFailed";
        :Raise Alarm;
        stop
      endif
    else (no)
      :Audit "SafetyRejected";
      :Notify Operator;
      stop
    endif
  endif
else (no)
  :Deny Command (No Lease);
  :Audit "LeaseDenied";
  stop
endif

note right
assumption: freshness SLO such as "status reflected within ~2s" applies at UI-to-state update point.
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence1_IssueCommand
actor Operator
participant "ControlAPI" as ControlAPI
participant "AuthService" as AuthService
participant "LeaseService" as LeaseService
participant "SafetyService" as SafetyService
participant "SequenceController" as SequenceController
participant "ControllerAdapter" as ControllerAdapter
participant "EventBus" as EventBus
database "StateStore" as StateStore
database "AuditLog" as AuditLog

Operator -> ControlAPI : Authenticate
ControlAPI -> AuthService : ValidateCredentials
AuthService --> ControlAPI : AuthOK(token)
ControlAPI -> LeaseService : AcquireLease
LeaseService -> AuditLog : Append(LeaseIssued)
LeaseService --> ControlAPI : LeaseGranted

Operator -> ControlAPI : IssueCommand
ControlAPI -> StateStore : GetLatestState
StateStore --> ControlAPI : SystemState

ControlAPI -> SafetyService : ValidateSafety(cmd,state)
SafetyService -> AuditLog : Append(SafetyEvaluated)
SafetyService --> ControlAPI : SafetyDecision(allowed)

alt allowed
  ControlAPI -> EventBus : Publish(CommandRequested)
  ControlAPI -> SequenceController : StartSequence
  SequenceController -> ControllerAdapter : SendCommand
  ControllerAdapter --> SequenceController : ControllerAck
  SequenceController -> EventBus : Publish(TelemetryEvent)
  EventBus -> StateStore : UpdateState
  ControlAPI -> AuditLog : Append(CommandExecuted)
  ControlAPI --> Operator : CommandResult(Completed)
else rejected
  ControlAPI -> AuditLog : Append(CommandRejected)
  ControlAPI --> Operator : CommandResult(Rejected)
end

note over ControllerAdapter
Contract-first protocol with versioned frames + checksum.
assumption: controller timing windows exist but not specified.
end note
@enduml
```

```plantuml
@startuml Sequence2_MonitorStatusAndExport
actor Operator
participant "MonitoringUI" as MonitoringUI
participant "MonitoringService" as MonitoringService
participant "EventBus" as EventBus
database "StateStore" as StateStore
participant "ExportService" as ExportService
participant "TelemetrySubscriber" as TelemetrySubscriber
database "AuditLog" as AuditLog

Operator -> MonitoringUI : OpenMonitor
MonitoringUI -> MonitoringService : SubscribeStatus
MonitoringService -> EventBus : Subscribe(TelemetryTopic)
EventBus --> MonitoringService : TelemetryEvent(stream)

loop each event
  MonitoringService -> StateStore : UpdateState
  MonitoringService -> MonitoringUI : PushStatus
end

MonitoringService -> ExportService : ExportTelemetry(batch)
ExportService -> AuditLog : Append(ExportPerformed)
ExportService --> TelemetrySubscriber : DeliverTelemetry

note over MonitoringService
Event-driven push to GUI; freshness SLO assumed (~2s) but not provided.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration1_IssueCommand
skinparam linetype ortho

object Operator
object ControlAPI
object AuthService
object LeaseService
object SafetyService
object SequenceController
object ControllerAdapter
object EventBus
object StateStore
object AuditLog

Operator -- ControlAPI
ControlAPI -- AuthService
ControlAPI -- LeaseService
ControlAPI -- SafetyService
ControlAPI -- SequenceController
SequenceController -- ControllerAdapter
ControlAPI -- EventBus
ControlAPI -- StateStore
ControlAPI -- AuditLog
LeaseService -- AuditLog
SafetyService -- AuditLog

Operator -> ControlAPI : 1 Authenticate
ControlAPI -> AuthService : 2 ValidateCredentials
ControlAPI -> LeaseService : 3 AcquireLease
LeaseService -> AuditLog : 4 Append(LeaseIssued)
Operator -> ControlAPI : 5 IssueCommand
ControlAPI -> StateStore : 6 GetLatestState
ControlAPI -> SafetyService : 7 ValidateSafety
SafetyService -> AuditLog : 8 Append(SafetyEvaluated)
ControlAPI -> EventBus : 9 Publish(CommandRequested)
ControlAPI -> SequenceController : 10 StartSequence
SequenceController -> ControllerAdapter : 11 SendCommand
ControlAPI -> AuditLog : 12 Append(CommandExecuted)

note bottom
Scenario: [IssueCommand] with lease + layered safety + deterministic sequence + immutable audit.
end note
@enduml
```

```plantuml
@startuml Collaboration2_MonitorStatusAndExport
skinparam linetype ortho

object Operator
object MonitoringUI
object MonitoringService
object EventBus
object StateStore
object ExportService
object TelemetrySubscriber
object AuditLog

Operator -- MonitoringUI
MonitoringUI -- MonitoringService
MonitoringService -- EventBus
MonitoringService -- StateStore
MonitoringService -- ExportService
ExportService -- TelemetrySubscriber
ExportService -- AuditLog

Operator -> MonitoringUI : 1 OpenMonitor
MonitoringUI -> MonitoringService : 2 SubscribeStatus
MonitoringService -> EventBus : 3 Subscribe(TelemetryTopic)
EventBus -> MonitoringService : 4 TelemetryEvent
MonitoringService -> StateStore : 5 UpdateState
MonitoringService -> MonitoringUI : 6 PushStatus
MonitoringService -> ExportService : 7 ExportTelemetry
ExportService -> AuditLog : 8 Append(ExportPerformed)
ExportService -> TelemetrySubscriber : 9 DeliverTelemetry

note bottom
Scenario: [MonitorStatus] + [ExportTelemetry] via event bus and push updates.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SafetyCriticalControl
skinparam packageStyle rectangle

package "ui" as ui {
  note bottom: Operator screens; status push; command entry
}

package "api" as api {
  note bottom: ControlAPI endpoints; request validation; orchestration
}

package "domain" as domain {
  note bottom: Command, Lease, Interlocks, Sequence, State model (pure)
}

package "services" as services {
  note bottom: Auth/Lease/Safety/Monitoring/Export services
}

package "persistence" as persistence {
  note bottom: StateStore, AuditLog, DataContractRegistry
}

package "messaging" as messaging {
  note bottom: EventBus abstraction; topics; replay hooks
}

package "integrations" as integrations {
  note bottom: ControllerAdapter; protocol frames; HIL simulator hooks
}

ui ..> api : uses
api ..> services : uses
services ..> domain : uses
services ..> messaging : uses
services ..> persistence : uses
services ..> integrations : uses
integrations ..> domain : uses
persistence ..> domain : maps

note right of domain
Key constraints:
- deterministic sequencing
- layered interlocks
- abort on unknown/unsafe
- immutable audit entries
end note

note right of integrations
Contract-first, versioned schemas; freeze dates/owners assumed per semantic memory.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SafetyCriticalControl
skinparam componentStyle rectangle

component "MonitoringUI" as MonitoringUI
component "ControlAPI" as ControlAPI
component "AuthService" as AuthService
component "LeaseService" as LeaseService
component "SafetyService" as SafetyService
component "SequenceController" as SequenceController
component "MonitoringService" as MonitoringService
component "ExportService" as ExportService
component "EventBus" as EventBus
component "ControllerAdapter" as ControllerAdapter
database "StateStore" as StateStore
database "AuditLog" as AuditLog
database "DataContractRegistry" as DataContractRegistry
component "TelemetrySubscriber" as TelemetrySubscriber <<external system>>
component "ControllerUnit" as ControllerUnit <<external system>>

interface IAuth
interface ILease
interface ISafety
interface ICommandAPI
interface IMonitor
interface IExport
interface IControllerIO
interface IEventBus

ControlAPI -down-> ICommandAPI
MonitoringService -down-> IMonitor
AuthService -down-> IAuth
LeaseService -down-> ILease
SafetyService -down-> ISafety
ExportService -down-> IExport
ControllerAdapter -down-> IControllerIO
EventBus -down-> IEventBus

MonitoringUI ..> ICommandAPI : uses
MonitoringUI ..> IMonitor : uses

ControlAPI ..> IAuth : requires
ControlAPI ..> ILease : requires
ControlAPI ..> ISafety : requires
ControlAPI ..> SequenceController : uses
ControlAPI ..> IEventBus : publishes
ControlAPI ..> StateStore : reads/writes
ControlAPI ..> AuditLog : appends

MonitoringService ..> IEventBus : subscribes
MonitoringService ..> StateStore : updates
MonitoringService ..> MonitoringUI : pushes

SequenceController ..> IControllerIO : requires
SequenceController ..> IEventBus : publishes
SequenceController ..> AuditLog : appends

ControllerAdapter ..> DataContractRegistry : uses
ControllerAdapter ..> ControllerUnit : communicates

ExportService ..> StateStore : reads
ExportService ..> TelemetrySubscriber : delivers
ExportService ..> AuditLog : appends

note right of AuditLog
Immutable append-only audit trail.
end note

note right of EventBus
Event-driven monitoring/control; decouple producers/consumers.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SafetyCriticalControl
skinparam nodeStyle rectangle

node "Operator Workstation" as WS {
  artifact "MonitoringUI"
}

node "Control Network (HA)" as NET {
  node "AppNode-1" as APP1 <<replica>> {
    artifact "ControlAPI"
    artifact "AuthService"
    artifact "LeaseService"
    artifact "SafetyService"
    artifact "SequenceController"
    artifact "MonitoringService"
    artifact "ExportService"
  }
  node "AppNode-2" as APP2 <<replica>> {
    artifact "ControlAPI"
    artifact "AuthService"
    artifact "LeaseService"
    artifact "SafetyService"
    artifact "SequenceController"
    artifact "MonitoringService"
    artifact "ExportService"
  }

  node "MessageBroker" as MB {
    artifact "EventBus"
  }

  database "StateDB" as StateDB {
    artifact "StateStore"
    artifact "DataContractRegistry"
  }

  database "AuditDB (WORM)" as AuditDB {
    artifact "AuditLog"
  }
}

node "Field Controller Unit" as FCU <<external system>> {
  artifact "ControllerUnit"
}

node "External Subscriber" as EXT <<external system>> {
  artifact "TelemetrySubscriber"
}

WS --> NET : TLS/secured link\nassumption: network security requirements not provided
APP1 --> MB : publish/subscribe
APP2 --> MB : publish/subscribe
APP1 --> StateDB : read/write
APP2 --> StateDB : read/write
APP1 --> AuditDB : append
APP2 --> AuditDB : append
APP1 --> FCU : controller I/O
APP2 --> FCU : controller I/O
APP1 --> EXT : telemetry export
APP2 --> EXT : telemetry export

note right of NET
HA via replicated app nodes.
assumption: explicit availability/latency targets not provided; treat as SLO-driven.
end note

note right of AuditDB
Immutable audit storage (WORM-like) for safety/compliance evidence.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SafetyCriticalControl
left to right direction
skinparam packageStyle rectangle

rectangle "Safety-Critical Control System" as SCS {
  rectangle "MonitoringUI Container" as C_UI <<container>> {
    note bottom: Operator GUI; status push; command forms
  }

  rectangle "ControlAPI Container" as C_API <<container>> {
    note bottom: Command orchestration; validation; exposes ICommandAPI
  }

  rectangle "Core Services Container" as C_SVC <<container>> {
    note bottom: AuthService, LeaseService, SafetyService, SequenceController, MonitoringService, ExportService
  }

  rectangle "Message Broker Container" as C_MB <<container>> {
    note bottom: EventBus topics; decouple; replay hooks
  }

  rectangle "State Store Container" as C_STATE <<container>> {
    note bottom: SystemState persistence; contracts registry
  }

  rectangle "Audit Log Container" as C_AUDIT <<container>> {
    note bottom: Immutable append-only audit entries
  }

  rectangle "Controller Integration Container" as C_ADAPTER <<container>> {
    note bottom: ControllerAdapter; versioned frames; checksums; HIL hooks
  }
}

rectangle "ControllerUnit" as X_CTRL <<external system>>
rectangle "TelemetrySubscriber" as X_SUB <<external system>>

C_UI --> C_API : HTTPS/WebSocket\n[MonitorStatus][IssueCommand]
C_API --> C_SVC : internal RPC\n[Authenticate][AcquireLease][ValidateSafety]
C_SVC --> C_MB : pub/sub\n[TelemetryEvent]
C_SVC --> C_STATE : read/write\n[SystemState]
C_SVC --> C_AUDIT : append\n[ImmutableAudit]
C_SVC --> C_ADAPTER : call\n[ExecuteSequence]
C_ADAPTER --> X_CTRL : serial/Ethernet\n[ContractFirst]
C_SVC --> X_SUB : export\n[ExportTelemetry]

note bottom of SCS
assumption: explicit SLOs (freshness/latency/availability) are to be derived and baselined as testable metrics.
end note
@enduml
```