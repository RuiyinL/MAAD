# Non-Functional Requirements Results:

[NFR-001]: Continuous availability (24/7/365)  
**Description:** “Reliability requirements – The RLCS Application must be available 24 hours per day, 7 days per week, 365 days per year.” / “The RLCS must be available 24/7, 365 days per year.”  
**Quality Attributes**: Availability, Reliability  
**Measurable Criteria (if provided):** 24/7/365 (no downtime target beyond uptime % elsewhere).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-056 (degraded mode), NFR-002  
- **Conflicts with:** Not specified  
---

[NFR-002]: Recovery time objective (RTO) ≤ 10 minutes on failure  
**Description:** “If there is a failure, recovery time must be no greater than 10 minutes…” Derived refinement per evaluator: From time of loss-of-control or monitoring (failure detection), RLCS must restore full operator command/control and status visibility within 10 minutes. Owner/Next action: Clarify the RTO metric's start/end points.  
**Quality Attributes**: Reliability, Resilience  
**Measurable Criteria (if provided):** RTO ≤ 10 minutes, measured from failure detection to restoration of full operator command/control and status visibility.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-056, NFR-003  
- **Conflicts with:** Not specified  
---

[NFR-003]: Annual uptime target (incomplete)  
**Description:** “…total yearly uptime must be at least 99.” Derived refinement per evaluator: The RLCS Application must maintain total yearly uptime of at least 99.9%, excluding planned maintenance. Owner/Next action: Confirm correct annual uptime % with stakeholders and update requirement wording.  
**Quality Attributes**: Availability  
**Measurable Criteria (if provided):** ≥ 99.9% total yearly uptime, excluding planned maintenance.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-002  
- **Conflicts with:** Not specified  
---

