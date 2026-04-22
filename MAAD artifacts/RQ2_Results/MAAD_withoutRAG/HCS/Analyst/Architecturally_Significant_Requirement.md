# Architecturally Significant Requirements Results

[ASR-001]: Two-tier on-prem topology: Home web server + Gateway master control  
**Description**:  
- “A DigitalHome System shall have the capability to establish an individual home web server hosted on a home computer.”  
- “The communication center of the DigitalHome system shall be a DigitalHome home web server…”  
- “Each DigitalHome shall contain a master control device (the DigitalHome Gateway Device) that connects to the home’s broadband Internet connection, and uses wireless communication…”  
**Architectural Impact:**  
Forces a decomposition into at least two major runtime nodes: (1) HomeWebServer for UI/API, accounts, storage, reporting, backups; (2) Gateway for RF communications, device acquisition, and command/control bridging to broadband/LAN. Drives network topology, deployment, interface design, and fault boundaries.  
**Quality Attributes Affected:** Availability, Reliability, Security, Performance, Deployability  
**Architectural Constraints:** Must include HomeWebServer on a home computer and a Gateway master control device; gateway mediates wireless device comms and broadband connectivity.  
**Rationale:** Strong structural constraint on system decomposition and deployment; cross-cuts most features.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, FR-005, NFR-009
- **Conflicts with:** NFR-010
---

[ASR-002]: Near-real-time telemetry and UI freshness (10 Hz acquisition; ≤2s update)  
**Description**:  
- “Sensor… shall have a minimum data acquisition rate of 10 Hz.”  
- “Displays… shall be updated at least every two seconds.”  
Acceptance criteria: “99% of update intervals ≤2s (UI views), and sensor feed acquisition rate ≥10 Hz in presence of N devices; system must generate ops alert if more than 1% of intervals exceed 2.5s or 10Hz consistently missed.”  
Expose metrics: ui_refresh_interval_secs (histogram, p99, p99.9); sensor_acquisition_rate_hz (per device, moving window of 60s). Alert: ops_alert_ui_stale if >1% of intervals exceed 2.5s in 15min window; ops_alert_sensor_lag if any sensor falls <10Hz for >1min.  
(Next action: Amend ASR-002 and NFR-001/002 with precise metric and alert design.)  
**Architectural Impact:**  
Drives eventing/streaming vs naive request/response polling; requires a telemetry ingestion pipeline, buffering, persistence strategy, and potentially push-based UI updates (e.g., streaming) to meet freshness under load. Impacts CPU/network sizing and scheduling on gateway/server.  
**Quality Attributes Affected:** Performance, Scalability, Responsiveness  
**Architectural Constraints:** Must sustain ≥10 Hz per sensor for acquisition and ensure UI condition views refresh ≤2 seconds; must define and expose observability metrics and alerts for freshness and acquisition compliance.  
**Rationale:** Quantified performance constraints that shape dataflow architecture end-to-end; requires measurable operational validation and alerting.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-006, FR-001, FR-002
- **Conflicts with:** NFR-010, NFR-008 (encryption overhead)
---

[ASR-003]: Wireless RF communications with 1000-foot indoor range  
**Description**:  
- “The Gateway shall contain an RF Module…”  
- “The Gateway device shall operate up to a 1000-foot range for indoor transmission.”  
**Architectural Impact:**  
Constrain wireless technology choice, gateway hardware capability, and network protocol design (message reliability, retries, addressing). Affects placement assumptions and error handling for out-of-range devices.  
**Quality Attributes Affected:** Connectivity, Reliability, Performance  
**Architectural Constraints:** Must include RF module and support indoor range up to 1000 feet; all devices must communicate through gateway within this range.  
**Rationale:** Hardware/communication constraint with broad architectural consequences.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005
- **Conflicts with:** NFR-010
---

[ASR-004]: High reliability target (≤1 failure per 10,000 operating hours)  
**Description**: “The DigitalHome System must be highly reliable with no more than 1 failure per 10,000 hours of operation.”  
**Architectural Impact:**  
Necessitates resilience patterns (watchdogs/health checks, fault detection, graceful degradation), robust state management, and operational monitoring to define/measure “failure” and prevent cascading faults across gateway/server/UI. Influences component boundaries and recovery strategy.  
**Quality Attributes Affected:** Reliability, Availability, Safety (risk mitigation)  
**Architectural Constraints:** Architecture must support meeting the quantified failure-rate target across integrated subsystems.  
**Rationale:** A stringent quantified reliability target; cross-cutting and high risk.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-006, NFR-005, NFR-006
- **Conflicts with:** NFR-010, NFR-011
---

[ASR-005]: Backup and recovery mechanisms (daily backup; restore-from-latest)  
**Description**:  
- “The Digital Home System shall incorporate backup and recovery mechanisms.”  
- “...backup all system data… on a daily basis…”  
- “...recovery mechanism shall restore system data… from the most recent backup.”  
**Architectural Impact:**  
Forces explicit persistence architecture (what data is “system data”), backup orchestration, storage location/format, consistency strategy, and recovery workflows integrated into operations. Impacts database choice and deployment.  
**Quality Attributes Affected:** Recoverability, Reliability, Data Integrity  
**Architectural Constraints:** Must implement daily backups for configuration/defaults/plans/usage data and automated/defined restoration from the most recent backup.  
**Rationale:** Cross-cutting operational capability affecting storage, deployment, and runtime services.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-034
- **Conflicts with:** NFR-010
---

