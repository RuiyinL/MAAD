## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCaseDiagram
left to right direction
skinparam packageStyle rectangle

actor "ObservingAstronomer" as ObservingAstronomer
actor "TelescopeOperator" as TelescopeOperator
actor "OperationsStaff" as OperationsStaff
actor "RemoteUser" as RemoteUser
actor "PolicyAdmin" as PolicyAdmin
actor "InstrumentEngineer" as InstrumentEngineer

actor "GeminiArchive" as GeminiArchive <<external>>
actor "StarCatalogService" as StarCatalogService <<external>>
actor "WeatherStation" as WeatherStation <<external>>
actor "TimeReferenceSystem" as TimeReferenceSystem <<external>>

rectangle "Gemini Observing Control System (OCS)" as OCS {
  usecase "Authenticate\n[Authenticate]" as UC_Authenticate
  usecase "Select Level/Mode\n[SelectMode]" as UC_SelectMode
  usecase "Run Observing Queue\n[RunQueue]" as UC_RunQueue
  usecase "Direct Control\n[DirectControl]" as UC_DirectControl
  usecase "Monitor Status\n[MonitorStatus]" as UC_MonitorStatus
  usecase "Allocate Resources\n[AllocateResource]" as UC_AllocateResource
  usecase "Run Simulation\n[RunSimulation]" as UC_RunSimulation
  usecase "Manage Remote Policy\n[ManageRemotePolicy]" as UC_ManageRemotePolicy
  usecase "Archive & Retrieve Data\n[ArchiveData]" as UC_ArchiveData
  usecase "Run Self Tests\n[SelfTest]" as UC_SelfTest
}

ObservingAstronomer --> UC_Authenticate
ObservingAstronomer --> UC_RunQueue
ObservingAstronomer --> UC_MonitorStatus
ObservingAstronomer --> UC_ArchiveData

TelescopeOperator --> UC_Authenticate
TelescopeOperator --> UC_SelectMode
TelescopeOperator --> UC_RunQueue
TelescopeOperator --> UC_DirectControl
TelescopeOperator --> UC_MonitorStatus
TelescopeOperator --> UC_AllocateResource

OperationsStaff --> UC_Authenticate
OperationsStaff --> UC_SelectMode
OperationsStaff --> UC_DirectControl
OperationsStaff --> UC_SelfTest
OperationsStaff --> UC_RunSimulation
OperationsStaff --> UC_AllocateResource

InstrumentEngineer --> UC_Authenticate
InstrumentEngineer --> UC_RunSimulation
InstrumentEngineer --> UC_SelfTest
InstrumentEngineer --> UC_MonitorStatus

RemoteUser --> UC_Authenticate
RemoteUser --> UC_MonitorStatus
RemoteUser --> UC_RunQueue

PolicyAdmin --> UC_Authenticate
PolicyAdmin --> UC_ManageRemotePolicy

GeminiArchive <-- UC_ArchiveData
StarCatalogService <-- UC_RunQueue
WeatherStation <-- UC_RunQueue
TimeReferenceSystem <-- UC_RunQueue

UC_SelectMode ..> UC_Authenticate : <<include>>
UC_RunQueue ..> UC_Authenticate : <<include>>
UC_DirectControl ..> UC_Authenticate : <<include>>
UC_MonitorStatus ..> UC_Authenticate : <<include>>
UC_AllocateResource ..> UC_Authenticate : <<include>>
UC_RunSimulation ..> UC_Authenticate : <<include>>
UC_ManageRemotePolicy ..> UC_Authenticate : <<include>>
UC_ArchiveData ..> UC_Authenticate : <<include>>
UC_SelfTest ..> UC_Authenticate : <<include>>

UC_DirectControl ..> UC_AllocateResource : <<include>>
UC_RunQueue ..> UC_AllocateResource : <<include>>

UC_DirectControl ..> UC_SelectMode : <<extend>>
UC_RunSimulation ..> UC_SelectMode : <<extend>>

note right of UC_DirectControl
FR-004/ASR-002: Observing mode via Sequencer only (no direct control)
FR-013: Ops may enable interactive direct control (exception)
end note

note right of UC_MonitorStatus
FR-005/NFR-003/ASR-003: Read-only, non-intrusive monitoring
end note

note bottom of UC_ManageRemotePolicy
FR-018/ASR-006: Dynamic site restrictions, effect within 60s
end note

note bottom
assumption: "RemoteUser" represents remote astronomers/operators using remote UI; remote direct control is additionally constrained by safety prerequisites (FR-021).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml ClassDiagram
skinparam classAttributeIconSize 0

