# Functional Requirements Results

[FR-001]: Launch via Web-Based Menu (“Math Umbrella”)
**Description**: “The umbrella will be a web-based menu system allowing the user to choose between the systems… providing links to projects relating to fractions, decimals, and percents… accessible over the World Wide Web.”
  
**Rationale:** Describes user-facing navigation behavior (selecting among systems/projects).

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** Not specified
---

[FR-002]: Play Introductory Movie with Optional Skip
**Description**: “The Space Fractions system will have an introductory movie… The primary input… is… a mouse click… option to skip the introductory movie… If a click is detected, the movie is immediately terminated… If no click is registered, the movie plays in its entirety… then… proceeds to the main menu.”
  
**Rationale:** Specifies system behavior for intro playback, skip detection, and transition.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-004
- **Conflicts with:** Not specified
---

[FR-003]: Provide Main Menu with Help and Links
**Description**: “The Space Fractions system will have a main menu, including a brief help section… At the main title screen, the user will be able to view a general help screen… Also, a short summary… and a link… To start… click… Another button… connects… to the Denominators’ web page.”
  
**Rationale:** Defines UI functions available from the main menu (help, start, external link).

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004, NFR-001
- **Conflicts with:** Not specified
---

[FR-004]: Present Fraction Question Sequence as Multiple Choice Storyline
**Description**: “The Space Fractions system will have a series of fraction questions… that sequentially form a storyline… presented as a multiple-choice questionnaire… The user will be given a problem and then must click the correct solution.”
  
**Rationale:** Core gameplay function: present questions and collect answers.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-004
- **Conflicts with:** Not specified
---

[FR-005]: Provide Per-Question Feedback and Retry Handling
**Description**: “If the player selects the correct answer, a confirmation message is displayed… For incorrect answers, the player is informed… and given another opportunity… without the possibility of earning points for that question… Output will be sounds and animations… to acknowledge success or failure.”
  
**Rationale:** Specifies functional outcomes after each answer (feedback + scoring consequence).

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-007, NFR-004
- **Conflicts with:** Not specified
---

[FR-006]: Provide Hints via Robotic Sidekick
**Description**: “A friendly robotic sidekick will assist with general usability issues and give hints towards the correct response.”
  
**Rationale:** Describes an assistance function available during gameplay.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** Not specified
---

[FR-007]: Calculate, Store, and Display User Score at End (with Ranking/Message)
**Description**: “At the end… students will be given feedback based on their system scores… ending scene where the user’s score is calculated and ranked… In addition, the player’s exact score will be given with a customized message… The user’s score must be kept as local data… so that the results may be given at the end.”
  
**Rationale:** Defines scoring lifecycle: maintain score during play and present results at end.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005, FR-009
- **Conflicts with:** NFR-011 (if later added requirement to persist scores server-side)
---

[FR-008]: Support Story Branching at Critical Points
**Description**: “The systemplay will be dynamic and adaptive to provide different storylines based on the user’s progress… includes ‘critical points’ where the storyline can diverge… The last scene will be determined by the user’s response on certain critical questions.”
  
**Rationale:** Specifies functional branching logic affecting storyline and ending.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-009
- **Conflicts with:** Not specified
---

[FR-009]: Provide Ending Scene with Exit or Replay/Main Menu Option
**Description**: “The Space Fractions system will have an ending scene… with an option to quit… or try again… Player interaction… through mouse clicks… choose between exiting… or returning to the main menu.”
  
**Rationale:** Defines end-of-game flow and navigation options.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007
- **Conflicts with:** Not specified
---

[FR-010]: Validate Fraction Inputs and Denominator Non-Zero
**Description**: “Inputs… in the form of two integers representing the numerator and denominator… validate… ensure they are integers and that the denominator is not zero… error handling… displaying an error message… requesting a new input.”
  
**Rationale:** Input validation and error handling are explicit system behaviors.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** Not specified
---

[FR-011]: Convert Fraction to Decimal and Apply to Spaceship Velocity in Real Time
**Description**: “If the input is valid… calculates the velocity adjustment by converting the fraction into a decimal value and applying it to the spaceship’s current velocity… applied to the game’s physics engine to update the spaceship’s speed in real-time… output timing is immediate.”
  
**Rationale:** Defines a concrete input-process-output transformation tied to gameplay.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006
- **Conflicts with:** Not specified
---

[FR-012]: Provide Web-Accessible Question Updater for Administrators
**Description**: “A component accessible over the World Wide Web will allow the series of fraction questions to be updated by an administrator… She navigates to the updater page, which asks for a password… uses an intuitive web forms interface… pulldown menus and text fields… Each question is managed on a separate page… submission button… validation check… Once… passes… the update… finalized.”
  
**Rationale:** Specifies admin workflows and editing operations for question content.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-007, NFR-008, ASR-004
- **Conflicts with:** Not specified
---

[FR-013]: Persist Updated Questions to Server File for Game Use
**Description**: “This information must be saved in a file on the web server where the Space Fractions system is hosted and will be easily edited… This file contains the updated question data… structured in a format that the system sequence can dynamically read and incorporate into the gameplay… real-time updates… without… restarts.”
  
**Rationale:** Defines persistence behavior and runtime consumption of updated content.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, NFR-009, ASR-004
- **Conflicts with:** NFR-006 (if update approach harms load/performance)
---

[FR-014]: Open External Resources in Separate Window from Umbrella
**Description**: “The chosen S2S project is opened in a separate window… allowing… explore… without leaving… the Space Fractions system.”
  
**Rationale:** Defines how external content is launched/presented.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-004
- **Conflicts with:** Not specified
---

[FR-015]: Restrict One User per Single Running Instance
**Description**: “Only one person can use a single instance of the Space Fractions system. However… more than one user can access the product and download its content for use on their computer.”
  
**Rationale:** Specifies a behavioral usage rule for a runtime instance.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** Not specified
---