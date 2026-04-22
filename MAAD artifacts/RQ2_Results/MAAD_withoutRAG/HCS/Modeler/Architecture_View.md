## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml DigitalHome_UseCase
left to right direction
skinparam packageStyle rectangle

actor EndUser
actor MasterUser
actor Technician
actor "ISP/Internet" as ISP

rectangle "DigitalHome System" {
  usecase "Authenticate" as UC_Auth
  usecase "Monitor Environment" as UC_Monitor
  usecase "Control Environment" as UC_Control
  usecase "Manage Plans" as UC_Plans
  usecase "Override Settings" as UC_Override
  usecase "View Reports" as UC_Reports
  usecase "Manage Accounts" as UC_Accounts
  usecase "Configure System" as UC_Config
  usecase "Backup/Restore" as UC_Backup
  usecase "Handle Errors" as UC_Errors
}

EndUser --> UC_Auth
EndUser --> UC_Monitor
EndUser --> UC_Control
EndUser --> UC_Plans
EndUser --> UC_Override
EndUser --> UC_Reports

MasterUser --> UC_Auth
MasterUser --> UC_Accounts
MasterUser --> UC_Config
MasterUser --> UC_Reports

Technician --> UC_Auth
Technician --> UC_Config
Technician --> UC_Backup
Technician --> UC_Reports

UC_Monitor ..> UC_Auth : <<include>>
UC_Control ..> UC_Auth : <<include>>
UC_Plans ..> UC_Auth : <<include>>
UC_Override ..> UC_Auth : <<include>>
UC_Reports ..> UC_Auth : <<include>>
UC_Accounts ..> UC_Auth : <<include>>
UC_Config ..> UC_Auth : <<include>>
UC_Backup ..> UC_Auth : <<include>>

UC_Control ..> UC_Override : <<extend>>
UC_Plans ..> UC_Override : <<extend>>

UC_Monitor ..> UC_Errors : <<include>>
UC_Control ..> UC_Errors : <<include>>
UC_Plans ..> UC_Errors : <<include>>
UC_Reports ..> UC_Errors : <<include>>
UC_Config ..> UC_Errors : <<include>>
UC_Backup ..> UC_Errors : <<include>>

ISP -- UC_Monitor
ISP -- UC_Control

note right of UC_Override
maps: FR-011/012/019/025/027
precedence: Manual > Planned > Default
end note

note right of UC_Monitor
maps: FR-001A, FR-006
NFR-001: UI <=2s
NFR-002: acquisition >=10Hz
end note

note right of UC_Auth
maps: FR-002A/002B, FR-003D, FR-032/033/034
NFR-008/ASR-006 TLS+Audit
end note

note "assumption: 'user' in FRs corresponds to EndUser unless role-specific (MasterUser/Technician) is stated." as A1
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml DigitalHome_Class
skinparam classAttributeIconSize 0

class UserAccount <<persisted>> {
  -id : int
  -username : string
  -role : UserRole
  -dateCreatedUtc : datetime
  +authenticate(password : string) : AuthSession
}

enum UserRole {
  GENERAL
  MASTER
  TECHNICIAN
}

class UserProfile <<persisted>> {
  -id : int
  -userId : int
  -tempUnits : TempUnits
  +setTempUnits(units : TempUnits) : void
}

enum TempUnits {
  C
  F
}

class Device <<persisted>> {
  -deviceId : string
  -deviceType : DeviceType
  -location : string
  -online : boolean
  +getStatus() : DeviceStatus
}

enum DeviceType {
  THERMOSTAT
  HUMIDISTAT
  CONTACT_SENSOR
  POWER_SWITCH
  ALARM_LIGHT
  ALARM_SOUND
}

class TelemetrySample <<persisted>> {
  -sampleId : string
  -deviceId : string
  -metric : string
  -value : decimal
  -timestampUtc : datetime
}

class Plan <<persisted>> {
  -planId : string
  -month : int
  -year : int
  -ownerUserId : int
  +getPeriodSetting(date : date, period : int, metric : string, deviceId : string) : decimal
  +setPeriodSetting(date : date, period : int, metric : string, deviceId : string, value : decimal) : void
}

