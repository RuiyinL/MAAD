## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCase
left to right direction
skinparam packageStyle rectangle

actor "EndUser" as EndUser
actor "Admin" as Admin

rectangle "Math Umbrella (Web Menu)" {
  usecase "Launch Menu\n(LaunchMenu)" as UC_LaunchMenu
  usecase "Open Project\n(OpenProject)" as UC_OpenProject
  usecase "Open External Resource\n(OpenExternal)" as UC_OpenExternal
}

rectangle "Space Fractions (Game)" {
  usecase "Play Intro\n(PlayIntro)" as UC_PlayIntro
  usecase "Skip Intro\n(SkipIntro)" as UC_SkipIntro
  usecase "View Help\n(ViewHelp)" as UC_ViewHelp
  usecase "Start Game\n(StartGame)" as UC_StartGame
  usecase "Answer Question\n(AnswerQuestion)" as UC_AnswerQuestion
  usecase "Get Hint\n(GetHint)" as UC_GetHint
  usecase "View Results\n(ViewResults)" as UC_ViewResults
  usecase "Replay or Exit\n(ReplayExit)" as UC_ReplayExit
}

rectangle "Question Admin (Updater)" {
  usecase "Admin Login\n(AdminLogin)" as UC_AdminLogin
  usecase "Edit Question\n(EditQuestion)" as UC_EditQuestion
  usecase "Publish Question Bank\n(PublishQuestions)" as UC_PublishQuestions
}

EndUser --> UC_LaunchMenu
EndUser --> UC_OpenProject
UC_OpenProject ..> UC_OpenExternal : <<extend>>
EndUser --> UC_PlayIntro
UC_PlayIntro ..> UC_SkipIntro : <<extend>>
EndUser --> UC_ViewHelp
EndUser --> UC_StartGame
EndUser --> UC_AnswerQuestion
UC_AnswerQuestion ..> UC_GetHint : <<extend>>
EndUser --> UC_ViewResults
EndUser --> UC_ReplayExit

Admin --> UC_AdminLogin
Admin --> UC_EditQuestion
UC_EditQuestion ..> UC_PublishQuestions : <<include>>

note right of UC_OpenExternal
FR-014: separate window/tab
end note

note bottom of UC_ViewResults
ASR-002: score session-local
end note

note bottom of UC_AdminLogin
NFR-008: HTTPS, pw>=12, lockout(5)
end note

' assumption: "user" => EndUser; "Denominators web page" treated as External Resource opened from menu
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml Class
skinparam classAttributeIconSize 0

class GameApp {
  -appVersion: String
  -lastSyncAt: String
  +boot(): void
  +loadQuestionBank(): void
  +showMainMenu(): void
}

class MenuController {
  +playIntro(): void
  +skipIntro(): void
  +showHelp(): void
  +openExternal(url: String): void
}

class GameSession {
  -sessionId: String
  -startedAt: String
  -currentQuestionId: String
  -attemptsThisQuestion: int
  -pointsLockedForQuestion: boolean
  +start(): void
  +submitAnswer(choiceIndex: int): boolean
  +requestHint(): String
  +advance(nextQuestionId: String): void
  +finish(): void
}

class ScoreBoard <<immutable>> {
  -correctCount: int
  -totalQuestions: int
  -scorePoints: int
  -rank: String
  -message: String
  +awardPoints(points: int): ScoreBoard
  +lockPointsForCurrentQuestion(): ScoreBoard
  +computeRank(): String
  +composeMessage(): String
}

class QuestionBank <<cacheable>> {
  -version: String
  -etag: String
  -ttlSeconds: int
  +getQuestion(id: String): Question
  +getStartQuestionId(): String
  +reloadIfStale(now: String): boolean
}

class Question {
  +id: String
  +prompt: String
  +choices: String[ ]
  +correctIndex: int
  +critical: boolean
  +branchRules: BranchRule[ ]
  +inputMode: String
  +isCorrect(choiceIndex: int): boolean
  +nextQuestionId(answerCorrect: boolean): String
}

class BranchRule {
  +condition: String
  +nextQuestionId: String
}

