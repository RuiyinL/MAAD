## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseView
left to right direction
skinparam packageStyle rectangle

actor Operator
actor Admin as SystemAdministrator
actor Maintainer as MaintenanceUser
actor RemoteUser
actor ExternalSystem
actor "Field Technician" as FieldTechnician

rectangle "RLCS (I-15 Reversible Lane Control System)" {
  usecase "Log On" as UC_LogOn
  usecase "View Status" as UC_ViewStatus
  usecase "Acquire Command Control" as UC_CommandControl
  usecase "Execute Open/Close\nSequence" as UC_OperateLanes
  usecase "Override Device\nStatus" as UC_Override
  usecase "Configure System" as UC_Configure
  usecase "Manage Users" as UC_ManageUsers
  usecase "Review/Export Logs" as UC_Logs
  usecase "Enter Work Order\n& Diary" as UC_WorkDiary
  usecase "Export Status Data" as UC_ExportStatus
  usecase "Degraded/Alternate\nControl" as UC_Degraded

  usecase "Authenticate User" as UC_Auth <<include>>
  usecase "Authorize Action" as UC_Authorize <<include>>
  usecase "Safety Screen Command" as UC_Safety <<include>>
  usecase "Audit Log Activity" as UC_Audit <<include>>
  usecase "Step-up Auth\n(Rules)" as UC_StepUp <<extend>>
  usecase "Takeover Command\nControl" as UC_Takeover <<extend>>
}

Operator --> UC_LogOn
Operator --> UC_ViewStatus
Operator --> UC_CommandControl
Operator --> UC_OperateLanes
Operator --> UC_Override
Operator --> UC_Logs
Operator --> UC_WorkDiary
Operator --> UC_Degraded

SystemAdministrator --> UC_LogOn
SystemAdministrator --> UC_Configure
SystemAdministrator --> UC_ManageUsers
SystemAdministrator --> UC_Logs

MaintenanceUser --> UC_LogOn
MaintenanceUser --> UC_ViewStatus
MaintenanceUser --> UC_Logs
MaintenanceUser --> UC_WorkDiary

RemoteUser --> UC_LogOn
RemoteUser --> UC_CommandControl
RemoteUser --> UC_Degraded

ExternalSystem --> UC_ExportStatus

FieldTechnician --> UC_Degraded

UC_LogOn ..> UC_Auth : <<include>>
UC_CommandControl ..> UC_Authorize : <<include>>
UC_OperateLanes ..> UC_Authorize : <<include>>
UC_OperateLanes ..> UC_Safety : <<include>>
UC_Override ..> UC_Authorize : <<include>>
UC_Override ..> UC_Safety : <<include>>
UC_Configure ..> UC_Authorize : <<include>>
UC_Configure ..> UC_StepUp : <<extend>>
UC_Logs ..> UC_Audit : <<include>>
UC_OperateLanes ..> UC_Audit : <<include>>
UC_CommandControl ..> UC_Audit : <<include>>
UC_Override ..> UC_Audit : <<include>>
UC_Configure ..> UC_Audit : <<include>>
UC_CommandControl ..> UC_Takeover : <<extend>>

note right of UC_CommandControl
assumption: NFR-020 means
only one Operator session holds
command-control lease; multiple
monitor-only sessions allowed.
end note

note right of UC_ExportStatus
assumption: External systems are
read-only via DMZ server, outbound-only
(one-way transfer); no inbound inputs.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassView
hide circle
skinparam classAttributeIconSize 0

class User {
  +userId: String
  +username: String
  -passwordHash: String
  +role: Role
  +securityLevel: int
  +isRemoteAllowed: boolean
  +isActive: boolean
  +authenticate(password: String): boolean
}

enum Role {
  Operator
  SystemAdministrator
  MaintenanceUser
  MonitorOnly
}

class Workstation {
  +workstationId: String
  +locationName: String
  +isAuthorizedForCommand: boolean
  +isRemoteDialIn: boolean
}

class Session {
  +sessionId: String
  +loginTime: DateTime
  +lastSeen: DateTime
  +mode: SessionMode
  +requestCommandControl(): void
  +releaseCommandControl(): void
}

