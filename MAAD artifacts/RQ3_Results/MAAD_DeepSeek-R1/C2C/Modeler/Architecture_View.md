## Architecture Summary & Quality-Attribute Analysis  
**Proposed Architecture**: A layered security-focused architecture using API Gateway pattern for TLS/mTLS enforcement, RBAC authorization, and WORM-protected audit logging. Core components include Authentication Service, Incident Service, and Audit Logger deployed on Windows NT with OPSEC hardening.  

**Key Quality Attributes**:  
1. **Security** (ASR-003/NFR-001):  
   - *Tactics*: Mutual TLS, OAuth2.1 PKCE, credential rotation  
   - *Risks*: Legacy OS vulnerabilities vs. modern crypto requirements  
   - *Trade-off*: TLS termination at gateway simplifies NT deployment but reduces end-to-end encryption  

2. **Reliability** (FR-055):  
   - *Tactics*: WORM storage, atomic audit writes  
   - *Tension*: Write durability vs. NT filesystem limitations  

3. **Compatibility** (NFR-001):  
   - *Constraints*: Windows NT SP6a dependencies  
   - *Risk*: Modern security libraries incompatible with NT  

4. **Auditability** (ASR-003/FR-055):  
   - *Tactics*: Immutable logs with operatorID-incidentId binding  
   - *Trade-off*: WORM storage complexity vs. regulatory compliance  

**Architectural Style**:  
- **API Gateway + Layered Architecture**: Centralizes security enforcement (ASR-003) while isolating NT-specific components (NFR-001)  
- **Hexagonal Pattern**: Decouples core logic from legacy OS dependencies via adapters  

---

## Architectural Patterns & Tactics  
**Patterns**:  
1. **API Gateway** (ASR-003):  
   - Handles TLS/mTLS termination and OAuth flows  
   - *Justification*: Centralizes security-critical functions  

2. **Adapter-Broker** (NFR-001):  
   - WORM storage adapter abstracts NT filesystem  
   - *Justification*: Isolates legacy OS dependencies  

3. **RBAC Enforcement** (ASR-003):  
   - Policy decision point in gateway  
   - *Justification*: Mandates operator authorization  

**Tactics**:  
- **Credential Rotation** (ASR-003):  
  Scheduled secret generator with 90-day lifecycle  
- **Schema Validation** (FR-055):  
  JSON schema enforcement at gateway  
- **OPSEC Hardening** (NFR-001):  
  Disabled services + restricted account policy  

---

## PlantUML Diagrams  

### ScenarioView  
1. UseCase  
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Operator as op
usecase "EnterIncident" as UC1
usecase "AuthenticateUser" as UC2
usecase "LogAuditEntry" as UC3

op --> UC1
UC1 --> UC2 : <<include>>
UC1 --> UC3 : <<extend>>

note right of UC1
  FR-055: Incident entry
  with auth enforcement
end note
@enduml
```

### LogicView  
2. Class  
```plantuml
@startuml ClassDiagram
class Incident {
  -incidentId: String
  -timestamp: DateTime
  -networkId: String
  -description: String
}

class AuditLog {
  -logId: String
  -operatorId: String
  -command: String
  -targetDevice: String
  -result: String
  +logEntry()
}

class Operator {
  -operatorId: String
  -credentials: String
}

class IncidentService {
  +createIncident()
  +validateSchema()
}

IncidentService "1" *-- "0..*" Incident
IncidentService "1" --> "1" AuditLog
Operator "1" --> "0..*" AuditLog

note top of IncidentService
  «security»
  Enforces ASR-003 auth
end note
@enduml
```

3. Object  
```plantuml
@startuml

object "incident1 : Incident" as incident1 {
  incidentId = "INC-2024-XYZ"
  timestamp = "2024-05-17T14:30:00Z"
  networkId = "NET-001"
  description = "Router failure"
}

object "audit1 : AuditLog" as audit1 {
  logId = "AUD-8876"
  operatorId = "OP-99"
  command = "CREATE_INCIDENT"
  targetDevice = "API_GW"
  result = "SUCCESS"
}

object "operator1 : Operator" as operator1 {
  operatorId = "OP-99"
}

incident1 -- audit1 : CreateIncident
operator1 -- audit1

