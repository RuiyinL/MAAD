### Architecture Summary & Quality-Attribute Analysis  
**Proposed Architecture**: A **layered event-driven architecture** with **CQRS patterns** for real-time control systems, leveraging **microservices** for critical components (authentication, safety validation, command routing). The system uses hierarchical command routing (TSU > FCU > DCU), atomic rollback for safety interlocks, and dual-admin workflows for security-critical operations.  

**Quality Attributes & Trade-offs**:  
1. **Reliability/Availability** (ASR-001, NFR-001):  
   - *Tactic*: Active-active redundancy with automated failover.  
   - *Risk*: Failover latency (<10min) conflicts with lock TTL constraints (ASR-003).  
2. **Security** (NFR-002, NFR-005, ASR-002):  
   - *Tactic*: SHA-256 enforcement + dual-auth overrides.  
   - *Trade-off*: Cryptographic overhead increases latency (vs. NFR-004).  
3. **Performance** (NFR-003, NFR-004):  
   - *Tactic*: Degraded-mode throttling + event-sourcing.  
   - *Tension*: Real-time latency (≤2s) vs. overload degradation.  
4. **Safety** (ASR-003, ASR-004):  
   - *Tactic*: Atomic rollback + time-synchronized locks.  
   - *Risk*: Clock drift (>150ms) triggers false alerts.  
5. **Maintainability** (FR-008, FR-009):  
   - *Tactic*: Versioned configuration schemas + audit logs.  

**Architectural Styles**:  
- **Event-Driven + CQRS**: Separates command execution (FR-006) from real-time status queries (FR-003).  
- **Layered Microservices**: Isolates security-critical components (Auth, Safety) for ASR-002 compliance.  
- **Hybrid Rationale**: CQRS handles write/read segregation for device overrides (FR-004) and status displays; microservices enable dual-admin workflows (FR-008) without monolithic bottlenecks.  

### Patterns & Tactics  
1. **Patterns**:  
   - **Broker** (Event bus for device monitoring FR-010)  
   - **Circuit Breaker** (Degraded mode per NFR-003)  
   - **Repository** (ConfigChangeLog for FR-008)  
   - **Strategy** (SafetyRule validation FR-005)  
2. **Tactics**:  
   - Replication (NFR-001): Service replicas for FCU/DCU controllers.  
   - Caching (NFR-004): Device status snapshots.  
   - Authentication (NFR-005): SHA-256 migration with lockout.  
   - Atomic Rollback (ASR-004): Compensating transactions.  

---

## ScenarioView  
1. UseCase — Scenario View: Use Case Diagram  
```plantuml
@startuml UseCaseDiagram  
left to right direction  
actor EndUser as EU  
actor Admin as AD  
actor System as SY  
usecase (Authenticate) as UC1  
usecase (RequestCommandControl) as UC2  
usecase (GrantCommandControl) as UC3  
usecase (HandoverFeedback) as UC4  
usecase (ViewStatus) as UC5  
usecase (OverrideDevice) as UC6  
usecase (ValidateSafetyRule) as UC7  
usecase (ExecuteSequence) as UC8  
usecase (ManageAlarm) as UC9  
usecase (ChangeConfig) as UC10  
usecase (GenerateReport) as UC11  
usecase (MonitorDevice) as UC12  
EU --> UC1  
EU --> UC2  
EU --> UC5  
EU --> UC6  
EU --> UC8  
EU --> UC9  
AD --> UC1  
AD --> UC3  
AD --> UC7  
AD --> UC10  
AD --> UC11  
SY --> UC9  
SY --> UC12  
UC2 .> UC3 : <<extend>>  
UC3 .> UC4 : <<include>>  
note right of UC3: Approval required if high-security  
@enduml  
```  

## LogicView  
2. Class — Logic View: Class Diagram  
```plantuml  
@startuml ClassDiagram  
class User {  
  -username: String  
  -passwordHash: String  
  -lockedUntil: DateTime  
  +login()  
  +upgradePassword()  
}  

class CommandControl {  
  -requestId: UUID  
  -status: Enum  
  +grantControl()  
  +handover()  
}  

class Device {  
  -deviceId: String  
  -status: String  
  -overrideColor: String  
  +updateStatus()  
}  

class SafetyRule {  
  -schemaVersion: String  
  -signature: String  
  +validate()  
}  

class ConfigChangeLog {  
  -changeId: UUID  
  -oldValue: String  
  -newValue: String  
  +rollback()  
}  

class Alarm {  
  -alarmId: String  
  -triggeredAt: DateTime  
  +resolve()  
}  

User "1" --> "0..*" CommandControl  
CommandControl "1" --> "1..*" Device  
SafetyRule "1" --> "1" CommandControl  
ConfigChangeLog "1" --> "1" User : dual-auth  
Alarm "1" --> "1" Device  
note top of SafetyRule: «immutable»\nSchema v1.0 enforced  
note bottom of ConfigChangeLog: «persisted»\nAtomic rollback  
@enduml  
```  

3. Object — Logic View: Object Diagram  
```plantuml  
@startuml

object "user1 : User" as user1 <<Authenticate>> {
  username = "ops1"
  passwordHash = "sha256$..."
}

object "cmdCtrl1 : CommandControl" as cmdCtrl1 <<RequestCommandControl>> {
  status = "REQUESTED"
}

object "device1 : Device" as device1 <<OverrideDevice>> {
  deviceId = "DCU-7"
  overrideColor = "RED"
}

user1 --> cmdCtrl1
cmdCtrl1 --> device1

@enduml
```  