enum OperationalLevel {
  OBSERVING
  MAINTENANCE
  TEST
}

enum AccessMode {
  OBSERVING
  MONITORING
  OPERATION
  PLANNING
  TESTING
  ADMINISTRATIVE
}

enum CommandResultCode {
  ACK
  NAK
  TIMEOUT
}

class User {
  +userId: String
  +username: String
  +roles: List<String>
}

class Session {
  +sessionToken: String
  +remoteSiteId: String
  +activeModes: Set<AccessMode>
  +createdAtUtc: String
  +addMode(mode: AccessMode)
  +removeMode(mode: AccessMode)
}

class RBACPolicy {
  +policyVersion: String
  +isAllowed(role: String, level: OperationalLevel, mode: AccessMode, operation: String): boolean
}

class OperationalState {
  +currentLevel: OperationalLevel
  +setLevel(level: OperationalLevel)
  +getLevel(): OperationalLevel
}

class RemoteSitePolicy {
  +policyVersion: String
  +allowedSites: Set<String>
  +isSiteAllowed(siteId: String, operation: String): boolean
  +updateAllowedSites(sites: Set<String>)
}

class Resource {
  +resourceId: String
  +resourceType: String
}

class ResourceLease {
  +leaseId: String
  +ownerSessionToken: String
  +resourceId: String
  +expiresAtUtc: String
}

class AccessModeAllocator {
  +requestLease(session: Session, resources: List<Resource>, mode: AccessMode): ResourceLease
  +releaseLease(leaseId: String)
  +detectAndResolveDeadlock()
}

class Command {
  +commandId: String
  +cmd: String
  +argsJson: String
  +isIdempotent: boolean
  +requiresSafetyInterlock: boolean
}

class CommandEnvelope {
  +correlationId: String
  +timestampUtc: String
  +sessionToken: String
  +accessMode: AccessMode
  +operationalLevel: OperationalLevel
  +command: Command
}

class CommandResponse {
  +correlationId: String
  +resultCode: CommandResultCode
  +reason: String
  +acceptedAtUtc: String
}

class CommandRouter {
  +validateAndRoute(env: CommandEnvelope): CommandResponse
}

class Sequencer {
  +runQueue(queueId: String)
  +submitStep(env: CommandEnvelope): CommandResponse
  +breakAndResequence(queueId: String)
}

class Scheduler {
  +buildQueue(): String
  +resortQueue(queueId: String)
  +applyRules()
}

class ControlGateway {
  +sendToIoc(env: CommandEnvelope): CommandResponse
  +queryStatus(variable: String): ControlVariable
}

class ControlVariable {
  +timestampUtc: String
  +variable: String
  +value: String
  +unit: String
  +statusCode: int
  +errorMessage: String
}
note right of ControlVariable
FR-051: Must not block/lock control even when faulty.
NFR-004: status requests <= 5s; local updates <= 4s.
end note

class Subsystem {
  +subsystemId: String
  +name: String
  +mode: String
  +getVersion(): String
  +selfTest(level: String): String
}

class SimulatorAdapter {
  +simulate(env: CommandEnvelope): CommandResponse
}

class DataProduct {
  +datasetId: String
  +fitsPath: String
  +compression: String <<immutable>>
  +headersJson: String
}

class ArchiveClient {
  +archive(dataset: DataProduct)
  +query(criteria: String): List<DataProduct>
}

class AuditLogEntry <<persisted>> {
  +timestampUtc: String
  +userId: String
  +subsystem: String
  +action: String
  +resultCode: String
}

class EventLogEntry <<persisted>> {
  +eventTimeUtc: String
  +origin: String
  +severity: String
  +errorCode: String
  +correlationId: String
  +userAction: String
}

User "1" -- "0..*" Session
Session "1" o-- "1" OperationalState
Session "1" ..> RBACPolicy : uses
Session "1" ..> RemoteSitePolicy : uses

Sequencer "1" -- "1" Scheduler
Sequencer "1" ..> CommandRouter : uses
CommandRouter "1" ..> RBACPolicy : authorize
CommandRouter "1" ..> RemoteSitePolicy : siteGate
CommandRouter "1" ..> AccessModeAllocator : allocate
CommandRouter "1" ..> ControlGateway : route
ControlGateway "1" ..> Subsystem : controls
ControlGateway "1" ..> SimulatorAdapter : simulate

AccessModeAllocator "1" o-- "0..*" ResourceLease
ResourceLease "*" --> "1" Resource

CommandEnvelope "1" o-- "1" Command
CommandRouter ..> AuditLogEntry : writes
CommandRouter ..> EventLogEntry : writes

