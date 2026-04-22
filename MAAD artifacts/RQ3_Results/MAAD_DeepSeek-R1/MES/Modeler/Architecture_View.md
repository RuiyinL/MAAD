## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCaseDiagram
left to right direction
actor Timer
actor ESOC as "ESOC"
actor PublicUser as "PublicUser"
actor InternalUser as "InternalUser"
actor NASA_PDS as "NASA_PDS"
actor IRF as "IRF"

usecase (UC01: AcquireDailyTelemetry) as UC01
usecase (UC02: ProcessToIDFS) as UC02
usecase (UC03: ArchiveProcessedData) as UC03
usecase (UC04: DistributeToCoIs) as UC04
usecase (UC05: SubmitToPDS) as UC05
usecase (UC06: DisplayPublicData) as UC06
usecase (UC07: DisplayTeamData) as UC07
usecase (UC08: MonitorErrorAlerts) as UC08
usecase (UC09: RetrieveAlgorithms) as UC09

Timer --> UC01 : Triggers
ESOC --> UC01 : Provides data
Timer --> UC04 : Triggers
Timer --> UC05 : Triggers
PublicUser --> UC06
InternalUser --> UC07
InternalUser --> UC08
IRF --> UC09

UC01 .> UC02 : <<include>>
UC01 .> UC03 : <<include>>
UC04 .> UC03 : <<extend>> \n(If archived)

note right of UC07
  <<PasswordProtected>>
  according to FR-010, FR-015
end note

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml ClassDiagram
class TelemetryData {
  +source: String
  +timestamp: DateTime
  +rawPayload: byte[]
  +status: ProcessingStatus
  +validateSchema()
}

class IDFSDataSet {
  +datasetType: DataType
  +version: String
  +referenceSchemaId: String
  +content: byte[]
  +convertToPDSCompliant()
}

class ProcessingJob {
  -jobId: UUID
  +scheduleTime: DateTime
  +completionDeadline: DateTime
  +currentState: JobState
  +executeProcessing()
}

class WebDisplay {
  +displayType: DisplayType
  +dataViewConfig: JSON
  +generateView()
}

class ErrorLog {
  +errorCode: String
  +timestamp: DateTime
  +severity: ErrorSeverity
  +quarantineDataId: String
  +generateAlert()
}

class DataArchive {
  +archiveId: String
  +retentionPeriod: int
  +backupSchedule: String
  +retrieveDataset()
}

TelemetryData "1" -- "1" IDFSDataSet : processed to >
ProcessingJob "1" -- "*" TelemetryData : processes >
ProcessingJob "1" -- "1" ErrorLog : manages >
WebDisplay "1" -- "*" IDFSDataSet : consumes >
DataArchive "1" -- "*" IDFSDataSet : stores >
DataArchive "1" -- "*" TelemetryData : stores >

note top of TelemetryData
  <<persisted>>
  Archived locally per ASR-003
end note

note bottom of IDFSDataSet
  <<immutable>> after generation
  PDS compliance via FR-020
end note

@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml ObjectDiagram
object telemetry_20231005 as "telemetry_20231005 : TelemetryData" 
telemetry_20231005 : source = "ESOC"
telemetry_20231005 : status = RAW

object science_dataset_001 as "science_dataset_001 : IDFSDataSet"
science_dataset_001 : datasetType = SCIENCE
science_dataset_001 : version = "1.2.0"

object job_4421 as "job_4421 : ProcessingJob"
job_4421 : currentState = RUNNING

object cleaning_job as "cleaning_job : ProcessingJob" 
cleaning_job : scheduleTime = 2023-10-05T01:00Z

telemetry_20231005 --> science_dataset_001 : becomes
job_4421 --> telemetry_20231005 : processes
cleaning_job --> job_4421 : precedes
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml StateDiagram
state ProcessingPipeline {
  [*] --> Created : DataReceived
  Created --> Validated : SchemaValidation
  Validated : Entry / log timestamp
  Validated --> Processed : ProcessJobCompletion
  state fork_state <<fork>>
  Processed --> fork_state
  fork_state --> Archived : StorageCompletion
  fork_state --> PDSReady : PDSComplianceCheck
  Archived --> Distrubuted : DistributionTrigger
  fork_state --> Quarantined : ValidationError 
  Quarantined --> [*] : Resolved
  Distributed --> [*] : CoIDelivery
  PDSReady --> Submitted : PDSTransfer
  Submitted --> [*] : ConfirmationReceived
}
Quarantined: Critical incident\ngenerates alerts per FR-011
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml ActivityDiagram
start
partition "Daily Processing Workflow" {
  :Acquire Telemetry from ESOC;
  fork
    :Check ESOC_clean flag?;
    if (Clean available?) then (yes)
      :Use ESOC telemetry;
    else (no)
      :Generate cleaned telemetry;
      :Archive intermediate file;
    endif
  fork again
    :Process science data to IDFS;
    :Process engineering data to IDFS;
  fork again
    :Perform schema validation;
    if (Validation passed?) then (yes)
      :Update metadata;
    else (no)
      #red:(Quarantine dataset);
      :Trigger alert;
      stop
    endif
  end fork
  :Archive processed IDFS;
}
partition ErrorHandling {
  group Concurrent monitoring [ErrorHandling]
    :Detect timeout?;
    if (Deadline exceeded?) then (yes)
      #red:Log SLA violation;
      :Notify operations team;
    else (no)
    endif
  end
}
:Distribute to IDFS to Co-I's;
stop