class OverrideSetting <<persisted>> {
  -overrideId : string
  -deviceId : string
  -metric : string
  -value : decimal
  -source : OverrideSource
  -effectiveFromUtc : datetime
  -effectiveUntilUtc : datetime
  +isActive(nowUtc : datetime) : boolean
}

enum OverrideSource {
  WEBSITE
  MANUAL_DEVICE
}

class ControlCommand <<immutable>> {
  +commandId : string
  +deviceId : string
  +metric : string
  +value : decimal
  +issuedAtUtc : datetime
  +issuedByUserId : int
}

class AlarmIncident <<persisted>> {
  -incidentId : string
  -sensorId : string
  -activatedAtUtc : datetime
  -type : string
}

class AuditEvent <<persisted>> {
  -eventId : string
  -timestampUtc : datetime
  -userId : int
  -role : UserRole
  -action : string
  -target : string
  -status : string
}

class HomeDatabase <<persisted>> {
  +saveTelemetry(sample : TelemetrySample) : void
  +saveCommand(cmd : ControlCommand) : void
  +saveAudit(event : AuditEvent) : void
  +saveIncident(incident : AlarmIncident) : void
  +queryReport(month : int, year : int) : Report
}

class Report {
  +toCsv() : bytes
  +toPdf() : bytes
}

class DeviceRegistry <<persisted>> {
  +registerDevice(device : Device) : void
  +listDevices() : List<Device>
  +getDevice(deviceId : string) : Device
}

class ArbitrationEngine {
  +resolveSetpoint(deviceId : string, metric : string, nowUtc : datetime) : decimal
  +applyOverride(cmd : ControlCommand, plan : Plan) : OverrideSetting
}

UserAccount "1" o-- "0..1" UserProfile
UserAccount "1" -- "0..*" Plan
DeviceRegistry "1" o-- "0..*" Device
Device "1" -- "0..*" TelemetrySample
Plan "1" -- "0..*" OverrideSetting
Device "1" -- "0..*" OverrideSetting
HomeDatabase "1" o-- "0..*" TelemetrySample
HomeDatabase "1" o-- "0..*" AuditEvent
HomeDatabase "1" o-- "0..*" AlarmIncident

ArbitrationEngine ..> Plan
ArbitrationEngine ..> OverrideSetting
ArbitrationEngine ..> ControlCommand
ArbitrationEngine ..> DeviceRegistry

note right of TelemetrySample
ASR-002/NFR-002: acquisition >=10Hz
timestamps in UTC ISO-8601 for reporting
end note

note right of AuditEvent
NFR-008/ASR-006: retain >=1y
ingest SLO: 99% within 5s
schema: {event_id,timestamp,user_id,role,action,target,status}
end note

note right of ControlCommand
FR-009/017 constraints validated in services:
thermostat 60..80 step 1
humidistat 30..60 step 1
end note

note right of ArbitrationEngine
Canonical precedence:
Manual > Planned > Default
maps FR-011/012/019/025/027
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml DigitalHome_Object
skinparam classAttributeIconSize 0

object user1 as "user1:UserAccount [MonitorEnvironment]" {
  id = 42
  username = "alex"
  role = GENERAL
}

object profile1 as "profile1:UserProfile [MonitorEnvironment]" {
  id = 42
  userId = 42
  tempUnits = F
}

object gwThermo1 as "thermo1:Device [ControlEnvironment]" {
  deviceId = "tstat-01"
  deviceType = THERMOSTAT
  location = "LivingRoom"
  online = true
}

object sample1 as "sample1:TelemetrySample [MonitorEnvironment]" {
  sampleId = "s-1001"
  deviceId = "tstat-01"
  metric = "temperatureF"
  value = 72.0
  timestampUtc = "2026-04-22T12:00:01Z"
}

object planApr as "planApr:Plan [ManagePlans]" {
  planId = "plan-2026-04"
  month = 4
  year = 2026
  ownerUserId = 42
}

object override1 as "override1:OverrideSetting [OverrideSettings]" {
  overrideId = "ov-9001"
  deviceId = "tstat-01"
  metric = "setpointF"
  value = 74.0
  source = WEBSITE
  effectiveFromUtc = "2026-04-22T12:00:10Z"
  effectiveUntilUtc = "2026-04-22T13:00:00Z"
}

