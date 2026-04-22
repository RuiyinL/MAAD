## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SafetyCriticalControl
left to right direction
skinparam packageStyle rectangle

actor Operator
actor Supervisor
actor MaintenanceTech
actor ExternalExportSystem as ExportSystem
actor FieldController as Controller

rectangle "Safety-Critical Control System" as SCS {
  usecase "Authenticate" as UC_Authenticate
  usecase "Acquire Control Lease" as UC_AcquireLease
  usecase "View Status" as UC_ViewStatus
  usecase "Issue Command" as UC_IssueCommand
  usecase "Execute Sequence" as UC_ExecuteSequence
  usecase "Acknowledge Safety Prompt" as UC_AckPrompt
  usecase "Override / Abort" as UC_Abort
  usecase "Configure Devices" as UC_Configure
  usecase "Export Telemetry" as UC_Export
  usecase "Run Diagnostics" as UC_Diagnostics
  usecase "Review Audit Log" as UC_AuditReview

  UC_IssueCommand ..> UC_Authenticate : <<include>>
  UC_IssueCommand ..> UC_AcquireLease : <<include>>
  UC_ExecuteSequence ..> UC_AckPrompt : <<include>>
  UC_Abort ..> UC_ExecuteSequence : <<extend>>
  UC_Diagnostics ..> UC_ViewStatus : <<include>>
  UC_AuditReview ..> UC_Authenticate : <<include>>
}

Operator --> UC_Authenticate
Operator --> UC_AcquireLease
Operator --> UC_ViewStatus
Operator --> UC_IssueCommand
Operator --> UC_ExecuteSequence
Operator --> UC_AckPrompt
Operator --> UC_Abort
Operator --> UC_AuditReview

Supervisor --> UC_AuditReview
Supervisor --> UC_Abort

MaintenanceTech --> UC_Diagnostics
MaintenanceTech --> UC_Configure
MaintenanceTech --> UC_ViewStatus

ExportSystem --> UC_Export
Controller --> UC_ViewStatus
Controller --> UC_IssueCommand

note right of SCS
assumption: FR/NFR/ASR details not provided; inferred safety-critical remote control system.
assumption: single-operator command-control enforced via lease/lock.
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
  +displayName: String
  +role: String
  +authenticate(credentials: String): AuthToken
  +requestLease(): ControlLease
}

class AuthToken <<immutable>> {
  +tokenId: String
  +issuedAt: Instant
  +expiresAt: Instant
  +subjectId: String
  +isValid(now: Instant): boolean
}

class ControlLease {
  +leaseId: String
  +holderOperatorId: String
  +acquiredAt: Instant
  +expiresAt: Instant
  +isActive(now: Instant): boolean
  +renew(): void
  +release(): void
}

class Command {
  +commandId: String
  +type: String
  +targetDeviceId: String
  +requestedAt: Instant
  +requestedBy: String
  +parameters: Map
  +validate(): boolean
}

class ControlSequence {
  +sequenceId: String
  +name: String
  +steps: List
  +start(command: Command): void
  +abort(reason: String): void
}

class SafetyInterlock {
  +interlockId: String
  +layer: String
  +evaluate(cmd: Command, snapshot: DeviceSnapshot): SafetyDecision
}

class SafetyDecision <<immutable>> {
  +allowed: boolean
  +reasonCode: String
}

class Device {
  +deviceId: String
  +deviceType: String
  +location: String
  +isOnline: boolean
  +apply(command: Command): void
}

class DeviceSnapshot <<immutable>> {
  +snapshotId: String
  +capturedAt: Instant
  +deviceStates: Map
  +ageMs(now: Instant): long
}

class Event {
  +eventId: String
  +eventType: String
  +occurredAt: Instant
  +payload: Map
}

class EventBus {
  +publish(event: Event): void
  +subscribe(topic: String): void
}

class AuditRecord <<immutable>> <<persisted>> {
  +recordId: String
  +timestamp: Instant
  +actorId: String
  +action: String
  +hash: String
}

class AuditLog <<persisted>> {
  +append(record: AuditRecord): void
  +query(filter: Map): List
}

class ControllerAdapter {
  +adapterId: String
  +protocolVersion: String
  +sendCommand(cmd: Command): void
  +readTelemetry(): DeviceSnapshot
}

