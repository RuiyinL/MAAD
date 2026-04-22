# Non-Functional Requirements Results:
[NFR-001]: Network Interface Speed
**Description:** Acceptance: copy test traffic at 100 Mbit/s sustained to all interfaces; packet loss <0.01%. The interface between the CMIB, Master Correlator Control Computer, and Correlator Power Control Computer shall be Ethernet of 100 Mbits/sec or better data rate.

**Quality Attributes**: Performance, Interoperability

**Measurable Criteria (if provided):**  Ethernet 100 Mbits/sec or better; packet loss <0.01% sustained.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Network Segmentation)
- **Conflicts with:** None
---
[NFR-002]: Cabling Type
**Description:** Acceptance: All network links must use transformer coupled copper twisted pair unless a documented EMI or physical constraint is cited and approved, in which case installed cabling must provide equal or better RFI performance as measured by RFI benchmark X. The interface shall be transformer coupled copper twisted pair unless other materials are required for noise, ground isolation, or physical layout constraints.

**Quality Attributes**: Reliability, Maintainability

**Measurable Criteria (if provided):**  Transformer coupled copper twisted pair; documented exceptions with RFI benchmark validation.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** NFR-006 (RFI Shielding)
---
[NFR-003]: Network Switching
**Description:** Network switches shall be employed to reduce network wiring complexity such that the average number of cable interconnects per rack is reduced by at least 30% compared to a point-to-point baseline.

**Quality Attributes**: Maintainability, Scalability

**Measurable Criteria (if provided):**  Average number of cable interconnects per rack reduced by at least 30% compared to point-to-point baseline.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-004]: Network Segmentation
**Description:** The Master Correlator Control Computer-CMIB, Master Correlator Control Computer-Correlator Power Control Computer, and Master Correlator Control Computer-VLA Expansion Project Monitor and Control System networks shall be on separate physical interfaces.

**Quality Attributes**: Security, Reliability, Performance

**Measurable Criteria (if provided):**  Separate physical interfaces.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Network Segmentation)
- **Conflicts with:** None
---
[NFR-005]: Redundant Power Control Path
**Description:** There shall be a redundant communication path between the Master Correlator Control Computer and Correlator Power Control Computer to provide for remote reboot in the event of a networking or computing failure.

**Quality Attributes**: Reliability, Availability

**Measurable Criteria (if provided):**  Redundant communication path.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Redundant Masters)
- **Conflicts with:** None
---
[NFR-006]: RFI Shielding
**Description:** Acceptance: All cable pathways penetrating shielded room must provide <X dB RFI leakage at Y MHz to Z GHz, verified by RFI test procedure Q. Pathways penetrating the correlator shielded room shall be fiber optic or other low RFI material to meet RFI specifications.

**Quality Attributes**: Reliability, Compliance

**Measurable Criteria (if provided):**  Fiber optic or low RFI material; <X dB RFI leakage at Y MHz to Z GHz per test procedure Q.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** NFR-002 (Cabling Type)
---
[NFR-007]: Network Protection
**Description:** Network routers/switches must employ a firewall with only IP whitelisting at the Control Computer interface and generate an intrusion attempt alert within 30 seconds.

**Quality Attributes**: Security, Performance

**Measurable Criteria (if provided):**  Firewall with IP whitelisting; intrusion alert within 30 seconds.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Security Architecture)
- **Conflicts with:** None
---
[NFR-008]: CMIB Bus Interface
**Description:** Acceptance: Bus selection may include PCI/ISA or newer bus standards upon validation with integration test X. The CMIB daughter board shall communicate with the correlator carrier boards via either the PCI or ISA busses.

**Quality Attributes**: Interoperability, Portability

**Measurable Criteria (if provided):**  PCI or ISA busses; newer standards allowed with integration test X validation.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-009]: CMIB Memory
**Description:** The CMIB shall contain 64 Mbytes or greater of SDRAM.

**Quality Attributes**: Performance, Capacity

**Measurable Criteria (if provided):**  64 Mbytes or greater of SDRAM.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-010]: CMIB Operating System
**Description:** The CMIB shall have capacity to boot and run a generic COTS operating system in a near real-time environment from local non-volatile storage.

**Quality Attributes**: Performance, Portability

**Measurable Criteria (if provided):**  Near real-time environment.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Load Separation)
- **Conflicts with:** None
---
[NFR-011]: Master Computer Availability
**Description:** The Master Correlator Control Computer shall be a high availability type general- purpose computer.

**Quality Attributes**: Availability, Reliability

