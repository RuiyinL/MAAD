## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SpaceFractions
left to right direction

actor "EndUser" as EndUser
actor "Administrator" as Administrator
actor "EmailService" as EmailService

rectangle "Space Fractions" {
  usecase "Play Intro" as UC_PlayIntro
  usecase "Skip Intro" as UC_SkipIntro
  usecase "View Main Menu" as UC_MainMenu
  usecase "View Help" as UC_Help
  usecase "Start Game" as UC_StartGame
  usecase "Answer Question" as UC_AnswerQ
  usecase "Get Hint" as UC_Hint
  usecase "View Results" as UC_Results
  usecase "Replay Game" as UC_Replay
  usecase "Open External Link" as UC_External

  usecase "Admin Login" as UC_AdminLogin
  usecase "Reset Password" as UC_ResetPwd
  usecase "Edit Questions" as UC_EditQ
  usecase "Publish Question Bank" as UC_PublishQ
}

EndUser --> UC_PlayIntro
EndUser --> UC_MainMenu
EndUser --> UC_StartGame
EndUser --> UC_AnswerQ
EndUser --> UC_Hint
EndUser --> UC_Results
EndUser --> UC_Replay
EndUser --> UC_External
EndUser --> UC_Help

Administrator --> UC_AdminLogin
Administrator --> UC_ResetPwd
Administrator --> UC_EditQ
Administrator --> UC_PublishQ

EmailService <-- UC_ResetPwd

UC_SkipIntro ..> UC_PlayIntro : <<extend>>
UC_Help ..> UC_MainMenu : <<extend>>

UC_StartGame ..> UC_MainMenu : <<include>>
UC_AnswerQ ..> UC_StartGame : <<include>>
UC_Hint ..> UC_AnswerQ : <<extend>>
UC_Results ..> UC_AnswerQ : <<include>>
UC_Replay ..> UC_Results : <<extend>>

UC_EditQ ..> UC_AdminLogin : <<include>>
UC_PublishQ ..> UC_EditQ : <<include>>
UC_ResetPwd ..> UC_AdminLogin : <<extend>>

note bottom of UC_PlayIntro
assumption: Intro movie is optional but shown by default on first load; user may skip at any time.
end note

note bottom of UC_External
assumption: External links open in a new tab/window with rel="noopener noreferrer".
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
  +routeTo(viewId: String): void
}

class Router {
  -currentRoute: String
  +go(route: String): void
}

class IntroPlayer <<cacheable>> {
  -introUrl: String
  +playIntro(): void
  +skipIntro(): void
  +onEnded(): void
}

class MainMenu {
  +show(): void
  +startGame(): void
  +openHelp(): void
  +openExternalLink(url: String): void
}

class GameSession <<session>> {
  -sessionId: String
  -score: int
  -questionIndex: int
  -noPointsOnRetry: boolean
  -branchKey: String
  +startNewGame(): void
  +awardPoint(): void
  +disablePointsForCurrentQuestion(): void
  +finalizeScore(): int
  +reset(): void
}

class QuestionBank <<cacheable>> {
  -schemaVersion: String
  -etag: String
  -lastSyncUtc: String
  -questions: List<Question>
  +loadIfStale(ttlSeconds: int): void
  +getQuestionByIndex(i: int): Question
  +getTotalQuestions(): int
}

class Question <<immutable>> {
  +id: String
  +prompt: String
  +choices: List<String>
  +answerIndex: int
  +skill: SkillType
  +metadata: Map<String,String>
  +isCritical: boolean
  +branchOnCorrect: String
  +branchOnWrong: String
  +validate(): boolean
}

enum SkillType {
  arithmetic
  equivalence
  graph
  improper
}

class AnswerAttempt {
  +questionId: String
  +selectedIndex: int
  +isCorrect: boolean
  +attemptNo: int
}

class FractionValidator {
  +validateIntegers(numerator: int, denominator: int): boolean
  +validateDenominatorNonZero(denominator: int): boolean
}

class StoryEngine {
  +applyBranching(session: GameSession, q: Question, attempt: AnswerAttempt): void
  +getEndingScene(branchKey: String): String
}

class HintBot {
  +getHint(q: Question): String
  +showUsabilityTip(context: String): String
}

