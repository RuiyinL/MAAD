## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction
skinparam packageStyle rectangle

actor "VLA M&C" as VLA_MC
actor "Backend Controller" as BackendCtrl
actor "Backend Data Processing" as BackendDP
actor "Operator" as Operator
actor "Developer" as Developer
actor "Administrator" as Admin
actor "UPS" as UPS
actor "Correlator Hardware" as CorrelatorHW

rectangle "Correlator Monitor & Control System (CMCS)" as CMCS {
  usecase "Translate Config" as UC_TranslateConfig
  usecase "Apply HW Config" as UC_ApplyHWConfig
  usecase "Control & Monitor" as UC_ControlMonitor
  usecase "Provide Sync Monitor" as UC_SyncMonitor
  usecase "Provide OnDemand Monitor" as UC_OnDemandMonitor
  usecase "Deliver Backend Data" as UC_DeliverBackendData
  usecase "Self-Heal Faults" as UC_SelfHeal
  usecase "Issue Alerts" as UC_Alerts
  usecase "Manage Access" as UC_ManageAccess
  usecase "Remote Debug Access" as UC_RemoteDebug
  usecase "View AutoCorr" as UC_AutoCorr
  usecase "Audit Access" as UC_Audit
}

VLA_MC --> UC_TranslateConfig
VLA_MC --> UC_ControlMonitor
VLA_MC --> UC_SyncMonitor
VLA_MC --> UC_OnDemandMonitor
VLA_MC --> UC_ManageAccess

BackendCtrl --> UC_ControlMonitor
BackendCtrl --> UC_DeliverBackendData

BackendDP --> UC_DeliverBackendData

Operator --> UC_ControlMonitor
Operator --> UC_OnDemandMonitor
Operator --> UC_AutoCorr
Operator --> UC_RemoteDebug

Developer --> UC_RemoteDebug

Admin --> UC_ManageAccess
Admin --> UC_Audit

UPS --> UC_ControlMonitor

CorrelatorHW --> UC_ControlMonitor

UC_TranslateConfig ..> UC_ApplyHWConfig : <<include>>
UC_ControlMonitor ..> UC_SelfHeal : <<include>>
UC_SelfHeal ..> UC_Alerts : <<extend>>
UC_RemoteDebug ..> UC_Audit : <<include>>
UC_ManageAccess ..> UC_Audit : <<include>>

note right of CMCS
assumption: "VLA M&C" represents the VLA Expansion Project Monitor & Control System.
assumption: "Backend Controller" is the control authority for sampling rates/contents.
assumption: "Remote Debug Access" covers FR-005/FR-021/FR-022/FR-031 with per-incident approval and MFA.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class VirtualCorrelatorInterface <<gateway>> {
  +translateConfig(extConfig: ExternalConfig): ConfigTableSet
  +submitControl(cmd: ControlCommand): Ack
  +queryState(query: StateQuery): SystemState
  +streamMonitor(filter: MonitorFilter): MonitorStream
}

class MasterControlNode <<ha>> {
  -nodeId: String
  -role: String  <<primary|secondary>>
  -stateVersion: long
  +applyConfig(tables: ConfigTableSet): Ack
  +routeControl(cmd: ControlCommand): Ack
  +aggregateMessages(msg: Message): void
  +replicateState(delta: StateDelta): void
  +failoverToSecondary(): void
}

class CMIBController <<realtime>> {
  -cmibId16: int
  -ipAddress: String
  -watchdogEnabled: boolean
  +executeRegisterWrite(cmd: ControlCommand): Ack
  +readbackRegisters(): RegisterSnapshot
  +interrogateHardware(): HardwareState
  +reboot(warmBoot: boolean): Ack
}

class ConfigTableSet <<immutable>> {
  +requestId: String
  +createdUtc: String
  +tablesHash: String
  +targetRackId: String
}

class MonitorSample {
  +timestampUtc: String
  +wallclockLocal: String
  +locationId: String
  +metric: String
  +value: String
  +isTimeSynchronous: boolean
}

class Message {
  +timestampUtc: String
  +wallclockLocal: String
  +locationId: String
  +messageId: String
  +severity: String
  +content: String
  +category: String
  +detailLevel: String
}

