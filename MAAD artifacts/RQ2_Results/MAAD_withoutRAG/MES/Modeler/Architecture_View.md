## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseView_APAF
left to right direction

actor ESOC
actor "APAF Operator" as Operator
actor "ASPERA-3 Co-I" as CoI
actor "Public User" as Public
actor "NASA PDS" as PDS
actor IRF
actor "NASA Repository" as NASARepo

artifact "APAF System" as APAF {
  usecase "AcquireTelemetry\n[AcquireTelemetry]" as UC_Acquire
  usecase "RunDailyPipeline\n[DailyProcess]" as UC_Daily
  usecase "GenerateIDFS\n[GenerateIDFS]" as UC_IDFS
  usecase "GenerateCleanTelemetry\n[CleanTelemetry]" as UC_Clean
  usecase "ArchiveProducts\n[Archive]" as UC_Archive
  usecase "PublishPublicDisplays\n[PublicDisplays]" as UC_PublicWeb
  usecase "ProvideTeamDisplays\n[TeamDisplays]" as UC_TeamWeb
  usecase "AuthenticateUser\n[Auth]" as UC_Auth
  usecase "DistributeToCoIs\n[Distribute]" as UC_Distribute
  usecase "SubmitToPDS\n[SubmitPDS]" as UC_PDS
  usecase "ProvideAlgorithmsToIRF\n[ProvideAlgorithms]" as UC_IRF
  usecase "PublishSoftwareToRepo\n[PublishSoftware]" as UC_Software
}

ESOC --> UC_Acquire
Operator --> UC_Daily
UC_Daily ..> UC_Acquire : <<include>>
UC_Daily ..> UC_IDFS : <<include>>
UC_Daily ..> UC_Archive : <<include>>
UC_Daily ..> UC_Distribute : <<include>>

UC_Clean ..> UC_Daily : <<extend>>
note right of UC_Clean
  extend condition: ESOC cleaned telemetry unavailable (FR-005, ASR-003)
end note

Public --> UC_PublicWeb
CoI --> UC_TeamWeb
UC_TeamWeb ..> UC_Auth : <<include>>

CoI --> UC_Distribute
PDS --> UC_PDS
UC_PDS ..> UC_IDFS : <<include>>

IRF --> UC_IRF
NASARepo --> UC_Software

note bottom of APAF
assumption: "public displays of most current data" expose only data marked public via ReleaseGate;
if "current" overlaps embargoed, content is withheld until release (ASR-005).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassView_APAF
skinparam classAttributeIconSize 0

class TelemetryBatch <<persisted>> {
  +batchId: String
  +source: String
  +acquiredAt: DateTime
  +checksumSha256: String
  +cleanedProvidedByEsoc: Boolean
  +status: BatchStatus
  +acquire(): void
  +verifyChecksum(): boolean
}

enum BatchStatus {
  ACQUIRED
  CLEANED
  PROCESSED
  ARCHIVED
  DISTRIBUTED
  FAILED
}

class CleanTelemetryFile <<persisted>> {
  +fileId: String
  +format: String
  +createdAt: DateTime
  +checksumSha256: String
  +provenance: String
  +generate(): void
  +validateFormat(): boolean
}

class IDFSDataset <<persisted>> {
  +datasetId: String
  +instrument: String
  +schemaVersion: String
  +createdAt: DateTime
  +isEmbargoed: Boolean
  +validateSchema(): boolean
}

class PDSBundle <<persisted>> {
  +bundleId: String
  +pds4Version: String
  +validatorReportPath: String
  +createdAt: DateTime
  +validatePds4(): boolean
  +package(): void
}

class ArchiveEntry <<persisted>> {
  +entryId: String
  +artifactType: String
  +path: String
  +storedAt: DateTime
  +retentionClass: String
  +store(): void
  +retrieve(): void
}

class DistributionJob <<persisted>> {
  +jobId: String
  +recipientGroup: String
  +artifactType: String
  +deadlineAt: DateTime
  +status: JobStatus
  +attemptCount: int
  +schedule(): void
  +markDelivered(): void
  +markMissed(): void
}