@enduml
```

4. State  
```plantuml
@startuml StateDiagram
[*] --> Created : createIncident()
Created --> Validating : submit()
Validating --> Rejected : invalidSchema
Validating --> Logged : validSchema
Logged --> Archived : persist()
Archived --> [*]
@enduml
```

### ProcessView  
5. Activity  
```plantuml
@startuml ActivityDiagram
start
:Authenticate Operator;
partition SecurityCheck {
  :Validate Credentials;
}
if (Valid?) then (yes)
  :Receive JSON;
  :Validate Schema;
  if (Valid?) then (yes)
    :Persist Incident;
    :Log Audit Entry;
    stop
  else (no)
    :Return 400/BAD_SCHEMA;
  endif
else (no)
  :Reject Request;
endif
stop
@enduml
```

6. Sequence  
```plantuml
@startuml SequenceDiagram1
actor Operator
participant APIGateway
participant AuthService
participant IncidentService
participant AuditLogger

Operator -> APIGateway: createIncident(JSON)
APIGateway -> AuthService: authenticate(token)
AuthService --> APIGateway: operatorID
APIGateway -> IncidentService: validateSchema(JSON)
IncidentService --> APIGateway: validationResult
APIGateway -> IncidentService: persistIncident()
IncidentService -> AuditLogger: logEntry(operatorID, incidentID)
AuditLogger --> IncidentService: auditConfirmed
IncidentService --> APIGateway: 201/Created
APIGateway --> Operator: Success
@enduml
```

```plantuml
@startuml SequenceDiagram2
actor Operator
participant APIGateway
participant AuthService
participant IncidentService

Operator -> APIGateway: createIncident(invalidJSON)
APIGateway -> AuthService: authenticate(token)
AuthService --> APIGateway: operatorID
APIGateway -> IncidentService: validateSchema(JSON)
IncidentService --> APIGateway: schemaError
APIGateway -> AuditLogger: logFailure(operatorID)
APIGateway --> Operator: 400/BAD_SCHEMA
@enduml
```

7. Collaboration  
```plantuml
@startuml CollaborationDiagram
component Operator
component APIGateway
component IncidentService
component AuditLogger

Operator -- APIGateway : 1: createIncident()
APIGateway -- IncidentService : 2: validateSchema()
IncidentService -- AuditLogger : 3: logEntry()
APIGateway -- Operator : 4: 201/Created

note top: Successful incident creation flow
@enduml
```

### DevelopmentView  
8. Package  
```plantuml
@startuml PackageDiagram
package "Security" {
  [AuthService]
  [CredentialManager]
}

package "Domain" {
  [IncidentService]
  [AuditLogger]
}

package "Persistence" {
  [IncidentRepository]
  [WORMAdapter]
}

[Security] --> [Domain]
[Domain] --> [Persistence]
note bottom of Persistence : NFR-001: Windows NT storage\nconstraints
@enduml
```

9. Component  
```plantuml
@startuml ComponentDiagram
component [API Gateway] as GW {
  interface "REST/HTTPS" as if1
}

component [Incident Service] as IS {
  interface "IncidentMgmt" as if2
}

component [Audit Service] as AUD {
  interface "WORMWriter" as if3
}

component [Auth Service] as AUTH {
  interface "OAuth2.1" as if4
}

GW -- IS : uses
GW -- AUD : uses
GW -- AUTH : uses
note right of AUD
  «ASR-003»
  WORM-protected storage
end note
@enduml
```

### PhysicalView  
10. Deployment  
```plantuml
@startuml DeploymentDiagram
node "Isolated Subnet" {
  node "Windows NT Server" {
    artifact API_Gateway
    artifact Incident_Service
    artifact Audit_Service
  }
  
  node "WORM Storage" as STG {
    database Audit_Volume
  }
}

API_Gateway -- Audit_Volume : RSYNC over TLS
note on link : ASR-003: Encrypted transfer

cloud External {
  actor Operator
}

Operator -- API_Gateway : HTTPS/TLS1.2+
@enduml
```

11. Container  
```plantuml
@startuml ContainerDiagram
container "Web Layer" as WEB {
  component "API Gateway" 
  technology "IIS 6.0"
}

container "App Layer" as APP {
  component "Incident Service"
  component "Audit Logger"
  technology "C++ Win32"
}

container "Storage" as STORE {
  component "WORM Filesystem"
  technology "NTFS WORM Extension"
}

Operator --> WEB : 443/HTTPS
WEB --> APP : RPC
APP --> STORE : Encrypted I/O
note right of STORE
  NFR-001: Disabled ports\nOPSEC hardened
end note
@enduml
```