[NFR-004]: Safety-critical system; catastrophic risk must be prevented  
**Description:** “Safety and security considerations… possibility of opening… opposite direction… catastrophic… barrier gates… catastrophic… if the system allows… an entrance to be opened… when … opposite … open, then the system has failed.” Derived refinement per evaluator: No command or sequence shall result in a wrong-way opening with probability greater than 10⁻⁹/hour of operation; passing hazard/fault-injection test batteries is required. Owner/Next action: Define and agree acceptable safety risk threshold and validation method.  
**Quality Attributes**: Safety, Reliability  
**Measurable Criteria (if provided):** Probability of wrong-way opening ≤ 10⁻⁹ per hour of operation; must pass hazard/fault-injection test batteries (details not specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, FR-039, FR-034  
- **Conflicts with:** FR-036 (override) unless constrained  
---

[NFR-005]: One-way external data transfer frequency (30 seconds)  
**Description:** “The transfer will occur every 30 seconds.”  
**Quality Attributes**: Performance, Interoperability  
**Measurable Criteria (if provided):** 30-second transfer interval.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-030, FR-029  
- **Conflicts with:** Not specified  
---

[NFR-006]: Status display update period 2 seconds  
**Description:** “Status information… updated every 2 seconds.” / “The field device status information display update frequency shall be 2 seconds…”  
**Quality Attributes**: Performance (freshness), Usability  
**Measurable Criteria (if provided):** 2 seconds (configurable to more than 2 seconds).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, NFR-007, NFR-011  
- **Conflicts with:** Not specified  
---

[NFR-007]: Device state change reflected on screen within 2 seconds  
**Description:** “Any change in device state shall be reported on the screen not later than 2 seconds from the time it occurs.”  
**Quality Attributes**: Performance (latency)  
**Measurable Criteria (if provided):** ≤ 2 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, NFR-011  
- **Conflicts with:** Not specified  
---

[NFR-008]: Monitoring/polling rate per mode (stored in DB; degraded mode specific)  
**Description:** “During ‘degraded’ mode, the system shall monitor device sensors at the frequency rate stored in the database… In general… frequency specified in the System Control Parameters for that mode.”  
**Quality Attributes**: Performance, Configurability  
**Measurable Criteria (if provided):** Not specified (rate values stored in DB).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, FR-049  
- **Conflicts with:** NFR-006 (2s update) if configured higher than 2s  
---

[NFR-009]: Startup time limit (field startup ≤ 30 seconds)  
**Description:** “If everything is OK the start up process shall not exceed 30 seconds.”  
**Quality Attributes**: Performance, Availability  
**Measurable Criteria (if provided):** ≤ 30 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-045  
- **Conflicts with:** Not specified  
---

[NFR-010]: Facility map refresh 2 seconds (configurable to more than 2 seconds)  
**Description:** “The facility map on the screen shall refresh every 2 seconds but can be configurable within the database to more than 2 seconds…”  
**Quality Attributes**: Performance, Usability  
**Measurable Criteria (if provided):** 2 seconds default; configurable higher.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-012, FR-049  
- **Conflicts with:** Not specified  
---

[NFR-011]: Alarm detection/notification latency ≤ 2 seconds  
**Description:** “The RLCS notification to the operator workstation of any critical alarms shall occur within 2 seconds of alarm detection…” / “The RLCS shall detect alarm conditions within 2 seconds of occurrence.”  
**Quality Attributes**: Performance, Safety  
**Measurable Criteria (if provided):** ≤ 2 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-047, FR-013  
- **Conflicts with:** Not specified  
---

[NFR-012]: Log integrity (non-editable logs)  
**Description:** “Device command log shall not be editable by users… System Operation command shall not be editable by users… Device command log shall… include failed or aborted commands.”  
**Quality Attributes**: Security (non-repudiation), Auditability  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-025, FR-024  
- **Conflicts with:** FR-026 (editable work order fields must not alter immutable log facts)  
---

[NFR-013]: Non-volatile residency of controller code/data and replicated rule sets  
**Description:** “The processing code at the FCU and DCU controllers shall be resident in non-volatile memory.” / “application software processing code and … login information at the FCU and DCU controllers shall be resident in non-volatile memory.” / “items… replicated… maintained in non-volatile, non-removable memory…”  
**Quality Attributes**: Reliability, Safety  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-053, FR-052  
- **Conflicts with:** Not specified  
---

[NFR-014]: Communications integrity via checksums; integrity checks “multiple levels”  
**Description:** “Valid checksum algorithms must be employed to check the integrity of messages between units.”  
**Quality Attributes**: Security (integrity), Reliability  
**Measurable Criteria (if provided):** Not specified (algorithm unspecified; separate MD5 for code/data).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-033, FR-042  
- **Conflicts with:** Not specified  
---

[NFR-015]: Security boundary via firewall; no wireless FCU–DCU; secure remote access  
**Description:** “remote access through a firewall… by authorized users.” / “wireless connections between the FCU and DCU controllers are not an option due to security and interference considerations” / “secure remote dial-in interface through a firewall…” Derived refinement per evaluator: Remote access via dial-in or network must use mutually-authenticated TLS 1.2+ or equivalent, with credentialed user logins and full access/session logging. Owner/Next action: Expand NFR-015 to specify explicit connection/auth and encryption requirements.  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** TLS 1.2+ (or equivalent) with mutual authentication; full access/session logging (retention not specified here).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-028  
- **Conflicts with:** Not specified  
---

[NFR-016]: Role-based access control with multi-dimensional security levels  
**Description:** “Personnel Security Level… restrict access… Command Level, Device, Mode, Workstation…” and “Command levels… ‘Status Only’, ‘Control’, ‘Override’…”  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-018, FR-009, FR-005  
- **Conflicts with:** Not specified  
---

[NFR-017]: Password policy controls (aging, minimum username/password lengths)  
**Description:** “The system will provide for password aging… minimum username and password lengths… controllable by the system administrator.”  
**Quality Attributes**: Security  
**Measurable Criteria (if provided):** Not specified (minimum lengths not given).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-018, FR-003  
- **Conflicts with:** Not specified  
---

[NFR-018]: Private network requirement and media constraints  
**Description:** “RLCS workstations and controllers will reside on a private network… communication media will include fiber, Cat 5 wiring, leased lines and dial-up lines… communications … continue to be copper… primary mode fiber and secondary ISDN… fail over will be transparent…” Derived refinement per evaluator: RLCS workstations/controllers must reside on VLANs/subnets segregated from public networks, with controlled interfaces to DMZ/externals. Owner/Next action: Consult security architects to specify network security zones.  
**Quality Attributes**: Reliability, Performance, Security  
**Measurable Criteria (if provided):** Logical separation/segregation via VLANs/subnets and controlled interfaces to DMZ/externals (no quantitative metrics specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-056  
- **Conflicts with:** Not specified  
---

[NFR-019]: Transparent communications failover (fiber primary; ISDN secondary)  
**Description:** “The primary mode of communication is fiber and secondary is ISDN. The fail over will be transparent to the RLCS application.”  
**Quality Attributes**: Availability, Reliability  
**Measurable Criteria (if provided):** Not specified.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-018  
- **Conflicts with:** Not specified  
---

[NFR-020]: Single operator constraint (only one operator logged on at a time)  
**Description:** “Only one ‘operator’ may be logged onto the system at any given time.” Derived refinement per evaluator: Only one operator session may have command control; monitor-only sessions may be concurrent. Owner/Next action: Clarify role definitions and session limits.  
**Quality Attributes**: Security, Safety (operational control), Usability  
**Measurable Criteria (if provided):** At most 1 Operator role session with command control concurrently; concurrent monitor-only sessions permitted (numeric limit addressed in NFR-023).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-006  
- **Conflicts with:** NFR-023 (supports multiple users logged on) unless role-scoped  
---

[NFR-021]: No apportionment across releases (single release delivery)  
**Description:** “The RLCS software will not be apportioned, or split between multiple releases. The complete set of requirements will be included in one release.”  
**Quality Attributes**: Delivery/Process Constraint  
**Measurable Criteria (if provided):** Single release.  
**Dependencies** / **Conflicts**:  
- **Depends on:** Not specified  
- **Conflicts with:** Not specified  
---

[NFR-022]: Extensibility without programming effort for roadway changes  
**Description:** “The RLCS software shall be designed to allow for future changes to the roadway without requiring programming effort… change in the number of closure devices.” Derived refinement per evaluator: Addition/removal of field devices and map objects shall be achieved in production via GUI/config updates, not source code or deployed binary changes. Owner/Next action: Add acceptance test steps for extensibility.  
**Quality Attributes**: Maintainability, Modifiability  
**Measurable Criteria (if provided):** Must be achievable via GUI/config updates; no source code or deployed binary changes (no additional quantitative criteria specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-049, FR-022, FR-023  
- **Conflicts with:** Not specified  
---

[NFR-023]: Multi-user support up to DB-defined maximum  
**Description:** “The RLCS shall support multiple users logged on, up to the limit of the number of users defined in the database.” Derived refinement per evaluator: The RLCS shall support at least 10 concurrent non-operator user sessions, and 1 operator session, unless otherwise configured. Owner/Next action: Propose/test and document a reasonable default user concurrency target.  
**Quality Attributes**: Scalability  
**Measurable Criteria (if provided):** ≥ 10 concurrent non-operator sessions and 1 operator session by default; higher limits permitted if configured.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-018  
- **Conflicts with:** NFR-020 (single operator) unless role-scoped  
---

[NFR-024]: GUI response time for status updates ≤ 2 seconds (excluding device/network)  
**Description:** “Not including device and network response times, requests from the GUI for status updates shall not exceed 2 seconds to update the GUI display.”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** ≤ 2 seconds (excluding device/network).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-032, NFR-025  
- **Conflicts with:** Not specified  
---

[NFR-025]: GUI response time for control command processing ≤ 2 seconds (excluding device/network)  
**Description:** “Not including device and network response time, requests from the GUI for device status changes (control commands) shall not exceed 2 seconds.”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** ≤ 2 seconds (excluding device/network).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, FR-033  
- **Conflicts with:** Not specified  
---

[NFR-026]: Device sensor status arrival to RLCS within 2 seconds  
**Description:** “The RLCS shall receive device status information from devices sensors within 2 seconds of the status information being issued by the device sensor.”  
**Quality Attributes**: Performance, Safety  
**Measurable Criteria (if provided):** ≤ 2 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031  
- **Conflicts with:** Not specified  
---

[NFR-027]: Field device command response within 12 seconds after operator confirmation  
**Description:** “Field devices shall receive respond to commands from the RLCS within 12 seconds of the command confirmation being issued by the operator…”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** ≤ 12 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-038, FR-039  
- **Conflicts with:** Not specified  
---

[NFR-028]: Controller-to-central status transmission every 2 seconds or less  
**Description:** “The field units (controllers) shall continually monitor… and send the status to the central … computer in the TMC every 2 seconds or less.”  
**Quality Attributes**: Performance, Availability  
**Measurable Criteria (if provided):** ≤ 2 seconds.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-031, NFR-018  
- **Conflicts with:** Not specified  
---

[NFR-029]: Scheduled event scan at least every 60 seconds  
**Description:** “At a minimum of every 60 seconds, the system shall check the current date and time against a list of scheduled events…”  
**Quality Attributes**: Performance  
**Measurable Criteria (if provided):** ≤ 60 seconds between checks.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-037  
- **Conflicts with:** Not specified  
---

[NFR-030]: Report retention of generated results (≥60 days, configurable up to 1 year)  
**Description:** “store and retrieve previously created report results … minimum period of 60 days, but configurable for up to one year.”  
**Quality Attributes**: Maintainability, Operability  
**Measurable Criteria (if provided):** ≥ 60 days; configurable to 1 year.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-051, FR-049  
- **Conflicts with:** Not specified  
---

[NFR-031]: Continuous operation without reboot for ≥ 30 consecutive days  
**Description:** “The RLCS must demonstrate the ability to function continuously without needing to be reset or rebooted due to an RLCS error for at least 30 consecutive days.” Derived refinement per evaluator: System shall log its uptime daily and create a fault/alert event if a reboot occurs within 30 consecutive days due to RLCS error. Owner/Next action: Add explicit uptime monitoring/reporting requirements.  
**Quality Attributes**: Reliability, Availability  
**Measurable Criteria (if provided):** ≥ 30 consecutive days without reboot due to RLCS error; daily uptime logging; alert on reboot within 30 days (alert timing not specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-001, NFR-002  
- **Conflicts with:** Not specified  
---

[NFR-032]: Redundancy to ensure uninterrupted operation  
**Description:** “The RLCS must be built with redundant capabilities to ensure uninterrupted operation.” Derived refinement per evaluator: System must continue operations with no data loss or failed commands in event of a single FCU, power supply, or network circuit failure. Owner/Next action: List specific redundancy requirements by subsystem.  
**Quality Attributes**: Availability, Resilience  
**Measurable Criteria (if provided):** Must continue operations with no data loss or failed commands after a single FCU, power supply, or network circuit failure.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-056  
- **Conflicts with:** Not specified  
---

[NFR-033]: Open architecture—modular and scalable; growth capacity  
**Description:** “The RLCS shall utilize an open architecture that is modular and scaleable… scaled up to… two additional DCU controllers… plus four additional CMS… twenty additional contact closures.”  
**Quality Attributes**: Modifiability, Scalability  
**Measurable Criteria (if provided):** Must scale to +2 DCUs (DCU1-sized), +4 CMS, +20 contact closures.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-055, NFR-022  
- **Conflicts with:** Not specified  
---

[NFR-034]: Use open systems standards wherever possible  
**Description:** “Wherever possible open systems standards for hardware, software, software development tools, and communications shall be used.” Derived refinement per evaluator: All RLCS communication and data interfaces must use industry open protocols (TCP/IP, SNMP, SQL). Owner/Next action: Map all open-stndards to subsystems/components.  
**Quality Attributes**: Portability, Interoperability  
**Measurable Criteria (if provided):** Must use TCP/IP, SNMP, and SQL for relevant communications/data interfaces (scope details not specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-055, NFR-018  
- **Conflicts with:** Not specified  
---

[NFR-035]: COTS technology preferences/constraints (DB, OS, reporting, config mgmt)  
**Description:** “data processing, security, and reporting functions… implemented with commercial off-the-shelf software… Oracle 8i… HP UX or Solaris… Windows NT or Linux… OS/9 or other real time OS… Crystal Reports/Brio… CCC/Harvest…” Derived refinement per evaluator: If listed COTS tool is unsupported, an alternative with equivalent support and capability must be selected. Owner/Next action: Clarify COTS/alternative tool policy.  
**Quality Attributes**: Portability, Maintainability (tooling), Operability  
**Measurable Criteria (if provided):** Use listed COTS tools; if unsupported, select equivalent supported alternative (equivalence criteria not specified).  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-050, FR-051  
- **Conflicts with:** Not specified  
---

[NFR-036]: Memory constraints depend on selected controller  
**Description:** “The only memory constraints imposed on the software will depend on constraints associated with the intelligent controller selected for the system.” Derived refinement per evaluator: Minimum 128MB RAM, 32MB flash required unless otherwise specified by selected controller's specification. Owner/Next action: Estimate and document baseline controller memory requirements.  
**Quality Attributes**: Resource Constraints  
**Measurable Criteria (if provided):** Minimum 128MB RAM and 32MB flash unless otherwise specified by selected controller's specification.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-055  
- **Conflicts with:** Not specified  
---