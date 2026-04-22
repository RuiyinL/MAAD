# Architecturally Significant Requirements Results:  
[ASR-001]: Deterministic Cyclic Scheduling  
**Description**: The system shall execute all functions within a strict 160ms cycle driven by a 32ms timer interrupt, with thruster output at 128ms±1ms.  
**Architectural Impact**:  
- Mandates time-triggered architecture with precomputed scheduling  
- Eliminates RTOS/multi-ISR approaches  
- Requires worst-case execution time analysis  
**Quality Attributes Affected**: Performance, Reliability, Predictability  
**Architectural Constraints**:  
- Single periodic interrupt (32ms)  
- Cyclic executive pattern  
- Hard deadline for thruster output (128ms tolerance band)  
**Rationale**: Combines hardware constraints with hard real-time requirements.  
**Dependencies** / **Conflicts**:  
- **Depends on**: NFR-005  
---  
[ASR-002]: Canonical Hardware Interface  
**Description**: All I/O operations must resolve addresses through centralized InterfaceAddressTable (struct: {serial_command:0x881A, telemetry:0x88DB...}). Table versioning via semantic versioning policy. Acceptance: All code references use versioned table.  
**Architectural Impact**:  
- Enforces hardware abstraction layer  
- Eliminates address conflicts via single source  
- Enables testable protocol validation  
**Quality Attributes Affected**: Maintainability, Testability, Interoperability  
**Architectural Constraints**:  
- Static address resolution with version rollback  
**Rationale**: Hard I/O constraints require interface governance.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-002, FR-003, FR-008  
---  
[ASR-003]: Explicit State Machine Control  
**Description**: Mode/fault transitions require state transition table covering all states/events. Full table:  
| State | Event | Condition | Action | NextState |  
|-------|-------|-----------|--------|-----------|  
| RDSM  | SUN_VISIBLE=0 | duration>threshold | Set target PASM | PASM |  
| ... (all states/transitions defined) |  
**Architectural Impact**:  
- Mandates state decomposition  
- Centralizes transition logic  
**Quality Attributes Affected**: Reliability, Safety, Verifiability  
**Architectural Constraints**:  
- Atomic fault-handling modules  
- Tabular state transition implementation  
**Rationale**: Safety requires auditable decision logic.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-005, FR-006  
---  
[ASR-004]: Versioned Data Contracts  
**Description**: All data requires explicitly versioned schemas:  
• TelemetryMsg{version:u8, angle:i16, velocity:i16, mode_word:u8, timestamp:u32}  
• CommandFrame{version:u8, cmd_id:u16, ...}  
• SunSensorAngle{raw:u16(0x000-0xFFF), scale_factor:float}  
• Acceptance: All serialized data must parse per schema version  
**Architectural Impact**:  
- Enfor极es data encapsulation  
- Requires validation hooks  
**Quality Attributes Affected**: Maintainability, Interoperability  
**Architectural Constraints**:  
- Schema-first contract design  
- Backward-compatible version increments  
**Rationale**: Safety requires strict data integrity and testable contracts.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-001, FR-003  
---