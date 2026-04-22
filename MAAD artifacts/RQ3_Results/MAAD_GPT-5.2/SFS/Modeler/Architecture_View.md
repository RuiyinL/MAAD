## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SpaceFractions
left to right direction
skinparam packageStyle rectangle

actor "EndUser" as EndUser
actor "Admin" as Admin
actor "ExternalProjectSite" as ExternalProjectSite
actor "DenominatorsWebsite" as DenominatorsWebsite

rectangle "SpaceFractions Web System" as System {
  usecase "Play Game" as UC_PlayGame
  usecase "Watch Intro" as UC_WatchIntro
  usecase "Skip Intro" as UC_SkipIntro
  usecase "Use Main Menu" as UC_MainMenu
  usecase "Answer Questions" as UC_Answer
  usecase "Get Hint" as UC_Hint
  usecase "Adjust Velocity" as UC_Velocity
  usecase "View Final Score" as UC_FinalScore
  usecase "Try Again / Quit" as UC_EndNav
  usecase "Open Umbrella Links" as UC_Umbrella
  usecase "Open Denominators Page" as UC_Denom
  usecase "Update Questions" as UC_UpdateQ
  usecase "Admin Login" as UC_AdminLogin
}

EndUser --> UC_PlayGame
EndUser --> UC_MainMenu
EndUser --> UC_Umbrella
EndUser --> UC_Denom

UC_PlayGame ..> UC_WatchIntro : <<include>>
UC_SkipIntro ..> UC_WatchIntro : <<extend>>
EndUser --> UC_SkipIntro

UC_PlayGame ..> UC_Answer : <<include>>
UC_Answer ..> UC_Hint : <<extend>>
EndUser --> UC_Hint

UC_Answer ..> UC_Velocity : <<include>>
UC_Answer ..> UC_FinalScore : <<include>>
UC_FinalScore ..> UC_EndNav : <<include>>
EndUser --> UC_EndNav

Admin --> UC_UpdateQ
UC_UpdateQ ..> UC_AdminLogin : <<include>>
Admin --> UC_AdminLogin

UC_Umbrella --> ExternalProjectSite
UC_Denom --> DenominatorsWebsite

note right of System
assumption: "user" in FRs maps to EndUser (sixth-grade student).
assumption: ExternalProjectSite represents any Math Umbrella linked project (FR-023).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_SpaceFractions
skinparam classAttributeIconSize 0

class GameApp {
  +start(): void
  +routeTo(screen: ScreenId): void
}

class ScreenRouter {
  -currentScreen: ScreenId
  +showIntro(): void
  +showMainMenu(): void
  +showGameplay(): void
  +showEnding(): void
}

class IntroMoviePlayer {
  -isPlaying: Boolean
  +play(): void
  +skip(): void
  +onEnded(): void
}

class MainMenu {
  +showHelp(): void
  +startGame(): void
  +openDenominators(): void
  +openUmbrella(): void
}

class GameSession {
  -sessionId: String
  -score: Score
  -progress: StoryProgress
  +start(): void
  +answer(choiceId: String): FeedbackEvent
  +applyVelocityFraction(numerator: Integer, denominator: Integer): void
  +end(): GameResult
}

class QuestionBank <<cacheable>> {
  -sourceUrl: String
  -questions: Question[]
  +load(): void
  +getQuestion(id: String): Question
  +getNext(progress: StoryProgress): Question
}

class Question {
  +id: String
  +prompt: String
  +choices: Choice[]
  +answer: String
  +hint: String
  +isCritical: Boolean
}

class Choice {
  +id: String
  +text: String
}

class StoryEngine {
  +nextQuestion(progress: StoryProgress, lastCorrect: Boolean): Question
  +branch(progress: StoryProgress): void
}

class StoryProgress {
  +currentQuestionId: String
  +correctOnCritical: Boolean
  +attemptedIds: String[]
}

class Score <<local>> {
  +points: Integer
  +penalizedQuestionIds: String[]
  +addPoint(questionId: String): void
  +markNoPoint(questionId: String): void
  +rank(): String
}

class FeedbackService {
  +emitFeedback(type: String, withinMs: Integer): FeedbackEvent
  +showMessage(text: String): void
}

