# Non-Functional Requirements Results:
    [NFR-001]: Security
    **Description:** The system shall enforce role-based access control, store credentials using salted hashing, provide audit logging of every access, encrypt all data in transit and at rest using AES-256, and pass an independent penetration test prior to release.

    **Quality Attributes**: Security

    **Measurable Criteria (if provided):**  The system shall pass an independent penetration test prior to release.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [NFR-002]: Data Storage
    **Description:** The system shall store astronomical data in a format that is compatible with the GEMINI archive requirements. Astronomical data must validate against Gemini Archive Spec Rev 3.2/FITS 4.0; test: upload 10GB of sample data, zero errors. Interactive availability = 'retrieve any FITS file from last 3 days via API in <5 sec at 98th percentile, up to 3 concurrent users'.

    **Quality Attributes**: Data Storage

    **Measurable Criteria (if provided):**  The system shall store 7 days of data produced by the largest instrument.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-007 (Data Acquisition)
    - **Conflicts with:** None

    ---

    [NFR-003]: Network Bandwidth
    **Description:** The system shall transfer data between the virtual telescope system and attached workstations at a rate of 20-40 Mbits/second.

    **Quality Attributes**: Network Bandwidth

    **Measurable Criteria (if provided):**  20-40 Mbits/second

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-008 (Data Transfer)
    - **Conflicts with:** None

    ---

    [NFR-004]: Usability
    **Description:** The user interface shall allow users to execute standard observation workflow in <5 minutes with <2 errors, and be rated at least 4/5 in post-session usability feedback by >80% of test users.

    **Quality Attributes**: Usability

    **Measurable Criteria (if provided):**  <5 minutes with <2 errors, and be rated at least 4/5 in post-session usability feedback by >80% of test users.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-009 (User Interface)
    - **Conflicts with:** None

    ---

    [NFR-005]: Reliability
    **Description:** The system shall achieve ≥99.9% uptime (unplanned downtime <9h/year), MTBF ≥1000h, and automatically recover from defined faults within 5 minutes.

    **Quality Attributes**: Reliability

    **Measurable Criteria (if provided):**  ≥99.9% uptime (unplanned downtime <9h/year), MTBF ≥1000h, and automatically recover from defined faults within 5 minutes.

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---

    [NFR-006]: Maintainability
    **Description:** Mean time to repair (MTTR) shall be <4 hours for critical systems; all subsystems have end-to-end stepwise documented diagnostic and recovery/upgrade procedures.

    **Quality Attributes**: Maintainability

    **Measurable Criteria (if provided):**  <4 hours for critical systems

    **Dependencies** / **Conflicts**:
    - **Depends on:** FR-001 (User Access Control)
    - **Conflicts with:** None

    ---