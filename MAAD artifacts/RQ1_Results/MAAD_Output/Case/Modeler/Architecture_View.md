## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCase_ScenarioView
left to right direction
skinparam packageStyle rectangle

actor EndUser as EndUser
actor Admin as Admin
actor "External Browser" as ExternalBrowser

rectangle "Web Learning Game System" as System {
  usecase "Play Game" as UC_PlayGame
  usecase "View Intro" as UC_ViewIntro
  usecase "Answer Question" as UC_AnswerQuestion
  usecase "Get Feedback" as UC_GetFeedback
  usecase "View Score" as UC_ViewScore

  usecase "Admin Login" as UC_AdminLogin
  usecase "Manage Questions" as UC_ManageQuestions
  usecase "Validate Content" as UC_ValidateContent
  usecase "Publish Update" as UC_PublishUpdate
  usecase "View Audit Log" as UC_ViewAuditLog
}

EndUser --> UC_PlayGame
EndUser --> UC_ViewIntro
EndUser --> UC_AnswerQuestion
EndUser --> UC_GetFeedback
EndUser --> UC_ViewScore

Admin --> UC_AdminLogin
Admin --> UC_ManageQuestions
Admin --> UC_ViewAuditLog

UC_PlayGame ..> UC_ViewIntro : <<include>>
UC_PlayGame ..> UC_AnswerQuestion : <<include>>
UC_AnswerQuestion ..> UC_GetFeedback : <<include>>
UC_PlayGame ..> UC_ViewScore : <<include>>

UC_ManageQuestions ..> UC_ValidateContent : <<include>>
UC_ManageQuestions ..> UC_PublishUpdate : <<include>>

ExternalBrowser --> UC_PlayGame
ExternalBrowser --> UC_AdminLogin

note right of System
assumption: FR/NFR/ASR artifacts not provided; inferred from semantic memory:
- standards-based HTML5 web app (no plugins)
- contract-first admin question updates (JSON schema + server validation)
- atomic publish + audit logging + hardened auth
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class GameSession {
  +sessionId: String
  +userAgent: String
  +startedAtUtc: String
  +status: String
  +start()
  +end()
}

class QuestionBank <<persisted>> {
  +version: String
  +schemaVersion: String
  +lastPublishedAtUtc: String
  +load()
  +getQuestion(questionId: String): Question
}

class Question {
  +questionId: String
  +prompt: String
  +choices: String[*]
  +correctChoiceIndex: int
  +difficulty: String
  +validate(): boolean
}

class AnswerAttempt {
  +attemptId: String
  +questionId: String
  +selectedChoiceIndex: int
  +isCorrect: boolean
  +answeredAtUtc: String
  +evaluate(q: Question): boolean
}

class Score {
  +scoreId: String
  +points: int
  +correctCount: int
  +incorrectCount: int
  +update(isCorrect: boolean)
}

class AdminUser <<persisted>> {
  +adminId: String
  +username: String
  -passwordHash: String
  +isLocked: boolean
  +failedAttempts: int
  +authenticate(password: String): boolean
  +lock()
}

class AdminSession {
  +sessionId: String
  +adminId: String
  +createdAtUtc: String
  +expiresAtUtc: String
  +isExpired(nowUtc: String): boolean
  +invalidate()
}

class ContentUpdateRequest {
  +requestId: String
  +submittedAtUtc: String
  +submittedByAdminId: String
  +payloadJson: String
  +validateAgainstSchema(schemaVersion: String): boolean
}

class ContentPublisher {
  +publishAtomic(req: ContentUpdateRequest): String
  +writeTemp()
  +atomicRename()
}

class AuditLogEntry <<immutable>> {
  +eventId: String
  +timestampUtc: String
  +adminId: String
  +remoteIp: String
  +action: String
  +beforeHash: String
  +afterHash: String
}

class AuditLog <<persisted>> {
  +retentionYears: int
  +append(entry: AuditLogEntry)
  +query(fromUtc: String, toUtc: String): AuditLogEntry[*]
}

GameSession "1" o-- "0..*" AnswerAttempt
GameSession "1" o-- "1" Score
QuestionBank "1" *-- "1..*" Question
AnswerAttempt "0..*" --> "1" Question : evaluates
AdminUser "1" o-- "0..*" AdminSession
ContentUpdateRequest "0..*" --> "1" AdminUser : submittedBy
ContentPublisher "1" --> "1" QuestionBank : updates
ContentPublisher "1" --> "1" AuditLog : writes
AuditLog "1" *-- "0..*" AuditLogEntry

