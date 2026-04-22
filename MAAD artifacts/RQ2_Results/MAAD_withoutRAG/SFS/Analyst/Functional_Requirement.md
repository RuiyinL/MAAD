# Functional Requirements Results

[FR-001]: Launch and play an introductory movie with skip option  
**Description**: “The Space Fractions system will have an introductory movie to set up the storyline.” / “The primary input for this component is the user's interaction in the form of a mouse click… option to skip the introductory movie… If a click is detected, the movie is immediately terminated, and the system transitions the user to the game's main menu… If no click is registered, the movie plays in its entirety, after which the Space Fractions system automatically proceeds to the main menu.”  

**Rationale:** Defines system behavior for starting/playing/skipping the intro and transitioning to the main menu.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-006
- **Conflicts with:** NFR-001
---

[FR-002]: Provide main menu with help and navigation options  
**Description**: “The Space Fractions system will have a main menu, including a brief help section.” / “At the main title screen, the user will be able to view a general help screen… Also, a short summary of our team and a link to our website will be provided.”  

**Rationale:** Specifies menu functions and available user actions.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-006
- **Conflicts with:** None specified
---

[FR-003]: Start gameplay from main menu  
**Description**: “To start the Space Fractions system, the user will click on the corresponding button.” / “One button initiates the game, leading players directly into the gameplay experience.”  

**Rationale:** Describes the user-triggered function that begins the game sequence.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-006
- **Conflicts with:** None specified
---

[FR-004]: Provide fraction-question gameplay sequence with multiple-choice interactions  
**Description**: (Derived from FR-004) “The Space Fractions system will have a series of fraction questions… presented as a multiple-choice questionnaire.” / “The user will be given a problem and then must click the correct solution.” / “If the player selects the correct answer… transitions to the next question… For incorrect answers, the player is informed… given another opportunity… without the possibility of earning points for that question.” Question schema: { id: string, prompt: string, choices: [string], answerIndex: int, skill: enum ('arithmetic'|'equivalence'|'graph'|'improper'), metadata: object }. See sample .json in QA repo. Owner: Content QA/Dev; Next action: Document and circulate question schema to development and content QA.  

**Rationale:** Defines the core functional flow of presenting questions, capturing answers, giving feedback, and sequencing.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-011, FR-012, NFR-006
- **Conflicts with:** None specified
---

[FR-004A]: Present a new fraction question  
**Description**: (Derived from FR-004) “The Space Fractions system will have a series of fraction questions… presented as a multiple-choice questionnaire.”  

**Rationale:** Atomic behavior: displaying a question to the user.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006
- **Conflicts with:** None specified
---

[FR-004B]: Capture the user's answer selection  
**Description**: (Derived from FR-004) “The user will be given a problem and then must click the correct solution.”  

**Rationale:** Atomic behavior: collecting user input for an answer choice.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-006
- **Conflicts with:** None specified
---

[FR-004C]: Provide success/failure feedback per answer  
**Description**: (Derived from FR-004) “If the player selects the correct answer, a confirmation message is displayed…” / “For incorrect answers, the player is informed of the mistake…”  

**Rationale:** Atomic behavior: feedback output based on correctness.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-011, NFR-006
- **Conflicts with:** None specified
---

[FR-004D]: Apply progression rules (next question / retry with no points)  
**Description**: (Derived from FR-004) “If the player selects the correct answer… transitions to the next question…” / “For incorrect answers… given another opportunity… without the possibility of earning points for that question.”  

**Rationale:** Atomic behavior: governs sequencing and scoring eligibility.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004A, FR-004B, FR-004C
- **Conflicts with:** None specified
---

[FR-005]: Support question types covering multiple fraction skills  
**Description**: “fraction questions (testing arithmetic, equivalence, graphical interpretation, and improper versus proper fraction skills).”  

**Rationale:** Specifies functional coverage of the question content the system must present.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** None specified
---

[FR-006]: Provide adaptive/dynamic storyline with critical branching points  
**Description**: (Derived from FR-006) “The systemplay will be dynamic and adaptive to provide different storylines based on the user's progress.” / “The system sequence includes ‘critical points’ where the storyline can diverge based on whether the player answers these pivotal questions correctly.” / “The last scene will be determined by the user's response on certain critical questions that impact the story's plot.” Critical story branches must be confirmed invariant (via Selenium) on latest Chrome/Firefox/Safari/Edge (Windows/macOS) for all n>10 seeded input scenarios. Owner: QA; Next action: Expand test pipeline coverage for divergent/adaptive branches and document cross-browser conformance.  

**Rationale:** Defines branching logic that changes narrative flow based on performance.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-012
- **Conflicts with:** NFR-005
---

[FR-007]: Provide robotic sidekick hints and usability assistance  
**Description**: “A friendly robotic sidekick will assist with general usability issues and give hints towards the correct response.”  

**Rationale:** Describes an in-game assistance function.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-006
- **Conflicts with:** None specified
---

[FR-008]: Calculate and display ending score with ranking/message and replay/quit options  
**Description**: “The Space Fractions system will have an ending scene where the user's score is calculated and ranked, with an option to quit the system or try again.” / “In addition, the player's exact score will be given with a customized message.” / “Player interaction… choose between exiting the system or returning to the main menu.”  

**Rationale:** Defines end-of-game computation and user options.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, FR-013, NFR-006
- **Conflicts with:** FR-014 (if “single instance” interpreted as disallowing replay within same browser context; unclear)
---