class FeedbackEngine {
  +playSuccess(): void
  +playFailure(): void
  +announceAriaLive(message: String): void
}

class PhysicsEngine {
  -velocity: float
  +setVelocity(v: float): void
  +getVelocity(): float
}

class VelocityAdjuster {
  +adjustVelocity(current: float, numerator: int, denominator: int): float
}

class ResultsView {
  +render(score: int, rank: String, message: String): void
  +replay(): void
  +quit(): void
}

class QuestionBankClient <<gateway>> {
  -baseUrl: String
  +fetchManifest(): String
  +fetchQuestions(etag: String): QuestionBank
}

class AdminAuthService <<security>> {
  +login(username: String, password: String): AdminSession
  +logout(sessionId: String): void
  +requestPasswordReset(email: String): void
  +resetPassword(token: String, newPassword: String): void
}

class AdminSession <<security>> {
  +adminId: String
  +sessionId: String
  +expiresAtUtc: String
  +isLockedOut: boolean
}

class QuestionBankUpdater {
  +validateAndPublish(bank: QuestionBank): void
  +rollbackToLastGood(): void
}

class AuditLog <<persisted>> {
  +append(eventType: String, adminId: String, ip: String, details: String): void
}

GameApp o-- Router
GameApp o-- IntroPlayer
GameApp o-- MainMenu
GameApp o-- GameSession
GameApp o-- QuestionBank
GameApp o-- StoryEngine
GameApp o-- HintBot
GameApp o-- FeedbackEngine
GameApp o-- ResultsView
QuestionBank "1" *-- "1..*" Question
Question "0..*" o-- AnswerAttempt
Question --> SkillType

StoryEngine --> GameSession
StoryEngine --> Question
StoryEngine --> AnswerAttempt

VelocityAdjuster --> FractionValidator
VelocityAdjuster --> PhysicsEngine

QuestionBank --> QuestionBankClient

QuestionBankUpdater --> QuestionBank
QuestionBankUpdater --> AuditLog
AdminAuthService --> AuditLog
AdminAuthService --> AdminSession

note right of IntroPlayer
NFR-001/ASR-002: HTML5 video/audio only (MP4/WebM/OGG), no plugins.
end note

note right of QuestionBank
ASR-005: ETag/TTL reload (<=60s) and schemaVersion; rollback on invalid update.
end note

note right of AdminAuthService
NFR-007/ASR-007: HTTPS-only, bcrypt hashing, lockout after 5 fails (10m),
session timeout 15m inactivity, audit trail (timestamp/IP).
end note

note right of VelocityAdjuster
FR-013/NFR-002: 95th percentile <=150ms on 2015+ Chromebook for input->velocity update.
end note

note right of FeedbackEngine
FR-011: Provide ARIA-live alternatives; pass WAVE audit >=98% on main screens.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SpaceFractions
artifact app1 as "app1:GameApp [StartGame]"
artifact menu1 as "menu1:MainMenu [ViewMainMenu]"
artifact session1 as "session1:GameSession [StartGame]\nsessionId='S-9f3'\nscore=0\nquestionIndex=0\nnoPointsOnRetry=false\nbranchKey='A'"
artifact bank1 as "bank1:QuestionBank [AnswerQuestion]\nschemaVersion='1.0'\netag='W/\"a1b2\"'\nlastSyncUtc='2026-04-22T12:00:00Z'"
artifact q1 as "q1:Question [PresentQuestion]\nid='Q-001'\nprompt='1/2 + 1/4 = ?'\nchoices=['1/6','3/4','1/8','2/6']\nanswerIndex=1\nskill=arithmetic\nisCritical=true\nbranchOnCorrect='B'\nbranchOnWrong='C'"
artifact attempt1 as "attempt1:AnswerAttempt [AnswerQuestion]\nquestionId='Q-001'\nselectedIndex=2\nisCorrect=false\nattemptNo=1"
artifact hint1 as "hint1:HintBot [GetHint]"
artifact fb1 as "fb1:FeedbackEngine [Feedback]"
artifact phys1 as "phys1:PhysicsEngine [AdjustVelocity]\nvelocity=12.5"
artifact va1 as "va1:VelocityAdjuster [AdjustVelocity]"
artifact val1 as "val1:FractionValidator [Validate]"

