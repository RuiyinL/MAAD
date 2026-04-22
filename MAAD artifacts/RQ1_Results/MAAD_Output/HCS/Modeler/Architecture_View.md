## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction

actor "EndUser" as EndUser
actor "Admin" as Admin

rectangle "Web Learning Game System" as System {
  usecase "Play Game" as UC_PlayGame
  usecase "View Intro" as UC_ViewIntro
  usecase "Answer Question" as UC_AnswerQuestion
  usecase "Get Feedback" as UC_GetFeedback
  usecase "View Score" as UC_ViewScore
  usecase "Manage Questions" as UC_ManageQuestions
  usecase "Login Admin" as UC_LoginAdmin
  usecase "Update Questions" as UC_UpdateQuestions
  usecase "Validate Content" as UC_ValidateContent
  usecase "Audit Changes" as UC_AuditChanges
}

EndUser --> UC_PlayGame
EndUser --> UC_ViewIntro
EndUser --> UC_AnswerQuestion
EndUser --> UC_GetFeedback
EndUser --> UC_ViewScore

Admin --> UC_ManageQuestions
Admin --> UC_LoginAdmin
Admin --> UC_UpdateQuestions

UC_PlayGame ..> UC_ViewIntro : <<include>>
UC_AnswerQuestion ..> UC_GetFeedback : <<include>>

UC_ManageQuestions ..> UC_LoginAdmin : <<include>>
UC_UpdateQuestions ..> UC_ValidateContent : <<include>>
UC_UpdateQuestions ..> UC_AuditChanges : <<include>>

note right of System
assumption: Requirements artifacts (FR/NFR/ASR) not provided in prompt;
use cases derived from semantic memory decisions:
- HTML5-only web gameplay with intro/animations/audio
- Contract-first admin question updates (JSON schema + server validation)
- Atomic file update semantics
- Hardened admin auth + audit logging/retention
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
  +startedAtUtc: String
  +currentQuestionIndex: int
  +score: int
  +status: String
  +start(): void
  +nextQuestion(): Question
  +submitAnswer(answerId: String): Feedback
  +end(): void
}

class QuestionBank <<persisted>> {
  +version: String
  +updatedAtUtc: String
  +load(): void
  +getQuestion(index: int): Question
  +count(): int
}

class Question {
  +questionId: String
  +prompt: String
  +choices: List<String>
  +correctAnswerId: String
  +difficulty: String
  +validate(): boolean
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
  +lastLoginAtUtc: String
  +authenticate(password: String): boolean
  +lock(): void
}

class AdminSession {
  +sessionId: String
  +adminId: String
  +createdAtUtc: String
  +expiresAtUtc: String
  +isExpired(nowUtc: String): boolean
  +invalidate(): void
}

class ContentUpdateRequest {
  +requestId: String
  +adminId: String
  +submittedAtUtc: String
  +jsonPayload: String
  +schemaVersion: String
  +validateAgainstSchema(): boolean
}

class ContentRepository <<persisted>> {
  +contentPath: String
  +tempPath: String
  +readJson(): String
  +writeAtomic(json: String): void
  +getCurrentVersion(): String
}

class AuditLogEntry <<immutable>> <<persisted>> {
  +entryId: String
  +timestampUtc: String
  +adminId: String
  +remoteIp: String
  +action: String
  +beforeHash: String
  +afterHash: String
  +details: String
}

class AuditLog <<persisted>> {
  +retentionYears: int
  +append(entry: AuditLogEntry): void
  +exportSnapshot(fromUtc: String, toUtc: String): String
}

GameSession "1" o-- "1" QuestionBank : uses
QuestionBank "1" *-- "1..*" Question : contains
GameSession "1" --> "0..*" Feedback : produces

AdminUser "1" --> "0..*" AdminSession : creates
ContentUpdateRequest "1" --> "1" AdminUser : submittedBy
ContentRepository "1" --> "0..*" ContentUpdateRequest : persists
AuditLog "1" *-- "0..*" AuditLogEntry : entries
AuditLogEntry "0..*" --> "1" AdminUser : actor

note right of ContentRepository
ASR: atomic file update semantics
- write temp file then atomic rename
- prevent corruption on crash
end note

note right of ContentUpdateRequest
ASR: contract-first content updates
- explicit JSON schema
- server-side validation
end note

note right of AdminUser
ASR: hardened auth
- >=12 char passwords
- salted hashing (bcrypt/Argon2)
- lockout after 5 failures
- session timeout policy
end note

note right of AuditLogEntry
ASR: audit logging/retention
- timestamp UTC, adminId, remoteIp, before/after
- retention >= 2 years
end note

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView

object qb1 as "qb1:QuestionBank [PlayGame]" {
  version = "2026.03.13"
  updatedAtUtc = "2026-03-13T10:00:00Z"
}

