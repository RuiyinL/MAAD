# Functional Requirements Results:

[FR-001]: Complaint Registration Module
**Description**: Citizens can register their complaints with police and the Registration module acts as an interface between the police and citizens, easing the approach, interaction and information exchange between police and complainants. Inputs: complainant name, contact, category, narrative; Outputs: registration ID, confirmation; Preconditions: authenticated or verified session.

**Rationale:** This describes a core system function - the ability for citizens to register complaints through a dedicated module.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-001 (Performance), ASR-001 (SOA Architecture)
- **Conflicts with:** None identified
---

[FR-002A]: Automated Evidence Capture
**Description**: Automated evidence capture (inputs: evidence file, investigator ID, output: evidence ID, status). Derived from FR-002.

**Rationale:** This describes an atomic sub-function of the investigation process automation - capturing evidence.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Registration Module)
- **Conflicts with:** None identified
---

[FR-002B]: Automated Task Assignment
**Description**: Automated task assignment (input: case ID, output: assigned user/task ID). Derived from FR-002.

**Rationale:** This describes an atomic sub-function of the investigation process automation - assigning tasks.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-001 (Registration Module)
- **Conflicts with:** None identified
---

[FR-003]: Prosecution and Court Interface
**Description**: The Prosecution module of the CCTNS aids interfacing with courts by providing a platform to record entries of the court interactions.

**Rationale:** This describes a specific function - recording court interaction entries for prosecution purposes.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-002A (Automated Evidence Capture)
- **Conflicts with:** None identified
---

[FR-004]: Case and Criminal Search Functionality
**Description**: The Search module gives police personnel the ability to execute a basic or advanced search on cases. Police personnel can search for a particular person, type of crime, modus operandi, property etc. It also gives the user the ability to customize the results view by criminal/accused or by cases. Input: {crime_type: string, accused_name: string, date_range: [date, date], ...}; Output: {results: [{case_id, summary, ...}], total_count, paging: {page, pageSize}}.

**Rationale:** This describes core search functionality with multiple search criteria and result customization options.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-002 (Search Performance), ASR-008 (Search Optimization)
- **Conflicts with:** None identified
---

[FR-005]: Reporting Functionality
**Description**: The system makes reporting easy for police by enabling them to execute different types of queries such as monthly reporting, RTI related etc.

**Rationale:** This describes a reporting function that transforms stored data into various report formats.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Search Functionality)
- **Conflicts with:** None identified
---

[FR-006]: Citizen Information Exchange
**Description**: The Citizen Interface module acts as a conduit for the information exchange between citizens and police units/personnel. Citizens can use it as a tool to get information or acknowledgements from police. The police in turn can use it to respond to citizens with very little turnaround time. Inputs: request type, citizen ID, message. Outputs: status, response message. Preconditions: authenticated citizen or verified contact. Output: {status: 'success'|'error', message: string, code: int, data: {...}}.

**Rationale:** This describes bidirectional communication functionality between citizens and police.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-003 (Availability), ASR-004 (Browser-based Access)
- **Conflicts with:** None identified
---

[FR-007]: Role-Based Navigation
**Description**: The Navigation module provides role based landing pages which help in navigating through the CCTNS application. It shows information such as cases assigned, alerts, pending tasks etc. Each role-based landing page must display: assigned case list (table), pending alerts (list), pending task count.

**Rationale:** This describes navigation functionality that adapts based on user roles.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control)
- **Conflicts with:** None identified
---

[FR-008]: Context-Sensitive Help
**Description**: The solution should provide detailed context-sensitive help material for all the possible actions and scenarios on all user interfaces in the application. Acceptance: At least 95% of user flows have relevant help tip or doc popup, as validated by QA checklist.

**Rationale:** This describes a help function that provides action-specific guidance to users.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Usability)
- **Conflicts with:** None identified
---

[FR-009]: Defect and Enhancement Request Tracking
**Description**: The solution should provide an interface for the user to log any defects or enhancement requests on the application and track thereafter. The solution should enable the user to track the submitted defect or enhancement request. Fields: {id, title, description, status, category, submitted_by, created_at}.