app1 -- menu1
app1 -- session1
app1 -- bank1
bank1 *-- q1
q1 o-- attempt1
app1 -- hint1
app1 -- fb1
va1 -- val1
va1 -- phys1

note right of bank1
[ASR-005] bank reloadIfStale(TTL=60s) driven by ETag.
end note

note right of session1
[ASR-006] score stored in-memory only; cleared on tab close.
end note
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_GameSession
hide empty description

[*] --> Idle

Idle --> IntroPlaying : appStart / playIntro()
IntroPlaying --> MainMenu : introEnded / routeTo(MainMenu)
IntroPlaying --> MainMenu : skipClick / skipIntro(); routeTo(MainMenu)

MainMenu --> LoadingQuestions : startGameClick / startNewGame()
LoadingQuestions --> PresentingQuestion : questionsLoaded [bankValid] / questionIndex=0
LoadingQuestions --> MainMenu : loadFailed / showError()

PresentingQuestion --> EvaluatingAnswer : choiceSelected / captureAnswer()
EvaluatingAnswer --> FeedbackCorrect : [isCorrect] / awardPoint()
EvaluatingAnswer --> FeedbackWrong : [!isCorrect] / disablePointsForCurrentQuestion()

FeedbackWrong --> PresentingQuestion : retryClick / (no points for this question)
FeedbackCorrect --> Branching : applyProgression / questionIndex++

Branching --> PresentingQuestion : [!isCritical] / nextQuestion()
Branching --> PresentingQuestion : [isCritical] / applyBranching()
Branching --> Results : [lastQuestion] / finalizeScore()

Results --> MainMenu : replayClick / reset()
Results --> Quit : quitClick

Quit --> [*]

note right of LoadingQuestions
ASR-005: client reloadIfStale(TTL<=60s); invalid content rejected server-side with rollback.
end note

note right of EvaluatingAnswer
FR-012: validate fraction inputs (integers, denom!=0) before applying calculations.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_GameplayFlow
start
:Load Web App Shell;
note right
ASR-001/ASR-002: Web-based, HTML5/JS/CSS/SVG/Canvas only; no plugins.
NFR-009/ASR-008: First-interactive <3s; bundle <=2.5MB (compressed).
end note

:Play Intro Movie;
if (User clicks Skip?) then (yes)
  :Skip Intro;
endif
:Show Main Menu;

if (User selects Help?) then (yes)
  :Show Help Screen;
  :Return to Main Menu;
endif

if (User clicks Start Game?) then (yes)
  :Init GameSession (score=0);
  :Load QuestionBank (ETag/TTL);
  note right
  ASR-005: reloadIfStale(TTL<=60s), use ETag; show lastSync/version.
  end note

  while (More questions?) is (yes)
    :Present Question;
    :Optional Hint (HintBot);
    :Capture Answer Selection;
    :Validate Input [ValidationCheck];
    if (Answer correct?) then (yes)
      :Play Success Feedback (sound/animation + ARIA-live);
      :Award Point;
    else (no)
      :Play Failure Feedback (sound/animation + ARIA-live);
      :Disable points for this question;
      :Retry same question;
    endif

    :Apply Branching (critical questions);
  endwhile (no)

  :Compute Final Score and Rank;
  :Render Ending Scene (branch outcome);
  if (Replay?) then (yes)
    :Reset session and go to Main Menu;
  else (no)
    stop
  endif
else (no)
  :Stay on Main Menu;
  stop
endif
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence1_Gameplay_AnswerQuestion
title Sequence 1: Answer Question (Gameplay)

actor EndUser as EndUser
participant "GameApp" as GameApp
participant "Router" as Router
participant "QuestionBankClient" as QuestionBankClient
participant "QuestionBank" as QuestionBank
participant "GameSession" as GameSession
participant "FeedbackEngine" as FeedbackEngine
participant "StoryEngine" as StoryEngine

EndUser -> GameApp : startGameClick
GameApp -> GameSession : startNewGame
GameApp -> QuestionBank : loadIfStale(TTL=60)
QuestionBank -> QuestionBankClient : fetchManifest
QuestionBankClient --> QuestionBank : manifest(etag,lastModified)
QuestionBank -> QuestionBankClient : fetchQuestions(if-none-match etag)
QuestionBankClient --> QuestionBank : questionsJson(schemaVersion,questions)

