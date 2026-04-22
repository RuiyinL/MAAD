## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Citizen as CIT
actor PoliceOfficer as PO
actor Prosecutor as PROS
actor Admin as ADM
actor SuperUser as SU
actor ExternalSystem as ES

usecase "Register Complaint" as UC001
usecase "Initiate Investigation" as UC002
usecase "Log Court Interaction" as UC003
usecase "Search Cases/Suspects" as UC004
usecase "Customize Results" as UC005
usecase "Generate Reports" as UC006
usecase "Send OTP" as UC007
usecase "View Role Dashboard" as UC008
usecase "Scan/Upload File" as UC009
usecase "Configure Alerts" as UC010
usecase "Manage Access Control" as UC011
usecase "Enforce Security Policy" as UC012
usecase "Handle Restricted Access" as UC013
usecase "View Context Help" as UC014
usecase "Export Audit Trail" as UC015

CIT --> UC001
PO --> UC002
PO --> UC004
PO --> UC005
PO --> UC006
PO --> UC008
PO --> UC009
PO --> UC010
PROS --> UC003
PROS --> UC004
PROS --> UC006
ADM --> UC011
ADM --> UC013
ADM --> UC015
SU --> UC012
SU --> UC011

UC001 .> UC007 : <<include>>
UC009 .> ES : <<extend>>
UC007 .> ES : <<extend>>
UC014 .> UC001 : <<extend>>
UC014 .> UC002 : <<extend>>
UC014 .> UC003 : <<extend>>
UC014 .> UC004 : <<extend>>

note right of UC007
  assumption: OTP generation 
  integrated with complaint reg
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class Complaint {
  -complaintId: String
  -description: String
  -status: String
  +registerComplaint()
  +updateStatus()
}

class Investigation {
  -investigationId: String
  -startDate: Date
  -status: String
  +initiateInvestigation()
}

class CourtInteraction {
  -interactionId: String
  -date: Date
  -details: String
  +logInteraction()
}

class Case {
  -caseId: String
  -summary: String
  -offenseType: String
  +searchCases()
}

class Suspect {
  -suspectId: String
  -name: String
  -status: String
}

class User {
  -userId: String
  -role: String
  -uiSettings: JSON
  +customizeUI()
}

class AuditLog {
  -logId: String
  -timestamp: DateTime
  -action: String
  -entityId: String
  +exportLogs()
}

class SecurityPolicy {
  -policyId: String
  -attributes: String[]
}

Complaint "1" --> "1" Investigation
Investigation "1" --> "0..1" CourtInteraction
Case "1" *-- "0..*" Suspect
User "1" -- "0..*" Case : accesses >
User "1" -- "1" SecurityPolicy : enforces >
AuditLog "1" -- "0..*" Case : records >
Case o-- Complaint
Case o-- Investigation

note top of AuditLog
  <<immutable>>
  Append-only per ASR-001
end note

note bottom of Case
  <<cacheable>>
  Optimized for search per ASR-005
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
object citizen1 as "citizen1: Citizen" {
  name = "John Doe"
}
object complaint1 as "complaint1: Complaint [RegisterComplaint]" {
  complaintId = "CMP-1001"
  description = "Noise complaint"
  status = "Registered"
}
object case1 as "case1: Case" {
  caseId = "CASE-2023-001"
  summary = "Residential disturbance"
}
object audit1 as "audit1: AuditLog" {
  logId = "AUD-778"
  action = "CREATE"
}

citizen1 --> complaint1
complaint1 --> case1
case1 --> audit1

object officer1 as "officer1: PoliceOfficer [SearchCases]" {
  userId = "PO-887"
}
object searchResults as "results: Case[]" {
  case1 : CASE-2023-001
  case2 : CASE-2023-005
}
object suspect1 as "suspect1: Suspect" {
  name = "Mark Smith"
}

officer1 --> searchResults
searchResults --> case1
case1 --> suspect1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
[*] --> Registered
Registered --> UnderInvestigation : initiateInvestigation
UnderInvestigation --> InCourt : logCourtInteraction
UnderInvestigation --> Closed : resolveWithoutTrial
InCourt --> Closed : concludeTrial

state UnderInvestigation {
  [*] --> EvidenceCollection
  EvidenceCollection --> WitnessInterview
  WitnessInterview --> Analysis
  Analysis --> ReportPreparation
}

note right of Registered
  Trigger: Complaint registered (FR-001)
end note

note left of Closed
  Terminal state for case lifecycle
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml

|Citizen|
start
:Citizen registers complaint;

|Police Station|
:Validate input\n<<SecurityCheck>>;
:Generate OTP via HMAC;
:Send SMS via Twilio;
:Verify OTP;

if (OTP valid?) then (yes)
  :Create case record;
  :Initiate investigation;
  :Log audit entry;
else (no)
  :Log failure attempt;
  if (3 failures?) then (yes)
    :Escalate incident;
  endif
endif

|Citizen|
:Update citizen status;

stop

note right
  FR-007:
  OTP generation & verification
end note

note left
  ASR-001:
  Audit log must be append-only
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
actor Citizen as CIT
participant "UI Layer" as UI
participant "ComplaintService" as SVC
participant "OTPGenerator" as OTP
participant "SMSGateway" as SMS
participant "Database" as DB

