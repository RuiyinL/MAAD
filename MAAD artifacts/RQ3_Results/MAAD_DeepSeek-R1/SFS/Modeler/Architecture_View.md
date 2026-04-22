## Architecture Summary & Quality-Attribute Analysis
**Proposed Architecture:**  
A layered web application with HTML5 client (SPA), stateless backend services, and atomic file-based persistence. Client-side handles game flow/UI while server manages admin functions. Adheres to HTML5 standards (ASR-001) with strict accessibility (ASR-005) and security controls (ASR-007).

**Key Quality Attributes:**  
1. **Usability** (NFR-001/ASR-005):  
   - Risk: Overly complex UI hinders sixth-grade usability  
   - Tactic: Simplified navigation flows + WCAG 2.1 AA compliance  
2. **Security** (NFR-003/ASR-007):  
   - Trade-off: Strong auth (bcrypt-12/TLS 1.2+) increases latency  
   - Tactic: Isolated admin subsystem with audit logging  
3. **Performance** (NFR-002):  
   - Risk: Heavy media assets impact load times  
   - Tactic: CDN caching + connection-aware streaming  
4. **Availability** (NFR-004/NFR-005):  
   - Tension: Global availability vs cost constraints  
   - Tactic: Multi-region deployment + synthetic monitoring  
5. **Maintainability** (NFR-006):  
   - Risk: JSON schema evolution breaks validation  
   - Tactic: Contract-first question updates (ASR-004)  

**Architectural Style:**  
**Layered Architecture with Hexagonal Ports/Adapters**  
- Client Layer (HTML5 SPA): Implements presentation logic  
- Application Layer: Game flow controllers + validation services  
- Infrastructure Layer: File I/O adapters + security components  
*Justification:* Aligns with web deployment (ASR-002), enables testability (NFR-006), and isolates atomic file operations (ASR-004) via adapters. Supports stateless concurrency (NFR-007).

---

## Architectural Patterns & Tactics
**Patterns:**  
1. **Front Controller (Client):** Centralizes input handling for keyboard/mouse (FR-001/FR-002)  
2. **Strategy (Validation):** Interchangeable validators for fractions (FR-004) vs questions (FR-006)  
3. **Observer (UI):** Decouples storyline branching (FR-003c) from question logic  
4. **Repository (Server):** Abstracts atomic file operations (ASR-004)  

**Tactics:**  
- **Security:** TLS termination proxies (NFR-003) + bcrypt hashing adapters (ASR-007)  
- **Reliability:** Atomic file writes via temp/rename (ASR-004)  
- **Performance:** Browser-side caching of questions (NFR-002)  
- **Accessibility:** ARIA label generators (ASR-005)  

---

## PlantUML Diagrams

### ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase
left to right direction
actor EndUser as EU
actor Admin as AD
actor ExternalSystem as ES
usecase "PlayIntroMovie" as UC1
usecase "NavigateMainMenu" as UC2
usecase "AnswerQuestion" as UC3
usecase "ProvideHint" as UC4
usecase "BranchStoryline" as UC5
usecase "AdjustVelocity" as UC6
usecase "DisplayEndingScene" as UC7
usecase "UpdateQuestions" as UC8
usecase "AccessExternalResource" as UC9
EU --> UC1
EU --> UC2
EU --> UC3
UC3 <.. UC4 : <<extend>>
UC3 <.. UC5 : <<extend>>
EU --> UC6
EU --> UC7
AD --> UC8
EU --> UC9
note right of UC3 : Triggered on incorrect answer
note right of UC8 : Requires authentication
@enduml
```

### LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class
class GameState {
  -currentQuestion: Question
  -score: int
  +updateScore()
  +navigateTo()
}

class Question {
  -id: String
  -options: List<String>
  -correctAnswer: String
  -hint: String
  +validateAnswer()
}

class FractionInput {
  -numerator: int
  -denominator: int
  +convertToDecimal()
  +validate()
}

class AdminController {
  -authService: AuthService
  +updateQuestions()
}

class AuthService {
  +authenticate()
  +generateHash()
}

GameState "1" *-- "1..*" Question
FractionInput -- GameState : updates >
AdminController o-- AuthService
AdminController --> Question : manages >

note top of FractionInput: «immutable»\nNon-zero denominator constraint
note bottom of Question: JSON schema v1.0\n«persisted»
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object

object "gameSession1 : GameState" as gameSession1 {
  AnswerQuestion
  --
  currentQuestion = q1
  score = 150
}

object "q1 : Question" as q1 {
  id = "FRAC-101"
  options = "1/2, 3/4"
  correctAnswer = "1/2"
}

object "input1 : FractionInput" as input1 {
  numerator = 1
  denominator = 2
}

gameSession1 --> q1
input1 --> gameSession1 : updates

@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State
[*] --> IntroMovie
IntroMovie --> MainMenu : skip/timeout
MainMenu --> Gameplay : startSelected
Gameplay --> AnswerValidation : answerSubmitted
AnswerValidation --> HintDisplay : if incorrect
HintDisplay --> Gameplay
AnswerValidation --> StoryBranch : if critical
StoryBranch --> Gameplay
Gameplay --> EndingScene : lastQuestion
EndingScene --> [*] : quitSelected
EndingScene --> MainMenu : menuSelected
@enduml
```

### ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity

start
:Load Intro Movie;

if (Skip triggered?) then (yes)
else (no)
  :Play Full Movie;
endif

:Display Main Menu;

fork
  :Select Game Start;
fork again
  :Access Help Section;
end fork

:Present Question;

repeat
  :Receive Answer;
  :Validate Answer;

  if (incorrect?) then (yes)
    :Provide Hint;
    :Record Attempt;
  endif

repeat while (correct?) is (no)

if (critical?) then (yes)
  :Execute Story Branch;
endif

:Update Score;

if (last question?) then (yes)
  :Show Ending Scene;
endif

stop

@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml Sequence
actor EndUser
participant UI
participant GameEngine
participant ValidationService
EndUser -> UI : SubmitAnswer(1/2)
UI -> GameEngine : answerEvent
GameEngine -> ValidationService : validateFraction
ValidationService --> GameEngine : valid
GameEngine -> GameEngine : updateVelocity
GameEngine --> UI : showSuccess
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration
component UI
component GameEngine
component ValidationService
component FileStorage
UI - GameEngine : 1: answerEvent
GameEngine - ValidationService : 2: validate
ValidationService - FileStorage : 3: getSchema
FileStorage --> ValidationService : 4: schema
ValidationService --> GameEngine : 5: result
note bottom: Critical path for FR-004
@enduml
```

### DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package
package "Client" {
  [UI Components]
  [Game Logic]
}

package "Server" {
  [Admin Services]
  [Validation]
}

package "Shared" {
  [Data Contracts]
}

[UI Components] --> [Game Logic]
[Admin Services] --> [Validation]
[Game Logic] --> [Data Contracts]
[Validation] --> [Data Contracts]
note top of [Validation] : Atomic updates\n«ASR-004»
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component

component "HTML5 Game Client\n--\nHandles UI rendering\nand local state" as GameClient
component "Admin Service\n--\nQuestion updates\nwith auth" as AdminService
component "Validation Engine\n--\nSchema-based\nfraction checks" as ValidationEngine
component "File Storage" as FS

GameClient --> ValidationEngine : uses
AdminService --> ValidationEngine : requires
AdminService -- FS

note right of FS
  Atomic writes
  <<ASR-004>>
end note

@enduml
```

### PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment
node "Web Browser" as WB {
  component GameClient
}

node "Cloud Server" as CS {
  component AdminService
  component ValidationEngine
  database "QuestionStore"
}

WB - CS : HTTPS
AdminService - QuestionStore : Atomic writes
note on link : ASR-004 compliance
cloud "CDN" {
  component "MediaCache"
}
CS -- MediaCache : static assets
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container
container "Browser SPA" as SPA {
  component GameEngine
  component LocalStorage
}

container "Web Server" as WS {
  component AdminAPI
  component AuthService
}

container "File System" as FS {
  component QuestionRepository
}

database "AuditLog" as AL

SPA --> WS : REST/HTTPS
WS --> FS : File I/O
WS --> AL : Write logs
note on link : TLS 1.2+\n«NFR-003»
@enduml
```