ArchiveClient ..> DataProduct : transfers
Sequencer ..> ArchiveClient : triggers archive

note top of CommandRouter
ASR-002: Sequencer/scheduler primary control path.
NFR-001: accept/reject <=2s; timeouts ~500ms; handshake 100-200ms.
NFR-008: TLS + audit on every access/admin action.
end note

note top of AccessModeAllocator
ASR-005/FR-027: critical resources solely through allocation; no deadlock.
ASR-012: active instrument isolation + beam exclusivity.
end note

note bottom of DataProduct
FR-034/35/37/38 + NFR-006: lossless compression; FITS with full headers.
ASR-009 + NFR-007: storage tiers + retention (7d, last 3d interactive).
end note
@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml ObjectDiagram
skinparam classAttributeIconSize 0

object "opUser:User [RunQueue]" as opUser {
  userId = "u-102"
  username = "operator1"
  roles = "[TelescopeOperator]"
}

object "sess1:Session [RunQueue]" as sess1 {
  sessionToken = "st-8f3a"
  remoteSiteId = "SITE-LOCAL"
  activeModes = "{OBSERVING, MONITORING}"
  createdAtUtc = "2026-04-22T19:12:00Z"
}

object "opState:OperationalState [SelectMode]" as opState {
  currentLevel = "OBSERVING"
}

object "rbac:RBACPolicy [Authenticate]" as rbac {
  policyVersion = "2026.04"
}

object "sitePolicy:RemoteSitePolicy [ManageRemotePolicy]" as sitePolicy {
  policyVersion = "2026.04"
  allowedSites = "{SITE-LOCAL, SITE-BASE}"
}

object "alloc:AccessModeAllocator [AllocateResource]" as alloc

object "beam:Resource [AllocateResource]" as beam {
  resourceId = "RES-BEAM-1"
  resourceType = "TelescopeBeam"
}

object "lease1:ResourceLease [AllocateResource]" as lease1 {
  leaseId = "L-5512"
  ownerSessionToken = "st-8f3a"
  resourceId = "RES-BEAM-1"
  expiresAtUtc = "2026-04-22T19:22:00Z"
}

object "cmd1:Command [RunQueue]" as cmd1 {
  commandId = "C-9001"
  cmd = "CMD_SLEW"
  argsJson = "{target:'M42'}"
  isIdempotent = "false"
  requiresSafetyInterlock = "true"
}

object "env1:CommandEnvelope [RunQueue]" as env1 {
  correlationId = "corr-7aa1"
  timestampUtc = "2026-04-22T19:12:05Z"
  sessionToken = "st-8f3a"
  accessMode = "OBSERVING"
  operationalLevel = "OBSERVING"
}

opUser -- sess1
sess1 o-- opState
sess1 ..> rbac
sess1 ..> sitePolicy

alloc o-- lease1
lease1 --> beam

env1 o-- cmd1

note bottom of env1
scenario: Operator runs queue step; resource lease required; command is safety-sensitive (no auto-retry).
end note
@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml StateDiagram
hide empty description

state "OCS Control Session" as OCSSession

[*] --> Unauthenticated

Unauthenticated --> Authenticated : Authenticate [Authenticate]\n/ issueSessionToken
Authenticated --> Unauthenticated : Logout

state Authenticated {
  [*] --> ModeNegotiation

  ModeNegotiation --> Active : SelectMode [SelectMode]\n[allowedCombos]\n/ setActiveModes
  ModeNegotiation --> Denied : SelectMode [conflict]\n/ returnExplicitError
  Denied --> ModeNegotiation : RetryMode

  state Active {
    [*] --> Ready

    Ready --> Observing : EnterObserving [mode==OBSERVING]\n/ bindSequencerOnly
    Ready --> Monitoring : EnterMonitoring [mode==MONITORING]\n/ readOnly
    Ready --> Operation : EnterOperation [mode==OPERATION]\n/ allowDirectControl
    Ready --> Planning : EnterPlanning [mode==PLANNING]\n/ useSimulatorOnly
    Ready --> Testing : EnterTesting [mode==TESTING]\n/ sandboxedResources
    Ready --> Administrative : EnterAdmin [mode==ADMINISTRATIVE]\n/ inquiryOnly

    Observing --> Ready : LeaveMode
    Monitoring --> Ready : LeaveMode
    Operation --> Ready : LeaveMode
    Planning --> Ready : LeaveMode
    Testing --> Ready : LeaveMode
    Administrative --> Ready : LeaveMode

    state "Command Path" as CommandPath {
      [*] --> Idle
      Idle --> Authorize : SubmitCommand [any]\n/ rbacCheck+siteGate
      Authorize --> Allocate : [needsCriticalResource]\n/ requestLease
      Authorize --> Route : [noCriticalResource]
      Allocate --> Route : [leaseGranted]
      Allocate --> Rejected : [deadlockOrDenied]\n/ NAK
      Route --> Acked : SendToIOC [ACK<=2s]\n/ writeAuditLog
      Route --> Failed : SendToIOC [NAK|Timeout]\n/ writeEventLog
      Acked --> Idle
      Failed --> Idle
      Rejected --> Idle
    }

    Ready --> CommandPath
  }
}

