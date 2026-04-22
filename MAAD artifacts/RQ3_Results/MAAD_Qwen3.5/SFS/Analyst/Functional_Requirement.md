# Functional Requirements Results:
[FR-001]: Introductory Movie Playback and Skip
**Description**: Upon starting the system, the system shall automatically play an introductory movie to provide background story and information. The system shall allow the user to skip the movie at any point via a mouse click, immediately transitioning to the main menu. If no click is detected, the movie shall play to completion before transitioning.

**Rationale:** This requirement defines the initial user interaction and state transition (Intro -> Main Menu), representing a core behavior of the application startup sequence.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Performance/Load Time), ASR-001 (Web-Based Architecture)
- **Conflicts with:** None
---
[FR-002]: Main Menu Navigation and Help
**Description**: The system shall display a main menu screen containing options to start the game, view a help section, and access external links (e.g., Denominators' web page). The system shall remain in a listening state for mouse clicks on these options and execute the corresponding action (start game, show help, redirect URL).

**Rationale:** This requirement describes the primary navigation function and entry point for user tasks, transforming user input into system state changes or external redirects.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Intro Movie), FR-003a (Gameplay Sequence)
- **Conflicts with:** None
---
[FR-003a]: Fraction Question Presentation (Multiple-Choice)
**Description**: The system shall support multiple-choice fraction questions. User answer input for all fraction questions shall be via mouse selection of multiple-choice options. No free-form typing or custom fraction entry is supported. (Derived from FR-003)

**Rationale:** This defines the core educational function of the system, detailing the input (question display) and output (answer selection) transformation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Question Updater - data source)
- **Conflicts with:** None
---
[FR-003b]: Fraction Question Presentation (Direct Input)
**Description**: The system shall support direct fraction input (numerator/denominator fields) for velocity adjustment phases as described in the SRS. Both types must be validated and configurable per question definition schema. (Derived from FR-003)

**Rationale:** This defines the core educational function of the system, detailing the input (question display) and output (answer selection) transformation.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-007 (Question Updater - data source)
- **Conflicts with:** None
---
[FR-004]: Answer Validation and Feedback
**Description**: Upon receiving an answer, the system shall validate the response. If correct, the system shall display a confirmation message and proceed to the next question. If incorrect, the system shall inform the player of the mistake and allow a retry without points. The system shall provide immediate visual feedback (animations) for success or failure. Auditory feedback must be optional/on mute by default, with equivalent visual cues for all sounds.

**Rationale:** This requirement specifies the processing logic for user inputs and the corresponding system responses, essential for the learning loop.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-003a (Question Presentation), FR-003b (Question Presentation), NFR-003 (Feedback Responsiveness)
- **Conflicts with:** None
---
[FR-005]: Scoring and Story Adaptation
**Description**: The system shall track the user's score locally. All user scores and game session data are maintained solely in the browser memory or localStorage, and are destroyed upon browser/tab close. No scoring data is sent to the server or retained after the game session. At critical question junctures, the system shall alter the storyline progression based on the user's response (correct/incorrect). The system shall calculate a final rank/score at the end of the sequence.

**Rationale:** This describes the internal state management and conditional logic that personalizes the user experience based on performance.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Answer Validation)
- **Conflicts with:** None
---
[FR-006]: Ending Scene and Session Management
**Description**: Upon completion of the question sequence, the system shall display an ending scene reflecting the player's performance. The system shall provide options to quit the system or return to the main menu to try again.

**Rationale:** This defines the termination logic of the gameplay loop and the transition options available to the user post-assessment.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-005 (Scoring)
- **Conflicts with:** None
---
[FR-007]: Administrator Question Updater
**Description**: The system shall provide a web-accessible interface for administrators to update, edit, and save fraction questions. The system shall require password authentication for access. Updates shall be saved to a file on the web server and applied without requiring a system restart. Questions must comply with schema: {id: string, prompt: string, choices: array of string, answer_index: int, rationale: string} and pass linter before save.

**Rationale:** This is a distinct functional capability for system maintenance, involving authentication, data modification, and persistence.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Security - Admin Auth), ASR-002 (File-Based Content Management)
- **Conflicts with:** None
---
[FR-008]: Math Umbrella External Links
**Description**: The system shall provide a component containing links to external S2S projects (fractions, decimals, percents). Selecting a link shall open the external resource in a separate window while maintaining the current system session.

**Rationale:** This describes the integration behavior with external systems and the handling of browser window context.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Platform Compatibility)
- **Conflicts with:** None
---