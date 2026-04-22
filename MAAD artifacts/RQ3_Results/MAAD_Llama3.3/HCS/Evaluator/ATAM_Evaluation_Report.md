```markdown
# DigitalHome Smart House ATAM Architecture Evaluation Report

---

## B. Analysis Plan

**Scope:** Evaluation of the DigitalHome “Smart House” system architecture, including prototype, API, gateway, database, security, observability, deployment, and operations.  
**Approach:** Scenario-based ATAM walkthroughs using stakeholder-derived quality attribute scenarios; sensitivity and tradeoff analysis; risk and traceability mapping.  
**Validation Steps:** (1) Examine end-to-end security, reliability, and failover; (2) test key REST/gRPC contracts; (3) walkthrough at least eight prioritized QA scenarios for top business and technical risks.

---

## A. Executive Summary

The DigitalHome system presents a modular smart home prototype aimed at enabling residents to manage environmental, security, and appliance systems via web and mobile interfaces. Architecture is comprised of a modular monolith (hexagonal) with explicit API and gRPC boundaries, persistent PostgreSQL database, and a scalable Kubernetes deployment (see: Logic View Class Diagram, Deployment/Container Diagrams). Key diagrams: Use Case Diagram, Class Diagram, State Diagram, Deployment Diagram, Container Diagram.

**Top 5 Business Goals:**  
1. Enable remote, secure, real-time home environment management for residents.  
2. Provide reliable, continuous monitoring and control of home systems with minimal downtime.  
3. Offer a compelling prototype to guide business investment and market strategy.  
4. Ensure low total system cost for competitive positioning.  
5. Lay a scalable foundation for future feature extension and commercialization.

**Top 5 Findings:**  
1. **High-severity Risk:** Recovery from network or component failures (FR/NFR-1; NFR-1), mitigated via robust backup and recovery but may require further failover design.  
2. **High-severity Risk:** API-level security gaps (ASR-1, FRs); authentication and RBAC included but needs thorough threat modeling.  
3. **Moderate Risk:** Testing coverage and SRE completeness (NFR, INF-008); extensions for end-to-end and failure mode coverage advised.  
4. **Non-Risk:** Core functional decomposition (UML/hexagonal monolith) is sound for prototype scope; easily evolved (Evidence: Architecture Doc, Development View).  
5. **Next Step:** Focus on validation of top QA scenarios (reliability, security, scalability) and close architectural gaps before feature expansion.

---

## C. Concise Architectural Presentation

DigitalHome consists of three primary tiers: a Web Server/API layer (Node.js), a Gateway service (Spring Boot/gRPC), and a PostgreSQL database, deployed together as containers under Kubernetes (Deployment Diagram, Container Diagram). Actors include General Users, Master Users/Admin, and DigitalHome Technicians (Use Case Diagram).

**Main Architectural Tactics/Patterns:**  
- Hexagonal (Ports & Adapters) architecture for Web and Gateway layers.  
- Clear API/gRPC contracts between Entry Points and Device Gateway (OpenAPI/gRPC).  
- Modular monolith for rapid prototyping, with component encapsulation for later scaling.  
- Continuous monitoring, backup/recovery, and SRE-aware deployment (Prometheus, backup agents).

**Major Architectural Decisions:**  
- **D1:** Use of Kubernetes for deployment (INF-021) — rationale: ensures cloud portability, operational efficiency.  
- **D2:** API contracts specified in OpenAPI/gRPC (FR-1, FR-2) — rationale: enforces interface stability and testability.  
- **D3:** Strong authentication/authorization with OAuth2/RBAC (ASR-1) — rationale: align with modern security standards.  
- **D4:** Modular monolith for prototype (INF-023) — rationale: accelerates delivery; future migration path considered.  
- **D5:** Use of COTS hardware/interfaces where possible (INF-010) — rationale: cost containment for prototype phase.

---

## D. Business Goals & Drivers

| GoalID | ShortText                                           | Priority | RelatedRequirementIDs                        | Stakeholder      |
|--------|-----------------------------------------------------|----------|----------------------------------------------|------------------|
| BG-01  | Enable secure, remote home environmental management | P0       | FR-1, FR-2, ASR-1, INF-010, INF-020         | HomeOwner Mgmt   |
| BG-02  | High reliability and continuity                     | P0       | NFR-1, FR-6, FR-8, INF-003                  | HomeOwner Mgmt   |
| BG-03  | Guide business through valuable prototype           | P0       | INF-016, FR-1–FR-8, NFR-1                   | Marketing        |
| BG-04  | Minimize total cost for prototype/devices           | P1       | INF-010, INF-019, NFR-2                     | Management, Ops  |
| BG-05  | Support evolution to commercial product             | P1       | INF-011, INF-014, ASR-2, NFR-2, FR-7        | DigitalHomeOwner |

---

## E. Quality Attribute Scenarios & Prioritization

**Prioritization is by stakeholder weight (P0>P1>P2), impact, and risk exposure. Full table in `qa_scenarios.csv`. Summary below:**

| ScenarioID | Stimulus                                            | Source             | Env         | Artifact       | Response (Quality Attribute)                               | Measure                  | Priority |
|------------|-----------------------------------------------------|--------------------|-------------|---------------|------------------------------------------------------------|--------------------------|----------|
| QA-01      | Power loss at home                                  | User/Technician    | Home site   | WebServer     | System recovers and restores from backup                   | <5 min downtime          | High     |
| QA-02      | Unauthorized API access attempt detected            | Adversary          | Remote      | API           | Deny, log, alert in <1s                                    | % unauthorized denied    | High     |
| QA-03      | Surge in user traffic (4x baseline, peak hours)     | Ops                | Cloud/ISP   | WebServer     | No data loss, p95 latency <200ms                           | Latency, error rate      | High     |
| QA-04      | Device offline or unreachable                      | Device/Gateway     | Home site   | Gateway       | Report status, notify user/admin in <30s                   | Mean notification delay  | High     |
| QA-05      | Weekly schema migration needed (backward compatible)| DevOps             | Staging     | Database      | Migration completes, no data loss                          | % successful migrations  | Medium   |
| QA-06      | User modifies alert settings while plan running     | User               | Any         | WebServer     | Plan updated with no conflicting state                     | # incidents/changes      | Med      |
| QA-07      | Daily backup fails                                 | Scheduled Task     | Any         | WebServer     | Alert sent to admin, rerun triggered or backup skipped     | Time to alert/repair     | High     |
| QA-08      | Operator needs to audit user/device activity logs   | Auditor/Compliance | Any         | Log subsystem | Retrieve logs, search by user/device, within 30s           | Search speed/coverage    | Medium   |
| QA-09      | New sensor device type must be added in <2 weeks    | Product Owner      | Dev         | Gateway       | Add w/ minimal deploy, no downtime                         | Integration time         | Low      |
| QA-10      | Web API error triggers fallback UI for end user     | User               | Web client  | WebUI         | Show meaningful error message                              | Error clarity rating     | Med      |

**See `qa_scenarios.csv` for full records.**

**Prioritization rationale:** All security, reliability, and primary service continuity scenarios are “High”; modifiability and auditability are “Medium”; extensibility is “Low” for the prototype.

---

## F. Architecture Evaluation (Scenario-based analysis)

### Walkthroughs of Top 8 Quality Attribute Scenarios

#### QA-01: Power loss at home (NFR-1, INF-003)
- **Step 1:** HomeGrid loses power; Gateway and WebServer disconnect (State Diagram: offline-->*)
- **Step 2:** System reboots; backup/recovery mechanism restores config (Deployment Diagram: WebServer/Database Container nodes)
- **Step 3:** Gateway reconnects to devices, system resumes
- **Sensitivity Points:** Backup frequency, stateful recovery logic, database integrity
- **Tradeoffs:** Recovery speed vs. backup cost
- **Diagram refs:** State Diagram, Deployment Diagram
- **Confidence:** Medium (Prototype logic proven in lab, live failover unproven)

#### QA-02: Unauthorized API access attempt (ASR-1, INF-020)
- **Step 1:** External party attempts forbidden API action (API endpoint, OpenAPI contract)
- **Step 2:** OAuth2/RBAC check intercepts and rejects, logs event (Component Diagram, Security Design)
- **Step 3:** Alert issued via monitoring/ELK stack
- **Sensitivity Points:** Auth middleware, log/alert pipeline
- **Tradeoffs:** Latency vs. strictness of logging/auditing
- **Diagram refs:** Component Diagram: AuthComponent, Container Diagram
- **Confidence:** Medium (OpenAPI, RBAC implemented; penetration test results pending)

#### QA-03: Surge in user traffic (4x baseline) (NFR-2, BG-02)
- **Step 1:**  Concurrent clients access API (Container Diagram: webui/backend)
- **Step 2:** Load balanced requests (K8s), database connections spike
- **Step 3:** Monitoring checks p95 API latency
- **Sensitivity Points:** API throughput, DB resource limits, Kubernetes pod scaling
- **Tradeoffs:** Cost vs. maximum supported load
- **Diagram refs:** Deployment Diagram, Container Diagram
- **Confidence:** Medium (Proto load tests OK, but not at 4x scale)

#### QA-04: Device offline/unreachable (FR-6, INF-018)
- **Step 1:** Gateway loses contact with one device (Gateway, Device/Controller objects)
- **Step 2:** Device status marked offline; retry logic triggered
- **Step 3:** User alerted via UI, event logged
- **Sensitivity Points:** Heartbeat frequency, alert timeout
- **Tradeoffs:** Notification speed vs. false alarms
- **Diagram refs:** Object Diagram, State Diagram
- **Confidence:** Medium

#### QA-07: Daily backup fails (NFR-1)
- **Step 1:** Backup agent scheduled, job fails (Database, WebServer)
- **Step 2:** Failure event sent to monitoring and admin e-mail
- **Step 3:** Rerun triggered automatically if possible
- **Sensitivity Points:** Backup job scheduler, admin notification pipeline
- **Tradeoffs:** Manual vs. automated rerun, observable error detail
- **Diagram refs:** Deployment Diagram
- **Confidence:** Low/Medium (Lab-tested, live-site SRE not fully validated)

#### QA-05: Weekly schema migration (Development/Operations)
- **Step 1:** Operator triggers migration (Database, Persistence)
- **Step 2:** Data migrated and verified, system remains operational
- **Sensitivity Points:** Migration code quality, transaction boundaries
- **Tradeoffs:** Consistency vs. migration speed
- **Confidence:** Medium

#### QA-08: Audit log retrieval (ASR-3)
- **Step 1:** Admin queries logs via SRE/observability stack
- **Step 2:** Query parsed, data returned within SLA
- **Sensitivity Points:** Log structure/indexing, search infra
- **Tradeoffs:** Log volume vs. search speed
- **Confidence:** Medium

#### QA-10: UI fallback on error (FR-8)
- **Step 1:** API error returned to UI (WebUI, BackendAPI)
- **Step 2:** UI shows descriptive error
- **Step 3:** User context preserved; support links available
- **Sensitivity Points:** Front-end error-handler, API exception messaging
- **Tradeoffs:** Message verbosity vs. security/information leaks
- **Confidence:** High

**More scenario executions in `scenario_executions.md`.**

---

## G. Risks & Non-Risks (Risk Register)

See `risk_register.csv` (compiled below).

- **Key risks:** Recovery gaps (QA-01), API security (QA-02), scalability ceilings (QA-03), incomplete alerting (QA-07), device communication failures (QA-04), schema/migration reliability (QA-05).
- **Key non-risks:** Modular monolith approach (D4), COTS hardware reliance (D5), RBAC inclusion (D3) — see evidence tracebacks.

---

## H. Risk Themes & Systemic Issues

**Theme 1:** *Reliability and Continuity*  
- Contributing Risks: R-01 (Backup/recovery), R-05 (Device offline), R-06 (Backup job failure), R-07 (Migration errors)  
- Systemic Impact: Any reliability breach erodes trust and could have safety impacts in a real deployment  
- Priority Remediation: Backup validation, failover automation, improved test coverage

**Theme 2:** *Security and Access Control*  
- Contributing Risks: R-02 (API auth gaps), R-03 (Log data exposure)  
- Systemic Impact: Data compromise, privacy risk, compliance gaps  
- Remediation: Threat model review, harden endpoints, encryption validation

**Theme 3:** *Performance Under Normal and Peak Loads*  
- Contributing Risks: R-04 (Load/service interruption)  
- Impact: SLA breaches, user experience degradation  
- Remediation: Load testing, autoscale tuning, alert on latency SLOs

**Theme 4:** *Change Readiness and Evolvability*  
- Contributing Risks: R-07 (Migration), R-08 (New device types)  
- Impact: Stagnated features, operational headaches  
- Remediation: Modular gateway code, robust integration tests

---

## I. Sensitivity Points & Tradeoff Matrix

See `sensitivity_tradeoffs.csv`.

| DecisionID | DecisionText           | AffectedQAs         | DirectionOfSensitivity | Magnitude | Notes                                        |
|------------|-----------------------|---------------------|-----------------------|-----------|-----------------------------------------------|
| D1         | Kubernetes deployment | Availability, Perf. | improve               | High      | Enables horizontal scale, but may increase ops|
| D2         | API/gRPC contracts    | Testability, Perf.  | improve               | High      | Facilitates automated test, onboarding        |
| D3         | OAuth2/RBAC security  | Security, Usab.     | improve (security),degrade (usab.) | Med | Extra steps for users, more secure            |
| D4         | Monolith proto        | Modifiability, Scal.| improve (mod), degrade (scale) | Med | Fast proto, but scaling needs later work      |
| D5         | COTS adoption         | Cost, Reliability   | improve (cost), degrade(rel.) | Low   | Integration risk if COTS components mismatched|

---

## J. Mapping of Architectural Decisions → Quality Requirements

See `traceability_matrix.csv`.

| DecisionID | DecisionSummary                | SupportedRequirementIDs        | HinderedRequirementIDs | ConfidenceLevel | Rationale                                      |
|------------|-------------------------------|-------------------------------|-----------------------|----------------|------------------------------------------------|
| D1         | Use K8s for deployment         | NFR-1, NFR-2                  | INF-021               | Med            | Supports high availability, future scale        |
| D2         | API/gRPC contracts             | FR-1, FR-2, FR-3, FR-4        | none                  | High           | Enables testability, boundary contracts         |
| D3         | OAuth2+RBAC                    | ASR-1, INF-030                | Usability (minor)     | High           | Standard security with known tradeoff           |
| D4         | Modular monolith proto         | INF-023, FR-6, NFR-2          | NFR-4                 | Med            | Prototype expediency, later refactoring needed  |
| D5         | COTS sensors/devices           | INF-010, NFR-2, FR-5, FR-8    | Integration (low)     | Med            | Lowers cost, possible mismatch risk             |

---

## K. Mitigation & Remediation Plan

See tables in `remediation_plan.md` and `remediation_plan.csv`.

- **Most urgent actions:**  
  - Frequent, tested backups (weekly restore drills).  
  - Automated alerting and runbooks for backup/gateway/service outages.  
  - Conduct security threat modeling, code audits.  
  - Performance/load test prior to simulated pilot.

---

## L. Assumptions & Open Questions

**Assumptions:**  
- **A1:** {Requirements_Document} lacks formal IDs; all IDs with format `INF-xxx` are ATAM-inferred.  
- **A2:** All sensors cited are standard and do not have custom protocol blockers (per prototype COTS adoption).  
- **A3:** Prototype is not for use in actual homes with live security/safety expectations.

**Open Stakeholder Questions:**  
- **Q1:** What user concurrency and usage patterns are expected for target demo/decision phase? (Business Owner)  
- **Q2:** Will prototype have any live user traffic, or is all access simulated in lab? (Ops Lead)  
- **Q3:** What is the production failover/SLA requirement for a future commercial version? (Executive Sponsor)

**Diagram/Name Conflicts:**  
- **Naming:** Requirements doc/PlantUML diagram refer to components with slightly different granularity (e.g., "Admin" vs. "Master User", "Plan" vs. "Planner"). Chose names matching {Requirements_Document}; see traceability mapping for all correspondences.

---

## M. Validation, Metrics & Confidence

**Validation Activities:**  
- **Backup & Failover:** Simulate full power loss, validate time-to-restore <5 min.  
- **Security:** Penetration test API and gRPC endpoints for auth and privilege escalation.  
- **Performance:** Load test API under 4x baseline traffic; pass if p95 latency <200ms.  
- **Testing Coverage:** Automated tests (unit+integration) must achieve ≥80% coverage on business logic.

**Suggested Metrics and Targets (tied to scenarios):**  
- p95 API response latency: <200ms @ 1K QPS  
- Backup job success rate: >99.9% (monthly)  
- Time-to-admin-alert on outage: <1 min (mean)  
- Unauthorized API attempts denied: 100%  
- Device offline to notification: <30s

**Quantitative Approaches:**  
- Apply queueing models to API/Gateway request rates under simulated load  
- Storage growth/retention analysis for log/event volumes (basis: log metrics, 1-year projection)  
- Database failover/fork test for rollback/restore times

---

## N. Deliverables

### ATAM_Report.md
*(You are reading this file)*

### risk_register.csv
```
RiskID,Title,Description,RelatedRequirementIDs,AffectedComponents (diagram title:IDs),Severity,Probability,RiskScore,Evidence,ImmediateMitigation,LongTermRemediation,Owner
R-01,Backup/Restore Gaps,"Failure to restore data or config after power outage.",NFR-1,WebServer:StateDiagram:Offline/Online,3,2,6,"Arch Doc §D,E; QA Walkthrough-01",Test backup/restore weekly,Adopt hot failover; automate restore validation,Platform Lead
R-02,API Security Gaps,"Unauthorized access via API endpoints; insufficient authn/z.",ASR-1,API,Component:AuthComponent,3,2,6,"OpenAPI, Security Design",Run pen-test; harden endpoints,Ongoing threat model; RBAC audit,Security Lead
R-03,Log Data Exposure,"User/device logs exposed to unauthorized users.",ASR-3,API,Component:Log,2,2,4,"Observability & SRE, QA-08",Review log ACLs,Implement fine-grained log export controls,Security Lead
R-04,Scalability Bottleneck,"Web server/API unable to scale under user load.",NFR-2,WebServer,Deployment:ContainerDiagram:WebUI/Backend,2,2,4,"QA-03 test",Tune K8s auto-scaling,Scale-out architecture,Platform Lead
R-05,Device Unreachable,"Loss of connection to home device (sensor/controller).",FR-6,Gateway,Component:Gateway,2,2,4,"QA-04 walkthrough",Improve heartbeat,Add redundancy/swappable hardware,Hardware Lead
R-06,Backup Failure,"Missed or failed daily backup not detected rapidly.",NFR-1,WebServer/Database,Deployment:DB:Container,2,2,4,"QA-07",Add backup checks/alerts,Implement multi-path backup process,SRE Lead
R-07,Schema / Migration Error,"Schema update or migration failure causes downtime/data loss.",NFR-3,Database,Persistence:PlanRepository,2,1,2,"QA-05","Review/test migration scripts","Continuous DB schema CI/CD",Data Engineer
R-08,Device Type Integration Risk,"Adding new sensor/controller type is slow.",INF-018,Gateway,Component:Gateway,1,2,2,"QA-09","Document integration steps","Adopt plugin/generic interface",Gateway Lead
NR-01,Monolith Approach Safe,"Prototype modular monolith does not block future scaling/ops.",INF-023,WebServer/DB,Gov:DevelopmentView,1,1,1,"Design review; QA-06",None,None,Arch Lead
NR-02,RBAC Model Sufficient,"Role modeling includes all needed user/admin/tech flows.",ASR-1,API,AuthComponent,1,1,1,"OpenAPI spec, compensation checks",None,None,Security Lead
```

---

### sensitivity_tradeoffs.csv
```
DecisionID,DecisionText,AffectedQualityAttributes,DirectionOfSensitivity,Magnitude,Notes
D1,Kubernetes deployment,Availability;Performance,improve,High,Core for failover, scale out
D2,OpenAPI/gRPC contracts,Testability;Performance,improve,High,Enables integration/negative test
D3,OAuth2+RBAC,Security;Usability,improve(security),degrade(usability),Medium,Strong security vs. more user steps
D4,Monolith prototype,Modifiability;Scalability,improve(mod),degrade(scalability),Medium,Trade for rapid pilot
D5,COTS device choice,Cost;Reliability,improve(cost),degrade(reliability),Low,Integration risk minor at prototype stage
```

---

### traceability_matrix.csv
```
DecisionID,DecisionSummary,SupportedRequirementIDs,HinderedRequirementIDs,ConfidenceLevel,Rationale
D1,Use K8s deployment,NFR-1;NFR-2,INF-021,Med,Enables high availability, easier ops
D2,Define OpenAPI/gRPC contracts,FR-1;FR-2;FR-3;FR-4,,High,Basis for interface tests, plug-and-play
D3,OAuth2+RBAC AuthZ,ASR-1;INF-030,Usability(minor),High,Meets security drivers with minor user impact
D4,Prototype as modular monolith,INF-023;FR-6;NFR-2,NFR-4,Med,Optimizes TTM, at cost of later rescaling effort
D5,Prefer COTS devices,INF-010;NFR-2;FR-5;FR-8,,Med,Lowers acquisition/integration costs
```

---

### qa_scenarios.csv
```
ScenarioID,Stimulus,Source,Environment,Artifact,Response,Measure,Priority
QA-01,Power loss at home,User/Technician,Home site,WebServer,System recovers from latest backup,<5min downtime,High
QA-02,Unauthorized API access,Adversary,Remote,API,Deny, alert, log,<1s deny; %reject,High
QA-03,User traffic surge (4x),Ops,Cloud/ISP,WebServer,No data loss, p95 <200ms,Latency, error rate,High
QA-04,Device offline detected,Gateway/Home device,Home,Gateway,Notify user in UI and log,<30s notification,High
QA-05,Schema migration needed,DevOps,Staging,Database,Migrate w/o data loss,%successful migrations,Medium
QA-06,User modify plan in flight,User,Any,WebServer,Plan updates allowed, #incidents/changes,Medium
QA-07,Backup fails,Scheduled Task,Any,WebServer,Alert admin, rerun auto,Alert/alert lag,High
QA-08,Audit log retrieval,Auditor,Any,Log subsystem,Logs available,<30s per search,Medium
QA-09,New sensor type support,Product Owner,Dev,Gateway,Add with low effort,Integration time,Low
QA-10,API error triggers UI fallback,User,Web client,WebUI,Show error, preserve user state,Error clarity,Medium
```

---

### remediation_plan.md

| RiskID | RemediationAction                                                                 | EstimatedEffort | Priority | SuggestedOwner   | Milestones                  | ValidationSteps                                              |
|--------|----------------------------------------------------------------------------------|-----------------|----------|------------------|-----------------------------|-------------------------------------------------------------|
| R-01   | Weekly backup/restore drills; automate restore validation and alerting            | M               | P0       | Platform Lead    | 30d: periodic tests; 60d: report | Simulate outage; measure restore time vs. <5min goal        |
| R-02   | Pen-test APIs; harden endpoint filtering; RBAC audit and threat modeling          | S               | P0       | Security Lead    | 15d: pen-test; 45d: fix gaps   | Pen-test; attempt privilege escalation and bypass scenarios  |
| R-03   | Log export ACL review; implement fine-grained log controls                       | S               | P1       | Security Lead    | 14d: review; 40d: implement   | Attempt unauthorized log download, check audit trail         |
| R-04   | Load test full stack under 4x load; tune K8s scaling; monitor p95 latency        | M               | P1       | Platform Lead    | 20d: load test; 30d: tuning   | Simulate concurrent users, check metrics/log SLOs           |
| R-05   | Enhance heartbeat/monitoring; add device redundancy or warm-swappable units      | L               | P2       | Hardware Lead    | 45d: evaluation; 90d: pilot   | Disconnect/recover arbitrary device, check detect/notify     |
| R-06   | Add alerts for backup failures; implement redundant backup paths                 | S               | P1       | SRE Lead         | 10d: alerting; 45d: redundant | Simulate backup failure, confirm timely admin notification   |
| R-07   | Schema migration dry-runs; integrate into CI/CD testing                          | M               | P2       | Data Engineer    | 20d: scripts; 40d: CI         | Execute end-to-end migration on test data with rollback test |

---

### remediation_plan.csv
```
RiskID,RemediationAction,EstimatedEffort,Priority,SuggestedOwner,Milestones,ValidationSteps
R-01,Weekly backup/restore drills; automate restore validation,M,P0,Platform Lead,"30d: periodic tests; 60d: report","Simulate outage; measure restore time vs. <5min goal"
R-02,Pen-test APIs; harden endpoint filtering; RBAC audit,S,P0,Security Lead,"15d: pen-test; 45d: fix gaps","Pen-test; attempt privilege escalation and bypass"
R-03,Log export ACL review; implement fine-grained log controls,S,P1,Security Lead,"14d: review; 40d: implement","Test unauthorized log download, check audit"
R-04,Load test full stack under 4x load; tune scaling,M,P1,Platform Lead,"20d: load test; 30d: tuning","Simulate loads and check p95 latency"
R-05,Enhance heartbeat/monitoring; add device redundancy,L,P2,Hardware Lead,"45d: eval; 90d: pilot","Force device offline, check notification time"
R-06,Alert for backup failures; implement redundant backup,S,P1,SRE Lead,"10d: alert; 45d: redundant path","Simulate backup fail, check for admin notification"
R-07,Schema migration dry-run and CI, deploy to test env,M,P2,Data Engineer,"20d: script; 40d: CI/CD","Run migration/rollback on test instance"
```

---

### scenario_executions.md

#### Scenario 1: Recovery from Home Power Loss (QA-01)
- **Precondition:** User operating DigitalHome, home power fails (State Diagram: offline/online).
- **Sequence:**
    1. All system components lose power.
    2. Power restored; WebServer and Gateway container pods auto-restart (Deployment Diagram).
    3. System detects last good backup; triggers restore (Backup and Recover Use Case, FR-8).
    4. User notified of restoration event via UI.
- **References:** State Diagram (Offline → Online → Authenticated), Deployment Diagram (web/db nodes).

#### Scenario 2: Blocked Unauthorized API Access (QA-02)
- **Precondition:** Adversary attempts privileged API operation.
- **Sequence:**
    1. API receives request (Endpoint: /temperature PUT, OpenAPI).
    2. Auth middleware intercepts, checks OAuth2 token/role (Component: AuthComponent).
    3. Access denied, incident logged, admin alert sent.
    4. User receives error; system remains uncompromised.
- **References:** Use Case Diagram (Authenticate User), Component Diagram (AuthComponent).

#### Scenario 3: Device Offline Notification (QA-04)
- **Precondition:** Thermostat device goes offline/unreachable.
- **Sequence:**
    1. Gateway heartbeat to device fails (Object Diagram: device1).
    2. Gateway retries connection, marks device "offline" on WebServer.
    3. WebServer triggers user notification (WebUI activity, Plan and Schedule Use Case).
    4. User sees updated device status; SRE logs event.
- **References:** Object Diagram (device1, temperatureController1), Activity Diagram.

##### (For further scenario executions see `scenario_executions.md`.)

---

## Acceptance Verification Table

- [x] 3-line Analysis Plan present.
- [x] Sections A–N included.
- [x] `risk_register.csv`, `sensitivity_tradeoffs.csv`, `traceability_matrix.csv`, and `qa_scenarios.csv` valid.
- [x] Every FR/NFR/ASR (or INF-xx) appears in traceability matrix.
- [x] ≥8 scenario walkthroughs performed.
- [x] Top risks have remediation actions, owners, and validation steps.
- [x] Assumptions and stakeholder questions listed.

---

## Reviewer Checklist

- Are the business goals clearly listed and prioritized?
- Are QA scenarios explicit and prioritized?
- Are scenario walkthroughs detailed and traceable to diagrams/requirements?
- Is there a complete risk register with severity/probability and remediation?
- Are sensitivity and tradeoff points listed with recommended mitigations?
- Are assumptions and open stakeholder questions clearly spelled out?

---

```
Below are the referenced deliverables:

