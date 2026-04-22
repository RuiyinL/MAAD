# Architecturally Significant Requirements Results:

[ASR-001]: Safety-critical interlocks to prevent wrong-way openings and catastrophic gate conditions  
**Description**: “The risk is the possibility of opening an entrance for one direction of travel, with one or more entrances already open in the opposite direction… catastrophic… The control system must not attempt to open any entrance closure device, if the status of any opposite direction entrance closure device is ‘unknown’ or open’… Safety screening … multi-layered … applied … at originating control unit… subordinate control units… just prior to actual command execution.” Derived refinement per evaluator: All control units must execute and log safety screening for every command; a daily integrity/consistency test confirms identical rules/logic/versions systemwide. Owner/Next action: Add systemwide periodic ruleset validation and specify test protocol.  
**Architectural Impact:**  
Requires deterministic sequencing/state machines and multi-layer safety screening implemented across distributed control units (TSU/FCU/DCU), with consistent replicated rule sets and consistent device state distribution. Drives command validation pipelines, abort semantics, and safety-rule storage/execution near devices.  
**Quality Attributes Affected:** Safety, Reliability, Performance  
**Architectural Constraints:**  
- Multi-layer safety screening at all command hops and at executing controller  
- Abort/halt behavior on unsafe/unknown states  
- Safety rules stored in non-volatile memory at control units  
**Rationale:** Catastrophic risk + cross-cutting effect on all control flows; dominates architecture and test strategy.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-041, FR-039, FR-034, FR-053  
- **Conflicts with:** FR-036 (override) unless constrained/limited  
---

[ASR-002]: Hierarchical distributed control architecture (TSU > FCU > DCU) with superior-to-inferior command forwarding  
**Description**: “Commands are only forwarded from superior units to inferior ones… The TSU is superior to the FCUs which are superior to the DCUs.”  
**Architectural Impact:**  
Forces a tiered command-routing model, authority boundaries, and conflict resolution. Requires clear ownership of devices, message routing, and state synchronization across tiers.  
**Quality Attributes Affected:** Safety, Security, Reliability  
**Architectural Constraints:**  
- Enforce command routing directionality and authorization by tier  
- Prevent peer/lower units from changing higher-controlled device states  
**Rationale:** Strong structural constraint on component decomposition and communications patterns.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-042, FR-041  
- **Conflicts with:** Not specified  
---

[ASR-003]: Tight end-to-end telemetry freshness and UI latency targets (2 seconds)  
**Description**: “Status… updated every 2 seconds… Any change in device state… on the screen not later than 2 seconds… critical alarms … within 2 seconds… controllers … send status … every 2 seconds or less… detect alarm conditions within 2 seconds…”  
**Architectural Impact:**  
Requires event-driven/push or high-frequency polling architecture, efficient messaging, prioritization, and bounded-latency pipelines from sensor to DB to GUI. Affects threading model, transport selection, buffering, and backpressure strategy.  
**Quality Attributes Affected:** Performance, Safety, Availability  
**Architectural Constraints:**  
- Support 2s update/notification loops under normal and degraded modes  
- Ensure DB/update path does not violate UI/monitoring deadlines  
**Rationale:** Unusually strict real-time-ish requirements across distributed components.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006, NFR-007, NFR-011, NFR-028  
- **Conflicts with:** NFR-008 (configurable slower monitoring) if set too high for safety  
---

[ASR-004]: High availability, redundancy, and degraded-mode operation with alternate control points  
**Description**: “must be available 24/7… recovery time… no greater than 10 minutes… built with redundant capabilities… degraded mode… alternate control at FCU… dial in… if FCUs fail… direct control at DCUs… laptops… manual control…”  
**Architectural Impact:**  
Drives redundancy design, failover strategies, role of FCUs as backup control planes, remote-access architecture, and operational runbooks. Requires separation of concerns between monitoring, control authority, and local autonomy at controllers.  
**Quality Attributes Affected:** Availability, Reliability, Safety  
**Architectural Constraints:**  
- Provide alternate control paths (TMC→FCU→DCU) and remote dial-in  
- Support manual fallback modes without corrupting system state  
- Achieve RTO ≤ 10 minutes  
**Rationale:** Cross-cutting resilience requirement affecting deployment topology, communications, and controller autonomy.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-056, NFR-001, NFR-002, NFR-032  
- **Conflicts with:** FR-005 (specified workstations) unless aligned with failover endpoints  
---

[ASR-005]: External one-way data export via firewall to external server (every 30 seconds) + one-way serial link  
**Description**: “one way data transfer to a computer outside of the RLCS network… every 30 seconds… one way serial data transfer… The Reversible Lane Control System does not accept or process any input from other systems.”  
**Architectural Impact:**  
Requires a secure data publishing boundary (DMZ/external server datastore), strict unidirectional interfaces (data diode pattern or firewall rules), and a defined export schema/versioning. Prevents any inbound integration paths.  
**Quality Attributes Affected:** Security, Interoperability, Availability  
**Architectural Constraints:**  
- Outbound-only interface for external systems  
- Export cadence 30 seconds  
- No inbound commands/inputs from external systems  
**Rationale:** Strong interface/security boundary shaping network zones and integration design.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-029, FR-030, NFR-005  
- **Conflicts with:** Not specified  
---