note right of ContentPublisher
ASR: atomic file update semantics (temp write + atomic rename)
end note

note right of ContentUpdateRequest
ASR: contract-first JSON schema validation (server-side)
end note

note right of AdminUser
ASR: hardened auth (>=12 chars, salted hash e.g., bcrypt/Argon2),
lockout after 5 failures, HTTPS-only endpoints
end note

note right of AuditLog
ASR: audit logging with required fields + retention >= 2 years
end note
@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml Object_LogicView
object session1 as "session1:GameSession [PlayGame]" {
  sessionId = "S-9f2a"
  userAgent = "Chrome/122"
  startedAtUtc = "2026-03-13T10:00:00Z"
  status = "Active"
}

object bank1 as "bank1:QuestionBank [ManageQuestions]" {
  version = "2026.03.13-1"
  schemaVersion = "1.0.0"
  lastPublishedAtUtc = "2026-03-13T09:55:00Z"
}

object q1 as "q1:Question [AnswerQuestion]" {
  questionId = "Q-101"
  prompt = "What is 2+2?"
  choices = "{2,3,4,5}"
  correctChoiceIndex = 2
  difficulty = "Easy"
}

object attempt1 as "attempt1:AnswerAttempt [AnswerQuestion]" {
  attemptId = "A-0001"
  questionId = "Q-101"
  selectedChoiceIndex = 2
  isCorrect = true
  answeredAtUtc = "2026-03-13T10:00:10Z"
}

object score1 as "score1:Score [ViewScore]" {
  scoreId = "SC-1"
  points = 10
  correctCount = 1
  incorrectCount = 0
}

object admin1 as "admin1:AdminUser [AdminLogin]" {
  adminId = "ADM-7"
  username = "contentAdmin"
  isLocked = false
  failedAttempts = 0
}

object req1 as "req1:ContentUpdateRequest [PublishUpdate]" {
  requestId = "R-55"
  submittedAtUtc = "2026-03-13T09:54:30Z"
  submittedByAdminId = "ADM-7"
  payloadJson = "{...questions...}"
}

session1 -- attempt1
session1 -- score1
bank1 -- q1
attempt1 ..> q1 : evaluates
req1 ..> admin1 : submittedBy
@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml State_LogicView_GameSession
hide empty description

state "GameSession Lifecycle" as GSL {
  [*] --> Created

  Created --> Active : start()/initUi
  Active --> Asking : nextQuestion [hasMore]/renderQuestion
  Asking --> Evaluating : submitAnswer/recordAttempt
  Evaluating --> Feedback : evaluate()/computeScore
  Feedback --> Asking : continue [hasMore]/renderQuestion
  Feedback --> Completed : finish [!hasMore]/showSummary

  Active --> Abandoned : timeout [inactive]/end()
  Asking --> Abandoned : timeout [inactive]/end()
  Feedback --> Abandoned : timeout [inactive]/end()

  Completed --> [*]
  Abandoned --> [*]
}

note right of GSL
NFR/ASR (inferred): feedback responsiveness observable within 500ms;
session timeout policy for admin sessions; end-user session may abandon on inactivity.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml Activity_ProcessView_AdminPublishUpdate
start
:Open Admin UI;
:Enter credentials;
:Authenticate [SecurityCheck];
if (Auth OK?) then (yes)
  :Create ContentUpdateRequest;
  :Upload/Edit questions JSON;
  :ValidateAgainstSchema [ContractCheck];
  if (Valid?) then (yes)
    :Write temp file;
    :Atomic rename publish;
    :Append AuditLogEntry;
    :Return success + new version;
  else (no)
    :Return validation errors;
  endif
else (no)
  :Increment failedAttempts;
  if (failedAttempts >= 5) then (lock)
    :Lock AdminUser;
  endif
  :Return auth error;
endif
stop

note right
ASR: HTTPS-only endpoints; server-side validation; atomic publish; audit retention >= 2 years.
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram

