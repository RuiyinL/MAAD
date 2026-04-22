## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Satellite as "Satellite"
actor GroundCommand as "Ground Command"
actor SunSensor as "Sun Sensor"
actor Gyroscope as "Gyroscope"

usecase "Sun Acquisition" as (FR-001)
usecase "Satellite Attitude Control" as (FR-002)
usecase "Ground Command Reception" as (FR-003)
usecase "Sun Sensor Data Acquisition" as (FR-004)
usecase "Thruster Data Acquisition" as (FR-005)
usecase "Three-Axis Attitude Determination" as (FR-006)
usecase "Sun Search Mode Switching" as (FR-007)
usecase "Fault Management" as (FR-008)
usecase "Telemetry Data Transmission" as (FR-009)

Satellite -- (FR-001)
Satellite -- (FR-002)
GroundCommand -- (FR-003)
SunSensor -- (FR-004)
Gyroscope -- (FR-005)
Satellite -- (FR-006)
Satellite -- (FR-007)
Satellite -- (FR-008)
Satellite -- (FR-009)

(FR-002) ..> (FR-001) : <<include>>
(FR-003) ..> (FR-002) : <<extend>>
(FR-004) ..> (FR-001) : <<include>>
(FR-005) ..> (FR-002) : <<include>>
(FR-006) ..> (FR-001) : <<include>>
(FR-007) ..> (FR-002) : <<extend>>
(FR-008) ..> (FR-002) : <<extend>>
(FR-009) ..> (FR-002) : <<include>>
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class Satellite {
  - attitude: float
  - velocity: float
  + determineAttitude()
  + controlAttitude()
}

class GroundCommand {
  - command: string
  + sendCommand()
}

class SunSensor {
  - data: float
  + acquireData()
}

class Gyroscope {
  - data: float
  + acquireData()
}

class Thruster {
  - status: bool
  - power: uint8
  + acquireData()
}

class Telemetry {
  - mode: byte
  - angle: uint16
  - velocity: q15
  + transmitData()
}

Satellite "1" *-- "1" GroundCommand
Satellite "1" *-- "1" SunSensor
Satellite "1" *-- "1" Gyroscope
Satellite "1" *-- "1" Thruster
Satellite "1" *-- "1" Telemetry
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
object satellite1 : Satellite
object groundCommand1 : GroundCommand
object sunSensor1 : SunSensor
object gyroscope1 : Gyroscope
object thruster1 : Thruster
object telemetry1 : Telemetry

satellite1 : attitude = 0.0
satellite1 : velocity = 0.0
groundCommand1 : command = "start"
sunSensor1 : data = 10.0
gyroscope1 : data = 20.0
thruster1 : status = true
thruster1 : power = 50
telemetry1 : mode = 1
telemetry1 : angle = 30
telemetry1 : velocity = 0.5

satellite1 -- groundCommand1
satellite1 -- sunSensor1
satellite1 -- gyroscope1
satellite1 -- thruster1
satellite1 -- telemetry1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
state "Idle" as idle
state "Acquiring" as acquiring
state "Controlling" as controlling
state "Transmitting" as transmitting

[*] --> idle
idle --> acquiring : startAcquisition
acquiring --> controlling : acquisitionComplete
controlling --> transmitting : controlComplete
transmitting --> idle : transmissionComplete

note right of idle : Satellite attitude determination
note right of acquiring : Satellite attitude control
note right of transmitting : Telemetry data transmission
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram
start
:Start Acquisition;
if (Acquisition Complete?) then (yes)
  :Determine Attitude;
  :Control Attitude;
  if (Control Complete?) then (yes)
    :Transmit Telemetry;
  else (no)
    :Error Handling;
  endif
else (no)
  :Error Handling;
endif
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
participant Satellite as "Satellite"
participant GroundCommand as "Ground Command"
participant SunSensor as "Sun Sensor"
participant Gyroscope as "Gyroscope"

Satellite->>GroundCommand: sendCommand("start")
GroundCommand->>Satellite: receiveCommand()
Satellite->>SunSensor: acquireData()
SunSensor->>Satellite: sendData(10.0)
Satellite->>Gyroscope: acquireData()
Gyroscope->>Satellite: sendData(20.0)
@enduml
```

```plantuml
@startuml SequenceDiagram2
participant Satellite as "Satellite"
participant Thruster as "Thruster"
participant Telemetry as "Telemetry"

Satellite->>Thruster: acquireData()
Thruster->>Satellite: sendData(status=true, power=50)
Satellite->>Telemetry: transmitData(mode=1, angle=30, velocity=0.5)
Telemetry->>Satellite: transmissionComplete()
@enduml
```

7. Collaboration — Process View: Collaboration Diagram 
```plantuml
@startuml CollaborationDiagram1
participant "Satellite"
participant "Ground Command"
participant "Sun Sensor"
participant "Gyroscope"

Satellite ->> GroundCommand: sendCommand("start")
GroundCommand ->> Satellite: receiveCommand()
Satellite ->> SunSensor: acquireData()
SunSensor ->> Satellite: sendData(10.0)
Satellite ->> Gyroscope: acquireData()
Gyroscope ->> Satellite: sendData(20.0)
@enduml
```

```plantuml
@startuml CollaborationDiagram2
participant Satellite
participant Thruster
participant Telemetry

Satellite ->> Thruster: acquireData()
Thruster ->> Satellite: sendData(status=true, power=50)
Satellite ->> Telemetry: transmitData(mode=1, angle=30, velocity=0.5)
Telemetry ->> Satellite: transmissionComplete()
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package Satellite {
  class Satellite
  class GroundCommand
  class SunSensor
  class Gyroscope
}

package Thruster {
  class Thruster
}

package Telemetry {
  class Telemetry
}

Satellite -- Thruster
Satellite -- Telemetry
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
component Satellite {
  port "command"
  port "data"
}

component GroundCommand {
  port "command"
}

component SunSensor {
  port "data"
}

component Gyroscope {
  port "data"
}

component Thruster {
  port "data"
}

component Telemetry {
  port "data"
}

Satellite ..> GroundCommand : command
Satellite ..> SunSensor : data
Satellite ..> Gyroscope : data
Satellite ..> Thruster : data
Satellite ..> Telemetry : data
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node "Satellite Node" as satelliteNode {
  component Satellite
  component GroundCommand
  component SunSensor
  component Gyroscope
}

node "Thruster Node" as thrusterNode {
  component Thruster
}

node "Telemetry Node" as telemetryNode {
  component Telemetry
}

satelliteNode -- thrusterNode
satelliteNode -- telemetryNode
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
container "Satellite Container" as satelliteContainer {
  component Satellite
  component GroundCommand
  component SunSensor
  component Gyroscope
}

container "Thruster Container" as thrusterContainer {
  component Thruster
}

container "Telemetry Container" as telemetryContainer {
  component Telemetry
}

satelliteContainer -- thrusterContainer
satelliteContainer -- telemetryContainer
@enduml
```