class SpoolBuffer <<persisted>> {
  +retentionHours: int
  +maxBytes: long
  +enqueue(sample: MonitorSample): void
  +dequeueBatch(max: int): List
  +overrunAlert(): void
}

class EventQueue <<persisted>> {
  +retentionHours: int
  +enqueue(cmd: ControlCommand): void
  +dequeue(): ControlCommand
  +size(): long
}

class BackendDataPublisher {
  +publishDataSet(data: BackendDataSet): Ack
}

class BackendDataSet {
  +dataSetId: String
  +createdUtc: String
  +payloadRef: String
}

class HealthManager {
  +evaluateHealth(): HealthStatus
  +attemptSelfHeal(fault: Fault): Ack
  +issueAlert(fault: Fault): void
}

class PowerControlNode {
  +remoteReboot(target: String): Ack
  +reportPowerEvent(evt: PowerEvent): void
}

class PowerEvent {
  +eventType: String
  +timeRemainingSec: int
  +timestampUtc: String
}

class AuthService <<security>> {
  +authenticate(cert: X509Cert, mfa: MfaProof): Session
  +authorize(session: Session, action: String): Decision
  +revokeUser(userId: String): void
}

class RBACPolicy <<security>> {
  +roles: List
  +privileges: List
  +isAllowed(role: String, action: String): boolean
}

class AuditLog <<persisted>> {
  +write(event: AuditEvent): void
  +purge(olderThanDays: int): void
}

class AuditEvent {
  +timestampUtc: String
  +actorUserId: String
  +actionType: String
  +outcome: String
  +target: String
}

class ControlCommand {
  +commandId: String
  +timestampUtc: String
  +targetId: String
  +type: String
  +payload: String
}

class SystemState {
  +stateVersion: long
  +masterRole: String
  +rackStates: String
  +lastUpdatedUtc: String
}

VirtualCorrelatorInterface --> MasterControlNode : uses
MasterControlNode "1" o-- "1..*" CMIBController : coordinates
MasterControlNode --> BackendDataPublisher : uses
MasterControlNode --> SpoolBuffer : uses
MasterControlNode --> EventQueue : uses
MasterControlNode --> HealthManager : uses
MasterControlNode --> PowerControlNode : uses
MasterControlNode --> AuthService : uses
AuthService --> RBACPolicy : uses
AuthService --> AuditLog : writes
VirtualCorrelatorInterface --> AuthService : uses
VirtualCorrelatorInterface --> AuditLog : writes

CMIBController --> Message : emits
MasterControlNode --> Message : aggregates
SpoolBuffer --> MonitorSample : stores
BackendDataPublisher --> BackendDataSet : publishes
PowerControlNode --> PowerEvent : receives

note right of AuthService
NFR-014/NFR-015/FR-041..FR-050:
- mutual TLS/SSH, MFA for privileged actions
- deny access if CRL check fails
- session expiry policy
end note

note right of SpoolBuffer
FR-013: spool monitor data up to 24h at peak rate; overrun triggers alert.
end note

note right of EventQueue
FR-039/ASR-009: store config/control events for >=96h during comms loss.
end note

note right of CMIBController
FR-025: IP mapping 10.24.<high8>.<low8> from 16-bit id.
FR-032: hardware watchdog reboot and return to service.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView
skinparam classAttributeIconSize 0

object vci1 as "vci1:VirtualCorrelatorInterface [TranslateConfig]" {
}

object masterP as "masterP:MasterControlNode [ControlMonitor]" {
  nodeId = "MCC-PRIMARY"
  role = "primary"
  stateVersion = 18422
}

object masterS as "masterS:MasterControlNode [Failover]" {
  nodeId = "MCC-SECONDARY"
  role = "secondary"
  stateVersion = 18422
}

object tables1 as "tables1:ConfigTableSet [TranslateConfig]" {
  requestId = "REQ-2026-03-13-001"
  createdUtc = "2026-03-13T02:10:00Z"
  tablesHash = "sha256:ab12..."
  targetRackId = "RACK-07"
}

object cmd1 as "cmd1:ControlCommand [ControlMonitor]" {
  commandId = "CMD-7781"
  timestampUtc = "2026-03-13T02:10:02Z"
  targetId = "CMIB-0x12AF"
  type = "SetSampleRate"
  payload = "rateHz=10;metrics=temps,voltages"
}