enum SessionMode {
  MonitorOnly
  CommandControl
}

class CommandLease {
  +leaseId: String
  +holderUserId: String
  +holderWorkstationId: String
  +acquiredAt: DateTime
  +expiresAt: DateTime
  +takeoverBy(user: User): boolean
  +isHeld(): boolean
}

class Device {
  +deviceId: String
  +deviceType: String
  +location: String
  +direction: String
  +status: DeviceStatus
  +lastUpdate: DateTime
  +setDesiredState(desired: DeviceStatus): void
}

enum DeviceStatus {
  Open
  Closed
  Unknown
  Failed
  Overridden
}

class SensorStatus {
  +sensorId: String
  +deviceId: String
  +value: String
  +quality: String
  +timestamp: DateTime
}

class ControlCommand {
  +commandId: String
  +commandType: String
  +targetDeviceId: String
  +requestedBy: String
  +requestedAt: DateTime
  +confirmedAt: DateTime
  +status: CommandStatus
  +validate(): boolean
}

enum CommandStatus {
  Proposed
  Confirmed
  Aborted
  Sent
  Completed
  Halted
  Failed
}

class SafetyRuleSet <<persisted>> {
  +ruleSetId: String
  +version: String
  +effectiveAt: DateTime
  +evaluate(cmd: ControlCommand, snapshot: FacilityStatusSnapshot): SafetyDecision
}

class SafetyDecision {
  +isAllowed: boolean
  +reason: String
}

class Sequence {
  +sequenceId: String
  +name: String
  +mode: String
  +scheduleCron: String
  +state: SequenceState
  +start(): void
  +halt(reason: String): void
  +resume(): void
}

enum SequenceState {
  Idle
  PendingConfirmation
  Executing
  Halted
  Completed
}

class FacilityStatusSnapshot {
  +snapshotId: String
  +capturedAt: DateTime
  +isStale(maxAgeSeconds: int): boolean
}

class AuditLogEntry <<immutable>> {
  +entryId: String
  +timestamp: DateTime
  +userId: String
  +workstationId: String
  +action: String
  +details: String
  +hashChain: String
}

class ConfigChange {
  +changeId: String
  +changedBy: String
  +changedAt: DateTime
  +impactedUnits: String[*]
  +validateConflicts(): String[*]
}

class IntegrityReport <<immutable>> {
  +unitId: String
  +verifiedAt: DateTime
  +algorithm: String
  +result: String
  +digest: String
}

class ExternalExportFile <<immutable>> {
  +exportId: String
  +createdAt: DateTime
  +schemaVersion: String
  +buildPayload(snapshot: FacilityStatusSnapshot): String
}

Session "1" o-- "1" User
Session "1" o-- "1" Workstation
CommandLease "0..1" --> "1" Session : heldBy
ControlCommand "0..*" --> "1" Session : issuedBy
ControlCommand "0..*" --> "1" Device : target
Device "1" *-- "0..*" SensorStatus
SafetyRuleSet "1" --> "0..*" ControlCommand : validates >
SafetyRuleSet "1" --> "0..*" FacilityStatusSnapshot : uses >
Sequence "1" o-- "0..*" ControlCommand : steps
FacilityStatusSnapshot "1" o-- "0..*" Device : statuses
AuditLogEntry "0..*" --> "0..1" Session : actorContext
AuditLogEntry "0..*" --> "0..1" ControlCommand : commandRef
AuditLogEntry "0..*" --> "0..1" ConfigChange : configRef
IntegrityReport "0..*" --> "1" Workstation : unit
ExternalExportFile "0..*" --> "1" FacilityStatusSnapshot : source

note right of SafetyRuleSet
ASR-001/FR-041:
validated at each unit;
stored in non-volatile memory;
must abort on unsafe/unknown.
end note

note right of AuditLogEntry
FR-025/NFR-012:
tamper-proof storage, 365+ days retention;
no user edits; include failed/aborted commands.
end note

note right of CommandLease
ASR-008:
single active command-control;
workstation allow-list; takeover workflow logged.
end note

note right of ExternalExportFile
ASR-005:
outbound-only export every 30s to DMZ;
no inbound inputs from external systems.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectView
skinparam classAttributeIconSize 0

