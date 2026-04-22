## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_APAF
left to right direction
skinparam packageStyle rectangle

actor "ESOC" as ESOC
actor "CoI" as CoI
actor "PublicUser" as PublicUser
actor "PI" as PI
actor "Admin" as Admin
actor "SRE" as SRE
actor "NASA PDS" as PDS
actor "IRF" as IRF
actor "NASA Approved Repo" as Repo

rectangle "APAF System" as APAF {
  usecase "AcquireTelemetry" as UC_Acquire
  usecase "ProcessToIDFS" as UC_Process
  usecase "GenerateCleanedTelemetry" as UC_Clean
  usecase "ArchiveArtifacts" as UC_Archive
  usecase "DistributeToCoIs" as UC_Distribute
  usecase "PublicWebDisplay" as UC_PublicWeb
  usecase "TeamWebDisplay" as UC_TeamWeb
  usecase "SubmitToPDS" as UC_PDS
  usecase "ProvideAlgorithmsToIRF" as UC_IRF
  usecase "ProvideAccessSoftware" as UC_AccessSW
  usecase "ProvideAnalysisSoftware" as UC_AnalysisSW
  usecase "IntegrateAnalysisSoftwareRepo" as UC_Repo
  usecase "AlertOnFailure" as UC_Alert
  usecase "ValidateSchema" as UC_Validate
}

ESOC --> UC_Acquire
SRE --> UC_Alert

UC_Acquire ..> UC_Validate : <<include>>
UC_Process ..> UC_Validate : <<include>>
UC_Clean ..> UC_Validate : <<include>>
UC_Distribute ..> UC_Validate : <<include>>
UC_PDS ..> UC_Validate : <<include>>

UC_Process ..> UC_Acquire : <<include>>
UC_Clean ..> UC_Acquire : <<include>>
UC_Archive ..> UC_Acquire : <<include>>
UC_Archive ..> UC_Process : <<include>>
UC_Archive ..> UC_Clean : <<include>>

UC_Clean ..> UC_Acquire : <<extend>>\n[ESOC cleaned-up missing by 02:00 UTC]

UC_Distribute ..> UC_Process : <<include>>
UC_Distribute ..> UC_Clean : <<extend>>\n[intermediate exists]

CoI --> UC_Distribute
CoI --> UC_TeamWeb
PublicUser --> UC_PublicWeb

PI --> UC_PublicWeb : approve publish
PI --> UC_TeamWeb : approve publish
Admin --> UC_TeamWeb : manage roles/config
Admin --> UC_PublicWeb : manage content

PDS --> UC_PDS
IRF --> UC_IRF
Repo --> UC_Repo

CoI --> UC_AccessSW
CoI --> UC_AnalysisSW
UC_Repo ..> UC_AnalysisSW : <<include>>

note right of UC_Acquire
assumption: ESOC is modeled as an external actor providing
telemetry via "protocol X, format Y" and daily file delivery.
end note

note right of UC_TeamWeb
NFR-002/NFR-003: MFA, RBAC, audit logs retained 180 days,
session timeout 30 min, password policy enforced.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_APAF
skinparam classAttributeIconSize 0

class TelemetryFile <<persisted>> {
  +fileId: String
  +source: String
  +format: String
  +acquisitionTimeUtc: DateTime
  +checksum: String
  +status: String
  +storeRaw()
  +verifyChecksum()
}

class CleanedTelemetryFile <<persisted>> {
  +fileId: String
  +schemaRef: String
  +generatedBy: String  <<ESOC|APAF>>
  +generationTimeUtc: DateTime
  +status: String
  +clean()
  +validateSchema()
}

class IDFSDataset <<persisted>> {
  +datasetId: String
  +schemaVersion: String
  +instrument: String
  +coverageStartUtc: DateTime
  +coverageEndUtc: DateTime
  +validationStatus: String
  +validateSchema()
  +publish()
}

class CalibrationResult {
  +calibrationId: String
  +absoluteErrorPct: float
  +guideRef: String
  +isWithinTolerance(): boolean
}