class FeedbackEvent {
  +type: String
  +timestampUtc: String
}

class FractionValidator {
  +validateIntegers(numerator: Integer, denominator: Integer): Boolean
  +validateNonZeroDenominator(denominator: Integer): Boolean
}

class VelocityCalculator {
  +toDecimal(numerator: Integer, denominator: Integer): Float
  +adjust(currentVelocity: Float, delta: Float): Float
}

class PhysicsEngine {
  -velocity: Float
  +setVelocity(v: Float): void
  +tick(dtMs: Integer): void
}

class AdminAuthService {
  +login(adminId: String, password: String): Boolean
  +lockoutIfNeeded(adminId: String): void
}

class AuditLogger <<persisted>> {
  +append(entry: AuditLogEntry): void
}

class AuditLogEntry {
  +timestampUtc: String
  +adminId: String
  +remoteIp: String
  +fieldChanged: String
  +before: String
  +after: String
}

class QuestionUpdaterController {
  +loadEditor(): void
  +validateAndSave(updated: Question[]): Boolean
}

class QuestionFileRepository <<persisted>> {
  -filePath: String
  +readAll(): Question[]
  +writeAtomically(updated: Question[]): void
  +validateSchema(updated: Question[]): Boolean
}

GameApp --> ScreenRouter
ScreenRouter --> IntroMoviePlayer
ScreenRouter --> MainMenu
ScreenRouter --> GameSession

GameSession *-- Score
GameSession *-- StoryProgress
GameSession --> QuestionBank
GameSession --> StoryEngine
GameSession --> FeedbackService
GameSession --> FractionValidator
GameSession --> VelocityCalculator
GameSession --> PhysicsEngine

QuestionBank "1" o-- "0..*" Question
Question "1" o-- "2..*" Choice

QuestionUpdaterController --> AdminAuthService
QuestionUpdaterController --> QuestionFileRepository
QuestionUpdaterController --> AuditLogger

note right of FeedbackService : FR-019 must fire feedback event within 500ms
note right of QuestionFileRepository : ASR-003 UTF-8 JSON + atomic write
note right of AdminAuthService : >=12 char passwords + lockout + audit
note right of Score : stored in browser memory only

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SpaceFractions
skinparam classAttributeIconSize 0

object app1 as "app1:GameApp [PlayGame]" {
}

object router1 as "router1:ScreenRouter [PlayGame]" {
  currentScreen = "INTRO"
}

object intro1 as "intro1:IntroMoviePlayer [WatchIntro]" {
  isPlaying = true
}

object session1 as "session1:GameSession [AnswerQuestions]" {
  sessionId = "sess-7f3a"
}

object score1 as "score1:Score [ViewFinalScore]" {
  points = 30
  penalizedQuestionIds = "{Q3}"
}

object progress1 as "progress1:StoryProgress [AdaptiveStory]" {
  currentQuestionId = "Q5"
  correctOnCritical = true
  attemptedIds = "{Q1,Q2,Q3,Q4,Q5}"
}

object bank1 as "bank1:QuestionBank [LoadQuestions]" {
  sourceUrl = "/content/questions.json"
}

object q5 as "q5:Question [AnswerQuestions]" {
  id = "Q5"
  prompt = "Which fraction equals 0.5?"
  answer = "1/2"
  hint = "Divide numerator by denominator."
  isCritical = true
}

object physics1 as "physics1:PhysicsEngine [AdjustVelocity]" {
  velocity = 12.5
}

app1 -- router1
router1 -- intro1
router1 -- session1
session1 -- score1
session1 -- progress1
session1 -- bank1
bank1 -- q5
session1 -- physics1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_GameSession
hide empty description

[*] --> Initialized : startGame

Initialized --> IntroPlaying : showIntro
IntroPlaying --> MainMenuShown : introEnded / showMainMenu
IntroPlaying --> MainMenuShown : skipClick / skip(); showMainMenu

MainMenuShown --> GameplayActive : startClick / start()
GameplayActive --> QuestionPresented : nextQuestion / renderQuestion