class FractionInputValidator {
  +validate(numeratorText: String, denominatorText: String): ValidationResult
}

class ValidationResult {
  +valid: boolean
  +numerator: int
  +denominator: int
  +errorMessage: String
}

class PhysicsEngine {
  -currentVelocity: float
  +applyVelocityDelta(delta: float): void
  +setVelocity(v: float): void
}

class FractionConverter {
  +toDecimal(numerator: int, denominator: int): float
}

class FeedbackAnimator {
  +playCorrect(): void
  +playIncorrect(): void
  +showMessage(text: String): void
}

class SidekickAssistant {
  +getUsabilityHint(context: String): String
  +getAnswerHint(question: Question): String
}

class AdminUpdaterUI {
  +login(username: String, password: String): void
  +editQuestion(q: Question): void
  +publish(): void
}

class AdminAuthService {
  +authenticate(username: String, password: String): boolean
  +recordFailedAttempt(username: String): void
  +lockoutIfNeeded(username: String): void
}

class AuditLogger <<persisted>> {
  +logEvent(adminId: String, eventType: String, sourceIp: String): void
}

class QuestionBankRepository <<persisted>> {
  -filePath: String
  +readCurrent(): QuestionBank
  +validateSchema(bank: QuestionBank): boolean
  +atomicWrite(bank: QuestionBank): void
}

GameApp *-- MenuController
GameApp *-- GameSession
GameApp *-- QuestionBank

GameSession *-- ScoreBoard
GameSession o-- QuestionBank
GameSession --> FeedbackAnimator
GameSession --> SidekickAssistant
GameSession --> PhysicsEngine
GameSession --> FractionInputValidator
FractionInputValidator --> ValidationResult
PhysicsEngine <-- FractionConverter

QuestionBank *-- Question
Question *-- BranchRule

AdminUpdaterUI --> AdminAuthService
AdminUpdaterUI --> QuestionBankRepository
AdminUpdaterUI --> AuditLogger
QuestionBankRepository --> AuditLogger : logs publish

note right of QuestionBank
ASR-004: versioned JSON schema
ETag + TTL<=60s reload policy
end note

note right of AdminAuthService
NFR-008/ASR-005:
HTTPS-only, pw>=12, lockout after 5,
hash (bcrypt/Argon2), server sessions
end note

note bottom of GameSession
ASR-002: score/state session-local (single user per instance)
end note

note bottom of PhysicsEngine
NFR-006: real-time velocity update
end note
@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml Object
skinparam classAttributeIconSize 0

object "app1:GameApp\n[StartGame]" as app1 {
  appVersion = "1.0.0"
  lastSyncAt = "2026-04-20T10:00:12Z"
}

object "bank1:QuestionBank\n[LoadQuestions]" as bank1 {
  version = "2026.04.20-3"
  etag = "W/\"qbank-9f21\""
  ttlSeconds = 60
}

object "sess1:GameSession\n[AnswerQuestion]" as sess1 {
  sessionId = "sess-7c2a"
  currentQuestionId = "Q-CRIT-05"
  attemptsThisQuestion = 1
  pointsLockedForQuestion = false
}

object "q5:Question\n[Branching]" as q5 {
  id = "Q-CRIT-05"
  prompt = "Which fraction equals 0.5?"
  correctIndex = 2
  critical = true
  inputMode = "multipleChoice"
}

object "score1:ScoreBoard\n[LocalScore]" as score1 {
  correctCount = 4
  totalQuestions = 10
  scorePoints = 40
  rank = "Cadet"
  message = "Good work—try again for Captain!"
}

object "phys1:PhysicsEngine\n[RealTimeVelocity]" as phys1 {
  currentVelocity = 12.5
}

app1 -- bank1
app1 -- sess1
sess1 -- q5
sess1 -- score1
sess1 -- phys1
@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml State
hide empty description