object cmd1 as "cmd1:ControlCommand [ControlEnvironment]" {
  commandId = "cmd-7001"
  deviceId = "tstat-01"
  metric = "setpointF"
  value = 74.0
  issuedAtUtc = "2026-04-22T12:00:10Z"
  issuedByUserId = 42
}

user1 -- profile1
user1 -- planApr
gwThermo1 -- sample1
gwThermo1 -- override1
override1 .. cmd1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml DigitalHome_State_OverrideSetting
hide empty description

state "OverrideSetting Lifecycle" as OSL {

  [*] --> Created : createOverride

  Created --> Active : activate\n[effectiveFromUtc <= now < effectiveUntilUtc]
  Created --> Expired : timePassed\n[now >= effectiveUntilUtc]

  Active --> Active : refresh\n(updateEffectiveUntil)\n[action: extendUntilNextPlannedBoundary]
  Active --> Expired : plannedBoundaryReached\n[now >= effectiveUntilUtc]
  Active --> Cancelled : cancelOverride

  Expired --> [*]
  Cancelled --> [*]
}

note right of OSL
Canonical precedence for setpoint resolution:
Manual > Planned > Default
Manual override duration: until end of current or next planned interval (FR-011/012/019/025/027)
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml DigitalHome_Activity_RemoteMonitorAndControl
start
:Open Web UI;
:Authenticate [SecurityCheck];
if (Auth OK?) then (yes)
  :Load device list;
  fork
    :Subscribe telemetry stream;
    note right
    NFR-001: UI updates <= 2s
    ASR-002: ui_refresh_interval_secs metric + alert
    end note
  fork again
    :Gateway acquisition loop;
    note right
    NFR-002: per-sensor >=10Hz
    sensor_acquisition_rate_hz metric + alert
    end note
  end fork

  :Render current conditions;
  if (User issues control?) then (yes)
    :Validate command constraints;
    :Apply arbitration (Manual > Planned > Default);
    :Send control command to Gateway;
    :Persist command + audit event;
    if (Device ack?) then (yes)
      :Update UI state;
    else (no)
      :Show descriptive error [FR-035];
    endif
  else (no)
    :Continue monitoring;
  endif

  :Optionally request report (CSV/PDF);
  :Log out;
  stop
else (no)
  :Show descriptive error [FR-035];
  stop
endif
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml DigitalHome_Sequence_RemoteMonitor
autonumber
actor EndUser
participant "WebUI" as WebUI
participant "HomeWebServerAPI" as API
participant "AuthService" as Auth
participant "TelemetryService" as Telemetry
database "HomeDatabase" as DB
participant "EventBus" as Bus
participant "GatewayAPI" as GWAPI
participant "DigitalHomeGateway" as GW

EndUser -> WebUI : OpenDashboard
WebUI -> API : Login(username,password)
API -> Auth : authenticate()
Auth -> DB : getUserAccount()
DB --> Auth : userAccount
Auth --> API : authSession
API --> WebUI : LoginOK(token)

WebUI -> API : SubscribeTelemetry(token)
API -> Auth : authorize(token)
Auth --> API : ok
API -> Telemetry : openStream(userId)

Telemetry -> DB : loadLatestSnapshots()
DB --> Telemetry : snapshots
Telemetry --> WebUI : InitialSnapshot

loop every 0..2s (p99 <=2s)
  GW -> Bus : PublishTelemetry(sample)
  Telemetry -> Bus : ConsumeTelemetry
  Telemetry -> DB : persistTelemetry(sample)
  Telemetry --> WebUI : PushUpdate(sample)
end

note right of Telemetry
NFR-001/ASR-002: UI freshness metric ui_refresh_interval_secs
Alert if >1% intervals >2.5s/15min
end note

note right of GW
NFR-002: acquisition >=10Hz per sensor
end note
@enduml
```

```plantuml
@startuml DigitalHome_Sequence_PlanOverrideControl
autonumber
actor EndUser
participant "WebUI" as WebUI
participant "HomeWebServerAPI" as API
participant "AuthService" as Auth
participant "PlannerService" as Planner
participant "ArbitrationEngine" as Arb
database "HomeDatabase" as DB
participant "GatewayAPI" as GWAPI
participant "DigitalHomeGateway" as GW
participant "RFModule" as RF

