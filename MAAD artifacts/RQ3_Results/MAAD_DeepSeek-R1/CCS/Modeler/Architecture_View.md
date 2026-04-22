## Architecture Summary & Quality-Attribute Analysis
**Proposed Architecture:** Master/Slave architecture with redundant stateful Masters (ASR-001, ASR-003) and a Virtual Correlator Interface (VCI) gateway (ASR-002). Deterministic real-time processing occurs at Slave nodes (CMIB controllers), while the Master handles aggregation and network resilience. Features include network segmentation (ASR-004), encrypted audit logging (ASR-008), durable spooling (ASR-009), and OpenAPI-defined contracts (FR-002, FR-013).

**Key Quality Attributes:**
1. **Performance** (NFR-001):  
   - *Tactic:* Isolate real-time processing in Slaves  
   - *Risk:* VCI translation latency  
   - *Trade-off:* Accept quasi-real-time in Master for network resilience

2. **Reliability** (FR-008, ASR-005):  
   - *Tactic:* Redundant Masters + 24h spooling  
   - *Risk:* State replication complexity  
   - *Trade-off:* Increased storage vs zero data loss  

3. **Security** (ASR-008, FR-015):  
   - *Tactic:* VCI as security choke-point  
   - *Risk:* Overhead from cryptographic controls  
   - *Trade-off:* Strict access vs debug flexibility  

4. **Maintainability** (NFR-002, ASR-007):  
   - *Tactic:* Hot-swappable modules  
   - *Risk:* Auto-recovery race conditions  
   - *Trade-off:* Modularity vs hardware abstraction  

5. **Availability** (ASR-003, ASR-009):  
   - *Tactic:* Primary/secondary failover  
   - *Risk:* Split-brain scenarios  
   - *Trade-off:* State continuity complexity  

**Architectural Style:** Layered + Event-Driven Hybrid  
- *Justification:*  
  - **Layered:** Isolates translation (VCI), coordination (Master), and real-time processing (Slaves) per ASR-001/ASR-002  
  - **Event-Driven:** Handles asynchronous fault recovery (FR-003) and spooling (FR-006) via durable queues  

---

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram  
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Operator
actor MaintenanceEngineer
actor ExternalSystem
rectangle System {
  Operator --> (Translate Configuration)
  Operator --> (View Alarm Overlays)
  MaintenanceEngineer --> (Perform Debug Access)
  MaintenanceEngineer --> (Trace Hardware Faults)
  ExternalSystem --> (Deliver External Feeds)
  ExternalSystem --> (Export Secured Data)
  
  (Translate Configuration) .> (Package Control Data) : <<include>>
  (Perform Debug Access) .> (Log Audit Trail) : <<include>>
  (Trace Hardware Faults) .> (Render Isolation Guidance) : <<extend>>
}
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram  
```plantuml
@startuml ClassDiagram
class VCIGateway {
  +translateConfiguration(schema: JSON): void
  +authenticateRequest(): boolean
}
class MasterController {
  -stateVersion: int
  +replicateState(): void
  +routeToSlave(command: string): void
}
class CMIBController {
  -hardwareState: string
  +processRealTimeCommand(): void
  +autoRecoverFault(): void
}
class SpoolManager {
  -bufferSize: int
  +spoolMonitorData(): void
  +alertStorageFull(): void
}
class AuditLogger {
  +logAccessAttempt(user: string): void
  +encryptLog(): void
}

VCIGateway --> MasterController : routes to
MasterController "1" *-- "many" CMIBController : controls
MasterController --> SpoolManager : delegates
SpoolManager --> AuditLogger : notifies
CMIBController --> AuditLogger : reports faults

note top of VCIGateway: «gateway»\nEnforces ASR-002
note bottom of CMIBController: «real-time»\nNFR-001 ≤2ms
note right of SpoolManager: ASR-005\n24h buffer
@enduml
```

3. Object — Logic View: Object Diagram  
```plantuml
@startuml
!theme plain

object "gateway : VCIGateway" as GW <<Ingress>>

object "master1 : MasterController" as M1 <<FR-Routing>> {
  stateVersion = 42
}

object "cmib23 : CMIBController" as C1 <<Runtime>> {
  hardwareState = "NORMAL"
}

object "spooler : SpoolManager" as S1 <<Buffer>> {
  bufferSize = 95
}

object "faultRecovery : CMIBController" as C2 <<AutonomousFaultRecovery>> {
  hardwareState = "FAILED"
}

GW --> M1 : routes
M1 --> C1 : controls
M1 --> S1 : manages state
C1 --> S1 : log fault event

note right of C2
  Failure scenario:
  autonomous recovery triggered
  <<ASR-007>>
end note

@enduml
```

4. State — Logic View: State Diagram  
```plantuml
@startuml StateDiagram
[*] --> Initializing : PowerOn
Initializing --> Normal: / initHardware()
Normal --> FaultDetected: HardwareError
FaultDetected --> Recovering: TimerStart
Recovering --> Normal: HeartbeatRestored\n/ validateChecksum()
Recovering --> Maintenance: ManualIntervention
Maintenance --> Normal: HotSwapComplete
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram  
```plantuml
@startuml ActivityDiagram
start
:Receive External Feed;
fork
  :Translate via VCI;
