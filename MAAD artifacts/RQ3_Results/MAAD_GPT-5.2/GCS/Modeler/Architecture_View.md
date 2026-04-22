## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml Gemini_UseCase
left to right direction
skinparam packageStyle rectangle

actor "Astronomer" as Astronomer
actor "TelescopeOperator" as TelescopeOperator
actor "OperationsStaff" as OperationsStaff
actor "MaintenanceEngineer" as MaintenanceEngineer
actor "RemoteUser" as RemoteUser
actor "VisitorInstrument" as VisitorInstrument
actor "SafetyInterlockSystem" as SafetyInterlockSystem
actor "GeminiArchive" as GeminiArchive
actor "HomeInstitute" as HomeInstitute

rectangle "Gemini Observatory Control System (Gemini OCS)" as System {
  usecase "Logon" as UC_Logon
  usecase "Select Mode" as UC_SelectMode
  usecase "Submit Observation" as UC_SubmitObs
  usecase "Execute Sequence" as UC_ExecSeq
  usecase "Direct Control" as UC_DirectControl
  usecase "Monitor Status" as UC_Monitor
  usecase "Reconfigure System" as UC_Reconfig
  usecase "Run Self-Test" as UC_SelfTest
  usecase "Archive Data" as UC_Archive
  usecase "Transfer FITS" as UC_TransferFITS
  usecase "Use Simulator" as UC_Simulate
  usecase "Visitor Instrument Ops" as UC_VisitorOps
  usecase "Emergency Safe State" as UC_SafeState

  usecase "Authorize Access" as UC_Auth <<include>>
  usecase "Allocate Resources" as UC_Allocate <<include>>
  usecase "Validate Command" as UC_Validate <<include>>
  usecase "Audit Log" as UC_Audit <<include>>
  usecase "Site Restrict" as UC_SiteRestrict <<include>>
  usecase "Local Safety Gate" as UC_SafetyGate <<include>>
}

Astronomer --> UC_Logon
Astronomer --> UC_SelectMode
Astronomer --> UC_SubmitObs
Astronomer --> UC_Monitor
Astronomer --> UC_Simulate

TelescopeOperator --> UC_Logon
TelescopeOperator --> UC_SelectMode
TelescopeOperator --> UC_ExecSeq
TelescopeOperator --> UC_DirectControl
TelescopeOperator --> UC_Monitor
TelescopeOperator --> UC_Reconfig

OperationsStaff --> UC_Logon
OperationsStaff --> UC_SelectMode
OperationsStaff --> UC_DirectControl
OperationsStaff --> UC_Reconfig
OperationsStaff --> UC_SelfTest
OperationsStaff --> UC_Simulate

MaintenanceEngineer --> UC_Logon
MaintenanceEngineer --> UC_SelectMode
MaintenanceEngineer --> UC_SelfTest
MaintenanceEngineer --> UC_Reconfig
MaintenanceEngineer --> UC_Monitor

RemoteUser --> UC_Logon
RemoteUser --> UC_SelectMode
RemoteUser --> UC_SubmitObs
RemoteUser --> UC_Monitor

VisitorInstrument --> UC_VisitorOps
VisitorInstrument --> UC_Monitor
VisitorInstrument --> UC_Simulate

SafetyInterlockSystem --> UC_SafeState

GeminiArchive <-- UC_Archive
HomeInstitute <-- UC_TransferFITS

UC_SelectMode .> UC_Auth : <<include>>
UC_SubmitObs .> UC_Auth : <<include>>
UC_ExecSeq .> UC_Allocate : <<include>>
UC_ExecSeq .> UC_Validate : <<include>>
UC_ExecSeq .> UC_Audit : <<include>>
UC_DirectControl .> UC_Auth : <<include>>
UC_DirectControl .> UC_Allocate : <<include>>
UC_DirectControl .> UC_Validate : <<include>>
UC_DirectControl .> UC_Audit : <<include>>
UC_Monitor .> UC_Auth : <<include>>
UC_Monitor .> UC_Audit : <<include>>
UC_Reconfig .> UC_Auth : <<include>>
UC_Reconfig .> UC_Allocate : <<include>>
UC_Reconfig .> UC_Audit : <<include>>
UC_SelfTest .> UC_Auth : <<include>>
UC_SelfTest .> UC_Audit : <<include>>
UC_Archive .> UC_Audit : <<include>>
UC_TransferFITS .> UC_Audit : <<include>>
UC_VisitorOps .> UC_Auth : <<include>>
UC_VisitorOps .> UC_Validate : <<include>>
UC_VisitorOps .> UC_Audit : <<include>>