state "GameSession" as GS {
  [*] --> Booting : boot()
  Booting --> IntroPlaying : playIntro()
  IntroPlaying --> MainMenu : introFinished
  IntroPlaying --> MainMenu : SkipIntro / skipIntro()

  MainMenu --> HelpScreen : ViewHelp
  HelpScreen --> MainMenu : Back

  MainMenu --> LoadingQuestions : StartGame
  LoadingQuestions --> InQuestion : questionsReady

  state InQuestion {
    [*] --> Presenting
    Presenting --> AwaitingAnswer : showQuestion
    AwaitingAnswer --> Evaluating : AnswerQuestion

    Evaluating --> CorrectFeedback : [isCorrect] / playCorrect
    Evaluating --> IncorrectFeedback : [!isCorrect] / playIncorrect

    IncorrectFeedback --> AwaitingAnswer : Retry / lockPointsForCurrentQuestion
    CorrectFeedback --> BranchDecision : Advance

    BranchDecision --> Presenting : [hasNext] / advance(nextId)
    BranchDecision --> Results : [isLast] / finish()
  }

  Results --> EndingScene : ViewResults
  EndingScene --> MainMenu : ReplayExit [replay]
  EndingScene --> [*] : ReplayExit [exit]
}

note right of IntroPlaying
FR-002: click-to-skip
end note

note right of LoadingQuestions
ASR-004: read versioned JSON
ETag/TTL reload<=60s
end note

note right of Evaluating
FR-005: incorrect => retry, no points
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml Activity
start
:LaunchMenu;
:OpenProject (Space Fractions);

:Load Web App Shell;
note right
ASR-001/NFR-003: HTML5/JS, no plugins
end note

:PlayIntro;
if (Click to skip?) then (yes)
  :SkipIntro;
else (no)
  :Wait until intro ends;
endif
:ShowMainMenu;

if (ViewHelp?) then (yes)
  :DisplayHelp;
  :ReturnToMenu;
endif

:StartGame;
:Fetch QuestionBank [CacheCheck];
note right
ASR-004: ETag + Cache-Control
TTL <= 60s
end note

repeat
  :PresentQuestion;
  if (Hint requested?) then (yes)
    :ShowSidekickHint;
  endif

  :GetAnswer (mouse click);
  :EvaluateAnswer;
  if (Correct?) then (yes)
    :PlayCorrect Feedback;
    :UpdateScore (award points);
  else (no)
    :PlayIncorrect Feedback;
    :LockPointsForQuestion;
    :RetrySameQuestion;
  endif

  if (FractionInput question?) then (yes)
    :ValidateFractionInput;
    if (Valid?) then (yes)
      :ConvertToDecimal;
      :ApplyVelocityDelta [Immediate];
      note right
NFR-006: real-time update
end note
    else (no)
      :ShowErrorMessage;
    endif
  endif

  :ApplyBranchRule;
repeat while (HasNextQuestion?) is (yes)

:ComputeRankAndMessage;
:ShowEndingScene;
if (Replay?) then (yes)
  :ReturnToMainMenu;
  stop
else (no)
  :ExitGame;
  stop
endif
@enduml
```

6. Sequence — Process View: Sequence Diagram

```plantuml
@startuml Sequence_S1_Gameplay
title S1: EndUser plays question sequence with branching + scoring

actor EndUser
participant "GameApp" as GameApp
participant "MenuController" as MenuController
participant "GameSession" as GameSession
participant "QuestionBank" as QuestionBank
participant "FeedbackAnimator" as FeedbackAnimator
participant "SidekickAssistant" as SidekickAssistant

EndUser -> GameApp : OpenProject
GameApp -> MenuController : PlayIntro
alt SkipIntro
  EndUser -> MenuController : SkipIntro
end
MenuController -> GameApp : ShowMainMenu

EndUser -> MenuController : StartGame
MenuController -> GameApp : StartGame
GameApp -> QuestionBank : reloadIfStale()
QuestionBank --> GameApp : questionsReady(version, etag)

GameApp -> GameSession : start()
loop For each question
  GameSession -> QuestionBank : getQuestion(id)
  QuestionBank --> GameSession : Question
  GameSession -> FeedbackAnimator : showMessage(prompt+choices)

  opt GetHint
    EndUser -> GameSession : requestHint()
    GameSession -> SidekickAssistant : getAnswerHint(question)
    SidekickAssistant --> GameSession : hintText
    GameSession -> FeedbackAnimator : showMessage(hintText)
  end

  EndUser -> GameSession : submitAnswer(choiceIndex)
  alt Correct
    GameSession -> FeedbackAnimator : playCorrect()
  else Incorrect
    GameSession -> FeedbackAnimator : playIncorrect()
    note right of GameSession
      FR-005: retry, no points
    end note
  end
  GameSession -> GameSession : advance(nextQuestionId)