fork again
  :Spool to Local Storage;
  note right: ASR-009 Durable Spooling
end fork
:Package with Control Data;
:Route to CMIB Controller;
if (Fault Detected?) then (yes)
  :Start Recovery Timer;
  :Auto-Recover Hardware;
  -[#blue,dashed]-> Security;
else (no)
endif
:Generate Heartbeat;
:Validate Checksum;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram  
```plantuml
@startuml SequenceDiagram_HardwareRecovery
actor Operator
participant VCI
participant Master
participant CMIB
participant Spooler

Operator -> VCI: Submit Config Update
VCI -> Master: Translated Schema
Master -> CMIB: Deploy Config
CMIB --> Master: ConfigACK
CMIB -> CMIB: Detect Fault
CMIB -> Master: Fault Alert
Master -> Spooler: Buffer State
Master -> CMIB: Initiate Recovery
CMIB --> Master: Heartbeat Restored
@enduml
```

```plantuml
@startuml SequenceDiagram_DebugAccess
actor Maintenance
participant VCI
participant AuthService
participant Logger
database AuditDB

Maintenance -> VCI: Debug Request
VCI -> AuthService: Validate Role
AuthService --> VCI: AccessGranted
VCI -> Logger: Log Attempt
Logger -> AuditDB: Persist Log
AuditDB --> Logger: WriteConfirm
Logger --> VCI: LogSuccess
VCI -> Master: Enable Debug
@enduml
```

7. Collaboration — Process View: Collaboration Diagram  
```plantuml
@startuml CollaborationDiagram_HardwareRecovery
component Operator
component VCI
component Master
component CMIB
component Spooler

Operator -- VCI : 1: Submit Config
VCI -- Master : 2: Translated Schema
Master -- CMIB : 3: Deploy Config
CMIB -- CMIB : 4: Detect Fault
CMIB -- Master : 5: Fault Alert
Master -- Spooler : 6: Buffer State
Master -- CMIB : 7: Initiate Recovery
note right: Scenario: FR-008 Hardware Failure Recovery
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram  
```plantuml
@startuml PackageDiagram
package "API Layer" {
  [VCIGateway]
  [OpenAPI Contracts]
}
package "Control Layer" {
  [MasterController]
  [FailoverManager]
}
package "Hardware Abstraction" {
  [CMIBDriver]
  [RegisterMapper]
}
package "Persistence" {
  [SpoolService]
  [AuditLogger]
}

"API Layer" --> "Control Layer"
"Control Layer" --> "Hardware Abstraction"
"Hardware Abstraction" --> "Persistence"
note top of "API Layer": ASR-002 Single Access Point
note bottom of "Persistence": ASR-005 Offline Operation
@enduml
```

9. Component — Development View: Component Diagram  
```plantuml
@startuml ComponentDiagram
component VCIGateway {
  interface ConfigAPI
}
component MasterController {
  interface SlaveCoordinator
}
component CMIBDriver {
  interface HardwareRegister
}
component SpoolService {
  interface BufferAPI
}
component AuditService {
  interface LogWriter
}

VCIGateway::ConfigAPI -- MasterController::SlaveCoordinator
MasterController::SlaveCoordinator -- CMIBDriver::HardwareRegister
CMIBDriver .> SpoolService::BufferAPI : uses
SpoolService::BufferAPI .> AuditService::LogWriter : notifies
note left of VCIGateway: «security»\nASR-008
note right of CMIBDriver: «real-time»\nNFR-001
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram  
```plantuml
@startuml DeploymentDiagram
node "Master Network" {
  artifact PrimaryMaster : MasterController
  artifact SecondaryMaster : MasterController
  database StateDB
}
node "CMIB Cluster" {
  artifact CMIB1 : CMIBController
  artifact CMIB2 : CMIBController
}
node "Security Zone" {
  artifact VCI : VCIGateway
  artifact AuditVault : EncryptedStorage
}

PrimaryMaster -[hidden]-> SecondaryMaster : heartbeat
PrimaryMaster --> CMIB1 : 100Mbps Fiber
PrimaryMaster --> CMIB2 : 100Mbps Fiber
VCI --> PrimaryMaster : HTTPS
CMIB1 --> AuditVault : Syslog
note on link: ASR-004 Segregated Interfaces
@enduml
```

11. Container — Physical View: Container Diagram  
```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle

component "VCI Gateway\n[Nginx / TLS]\nSchema translation + AuthZ" as VCI
component "Master Control\n[Java / Quarkus]\nState replication + Routing" as MASTER
component "CMIB Runtime\n[C++ / RTOS]\nHardware control" as CMIB
component "Spool Storage\n[Redis]\n24h buffer" as SPOOL
component "Audit Service\n[AWS S3]\nEncrypted logs" as AUDIT

VCI --> MASTER : OpenAPI 3.0
MASTER --> CMIB : Protobuf
CMIB --> SPOOL : JSON
SPOOL --> AUDIT : Encrypted Stream

note left of VCI
  ASR-002: Single Access
end note

note right of CMIB
  ASR-007: Hot-Swap
end note

@enduml
```