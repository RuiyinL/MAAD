## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction
skinparam packageStyle rectangle

actor "EndUser" as EndUser
actor "Admin" as Admin
actor "Browser" as Browser
actor "AuditReviewer" as AuditReviewer

rectangle "Web Learning Game System" as WLG {
  usecase "Start Game" as UC_StartGame
  usecase "Play Session" as UC_PlaySession
  usecase "Answer Question" as UC_AnswerQuestion
  usecase "View Feedback" as UC_ViewFeedback
  usecase "View Score" as UC_ViewScore
  usecase "Manage Content" as UC_ManageContent
  usecase "Login Admin" as UC_LoginAdmin
  usecase "Validate Content" as UC_ValidateContent
  usecase "Publish Questions" as UC_PublishQuestions
  usecase "View Audit Log" as UC_ViewAuditLog
  usecase "Lock Account" as UC_LockAccount
}

EndUser --> UC_StartGame
EndUser --> UC_PlaySession
EndUser --> UC_AnswerQuestion
EndUser --> UC_ViewFeedback
EndUser --> UC_ViewScore

Admin --> UC_ManageContent
Admin --> UC_LoginAdmin
Admin --> UC_ViewAuditLog

AuditReviewer --> UC_ViewAuditLog

Browser --> UC_StartGame
Browser --> UC_PlaySession

UC_PlaySession ..> UC_AnswerQuestion : <<include>>
UC_AnswerQuestion ..> UC_ViewFeedback : <<include>>
UC_ManageContent ..> UC_ValidateContent : <<include>>
UC_ManageContent ..> UC_PublishQuestions : <<include>>
UC_ManageContent ..> UC_LoginAdmin : <<include>>
UC_LoginAdmin ..> UC_LockAccount : <<extend>>

note right of WLG
assumption: System is a standards-based HTML5 web app (no plugins).
assumption: Admin content updates are contract-first JSON schema validated and written atomically.
assumption: Audit logs are retained >= 2 years and accessible to Admin/AuditReviewer.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class Player {
  +playerId: String
  +displayName: String
  +startSession(): GameSession
}

class GameSession {
  +sessionId: String
  +startedAtUtc: DateTime
  +endedAtUtc: DateTime
  +status: SessionStatus
  +currentIndex: int
  +score: int
  +start(): void
  +submitAnswer(answer: Answer): Feedback
  +end(): void
}

enum SessionStatus {
  New
  InProgress
  Completed
  Abandoned
}

class QuestionBank <<persisted>> {
  +version: String
  +updatedAtUtc: DateTime
  +loadActiveSet(): List<Question>
  +validateSchema(payloadJson: String): ValidationResult
}

class Question <<immutable>> {
  +questionId: String
  +prompt: String
  +choices: List<String>
  +correctIndex: int
  +difficulty: String
  +validate(): ValidationResult
}

class Answer {
  +questionId: String
  +selectedIndex: int
  +answeredAtUtc: DateTime
}

class Feedback {
  +isCorrect: boolean
  +message: String
  +awardedPoints: int
}

class AdminUser <<persisted>> {
  +adminId: String
  +username: String
  -passwordHash: String
  +isLocked: boolean
  +failedAttempts: int
  +lastLoginAtUtc: DateTime
  +authenticate(password: String): boolean
  +lock(): void
  +resetFailures(): void
}

class AdminSession {
  +sessionId: String
  +adminId: String
  +createdAtUtc: DateTime
  +expiresAtUtc: DateTime
  +isExpired(nowUtc: DateTime): boolean
}

class AuditLogEntry <<persisted>> {
  +eventId: String
  +timestampUtc: DateTime
  +adminId: String
  +remoteIp: String
  +action: String
  +beforeJson: String
  +afterJson: String
}

class ContentUpdateRequest {
  +payloadJson: String
  +submittedAtUtc: DateTime
  +validateAgainstSchema(): ValidationResult
}

class ValidationResult {
  +isValid: boolean
  +errors: List<String>
}

Player "1" o-- "0..*" GameSession
GameSession "1" --> "1..*" Question : uses
GameSession "0..*" --> "0..*" Answer : records
GameSession "0..*" --> "0..*" Feedback : produces

QuestionBank "1" *-- "1..*" Question : contains

AdminUser "1" o-- "0..*" AdminSession
AdminUser "1" --> "0..*" AuditLogEntry : writes
ContentUpdateRequest "1" --> "1" QuestionBank : updates

note right of AdminUser
Security ASR: >=12 char passwords, salted hashing (bcrypt/Argon2),
lockout after 5 failures, session timeout, HTTPS-only.
end note