object q1 as "q1:Question [AnswerQuestion]" {
  questionId = "Q-001"
  prompt = "What is 2+2?"
  choices = "[A:3,B:4,C:5]"
  correctAnswerId = "B"
  difficulty = "Easy"
}

object gs1 as "gs1:GameSession [PlayGame]" {
  sessionId = "S-1001"
  startedAtUtc = "2026-03-13T10:05:00Z"
  currentQuestionIndex = 0
  score = 0
  status = "InProgress"
}

object fb1 as "fb1:Feedback [GetFeedback]" {
  isCorrect = true
  message = "Correct!"
  awardedPoints = 10
}

object admin1 as "admin1:AdminUser [ManageQuestions]" {
  adminId = "A-01"
  username = "contentAdmin"
  isLocked = false
  failedAttempts = 0
  lastLoginAtUtc = "2026-03-13T09:55:00Z"
}

object cur1 as "cur1:ContentUpdateRequest [UpdateQuestions]" {
  requestId = "R-9001"
  adminId = "A-01"
  submittedAtUtc = "2026-03-13T10:10:00Z"
  schemaVersion = "1.0"
  jsonPayload = "{...questions...}"
}

object repo1 as "repo1:ContentRepository [UpdateQuestions]" {
  contentPath = "/data/questions.json"
  tempPath = "/data/questions.json.tmp"
}

object al1 as "al1:AuditLog [AuditChanges]" {
  retentionYears = 2
}

object ae1 as "ae1:AuditLogEntry [AuditChanges]" {
  entryId = "E-777"
  timestampUtc = "2026-03-13T10:10:02Z"
  adminId = "A-01"
  remoteIp = "203.0.113.10"
  action = "UpdateQuestions"
  beforeHash = "sha256:aaa..."
  afterHash = "sha256:bbb..."
  details = "Updated Q-001 choices"
}

gs1 o-- qb1
qb1 *-- q1
gs1 --> fb1

cur1 --> admin1
repo1 --> cur1
al1 *-- ae1
ae1 --> admin1

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_GameSession
hide empty description

state "GameSession Lifecycle" as GSL {
  [*] --> Created

  Created --> InProgress : start()/initSession
  InProgress --> ShowingQuestion : nextQuestion()/render
  ShowingQuestion --> AwaitingAnswer : displayPrompt
  AwaitingAnswer --> Evaluating : submitAnswer(answerId)
  Evaluating --> ShowingFeedback : computeScore/emitFeedback
  ShowingFeedback --> ShowingQuestion : nextQuestion() [hasMoreQuestions]
  ShowingFeedback --> Completed : end() [!hasMoreQuestions]

  Completed --> [*]
}

note right of Evaluating
NFR/ASR-derived UX constraint:
feedback should be observable quickly (e.g., DOM update within target window).
assumption: exact timing not provided; enforce via UI event + test harness.
end note

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_UpdateQuestions
start

:Admin opens Admin UI;
:Enter username/password;
:Authenticate [SecurityCheck];

if (Auth OK?) then (yes)
  :Load current questions.json;
  :Admin edits questions;
  :Submit update request;

  :Validate JSON schema [ContractCheck];
  if (Valid?) then (yes)
    :Read current file hash;
    :Write temp file;
    :fsync temp file;
    :Atomic rename temp->questions.json [AtomicWrite];
    :Re-read and verify hash/version;
    :Append audit entry [Audit];
    :Return success;
  else (no)
    :Return validation errors;
  endif

else (no)
  :Increment failed attempts;
  if (>=5 failures?) then (yes)
    :Lock account;
  endif
  :Return auth error;
endif

stop

note right
ASR mapping:
- Hardened auth: lockout after 5 failures, session timeout (not shown)
- Contract-first: JSON schema validation server-side
- Atomic update: temp + atomic rename to prevent corruption
- Audit: append-only entry with UTC timestamp, adminId, remoteIp, before/after
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_PlayAndAnswer
title S1: EndUser plays game and answers a question

actor EndUser
participant "WebUI" as WebUI
participant "GameController" as GameController
participant "QuestionService" as QuestionService
database "ContentRepository" as ContentRepository

EndUser -> WebUI : StartGame
WebUI -> GameController : start()
GameController -> QuestionService : loadQuestionBank
QuestionService -> ContentRepository : readJson
ContentRepository --> QuestionService : questionsJson
QuestionService --> GameController : questionBank
GameController --> WebUI : RenderIntro
WebUI --> EndUser : ShowIntro

WebUI -> GameController : nextQuestion
GameController -> QuestionService : getQuestion(index)
QuestionService --> GameController : question
GameController --> WebUI : RenderQuestion

