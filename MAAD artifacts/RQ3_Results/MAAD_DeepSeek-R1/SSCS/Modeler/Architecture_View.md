## Architecture Summary & Quality-Attribute Analysis  
**Proposed Architecture**: Deterministic cyclic executive using time-triggered scheduling (32ms ISR driving 160ms cycles) with strict within-cycle timing. Features include:  
- Hardware abstraction via `InterfaceAddressTable`  
- Explicit state machines for mode/fault transitions  
- Schema-validated data contracts  
- Centralized fault logging  

**Quality Attribute Analysis**:  
1. **Performance** (ASR-001, NFR-001/002/004):  
   - *Trade-off*: Fixed scheduling ensures 128ms±1ms thruster control but limits dynamic adaptation  
   - *Risk*: WCET breaches in 11MHz CPU may violate 5µs inter-byte latency  
2. **Reliability** (NFR-003, ASR-003):  
   - *Tension*: Explicit state tables enable verifiability but increase memory usage in 8KB SRAM  
3. **Maintainability** (ASR-002/004):  
   - *Trade-off*: Versioned schemas prevent integration errors but require governance overhead  

**Architectural Style**: **Layered Architecture** + **State Pattern**  
- *Justification*:  
  - Layering isolates hardware interaction (HAL) from control logic (ASR-002)  
  - State pattern implements mode transitions (ASR-003)  
  - Cyclic executive satisfies hard real-time constraints (ASR-001)  

---

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor GroundStation as gs
actor GyroscopeHardware as gyro
actor SunSensorHardware as sun
actor ThrusterHardware as thrust

usecase "FR-001: ReceiveGroundCommand" as uc1
usecase "FR-002: FetchGyroData" as uc2
usecase "FR-003: CollectSensorData" as uc3
usecase "FR-004: DetermineAttitude" as uc4
usecase "FR-005: ManageOperationalModes" as uc5
usecase "FR-006: HandleFaultConditions" as uc6
usecase "FR-007: ControlThrusters" as uc7
usecase "FR-008: TransmitTelemetry" as uc8

gs --> uc1 : triggers
gs --> uc8
gyro --> uc2 : provides data
sun --> uc3 : provides status
thrust --> uc7 : receives signals

uc3 .> uc4 : <<include>>
uc4 .> uc5 : <<include>>
uc5 ..|> uc7 : <<extend>> at 128ms
uc6 .> uc5 : <<extend>> on fault
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class InterfaceAddressTable {
  - static SERIAL_COMMAND : uint = 0x88DA  
  - static GYROSCOPE : uint = 0x881A
  - static TELEMETRY : uint = 0x88DB
  + getAddress(portType)
}

class SensorData {
  - sun_angle : uint16
  - gyro_pulse_count : uint16
  - thruster_status : bool[12]
  - SP_signal : uint8
  + validate() : bool
}

class AttitudeComputer {
  - angular_velocity : float[3]
  - attitude_angle : float[3]  
  + compute(sensor: SensorData)
}

class ModeManager {
  - current_mode : {RDSM, PASM, RASM, CSM}
  - duration_counter : uint32
  - transition_table : StateTransition[]
  + evaluateTransition(sensor: SensorData)
}

class FaultLogger {
  - log_buffer[128]
  - head : uint8
  + record(code: uint8, action: uint8)
}

AttitudeComputer "1" *-- "1" SensorData : consumes
ModeManager "1" *-- "1..*" StateTransition : uses
FaultLogger --> SensorData : checks
InterfaceAddressTable ..> SerialDriver : injected dependency
@enduml
```

3. Object — Logic View: Object Diagram  
```plantuml
@startuml ObjectDiagram

object "sensor1 : SensorData" as sensor1 {
  FR-003 Instance
  --
  sun_angle = 0x3A1
  gyro_pulse_count = 428
  thruster_status = "true,false,..."
  SP_signal = 0x07
}

object "attitude1 : AttitudeComputer" as attitude1 {
  FR-004 Computation
  --
  angular_velocity = "[0.01,0,0.02]"
  attitude_angle = "[12.3,0,45.6]"
}

object "mode1 : ModeManager" as mode1 {
  FR-005 Execution
  --
  current_mode = RDSM
  duration_counter = 3
}

sensor1 -- attitude1
attitude1 -- mode1

@enduml
```

4. State — Logic View: State Diagram  
```plantuml
@startuml StateDiagram
[*] --> RDSM : Initialize

state RDSM {
  [*] --> Active : STANDBY
}

state PASM {
  [*] --> Orientation : SUN_VISIBLE
}

RDSM --> PASM : SUN_VISIBLE=0 \n&& duration>threshold
PASM --> RDSM : VELOCITY>0.02°/s
state FaultRecovery {
  [*] --> PowerCycleGyro : GYRO_ERROR
}