note right of QuestionBank
ASR: JSON schema validation + atomic file update (temp write + rename).
end note

note right of AuditLogEntry
ASR: audit fields (UTC timestamp, adminId, remoteIp, before/after),
retention >= 2 years.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView
skinparam classAttributeIconSize 0

object "player1:Player [PlaySession]" as player1 {
  playerId = "p-1001"
  displayName = "Alex"
}

object "session1:GameSession [PlaySession]" as session1 {
  sessionId = "s-9001"
  startedAtUtc = "2026-03-13T10:00:00Z"
  status = InProgress
  currentIndex = 1
  score = 10
}

object "q1:Question [AnswerQuestion]" as q1 {
  questionId = "q-001"
  prompt = "2 + 2 = ?"
  choices = "[2,3,4,5]"
  correctIndex = 2
  difficulty = "Easy"
}

object "a1:Answer [AnswerQuestion]" as a1 {
  questionId = "q-001"
  selectedIndex = 2
  answeredAtUtc = "2026-03-13T10:00:12Z"
}

object "f1:Feedback [ViewFeedback]" as f1 {
  isCorrect = true
  message = "Correct!"
  awardedPoints = 10
}

object "admin1:AdminUser [ManageContent]" as admin1 {
  adminId = "a-01"
  username = "contentAdmin"
  isLocked = false
  failedAttempts = 0
}

object "req1:ContentUpdateRequest [PublishQuestions]" as req1 {
  payloadJson = "{...questions...}"
  submittedAtUtc = "2026-03-13T11:00:00Z"
}

player1 -- session1
session1 -- q1
session1 -- a1
session1 -- f1
admin1 -- req1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_GameSession
hide empty description

[*] --> New : StartGame
New --> InProgress : PlaySession / start()

InProgress --> InProgress : AnswerQuestion / submitAnswer()
InProgress --> Completed : EndSession / end()
InProgress --> Abandoned : Timeout [noActivity] / end()

Completed --> [*]
Abandoned --> [*]

note right of InProgress
NFR/ASR: feedback event observable within 500ms (UI),
time-to-playable under constrained bandwidth (test harness).
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_PlaySession
start
:Load Web UI (HTML5);
:Fetch active questions;
note right
NFR: time-to-playable measured under bandwidth simulation.
end note

:Start session;
repeat
  :Render question;
  :User selects answer;
  :Submit answer;
  :Compute correctness;
  :Update score;
  :Render feedback [SecurityCheck: no PII];
  note right
NFR: feedback DOM update within 500ms.
end note
repeat while (More questions?) is (yes)

:End session;
:Show final score;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_PlaySession
title Scenario S1: EndUser plays session and answers a question

actor EndUser as EndUser
participant "WebUI" as WebUI
participant "GameAPI" as GameAPI
participant "QuestionService" as QuestionService
database "ContentStore(JSON)" as ContentStore
participant "ScoringService" as ScoringService

EndUser -> WebUI : StartGame
WebUI -> GameAPI : StartSession
GameAPI -> QuestionService : LoadActiveSet
QuestionService -> ContentStore : ReadQuestions
ContentStore --> QuestionService : QuestionsJson
QuestionService --> GameAPI : QuestionList
GameAPI --> WebUI : SessionStarted + FirstQuestion

EndUser -> WebUI : AnswerQuestion
WebUI -> GameAPI : SubmitAnswer
GameAPI -> ScoringService : ScoreAnswer
ScoringService --> GameAPI : Feedback
GameAPI --> WebUI : ViewFeedback + UpdateScore

note right of WebUI
NFR: feedback visible within 500ms (measured by DOM event).
end note
@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_AdminPublish
title Scenario S2: Admin logs in and publishes updated questions (schema-validated, atomic write)

actor Admin as Admin
participant "AdminUI" as AdminUI
participant "AdminAPI" as AdminAPI
participant "AuthService" as AuthService
participant "ContentService" as ContentService
database "ContentStore(JSON)" as ContentStore
database "AuditLogStore" as AuditLogStore

Admin -> AdminUI : LoginAdmin
AdminUI -> AdminAPI : Authenticate
AdminAPI -> AuthService : VerifyPassword
AuthService --> AdminAPI : AuthOK + Session
AdminAPI --> AdminUI : AdminSession

Admin -> AdminUI : ManageContent
AdminUI -> AdminAPI : ValidateContent
AdminAPI -> ContentService : ValidateSchema
ContentService --> AdminAPI : ValidationResult

alt valid
  AdminUI -> AdminAPI : PublishQuestions
  AdminAPI -> ContentService : AtomicWrite
  ContentService -> ContentStore : WriteTempThenRename
  ContentService -> AuditLogStore : AppendAuditEntry
  ContentService --> AdminAPI : PublishOK
  AdminAPI --> AdminUI : PublishOK