GameApp -> Router : go(Gameplay)

GameApp -> QuestionBank : getQuestionByIndex(0)
QuestionBank --> GameApp : Question

GameApp --> EndUser : renderQuestion

EndUser -> GameApp : choiceSelected(selectedIndex)
GameApp -> GameSession : recordAttempt
GameApp -> StoryEngine : applyBranching(session,q,attempt)
StoryEngine --> GameApp : branchUpdate(optional)

alt isCorrect
  GameApp -> FeedbackEngine : playSuccess
  FeedbackEngine --> GameApp : feedbackDone
  GameApp -> GameSession : awardPoint
  GameApp --> EndUser : showNextQuestion
else isWrong
  GameApp -> FeedbackEngine : playFailure
  GameApp -> GameSession : disablePointsForCurrentQuestion
  GameApp --> EndUser : allowRetry
end

note over QuestionBankClient,QuestionBank
ASR-005: ETag + Cache-Control TTL reload (<=60s). Client must tolerate network failure and keep last-known-good bank.
end note

note over FeedbackEngine
FR-011: provide ARIA-live announcements; no Flash.
end note
@enduml
```

```plantuml
@startuml Sequence2_Admin_UpdateQuestions
title Sequence 2: Admin Update Questions (Validate + Publish + Rollback)

actor Administrator as Administrator
participant "AdminAuthService" as AdminAuthService
participant "QuestionBankUpdater" as QuestionBankUpdater
participant "AuditLog" as AuditLog
participant "QuestionFileStore" as QuestionFileStore
participant "EmailService" as EmailService

Administrator -> AdminAuthService : login(username,password)
AdminAuthService -> AuditLog : append(LoginAttempt,adminId,ip)
alt loginSuccess
  AdminAuthService --> Administrator : adminSession(sessionId)
else loginFailed
  AdminAuthService --> Administrator : error(lockoutMaybe)
  return
end

Administrator -> QuestionBankUpdater : validateAndPublish(questionBankDraft)
QuestionBankUpdater -> AuditLog : append(EditAttempt,adminId,ip)

QuestionBankUpdater -> QuestionBankUpdater : validateSchemaVersion
QuestionBankUpdater -> QuestionBankUpdater : validateQuestions
alt valid
  QuestionBankUpdater -> QuestionFileStore : writeAtomically(questions.json)
  QuestionFileStore --> QuestionBankUpdater : writeOk(newEtag)
  QuestionBankUpdater -> AuditLog : append(PublishSuccess,adminId,ip)
  QuestionBankUpdater --> Administrator : publishOk(newEtag)
else invalid
  QuestionBankUpdater -> QuestionFileStore : rollbackToLastGood()
  QuestionFileStore --> QuestionBankUpdater : rollbackOk
  QuestionBankUpdater -> AuditLog : append(PublishRejected,adminId,ip)
  QuestionBankUpdater -> EmailService : notifyAdmin(rejectedDetails)
  EmailService --> QuestionBankUpdater : accepted
  QuestionBankUpdater --> Administrator : publishRejected(errors)
end

note over AdminAuthService
NFR-007/ASR-007: HTTPS-only; bcrypt; lockout after 5 failures (10m); session timeout 15m inactivity.
end note

note over QuestionFileStore
FR-018/ASR-004/ASR-005: server-hosted JSON file persistence; atomic write + rollback to last-known-good.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration1_Gameplay_AnswerQuestion
title Collaboration 1: Answer Question (Gameplay)

object EndUser
object GameApp
object Router
object QuestionBank
object QuestionBankClient
object GameSession
object FeedbackEngine
object StoryEngine

EndUser -- GameApp
GameApp -- Router
GameApp -- QuestionBank
QuestionBank -- QuestionBankClient
GameApp -- GameSession
GameApp -- FeedbackEngine
GameApp -- StoryEngine

EndUser -> GameApp : 1 startGameClick
GameApp -> GameSession : 2 startNewGame
GameApp -> QuestionBank : 3 loadIfStale(TTL=60)
QuestionBank -> QuestionBankClient : 4 fetchQuestions(ETag)
GameApp -> Router : 5 go(Gameplay)
EndUser -> GameApp : 6 choiceSelected
GameApp -> StoryEngine : 7 applyBranching
GameApp -> FeedbackEngine : 8 playSuccess/playFailure
GameApp -> GameSession : 9 awardPoint/disablePoints