enum JobStatus {
  QUEUED
  IN_PROGRESS
  DELIVERED
  MISSED
  ESCALATED
}

class ReleaseGate <<persisted>> {
  +gateId: String
  +datasetId: String
  +state: ReleaseState
  +changedAt: DateTime
  +changedBy: String
  +authorizePublication(): boolean
  +setPublic(): void
}

enum ReleaseState {
  EMBARGOED
  PUBLIC
}

class UserAccount <<persisted>> {
  +userId: String
  +username: String
  -passwordHash: String
  +role: Role
  +passwordRotatedAt: Date
  +authenticate(password: String): boolean
  +authorize(action: String): boolean
}

enum Role {
  ADMIN
  COI
  PUBLIC
}

class ErrorEvent <<persisted>> {
  +eventId: String
  +occurredAt: DateTime
  +component: String
  +errorType: String
  +severity: String
  +message: String
  +batchId: String
  +correlationId: String
}

class IntegrityService {
  +computeSha256(path: String): String
  +gateOrFail(expectedSha: String, actualSha: String): void
  +retry(operation: String, maxRetries: int): boolean
  +rollback(correlationId: String): void
}

class MonitoringService {
  +recordMetric(name: String, value: long): void
  +raiseAlert(name: String, details: String): void
}

TelemetryBatch "1" o-- "0..*" CleanTelemetryFile : produces
TelemetryBatch "1" o-- "0..*" IDFSDataset : produces
IDFSDataset "1" o-- "0..1" PDSBundle : packagedAs
TelemetryBatch "1" o-- "0..*" ArchiveEntry : archivedAs
IDFSDataset "1" o-- "0..*" ArchiveEntry : archivedAs
CleanTelemetryFile "1" o-- "0..*" ArchiveEntry : archivedAs

DistributionJob "0..*" --> "0..*" IDFSDataset : delivers
DistributionJob "0..*" --> "0..*" CleanTelemetryFile : delivers

ReleaseGate "1" --> "1" IDFSDataset : controls

IntegrityService ..> TelemetryBatch
IntegrityService ..> IDFSDataset
IntegrityService ..> ArchiveEntry
MonitoringService ..> DistributionJob
MonitoringService ..> ErrorEvent

note right of UserAccount
NFR-004: password min 12, complexity, rotate quarterly;
all accesses logged with userId/timestamp.
end note

note right of DistributionJob
NFR-010/011/012: 24h SLO; alert at 22h; retry up to 3;
escalate if undelivered after 48h.
end note

note bottom of IDFSDataset
NFR-001/ASR-002: must validate against IDFS schema vX.Y using validator-tool.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectView_APAF
artifact batch2026_04_21 {
  batchId = "TB-2026-04-21"
  source = "ESOC/NISN"
  acquiredAt = "2026-04-21T02:10Z"
  checksumSha256 = "a9f2...d31c"
  cleanedProvidedByEsoc = false
  status = ACQUIRED
}

artifact clean1 {
  fileId = "CTF-2026-04-21-A3"
  format = "CCSDS"
  createdAt = "2026-04-21T02:40Z"
  checksumSha256 = "b12a...91ef"
  provenance = "APAF cleanup v1.3; source TB-2026-04-21"
}

artifact idfsA3 {
  datasetId = "IDFS-A3-2026-04-21"
  instrument = "ASPERA-3"
  schemaVersion = "X.Y"
  createdAt = "2026-04-21T04:05Z"
  isEmbargoed = true
}

artifact rel1 {
  gateId = "RG-001"
  datasetId = "IDFS-A3-2026-04-21"
  state = EMBARGOED
  changedAt = "2026-04-21T04:10Z"
  changedBy = "admin1"
}

artifact archRaw {
  entryId = "AE-RAW-001"
  artifactType = "RAW_TLM"
  path = "/archive/raw/2026/04/21/TB-2026-04-21.bin"
  storedAt = "2026-04-21T02:15Z"
  retentionClass = "mission"
}

