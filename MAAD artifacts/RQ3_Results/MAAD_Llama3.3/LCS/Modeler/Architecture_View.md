## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
actor System as "System"

usecase (System Startup) as (FR-001)
usecase (Device Status Monitoring) as (FR-002)
usecase (Command Control) as (FR-003)
usecase (Safety Screening) as (FR-004)
usecase (Logging) as (FR-005)

EndUser -- (FR-002)
EndUser -- (FR-003)
Admin -- (FR-001)
Admin -- (FR-005)
System -- (FR-001)
System -- (FR-002)
System -- (FR-003)
System -- (FR-004)
System -- (FR-005)

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class System {
  - id: string
  - cabinetId: string
  + startup(): void
  + monitorDeviceStatus(): void
  + controlCommand(): void
  + safetyScreening(): void
  + logging(): void
}

class Device {
  - id: string
  - status: string
  + getStatus(): string
}

class Command {
  - id: string
  - payload: string
  + execute(): void
}

class SafetyRule {
  - id: string
  - rule: string
  + validate(): boolean
}

class Log {
  - id: string
  - message: string
  + log(): void
}

System --* Device
System --* Command
System --* SafetyRule
System --* Log

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
artifact system1
artifact device1
artifact command1
artifact safetyRule1
artifact log1

system1 -- device1
system1 -- command1
system1 -- safetyRule1
system1 -- log1

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
state SystemStartup
state DeviceStatusMonitoring
state CommandControl
state SafetyScreening
state Logging

[*] --> SystemStartup
SystemStartup --> DeviceStatusMonitoring : startup completed
DeviceStatusMonitoring --> CommandControl : device status monitored
CommandControl --> SafetyScreening : command executed
SafetyScreening --> Logging : safety screening completed
Logging --> [*] : logging completed

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram
start
:Startup System;
fork
  :Monitor Device Status;
  :Control Command;
  :Safety Screening;
join
:Logging;
if (Safety Screening Failed?) then
  :Alert Admin;
else
  :Continue Operation;
endif
stop

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
participant System as "System"
participant Device as "Device"
participant Command as "Command"
participant SafetyRule as "Safety Rule"
participant Log as "Log"

System->>Device: monitorDeviceStatus()
Device->>System: return status
System->>Command: controlCommand()
Command->>System: return result
System->>SafetyRule: safetyScreening()
SafetyRule->>System: return result
System->>Log: log()
Log->>System: return result

@enduml
```

```plantuml
@startuml SequenceDiagram2
participant System as "System"
participant Admin as "Admin"
participant Log as "Log"

System->>Admin: alertAdmin()
Admin->>System: return acknowledgement
System->>Log: logAlert()
Log->>System: return result

@enduml
```

7. Collaboration — Process View: Collaboration Diagram 
```plantuml
@startuml CollaborationDiagram1
participant System
participant Device
participant Command
participant SafetyRule
participant Log

System->>Device: monitorDeviceStatus()
Device->>System: return status
System->>Command: controlCommand()
Command->>System: return result
System->>SafetyRule: safetyScreening()
SafetyRule->>System: return result
System->>Log: log()
Log->>System: return result

note right of System: Scenario: System Startup

@enduml
```

```plantuml
@startuml CollaborationDiagram2
participant System
participant Admin
participant Log

System->>Admin: alertAdmin()
Admin->>System: return acknowledgement
System->>Log: logAlert()
Log->>System: return result

note right of System: Scenario: Safety Screening Failed

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package System {
  class System
  class Device
  class Command
  class SafetyRule
  class Log
}

package API {
  interface SystemAPI
  interface DeviceAPI
  interface CommandAPI
  interface SafetyRuleAPI
  interface LogAPI
}

package Persistence {
  class SystemRepository
  class DeviceRepository
  class CommandRepository
  class SafetyRuleRepository
  class LogRepository
}

System -- API
API -- Persistence

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
component SystemComponent
component DeviceComponent
component CommandComponent
component SafetyRuleComponent
component LogComponent

component SystemAPIComponent
component DeviceAPIComponent
component CommandAPIComponent
component SafetyRuleAPIComponent
component LogAPIComponent

component SystemRepositoryComponent
component DeviceRepositoryComponent
component CommandRepositoryComponent
component SafetyRuleRepositoryComponent
component LogRepositoryComponent

SystemComponent -- SystemAPIComponent
DeviceComponent -- DeviceAPIComponent
CommandComponent -- CommandAPIComponent
SafetyRuleComponent -- SafetyRuleAPIComponent
LogComponent -- LogAPIComponent

SystemAPIComponent -- SystemRepositoryComponent
DeviceAPIComponent -- DeviceRepositoryComponent
CommandAPIComponent -- CommandRepositoryComponent
SafetyRuleAPIComponent -- SafetyRuleRepositoryComponent
LogAPIComponent -- LogRepositoryComponent

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node SystemNode
node DeviceNode
node CommandNode
node SafetyRuleNode
node LogNode

node SystemAPIGateway
node DeviceAPIGateway
node CommandAPIGateway
node SafetyRuleAPIGateway
node LogAPIGateway

node SystemDatabase
node DeviceDatabase
node CommandDatabase
node SafetyRuleDatabase
node LogDatabase

SystemNode -- SystemAPIGateway
DeviceNode -- DeviceAPIGateway
CommandNode -- CommandAPIGateway
SafetyRuleNode -- SafetyRuleAPIGateway
LogNode -- LogAPIGateway

SystemAPIGateway -- SystemDatabase
DeviceAPIGateway -- DeviceDatabase
CommandAPIGateway -- CommandDatabase
SafetyRuleAPIGateway -- SafetyRuleDatabase
LogAPIGateway -- LogDatabase

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
artifact SystemContainer
artifact DeviceContainer
artifact CommandContainer
artifact SafetyRuleContainer
artifact LogContainer

artifact SystemAPIContainer
artifact DeviceAPIContainer
artifact CommandAPIContainer
artifact SafetyRuleAPIContainer
artifact LogAPIContainer

artifact SystemDatabaseContainer
artifact DeviceDatabaseContainer
artifact CommandDatabaseContainer
artifact SafetyRuleDatabaseContainer
artifact LogDatabaseContainer

SystemContainer -- SystemAPIContainer
DeviceContainer -- DeviceAPIContainer
CommandContainer -- CommandAPIContainer
SafetyRuleContainer -- SafetyRuleAPIContainer
LogContainer -- LogAPIContainer

SystemAPIContainer -- SystemDatabaseContainer
DeviceAPIContainer -- DeviceDatabaseContainer
CommandAPIContainer -- CommandDatabaseContainer
SafetyRuleAPIContainer -- SafetyRuleDatabaseContainer
LogAPIContainer -- LogDatabaseContainer

@enduml
```