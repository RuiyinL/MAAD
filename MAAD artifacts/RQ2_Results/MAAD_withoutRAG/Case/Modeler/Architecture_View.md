## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_ScenarioView
left to right direction
skinparam packageStyle rectangle

actor Nurse as Nurse
actor MedicalStaff as MedicalStaff
actor "NursesStationSystem" as NursesStationSystem
actor Visitor as Visitor
actor Operator as Operator
actor Overseer as Overseer
actor "DoorUser" as DoorUser
actor "LibraryStaff" as LibraryStaff
actor "LibraryMember" as LibraryMember
actor "PCUser" as PCUser
actor "CourtMember" as CourtMember

rectangle "CyberPhysical Control Platform" {
  usecase "MonitorVitals" as UC_MonitorVitals
  usecase "ManageSafeRanges" as UC_ManageSafeRanges
  usecase "SendICUAlerts" as UC_SendICUAlerts
  usecase "AttemptDoorEntry" as UC_AttemptDoorEntry
  usecase "OperateTurnstile" as UC_OperateTurnstile
  usecase "ControlTrafficLights" as UC_ControlTrafficLights
  usecase "OverrideTrafficPhase" as UC_OverrideTrafficPhase
  usecase "OperateSluiceGate" as UC_OperateSluiceGate
  usecase "ControlHeating" as UC_ControlHeating
  usecase "ManageLibrary" as UC_ManageLibrary
  usecase "GenerateReports" as UC_GenerateReports
  usecase "ShowPCConfig" as UC_ShowPCConfig
  usecase "StartLightingSession" as UC_StartLightingSession
}

Nurse --> UC_SendICUAlerts
MedicalStaff --> UC_ManageSafeRanges
NursesStationSystem --> UC_SendICUAlerts

DoorUser --> UC_AttemptDoorEntry

Visitor --> UC_OperateTurnstile

Operator --> UC_OperateSluiceGate
Overseer --> UC_OverrideTrafficPhase
Operator --> UC_ControlTrafficLights

Operator --> UC_ControlHeating

LibraryStaff --> UC_ManageLibrary
LibraryStaff --> UC_GenerateReports
LibraryMember --> UC_ManageLibrary

PCUser --> UC_ShowPCConfig

CourtMember --> UC_StartLightingSession

UC_MonitorVitals .> UC_SendICUAlerts : <<include>>
UC_ManageSafeRanges .> UC_SendICUAlerts : <<include>>

UC_ControlTrafficLights .> UC_OverrideTrafficPhase : <<extend>>
UC_OperateSluiceGate .> UC_ControlTrafficLights : <<extend>>

note right of UC_MonitorVitals
assumption: ICU monitoring and persistence are triggered by system scheduler,
with nurses notified via NursesStationSystem.
end note

note right of UC_ControlTrafficLights
assumption: Traffic light controller runs autonomously; operator interacts only for override/config.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_LogicView
skinparam classAttributeIconSize 0

class PluginManager {
  +loadPlugin(pluginId: String)
  +startAll()
  +stopAll()
}

class EventBus {
  +publish(eventType: String, payload: String)
  +subscribe(eventType: String, handlerId: String)
}

interface HardwareIO {
  +readPort(portId: String): int
  +writePort(portId: String, value: int)
  +readRegister(addr: int): int
  +writeRegister(addr: int, value: int)
  +emitPulse(lineId: String, durationMs: int)
  +readStatus(lineId: String): boolean
}

class Scheduler {
  +registerPeriodic(jobId: String, periodMs: int)
  +cancel(jobId: String)
  +validatePeriod(periodMs: int): boolean
}

class AuditLogger {
  +logAccess(userId: String, action: String, resourceId: String)
  +logSecurity(eventId: String, outcome: String)
  +logError(message: String)
}

class MetricsCollector {
  +observe(name: String, value: double)
  +inc(name: String)
}

class PatientMonitor «persisted» {
  -patientId: String
  -samplingPeriodMs: int
  +readVitals(io: HardwareIO): VitalMeasurement
  +detectDeviceFailure(io: HardwareIO): boolean
}

class SafeRange «persisted» {
  -patientId: String
  -factor: String
  -minValue: double
  -maxValue: double
  +isOutOfRange(value: double): boolean
}

class VitalMeasurement «persisted» {
  -measurementId: String
  -patientId: String
  -timestampUtc: String
  -pulse: int
  -temperatureC: double
  -systolicMmHg: int
  -diastolicMmHg: int
  -skinResistanceOhm: double
  +checksum(): String
}

class Alert {
  -alertId: String
  -timestampUtc: String
  -severity: String
  -category: String
  -message: String
  +formatForStation(): String
}

class DoorAccessAttempt {
  -attemptId: String
  -timestampUtc: String
  -cameraId: String
  +extractFrame(): String
}

class FaceTemplate «persisted» {
  -subjectId: String
  -templateCiphertext: String
  -expiresOn: String
  +isExpired(now: String): boolean
}

class AccessDecision {
  -attemptId: String
  -result: String
  -latencyMs: int
  +isAllowed(): boolean
}

class TurnstileSession {
  -sessionId: String
  -coinsInserted: int
  -state: String
  +insertCoin()
  +allowEntry(io: HardwareIO)
  +denyEntry(io: HardwareIO