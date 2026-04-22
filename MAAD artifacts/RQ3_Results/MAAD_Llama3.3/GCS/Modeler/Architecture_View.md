## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
actor TelescopeSystem as "Telescope System"

usecase (Observe) as "Observe"
usecase (Monitor) as "Monitor"
usecase (Operate) as "Operate"
usecase (Test) as "Test"
usecase (Administer) as "Administer"
usecase (AcquireData) as "Acquire Data"
usecase (TransferData) as "Transfer Data"

EndUser -- (Observe)
EndUser -- (Monitor)
EndUser -- (Operate)
EndUser -- (Test)
Admin -- (Administer)
TelescopeSystem -- (AcquireData)
TelescopeSystem -- (TransferData)

(Observe) ..> (AcquireData) : <<include>>
(Monitor) ..> (AcquireData) : <<include>>
(Operate) ..> (AcquireData) : <<include>>
(Test) ..> (AcquireData) : <<include>>
(Administer) ..> (TransferData) : <<include>>
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class User {
  - id: Integer
  - role: String
  - privileges: List<String>
}

class Telescope {
  - id: Integer
  - name: String
  - status: String
}

class Instrument {
  - id: Integer
  - name: String
  - status: String
}

class Observation {
  - id: Integer
  - user: User
  - telescope: Telescope
  - instrument: Instrument
  - startTime: Date
  - endTime: Date
}

class Data {
  - id: Integer
  - observation: Observation
  - fileType: String
  - fileSize: Long
}

User "1" --* Observation
Telescope "1" --* Observation
Instrument "1" --* Observation
Observation "1" --* Data
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
participant user1
participant telescope1
participant instrument1
participant observation1
participant data1

user1 --> observation1
telescope1 --> observation1
instrument1 --> observation1
observation1 --> data1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
state Observing
state Monitoring
state Operating
state Testing
state Administering

[*] --> Observing
Observing --> Monitoring : stopObserving
Monitoring --> Operating : startOperating
Operating --> Testing : startTesting
Testing --> Administering : startAdministering
Administering --> [*] : stopAdministering
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram
start
:Observe;
if (isMonitoringRequired?) then (yes)
  :Monitor;
else (no)
  :Operate;
endif
:AcquireData;
:TransferData;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
participant EndUser as "End User"
participant TelescopeSystem as "Telescope System"
participant DataAcquisition as "Data Acquisition"

EndUser->>TelescopeSystem: observe()
TelescopeSystem->>DataAcquisition: acquireData()
DataAcquisition->>TelescopeSystem: returnData()
TelescopeSystem->>EndUser: returnObservation()
@enduml
```

```plantuml
@startuml SequenceDiagram2
participant Admin as "Admin"
participant TelescopeSystem as "Telescope System"
participant DataTransfer as "Data Transfer"

Admin->>TelescopeSystem: administer()
TelescopeSystem->>DataTransfer: transferData()
DataTransfer->>TelescopeSystem: returnTransferStatus()
TelescopeSystem->>Admin: returnAdminStatus()
@enduml
```

7. Collaboration — Process View: Collaboration Diagram 
```plantuml
@startuml CollaborationDiagram1
participant "End User" as EndUser
participant "Telescope System" as TelescopeSystem
participant "Data Acquisition" as DataAcquisition

EndUser ->> TelescopeSystem: observe()
TelescopeSystem ->> DataAcquisition: acquireData()
DataAcquisition ->> TelescopeSystem: returnData()
TelescopeSystem ->> EndUser: returnObservation()
@enduml
```

```plantuml
@startuml CollaborationDiagram2
participant Admin
participant TelescopeSystem
participant DataTransfer

Admin ->> TelescopeSystem: administer()
TelescopeSystem ->> DataTransfer: transferData()
DataTransfer ->> TelescopeSystem: returnTransferStatus()
TelescopeSystem ->> Admin: returnAdminStatus()
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package api
package domain
package persistence
package ui
package integrations

api -- domain
domain -- persistence
persistence -- ui
ui -- integrations
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
component AuthComponent
component OrderService
component AuthService
component DataAcquisitionService
component DataTransferService

AuthComponent -- OrderService
OrderService -- AuthService
AuthService -- DataAcquisitionService
DataAcquisitionService -- DataTransferService
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node WebServer
node DatabaseServer
node DataAcquisitionServer
node DataTransferServer

WebServer -- DatabaseServer
DatabaseServer -- DataAcquisitionServer
DataAcquisitionServer -- DataTransferServer
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
artifact WebUI
artifact BackendAPI
artifact Database
artifact Cache
artifact MessageQueue

WebUI -- BackendAPI
BackendAPI -- Database
Database -- Cache
Cache -- MessageQueue
@enduml
```