PASM --> FaultRecovery : 5x CommError
FaultRecovery --> PASM : RecoveryComplete
@enduml
```

## ProcessView  
5. Activity — Process View: Activity Diagram  
```plantuml
@startuml ActivityDiagram
start
:32ms ISR 5x;
partition 160ms_Cycle {
  :Receive ground command;
  :Fetch gyro data **>5ms delay**;
  :Collect sensor data;
  :Compute attitude;
  group within 128ms±1ms
    :Control thrusters;
  end group
  :Manage modes;
  :Transmit telemetry **<5µs/byte**;
}
:Log faults **if detected**;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram  
```plantuml
@startuml SequenceDiagram
participant GroundStation
participant CommandHandler
participant GyroDriver
participant ModeManager
participant ThrusterController

autonumber 1 
GroundStation -> CommandHandler: FR-001: CommandFrame(0x88DA)
CommandHandler -> ModeManager: setMode() **if valid**
GyroDriver -> CommandHandler: FR-002: sendCmd(0xEB91)
activate GyroDriver
hnote over GyroDriver: Wait >5ms
GyroDriver -> CommandHandler: GyroData(0x881A)
deactivate GyroDriver
ModeManager -> ThrusterController: FR-007: setThrusters() **@128ms±1ms**
@enduml
```

```plantuml
@startuml SequenceDiagram_Fault
participant SensorMonitor
participant FaultManager
participant ThrusterController
participant FaultLogger

autonumber 1 
SensorMonitor -> FaultManager: FR-006: ThrusterError()
FaultManager -> ThrusterController: shutdownJets() **<1s/5s**
FaultManager -> FaultLogger: record(FAULT_CODE)
hnote over FaultLogger : RAM≥128 entries
@enduml
```

7. Collaboration — Process View: Collaboration Diagram  
```plantuml
@startuml CollaborationDiagram
participant GroundStation
participant CommandHandler as CH
participant ModeManager as MM
participant ThrusterController as TC

GroundStation -[#0000FF]-> CH: 1: CommandByte**
CH -[#0000FF]-> MM: 2: setOperatingMode()
MM -[#FF0000]-> TC: 3: setThrusters()@128ms
note bottom 
  ** Scenario: Normal operation flow
  //FR-001 receipt leads to thruster adjustment//
end note
@enduml
```

## DevelopmentView  
8. Package — Development View: Package Diagram  
```plantuml
@startuml PackageDiagram
package HAL {
  [SerialDriver]
  [InterfaceTable]
}

package Sensors {
  [GyroDriver]
  [SunSensor]
}

package Control {
  [AttitudeComputer]
  [ModeEngine]
  [FaultManager]
}

package Actuators {
  [ThrusterController]
}

package Util {
  [DataContracts]
  [FaultLogger]
}

HAL - Sensors
Sensors - Control
Control - Actuators
Util -up-> DataContracts : verifies
@enduml
```

9. Component — Development View: Component Diagram  
```plantuml
@startuml ComponentDiagram

' ===== Components =====
component "SerialDriver\n<<singleton>>" as SD
component "ModeEngine" as ME
component "DataValidator" as DV

' ===== Interfaces =====
interface ISerial
interface IMode
interface IValidator

' ===== Provided Interfaces =====
SD - ISerial
ME - IMode
DV - IValidator

' ===== Required Interfaces =====
SD ..> IMode : uses

' ===== Internal mapping (optional clarity) =====
IMode - ME

' ===== Requirement Trace =====
note right of DV
  <<trace>>
  ASR-004
  enforces schema validation
end note

@enduml
```

## PhysicalView  
10. Deployment — Physical View: Deployment Diagram  
```plantuml
@startuml

node "Satellite Computer" {
  artifact "CPU (80C32E, 11.0592MHz)" as CPU
  artifact "PROM (32KB)"
  artifact "SRAM (8KB)"
}

node "Gyroscope" as GYRO
node "Sun Sensors" as SS
node "Thrusters" as TH

CPU -- GYRO : RS-422
CPU -- SS : ADC
CPU -- TH : Digital Control

@enduml
```

11. Container — Physical View: Container Diagram  
```plantuml
@startuml ContainerDiagram
container "Flight Software" {
  component CommandParser
  component AttitudeEstimator
  component PulseWidthController
  database "FaultLog" as FL
}

container "Ground Station" as Gs {
  component CommandInitiator
}

Gs -> CommandParser : UDP/Serial @160ms
PulseWidthController -> Gyroscope : Serial(0x881A) >5ms delay
AttitudeEstimator .> FL : writes logs
@enduml
```