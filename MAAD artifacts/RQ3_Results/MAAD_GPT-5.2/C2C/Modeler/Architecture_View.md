## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction
skinparam packageStyle rectangle

actor "MapUser" as MapUser
actor "IncidentOperator" as IncidentOperator
actor "RemoteControlOperator" as RemoteControlOperator
actor "IncidentAdmin" as IncidentAdmin
actor "ExternalTrafficSystem" as ExternalTrafficSystem
actor "PeerCenter" as PeerCenter
actor "NCTCOGGeoData" as NCTCOGGeoData

rectangle "Center-to-Center System" as C2C {
  usecase "ViewMap" as UC_ViewMap
  usecase "ViewIncidents" as UC_ViewIncidents
  usecase "IncidentDrilldown" as UC_IncidentDrilldown
  usecase "EnterIncident" as UC_EnterIncident
  usecase "EnterLaneClosure" as UC_EnterLaneClosure
  usecase "ModifyIncident" as UC_ModifyIncident
  usecase "DeleteIncident" as UC_DeleteIncident
  usecase "IssueDeviceCommand" as UC_IssueDeviceCommand
  usecase "ViewDeviceStatus" as UC_ViewDeviceStatus
  usecase "SyncRepositories" as UC_SyncRepositories
  usecase "AuthenticateUser" as UC_AuthenticateUser
  usecase "AuthorizeAction" as UC_AuthorizeAction
}

MapUser --> UC_ViewMap
MapUser --> UC_ViewIncidents
MapUser --> UC_IncidentDrilldown

IncidentOperator --> UC_EnterIncident
IncidentOperator --> UC_EnterLaneClosure
IncidentOperator --> UC_ModifyIncident
IncidentOperator --> UC_ViewIncidents

IncidentAdmin --> UC_DeleteIncident

RemoteControlOperator --> UC_IssueDeviceCommand
RemoteControlOperator --> UC_ViewDeviceStatus

ExternalTrafficSystem --> UC_ViewDeviceStatus
ExternalTrafficSystem --> UC_ViewIncidents

PeerCenter --> UC_ViewDeviceStatus
PeerCenter --> UC_IssueDeviceCommand
PeerCenter --> UC_SyncRepositories

NCTCOGGeoData --> UC_ViewMap

UC_ViewMap ..> UC_ViewDeviceStatus : <<include>>
UC_ViewMap ..> UC_ViewIncidents : <<include>>
UC_IncidentDrilldown ..> UC_AuthorizeAction : <<include>>
UC_IncidentDrilldown ..> UC_ViewIncidents : <<extend>>

UC_EnterIncident ..> UC_AuthenticateUser : <<include>>
UC_EnterLaneClosure ..> UC_AuthenticateUser : <<include>>
UC_ModifyIncident ..> UC_AuthenticateUser : <<include>>
UC_DeleteIncident ..> UC_AuthenticateUser : <<include>>
UC_DeleteIncident ..> UC_AuthorizeAction : <<include>>

UC_IssueDeviceCommand ..> UC_AuthenticateUser : <<include>>
UC_IssueDeviceCommand ..> UC_AuthorizeAction : <<include>>
UC_ViewDeviceStatus ..> UC_AuthenticateUser : <<include>>

note right of C2C
assumption: "ExternalTrafficSystem" represents any connected legacy TMC system via adapters (ASR-001).
assumption: "PeerCenter" represents another center consuming status and issuing control (FR-005..FR-028, FR-035..FR-037).
assumption: Incident drill-down requires 'IncidentViewer' claim (FR-045).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class Network <<persisted>> {
  +networkId: String
  +name: String
  +getTopology(): Topology
}

class Topology <<persisted>> {
  +topologyId: String
  +networkId: String
  +getLinks(): List<Link>
  +getNodes(): List<Node>
}

class Link <<persisted>> {
  +linkId: String
  +name: String
  +type: String
  +speedKph: Integer
}

class Node <<persisted>> {
  +nodeId: String
  +name: String
  +typeDescription: String
}

class Incident <<persisted>> {
  +incidentId: String
  +networkId: String
  +description: String
  +roadway: String
  +geo: String
  +timestamp: String
  +impact: String
  +create(): void
  +update(): void
  +delete(): void
}