object op1 as "op1:User [CommandControl]" {
  userId = "U-1001"
  username = "j.smith"
  role = "Operator"
  securityLevel = 5
  isRemoteAllowed = false
}

object ws1 as "ws1:Workstation [CommandControl]" {
  workstationId = "TMC-WS-01"
  locationName = "TMC Main"
  isAuthorizedForCommand = true
  isRemoteDialIn = false
}

object sess1 as "sess1:Session [LogOn]" {
  sessionId = "S-7788"
  loginTime = "2026-04-22T06:01:10"
  mode = "CommandControl"
}

object lease1 as "lease1:CommandLease [AcquireLease]" {
  leaseId = "L-55"
  holderUserId = "U-1001"
  holderWorkstationId = "TMC-WS-01"
  expiresAt = "2026-04-22T06:11:10"
}

object seq1 as "seq1:Sequence [OpenLanes]" {
  sequenceId = "SEQ-OPEN-AM"
  name = "Morning Open"
  mode = "PeakAM"
  state = "Executing"
}

object gateN1 as "gateN1:Device [Gate]" {
  deviceId = "GATE-N-01"
  deviceType = "BarrierGate"
  direction = "NB"
  status = "Closed"
  lastUpdate = "2026-04-22T06:01:09"
}

object cmd1 as "cmd1:ControlCommand [ConfirmExecute]" {
  commandId = "CMD-9001"
  commandType = "OpenGate"
  targetDeviceId = "GATE-N-01"
  status = "Confirmed"
  confirmedAt = "2026-04-22T06:01:12"
}

object audit1 as "audit1:AuditLogEntry [Audit]" {
  entryId = "A-1"
  timestamp = "2026-04-22T06:01:12"
  userId = "U-1001"
  workstationId = "TMC-WS-01"
  action = "ConfirmSequenceStep"
  details = "SEQ-OPEN-AM CMD-9001"
}

sess1 -- op1
sess1 -- ws1
lease1 --> sess1
seq1 o-- cmd1
cmd1 --> gateN1
audit1 ..> cmd1

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateView
hide empty description

state "OperationalSequence\n(Sequence)" as Seq {
  [*] --> Idle

  Idle --> PendingConfirmation : scheduleDue / presentToOperator
  PendingConfirmation --> Executing : confirmExecute [hasCommandLease && authorized]
  PendingConfirmation --> Idle : cancel

  state Executing {
    [*] --> StepStart
    StepStart --> SafetyScreening : proposeCommand
    SafetyScreening --> CommandDispatch : [safetyAllowed && sensorsValid && noUnknownClosure]
    SafetyScreening --> Halted : [!safetyAllowed || !sensorsValid || unknownClosure] / logAbort

    CommandDispatch --> AwaitDeviceResponse : sendCommand / startTimeout(12s)
    AwaitDeviceResponse --> StepComplete : deviceAck
    AwaitDeviceResponse --> Halted : timeout / logHalt
    AwaitDeviceResponse --> Halted : unexpectedStateChange / logHalt

    StepComplete --> StepStart : nextStep [moreSteps]
    StepComplete --> Completed : [lastStep]
  }

  Executing --> Halted : haltCondition / alarmCritical
  Halted --> Executing : resume [withinCorrectionWindow] / reapplySafetyScreen
  Halted --> Idle : abortSequence

  Completed --> Idle : reset
}

note right of Seq
FR-039/FR-040/NFR-027:
halt on timeout/unsafe/unexpected changes;
resume only within configured window;
command response window 12s after operator confirmation.
end note

note left of Seq
ASR-001/FR-033/FR-034/FR-035:
multi-level integrity & safety gating;
abort if any closure status unknown;
execute only with valid sensor status.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityView
skinparam shadowing false

start
:Display live status\n(2s refresh) [Telemetry];
:Operator logs on [Auth];
:Request command control [Lease];
if (Workstation authorized?) then (yes)
  if (Lease held by other user?) then (yes)
    :Offer takeover if higher security [Takeover];
    if (Takeover accepted?) then (yes)
      :Acquire lease;
      :Notify prior holder;
    else (no)
      :Continue monitor-only;
      stop
    endif
  else (no)
    :Acquire lease;
  endif