end

GameSession -> FeedbackAnimator : showMessage(results+rank)
EndUser -> MenuController : ReplayExit
@enduml
```

```plantuml
@startuml Sequence_S2_AdminUpdate
title S2: Admin updates question bank and publishes to server file

actor Admin
participant "AdminUpdaterUI" as AdminUpdaterUI
participant "AdminAuthService" as AdminAuthService
participant "QuestionBankRepository" as QuestionBankRepository
participant "AuditLogger" as AuditLogger

Admin -> AdminUpdaterUI : AdminLogin(username,password)
AdminUpdaterUI -> AdminAuthService : authenticate()
alt Auth OK
  AdminAuthService --> AdminUpdaterUI : authToken/sessionOk
  Admin -> AdminUpdaterUI : EditQuestion(formData)
  AdminUpdaterUI -> QuestionBankRepository : readCurrent()
  QuestionBankRepository --> AdminUpdaterUI : QuestionBank(version)

  AdminUpdaterUI -> QuestionBankRepository : validateSchema(updatedBank)
  QuestionBankRepository --> AdminUpdaterUI : valid

  Admin -> AdminUpdaterUI : PublishQuestions
  AdminUpdaterUI -> QuestionBankRepository : atomicWrite(updatedBank+versionBump)
  QuestionBankRepository -> AuditLogger : logEvent(adminId,"PublishQuestions",sourceIp)
  AuditLogger --> QuestionBankRepository : logged
  QuestionBankRepository --> AdminUpdaterUI : publishOk(etag,newVersion)
  AdminUpdaterUI --> Admin : Confirmation(newVersion)
else Auth FAIL
  AdminAuthService --> AdminUpdaterUI : authFail
  AdminUpdaterUI -> AdminAuthService : recordFailedAttempt()
  AdminUpdaterUI -> AdminAuthService : lockoutIfNeeded()
  AdminUpdaterUI --> Admin : Error(lockoutOrRetry)
end

note right of AdminAuthService
NFR-008/ASR-005:
HTTPS-only, pw>=12, lockout after 5
end note

note right of QuestionBankRepository
ASR-004/FR-013:
file-based persistence, atomic write, versioned JSON
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml Collaboration_S1_Gameplay
title Collaboration (S1): Gameplay question sequence

actor EndUser
rectangle "GameApp" as GameApp
rectangle "MenuController" as MenuController
rectangle "GameSession" as GameSession
rectangle "QuestionBank" as QuestionBank
rectangle "FeedbackAnimator" as FeedbackAnimator
rectangle "SidekickAssistant" as SidekickAssistant

EndUser -- MenuController
MenuController -- GameApp
GameApp -- QuestionBank
GameApp -- GameSession
GameSession -- QuestionBank
GameSession -- FeedbackAnimator
GameSession -- SidekickAssistant

EndUser -> MenuController : 1. OpenProject
MenuController -> GameApp : 2. StartGame
GameApp -> QuestionBank : 3. reloadIfStale
GameApp -> GameSession : 4. start
GameSession -> QuestionBank : 5. getQuestion
GameSession -> FeedbackAnimator : 6. showMessage
EndUser -> GameSession : 7. submitAnswer
GameSession -> FeedbackAnimator : 8. playCorrect/playIncorrect
GameSession -> GameSession : 9. advance

note bottom
Origin: FR-004/FR-005/FR-008/FR-007
end note
@enduml
```

```plantuml
@startuml Collaboration_S2_AdminUpdate
title Collaboration (S2): Admin updates and publishes question bank

actor Admin
rectangle "AdminUpdaterUI" as AdminUpdaterUI
rectangle "AdminAuthService" as AdminAuthService
rectangle "QuestionBankRepository" as QuestionBankRepository
rectangle "AuditLogger" as AuditLogger

