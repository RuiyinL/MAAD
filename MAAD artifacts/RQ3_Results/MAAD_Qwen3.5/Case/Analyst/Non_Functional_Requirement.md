# Non-Functional Requirements Results:
[NFR-001]: Patient Monitoring Reliability
**Description:** If an analog device fails, the nurses' station is notified. Measurable NFR: 99.99% of alerts must be delivered and acknowledged within 3 seconds; audit trail required for all alert events. For each alert event: record {alert_id, timestamp_sent, timestamp_delivered, timestamp_ack, ack_user}, audit log stores all rows. Metric names: 'alert_delivery_latency_ms', 'alert_ack_latency_ms', 'alert_audit_event'. [Next Action: Define metrics and log schema for alert audit.]

**Quality Attributes**: Reliability, Safety

**Measurable Criteria (if provided):** 99.99% of alerts must be delivered and acknowledged within 3 seconds; audit trail required for all alert events. Metric names: 'alert_delivery_latency_ms', 'alert_ack_latency_ms', 'alert_audit_event'. Log format: {alert_id, timestamp_sent, timestamp_delivered, timestamp_ack, ack_user}.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[NFR-002]: Airport Shuttle Ride Comfort
**Description:** The journey should be as fast as possible, subject to certain limits on the speed, acceleration, and deceleration to give passengers a comfortable ride and avoid excessive wear. The shuttle's maximum speed must not exceed 5 m/s, acceleration/deceleration must not exceed 1 m/s².

**Quality Attributes**: Performance, Usability, Maintainability

**Measurable Criteria (if provided):** Maximum speed must not exceed 5 m/s, acceleration/deceleration must not exceed 1 m/s².

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-003]: Traffic Light Flexibility
**Description:** To change the regime only the card needs to be changed; manufacturers supply a range of cards to suit any condition. System shall load new regime and switch to new light sequence within 10 seconds of card insertion.

**Quality Attributes**: Modifiability, Usability

**Measurable Criteria (if provided):** System shall load new regime and switch to new light sequence within 10 seconds of card insertion.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004
- **Conflicts with:** None
---
[NFR-004]: Package Router Reliability
**Description:** The system must report misrouted packages and handle unpredictable package speeds where packages may get too close together.

**Quality Attributes**: Reliability, Robustness

**Measurable Criteria (if provided):** All misrouted packages must be reported.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[NFR-005]: Secure Door Security
**Description:** The secure door is to be controlled by a computer that recognises facial features compared with entries in a database of cleared people. Admission only after facial match with >97% certainty (FAR <0.1%), all recognition data encrypted in transit/rest, all accesses logged. All facial recognition data must be encrypted using AES-256 at rest, TLS 1.3 in transit; access logs must capture actor, timestamp, action, and be retained for 5 years. All facial data access logged per GDPR, SIEM pushes to centralized logging in JSON: {event_id, user_id, timestamp, action}; AES key rotates annually. [Next Action: Align with InfoSec to define policy fields and log sampling.]

**Quality Attributes**: Security

**Measurable Criteria (if provided):** Admission only after facial match with >97% certainty (FAR <0.1%), all recognition data encrypted in transit/rest, all accesses logged. All facial recognition data must be encrypted using AES-256 at rest, TLS 1.3 in transit; access logs must capture actor, timestamp, action, and be retained for 5 years. SIEM pushes to centralized logging in JSON: {event_id, user_id, timestamp, action}; AES key rotates annually.

**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---