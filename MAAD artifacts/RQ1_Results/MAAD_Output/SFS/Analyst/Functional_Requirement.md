# Functional Requirements Results

[FR-001]: Provide web-based interactive fraction-learning game  
**Description**: “The Space Fractions system is a learning tool created to help improve fraction-solving skills for sixth-grade students. The product will be a web-based, interactive system.”  
**Rationale:** Describes the primary system function delivered to users (interactive learning gameplay).  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001, NFR-002
- **Conflicts with:** NFR-003
---

[FR-002]: Provide umbrella (menu) to access related math projects  
**Description**: “The umbrella will be a web-based menu system allowing the user to choose between the systems… providing links to projects relating to fractions, decimals, and percents in a format accessible over the World Wide Web.”  
**Rationale:** Specifies a user-facing navigation function to select among multiple systems/resources.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001
- **Conflicts with:** NFR-003
---

[FR-003]: Play introductory movie and transition to main menu  
**Description**: “The Space Fractions system will have an introductory movie to set up the storyline… Upon starting… the user is taken through a brief introductory movie… Otherwise, they will watch the movie to its completion and be taken to the main screen.”  
**Rationale:** Defines a concrete behavior sequence and state transition at startup.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002
- **Conflicts with:** Not specified
---

[FR-004]: Allow user to skip introductory movie via mouse click  
**Description**: “The primary input… is… a mouse click… allows players the option to skip the introductory movie at any point… If a click is detected, the movie is immediately terminated, and the system transitions… to the game's main menu.”  
**Rationale:** Describes an input-triggered behavior and resulting navigation.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, NFR-004
- **Conflicts with:** Not specified
---

[FR-005]: Provide main menu with help and links  
**Description**: “The Space Fractions system will have a main menu, including a brief help section… At the main title screen, the user will be able to view a general help screen… Also, a short summary of our team and a link to our website will be provided.”  
**Rationale:** Specifies UI functions available from the main screen.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** Not specified
---

[FR-006]: Start gameplay from main menu  
**Description**: “To start the Space Fractions system, the user will click on the corresponding button.” / “One button initiates the game, leading players directly into the gameplay experience.”  
**Rationale:** Defines a user action and system response to initiate the game sequence.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005
- **Conflicts with:** Not specified
---

[FR-007]: Redirect user to external Denominators web page from main menu  
**Description**: “Another button or hyperlink connects players to the Denominators' web page… the system facilitates this redirection, opening the web page either within the game environment or in a separate browser window.”  
**Rationale:** Describes a navigation function to an external resource.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-005, NFR-001
- **Conflicts with:** NFR-003
---

[FR-008]: Present sequential fraction questions integrated with storyline  
**Description**: “The Space Fractions system will have a series of fraction questions… that sequentially form a storyline…” / “The primary function… is to engage players with a series of multiple-choice questions focused on fractions… integrated within a storyline…”  
**Rationale:** Core functional behavior: content presentation and progression.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006
- **Conflicts with:** Not specified
---

[FR-009]: Support multiple-choice answering via mouse clicks  
**Description**: “These questions… will be presented as a multiple-choice questionnaire. The user will be given a problem and then must click the correct solution.” / “Input will consist entirely of mouse clicks for the user to choose answer options and to set preferences.”  
**Rationale:** Defines input modality and answering mechanism.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004
- **Conflicts with:** Not specified
---

[FR-010]: Provide per-question feedback and retry behavior  
**Description**: “If the player selects the correct answer, a confirmation message is displayed… For incorrect answers, the player is informed of the mistake and given another opportunity… without the possibility of earning points for that question.”  
**Rationale:** Specifies system responses to correct/incorrect inputs and scoring rule.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** Not specified
---

[FR-011]: Provide hints via robotic sidekick  
**Description**: “A friendly robotic sidekick will assist with general usability issues and give hints towards the correct response.”  
**Rationale:** Describes an assistance function during gameplay.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-004
- **Conflicts with:** Not specified
---

[FR-012]: Adapt storyline based on user progress and critical questions  
**Description**: “The systemplay will be dynamic and adaptive to provide different storylines based on the user's progress.” / “The system sequence includes ‘critical points’ where the storyline can diverge based on whether the player answers these pivotal questions correctly.”  
**Rationale:** Defines conditional branching behavior affecting narrative flow.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, FR-010
- **Conflicts with:** Not specified
---