[ASR-006]: Controller/hardware abstraction via I/O driver software; support multiple possible controllers (e.g., 2070 ATC)  
**Description**: “software shall send to and receive data from the field device I/O cards through I/O driver software… controller … replaced with … 2070 ATC … or equal… unknown… which controller will be used… software must interface with whichever controller is chosen…”  
**Architectural Impact:**  
Forces a pluggable HardwareIO/driver abstraction and integration contracts; requires simulation harnesses and device adapter modules to decouple application logic from specific controller hardware.  
**Quality Attributes Affected:** Modifiability, Portability, Testability, Reliability  
**Architectural Constraints:**  
- Use driver-based interface to I/O cards/controllers  
- Support controller substitution without rewriting core logic  
**Rationale:** High integration risk and pervasive impact on control/monitoring modules.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-054, FR-055, NFR-036  
- **Conflicts with:** Not specified  
---

[ASR-007]: Integrity protection of controller non-volatile code/data using hash verification (MD5 specified)  
**Description**: “The system shall … employ a one-way hash function… MD5 algorithm is acceptable… verification at least once a day… results recorded… failure causes alarm… prevent affected unit from being used in control sequences… hash function… used to encrypt user passwords.” Derived refinement per evaluator: All integrity validations and password storage must use SHA-256 or stronger cryptographic hash functions; MD5 is not permitted. Owner/Next action: Update all references to MD5 to require a secure, industry-approved algorithm.  
**Architectural Impact:**  
Introduces a platform-wide integrity subsystem (digest generation, storage, verification scheduler, alarm integration, and enforcement hooks that disable units). Also affects credential storage/auth flows.  
**Quality Attributes Affected:** Security (integrity), Safety, Availability  
**Architectural Constraints:**  
- Digest tables stored in non-volatile memory per unit  
- Daily verification and operator-triggered verification  
- Block unit from participating in control sequences on failure  
- MD5 specified (legacy)  
**Rationale:** Cross-cutting security/safety mechanism with operational enforcement impacts; potential conflict with modern crypto standards.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-052, FR-047, NFR-013  
- **Conflicts with:** NFR-015 (security best practices; MD5 weakness)  
---

[ASR-008]: Single-operator command-control and workstation-based authorization constraints  
**Description**: “Only one ‘operator’ may be logged onto the system at any given time.” / “Command control shall be from only specified workstations.” / takeover rules for higher-security users.  
**Architectural Impact:**  
Requires a centralized or distributed lock/lease mechanism for command authority, consistent enforcement across nodes (TMC/FCU/DCU), session management, and audit trails for control transfer.  
**Quality Attributes Affected:** Safety, Security, Usability  
**Architectural Constraints:**  
- Enforce single active operator command authority at a time  
- Enforce workstation allow-lists for command control  
- Support secure takeover workflow and notification  
**Rationale:** Cross-cutting constraint on authentication/authorization, UI flows, and distributed coordination.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004, FR-005, FR-006, NFR-016  
- **Conflicts with:** NFR-023 (multi-user support) unless role separation clarified  
---

[ASR-009]: COTS platform constraints for DBMS/reporting/OS and separation of reporting workload  
**Description**: “A commercial off-the-shelf database management system shall be used…” / “COTS reporting tool…” / technology preferences (Oracle 8i; HP-UX/Solaris; Windows NT/Linux; OS/9; Crystal Reports/Brio) and “Report processing shall not impact any other performance requirements…”  
**Architectural Impact:**  
Constrains technology stack and requires architectural separation/isolation of reporting workloads (e.g., extracts, replicas, dedicated resources) to prevent interference with control/monitoring latency SLOs.  
**Quality Attributes Affected:** Performance, Maintainability, Operability  
**Architectural Constraints:**  
- Use COTS DBMS and reporting tool  
- Ensure reporting does not degrade monitoring/control/UI response requirements  
**Rationale:** Major technology and performance isolation constraints affecting deployment and data architecture.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-050, FR-051, NFR-024, NFR-025  
- **Conflicts with:** Not specified  
---

[ASR-010]: Modular, scalable, open-standards architecture with specified growth capacity  
**Description**: “open architecture… modular and scaleable… scaled up to… two additional DCU controllers… plus four additional CMS, and … twenty additional contact closures… Wherever possible open systems standards… The RLCS software shall be designed to allow for future changes… without requiring programming effort.”  
**Architectural Impact:**  
Requires modular decomposition, configuration-driven device/map models, schema-driven UI, and extensible device catalogs. Influences plugin boundaries and configuration management/versioning.  
**Quality Attributes Affected:** Modifiability, Scalability, Portability  
**Architectural Constraints:**  
- Must scale to the stated additional controllers/devices  
- Prefer open standards for interfaces and tooling  
- Roadway/device changes should be achievable via configuration, not code  
**Rationale:** Strong architectural direction impacting componentization and configuration strategy.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-033, NFR-034, NFR-022, FR-022, FR-023  
- **Conflicts with:** NFR-021 (single-release delivery may constrain incremental modular rollout)  
---