class PDSSubmissionPackage <<persisted>> {
  +packageId: String
  +pdsStandard: String
  +submissionDeadlineUtc: DateTime
  +status: String
  +buildPackage()
  +submit()
}

class ArchiveObject <<persisted>> {
  +archiveId: String
  +path: String
  +retentionUntilUtc: DateTime
  +artifactType: String
  +backupNightly()
  +restoreTest()
}

class DistributionJob <<persisted>> {
  +jobId: String
  +targetGroup: String
  +createdUtc: DateTime
  +status: String
  +retryCount: int
  +dispatch()
  +confirmReceipts()
}

class WebDisplayConfig <<persisted>> {
  +configId: String
  +displayType: String  <<Public|Team>>
  +refreshSlaMinutes: int
  +queryDefinition: String
  +update()
}

class UserAccount <<persisted>> {
  +userId: String
  +email: String
  +role: String  <<public|coi|admin>>
  +mfaEnabled: boolean
  +passwordLastRotatedUtc: DateTime
  +authenticate()
  +authorize()
  +deactivate()
}

class AuditLogEntry <<persisted>> {
  +entryId: String
  +logType: String  <<access|error>>
  +timestampUtc: DateTime
  +actorId: String
  +action: String
  +details: String
  +retainDays: int
}

class QuarantineItem <<persisted>> {
  +itemId: String
  +reason: String
  +createdUtc: DateTime
  +status: String
  +quarantine()
  +release()
}

TelemetryFile "1" o-- "0..*" CleanedTelemetryFile : derivedFrom
CleanedTelemetryFile "0..*" --> "0..*" IDFSDataset : inputTo
IDFSDataset "0..*" --> "0..1" CalibrationResult : validatedBy
IDFSDataset "0..*" --> "0..*" PDSSubmissionPackage : packagedIn
TelemetryFile "0..*" --> "0..*" ArchiveObject : archivedAs
CleanedTelemetryFile "0..*" --> "0..*" ArchiveObject : archivedAs
IDFSDataset "0..*" --> "0..*" ArchiveObject : archivedAs
DistributionJob "0..*" --> "0..*" IDFSDataset : distributes
DistributionJob "0..*" --> "0..*" CleanedTelemetryFile : distributes
WebDisplayConfig "0..*" --> "0..*" IDFSDataset : reads
UserAccount "1" --> "0..*" AuditLogEntry : generates
QuarantineItem "0..*" --> "0..1" TelemetryFile : holds
QuarantineItem "0..*" --> "0..1" CleanedTelemetryFile : holds
QuarantineItem "0..*" --> "0..1" IDFSDataset : holds

note right of IDFSDataset
ASR-002: must conform to IDFS schema v1.3.2.
Validate on every output (FR-002/FR-003).
end note

note right of DistributionJob
ASR-007/NFR-005..007: deliver within 24h (conditional),
retry up to 3 times, notify on errors within 2h.
end note

note right of UserAccount
ASR-006/NFR-002/NFR-003: MFA for team accounts,
password >=12 chars, rotate 90 days, deactivate within 72h,
session timeout 30 min, RBAC actions logged 180 days.
end note

note right of QuarantineItem
ASR-009/NFR-004: on checksum mismatch/missing file/schema failure:
alert within 10 min, quarantine artifact, log to error audit.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_APAF
skinparam classAttributeIconSize 0

object "raw1:TelemetryFile [AcquireTelemetry]" as raw1 {
  fileId = "ESOC_2026-03-14_ASP3_RAW_001"
  source = "ESOC"
  format = "formatY"
  acquisitionTimeUtc = "2026-03-14T01:05Z"
  checksum = "sha256:ab12..."
  status = "Acquired"
}

object "clean1:CleanedTelemetryFile [GenerateCleanedTelemetry]" as clean1 {
  fileId = "APAF_2026-03-14_ASP3_CLEAN_001"
  schemaRef = "clean-schema:v1"
  generatedBy = "APAF"
  generationTimeUtc = "2026-03-14T02:10Z"
  status = "Validated"
}