else (no)
  :Deny command control;
  stop
endif

:Scan scheduled events\n(<=60s) [Scheduler];
:Present scheduled sequence\nfor confirmation [HITL];

if (Operator confirms?) then (yes)
  :Build FacilityStatusSnapshot;
  :Integrity checks (multi-level)\n[IntegrityCheck];
  :Safety screen command\nat TSU [SafetyCheck];

  if (Safety allowed?) then (yes)
    fork
      :Persist command proposal\n& audit log [Audit];
    fork again
      :Forward command TSU->FCU->DCU\n[Hierarchy];
    end fork

    :Validate safety at FCU and DCU\n[SafetyCheck];
    :Dispatch to I/O driver\n[HardwareIO];
    :Await device response\n(timeout 12s);
    if (Response OK?) then (yes)
      :Update DB + publish telemetry\n(<=2s) [Perf];
      :Continue next step or complete;
    else (no)
      :Halt sequence + raise alarm\n(<=2s) [Alarm];
      :Offer operator guidance\n[DecisionSupport];
    endif
  else (no)
    :Abort command + log reason;
  endif
else (no)
  :Cancel scheduled operation;
endif

stop

note right
NFR-006/007/011/028:
status & alarms visible within 2s;
controllers push status every 2s or less.
end note

note left
ASR-001/002:
multi-hop validation; superior-to-inferior forwarding only.
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_CommandControlAndOperate
skinparam sequenceMessageAlign center

actor Operator
participant "RLCS GUI" as GUI
participant "AuthService" as Auth
participant "LeaseManager" as Lease
participant "SequenceEngine" as SeqEng
participant "SafetyService" as Safety
database "RLCS DBMS" as DB
participant "TSU Controller" as TSU
participant "FCU Controller" as FCU
participant "DCU Controller" as DCU
participant "HardwareIO Adapter" as HW
participant "AuditLogService" as Audit

Operator -> GUI : LogOn
GUI -> Auth : authenticateUser
Auth -> DB : getUserAndPolicy
DB --> Auth : user+policy
Auth --> GUI : authOk

Operator -> GUI : RequestCommandControl
GUI -> Lease : acquireLease(workstationId,userId)
alt leaseHeldByOther
  Lease --> GUI : takeoverRequired
  GUI -> Operator : TakeoverPrompt
  Operator -> GUI : AcceptTakeover
  GUI -> Lease : takeoverLease
  Lease -> Audit : logTakeover
  Audit -> DB : appendAuditEntry
  DB --> Audit : stored
  Lease --> GUI : leaseGranted
else leaseFree
  Lease -> Audit : logLeaseAcquire
  Audit -> DB : appendAuditEntry
  DB --> Audit : stored
  Lease --> GUI : leaseGranted
end

GUI -> SeqEng : confirmSequenceExecute(sequenceId)
SeqEng -> DB : loadSequenceAndRules
DB --> SeqEng : sequence+rules
SeqEng -> DB : buildStatusSnapshot
DB --> SeqEng : snapshot

SeqEng -> Safety : safetyScreen(command,snapshot)
Safety --> SeqEng : allowed

SeqEng -> Audit : logCommandProposed
Audit -> DB : appendAuditEntry
DB --> Audit : stored

SeqEng -> TSU : forwardCommandTSU
TSU -> Safety : safetyScreenLocal
Safety --> TSU : allowed
TSU -> FCU : forwardCommandFCU
FCU -> Safety : safetyScreenLocal
Safety --> FCU : allowed
FCU -> DCU : forwardCommandDCU
DCU -> Safety : safetyScreenLocal
Safety --> DCU : allowed

DCU -> HW : dispatchToIO
note right of HW
NFR-027: device response within 12s
from operator confirmation (excluding network/device variance).
end note
HW --> DCU : deviceAck

DCU --> FCU : statusUpdate
FCU --> TSU : statusUpdate
TSU --> SeqEng : statusUpdate
SeqEng -> DB : persistStatus
DB --> SeqEng : ok
SeqEng --> GUI : publishTelemetry(<=2s)

