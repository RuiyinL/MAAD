## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction

actor Operator
actor Supervisor
actor MaintenanceTech
actor ExternalDataConsumer as DataConsumer
actor ControllerUnit as Controller

rectangle "RLCS Reversible Lane Control System" as RLCS {
  usecase "Acquire Device\nStatus" as UC_AcquireStatus
  usecase "Request Lane\nMode Change" as UC_RequestMode
  usecase "Execute Safety\nInterlocks" as UC_Interlocks
  usecase "Issue Controller\nCommands" as UC_IssueCmd
  usecase "Acknowledge/\nConfirm Action" as UC_Confirm
  usecase "View Live\nTelemetry" as UC_ViewTelemetry
  usecase "Export One-Way\nData Feed" as UC_Export
  usecase "Manage Lease/\nLock Control" as UC_Lease
  usecase "Review Audit\nLog" as UC_Audit
  usecase "Run Diagnostics\n(HIL/SIM)" as UC_Diag
}

Operator --> UC_ViewTelemetry
Operator --> UC_RequestMode
Operator --> UC_Confirm
Operator --> UC_Lease

Supervisor --> UC_Audit
Supervisor --> UC_Lease

MaintenanceTech --> UC_Diag
MaintenanceTech --> UC_AcquireStatus

DataConsumer --> UC_Export

Controller --> UC_AcquireStatus
Controller --> UC_IssueCmd

UC_RequestMode ..> UC_Lease : <<include>>
UC_RequestMode ..> UC_Interlocks : <<include>>
UC_RequestMode ..> UC_IssueCmd : <<include>>
UC_RequestMode ..> UC_Confirm : <<include>>

UC_ViewTelemetry ..> UC_AcquireStatus : <<include>>
UC_Export ..> UC_AcquireStatus : <<include>>

UC_IssueCmd ..> UC_Interlocks : <<include>>

note bottom of RLCS
assumption: FR/NFR/ASR details were not provided; inferred actors/use cases from
semantic memory for RLCS: single-operator lease/lock, deterministic sequencing,
event-driven telemetry push, one-way external export, immutable audit logging,
multi-layer interlocks (originating + subordinate + executing controller).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
hide circle
skinparam classAttributeIconSize 0

class Operator {
  +operatorId: String
  +name: String
  +role: String
}

class Lease {
  +leaseId: String
  +holderOperatorId: String
  +expiresAtUtc: DateTime
  +isValid(nowUtc: DateTime): boolean
  +renew(durationSec: int)
  +release()
}

class LaneSegment {
  +segmentId: String
  +name: String
  +currentMode: LaneMode
  +requestedMode: LaneMode
  +lastModeChangeUtc: DateTime
  +requestModeChange(target: LaneMode)
}

enum LaneMode {
  CLOSED
  OPEN_EASTBOUND
  OPEN_WESTBOUND
  TRANSITIONING
  FAULT_HOLD
}

class ControlCommand {
  +commandId: String
  +segmentId: String
  +targetMode: LaneMode
  +issuedByOperatorId: String
  +issuedAtUtc: DateTime
  +correlationId: String
}

class DeviceStatus {
  +deviceId: String
  +segmentId: String
  +deviceType: String
  +state: String
  +direction: String
  +updatedAtUtc: DateTime
  +isFresh(maxAgeSec: int, nowUtc: DateTime): boolean
}

class SafetyInterlockResult {
  +resultId: String
  +commandId: String
  +isSafe: boolean
  +reasonCode: String
  +evaluatedAtUtc: DateTime
}

class ControllerAdapter {
  +adapterVersion: String
  +sendCommand(cmd: ControlCommand): boolean
  +readStatus(segmentId: String): DeviceStatus[*]
}

class EventBus {
  +publish(eventType: String, payload: String)
  +subscribe(eventType: String)
}

class AuditEvent {
  +eventId: String
  +eventType: String
  +actorId: String
  +occurredAtUtc: DateTime
  +payloadHash: String
}

class DataExportFeed {
  +feedId: String
  +schemaVersion: String
  +publishSnapshot(status: DeviceStatus[*])
}