EndUser -> WebUI : SubmitAnswer
WebUI -> GameController : submitAnswer(answerId)
GameController -> QuestionService : evaluateAnswer(questionId, answerId)
QuestionService --> GameController : feedback
GameController --> WebUI : RenderFeedback
WebUI --> EndUser : ShowFeedback

note right of WebUI
assumption: HTML5-only runtime (no plugins).
Intro/animations/audio via standard browser APIs.
end note

@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_AdminUpdateQuestions
title S2: Admin updates questions with schema validation, atomic write, and audit

actor Admin
participant "AdminWebUI" as AdminWebUI
participant "AdminController" as AdminController
participant "AuthService" as AuthService
participant "ContentService" as ContentService
database "ContentRepository" as ContentRepository
database "AuditLog" as AuditLog

Admin -> AdminWebUI : Login
AdminWebUI -> AdminController : login(username,password)
AdminController -> AuthService : authenticate
AuthService --> AdminController : authResult(sessionId/deny)
AdminController --> AdminWebUI : LoginResult

Admin -> AdminWebUI : SubmitUpdate
AdminWebUI -> AdminController : updateQuestions(jsonPayload)
AdminController -> AuthService : authorize(sessionId,"UpdateQuestions")
AuthService --> AdminController : authorized

AdminController -> ContentService : validateAgainstSchema(jsonPayload)
ContentService --> AdminController : valid/invalid

alt valid
  AdminController -> ContentService : writeAtomic(jsonPayload)
  ContentService -> ContentRepository : writeTemp
  ContentRepository --> ContentService : tempWritten
  ContentService -> ContentRepository : atomicRename
  ContentRepository --> ContentService : renamed
  ContentService --> AdminController : updateOk(beforeHash,afterHash)

  AdminController -> AuditLog : append(adminId,remoteIp,action,beforeHash,afterHash)
  AuditLog --> AdminController : appended
  AdminController --> AdminWebUI : UpdateSuccess
else invalid
  AdminController --> AdminWebUI : ValidationErrors
end

note right of AuthService
ASR: lockout after 5 failures; salted hashing (bcrypt/Argon2);
HTTPS-only endpoints (deployment concern).
end note

@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_PlayAndAnswer
title Collaboration S1: Play and Answer

actor EndUser
rectangle WebUI
rectangle GameController
rectangle QuestionService
database ContentRepository

EndUser -- WebUI
WebUI -- GameController
GameController -- QuestionService
QuestionService -- ContentRepository

WebUI : 1. StartGame
GameController : 2. start()
QuestionService : 3. loadQuestionBank
ContentRepository : 4. readJson
WebUI : 5. RenderIntro
WebUI : 6. nextQuestion
QuestionService : 7. getQuestion
WebUI : 8. RenderQuestion
WebUI : 9. SubmitAnswer
GameController : 10. submitAnswer
QuestionService : 11. evaluateAnswer
WebUI : 12. RenderFeedback

note right
Scenario mapping: EndUser plays game, loads questions, answers, receives feedback.
end note

@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_AdminUpdateQuestions
title Collaboration S2: Admin Update Questions

actor Admin
rectangle AdminWebUI
rectangle AdminController
rectangle AuthService
rectangle ContentService
database ContentRepository
database AuditLog

Admin -- AdminWebUI
AdminWebUI -- AdminController
AdminController -- AuthService
AdminController -- ContentService
ContentService -- ContentRepository
AdminController -- AuditLog

AdminWebUI : 1. Login
AdminController : 2. login()
AuthService : 3. authenticate
AdminWebUI : 4. SubmitUpdate
AdminController : 5. authorize
ContentService : 6. validateAgainstSchema
ContentRepository : 7. writeTemp
ContentRepository : 8. atomicRename
AuditLog : 9. append

note right
Scenario mapping: Admin updates questions with server-side schema validation,
atomic file update, and audit logging/retention.
end note

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as ui {
  note bottom: HTML5 Web UI (no plugins)\n[Usability][Maintainability]
}

package "api" as api {
  note bottom: HTTP controllers for game + admin\n[Security]
}

package "domain" as domain {
  note bottom: Core entities + rules\n[Modifiability]
}

package "services" as services {
  note bottom: Use-case services (game, content, auth)\n[Performance][Security]
}

package "persistence" as persistence {
  note bottom: File-based JSON repo + atomic writes\n[Reliability]
}

package "audit" as audit {
  note bottom: Append-only audit + export\n[Compliance]
}

ui ..> api : uses
api ..> services : calls
services ..> domain : uses
services ..> persistence : reads/writes
services ..> audit : appends
audit ..> persistence : stores

note right of persistence
ASR: atomic rename semantics; validate before write.
end note

