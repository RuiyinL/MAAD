# Architecture Summary & Quality-Attribute Analysis

**Architecture Summary:**
The system is designed as a **Layered Web Architecture** with a clear separation between the Client-Side Game Engine and the Server-Side Content Management System. The client is a Single Page Application (SPA) using HTML5, CSS, and JavaScript, responsible for rendering, game logic, and local state management. The server acts as a static content host for the game assets and a secure API for administrative question updates. Data persistence is hybrid: game sessions are stored locally (browser memory/localStorage) per ASR-004, while question banks are stored as JSON files on the server per ASR-002.

**Quality Attributes & Trade-offs:**
1.  **Portability & Compatibility (NFR-001, ASR-001):**
    *   *Decision:* HTML5/JS stack replaces Flash.
    *   *Trade-off:* Loss of legacy Flash asset compatibility; requires modern browser APIs for audio/animation.
    *   *Risk:* Browser inconsistency mitigated by cross-browser testing suites.
2.  **Security (NFR-003, ASR-003):**
    *   *Decision:* HTTPS enforcement, salted hashing for admin auth, audit logging.
    *   *Trade-off:* Increased server complexity for admin module; client-side score validation is vulnerable to tampering (accepted risk for educational tool).
3.  **Maintainability (NFR-004, ASR-002):**
    *   *Decision:* Content (JSON) separated from Code (JS). Atomic file writes.
    *   *Trade-off:* File-based storage limits concurrent admin edits compared to a database; requires locking mechanisms.
4.  **Performance (NFR-002):**
    *   *Decision:* Asset optimization for low bandwidth (56Kbps simulation).
    *   *Trade-off:* Visual fidelity may be reduced to meet load time constraints.
5.  **Usability (NFR-005):**
    *   *Decision:* Mouse-only input, accessibility compliance (axe).
    *   *Trade-off:* Limits interaction complexity to ensure accessibility for low-literacy users.

# Architectural Style & Rationale

**Primary Style: Layered Architecture (Client-Server)**
*   **Justification:** Clearly separates user interaction (Client) from content persistence and security (Server). Aligns with ASR-001 (Web-Based) and ASR-003 (Security Boundary).
*   **Interaction:** Client requests questions/assets; Server serves static files or handles authenticated admin updates.

**Secondary Style: Model-View-Controller (MVC) [Client-Side]**
*   **Justification:** Organizes client code into Game State (Model), Rendering (View), and Input Handling (Controller). Supports NFR-005 (Usability) by isolating logic from UI.
*   **Interaction:** User input triggers Controller, updates Model, notifies View.

# Architecture Patterns & Tactics

1.  **Repository Pattern (Data Access):**
    *   *Application:* `QuestionRepository` abstracts JSON file access.
    *   *Rationale:* Supports ASR-002 (File-Based Content) and allows swapping storage mechanisms later without changing game logic.
2.  **State Pattern (Game Flow):**
    *   *Application:* `GameState` manages transitions (Intro -> Menu -> Play -> End).
    *   *Rationale:* Encapsulates complex transition logic defined in FR-001, FR-002, FR-006.
3.  **Command Pattern (User Input):**
    *   *Application:* Input actions (Skip, Select Answer) encapsulated as commands.
    *   *Rationale:* Supports undo/retry logic (FR-004) and decouples input from execution.
4.  **Security Tactics:**
    *   *Authentication:* Bcrypt/Argon2 hashing (NFR-003).
    *   *Transport:* HTTPS-only for admin endpoints (ASR-003).
    *   *Audit:* Immutable log files for admin actions (ASR-003).
5.  **Reliability Tactics:**
    *   *Atomic Writes:* Temp-file + Rename for question updates (ASR-002).
    *   *Local Persistence:* localStorage for session survival across refreshes (FR-005).

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCaseDiagram
left to right direction
skinparam packageStyle rectangle

actor "Student" as Student
actor "Administrator" as Admin

rectangle "Fraction Math Game System" {
  usecase "Play Intro Movie" as UC1
  usecase "Navigate Main Menu" as UC2
  usecase "Answer Fraction Question" as UC3
  usecase "View Help & Links" as UC4
  usecase "View Score & Ending" as UC5
  usecase "Update Questions" as UC6
  usecase "Authenticate Admin" as UC7
}

Student --> UC1
Student --> UC2
Student --> UC3
Student --> UC4
Student --> UC5

Admin --> UC7
Admin --> UC6

UC6 ..> UC7 : <<include>>
UC3 ..> UC5 : <<include>>

note right of UC6
  Requires Atomic File Write
  & Audit Logging (ASR-002/003)