artifact archIdfs {
  entryId = "AE-IDFS-001"
  artifactType = "IDFS"
  path = "/archive/idfs/2026/04/21/IDFS-A3-2026-04-21/"
  storedAt = "2026-04-21T04:07Z"
  retentionClass = "mission"
}

artifact jobCoI {
  jobId = "DJ-1001"
  recipientGroup = "AllCoIs"
  artifactType = "IDFS+CleanTelemetry"
  deadlineAt = "2026-04-22T02:10Z"
  status = IN_PROGRESS
  attemptCount = 1
}

batch2026_04_21 -- clean1
batch2026_04_21 -- idfsA3
batch2026_04_21 -- archRaw
idfsA3 -- archIdfs
idfsA3 -- rel1
jobCoI -- idfsA3
jobCoI -- clean1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateView_TelemetryBatch
hide empty description

state "TelemetryBatch Lifecycle" as TB {

  [*] --> Scheduled : RunDailyPipeline

  Scheduled --> Acquiring : AcquireTelemetry
  Acquiring --> Acquired : ingestOk / logIngest()
  Acquiring --> Failed : ingestFail / emitErrorEvent()

  Acquired --> Cleaning : [cleanedProvidedByEsoc==false] CleanTelemetry
  Acquired --> Cleaned : [cleanedProvidedByEsoc==true]

  Cleaning --> Cleaned : cleanupOk / storeIntermediate()
  Cleaning --> Failed : cleanupFail / emitErrorEvent()

  state "Processing" as Processing {
    [*] --> Transforming
    Transforming --> ValidatingIDFS : GenerateIDFS
    ValidatingIDFS --> Processed : [idfsValid==true] / recordMetric()
    ValidatingIDFS --> Failed : [idfsValid==false] / emitErrorEvent()
  }

  Cleaned --> Processing : ProcessTelemetry

  Processed --> Archiving : ArchiveProducts
  Archiving --> Archived : archiveOk
  Archiving --> Failed : archiveFail / emitErrorEvent()

  Archived --> Distributing : DistributeToCoIs
  Distributing --> Distributed : deliveredWithin24h
  Distributing --> MissedSLO : [now>deadlineAt] / raiseAlert()
  MissedSLO --> Distributing : retryDelivery [attemptCount<3]
  MissedSLO --> Escalated : escalate [now>deadlineAt+48h]

  Distributed --> [*] : Complete

  Failed --> [*]
  Escalated --> [*]
}

note right of TB
ASR-006/NFR-003: all critical errors logged centrally; retries/rollback via IntegrityService.
ASR-007/NFR-010/011/012: deadline-driven distribution with alerts and escalation.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityView_DailyPipeline
start
:Trigger schedule (daily);
:AcquireTelemetry from ESOC via NISN;
:Verify checksum [IntegrityGate];

if (Ingest OK?) then (yes)
  :Store raw telemetry to LocalArchive;
else (no)
  :Log ErrorEvent;
  :Raise alert (critical);
  stop
endif

if (ESOC cleaned telemetry provided?) then (yes)
  :Register cleaned telemetry reference;
else (no)
  :GenerateCleanTelemetry;
  :Validate cleaned format [IntegrityGate];
  :Store cleaned telemetry to LocalArchive;
endif

fork
  :Process science data;
  :GenerateIDFS (ASPERA-3);
  :Validate IDFS schema vX.Y [ComplianceGate];
fork again
  :Process engineering/ancillary;
  :GenerateIDFS (MEX OA);
  :Validate IDFS schema vX.Y [ComplianceGate];
end fork

:Archive IDFS datasets to LocalArchive;
:Update ReleaseGate state (embargo/public);
:Queue DistributionJob(s) for Co-Is (deadline=+24h);

note right
NFR-010/011/012: alert at 22h; retry up to 3; escalate if >48h.
end note

:Execute distribution (push/pull channel);
:Record SLO metrics & delivery logs;