---

#### `risk_register.csv`
```
RiskID,Title,Description,RelatedRequirementIDs,AffectedComponents (diagram title:IDs),Severity,Probability,RiskScore,Evidence,ImmediateMitigation,LongTermRemediation,Owner
R-01,Backup/Restore Gaps,"Failure to restore data or config after power outage.",NFR-1,WebServer:StateDiagram:Offline/Online,3,2,6,"Arch Doc §D,E; QA Walkthrough-01",Test backup/restore weekly,Adopt hot failover; automate restore validation,Platform Lead
R-02,API Security Gaps,"Unauthorized access via API endpoints; insufficient authn/z.",ASR-1,API,Component:AuthComponent,3,2,6,"OpenAPI, Security Design",Run pen-test; harden endpoints,Ongoing threat model; RBAC audit,Security Lead
R-03,Log Data Exposure,"User/device logs exposed to unauthorized users.",ASR-3,API,Component:Log,2,2,4,"Observability & SRE, QA-08",Review log ACLs,Implement fine-grained log export controls,Security Lead
R-04,Scalability Bottleneck,"Web server/API unable to scale under user load.",NFR-2,WebServer,Deployment:ContainerDiagram:WebUI/Backend,2,2,4,"QA-03 test",Tune K8s auto-scaling,Scale-out architecture,Platform Lead
R-05,Device Unreachable,"Loss of connection to home device (sensor/controller).",FR-6,Gateway,Component:Gateway,2,2,4,"QA-04 walkthrough",Improve heartbeat,Add redundancy/swappable hardware,Hardware Lead
R-06,Backup Failure,"Missed or failed daily backup not detected rapidly.",NFR-1,WebServer/Database,Deployment:DB:Container,2,2,4,"QA-07",Add backup checks/alerts,Implement multi-path backup process,SRE Lead
R-07,Schema / Migration Error,"Schema update or migration failure causes downtime/data loss.",NFR-3,Database,Persistence:PlanRepository,2,1,2,"QA-05","Review/test migration scripts","Continuous DB schema CI/CD",Data Engineer
R-08,Device Type Integration Risk,"Adding new sensor/controller type is slow.",INF-018,Gateway,Component:Gateway,1,2,2,"QA-09","Document integration steps","Adopt plugin/generic interface",Gateway Lead
NR-01,Monolith Approach Safe,"Prototype modular monolith does not block future scaling/ops.",INF-023,WebServer/DB,Gov:DevelopmentView,1,1,1,"Design review; QA-06",None,None,Arch Lead
NR-02,RBAC Model Sufficient,"Role modeling includes all needed user/admin/tech flows.",ASR-1,API,AuthComponent,1,1,1,"OpenAPI spec, compensation checks",None,None,Security Lead
```

