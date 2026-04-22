# Functional Requirements Results:
[FR-001]: User classification-based access control  
**Description**: The system shall classify users into Astronomer, Science Observer, Telescope Operator, Support Personnel, Developers, and Administrators, each with distinct access privileges and operational capabilities. Precondition: User authenticated via LDAP; role mapping via 'user_role' LDAP attribute. Acceptance: Attempt all logins using test LDAP accounts for all classes; access modes match specification table.  

**Rationale:** Defines specific system behaviors for user role handling and access control.  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-002 (Operational Levels), FR-003 (Access Modes)  
---  
[FR-002]: Operational level enforcement  
**Description**: The system shall enforce three disjoint operational levels (Observing, Maintenance, Test) with access restrictions based on current level. Operational level enforced by 'GeminiControlPolicy' subsystem; acceptance: test suite attempts forbidden actions at each level; system blocks and logs at INFO with user, attempted action, and timestamp.  

**Rationale:** Specifies conditional system behavior for operational state management.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-001 (User classification)  
---  
[FR-004]: Multi-instrument parallel operations  
**Description**: The system shall support parallel operations for multiple mounted instruments. Adverse impact is defined as performance degradation >10% in the active instrument's throughput or any operational error attributable to actions of inactive instruments. The system must log and alarm on such events.  

**Rationale:** Defines specific instrument interaction behaviors with measurable adverse impact criteria.  

**Dependencies** / **Conflicts**:  
- **Depends on:** ASR-003 (Multi-instrument concurrency)  
---  
[FR-005]: Visitor instrument interface  
**Description**: The system shall provide standardized interfaces for visitor instruments supporting status acquisition, preprogrammed sequences, telescope offsetting, and focus control. The interface shall expose a JSON API schema: { 'status': { 'instrument_id': string, 'state': string, ... }, ... } with version key. Extensibility rules must be defined. The API SHALL conform to an OpenAPI 3.0 specification with change control for breaking changes. Error codes SHALL be enumerated. Example OpenAPI 3.0 schema stub:  
```yaml  
openapi: 3.0.0  
info:  
  title: Visitor Instrument API  
  version: 1.0.0  
paths:  
  /status:  
    get:  
      summary: Get instrument status  
      responses:  
        '200':  
          description: OK  
          content:  
            application/json:  
              schema:  
                $ref: '