class LaneClosure <<persisted>> {
  +laneClosureId: String
  +networkId: String
  +description: String
  +create(): void
  +delete(): void
}

abstract class Device <<persisted>> {
  +deviceId: String
  +networkId: String
  +name: String
  +location: String
  +status: String
  +getStatus(): String
}

class DMS <<persisted>> {
  +beaconsOn: Boolean
}

class LCS <<persisted>> {
  +laneAssignment: String
}

class CCTV <<persisted>> {
  +videoChannelInputId: String
}

class DeviceCommand <<persisted>> {
  +commandId: String
  +networkId: String
  +deviceType: String
  +deviceId: String
  +operation: String
  +payload: String
  +requestedBy: String
  +requestedAt: String
  +status: String
  +validate(): Boolean
}

class CommandTimeframe <<persisted>> {
  +networkId: String
  +deviceType: String
  +daysAccepted: String[*]
  +timesAccepted: String[*]
}

class UserAccount <<persisted>> {
  +userId: String
  +username: String
  -passwordHash: String
  +mfaEnabled: Boolean
  +lockedUntil: String
  +verifyPassword(password: String): Boolean
  +isLocked(): Boolean
}

class AuthSession <<persisted>> {
  +sessionId: String
  +userId: String
  +issuedAt: String
  +expiresAt: String
  +claims: String[*]
}

class AuditEvent <<immutable>> {
  +eventId: String
  +timestamp: String
  +type: String
  +userId: String
  +action: String
  +targetId: String
  +details: String
  +hashPrev: String
  +hashThis: String
}

class TrafficRepository <<persisted>> {
  +saveIncident(i: Incident): void
  +saveLaneClosure(lc: LaneClosure): void
  +saveDevice(d: Device): void
  +saveCommand(cmd: DeviceCommand): void
  +queryIncidents(networkId: String): List<Incident>
  +queryDeviceStatus(networkId: String, deviceType: String): List<Device>
}

interface IExternalTrafficSystemAdapter {
  +connect(): void
  +pullUpdates(): void
  +pushCommand(cmd: DeviceCommand): void
}

class TMDDCodec {
  +encode(message: String): String
  +decode(payload: String): String
  +validateSchema(payload: String): Boolean
  +negotiateVersion(peer: String): String
}

class SecurityGateway {
  +enforceTlsMutual(): void
  +redactSecrets(input: String): String
  +authorize(claim: String, session: AuthSession): Boolean
}

Network "1" o-- "1" Topology
Topology "1" *-- "0..*" Link
Topology "1" *-- "0..*" Node

Network "1" o-- "0..*" Incident
Network "1" o-- "0..*" LaneClosure
Network "1" o-- "0..*" Device
Network "1" o-- "0..*" CommandTimeframe

Device <|-- DMS
Device <|-- LCS
Device <|-- CCTV

DeviceCommand "0..*" --> "1" Device : targets
UserAccount "1" --> "0..*" AuthSession
UserAccount "1" --> "0..*" AuditEvent
TrafficRepository "1" --> "0..*" AuditEvent : writes

IExternalTrafficSystemAdapter ..> TMDDCodec : uses
SecurityGateway ..> UserAccount : verifies
SecurityGateway ..> AuditEvent : logs
TrafficRepository ..> SecurityGateway : uses

note right of TMDDCodec
NFR-001/002/003/013/ASR-004:
TMDD v3.0+ over DATEX/ASN v1.5 over TCP/IP with TLS 1.2+.
Schema validation + version negotiation at session start.
end note

note right of SecurityGateway
NFR-004/NFR-006/ASR-008:
- Password min 12, lockout 5 attempts/30 min
- bcrypt/scrypt hashes
- MFA enforced when enabled
- mTLS for password-field APIs
- audit logs must never contain password
end note

note bottom of TrafficRepository
ASR-003: relational repository (PostgreSQL/MySQL),
indexed by networkId, deviceId, timestamp.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView
skinparam classAttributeIconSize 0

object "net1:Network [ViewMap]" as net1 {
  networkId = "N-DFW-01"
  name = "DFW Core"
}

object "topo1:Topology [ViewMap]" as topo1 {
  topologyId = "T-001"
  networkId = "N-DFW-01"
}

object "link1:Link [ColorCodeLinks]" as link1 {
  linkId = "L-635E-12"
  name = "I-635 EB"
  type = "INTERSTATE"
  speedKph = 42
}