UC_DirectControl ..> UC_ExecSeq : <<extend>> "Interactive override"
UC_SubmitObs ..> UC_ExecSeq : <<extend>> "Scheduler triggers"
UC_SafeState .> UC_SafetyGate : <<include>>
UC_ExecSeq .> UC_SiteRestrict : <<include>>
UC_DirectControl .> UC_SiteRestrict : <<include>>
UC_ExecSeq .> UC_SafetyGate : <<include>>
UC_DirectControl .> UC_SafetyGate : <<include>>

note right of System
assumption: "RemoteUser" includes remote astronomer/operator; remote direct control is mediated by Scheduler/Sequencer (FR-025) and gated by site policy (FR-023) and local safety presence (FR-024).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Gemini_Class
skinparam classAttributeIconSize 0

class UserSession {
  +sessionId: String
  +userId: String
  +role: Role
  +siteId: String
  +loginTime: DateTime
  +lastActivityTime: DateTime
  +operationalLevel: OperationalLevel
  +accessMode: AccessMode
  +isRemote: Boolean
  +logout()
  +isExpired(): Boolean
}

enum Role {
  Astronomer
  TelescopeOperator
  OperationsStaff
  MaintenanceEngineer
  RemoteUser
  VisitorInstrument
}

enum OperationalLevel {
  Observing
  Maintenance
  Test
}

enum AccessMode {
  Observing
  Monitoring
  Operation
  Planning
  Testing
  Administrative
}

class PolicyRule {
  +ruleId: String
  +effect: Effect
  +allowedSites: String[*]
  +allowedRoles: Role[*]
  +allowedLevels: OperationalLevel[*]
  +allowedModes: AccessMode[*]
  +allowedOperations: String[*]
}

enum Effect { Allow Deny }

class AuthorizationDecision {
  +decisionId: String
  +effect: Effect
  +reason: String
  +policyVersion: String
}

class Command {
  +commandId: String
  +type: String
  +target: String
  +parameters: Map
  +requestedAt: DateTime
  +requestedBy: String
  +siteId: String
  +requiresResource: Boolean
  +validate(): ValidationResult
}

class ValidationResult {
  +isValid: Boolean
  +errorCode: String
  +message: String
}

class AckNak {
  +commandId: String
  +status: String  'ACK|NAK
  +sentAt: DateTime
  +timeoutMs: int
}

class ResourceLease {
  +leaseId: String
  +resourceId: String
  +holderSessionId: String
  +mode: AccessMode
  +expiresAt: DateTime
  +renew()
  +release()
}

class SubsystemEndpoint {
  +subsystemId: String
  +kind: String  'Telescope|Instrument|Env|Data|Safety
  +supportsSimulation: Boolean
  +status(): Map
  +execute(cmd: Command): AckNak
  +selfTest(level: String): Map
}

class ParameterDB <<persisted>> {
  +key: String
  +type: String
  +value: String
  +allowedMin: String
  +allowedMax: String
  +errorResponse: String
  +read(key: String): String
  +writeAsync(key: String, value: String)
}

class ObservationPlan <<persisted>> {
  +planId: String
  +programId: String
  +constraints: Map
  +sequence: String
  +simulate(): SimulationResult
}

class SimulationResult {
  +resultId: String
  +isFeasible: Boolean
  +warnings: String[*]
}

class TelemetryEvent <<immutable>> {
  +eventId: String
  +timestamp: DateTime
  +source: String
  +type: String
  +payload: Map
}

class AuditEvent <<immutable>> {
  +auditId: String
  +timestamp: DateTime
  +actorSessionId: String
  +action: String
  +target: String
  +result: String
}

class DataProduct <<persisted>> {
  +dataId: String
  +format: String  'FITS
  +compressed: Boolean
  +header: Map
  +storedAt: String
}

class SchedulerSequencer {
  +queueId: String
  +submitPlan(plan: ObservationPlan): String
  +resequence(reason: String)
  +prepareSequence(planId: String)
  +executeNext(): String
  +breakQueue()
}

class AccessModeAllocator {
  +allocate(resourceId: String, session: UserSession, mode: AccessMode): ResourceLease
  +avoidDeadlock(): Boolean
  +release(leaseId: String)
}

class SafetyManager {
  +hazardDetected(hazardCode: String)
  +initiateSafeState(): Boolean
  +confirmSafeState(): Boolean
}

class LoggingService {
  +appendTelemetry(e: TelemetryEvent)
  +appendAudit(e: AuditEvent)
  +queryStatus(topic: String): Map
}

UserSession "1" o-- "0..*" ResourceLease
SchedulerSequencer "1" --> "0..*" SubsystemEndpoint : orchestrates
SchedulerSequencer "1" --> "0..*" ObservationPlan : executes
AccessModeAllocator "1" --> "0..*" ResourceLease : issues
Command "1" --> "0..1" ResourceLease : requires
SubsystemEndpoint "1" --> "1" ParameterDB : reads/writes
LoggingService "1" --> "0..*" TelemetryEvent
LoggingService "1" --> "0..*" AuditEvent
DataProduct "0..*" --> "1" ObservationPlan : producedBy
SafetyManager "1" --> "0..*" SubsystemEndpoint : safeCommands
SafetyManager "1" --> "1" LoggingService : logs