fork
  :PublishPublicDisplays (only PUBLIC via ReleaseGate);
fork again
  :ProvideTeamDisplays (Auth/RBAC + audit logging);
end fork

:Evaluate PDS submission backlog;
if (PDS due?) then (yes)
  :Calibrate & validate for PDS;
  :Package PDS4 bundle;
  :Validate with PDS4 validator [ComplianceGate];
  :SubmitToPDS;
  :Store delivery record evidence;
endif

stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml SequenceView_S1_DailyPipeline
autonumber
actor "APAF Operator" as Operator
participant "PipelineOrchestrator" as Orchestrator
participant "ESOCIngestAdapter" as ESOCAdapter
participant "IntegrityService" as Integrity
participant "TelemetryCleanupService" as Cleanup
participant "IDFSProcessor" as IDFSProc
participant "IDFSValidatorAdapter" as IDFSVal
database "LocalArchive" as Archive
participant "MonitoringService" as Monitor
participant "DistributionService" as Dist

Operator -> Orchestrator : RunDailyPipeline
Orchestrator -> ESOCAdapter : AcquireTelemetry
ESOCAdapter --> Orchestrator : TelemetryBatch(acquired)
Orchestrator -> Integrity : VerifyChecksum
Integrity --> Orchestrator : ok

Orchestrator -> Archive : StoreRawTelemetry
Archive --> Orchestrator : stored

alt ESOC cleaned telemetry missing
  Orchestrator -> Cleanup : CleanTelemetry
  Cleanup -> Integrity : ComputeSha256
  Integrity --> Cleanup : sha256
  Cleanup --> Orchestrator : CleanTelemetryFile(created)
  Orchestrator -> Archive : StoreCleanTelemetry
  Archive --> Orchestrator : stored
else ESOC cleaned telemetry provided
  Orchestrator -> Monitor : RecordMetric(cleanedProvided=1)
end

Orchestrator -> IDFSProc : GenerateIDFS
IDFSProc --> Orchestrator : IDFSDataset(created)
Orchestrator -> IDFSVal : ValidateIDFS
IDFSVal --> Orchestrator : valid

Orchestrator -> Archive : StoreIDFS
Archive --> Orchestrator : stored

Orchestrator -> Dist : CreateDistributionJobs(deadline+24h)
Dist --> Orchestrator : jobsQueued

Orchestrator -> Monitor : RecordMetric(pipelineDuration)
Orchestrator --> Operator : PipelineComplete

note right of Dist
NFR-010/011/012: alert at 22h, retry<=3, escalate at 48h.
end note
@enduml
```

```plantuml
@startuml SequenceView_S2_TeamWebAccess
autonumber
actor "ASPERA-3 Co-I" as CoI
participant "WebPortal" as Web
participant "AuthService" as Auth
participant "AuditLog" as Audit
participant "DataAPI" as API
participant "ReleaseGateService" as Release
database "LocalArchive" as Archive

CoI -> Web : OpenTeamDisplays
Web -> Auth : AuthenticateUser(credentials)
Auth -> Audit : LogAccessAttempt
Audit --> Auth : logged
Auth --> Web : authOk(role=COI)

Web -> API : QueryIDFS(datasetId)
API -> Release : AuthorizePublication(datasetId, role=COI)
Release --> API : allowed (embargoedOkForCOI)
API -> Archive : RetrieveIDFS(datasetId)
Archive --> API : IDFS data
API --> Web : RenderTeamDisplay
Web --> CoI : TeamDisplayShown

note right of Auth
NFR-004: password>=12, complexity, rotate quarterly; RBAC enforced; all access logged.
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationView_S1_DailyPipeline
actor "APAF Operator" as Operator
rectangle "PipelineOrchestrator" as Orchestrator
rectangle "ESOCIngestAdapter" as ESOCAdapter
rectangle "IntegrityService" as Integrity
rectangle "TelemetryCleanupService" as Cleanup
rectangle "IDFSProcessor" as IDFSProc
rectangle "IDFSValidatorAdapter" as IDFSVal
database "LocalArchive" as Archive
rectangle "DistributionService" as Dist
rectangle "MonitoringService" as Monitor

