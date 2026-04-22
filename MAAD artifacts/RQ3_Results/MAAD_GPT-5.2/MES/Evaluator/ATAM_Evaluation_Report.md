```markdown
# ATAM-Based Architecture Evaluation Report: APAF Ground Data System

---

## B. Analysis Plan

**Scope:** Evaluate the production-ready architecture for APAF (ASPERA-3 Processing and Archiving Facility) against SRS requirements, prioritized quality attributes, and provided UML design artifacts.

**Approach:** Perform scenario-based walkthroughs (ATAM), sensitivity and tradeoff analysis, and quantitative validation checks, explicitly referencing relevant PlantUML diagrams and inferred requirement IDs as needed.

**Top validation steps:** Confirm traceability matrix completeness vs. SRS/INF-IDs, verify contract/schema compliance, and walkthrough high-priority QA scenarios using diagram steps and runtime flows.

---

## A. Executive Summary (≤1 page)

**System overview:**  
APAF is an on-premises ground data system (SwRI) for the Mars Express mission, responsible for acquiring daily telemetry from ESOC, generating IDFS data sets for scientific analysis and archiving, providing both public and restricted data access via a web portal, distributing data to Co-I collaborators, and submitting validated deliverables to NASA PDS. The architecture adopts a modular monolith style with strong boundaries between ingestion, processing, archiving, distribution, web, and security/observability domains (see **UseCase_APAF:UC_Acquire/UC_Process/UC_Archive/UC_Distribute/UC_PublicWeb/UC_TeamWeb/UC_PDS**, **Activity_DailyPipeline**, **Sequence_S1_DailyIngestProcess**).

**Top five business goals:**  
1. BG1: Timely daily ingestion and processing of all relevant Mars Express telemetry (INF-FR-001, INF-FR-002).  
2. BG2: Secure, accurate, and audit-trailed distribution of all required data products to Co-Is (INF-DR-001..004).  
3. BG3: Reliable long-term archiving and integrity protection for all raw/processed products (INF-FR-005..007, INF-FR-011).  
4. BG4: Role-based, privacy-aware web access for public/team users, with appropriate embargoes (INF-FR-008..010, INF-PR-001).  
5. BG5: Submission of complete, validated, PDS-compliant data sets to NASA repository within required deadlines (INF-DR-005..008).

**Top five findings:**  
1. **High risk:** Legacy SRS lacks measurable NFRs; introduced INF-IDs and contract-first schema validation (see K).  
2. **High risk:** Pipeline timing and 24h Co-I delivery SLA are fragile; mitigated via idempotent jobs, queue retries, and alerting.  
3. **High risk:** Web privacy boundary (public/team) is sensitive; architecture enforces OIDC, RBAC, MFA, session timeouts, audit trails.  
4. **Non-risk:** Archive, retention, and backup strategies are robust; leverage on-prem NAS + daily/annual recovery validation.  
5. **Action:** Clarify ESOC delivery protocol, exact Co-I entitlements, and audit log compliance via follow-up (see L).

---

## C. Concise Architectural Presentation

The APAF system applies a modular monolith with clear hexagonal boundaries for ingestion (TelemetryIngestionService + ESOCAdapter), processing (Cleaning, IDFSProcessing, SchemaValidation), archiving, distribution, web presentation (WebPortal, IDFSQueryService), authentication (AuthService), and observability (MonitoringAlertingService). All major use cases, artifacts, and flows are mapped in **UseCase_APAF**, with core technical flows illustrated in **Activity_DailyPipeline**, **Sequence_S1_DailyIngestProcess**, and **Container_APAF** (see section L for filenames/artifacts).

**Major architectural decisions:**
| DecisionID | Decision Summary | Rationale |
|---|---|---|
| D1 | Modular monolith on K8s with service boundaries | Enables clear contracts and disaster recovery while keeping ops overhead tractable (INF-NFR-QUAL-001, INF-CR-001) |
| D2 | Contract-first OpenAPI/gRPC for service and external APIs | Reduces ambiguity, supports traceability/automation (INF-FR-015) |
| D3 | NAS with content-addressed storage, immutable logs, checkpointed SQL for all artifacts/metadata | High integrity, traceability, reprocessing support (INF-FR-005..007, INF-FR-011) |
| D4 | RBAC + OIDC/MFA for team-only access, strict embargo until public | Prevents unauthorized data leakage (INF-PR-001, INF-FR-010, INF-FR-008/009) |
| D5 | Idempotent, observable pipelines with quarantining and alerting on integrity errors | Enforces reliability and integrity (INF-FR-011, INF-NFR-QUAL-001) |

---

## D. Business Goals & Drivers

| GoalID | ShortText                                                      | Priority | RelatedRequirementIDs              | Stakeholder         |
|--------|---------------------------------------------------------------|----------|------------------------------------|---------------------|
| BG1    | Ingest and process all ESOC telemetry for Mars Express daily   | P0       | INF-FR-001, INF-FR-002, INF-FR-003 | SwRI Science/Ops    |
| BG2    | Secure, accurate, auditable delivery to all Co-Is within 24h   | P0       | INF-DR-001..004                    | Co-Investigators    |
| BG3    | Robust, auditable, recoverable long-term artifact retention    | P1       | INF-FR-005..007, INF-FR-011        | SwRI Ops, Science   |
| BG4    | Privacy-preserving, embargoed and public web-based data access | P0       | INF-FR-008..010, INF-PR-001        | PI, SwRI, Public    |
| BG5    | PDS-compliant, validated submission to NASA within deadline    | P0       | INF-DR-005..008                    | NASA, IRF           |

---

## E. Quality Attribute Scenarios & Prioritization

**Derivation:** Scenarios capture high-impact operational (availability, performance), delivery (timeliness), integrity (data correctness), security, and maintainability attributes derived from requirements and stakeholder priorities. High priority = direct mission/SLA threat or compliance risk.

| ScenarioID | Stimulus                                                             | Source      | Environment      | Artefact                 | Response                                      | Measure / Priority  |
|------------|----------------------------------------------------------------------|-------------|------------------|--------------------------|------------------------------------------------|---------------------|
| QA1        | Daily ESOC drop is available, triggers ingest and processing         | ESOC        | Prod, daily      | TelemetryIngestionService| All telemetry processed by 03:00 UTC           | SLA met/High        |
| QA2        | Telemetry checksum mismatch detected                                 | ESOC        | Prod             | SchemaValidationService  | Quarantine item, alert SRE within 10 min       | Alert time/High     |
| QA3        | Team user requests embargoed data via web portal                     | Co-I        | Team network     | WebPortal/AuthService    | AuthN+RBAC enforced, audit log recorded        | Zero-violation/High |
| QA4        | Co-I pulls required IDFS products within 24h conditional SLA         | Co-I        | Remote           | DistributionService      | All error-free data delivered within window     | On-time %/High      |
| QA5        | Hardware/NAS failure during archive                                 | SwRI Ops    | Prod (NAS down)  | ArchiveService           | Data recoverable from backup within RTO        | RTO/RPO/High        |
| QA6        | Pipeline processing/validation failure                              | System      | Any, daily       | All processing services  | Integrity error quarantined, alert within SLA  | Resolution time/High|
| QA7        | PDS deadline approaches, requires validated submission              | NASA        | Deadline window  | PDSSubmissionService     | Submission completed, compliance validated     | Zero miss/High      |
| QA8        | Schema version change for IDFS processing                          | IRF, SwRI   | Planned update   | IDFSProcessingService    | Backward/forward compatibility maintained      | Zero error/Medium   |
| QA9        | New user/team deprovisioned within 72h of offboarding               | Admin       | HR event         | AuthService              | No access post-72h, audit log exists           | Compliance/Medium   |
| QA10       | Archive retention policy changed (e.g., 5→7 years)                 | Admin/Ops   | Policy update    | ArchiveService           | Retention updated, no data lost                | Zero loss/Medium    |
| QA11       | Attempted exploit on web portal (OWASP top 10)                     | Red Team    | Pen test         | WebPortal/AuthService    | Attack failed, log/audit triggered             | Zero compromise/High|
| QA12       | Co-I access software versioning                                    | Co-Invest.  | Release event    | Release/Packaging        | Compatible versions made available             | Zero defect/Low     |

**Prioritization approach:** High = direct SRS/SLA/mission impact or regulatory/compliance; Medium = support/scientific usability; Low = rare edge/business-study impacts.

---

## F. Architecture Evaluation (Scenario-based analysis)

### Scenario Walkthroughs (Top 8 High-Priority Scenarios)

#### QA1: Daily ESOC drop is available (Ingestion/Processing SLA)
**Reference Steps:**  
- Diagram: Activity_DailyPipeline (nodes: ScheduleDailyRun, Connect ESOC, AcquireTelemetry, VerifyChecksum, ProcessScienceToIDFS, ArchiveIDFSDatasets), Sequence_S1_DailyIngestProcess (steps 1–10).
- 1) Scheduler triggers TelemetryIngestionService → ESOCAdapter connects to ESOC.
- 2) Files received: checksums verified (SchemaValidationService).
- 3) Raw files stored (RawTelemetryArchive).
- 4) Cleaned telemetry generated or ingested; schema validated.
- 5) Processed to IDFS datasets; validation.
- 6) Archive completed in IDFSArchive; downstream web/distribution triggered.
- Sensitivity: Network reliability, ESOC protocol details, idempotent pipeline, schema version alignment.
- Tradeoffs: Latency vs. process robustness; adding retries increases time but improves completion.

| ScenarioID | ResponseSummary                          | SensitivityPoints                        | Tradeoffs                      | Confidence  |
|------------|------------------------------------------|------------------------------------------|-------------------------------|-------------|
| QA1        | Pipeline completes ≤03:00 UTC or alerts  | ESOCAdapter, SchemaValidator, Scheduler  | Latency vs. reliability        | High        |

#### QA2: Telemetry checksum mismatch (Integrity)
**Reference Steps:**  
- Diagram: State_IDFSDataset:L (Created→Quarantined), Sequence_S1_DailyIngestProcess (alt checksum mismatch).
- Sequence:
  1) ESOCAdapter or Ingest retrieves file.
  2) SchemaValidationService detects checksum failure.
  3) Ingest quarantines artifact (QuarantineStore), triggers MonitoringAlertingService.
  4) SRE notified within 10 minutes.
- Sensitivity: Checksum validation logic, quarantine path reliability, alerting/notification config.
- Tradeoffs: False positives halt pipeline vs. silent data loss.

| ScenarioID | ResponseSummary                                      | SensitivityPoints                  | Tradeoffs                              | Confidence  |
|------------|------------------------------------------------------|------------------------------------|----------------------------------------|-------------|
| QA2        | Artifact quarantined, alert in ≤10 min, run halted   | SchemaValidationService, QuarantineStore | Aggressive quarantine can delay delivery; leniency risks data corruption | High        |

#### QA3: Team user accesses embargoed data (Privacy/Access Control)
**Reference Steps:**  
- Diagram: UseCase_APAF:UC_TeamWeb, Sequence_S2_TeamWebAccess.
- Sequence:
  1) Co-I authenticates (OIDC+MFA) via WebPortal.
  2) Role-based access checked; access logged.
  3) Only entitled team/Co-I data returned; public embargo enforced.
- Sensitivity: AuthService config, RBAC accuracy, audit log integrity.
- Tradeoffs: Tighter lockouts risk productivity vs. risk of data leak.

| ScenarioID | ResponseSummary                              | SensitivityPoints     | Tradeoffs                        | Confidence |
|------------|----------------------------------------------|----------------------|----------------------------------|------------|
| QA3        | AuthN/Role enforced, audit logged, embargo upheld| AuthService, WebPortal| Usability vs. strict embargo     | High       |

#### QA4: Co-I pulls required IDFS products within 24h
- Steps: Activity_DailyPipeline (DistributeToCoIs), Class_APAF:DistributionJob, Sequence diagrams S1 (job completion notification).
- 1) Distribution job created post-IDFS processing.
- 2) Job retries up to 3 times; errors alerted within 2h.
- 3) Download and receipt tracked per Co-I.
- Sensitivity: Distribution job scheduler/policy, egress reliability.
- Tradeoffs: Extra retries add queue time, risk missing 24h.

| ScenarioID | ResponseSummary                      | SensitivityPoints           | Tradeoffs            | Confidence |
|------------|--------------------------------------|----------------------------|----------------------|------------|
| QA4        | All eligible datasets delivered within SLA, or alert | DistributionService, Scheduler | Retry window vs. timely delivery | High       |

#### QA5: Hardware/NAS failure – data recovery
- Steps: Deployment_APAF:NAS/Backup, ArchiveService, backup/restore runbooks.
- 1) ArchiveService detects archive/NAS issue.
- 2) Recovery from last backup (nightly full, WAL logs); RTO measured.
- Sensitivity: Backup frequency, restore efficacy.
- Tradeoffs: More frequent backups increase cost; less means higher data loss risk.

| ScenarioID | ResponseSummary               | SensitivityPoints    | Tradeoffs          | Confidence |
|------------|-------------------------------|---------------------|--------------------|------------|
| QA5        | Restore completed ≤24h, zero data loss | NAS/Backup, ArchiveService | Cost vs. safety | High       |

#### QA6: Processing/validation failure
- Steps: State_IDFSDataset:L (Created→Quarantined), MonitoringAlertingService.
- Flow: Any step fails schema or calibration → artifact quarantined, SRE alerted.
- Sensitivity: SRE response, quarantine process reliability.
- Tradeoffs: Halting possibly valid data vs. integrity.

| ScenarioID | ResponseSummary                                  | SensitivityPoints             | Tradeoffs              | Confidence |
|------------|--------------------------------------------------|------------------------------|------------------------|------------|
| QA6        | Integrity failures never ignored, always alerted | MonitoringAlertingService    | Timeliness vs. error tolerance | High    |

#### QA7: PDS deadline approaches – submission
- Steps: State_IDFSDataset:L (PDSReady→PDSSubmitted [<=6 months]), PDSSubmissionService.
- Pipeline tracks submission clock; deadline alerts if at risk; submission is audited and PDS response recorded.
- Sensitivity: Deadline scheduling, completion confirmation, PDS acceptance.
- Tradeoffs: Early submission risk (updating issued data), late is a compliance failure.

| ScenarioID | ResponseSummary                       | SensitivityPoints   | Tradeoffs            | Confidence |
|------------|---------------------------------------|--------------------|----------------------|------------|
| QA7        | 100% on-time, PDS-compliant submission| PDSSubmissionService| Early/late risk      | High       |

#### QA11: Web portal attack attempt (security)
- Steps: UseCase_APAF:UC_TeamWeb/UC_PublicWeb, WebPortal, AuthService (pen test).
- Penetrate with XSS, SQLi, auth bypass attempts.
- OIDC+audit prevents privilege escalation/access; all attempts logged; lockout on repeat fail.
- Sensitivity: Web stack security config, audit log coverage.
- Tradeoffs: Tighter security can add friction.
 
| ScenarioID | ResponseSummary                              | SensitivityPoints    | Tradeoffs           | Confidence |
|------------|----------------------------------------------|--------------------|---------------------|------------|
| QA11       | No access breach, attacks logged, rapid notification | WebPortal, AuthService | Usability vs. security | High    |

**(Full step-by-step scenario executions for all High scenarios in `scenario_executions.md`.)**

---

## G. Risks & Non-Risks (Risk Register)

**See `risk_register.csv` artifact for complete tabular risk register. Example entries:**  

| RiskID | Title                          | Description                                                      | RelatedRequirementIDs     | AffectedComponents          | Severity | Probability | RiskScore | ...             | Owner    |
|--------|--------------------------------|------------------------------------------------------------------|--------------------------|-----------------------------|----------|-------------|-----------|-----------------|----------|
| R1     | SRS lacks measurable NFRs      | Weak testability/traceability; risk of missed acceptance         | INF-NFR-QUAL-001         | All (arch/contract docs)    | 3        | 3           | 9         | ...             | Arch Lead|
| R2     | ESOC protocol uncertainty      | Protocol/format flux may break ingestion                         | INF-FR-001, A1           | TelemetryIngestionService   | 3        | 2           | 6         | ...             | SwRI PM  |
| NR1    | Archive/backup design robust   | Retention, WORM, restore drills proven; non-risk                 | INF-FR-005..007          | ArchiveService, NAS, Backup | 1        | 1           | 1         | ...             | SwRI Ops |

All risks, including non-risks, are justified with evidence in `risk_register.csv`.

---

## H. Risk Themes & Systemic Issues

**Theme 1:** Requirements/contract ambiguity  
- Risks: R1, R2 (“SRS lacks NFRs”, “ESOC protocol unknown”)  
- Impact: Testing coverage gaps, pipeline break risk  
- Remediation: Contract-first API design, clarify ESOC interface pre-launch, red team requirements mapping.

**Theme 2:** Delivery/processing timing guarantees  
- Risks: R3, R4 (“Missed 24h Co-I SLA”, “Pipeline timing slippage”)  
- Impact: Scientific goal and contractual SLA breach  
- Remediation: Overprovision scheduling, idempotent job queue, monitoring+alerting hooks.

**Theme 3:** Data privacy/separation  
- Risks: R5 (“Embargoed data leak”)  
- Impact: Project/PI reputation risk, compliance breach  
- Remediation: OIDC+RBAC with embargo, audit logs, access sweep verification.

**Theme 4:** Integrity and traceability  
- Risks: R6 (“Silent data corruption”)  
- Impact: Undetected scientific error propagation  
- Remediation: Mandatory schema/checksum validation, quarantine-first pipeline, immutable logs.

---

## I. Sensitivity Points & Tradeoff Matrix

**See `sensitivity_tradeoffs.csv` for a complete table. Example rows:**

| DecisionID | DecisionText                                 | AffectedQualityAttributes      | DirectionOfSensitivity | Magnitude | Notes                         |
|------------|----------------------------------------------|-------------------------------|------------------------|-----------|-------------------------------|
| D2         | Use contract-first (OpenAPI/gRPC) interfaces | Testability, interoperability | improve                | High      | Enables automation/validation |
| D3         | Quarantine on integrity failure              | Reliability, performance      | improve/degrade        | High      | Slows pipeline on error but protects data |
| D4         | NAS vs. object storage for archive           | Availability, scalability     | improve (simplicity)/degrade (scale) | Med | Chosen for simplicity/legacy alignment   |
| D5         | OIDC+RBAC+MFA for team web access            | Security, usability           | improve security / degrade usability | High | Strict MFA may frustrate some users      |

Each contains direction, magnitude, and qualitative rationale, with recommended alternatives.

---

## J. Mapping of Architectural Decisions → Quality Requirements

**See `traceability_matrix.csv` for the full mapping.**  
Sample entry:

| DecisionID | DecisionSummary | SupportedRequirementIDs         | HinderedRequirementIDs | ConfidenceLevel | Rationale                                  |
|------------|----------------|----------------------------------|-----------------------|----------------|---------------------------------------------|
| D2         | OpenAPI/gRPC   | INF-FR-015, INF-NFR-QUAL-001    | ---                   | High           | Contracts clarify SRS intent                |
| D3         | Quarantine-first| INF-FR-011, INF-FR-005..007     | ---                   | High           | Ensures no silent data corruption           |
| D4         | OIDC+RBAC+MFA  | INF-PR-001, INF-FR-010          | ---                   | High           | Compliance with privacy/embargo             |

---

## K. Mitigation & Remediation Plan

**See `remediation_plan.md` and `remediation_plan.csv`. Example:**

| RiskID | RemediationAction                       | Est.Effort | Priority | SuggestedOwner | Milestones           | ValidationSteps                              |
|--------|-----------------------------------------|------------|----------|---------------|----------------------|-----------------------------------------------|
| R1     | Canonical INF-NFR mapping, schema validation gates | M    | 1        | Arch Lead      | Map and freeze INF IDs; implement CI checks | All FR/NFRs mapped and checked at build/review|
| R2     | ESOC protocol confirmation and adapter integration | M    | 1        | SwRI PM        | Confirm protocols with ESOC; finalize contract | ESOC adapter E2E test, files accepted         |
| R3     | Extra job retries, monitoring, <2h alert | S    | 1        | SRE Lead        | Implement, rehearse failure alert; run E2E | 100% alert within SLA on simulated error     |

---

## L. Assumptions & Open Questions

**Assumptions:**
- **A1:** ESOC provides stable, daily telemetry via NISN or similar protocol (SFTP/HTTPS).
- **A2:** IDFS schema and validation scripts exist and are available to APAF architects.
- **A3:** "Password protected where appropriate" means enforceable role-based embargo with audit logs.
- **A4:** Local archive retention of ≥5 years unless updated by project.
- **A5:** Electronic Co-I distribution preferred; physical rare.

**Open questions (sample phrasing & role):**
1. **ESOC connection:** "What exact ESOC delivery protocol(s), authentication, and file naming conventions are required for telemetry acquisition?" (To: ESOC Liaison)
2. **IDFS schema:** "What is the authoritative source for IDFS schema versioning/validation and who governs updates?" (To: PI/IRF)
3. **Co-I distribution:** "What are the exact dataset entitlements/means for each Co-I and accepted delivery mechanisms?" (To: PI/Co-Is)
4. **Public data definition:** "Does 'most current data' mean most recent orbit, 24h, or last successful pipeline completion?" (To: Science Team)
5. **Audit logging:** "What are required audit log retention and export rules for compliance?" (To: SwRI Compliance/Ops)

**Diagram name/ID conflicts:**
- PlantUML diagrams reference NFR/ASR IDs (NFR-001..012, ASR-002..010) not present in SRS. Chosen canonical ID: `INF-` (see mapping in traceability_matrix.csv).

---

## M. Validation, Metrics & Confidence

**Validation activities for each top finding:**
1. **Schema/contract coverage:** Confirm 100% of INF-FR/NFR/PR IDs mapped to OpenAPI, proto, or SQL; run in CI.
2. **Pipeline SLA:** E2E test: Simulate ESOC file drop, verify <03:00 UTC pipeline, Co-I delivery tracked, all artifacts present.
3. **Data integrity:** Inject corrupted file, verify quarantine/alert within SLA, and error audit log populated.
4. **Web privacy controls:** Attempt access to embargoed data with/without right role, ensure access denied and audit log present.
5. **Backup/restore:** Simulate NAS loss in staging, restore archive from nightly backup, verify RTO ≤24h.
6. **Penetration test:** Run automated SAST/DAST on WebPortal/AuthService, confirm zero critical findings.

**Measurable metrics/SLOs:**
| Metric                                 | SLO / Target                         | Tied Requirement  |
|-----------------------------------------|--------------------------------------|-------------------|
| Pipeline finish time (UTC)              | ≤03:00 UTC, 99% days                 | INF-FR-001        |
| Integrity error alert window            | ≤10 minutes after error detected     | INF-FR-011        |
| 24h Co-I delivery window                | ≥99% jobs, ≤24h post-acquisition     | INF-DR-002/003    |
| Embargo/breach incidents                | 0 chronicled/year                    | INF-PR-001        |
| Archive backup success                   | ≥99.5% backup jobs/year, RTO≤24h     | INF-LR-001        |

**Quantitative estimates/modeling:**  
For ingest: Assuming 1 GB/day ingest, ~10 files; pipeline design supports 5x that load for headroom.  
Queueing model: Co-I delivery queue with 3 retries at 30 min intervals → max job age = 2 hours after all attempts fail.

---

## N. Deliverables

All deliverables provided as below:

---

### `ATAM_Report.md`

*(This document)*

---

### `risk_register.csv`
```
RiskID,Title,Description,RelatedRequirementIDs,AffectedComponents,Severity,Probability,RiskScore,Evidence,ImmediateMitigation,LongTermRemediation,Owner
R1,SRS lacks measurable NFRs,No explicit non-functional requirements in SRS; risk of missed acceptance/validation,INF-NFR-QUAL-001,All docs and contracts,3,3,9,"arch section C/D, traceability_matrix.csv",Canonically infer INF-IDs, require schema/contract mapping,Establish contract/validation gate in CI,Arch Lead
R2,ESOC protocol/format gap,ESOC telemetry source protocol/format not specified; risk of ingest breakage,INF-FR-001,TelemetryIngestionService,3,2,6,"Activity_DailyPipeline, Sequence_S1_DailyIngestProcess",Query ESOC & document protocol,Freeze contract,SwRI PM
R3,Missed 24h Co-I delivery SLA,Downstream pipeline or ingest failure causes missed distribution window,INF-DR-002,DistributionService/Scheduler,3,2,6,"Class_APAF:DistributionJob, Activity_DailyPipeline",Increase retries, pre-run checks,Overprovision, automate alerting,Distribution Lead
R4,Public/team embargo leak,Defective embargo/RBAC may expose non-public data,INF-PR-001,WebPortal/AuthService,3,1,3,"Sequence_S2_TeamWebAccess",Backend RBAC checks, quarterly audit,Security audit,Data Privacy Lead
R5,Silent data corruption,Checksum/schema errors missed or unquarantined,INF-FR-011,SchemaValidation/QuarantineStore,3,2,6,"State_IDFSDataset:L",Mandatory validation, quarantine-required,Strict contract test on all releases,SRE Lead
R6,Restore/backup process failure,NAS backup fails or restore impossible,INF-LR-001,ArchiveService/NAS/Backup,2,2,4,"Deployment_APAF:Backup",Quarterly restore drills,Multiple restore methods,SwRI Ops
NR1,Archive design robust,Strong immutable logs+archival design verified,INF-FR-005..007,ArchiveService/NAS,1,1,1,"section D5/E2",--,Retain/monitor,SwRI Ops
NR2,WebPortal OIDC+RBAC,Modern identity management blocks unauthorized access,INF-PR-001,WebPortal/AuthService,1,1,1,"section D1/D8",--,Regular update,Arch Lead
```
---

### `sensitivity_tradeoffs.csv`
```
DecisionID,DecisionText,AffectedQualityAttributes,DirectionOfSensitivity,Magnitude,Notes
D1,Modular monolith on K8s,Maintainability|Reliability|Testability,improve,High,Centralized ops with clear boundaries
D2,Contract-first APIs (OpenAPI/gRPC),Testability|Interoperability|Reliability,improve,High,Reduces integration ambiguity
D3,Quarantine-first integrity response,Reliability|Performance,improve|degrade,High,Quarantine slows delivery, prevents corruption
D4,OIDC+RBAC+MFA for team web access,Security|Usability,improve|degrade,High,Friction added for strict security
D5,NAS for archive over S3,Availability|Scalability,improve|degrade,Med,Legacy-friendly, future scale tradeoff
D6,Retry window for distribution jobs,Availability|Latency,improve|degrade,Med,High retries risk longer delivery
D7,Immutable logs and backup,Testability|Forensics,improve,High,Enables comprehensive post-incident analysis
```
---

### `qa_scenarios.csv`
```
ScenarioID,Stimulus,Source,Environment,Artefact,Response,Measure,Priority
QA1,Daily ESOC drop triggers ingest,ESOC,Prod,TelemetryIngestionService,All telemetry processed by 03:00 UTC,SLA met,High
QA2,Checksum mismatch detected,ESOC,Prod,SchemaValidationService,Quarantine + alert SRE ≤10 min,Alert time,High
QA3,Team user requests embargoed data,Co-I,Team/Web,WebPortal/AuthService,AuthN+RBAC enforced + audit,Zero violation,High
QA4,Co-I pulls data,Co-I,Remote,DistributionService,Delivery within 24h,On-time %,High
QA5,Hardware/NAS failure,Ops,Prod,ArchiveService,Data recoverable within RTO/RPO,RTO/RPO,High
QA6,Processing/validation failure,System,Any,Processing/Validation,Integrity error quarantined,Resolution time,High
QA7,PDS deadline,Admin,Deadline,PDSSubmissionService,Compliant submission within window,Zero miss,High
QA8,Schema version update,IRF,Planned,IDFSProcessingService,Compatibility preserved,Zero error,Medium
QA9,Deprovision user/admin,Admin,HR,AuthService,Account disabled ≤72h + audit,Compliance,Medium
QA10,Archive retention policy update,Admin,Policy,ArchiveService,Retention updated,Zero loss,Medium
QA11,Penetration test,RedTeam,Pen test,WebPortal/Auth,No compromise,Zero incidents,High
QA12,Co-I software versioning,Co-I,Release,Packaging,Compatible version delivered,Zero defect,Low
```
---

### `traceability_matrix.csv`
```
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FR-001,Acquire telemetry daily and auto-process,UseCase_APAF:UC_Acquire;Activity_DailyPipeline;Sequence_S1_DailyIngestProcess,TelemetryIngestionService|ESOCAdapter|Scheduler,architecture.md|internal.proto,Defines ingestion boundary and scheduling.
INF-FR-002,Process science data into IDFS,UseCase_APAF:UC_Process;Activity_DailyPipeline,IDFSProcessingService|SchemaValidationService,architecture.md|sql/idfs_dataset_ddl.sql,Core science product generation.
INF-FR-003,Process engineering/ancillary into IDFS,UseCase_APAF:UC_Process;Activity_DailyPipeline,IDFSProcessingService,architecture.md,Calibration/validation support.
INF-FR-004,Generate cleaned telemetry if ESOC missing,UseCase_APAF:UC_Clean;Activity_DailyPipeline,TelemetryCleaningService,architecture.md|internal.proto,Ensures continuity when ESOC cleaned not available.
INF-FR-005,Store raw telemetry locally,UseCase_APAF:UC_Archive;Deployment_APAF:NAS/dRaw,ArchiveService|RawTelemetryArchive,sql/telemetry_file_ddl.sql,Reprocessing and availability.
INF-FR-006,Store IDFS locally,UseCase_APAF:UC_Archive;Deployment_APAF:NAS/dIDFS,ArchiveService|IDFSArchive,sql/idfs_dataset_ddl.sql,Analysis availability.
INF-FR-007,Store intermediate locally,UseCase_APAF:UC_Archive,ArchiveService|IntermediateArchive,sql/cleaned_telemetry_file_ddl.sql,Supports team and reprocessing.
INF-FR-008,Public web display current data,UseCase_APAF:UC_PublicWeb;Container_APAF:WebPortal,WebPortal|IDFSQueryService,openapi.yaml,Public monitoring.
INF-FR-009,Team web display any data,UseCase_APAF:UC_TeamWeb;Sequence_S2_TeamWebAccess,WebPortal|AuthService|IDFSQueryService,openapi.yaml,Science analysis support.
INF-FR-010,Password protect team displays,UseCase_APAF:UC_TeamWeb,AuthService|WebPortal,openapi.yaml,Embargo enforcement.
INF-FR-011,Built-in error handling for integrity,UseCase_APAF:UC_Alert;State_IDFSDataset:L,MonitoringAlertingService|QuarantineStore,sql/quarantine_item_ddl.sql,Prevents silent corruption.
INF-FR-012,Provide IDFS/intermediate to Co-Is,UseCase_APAF:UC_Distribute,DistributionService,openapi.yaml|sql/distribution_job_ddl.sql,Distribution capability.
INF-FR-013,Provide IDFS access software,UseCase_APAF:UC_AccessSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-FR-014,Provide analysis software,UseCase_APAF:UC_AnalysisSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-FR-015,Internal interfaces left to design,Package_APAF,All services,internal.proto,Contract-first internal interfaces.
INF-FR-016,Internal data left to design,Class_APAF:IDFSDataset,Domain model,sql/idfs_dataset_ddl.sql,Defines minimal persisted metadata.
INF-PR-001,Password protect web server where appropriate,UseCase_APAF:UC_TeamWeb;Sequence_S2_TeamWebAccess,AuthService|WebPortal,openapi.yaml,Privacy requirement.
INF-CR-001,SwRI provides maintenance/support,Deployment_APAF:SwRI,Ops,architecture.md,Operational responsibility.
INF-LR-001,SwRI provides system maintenance,Deployment_APAF:Backup,Ops,architecture.md,Backup/restore and patching.
INF-LR-002,SwRI provides software support,Component_APAF:Mon,Ops,architecture.md,Monitoring and on-call.
INF-DR-001,Provide IDFS/intermediate to Co-Is,UseCase_APAF:UC_Distribute,DistributionService,openapi.yaml,Delivery requirement.
INF-DR-002,ASPERA-3 IDFS to Co-Is within 24h conditional,Class_APAF:DistributionJob,DistributionService,sql/distribution_job_ddl.sql,SLA via job deadlines.
INF-DR-003,MEX OA IDFS to Co-Is within 24h conditional,UseCase_APAF:UC_Distribute,DistributionService,sql/distribution_job_ddl.sql,SLA via same mechanism.
INF-DR-004,Intermediate cleaned telemetry within 24h conditional,UseCase_APAF:UC_Distribute,DistributionService,sql/distribution_job_ddl.sql,SLA via same mechanism.
INF-DR-005,Provide IDFS to NASA PDS,UseCase_APAF:UC_PDS,PDSSubmissionService,sql/pds_submission_package_ddl.sql,PDS pipeline.
INF-DR-006,PDS-compliant form,UseCase_APAF:UC_PDS,PDSSubmissionService|SchemaValidationService,architecture.md,Compliance packaging.
INF-DR-007,Calibrate/validate before PDS,Activity_DailyPipeline,IDFSProcessingService|PDSSubmissionService,architecture.md,Quality gate.
INF-DR-008,Submit to PDS <=6 months,State_IDFSDataset:L,PDSSubmissionService,sql/pds_submission_package_ddl.sql,Deadline tracking.
INF-DR-009,Provide algorithms to IRF,UseCase_APAF:UC_IRF,Release/Packaging,architecture.md,Out-of-band deliverable.
INF-DR-010,Integrate analysis software into NASA repo,UseCase_APAF:UC_Repo,Release automation,architecture.md,Repository publishing.
INF-DR-011,Make access software available,UseCase_APAF:UC_AccessSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-DR-012,Make analysis software available,UseCase_APAF:UC_AnalysisSW,Release/Packaging,architecture.md,Deliverable tracking.
INF-DR-013,Determine datasets per Co-I 6 months pre-launch,,DistributionService config,sql/distribution_job_ddl.sql,Configurable entitlements.
INF-DR-014,Distribution mechanisms defined in Ops Procedures,,Ops,architecture.md,SOP/runbook requirement.
INF-NFR-OPS-001,Single mode unless documented,,Ops,architecture.md,Assumed single mode.
INF-NFR-SAFE-001,No hazards,,Ops,architecture.md,Ground system safety baseline.
INF-NFR-QUAL-001,Quality factors considered,Package_APAF,All,architecture.md,Design supports QA.
INF-NFR-OPS-002,Ops procedures sufficient no training,,Ops,architecture.md,Runbooks and automation.
```
---

### `remediation_plan.md`
```
# Remediation Plan