PolicyRule "0..*" --> "1" AuthorizationDecision : evaluatesTo
UserSession "1" --> "0..*" AuthorizationDecision : obtains

note right of SchedulerSequencer
ASR-002: primary control plane; observing mode commands must be mediated.
end note

note right of AccessModeAllocator
ASR-008/FR-038: all critical resources via allocator; deadlock freedom required.
end note

note right of LoggingService
ASR-009/FR-040/NFR-024: sustain 200Hz bursts; isolate from control path.
end note

note right of SafetyManager
ASR-012/NFR-012: initiate safe-state <=2s; confirm <=10s; interlocks independent.
end note

note right of UserSession
NFR-006: privileges at login; 12+ char password; auto-logout 30 min inactivity; privilege changes audited.
end note

note right of Command
NFR-001: accept/reject within 2s (99.9%); no execution before ACK.
NFR-009: retries; commands not lost.
end note

note right of ParameterDB
ASR-011/NFR-005: 2-3ms access; async writes; EPICS in IOC.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Gemini_Object
skinparam classAttributeIconSize 0

object session1 as "session1:UserSession [ExecuteSequence]" {
  userId = "op-17"
  role = "TelescopeOperator"
  siteId = "Summit"
  operationalLevel = "Observing"
  accessMode = "Operation"
  isRemote = false
}

object plan1 as "plan1:ObservationPlan [SubmitObservation]" {
  planId = "PLAN-2026-0313-001"
  programId = "GS-2026A-Q-12"
  sequence = "ACQ->EXPOSE(60s)x3->DITHER"
}

object cmd1 as "cmd1:Command [ExecuteSequence]" {
  commandId = "CMD-88421"
  type = "Slew"
  target = "Telescope"
  siteId = "Summit"
}

object lease1 as "lease1:ResourceLease [AllocateResources]" {
  leaseId = "LEASE-77"
  resourceId = "TelescopeBeam"
  holderSessionId = "session1"
  mode = "Operation"
}

object seq1 as "seq1:SchedulerSequencer [ExecuteSequence]" {
  queueId = "Q-NIGHT-2026-0313"
}

object alloc1 as "alloc1:AccessModeAllocator [AllocateResources]" {
}

object tel1 as "tel1:SubsystemEndpoint [ExecuteSequence]" {
  subsystemId = "TCS"
  kind = "Telescope"
  supportsSimulation = false
}

object log1 as "log1:LoggingService [AuditLog]" {
}

object audit1 as "audit1:AuditEvent [AuditLog]" {
  action = "ExecuteCommand"
  target = "TCS"
  result = "ACK"
}

session1 -- lease1
seq1 -- plan1
seq1 -- tel1
seq1 -- alloc1
cmd1 -- lease1
log1 -- audit1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml Gemini_State_OperationalLevel
hide empty description

state "OperationalLevelStateMachine" as OLSM {
  [*] --> PoweredOff

  PoweredOff --> Booting : powerOn
  Booting --> ObservingLevel : bootOk / versionConsistencyCheck
  Booting --> MaintenanceLevel : bootOk [maintenanceRequested]
  Booting --> TestLevel : bootOk [testRequested]

  ObservingLevel --> MaintenanceLevel : enterMaintenance [authorized]
  ObservingLevel --> TestLevel : enterTest [authorized]
  MaintenanceLevel --> ObservingLevel : exitMaintenance [authorized]
  TestLevel --> ObservingLevel : exitTest [authorized]

  state ObservingLevel {
    [*] --> ObservingMode
    ObservingMode --> MonitoringMode : switchMode [authorized]
    MonitoringMode --> ObservingMode : switchMode [authorized]
    ObservingMode --> OperationMode : enableOperation [role==TelescopeOperator]
    OperationMode --> ObservingMode : disableOperation
    ObservingMode --> PlanningMode : switchMode
    PlanningMode --> ObservingMode : switchMode
    ObservingMode --> AdministrativeMode : switchMode [role==OperationsStaff]
    AdministrativeMode --> ObservingMode : switchMode
  }

  state MaintenanceLevel {
    [*] --> MaintenanceMode
    MaintenanceMode --> MonitoringMode : switchMode
    MonitoringMode --> MaintenanceMode : switchMode
    MaintenanceMode --> TestingMode : runSelfTest [authorized]
    TestingMode --> MaintenanceMode : endTest
  }

  state TestLevel {
    [*] --> TestingMode
    TestingMode --> MonitoringMode : switchMode
    MonitoringMode --> TestingMode : switchMode
  }

  ObservingLevel --> SafeState : hazardNotification / initiateSafeState
  MaintenanceLevel --> SafeState : hazardNotification / initiateSafeState
  TestLevel --> SafeState : hazardNotification / initiateSafeState
  SafeState --> MaintenanceLevel : recover [authorized] / reconfigure
  SafeState --> ObservingLevel : recover [authorized] / reconfigure

  ObservingLevel --> PoweredOff : shutdown
  MaintenanceLevel --> PoweredOff : shutdown
  TestLevel --> PoweredOff : shutdown
}

