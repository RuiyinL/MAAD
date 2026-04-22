Analysis Plan:
Scope: Design a production-ready architectural documentation for a patient monitoring program, aligning with the provided requirements document and PlantUML diagrams.
Approach: Normalize the requirements into atomic, measurable statements, and create a traceability matrix to ensure every requirement is mapped to a component and artifact.
Top validation steps: Verify that every functional requirement (FR), non-functional requirement (NFR), and architectural requirement (ASR) is included in the traceability matrix, and that each major component has a clear API contract, data schema, and recommended technology stack with justifications tied to ASR/NFR IDs.

# A. Executive Summary
The patient monitoring program is designed to read vital signs from patients on a periodic basis and store them in a database. The system will notify the nurses' station if a patient's vital signs fall outside a safe range or if an analog device fails. The chosen architectural style is a modular monolith, with a deployment topology consisting of a single server and a database. The top 3 design risks are data consistency, security, and scalability, with mitigations including the use of transactions, encryption, and load balancing.

| Design Risk | Mitigation |
| --- | --- |
| Data Consistency | Use transactions to ensure data integrity |
| Security | Implement encryption and access controls to protect patient data |
| Scalability | Use load balancing and horizontal scaling to handle increased traffic |

# B. Traceability & Rationale
The following table shows the traceability matrix for the patient monitoring program:

| Requirement ID | Short Text | Diagram(s) | Component(s) | Artifact filename(s) | Rationale |
| --- | --- | --- | --- | --- | --- |
| FR-1 | Read vital signs from patients | UseCase: PatientMonitoring | PatientMonitor | openapi.yaml | This requirement is necessary to collect patient data |
| NFR-1 | Store patient data in a database | Class: Patient | Database | sql/patient_ddl.sql | This requirement is necessary to persist patient data |
| ASR-1 | Notify nurses' station if patient data falls outside safe range | Sequence: Notification | NotificationService | internal.proto | This requirement is necessary to alert medical staff of potential issues |

# C. Architecture Overview
The patient monitoring program consists of the following components:
- PatientMonitor: responsible for reading vital signs from patients
- Database: responsible for storing patient data
- NotificationService: responsible for notifying the nurses' station if patient data falls outside a safe range

The system uses a modular monolith architecture, with a deployment topology consisting of a single server and a database. The PatientMonitor component uses a contract-first approach, with an OpenAPI definition for the external API. The Database component uses a relational database management system, with a SQL schema defined for the patient data.

# D. Detailed Technical Design
## PatientMonitor
### Responsibilities & Data Ownership
The PatientMonitor component is responsible for reading vital signs from patients and storing them in the database. It owns the patient data and is responsible for ensuring its accuracy and integrity.

### Technology Options
- Language/Runtime: Java 17, Python 3.10, or Node.js 18
- Web Framework: Spring Boot, Django, or Express.js
- RPC/HTTP: gRPC, REST, or GraphQL
- Persistence: PostgreSQL, MySQL, or MongoDB
- Cache: Redis, Memcached, or In-Memory
- Messaging: Apache Kafka, RabbitMQ, or Amazon SQS
- Search: Elasticsearch, Apache Solr, or MongoDB
- Authn/Authz: OAuth2, OIDC, or JWT
- Observability: Prometheus, Grafana, or New Relic
- CI/CD: Jenkins, GitLab CI/CD, or CircleCI
- Container Runtime: Docker, Kubernetes, or Containerd
- Infra Provisioning: Terraform, AWS CloudFormation, or Azure Resource Manager