note bottom
Origin: FR-003/FR-004/FR-006/FR-009/FR-011 and ASR-005 (dynamic question reload).
end note
@enduml
```

```plantuml
@startuml Collaboration2_Admin_UpdateQuestions
title Collaboration 2: Admin Update Questions (Validate + Publish)

object Administrator
object AdminAuthService
object QuestionBankUpdater
object QuestionFileStore
object AuditLog
object EmailService

Administrator -- AdminAuthService
Administrator -- QuestionBankUpdater
AdminAuthService -- AuditLog
QuestionBankUpdater -- AuditLog
QuestionBankUpdater -- QuestionFileStore
QuestionBankUpdater -- EmailService

Administrator -> AdminAuthService : 1 login
AdminAuthService -> AuditLog : 2 append(LoginAttempt)
Administrator -> QuestionBankUpdater : 3 validateAndPublish
QuestionBankUpdater -> AuditLog : 4 append(EditAttempt)
QuestionBankUpdater -> QuestionFileStore : 5 writeAtomically / rollbackToLastGood
QuestionBankUpdater -> AuditLog : 6 append(PublishSuccess/Rejected)
QuestionBankUpdater -> EmailService : 7 notifyAdmin(onReject)

note bottom
Origin: FR-016/FR-017/FR-018, NFR-007, ASR-004/ASR-005/ASR-007.
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SpaceFractions
skinparam packageStyle rectangle

package "ui" as ui {
  class GameApp
  class Router
  class IntroPlayer
  class MainMenu
  class ResultsView
}

package "domain" as domain {
  class GameSession
  class Question
  enum SkillType
  class AnswerAttempt
}

package "gameplay" as gameplay {
  class StoryEngine
  class HintBot
  class FeedbackEngine
  class PhysicsEngine
  class VelocityAdjuster
  class FractionValidator
}

package "content" as content {
  class QuestionBank
  class QuestionBankClient
}

package "admin" as admin {
  class AdminAuthService
  class AdminSession
  class QuestionBankUpdater
}

package "infrastructure" as infra {
  class QuestionFileStore
  class AuditLog
  class EmailServiceAdapter
}

ui ..> domain
ui ..> gameplay
ui ..> content

gameplay ..> domain
content ..> domain

admin ..> content
admin ..> infra

content ..> infra : uses HTTP

note right of ui
ASR-002/NFR-001: HTML5-only UI (no plugins). NFR-006: usability target (reach Q1 <2m).
end note

note right of admin
NFR-007/ASR-007: HTTPS, bcrypt, lockout, timeout, audit.
end note

note right of content
ASR-005: ETag/TTL refresh (<=60s), schemaVersion, last-known-good.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SpaceFractions
skinparam componentStyle rectangle

component "WebGameUI\n[Gameplay+Menu]" as WebGameUI
component "GameCore\n[State+Rules]" as GameCore
component "ContentClient\n[ETag+TTL]" as ContentClient
component "MediaEngine\n[HTML5 Audio/Video]" as MediaEngine
component "AdminWebUI\n[Question Editor]" as AdminWebUI

component "AdminAPI\n[Auth+Update]" as AdminAPI
component "QuestionFileStore\n[questions.json]" as QuestionFileStore
component "AuditLogStore\n[append-only]" as AuditLogStore
component "EmailAdapter\n[Reset/Alerts]" as EmailAdapter

interface "IGameplay" as IGameplay
interface "IContent" as IContent
interface "IAdminAuth" as IAdminAuth
interface "IQuestionUpdate" as IQuestionUpdate

WebGameUI ..> IGameplay
GameCore - IGameplay

WebGameUI ..> IContent
ContentClient - IContent

WebGameUI ..> MediaEngine
GameCore ..> MediaEngine : uses

AdminWebUI ..> IAdminAuth
AdminAPI - IAdminAuth

AdminWebUI ..> IQuestionUpdate
AdminAPI - IQuestionUpdate

AdminAPI ..> QuestionFileStore : read/write
AdminAPI ..> AuditLogStore : append
AdminAPI ..> EmailAdapter : notify