note right of SafeState
NFR-012: initiate safe-state <=2s; confirm <=10s.
end note

note right of ObservingLevel
FR-045: in Engineering/Maintenance, ignore directives from other systems but still provide status.
(Mode gating enforced by authorization + command router.)
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Gemini_Activity_ExecuteSequence
skinparam activityStyle rounded

start
:Logon;
:Determine privileges [SecurityCheck];
:Select operational level & access mode;

if (Mode == Observing?) then (yes)
  :Enforce "sequencer-mediated" control;
else (no)
  :Allow maintenance/test workflows;
endif

:Submit ObservationPlan;
:Validate plan & commands [ValidateCommand];

note right
NFR-001: accept/reject <= 2s (99.9%).
FR-050: range/validity checking before execution.
end note

:Authorize access [AuthorizeAccess];
:Apply site restrictions [SiteRestrict];

if (Remote control?) then (yes)
  :Check local safety presence [LocalSafetyGate];
  note right
  FR-024: local staff + stop button + video/audio required.
  end note
endif

:Allocate critical resources [AllocateResources];
note right
FR-038/ASR-008: deadlock-free allocation; critical resources only via allocator.
end note

fork
  :Execute next step via SchedulerSequencer;
  :Send command to SubsystemEndpoint;
  :Receive ACK/NAK;
  note right
  FR-044/NFR-002: handshake 100-200ms; timeout ~500ms; retries (NFR-009).
  end note
fork again
  :Stream telemetry to LoggingService;
  :Append audit events;
  note right
  FR-040/ASR-009: 200Hz bursts; no data loss; isolate from control path.
  end note
end fork

:Acquire detector data;
:Quick-look assessment (sync);
:Near-line processing (async);

note right
FR-034 quick-look synchronous; FR-035 near-line async; acquisition takes precedence.
NFR-007: background tasks <=5% CPU or <=200ms added latency while observing.
end note

:Archive DataProduct to GeminiArchive;
:Release resource leases;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Gemini_Sequence_ExecuteSequence
autonumber
actor TelescopeOperator as TelescopeOperator
participant "GeminiUI" as GeminiUI
participant "AuthService" as AuthService
participant "PolicyService" as PolicyService
participant "SchedulerSequencer" as SchedulerSequencer
participant "AccessModeAllocator" as AccessModeAllocator
participant "CommandRouter" as CommandRouter
participant "TelescopeControlSubsystem" as TelescopeControlSubsystem
participant "LoggingService" as LoggingService
database "ParameterDB" as ParameterDB
participant "SafetyManager" as SafetyManager

TelescopeOperator -> GeminiUI : Logon
GeminiUI -> AuthService : Authenticate
AuthService --> GeminiUI : SessionToken

GeminiUI -> PolicyService : SelectMode(level,mode)
PolicyService --> GeminiUI : ModeAccepted

GeminiUI -> SchedulerSequencer : SubmitPlan(plan)
SchedulerSequencer -> PolicyService : AuthorizeAccess(plan)
PolicyService --> SchedulerSequencer : Allow

SchedulerSequencer -> AccessModeAllocator : AllocateResources(TelescopeBeam)
AccessModeAllocator --> SchedulerSequencer : ResourceLease

SchedulerSequencer -> CommandRouter : ValidateCommand(sequenceStep)
note right of CommandRouter
NFR-001: accept/reject <=2s; no execution before ACK.
end note
CommandRouter -> PolicyService : AuthorizeAccess(command)
PolicyService --> CommandRouter : Allow
CommandRouter -> SafetyManager : LocalSafetyGate(command)
SafetyManager --> CommandRouter : SafetyOk

CommandRouter -> TelescopeControlSubsystem : ExecuteCommand(cmd)
TelescopeControlSubsystem -> ParameterDB : ReadParams
ParameterDB --> TelescopeControlSubsystem : Params
TelescopeControlSubsystem --> CommandRouter : ACK/NAK

CommandRouter -> LoggingService : AuditLog(action,result)
CommandRouter -> LoggingService : TelemetryLog(status)

alt NAK or timeout
  note right
  NFR-009: auto-retry; commands not lost; retry attempts logged.
  NFR-002: timeout ~500ms; handshake 100-200ms.
  end note
  CommandRouter -> TelescopeControlSubsystem : RetryExecute(cmd)
  TelescopeControlSubsystem --> CommandRouter : ACK/NAK
  CommandRouter -> LoggingService : AuditLog(retry,result)