object "inc1:Incident [ViewIncidents]" as inc1 {
  incidentId = "INC-2026-0312-001"
  networkId = "N-DFW-01"
  description = "Crash blocking right lane"
  roadway = "I-635 EB"
  geo = "32.909,-96.770"
  timestamp = "2026-03-12T14:05:00Z"
  impact = "MAJOR"
}

object "user1:UserAccount [AuthenticateUser]" as user1 {
  userId = "U-1007"
  username = "remote.operator"
  mfaEnabled = true
  lockedUntil = ""
}

object "sess1:AuthSession [AuthenticateUser]" as sess1 {
  sessionId = "S-abc123"
  userId = "U-1007"
  issuedAt = "2026-03-12T14:10:00Z"
  expiresAt = "2026-03-12T16:10:00Z"
  claims = "{DeviceController,IncidentViewer}"
}

object "dms1:DMS [ViewDeviceStatus]" as dms1 {
  deviceId = "DMS-77"
  networkId = "N-DFW-01"
  name = "DMS I-635@Coit"
  location = "I-635 EB @ Coit Rd"
  status = "ONLINE"
  beaconsOn = false
}

object "cmd1:DeviceCommand [IssueDeviceCommand]" as cmd1 {
  commandId = "CMD-9001"
  networkId = "N-DFW-01"
  deviceType = "DMS"
  deviceId = "DMS-77"
  operation = "DISPLAY_MESSAGE"
  payload = "{text:'CRASH AHEAD',beacons:true}"
  requestedBy = "remote.operator"
  requestedAt = "2026-03-12T14:12:00Z"
  status = "PENDING"
}

net1 o-- topo1
topo1 *-- link1
net1 o-- inc1
net1 o-- dms1
user1 --> sess1
cmd1 --> dms1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_DeviceCommandLifecycle
hide empty description

state "DeviceCommand Lifecycle" as DCL {

  [*] --> Draft : create

  Draft --> Validated : validate [schemaOk && timeframeOk]\n/ redactSecrets()
  Draft --> Rejected : validate [!schemaOk || !timeframeOk]\n/ audit("REJECTED")

  Validated --> Sent : send\n/ enforceTlsMutual()
  Sent --> Pending : ackReceived [status=="PENDING"]
  Sent --> Succeeded : ackReceived [status=="SUCCESS"]\n/ audit("SUCCESS")
  Sent --> Failed : ackReceived [status=="FAILED"]\n/ audit("FAILED")

  Pending --> Succeeded : statusUpdate [status=="SUCCESS"]\n/ audit("SUCCESS")
  Pending --> Failed : statusUpdate [status=="FAILED"]\n/ audit("FAILED")
  Pending --> Failed : timeout [elapsed>2s after reply]\n/ audit("TIMEOUT")

  Rejected --> [*]
  Succeeded --> [*]
  Failed --> [*]
}

note right of DCL
FR-070: display SUCCESS/FAILED/PENDING or error within 2s of reply.
NFR-006: never log password; mTLS required for password-field messages.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_RemoteDeviceCommand
skinparam activityStyle rounded

start
:Launch Remote Control GUI;
:Prompt username/password [SecurityCheck];
:POST /auth/login over HTTPS/TLS [SecurityCheck];

if (Password >= 12 chars?) then (yes)
  :Verify bcrypt/scrypt hash [SecurityCheck];
else (no)
  :Reject + AuditEvent (no password logged);
  stop
endif

if (Failed attempts >= 5?) then (yes)
  :Lock account 30 min + AuditEvent;
  stop
else (no)
endif

if (MFA enabled?) then (yes)
  :Perform MFA challenge [SecurityCheck];
  if (MFA ok?) then (yes)
  else (no)
    :Reject + AuditEvent;
    stop
  endif
else (no)
endif

:Select networkId;
:Select deviceType + deviceId;
:Enter command payload;

:Validate schema + timeframe [ContractCheck];
:Enforce mutual TLS for command endpoint [SecurityCheck];

fork
  :Send DeviceCommand to C2C API;
fork again
  :Write AuditEvent (username only);
end fork

:Receive command status reply;
note right
FR-070: show SUCCESS/FAILED/PENDING or error within 2s of reply.
end note
:Display status in scrollable list;

stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_IssueDeviceCommand
title S1: IssueDeviceCommand (RemoteControlOperator -> DMS) [FR-056..FR-070, FR-005, NFR-004, NFR-006, ASR-008]

actor RemoteControlOperator as RemoteControlOperator
participant "RemoteControlGUI" as RemoteControlGUI
participant "SecurityGateway" as SecurityGateway
participant "CommandController" as CommandController
participant "TMDDCodec" as TMDDCodec
database "TrafficRepository" as TrafficRepository
participant "AdapterBroker" as AdapterBroker
participant "ExternalTrafficSystemAdapter" as ExternalTrafficSystemAdapter

RemoteControlOperator -> RemoteControlGUI : login()
RemoteControlGUI -> SecurityGateway : authenticateUser(username,password)
note right of SecurityGateway
- min 12 chars
- lockout 5/30min
- bcrypt/scrypt verify
- MFA if enabled
end note
SecurityGateway --> RemoteControlGUI : authSession(claims)

RemoteControlOperator -> RemoteControlGUI : submitCommand(networkId,dmsId,payload)
RemoteControlGUI -> CommandController : issueDeviceCommand(session,cmd)
CommandController -> SecurityGateway : authorizeAction("DeviceController",session)
SecurityGateway --> CommandController : authorized

CommandController -> TMDDCodec : validateSchema(cmd)
TMDDCodec --> CommandController : schemaOk

CommandController -> SecurityGateway : enforceTlsMutual()
SecurityGateway --> CommandController : tlsOk

CommandController -> TrafficRepository : saveCommand(cmd{status=PENDING})
CommandController -> TrafficRepository : appendAuditEvent(usernameOnly)

CommandController -> TMDDCodec : encode(TMDD/DATEXASN)
TMDDCodec --> CommandController : payload

CommandController -> AdapterBroker : routeToAdapter(networkId,deviceType)
AdapterBroker -> ExternalTrafficSystemAdapter : pushCommand(payload)
ExternalTrafficSystemAdapter --> AdapterBroker : ack(status)
AdapterBroker --> CommandController : ack(status)

CommandController -> TrafficRepository : updateCommandStatus(status)
CommandController --> RemoteControlGUI : commandStatus(status,errorMessage?)
RemoteControlGUI --> RemoteControlOperator : displayStatus()

note over RemoteControlGUI
FR-070: display within 2s of reply.
end note
@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_ViewMapAndIncidents
title S2: ViewMap + IncidentDrilldown (MapUser) [FR-039..FR-047, FR-045, NFR-005, NFR-007, NFR-008]

actor MapUser as MapUser
participant "WebMapUI" as WebMapUI
participant "MapController" as MapController
participant "SecurityGateway" as SecurityGateway
participant "MapRenderService" as MapRenderService
database "TrafficRepository" as TrafficRepository
participant "NCTCOGGeoDataClient" as NCTCOGGeoDataClient

MapUser -> WebMapUI : openMap()
WebMapUI -> MapController : loadMap(viewport,zoom)
MapController -> NCTCOGGeoDataClient : fetchBasemapTiles(viewport,zoom)
NCTCOGGeoDataClient --> MapController : basemap

MapController -> TrafficRepository : queryLinkSpeeds(networkId)
TrafficRepository --> MapController : linkSpeeds
MapController -> MapRenderService : colorCodeLinks(linkSpeeds,thresholdsYaml)
MapRenderService --> MapController : styledLinks

MapController -> TrafficRepository : queryIncidents(networkId)
TrafficRepository --> MapController : incidents
MapController --> WebMapUI : renderMap(basemap,styledLinks,incidentIcons)

MapUser -> WebMapUI : clickIncident(incidentId)
WebMapUI -> MapController : incidentDrilldown(incidentId,session)
MapController -> SecurityGateway : authorizeAction("IncidentViewer",session)
alt authorized
  SecurityGateway --> MapController : authorized
  MapController -> TrafficRepository : getIncidentDetails(incidentId)
  TrafficRepository --> MapController : incidentDetails
  MapController --> WebMapUI : showDialog(details)
else denied
  SecurityGateway --> MapController : denied
  MapController --> WebMapUI : showAccessDenied()