Authenticated --> LockedOut : ExcessiveFailedAttempts\n/ auditLog
LockedOut --> Unauthenticated : LockoutExpired

note right of Planning
FR-007/ASR-008: no real telescope access; simulator and virtual telescope only.
end note

note right of Observing
FR-004/ASR-002: observing mode via sequencer only; no direct telescope/instrument control.
end note

note bottom of CommandPath
NFR-001: accept/reject <=2s; timeouts ~500ms.\nASR-005: allocation must avoid deadlock.\nNFR-008: audit on access/admin actions.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml ActivityDiagram
skinparam activityStyle rounded

start
:Open UI (local or remote);
:Authenticate [SecurityCheck];
note right
FR-039/NFR-008: roles returned; all attempts audited; TLS required.
end note

:Select operational level & access mode(s) [SelectMode];
if (Mode combination permitted?) then (yes)
  :Establish session mode state;
else (no)
  :Return explicit conflict error;
  stop
endif

:Load observing queue [RunQueue];
:Fetch site conditions + rules;
fork
  :Get weather conditions;
  note right
  FR-050: centralized meteorological info.
  end note
fork again
  :Query star catalogs;
  note right
  FR-048: guide/standard star selection support.
  end note
end fork

:Resort queue if needed [Resequence];
note right
FR-014/FR-017: break & resequence based on QA/conditions.
end note

repeat
  :Select next observing sequence;
  :Request resource allocation (beam, telescope, instrument) [AllocateResource];
  note right
  FR-027/ASR-005: allocator sole authority; deadlock avoidance.
  end note

  if (Allocated?) then (yes)
    :Sequencer submits command step(s) [SubmitStep];
    note right
    NFR-001: accept/reject <=2s; IOC handshake 100-200ms; timeouts ~500ms.
    end note

    fork
      :Update status displays [MonitorStatus];
      note right
      NFR-004: local <=4s updates; queries <=5s.
      end note
    fork again
      :Write audit/event logs;
      note right
      NFR-013/NFR-014: timestamp+CorrelationID; traceability.
      end note
    fork again
      :Quick-look processing (sync) [QuickLook];
      note right
      FR-045: synchronous with acquisition; must not require manual intervention.
      end note
    end fork

    :Store data (lossless, standard format) [StoreData];
    :Archive to GeminiArchive [ArchiveData];
    note right
    FR-036/ASR-009: automatic archiving; NFR-007 retention.
    end note

    :Release resource lease;
  else (no)
    :Record NAK + reason;
  endif
repeat while (Queue not empty?) is (yes)

stop
@enduml
```

6. Sequence — Process View: Sequence Diagram

```plantuml
@startuml SequenceScenario1_RunQueueAndControl
autonumber
actor TelescopeOperator as TelescopeOperator
participant "RemoteUI" as RemoteUI
participant "AuthService" as AuthService
participant "PolicyService" as PolicyService
participant "Sequencer" as Sequencer
participant "Scheduler" as Scheduler
participant "CommandRouter" as CommandRouter
participant "AccessModeAllocator" as AccessModeAllocator
participant "ControlGateway" as ControlGateway
database "ParameterDB" as ParameterDB
participant "TelescopeIOC" as TelescopeIOC
participant "InstrumentIOC" as InstrumentIOC
participant "AuditLogService" as AuditLogService
participant "EventLogService" as EventLogService

TelescopeOperator -> RemoteUI : Authenticate
RemoteUI -> AuthService : authenticate(username,password,mfa_token)
AuthService --> RemoteUI : sessionToken,roles

RemoteUI -> PolicyService : selectMode(sessionToken, level=OBSERVING, modes={OBSERVING,MONITORING})
PolicyService --> RemoteUI : modeAccepted

RemoteUI -> Sequencer : runQueue(queueId)
Sequencer -> Scheduler : buildOrLoadQueue
Scheduler -> ParameterDB : readSiteRules
ParameterDB --> Scheduler : rules
Scheduler --> Sequencer : queueReady