end

SchedulerSequencer --> GeminiUI : StepResult
@enduml
```

```plantuml
@startuml Gemini_Sequence_RemoteMonitoring
autonumber
actor RemoteUser as RemoteUser
participant "RemoteGeminiUI" as RemoteGeminiUI
participant "SecurityGateway" as SecurityGateway
participant "AuthService" as AuthService
participant "PolicyService" as PolicyService
participant "MonitoringService" as MonitoringService
participant "LoggingService" as LoggingService
participant "SubsystemStatusAPI" as SubsystemStatusAPI

RemoteUser -> RemoteGeminiUI : Logon
RemoteGeminiUI -> SecurityGateway : TLSConnect
note right of SecurityGateway
NFR-030: TLS 1.2+ for remote command/data and DB access.
NFR-029: firewall/gateway; whitelist only; IDS alert <=1 min.
end note
SecurityGateway -> AuthService : Authenticate
AuthService --> SecurityGateway : SessionToken
SecurityGateway --> RemoteGeminiUI : SessionToken

RemoteGeminiUI -> PolicyService : SelectMode(Monitoring)
PolicyService --> RemoteGeminiUI : ModeAccepted

RemoteGeminiUI -> MonitoringService : SubscribeDisplays(selection)
MonitoringService -> PolicyService : AuthorizeAccess(readOnly)
PolicyService --> MonitoringService : Allow

loop up to 10Hz per subsystem (rate-limited)
  MonitoringService -> SubsystemStatusAPI : QueryStatus
  SubsystemStatusAPI --> MonitoringService : StatusSnapshot
  MonitoringService --> RemoteGeminiUI : UpdateDisplay
end

MonitoringService -> LoggingService : AuditLog(monitorSession)

note right of MonitoringService
FR-004/NFR-007: monitoring read-only and non-intrusive; <=5% CPU or <=200ms added latency while observing.
NFR-023: local update <=4s; remote update <=8s; status request <=5s.
FR-051: continuous monitoring up to 10Hz; limit concurrent sessions per node.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Gemini_Collaboration_ExecuteSequence
skinparam linetype ortho

actor TelescopeOperator as TelescopeOperator
rectangle GeminiUI as GeminiUI
rectangle PolicyService as PolicyService
rectangle SchedulerSequencer as SchedulerSequencer
rectangle AccessModeAllocator as AccessModeAllocator
rectangle CommandRouter as CommandRouter
rectangle TelescopeControlSubsystem as TelescopeControlSubsystem
rectangle SafetyManager as SafetyManager
rectangle LoggingService as LoggingService

TelescopeOperator -- GeminiUI
GeminiUI -- PolicyService
GeminiUI -- SchedulerSequencer
SchedulerSequencer -- AccessModeAllocator
SchedulerSequencer -- CommandRouter
CommandRouter -- PolicyService
CommandRouter -- SafetyManager
CommandRouter -- TelescopeControlSubsystem
CommandRouter -- LoggingService

note right of TelescopeOperator
Scenario: Execute Sequence (FR-010/FR-003/FR-044/NFR-001)
end note

TelescopeOperator -> GeminiUI : 1:SubmitPlan
GeminiUI -> SchedulerSequencer : 2:SubmitPlan
SchedulerSequencer -> PolicyService : 3:AuthorizeAccess
SchedulerSequencer -> AccessModeAllocator : 4:AllocateResources
SchedulerSequencer -> CommandRouter : 5:ValidateCommand
CommandRouter -> SafetyManager : 6:LocalSafetyGate
CommandRouter -> TelescopeControlSubsystem : 7:ExecuteCommand
CommandRouter -> LoggingService : 8:AuditLog
@enduml
```

```plantuml
@startuml Gemini_Collaboration_RemoteMonitoring
skinparam linetype ortho

actor RemoteUser as RemoteUser
rectangle RemoteGeminiUI as RemoteGeminiUI
rectangle SecurityGateway as SecurityGateway
rectangle PolicyService as PolicyService
rectangle MonitoringService as MonitoringService
rectangle SubsystemStatusAPI as SubsystemStatusAPI
rectangle LoggingService as LoggingService

RemoteUser -- RemoteGeminiUI
RemoteGeminiUI -- SecurityGateway
RemoteGeminiUI -- PolicyService
RemoteGeminiUI -- MonitoringService
MonitoringService -- PolicyService
MonitoringService -- SubsystemStatusAPI
MonitoringService -- LoggingService

note right of RemoteUser
Scenario: Remote Monitoring (FR-020/FR-026/NFR-030/NFR-023)
end note