**Rationale:** This describes a tracking function for system defects and enhancement requests.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[FR-010]: Alert Notification System
**Description**: The solution should send alerts (e.g., email, SMS) to the user if the user chooses to whenever any action has been taken on the alert. Acceptance: 95% of all notifications delivered <2 min, retry up to 3x, with failed-delivery audit.

**Rationale:** This describes a notification function that sends alerts via multiple channels.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-005 (Communication Services)
- **Conflicts with:** None identified
---

[FR-011]: Help-Desk Reporting
**Description**: The solution should enable the help-desk user to view the reports on the submitted defects or enhancement requests category-wise, status-wise, and age- wise.

**Rationale:** This describes a reporting function specific to help-desk operations.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009 (Defect Tracking)
- **Conflicts with:** None identified
---

[FR-012]: Audit Trail Capture - Actions
**Description**: The CCTNS system must keep an unalterable audit trail capable of automatically capturing and storing information about all the actions (create/read/update/delete) that are taken upon the critical entities in the CCTNS system. Audit record schema: {event_type: 'UPDATE', entity: 'CASE', entity_id: 123, user_id: 20, timestamp: <iso_ts>, hash_prev: <sha256>}.

**Rationale:** This describes a core logging function that captures all CRUD operations on critical entities.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Unalterable Audit Trail), NFR-005 (Security)
- **Conflicts with:** None identified
---

[FR-013]: Audit Trail Capture - User Information
**Description**: The CCTNS system must keep an unalterable audit trail capable of automatically capturing and storing information about the user initiating and or carrying out the action. Audit record schema includes user_id.

**Rationale:** This describes audit logging of user identity for each action.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Unalterable Audit Trail), ASR-006 (Access Control)
- **Conflicts with:** None identified
---

[FR-014]: Audit Trail Capture - Timestamp
**Description**: The CCTNS system must keep an unalterable audit trail capable of automatically capturing and storing information about the date and time of the event. Audit record schema includes timestamp.

**Rationale:** This describes audit logging of temporal information for each event.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-002 (Unalterable Audit Trail)
- **Conflicts with:** None identified
---

[FR-015]: Audit Trail Export
**Description**: The CCTNS system must be able to export audit trails for specified cases (without affecting the audit trail stored by The CCTNS system). This functionality can be used by external auditors who wish to examine or analyse system activity. Export: Encrypted JSON file, includes all audit fields + signature block.

**Rationale:** This describes an export function for audit trail data.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012 (Audit Trail Capture)
- **Conflicts with:** None identified
---

[FR-016]: Access Control - User/Group Limitation
**Description**: The CCTNS system must allow the user to limit access to cases to specified users or user groups. Role: {id, name, permissions:[]}, User: {id, roles:[], groups:[]}, Permission: {id, object, action}.

**Rationale:** This describes an access control function for case-level permissions.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control)
- **Conflicts with:** None identified
---

[FR-017]: Role-Based Functionality Control
**Description**: The CCTNS system should provide for role-based control for the functionality within the CCTNS system.

**Rationale:** This describes function-level access control based on user roles.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control)
- **Conflicts with:** None identified
---

[FR-018]: User Group Membership
**Description**: The CCTNS system must allow a user to be a member of more than one group.

**Rationale:** This describes a user management function for group membership.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control)
- **Conflicts with:** None identified
---

[FR-019]: Security Attribute Management
**Description**: The CCTNS system must allow changes to security attributes for groups or users (such as access rights, security level, privileges, password allocation and management) to be made only by super-user.

**Rationale:** This describes an administrative function for security attribute management.

**Dependencies** / **Conflicts**:
- **Depends on:** ASR-006 (Role-Based Access Control), NFR-005 (Security)
- **Conflicts with:** None identified
---

[FR-020]: Access Denial Response Options
**Description**: If a user requests access to, or searches for, a case which he does not have the right to access, the CCTNS system must provide one of the following responses (selectable at configuration time): display title and metadata; display the existence of a case but not its title or other metadata; do not display any case information or indicate its existence in any way. Audit log: {user_id, resource_id, attempted_action, timestamp, outcome: 'denied', client_ip}.

