# Architecturally Significant Requirements Results:
[ASR-001]: Home Web Server as Central Hub  
**Description**: The communication center of the DigitalHome system shall be a DigitalHome home web server, through which a user shall be able to monitor and control home devices and systems.  
**Architectural Impact**:  
Mandates a centralized web-server component for UI, control logic, and data storage, driving modular decomposition (e.g., UI layer, business logic APIs). Requires HTTP interfaces and influences technology choices (web frameworks, security protocols).  
**Quality Attributes Affected**:  
Scalability, Security, Usability  
**Architectural Constraints**:  
Must implement web-server capabilities (account management, real-time UI updates, database storage).  
**Rationale**:  
Foundation for user interactions; constrains decomposition; high risk if performance/security not addressed.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-006, NFR-009  
- **Conflicts with:** NFR-002 (cost minimization)  
---  
[ASR-002]: Wireless Gateway Communication  
**Description**: Gateway must support IEEE 802.15.4 (Zigbee) protocol at 2.4GHz.  
**Architectural Impact**:  
Requires RF communication module; constrains protocols (e.g., Zigbee/Z-Wave); impacts data flow patterns and adapter design for device integration. Limits physical component placement.  
**Quality Attributes Affected**:  
Interoperability, Performance  
**Architectural Constraints**:  
Must implement RF module with ≤1000ft range; define message schemas for sensor/controller data.  
**Rationale**:  
Hardware constraint with software implications; high business value for device compatibility.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-003  
- **Conflicts with:** None  
---  
[ASR-003]: Strict Reliability Metric  
**Description**: Failure event: {timestamp, event_type, impact_duration, affected_component, recovery_action}. Alert if >1 event/10,000 hours per deployment.  
**Architectural Impact**:  
Drives redundancy in critical components; mandates fault-tolerant design (e.g., watchdog timers, transaction rollbacks). Requires logging/monitoring hooks for SLO validation.  
**Quality Attributes Affected**:  
Reliability, Availability, Maintainability  
**Architectural Constraints**:  
Must implement backup/recovery modules and real-time health checks; constrains deployment topology.  
**Rationale**:  
Quantitative quality goal forces specific patterns; cross-cutting mechanism impacts all components.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-004, NFR-010  
- **Conflicts with:** NFR-002 (cost minimization)  
---  
[ASR-004]: High-Frequency Data Processing  
**Description**: Sensor buffers may lose no more than 1% packets per 1 hour; lag from sensor to UI <2s 99% of the time. Metric: sensor.packet_loss_rate (window: 1h, alert if >1%); Metric: sensor_to_ui.lag_ms (window: 24h, alert P99 >2s).  
**Architectural Impact**:  
Requires push-based communication (WebSocket/SSE) to meet UI freshness; forces buffering/stream-processing for sensor data at 10Hz; constrains database write-throughput.  
**Quality Attributes Affected**:  
Performance, Responsiveness  
**Architectural Constraints**:  
Asynchronous messaging; real-time processing modules; optimized storage for telemetry.  
**Rationale**:  
Extreme performance requirements for prototype; influences communication patterns and scalability.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-005, NFR-006  
- **Conflicts with:** ASR-003 (reliability under load)  
---  
[ASR-005]: Security and Compliance  
**Description**: Authentication and transport security must use TLS 1.3+, AES-256, salted SHA-256 for passwords, audit all access per NFR-009.  
**Architectural Impact**:  
Mandates security layers (TLS, password policies, audit logs); forces compliance checks in HVAC control logic; selects encryption libraries.  
**Quality Attributes Affected**:  
Security, Compliance  
**Architectural Constraints**:  
Strong authN/authZ; encrypted data in transit; standards-adherent APIs.  
**Rationale**:  
Cross-cutting concerns affecting all components; high-risk area without explicit constraints.  
**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008, NFR-009  
- **Conflicts with:** NFR-002 (implementation cost)  
---  
[ASR-006]: Prototype-to-Commercial Extensibility  
**Description**: ≥80% coverage applies for UI (Istanbul), backend (pytest-cov), and device subsystems, with CI report uploaded to pipeline.  
**Architectural Impact**:  
Imposes modular-monolith (hexagonal) architecture; requires clear interfaces (OpenAPI/ProtoDB) and constrained tech stack for portability.  
**Quality Attributes Affected**:  
Maintainability, Extensibility  
**Architectural Constraints**:  
Adapter patterns; contract-first development; separation of core logic from devices/simulation.  
**Rationale**:  
Business-critical for evolution; trade-off between prototype agility and commercial readiness.  
**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-001, ASR-004  
- **Conflicts with:** NFR-001 (simulation vs. real device duality)  
---