object "idfs1:IDFSDataset [ProcessToIDFS]" as idfs1 {
  datasetId = "IDFS_ASP3_2026-03-14_DAILY"
  schemaVersion = "1.3.2"
  instrument = "ASPERA-3"
  coverageStartUtc = "2026-03-13T00:00Z"
  coverageEndUtc = "2026-03-13T23:59Z"
  validationStatus = "Pass"
}

object "dist1:DistributionJob [DistributeToCoIs]" as dist1 {
  jobId = "DIST_2026-03-14_01"
  targetGroup = "ASPERA-3 Co-Is"
  createdUtc = "2026-03-14T02:30Z"
  status = "Dispatched"
  retryCount = 0
}

object "arch1:ArchiveObject [ArchiveArtifacts]" as arch1 {
  archiveId = "ARC_2026-03-14_0001"
  path = "/archive/raw/2026/03/ESOC_2026-03-14_ASP3_RAW_001"
  retentionUntilUtc = "2031-03-14T00:00Z"
  artifactType = "RawTelemetry"
}

object "webTeam1:WebDisplayConfig [TeamWebDisplay]" as webTeam1 {
  configId = "WEB_TEAM_SCI_01"
  displayType = "Team"
  refreshSlaMinutes = 15
  queryDefinition = "science_dashboard_v1"
}

raw1 -- clean1 : derivedFrom
clean1 -- idfs1 : inputTo
idfs1 -- dist1 : distributes
raw1 -- arch1 : archivedAs
idfs1 -- webTeam1 : reads
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_IDFSDataset
hide empty description

state "IDFSDataset Lifecycle" as L {

  [*] --> Created : ProcessToIDFS

  Created --> SchemaValidated : ValidateSchema / validateSchema()
  Created --> Quarantined : SchemaNonconformance / quarantine()

  SchemaValidated --> Archived : ArchiveArtifacts / store()
  SchemaValidated --> Distributed : DistributeToCoIs / dispatch()

  Distributed --> Archived : ArchiveArtifacts / store()

  Archived --> PDSReady : CalibrateValidate / checkTolerance()
  PDSReady --> PDSSubmitted : SubmitToPDS / submit()

  SchemaValidated --> Quarantined : ChecksumMismatch / quarantine()
  Archived --> Quarantined : MissingFileDetected / quarantine()

  Quarantined --> Created : OperatorRelease / release()
  Quarantined --> [*] : Discard / recordAudit()

  PDSSubmitted --> [*] : Complete
}

note right of L
NFR-004: on checksum mismatch, missing file, schema failure:
alert SRE within 10 min; quarantine; log to error_audit_log.
end note

note bottom of L
NFR-008: PDS submission <= 6 months after acquisition.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_DailyPipeline
start
:ScheduleDailyRun;
note right
NFR-001: complete between 01:00-03:00 UTC;
failure alerts SRE within 10 min.
end note

:Connect ESOC;
repeat
  :AcquireTelemetry;
  :VerifyChecksum [IntegrityCheck];
repeat while (connection lost?) is (yes)
->no;

if (Missing cleaned-up by 02:00 UTC?) then (yes)
  :GenerateCleanedTelemetry;
  :ValidateSchema [IDFS/CleanSchema];
else (no)
  :IngestCleanedTelemetry;
  :ValidateSchema [IDFS/CleanSchema];
endif

fork
  :ProcessScienceToIDFS;
  :ValidateSchema [IDFS v1.3.2];
fork again
  :ProcessEngineeringToIDFS;
  :CalibrateEngineering;
  note right
  FR-003: absolute error < 2% per guide v3.4.
  end note
  :ValidateSchema [IDFS v1.3.2];
end fork

:ArchiveRawTelemetry;
:ArchiveIntermediateIfAny;
:ArchiveIDFSDatasets;
note right
ASR-004: retain >= 5 years; nightly incremental backup;
annual restore test >99% recovery.
end note

fork
  :UpdatePublicWebDisplay;
  note right
  FR-008: refresh < 15 min after ingestion;
failure triggers operator alert.
  end note
fork again
  :UpdateTeamWebDisplay [AuthRequired];
end fork