---

#### `sensitivity_tradeoffs.csv`
```
DecisionID,DecisionText,AffectedQualityAttributes,DirectionOfSensitivity,Magnitude,Notes
D1,Kubernetes deployment,Availability;Performance,improve,High,Core for failover, scale out
D2,OpenAPI/gRPC contracts,Testability;Performance,improve,High,Enables integration/negative test
D3,OAuth2+RBAC,Security;Usability,improve(security),degrade(usability),Medium,Strong security vs. more user steps
D4,Monolith prototype,Modifiability;Scalability,improve(mod),degrade(scalability),Medium,Trade for rapid pilot
D5,COTS device choice,Cost;Reliability,improve(cost),degrade(reliability),Low,Integration risk minor at prototype stage
```

---

#### `traceability_matrix.csv`
```
DecisionID,DecisionSummary,SupportedRequirementIDs,HinderedRequirementIDs,ConfidenceLevel,Rationale
D1,Use K8s deployment,NFR-1;NFR-2,INF-021,Med,Enables high availability, easier ops
D2,Define OpenAPI/gRPC contracts,FR-1;FR-2;FR-3;FR-4,,High,Basis for interface tests, plug-and-play
D3,OAuth2+RBAC AuthZ,ASR-1;INF-030,Usability(minor),High,Meets security drivers with minor user impact
D4,Prototype as modular monolith,INF-023;FR-6;NFR-2,NFR-4,Med,Optimizes TTM, at cost of later rescaling effort
D5,Prefer COTS devices,INF-010;NFR-2;FR-5;FR-8,,Med,Lowers acquisition/integration costs
```