Operator "1" -- "0..1" Lease : holds >
LaneSegment "1" o-- "0..*" DeviceStatus : has >
LaneSegment "1" o-- "0..*" ControlCommand : commands >
ControlCommand "1" --> "1" SafetyInterlockResult : produces >
ControllerAdapter ..> ControlCommand : sends >
ControllerAdapter ..> DeviceStatus : reads >
EventBus ..> DeviceStatus : publishes >
EventBus ..> ControlCommand : publishes >
EventBus ..> SafetyInterlockResult : publishes >
AuditEvent ..> Operator : actor >
AuditEvent ..> ControlCommand : about >
DataExportFeed ..> DeviceStatus : exports >

note right of ControllerAdapter
Contract-first integration: versioned protocol/data contracts;
unknown vendor details treated as stubbed interfaces with owners/freeze dates.
end note

note bottom of DeviceStatus
ASR: telemetry freshness + deterministic sequencing.
Tactic: reject stale status (e.g., maxAgeSec <= 3) for safety checks.
end note

note bottom of AuditEvent
ASR: immutable audit logging.
Tactic: append-only persisted events + payload hashing for integrity evidence.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView
object operator1 as "operator1:Operator [RequestModeChange]" {
  operatorId = "op-42"
  name = "A. Rivera"
  role = "Operator"
}

object lease1 as "lease1:Lease [ManageLease]" {
  leaseId = "lease-9c1"
  holderOperatorId = "op-42"
  expiresAtUtc = "2026-04-22T10:20:00Z"
}

object segment1 as "segment1:LaneSegment [RequestModeChange]" {
  segmentId = "seg-7"
  name = "Bridge Approach"
  currentMode = "CLOSED"
  requestedMode = "OPEN_EASTBOUND"
  lastModeChangeUtc = "2026-04-22T10:12:10Z"
}

object cmd1 as "cmd1:ControlCommand [IssueCommand]" {
  commandId = "cmd-10017"
  segmentId = "seg-7"
  targetMode = "OPEN_EASTBOUND"
  issuedByOperatorId = "op-42"
  issuedAtUtc = "2026-04-22T10:15:01Z"
  correlationId = "corr-55aa"
}

object ds1 as "ds1:DeviceStatus [AcquireStatus]" {
  deviceId = "gate-3"
  segmentId = "seg-7"
  deviceType = "BarrierGate"
  state = "CLOSED"
  direction = "N/A"
  updatedAtUtc = "2026-04-22T10:15:00Z"
}

object ds2 as "ds2:DeviceStatus [AcquireStatus]" {
  deviceId = "sign-8"
  segmentId = "seg-7"
  deviceType = "LaneArrowSign"
  state = "RED_X"
  direction = "EASTBOUND"
  updatedAtUtc = "2026-04-22T10:15:00Z"
}

object interlock1 as "interlock1:SafetyInterlockResult [SafetyInterlocks]" {
  resultId = "si-771"
  commandId = "cmd-10017"
  isSafe = "true"
  reasonCode = "OK_ALL_CLEAR"
  evaluatedAtUtc = "2026-04-22T10:15:01Z"
}

operator1 -- lease1
segment1 -- ds1
segment1 -- ds2
segment1 -- cmd1
cmd1 -- interlock1

note bottom
assumption: object values reflect safety-critical reversible-lane control:
barrier gates + lane arrow signs, with operator lease and safety interlock result.
end note
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_LaneSegment
hide empty description