:DistributeToCoIs;
note right
NFR-005..007: deliver <=24h (conditional);
retry up to 3; notify errors within 2h.
end note

:BuildPDSSubmissionPackage;
:CalibrateAndValidateForPDS;
:SubmitToPDS;
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_S1_DailyIngestProcess
autonumber
actor "SRE" as SRE
participant "Scheduler" as Scheduler
participant "TelemetryIngestionService" as Ingest
participant "ESOCAdapter" as ESOCAdapter
database "RawTelemetryArchive" as RawArc
participant "TelemetryCleaningService" as CleanSvc
participant "IDFSProcessingService" as Proc
participant "SchemaValidationService" as Val
database "IDFSArchive" as IDFSArc
participant "MonitoringAlertingService" as Mon

Scheduler -> Ingest : StartDailyRun
Ingest -> ESOCAdapter : Connect
note right of ESOCAdapter
FR-001: retry policy max 5 attempts in 10 minutes
on connection loss.
end note

ESOCAdapter -> ESOCAdapter : AcquireFiles
ESOCAdapter --> Ingest : TelemetryFiles

Ingest -> Val : VerifyChecksum
alt checksum mismatch
  Val --> Ingest : ChecksumFail
  Ingest -> Ingest : QuarantineArtifact
  Ingest -> Mon : AlertFailure
  Mon --> SRE : Notify(<=10min)
  return
else ok
  Val --> Ingest : ChecksumOk
end

Ingest -> RawArc : StoreRawTelemetry

Ingest -> CleanSvc : CheckCleanedAvailability(02:00UTC)
alt cleaned missing
  CleanSvc -> CleanSvc : GenerateCleanedTelemetry
  CleanSvc -> Val : ValidateSchema
  alt schema nonconformance
    Val --> CleanSvc : SchemaFail
    CleanSvc -> Mon : AlertFailure
    Mon --> SRE : Notify(<=10min)
    return
  else pass
    Val --> CleanSvc : SchemaPass
  end
else cleaned provided
  CleanSvc -> Val : ValidateSchema
  Val --> CleanSvc : SchemaPass
end

CleanSvc --> Proc : CleanedTelemetryReady
Proc -> Proc : ProcessScienceToIDFS
Proc -> Proc : ProcessEngineeringToIDFS
Proc -> Val : ValidateSchema(IDFS v1.3.2)
Val --> Proc : ValidationResult

alt validation fail
  Proc -> Proc : QuarantineArtifact
  Proc -> Mon : AlertFailure
  Mon --> SRE : Notify(<=10min)
else pass
  Proc -> IDFSArc : StoreIDFSDatasets
end

Ingest -> Mon : EmitRunMetrics
Mon --> Scheduler : RunStatus
@enduml
```

```plantuml
@startuml Sequence_S2_TeamWebAccess
autonumber
actor "CoI" as CoI
participant "WebPortal" as WebPortal
participant "AuthService" as Auth
database "AccessAuditLog" as AccessLog
participant "IDFSQueryService" as Query
database "IDFSArchive" as IDFSArc

CoI -> WebPortal : OpenTeamWebDisplay
WebPortal -> Auth : Authenticate(MFA)
Auth -> AccessLog : LogAuthAttempt
Auth --> WebPortal : AuthToken

WebPortal -> Auth : Authorize(role=CoI)
Auth -> AccessLog : LogRBACAction
Auth --> WebPortal : Permit

WebPortal -> Query : QueryDatasets
Query -> IDFSArc : ReadIDFSData
IDFSArc --> Query : IDFSData
Query --> WebPortal : RenderData

note right of Auth
NFR-002: MFA required; logs retained >=180 days;
PI signoff logged for transition to public.
NFR-003: password policy and deprovisioning.
Session timeout 30 min (ASR-006).
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_S1_DailyIngestProcess
skinparam linetype ortho

object "Scheduler" as Scheduler
object "TelemetryIngestionService" as Ingest
object "ESOCAdapter" as ESOCAdapter
object "SchemaValidationService" as Val
object "TelemetryCleaningService" as CleanSvc
object "IDFSProcessingService" as Proc
object "RawTelemetryArchive" as RawArc
object "IDFSArchive" as IDFSArc
object "MonitoringAlertingService" as Mon
object "SRE" as SRE