CIT -> UI: Submit complaint
UI -> SVC: processComplaint()
SVC -> OTP: generateOTP()
OTP --> SVC: OTP code
SVC -> SMS: sendSMS(OTP)
SMS --> SVC: delivery status
UI -> CIT: Show OTP prompt
CIT -> UI: Enter OTP
UI -> SVC: validateOTP()
SVC -> DB: saveComplaint()
DB --> SVC: success
SVC -> DB: createAuditLog()
DB --> SVC: success
SVC --> UI: confirmation
UI --> CIT: Success message
@enduml
```

```plantuml
@startuml SequenceDiagram2
actor Officer as PO
participant "UI Layer" as UI
participant "SearchService" as SRCH
participant "Cache" as CACHE
participant "Database" as DB

PO -> UI: Enter search criteria
UI -> SRCH: executeSearch()
SRCH -> CACHE: checkCache()
CACHE --> SRCH: cache miss
SRCH -> DB: queryCases()
DB --> SRCH: results
SRCH -> SRCH: applyACLFiltering()
SRCH -> CACHE: storeResults()
SRCH --> UI: paginatedResults
UI -> UI: applyCustomColumns()
UI --> PO: Display results
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationDiagram1
component "Citizen" as CIT
component "ComplaintService" as SVC
component "OTPGenerator" as OTP
component "SMSGateway" as SMS
component "Database" as DB

CIT -- SVC : 1: submitComplaint()
SVC -- OTP : 2: generateOTP()
SVC -- SMS : 3: sendSMS()
SVC -- DB : 4: saveRecord()
SVC -- DB : 5: logAudit()

note top
  Complaint Registration Workflow
  (FR-001, FR-007)
end note
@enduml
```

```plantuml
@startuml CollaborationDiagram2
component "PoliceOfficer" as PO
component "SearchService" as SRCH
component "Cache" as CACHE
component "Database" as DB
component "ACLService" as ACL

PO -- SRCH : 1: searchRequest()
SRCH -- CACHE : 2: checkCache()
SRCH -- DB : 3: queryDB()
DB -- SRCH : 4: results
SRCH -- ACL : 5: applyFilters()
SRCH -- CACHE : 6: cacheResults()
SRCH -- PO : 7: returnResults()

note bottom
  Case Search Workflow
  (FR-004, FR-013)
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package "UI Layer" {
  [Web Components]
  [Controllers]
}

package "Application Layer" {
  [Services]
  [DTOs]
}

package "Domain Layer" {
  [Entities]
  [Repositories]
}

package "Infrastructure" {
  [Persistence]
  [External Integrations]
}

[Controllers] --> [Services]
[Services] --> [Entities]
[Services] --> [Repositories]
[Repositories] --> [Persistence]
[Services] --> [External Integrations]

note bottom of [Domain Layer]
  Core business logic
  Audit immutable per ASR-001
end note

note right of [Infrastructure]
  Implements offline sync
  per ASR-002
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
component "Complaint Mgmt" as COMP {
  interface "registerComplaint()"
}
component "Investigation Mgmt" as INV {
  interface "initiateInvestigation()"
}
component "Search Engine" as SEARCH {
  interface "searchCases()"
}
component "Audit System" as AUDIT {
  interface "logEvent()"
}
component "Offline Sync" as SYNC {
  interface "synchronizeData()"
}

COMP --> AUDIT : logs events
INV --> COMP : uses
SEARCH --> AUDIT : logs access
SEARCH --> SYNC : offline data
SYNC --> AUDIT : sync events

note top of AUDIT
  <<Immutable Component>>
  Append-only storage
end note

note bottom of SEARCH
  <<Cacheable>>
  Optimized per ASR-005
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node "Central Data Center" {
  artifact "Web Server Cluster" as WS
  artifact "App Server Cluster" as AS
  artifact "Primary DB" as DB1
  artifact "Audit DB" as DB2
  artifact "Cache Cluster" as CACHE
}

node "Police Station A" {
  artifact "Local Server" as LS1
  artifact "Offline DB" as ODB1
}

node "Police Station B" {
  artifact "Local Server" as LS2
  artifact "Offline DB" as ODB2
}

cloud "SMS Gateway" as SMS
cloud "AV Service" as AV

WS - AS : LAN
AS - DB1 : GigE
AS - DB2 : GigE
AS - CACHE : LAN
LS1 <- AS : HTTPS Sync
LS2 <- AS : HTTPS Sync
LS1 --> SMS : API Call
AS --> AV : API Call

note left of WS
  Load-balanced
  Static content hosting
end note

note right of DB2
  Append-only storage
  Cryptographic integrity
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
container "Web Browser" as WB {
  component "React UI"
}

container "API Gateway" as GW {
  component "NGINX"
}

container "Application Server" as APP {
  component "ComplaintService"
  component "SearchService"
  component "SyncService"
}

container "Database" as DB {
  component "PostgreSQL"
}

container "Audit Store" as AUDIT {
  component "ImmutableDB"
}

container "Cache" as CACHE {
  component "Redis"
}

container "Message Broker" as MSG {
  component "Kafka"
}

WB --> GW : HTTPS
GW --> APP : REST/JSON
APP --> DB : JDBC
APP --> AUDIT : gRPC
APP --> CACHE : Redis protocol
APP --> MSG : Events
MSG --> APP : Commands
SyncService --> APP : Sync API

note left of APP
  Stateless services
  Supports ASR-004
end note

note right of AUDIT
  WORM storage
  Hash-chained entries
end note
@enduml
```