[ASR-006]: Web security: authentication and encryption (e.g., TLS)  
**Description**: “The DigitalHome web system shall provide for authentication and information encryption… such as Transport Layer Security. All authentication and configuration change events (user id, timestamp, action) shall be logged and made available for compliance review for at least 1 year. Acceptance: 99% of auth/config changes appear in audit log within 5s; logs retained ≥1y; random event spot checks pass. Schema: {event_id, user_id, action_type, entity, timestamp, result}; SLO: 99% of events ingested/displayed in ops tool within ≤5s. Review: monthly admin audit with 5% event sampling.” (Next action: Update ASR-006 with audit log schema, performance SLO and review/validation steps.)  
**Architectural Impact:**  
Imposes security architecture for identity/authentication flows, credential storage, session management, and encrypted transport for UI/API access. Affects component interfaces (web server, clients), remote access design, and certificate/key management.  
**Quality Attributes Affected:** Security, Privacy, Compliance, Performance  
**Architectural Constraints:** Must provide authentication and encrypted communications for the web system; requires adoption of a recognized secure transport mechanism (e.g., TLS); must implement audit logging for authentication and configuration change events retained ≥1 year with verifiable ingestion latency (≤5s for 99% of events) and periodic spot checks.  
**Rationale:** Cross-cutting security requirement with broad architectural implications; adds measurable audit-trail acceptance criteria.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, FR-032, FR-033, FR-034
- **Conflicts with:** ASR-002 (timing), NFR-010 (cost)
---

[ASR-007]: Multi-role access and configuration control (General vs Master vs Technician)  
**Description**:  
- “A Master user… shall be able to change the configuration of the system…”  
- “A DigitalHome Technician… [has] rights beyond the… General User… starting and stopping operation…”  
**Architectural Impact:**  
Requires role-based access control (RBAC), privilege separation, admin workflows, and potentially auditability of configuration changes. Influences API authorization, UI design, and data model for accounts/roles.  
**Quality Attributes Affected:** Security, Maintainability, Operability  
**Architectural Constraints:** Must support distinct roles with differentiated permissions for configuration and operations.  
**Rationale:** Cross-cutting authorization model affecting most modules and endpoints.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-033, FR-034, NFR-008
- **Conflicts with:** Not identified
---

[ASR-008]: System must be testable in a realistic simulated environment  
**Description**:  
- “The DigitalHome system will be tested in a simulated environment.”  
- “...simulated environment will be realistic and adhere to the physical properties and constraints of an actual home and to real sensors and controllers. Simulated environment tests must cover 95%+ of functional cases, and inject at least 10 types of sensor failure conditions, measured by Jenkins CI pipeline. Test plan must document: [loss, outlier, stuck-at, drift, CRC error, delayed, intermittent drop, duplicate, spike, malformed, unauthorized device].”  
(Next action: Update ASR-008 test plan and CI scripts with explicit list and mappings.)  
**Architectural Impact:**  
Forces design-for-testability: abstraction around hardware I/O, simulators/stubs for sensors/controllers and network conditions, and repeatable end-to-end test harnesses. Strongly affects how device integrations are implemented.  
**Quality Attributes Affected:** Testability, Maintainability, Reliability (verification)  
**Architectural Constraints:** Must support full-system operation and testing against a simulation that emulates real home/device constraints; automated simulation tests must reach 95%+ functional case coverage and include ≥10 sensor failure condition types executed in Jenkins CI.  
**Rationale:** A major verification constraint that shapes integration architecture and interfaces.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-004, FR-005, FR-006
- **Conflicts with:** NFR-011, NFR-010
---

[ASR-009]: Standards and compatibility constraints for HVAC (ASHRAE 2010; multiple HVAC types)  
**Description**:  
- “The system shall be compatible with a centralized HVAC… gas, oil, electricity, solar…”  
- “The system shall adhere to… [ASHRAE 2010].”  
**Architectural Impact:**  
Constrains device integration interfaces, thermostat control logic assumptions, and potentially certification/compliance documentation. May influence plugin/adaptor patterns for different HVAC configurations.  
**Quality Attributes Affected:** Compatibility, Compliance, Maintainability  
**Architectural Constraints:** Must support enumerated HVAC types and conform to ASHRAE 2010 practices/policies/procedures.  
**Rationale:** External compliance/compatibility constraints that shape integration architecture.  
**Dependencies** / **Conflicts**:
- **Depends on:** FR-007..FR-013
- **Conflicts with:** NFR-010
---

[ASR-010]: Prototype must be evolvable into commercial product  
**Description**: “Although the product produced under this document will be a ‘prototype’ version, all modules and components of this prototype version shall be designed and implemented in such a manner that it may be incorporated in a fully specified commercial version of the DigitalHome System. All modules must expose interfaces documented in UML 2.0, and separation-of-concerns shall be reviewed in code walkthroughs. Acceptance: 99% of modules reviewed for interface UML/SoC prior to release; sample code audit reports attached to closure docs.” (Next action: State measurable/compliance step for evolvability in ASR-010.)  
**Architectural Impact:**  
Drives modularity, clean interfaces, separation of concerns, and avoidance of hard-coded prototype shortcuts that block scaling or hardening. Influences layering, plugin boundaries, and maintainability choices.  
**Quality Attributes Affected:** Modifiability, Maintainability, Scalability (future-proofing)  
**Architectural Constraints:** Prototype modules/components must be designed for reuse/incorporation into a future commercial system; module interfaces must be documented in UML 2.0; separation-of-concerns must be reviewed in code walkthroughs; ≥99% of modules must undergo such review before release with audit evidence attached.  
**Rationale:** Long-term structural constraint influencing architecture more than individual features, now with measurable compliance gates.  
**Dependencies** / **Conflicts**:
- **Depends on:** NFR-011 (time-box), NFR-012 (standards)
- **Conflicts with:** NFR-011 (schedule pressure), NFR-010 (cost pressure)
---