Operator -- Orchestrator
Orchestrator -- ESOCAdapter
Orchestrator -- Integrity
Orchestrator -- Cleanup
Orchestrator -- IDFSProc
Orchestrator -- IDFSVal
Orchestrator -- Archive
Orchestrator -- Dist
Orchestrator -- Monitor

Orchestrator : 1. RunDailyPipeline
Orchestrator -> ESOCAdapter : 2. AcquireTelemetry
Orchestrator -> Integrity : 3. VerifyChecksum
Orchestrator -> Archive : 4. StoreRawTelemetry
Orchestrator -> Cleanup : 5. CleanTelemetry (if needed)
Orchestrator -> IDFSProc : 6. GenerateIDFS
Orchestrator -> IDFSVal : 7. ValidateIDFS
Orchestrator -> Archive : 8. StoreIDFS
Orchestrator -> Dist : 9. CreateDistributionJobs
Orchestrator -> Monitor : 10. RecordMetrics

note bottom
scenario: Daily automated telemetry ingest -> optional cleanup -> IDFS generation/validation -> archive -> distribute (FR-001/002/003/005/006/007/013; ASR-001/003/004/007).
end note
@enduml
```

```plantuml
@startuml CollaborationView_S2_TeamWebAccess
actor "ASPERA-3 Co-I" as CoI
rectangle "WebPortal" as Web
rectangle "AuthService" as Auth
rectangle "AuditLog" as Audit
rectangle "DataAPI" as API
rectangle "ReleaseGateService" as Release
database "LocalArchive" as Archive

CoI -- Web
Web -- Auth
Auth -- Audit
Web -- API
API -- Release
API -- Archive

CoI -> Web : 1. OpenTeamDisplays
Web -> Auth : 2. AuthenticateUser
Auth -> Audit : 3. LogAccessAttempt
Web -> API : 4. QueryIDFS
API -> Release : 5. AuthorizePublication
API -> Archive : 6. RetrieveIDFS
API -> Web : 7. RenderTeamDisplay
Web -> CoI : 8. Show

note bottom
scenario: Password-protected science-analysis displays with RBAC and audit logging (FR-010/011; NFR-004; ASR-005).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml PackageView_APAF
skinparam packageStyle rectangle

package "ui" as P_UI {
  note bottom: WebPortal (public + team views)
}

package "api" as P_API {
  note bottom: DataAPI for queries/download
}

package "domain" as P_DOMAIN {
  note bottom: TelemetryBatch, IDFSDataset, ReleaseGate, DistributionJob
}

package "application" as P_APP {
  note bottom: PipelineOrchestrator, use-case services
}

package "integrations" as P_INT {
  note bottom: ESOCIngestAdapter, IDFSValidatorAdapter, PDSValidatorAdapter
}

package "infrastructure" as P_INFRA {
  note bottom: LocalArchive, queues, scheduling, config
}

package "crosscutting" as P_XCUT {
  note bottom: AuthService, IntegrityService, MonitoringService, AuditLog
}

P_UI ..> P_API
P_API ..> P_APP
P_APP ..> P_DOMAIN
P_APP ..> P_INT
P_APP ..> P_INFRA
P_APP ..> P_XCUT
P_INT ..> P_XCUT
P_API ..> P_XCUT

note right of P_XCUT
ASR-006: centralized error handling/logging/alerts.
NFR-004: authentication/RBAC/audit.
end note

note right of P_DOMAIN
ASR-002: IDFS canonical products.
ASR-007: deadline-driven DistributionJob model.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml ComponentView_APAF
skinparam componentStyle rectangle