@enduml
```

```plantuml
@startuml Sequence_OverrideAndResume
skinparam sequenceMessageAlign center

actor Operator
participant "RLCS GUI" as GUI
participant "AuthService" as Auth
participant "LeaseManager" as Lease
participant "SequenceEngine" as SeqEng
participant "SafetyService" as Safety
database "RLCS DBMS" as DB
participant "TSU Controller" as TSU
participant "FCU Controller" as FCU
participant "DCU Controller" as DCU
participant "AuditLogService" as Audit

Operator -> GUI : OverrideDeviceStatus(reason)
GUI -> Auth : authorizeAction(Override,deviceId)
Auth -> DB : getRoleAndPermissions
DB --> Auth : permissions
Auth --> GUI : authorized

GUI -> Lease : verifyLeaseHeld
Lease --> GUI : leaseOk

GUI -> SeqEng : applyOverride(deviceId,overriddenStatus)
SeqEng -> Audit : logOverride(reason,credential)
Audit -> DB : appendAuditEntry
DB --> Audit : stored

SeqEng -> DB : markDeviceOverridden
DB --> SeqEng : ok

SeqEng -> Safety : reapplySafetyScreen(sequenceId)
Safety -> DB : loadSnapshotAndRules
DB --> Safety : snapshot+rules
Safety --> SeqEng : decision

alt safetyDenied
  SeqEng -> Audit : logResumeDenied
  Audit -> DB : appendAuditEntry
  DB --> Audit : stored
  SeqEng --> GUI : denyResume(unsafe)
else safetyAllowed
  Operator -> GUI : ResumeSequence
  GUI -> SeqEng : resume
  SeqEng -> TSU : forwardResumeCommand
  TSU -> FCU : forwardResumeCommand
  FCU -> DCU : forwardResumeCommand
  DCU -> Safety : safetyScreenLocal
  Safety --> DCU : allowed
  DCU --> FCU : statusUpdate
  FCU --> TSU : statusUpdate
  TSU --> SeqEng : statusUpdate
  SeqEng -> DB : persistStatus
  DB --> SeqEng : ok
  SeqEng --> GUI : publishTelemetry(<=2s)
end

note right of SeqEng
FR-036/ASR-001:
override cannot bypass safety screening;
resume requires re-application of safety checks.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_CommandControlAndOperate
skinparam linetype ortho

actor Operator
rectangle "RLCS GUI" as GUI
rectangle "AuthService" as Auth
rectangle "LeaseManager" as Lease
rectangle "SequenceEngine" as SeqEng
rectangle "SafetyService" as Safety
database "RLCS DBMS" as DB
rectangle "AuditLogService" as Audit
rectangle "TSU Controller" as TSU
rectangle "FCU Controller" as FCU

Operator -- GUI
GUI -- Auth
GUI -- Lease
GUI -- SeqEng
SeqEng -- Safety
Auth -- DB
SeqEng -- DB
Audit -- DB
SeqEng -- Audit
SeqEng -- TSU
TSU -- FCU

GUI : 1. LogOn
GUI -> Auth : 2. authenticateUser
Auth -> DB : 3. getUserAndPolicy
GUI -> Lease : 4. acquireLease
Lease -> Audit : 5. logLeaseAcquire
Audit -> DB : 6. appendAuditEntry
GUI -> SeqEng : 7. confirmSequenceExecute
SeqEng -> DB : 8. loadSequenceAndRules
SeqEng -> Safety : 9. safetyScreen
SeqEng -> TSU : 10. forwardCommandTSU
TSU -> FCU : 11. forwardCommandFCU
SeqEng -> DB : 12. persistStatus
SeqEng -> GUI : 13. publishTelemetry

note right of GUI
Scenario: Operator acquires command control and confirms
a scheduled open/close sequence (FR-006, FR-038, FR-037),
with multi-layer safety screening (FR-041/ASR-001).
end note
@enduml
```

```plantuml
@startuml Collaboration_OverrideAndResume
skinparam linetype ortho