end note

note left of UC1
  Skipable via Mouse Click
  (FR-001)
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml ClassDiagram
class GameSession {
  -sessionId: String
  -score: int
  -currentQuestionId: String
  -state: GameState
  +startSession()
  +updateScore(points: int)
  +endSession()
}

class Question {
  -id: String
  -prompt: String
  -choices: String[]
  -answerIndex: int
  -rationale: String
  +validateAnswer(input: int): boolean
  +getRationale(): String
}

class QuestionStore {
  -filePath: String
  +loadQuestions(): Question[]
  +saveQuestions(q: Question[]): void
  +validateSchema(q: Question): boolean
}

class AdminUser {
  -username: String
  -passwordHash: String
  -lastLogin: Date
  +authenticate(password: String): boolean
  +logAction(action: String): void
}

class SceneManager {
  -currentState: State
  +transitionTo(state: State): void
  +render(): void
}

class InputHandler {
  +handleClick(event: Event): void
  +handleKeyPress(key: char): void
}

GameSession "1" -- "1" SceneManager
GameSession "1" -- "0..*" Question
QuestionStore "1" -- "0..*" Question
AdminUser "1" -- "1" QuestionStore
SceneManager ..> InputHandler

note top of QuestionStore
  ASR-002: File-Based
  Atomic Writes
end note

note bottom of GameSession
  ASR-004: Client-Side
  LocalStorage Only
end note
@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml ObjectDiagram
object session1 : GameSession [PlayGame] {
  sessionId = "sess_123"
  score = 15
  currentState = Playing
}

object q1 : Question [MultipleChoice] {
  id = "q_001"
  prompt = "1/2 + 1/2 = ?"
  choices = ["1", "2", "1/4"]
  answerIndex = 0
}

object store : QuestionStore [ContentMgr] {
  filePath = "/data/questions.json"
}

object admin : AdminUser [AdminUpdate] {
  username = "superadmin"
  lastLogin = "2023-10-27"
}

session1 --> q1
store --> q1
admin --> store
@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml StateDiagram
[*] --> IntroPlaying

state IntroPlaying {
  [*] --> PlayingMovie
  PlayingMovie --> MenuReady : Movie End OR Skip Click
}

state MenuReady {
  [*] --> WaitingInput
  WaitingInput --> GamePlaying : Start Clicked
  WaitingInput --> HelpShown : Help Clicked
  WaitingInput --> ExternalLink : Link Clicked
}

state GamePlaying {
  [*] --> QuestionDisplayed
  QuestionDisplayed --> Validating : Answer Selected
  Validating --> FeedbackShown : Validation Complete
  FeedbackShown --> QuestionDisplayed : Next Question
  FeedbackShown --> SessionEnd : Last Question
}

state SessionEnd {
  [*] --> ResultsDisplayed
  ResultsDisplayed --> MenuReady : Retry Clicked
  ResultsDisplayed --> [*] : Quit Clicked
}

IntroPlaying --> MenuReady
MenuReady --> GamePlaying
GamePlaying --> SessionEnd
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml ActivityDiagram
start
:Load Assets;
note right: NFR-002 Performance
:Play Intro Movie;
if (Skip Clicked?) then (Yes)
  :Stop Movie;
else (No)
  :Wait Completion;
endif
:Display Main Menu;
:Wait User Input;
if (Start Game) then (Yes)
  :Load Question Set;
  :Display Question;
  :Wait Answer Input;
  :Validate Answer;
  if (Correct?) then (Yes)
    :Update Score;
    :Show Success Feedback;
  else (No)
    :Show Error Feedback;
    :Allow Retry;
  endif
  :Check Sequence Complete;
  if (Complete?) then (Yes)
    :Show Ending Scene;
    :Save Session Data;
    stop
  else (No)
    :Load Next Question;
    -[dotted]-> Display Question;
  endif
else (Help/Links)
  :Show Help/Redirect;
  -[dotted]-> Display Main Menu;
endif
@enduml
```

6. Sequence — Process View: Sequence Diagram 

```plantuml
@startuml SequenceDiagram
title Sequence: Student Play & Admin Update (Combined)

participant "Student" as Student
participant "GameUI" as UI
participant "GameEngine" as Engine
participant "LocalStorage" as Storage
participant "Admin" as Admin
participant "AuthSvc" as Auth
participant "QuestionSvc" as QSvc
participant "FileStore" as Files