Admin -- AdminUpdaterUI
AdminUpdaterUI -- AdminAuthService
AdminUpdaterUI -- QuestionBankRepository
QuestionBankRepository -- AuditLogger

Admin -> AdminUpdaterUI : 1. AdminLogin
AdminUpdaterUI -> AdminAuthService : 2. authenticate
Admin -> AdminUpdaterUI : 3. EditQuestion
AdminUpdaterUI -> QuestionBankRepository : 4. readCurrent
AdminUpdaterUI -> QuestionBankRepository : 5. validateSchema
Admin -> AdminUpdaterUI : 6. PublishQuestions
AdminUpdaterUI -> QuestionBankRepository : 7. atomicWrite(versionBump)
QuestionBankRepository -> AuditLogger : 8. logEvent

note bottom
Origin: FR-012/FR-013 + NFR-007/NFR-008 + ASR-004/ASR-005
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml Package
skinparam packageStyle rectangle

package "ui" as UI {
  note bottom
  Menus, intro, help, feedback, sidekick
  NFR-004 usability (mouse-driven)
  end note
}

package "domain" as Domain {
  note bottom
  Deterministic rules: validation, scoring, branching
  ASR-003 environment-invariant behavior
  end note
}

package "content" as Content {
  note bottom
  Question schema, versioning, TTL/ETag reload
  ASR-004 + ASR-006 bandwidth tactics
  end note
}

package "infrastructure" as Infra {
  note bottom
  HTTP, caching headers, storage adapters
  end note
}

package "admin" as AdminPkg {
  note bottom
  Admin updater UI + backend endpoints
  ASR-005 security + audit
  end note
}

package "security" as Security {
  note bottom
  Auth, sessions, password policy, lockout
  NFR-008
  end note
}

package "observability" as Obs {
  note bottom
  Audit logging + diagnostics hooks
  end note
}

UI ..> Domain : uses
UI ..> Content : uses
Domain ..> Content : reads
Content ..> Infra : uses
AdminPkg ..> Security : uses
AdminPkg ..> Content : updates
AdminPkg ..> Infra : uses
AdminPkg ..> Obs : logs
Security ..> Infra : uses
Obs ..> Infra : uses
@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml Component
skinparam componentStyle rectangle

component "MathUmbrellaWeb\n[LaunchMenu]" as MathUmbrellaWeb
component "SpaceFractionsSPA\n[PlayIntro|Gameplay]" as SpaceFractionsSPA
component "GameEngine\n[Scoring|Branching|Validation]" as GameEngine
component "RenderAudioUI\n[Canvas|WebAudio]" as RenderAudioUI
component "ContentLoader\n[ETag|TTL<=60s]" as ContentLoader

component "AdminUpdaterWeb\n[EditQuestion]" as AdminUpdaterWeb
component "AdminBackendAPI\n[PublishQuestions]" as AdminBackendAPI
component "AuthSessionService\n[PasswordPolicy|Lockout]" as AuthSessionService
component "AuditLogService\n[Auditability]" as AuditLogService
database  "QuestionBankFileStore\n[JSON File]" as QuestionBankFileStore

interface "IQuestionBank" as IQuestionBank
interface "IAdminAuth" as IAdminAuth
interface "IAuditLog" as IAuditLog

SpaceFractionsSPA --> RenderAudioUI : uses
SpaceFractionsSPA --> GameEngine : uses
SpaceFractionsSPA --> ContentLoader : uses
ContentLoader ..> IQuestionBank
GameEngine ..> IQuestionBank

AdminUpdaterWeb --> AdminBackendAPI : HTTPS
AdminBackendAPI ..> IAdminAuth
AdminBackendAPI ..> IAuditLog
AdminBackendAPI --> QuestionBankFileStore : read/write (atomic)
AuditLogService --> QuestionBankFileStore : (optional) append-only log file

AuthSessionService - IAdminAuth
AuditLogService - IAuditLog
ContentLoader - IQuestionBank

MathUmbrellaWeb --> SpaceFractionsSPA : open new window/tab
MathUmbrellaWeb ..> AdminUpdaterWeb : link (restricted)

