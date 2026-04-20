# Functional Requirements Results:
[FR-001]: System Introduction
**Description**: On page load, autoplay intro. [Label: 'Intro Movie']. If user clicks/taps, skip and go directly to main menu.
**Rationale:** This requirement describes a specific behavior of the system, which is to display an introductory movie with specified input/output behavior.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Main Menu
**Description**: The Space Fractions system will have a main menu, including a brief help section.
**Rationale:** This requirement describes a function of the system, which is to provide a main menu with a help section.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-003]: Fraction Questions
**Description**: { "question_id": "string", "prompt": "string", "options": [{ "value": "fraction-string", "is_correct": true/false }], "user_answer": "fraction-string" }
**Rationale:** This requirement describes a specific task of the system, which is to present fraction questions to the user with a defined input/output schema.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-004]: Score Calculation and Feedback
**Description**: The Space Fractions system will have an ending scene where the user's score is calculated and ranked, with an option to quit the system or try again.
**Rationale:** This requirement describes a function of the system, which is to calculate the user's score and provide feedback.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-005]: Administrator Question Updater
**Description**: All questions must be validated against a JSON schema and admin changes logged with user ID and timestamp; invalid submissions are rejected. { "user_id": "string", "event_type": "string", "ts": "ISO8601-timestamp", "ip_address": "IPv4/IPv6" }
**Rationale:** This requirement describes a specific function of the system, which is to allow administrators to update fraction questions with validation and logging.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-006]: User Input and Output
**Description**: The system must accept input from mouse, touch, and keyboard navigation, and emit output conforming to WAI-ARIA feedback requirements. All interactive components MUST define ARIA roles and support Tab/Enter navigation. Example: <button aria-label="Start Game">Start</button>
**Rationale:** This requirement describes the input and output behavior of the system.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-007]: System Availability
**Description**: System must achieve 99.5% monthly uptime, measured via external uptime monitor with 5-minute check interval.
**Rationale:** This requirement describes a function of the system, which is to be available over the Internet with a specified uptime.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-008]: Math Umbrella Component
**Description**: The Math Umbrella component is designed to serve as an educational resource hub within the system, providing players with easy access to a curated selection of external S2S projects that are specifically tailored to sixth graders.
**Rationale:** This requirement describes a function of the system, which is to provide an educational resource hub.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---