end
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_IssueDeviceCommand
title Collaboration S1: IssueDeviceCommand

object RemoteControlOperator
object RemoteControlGUI
object SecurityGateway
object CommandController
object TMDDCodec
object TrafficRepository
object AdapterBroker
object ExternalTrafficSystemAdapter

RemoteControlOperator -- RemoteControlGUI
RemoteControlGUI -- SecurityGateway
RemoteControlGUI -- CommandController
CommandController -- TMDDCodec
CommandController -- TrafficRepository
CommandController -- AdapterBroker
AdapterBroker -- ExternalTrafficSystemAdapter

RemoteControlOperator -> RemoteControlGUI : 1 login()
RemoteControlGUI -> SecurityGateway : 2 authenticateUser()
SecurityGateway -> RemoteControlGUI : 3 authSession()
RemoteControlOperator -> RemoteControlGUI : 4 submitCommand()
RemoteControlGUI -> CommandController : 5 issueDeviceCommand()
CommandController -> SecurityGateway : 6 authorizeAction()
CommandController -> TMDDCodec : 7 validateSchema()
CommandController -> TrafficRepository : 8 saveCommand()+audit()
CommandController -> TMDDCodec : 9 encode()
CommandController -> AdapterBroker : 10 routeToAdapter()
AdapterBroker -> ExternalTrafficSystemAdapter : 11 pushCommand()
ExternalTrafficSystemAdapter -> AdapterBroker : 12 ack()
AdapterBroker -> CommandController : 13 ack()
CommandController -> TrafficRepository : 14 updateStatus()
CommandController -> RemoteControlGUI : 15 commandStatus()
RemoteControlGUI -> RemoteControlOperator : 16 displayStatus()

note right of CommandController
Origin: FR-005 + FR-056..FR-070
Constraints: NFR-004 auth, NFR-006 redaction+mTLS
end note
@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_ViewMapAndIncidents
title Collaboration S2: ViewMapAndIncidents

object MapUser
object WebMapUI
object MapController
object NCTCOGGeoDataClient
object TrafficRepository
object MapRenderService
object SecurityGateway

MapUser -- WebMapUI
WebMapUI -- MapController
MapController -- NCTCOGGeoDataClient
MapController -- TrafficRepository
MapController -- MapRenderService
MapController -- SecurityGateway

MapUser -> WebMapUI : 1 openMap()
WebMapUI -> MapController : 2 loadMap()
MapController -> NCTCOGGeoDataClient : 3 fetchBasemapTiles()
MapController -> TrafficRepository : 4 queryLinkSpeeds()
MapController -> MapRenderService : 5 colorCodeLinks()
MapController -> TrafficRepository : 6 queryIncidents()
MapController -> WebMapUI : 7 renderMap()

MapUser -> WebMapUI : 8 clickIncident()
WebMapUI -> MapController : 9 incidentDrilldown()
MapController -> SecurityGateway : 10 authorizeAction(IncidentViewer)
MapController -> TrafficRepository : 11 getIncidentDetails()
MapController -> WebMapUI : 12 showDialog()/deny

note right of MapController
Origin: FR-039..FR-047, FR-045
Constraints: NFR-007 basemap source, NFR-008 thresholds YAML, RBAC for drilldown
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as pkg_ui {
  note bottom
  WebMapUI (ESRI ARC IMS) + IncidentGUI/RemoteControlGUI (ESRI Map Objects)
  Constraints: ASR-007, NFR-014, NFR-016
  end note
}

package "api" as pkg_api {
  note bottom
  Controllers for status, incidents, commands, auth
  Enforce TLS/mTLS + RBAC
  end note
}

package "kernel" as pkg_kernel {
  note bottom
  Microkernel runtime: plugin loading, config, gatekeeping
  ASR-005 building blocks; startup checks
  end note
}

package "domain" as pkg_domain {
  note bottom
  Canonical ITS/TMDD domain model
  end note
}

package "persistence" as pkg_persist {
  note bottom
  Relational repository + indexes + audit log
  ASR-003
  end note
}

package "integration" as pkg_integ {
  note bottom
  Adapters implementing IExternalTrafficSystemAdapter
  TMDD/DATEXASN codec + version negotiation
  ASR-001/004
  end note
}