object cmib1 as "cmib1:CMIBController [ControlMonitor]" {
  cmibId16 = 4783
  ipAddress = "10.24.18.175"
  watchdogEnabled = true
}

object spool1 as "spool1:SpoolBuffer [ProvideSyncMonitor]" {
  retentionHours = 24
  maxBytes = 50000000000
}

object queue1 as "queue1:EventQueue [OfflineQueue]" {
  retentionHours = 96
}

vci1 --> masterP
masterP --> masterS : replicateState
masterP --> tables1 : applyConfig
masterP --> cmd1 : routeControl
masterP --> cmib1
masterP --> spool1
masterP --> queue1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_MasterControlNode
hide empty description

state "MasterControlNode Lifecycle" as M {
  [*] --> Booting : powerOn
  Booting --> StandaloneReady : localBootOk\n(NFR-013)
  Booting --> Degraded : bootFailure

  StandaloneReady --> ConnectedExternal : extLinkUp
  ConnectedExternal --> StandaloneReady : extLinkDown

  state ConnectedExternal {
    [*] --> PrimaryActive : role=primary
    [*] --> SecondaryStandby : role=secondary

    PrimaryActive --> FailingOver : primaryHardFailureDetected
    FailingOver --> SecondaryStandby : rerouteComms\n(ASR-004/FR-019)
    FailingOver --> PrimaryActive : failoverAborted

    SecondaryStandby --> PrimaryActive : promoteSecondary
  }

  StandaloneReady --> ProcessingQueued : commsLoss\nqueueNotEmpty
  ConnectedExternal --> ProcessingQueued : commsLoss\nqueueNotEmpty
  ProcessingQueued --> ConnectedExternal : commsRestored\nqueueDrained
  ProcessingQueued --> StandaloneReady : commsRestored\nnoExternal

  ConnectedExternal --> SelfHealing : faultDetected
  StandaloneReady --> SelfHealing : faultDetected
  SelfHealing --> ConnectedExternal : healed\nwithin20s (NFR-008)
  SelfHealing --> Alerting : notHealed
  Alerting --> Degraded : operatorIntervention

  Degraded --> Booting : reboot
  Degraded --> [*] : shutdown
}
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_TranslateAndApply
skinparam activityStyle rounded

start
:Receive ExternalConfig from VLA M&C;
:Authenticate & Authorize [SecurityCheck];
note right
ASR-008 / NFR-014 / NFR-015:
mTLS + MFA for privileged actions; deny if CRL check fails.
end note

:Validate config schema;
:TranslateConfig -> ConfigTableSet;
:Persist ConfigTableSet locally;
note right
ASR-009: standalone capable; local persistence.
end note

fork
  :Replicate state/tables to Secondary Master;
  note right
ASR-004: state replication for failover.
end note
fork again
  :Enqueue ApplyConfig event (>=96h retention);
  note right
FR-039: continue processing during comms loss.
end note
end fork

:ApplyConfig to CMIBControllers;
note right
NFR-006/ASR-006: deterministic bounded-latency path.
end note

if (CMIB ack received?) then (yes)
  :Update SystemState;
  :Emit Message (timestamp UTC + wallclock);
  :Spool MonitorSample (<=24h);
else (no)
  :Attempt Self-Heal (reboot/warmBoot);
  if (Recovered?) then (yes)
    :Re-apply config;
  else (no)
    :Issue Alert notice;
  endif
endif

stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_TranslateAndApply
autonumber
actor "VLA M&C" as VLA_MC
participant "VirtualCorrelatorInterface" as VCI
participant "AuthService" as Auth
participant "MasterControlNode" as MasterP
participant "MasterControlNode" as MasterS
database "EventQueue" as Queue
participant "CMIBController" as CMIB
participant "AuditLog" as Audit

VLA_MC -> VCI : SubmitConfig
VCI -> Auth : AuthenticateAuthorize
Auth -> Audit : WriteAudit
Auth --> VCI : Decision(allow)

VCI -> VCI : TranslateConfig
VCI -> MasterP : ApplyConfig(tables)
MasterP -> MasterS : ReplicateState
MasterP -> Queue : EnqueueApplyConfig
note right of Queue
FR-039: >=96h retention for config/control events.
end note