loop for each step
  Sequencer -> CommandRouter : submitStep(CommandEnvelope)
  note right of CommandRouter
  NFR-001: accept/reject <= 2s before action.
  end note

  CommandRouter -> PolicyService : authorize(sessionToken, level, mode, cmd)
  PolicyService --> CommandRouter : allow/deny

  alt needs critical resources
    CommandRouter -> AccessModeAllocator : requestLease(resources={beam,telescope,instrument})
    AccessModeAllocator --> CommandRouter : leaseGranted/NAK
  end alt

  CommandRouter -> ControlGateway : sendToIoc(envelope)
  ControlGateway -> TelescopeIOC : cmd(ACK/NAK)
  TelescopeIOC --> ControlGateway : ACK/NAK (100-200ms handshake)
  ControlGateway -> InstrumentIOC : cmd(ACK/NAK)
  InstrumentIOC --> ControlGateway : ACK/NAK

  alt ACK
    ControlGateway --> CommandRouter : ACK
    CommandRouter -> AuditLogService : writeAudit(action, result=ACK, correlationId)
    AuditLogService --> CommandRouter : ok
    CommandRouter --> Sequencer : CommandResponse(ACK)
  else NAK/Timeout
    ControlGateway --> CommandRouter : NAK/TIMEOUT
    CommandRouter -> EventLogService : writeEvent(severity, errorCode, correlationId)
    EventLogService --> CommandRouter : ok
    CommandRouter --> Sequencer : CommandResponse(NAK/TIMEOUT)
  end alt
end

note bottom
FR-004/ASR-002: Operator uses Sequencer path in Observing mode.\nFR-064: retries only for retryable idempotent commands (not shown for CMD_SLEW).
end note
@enduml
```

```plantuml
@startuml SequenceScenario2_RemotePolicyUpdate
autonumber
actor PolicyAdmin as PolicyAdmin
participant "RemoteUI" as RemoteUI
participant "AuthService" as AuthService
participant "PolicyService" as PolicyService
database "PolicyDB" as PolicyDB
participant "AuditLogService" as AuditLogService
participant "CommandRouter" as CommandRouter

PolicyAdmin -> RemoteUI : Authenticate
RemoteUI -> AuthService : authenticate(username,password,mfa_token)
AuthService --> RemoteUI : sessionToken,roles=[PolicyAdmin]

PolicyAdmin -> RemoteUI : UpdateAllowedSites
RemoteUI -> PolicyService : updateRemoteSites(sessionToken, allowedSites)
PolicyService -> PolicyDB : persistPolicyChange
PolicyDB --> PolicyService : ok

PolicyService -> AuditLogService : writeAudit(action="UpdateRemoteSites", result="OK")
AuditLogService --> PolicyService : ok
PolicyService --> RemoteUI : policyUpdated

note right of PolicyService
FR-018/ASR-006: policy changes effective within 60s.
NFR-008: audit every admin action.
end note

... within 60s ...

actor RemoteUser as RemoteUser
RemoteUser -> RemoteUI : SubmitCommand
RemoteUI -> CommandRouter : submit(CommandEnvelope)
CommandRouter -> PolicyService : siteGate(remoteSiteId, operation)
PolicyService --> CommandRouter : allow/deny
CommandRouter --> RemoteUI : explicitErrorIfDenied
@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml CollaborationScenario1_RunQueueAndControl
skinparam linetype ortho
actor TelescopeOperator
participant RemoteUI
participant AuthService
participant PolicyService
participant Sequencer
participant CommandRouter
participant AccessModeAllocator
participant ControlGateway
participant TelescopeIOC
participant AuditLogService

TelescopeOperator -> RemoteUI
RemoteUI -> AuthService
RemoteUI -> PolicyService
RemoteUI -> Sequencer
Sequencer -> CommandRouter
CommandRouter -> PolicyService
CommandRouter -> AccessModeAllocator
CommandRouter -> ControlGateway
ControlGateway -> TelescopeIOC
CommandRouter -> AuditLogService

RemoteUI -> AuthService : 1 authenticate()
AuthService -> RemoteUI : 2 issueSessionToken()
RemoteUI -> PolicyService : 3 selectMode()
PolicyService -> RemoteUI : 4 modeAccepted()
RemoteUI -> Sequencer : 5 runQueue()
Sequencer -> CommandRouter : 6 submitStep()
CommandRouter -> PolicyService : 7 authorize()
PolicyService -> CommandRouter : 8 allow()
CommandRouter -> AccessModeAllocator : 9 requestLease()
AccessModeAllocator -> CommandRouter : 10 leaseGranted()
CommandRouter -> ControlGateway : 11 sendToIoc()
ControlGateway -> TelescopeIOC : 12 cmd()
TelescopeIOC -> CommandRouter : 13 ACK()
CommandRouter -> AuditLogService : 14 writeAudit()