package "security" as pkg_sec {
  note bottom
  AuthN/AuthZ, MFA, redaction, mTLS enforcement
  NFR-004/NFR-006/ASR-008
  end note
}

pkg_ui ..> pkg_api
pkg_api ..> pkg_sec
pkg_api ..> pkg_domain
pkg_api ..> pkg_persist
pkg_kernel ..> pkg_integ
pkg_integ ..> pkg_domain
pkg_integ ..> pkg_sec
pkg_persist ..> pkg_domain
pkg_api ..> pkg_kernel

note right of pkg_kernel
Platform constraints: Windows Server 2019+ certified (NFR-012),
core modules in C/C++ (NFR-015).
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

interface "IAuthAPI" as IAuthAPI
interface "IIncidentAPI" as IIncidentAPI
interface "IDeviceStatusAPI" as IDeviceStatusAPI
interface "IDeviceCommandAPI" as IDeviceCommandAPI
interface "IAdapterPlugin" as IAdapterPlugin
interface "ITMDDCodec" as ITMDDCodec
interface "ITrafficRepository" as ITrafficRepository

component "WebMapUI\n[ViewMap]" as WebMapUI
component "IncidentGUI\n[EnterIncident]" as IncidentGUI
component "RemoteControlGUI\n[IssueDeviceCommand]" as RemoteControlGUI

component "API Gateway\n[HTTPS/mTLS]" as APIGateway
component "AuthService\n[AuthenticateUser]" as AuthService
component "IncidentService\n[ViewIncidents]" as IncidentService
component "DeviceStatusService\n[ViewDeviceStatus]" as DeviceStatusService
component "DeviceCommandService\n[IssueDeviceCommand]" as DeviceCommandService
component "MapService\n[RenderMap]" as MapService

component "MicrokernelRuntime\n[BuildingBlocks]" as MicrokernelRuntime
component "AdapterBroker\n[RouteAdapter]" as AdapterBroker
component "ExternalTrafficSystemAdapter\n[Plugin]" as ExternalTrafficSystemAdapter
component "TMDDCodec\n[DATEX/ASN]" as TMDDCodec

database "TrafficRepositoryDB\n[Relational]" as TrafficRepositoryDB
component "AuditLog\n[HashChained]" as AuditLog

APIGateway - IAuthAPI
APIGateway - IIncidentAPI
APIGateway - IDeviceStatusAPI
APIGateway - IDeviceCommandAPI

AuthService ..|> IAuthAPI
IncidentService ..|> IIncidentAPI
DeviceStatusService ..|> IDeviceStatusAPI
DeviceCommandService ..|> IDeviceCommandAPI

TMDDCodec ..|> ITMDDCodec
ExternalTrafficSystemAdapter ..|> IAdapterPlugin

TrafficRepositoryDB - ITrafficRepository
AuditLog ..> TrafficRepositoryDB : stores

WebMapUI ..> APIGateway
IncidentGUI ..> APIGateway
RemoteControlGUI ..> APIGateway

IncidentService ..> ITrafficRepository
DeviceStatusService ..> ITrafficRepository
DeviceCommandService ..> ITrafficRepository
MapService ..> ITrafficRepository

DeviceStatusService ..> AdapterBroker
DeviceCommandService ..> AdapterBroker
AdapterBroker ..> IAdapterPlugin
AdapterBroker ..> ITMDDCodec
ExternalTrafficSystemAdapter ..> ITMDDCodec

MicrokernelRuntime ..> AdapterBroker
MicrokernelRuntime ..> ExternalTrafficSystemAdapter : loads
MicrokernelRuntime ..> TMDDCodec : configures

note right of APIGateway
NFR-003/NFR-006: TLS 1.2+; mTLS for password-field endpoints; fail-closed.
end note

note bottom of MicrokernelRuntime
ASR-005: multi-instance building blocks via configuration.
Startup gatekeeping: Windows/ESRI/DATEX runtime presence.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam componentStyle rectangle

node "Public Internet" as Internet

node "Remote Operator PC\n(Windows)\n[Public Network]" as RemotePC {
  artifact "RemoteControlGUI.exe" as RemoteExe
}

node "Map User Browser" as Browser {
  artifact "WebMapUI (HTML/JS)" as WebClient
}

node "C2C DMZ\nWindows Server 2019+\n[IIS/ReverseProxy]" as DMZ {
  artifact "API Gateway" as ApiGw
}

