## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction

actor EndUser as EndUser
actor Admin as Admin

rectangle "Web Quiz Game System" as System {
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
UC_AdminLogin ..> UC_ViewAuditLog : <<include>>

note right of System
assumption: Requirements artifacts (FR/NFR/ASR) not provided in prompt;
diagram is derived from semantic memory decisions:
- HTML5-only end-user experience (no plugins)
- Contract-first admin question updates (JSON schema + server validation)
- Atomic publish + hardened auth + audit logging/retention
end note

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class QuestionSet <<persisted>> {
  +setId: String
  +version: int
  +updatedAtUtc: String
  +load(): List<Question>
}

class Question {
  +questionId: String
  +prompt: String
  +choices: List<String>
  +correctIndex: int
  +explanation: String
  +validate(): boolean
}

class GameSession {
  +sessionId: String
  +startedAtUtc: String
  +status: SessionStatus
  +currentIndex: int
  +start(): void
  +submitAnswer(choiceIndex:int): Feedback
  +end(): Score
}

enum SessionStatus {
  New
  InProgress
  Completed
}

class Answer {
  +questionId: String
  +choiceIndex: int
  +answeredAtUtc: String
}

class Feedback {
  +isCorrect: boolean
  +message: String
  +renderWithinMs: int
}

class Score {
  +correctCount: int
  +totalCount: int
  +computedAtUtc: String
  +compute(answers:List<Answer>): void
}

class AdminUser <<persisted>> {
  +adminId: String
  +username: String
  +passwordHash: String
  +failedAttempts: int
  +lockedUntilUtc: String
  +verifyPassword(password:String): boolean
  +lockIfNeeded(): void
}

class AdminSession {
  +sessionId: String
  +adminId: String
  +createdAtUtc: String
  +expiresAtUtc: String
  +isValid(nowUtc:String): boolean
  +invalidate(): void
}

class ContentUpdateRequest {
  +requestId: String
  +submittedAtUtc: String
  +jsonPayload: String
  +schemaVersion: String
  +validateAgainstSchema(): boolean
}

class ContentRepository <<persisted>> {
  +path: String
  +readCurrent(): QuestionSet
  +writeTemp(payload:String): String
  +atomicPublish(tempPath:String): void
}

class AuditLogEntry <<immutable>> <<persisted>> {
  +entryId: String
  +timestampUtc: String
  +adminId: String
  +remoteIp: String
  +action: String
  +entity: String
  +beforeJson: String
  +afterJson: String
  +appendOnly(): void
}

QuestionSet "1" o-- "1..*" Question
GameSession "1" o-- "0..*" Answer
GameSession "1" --> "1" QuestionSet : uses
GameSession "1" --> "1" Score : produces
GameSession "1" --> "0..*" Feedback : emits

AdminUser "1" --> "0..*" AdminSession
ContentUpdateRequest "1" --> "1" QuestionSet : proposes
ContentRepository "1" --> "0..*" QuestionSet : stores
AuditLogEntry "0..*" --> "1" AdminUser : actor

note right of ContentRepository
ASR: atomic file update semantics
- writeTemp() then atomicPublish()
- prevent corruption on crash
end note

note right of ContentUpdateRequest
ASR: contract-first JSON schema
- validateAgainstSchema() server-side
end note

note right of AdminUser
ASR: hardened auth
- >=12 char passwords (policy)
- salted hashing (bcrypt/Argon2)
- lockout after 5 failures
end note

note right of AuditLogEntry
ASR: audit logging/retention
- append-only
- required fields (UTC, adminId, IP, before/after)
- retention >= 2 years
end note

note right of Feedback
NFR (from semantic memory): UI feedback observable within 500ms
end note

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_LogicView

object questionSet1 as "questionSet1:QuestionSet [PlayGame]" {
  setId = "qs-2026-03"
  version = 12
  updatedAtUtc = "2026-03-01T10:00:00Z"
}

object q1 as "q1:Question [AnswerQuestion]" {
  questionId = "Q-001"
  prompt = "What is 2+2?"
  choices = "[2,3,4,5]"
  correctIndex = 2
  explanation = "2+2=4"
}

object session1 as "session1:GameSession [PlayGame]" {
  sessionId = "sess-9f2a"
  startedAtUtc = "2026-03-14T09:00:00Z"
  status = InProgress
  currentIndex = 0
}

object ans1 as "ans1:Answer [AnswerQuestion]" {
  questionId = "Q-001"
  choiceIndex = 2
  answeredAtUtc = "2026-03-14T09:00:10Z"
}

object fb1 as "fb1:Feedback [GetFeedback]" {
  isCorrect = true
  message = "Correct!"
  renderWithinMs = 180
}

object score1 as "score1:Score [ViewScore]" {
  correctCount = 1
  totalCount = 1
  computedAtUtc = "2026-03-14T09:00:12Z"
}

questionSet1 o-- q1
session1 --> questionSet1 : uses
session1 o-- ans1
session1 o-- fb1
session1 --> score1 : produces

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_LogicView_GameSession
hide empty description

[*] --> New : start()

New --> InProgress : startGame / loadQuestionSet
InProgress --> InProgress : submitAnswer [hasNext] / computeFeedback
InProgress --> Completed : submitAnswer [!hasNext] / computeScore
Completed --> [*] : endSession

note right of InProgress
NFR: feedback event should be observable within 500ms
(derived from semantic memory decision)
end note

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ProcessView_AdminPublish
start

:Open Admin UI;
:Enter credentials;
:Validate credentials [SecurityCheck];
if (Auth OK?) then (yes)
  :Create AdminSession;
  :Load current QuestionSet;
  :Edit questions (client-side);
  :Submit ContentUpdateRequest;
  :Validate JSON schema (server-side) [ContractCheck];
  if (Schema valid?) then (yes)
    :Write temp file;
    :Atomic publish (rename) [IntegrityCheck];
    :Append AuditLogEntry [Audit];
    :Return success;
  else (no)
    :Return validation errors;
  endif
else (no)
  :Increment failedAttempts;
  if (>=5 failures?) then (yes)
    :Lock account (cooldown);
  endif
  :Return auth error;
endif

stop

note right
ASR-driven steps:
- server-side schema validation
- atomic publish semantics
- audit logging with retention
- lockout after 5 failures
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_ProcessView_S1_AdminPublishUpdate
autonumber

actor Admin as Admin
boundary AdminWebUI as AdminWebUI
control AdminAPI as AdminAPI
control AuthService as AuthService
control ContentService as ContentService
database ContentRepository as ContentRepository
database AuditLogStore as AuditLogStore

Admin -> AdminWebUI : AdminLogin
AdminWebUI -> AdminAPI : LoginRequest
AdminAPI -> AuthService : VerifyPassword
AuthService -> AuthService : CheckLockout
AuthService --> AdminAPI : AuthResult

alt Auth OK
  AdminWebUI -> AdminAPI : SubmitUpdate
  AdminAPI -> ContentService : ValidateContent
  ContentService -> ContentService : ValidateAgainstSchema
  ContentService --> AdminAPI : ValidationOK

  AdminAPI -> ContentService : PublishUpdate
  ContentService -> ContentRepository : WriteTemp
  ContentRepository --> ContentService : TempPath
  ContentService -> ContentRepository : AtomicPublish
  ContentRepository --> ContentService : Published(version+1)

  ContentService -> AuditLogStore : AppendAudit
  AuditLogStore --> ContentService : Appended

  AdminAPI --> AdminWebUI : PublishSuccess
else Auth Failed
  AuthService -> AuthService : IncrementFailedAttempts
  AuthService -> AuthService : LockIfNeeded(>=5)
  AdminAPI --> AdminWebUI : AuthError
end

note over AdminAPI,ContentService
ASR: HTTPS-only endpoints assumed; server-side validation required;
atomic publish prevents corruption; audit retention >= 2 years.
end note

@enduml
```

```plantuml
@startuml Sequence_ProcessView_S2_EndUserPlayGame
autonumber

actor EndUser as EndUser
boundary GameWebUI as GameWebUI
control GameAPI as GameAPI
control GameService as GameService
database ContentRepository as ContentRepository

EndUser -> GameWebUI : ViewIntro
GameWebUI -> GameWebUI : LoadHTML5Intro

EndUser -> GameWebUI : StartGame
GameWebUI -> GameAPI : StartSession
GameAPI -> GameService : CreateSession
GameService -> ContentRepository : ReadCurrent
ContentRepository --> GameService : QuestionSet
GameService --> GameAPI : SessionCreated
GameAPI --> GameWebUI : SessionToken

loop For each question
  EndUser -> GameWebUI : AnswerQuestion
  GameWebUI -> GameAPI : SubmitAnswer
  GameAPI -> GameService : EvaluateAnswer
  GameService --> GameAPI : Feedback
  GameAPI --> GameWebUI : GetFeedback
end

GameWebUI -> GameAPI : EndSession
GameAPI -> GameService : ComputeScore
GameService --> GameAPI : Score
GameAPI --> GameWebUI : ViewScore

note over GameWebUI
NFR (derived): feedback should be observable within 500ms.
end note

@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_ProcessView_S1_AdminPublishUpdate
' Communication diagram for scenario S1: AdminPublishUpdate
object Admin
object AdminWebUI
object AdminAPI
object AuthService
object ContentService
object ContentRepository
object AuditLogStore

Admin -- AdminWebUI
AdminWebUI -- AdminAPI
AdminAPI -- AuthService
AdminAPI -- ContentService
ContentService -- ContentRepository
ContentService -- AuditLogStore

Admin -> AdminWebUI : 1 AdminLogin
AdminWebUI -> AdminAPI : 2 LoginRequest
AdminAPI -> AuthService : 3 VerifyPassword
AuthService -> AuthService : 4 CheckLockout
AuthService -> AdminAPI : 5 AuthResult
AdminWebUI -> AdminAPI : 6 SubmitUpdate
AdminAPI -> ContentService : 7 ValidateContent
ContentService -> ContentService : 8 ValidateAgainstSchema
AdminAPI -> ContentService : 9 PublishUpdate
ContentService -> ContentRepository : 10 WriteTemp
ContentService -> ContentRepository : 11 AtomicPublish
ContentService -> AuditLogStore : 12 AppendAudit
AdminAPI -> AdminWebUI : 13 PublishSuccess

note right
Originating scenario: "Admin publishes question updates with schema validation,
atomic file update, hardened auth, and audit logging."
end note

@enduml
```

```plantuml
@startuml Collaboration_ProcessView_S2_EndUserPlayGame
' Communication diagram for scenario S2: EndUserPlayGame
object EndUser
object GameWebUI
object GameAPI
object GameService
object ContentRepository

EndUser -- GameWebUI
GameWebUI -- GameAPI
GameAPI -- GameService
GameService -- ContentRepository

EndUser -> GameWebUI : 1 ViewIntro
GameWebUI -> GameWebUI : 2 LoadHTML5Intro
EndUser -> GameWebUI : 3 StartGame
GameWebUI -> GameAPI : 4 StartSession
GameAPI -> GameService : 5 CreateSession
GameService -> ContentRepository : 6 ReadCurrent
GameService -> GameAPI : 7 SessionCreated
GameAPI -> GameWebUI : 8 SessionToken
EndUser -> GameWebUI : 9 AnswerQuestion
GameWebUI -> GameAPI : 10 SubmitAnswer
GameAPI -> GameService : 11 EvaluateAnswer
GameService -> GameAPI : 12 Feedback
GameAPI -> GameWebUI : 13 GetFeedback
GameWebUI -> GameAPI : 14 EndSession
GameAPI -> GameService : 15 ComputeScore
GameService -> GameAPI : 16 Score
GameAPI -> GameWebUI : 17 ViewScore

note right
Originating scenario: "End user plays HTML5 game, answers questions,
receives fast feedback, and views score."
end note

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_DevelopmentView
skinparam packageStyle rectangle

package "ui" as pkg_ui {
  note bottom
  Responsibilities: HTML5/CSS/JS game + admin UI
  Constraint: no plugins (HTML5-only)
  end note
}

package "api" as pkg_api {
  note bottom
  Responsibilities: REST endpoints, request/response DTOs
  Constraint: HTTPS-only assumed
  end note
}

package "domain" as pkg_domain {
  note bottom
  Responsibilities: core models + rules (GameSession, Question, Score)
  end note
}

package "application" as pkg_app {
  note bottom
  Responsibilities: use-cases (PlayGame, PublishUpdate)
  end note
}

package "persistence" as pkg_persist {
  note bottom
  Responsibilities: file-based content repo + audit store
  Constraint: atomic publish; append-only audit
  end note
}

package "security" as pkg_sec {
  note bottom
  Responsibilities: password hashing, lockout, session mgmt
  end note
}

pkg_ui ..> pkg_api : uses
pkg_api ..> pkg_app : calls
pkg_app ..> pkg_domain : uses
pkg_app ..> pkg_persist : reads/writes
pkg_api ..> pkg_sec : authn/authz
pkg_app ..> pkg_sec : session/lockout

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_DevelopmentView
skinparam componentStyle rectangle

component "GameWebUI" as GameWebUI <<UI>> [PlayGame]
component "AdminWebUI" as AdminWebUI <<UI>> [ManageQuestions]

component "GameAPI" as GameAPI <<REST>> [PlayGame]
component "AdminAPI" as AdminAPI <<REST>> [PublishUpdate]

component "AuthService" as AuthService <<Security>> [HardenedAuth]
component "GameService" as GameService <<Application>> [GameRules]
component "ContentService" as ContentService <<Application>> [ContractFirst]
component "ContentRepository" as ContentRepository <<Persistence>> [AtomicPublish]
component "AuditLogStore" as AuditLogStore <<Persistence>> [AppendOnlyAudit]

interface "IGameAPI" as IGameAPI
interface "IAdminAPI" as IAdminAPI
interface "IAuth" as IAuth
interface "IContent" as IContent
interface "IAudit" as IAudit

GameAPI - IGameAPI
AdminAPI - IAdminAPI
AuthService - IAuth
ContentService - IContent
AuditLogStore - IAudit

GameWebUI ..> IGameAPI : HTTPS
AdminWebUI ..> IAdminAPI : HTTPS

GameAPI ..> GameService : uses
GameAPI ..> AuthService : optional (admin-only endpoints separated)

AdminAPI ..> AuthService : uses
AdminAPI ..> ContentService : uses
ContentService ..> ContentRepository : uses
ContentService ..> IAudit : appends

note right of ContentService
ASR: JSON schema validation (server-side)
end note

note right of ContentRepository
ASR: temp write + atomic rename
end note

note right of AuthService
ASR: bcrypt/Argon2, >=12 chars policy, lockout after 5 failures
end note

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_PhysicalView
skinparam nodeStyle rectangle

node "User Device\n(Browser)" as UserDevice {
  artifact "GameWebUI" as ArtGameUI
}

node "Admin Device\n(Browser)" as AdminDevice {
  artifact "AdminWebUI" as ArtAdminUI
}

node "Web Server / Reverse Proxy\n(TLS termination)" as Proxy {
  note right
  Constraint: HTTPS-only
  end note
}

node "App Server (Replica 1)" as App1 {
  artifact "GameAPI"
  artifact "AdminAPI"
  artifact "AuthService"
  artifact "GameService"
  artifact "ContentService"
}

node "App Server (Replica 2)" as App2 {
  artifact "GameAPI"
  artifact "AdminAPI"
  artifact "AuthService"
  artifact "GameService"
  artifact "ContentService"
}

node "Stateful Storage" as Storage {
  artifact "ContentRepository\n(questions.json)" as ArtContentRepo
  artifact "AuditLogStore\n(audit.log)" as ArtAudit
  note right
  ASR: atomic publish; audit retention >= 2 years
  end note
}

UserDevice --> Proxy : HTTPS
AdminDevice --> Proxy : HTTPS
Proxy --> App1 : HTTPS
Proxy --> App2 : HTTPS

App1 --> Storage : file I/O
App2 --> Storage : file I/O

note bottom of App1
assumption: active-active replicas; file locking/versioning required
to avoid concurrent admin publish conflicts.
end note

@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_PhysicalView
left to right direction
skinparam rectangleStyle rounded

rectangle "EndUser Browser" as C_EndUser {
  rectangle "GameWebUI\n[PlayGame]\nHTML5/CSS/JS" as GameWebUI
}

rectangle "Admin Browser" as C_Admin {
  rectangle "AdminWebUI\n[ManageQuestions]\nHTML5/CSS/JS" as AdminWebUI
}

rectangle "Backend" as C_Backend {
  rectangle "GameAPI\n[PlayGame]\nREST/JSON" as GameAPI
  rectangle "AdminAPI\n[PublishUpdate]\nREST/JSON" as AdminAPI
  rectangle "AuthService\n[HardenedAuth]\nlockout+sessions" as AuthService
  rectangle "GameService\n[GameRules]\nscoring+feedback" as GameService
  rectangle "ContentService\n[ContractFirst]\nJSON schema validation" as ContentService
}

rectangle "Storage" as C_Storage {
  database "ContentRepository\n[AtomicPublish]\nquestions.json" as ContentRepository
  database "AuditLogStore\n[AppendOnlyAudit]\naudit.log" as AuditLogStore
}

GameWebUI --> GameAPI : HTTPS
AdminWebUI --> AdminAPI : HTTPS

GameAPI --> GameService : in-process call
GameService --> ContentRepository : read questions

AdminAPI --> AuthService : verifyPassword/lockout
AdminAPI --> ContentService : validate+publish
ContentService --> ContentRepository : writeTemp+atomicPublish
ContentService --> AuditLogStore : append audit

note right of GameWebUI
Constraint: no plugins (HTML5-only)
end note

note right of ContentService
ASR: server-side schema validation + atomic publish
end note

note right of AuditLogStore
ASR: retention >= 2 years; append-only
end note

@enduml
```