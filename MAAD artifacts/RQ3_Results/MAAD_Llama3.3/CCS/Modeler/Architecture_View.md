## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
actor Correlator as "Correlator"
usecase (Configure Correlator) as (ConfigureCorrelator)
usecase (Process Data) as (ProcessData)
usecase (Monitor Correlator) as (MonitorCorrelator)
usecase (Access System) as (AccessSystem)
EndUser -- (ConfigureCorrelator)
EndUser -- (ProcessData)
EndUser -- (MonitorCorrelator)
Admin -- (AccessSystem)
Correlator -- (ConfigureCorrelator)
Correlator -- (ProcessData)
Correlator -- (MonitorCorrelator)
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class
class Correlator {
  - id: String
  - configuration: String
  + configure()
  + process()
  + monitor()
}
class Data {
  - id: String
  - value: String
  + process()
}
class User {
  - id: String
  - role: String
  + access()
}
class System {
  - id: String
  - status: String
  + monitor()
}
Correlator --* Data
Correlator --* User
User --* System
System --* Correlator
@enduml
```
3. Object — Logic View: Object Diagram
```plantuml
@startuml
participant correlator1
participant data1
participant user1
participant system1
correlator1 -> data1
correlator1 -> user1
user1 -> system1
system1 -> correlator1
@enduml
```
4. State — Logic View: State Diagram
```plantuml
@startuml State
state Configure
state Process
state Monitor
state Access
[*] --> Configure
Configure --> Process : start
Process --> Monitor : finish
Monitor --> Access : error
Access --> Configure : retry
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity
start
:Configure Correlator;
fork
  :Process Data;
  :Monitor Correlator;
join
:Access System;
if (error?) then
  :Retry;
else
  :Finish;
endif
stop
@enduml
```
6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml Sequence1
participant EndUser as "End User"
participant Correlator as "Correlator"
participant System as "System"
EndUser->>Correlator: configure()
Correlator->>System: process()
System->>Correlator: monitor()
Correlator->>EndUser: result
@enduml
```
```plantuml
@startuml Sequence2
participant Admin as "Admin"
participant System as "System"
Admin->>System: access()
System->>Admin: status
@enduml
```
7. Collaboration — Process View: Collaboration Diagram 
```plantuml
@startuml Collaboration1
participant "End User" as EndUser
participant "Correlator" as Correlator
participant "System" as System
EndUser ->> Correlator: configure()
Correlator ->> System: process()
System ->> Correlator: monitor()
Correlator ->> EndUser: result
note right of Correlator: Configure Correlator
@enduml
```
```plantuml
@startuml Collaboration2
participant Admin
participant System
Admin->>System: access()
System->>Admin: status
note right of Admin: Access System
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package
package Correlator {
  class Correlator
  class Data
}
package System {
  class System
  class User
}
package API {
  interface CorrelatorAPI
  interface SystemAPI
}
Correlator --* System
System --* API
@enduml
```
9. Component — Development View: Component Diagram
```plantuml
@startuml Component
component CorrelatorComponent {
  interface CorrelatorAPI
  class Correlator
}
component SystemComponent {
  interface SystemAPI
  class System
}
component Database {
  class Data
}
CorrelatorComponent --* SystemComponent
SystemComponent --* Database
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment
node CorrelatorNode {
  component CorrelatorComponent
}
node SystemNode {
  component SystemComponent
}
node DatabaseNode {
  component Database
}
CorrelatorNode --* SystemNode
SystemNode --* DatabaseNode
@enduml
```
11. Container — Physical View: Container Diagram
```plantuml
@startuml Container
container CorrelatorContainer {
  component CorrelatorComponent
  technology "Docker"
}
container SystemContainer {
  component SystemComponent
  technology "Kubernetes"
}
container DatabaseContainer {
  component Database
  technology "MySQL"
}
CorrelatorContainer --* SystemContainer
SystemContainer --* DatabaseContainer
@enduml
```