component "WebPortal\n[PublicDisplays|TeamDisplays]" as Web
component "DataAPI\n[Query|Download]" as API
component "AuthService\n[RBAC]" as Auth
component "AuditLog\n[AccessLog]" as Audit
component "PipelineOrchestrator\n[DailyProcess]" as Orchestrator
component "ESOCIngestAdapter\n[AcquireTelemetry]" as ESOCAdapter
component "TelemetryCleanupService\n[CleanTelemetry]" as Cleanup
component "IDFSProcessor\n[GenerateIDFS]" as IDFSProc
component "IDFSValidatorAdapter\n[ValidateIDFS]" as IDFSVal
component "ReleaseGateService\n[Embargo]" as Release
component "DistributionService\n[Distribute]" as Dist
component "PDSExportService\n[SubmitPDS]" as PDSExport
component "PDSValidatorAdapter\n[ValidatePDS4]" as PDSVal
component "IntegrityService\n[IntegrityGate]" as Integrity
component "MonitoringService\n[SLO|Alerts]" as Monitor
database "LocalArchive" as Archive
queue "JobQueue\n[DistributionJobs]" as Queue

interface IAuth
interface IDataQuery
interface IIngest
interface IArchive
interface IIntegrity
interface IMonitor

Auth - IAuth
API - IDataQuery
ESOCAdapter - IIngest
Archive - IArchive
Integrity - IIntegrity
Monitor - IMonitor

Web ..> IAuth
Web ..> IDataQuery

API ..> IAuth
API ..> Release
API ..> Archive
API ..> Audit

Orchestrator ..> ESOCAdapter
Orchestrator ..> Cleanup
Orchestrator ..> IDFSProc
Orchestrator ..> IDFSVal
Orchestrator ..> Archive
Orchestrator ..> Dist
Orchestrator ..> Integrity
Orchestrator ..> Monitor
Orchestrator ..> Release

Dist ..> Queue
Dist ..> Archive
Dist ..> Monitor

PDSExport ..> Archive
PDSExport ..> PDSVal
PDSExport ..> Monitor
PDSExport ..> Integrity

note right of IDFSVal
NFR-001: validate against IDFS schema vX.Y using validator-tool.
end note

note right of PDSVal
NFR-001/FR-017: PDS4 validator pass; store evidence in delivery record.
end note

note bottom of Dist
ASR-007: 24h SLO enforcement, retries, escalation.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentView_APAF
skinparam nodeStyle rectangle

node "ESOC Systems" as ESOC {
  artifact "Telemetry Source" as ESOCSrc
}

node "SwRI Network" as SwRI {
  node "APAF App Server (VM)\n[batch+api]" as AppVM {
    artifact "WebPortal" as A_Web
    artifact "DataAPI" as A_API
    artifact "PipelineOrchestrator" as A_Orch
    artifact "ESOCIngestAdapter" as A_Ingest
    artifact "TelemetryCleanupService" as A_Clean
    artifact "IDFSProcessor" as A_IDFS
    artifact "PDSExportService" as A_PDS
    artifact "AuthService" as A_Auth
    artifact "ReleaseGateService" as A_Rel
    artifact "DistributionService" as A_Dist
    artifact "IntegrityService" as A_Int
    artifact "MonitoringService" as A_Mon
    artifact "AuditLog" as A_Audit
  }

  node "LocalArchive Storage (NAS)\n[stateful]" as NAS {
    database "LocalArchive" as D_Archive
  }

  node "Job Queue Node\n[stateful]" as QNode {
    queue "JobQueue" as D_Queue
  }

  node "Ops Workstation" as Ops {
    artifact "Operator Console" as OpsConsole
  }
}

node "External: NASA PDS" as PDS {
  artifact "PDS Endpoint" as PDSEnd
}

ESOCSrc -- AppVM : NISN/ESOC link\n(NFR-002)
AppVM -- NAS : LAN (high throughput)
AppVM -- QNode : LAN
OpsConsole -- AppVM : HTTPS
AppVM -- PDSEnd : Secure transfer\n(FR-016/017)

note right of AppVM
ASR-001: unattended daily batch.
ASR-006: centralized logging/alerts.
end note