state "LaneSegment Lifecycle" as LSL {
  [*] --> CLOSED

  CLOSED --> TRANSITIONING : RequestModeChange(target!=CLOSED)\n[LeaseValid]/startSequence()
  TRANSITIONING --> OPEN_EASTBOUND : InterlocksPass(target=OPEN_EASTBOUND)\n/doExecuteCommands()
  TRANSITIONING --> OPEN_WESTBOUND : InterlocksPass(target=OPEN_WESTBOUND)\n/doExecuteCommands()
  TRANSITIONING --> FAULT_HOLD : InterlocksFail/abortAndHold()
  TRANSITIONING --> CLOSED : OperatorCancel/rollbackToSafe()

  OPEN_EASTBOUND --> TRANSITIONING : RequestModeChange(target!=OPEN_EASTBOUND)\n[LeaseValid]/startSequence()
  OPEN_WESTBOUND --> TRANSITIONING : RequestModeChange(target!=OPEN_WESTBOUND)\n[LeaseValid]/startSequence()

  OPEN_EASTBOUND --> FAULT_HOLD : UnsafeDetected(staleStatus or oppositeDir)/abortAndHold()
  OPEN_WESTBOUND --> FAULT_HOLD : UnsafeDetected(staleStatus or oppositeDir)/abortAndHold()
  CLOSED --> FAULT_HOLD : UnsafeDetected/hold()

  FAULT_HOLD --> CLOSED : RecoverToSafe\n[SupervisorOverride]/forceSafeClose()
  FAULT_HOLD --> TRANSITIONING : RetryModeChange\n[LeaseValid]/startSequence()

  note right of TRANSITIONING
  Deterministic sequencing + multi-layer screening:
  originating unit -> subordinate unit -> executing controller.
  Abort on unknown/opposite-direction unsafe states.
  end note
}
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_RequestModeChange
start
:Acquire Lease [SecurityCheck];
if (Lease valid?) then (yes)
  :Select LaneSegment;
  :Enter Target LaneMode;
  :Fetch latest DeviceStatus;
  note right
    ASR: freshness gate
    reject stale status (e.g., maxAge <= 3s)
  end note
  if (Status fresh?) then (yes)
    :Run Safety Interlocks;
    if (Interlocks pass?) then (yes)
      :Prompt Operator Confirm;
      if (Confirmed?) then (yes)
        :Publish ControlCommand to EventBus;
        fork
          :ControllerAdapter sendCommand();
        fork again
          :Append AuditEvent (immutable);
        fork again
          :Push Telemetry update to GUI;
        end fork
        :Await Command Ack/Timeout;
        note right
          NFR/ASR: deterministic response windows;
          apply retry/backoff; fail-safe on timeout.
        end note
        if (Ack OK?) then (yes)
          :Update LaneSegment mode;
        else (no)
          :Abort and Hold (FAULT_HOLD);
        endif
      else (no)
        :Cancel request;
      endif
    else (no)
      :Abort and Hold (FAULT_HOLD);
    endif
  else (no)
    :Abort and Hold (FAULT_HOLD);
  endif
  :Release/Renew Lease;
else (no)
  :Deny Control (No Lease);
endif
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_RequestModeChange
title S1 - Request Lane Mode Change (with interlocks + audit)

actor Operator
participant "RLCS GUI" as Gui
participant "Control API" as Api
participant "LeaseManager" as LeaseMgr
participant "SafetyInterlockService" as InterlockSvc
participant "EventBus" as Bus
participant "ControllerAdapter" as Ctrl
database "OperationalDB" as Db
database "AuditLog" as Audit

Operator -> Gui : RequestModeChange
Gui -> Api : RequestModeChange
Api -> LeaseMgr : ValidateLease
LeaseMgr --> Api : LeaseValid

Api -> Ctrl : ReadStatus
Ctrl --> Api : DeviceStatus[]
Api -> InterlockSvc : EvaluateInterlocks
InterlockSvc --> Api : InterlocksPass

Api -> Gui : PromptConfirm
Operator -> Gui : ConfirmAction
Gui -> Api : ConfirmAction

Api -> Bus : PublishControlCommand
Bus --> Ctrl : ControlCommand (async)
Ctrl -> Bus : CommandAck (async)

Api -> Audit : AppendAuditEvent
Audit --> Api : AppendOK

Api -> Db : UpdateLaneSegmentMode
Db --> Api : UpdateOK
Api --> Gui : ModeChangeResult

note over Api
ASR: deterministic sequencing; abort on unknown/opposite-direction unsafe states;
enforce single-operator command-control via lease/lock.
end note
@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_ExportOneWayData
title S2 - Export One-Way Data Feed (external consumer)

actor DataConsumer
participant "DataExportService" as ExportSvc
participant "EventBus" as Bus
database "OperationalDB" as Db

DataConsumer -> ExportSvc : SubscribeFeed
ExportSvc -> Bus : SubscribeTelemetry
Bus --> ExportSvc : DeviceStatusChanged (async)

ExportSvc -> Db : ReadLatestSnapshot
Db --> ExportSvc : DeviceStatus[]
ExportSvc --> DataConsumer : PublishSnapshot (one-way)

note over ExportSvc
ASR: external export is one-way (no control backchannel).
Contract-first: versioned schemaVersion for payload.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_RequestModeChange
title S1 Collaboration - Request Lane Mode Change

object Operator
object "RLCS GUI" as Gui
object "Control API" as Api
object "LeaseManager" as LeaseMgr
object "SafetyInterlockService" as InterlockSvc
object "EventBus" as Bus
object "ControllerAdapter" as Ctrl
object "AuditLog" as Audit

