# Architecturally Significant Requirements Results:
[ASR-001]: Real-time Data Processing
**Description**: Measure time between event detection (DB write) and nurses' UI 'ack' action logged, using synchronized NTP clock.
**Architectural Impact:**  This requirement influences the choice of architecture, specifically the need for a real-time data processing system.
**Quality Attributes Affected:**  Performance, Reliability, Availability
**Architectural Constraints:**  The system must be able to handle high volumes of data in real-time, with minimal latency and maximum reliability.
**Rationale:**  This requirement is architecturally significant because it imposes strong constraints on the design, specifically the need for a real-time data processing system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[ASR-002]: Secure Data Storage
**Description**: Encryption: AES-256-GCM with 12-month key rotation; RBAC roles: user, admin, auditor.
**Architectural Impact:**  This requirement influences the choice of architecture, specifically the need for secure data storage and transmission.
**Quality Attributes Affected:**  Security, Reliability
**Architectural Constraints:**  The system must use secure protocols for data transmission and storage, such as encryption and access controls.
**Rationale:**  This requirement is architecturally significant because it imposes strong constraints on the design, specifically the need for secure data storage and transmission.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-003
- **Conflicts with:** None
---
[ASR-003]: Scalable Architecture
**Description**: SLI: time from DB insert to UI render; 95th percentile under 2s in a 10-min rolling window.
**Architectural Impact:**  This requirement influences the choice of architecture, specifically the need for a scalable system.
**Quality Attributes Affected:**  Scalability, Performance, Reliability
**Architectural Constraints:**  The system must be designed to handle increasing loads and scale accordingly, with minimal impact on performance and reliability.
**Rationale:**  This requirement is architecturally significant because it imposes strong constraints on the design, specifically the need for a scalable system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[ASR-004]: Fault Tolerant System
**Description**: Recovery clock starts at node loss; ends at restored ≥80% capacity and all services healthy by SLO dashboard.
**Architectural Impact:**  This requirement influences the choice of architecture, specifically the need for a fault-tolerant system.
**Quality Attributes Affected:**  Reliability, Availability
**Architectural Constraints:**  The system must be designed to detect and recover from failures, with minimal impact on availability and reliability.
**Rationale:**  This requirement is architecturally significant because it imposes strong constraints on the design, specifically the need for a fault-tolerant system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---
[ASR-005]: Real-time Notification
**Description**: Start: out-of-range data persisted; Stop: UI alert visible; time capped at 2s; measured using NTP-synced logs.
**Architectural Impact:**  This requirement influences the choice of architecture, specifically the need for a real-time notification system.
**Quality Attributes Affected:**  Performance, Reliability, Availability
**Architectural Constraints:**  The system must be able to provide real-time notifications, with minimal latency and maximum reliability.
**Rationale:**  This requirement is architecturally significant because it imposes strong constraints on the design, specifically the need for a real-time notification system.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, FR-002
- **Conflicts with:** None
---