EndUser -> WebUI : SetThermostat(74F)
WebUI -> API : PostControlCommand(token,deviceId,metric,value)
API -> Auth : authorize(token)
Auth --> API : ok

API -> Planner : getActivePlan(deviceId,month,year)
Planner -> DB : loadPlan()
DB --> Planner : plan

API -> Arb : resolveSetpoint(deviceId,metric,nowUtc)
Arb -> DB : loadActiveOverrides(deviceId,metric)
DB --> Arb : overrides
Arb --> API : resolvedValue(74F)\n(precedence Manual>Planned>Default)

API -> DB : saveCommand(cmd)
API -> DB : saveAudit(event)
API -> GWAPI : sendControlCommand(cmd)

GWAPI -> GW : deliverCommand(cmd)
GW -> RF : transmit(cmd)
RF --> GW : ack(status)
GW --> GWAPI : commandAck
GWAPI --> API : ack
API --> WebUI : CommandResult(OK)

note right of Arb
FR-009 constraint validated (60..80 step 1)
FR-011/012/027 precedence canonical
end note

note right of API
NFR-008/ASR-006: TLS, audit within 5s (99%)
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml DigitalHome_Collab_RemoteMonitor
skinparam linetype ortho

actor EndUser
rectangle WebUI
rectangle "HomeWebServerAPI" as API
rectangle "AuthService" as Auth
rectangle "TelemetryService" as Telemetry
database "HomeDatabase" as DB
rectangle "EventBus" as Bus
rectangle "DigitalHomeGateway" as GW

EndUser -- WebUI
WebUI -- API
API -- Auth
API -- Telemetry
Telemetry -- DB
Telemetry -- Bus
GW -- Bus

WebUI ..> API : 1:Login
API ..> Auth : 2:authenticate
Auth ..> DB : 3:getUserAccount
API ..> WebUI : 4:LoginOK
WebUI ..> API : 5:SubscribeTelemetry
API ..> Telemetry : 6:openStream
Telemetry ..> DB : 7:loadSnapshots
GW ..> Bus : 8:PublishTelemetry
Telemetry ..> Bus : 9:ConsumeTelemetry
Telemetry ..> WebUI : 10:PushUpdate

note right of WebUI
Scenario: Remote monitoring with near-real-time updates
Maps FR-001A, FR-006, NFR-001, NFR-002, ASR-002
end note
@enduml
```

```plantuml
@startuml DigitalHome_Collab_PlanOverrideControl
skinparam linetype ortho

actor EndUser
rectangle WebUI
rectangle "HomeWebServerAPI" as API
rectangle "AuthService" as Auth
rectangle "PlannerService" as Planner
rectangle "ArbitrationEngine" as Arb
database "HomeDatabase" as DB
rectangle "GatewayAPI" as GWAPI
rectangle "DigitalHomeGateway" as GW
rectangle "RFModule" as RF

EndUser -- WebUI
WebUI -- API
API -- Auth
API -- Planner
API -- Arb
Planner -- DB
Arb -- DB
API -- DB
API -- GWAPI
GWAPI -- GW
GW -- RF

WebUI ..> API : 1:PostControlCommand
API ..> Auth : 2:authorize
API ..> Planner : 3:getActivePlan
Planner ..> DB : 4:loadPlan
API ..> Arb : 5:resolveSetpoint
Arb ..> DB : 6:loadOverrides
API ..> DB : 7:saveCommand
API ..> DB : 8:saveAudit
API ..> GWAPI : 9:sendControlCommand
GWAPI ..> GW : 10:deliverCommand
GW ..> RF : 11:transmit
RF ..> GW : 12:ack
GWAPI ..> API : 13:ack
API ..> WebUI : 14:CommandResult

note right of API
Scenario: Override planned value via website and control device
Maps FR-001B, FR-009, FR-011/012/027, NFR-008, ASR-006
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml DigitalHome_Package
skinparam packageStyle rectangle

package "ui" as P_UI {
  class WebUI
}