else invalid
  AdminAPI --> AdminUI : ValidationErrors
end

note right of AuthService
ASR: lockout after 5 failures; session timeout; HTTPS-only.
end note

note right of ContentService
ASR: server-side validation + atomic file update semantics.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_PlaySession
title Collaboration S1: Play session + answer question

actor EndUser as EndUser
rectangle WebUI as WebUI
rectangle GameAPI as GameAPI
rectangle QuestionService as QuestionService
database ContentStore as ContentStore
rectangle ScoringService as ScoringService

EndUser -- WebUI
WebUI -- GameAPI
GameAPI -- QuestionService
QuestionService -- ContentStore
GameAPI -- ScoringService

WebUI : 1. StartGame
GameAPI : 2. StartSession
QuestionService : 3. LoadActiveSet
ContentStore : 4. ReadQuestions
WebUI : 5. AnswerQuestion
GameAPI : 6. SubmitAnswer
ScoringService : 7. ScoreAnswer
WebUI : 8. ViewFeedback

note right of WebUI
Origin: Scenario S1 sequence diagram.
end note
@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_AdminPublish
title Collaboration S2: Admin publish questions (validate + atomic write + audit)

actor Admin as Admin
rectangle AdminUI as AdminUI
rectangle AdminAPI as AdminAPI
rectangle AuthService as AuthService
rectangle ContentService as ContentService
database ContentStore as ContentStore
database AuditLogStore as AuditLogStore

Admin -- AdminUI
AdminUI -- AdminAPI
AdminAPI -- AuthService
AdminAPI -- ContentService
ContentService -- ContentStore
ContentService -- AuditLogStore

AdminUI : 1. LoginAdmin
AdminAPI : 2. Authenticate
AuthService : 3. VerifyPassword
AdminUI : 4. ManageContent
AdminAPI : 5. ValidateContent
ContentService : 6. ValidateSchema
AdminAPI : 7. PublishQuestions
ContentService : 8. AtomicWrite
AuditLogStore : 9. AppendAuditEntry

note right of AdminAPI
Origin: Scenario S2 sequence diagram.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as ui {
  class WebUI
  class AdminUI
}

package "api" as api {
  class GameAPI
  class AdminAPI
}

package "domain" as domain {
  class Player
  class GameSession
  class Question
  class Answer
  class Feedback
  class AdminUser
  class AdminSession
  class AuditLogEntry
}

package "services" as services {
  class QuestionService
  class ScoringService
  class AuthService
  class ContentService
  class AuditService
}

package "persistence" as persistence {
  class ContentStore
  class AuditLogStore
  class AdminStore
}

package "contracts" as contracts {
  class QuestionSchema
  class ContentUpdateRequest
  class ValidationResult
}

ui ..> api : uses
api ..> services : calls
services ..> domain : uses
services ..> persistence : reads/writes
api ..> contracts : validates
services ..> contracts : validates

note right of contracts
ASR: contract-first JSON schema + server-side validation.
end note

note right of persistence
ASR: atomic file update (temp + rename) for ContentStore;
audit retention >= 2 years for AuditLogStore.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

component "WebUI" as WebUI <<UI>> [PlaySession]
component "AdminUI" as AdminUI <<UI>> [ManageContent]

component "GameAPI" as GameAPI <<API>> [Session]
component "AdminAPI" as AdminAPI <<API>> [Admin]

component "QuestionService" as QuestionService <<Service>> [Questions]
component "ScoringService" as ScoringService <<Service>> [Scoring]
component "AuthService" as AuthService <<Service>> [Auth]
component "ContentService" as ContentService <<Service>> [Publish]
component "AuditService" as AuditService <<Service>> [Audit]

database "ContentStore(JSON)" as ContentStore <<Store>>
database "AdminStore" as AdminStore <<Store>>
database "AuditLogStore" as AuditLogStore <<Store>>

interface "IGame" as IGame
interface "IAdmin" as IAdmin
interface "IAuth" as IAuth
interface "IContent" as IContent
interface "IAudit" as IAudit

GameAPI - IGame
AdminAPI - IAdmin

AuthService - IAuth
ContentService - IContent
AuditService - IAudit

WebUI ..> IGame : uses
AdminUI ..> IAdmin : uses

GameAPI ..> QuestionService : uses
GameAPI ..> ScoringService : uses

AdminAPI ..> AuthService : uses
AdminAPI ..> ContentService : uses
AdminAPI ..> AuditService : uses

