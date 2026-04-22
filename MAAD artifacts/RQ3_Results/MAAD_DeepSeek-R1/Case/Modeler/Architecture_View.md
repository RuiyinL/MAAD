## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram

left to right direction
actor "Medical Staff" as MS
actor "Nurse" as Nurse
actor "Zoo Visitor" as ZV
actor "System Administrator" as Admin
actor "Traffic Controller" as TCK
actor "Monitoring Devices" as MD

usecase "Acquire Patient Data" as UC1
usecase "Configure Safe Ranges" as UC2
usecase "Notify Anomaly" as UC3
usecase "Recognize Face" as UC4
usecase "Enforce Payment" as UC5
usecase "Control Traffic Light" as UC6
usecase "Configure Traffic Regimes" as UC7
usecase "Control Shuttle Movement" as UC8
usecase "Generate Traffic Report" as UC9

MS --> UC2
MD --> UC1
System --> UC1
System --> UC3
System --> UC6
System --> UC8
System --> UC9
Nurse <-- UC3
ZV --> UC4
ZV --> UC5
Admin --> UC7
TCK --> UC7

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml
!theme plain

class Patient <<persisted>> {
  -id: String
  -name: String
  +getVitalSigns()
}

class PhysiologicalFactor <<persisted>> {
  -id: String
  -type: String
  +validate()
}

class Reading <<persisted>> <<immutable>> {
  -patientId: String
  -factorId: String
  -value: float
  -timestamp: DateTime
  +store()
}

class SafeRange <<persisted>> {
  -min: float
  -max: float
  -patientId: String
  +updateRange()
}

class NotificationService <<service>> {
  -retryCount: int
  +sendHL7Message()
  +escalateAlarm()
}

class TrafficLightController <<real-time>> {
  -currentPhase: String
  +switchPhase()
  +validateRegime()
}

class TrafficPhase

Reading "1" -- "1" Patient
Reading "1" -- "1" PhysiologicalFactor
SafeRange "1" -- "1" Patient

NotificationService --> Reading : consumes
NotificationService --> SafeRange : checks

TrafficLightController "1" -- "*" TrafficPhase

note top of NotificationService
  ASR-002: 99.9% requests <2s latency
  with fallback mechanism
end note

note top of TrafficLightController
  ASR-001: Phase tolerance ±50ms
  Hardware synchronization
end note

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml
!theme plain

object "patient1 : Patient" as patient1 {
  id = "P-001"
  name = "John Doe"
}

object "pulse : PhysiologicalFactor" as pulse {
  id = "F-001"
  type = "Pulse"
}

object "reading1 : Reading" as reading1 <<AnomalyDetection>> {
  patientId = "P-001"
  factorId = "F-001"
  value = 110.0
  timestamp = "2023-10-01T08:30:00"
}

object "range1 : SafeRange" as range1 {
  min = 60.0
  max = 100.0
  patientId = "P-001"
}

object "notify1 : NotificationService" as notify1 <<SendAlert>> {
  retryCount = 3
}

patient1 -- reading1
pulse -- reading1
patient1 -- range1

notify1 ..> reading1 : consumes
notify1 ..> range1 : checks

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram

state TrafficLight {
  [*] -> BothStop : Reset
  BothStop : Entry / startTimer(50s)
  BothStop -> StopGo : timerExpired
  StopGo : Entry / startTimer(120s)
  StopGo -> BothStop2 : timerExpired
  BothStop2 : Entry / startTimer(50s)
  BothStop2 -> GoStop : timerExpired
  GoStop : Entry / startTimer(120s)
  GoStop -> BothStop : timerExpired
}

note right of BothStop
  ASR-001: Strict timing (±50ms)
  per cycle
end note

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram

start
:Acquire Patient Data;
:Store in Database;
if (Value outside Safe Range?) then (yes)
  :Format HL7 Message;
  repeat :Send to Nurse Station;
    ->async Action;
    if (NACK received?) then (yes)
      :Increment Retry Counter;
    else (no)
      :Mark Delivered;
    endif
  repeat while (Retries<3 and <2s elapsed?) is (yes) not (no)
  if (Message not delivered?) then (yes)
    :Trigger Audible Alarm;
  else (no)
  endif
else (no)
endif
stop

note left
  ASR-002: Must complete entire
  chain within 2s with 99.9% SLA
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram-AnomalyNotification

actor Device
participant AcquisitionService
participant Database
participant AnomalyDetector
participant NotificationService
participant "Nurses' Station" as NurseStation

Device -> AcquisitionService: ReadPatientData(pulse, temp)
AcquisitionService -> Database: StoreReading(FR-002)
Database --> AcquisitionService: ACK
AcquisitionService -> AnomalyDetector: CheckAnomaly(FR-004)
AnomalyDetector -> Database: FetchSafeRange
Database --> AnomalyDetector: RangeData
alt Anomaly detected
  AnomalyDetector -> NotificationService: SendAlert
  loop 3 times [RetryLogic]
    NotificationService -> NurseStation: HL7 ORU^R01
    alt NACK received
      NurseStation --> NotificationService: NACK
      NotificationService -> NotificationService: DelayRetry
    else ACK
      NurseStation --> NotificationService: ACK
      break
    end
  end
  alt Timeout after 2s
    NotificationService --> NotificationService: TriggerAlarm
  end
end