note right of NAS
ASR-004/NFR-007: local archive for raw, IDFS, intermediates.
end note

note bottom of QNode
ASR-007: deadline-driven distribution jobs.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerView_APAF
skinparam rectangleStyle rounded
left to right direction

rectangle "External System\nESOC" as C_ESOC {
  rectangle "Telemetry Provider\n[ESOC/NISN]" as ESOCProv
}

rectangle "APAF System (SwRI)" as C_APAF {

  rectangle "WebPortal\n[PublicDisplays|TeamDisplays]\n(HTTPS)" as C_Web
  rectangle "Backend API\nDataAPI\n[Query|Download]" as C_API
  rectangle "Batch Runtime\nPipelineOrchestrator\n[DailyProcess]" as C_Batch

  rectangle "Cross-cutting Services\n[Integrity|Auth|Audit|Monitoring]" as C_XCut {
    rectangle "AuthService\n[RBAC]" as C_Auth
    rectangle "AuditLog\n[AccessLog]" as C_Audit
    rectangle "IntegrityService\n[IntegrityGate]" as C_Integrity
    rectangle "MonitoringService\n[SLO|Alerts]" as C_Monitor
    rectangle "ReleaseGateService\n[Embargo]" as C_Release
  }

  rectangle "Processing Services\n[IDFS|Cleanup|PDS]" as C_Proc {
    rectangle "ESOCIngestAdapter\n[AcquireTelemetry]" as C_Ingest
    rectangle "TelemetryCleanupService\n[CleanTelemetry]" as C_Clean
    rectangle "IDFSProcessor\n[GenerateIDFS]" as C_IDFS
    rectangle "IDFSValidatorAdapter\n[ValidateIDFS]" as C_IDFSVal
    rectangle "PDSExportService\n[SubmitPDS]" as C_PDS
    rectangle "PDSValidatorAdapter\n[ValidatePDS4]" as C_PDSVal
    rectangle "DistributionService\n[Distribute]" as C_Dist
  }

  database "LocalArchive\n[Raw|IDFS|Intermediate]" as C_Archive
  queue "JobQueue\n[DistributionJobs]" as C_Queue
}

rectangle "External System\nNASA PDS" as C_PDSext {
  rectangle "PDS Endpoint\n[PDS4 ingest]" as PDSIngest
}

rectangle "Users" as C_Users {
  actor "Public User" as U_Public
  actor "ASPERA-3 Co-I" as U_CoI
  actor "APAF Operator" as U_Op
}

U_Public --> C_Web : ViewPublic (HTTPS)
U_CoI --> C_Web : ViewTeam (HTTPS)
U_Op --> C_Batch : Operate/Schedule

C_Web --> C_API : Query/Render
C_API --> C_Auth : Authenticate
C_API --> C_Release : AuthorizePublication
C_API --> C_Audit : LogAccess
C_API --> C_Archive : Retrieve

C_Batch --> C_Ingest : AcquireTelemetry
C_Ingest --> ESOCProv : PullTelemetry (NISN)
C_Batch --> C_Integrity : VerifyChecksum
C_Batch --> C_Archive : StoreRaw

C_Batch --> C_Clean : CleanTelemetry (conditional)
C_Batch --> C_IDFS : GenerateIDFS
C_Batch --> C_IDFSVal : ValidateIDFS
C_Batch --> C_Archive : StoreIDFS/Intermediates
C_Batch --> C_Dist : CreateJobs
C_Dist --> C_Queue : Enqueue
C_Dist --> C_Archive : ReadArtifacts
C_Dist --> C_Monitor : SLO metrics/alerts

C_Batch --> C_PDS : Package/Submit
C_PDS --> C_PDSVal : ValidatePDS4
C_PDS --> PDSIngest : Transfer

note right of C_Web
ASR-005/NFR-004: public vs restricted; password policy; RBAC; audit logging.
end note

note bottom of C_Batch
ASR-001: daily automated pipeline with idempotency/retries.
end note
@enduml
```