note right
  **SLA Constraints**
  All steps must complete by 03:00 UTC
  per NFR-001
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram 
```plantuml
@startuml SequenceDailyProcessing
participant Timer
participant IngestService
participant ProcessingEngine
participant ValidationService
participant ArchiveService
participant ErrorMonitor

Timer -> IngestService: TriggerAcquisition
activate IngestService
IngestService -> ESOC: RequestTelemetry
ESOC --> IngestService: ReturnTelemetryData
IngestService -> ProcessingEngine: ProcessRawData(telemetry)
activate ProcessingEngine
ProcessingEngine -> ValidationService: ValidateSchema(data)
activate ValidationService
ValidationService -> ValidationService: CheckFormat(IDFSv1)
alt Schema valid
  ValidationService --> ProcessingEngine: ValidationPassed
  ProcessingEngine -> ProcessingEngine: TransformToIDFS
else Schema invalid
  ValidationService --> ProcessingEngine: ValidationFailed
  ProcessingEngine -> ErrorMonitor: QueueAlert(errorDetails)
  activate ErrorMonitor
  ErrorMonitor -> ErrorMonitor: QuarantineData
  ErrorMonitor --> ProcessingEngine
end
ProcessingEngine --> IngestService: ProcessedDataSet
deactivate ProcessingEngine
IngestService -> ArchiveService: PersistDataset
ArchiveService --> IngestService: StorageReceipt
deactivate IngestService
@enduml
```