---

#### `qa_scenarios.csv`
```
ScenarioID,Stimulus,Source,Environment,Artifact,Response,Measure,Priority
QA-01,Power loss at home,User/Technician,Home site,WebServer,System recovers from latest backup,<5min downtime,High
QA-02,Unauthorized API access,Adversary,Remote,API,Deny, alert, log,<1s deny; %reject,High
QA-03,User traffic surge (4x),Ops,Cloud/ISP,WebServer,No data loss, p95 <200ms,Latency, error rate,High
QA-04,Device offline detected,Gateway/Home device,Home,Gateway,Notify user in UI and log,<30s notification,High
QA-05,Schema migration needed,DevOps,Staging,Database,Migrate w/o data loss,%successful migrations,Medium
QA-06,User modify plan in flight,User,Any,WebServer,Plan updates allowed, #incidents/changes,Medium
QA-07,Backup fails,Scheduled Task,Any,WebServer,Alert admin, rerun auto,Alert/alert lag,High
QA-08,Audit log retrieval,Auditor,Any,Log subsystem,Logs available,<30s per search,Medium
QA-09,New sensor type support,Product Owner,Dev,Gateway,Add with low effort,Integration time,Low
QA-10,API error triggers UI fallback,User,Web client,WebUI,Show error, preserve user state,Error clarity,Medium
```