Operator "1" --> "0..*" ControlLease : holds
Operator "1" --> "0..*" Command : issues
Command "1" --> "0..1" ControlSequence : executes
SafetyInterlock "1..*" --> "1" Command : evaluates
SafetyInterlock "1..*" --> "1" DeviceSnapshot : checks
Device "1..*" o-- "0..*" DeviceSnapshot : snapshots
EventBus "1" --> "0..*" Event : carries
Command "1" --> "0..*" Event : emits
AuditLog "1" *-- "0..*" AuditRecord : stores
ControllerAdapter "1" --> "0..*" Device : controls
ControllerAdapter "1" --> "0..*" DeviceSnapshot : produces

note right of SafetyInterlock
Layered screening per semantic memory:
originating unit + subordinate unit + executing controller.
Abort on unknown/opposite-direction unsafe states.
end note

note right of ControllerAdapter
Interface contract-first:
versioned protocol schemas, explicit owners/freeze dates.
end note

note right of AuditLog
Immutable audit logging required.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SafetyCriticalControl
object operator1 as "operator1:Operator [IssueCommand]" {
  operatorId = "op-101"
  displayName = "Control Room A"
  role = "Operator"
}

object token1 as "token1:AuthToken [Authenticate]" {
  tokenId = "tkn-9f3"
  subjectId = "op-101"
  issuedAt = "2026-04-22T10:00:00Z"
  expiresAt = "2026-04-22T18:00:00Z"
}

object lease1 as "lease1:ControlLease [AcquireLease]" {
  leaseId = "lease-77"
  holderOperatorId = "op-101"
  acquiredAt = "2026-04-22T10:00:05Z"
  expiresAt = "2026-04-22T10:05:05Z"
}

object cmd1 as "cmd1:Command [IssueCommand]" {
  commandId = "cmd-5001"
  type = "SetLaneDirection"
  targetDeviceId = "lane-12"
  requestedAt = "2026-04-22T10:00:10Z"
  requestedBy = "op-101"
}

object snap1 as "snap1:DeviceSnapshot [ViewStatus]" {
  snapshotId = "snap-abc"
  capturedAt = "2026-04-22T10:00:09Z"
}

object interlock1 as "interlock1:SafetyInterlock [ExecuteSequence]" {
  interlockId = "si-origin"
  layer = "OriginatingUnit"
}

object audit1 as "audit1:AuditRecord [ReviewAuditLog]" {
  recordId = "ar-1"
  timestamp = "2026-04-22T10:00:10Z"
  actorId = "op-101"
  action = "IssueCommand cmd-5001"
  hash = "sha256:..."
}

operator1 -- token1
operator1 -- lease1
operator1 -- cmd1
cmd1 -- snap1
interlock1 -- cmd1
audit1 .. cmd1 : references
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_CommandLifecycle
hide empty description

state "Command Lifecycle" as CL {
  [*] --> Draft : create
  Draft --> Validating : validate()
  Validating --> Rejected : [invalid] / emit(Event.ValidationFailed)
  Validating --> PendingLease : [valid] / requestLease
  PendingLease --> Rejected : [leaseDenied] / emit(Event.LeaseDenied)
  PendingLease --> SafetyScreening : [leaseGranted] / snapshotFetch

  SafetyScreening --> Rejected : [unsafeOrUnknown] / emit(Event.SafetyAbort)
  SafetyScreening --> Scheduled : [safe] / enqueueSequence

  Scheduled --> Executing : start
  Executing --> Completed : [ackReceived] / emit(Event.CommandCompleted)
  Executing --> Aborted : abort
  Executing --> Failed : [timeoutOrError] / emit(Event.CommandFailed)

  Rejected --> [*]
  Completed --> [*]
  Aborted --> [*]
  Failed --> [*]
}

