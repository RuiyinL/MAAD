# Functional Requirements Results:
[FR-001A]: User Command Control Request  
**Description**: User requests command-control.  
**Rationale:** Part of command control workflow. Derived from FR-001.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-002  
---  

[FR-001B]: Command Control Grant with Approval  
**Description**: System grants/requires approval if higher-security user requests it.  
**Rationale:** Part of command control workflow. Derived from FR-001.  
**极速赛车开奖直播官网Dependencies / Conflicts**:  
- **Depends on:** FR-001A, FR-002  
---  

[FR-001C]: Command Control Handover Feedback  
**Description**: Explicit UI feedback shown for command handover and logging.  
**Rationale:** Part of command control workflow. Derived from FR-001.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-001A, FR-001B  
---  

[FR-002]: User Authentication  
**Description**: Acceptance: 5 failed login attempts/10min causes 30min lockout; first login with existing MD5 upgrades password to SHA-256.  
**Rationale:** Defines authentication input behavior.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-015  
---  

[FR-003]: Real-time Status Display  
**Description**: The GUI shall indicate the current date and time, user’s name, and workstation location name. Status information shall continually be updated every 2 seconds.  
**Rationale:** Specifies real-time status output behavior.  
**Dependencies / Conflicts**:  
- **Depends on:** NFR-004  
---  

[FR-004]: Device Override Handling  
**Description**: When a device status has been overridden, on the screen it shall appear with different color from the normal and alarm status colors.  
**Rationale:** Defines visual feedback for manual overrides.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-003  
---  

[FR-005]: Safety Rule Validation  
**Description**: Safety rules must conform to SafetyRule.schema.json v1.0; changes require dual-admin signoff and validated SHA-256 signature.  
**Rationale:** Describes safety-critical input validation logic.  
**Dependencies / Conflicts**:  
- **Depends on:** ASR-003  
---  

[FR-006]: Operational Sequence Execution  
**Description**: The RLCS shall execute stored operational control command sequences based on the current system mode of operation and the schedule for each sequence.  
**Rationale:** Specifies sequenced command processing behavior.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-005  
---  

[FR-007]: Alarm Management  
**Description**: For alarm status, the GUI shall issue an audible alarm, and the icon shall change color. The alarm icon shall revert automatically when the condition is removed.  
**Rationale:** Defines alarm notification and resolution behavior.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-003  
---  

[FR-008]: Configuration Management  
**Description**: Any config change must write to ConfigChangeLog (id, author1/2, old/new values, reason, timestamp, rollback ref); rollback also dual-auth.  
**Rationale:** Describes privileged configuration workflows.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-002  
---  

[FR-009]: Report Generation  
**Description**: The system shall generate reports including "Current User Report", "Event Log Report", "极速赛车开奖直播官网Safety Report", and "Operations and Maintenance Report" based on configurable parameters.  
**Rationale:** Specifies reporting functionality.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-008  
---  

[FR-010]: Device Monitoring  
**Description**: DeviceStatusEvent includes schema_version and for system-initiated events, operator_id is set to SYSTEM.  
**Rationale:** Defines real-time device monitoring behavior.  
**Dependencies / Conflicts**:  
- **Depends on:** NFR-004  
---