# Functional Requirements Results:
[FR-001]: Citizen Submits Complaint
**Description**: Inputs: {citizen_id: UUID, complaint_text: string, UTF-8, 1-2048 chars, profanity filtered (per <policy>), evidence_urls: [optional, URI, HTTPS only]}; Outputs: {complaint_id: UUID, status: enum [submitted, error:<code>]}. Precondition: citizen must be authenticated. Error: returns {error_code, message} on failure. Derived from original FR-001.
**Rationale:** This requirement describes a function of the system where citizens can register complaints and the police can take action on them.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-002]: Police Reviews/Accepts Complaint
**Description**: review_status: enum [pending, accepted, rejected, needs_info]; notification: {recipient_id: citizen_id, type: SMS|email, template_id, payload}. Derived from original FR-001.
**Rationale:** This requirement describes a function of the system that allows police to review and accept complaints.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-003]: Search Functionality
**Description**: Input: {filters: {...}}, Output: {cases: [{case_id, ...}], total, batch_size, error: {code,msg}}.
**Rationale:** This requirement describes a function of the system that allows police personnel to search for cases.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-004]: Citizen Interface
**Description**: The Citizen Interface module of the CCTNS acts as a conduit for the information exchange between citizens and police units/personnel.
**Rationale:** This requirement describes a function of the system that facilitates information exchange between citizens and police personnel.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-005]: Navigation Module
**Description**: The Navigation module of the CCTNS provides role-based landing pages which help in navigating through the CCTNS application.
**Rationale:** This requirement describes a function of the system that provides role-based navigation.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-006]: Registration Module
**Description**: The Registration module acts as an interface between the police and citizens and it eases the approach, interaction, and information exchange between police and complainants.
**Rationale:** This requirement describes a function of the system that facilitates registration and information exchange.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---
[FR-007]: Prosecution Module
**Description**: The Prosecution module of the CCTNS aids the interfacing by providing a platform to record entries of the court interactions.
**Rationale:** This requirement describes a function of the system that aids in court interactions.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---
[FR-008]: User Profile Management
**Description**: User profile changes must be approved by admin and logged as {user_id, action, timestamp, before, after}. Email must be validated (RFC 5322).
**Rationale:** This requirement describes a function of the system that manages user profiles.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-009]: Access Control
**Description**: Access is managed by RBAC: users assigned to groups with case/class-level permissions. All denied attempts are logged with {user_id, target_case_id, timestamp, reason}.
**Rationale:** This requirement describes a function of the system that controls access to cases.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-008
- **Conflicts with:** None
---
[FR-010]: Audit Trail
**Description**: Audit trail entries must be immutable, signed with SHA-256, retained at least 10 years, exportable per case, and testable by simulating log tampering or recovery from offline backup.
**Rationale:** This requirement describes a function of the system that maintains an audit trail.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---
[FR-011]: Investigation Automation
**Description**: Checklist schema: {id, steps:[{id,desc,mandatory}], ...}; logs: {type, actor, ts, related_case}. Steps marked 'mandatory' required for case closure.
**Rationale:** This requirement describes a function of the system that automates tasks for the investigation process.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-002
- **Conflicts with:** None
---