note right of CL
assumption: safety screening includes multi-layer interlocks and rejects unknown/stale snapshots.
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
:Select target device;
:Fetch latest DeviceSnapshot;
if (Snapshot fresh?) then (yes)
  :Compose Command;
  :Validate Command;
  fork
    :Run SafetyInterlock (Originating);
  fork again
    :Run SafetyInterlock (Subordinate);
  fork again
    :Run SafetyInterlock (Executing Controller);
  end fork
  if (All interlocks allow?) then (yes)
    :Persist AuditRecord (immutable);
    :Publish CommandIssued Event;
    :SendCommand via ControllerAdapter;
    :Await Ack/Result;
    if (Ack received before timeout?) then (yes)
      :Publish CommandCompleted Event;
      :Update GUI via push events;
    else (no)
      :Publish CommandFailed Event;
      :Abort / Hold Safe;
    endif
  else (no)
    :Publish SafetyAbort Event;
    :Show Safety Prompt / Block;
  endif
else (no)
  :Publish StaleSnapshot Event;
  :Block command;
endif
stop

note right
assumption: timeouts/thresholds are SLO-driven; exact values not provided.
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_S1_IssueCommand
title S1: Issue Command with Lease + Safety Interlocks

actor Operator
participant "GUI" as GUI
participant "AuthService" as AuthService
participant "LeaseService" as LeaseService
participant "ControlAPI" as ControlAPI
participant "SafetyService" as SafetyService
participant "TelemetryService" as TelemetryService
participant "ControllerAdapter" as ControllerAdapter
database "AuditLog" as AuditLog
queue "EventBus" as EventBus

Operator -> GUI : IssueCommand
GUI -> AuthService : Authenticate
AuthService --> GUI : AuthToken

GUI -> LeaseService : AcquireLease
LeaseService --> GUI : ControlLease

GUI -> ControlAPI : SubmitCommand
ControlAPI -> TelemetryService : FetchSnapshot
TelemetryService --> ControlAPI : DeviceSnapshot

ControlAPI -> SafetyService : EvaluateInterlocks
SafetyService --> ControlAPI : SafetyDecision

alt allowed
  ControlAPI -> AuditLog : AppendAuditRecord
  ControlAPI -> EventBus : Publish(CommandIssued)
  ControlAPI -> ControllerAdapter : SendCommand
  ControllerAdapter --> ControlAPI : Ack
  ControlAPI -> EventBus : Publish(CommandCompleted)
  EventBus --> GUI : PushStatusUpdate
else blocked
  ControlAPI -> EventBus : Publish(SafetyAbort)
  EventBus --> GUI : PushSafetyPrompt
end

note over ControlAPI,ControllerAdapter
assumption: deterministic sequencing and abort-on-unknown enforced end-to-end.
end note
@enduml
```

```plantuml
@startuml Sequence_S2_ExportTelemetry
title S2: Export Telemetry (One-way data export)

actor ExportSystem
participant "ExportAPI" as ExportAPI
participant "TelemetryService" as TelemetryService
queue "EventBus" as EventBus
database "ExportStore" as ExportStore

ExportSystem -> ExportAPI : RequestExport
ExportAPI -> TelemetryService : QueryTelemetryWindow
TelemetryService --> ExportAPI : TelemetryBatch
ExportAPI -> ExportStore : PersistExportBatch
ExportAPI -> EventBus : Publish(TelemetryExported)
ExportAPI --> ExportSystem : ExportPayload

note right of ExportAPI
assumption: export is outbound-only; no control commands accepted from ExportSystem.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_S1_IssueCommand
title Collaboration S1: Issue Command with Lease + Safety Interlocks

actor Operator
rectangle GUI
rectangle AuthService
rectangle LeaseService
rectangle ControlAPI
rectangle SafetyService
rectangle TelemetryService
rectangle ControllerAdapter
database AuditLog
queue EventBus

Operator -- GUI
GUI -- AuthService
GUI -- LeaseService
GUI -- ControlAPI
ControlAPI -- TelemetryService
ControlAPI -- SafetyService
ControlAPI -- AuditLog
ControlAPI -- ControllerAdapter
ControlAPI -- EventBus
EventBus -- GUI

GUI : 1 IssueCommand
GUI -> AuthService : 2 Authenticate
GUI -> LeaseService : 3 AcquireLease
GUI -> ControlAPI : 4 SubmitCommand
ControlAPI -> TelemetryService : 5 FetchSnapshot
ControlAPI -> SafetyService : 6 EvaluateInterlocks
ControlAPI -> AuditLog : 7 AppendAuditRecord
ControlAPI -> ControllerAdapter : 8 SendCommand
ControlAPI -> EventBus : 9 Publish(CommandCompleted)
EventBus -> GUI : 10 PushStatusUpdate