MasterP -> CMIB : ExecuteRegisterWrite/Configure
CMIB --> MasterP : Ack

MasterP -> Audit : WriteAudit
VCI <-- MasterP : Ack
VLA_MC <-- VCI : ConfigApplied
@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_SelfHealAndAlert
autonumber
participant "MasterControlNode" as MasterP
participant "HealthManager" as Health
participant "CMIBController" as CMIB
participant "PowerControlNode" as Power
participant "AuditLog" as Audit
actor "Operator" as Operator

MasterP -> Health : EvaluateHealth
Health -> CMIB : InterrogateHardware
CMIB --> Health : HardwareState

alt faultDetected
  Health -> MasterP : FaultDetected
  MasterP -> CMIB : Reboot(warmBoot=true)
  CMIB --> MasterP : Ack
  MasterP -> Health : EvaluateHealth
  Health -> CMIB : InterrogateHardware
  CMIB --> Health : HardwareState
  alt notRecovered
    MasterP -> Power : RemoteReboot(target=CMIB)
    Power --> MasterP : Ack
    MasterP -> Audit : WriteAudit
    MasterP -> Operator : IssueAlert
  else recovered
    MasterP -> Audit : WriteAudit
  end
else healthy
  MasterP -> Audit : WriteAudit
end
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_TranslateAndApply
skinparam linetype ortho

actor "VLA M&C" as VLA_MC
rectangle "VirtualCorrelatorInterface" as VCI
rectangle "AuthService" as Auth
rectangle "MasterControlNode" as MasterP
rectangle "MasterControlNode" as MasterS
database "EventQueue" as Queue
rectangle "CMIBController" as CMIB
database "AuditLog" as Audit

VLA_MC -- VCI
VCI -- Auth
VCI -- MasterP
MasterP -- MasterS
MasterP -- Queue
MasterP -- CMIB
Auth -- Audit
MasterP -- Audit

VLA_MC -> VCI : 1 SubmitConfig
VCI -> Auth : 2 AuthenticateAuthorize
Auth -> Audit : 3 WriteAudit
VCI -> MasterP : 4 ApplyConfig
MasterP -> MasterS : 5 ReplicateState
MasterP -> Queue : 6 EnqueueApplyConfig
MasterP -> CMIB : 7 Configure
MasterP -> Audit : 8 WriteAudit

note right of VCI
Scenario S1: Translate external configuration and apply to hardware (FR-001/FR-010).
end note
@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_SelfHealAndAlert
skinparam linetype ortho

actor "Operator" as Operator
rectangle "MasterControlNode" as MasterP
rectangle "HealthManager" as Health
rectangle "CMIBController" as CMIB
rectangle "PowerControlNode" as Power
database "AuditLog" as Audit

Operator -- MasterP
MasterP -- Health
Health -- CMIB
MasterP -- CMIB
MasterP -- Power
MasterP -- Audit

MasterP -> Health : 1 EvaluateHealth
Health -> CMIB : 2 InterrogateHardware
Health -> MasterP : 3 FaultDetected
MasterP -> CMIB : 4 Reboot(warmBoot)
MasterP -> Power : 5 RemoteReboot (if needed)
MasterP -> Audit : 6 WriteAudit
MasterP -> Operator : 7 IssueAlert (if not healed)

note right of Health
Scenario S2: Self-heal faults and issue alerts (FR-003/FR-016/FR-017/FR-018).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as P_UI {
  class "ConfigGUI"
  class "TestToolsGUI"
}

package "api" as P_API {
  class "VirtualCorrelatorInterface"
  class "VCIContracts"
}

package "domain" as P_Domain {
  class "ConfigTableSet"
  class "ControlCommand"
  class "SystemState"
  class "Message"
  class "MonitorSample"
}

package "services" as P_Services {
  class "MasterControlNode"
  class "HealthManager"
  class "BackendDataPublisher"
}

package "integrations" as P_Integrations {
  class "CMIBController"
  class "PowerControlNode"
  class "UPSAdapter"
  class "BackendDPAdapter"
}

package "security" as P_Security {
  class "AuthService"
  class "RBACPolicy"
}

package "persistence" as P_Persistence {
  class "SpoolBuffer"
  class "EventQueue"
  class "AuditLog"
}