note bottom
scenario: "Run observing queue and execute control commands via sequencer (no direct control in observing mode)" (FR-004, FR-012, ASR-002, ASR-005).
end note
@enduml
```

```plantuml
@startuml CollaborationScenario2_RemotePolicyUpdate
skinparam linetype ortho
actor PolicyAdmin as PolicyAdmin
actor RemoteUser as RemoteUser
rectangle RemoteUI as RemoteUI
rectangle AuthService as AuthService
rectangle PolicyService as PolicyService
database PolicyDB as PolicyDB
rectangle AuditLogService as AuditLogService
rectangle CommandRouter as CommandRouter

PolicyAdmin -- RemoteUI
RemoteUI -- AuthService
RemoteUI -- PolicyService
PolicyService -- PolicyDB
PolicyService -- AuditLogService
RemoteUser -- RemoteUI
RemoteUI -- CommandRouter
CommandRouter -- PolicyService

RemoteUI : 1 authenticate()
AuthService : 2 issueSessionToken()
RemoteUI : 3 updateRemoteSites()
PolicyService : 4 persistPolicyChange()
PolicyDB : 5 ok
PolicyService : 6 writeAudit()
AuditLogService : 7 ok
RemoteUI : 8 policyUpdated()

RemoteUI : 9 submitCommand()
CommandRouter : 10 siteGate()
PolicyService : 11 allow/deny()
CommandRouter : 12 explicitErrorIfDenied()

note bottom
scenario: "Policy admin updates allowed remote sites; policy enforced within 60s" (FR-018, ASR-006, NFR-008).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml PackageDiagram
skinparam packageStyle rectangle

package "ui" as ui {
  artifact RemoteUI
  note bottom of ui
  Responsibility: local/remote UI; mode-aware UX.
  NFR-010: uniform UI + role-dependent look-and-feel.
  end note
}

package "api" as api {
  artifact AuthAPI
  artifact CommandAPI
  artifact PolicyAPI
  artifact StatusAPI
  artifact ArchiveAPI
}

package "domain" as domain {
  artifact Session
  artifact OperationalState
  artifact CommandEnvelope
  artifact ResourceLease
  artifact DataProduct
}

package "security" as security {
  artifact AuthService
  artifact PolicyService
  artifact RBACPolicy
  artifact RemoteSitePolicy
  note bottom of security
  ASR-001/NFR-008: centralized authz; TLS; audit on every access/admin action.
  end note
}

package "orchestration" as orchestration {
  artifact Sequencer
  artifact Scheduler
  note bottom of orchestration
  ASR-002: sequencer/scheduler primary control path.
  end note
}

package "control" as control {
  artifact CommandRouter
  artifact ControlGateway
  artifact AccessModeAllocator
  artifact SimulatorAdapter
  note bottom of control
  ASR-004: common command+ACK/NAK; NFR-001 timings.
  ASR-005: allocation sole authority; deadlock avoidance.
  ASR-008: simulation adapters.
  end note
}

package "data" as data {
  artifact ParameterDB
  artifact ArchiveClient
  artifact QuickLookProcessor
  artifact NearLineProcessor
  note bottom of data
  ASR-009: storage tiers + archive + FITS; NFR-007 retention.
  FR-046: near-line async, acquisition precedence.
  end note
}

package "observability" as observability {
  artifact AuditLogService
  artifact EventLogService
  artifact MetricsService
  note bottom of observability
  ASR-011: traceability + 200Hz engineering logs (burst).
  NFR-003: non-interference; use async pipelines.
  end note
}

ui ..> api
api ..> domain
api ..> security
api ..> orchestration
api ..> control
api ..> data
orchestration ..> control
control ..> domain
data ..> domain
security ..> domain
control ..> observability
security ..> observability
data ..> observability

@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml ComponentDiagram
skinparam componentStyle rectangle

interface IAuthAPI
interface IPolicyAPI
interface ICommandAPI
interface IStatusAPI
interface IArchiveAPI

component "RemoteUI" as RemoteUI