**Measurable Criteria (if provided):**  High availability type.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-003 (Redundant Masters)
- **Conflicts with:** None
---
[NFR-012]: Master Stand-alone Boot
**Description:** Acceptance: Standalone failover test passes post-major release or monthly, no more than 5-minute downtime, 100% config confirmed. Failover to stand-alone mode shall be tested quarterly, achieving resumption of operation within 5 minutes and with 100% config/state preservation.

**Quality Attributes**: Availability, Reliability

**Measurable Criteria (if provided):**  Tested post-major release or monthly; resumption within 5 minutes; 100% config/state preservation.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-007 (Offline Operation)
- **Conflicts with:** None
---
[NFR-013]: Processor Determinism
**Description:** The Correlator Monitor and Control System processors shall be capable of responding to correlator hardware inputs in a deterministic fashion with sufficient performance to avoid data loss, corruption or overflows.

**Quality Attributes**: Performance, Reliability

**Measurable Criteria (if provided):**  Deterministic fashion, avoid data loss/corruption/overflows.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-004 (Load Separation)
- **Conflicts with:** None
---
[NFR-014]: Message Timestamping
**Description:** All messages passed between Correlator Monitor and Control System system layers shall have both UTC and wall clock time stamp information appropriate for the message type.

**Quality Attributes**: Observability, Traceability

**Measurable Criteria (if provided):**  UTC and wall clock time stamp.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-015]: Software Stability
**Description:** System must achieve MTBF of 30 days or longer without requiring restart, except for scheduled maintenance.

**Quality Attributes**: Reliability, Availability

**Measurable Criteria (if provided):**  MTBF of 30 days or longer.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-016]: Hardware Service Life
**Description:** Availability = ((total uptime - scheduled downtime)/total time). Alert if <99.99% in rolling 30d. System hardware shall achieve 99.99% annual availability, excluding scheduled outages and total power loss events.

**Quality Attributes**: Availability, Reliability

**Measurable Criteria (if provided):**  99.99% annual availability; alert if <99.99% in rolling 30d.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-009 (Watchdog/UPS Integration)
- **Conflicts with:** None
---
[NFR-017]: Hardware Expandability
**Description:** Acceptance: System support validated for up to eight CMIB adds per year with <= 5 min downtime each; further addition triggers review. Event log records duration of each CMIB addition; alert if downtime >5 min. The system shall support hot addition of at least two additional CMIB modules per year without more than 5 minutes of downtime per event.

**Quality Attributes**: Scalability, Maintainability

**Measurable Criteria (if provided):**  Hot addition of up to eight CMIB modules per year; <= 5 minutes downtime per event; alert if >5 min; further additions trigger review.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-018]: Security Authentication
**Description:** Quarterly audit: 100% of user accounts meet NIST 800-63B; failed audit triggers SRE escalation. All user passwords must meet NIST 800-63B minimum standards and expire every 90 days; all authentication traffic must be encrypted in transit.

**Quality Attributes**: Security

**Measurable Criteria (if provided):**  NIST 800-63B standards; 90-day expiration; encryption in transit; quarterly audit 100% compliance.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-008 (Security Architecture)
- **Conflicts with:** None
---
[NFR-019]: Privilege Control
**Description:** Each user shall have a set of system access properties that defines the user's privileges within the EVLA Correlator Monitor and Control System.

**Quality Attributes**: Security

**Measurable Criteria (if provided):**  Set of system access properties per user.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-021 (User Management)
- **Conflicts with:** None
---
[NFR-020]: Modular Replaceability
**Description:** Acceptance: List in doc Z updated per hardware inventory review, N=all critical devices. Critical devices: [CMIB, Power Control, Network Interface]; hot swap log shows <10 min downtime per device, 90% coverage per year. At least 90% of critical devices shall be hot-swappable and replaceable with no more than 10 minutes downtime per replacement.

**Quality Attributes**: Maintainability, Availability

**Measurable Criteria (if provided):**  90% of critical devices hot-swappable; <= 10 minutes downtime per replacement; logged per event; list updated per hardware inventory review.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Autonomous Recovery)
- **Conflicts with:** None
---
[NFR-021]: Documentation
**Description:** Acceptance: Passes onboarding checklist Q with median completion under 2h (N=3 new hires) per release. Acceptance: All docs pass automated markdown link check and linter on every git push. All documentation shall be provided as Markdown in a central Git repository, updated within 7 days of each software release, and pass onboarding usability testing.

**Quality Attributes**: Maintainability, Usability

**Measurable Criteria (if provided):**  Markdown in Git; updated within 7 days of release; pass onboarding testing; median completion under 2h; automated link check and linter on every git push.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---