P_UI ..> P_API : uses
P_API ..> P_Security : uses
P_API ..> P_Services : uses
P_Services ..> P_Domain : uses
P_Services ..> P_Persistence : uses
P_Services ..> P_Integrations : uses
P_Integrations ..> P_Domain : emits/consumes
P_Security ..> P_Persistence : audit

note right of P_API
ASR-002: VCI is the gateway/translation interface.
end note

note right of P_Services
ASR-004/ASR-007/ASR-009: HA master, self-monitoring, offline processing.
end note

note right of P_Integrations
ASR-005/ASR-010: Ethernet links, segmentation, watchdog, CMIB constraints.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

interface "IConfigAPI" as IConfigAPI
interface "IMonitorAPI" as IMonitorAPI
interface "IControlAPI" as IControlAPI
interface "IAuthNAuthZ" as IAuth
interface "IAudit" as IAudit
interface "ICMIBBus" as ICMIB
interface "IBackendData" as IBackend
interface "IPowerControl" as IPower

component "VCI Gateway\n[TranslateConfig]" as C_VCI
component "Master Service (Primary)\n[ControlMonitor]" as C_MasterP
component "Master Service (Secondary)\n[Failover]" as C_MasterS
component "Health Manager\n[SelfHeal]" as C_Health
component "Backend Data Publisher\n[DeliverBackendData]" as C_BackendPub
component "CMIB Adapter\n[Realtime]" as C_CMIB
component "Power Control Adapter\n[RemoteReboot]" as C_Power
component "Auth Service\n[RBAC]" as C_Auth
component "Audit Log Service\n[EncryptedAtRest]" as C_Audit
component "Spool Buffer Store\n[24h]" as C_Spool
component "Event Queue Store\n[96h]" as C_Queue

C_VCI - IConfigAPI
C_VCI - IMonitorAPI
C_VCI - IControlAPI
C_Auth - IAuth
C_Audit - IAudit
C_CMIB - ICMIB
C_BackendPub - IBackend
C_Power - IPower

C_VCI ..> IAuth : requires
C_VCI ..> IAudit : requires
C_VCI ..> C_MasterP : uses

C_MasterP ..> C_MasterS : replicateState
C_MasterP ..> C_Health : uses
C_MasterP ..> C_BackendPub : uses
C_MasterP ..> C_CMIB : uses
C_MasterP ..> C_Power : uses
C_MasterP ..> C_Spool : uses
C_MasterP ..> C_Queue : uses
C_MasterP ..> C_Audit : uses

C_Health ..> C_CMIB : interrogate/reboot
C_Health ..> C_Audit : audit

note right of C_MasterP
ASR-006/NFR-006: deterministic processing path for hardware inputs.
end note

note right of C_Auth
FR-041..FR-050: unique ID, revoke <=15 min, MFA, deny on CRL failure.
end note

note right of C_Spool
FR-013: spool monitor data up to 24h; overrun alert.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam nodeStyle rectangle

node "Operations Network\n(External)" as NET_OPS
node "Control/Monitor Network\n(Internal, segmented NIC)" as NET_CTRL
node "Backend Data Network\n(Secondary virtual network)" as NET_BACK

node "Master Control Node - Primary\n(COTS OS, multi-NIC, watchdog)" as NODE_MasterP {
  artifact "VCI Gateway" as A_VCI
  artifact "Master Service" as A_MasterP
  artifact "Auth Service" as A_Auth
  artifact "Audit Log Service" as A_Audit
  artifact "Spool Buffer Store" as A_Spool
  artifact "Event Queue Store" as A_Queue
  artifact "Backend Data Publisher" as A_BackendPub
  artifact "Health Manager" as A_Health
}

node "Master Control Node - Secondary\n(COTS OS, multi-NIC, watchdog)" as NODE_MasterS {
  artifact "Master Service" as A_MasterS
}

node "Rack Switch\n(Ethernet >=100Mbps, upgradeable >=1Gbps)" as SW_RACK
node "CMIB Rack\n(hot-swappable)" as NODE_RACK {
  node "CMIBController xN\n(near real-time, watchdog)" as NODE_CMIB
}

node "Power Control Node\n(redundant path)" as NODE_Power {
  artifact "Power Control Adapter" as A_Power
}