group Scenario 1: Student Gameplay
  Student -> UI : Click Start
  UI -> Engine : startSession()
  Engine -> Storage : loadSession()
  Storage --> Engine : sessionData
  Engine -> UI : renderQuestion()
  Student -> UI : Select Answer
  UI -> Engine : submitAnswer(val)
  Engine -> Engine : validate()
  Engine -> UI : showFeedback()
  Engine -> Storage : saveScore()
end

group Scenario 2: Admin Update
  Admin -> Auth : login(creds)
  Auth -> Auth : hashVerify()
  Auth --> Admin : Token
  Admin -> QSvc : updateQuestion(json)
  QSvc -> QSvc : validateSchema()
  QSvc -> Files : atomicWrite(temp+rename)
  Files --> QSvc : Success
  QSvc -> Auth : logAudit()
end
@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml CollaborationDiagram
title Collaboration: Student Play & Admin Update

object "1: Student" as Student
object "2: GameUI" as UI
object "3: GameEngine" as Engine
object "4: Storage" as Storage
object "5: Admin" as Admin
object "6: QuestionSvc" as QSvc
object "7: Files" as Files

Student -[1: Click Start]-> UI
UI -[2: startSession]-> Engine
Engine -[3: loadSession]-> Storage
Engine -[4: render]-> UI
Student -[5: Submit]-> UI
UI -[6: validate]-> Engine
Engine -[7: saveScore]-> Storage

Admin -[8: Login]-> QSvc
Admin -[9: Update]-> QSvc
QSvc -[10: Write]-> Files
QSvc -[11: Log]-> Files

note right of Student
  Scenario 1: Gameplay
end note
note left of Admin
  Scenario 2: Maintenance
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml PackageDiagram
package "ClientApp" <<HTML5/JS>> {
  package "UI" <<View>>
  package "Logic" <<Controller>>
  package "State" <<Model>>
}

package "ServerApp" <<Node/Python>> {
  package "API" <<REST>>
  package "Security" <<Auth/Log>>
  package "Storage" <<FileIO>>
}

package "External" {
  package "Browser" <<LocalStorage>>
  package "S2S Links" <<HTTP>>
}

ClientApp.UI ..> ClientApp.Logic
ClientApp.Logic ..> ClientApp.State
ClientApp.State ..> External.Browser

ServerApp.API ..> ServerApp.Security
ServerApp.API ..> ServerApp.Storage
ServerApp.Storage ..> External.Browser

note top of ServerApp.Security
  NFR-003: Hardened Auth
  ASR-003: Security Boundary
end note
@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml ComponentDiagram
component "GameRenderer" as Render {
  interface "IRender" as I1
}

component "InputManager" as Input {
  interface "IInput" as I2
}

component "QuestionEngine" as QEng {
  interface "IQuestion" as I3
}

component "AuthComponent" as Auth {
  interface "IAuth" as I4
}

component "ContentManager" as Content {
  interface "IContent" as I5
}

Render ..> Input
Input ..> QEng
QEng ..> Content
Content ..> Auth

note right of Content
  ASR-002: Atomic Writes
  JSON Schema Validation
end note

note left of Auth
  ASR-003: HTTPS Only
  Audit Logging
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml DeploymentDiagram
node "Client Device" {
  component "Web Browser" {
    artifact "Game Client" <<HTML/JS>>
    artifact "Local Storage" <<Data>>
  }
}

node "Web Server" <<Cloud VM>> {
  component "Web Server" <<Nginx/Apache>> {
    artifact "Static Assets" <<JS/CSS>>
    artifact "Question JSON" <<Data>>
    artifact "Audit Logs" <<Log>>
  }
  component "Admin API" <<Service>>
}

"Web Browser" -[HTTPS]-> "Web Server"
"Admin API" -[TCP]-> "Question JSON"

note bottom of "Client Device"
  NFR-001: Cross-Browser
  ASR-004: Local State
end note

note right of "Web Server"
  NFR-006: 99.5% Uptime
  ASR-002: File Persistence
end note
@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml ContainerDiagram
title System Container Overview

Person "Student" as S
Person "Admin" as A

Container_Boundary "System" {
  Container "Web App" <<HTML5/JS>> {
    +Render Game
    +Handle Input
    +Local Storage
  }
  Container "Admin API" <<HTTPS/JSON>> {
    +Auth Admin
    +Validate Schema
    +Write Files
  }
  Container "File Store" <<JSON Files>> {
    +Questions
    +Audit Logs
  }
}

S --> "Web App" : Mouse/Click
A --> "Admin API" : HTTPS Request
"Admin API" --> "File Store" : Read/Write
"Web App" --> "File Store" : Read Questions (Static)

note right of "Web App"
  ASR-001: No Plugins
  NFR-005: Accessible
end note
@enduml
```