note bottom
Scenario S1 derived from semantic memory: single-operator lease + layered interlocks + immutable audit + event-driven GUI updates.
end note
@enduml
```

```plantuml
@startuml Collaboration_S2_ExportTelemetry
title Collaboration S2: Export Telemetry (One-way export)

actor ExportSystem
rectangle ExportAPI
rectangle TelemetryService
database ExportStore
queue EventBus

ExportSystem -- ExportAPI
ExportAPI -- TelemetryService
ExportAPI -- ExportStore
ExportAPI -- EventBus

ExportSystem -> ExportAPI : 1 RequestExport
ExportAPI -> TelemetryService : 2 QueryTelemetryWindow
ExportAPI -> ExportStore : 3 PersistExportBatch
ExportAPI -> EventBus : 4 Publish(TelemetryExported)
ExportAPI --> ExportSystem : 5 ExportPayload

note bottom
Scenario S2 derived from semantic memory: external one-way data export with event publication.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SafetyCriticalControl
skinparam packageStyle rectangle

package "ui" as pkg_ui {
  note bottom: Operator GUI (push updates)
}

package "api" as pkg_api {
  note bottom: ControlAPI + ExportAPI (REST/IPC)
}

package "domain" as pkg_domain {
  note bottom: Commands, sequences, safety rules
}

package "application" as pkg_app {
  note bottom: Orchestration services, SLO timers
}

package "infrastructure" as pkg_infra {
  note bottom: EventBus, persistence, adapters
}

package "integrations" as pkg_int {
  note bottom: ControllerAdapter (versioned contracts)
}

pkg_ui ..> pkg_api : uses
pkg_api ..> pkg_app : calls
pkg_app ..> pkg_domain : uses
pkg_app ..> pkg_infra : uses
pkg_infra ..> pkg_int : uses
pkg_int ..> pkg_domain : maps

note right of pkg_int
Contract-first stubs:
versioned schemas + owners + freeze dates.
end note

note right of pkg_infra
Immutable audit logging + event-driven monitoring.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SafetyCriticalControl
skinparam componentStyle rectangle

artifact "GUI" as GUI
artifact "AuthService" as AuthService
artifact "LeaseService" as LeaseService
artifact "ControlAPI" as ControlAPI
artifact "SafetyService" as SafetyService
artifact "TelemetryService" as TelemetryService
artifact "ExportAPI" as ExportAPI
artifact "ControllerAdapter" as ControllerAdapter
artifact "EventBus" as EventBus
database "AuditLog" as AuditLog
database "ExportStore" as ExportStore

interface IAuth
interface ILease
interface IControl
interface ISafety
interface ITelemetry
interface IExport
interface IController

AuthService - IAuth
LeaseService - ILease
ControlAPI - IControl
SafetyService - ISafety
TelemetryService - ITelemetry
ExportAPI - IExport
ControllerAdapter - IController

GUI ..> IAuth
GUI ..> ILease
GUI ..> IControl

ControlAPI ..> ISafety
ControlAPI ..> ITelemetry
ControlAPI ..> IController
ControlAPI ..> AuditLog
ControlAPI ..> EventBus

TelemetryService ..> IController
TelemetryService ..> EventBus

ExportAPI ..> ITelemetry
ExportAPI ..> ExportStore
ExportAPI ..> EventBus

note right of ControllerAdapter
Versioned data contracts; simulator/HIL-friendly boundary.
end note

note bottom of LeaseService
Single-operator command-control via lease/lock.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SafetyCriticalControl
skinparam nodesep 35
skinparam ranksep 35

node "Operator Workstation" as WS {
  artifact "GUI" as A_GUI
}

node "Control Network (HA Pair)" as NET {
  node "AppServer-1" as APP1 {
    artifact "ControlAPI"
    artifact "AuthService"
    artifact "LeaseService"
    artifact "SafetyService"
    artifact "TelemetryService"
    artifact "ExportAPI"
  }
  node "AppServer-2" as APP2 {
    artifact "ControlAPI (replica)"
    artifact "AuthService (replica)"
    artifact "LeaseService (replica)"
    artifact "SafetyService (replica)"
    artifact "TelemetryService (replica)"
    artifact "ExportAPI (replica)"
  }

  node "Message Broker" as MQ {
    artifact "EventBus"
  }

  database "Audit DB" as AUDDB {
    artifact "AuditLog"
  }

  database "Export DB" as EXPDB {
    artifact "ExportStore"
  }
}

