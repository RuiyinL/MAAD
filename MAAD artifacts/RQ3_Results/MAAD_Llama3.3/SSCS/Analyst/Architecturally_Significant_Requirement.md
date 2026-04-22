# Architecturally Significant Requirements Results:
[ASR-001]: Deterministic Timing
**Description**: The system performs sun acquisition and controls the satellite's attitude in a deterministic and predictable manner, with all control actions completed within 160ms per cycle, 99.9% of cycles. Metric: control_action.timing.p99 (window=10,000 cycles); Alert: if p99 >160ms, raise SRE incident.
**Architectural Impact:**  
The system's architecture must be designed to ensure deterministic timing, which may involve the use of a real-time operating system, a cyclic executive, or other timing-related mechanisms.
**Quality Attributes Affected:**  
Performance, Reliability, Availability
**Architectural Constraints:**  
The system must use a deterministic timing mechanism, such as a cyclic executive or a real-time operating system.
**Rationale:**  
This requirement is architecturally significant because it imposes a strong constraint on the system's design and requires a specific architectural approach to ensure deterministic timing.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001, NFR-001
- **Conflicts with:** None
---

[ASR-002]: Serial Port Interface
**Description**: The system uses serial ports for communication with ground commands, gyroscope, and sun sensor, with a frame structure of {Header (1 byte = 0xAA), Length (1 byte), Payload (N bytes), Checksum (1 byte, sum mod 256)} and inter-byte spacing < 5us.
**Architectural Impact:**  
The system's architecture must be designed to accommodate the serial port interface, which may involve the use of a serial port driver, a communication protocol, or other interface-related mechanisms.
**Quality Attributes Affected:**  
Performance, Reliability, Availability
**Architectural Constraints:**  
The system must use a serial port interface, which may impose constraints on the system's design, such as the use of a specific communication protocol or the implementation of a serial port driver.
**Rationale:**  
This requirement is architecturally significant because it imposes a strong constraint on the system's design and requires a specific architectural approach to accommodate the serial port interface.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002, FR-003, NFR-002
- **Conflicts with:** None
---

[ASR-003]: Fault-Tolerant Design
**Description**: The system detects and recovers from component faults within 5s; failover event rate < 1/mission day. Metric: failover.time_to_recovery (event); Alert: if failover.event_rate >1/day, critical SRE ticket auto-triggered.
**Architectural Impact:**  
The system's architecture must be designed to accommodate fault tolerance, which may involve the use of redundancy, error detection and correction mechanisms, or other fault-tolerant design approaches.
**Quality Attributes Affected:**  
Reliability, Availability
**Architectural Constraints:**  
The system must be designed to detect and recover from faults, which may impose constraints on the system's design, such as the use of redundancy or the implementation of error detection and correction mechanisms.
**Rationale:**  
This requirement is architecturally significant because it imposes a strong constraint on the system's design and requires a specific architectural approach to ensure fault tolerance.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008, NFR-004
- **Conflicts with:** None
---

[ASR-004]: Real-Time Data Processing
**Description**: The system processes data from the gyroscope and sun sensor in real-time, with all control actions completed within 160ms per cycle, 99.9% of cycles.
**Architectural Impact:**  
The system's architecture must be designed to accommodate real-time data processing, which may involve the use of a real-time operating system, a cyclic executive, or other real-time related mechanisms.
**Quality Attributes Affected:**  
Performance, Reliability, Availability
**Architectural Constraints:**  
The system must use a real-time data processing mechanism, which may impose constraints on the system's design, such as the use of a specific communication protocol or the implementation of a real-time operating system.
**Rationale:**  
This requirement is architecturally significant because it imposes a strong constraint on the system's design and requires a specific architectural approach to ensure real-time data processing.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-003, FR-004, NFR-001
- **Conflicts with:** None
---

[ASR-005]: Secure Data Transmission
**Description**: The system ensures the security of the data transmitted and received, with all telemetry/command data exchanged over serial ports encrypted using AES-128 and authenticated using HMAC-SHA256. Metric: crypto.auth.fail.count (window=1h, alert if >0); Log: syslog/audit upon auth/encrypt fail; Auto-fault if 3 consecutive failures.
**Architectural Impact:**  
The system's architecture must be designed to accommodate secure data transmission, which may involve the use of encryption, authentication, or other security-related mechanisms.
**Quality Attributes Affected:**  
Security
**Architectural Constraints:**  
The system must use a secure data transmission mechanism, which may impose constraints on the system's design, such as the use of a specific encryption algorithm or the implementation of authentication mechanisms.
**Rationale:**  
This requirement is architecturally significant because it imposes a strong constraint on the system's design and requires a specific architectural approach to ensure secure data transmission.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-009, NFR-005
- **Conflicts with:** None
---