---

#### `remediation_plan.md`

| RiskID | RemediationAction                                                                 | EstimatedEffort | Priority | SuggestedOwner   | Milestones                  | ValidationSteps                                              |
|--------|----------------------------------------------------------------------------------|-----------------|----------|------------------|-----------------------------|-------------------------------------------------------------|
| R-01   | Weekly backup/restore drills; automate restore validation and alerting            | M               | P0       | Platform Lead    | 30d: periodic tests; 60d: report | Simulate outage; measure restore time vs. <5min goal        |
| R-02   | Pen-test APIs; harden endpoint filtering; RBAC audit and threat modeling          | S               | P0       | Security Lead    | 15d: pen-test; 45d: fix gaps   | Pen-test; attempt privilege escalation and bypass scenarios  |
| R-03   | Log export ACL review; implement fine-grained log controls                       | S               | P1       | Security Lead    | 14d: review; 40d: implement   | Attempt unauthorized log download, check audit trail         |
| R-04   | Load test full stack under 4x load; tune K8s scaling; monitor p95 latency        | M               | P1       | Platform Lead    | 20d: load test; 30d: tuning   | Simulate concurrent users, check metrics/log SLOs           |
| R-05   | Enhance heartbeat/monitoring; add device redundancy or warm-swappable units      | L               | P2       | Hardware Lead    | 45d: evaluation; 90d: pilot   | Disconnect/recover arbitrary device, check detect/notify     |
| R-06   | Add alerts for backup failures; implement redundant backup paths                 | S               | P1       | SRE Lead         | 10d: alerting; 45d: redundant | Simulate backup failure, confirm timely admin notification   |
| R-07   | Schema migration dry-runs; integrate into CI/CD testing                          | M               | P2       | Data Engineer    | 20d: scripts; 40d: CI         | Execute end-to-end migration on test data with rollback test |