[FR-009]: Keep user score as local/session data until end of game  
**Description**: (Derived from FR-009) “The user's score must be kept as local data within the Space Fractions system so that the results may be given at the end of the Space Fractions system.” Score exists only in RAM while browser tab is open and is cleared on close; not persisted to localStorage. Owner: Developer/doc; Next action: State session policy in documentation and user help.  

**Rationale:** Specifies functional handling of score state within the client session to enable final results.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-008
- **Conflicts with:** None specified
---

[FR-010]: Accept user input via mouse clicks for answers and preferences  
**Description**: (Derived from FR-010) “Input will consist entirely of mouse clicks for the user to choose answer options and to set preferences.” All UI controls must be operable via mouse, keyboard (Tab/Enter/Space), and touch; interactive elements must have accessible roles and states (ARIA), and expose APIs for automated testing. Owner: Developer; Next action: Revise FR-010 input definition and specify test hooks in the automation plan.  

**Rationale:** Defines the input method the system must support for gameplay/menu interactions.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-004, FR-008
- **Conflicts with:** None specified
---

[FR-011]: Provide feedback via sounds and animations for success/failure  
**Description**: (Derived from FR-011) “Output will be sounds and animations… to acknowledge success or failure in answering the fraction questions.” / “The output of this functional requirement is the visual and auditory presentation of the movie…” All non-text feedback must be available via screen reader, support ARIA-live regions, and not require Flash. Pass WAVE accessibility audit (score ≥ 98%) on main question/feedback screens. Owner: Documentation/code stubs; Next action: Update FR-011 and supporting doc/code stubs to specify accessibility acceptance criteria and output interface.  

**Rationale:** Defines output behavior for user feedback during interaction.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-006
- **Conflicts with:** NFR-001
---

[FR-012]: Validate fraction inputs and handle invalid inputs  
**Description**: “Upon receiving the fraction inputs, the Space Fractions system will validate the integrity and format of the data to ensure they are integers and that the denominator is not zero… error handling for invalid inputs, such as displaying an error message… requesting a new input.”  

**Rationale:** Defines data validation and error-handling behavior.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, NFR-006
- **Conflicts with:** None specified
---

[FR-013]: Compute spaceship velocity adjustments from fraction inputs and apply to physics engine  
**Description**: (Derived from FR-013) “calculating spaceship velocity adjustments based on fraction inputs… calculates the velocity adjustment by converting the fraction into a decimal value and applying it to the spaceship's current velocity… applied to the game's physics engine to update the spaceship's speed in real-time.” Function signature: adjustVelocity(current:float, numerator:int, denominator:int) => newVelocity:float; Output must update UI and physics state in <100ms for >99.5% of attempts. Owner: Developer; Next action: Add technical spec for velocity adjustment, including performance measurement, input validation, and tolerance.  

**Rationale:** Specifies a concrete input-processing-output transformation and integration point (physics update).  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012, NFR-002
- **Conflicts with:** None specified
---

[FR-014]: Provide web-accessible “Math Umbrella” menu linking to external projects by topic  
**Description**: “The umbrella will be a web-based menu system allowing the user to choose between the systems.” / “The umbrella will be a singular component, providing links to projects relating to fractions, decimals, and percents… accessible over the World Wide Web.” / “Players interact… through a series of links… open… in a separate window.”  

**Rationale:** Describes navigation functionality to external learning resources/projects.  

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003, NFR-006
- **Conflicts with:** None specified
---

[FR-015]: Provide link from main menu to external Denominators web page  
**Description**: (Derived from FR-015) “Another button or hyperlink connects players to the Denominators' web page… opening the web page either within the game environment or in a separate browser window.” All external links must open in a separate window/tab with rel attributes set to 'noopener noreferrer'. Owner: Developer; Next action: Adjust link coding patterns.  

**Rationale:** Defines a specific external navigation function from the menu.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-003
- **Conflicts with:** None specified
---

[FR-016]: Provide administrator question updater with password gate  
**Description**: (Derived from FR-016) “a component accessible over the World Wide Web will allow the series of fraction questions to be updated by an administrator” / “She navigates to the updater page, which asks for a password. Upon correct submission… interface to update the system…” Forgotten password workflow requires email verification; password can only be reset after confirmation of registered admin email and logs all activity. Owner: Architect/Developer; Next action: Add password reset/recovery requirements and related workflow to documentation and user help.  

**Rationale:** Describes an admin-only function and authentication gate for content updates.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-017, FR-018, NFR-007
- **Conflicts with:** None specified
---

[FR-017]: Allow administrator to edit questions via simplified/intuitive web forms  
**Description**: “will be easily edited through simplified administrative screens.” / “user-friendly interface consisting of pulldown menus and text fields… Each question is managed on a separate page… button to progress… submission button…”  

**Rationale:** Defines the admin editing workflow and UI behaviors.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, NFR-006
- **Conflicts with:** None specified
---

[FR-018]: Validate and persist updated questions to a server-hosted file  
**Description**: (Derived from FR-018) “This information must be saved in a file on the web server where the Space Fractions system is hosted…” / “The tool then performs a validation check… Once the data passes… finalized… file contains the updated question data… system sequence can dynamically read and incorporate… real-time updates… without… restarts…” All question files must use JSON schema version X.Y: { schemaVersion: string, questions: [ ... ] }. Invalid uploads are rejected and system rolls back to last known-good copy, logging error/alert to admin. Owner: Architect/QA; Next action: Draft schema documentation and add to admin subsystem acceptance criteria.  

**Rationale:** Specifies server-side persistence and validation behavior enabling runtime content consumption.  

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, NFR-010, NFR-007
- **Conflicts with:** NFR-002 (if “real-time” implies very low propagation latency; not quantified in SRS)
---