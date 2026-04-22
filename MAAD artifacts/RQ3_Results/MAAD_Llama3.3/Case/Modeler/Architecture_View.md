## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase
actor EndUser as "End User"
actor Admin as "Admin"
actor Nurse as "Nurse"

usecase "Patient Monitoring" as (PatientMonitoring)
usecase "Notification of Nurses' Station" as (NotificationOfNursesStation)
usecase "Secure Door Control" as (SecureDoorControl)
usecase "Turnstile System Operation" as (TurnstileSystemOperation)
usecase "Home Heating System Regulation" as (HomeHeatingSystemRegulation)

EndUser -- (PatientMonitoring)
Admin -- (SecureDoorControl)
Nurse -- (NotificationOfNursesStation)
EndUser -- (TurnstileSystemOperation)
EndUser -- (HomeHeatingSystemRegulation)

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class
class Patient {
  - id: string
  - name: string
  - vitals: Vitals
}

class Vitals {
  - pulse: int
  - temperature: float
  - bloodPressure: BloodPressure
}

class BloodPressure {
  - systolic: int
  - diastolic: int
}

class Nurse {
  - id: string
  - name: string
}

class Notification {
  - patientId: string
  - factor: string
  - value: string
  - threshold: string
  - timestamp: datetime
  - errorCode: string
}

Patient "1" --* Vitals
Vitals "1" --* BloodPressure
Nurse "1" --* Notification

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object
object patient1 : Patient
object vitals1 : Vitals
object bloodPressure1 : BloodPressure
object nurse1 : Nurse
object notification1 : Notification

patient1 -- vitals1
vitals1 -- bloodPressure1
nurse1 -- notification1

patient1 : id = "1"
patient1 : name = "John Doe"
vitals1 : pulse = 120
vitals1 : temperature = 37.5
bloodPressure1 : systolic = 120
bloodPressure1 : diastolic = 80
nurse1 : id = "1"
nurse1 : name = "Jane Doe"
notification1 : patientId = "1"
notification1 : factor = "pulse"
notification1 : value = "120"
notification1 : threshold = "100"
notification1 : timestamp = "2023-03-01 12:00:00"
notification1 : errorCode = "OUT_OF_RANGE"

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State
state PatientMonitoring {
  state Idle
  state Monitoring
  state Alert
}

state SecureDoorControl {
  state Locked
  state Unlocked
}

PatientMonitoring : Idle --> Monitoring : startMonitoring()
PatientMonitoring : Monitoring --> Alert : outOfRange()
PatientMonitoring : Alert --> Monitoring : reset()
SecureDoorControl : Locked --> Unlocked : unlock()
SecureDoorControl : Unlocked --> Locked : lock()

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity
start
:Start Patient Monitoring;
if (out of range?) then
  :Send Notification to Nurse;
else
  :Continue Monitoring;
endif
:Stop Patient Monitoring;
stop

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml Sequence1
participant Patient as "Patient"
participant Nurse as "Nurse"
participant System as "System"

Patient->>System: startMonitoring()
System->>Patient: monitorVitals()
Patient->>System: sendVitals(pulse=120, temperature=37.5, bloodPressure=systolic=120, diastolic=80)
System->>Nurse: sendNotification(patientId="1", factor="pulse", value="120", threshold="100", timestamp="2023-03-01 12:00:00", errorCode="OUT_OF_RANGE")

@enduml
```

```plantuml
@startuml Sequence2
participant Admin as "Admin"
participant System as "System"
participant Door as "Door"

Admin->>System: unlockDoor()
System->>Door: unlock()
Door->>System: unlocked()
System->>Admin: doorUnlocked()

@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration1
participant Patient
participant System
participant Nurse

Patient ->> System: startMonitoring()
System ->> Patient: monitorVitals()
Patient ->> System: sendVitals(pulse=120, temperature=37.5, bloodPressure(systolic=120, diastolic=80))
System ->> Nurse: sendNotification(patientId="1", factor="pulse", value="120", threshold="100", timestamp="2023-03-01 12:00:00", errorCode="OUT_OF_RANGE")

@enduml
```

```plantuml
@startuml Collaboration2
participant Admin
participant System
participant Door

Admin ->> System: unlockDoor()
System ->> Door: unlock()
Door ->> System: unlocked()
System ->> Admin: doorUnlocked()

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package
package PatientMonitoring {
  class Patient
  class Vitals
  class BloodPressure
}

package SecureDoorControl {
  class Door
  class Lock
}

package Notification {
  class Notification
  class Nurse
}

PatientMonitoring --* SecureDoorControl
SecureDoorControl --* Notification

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component
component PatientMonitoringComponent {
  interface PatientMonitoringInterface
  class Patient
  class Vitals
  class BloodPressure
}

component SecureDoorControlComponent {
  interface SecureDoorControlInterface
  class Door
  class Lock
}

component NotificationComponent {
  interface NotificationInterface
  class Notification
  class Nurse
}

PatientMonitoringComponent --* SecureDoorControlComponent
SecureDoorControlComponent --* NotificationComponent

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment
node PatientMonitoringNode {
  component PatientMonitoringComponent
}

node SecureDoorControlNode {
  component SecureDoorControlComponent
}

node NotificationNode {
  component NotificationComponent
}

PatientMonitoringNode --* SecureDoorControlNode
SecureDoorControlNode --* NotificationNode

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container
artifact PatientMonitoringContainer {
  component PatientMonitoringComponent
  database PatientMonitoringDatabase
}

artifact SecureDoorControlContainer {
  component SecureDoorControlComponent
  database SecureDoorControlDatabase
}

artifact NotificationContainer {
  component NotificationComponent
  database NotificationDatabase
}

PatientMonitoringContainer --* SecureDoorControlContainer
SecureDoorControlContainer --* NotificationContainer

@enduml
```