node "Field Site" as FIELD {
  node "Controller Host" as CH {
    artifact "ControllerAdapter"
  }
  node "Field Controller" as FC {
    artifact "Controller Firmware"
  }
}

node "External Network" as EXT {
  node "ExternalExportSystem" as EES
}

WS -- APP1 : HTTPS/IPC
WS -- APP2 : HTTPS/IPC
APP1 -- MQ : pub/sub
APP2 -- MQ : pub/sub
APP1 -- AUDDB : append/query
APP2 -- AUDDB : append/query
APP1 -- EXPDB : write/read
APP2 -- EXPDB : write/read
APP1 -- CH : control/telemetry link
APP2 -- CH : control/telemetry link
CH -- FC : fieldbus/serial

EES -- APP1 : export only
EES -- APP2 : export only

note right of NET
assumption: high availability required; active-active app tier.
SLOs not provided; treat latency/availability as measurable SLIs at API + controller boundary.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SafetyCriticalControl
skinparam packageStyle rectangle

rectangle "Operator Workstation" as C_WS {
  rectangle "GUI Container\n[OperatorUI]\nResponsibilities: command entry, prompts, live status" as CON_GUI
}

rectangle "Control Platform" as C_CP {
  rectangle "ControlAPI Container\n[CommandControl]\nResponsibilities: validate, orchestrate, publish events" as CON_ControlAPI
  rectangle "SafetyService Container\n[Interlocks]\nResponsibilities: layered safety screening, abort rules" as CON_Safety
  rectangle "TelemetryService Container\n[FreshStatus]\nResponsibilities: read controller telemetry, create snapshots" as CON_Telemetry
  rectangle "AuthService Container\n[SecurityCheck]\nResponsibilities: authentication, token issuance" as CON_Auth
  rectangle "LeaseService Container\n[LeaseLock]\nResponsibilities: single-operator lease/renew/release" as CON_Lease
  rectangle "ExportAPI Container\n[OneWayExport]\nResponsibilities: export telemetry payloads only" as CON_Export

  rectangle "EventBus Container\n[Broker]\nResponsibilities: pub/sub for telemetry + command events" as CON_EventBus
  rectangle "AuditLog DB\n[Immutable]\nResponsibilities: append-only audit records" as CON_AuditDB
  rectangle "ExportStore DB\n[Export]\nResponsibilities: persist exported batches" as CON_ExportDB
}

rectangle "Field Site" as C_Field {
  rectangle "ControllerAdapter Container\n[ProtocolContract]\nResponsibilities: versioned protocol, command/telemetry translation" as CON_Adapter
  rectangle "Field Controller\nResponsibilities: execute commands, emit telemetry" as CON_Controller
}

rectangle "External Export System" as C_External {
  rectangle "ExportSystem\nResponsibilities: receive payloads" as CON_ExternalExport
}

CON_GUI --> CON_Auth : authenticate
CON_GUI --> CON_Lease : acquireLease
CON_GUI --> CON_ControlAPI : submitCommand
CON_ControlAPI --> CON_Telemetry : fetchSnapshot
CON_ControlAPI --> CON_Safety : evaluateInterlocks
CON_ControlAPI --> CON_AuditDB : appendAudit
CON_ControlAPI --> CON_EventBus : publishEvents
CON_Telemetry --> CON_Adapter : readTelemetry
CON_ControlAPI --> CON_Adapter : sendCommand
CON_Adapter --> CON_Controller : fieldProtocol

CON_Export --> CON_Telemetry : queryTelemetry
CON_Export --> CON_ExportDB : persistBatch
CON_Export --> CON_EventBus : publishExported
CON_Export --> CON_ExternalExport : exportPayload

CON_EventBus --> CON_GUI : pushUpdates

note right of CON_Adapter
Contract-first boundary:
versioned schemas + stubs to unblock integration.
end note

note bottom of CON_Lease
Lease/lock prevents concurrent operators from issuing conflicting commands.
end note
@enduml
```