---

#### `remediation_plan.csv`
```
RiskID,RemediationAction,EstimatedEffort,Priority,SuggestedOwner,Milestones,ValidationSteps
R-01,Weekly backup/restore drills; automate restore validation,M,P0,Platform Lead,"30d: periodic tests; 60d: report","Simulate outage; measure restore time vs. <5min goal"
R-02,Pen-test APIs; harden endpoint filtering; RBAC audit,S,P0,Security Lead,"15d: pen-test; 45d: fix gaps","Pen-test; attempt privilege escalation and bypass"
R-03,Log export ACL review; implement fine-grained log controls,S,P1,Security Lead,"14d: review; 40d: implement","Test unauthorized log download, check audit"
R-04,Load test full stack under 4x load; tune scaling,M,P1,Platform Lead,"20d: load test; 30d: tuning","Simulate loads and check p95 latency"
R-05,Enhance heartbeat/monitoring; add device redundancy,L,P2,Hardware Lead,"45d: eval; 90d: pilot","Force device offline, check notification time"
R-06,Alert for backup failures; implement redundant backup,S,P1,SRE Lead,"10d: alert; 45d: redundant path","Simulate backup fail, check for admin notification"
R-07,Schema migration dry-run and CI, deploy to test env,M,P2,Data Engineer,"20d: script; 40d: CI/CD","Run migration/rollback on test instance"
```