actor Operator
rectangle "RLCS GUI" as GUI
rectangle "AuthService" as Auth
rectangle "LeaseManager" as Lease
rectangle "SequenceEngine" as SeqEng
rectangle "SafetyService" as Safety
database "RLCS DBMS" as DB
rectangle "AuditLogService" as Audit
rectangle "TSU Controller" as TSU
rectangle "DCU Controller" as DCU

Operator -- GUI
GUI -- Auth
GUI -- Lease
GUI -- SeqEng
SeqEng -- Safety
SeqEng -- Audit
Audit -- DB
Auth -- DB
SeqEng -- DB
SeqEng -- TSU
TSU -- DCU

GUI : 1. OverrideDeviceStatus
GUI -> Auth : 2. authorizeAction
GUI -> Lease : 3. verifyLeaseHeld
GUI -> SeqEng : 4. applyOverride
SeqEng -> Audit : 5. logOverride
Audit -> DB : 6. appendAuditEntry
SeqEng -> Safety : 7. reapplySafetyScreen
GUI : 8. ResumeSequence
GUI -> SeqEng : 9. resume
SeqEng -> TSU : 10. forwardResumeCommand
TSU -> DCU : 11. forwardResumeCommand
DCU -> Safety : 12. safetyScreenLocal

note right of SeqEng
Scenario: Override a failed/unknown device status with reason
then attempt resume; safety screening must still pass
(FR-036, FR-040, ASR-001).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageView
skinparam packageStyle rectangle

package "ui" as UI {
  note bottom: GUI screens: status/map/alarms\ncommands/config/log export (FR-002)
}

package "application" as APP {
  note bottom: use-case orchestration\nsequence confirmation, workflows
}

package "domain" as DOMAIN {
  note bottom: core model: Sequence, Command,\nSafetyRuleSet, Device, Lease
}

package "infrastructure" as INFRA {
  note bottom: DB access, audit storage,\nmessage bus, scheduling
}

package "integrations" as INTEG {
  note bottom: controllers & I/O drivers,\nexternal export to DMZ (ASR-005/006)
}

package "security" as SEC {
  note bottom: authn/authz, password policy,\nTLS, workstation allow-list (ASR-008)
}

package "observability" as OBS {
  note bottom: alarms, metrics, integrity checks\n(ASR-007, NFR-011)
}

UI ..> APP
APP ..> DOMAIN
APP ..> SEC
APP ..> INFRA
APP ..> INTEG
INFRA ..> DOMAIN
INTEG ..> DOMAIN
SEC ..> DOMAIN
OBS ..> INFRA
OBS ..> DOMAIN
APP ..> OBS

note right of APP
ASR-003: bounded-latency pipelines;\nprefer event-driven push to UI.
end note

note right of INTEG
ASR-002: TSU>FCU>DCU forwarding only;\nHardwareIO Adapter boundary.
end note

note left of INFRA
FR-050/ASR-009:\nCOTS DBMS; isolate reporting workload.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentView
skinparam componentStyle rectangle

component "RLCS GUI" as C_GUI <<UI>> 
component "ApplicationService" as C_APP 
component "SequenceEngine" as C_SEQ 
component "SafetyService" as C_SAFE 
component "LeaseManager" as C_LEASE 
component "AuthService" as C_AUTH 
component "TelemetryBus" as C_BUS <<broker>> 
component "AuditLogService" as C_AUDIT 
component "ConfigService" as C_CONFIG 
component "IntegrityService" as C_INTEG 
component "ExternalExportService" as C_EXPORT 
component "ControllerGateway" as C_GATE 
component "HardwareIO Adapter" as C_HW 
database "RLCS DBMS" as C_DB <<COTS>>

interface "IAuth" as IAuth
interface "ILease" as ILease
interface "ISequence" as ISeq
interface "ISafety" as ISafety
interface "IAudit" as IAudit
interface "IConfig" as IConfig
interface "IIntegrity" as IIntegrity
interface "IExport" as IExport
interface "IControllerLink" as ICtrl
interface "IHardwareIO" as IHW

C_AUTH - IAuth
C_LEASE - ILease
C_SEQ - ISeq
C_SAFE - ISafety
C_AUDIT - IAudit
C_CONFIG - IConfig
C_INTEG - IIntegrity
C_EXPORT - IExport
C_GATE - ICtrl
C_HW - IHW