```plantuml
@startuml Sequence_ProcessView_S1_AdminPublishUpdate
actor Admin as Admin
participant "AdminWebUI" as AdminWebUI
participant "AuthService" as AuthService
participant "ContentService" as ContentService
database "FileStore" as FileStore
database "AuditLogStore" as AuditLogStore

Admin -> AdminWebUI : AdminLogin
AdminWebUI -> AuthService : Authenticate(username,password)
AuthService -> AuthService : VerifyHash
AuthService --> AdminWebUI : AuthOK(sessionToken)

Admin -> AdminWebUI : ManageQuestions
AdminWebUI -> ContentService : SubmitUpdate(payloadJson,sessionToken)
ContentService -> AuthService : ValidateSession(sessionToken)
AuthService --> ContentService : SessionOK

ContentService -> ContentService : ValidateContent(schemaVersion)
ContentService -> FileStore : WriteTemp
ContentService -> FileStore : AtomicRename
ContentService -> AuditLogStore : AppendAudit(action,beforeAfter,ip)
ContentService --> AdminWebUI : PublishUpdate(resultVersion)

note over AdminWebUI,ContentService
ASR: contract-first JSON schema validation + atomic file update semantics.
end note
@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_EndUserPlayGame
actor EndUser as EndUser
participant "GameWebUI" as GameWebUI
participant "GameService" as GameService
database "FileStore" as FileStore

EndUser -> GameWebUI : PlayGame
GameWebUI -> GameService : StartSession(userAgent)
GameService --> GameWebUI : SessionStarted(sessionId)

GameWebUI -> GameService : GetQuestion
GameService -> FileStore : LoadQuestionBank
FileStore --> GameService : QuestionBank(version)
GameService --> GameWebUI : Question(prompt,choices)

EndUser -> GameWebUI : AnswerQuestion(selectedChoice)
GameWebUI -> GameService : SubmitAnswer(sessionId,questionId,selectedChoice)
GameService --> GameWebUI : GetFeedback(isCorrect,pointsDelta)

GameWebUI -> GameService : ViewScore
GameService --> GameWebUI : Score(points,correctCount,incorrectCount)

note over GameWebUI
NFR (inferred): standards-based HTML5 (no plugins); feedback responsiveness target.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml Collaboration_ProcessView_S1_AdminPublishUpdate
skinparam linetype ortho
actor Admin as Admin
rectangle AdminWebUI as AdminWebUI
rectangle AuthService as AuthService
rectangle ContentService as ContentService
database FileStore as FileStore
database AuditLogStore as AuditLogStore

Admin -- AdminWebUI
AdminWebUI -- AuthService
AdminWebUI -- ContentService
ContentService -- AuthService
ContentService -- FileStore
ContentService -- AuditLogStore

Admin -> AdminWebUI : 1 AdminLogin
AdminWebUI -> AuthService : 2 Authenticate
AuthService -> AdminWebUI : 3 AuthOK
Admin -> AdminWebUI : 4 ManageQuestions
AdminWebUI -> ContentService : 5 SubmitUpdate
ContentService -> AuthService : 6 ValidateSession
ContentService -> ContentService : 7 ValidateContent
ContentService -> FileStore : 8 WriteTemp
ContentService -> FileStore : 9 AtomicRename
ContentService -> AuditLogStore : 10 AppendAudit
ContentService -> AdminWebUI : 11 PublishUpdate

note right
Scenario: Admin publishes question update with schema validation, atomic file publish, and audit logging.
end note
@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_EndUserPlayGame
skinparam linetype ortho
actor EndUser as EndUser
rectangle GameWebUI as GameWebUI
rectangle GameService as GameService
database FileStore as FileStore

EndUser -- GameWebUI
GameWebUI -- GameService
GameService -- FileStore

EndUser -> GameWebUI : 1 PlayGame
GameWebUI -> GameService : 2 StartSession
GameService -> GameWebUI : 3 SessionStarted
GameWebUI -> GameService : 4 GetQuestion
GameService -> FileStore : 5 LoadQuestionBank
GameService -> GameWebUI : 6 Question
EndUser -> GameWebUI : 7 AnswerQuestion
GameWebUI -> GameService : 8 SubmitAnswer
GameService -> GameWebUI : 9 GetFeedback
GameWebUI -> GameService : 10 ViewScore
GameService -> GameWebUI : 11 Score

note right
Scenario: EndUser plays game: start session, fetch question, submit answer, receive feedback, view score.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package ui {
  note top of ui : HTML5 Web UI (no plugins)\nMVC presentation
}

package api {
  note top of api : HTTP endpoints\nHTTPS-only
}

package domain {
  note top of domain : Core model: sessions, questions, scoring
}

package application {
  note top of application : Use-cases orchestration\nvalidation + publishing
}

package persistence {
  note top of persistence : File-based JSON store\natomic rename semantics
}

package security {
  note top of security : AuthN/AuthZ\nlockout + session timeout
}

package audit {
  note top of audit : Append-only audit\nretention >= 2 years
}

ui ..> api
api ..> application
application ..> domain
application ..> persistence
application ..> security
application ..> audit
persistence ..> domain
security ..> domain
audit ..> domain
@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

component "GameWebUI" as GameWebUI <<UI>> [PlayGame]
component "AdminWebUI" as AdminWebUI <<UI>> [ManageQuestions]

component "ApiGateway" as ApiGateway <<API>> [HTTPSOnly]
component "GameService" as GameService <<Service>> [AnswerQuestion]
component "ContentService" as ContentService <<Service>> [PublishUpdate]
component "AuthService" as AuthService <<Security>> [Lockout]
component "AuditService" as AuditService <<Audit>> [Retention]

database "FileStore" as FileStore <<Storage>> [AtomicRename]
database "AuditLogStore" as AuditLogStore <<Storage>> [AppendOnly]

interface IGameApi
interface IAdminApi
interface IAuth
interface IAudit

GameWebUI --> ApiGateway : uses
AdminWebUI --> ApiGateway : uses

ApiGateway - IGameApi
ApiGateway - IAdminApi

GameService ..|> IGameApi
ContentService ..|> IAdminApi
AuthService ..|> IAuth
AuditService ..|> IAudit

GameService --> FileStore : reads
ContentService --> FileStore : writesTemp+rename
ContentService --> AuthService : validateSession
ContentService --> AuditService : appendAudit
AuditService --> AuditLogStore : persists
AuthService --> AuditLogStore : optionalAuthEvents

note right of FileStore
ASR: temp-file write + atomic rename to prevent corruption
end note

note right of AuthService
ASR: salted hash (bcrypt/Argon2), lockout after 5 failures, session timeout
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml Deployment_PhysicalView
skinparam linetype ortho

node "Client Device" as Client {
  artifact "Browser" as Browser
}

node "Web Server Node (Replica 1)" as Web1 {
  artifact "Static Web UI" as Static1
  artifact "Backend API" as Api1
}

node "Web Server Node (Replica 2)" as Web2 {
  artifact "Static Web UI" as Static2
  artifact "Backend API" as Api2
}

node "Storage Node" as Storage {
  artifact "QuestionBank JSON Files" as QFiles
  artifact "Audit Log Files" as AFiles
}

cloud "Internet" as Net

Browser -- Net
Net -- Web1 : HTTPS
Net -- Web2 : HTTPS
Web1 -- Storage : LAN
Web2 -- Storage : LAN

note right of Web1
NFR/ASR (inferred): fail-closed HTTPS-only; stateless API enables horizontal scaling.
end note

note right of Storage
ASR: atomic rename publish; audit retention >= 2 years.
end note
@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml Container_PhysicalView
skinparam rectangleStyle rounded
skinparam linetype ortho

rectangle "EndUser Browser\n[PlayGame]\nHTML5/CSS/JS" as C_EndUserBrowser
rectangle "Admin Browser\n[ManageQuestions]\nHTML5/CSS/JS" as C_AdminBrowser

rectangle "Web UI (Static Hosting)\n[NoPlugins]\nServes GameWebUI + AdminWebUI" as C_StaticHosting
rectangle "Backend API\n[HTTPSOnly]\nGameService + ContentService" as C_BackendApi
rectangle "Auth Service\n[Lockout]\nPassword hash + sessions" as C_Auth
rectangle "Audit Service\n[Retention]\nAppend audit entries" as C_Audit

database "FileStore\n[AtomicRename]\nquestionBank.json (schema-validated)" as C_FileStore
database "AuditLogStore\n[AppendOnly]\naudit.log (>=2y retention)" as C_AuditStore

C_EndUserBrowser --> C_StaticHosting : GET static assets
C_AdminBrowser --> C_StaticHosting : GET static assets

C_EndUserBrowser --> C_BackendApi : HTTPS Game API
C_AdminBrowser --> C_BackendApi : HTTPS Admin API

C_BackendApi --> C_Auth : validateSession/authenticate
C_BackendApi --> C_FileStore : read/write questions
C_BackendApi --> C_Audit : appendAudit
C_Audit --> C_AuditStore : persist
C_Auth --> C_AuditStore : optionalAuthEvents

note right of C_BackendApi
Style: layered/hexagonal application services over file persistence.
Tactics: server-side schema validation; atomic publish; audit logging.
end note
@enduml
```