Operator -- Gui
Gui -- Api
Api -- LeaseMgr
Api -- InterlockSvc
Api -- Bus
Bus -- Ctrl
Api -- Audit

Operator -> Gui : 1 RequestModeChange
Gui -> Api : 2 RequestModeChange
Api -> LeaseMgr : 3 ValidateLease
Api -> Ctrl : 4 ReadStatus
Api -> InterlockSvc : 5 EvaluateInterlocks
Api -> Gui : 6 PromptConfirm
Operator -> Gui : 7 ConfirmAction
Gui -> Api : 8 ConfirmAction
Api -> Bus : 9 PublishControlCommand
Bus -> Ctrl : 10 ControlCommand
Api -> Audit : 11 AppendAuditEvent

note bottom
Scenario S1: operator-initiated mode change guarded by lease + interlocks,
executed via event bus to controller adapter with immutable audit logging.
end note
@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_ExportOneWayData
title S2 Collaboration - Export One-Way Data Feed

object DataConsumer
object "DataExportService" as ExportSvc
object "EventBus" as Bus
object "OperationalDB" as Db

DataConsumer -- ExportSvc
ExportSvc -- Bus
ExportSvc -- Db

DataConsumer -> ExportSvc : 1 SubscribeFeed
ExportSvc -> Bus : 2 SubscribeTelemetry
Bus -> ExportSvc : 3 DeviceStatusChanged
ExportSvc -> Db : 4 ReadLatestSnapshot
ExportSvc -> DataConsumer : 5 PublishSnapshot

note bottom
Scenario S2: one-way export; consumer cannot issue control commands; payload is versioned.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as UI {
  note bottom
  Responsibility: operator GUI; live telemetry; confirmation prompts.
  end note
}

package "api" as API {
  note bottom
  Responsibility: control endpoints; orchestrate workflows; validation.
  end note
}

package "domain" as DOMAIN {
  note bottom
  Responsibility: LaneSegment, commands, interlocks, invariants (safety).
  end note
}

package "application" as APP {
  note bottom
  Responsibility: use-cases; deterministic sequencing; timeouts/retries.
  end note
}

package "integrations" as INTEG {
  note bottom
  Responsibility: ControllerAdapter + versioned protocol contracts; external export.
  end note
}

package "messaging" as MSG {
  note bottom
  Responsibility: EventBus abstraction; publish/subscribe.
  end note
}

package "persistence" as PERSIST {
  note bottom
  Responsibility: OperationalDB + AuditLog append-only storage.
  end note
}

UI ..> API
API ..> APP
APP ..> DOMAIN
APP ..> MSG
APP ..> INTEG
APP ..> PERSIST
INTEG ..> MSG
INTEG ..> DOMAIN
PERSIST ..> DOMAIN

note right of INTEG
ASR: contract-first stubs for unknown vendor I/O; versioned schemas + freeze dates.
end note

note right of PERSIST
ASR: immutable audit logging (append-only) for safety accountability.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

artifact "RLCS GUI" as Gui <<UI>> 
artifact "Control API" as Api <<Service>> 
artifact "LeaseManager" as LeaseMgr <<Service>> 
artifact "SafetyInterlockService" as InterlockSvc <<Service>> 
artifact "TelemetryService" as TelemetrySvc <<Service>> 
artifact "DataExportService" as ExportSvc <<Service>> 
artifact "EventBus" as Bus <<Broker>> 
database "OperationalDB" as Db
database "AuditLog" as Audit

interface IControlApi
interface ILease
interface IInterlocks
interface IEventBus
interface IController
interface IExport

Gui - IControlApi
Api ..|> IControlApi

Api - ILease
LeaseMgr ..|> ILease

Api - IInterlocks
InterlockSvc ..|> IInterlocks

Api - IEventBus
TelemetrySvc - IEventBus
ExportSvc - IEventBus
Bus ..|> IEventBus

Ctrl ..|> IController
Api ..> IController : reads status
Bus ..> Ctrl : publishes commands

Api ..> Db
Api ..> Audit
TelemetrySvc ..> Gui : pushes updates
ExportSvc ..> Db
ExportSvc ..> IExport
DataExportService - IExport

note right of Ctrl
Plugin/driver boundary:
ControllerAdapter is replaceable per vendor protocol; versioned contracts.
end note