state GameplayActive {
  [*] --> QuestionPresented

  QuestionPresented --> AwaitingAnswer : renderChoices
  AwaitingAnswer --> FeedbackShown : answerClick / evaluate; emitFeedback
  FeedbackShown --> QuestionPresented : correct / addPoint; advance
  FeedbackShown --> AwaitingAnswer : incorrect / markNoPoint; allowRetry

  FeedbackShown --> Branching : criticalAnswered [isCritical] / branch
  Branching --> QuestionPresented : branchDone

  AwaitingAnswer --> VelocityAdjusting : velocityInput / validate
  VelocityAdjusting --> AwaitingAnswer : valid / applyVelocityRealTime
  VelocityAdjusting --> AwaitingAnswer : invalid / showValidation; focusInput
}

QuestionPresented --> EndingShown : noMoreQuestions / end()
GameplayActive --> EndingShown : endGame

EndingShown --> MainMenuShown : tryAgainClick / showMainMenu
EndingShown --> [*] : quitClick

note right of VelocityAdjusting
ASR-008: apply velocity adjustment immediately to physics engine.
FR-016/FR-018: integer inputs; denominator != 0; show red message + focus.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_PlayGameEndToEnd
start
:Load /game (HTML/CSS/JS assets);
note right
NFR-009/ASR-007: intro+menu available <=60s @56Kbps simulation.
end note

:Initialize GameApp;
:Show Intro Movie;
if (Mouse click?) then (yes)
  :Skip Intro;
endif
:Show Main Menu;
:User clicks Start Game;
:Create GameSession (score in memory);
repeat
  :Load next Question (from QuestionBank);
  :Render prompt + choices;
  if (User requests hint?) then (yes)
    :Show hint (robot sidekick);
  endif
  :User clicks an answer;
  :Evaluate answer;
  :Emit feedback DOM event;
  note right
FR-019: event type=feedback within 500ms of click.
end note
  if (Correct?) then (yes)
    :Add point (if not penalized);
  else (no)
    :Show incorrect; mark no-point; allow retry;
  endif

  if (Velocity fraction entered?) then (yes)
    :Validate integers & denom!=0 [ValidationCheck];
    if (Valid?) then (yes)
      :Compute decimal and apply to PhysicsEngine immediately;
    else (no)
      :Show red validation message; focus input;
    endif
  endif

  if (Critical question?) then (yes)
    :Branch storyline based on correctness;
  endif
repeat while (More questions?) is (yes)

:Compute final score + rank + message;
:Show Ending Scene;
if (Try again?) then (yes)
  :Return to Main Menu;
  stop
else (quit)
  stop
endif
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_S1_PlayIntroToMenu
autonumber
actor EndUser
participant GameApp
participant ScreenRouter
participant IntroMoviePlayer
participant MainMenu

EndUser -> GameApp : openGame
GameApp -> ScreenRouter : showIntro
ScreenRouter -> IntroMoviePlayer : play

alt skipClick
  EndUser -> IntroMoviePlayer : skip
  IntroMoviePlayer -> ScreenRouter : onEnded
  ScreenRouter -> MainMenu : renderMenu
else watchToEnd
  IntroMoviePlayer -> ScreenRouter : onEnded
  ScreenRouter -> MainMenu : renderMenu
end

note right of IntroMoviePlayer
FR-004: skip at any point via mouse click.
end note
@enduml
```

```plantuml
@startuml Sequence_S2_AdminUpdateQuestions
autonumber
actor Admin
participant QuestionUpdaterController
participant AdminAuthService
participant QuestionFileRepository
participant AuditLogger

Admin -> QuestionUpdaterController : openUpdater
QuestionUpdaterController -> AdminAuthService : login(adminId,password)
AdminAuthService --> QuestionUpdaterController : authResult(ok/deny)

alt ok
  QuestionUpdaterController -> QuestionFileRepository : readAll
  QuestionFileRepository --> QuestionUpdaterController : questionsJson
  Admin -> QuestionUpdaterController : submitEdits(updatedQuestions)
  QuestionUpdaterController -> QuestionFileRepository : validateSchema(updatedQuestions)
  QuestionFileRepository --> QuestionUpdaterController : valid/invalid

  alt valid
    QuestionUpdaterController -> QuestionFileRepository : writeAtomically(updatedQuestions)
    QuestionUpdaterController -> AuditLogger : append(editAuditEntry)
    QuestionUpdaterController --> Admin : saveSuccess
  else invalid
    QuestionUpdaterController -> AuditLogger : append(validationFailEntry)
    QuestionUpdaterController --> Admin : showValidationErrors
  end