Scheduler -- Ingest
Ingest -- ESOCAdapter
Ingest -- Val
Ingest -- RawArc
Ingest -- CleanSvc
CleanSvc -- Val
CleanSvc -- Proc
Proc -- Val
Proc -- IDFSArc
Ingest -- Mon
Mon -- SRE

Scheduler : 1 StartDailyRun
Ingest : 2 Connect
ESOCAdapter : 3 AcquireFiles
Val : 4 VerifyChecksum
RawArc : 5 StoreRawTelemetry
CleanSvc : 6 CheckCleanedAvailability
CleanSvc : 7 GenerateCleanedTelemetry (if missing)
Val : 8 ValidateSchema
Proc : 9 ProcessToIDFS
Val : 10 ValidateSchema(IDFS)
IDFSArc : 11 StoreIDFSDatasets
Mon : 12 AlertFailure (on error)

note right of Ingest
Scenario S1: Daily ingest + processing with retries, validation,
quarantine+alert on integrity failures (FR-001, NFR-001, NFR-004).
end note
@enduml
```

```plantuml
@startuml Collaboration_S2_TeamWebAccess
skinparam linetype ortho

object "CoI" as CoI
object "WebPortal" as WebPortal
object "AuthService" as Auth
object "AccessAuditLog" as AccessLog
object "IDFSQueryService" as Query
object "IDFSArchive" as IDFSArc

CoI -- WebPortal
WebPortal -- Auth
Auth -- AccessLog
WebPortal -- Query
Query -- IDFSArc

CoI : 1 OpenTeamWebDisplay
WebPortal : 2 Authenticate(MFA)
Auth : 3 LogAuthAttempt
WebPortal : 4 Authorize(role=CoI)
Auth : 5 LogRBACAction
WebPortal : 6 QueryDatasets
Query : 7 ReadIDFSData
WebPortal : 8 RenderData

note right of WebPortal
Scenario S2: Team web access with MFA, RBAC, and audit logging
(NFR-002, NFR-003, ASR-006).
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_APAF
skinparam packageStyle rectangle

package "ui" as ui {
  note top
  WebPortal: public + team displays (FR-008/FR-009)
  end note
}

package "application" as app {
  note top
  Orchestration + use-case services; scheduled daily run (NFR-001)
  end note
}

package "domain" as dom {
  note top
  IDFS/telemetry domain model; invariants (ASR-002/ASR-005)
  end note
}

package "integrations" as integ {
  note top
  ESOC adapter; PDS submission; Co-I distribution; repo integration
  (FR-001, FR-013, FR-010, FR-022)
  end note
}

package "persistence" as pers {
  note top
  Local archives, metadata, quarantine, audit logs (ASR-004/ASR-009)
  end note
}

package "security" as sec {
  note top
  AuthN/AuthZ, MFA, RBAC, session mgmt, password policy (ASR-006)
  end note
}

package "observability" as obs {
  note top
  Monitoring, alerting, error audit log (NFR-001, NFR-004, NFR-012)
  end note
}

ui ..> sec : uses
ui ..> app : uses
app ..> dom : uses
app ..> integ : uses
app ..> pers : uses
app ..> obs : uses
integ ..> dom : uses
integ ..> pers : uses
sec ..> pers : uses (audit)
obs ..> pers : uses (logs)

note bottom
ASR-010: internal interface contracts live in SDDs and are versioned
with references to project-unique requirement IDs (NFR-010).
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_APAF
skinparam componentStyle rectangle