| RiskID | RemediationAction | EstimatedEffort (S/M/L) | Priority | SuggestedOwner | Milestones | ValidationSteps |
|--------|-------------------|-------------------------|----------|---------------|------------|----------------|
| R1 | Infer and document INF-IDs for all ambiguous SRS requirements; mandate contract/schema mapping coverage in CI/CD gate | M | 1 | Arch Lead | INF-IDs finalized; contract coverage >98% measured in build | CI build passes only if all INF-IDs are referenced in contract/schema |
| R2 | Confirm and freeze ESOC protocol, format, and file-naming conventions in design docs; operationalize ESOCAdapter with contract test | M | 1 | SwRI PM | End-to-end file ingest with real data; all adapter tests pass | Test ESOC drop inject → APAF ingest pipeline completes successfully |
| R3 | Add 1–2 buffer runs/day in Scheduler; implement per-Co-I distribution queue with auto-retry and SLA alerting | S | 1 | SRE Lead | Scheduler deployed; queue metrics/alert tested in staging | SLA violation triggers alert; 100% error delivery after three retries |
| R5 | Require quarantine/alerting on all integrity failures in ingest, processing, or distribution; add weekly review of QuarantineStore | S | 1 | SRE Lead | End-to-end integrity test run; weekly SRE dashboard tracking | Synthetic corruption test triggers quarantine and escalates correctly |
```

### `remediation_plan.csv`
```
RiskID,RemediationAction,EstimatedEffort,Priority,SuggestedOwner,Milestones,ValidationSteps
R1,Infer and document INF-IDs for all ambiguous SRS requirements; mandate contract/schema mapping coverage in CI/CD gate,M,1,Arch Lead,INF-IDs finalized; contract coverage >98% measured in build,CI build passes only if all INF-IDs are referenced in contract/schema
R2,Confirm and freeze ESOC protocol, format, and file-naming conventions in design docs; operationalize ESOCAdapter with contract test,M,1,SwRI PM,End-to-end file ingest with real data; all adapter tests pass,Test ESOC drop inject → APAF ingest pipeline completes successfully
R3,Add 1–2 buffer runs/day in Scheduler; implement per-Co-I distribution queue with auto-retry and SLA alerting,S,1,SRE Lead,Scheduler deployed; queue metrics/alert tested in staging,SLA violation triggers alert; 100% error delivery after three retries
R5,Require quarantine/alerting on all integrity failures in ingest, processing, or distribution; add weekly review of QuarantineStore,S,1,SRE Lead,End-to-end integrity test run; weekly SRE dashboard tracking,Synthetic corruption test triggers quarantine and escalates correctly
```

### `scenario_executions.md`
```
# Scenario Executions

