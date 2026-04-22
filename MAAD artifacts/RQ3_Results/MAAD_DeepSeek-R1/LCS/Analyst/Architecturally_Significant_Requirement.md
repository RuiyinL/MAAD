# Architecturally Significant Requirements Results:
[ASR-001]: Fault-Tolerant Operation  
**Description**: System must complete failover to redundant FCU/DCU or manual fallback within ≤10 minutes in 95% of cases, as proven during quarterly drills.  
**Architectural Impact:** Mandates drill-validated failover procedures.  
**Quality Attributes Affected:** Reliability, Availability  
**Architectural Constraints:** Quarterly failover validation drills.  
**Rationale:** Critical for 24/7 traffic management with catastrophic safety risks during downtime.  
**Dependencies / Conflicts**:  
- **Depends on:** NFR-001  
---  

[ASR-002]: Controller Integrity Enforcement  
**Description**: On hash verification failure, controller disables commands, logs event (ID, timestamp, operator IDs, reason), requires two separate admin logins to override.  
**Architectural Impact:** Requires atomic safe-mode transition and dual-auth protocols.  
**Quality Attributes Affected:** Security, Safety, Integrity  
**Architectural Constraints:** 5-second safe-mode enforcement, dual-auth override.  
**Rationale:** Prevents catastrophic control system compromise due to corrupted/malicious code.  
**Dependencies / Conflicts**:  
- **Depends on:** NFR-002  
---  

[ASR-003]: Hierarchical Command Routing  
**Description**: All nodes sync with <NTP-server-list>; on drift >150 ms trigger 'ClockSyncAlert' to operator and log event; lock TTL <= 1s strictly enforced.  
**Architectural Impact:** Enforces time-synchronized distributed locking with failure alerts.  
**Quality Attributes Affected:** Safety, Reliability  
**Architectural Constraints:** NTP clock sync, lock contention alerts.  
**Rationale:** Eliminates race conditions and prevents conflicting commands.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-001A  
---  

[ASR-004]: Safety Interlock Implementation  
**Description**: For any command rejected by any safety screen: all related DB/field writes are undone atomically; 'SafetyRollbackEvent' is logged within 2s, operator notified.  
**Architectural Impact:** Requires atomic rollback and alerting mechanisms.  
**Quality Attributes Affected:** Safety, Reliability  
**Architectural Constraints:** Multi-layer rollback, sub-2s alerting.  
**Rationale:** Mitigates catastrophic risks from unsafe command execution.  
**Dependencies / Conflicts**:  
- **Depends on:** FR-005  
---  

[ASR-005]: External Data Egress  
**Description**: Each external data egress (status, report, bulk export) is logged per ASR-005, and monthly audits include failed transmissions and SIEM alerts.  
**Architectural Impact:** Demands comprehensive egress monitoring and SIEM integration.  
**Quality Attributes Affected:** Security  
**Architectural Constraints:** Monthly SIEM audit reports.  
**Rationale:** Enforces security boundary and traceability for external data.  
**Dependencies / Conflicts**:  
- **Conflicts with:** High-frequency data requirements  
---