note right of AdminBackendAPI
ASR-005/NFR-008: HTTPS-only, sessions, hash (Argon2/bcrypt),
lockout after 5 failed attempts, audit privileged ops
end note

note right of ContentLoader
ASR-004 decision: ETag + Cache-Control + TTL reload<=60s
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml Deployment
skinparam componentStyle rectangle

node "Student Device\n(Windows/macOS)\n<<Browser>>" as StudentDevice {
  artifact "MathUmbrellaWeb" as A_Umbrella
  artifact "SpaceFractionsSPA" as A_SPA
}

node "Admin Device\n<<Browser>>" as AdminDevice {
  artifact "AdminUpdaterWeb" as A_AdminWeb
}

node "Web Server\n<<HTTPS/TLS>>" as WebServer {
  artifact "Static Asset Host\n(HTML/JS/CSS/media)" as A_Static
  artifact "AdminBackendAPI" as A_AdminAPI
  artifact "AuthSessionService" as A_Auth
  artifact "AuditLogService" as A_Audit
  artifact "QuestionBankFileStore\n(JSON file on disk)" as A_File
}

StudentDevice --> WebServer : HTTPS (assets + qbank.json)\n[ETag/Cache-Control]
AdminDevice --> WebServer : HTTPS (admin login/update)

note right of StudentDevice
NFR-003: latest 2 versions of major browsers
ASR-001: no plugins
end note

note right of WebServer
ASR-004: atomic file writes + version bump
ASR-005: audit logging + secure auth/session
end note

note bottom of StudentDevice
ASR-002: session-local score/state (single-user per running instance)
end note
@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml Container
skinparam packageStyle rectangle
left to right direction

rectangle "EndUser Browser\n<<Container>>" as C_EndUser {
  rectangle "SpaceFractionsSPA\n[PlayIntro|Gameplay]\nHTML5/JS/Canvas/WebAudio" as SPA
  rectangle "GameEngine (in-browser)\n[Scoring|Branching|Validation]\nSession-local state" as Engine
  rectangle "ContentLoader\n[ETag|TTL<=60s]" as Loader
  rectangle "MathUmbrellaWeb\n[LaunchMenu]" as Umbrella
}

rectangle "Admin Browser\n<<Container>>" as C_Admin {
  rectangle "AdminUpdaterWeb\n[EditQuestion]" as AdminWeb
}

rectangle "Web Server\n<<Container>>" as C_Server {
  rectangle "StaticAssetHost\n[Media|JS|CSS|qbank.json]" as StaticHost
  rectangle "AdminBackendAPI\n[PublishQuestions]" as AdminAPI
  rectangle "AuthSessionService\n[PasswordPolicy|Lockout]" as AuthSvc
  rectangle "AuditLogService\n[Auditability]" as AuditSvc
  database "QuestionBankFileStore\n[Versioned JSON]\n<<File>>" as FileStore
}

Umbrella --> SPA : openSeparateWindow (FR-014)
SPA --> Engine : invoke
SPA --> Loader : loadQuestions
Loader --> StaticHost : HTTPS GET qbank.json (ETag)
Engine --> SPA : events/renderModel
SPA --> StaticHost : HTTPS GET assets (progressive)

AdminWeb --> AdminAPI : HTTPS POST publish
AdminAPI --> AuthSvc : authenticate/session
AdminAPI --> FileStore : atomicWrite + version bump
AdminAPI --> AuditSvc : logEvent
AuditSvc --> FileStore : append audit log (assumption)

note right of Loader
ASR-004: cache-control/ETag + TTL<=60s
Real-time update without restart (eventual <=60s)
end note

note right of SPA
ASR-006/NFR-010: bandwidth/load-time constraints
progressive loading for media
end note

note right of AuthSvc
NFR-008/ASR-005: HTTPS-only; pw>=12; lockout(5);
hash storage; session expiry
end note

note bottom of Engine
ASR-003: deterministic rules to keep behavior invariant across browsers
end note

' assumption: audit log stored alongside file store (file-based); could be separate durable store later
@enduml
```