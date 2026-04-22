# Architecturally Significant Requirements Results:

[ASR-001]: Home Web Server Architecture
**Description**: The DigitalHome System shall have the capability to establish an individual home web server hosted on a home computer. The home web server will provide interaction with and control of the DigitalHome elements, storage of plans/data, and user account management. Acceptance: Server must implement automated OS and app security update checks and push notification/alert for pending patches within 24h. Monitoring agent logs patch compliance; alert generated if not compliant within 48h. Next action: Document security maintenance flow and required monitoring/alarming.
**Architectural Impact:**  
- Requires deployment of server-side software on customer-premise hardware (home computer).
- Dictates a client-server architecture where the "server" is distributed to homes.
- Influences security architecture (exposing home server to Internet requires robust protection).
**Quality Attributes Affected:**  
- Security, Deployability, Performance
**Architectural Constraints:**  
- Must run on a home computer (not purely cloud-based).
- Must host web server and database locally. ≥99% uptime; logs service restarts; automated update checks nightly; alert if unpatched >48h.
**Rationale:**  
This requirement fundamentally dictates the deployment topology and distribution model of the software, moving away from a purely SaaS model to a hybrid local-server model.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003 (Security), NFR-007 (Cost)
- **Conflicts with:** None identified
---

[ASR-002]: Gateway Device and Communication Protocol
**Description**: The DigitalHome Gateway device shall provide communication with all DigitalHome devices and connect with a broadband Internet connection. The Gateway shall contain an RF Module for wireless communication (up to 1000-foot range). Acceptance: RF communication must achieve 1000ft line-of-sight in test home; fallback: mesh network config with hop limit=3 and total range ≥1000ft. Next action: Document wireless protocol choice and contingency for out-of-range devices.
**Architectural Impact:**  
- Requires a specific hardware component (Gateway) acting as a bridge between Internet and local sensors.
- Constrains communication pattern to Hub-and-Spoke (Gateway to Devices) + Internet Backhaul.
- Impacts data acquisition architecture to support 10Hz sampling over RF.
**Quality Attributes Affected:**  
- Performance, Reliability, Scalability (device count)
**Architectural Constraints:**  
- Must support RF Module integration.
- Must support broadband Internet connectivity.
- Must handle wireless range constraints (1000 feet). Fallback mesh network config with hop limit=3.
**Rationale:**  
Defines the core communication infrastructure and hardware interface layer, critical for all device interactions.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Performance), NFR-002 (Reliability)
- **Conflicts with:** None identified
---

[ASR-003]: Data Backup and Recovery Mechanism
**Description**: The DigitalHome System shall incorporate backup and recovery mechanisms. The system will backup all system data on a daily basis. If the system fails, the recovery mechanism shall restore system data from the most recent backup. System must retain at least 7 daily backups; system recovery must restore last backup within 10 minutes of failure (RTO); RPO (data loss) must not exceed latest daily backup interval (24h max). Annual restore tests required. Next action: Write measurable backup/recovery criteria and test plan.
**Architectural Impact:**  
- Requires persistent storage architecture with redundancy.
- Necessitates automated scheduled jobs (backup) and restore procedures.
- Influences database design (must support point-in-time recovery or daily snapshots).
**Quality Attributes Affected:**  
- Reliability, Availability, Data Integrity
**Architectural Constraints:**  
- Must implement automated daily backup routine. Must implement data restoration logic. Retain ≥7 daily backups. RTO ≤ 10 minutes. RPO ≤ 24 hours. Annual restore tests.
**Rationale:**  
Directly impacts data persistence strategy and disaster recovery architecture, essential for meeting reliability NFRs.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Reliability), FR-009 (Backup Operations)
- **Conflicts with:** None identified
---

[ASR-004]: Development Process and Technology Standards
**Description**: HomeOwner has designated object-oriented development, using UML 2.0, as the preferred method. All modules shall be designed to be incorporated in a fully specified commercial version. Where possible, employ widely used, accepted, and available hardware and software technology.
**Architectural Impact:**  
- Constrains the software development lifecycle and design methodology (OO, UML).
- Implies a modular architecture to allow transition from prototype to commercial version.
- Limits technology stack choices to widely available/accepted technologies (cost/minimization).
**Quality Attributes Affected:**  
- Maintainability, Modifiability, Cost
**Architectural Constraints:**  
- Must use Object-Oriented design.
- Must use UML 2.0 for documentation.
- Must use standard/available technology (no custom/exotic tech).
**Rationale:**  
Constrains the engineering process and technology stack, influencing component design and long-term evolvability of the architecture.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-005 (Maintainability), NFR-007 (Cost)
- **Conflicts with:** None identified
---

[ASR-005]: Simulated Environment Testing
**Description**: The prototype DigitalHome software system will be situated in a simulated environment. The simulated environment will be realistic and adhere to the physical properties and constraints of an actual home and to real sensors and controllers. Acceptance: Automatic test harness executes all core device control and failure flows, logs timing; test report demonstrates 95% coverage and <10% timing variance. Next action: Define protocol list/assert test/coverage plan for simulation.
**Architectural Impact:**  
- Requires a simulation layer or adapter pattern to mimic hardware behavior during testing.
- Impacts the test architecture and integration strategy (hardware-in-the-loop vs. software simulation).
**Quality Attributes Affected:**  
- Testability, Reliability
**Architectural Constraints:**  
- System must support operation in a simulated hardware environment. Simulation must adhere to physical constraints (range, device limits). Emulates 95% of protocols/failure scenarios; ±10% latency fidelity.
**Rationale:**  
Influences the test harness architecture and the abstraction level of hardware interfaces to allow for simulation.
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Reliability)
- **Conflicts with:** None identified
---