C_GUI ..> IAuth
C_GUI ..> ILease
C_GUI ..> ISeq
C_GUI ..> IConfig
C_GUI ..> IAudit

C_APP ..> IAuth
C_APP ..> ILease
C_APP ..> ISeq
C_APP ..> IConfig
C_APP ..> IIntegrity
C_APP ..> IExport
C_APP ..> IAudit

C_SEQ ..> ISafety
C_SEQ ..> IAudit
C_SEQ ..> ICtrl
C_SEQ ..> C_BUS

C_GATE ..> IHW

C_AUTH ..> C_DB
C_LEASE ..> C_DB
C_SEQ ..> C_DB
C_CONFIG ..> C_DB
C_AUDIT ..> C_DB
C_EXPORT ..> C_DB
C_INTEG ..> C_DB

note right of C_BUS
ASR-003: publish device/alarm updates\nso GUI reflects changes <=2s.
end note

note right of C_EXPORT
ASR-005/FR-030: outbound-only to DMZ\n(every 30s) + one-way serial link.
end note

note left of C_SAFE
ASR-001/FR-041: safety screening\nat each hop and executing controller.
end note

note bottom of C_HW
ASR-006/FR-055: implement RLCS Device Control API v1.x\n(pluggable drivers/controllers).
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentView
skinparam linetype ortho
skinparam componentStyle rectangle

node "TMC Private LAN\n(VLAN Segmented)" as N_LAN {
  node "Operator Workstation\n(TMC-WS-01..n)" as N_WS {
    artifact "RLCS GUI" as A_GUI
  }

  node "App Server A" as N_APP_A {
    artifact "ApplicationService" as A_APP_A
    artifact "SequenceEngine" as A_SEQ_A
    artifact "SafetyService" as A_SAFE_A
    artifact "LeaseManager" as A_LEASE_A
    artifact "AuthService" as A_AUTH_A
    artifact "AuditLogService" as A_AUDIT_A
    artifact "ConfigService" as A_CONFIG_A
    artifact "IntegrityService" as A_INTEG_A
    artifact "ExternalExportService" as A_EXP_A
    artifact "TelemetryBus" as A_BUS_A
  }

  node "App Server B (Hot Standby)" as N_APP_B {
    artifact "ApplicationService" as A_APP_B
    artifact "SequenceEngine" as A_SEQ_B
    artifact "SafetyService" as A_SAFE_B
    artifact "LeaseManager" as A_LEASE_B
    artifact "AuthService" as A_AUTH_B
    artifact "AuditLogService" as A_AUDIT_B
    artifact "TelemetryBus" as A_BUS_B
  }

  database "RLCS DBMS Cluster\n(COTS)" as N_DB {
    artifact "RLCS DBMS" as A_DB
  }
}

node "Field Network\n(Fiber primary / ISDN secondary)" as N_FIELD {
  node "TSU Controller" as N_TSU {
    artifact "ControllerGateway" as A_TSU_GATE
    artifact "SafetyRuleSet (NV)" as A_TSU_RULES
  }
  node "FCU North Controller" as N_FCU_N {
    artifact "ControllerGateway" as A_FCU_GATE_N
    artifact "SafetyRuleSet (NV)" as A_FCU_RULES_N
    artifact "HardwareIO Adapter" as A_HW_N
  }
  node "FCU South Controller" as N_FCU_S {
    artifact "ControllerGateway" as A_FCU_GATE_S
    artifact "SafetyRuleSet (NV)" as A_FCU_RULES_S
    artifact "HardwareIO Adapter" as A_HW_S
  }
  node "DCU Controllers (1..*)" as N_DCU {
    artifact "ControllerGateway" as A_DCU_GATE
    artifact "SafetyRuleSet (NV)" as A_DCU_RULES
    artifact "HardwareIO Adapter" as A_HW_D
  }
}

node "Firewall / DMZ" as N_DMZ {
  node "External Status Server (DMZ)" as N_EXTSRV {
    artifact "External Status Datastore" as A_EXTDATA
  }
}

cloud "External Systems" as N_EXTSYS

