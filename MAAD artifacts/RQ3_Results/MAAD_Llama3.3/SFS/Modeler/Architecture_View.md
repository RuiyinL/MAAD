## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor EndUser as "End User"
actor Admin as "Admin"
rectangle System {
  usecase "Play Game" as (PlayGame)
  usecase "View Score" as (ViewScore)
  usecase "Update Questions" as (UpdateQuestions)
  usecase "View Help" as (ViewHelp)
}
EndUser -- (PlayGame)
EndUser -- (ViewScore)
EndUser -- (ViewHelp)
Admin -- (UpdateQuestions)
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class Game {
  - id: string
  - score: int
  + play(): void
  + viewScore(): int
}
class Question {
  - id: string
  - prompt: string
  - options: List<string>
  + getPrompt(): string
  + getOptions(): List<string>
}
class User {
  - id: string
  - username: string
  + playGame(game: Game): void
  + viewScore(game: Game): int
}
class Admin {
  - id: string
  - username: string
  + updateQuestions(questions: List<Question>): void
}
Game --* Question
User --* Game
Admin --* Question
@enduml
```
3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
participant game1
participant question1
participant user1
participant admin1
game1 --> question1
user1 --> game1
admin1 --> question1
@enduml
```
4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
state Playing
state Paused
state GameOver
[*] --> Playing
Playing --> Paused : pause()
Paused --> Playing : resume()
Playing --> GameOver : gameOver()
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram
start
:play game;
if (game over?) then (yes)
  :game over;
else (no)
  :continue playing;
endif
:calculate score;
:display score;
stop
@enduml
```
6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDiagram1
participant User
participant Game
participant Question
User->>Game: play()
Game->>Question: getPrompt()
Question->>Game: return prompt
Game->>User: display prompt
User->>Game: submit answer
Game->>Question: check answer
Question->>Game: return result
Game->>User: display result
@enduml
```
```plantuml
@startuml SequenceDiagram2
participant Admin
participant Question
Admin->>Question: update()
Question->>Admin: return success
@enduml
```
7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationDiagram1
participant User
participant Game
participant Question
User->>Game: play()
Game->>Question: getPrompt()
Question->>Game: return prompt
Game->>User: display prompt
User->>Game: submit answer
Game->>Question: check answer
Question->>Game: return result
Game->>User: display result
note right of Game: Scenario: Play Game
@enduml
```
```plantuml
@startuml CollaborationDiagram2
participant Admin
participant Question
Admin->>Question: update()
Question->>Admin: return success
note right of Question: Scenario: Update Questions
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageDiagram
package Game {
  class Game
  class Question
}
package User {
  class User
}
package Admin {
  class Admin
}
Game -- User
Game -- Admin
@enduml
```
9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentDiagram
artifact GameComponent
artifact QuestionComponent
artifact UserComponent
artifact AdminComponent
GameComponent -- QuestionComponent
GameComponent -- UserComponent
GameComponent -- AdminComponent
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node GameServer
node QuestionServer
node UserClient
node AdminClient
GameServer -- QuestionServer
GameServer -- UserClient
GameServer -- AdminClient
@enduml
```
11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
artifact GameContainer
artifact QuestionContainer
artifact UserContainer
artifact AdminContainer
GameContainer -- QuestionContainer
GameContainer -- UserContainer
GameContainer -- AdminContainer
@enduml
```