QuestionService ..> ContentStore : reads
ContentService ..> ContentStore : atomicWrite
AuthService ..> AdminStore : reads/writes
AuditService ..> AuditLogStore : append/read

note right of ContentService
ASR: validate JSON against schema; write temp then atomic rename.
end note

note right of AuthService
ASR: bcrypt/Argon2, lockout after 5 failures, session timeout, HTTPS-only.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam componentStyle rectangle

node "Client Device" as Client {
  artifact "Browser (HTML5)" as Browser
}

node "Web Tier" as WebTier {
  node "Web Server (TLS)" as WebServer {
    artifact "WebUI" as WebUI_art
    artifact "AdminUI" as AdminUI_art
  }
}

node "App Tier" as AppTier {
  node "App Server (replica 1)" as App1 {
    artifact "GameAPI" as GameAPI_art
    artifact "AdminAPI" as AdminAPI_art
    artifact "QuestionService" as QuestionService_art
    artifact "ScoringService" as ScoringService_art
    artifact "AuthService" as AuthService_art
    artifact "ContentService" as ContentService_art
    artifact "AuditService" as AuditService_art
  }
  node "App Server (replica 2)" as App2 {
    artifact "GameAPI" as GameAPI_art2
    artifact "AdminAPI" as AdminAPI_art2
    artifact "QuestionService" as QuestionService_art2
    artifact "ScoringService" as ScoringService_art2
    artifact "AuthService" as AuthService_art2
    artifact "ContentService" as ContentService_art2
    artifact "AuditService" as AuditService_art2
  }
}

node "Data Tier" as DataTier {
  node "Content Volume" as ContentVol {
    artifact "ContentStore(JSON files)" as ContentStore_art
  }
  node "Audit Volume" as AuditVol {
    artifact "AuditLogStore" as AuditLogStore_art
  }
  node "Admin DB" as AdminDB {
    artifact "AdminStore" as AdminStore_art
  }
}

Browser --> WebServer : HTTPS
WebServer --> App1 : HTTPS
WebServer --> App2 : HTTPS

App1 --> ContentVol : file I/O (atomic rename)
App2 --> ContentVol : file I/O (atomic rename)
App1 --> AuditVol : append-only
App2 --> AuditVol : append-only
App1 --> AdminDB : TCP
App2 --> AdminDB : TCP

note right of WebServer
ASR: HTTPS-only endpoints.
end note

note right of AppTier
NFR: availability via stateless replicas; sessions stored client-side or in-memory per request.
end note

note right of ContentVol
ASR: atomic update semantics; consider file lock to prevent concurrent writes.
end note

note right of AuditVol
ASR: retention >= 2 years.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
skinparam rectangle {
  roundCorner 10
}
skinparam packageStyle rectangle

rectangle "EndUser Browser" as EndUserBrowser <<External>> {
  rectangle "WebUI (HTML5/JS)" as WebUI <<Container>> [PlaySession]
}

rectangle "Admin Browser" as AdminBrowser <<External>> {
  rectangle "AdminUI (HTML5/JS)" as AdminUI <<Container>> [ManageContent]
}

rectangle "Backend" as Backend {
  rectangle "GameAPI" as GameAPI <<Container>> [Session]
  rectangle "AdminAPI" as AdminAPI <<Container>> [Admin]
  rectangle "QuestionService" as QuestionService <<Container>> [Questions]
  rectangle "ScoringService" as ScoringService <<Container>> [Scoring]
  rectangle "AuthService" as AuthService <<Container>> [Auth]
  rectangle "ContentService" as ContentService <<Container>> [Publish]
  rectangle "AuditService" as AuditService <<Container>> [Audit]
}

database "ContentStore (JSON files)" as ContentStore <<Container>> [AtomicWrite]
database "AdminStore" as AdminStore <<Container>> [Credentials]
database "AuditLogStore" as AuditLogStore <<Container>> [Retention>=2y]

WebUI --> GameAPI : HTTPS (StartSession/SubmitAnswer)
AdminUI --> AdminAPI : HTTPS (Auth/Publish)

GameAPI --> QuestionService : internal call
GameAPI --> ScoringService : internal call
AdminAPI --> AuthService : internal call
AdminAPI --> ContentService : internal call
AdminAPI --> AuditService : internal call

QuestionService --> ContentStore : read
ContentService --> ContentStore : validate + atomicWrite
AuthService --> AdminStore : read/write
AuditService --> AuditLogStore : append/read

note right of ContentService
ASR: JSON schema validation; temp-file then rename; server-side validation.
end note

note right of AuthService
ASR: bcrypt/Argon2; lockout after 5 failures; session timeout; HTTPS-only.
end note
@enduml
```