component "AuthService" as AuthService <<service>> 
component "PolicyService" as PolicyService <<service>> 
component "Sequencer" as Sequencer <<service>> 
component "Scheduler" as Scheduler <<service>> 
component "CommandRouter" as CommandRouter <<service>> 
component "AccessModeAllocator" as AccessModeAllocator <<service>> 
component "ControlGateway" as ControlGateway <<service>> 
component "SimulatorAdapter" as SimulatorAdapter <<plugin>> 
component "ParameterDB" as ParameterDB <<database>> 
component "TelemetryBus" as TelemetryBus <<broker>> 
component "QuickLookProcessor" as QuickLookProcessor <<service>> 
component "NearLineProcessor" as NearLineProcessor <<service>> 
component "ArchiveClient" as ArchiveClient <<service>> 
component "AuditLogService" as AuditLogService <<service>> 
component "EventLogService" as EventLogService <<service>> 
component "MetricsService" as MetricsService <<service>> 

RemoteUI - IAuthAPI
RemoteUI - IPolicyAPI
RemoteUI - ICommandAPI
RemoteUI - IStatusAPI
RemoteUI - IArchiveAPI

AuthService - IAuthAPI
PolicyService - IPolicyAPI
CommandRouter - ICommandAPI
ControlGateway - IStatusAPI
ArchiveClient - IArchiveAPI

Sequencer --> CommandRouter : submitStep()
Sequencer --> Scheduler : queueOps()
CommandRouter --> PolicyService : authorize+siteGate()
CommandRouter --> AccessModeAllocator : requestLease()
CommandRouter --> ControlGateway : sendToIoc()
ControlGateway --> SimulatorAdapter : simulateIfEnabled()
ControlGateway --> ParameterDB : readCachedParams()
Sequencer --> QuickLookProcessor : syncProcess()
QuickLookProcessor --> TelemetryBus : publishProducts()
NearLineProcessor --> TelemetryBus : subscribeProducts()
NearLineProcessor --> ParameterDB : asyncWrites()
ArchiveClient --> TelemetryBus : subscribeProducts()
ArchiveClient --> AuditLogService : auditArchive()
CommandRouter --> AuditLogService : auditAccess()
CommandRouter --> EventLogService : faultEvent()
AuditLogService --> MetricsService : emitMetrics()
EventLogService --> MetricsService : emitMetrics()

note right of CommandRouter
ASR-004/NFR-001: common command schema + ACK/NAK + timeouts.
NFR-008: audit all access; TLS on APIs.
end note

note right of NearLineProcessor
FR-046/ASR-003: acquisition precedence; drop/defer near-line under contention.
end note

note right of TelemetryBus
ASR-003/ASR-011: isolate monitoring/logging via async pub/sub to avoid interfering with observing.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml DeploymentDiagram
skinparam linetype ortho

node "Local Control Room\n(6 active nodes max)" as LocalStations {
  artifact "RemoteUI" as LocalRemoteUI
}

node "Remote Site\n(<=2 monitoring nodes)" as RemoteStations {
  artifact "RemoteUI" as RemoteRemoteUI
}

node "OCS Service Cluster\n(HA, replicated)" as OCSCluster {
  node "AppNode-1" as App1 {
    artifact "AuthService"
    artifact "PolicyService"
    artifact "Sequencer"
    artifact "Scheduler"
  }
  node "AppNode-2" as App2 {
    artifact "CommandRouter"
    artifact "AccessModeAllocator"
    artifact "ControlGateway"
    artifact "ArchiveClient"
  }
  node "AppNode-3" as App3 {
    artifact "QuickLookProcessor"
    artifact "NearLineProcessor"
    artifact "AuditLogService"
    artifact "EventLogService"
    artifact "MetricsService"
  }
  node "BrokerNode" as BrokerNode {
    artifact "TelemetryBus"
  }
}

node "DB Server" as DBServer {
  database "ParameterDB" as ParameterDB
  database "PolicyDB" as PolicyDB
  database "LogStore" as LogStore
}

node "IOC Network (EPICS)" as IOCNet {
  node "TelescopeIOC" as TelescopeIOC
  node "InstrumentIOC-A" as InstrumentIOCA
  node "InstrumentIOC-B" as InstrumentIOCB
}

node "GeminiArchive System" as GeminiArchive <<external>> {
  database "ArchiveDB" as ArchiveDB
}

cloud "LAN/WAN" as Network

LocalStations -- Network
RemoteStations -- Network
Network -- OCSCluster : TLS
OCSCluster -- DBServer : low-latency link
OCSCluster -- IOCNet : real-time control link
OCSCluster -- GeminiArchive : archive link

note right of OCSCluster
NFR-009/FR-057: scale to 6 active + 2 monitoring nodes, up to 10 active capacity.
NFR-003: isolate monitoring/testing/admin impact <=2% on observing latency.
end note

note right of IOCNet
NFR-001: handshake 100-200ms; timeouts ~500ms.
ASR-010: EPICS-based IOC DB.
end note

