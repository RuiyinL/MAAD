# Functional Requirements Results:
    [FR-001]: User Access Control
    **Description**: The system shall provide access control to the Gemini system, allowing users to log in and access different parts of the system based on their privileges. The system shall define a schema stub for user entity, including 'role', 'privileges', and access scopes (mode, location, operational context); provide a table mapping roles to permitted actions. Owner: Team-API; Next action: add schema stub

    **Rationale:** This requirement is functional because it describes a specific behavior of the system, namely controlling user access.

    **Dependencies** / **Conflicts**:
    - **Depends on:** NFR-001 (Security)
    - **Conflicts with:** None

    ---

    [FR-002]: Observing Mode
    **Description**: The system shall provide an observing mode that allows astronomers to collect science data, select instrument parameters, and perform quick-look data reduction. Quick-look data reduction shall generate a preview FITS image and compute SNR within 2 seconds after exposure. SNR calculated via method X in [DOI], using [data ext/HDU]; must produce result in FITS header within 2s; acceptance: sample workflow run, compared to reference output.

    **Rationale:** This requirement is functional because it describes a specific mode of operation of the system.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [FR-003]: Monitoring Mode
    **Description**: The system shall provide a monitoring mode that allows users to monitor the status of the telescope and instruments.

    **Rationale:** This requirement is functional because it describes a specific mode of operation of the system.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [FR-004]: Operation Mode
    **Description**: The system shall provide an operation mode that allows users to control the telescope and instruments directly.

    **Rationale:** This requirement is functional because it describes a specific mode of operation of the system.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [FR-005]: Testing Mode
    **Description**: The system shall provide a testing mode that allows users to test the telescope and instruments.

    **Rationale:** This requirement is functional because it describes a specific mode of operation of the system.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [FR-006]: Administrative Mode
    **Description**: The system shall provide an administrative mode that allows users to inquire about system utilization, efficiency, etc.

    **Rationale:** This requirement is functional because it describes a specific mode of operation of the system.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [FR-007]: Data Acquisition
    **Description**: The system shall acquire detector data as FITS files, with headers conforming to Gemini archive standards, and store to disk array X. FITS file must conform to [GeminiArchiveFITSvX] with required headers: [EXPID, DATE-OBS, ...]; validation: fits-schema-validator passes all files.

    **Rationale:** This requirement is functional because it describes a specific behavior of the system, namely acquiring and storing data.

    **Dependencies** / **Conflicts**:
    - **Depends on:** NFR-002 (Data Storage)
    - **Conflicts with:** None

    ---

    [FR-008]: Data Transfer
    **Description**: The system shall transfer data between the virtual telescope system and attached workstations at a rate of 20-40 Mbits/second.

    **Rationale:** This requirement is functional because it describes a specific behavior of the system, namely transferring data.

    **Dependencies** / **Conflicts**:
    - **Depends on:** NFR-003 (Network Bandwidth)
    - **Conflicts with:** None

    ---

    [FR-009]: User Interface
    **Description**: The user interface shall allow astronomers to schedule observations, monitor instrument status, and retrieve data using workflows that require no more than five steps per task.

    **Rationale:** This requirement is functional because it describes a specific behavior of the system, namely providing a user interface.

    **Dependencies** / **Conflicts**:
    - **Depends on:** NFR-004 (Usability)
    - **Conflicts with:** None

    ---