else deny
  QuestionUpdaterController -> AuditLogger : append(loginFailEntry)
  QuestionUpdaterController --> Admin : showLoginError
end

note right of AdminAuthService
FR-021: >=12 chars, salted+hashed, lockout after 5 failures, reset after 1h/helpdesk.
end note
note right of AuditLogger
NFR-008: audit schema + retention >=2 years (server-side).
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_S1_PlayIntroToMenu
skinparam linetype ortho
actor EndUser
rectangle GameApp
rectangle ScreenRouter
rectangle IntroMoviePlayer
rectangle MainMenu

EndUser -- GameApp
GameApp -- ScreenRouter
ScreenRouter -- IntroMoviePlayer
ScreenRouter -- MainMenu

EndUser -> GameApp : 1.openGame
GameApp -> ScreenRouter : 2.showIntro
ScreenRouter -> IntroMoviePlayer : 3.play
EndUser -> IntroMoviePlayer : 4.skip (optional)
IntroMoviePlayer -> ScreenRouter : 5.onEnded
ScreenRouter -> MainMenu : 6.renderMenu

note right of MainMenu
Scenario S1: FR-003/FR-004 intro movie then transition to main menu.
end note
@enduml
```

```plantuml
@startuml Collaboration_S2_AdminUpdateQuestions
skinparam linetype ortho
actor Admin
rectangle QuestionUpdaterController
rectangle AdminAuthService
rectangle QuestionFileRepository
rectangle AuditLogger

Admin -- QuestionUpdaterController
QuestionUpdaterController -- AdminAuthService
QuestionUpdaterController -- QuestionFileRepository
QuestionUpdaterController -- AuditLogger

Admin -> QuestionUpdaterController : 1.openUpdater
QuestionUpdaterController -> AdminAuthService : 2.login
QuestionUpdaterController -> QuestionFileRepository : 3.readAll
Admin -> QuestionUpdaterController : 4.submitEdits
QuestionUpdaterController -> QuestionFileRepository : 5.validateSchema
QuestionUpdaterController -> QuestionFileRepository : 6.writeAtomically (if valid)
QuestionUpdaterController -> AuditLogger : 7.appendAudit

note right of QuestionFileRepository
Scenario S2: FR-020/FR-021/FR-022 + ASR-003 (JSON file, atomic write).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SpaceFractions
skinparam packageStyle rectangle

package "ui" as ui
package "app" as app
package "domain" as domain
package "content" as content
package "physics" as physics
package "admin" as admin
package "security" as security
package "persistence" as persistence

ui ..> app
app ..> domain
domain ..> content
domain ..> physics
admin ..> security
admin ..> persistence
content ..> persistence

note as N1
Screens, input handling, accessibility usability (NFR-004)
end note
N1 .. ui

note as N2
Application bootstrap and routing
end note
N2 .. app

note as N3
Game rules, scoring, story branching (FR-008 to FR-015)
end note
N3 .. domain

note as N4
Question loading and schema model (ASR-003)
end note
N4 .. content

note as N5
Real-time velocity adjustment loop (ASR-008)
end note
N5 .. physics

note as N6
Updater UI and server endpoints (FR-020 to FR-022)
end note
N6 .. admin

note as N7
Admin auth, lockout, HTTPS assumptions, audit (NFR-008, FR-021)
end note
N7 .. security

note as N8
Server-side JSON file and audit log retention at least 2 years (ASR-003, NFR-008)
end note
N8 .. persistence

note as N9
NFR-007 maintainability via clear separation of content from code
end note
N9 .. content

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SpaceFractions

component "GameWebUI" as GameWebUI <<UI>>
component "AdminWebUI" as AdminWebUI <<UI>>

component "GameController" as GameController
component "GameplayEngine" as GameplayEngine
component "FeedbackService" as FeedbackService
component "PhysicsEngine" as PhysicsEngine
component "QuestionLoader" as QuestionLoader