4. State — Logic View: State Diagram  
```plantuml  
@startuml StateDiagram  
[*] --> Idle  
Idle --> Requested : requestControl()  
Requested --> Granted : grantControl()  
Granted --> HandedOver : handover()  
HandedOver --> Idle : releaseControl()  
Granted --> Idle : releaseControl()  
Requested --> Idle : cancelRequest()  
note right of Granted : Dual-auth required\nper ASR-002  
@enduml  
```  

## ProcessView  
5. Activity — Process View: Activity Diagram  
```plantuml  
@startuml ActivityDiagram  
start  
:User requests command control;  
if (High-security?) then  
  :Require admin approval;  
else  
endif  
:Grant control;  
:Log handover event;  
:Update UI feedback;  
stop  
note right: Timeout: 2s UI update (NFR-004)  
@enduml  
```  

6. Sequence — Process View: Sequence Diagram  
```plantuml  
@startuml SequenceDiagram  
actor EndUser  
participant GUI  
participant CommandService  
participant AuthService  
database ConfigDB  

EndUser -> GUI: Request command control  
GUI -> CommandService: controlRequest(userId)  
CommandService -> AuthService: validatePermissions(userId)  
AuthService -> ConfigDB: readUserSecurityLevel()  
AuthService --> CommandService: validationResult  
CommandService -> ConfigDB: logGrantEvent()  
CommandService --> GUI: confirmation  
GUI --> EndUser: display handover feedback  
note over CommandService,ConfigDB: Atomic write per ASR-004  
@enduml  
```  

```plantuml  
@startuml SequenceDiagram  
actor Admin  
participant SafetyService  
participant RuleValidator  
database SafetyDB  

Admin -> SafetyService: submitSafetyRule(rule)  
SafetyService -> RuleValidator: validateSchema(rule)  
RuleValidator --> SafetyService: schemaValid  
SafetyService -> SafetyDB: lockRuleTable()  
SafetyService -> SafetyDB: writeRule(rule)  
SafetyService --> Admin: successNotification  
note over SafetyService,SafetyDB: Dual-auth write per FR-005  
@enduml  
```  

7. Collaboration — Process View: Collaboration Diagram  
```plantuml  
@startuml CollaborationDiagram  
component GUI  
component CommandService  
component AuthService  
component ConfigDB  
component SafetyService  

GUI -- CommandService : 1: controlRequest()  
CommandService -- AuthService : 2: validatePermissions()  
AuthService -- ConfigDB : 3: querySecurityLevel()  
CommandService -- ConfigDB : 4: logEvent()  
CommandService -- SafetyService : 5: verifySafety()  
note bottom: Scenario: Command control workflow  
@enduml  
```  

## DevelopmentView  
8. Package — Development View: Package Diagram  
```plantuml  
@startuml PackageDiagram  
package "UI Layer" as UI {  
  [GUI]  
}  

package "Application Layer" as APP {  
  [CommandControl]  
  [Auth]  
  [Safety]  
}  

package "Domain Layer" as DOM {  
  [User]  
  [Device]  
}  

package "Infrastructure" as INF {  
  [Persistence]  
  [Logging]  
}  

UI --> APP : depends  
APP --> DOM : depends  
APP --> INF : depends  
note top of APP: [HighAvailability]\nRedundant instances  
@enduml  
```  

9. Component — Development View: Component Diagram  
```plantuml  
@startuml ComponentDiagram  
component AuthComponent {  
  interface IAuthentication  
}  

component CommandComponent {  
  interface ICommandControl  
}  

component SafetyComponent {  
  interface ISafetyValidation  
}  

component ReportComponent {  
  interface IReportGen  
}  

IAuthentication -- AuthComponent  
ICommandControl -- CommandComponent  
ISafetyValidation -- SafetyComponent  
CommandComponent .> IAuthentication : requires  
ReportComponent .> ICommandControl : requires  
note bottom of SafetyComponent: [SecurityCritical]\nDual-auth enforcement  
@enduml  
```  

## PhysicalView  
10. Deployment — Physical View: Deployment Diagram  
```plantuml  
@startuml DeploymentDiagram  
node "Primary DC" {  
  artifact FCU_Controller  
  artifact DCU_Controller  
  database PostgreSQL  
}  

node "Secondary DC" {  
  artifact FCU_Controller  
  artifact DCU_Controller  
  database PostgreSQL  
}  

node NTP_Server  

FCU_Controller -[dashed]-> NTP_Server : sync  
PostgreSQL -[#red]-> PostgreSQL : replication  
note right: Failover <10min (ASR-001)  
@enduml  
```  

11. Container — Physical View: Container Diagram  
```plantuml  
@startuml

skinparam componentStyle rectangle

component "Web UI\n[React]\nStatus display" as WebUI
component "API Gateway\n[Spring Cloud]\nRouting" as APIGW
component "Auth Service\n[NodeJS]\nAuthN/Z" as Auth
component "Command Service\n[Java]\nCommand execution" as Command
component "Database\n[PostgreSQL]\nPersistence" as DB

WebUI --> APIGW : HTTPS
APIGW --> Auth : gRPC
APIGW --> Command : gRPC
Command --> DB : JDBC

note left of Command
  Latency < 2s
  <<NFR-004>>
end note

@enduml
```