package "api" as P_API {
  class HomeWebServerAPI
}

package "security" as P_SEC {
  class AuthService
  class RbacPolicy
  class AuditLogger
}

package "domain" as P_DOM {
  class Device
  class Plan
  class OverrideSetting
  class ControlCommand
  class ArbitrationEngine
}

package "telemetry" as P_TEL {
  class TelemetryService
  class MetricsCollector
}

package "persistence" as P_PERS {
  class HomeDatabase
  class Repository
}

package "integrations" as P_INT {
  class GatewayAPI
  class DevicePluginHost
}

P_UI ..> P_API : uses
P_API ..> P_SEC : uses
P_API ..> P_DOM : uses
P_API ..> P_PERS : uses
P_API ..> P_INT : uses
P_TEL ..> P_PERS : persists
P_TEL ..> P_DOM : maps
P_INT ..> P_DOM : commands/events
P_SEC ..> P_PERS : audit store

note right of P_TEL
ASR-002/NFR-001/002:
metrics + alerts for freshness/acquisition
end note

note right of P_SEC
NFR-008/ASR-006:
TLS, RBAC, audit retention >=1y
end note

note right of P_INT
ASR-001/003:
Gateway + RF module via stable interface
Supports simulation via DevicePluginHost
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml DigitalHome_Component
skinparam componentStyle rectangle

component "WebUI" as C_WebUI <<UI>>
component "HomeWebServerAPI" as C_API <<API>>
component "AuthService" as C_Auth <<Security>>
component "AuditLogService" as C_Audit <<Security>>
component "TelemetryService" as C_Telemetry <<EventDriven>>
component "PlannerService" as C_Planner <<Domain>>
component "ArbitrationEngine" as C_Arb <<Domain>>
component "ReportingService" as C_Report <<Reporting>>
component "BackupRestoreService" as C_Backup <<Ops>>
database "HomeDatabase" as C_DB <<Persisted>>
queue "EventBus" as C_Bus <<Broker>>
component "GatewayAPI" as C_GWAPI <<Integration>>
component "DevicePluginHost" as C_Plugins <<Microkernel>>

interface "IAuth" as IAuth
interface "IAudit" as IAudit
interface "ITelemetryStream" as ITel
interface "IPlan" as IPlan
interface "IArbitration" as IArb
interface "IReport" as IRep
interface "IBackup" as IBak
interface "IGatewayControl" as IGW

C_Auth - IAuth
C_Audit - IAudit
C_Telemetry - ITel
C_Planner - IPlan
C_Arb - IArb
C_Report - IRep
C_Backup - IBak
C_GWAPI - IGW

C_WebUI ..> C_API : HTTPS(TLS)
C_API ..> IAuth
C_API ..> IAudit
C_API ..> ITel
C_API ..> IPlan
C_API ..> IArb
C_API ..> IRep
C_API ..> IBak
C_API ..> IGW

C_Audit ..> C_DB : write
C_Auth ..> C_DB : read/write
C_Telemetry ..> C_Bus : consume
C_Telemetry ..> C_DB : persist
C_Planner ..> C_DB : read/write
C_Report ..> C_DB : query
C_Backup ..> C_DB : snapshot
C_GWAPI ..> C_Plugins : uses
C_Plugins ..> C_Bus : publish

note right of C_GWAPI
ASR-001: Server->Gateway over LAN
ASR-003: RF behind plugins
ASR-008: simulation swaps plugins
end note

note right of C_Audit
ASR-006: 99% events visible <=5s
Retention >=1y export CSV/JSON
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DigitalHome_Deployment
skinparam componentStyle rectangle

node "EndUser Device\n(Web-ready Phone/PC/PDA)" as N_Client {
  artifact "Web Browser" as A_Browser
}

node "Home Network (LAN)" as N_LAN

node "HomeWebServer (Home Computer)\n<<ASR-001>>" as N_Server {
  artifact "WebUI Assets" as A_UI
  artifact "HomeWebServerAPI" as A_API
  artifact "AuthService" as A_Auth
  artifact "TelemetryService" as A_Tel
  artifact "PlannerService" as A_Planner
  artifact "ArbitrationEngine" as A_Arb
  artifact "ReportingService" as A_Report
  artifact "BackupRestoreService" as A_Backup
  database "HomeDatabase" as N_DB
  artifact "EventBus" as A_Bus
}