node "C2C App Tier\nWindows Server 2019+\n[C/C++ Services]" as AppTier {
  artifact "AuthService" as AuthSvc
  artifact "IncidentService" as IncSvc
  artifact "DeviceStatusService" as DevStatSvc
  artifact "DeviceCommandService" as DevCmdSvc
  artifact "MapService" as MapSvc
  artifact "MicrokernelRuntime" as Kernel
  artifact "AdapterBroker" as Broker
  artifact "TMDDCodec + DATEX/ASN runtime v1.7.0" as Codec
  artifact "ExternalTrafficSystemAdapter(s)" as Adapters
}

database "TrafficRepositoryDB\n(PostgreSQL/MySQL)\n[Indexed]" as DB

node "ESRI Map Server\nARC IMS 10.2" as EsriArcIMS {
  artifact "MapRenderService" as EsriRender
}

node "NCTCOG GeoData Warehouse\n[Basemap Source]" as NCTCOG

node "External Traffic System(s)\nLegacy/Peer Centers" as ExtSystems

Internet -- RemotePC
Internet -- Browser
Internet -- DMZ

RemotePC --> DMZ : HTTPS/TLS 1.2+\n(mTLS for commands)
Browser --> DMZ : HTTPS/TLS 1.2+

DMZ --> AppTier : internal TLS
AppTier --> DB : JDBC/ODBC (internal)
AppTier --> EsriArcIMS : LAN
EsriArcIMS --> NCTCOG : data feed

AppTier --> ExtSystems : TCP/IP + TLS 1.2+\nTMDD/DATEXASN

note right of AppTier
ASR-006: regional->parent sync every 10 min, batch 1000, LWW by timestamp.
end note

note bottom of DB
ASR-003: relational repository; indexes on networkId, deviceId, timestamp.
NFR-010/011: test-mode logging with <=10% median latency overhead.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
skinparam rectangleStyle rounded
left to right direction

rectangle "RemoteControlGUI\n[IssueDeviceCommand]\nC/C++ + ESRI Map Objects" as C_RemoteGUI
rectangle "IncidentGUI\n[EnterIncident]\nC/C++ + ESRI Map Objects" as C_IncidentGUI
rectangle "WebMapUI\n[ViewMap]\nServed via WWW" as C_WebMapUI

rectangle "API Gateway\n[HTTPS/mTLS]\nTLS 1.2+ fail-closed" as C_ApiGateway
rectangle "C2C Core Services\n[Microkernel]\nC/C++" as C_Core
rectangle "Adapter Plugins\n[IExternalTrafficSystemAdapter]\nC/C++" as C_Adapters
rectangle "TMDD/DATEXASN Codec\n[Standards]\nDATEX/ASN runtime v1.7.0" as C_Codec

database "TrafficRepositoryDB\n[Relational]\nIndexed + TMDD canonical fields" as C_DB
rectangle "Audit Log\n[Hash-chained]\nNo passwords" as C_Audit

rectangle "ESRI ARC IMS Map Server\n[RenderMapImages]" as C_Esri
rectangle "NCTCOG GeoData Warehouse\n[Basemap]" as C_NCTCOG
rectangle "External Traffic Systems / Peer Centers\n[TMDD/DATEXASN]" as C_External

C_RemoteGUI --> C_ApiGateway : device commands\n(username/password)\n(mTLS)
C_IncidentGUI --> C_ApiGateway : incident/lane closure CRUD\n(HTTPS)
C_WebMapUI --> C_ApiGateway : map overlays/incidents\n(HTTPS)

C_ApiGateway --> C_Core : route requests
C_Core --> C_DB : read/write
C_Core --> C_Audit : append events
C_Audit --> C_DB : persist

C_Core --> C_Adapters : route command/status
C_Adapters --> C_Codec : encode/decode + validate
C_Adapters --> C_External : TCP/IP + TLS\nTMDD/DATEXASN

C_Core --> C_Esri : request map render
C_Esri --> C_NCTCOG : basemap source

note right of C_ApiGateway
NFR-004: password policy, lockout, MFA.
NFR-006: redact secrets; audit logs never include password.
end note

note bottom of C_Esri
NFR-014: ESRI ARC IMS 10.2 constraint.
end note
@enduml
```