## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase
actor Citizen as "Citizen"
actor Police as "Police"
actor Admin as "Admin"

usecase "Submit Complaint" as (SubmitComplaint)
usecase "Review Complaint" as (ReviewComplaint)
usecase "Search Cases" as (SearchCases)
usecase "Manage User Profile" as (ManageUserProfile)
usecase "Configure Access Control" as (ConfigureAccessControl)

Citizen -- (SubmitComplaint)
Police -- (ReviewComplaint)
Police -- (SearchCases)
Admin -- (ManageUserProfile)
Admin -- (ConfigureAccessControl)

(SubmitComplaint) ..> (ReviewComplaint) : <<include>>
(SearchCases) ..> (ReviewComplaint) : <<include>>
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class
class Complaint {
  - id: UUID
  - text: string
  - status: enum
}

class User {
  - id: UUID
  - role: enum
}

class Case {
  - id: UUID
  - complaint: Complaint
  - status: enum
}

Complaint --* Case
User --* Case
@enduml
```
3. Object — Logic View: Object Diagram
```plantuml
@startuml
participant complaint1 as "Example complaint" << (C,#FFAAAA) >> 
participant user1 as "CITIZEN" << (U,#AAFFAA) >> 
participant case1 as "Case" << (C,#AAAAFF) >> 

complaint1 --> case1
user1 --> case1
@enduml
```
4. State — Logic View: State Diagram
```plantuml
@startuml State
state Submitted
state Pending
state Accepted
state Rejected

[*] --> Submitted
Submitted --> Pending : review
Pending --> Accepted : accept
Pending --> Rejected : reject
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity
start
: Submit complaint;
: Review complaint;
if (Complaint valid?) then (yes)
  : Accept complaint;
else (no)
  : Reject complaint;
endif
: Search cases;
: Display results;
stop
@enduml
```
6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml Sequence1
participant Citizen as "Citizen"
participant Police as "Police"
participant System as "System"

Citizen->>System: Submit complaint
System->>Police: Notify review
Police->>System: Review complaint
System->>Police: Return result
Police->>System: Accept/Reject complaint
System->>Citizen: Notify outcome
@enduml
```
```plantuml
@startuml Sequence2
participant Police as "Police"
participant System as "System"
participant Database as "Database"

Police->>System: Search cases
System->>Database: Query database
Database->>System: Return results
System->>Police: Display results
@enduml
```
7. Collaboration — Process View: Collaboration Diagram 
```plantuml
@startuml Collaboration1
participant Citizen
participant Police
participant System

Citizen ->> System : Submit complaint
System ->> Police : Notify review
Police ->> System : Review complaint
System ->> Police : Return result
Police ->> System : Accept/Reject complaint
System ->> Citizen : Notify outcome
@enduml
```
```plantuml
@startuml Collaboration2
participant Police
participant System
participant Database

Police ->> System : Search cases
System ->> Database : Query database
Database ->> System : Return results
System ->> Police : Display results
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package
package API {
  class ComplaintController
  class CaseController
}

package Domain {
  class Complaint
  class Case
}

package Persistence {
  class ComplaintRepository
  class CaseRepository
}

API -- Domain
Domain -- Persistence
@enduml
```
9. Component — Development View: Component Diagram
```plantuml
@startuml Component
component ComplaintService {
  interface ComplaintController
  class ComplaintRepository
}

component CaseService {
  interface CaseController
  class CaseRepository
}

ComplaintService -- CaseService
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment
node WebServer {
  component ComplaintService
  component CaseService
}

node DatabaseServer {
  database ComplaintDatabase
  database CaseDatabase
}

WebServer -- DatabaseServer
@enduml
```
11. Container — Physical View: Container Diagram
```plantuml
@startuml Container
artifact WebContainer {
  component ComplaintService
  component CaseService
}

artifact DatabaseContainer {
  database ComplaintDatabase
  database CaseDatabase
}

WebContainer -- DatabaseContainer
@enduml
```