node "UPS" as NODE_UPS
node "Backend Data Processing System" as NODE_BackendDP
node "VLA Expansion Project M&C" as NODE_VLA

NET_OPS -- NODE_MasterP : mTLS/SSH\n(NFR-015)
NET_OPS -- NODE_MasterS : mTLS/SSH\n(NFR-015)

NODE_VLA -- NET_OPS
NODE_BackendDP -- NET_BACK
NODE_UPS -- NET_CTRL

NODE_MasterP -- NET_CTRL
NODE_MasterS -- NET_CTRL
NODE_MasterP -- NET_BACK
NODE_MasterS -- NET_BACK

NET_CTRL -- SW_RACK
SW_RACK -- NODE_RACK : Ethernet\n(ASR-005)
NODE_MasterP -- NODE_Power : redundant link\n(FR-024)
NODE_Power -- NET_CTRL
NODE_CMIB -- NET_CTRL

NODE_MasterP -- NODE_MasterS : state replication\n(ASR-004)

NODE_MasterP -- NODE_BackendDP : datasets\n(FR-012/ASR-003)\n>99.99% test packets (NFR-005)

note right of NODE_MasterP
NFR-013/ASR-009: standalone boot/run; local persistence.
NFR-009: >=99.99% availability; MTTR <=30 min.
end note

note right of NET_CTRL
NFR-021: segmentation via separate physical interfaces; firewall rules enforced.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
skinparam rectangleStyle rounded
skinparam shadowing false

rectangle "External System: VLA M&C" as EXT_VLA
rectangle "External System: Backend Controller" as EXT_BackendCtrl
rectangle "External System: Backend Data Processing" as EXT_BackendDP
rectangle "External Device: UPS" as EXT_UPS
rectangle "External: Correlator Hardware" as EXT_HW

rectangle "CMCS: VCI Gateway\n[TranslateConfig][AccessGateway]\n(mTLS, RBAC, audit)" as CON_VCI
rectangle "CMCS: Master Service (HA)\n[ControlMonitor][State]\n(primary/secondary)" as CON_Master
rectangle "CMCS: Health Manager\n[SelfHeal][Alerts]" as CON_Health
rectangle "CMCS: CMIB Adapter\n[Realtime][Deterministic]" as CON_CMIB
rectangle "CMCS: Backend Data Publisher\n[DeliverBackendData]\n(secondary network)" as CON_BackendPub
rectangle "CMCS: Power Control Adapter\n[RemoteReboot]\n(redundant path)" as CON_Power

database "CMCS: Audit Log Store\n[EncryptedAtRest]\n(retain 1y)" as DB_Audit
database "CMCS: Spool Buffer Store\n[24h Monitor Spool]" as DB_Spool
database "CMCS: Event Queue Store\n[96h Control Queue]" as DB_Queue
rectangle "CMCS: Auth Service\n[RBAC][MFA][Cert]\n(revoke<=15min)" as CON_Auth

EXT_VLA --> CON_VCI : config/control/monitor
EXT_BackendCtrl --> CON_VCI : sampling control
CON_VCI --> CON_Auth : authenticate/authorize
CON_VCI --> DB_Audit : audit access
CON_VCI --> CON_Master : applyConfig/control/query

CON_Master --> DB_Queue : enqueue/dequeue
CON_Master --> DB_Spool : spool monitor
CON_Master --> DB_Audit : audit actions
CON_Master --> CON_Health : health events
CON_Health --> CON_CMIB : interrogate/reboot
CON_Master --> CON_CMIB : realtime control/monitor
CON_Master --> CON_Power : remote reboot
CON_Master --> CON_BackendPub : publish datasets

CON_BackendPub --> EXT_BackendDP : datasets over secondary network
CON_CMIB --> EXT_HW : CMIB bus / registers
EXT_UPS --> CON_Master : power events

note right of CON_CMIB
ASR-006/NFR-006: bounded latency processing to avoid data loss/corruption/overflows.
end note

note right of CON_VCI
ASR-002: all use through VCI or Master; VCI is gateway/translation interface.
end note

note bottom of DB_Audit
FR-042/NFR-014: audit fields include action type, timestamp, actor, outcome; encrypted volume.
end note
@enduml
```