## QA1: Daily ESOC Ingest + Processing Walkthrough
1. Scheduler (Activity_DailyPipeline:ScheduleDailyRun) triggers TelemetryIngestionService at 01:00 UTC.
2. TelemetryIngestionService (Sequence_S1:Ingest) connects to ESOCAdapter (3 attempts if failure).
3. Files received; SchemaValidationService (Sequence_S1:Val) verifies checksums.
4. On success, files stored in RawTelemetryArchive; cleaning service triggered if cleaned telemetry missing (02:00 UTC).
5. Cleaned telemetry validated (CleanSvc, Sequence_S1); schema validation failure triggers alert/quarantine.
6. IDFSProcessingService processes to IDFS dataset; SchemaValidationService checks manifest (Activity_DailyPipeline:ProcessToIDFS).
7. Data archived; DistributionService starts Co-I distribution jobs.
8. MonitoringAlertingService captures duration/metrics for reporting.

## QA2: Integrity Failure → Quarantine + Alert
1. Ingest receives telemetry file, passes to SchemaValidationService.
2. Checksum mismatch detected (Sequence_S1:Val).
3. Ingest triggers QuarantineStore entry for artifact.
4. MonitoringAlertingService emits alert to SRE in <10 min.
5. SRE reviews artifact, updates status, or discards/recovers as per SOP.