component "AdminController" as AdminController
component "AdminAuthService" as AdminAuthService
component "QuestionFileRepository" as QuestionFileRepository
component "AuditLogger" as AuditLogger

interface "IGameAPI" as IGameAPI
interface "IAdminAPI" as IAdminAPI
interface "IQuestionStore" as IQuestionStore
interface "IAudit" as IAudit
interface "IAuth" as IAuth

GameWebUI --> IGameAPI
GameController -- IGameAPI
GameController --> GameplayEngine
GameplayEngine --> QuestionLoader
GameplayEngine --> FeedbackService
GameplayEngine --> PhysicsEngine

AdminWebUI --> IAdminAPI
AdminController -- IAdminAPI
AdminController --> IAuth
AdminAuthService -- IAuth
AdminController --> IQuestionStore
QuestionFileRepository -- IQuestionStore
AdminController --> IAudit
AuditLogger -- IAudit

QuestionLoader --> IQuestionStore

note right of FeedbackService : FR-019 emit feedback event within 500ms
note right of QuestionFileRepository : ASR-003 schema validate JSON and atomic write
note right of AdminAuthService : FR-021 bcrypt or Argon2 lockout after 5 failures audit login

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SpaceFractions
skinparam componentStyle rectangle

node "Student Device\n(Browser: Chrome/Firefox/Safari/Edge)" as StudentDevice {
  artifact "GameWebUI (HTML/CSS/JS)" as GameWebUIArtifact
}

node "Admin Device\n(Browser)" as AdminDevice {
  artifact "AdminWebUI (HTML/CSS/JS)" as AdminWebUIArtifact
}

node "S2S Web Server (HTTPS)\n[99.9% uptime]" as WebServer {
  artifact "Static Content\n/game assets" as StaticContent
  artifact "Admin Backend\n(AdminController+Auth)" as AdminBackend
  artifact "Question JSON File\nquestions.json" as QuestionFile
  artifact "Audit Log Store\n(append-only)" as AuditStore
}

cloud "Internet" as Internet

StudentDevice -- Internet
AdminDevice -- Internet
Internet -- WebServer : HTTPS

note right of WebServer
NFR-001: 99.9% uptime measured by 60s probes.
NFR-008: HTTPS + audit retention >=2 years.
end note

note left of StudentDevice
NFR-002/NFR-005: standards-based HTML5; cross-browser consistency tests.
end note

note bottom of StaticContent
NFR-009/ASR-007: optimize assets for <=60s intro+menu @56Kbps simulation.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SpaceFractions
skinparam rectangleStyle rounded
skinparam componentStyle rectangle

rectangle "Student Browser" as StudentBrowser {
  component "GameWebUI\n[PlayGame]\nHTML5/CSS/JS" as GameWebUI
  component "In-Memory GameSession\n[LocalScore]" as LocalSession
}

rectangle "Admin Browser" as AdminBrowser {
  component "AdminWebUI\n[UpdateQuestions]\nHTML5/CSS/JS" as AdminWebUI
}

rectangle "S2S Hosting" as Hosting {
  component "Static Web Server\n[ServeAssets]\n(HTTP cache headers)" as StaticServer
  component "Admin Backend API\n[Auth+Update]\n(HTTPS)" as AdminAPI
  database "Question JSON File\n[questions.json]\nUTF-8" as QuestionStore
  database "Audit Log Store\n[>=2y retention]" as AuditStore
}

cloud "External Sites" as ExternalSites {
  component "DenominatorsWebsite" as DenomSite
  component "ExternalProjectSite" as UmbrellaSite
}

GameWebUI --> LocalSession : manageState
GameWebUI --> StaticServer : GET /game assets
AdminWebUI --> AdminAPI : HTTPS login/edit
AdminAPI --> QuestionStore : read/writeAtomically
AdminAPI --> AuditStore : appendAudit

GameWebUI --> DenomSite : openLink (new window)
GameWebUI --> UmbrellaSite : openLink (window.open + fallback)

note right of LocalSession
ASR-005/FR-014: score stored in browser memory only (no localStorage/disk).
end note

note right of AdminAPI
FR-021/NFR-008: strong password policy, lockout, audit schema.
end note

note bottom of StaticServer
NFR-009: intro+menu <=60s @56Kbps simulation.
end note
@enduml
```