RemoteUser -> RemoteGeminiUI : 1:SubscribeDisplays
RemoteGeminiUI -> SecurityGateway : 2:TLSConnect
RemoteGeminiUI -> PolicyService : 3:SelectMode
RemoteGeminiUI -> MonitoringService : 4:Subscribe
MonitoringService -> SubsystemStatusAPI : 5:QueryStatus
MonitoringService -> RemoteGeminiUI : 6:UpdateDisplay
MonitoringService -> LoggingService : 7:AuditLog
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Gemini_Package
skinparam packageStyle rectangle

package "ui" as ui {
  note bottom
  Gemini UI toolkit; uniform per access level (NFR-026) and portable (NFR-027).
  end note
}

package "security" as security {
  note bottom
  AuthN/AuthZ, site restrictions, auditing (NFR-006, FR-023, ASR-013).
  end note
}

package "orchestration" as orchestration {
  note bottom
  Scheduler/Sequencer control plane (ASR-002); queue resequencing (FR-011/FR-029).
  end note
}

package "resource" as resource {
  note bottom
  Access Mode Allocation; deadlock freedom (FR-038/ASR-008).
  end note
}

package "control" as control {
  note bottom
  Command routing, protocol, subsystem adapters (ASR-003, FR-044).
  end note
}

package "telemetry" as telemetry {
  note bottom
  Telemetry + audit logging pipeline (ASR-009/FR-040/NFR-024).
  end note
}

package "data" as data {
  note bottom
  Data acquisition, quick-look, near-line, archive/transfer (FR-031..FR-037).
  end note
}

package "simulation" as simulation {
  note bottom
  Virtual telescope + subsystem simulators (ASR-006/FR-052/FR-030).
  end note
}

package "safety" as safety {
  note bottom
  Safety manager; safe-state orchestration (ASR-012/FR-049).
  end note
}

ui ..> security
ui ..> orchestration
ui ..> telemetry

orchestration ..> security
orchestration ..> resource
orchestration ..> control
orchestration ..> data
orchestration ..> simulation
orchestration ..> safety

control ..> security
control ..> telemetry
control ..> safety

data ..> telemetry
data ..> control

simulation ..> control
simulation ..> data

resource ..> security
safety ..> telemetry
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Gemini_Component
skinparam componentStyle rectangle

component "GeminiUI" as GeminiUI <<UI>> [ModeAware]
component "RemoteGeminiUI" as RemoteGeminiUI <<UI>> [NetworkTransparent]

component "SecurityGateway" as SecurityGateway <<Gateway>> [Firewall+TLS]
component "AuthService" as AuthService <<Service>> [RBAC]
component "PolicyService" as PolicyService <<Service>> [Level+Mode+SitePolicy]

component "SchedulerSequencer" as SchedulerSequencer <<Service>> [Orchestration]
component "AccessModeAllocator" as AccessModeAllocator <<Service>> [DeadlockFree]
component "CommandRouter" as CommandRouter <<Service>> [ACK/NAK]

component "MonitoringService" as MonitoringService <<Service>> [ReadOnly]
component "LoggingService" as LoggingService <<Service>> [200HzBurst]
component "SafetyManager" as SafetyManager <<Service>> [SafeState]

component "ParameterDB" as ParameterDB <<Database>> [2-3ms]
component "DataAcquisitionService" as DataAcquisitionService <<Service>> [DetectorData]
component "QuickLookService" as QuickLookService <<Service>> [SyncQA]
component "NearLineProcessingService" as NearLineProcessingService <<Service>> [Async]
component "ArchiveTransferService" as ArchiveTransferService <<Service>> [Archive+FITS]

component "VirtualTelescopeSimulator" as VirtualTelescopeSimulator <<Service>> [Simulation]
component "VisitorInstrumentAPI" as VisitorInstrumentAPI <<API>> [StableSubset]

component "TelescopeControlSubsystem" as TelescopeControlSubsystem <<Subsystem>> [IOCAdapter]
component "InstrumentControlSubsystem" as InstrumentControlSubsystem <<Subsystem>> [MultiInstrument]
component "SubsystemStatusAPI" as SubsystemStatusAPI <<API>> [StatusNoLock]

interface "IAuth" as IAuth
interface "IPolicy" as IPolicy
interface "ISequencer" as ISequencer
interface "IAllocator" as IAllocator
interface "ICommand" as ICommand
interface "IMonitor" as IMonitor
interface "ILog" as ILog
interface "ISafety" as ISafety
interface "IParamDB" as IParamDB
interface "IStatus" as IStatus
interface "IVisitor" as IVisitor

AuthService - IAuth
PolicyService - IPolicy
SchedulerSequencer - ISequencer
AccessModeAllocator - IAllocator
CommandRouter - ICommand
MonitoringService - IMonitor
LoggingService - ILog
SafetyManager - ISafety
ParameterDB - IParamDB
SubsystemStatusAPI - IStatus
VisitorInstrumentAPI - IVisitor