@enduml
```

```plantuml
@startuml SequenceDiagram-TrafficCycle

participant "Timer Service" as Timer
participant TrafficController
participant "Light Hardware" as Light

Timer -> TrafficController: PhaseTimeout
TrafficController -> TrafficController: DetermineNextPhase(FR-010)
TrafficController -> Light: ActivatePhase
activate Light
Light --> TrafficController: Confirmation
deactivate Light
TrafficController -> Timer: SetPhaseTimer

note right
  ASR-001: Cycle timing must be
  ±50ms for safety compliance
end note

@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationDiagram-AnomalyNotification

component Device
component AcquisitionService
component Database
component AnomalyDetector
component NotificationService
component NurseStation

Device -- AcquisitionService : 1. ReadPatientData()
AcquisitionService -- Database : 2. StoreReading()
Database -- AcquisitionService : 3. ACK
AcquisitionService -- AnomalyDetector : 4. CheckAnomaly()
AnomalyDetector -- Database : 5. FetchSafeRange
Database -- AnomalyDetector : 6. ReturnRange
AnomalyDetector -- NotificationService : 7. SendAlert
NotificationService -- NurseStation : 8. SendHL7Message
NurseStation -- NotificationService : 9. ACK/NACK

note top: ASR-002: End-to-end latency \n≤2s with 99.9% reliability
```

```plantuml
@startuml CollaborationDiagram-TrafficCycle

component TimerService
component TrafficController
component LightHardware

TimerService -- TrafficController : 1. PhaseTimeout
TrafficController -- TrafficController : 2. NextPhaseLogic
TrafficController -- LightHardware : 3. SetPhase
LightHardware -- TrafficController : 4. OperationACK
TrafficController -- TimerService : 5. ResetTimer

note top: ASR-001: Phase transitions \nmust be ±50ms accurate
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml

package "Acquisition" as ACQ {
  component PatientDataCapture
  component DeviceInterface
}

package "Processing" as PROC {
  component AnomalyDetection
  component TrafficControl
  component CommandValidator
}

package "Notification" as NOTI {
  component HL7Adapter
  component AlertScheduler
}

package "Persistence" as PERS {
  component PatientRepository
  component ConfigRepository
}

package "Security" as SEC {
  component FaceRecognition
  component AccessControl
}

ACQ --> PROC : provides data
PROC --> NOTI : emits events

ACQ --> PERS : stores data
PROC ..> PERS : reads config

SEC ..> ACQ
SEC ..> PROC
SEC ..> NOTI
SEC --> PERS

note as N1
ASR-002:
Reliability + retry logic
(99.9% delivery)
end note

N1 .. NOTI

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram

component "Patient Monitoring" as PM {
  [AcquisitionService]
  [AnomalyDetector]
  interface "ReadingObserver"
}

component "Notification Engine" as NE {
  [HL7Sender]
  [RetryManager]
}

component "Traffic Control" as TC {
  [PhaseController]
  [RegimeValidator]
}

PM -> NE : alerts via <<HL7>>
NE --> "Nurses Station" : message delivery
TC --> "Light Hardware" : control signals

note bottom of PM
  Handles FR-001, FR-002, FR-004
  with ASR-002 compliance
end note

note top of TC
  Implements ASR-001 real-time
  constraints and ASR-005
  pluggable regimes
end note

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml
!theme plain

node "Medical Data Center" as MDC {

  node "App Server Cluster" as APP {
    artifact "Patient Monitoring"
    artifact "Notification Engine"
  }

  node "RT Controller #1" as RTC1 <<real-time>> {
    artifact "Traffic Control"
  }

  node "RT Controller #2" as RTC2 <<real-time>> <<redundant>> {
    artifact "Traffic Control"
  }

  node "Database Cluster" as DB {
    artifact "PostgreSQL (Primary)" <<primary>>
    artifact "PostgreSQL (Secondary)" <<secondary>>
  }
}

cloud "Hospital Network" as HNET {
  node "Workstation" as WS {
    artifact "Config UI"
  }
  node "Nurses Station" as NS
}

node "IoT Gateway" as IOT {
  artifact "Sensors"
}

node "Traffic Light Hardware" as HW

' ===== Connections =====
IOT .up..> MDC : secure link

APP --> DB : read/write
WS --> APP : config access
APP --> NS : alerts

RTC1 --> HW : control
RTC2 --> HW : backup

note right of RTC1
  ASR-001:
  Redundant controllers
  for fault tolerance
end note

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram

container "Web App Server" {
  component [Patient Monitoring] <<Spring Boot>>
  component [Notification Service] <<Quarkus>>
}

container "Database" {
  component [PostgreSQL] <<Database>>
}

container "RT Controller" {
  component [Traffic Control] <<C++>>
}

container "IoT Gateway" {
  component [Data Collector] <<Python>>
}

queue "MQTT Bus" as MQTT {
  [PatientReadings]
}

[Patient Monitoring] --> [PostgreSQL] : JDBC
[IoT Gateway] --> MQTT : publish
[Patient Monitoring] --> MQTT : subscribe
[Notification Service] -- [Nurses Station] : HL7 over TCP
[Traffic Control] -- [Light Hardware] : GPIO/CAN

note top of Notification Service
  NFR-002: Uses AES-256 encryption
  for sensitive data
  with 90d audit retention
end note

@enduml
```