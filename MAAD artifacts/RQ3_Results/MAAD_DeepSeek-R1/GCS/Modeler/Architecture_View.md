## Architecture Summary & Quality-Attribute Analysis

**Proposed Architecture**: A distributed layered architecture with microkernel pattern for operational control, combining:
- Real-time subsystem (IOC layer) for hardware control
- Centralized configuration management via EPICS-compatible database
- Microservices for user management/instrument control
- Event-driven fault handling
- API gateway for visitor instruments

**Quality Attribute Analysis**:
1. **Reliability** (ASR-005/006, NFR-006/007)
   - Tactic: Hardware interlocks + state persistence
   - Risk: Recovery time objective conflicts with safety transition timing
   - Trade-off: Redundancy vs hardware independence mandate

2. **Safety** (ASR-002/006)
   - Tactic: Hardware-enforced state machines
   - Risk: Software/hardware coordination latency
   - Tension: Atomic transitions vs logging overhead

3. **Performance** (ASR-004, NFR-001/003/008)
   - Tactic: Cyclic executives + caching
   - Risk: 128ms thruster cycle conflicts with 100 TPS control throughput
   - Trade-off: Data freshness vs caching depth

4. **Security** (FR-001, NFR-009)
   - Tactic: Mutual TLS + LDAP attribute mapping
   - Risk: Role mapping latency impacting command response SLO

5. **Scalability** (ASR-001, NFR-005)
   - Tactic: Location-based routing
   - Tension: Hierarchical communication vs parallel instrument ops

## Architectural Style & Rationale
**Hybrid Style**: Layered + Microkernel + Event-Driven  
- **Layered architecture** (ASR-007): Configuration DB layer supports maintainability  
- **Microkernel** (ASR-002/004): Central policy engine for operational levels/instrument control  
- **Event-driven** (NFR-006): Fault notification broker satisfies 10s SLO  
*Justification*:  
- Hardware control isolation (ASR-004/006) requires microkernel  
- Distributed operations (ASR-001) needs layered decoupling  
- Fault handling (NFR-006) mandates event bus  

## Architecture Patterns & Tactics
**Patterns**:  
1. **State Machine** (FR-002/ASR-002): Enforces operational levels  
2. **Broker** (NFR-006): Routes fault events  
3. **CQRS** (NFR-003): Separates command/status paths  

**Tactics**:  
- **Hardware Interlocks** (ASR-006): Dedicated safety subsystem  
- **Cyclic Executive** (ASR-004): Time-triggered scheduler  
- **LDAP Attribute Caching** (FR-001): Pre-fetched role mapping  
- **Deadlock Monitor** (ASR-003): Nightly conflict scanner  

---

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Astronomer
actor ScienceObserver
actor TelescopeOperator
actor SupportPersonnel
actor Developer
actor Administrator
actor VisitorInstrument as "VisitorInstrument (External)"

usecase "Authenticate via LDAP" as UC1
usecase "Set Operational Level" as UC2
usecase "Control Active Instrument" as UC3
usecase "Monitor Fault Events" as UC4
usecase "Execute Preprogrammed Sequence" as UC5
usecase "Access Configuration DB" as UC6
usecase "Perform Safety Transition" as UC7
usecase "Acquire Instrument Status" as UC8

Astronomer --> UC3
Astronomer --> UC5
ScienceObserver --> UC3
TelescopeOperator --> UC2
TelescopeOperator --> UC7
SupportPersonnel --> UC4
SupportPersonnel --> UC6
Developer --> UC6
Administrator --> UC1
VisitorInstrument --> UC8
VisitorInstrument --> UC5

UC1 .> UC2 : <<include>>
UC2 .> UC7 : <<extend>> if safety-critical
UC3 .> UC8 : <<include>>

note right of UC2
  Precondition: Hardware interlocks engaged
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class User {
  +username: String
  +location: FacilityCode
  +authenticate()
  +getRole(): UserRole
}

class OperationalLevel {
  -currentLevel: LevelType
  +transitionLevel()
  +getCurrentLevel(): LevelType
}

class Instrument {
  +instrumentId: String
  +state: InstrumentState
  +status: JSON
  +control()
  +getStatus(): JSON
}

class ControlPolicy {
  +validateAccess()
  +enforceLevel()
  +logAccessAttempt()
}

class FaultEvent {
  +timestamp: DateTime
  +moduleId: String
  +errorCode: int
  +description: String
  +notify()
}

class ConfigurationDB {
  +getParameter()
  +updateParameter()
}

User "1" *-- "1" ControlPolicy : enforces >
OperationalLevel "1" o-- "1" ControlPolicy : uses
Instrument "1" -- "*" ControlPolicy : managed by
FaultEvent "1" -- "1" Instrument : triggers
ConfigurationDB "1" -- "*" Instrument : configures

note top of ConfigurationDB
  «persisted»
  Access time: 2-3ms (NFR-008)
end note

note bottom of ControlPolicy
  Enforces FR-001/FR-002
  and ASR-002
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml
!theme plain

object "operator1 : User" as operator1 {
  username = "op_001"
  location = "Base"
}

object "obsLevel : OperationalLevel" as obsLevel {
  currentLevel = "Observing"
}

object "gmosInstrument : Instrument" as gmosInstrument {
  instrumentId = "GMOS-S"
  state = "Acquiring"
}

object "policyEngine : ControlPolicy" as policyEngine