[FR-013]: Calculate and present final score with ranking and customized message  
**Description**: “The Space Fractions system will have an ending scene where the user's score is calculated and ranked…” / “In addition, the player's exact score will be given with a customized message.”  
**Rationale:** Specifies end-of-game computation and output presentation.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, FR-014
- **Conflicts with:** Not specified
---

[FR-014]: Store user score locally for end-of-game results  
**Description**: Derived from FR-014. “User score is kept in browser memory (not persisted to disk or localStorage); resets when user closes/reloads tab.” Next action: Add storage model to requirements and data architecture section.  
**Rationale:** Defines required data handling behavior to support scoring output.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010
- **Conflicts with:** Not specified
---

[FR-015]: Provide ending scene with quit or try-again navigation  
**Description**: “The Space Fractions system will have an ending scene… with an option to quit the system or try again.” / “presents players with the option to either conclude… or navigate back to the main menu…”  
**Rationale:** Defines end-state UI actions and navigation outcomes.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-013
- **Conflicts with:** Not specified
---

[FR-016]: Validate fraction input for velocity adjustment (integers; denominator non-zero)  
**Description**: Derived from FR-016. “If input fails integer/≠0 rule, system displays red validation message and focuses input field for correction.” Next action: List explicit input validation rules and error messages in functional spec.  
**Rationale:** Input validation is a functional behavior with explicit rules.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-017
- **Conflicts with:** Not specified
---

[FR-017]: Compute spaceship velocity adjustment from fraction input and apply in real time  
**Description**: “If the input is valid… calculates the velocity adjustment by converting the fraction into a decimal value and applying it to the spaceship's current velocity… applied to the game's physics engine to update the spaceship's speed in real-time… output timing is immediate.”  
**Rationale:** Defines a deterministic input→processing→output transformation and application to game state.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016
- **Conflicts with:** Not specified
---

[FR-018]: Handle invalid fraction inputs with error message and re-entry  
**Description**: “The processing includes error handling for invalid inputs, such as displaying an error message to the player and requesting a new input.”  
**Rationale:** Specifies functional error-path behavior and user guidance.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-016, NFR-004
- **Conflicts with:** Not specified
---

[FR-019]: Provide standards-based audio/animation feedback for success/failure  
**Description**: Derived from FR-019. “All answer feedback cues must fire DOM event (type=feedback) within 500ms of user click, observable in browser devtools.” Next action: Update FR-019 wording and test plan for observable JS event/spec.  
**Rationale:** Defines system outputs tied to gameplay outcomes with testable timing and observable signal.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-010, NFR-002
- **Conflicts with:** Not specified
---

[FR-020]: Provide web-accessible Question Updater for administrators  
**Description**: “a component accessible over the World Wide Web will allow the series of fraction questions to be updated by an administrator…” / “The Question Updater is envisioned as a web-accessible tool designed specifically for system administrators.”  
**Rationale:** Describes an administrative function for content management.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, FR-022, NFR-001
- **Conflicts with:** Not specified
---

[FR-021]: Authenticate administrator access to updater via password  
**Description**: Derived from FR-021. “Admin authentication must: (1) Require passwords ≥12 char, stored salted+hashed with bcrypt/Argon2, (2) Lock out after 5 failed logins, (3) Reset by helpdesk or 1-hour timeout, (4) Audit log each login/edit with UTC time, admin ID, remote IP, field changed, before/after value; logs stored ≥2 years.” Next action: Write a password/security policy section in SRS; enumerate all controls and acceptance tests for admin subsystem.  
**Rationale:** Defines an access-control function (authentication step) with explicit security controls and audit requirements.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-020, NFR-008
- **Conflicts with:** Not specified
---

[FR-022]: Allow admin to edit questions via simplified web forms and save to server file  
**Description**: “This information must be saved in a file on the web server… and will be easily edited through simplified administrative screens.” / “Administrators interact… through… pulldown menus and text fields… Each question is managed on a separate page… submission… validation check… Once… passes… finalized… file contains the updated question data… system sequence can dynamically read…”  
**Rationale:** Specifies CRUD-like editing workflow, validation, and persistence mechanism.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-021, NFR-007
- **Conflicts with:** Not specified
---

[FR-023]: Open selected Math Umbrella external project in separate window  
**Description**: Derived from FR-023. “On link trigger, attempt window.open; if blocked, display fallback hyperlink to click.” Next action: Add detailed open-new-window behavior to spec and user manual.  
**Rationale:** Defines link selection behavior and windowing outcome with pop-up blocker fallback.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, NFR-001
- **Conflicts with:** NFR-003
---