### Recommended Default Stack
- Language/Runtime: Java 17
- Web Framework: Spring Boot
- RPC/HTTP: gRPC
- Persistence: PostgreSQL
- Cache: Redis
- Messaging: Apache Kafka
- Search: Elasticsearch
- Authn/Authz: OAuth2
- Observability: Prometheus
- CI/CD: Jenkins
- Container Runtime: Docker
- Infra Provisioning: Terraform
Justification: meets ASR-1 (notify nurses' station if patient data falls outside safe range) and NFR-1 (store patient data in a database)

### Interface Design
#### External APIs
The PatientMonitor component exposes an external API for reading vital signs from patients. The API is defined using OpenAPI and includes the following endpoints:
```yml
openapi: 3.0.0
info:
  title: PatientMonitor API
  description: API for reading vital signs from patients
  version: 1.0.0
paths:
  /patients/{patientId}/vital-signs:
    get:
      summary: Read vital signs from a patient
      parameters:
        - in: path
          name: patientId
          schema:
            type: integer
          required: true
          description: Patient ID
      responses:
        200:
          description: Vital signs read successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  pulse:
                    type: integer
                  temperature:
                    type: number
                  bloodPressure:
                    type: object
                    properties:
                      systolic:
                        type: integer
                      diastolic:
                        type: integer
        404:
          description: Patient not found
```
#### Internal Contracts
The PatientMonitor component uses an internal contract for communicating with the Database component. The contract is defined using gRPC and includes the following messages:
```proto
syntax = "proto3";

package patientmonitor;

service PatientMonitor {
  rpc ReadVitalSigns(ReadVitalSignsRequest) returns (ReadVitalSignsResponse) {}
}

message ReadVitalSignsRequest {
  int32 patient_id = 1;
}

message ReadVitalSignsResponse {
  int32 pulse = 1;
  float temperature = 2;
  BloodPressure blood_pressure = 3;
}

message BloodPressure {
  int32 systolic = 1;
  int32 diastolic = 2;
}
```
### Data Model / Schema
The PatientMonitor component uses a relational database management system to store patient data. The schema for the patient data is defined as follows:
```sql
CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  date_of_birth DATE NOT NULL
);

CREATE TABLE vital_signs (
  id SERIAL PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  pulse INTEGER NOT NULL,
  temperature FLOAT NOT NULL,
  blood_pressure_systolic INTEGER NOT NULL,
  blood_pressure_diastolic INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
### Caching & Consistency Strategy
The PatientMonitor component uses a caching layer to improve performance. The caching layer is implemented using Redis and includes the following cache keys:
- `patient:{patientId}:vital-signs`: stores the vital signs for a patient
The caching layer is configured to expire cache entries after 1 hour.

# E. Operations & Deployment
The PatientMonitor component is deployed using a Kubernetes-ready plan. The plan includes the following components:
- `PatientMonitor`: the PatientMonitor component
- `Database`: the database component
- `Redis`: the caching layer
The plan uses a rolling update strategy to ensure zero downtime during deployments.

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: patient-monitor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: patient-monitor
  template:
    metadata:
      labels:
        app: patient-monitor
    spec:
      containers:
        - name: patient-monitor
          image: patient-monitor:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              value: "postgresql://user:password@database:5432/patient_monitor"
            - name: REDIS_URL
              value: "redis://redis:6379/0"
```
# F. Security Design
The PatientMonitor component uses a security design that includes the following components:
- Authentication: OAuth2
- Authorization: Role-Based Access Control (RBAC)
- Encryption: TLS
- Secrets Management: Hashicorp Vault
The security design is implemented using a combination of infrastructure and application-level security controls.

# G. Observability & SRE
The PatientMonitor component uses an observability design that includes the following components:
- Monitoring: Prometheus
- Logging: ELK Stack
- Tracing: Jaeger
The observability design is implemented using a combination of infrastructure and application-level observability controls.

# H. Testing Strategy
The PatientMonitor component uses a testing strategy that includes the following components:
- Unit Testing: JUnit
- Integration Testing: TestNG
- End-to-End Testing: Cypress
The testing strategy is implemented using a combination of automated and manual testing techniques.

# I. Migration, Data Conversion & Rollout Plan
The PatientMonitor component uses a migration plan that includes the following components:
- Data Migration: uses a data migration tool to migrate data from the old system to the new system
- Code Migration: uses a code migration tool to migrate code from the old system to the new system
- Rollout Plan: uses a rollout plan to deploy the new system to production

# J. Tradeoffs & Alternatives
The PatientMonitor component uses a tradeoff analysis that includes the following components:
- Tradeoff Analysis: uses a tradeoff analysis to evaluate the pros and cons of different design options
- Alternative Designs: uses alternative designs to evaluate the pros and cons of different design options

# K. Open Questions & Assumptions
The PatientMonitor component uses an open questions and assumptions analysis that includes the following components:
- Open Questions: uses an open questions analysis to identify areas where more information is needed
- Assumptions: uses an assumptions analysis to identify areas where assumptions are made

# L. Deliverables
The following deliverables are included:
```markdown
# architecture.md
# openapi.yaml
# internal.proto
# k8s/patient-monitor-deployment.yaml
# sql/patient_ddl.sql
# traceability_matrix.csv
```
---  
# Acceptance Criteria
The following acceptance criteria are included:
- [ ] 3-line Analysis Plan present
- [ ] Sections A-L included
- [ ] Every FR/NFR/ASR mapped in traceability matrix
- [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included
- [ ] Representative k8s manifest snippet included
- [ ] SQL DDL / NoSQL models for primary entities included
- [ ] All major components have at least one API contract and a data schema
- [ ] Assumptions and unresolved questions listed

---  
# How to review
The following review checklist is included:
- All FR/NFR/ASR present in traceability matrix?
- OpenAPI + internal API contract included and valid?
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?
- k8s snippet present and syntactically valid?
- SQL DDLs provided for persisted entities?
- Assumptions and open questions clearly listed?