node "DigitalHomeGateway\n(Master Control)\n<<ASR-001>>" as N_GW {
  artifact "GatewayAPI" as A_GWAPI
  artifact "DevicePluginHost" as A_Plugins
  artifact "RFModule" as A_RF
  artifact "Watchdog/HealthAgent" as A_Health
}

node "Sensors/Controllers\n(Thermostats/Humidistats/Contacts/Switches/Alarms)" as N_Devices

cloud "ISP/Internet\n>=5Mbps down/1Mbps up\n99% monthly uptime" as N_ISP

N_Client --> N_ISP : HTTPS(TLS)\nRemote access
N_ISP --> N_LAN
N_LAN --> N_Server : HTTPS(TLS)\nUI/API
N_Server --> N_GW : LAN TCP/gRPC\ncommands+telemetry
N_GW --> N_Devices : RF Wireless\n<=1000ft indoor

note right of N_Server
NFR-004: reliability MTBF target
NFR-005/006: daily backup, RPO<=24h RTO<=60m
NFR-008: TLS + audit retention >=1y
end note

note right of N_GW
ASR-002/NFR-002: acquisition >=10Hz
ASR-003: RF range 1000ft
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml DigitalHome_Container
skinparam rectangle {
  roundCorner 10
}
skinparam componentStyle rectangle

rectangle "EndUser Device" as C1 {
  rectangle "Web Browser\n[Monitor/Control]" as Browser
}

rectangle "HomeWebServer (on-prem home computer)\n<<ASR-001>>" as C2 {
  rectangle "WebUI Container\n[Personal Web Page]" as WebUI
  rectangle "API Container\n[HomeWebServerAPI]" as API
  rectangle "Auth/Audit Container\n[RBAC+Audit]" as Sec
  rectangle "Telemetry Container\n[Stream+Persist]" as Tel
  rectangle "Planning/Arbitration Container\n[Plans+Overrides]" as Plan
  rectangle "Reporting Container\n[CSV/PDF]" as Rep
  rectangle "Backup/Restore Container\n[Daily Backup]" as Bak
  database "HomeDatabase\n(config,user_accounts,plans,usage_log,telemetry)\n<<persisted>>" as DB
  rectangle "EventBus Container\n[Broker]" as Bus
}

rectangle "DigitalHomeGateway (master control)\n<<ASR-001>>" as C3 {
  rectangle "GatewayAPI Container\n[Command Bridge]" as GWAPI
  rectangle "DevicePluginHost Container\n[Microkernel]" as Plugins
  rectangle "RFModule Container\n[Wireless I/O]" as RF
}

cloud "ISP/Internet\n(NFR-009)" as ISP
rectangle "Home Devices\n(Thermostats, Humidistats,\nContact Sensors, Power Switches, Alarms)" as Devices

Browser --> ISP : HTTPS(TLS)
ISP --> API : HTTPS(TLS)\nRemote access
Browser --> WebUI : HTTPS(TLS)

WebUI --> API : HTTPS(TLS)
API --> Sec : authorize/audit
API --> Tel : subscribe
API --> Plan : plan+override
API --> Rep : reports
API --> Bak : backup ops
Sec --> DB : read/write
Tel --> Bus : consume
Tel --> DB : persist telemetry
Plan --> DB : plans/overrides
Rep --> DB : query/report
Bak --> DB : backup/restore

API --> GWAPI : LAN secure channel
GWAPI --> Plugins : invoke
Plugins --> RF : transmit/receive
RF --> Devices : RF Wireless\n<=1000ft (ASR-003)

note right of Tel
NFR-001/ASR-002: UI <=2s via push stream
NFR-002: acquisition >=10Hz (enforced at gateway)
Metrics+alerts emitted
end note

note right of Sec
NFR-008/ASR-006:
TLS v1.2+; audit schema; retention >=1y; export CSV/JSON
end note

note right of Bak
NFR-005/006:
daily backup time set by Technician
RPO<=24h, RTO<=60m; restore drills
end note
@enduml
```