operator1 --> obsLevel : sets level
operator1 --> gmosInstrument : controls
policyEngine --> operator1 : validates
policyEngine --> gmosInstrument : enforces

note top of gmosInstrument
  Active instrument during FR-004 scenario
  <<ControlActiveInstrument>>
end note

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
[*] --> Maintenance
Maintenance --> Observing : / startObserving() \n guard: HardwareInterlockOK
Observing --> Test : / startCalibration()
Test --> Maintenance : / completeTest()
Observing --> [*] : EmergencyShutdown
Maintenance --> [*] : EmergencyShutdown
Test --> [*] : EmergencyShutdown

state "SafetyTransition" as ST {
  [*] --> SafeState
  SafeState --> [*] : ResetConfirmed
}

Observing --> ST : HardwareFaultDetected
Maintenance --> ST : HardwareFaultDetected
Test --> ST : HardwareFaultDetected

note left of Observing
  ASR-002: Requires supervisor
  approval for transitions
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml
!theme plain

start
:Authenticate via LDAP;

if (Role valid?) then (yes)
  :Set Operational Level\n(Observing / Maintenance / Test);

  fork
    :Control Active Instrument;
  fork again
    :Monitor Inactive Instruments;
  end fork

  :Check for adverse impact (NFR-004);

  if (Impact > 10%) then (yes)
    :Trigger Alarm;
    :Log Event;
  else (no)
  endif

  :Acquire Status Updates;
  :Update UI within 4s\n<<NFR-003>>;

else (no)
  :Log Access Violation;
  :Return HTTP 401;
endif

stop

note right
  ASR-002:
  Hardware interlocks engaged
  during transition
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
actor Astronomer as A
participant API_Gateway
participant ControlService
participant "IOC Layer" as IOC
database ConfigDB

A -> API_Gateway: SubmitCommand()
activate API_Gateway
API_Gateway -> ControlService: ForwardCommand()
activate ControlService
ControlService -> ConfigDB: getAccessPolicy()
activate ConfigDB
ConfigDB --> ControlService: Policy
deactivate ConfigDB
ControlService -> ControlService: validateAccess()
ControlService -> IOC: ExecuteCommand()
activate IOC
IOC --> ControlService: CommandAck(128ms)
deactivate IOC
ControlService --> API_Gateway: Response(within 2s)
deactivate ControlService
API_Gateway --> A: CommandResult
deactivate API_Gateway

note right of ControlService
  Satisfies ASR-004 timing
  and NFR-003 response SLO
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationDiagram
component "Operator" as Op
component "ControlPolicy" as CP
component "InstrumentController" as IC
component "SafetyMonitor" as SM
component "ConfigDB" as DB

Op -- CP : 1: validateAccess()
CP -- DB : 2: getPolicy()
CP -- IC : 3: authorizeCommand()
IC -- SM : 4: verifySafety()
SM -- IC : 5: safetyStatus
IC -- Op : 6: commandResult

note top
  Sequence for FR-002 enforcement
  and ASR-006 safety check
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package "UI Layer" {
  [Web Interface]
  [API Gateway]
}

package "Control Layer" {
  [Policy Engine]
  [Instrument Manager]
}

package "Data Layer" {
  [Configuration DB]
  [Event Logging]
}

package "Safety Layer" {
  [Hardware Interlocks]
  [Fault Monitor]
}

"UI Layer" --> "Control Layer"
"Control Layer" --> "Data Layer"
"Control Layer" --> "Safety Layer"
"Safety Layer" --> "Data Layer"

note bottom of "Data Layer"
  Centralized config management
  per ASR-007
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
component "AuthService" as AS [
  LDAP integration
  Role mapping
]

component "PolicyEngine" as PE [
  Operational level enforcement
  Access validation
]

component "InstrumentController" as IC [
  Multi-instrument coordination
  Status aggregation
]

component "FaultHandler" as FH [
  Event notification
  Log formatting
]

AS -- PE : provides auth
PE -- IC : controls access
IC -- FH : reports faults

PE -[dashed]-> "ConfigurationDB" : reads policies
FH -[dashed]-> "EventLog" : writes entries

note top of FH
  Implements NFR-006
  fault notification SLO
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node "Control Facility" as CF {
  node "K8s Cluster" {
    artifact API_Gateway
    artifact ControlServices
    artifact AuthService
  }
  node "Database Server" {
    database ConfigDB
    database EventLog
  }
}

node "Telescope Site" as TS {
  node "Real-Time Controller" {
    component IOC_Layer
    component SafetyInterlock
  }
  node "Instrument Cluster" {
    component InstrumentController
  }
}

CF -- TS : 10Gbps fiber \n [20-40 Mbits/s data]
TS -- CF : Command/Status

note on link
  Meets NFR-004 bandwidth
  and ASR-001 distributed ops
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
node "Control Node" {
  container "Web UI" as UI {
    Component ReactApp
  }
  container "API Gateway" as GW {
    Component NGINX
  }
  container "Control Service" as CS {
    Component PolicyEngine
    Component InstrumentManager
  }
  container "Database" as DB {
    Component PostgreSQL
  }
}

node "Monitoring Node" {
  container "Fault Processor" as FP {
    Component LogAggregator
    Component AlertManager
  }
}

UI --> GW : HTTPS
GW --> CS : gRPC
CS --> DB : SQL
CS --> FP : Kafka
FP --> DB : Writes

note left of DB
  ConfigurationDB with
  2-3ms access (NFR-008)
end note
@enduml
```