component "WebPortal" as WebPortal <<UI>> [PublicWebDisplay/TeamWebDisplay]
component "AuthService" as AuthService <<Security>> [RBAC/MFA]
component "TelemetryIngestionService" as Ingest <<Service>> [AcquireTelemetry]
component "ESOCAdapter" as ESOCAdapter <<Adapter>> [protocolX/formatY]
component "TelemetryCleaningService" as CleanSvc <<Service>> [GenerateCleanedTelemetry]
component "IDFSProcessingService" as Proc <<Service>> [ProcessToIDFS]
component "SchemaValidationService" as Val <<Service>> [ValidateSchema]
component "ArchiveService" as ArchiveSvc <<Service>> [ArchiveArtifacts]
component "DistributionService" as DistSvc <<Service>> [DistributeToCoIs]
component "PDSSubmissionService" as PDSSvc <<Service>> [SubmitToPDS]
component "MonitoringAlertingService" as Mon <<Service>> [AlertOnFailure]
component "IDFSQueryService" as Query <<Service>> [QueryIDFS]

database "RawTelemetryArchive" as RawArc
database "IntermediateArchive" as IntArc
database "IDFSArchive" as IDFSArc
database "QuarantineStore" as Quarantine
database "AccessAuditLog" as AccessLog
database "ErrorAuditLog" as ErrorLog

interface "IAuth" as IAuth
interface "IESOC" as IESOC
interface "IValidate" as IValidate
interface "IArchive" as IArchive
interface "IDistribute" as IDistribute
interface "IPDSSubmit" as IPDSSubmit
interface "IQueryIDFS" as IQueryIDFS

WebPortal - IAuth
AuthService ..|> IAuth
AuthService --> AccessLog : writes

Ingest - IESOC
ESOCAdapter ..|> IESOC

Proc - IValidate
Val ..|> IValidate

ArchiveSvc - IArchive
ArchiveSvc ..|> IArchive

DistSvc - IDistribute
DistSvc ..|> IDistribute

PDSSvc - IPDSSubmit
PDSSvc ..|> IPDSSubmit

Query - IQueryIDFS
Query ..|> IQueryIDFS

Ingest --> ESOCAdapter : uses
Ingest --> Val : uses
Ingest --> RawArc : stores
Ingest --> Quarantine : quarantines
Ingest --> Mon : emits

CleanSvc --> Val : uses
CleanSvc --> IntArc : stores
CleanSvc --> Quarantine : quarantines
CleanSvc --> Mon : emits

Proc --> Val : uses
Proc --> IDFSArc : stores
Proc --> Quarantine : quarantines
Proc --> Mon : emits

ArchiveSvc --> RawArc : manages
ArchiveSvc --> IntArc : manages
ArchiveSvc --> IDFSArc : manages

DistSvc --> IDFSArc : reads
DistSvc --> IntArc : reads
DistSvc --> Mon : alerts

PDSSvc --> IDFSArc : reads
PDSSvc --> Val : validates
PDSSvc --> Mon : alerts

Mon --> ErrorLog : writes

note right of ESOCAdapter
FR-001: retry max 5 attempts/10 min on connection loss.
end note

note right of Val
NFR-004: detect checksum mismatch, missing file, schema nonconformance;
quarantine + alert within 10 min; log reviewable within 1 hour.
end note

note bottom of WebPortal
FR-008: public display refresh <15 min after ingestion; failure alerts operator.
ASR-006: mixed public/restricted access with RBAC + audit.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_APAF
skinparam componentStyle rectangle

node "SwRI On-Prem Network" as SwRI {
  node "APAF App Server (VM)" as AppVM {
    artifact "WebPortal" as aWeb
    artifact "AuthService" as aAuth
    artifact "TelemetryIngestionService" as aIngest
    artifact "ESOCAdapter" as aESOC
    artifact "TelemetryCleaningService" as aClean
    artifact "IDFSProcessingService" as aProc
    artifact "SchemaValidationService" as aVal
    artifact "ArchiveService" as aArchive
    artifact "DistributionService" as aDist
    artifact "PDSSubmissionService" as aPDS
    artifact "IDFSQueryService" as aQuery
    artifact "MonitoringAlertingService" as aMon
    artifact "Scheduler" as aSched
  }

  node "Archive Storage (NAS)" as NAS {
    database "RawTelemetryArchive" as dRaw
    database "IntermediateArchive" as dInt
    database "IDFSArchive" as dIDFS
    database "QuarantineStore" as dQ
  }

  node "Logs Storage" as Logs {
    database "AccessAuditLog" as dAccess
    database "ErrorAuditLog" as dError
  }

  node "Backup System" as Backup {
    artifact "NightlyIncrementalBackup" as bkp
    artifact "AnnualRestoreTest" as rst
  }
}