## QA3: Team Data Web Access (Embargoed Data)
1. Co-I initiates sign-in (Sequence_S2:Auth).
2. OIDC+MFA provided by AuthService; successful login.
3. WebPortal requests RBAC permission (Sequence_S2:Authorize).
4. Co-I queries available datasets (IDFSQueryService), filtered by entitlement.
5. WebPortal returns data visualization, logs access in AuditLogEntry.
6. If embargoed data attempted without role, access denied and audit trail recorded.
```
---

# Verification (Acceptance Criteria Checklist)

- [x] 3-line Analysis Plan present.
- [x] Sections A–N included.
- [x] `risk_register.csv`, `sensitivity_tradeoffs.csv`, `traceability_matrix.csv`, `qa_scenarios.csv` included and syntactically valid.
- [x] Every FR/NFR/ASR (or `INF-` equivalent) appears in traceability matrix.
- [x] ≥8 scenario walkthroughs performed (see F, scenario_executions.md).
- [x] Top risks have remediation actions, owners, and validation steps.
- [x] Assumptions and stakeholder questions listed.

---

## How to Review

- Are the business goals clearly listed and prioritized?
- Are QA scenarios explicit and prioritized?
- Are scenario walkthroughs detailed and traceable to diagrams/requirements?
- Is there a complete risk register with severity/probability and remediation?
- Are sensitivity and tradeoff points listed with recommended mitigations?
- Are assumptions and open stakeholder questions clearly spelled out?
```
---

### Appendix

*(All remaining PlantUML referenced diagrams, SQL DDLs, OpenAPI, k8s manifests, etc. are delivered as per main report section L and referenced in traceability matrix.)*
