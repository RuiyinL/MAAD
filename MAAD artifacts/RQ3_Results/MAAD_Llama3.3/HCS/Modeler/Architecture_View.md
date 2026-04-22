## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
actor PaymentGateway as "Payment Gateway"

usecase "Manage User Account" as (ManageUserAccount)
usecase "Control Temperature" as (ControlTemperature)
usecase "Control Humidity" as (ControlHumidity)
usecase "Manage Security" as (ManageSecurity)
usecase "Manage Appliances" as (ManageAppliances)
usecase "Plan and Schedule" as (PlanAndSchedule)
usecase "Authenticate User" as (AuthenticateUser)
usecase "Backup and Recover" as (BackupAndRecover)

EndUser -- (ManageUserAccount)
EndUser -- (ControlTemperature)
EndUser -- (ControlHumidity)
EndUser -- (ManageSecurity)
EndUser -- (ManageAppliances)
EndUser -- (PlanAndSchedule)
EndUser -- (AuthenticateUser)
Admin -- (ManageUserAccount)
Admin -- (BackupAndRecover)
PaymentGateway -- (PlanAndSchedule)
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml
class User {
  - id: UUID
  - name: String
  - email: String
  - hash: String
}

class Plan {
  - id: UUID
  - userId: UUID
  - params: List<Param>
}

class Device {
  - id: UUID
  - type: String
  - location: String
}

class TemperatureController {
  + controlTemperature(targetTemp: float)
}

class HumidityController {
  + controlHumidity(targetHumidity: float)
}

class SecurityManager {
  + manageSecurity()
}

class ApplianceManager {
  + manageAppliances()
}

User "1" --* Plan
Plan "1" --* Param
Device "1" --* TemperatureController
Device "1" --* HumidityController
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml
participant user1
participant plan1
participant device1
participant temperatureController
participant humidityController

user1 -> plan1
plan1 -> device1
device1 -> temperatureController
device1 -> humidityController
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml
state "Offline" as offline
state "Online" as online
state "Authenticated" as authenticated

[*] --> offline
offline --> online : connect
online --> authenticated : authenticate
authenticated --> online : disconnect
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml
start
:Connect to system;
if (Authenticated?) then (yes)
  :Control temperature;
  :Control humidity;
  :Manage security;
  :Manage appliances;
  :Plan and schedule;
else (no)
  :Authenticate user;
endif
:Backup and recover;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml
participant EndUser as "End User"
participant TemperatureController as "Temperature Controller"
participant HumidityController as "Humidity Controller"
participant SecurityManager as "Security Manager"
participant ApplianceManager as "Appliance Manager"

EndUser->>TemperatureController: controlTemperature(22.0)
TemperatureController->>TemperatureController: adjust temperature
EndUser->>HumidityController: controlHumidity(60.0)
HumidityController->>HumidityController: adjust humidity
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml
participant "End User" as EndUser
participant "Temperature Controller" as TemperatureController
participant "Humidity Controller" as HumidityController
participant "Security Manager" as SecurityManager
participant "Appliance Manager" as ApplianceManager

EndUser ->> TemperatureController: controlTemperature(22.0)
TemperatureController ->> TemperatureController: adjust temperature
EndUser ->> HumidityController: controlHumidity(60.0)
HumidityController ->> HumidityController: adjust humidity
note right of EndUser: Scenario: Control temperature and humidity
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml
package "API" as api {
  class UserController
  class TemperatureController
  class HumidityController
}

package "Domain" as domain {
  class User
  class Plan
  class Device
}

package "Persistence" as persistence {
  class UserRepository
  class PlanRepository
  class DeviceRepository
}

api --* domain
domain --* persistence
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml
component "AuthComponent" as auth {
  interface "AuthenticateUser"
  port "authPort"
}

component "TemperatureComponent" as temperature {
  interface "ControlTemperature"
  port "temperaturePort"
}

component "HumidityComponent" as humidity {
  interface "ControlHumidity"
  port "humidityPort"
}

auth --* temperature
temperature --* humidity
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml
node "WebServer" as web {
  component "AuthComponent"
  component "TemperatureComponent"
  component "HumidityComponent"
}

node "DatabaseServer" as db {
  component "UserRepository"
  component "PlanRepository"
  component "DeviceRepository"
}

web -- db
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml
container "WebUI" as webui {
  responsibility "User Interface"
  technology "React"
}

container "BackendAPI" as backend {
  responsibility "API"
  technology "Node.js"
}

container "Database" as db {
  responsibility "Data Storage"
  technology "MySQL"
}

webui -- backend
backend -- db
@enduml
```