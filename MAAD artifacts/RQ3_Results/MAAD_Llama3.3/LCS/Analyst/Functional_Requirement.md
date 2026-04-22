# Functional Requirements Results:
[FR-001]: System Startup
**Description**: The RLCS software in the field shall first identify its unit when it starts, by reading the cabinet id. The RLCS software will then proceed to make sure that all the cards required in that unit are present and working properly. RLCS software will do a control system integrity check and initialize all the specified tables. If everything is OK the start up process shall not exceed 30 seconds.

**Rationale:** This requirement describes the behavior of the system during startup, which is a functional aspect.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-002]: Device Status Monitoring with Explicit Interface
**Description**: Each field device shall be polled using {Modbus TCP|RS232 ASCII}, protocol negotiated/configured per device type as listed in Appendix D; any unspecified device must have protocol defined before acceptance.

**Rationale:** This requirement describes the behavior of monitoring device status, which is a functional aspect.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-003]: Command Control with Integrity Checking
**Description**: All integrity checks for system/operator commands SHALL use SHA-256 hash with signed command payload (see MSG-INTEGRITY-001); failure SHALL log to DEVICE_COMMAND_LOG within 2 seconds.

**Rationale:** This requirement describes the behavior of command control with integrity checking, which is a functional aspect.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-004]: Safety Screening
**Description**: Each control command that is processed must be validated against the secured safety rules for the command.

**Rationale:** This requirement describes the behavior of safety screening, which is a functional aspect.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-005]: Logging with Defined Schema and Audit/Immutability
**Description**: Device Command Log entries SHALL be recorded in an append-only, cryptographically signed journal (see APPEND-ONLY-LOG-STD-001); attempted deletion/modification SHALL raise a security event.

**Rationale:** This requirement describes the behavior of logging with a defined schema and audit/immutability, which is a functional aspect.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---