GeminiUI ..> IAuth
GeminiUI ..> IPolicy
GeminiUI ..> ISequencer
GeminiUI ..> IMonitor

RemoteGeminiUI ..> SecurityGateway
SecurityGateway ..> IAuth
SecurityGateway ..> IPolicy
SecurityGateway ..> IMonitor
SecurityGateway ..> ICommand

SchedulerSequencer ..> IPolicy
SchedulerSequencer ..> IAllocator
SchedulerSequencer ..> ICommand
SchedulerSequencer ..> ISafety
SchedulerSequencer ..> ILog

CommandRouter ..> IPolicy
CommandRouter ..> ISafety
CommandRouter ..> ILog

MonitoringService ..> IPolicy
MonitoringService ..> IStatus
MonitoringService ..> ILog

TelescopeControlSubsystem ..> IParamDB
InstrumentControlSubsystem ..> IParamDB

DataAcquisitionService ..> ICommand
QuickLookService ..> ILog
NearLineProcessingService ..> ILog
ArchiveTransferService ..> ILog

VirtualTelescopeSimulator ..> ICommand
VisitorInstrumentAPI ..> ICommand
VisitorInstrumentAPI ..> IStatus

note right of VisitorInstrumentAPI
ASR-007: stable subset API; semantic versioning; 2-year backward compatibility after deprecation.
end note

note right of CommandRouter
ASR-003/FR-044: uniform ACK/NAK, timeouts, handshaking; retries (NFR-009).
end note

note right of MonitoringService
FR-021: status on request without delaying control or locking.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Gemini_Deployment
skinparam linetype ortho

node "Summit LAN\n(20-40 Mbps)" as SummitLAN {
  node "ControlNode-1\n(Active)" as CN1 {
    artifact "GeminiUI"
    artifact "SchedulerSequencer"
    artifact "CommandRouter"
    artifact "MonitoringService"
  }
  node "ControlNode-2\n(Active)" as CN2 {
    artifact "GeminiUI"
    artifact "SchedulerSequencer (HA standby)"
    artifact "CommandRouter"
  }
  node "TelemetryNode" as TN {
    artifact "LoggingService"
  }
  database "ParameterDB (EPICS IOC)\n2-3ms access" as PDB
  node "IOC Network" as IOCNet {
    node "TCS IOC" as TCSIOC {
      artifact "TelescopeControlSubsystem"
    }
    node "Instrument IOC(s)" as INSTRIOC {
      artifact "InstrumentControlSubsystem"
    }
  }
  node "Safety Hardware\n(Independent Interlocks)" as SafetyHW
  node "Time/Event Buses\n(TimeBus/ReflectiveMemory/EventBus)" as TimeBus
  node "DataNode" as DN {
    artifact "DataAcquisitionService"
    artifact "QuickLookService"
    artifact "NearLineProcessingService"
    artifact "ArchiveTransferService"
  }
}

node "Base Facility LAN" as BaseLAN {
  node "RemoteOpsNode" as RON {
    artifact "RemoteGeminiUI"
  }
  node "SecurityGateway\n(Firewall+IDS+TLS)" as GW {
    artifact "SecurityGateway"
    artifact "AuthService"
    artifact "PolicyService"
  }
}

node "GeminiArchive Facility" as ArchiveSite {
  node "GeminiArchive" as GeminiArchive
}

node "Home Institute" as HomeInstitute {
  node "InstituteDataServer" as InstituteDataServer
}

CN1 -- SummitLAN
CN2 -- SummitLAN
TN -- SummitLAN
DN -- SummitLAN
PDB -- SummitLAN
IOCNet -- SummitLAN
SafetyHW -- SummitLAN
TimeBus -- SummitLAN

CN1 --> IOCNet : Control/Telemetry
CN1 --> PDB : ParamRead/WriteAsync
CN1 --> TN : Telemetry/Audit (burst 200Hz)
DN --> TN : ProcessingLogs
DN --> GeminiArchive : ArchiveData
ArchiveTransferService ..> InstituteDataServer : FITSTransfer

RON --> GW : WAN (leased line for essential)\nTLS 1.2+
GW --> SummitLAN : WAN link\nRemote RTT <=10s (NFR-021)

SafetyHW --> CN1 : HazardSignal
CN1 --> SafetyHW : SafeStateCommand

note right of SummitLAN
NFR-022: up to 6 active + 2 monitoring nodes; cope with 10 nodes.
NFR-007: background tasks <=5% CPU or <=200ms added latency while observing.
end note

note right of GW
NFR-029: whitelist-only; IDS alert <=1 min; quarterly pen tests.
NFR-030: encrypted remote channels.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Gemini_Container
left to right direction
skinparam packageStyle rectangle

rectangle "Remote Site" as RemoteSite {
  rectangle "RemoteGeminiUI\n[Monitoring/Planning]\n(NFR-027 portable)" as C_RemoteUI
}