note bottom of Api
Tactics: lease/lock enforcement; deterministic workflow; fail-safe abort to FAULT_HOLD;
emit audit events for all control actions.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam componentStyle rectangle

node "Operator Workstation" as WS {
  artifact "RLCS GUI" as A_Gui
}

node "Control Network (Secure VLAN)" as VLAN {
  node "App Server A" as AppA {
    artifact "Control API" as A_ApiA
    artifact "LeaseManager" as A_LeaseA
    artifact "SafetyInterlockService" as A_IntA
    artifact "TelemetryService" as A_TelA
    artifact "DataExportService" as A_ExpA
  }
  node "App Server B" as AppB {
    artifact "Control API" as A_ApiB
    artifact "LeaseManager" as A_LeaseB
    artifact "SafetyInterlockService" as A_IntB
    artifact "TelemetryService" as A_TelB
    artifact "DataExportService" as A_ExpB
  }

  node "Message Broker" as Broker {
    artifact "EventBus" as A_Bus
  }

  node "DB Server" as DBS {
    database "OperationalDB" as D_Db
    database "AuditLog (append-only)" as D_Audit
  }

  node "Controller Gateway" as GW {
    artifact "ControllerAdapter" as A_Ctrl
  }

  node "Lane Controller Unit" as Controller {
    artifact "Vendor Controller Firmware" as FW
  }
}

node "External Network (One-way)" as ONEWAY {
  node "External Data Consumer" as Consumer
}

WS --> VLAN : HTTPS/WebSocket\n(telemetry push)
AppA --> Broker : publish/subscribe
AppB --> Broker : publish/subscribe
Broker --> GW : command/events
GW --> Controller : fieldbus/serial/Ethernet\n(contract-stubbed)

AppA --> DBS : SQL
AppB --> DBS : SQL
AppA --> ONEWAY : export feed (one-way)
AppB --> ONEWAY : export feed (one-way)

note right of AppA
NFR/ASR inferred: high availability via active-active app servers.
Deterministic processing enforced at application layer with timeouts.
end note

note right of DBS
ASR: immutable audit; keep separate append-only storage/log.
end note

note right of ONEWAY
ASR: one-way data export; no inbound control path.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
skinparam rectangle {
  roundCorner 10
}

rectangle "Operator Workstation" as WS {
  rectangle "RLCS GUI\n[ViewTelemetry][ConfirmAction]" as GUI
}

rectangle "Control Plane" as CP {
  rectangle "Control API\n[RequestModeChange]\n[LeaseEnforced]" as API
  rectangle "SafetyInterlockService\n[MultiLayerInterlocks]" as INT
  rectangle "LeaseManager\n[SingleOperatorLock]" as LEASE
  rectangle "TelemetryService\n[PushToGUI]" as TEL
  rectangle "DataExportService\n[OneWayExport]\n[SchemaVersioned]" as EXP
  rectangle "EventBus\n[EventDriven]" as BUS
  rectangle "ControllerAdapter\n[ContractFirst][Plugin]" as ADAPTER
  rectangle "OperationalDB\n[State]" as DB
  rectangle "AuditLog\n[AppendOnly][Immutable]" as AUDIT
}

rectangle "Field Devices" as FIELD {
  rectangle "Lane Controller Unit\n[ExecutingController]" as CTRLUNIT
}

rectangle "External Systems" as EXT {
  rectangle "External Data Consumer\n[ReadOnly]" as CONSUMER
}

GUI --> API : HTTPS/WebSocket
API --> LEASE : validate/renew
API --> INT : evaluate interlocks
API --> BUS : publish ControlCommand
BUS --> ADAPTER : deliver command (async)
ADAPTER --> CTRLUNIT : vendor protocol (versioned)
ADAPTER --> BUS : publish status/ack (async)
BUS --> TEL : telemetry events
TEL --> GUI : push updates

API --> DB : read/write state
API --> AUDIT : append audit
EXP --> BUS : subscribe telemetry
EXP --> DB : read snapshot
EXP --> CONSUMER : one-way feed

note right of ADAPTER
ASR: unknown vendor interfaces => versioned stubs/data contracts, owners, freeze dates.
end note

note bottom of INT
Safety tactic: abort on stale/unknown/opposite-direction unsafe states; hold in FAULT_HOLD.
end note
@enduml
```