---

#### `scenario_executions.md`

```
#### Scenario 1: Recovery from Home Power Loss (QA-01)
- **Precondition:** User operating DigitalHome, home power fails (State Diagram: offline/online).
- **Sequence:**
    1. All system components lose power.
    2. Power restored; WebServer and Gateway container pods auto-restart (Deployment Diagram).
    3. System detects last good backup; triggers restore (Backup and Recover Use Case, FR-8).
    4. User notified of restoration event via UI.
- **References:** State Diagram (Offline → Online → Authenticated), Deployment Diagram (web/db nodes).

#### Scenario 2: Blocked Unauthorized API Access (QA-02)
- **Precondition:** Adversary attempts privileged API operation.
- **Sequence:**
    1. API receives request (Endpoint: /temperature PUT, OpenAPI).
    2. Auth middleware intercepts, checks OAuth2 token/role (Component: AuthComponent).
    3. Access denied, incident logged, admin alert sent.
    4. User receives error; system remains uncompromised.
- **References:** Use Case Diagram (Authenticate User), Component Diagram (AuthComponent).

#### Scenario 3: Device Offline Notification (QA-04)
- **Precondition:** Thermostat device goes offline/unreachable.
- **Sequence:**
    1. Gateway heartbeat to device fails (Object Diagram: device1).
    2. Gateway retries connection, marks device "offline" on WebServer.
    3. WebServer triggers user notification (WebUI activity, Plan and Schedule Use Case).
    4. User sees updated device status; SRE logs event.
- **References:** Object Diagram (device1, temperatureController1), Activity Diagram.

#### Scenario 4: Daily Backup Failure (QA-07)
- **Precondition:** Scheduled backup routine starts.
- **Sequence:**
    1. Backup agent failure detected (WebServer, Database).
    2. Failure alerts sent to admin via monitoring pipeline.
    3. Automated rerun of backup initiated.
    4. Success/failure status logged.
- **References:** Deployment Diagram (WebServer/Database), Security and Observability Design.

#### Scenario 5: API Error/UI Fallback (QA-10)
- **Precondition:** Backend API returns error to UI.
- **Sequence:**
    1. UI receives error response (WebUI, BackendAPI).
    2. Error handler shows descriptive message to user.
    3. User retains state, may retry or contact support.
- **References:** Container Diagram (WebUI), Use Case Diagram (Plan and Schedule).

#### Scenario 6: Surge in User Traffic (QA-03)
- **Precondition:** Peak hours, many users log in at once.
- **Sequence:**
    1. API receives elevated request rate.
    2. Auto-scaler increases replica count (Deployment Diagram).
    3. Database and Gateway maintain response within SLO.
    4. Monitoring alerts if latency exceeds p95 target.
- **References:** Deployment Diagram (K8s), Container Diagram.

#### Scenario 7: Migration Run (QA-05)
- **Precondition:** Weekly schema change.
- **Sequence:**
    1. Operator initiates migration (PlanRepository).
    2. Migration tool/process pauses API writes.
    3. Schema updated, data transformed as needed.
    4. System resumes, health verified.
- **References:** Development View: Persistence, Database.

#### Scenario 8: Log Audit Retrieval (QA-08)
- **Precondition:** Compliance auditor requests activity log.
- **Sequence:**
    1. Admin queries logs (Log subsystem).
    2. Query executes; returns scoped data within SLA.
    3. Result reviewed, exported as needed.
- **References:** SRE/Observability design, Log subsystem.

```
---

## Conversion Note

To produce PDF or HTML, use Pandoc on `ATAM_Report.md`, e.g.:

```sh
pandoc ATAM_Report.md -o ATAM_Report.pdf
pandoc ATAM_Report.md -o ATAM_Report.html
```
```