rectangle "Security Perimeter" as Perimeter {
  rectangle "SecurityGateway\n[Firewall+TLS+IDS]\n(NFR-029/030)" as C_Gateway
  rectangle "AuthService\n[RBAC Sessions]\n(NFR-006)" as C_Auth
  rectangle "PolicyService\n[Level/Mode/Site Policy]\n(FR-023/ASR-001)" as C_Policy
}

rectangle "Summit Control Network" as Summit {
  rectangle "GeminiUI\n[Mode-aware UI]\n(NFR-026)" as C_LocalUI
  rectangle "SchedulerSequencer\n[Orchestration]\n(ASR-002)" as C_Sequencer
  rectangle "CommandRouter\n[ACK/NAK + Validate]\n(ASR-003/NFR-001)" as C_CommandRouter
  rectangle "AccessModeAllocator\n[Resource Leases]\n(ASR-008)" as C_Allocator
  rectangle "MonitoringService\n[Read-only]\n(FR-004/FR-021)" as C_Monitor
  rectangle "LoggingService\n[Telemetry+Audit]\n(ASR-009 200Hz)" as C_Log
  rectangle "SafetyManager\n[Safe-state]\n(ASR-012)" as C_Safety
  rectangle "DataAcquisitionService\n[Detector Data]\n(FR-031..33)" as C_DAQ
  rectangle "QuickLookService\n[Sync QA]\n(FR-034)" as C_QuickLook
  rectangle "NearLineProcessingService\n[Async]\n(FR-035)" as C_NearLine
  rectangle "ArchiveTransferService\n[Archive+FITS]\n(FR-036/37)" as C_ArchiveXfer
  database "ParameterDB\n[2-3ms async writes]\n(ASR-011)" as C_ParamDB
  rectangle "VirtualTelescopeSimulator\n[Simulation]\n(ASR-006)" as C_Sim
  rectangle "VisitorInstrumentAPI\n[Stable Subset]\n(ASR-007)" as C_VisitorAPI
  rectangle "TelescopeControlSubsystem\n[IOC Adapter]\n(ASR-004)" as C_TCS
  rectangle "InstrumentControlSubsystem\n[Instrument Servers]\n(FR-014/15/16)" as C_ICS
  rectangle "SubsystemStatusAPI\n[Status No Lock]\n(FR-021)" as C_StatusAPI
}

rectangle "External Systems" as External {
  rectangle "GeminiArchive\n[Archive Store]" as C_Archive
  rectangle "HomeInstitute\n[Data Receiver]" as C_Home
  rectangle "SafetyInterlockSystem\n[Independent]" as C_Interlock
}

C_RemoteUI --> C_Gateway : TLS UI traffic
C_Gateway --> C_Auth : Authenticate
C_Gateway --> C_Policy : Policy checks
C_Gateway --> C_Monitor : Remote monitoring
C_Gateway --> C_Sequencer : Remote submit (mediated)

C_LocalUI --> C_Auth
C_LocalUI --> C_Policy
C_LocalUI --> C_Sequencer
C_LocalUI --> C_Monitor

C_Sequencer --> C_Allocator : AllocateResources
C_Sequencer --> C_CommandRouter : ExecuteSequence
C_CommandRouter --> C_Policy : AuthorizeAccess
C_CommandRouter --> C_Safety : LocalSafetyGate
C_CommandRouter --> C_TCS : ControlCommands
C_CommandRouter --> C_ICS : ControlCommands
C_Monitor --> C_StatusAPI : QueryStatus
C_StatusAPI --> C_TCS : Status
C_StatusAPI --> C_ICS : Status

C_TCS --> C_ParamDB : ParamRead/WriteAsync
C_ICS --> C_ParamDB : ParamRead/WriteAsync

C_CommandRouter --> C_Log : Audit/Telemetry
C_Monitor --> C_Log : Audit
C_DAQ --> C_Log : Telemetry
C_QuickLook --> C_Log : QA results
C_NearLine --> C_Log : Reduction logs

C_DAQ --> C_QuickLook : ProvideFrames
C_DAQ --> C_NearLine : EnqueueAsync
C_ArchiveXfer --> C_Archive : ArchiveData
C_ArchiveXfer --> C_Home : FITSTransfer

C_Sim --> C_CommandRouter : SimulatedCommands
C_VisitorAPI --> C_CommandRouter : SubsetCommands
C_VisitorAPI --> C_StatusAPI : Status

C_Interlock --> C_Safety : HazardNotification
C_Safety --> C_TCS : SafeState
C_Safety --> C_ICS : SafeState

note right of Summit
NFR-007: monitoring/testing/admin must not impact observing (<=5% CPU or <=200ms latency).
NFR-018: essential remote tasks over project-controlled links.
end note
@enduml
```