ContentClient ..> QuestionFileStore : HTTP GET

note right of ContentClient
ASR-005: cache-control + ETag; TTL reload <=60s.
end note

note right of AdminAPI
NFR-007/ASR-007: HTTPS-only, bcrypt, lockout (5 fails/10m), session timeout (15m), audit.
end note

note bottom of MediaEngine
NFR-001/ASR-002: MP4/WebM/OGG + MP3/WAV; Canvas/SVG; no plugins.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SpaceFractions
skinparam componentStyle rectangle

node "User Device\n(PC/Chromebook/iPad)\n[Chrome/Firefox/Edge/Safari]" as Client {
  artifact "Browser" as Browser
  artifact "SpaceFractions WebGameUI\n(static JS/CSS/assets)" as UIArtifact
}

cloud "Internet" as Net

node "Web Host (HTTPS)\n[99.5% uptime target]" as WebHost {
  artifact "Static Assets\n(CDN origin)" as StaticAssets
  artifact "AdminAPI" as AdminAPIArtifact
  artifact "QuestionFileStore\nquestions.json + last-good" as QuestionFileStoreArtifact
  artifact "AuditLogStore" as AuditLogArtifact
}

node "Email Provider" as EmailNode {
  artifact "EmailService" as EmailArtifact
}

Browser --> UIArtifact
Client --> Net
Net --> WebHost : HTTPS

UIArtifact --> StaticAssets : GET bundles/assets
UIArtifact --> QuestionFileStoreArtifact : GET questions.json (ETag)

AdminAPIArtifact --> QuestionFileStoreArtifact : atomic write/rollback
AdminAPIArtifact --> AuditLogArtifact : append
AdminAPIArtifact --> EmailArtifact : SMTP/API

note right of Client
NFR-009/ASR-008: First-interactive <3s on 10Mbps, 2015+ HW.
NFR-005/ASR-003: behavior invariant; Selenium regression in browser matrix.
end note

note right of WebHost
ASR-004/ASR-005: server-hosted JSON persistence; dynamic incorporation without restart.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SpaceFractions
skinparam rectangleStyle rounded
left to right direction

actor "EndUser" as EndUser
actor "Administrator" as Administrator

rectangle "Client (Browser)" as Client {
  rectangle "WebGameUI\n[Intro/Menu/Gameplay/Results]\nTech: HTML5 + JS framework" as WebGameUI
  rectangle "GameCore\n[Session Score + Rules]\nState: in-memory per tab" as GameCore
}

rectangle "Server (Web Host)" as Server {
  rectangle "StaticContent\n[JS/CSS/media]\nServes: gzip/brotli" as StaticContent
  rectangle "QuestionFileStore\n[questions.json]\nETag + Cache-Control" as QuestionFileStore
  rectangle "AdminAPI\n[Auth + Question Update]\nHTTPS-only" as AdminAPI
  rectangle "AuditLogStore\n[Append-only]\nRetention policy" as AuditLogStore
}

rectangle "External" as External {
  rectangle "EmailService\n[Reset/Alerts]" as EmailService
  rectangle "ExternalLinks\n[Math Umbrella/Denominators]" as ExternalLinks
}

EndUser --> WebGameUI : click/touch/keyboard
WebGameUI --> GameCore : gameplay events
WebGameUI --> StaticContent : GET assets
WebGameUI --> QuestionFileStore : GET questions.json (ETag)

Administrator --> AdminAPI : login/update
AdminAPI --> QuestionFileStore : validate + atomic write/rollback
AdminAPI --> AuditLogStore : append audit
AdminAPI --> EmailService : password reset/alerts

WebGameUI --> ExternalLinks : open in new tab

note right of GameCore
ASR-006/NFR-008: single-user per running instance; score not persisted.
end note

note right of QuestionFileStore
ASR-005: schemaVersion + last-known-good rollback; client TTL reload <=60s.
end note

note right of AdminAPI
NFR-007/ASR-007: bcrypt, lockout 5 fails/10m, session timeout 15m, audit (timestamp/IP), HTTPS.
end note

note bottom of WebGameUI
FR-010/FR-011/NFR-006: accessible controls (mouse/keyboard/touch), ARIA roles/states, ARIA-live feedback; WAVE >=98%.
end note
@enduml
```