**Rationale:** This describes configurable behavior for unauthorized access attempts.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-016 (Access Control), ASR-006 (Role-Based Access Control)
- **Conflicts with:** None identified
---

[FR-021]: Search Result Access Filtering
**Description**: If a user performs a quick or advanced search, the CCTNS system must never include in the search result list any record which the user does not have the right to access.

**Rationale:** This describes access control filtering applied to search results.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-004 (Search Functionality), FR-016 (Access Control)
- **Conflicts with:** None identified
---

[FR-022]: Unauthorized Access Logging
**Description**: If the CCTNS system allows users to make unauthorised attempts to access cases, it must log these in the audit trail.

**Rationale:** This describes security logging for unauthorized access attempts.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012 (Audit Trail Capture), FR-016 (Access Control)
- **Conflicts with:** None identified
---

[FR-023]: Error Message Display
**Description**: All error messages produced by the CCTNS system must be meaningful, so that they can be appropriately acted upon by the users who are likely to see them. Ideally, each error message will be accompanied by explanatory text and an indication of the action(s) which the user can take in response to the error. Error message schema: { code: 'ERR-LOGIN-001', message: 'Invalid username or password', actions: ['retry', 'reset password'], lang: 'en', details: {...} }. Test: 95%+ settings preserved.

**Rationale:** This describes error handling and user communication functionality.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Usability)
- **Conflicts with:** None identified
---

[FR-024]: UI Customization
**Description**: The interfaces must be made customizable or user-configurable to the extent possible (e.g., the displayed columns in the table, move, resize, modify the appearance). Such configurations must be saved in the user profile. Users must configure: column show/hide, column order, font size. Changes persist in user profile; test by login/logout. Test: user changes font size, logs out/in, change persists; pass if 95%+ settings preserved.

**Rationale:** This describes a customization function for user interface elements.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Usability)
- **Conflicts with:** None identified
---

[FR-025]: Persistent Data Entry Defaults
**Description**: The CCTNS system must allow persistent defaults for data entry where desirable. These defaults should include: user-definable values; values same as previous item; values derived from context, e.g. date, file reference, user identifier.

**Rationale:** This describes a data entry assistance function with persistent defaults.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[FR-026]: Multi-Entity Display
**Description**: The CCTNS system must be able to display several entities (cases, suspects) simultaneously. Test: 90% of screens configurable.

**Rationale:** This describes a display function for multiple entity types.

**Dependencies** / **Conflicts**:
- **Depends on:** NFR-004 (Usability)
- **Conflicts with:** None identified
---

[FR-027]: Printable Document Versions
**Description**: If a document is either too long, dispersed over several pages or in a specific layout that is not suitable for online reading, a printer-friendly version of the document should be provided that prints the content in a form acceptable to the user.

**Rationale:** This describes a document output function for printing.

**Dependencies** / **Conflicts**:
- **Depends on:** None identified
- **Conflicts with:** None identified
---

[FR-028]: Violation Capture and Storage
**Description**: The CCTNS system must be able to capture and store violations (i.e. a user's attempts to access a case to which he is denied access), and (where violations can validly be attempted) attempted violations, of access control mechanisms. Audit log: {user_id, resource_id, attempted_action, timestamp, outcome: 'denied', client_ip}.

**Rationale:** This describes security violation logging functionality.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012 (Audit Trail Capture), FR-016 (Access Control)
- **Conflicts with:** None identified
---

[FR-029]: Audit Trail by Workstation/Network
**Description**: The CCTNS system should be able to provide reports for actions on cases organised by workstation and (where technically appropriate) by network address.

**Rationale:** This describes a reporting function for audit data organized by location.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-012 (Audit Trail Capture)
- **Conflicts with:** None identified
---

[FR-030]: Defect/Enhancement Tracking Support Access
**Description**: The support solution should be accessible to the users both from within the application and also outside the application through a browser interface.

**Rationale:** This describes access methods for the support/defect tracking functionality.

**Dependencies** / **Conflicts**:
- **Depends on:** FR-009 (Defect Tracking), ASR-004 (Browser-based Access)
- **Conflicts with:** None identified
---