note right of audit
ASR: retention >= 2 years; include UTC timestamp, adminId, remoteIp, before/after.
end note

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

component "WebUI" as WebUI <<UI>> [PlayGame]
component "AdminWebUI" as AdminWebUI <<UI>> [ManageQuestions]

component "GameAPI" as GameAPI <<API>> [PlayGame]
component "AdminAPI" as AdminAPI <<API>> [UpdateQuestions]

component "GameController" as GameController <<Controller>>
component "AdminController" as AdminController <<Controller>>

component "QuestionService" as QuestionService <<Service>> [Cacheable]
component "ContentService" as ContentService <<Service>> [ContractFirst]
component "AuthService" as AuthService <<Service>> [HardenedAuth]
component "AuditService" as AuditService <<Service>> [AppendOnly]

database "ContentRepository" as ContentRepository <<FileStore>> [AtomicWrite]
database "AuditLog" as AuditLog <<LogStore>> [Retention2Y]

interface "IGame" as IGame
interface "IAdmin" as IAdmin
interface "IAuth" as IAuth
interface "IContent" as IContent
interface "IAudit" as IAudit

WebUI --> GameAPI
AdminWebUI --> AdminAPI

GameAPI - IGame
AdminAPI - IAdmin

GameAPI --> GameController
AdminAPI --> AdminController

GameController --> QuestionService
AdminController --> AuthService
AdminController --> ContentService
AdminController --> AuditService

AuthService - IAuth
ContentService - IContent
AuditService - IAudit

QuestionService --> ContentRepository
ContentService --> ContentRepository
AuditService --> AuditLog

note right of ContentService
ASR: JSON schema validation server-side (contract-first).
end note

note right of ContentRepository
ASR: temp-file + atomic rename; prevent corruption.
end note

note right of AuthService
ASR: bcrypt/Argon2, lockout after 5 failures, session timeout.
end note

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam componentStyle rectangle

node "User Device\n(Browser)" as UserDevice {
  artifact "WebUI" as AWebUI
}

node "Admin Device\n(Browser)" as AdminDevice {
  artifact "AdminWebUI" as AAdminWebUI
}

node "Web Server Node" as WebServer {
  artifact "GameAPI" as AGameAPI
  artifact "AdminAPI" as AAdminAPI
  artifact "QuestionService" as AQuestionService
  artifact "ContentService" as AContentService
  artifact "AuthService" as AAuthService
  artifact "AuditService" as AAuditService
}

node "Storage Volume" as Storage {
  artifact "questions.json" as QuestionsJson
  artifact "audit.log" as AuditFile
}

UserDevice --> WebServer : HTTPS
AdminDevice --> WebServer : HTTPS

WebServer --> Storage : local FS / mounted volume

note right of WebServer
ASR: HTTPS-only admin endpoints.
Auth hardening + audit logging enforced server-side.
end note

note right of Storage
ASR: atomic rename for questions.json updates.
Audit retention >= 2 years (storage sizing/backup policy).
end note

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
left to right direction
skinparam componentStyle rectangle

rectangle "EndUser Browser" as C_EndUserBrowser <<Container>> {
  component "WebUI\n[PlayGame][HTML5-only]" as C_WebUI
}

rectangle "Admin Browser" as C_AdminBrowser <<Container>> {
  component "AdminWebUI\n[ManageQuestions]" as C_AdminWebUI
}

rectangle "Backend" as C_Backend <<Container>> {
  component "GameAPI\n[PlayGame]" as C_GameAPI
  component "AdminAPI\n[UpdateQuestions]" as C_AdminAPI
  component "AuthService\n[HardenedAuth]" as C_AuthService
  component "ContentService\n[ContractFirst]" as C_ContentService
  component "QuestionService\n[Cacheable]" as C_QuestionService
  component "AuditService\n[AppendOnly]" as C_AuditService
}

rectangle "Data" as C_Data <<Container>> {
  database "ContentRepository\nquestions.json\n[AtomicWrite]" as C_ContentRepository
  database "AuditLog\n[Retention2Y]" as C_AuditLog
}

C_WebUI --> C_GameAPI : HTTPS/JSON
C_AdminWebUI --> C_AdminAPI : HTTPS/JSON

C_GameAPI --> C_QuestionService
C_QuestionService --> C_ContentRepository : readJson

C_AdminAPI --> C_AuthService : authenticate/authorize
C_AdminAPI --> C_ContentService : validate/writeAtomic
C_ContentService --> C_ContentRepository : writeTemp+atomicRename
C_AdminAPI --> C_AuditService : append
C_AuditService --> C_AuditLog : append-only

note right of C_Backend
Style: layered/hexagonal within backend (controllers->services->repositories).
Tactics: server-side validation, atomic writes, audit append-only, auth lockout.
end note

@enduml
```