note bottom of Network
NFR-005: LAN throughput 20-40 Mbit/s for data transfer.
end note
@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml ContainerDiagram
left to right direction
skinparam rectangleStyle rounded
skinparam linetype ortho

rectangle "RemoteUI\n[Monitoring][Operations][Planning]\n(NFR-010 UX, FR-022 keyboard non-effective for monitoring)" as C_UI

rectangle "OCS API Gateway\n[IAuthAPI][IPolicyAPI][ICommandAPI][IStatusAPI][IArchiveAPI]\n(TLS, audit hooks)" as C_APIGW

rectangle "AuthService\n[Authenticate]\n(FR-039, NFR-008)" as C_AUTH
rectangle "PolicyService\n[RBAC][SiteRestriction]\n(ASR-001, ASR-006)" as C_POLICY
rectangle "Sequencer\n[RunQueue]\n(ASR-002)" as C_SEQ
rectangle "Scheduler\n[Resequence]\n(FR-014, FR-017)" as C_SCHED
rectangle "CommandRouter\n[RouteCommand]\n(ASR-004/NFR-001)" as C_ROUTER
rectangle "AccessModeAllocator\n[AllocateResource]\n(ASR-005/ASR-012)" as C_ALLOC
rectangle "ControlGateway\n[IOCBridge][StatusAPI]\n(FR-051 non-blocking)" as C_GW
rectangle "SimulatorAdapter\n[Simulation]\n(ASR-008)" as C_SIM

rectangle "TelemetryBus\n[PubSub]\n(ASR-003 isolation, ASR-011)" as C_BUS
rectangle "QuickLookProcessor\n[QuickLook]\n(FR-045 sync)" as C_QL
rectangle "NearLineProcessor\n[NearLine]\n(FR-046 async, drop under contention)" as C_NL
rectangle "ArchiveClient\n[ArchiveData]\n(ASR-009)" as C_ARCH

database "ParameterDB\n(ASR-010, NFR-017 2-3ms)\ncache+async writes" as C_PARAMDB
database "PolicyDB\n(remote site policy + RBAC snapshots)" as C_POLICYDB
database "LogStore\n[Audit+Event]\n(NFR-013/014, immutability/retention)" as C_LOGDB

rectangle "MetricsService\n[SLO/SLI]\n(NFR-003/004/011/015/017)" as C_METRICS

cloud "IOC Network (EPICS)\n[TelescopeIOC][InstrumentIOCs]" as C_IOCNET
cloud "GeminiArchive\n(external)" as C_GEMARCH
cloud "External Data Sources\n[WeatherStation][StarCatalogService][TimeReferenceSystem]" as C_EXT

C_UI --> C_APIGW : HTTPS/TLS
C_APIGW --> C_AUTH : auth()
C_APIGW --> C_POLICY : authorize()+siteGate()
C_APIGW --> C_SEQ : runQueue()
C_APIGW --> C_ROUTER : submitCommand()
C_APIGW --> C_GW : statusQuery()
C_APIGW --> C_ARCH : archiveQuery()

C_SEQ --> C_SCHED : build/resortQueue()
C_SEQ --> C_ROUTER : submitStep()

C_ROUTER --> C_POLICY : RBAC+siteRestriction
C_ROUTER --> C_ALLOC : requestLease()
C_ROUTER --> C_GW : sendToIoc()
C_GW --> C_IOCNET : ACK/NAK protocol
C_GW --> C_SIM : simulateIfEnabled()
C_GW --> C_PARAMDB : readCriticalParams()

C_QL --> C_BUS : publish()
C_NL --> C_BUS : subscribe()
C_ARCH --> C_BUS : subscribe()
C_ARCH --> C_GEMARCH : archive(FITS)

C_POLICY --> C_POLICYDB : persistPolicy
C_AUTH --> C_LOGDB : auditLogin
C_ROUTER --> C_LOGDB : audit+event
C_QL --> C_LOGDB : processingEvents
C_NL --> C_LOGDB : processingEvents

C_LOGDB --> C_METRICS : emitSLIs
C_APIGW --> C_METRICS : apiLatency
C_GW --> C_METRICS : statusLatency

C_SCHED --> C_EXT : fetchConditions/catalog/time

note right of C_ROUTER
NFR-001: accept/reject <=2s; timeouts ~500ms.
FR-064: retries only for retryable idempotent commands.
end note

note right of C_BUS
ASR-003: monitoring/admin/testing must not impact observing (>2%).
Use async pub/sub + rate limits + separate consumers.
end note

note bottom of C_ARCH
NFR-006: lossless compression enforced for transmissions.
end note
@enduml
```