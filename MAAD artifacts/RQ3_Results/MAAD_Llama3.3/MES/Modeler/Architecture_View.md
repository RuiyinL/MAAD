## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
actor ESOC as "ESOC"
actor PDS as "PDS"
actor ASPERA3_CoI as "ASPERA-3 Co-I"

EndUser -- (Acquire Telemetry Data)
EndUser -- (Process Science Data)
EndUser -- (Provide Web-Based Displays)
Admin -- (Manage System)
ESOC -- (Provide Telemetry Data)
PDS -- (Receive IDFS Data)
ASPERA3_CoI -- (Access IDFS Data)

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml
class TelemetryData {
  - id: String
  - data: String
}

class IDFSData {
  - id: String
  - data: String
}

class User {
  - id: String
  - role: String
}

class System {
  - id: String
  - status: String
}

TelemetryData --* System : acquired by
IDFSData --* System : processed by
User --* System : manages
System --* User : has

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml
object telemetryData1 : TelemetryData
object idfsData1 : IDFSData
object user1 : User
object system1 : System

telemetryData1 -- system1
idfsData1 -- system1
user1 -- system1

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml
state Acquiring
state Processing
state Completed
state Failed

[*] --> Acquiring
Acquiring --> Processing : telemetry data acquired
Processing --> Completed : idfs data processed
Processing --> Failed : error occurred
Failed --> Acquiring : retry

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml
start
:Acquire Telemetry Data;
:Process Science Data;
:Provide Web-Based Displays;
:Store Telemetry Data;
:Store IDFS Data;
:Submit IDFS Data to PDS;
stop

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml
participant EndUser as "End User"
participant System as "System"
participant ESOC as "ESOC"
participant PDS as "PDS"

EndUser->>System: request telemetry data
System->>ESOC: request telemetry data
ESOC->>System: provide telemetry data
System->>EndUser: provide idfs data
System->>PDS: submit idfs data

@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml
participant "End User" as EndUser
participant "System" as System
participant "ESOC" as ESOC
participant "PDS" as PDS

EndUser ->> System: request telemetry data
System ->> ESOC: request telemetry data
ESOC ->> System: provide telemetry data
System ->> EndUser: provide idfs data
System ->> PDS: submit idfs data

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml
package api {
  class TelemetryData
  class IDFSData
}

package domain {
  class User
  class System
}

package persistence {
  class Database
}

api --* domain
domain --* persistence

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml
component TelemetryDataAcquirer
component IDFSDataProcessor
component WebDisplayProvider
component SystemManager

TelemetryDataAcquirer --* IDFSDataProcessor
IDFSDataProcessor --* WebDisplayProvider
WebDisplayProvider --* SystemManager

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml
node WebServer
node DatabaseServer
node PDS_Server

artifact TelemetryDataAcquirer
artifact IDFSDataProcessor
artifact WebDisplayProvider
artifact SystemManager

WebServer --* DatabaseServer
DatabaseServer --* PDS_Server
TelemetryDataAcquirer --* WebServer
IDFSDataProcessor --* WebServer
WebDisplayProvider --* WebServer
SystemManager --* WebServer

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml
artifact WebUI
artifact BackendAPI
artifact Database
artifact Cache
artifact MessageQueue

WebUI --* BackendAPI
BackendAPI --* Database
Database --* Cache
Cache --* MessageQueue

@enduml
```