cloud "ESOC Systems" as ESOC
cloud "NASA PDS" as PDS
cloud "Co-I Endpoints" as COI
cloud "NASA Approved Repo" as Repo

ESOC --> AppVM : protocolX/formatY\n(retry 5/10min)
AppVM --> NAS : NFS/SMB
AppVM --> Logs : write logs
NAS --> Backup : nightly backup
Backup --> NAS : restore test

AppVM --> COI : electronic distribution\n(<=24h conditional)
AppVM --> PDS : PDS submission\n(<=6 months)
AppVM --> Repo : publish analysis software

note right of AppVM
NFR-001: daily run completes 01:00-03:00 UTC.
NFR-012: uptime >=99.7% measured by service_monitor.
end note

note right of NAS
ASR-004: retain >=5 years; nightly incremental backup;
annual restore test >99% recovery.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_APAF
skinparam rectangleStyle rounded
left to right direction

rectangle "APAF System (SwRI On-Prem)" as APAF {
  rectangle "WebPortal" as WebPortal
  note right of WebPortal
  [PublicWebDisplay/TeamWebDisplay]
  Public: current data
  Team: all data (RBAC)
  end note

  rectangle "Backend Services" as Backend {
    rectangle "TelemetryIngestionService" as Ingest
    rectangle "TelemetryCleaningService" as CleanSvc
    rectangle "IDFSProcessingService" as Proc
    rectangle "SchemaValidationService" as Val
    rectangle "ArchiveService" as ArchiveSvc
    rectangle "DistributionService" as DistSvc
    rectangle "PDSSubmissionService" as PDSSvc
    rectangle "IDFSQueryService" as Query
    rectangle "AuthService" as Auth
    rectangle "MonitoringAlertingService" as Mon
    rectangle "Scheduler" as Scheduler
  }

  database "RawTelemetryArchive" as RawArc
  database "IntermediateArchive" as IntArc
  database "IDFSArchive" as IDFSArc
  database "QuarantineStore" as Quarantine
  database "AccessAuditLog" as AccessLog
  database "ErrorAuditLog" as ErrorLog
}

cloud "ESOC" as ESOC
cloud "Co-I Users/Systems" as CoI
cloud "Public Users" as Public
cloud "NASA PDS" as PDS
cloud "IRF" as IRF
cloud "NASA Approved Repo" as Repo

Public --> WebPortal : view current
CoI --> WebPortal : view team displays
WebPortal --> Auth : authenticate/authorize
Auth --> AccessLog : audit (>=180 days)

Scheduler --> Ingest : daily run (01:00-03:00 UTC)
Ingest --> ESOC : acquire (protocolX/formatY)
Ingest --> Val : checksum/schema checks
Val --> Quarantine : quarantine on failure
Val --> Mon : alert (<=10 min)
Mon --> ErrorLog : error_audit_log

Ingest --> RawArc : store raw
CleanSvc --> IntArc : store intermediate
Proc --> IDFSArc : store IDFS (schema v1.3.2)
ArchiveSvc --> RawArc
ArchiveSvc --> IntArc
ArchiveSvc --> IDFSArc

Query --> IDFSArc : read for displays
WebPortal --> Query : query

DistSvc --> IDFSArc : read
DistSvc --> IntArc : read
DistSvc --> CoI : distribute (<=24h conditional)

PDSSvc --> IDFSArc : read
PDSSvc --> PDS : submit (<=6 months)

Backend --> IRF : provide algorithms (out-of-band)
Backend --> Repo : integrate analysis software

note bottom of APAF
ASR-009/NFR-004: detect checksum mismatch, missing file, schema nonconformance;
quarantine + alert + audit logging.
ASR-006: mixed public/restricted access with RBAC, MFA, session timeout 30 min.
end note
@enduml
```