N_WS -- N_LAN
N_WS --> N_APP_A : TCP/IP (TLS)
N_WS --> N_APP_B : TCP/IP (TLS)
N_APP_A --> N_DB : SQL
N_APP_B --> N_DB : SQL

N_APP_A --> N_TSU : TCP/IP (checksum)
N_TSU --> N_FCU_N : TCP/IP (checksum)
N_TSU --> N_FCU_S : TCP/IP (checksum)
N_FCU_N --> N_DCU : copper/fiber (no wireless)
N_FCU_S --> N_DCU : copper/fiber (no wireless)

N_APP_A --> N_DMZ : outbound-only
N_DMZ --> N_EXTSRV : one-way file drop (30s)
N_EXTSYS --> N_EXTSRV : read-only

note right of N_APP_A
NFR-001/002/032:\nredundant app tier; RTO<=10min;\ncontinue ops under single failure.
end note

note right of N_FIELD
NFR-028: controllers send status every 2s or less.\nNFR-019: transparent comms failover.
end note

note right of N_DMZ
ASR-005: RLCS accepts no inbound inputs\nfrom external systems.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerView
skinparam componentStyle rectangle
skinparam linetype ortho

rectangle "TMC Workstation" as CT_WS {
  rectangle "RLCS GUI" as CT_GUI
}

rectangle "RLCS Control Plane (Private LAN)" as CT_CP {
  rectangle "ApplicationService" as CT_APP
  rectangle "SequenceEngine" as CT_SEQ
  rectangle "SafetyService" as CT_SAFE
  rectangle "LeaseManager" as CT_LEASE
  rectangle "AuthService" as CT_AUTH
  rectangle "AuditLogService" as CT_AUDIT
  rectangle "TelemetryBus" as CT_BUS
  rectangle "ConfigService" as CT_CONFIG
  rectangle "IntegrityService" as CT_INTEG
  database "RLCS DBMS (COTS)" as CT_DB
}

rectangle "Field Control Tier" as CT_FIELD {
  rectangle "TSU Controller" as CT_TSU
  rectangle "FCU Controller" as CT_FCU
  rectangle "DCU Controller" as CT_DCU
  rectangle "HardwareIO Adapter" as CT_HW
}

rectangle "DMZ" as CT_DMZ {
  rectangle "ExternalExportService" as CT_EXPORT
  database "External Status Datastore" as CT_EXTDB
}

cloud "External Systems" as CT_EXT

CT_GUI --> CT_AUTH : LogOn (TLS)
CT_GUI --> CT_LEASE : AcquireLease (TLS)
CT_GUI --> CT_SEQ : ConfirmSequence (TLS)
CT_GUI <-- CT_BUS : TelemetryPush (<=2s)

CT_APP --> CT_AUTH : RBAC
CT_APP --> CT_CONFIG : Config
CT_APP --> CT_INTEG : VerifyIntegrity
CT_APP --> CT_AUDIT : AuditWrite
CT_APP --> CT_DB : SQL

CT_SEQ --> CT_SAFE : SafetyScreen
CT_SEQ --> CT_AUDIT : AuditCommand
CT_SEQ --> CT_DB : Snapshot/Status
CT_SEQ --> CT_TSU : ForwardCommand (checksum)
CT_BUS --> CT_GUI : Status/Alarms

CT_TSU --> CT_FCU : SuperiorToInferior
CT_FCU --> CT_DCU : SuperiorToInferior
CT_DCU --> CT_HW : DriverAPI v1.x

CT_EXPORT --> CT_DB : ReadSnapshot
CT_EXPORT --> CT_EXTDB : OneWayDrop (30s)
CT_EXT --> CT_EXTDB : ReadOnly

note right of CT_SAFE
ASR-001: multi-layer interlocks;\nabort on unknown/opposite open.\nValidated at each tier.
end note

note right of CT_AUDIT
FR-025/NFR-012:\nimmutable audit logs, 365+ day retention.
end note

note right of CT_EXPORT
ASR-005:\noutbound-only export; no inbound commands.
end note

note left of CT_BUS
ASR-003:\nevent-driven updates to meet 2s UI/alarms latency.
end note
@enduml
```