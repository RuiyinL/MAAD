# Functional Requirements Results:
[FR-001]: Introductory Movie Playback  
**Description**: Upon starting the Space Fractions system, an introductory movie plays automatically to provide background story and information. The movie can be skipped at any time with a mouse click or keyboard command (tab/enter/space), transitioning to the main menu. If not skipped, it plays to completion before transitioning. Acceptance: All movie skip actions must be achievable via both mouse and keyboard.  
**Rationale:** Describes system behavior triggered by startup condition (movie playback) and user input (click/keyboard to skip).  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001 (HTML5 runtime)  
---  

[FR-002]: Main Menu Navigation  
**Description**: At the main title screen, users can view a help section with basic instructions, see team information, click a button to start gameplay, or select a link to access the Denominators' web page. Navigation occurs via mouse clicks or keyboard commands.  
**Rationale:** Specifies system functions (displaying menu options) and input-output transformations (click/keyboard → screen transition).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001  
---  

[FR-003a]: Question Presentation and Answer Validation  
**Description**: Users progress through multiple-choice fraction questions. User selects answer; system validates and confirms correctness. Derived from FR-003.  
**Rationale:** Defines atomic input validation behavior for fraction questions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-002  
---  

[FR-003b]: Hint Delivery System  
**Description**: System displays hints through robotic sidekick when user provides incorrect answers. Derived from FR-003.  
**Rationale:** Describes conditional help functionality based on user input.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003a  
---  

[FR-003c]: Storyline Branching Logic  
**Description**: For critical questions, system branches storyline based on answer correctness. Derived from FR-003.  
**Rationale:** Specifies narrative adaptation behavior based on user decisions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003a  
---  

[FR-004]: Velocity Adjustment Calculation  
**Description**: During gameplay, process fraction inputs (numerator/denominator integers) for spaceship velocity adjustments. Validate inputs (integers, non-zero denominator), convert fractions to decimals, apply to velocity, and update physics. Display error messages for invalid inputs. Acceptance: On valid input, velocity update must occur <200ms and display new speed as 'x.xx m/s'. On error, display 'Please enter a valid fraction' in dialog for ≥3sec.  
**Rationale:** Describes computational function (fraction-to-velocity transformation) with input validation and output generation.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003a  
---  

[FR-005]: Ending Scene Display  
**Description**: After the final question, display total score and narrative conclusion based on critical decisions. Provide options to quit or return to the main menu via mouse clicks or keyboard commands.  
**Rationale:** Specifies end-state behavior (score display, narrative resolution) and user-initiated transitions.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-003c  
---  

[FR-006]: Question Updater Operation  
**Description**: Administrators navigate to a password-protected web interface, edit questions via forms/pulldown menus, submit changes, and trigger validation. Valid updates save to a server file for system access. Question files must conform to Appendix A: JSON Schema v1.0 for questions.  
**Rationale:** Defines administrative functions (authentication, data editing, persistence) with input-processing-output flow.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-004 (server file storage)  
---  

[FR-007]: Math Umbrella Resource Access  
**Description**: Provide links to external S2S projects (fractions/decimals/percents). Open selected resources in separate browser windows upon mouse click or keyboard command. Acceptance: Upon clicking a resource link, the system opens the destination in a new browser tab; if pop-ups are blocked, an alert informs the user. The originating system session remains active and visible.  
**Rationale:** Describes linking functionality (input → resource access) with concrete acceptance criteria for window handling.  
**Dependencies** / **Conflicts**:  
---