```plantuml
@startuml SequenceWebAccess
participant PublicUser
participant WebGateway
participant AuthService
participant DisplayService
participant DataRepository

PublicUser -> WebGateway: RequestPublicDisplay
WebGateway -> DisplayService: GetLatestPublicData
DisplayService -> DataRepository: QueryPublicIDFS
DataRepository --> DisplayService: ReturnDisplayData
DisplayService --> WebGateway: RenderHTML+JSON
WebGateway --> PublicUser: DisplayScienceView

InternalUser -> WebGateway: RequestTeamDisplay
WebGateway -> AuthService: Authenticate(credentials)
AuthService --> WebGateway: RBAC_Token(CoI_Role)
WebGateway -> DisplayService: GetDetailedScienceData
DisplayService -> DataRepository: QueryAllIDFS
DataRepository --> DisplayService: ReturnFullDataset
DisplayService --> WebGateway: RenderTeamView
WebGateway --> InternalUser: DisplayTeamDashboard

note right of AuthService
  <<Validation>> Role enforcement
  per FR-015 (RBAC protection)
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml CollaborationDiagram
component Timer
component ProcessingService
component ValidationService
component ESOC
component ArchiveSystem
component CoIAccessPoint

Timer::1.Calls ---> ProcessingService:: : T+00:00
ProcessingService::2.RequestData ---> ESOC:: : T+00:05
ESOC::3.Provides --> ProcessingService:: : T+00:10
ProcessingService::4.Validates --> ValidationService:: : T+00:15
ValidationService::5.Confirms --> ProcessingService:: : T+00:20
ProcessingService::6.Archives --> ArchiveSystem:: : T+00:45
ArchiveSystem::7.Confirms --> ProcessingService:: : T+01:00
ProcessingService::8.Notifies ---> CoIAccessPoint:: : T+01:05

note top
  Critical path timeline follows
  NFR-001 deadline constraints
end note
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml

' ===== Packages =====
package "Data Acquisition" as DA {
  [Telemetry Reader] as TR
  [ESOC Adapter] as EA
}

package "Processing Core" as PC {
  [IDFS Transformer] as IT
  [Validation Engine] as VE
  [Science Processor] as SP
}

package "Storage" as ST {
  [Archive Manager] as AM
  [Object Repository] as OR
}

package "Distribution" as DI {
  [CoI Delivery] as CD
  [PDS Exporter] as PE
}

package "Web Presentation" as WP {
  [Public UI] as UI
  [Team Portal] as TP
}

package "Security" as SEC {
  [RBAC Service] as RBAC
}

package "Error Handling" as EH {
  [Quarantine Manager] as QM
  [Alerting System] as AS
}

' ===== Package-level relationships =====
DA -- PC
PC -- ST
PC --> EH
ST -- DI
WP --> SEC

' ===== Component-level relationship =====
DI --> PE

' ===== Note =====
note bottom of ST
  Retention:
  >=5 years per ASR-003
end note

@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml

skinparam componentStyle rectangle

' ===== Components =====
component DataIngestion <<Async>>

component IDFSProcessor <<Transactional>>

component ArchiveManagement <<Persistent>>

component DistributionHub <<Scheduled>>

component WebPresentation <<REST>>

component SecurityPackage <<SharedUtility>>

component "ErrorFramework <<Crosscutting>>

' ===== Interfaces =====
interface ischema
interface ipds

' ===== Relationships =====
DataIngestion --> IDFSProcessor : RawTelemetry
IDFSProcessor --> ischema : validates
IDFSProcessor --> ArchiveManagement : VerifiedIDFS
ArchiveManagement --> DistributionHub : ArchivedData
DistributionHub --> ipds : PDSSubmission
WebPresentation -- ArchiveManagement : QueryMetadata
SecurityPackage -- WebPresentation : enforceRBAC

' ===== Error Handling =====
ErrorFramework ..> DataIngestion : Listens for failures
ErrorFramework ..> IDFSProcessor : Schema fails
ErrorFramework ..> ArchiveManagement : Storage alerts

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml DeploymentDiagram
node "Primary Data Center" {
  node "Linux Cluster" {
    artifact BatchProcessingServer_1 as batch1 
    artifact BatchProcessingServer_2 as batch2
    database ArchiveStorage_1 as db1
    database ArchiveStorage_2 as db2
  }
  
  artifact RESTGateway_1 as web1 
  artifact RESTGateway_2 as web2
}

node "ESOC Data Source" {
  artifact ExternalFeedProxy 
}

node "Co-I Access Zone" {
  fleet CoI_DeliveryNode [5]
}

cloud "NASA PDS Registry" {
  component PDSApiGateway
}

BatchProcessingServer_1 -[#blue] DB_LAN--> db1 : 10GbE
batch2 -[#blue] DB_LAN--> db2 : 10GbE
web1 -[#red] SAN--> db1 : iSCSI
web2 -[#red] SAN--> db2 : iSCSI
ExternalFeedProxy -[#green] Internet--> BatchProcessingServer_1 : SFTP
ExternalFeedProxy -[#green] Internet--> batch2
CoI_DeliveryNode -[#blue] Intranet- BatchProcessingServer_1
BatchProcessingServer_1 -[#orange] TLS--> PDSApiGateway

note right of BatchProcessingServer_1
  **Redundancy:** Active/Active config
  **Performance:** SLA 03:00 UTC daily
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml ContainerDiagram
node "Virtualized Environment" {
  container RestGateway [
    RESTful Gateway
    - Nginx reverse proxy
    - API routing rules
  ] <<K8s Pod>>

  container BatchProcessing [
    Data Pipeline Controller
    - Apache Airflow
    - Job scheduling
  ] <<Job Scheduler>>

  container ProcessingWorker [
    Transform Worker
    - Python + C extensions
    - Memory: 16GB
  ] <<K8s Deployment>> {
    component ScienceProcessor
    component DataValidator
  }

  database ObjectStorage [
    MinIO Cluster
    - Binary object store
    - S3-compatible
  ] <<Replicated Storage>>

  container Messaging [
    Kafka Cluster
    - Error alerts stream
    "partitions=6"
  ] <<Message Broker>>

  container PDSExporter [
    PDS Submission Agent
    - Crontab schedule
    - On-prem service
  ]

  container AuditDashboard [
    Security Monitor
    - Kibana dashboard
    - Audit log analysis
  ]

  ProcessingWorker - ObjectStorage: Writes datasets
  BatchProcessing --> ProcessingWorker: Controls jobs
  ProcessingWorker -> Messaging: Reports failures
  RestGateway - ObjectStorage: Retrieves data
  PDSExporter - ObjectStorage: Exports datasets
  AuditDashboard - Messaging: Consumes error logs

  note right of ObjectStorage
    **Scalability:** MinIO cluster expands to PB
    **Guarantees:** Data versioning + encryption
    per ASR-003
  end note
}
@enduml
```