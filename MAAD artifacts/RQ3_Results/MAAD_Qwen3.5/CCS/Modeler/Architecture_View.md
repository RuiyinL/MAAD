## Architecture Summary & Quality-Attribute Analysis

**Architecture Summary**
The proposed architecture for the Correlator Monitor and Control System (CMCS) is a **Hierarchical Master/Slave System with a Secure Gateway**. It features redundant Master Control Computers (Primary/Secondary) that manage intelligent slave nodes (CMIBs) responsible for real-time hardware interaction. A Virtual Correlator Interface (VCI) acts as the single secure entry point for all external configurations and commands, enforcing security and translation logic. The system is segmented into distinct network zones (Control, Power, Operations) to ensure determinism and security. Autonomous health monitoring agents reside on all nodes, utilizing hardware watchdogs and UPS integration for self-healing and graceful degradation.

**Quality-Attribute Analysis**
*   **Availability & Reliability**: Driven by ASR-003 (Redundant Masters) and ASR-009 (Watchdog/UPS).
    *   *Risk*: State replication lag between masters could cause data inconsistency during failover.
    *   *Mitigation*: Synchronous replication for critical state, asynchronous for logs.
*   **Security**: Driven by ASR-002 (VCI Gateway) and ASR-008 (Audit/Access).
    *   *Risk*: VCI becomes a single point of failure or bottleneck.
    *   *Mitigation*: VCI is clustered behind a load balancer; strict network segmentation (ASR-005).
*   **Performance & Determinism**: Driven by ASR-004 (Load Separation).
    *   *Risk*: Network chaos on Master affecting Slave real-time deadlines.
    *   *Mitigation*: Physical network separation and local buffering on CMIBs (FR-010).
*   **Maintainability**: Driven by FR-020 (Modular Replaceability) and FR-027 (Source Availability).
    *   *Trade-off*: Hot-swap capability increases hardware complexity and cost.

**Recommended Architecture Style**
**Layered Master/Slave with Event-Driven Monitoring**.
*   **Justification**:
    *   **Master/Slave (ASR-001)**: Directly maps to the physical control hierarchy (Master Computer -> CMIB -> Hardware).
    *   **Layered**: Separates UI (GUI), Business Logic (VCI/Control), and Hardware Abstraction (CMIB), addressing Maintainability and Security.
    *   **Event-Driven**: Used for Health Monitoring and Alerting (FR-003, FR-013), allowing asynchronous processing of faults without blocking control loops.

## Architectural Style & Rationale

**Primary Style: Hierarchical Master/Slave**
*   **Rationale**: The requirements explicitly demand a Master/Slave topology (ASR-001) where the Master coordinates activities and Slaves (CMIBs) handle intelligent hardware control. This supports the **Scalability** (add more CMIBs) and **Reliability** (Master manages state) needs.
*   **Link to Requirements**: ASR-001, FR-001, FR-024.

**Secondary Style: Layered (n-tier)**
*   **Rationale**: Separation of concerns is critical.
    *   *Presentation Layer*: Human GUI (FR-008) & Remote Login (FR-019).
    *   *Application Layer*: VCI Gateway (ASR-002), Control Logic.
    *   *Data Layer*: Configuration DB, Log Storage (FR-020).
    *   *Device Layer*: CMIBs, Power Control.
*   **Link to Requirements**: ASR-002, FR-005, FR-018.

**Hybrid Interaction**: The Master/Slave structure exists primarily in the lower two layers (Application/Device). The upper layers interact with the "Master" node via the VCI, abstracting the underlying topology.

## Architecture Patterns & Tactics

**1. Gateway Pattern (VCI)**
*   **Application**: All external requests pass through the Virtual Correlator Interface.
*   **Addresses**: Security (ASR-008), Translation (FR-001), Interoperability (ASR-002).
*   **Tactic**: Centralized authentication and schema validation before commands reach the control logic.

**2. Active-Passive Redundancy (Failover)**
*   **Application**: Primary and Secondary Master Control Computers.
*   **Addresses**: Availability (ASR-003), Reliability (NFR-011).
*   **Tactic**: Heartbeat monitoring between Masters; automatic IP rerouting (FR-016) upon failure detection.

**3. Observer Pattern (Health Monitoring)**
*   **Application**: Health Monitor subsystem observing CMIBs and OS metrics.
*   **Addresses**: Reliability (ASR-006), Observability (FR-003).
*   **Tactic**: Polling/Interrupts trigger alerts and recovery scripts autonomously.

**4. Bulkhead Pattern (Network Segmentation)**
*   **Application**: Separate physical interfaces for Control, Power, and Ops networks.
*   **Addresses**: Security (ASR-005), Performance (NFR-004).
*   **Tactic**: Physical isolation prevents traffic spikes or attacks on one network from affecting critical control loops.

## 4+1 View Diagrams

## ScenarioView
1. UseCase — Scenario View: Use Case Diagram

```plantuml
@startuml UseCaseDiagram
title CMCS Scenario View - Use Cases

actor "Operator" as Operator
actor "Admin" as Admin
actor "VLA Expansion System" as VLA_System
actor "CMIB Hardware" as CMIB_HW

rectangle "Correlator Monitor & Control System" {
  usecase "Configure Correlator" as UC_Config
  usecase "Monitor Health" as UC_Monitor
  usecase "Autonomous Recovery" as UC_Recover
  usecase "Access System (Remote)" as UC_Access
  usecase "Manage Users" as UC_Users
  usecase "View Logs/Audit" as UC_Logs
  usecase "Receive External Config" as UC_ExtConfig
}

Operator --> UC_Config
Operator --> UC_Monitor
Operator --> UC_Access
Operator --> UC_Logs

Admin --> UC_Users
Admin --> UC_Access
Admin --> UC_Logs
Admin --> UC_Config

VLA_System --> UC_ExtConfig
VLA_System --> UC_Monitor

CMIB_HW --> UC_Recover
CMIB_HW --> UC_Monitor

UC_Config ..> UC_Access : <<include>>
UC_ExtConfig ..> UC_Config : <<extends>>
UC_Recover ..> UC_Logs : <<include>>

note right of UC_Recover
  Triggered by Watchdog
  or Health Check
  (FR-003, ASR-006)
end note

note left of UC_ExtConfig
  Via VCI Gateway
  (ASR-002)
end note

@enduml
```

## LogicView
2. Class — Logic View: Class Diagram

```plantuml
@startuml ClassDiagram
title CMCS Logic View - Class Diagram

class "MasterControlComputer" as Master {
  +state: SystemState
  +replicateState()
  +failover()
  +routeCommand()
}

class "CMIB" as CMIB {
  +id: String
  +status: HealthStatus
  +configVersion: String
  +executeConfiguration()
  +readBoardID()
  +reportHealth()
}

class "VCIGateway" as VCI {
  +validateSchema()
  +translateConfig()
  +auditAccess()
}

class "HealthMonitor" as Monitor {
  +thresholds: Map
  +checkHeartbeat()
  +triggerRecovery()
  +alertOperator()
}

class "Configuration" as Config {
  +version: String
  +parameters: JSON
  +timestamp: DateTime
}

class "AuditLog" as Log {
  +user: String
  +action: String
  +timestamp: DateTime
  +persist()
}

Master "1" -- "1..*" CMIB : controls >
Master "1" -- "1" VCI : exposes >
Master "1" -- "1..*" Monitor : contains >
CMIB "1" -- "0..*" Config : holds >
Master -- Log : writes >
VCI -- Log : writes >

note "Redundant Pair" as Note1
Note1 .. Master : NFR-011

note "Real-time Edge" as Note2
Note2 .. CMIB : ASR-004

@enduml
```

3. Object — Logic View: Object Diagram

```plantuml
@startuml ObjectDiagram
title CMCS Logic View - Object Diagram

object "PrimaryMaster" as Master1 [MasterControlComputer] {
  state = "Active"
  role = "Primary"
}

object "SecondaryMaster" as Master2 [MasterControlComputer] {
  state = "Standby"
  role = "Secondary"
}

object "CMIB_01" as CMIB1 [CMIB] {
  id = "CMIB-001"
  status = "Operational"
  configVersion = "v2.1"
}

object "CurrentConfig" as C1 [Configuration] {
  version = "v2.1"
  timestamp = "2023-10-27T10:00:00Z"
}

object "VCI_Service" as VCI1 [VCIGateway] {
  status = "Listening"
}

Master1 --> CMIB1 : controls
Master1 --> VCI1 : exposes
Master1 --> Master2 : replicates state
CMIB1 --> C1 : uses
VCI1 --> Master1 : routes

note "Scenario: Normal Operation\n[MonitorHealth]" as N1
N1 .. Master1

@enduml
```

4. State — Logic View: State Diagram

```plantuml
@startuml StateDiagram
title CMCS Logic View - System State Diagram

[*] --> Booting
Booting --> Operational : Config Loaded
Booting --> Failed : Boot Error

Operational --> Degraded : Minor Fault Detected
Degraded --> Operational : Auto-Recovery Success
Degraded --> Failed : Recovery Failed

Operational --> Maintenance : Admin Request
Maintenance --> Operational : Maintenance Complete

Failed --> Recovering : Watchdog Trigger
Recovering --> Operational : Reboot Success
Recovering --> Failed : Reboot Failed

state Failed {
  [*] --> Alerting
  Alerting --> WaitingRepair : Alert Sent
}

note right of Operational
  Normal Control Loop
  (FR-003)
end note

note left of Recovering
  Autonomous Action
  (ASR-006)
end note

@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram

```plantuml
@startuml ActivityDiagram
title CMCS Process View - Health Monitoring & Recovery

start

:Receive Heartbeat/Status;
:Check Thresholds (CPU, Temp, Error Rate);
if (Threshold Exceeded?) then (Yes)
  :Log Fault Event;
  :Attempt Autonomous Recovery (Reboot/Reconfig);
  if (Recovery Success?) then (Yes)
    :Update State to Operational;
    :Log Recovery Success;
  else (No)
    :Send Alert to Operator (Email/SMS);
    :Update State to Failed;
    :Trigger Failover (if Master);
  endif
else (No)
  :Update State to Operational;
endif

:Wait for Next Interval (10s);
stop

note right of Attempt Autonomous Recovery
  Must complete within 60s
  (FR-003)
end note

note bottom of Send Alert
  Log to audit.log
  (FR-020)
end note

@enduml
```

6. Sequence — Process View: Sequence Diagram

```plantuml
@startuml SequenceDiagram
title CMCS Process View - Sequence Diagram (Scenario 1: Configuration Update)

actor Operator
participant "VCI Gateway" as VCI
participant "Master Control" as Master
participant "CMIB" as CMIB
participant "Audit Log" as Log

Operator -> VCI : Submit Configuration (JSON)
activate VCI
VCI -> VCI : Validate Schema (FR-002)
VCI -> Log : Log Access Attempt
VCI -> Master : Translate & Forward Config
activate Master
Master -> CMIB : Update Hardware Config
activate CMIB
CMIB -> CMIB : Apply Config
CMIB --> Master : Acknowledge
deactivate CMIB
Master --> VCI : Confirm Update
deactivate Master
VCI --> Operator : Success Response
deactivate VCI

note right of VCI
  Security Check &
  Translation (ASR-002)
end note

newpage

title CMCS Process View - Sequence Diagram (Scenario 2: Autonomous Recovery)

participant "Watchdog Timer" as Watchdog
participant "OS/Kernel" as OS
participant "Health Monitor" as Monitor
participant "Alert System" as Alert

Watchdog -> OS : Timeout (System Hang)
OS --> Watchdog : No Response
Watchdog -> OS : Trigger Reboot
OS --> OS : Reboot
OS -> Monitor : System Restarted
Monitor -> Monitor : Check Health Status
Monitor -> Alert : Log Recovery Event
Monitor -> Alert : Send Alert if Failed > 1 attempt

note left of Watchdog
  Hardware Based
  (FR-022)
end note

@enduml
```

7. Collaboration — Process View: Collaboration Diagram

```plantuml
@startuml CollaborationDiagram
title CMCS Process View - Collaboration Diagram

object "Operator" as Op
object "VCI_Gateway" as VCI
object "Master_Node" as Master
object "CMIB_Slave" as CMIB
object "Database" as DB
object "Alert_Service" as Alert

Op -- VCI : 1. Submit Config
VCI -- Master : 2. Route Command
Master -- CMIB : 3. Apply Config
Master -- DB : 4. Log Transaction
CMIB -- Master : 5. Ack Status
Master -- Alert : 6. Notify (if error)

note "Scenario 1: Config Update\n(Sequential Flow)" as N1
N1 .. Op

note "Scenario 2: Recovery\n(Internal Flow)" as N2
N2 .. CMIB

@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram

```plantuml
@startuml PackageDiagram
title CMCS Development View - Package Diagram

package "UI_Layer" {
  [Web GUI]
  [CLI Tools]
}

package "API_Layer" {
  [VCI Gateway]
  [Auth Service]
}

package "Control_Layer" {
  [Master Controller]
  [Health Monitor]
  [Replication Mgr]
}

package "Hardware_Abstraction" {
  [CMIB Firmware]
  [Power Control Driver]
}

package "Data_Layer" {
  [Config DB]
  [Audit Log]
  [Spool Queue]
}

UI_Layer --> API_Layer : HTTPS
API_Layer --> Control_Layer : Internal RPC
Control_Layer --> Hardware_Abstraction : Ethernet/PCI
Control_Layer --> Data_Layer : SQL/Queue

note "Security Boundary" as NB
NB .. API_Layer

note "Real-time Boundary" as RB
RB .. Hardware_Abstraction

@enduml
```

9. Component — Development View: Component Diagram

```plantuml
@startuml ComponentDiagram
title CMCS Development View - Component Diagram

component "VCI Service" as VCI {
  port "REST_API" as P1
  port "Auth" as P2
}

component "Control Service" as Control {
  port "Command Bus" as P3
  port "State DB" as P4
}

component "Monitor Service" as Monitor {
  port "Heartbeat" as P5
  port "Alerts" as P6
}

component "CMIB Agent" as Agent {
  port "Hardware Bus" as P7
}

VCI P1 --> Control P3 : Commands
Control P4 ..> "ConfigDB" : Persists
Monitor P5 ..> Agent P7 : Polls
Monitor P6 --> "AlertManager" : Pushes

note "High Availability\n(Active-Passive)" as HA
HA .. Control

note "Deterministic\n(Real-time)" as RT
RT .. Agent

@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram

```plantuml
@startuml DeploymentDiagram
title CMCS Physical View - Deployment Diagram

node "Operator Workstation" {
  component "Web Browser"
  component "SSH Client"
}

node "Primary Master Node" as Master1 {
  component "Master Control App"
  component "VCI Gateway"
  component "Monitor Agent"
}

node "Secondary Master Node" as Master2 {
  component "Master Control App (Standby)"
  component "VCI Gateway (Standby)"
}

node "Correlator Rack" {
  node "CMIB Slot 1" {
    component "CMIB Firmware"
  }
  node "CMIB Slot 2" {
    component "CMIB Firmware"
  }
  component "Power Control Unit"
}

node "Network Infrastructure" {
  component "Control Switch"
  component "Ops Switch"
}

Master1 -- Master2 : Heartbeat Link
Master1 -- "Control Switch" : 100Mbit Ethernet
"Control Switch" -- "CMIB Slot 1" : Control Net
"Control Switch" -- "CMIB Slot 2" : Control Net
"Operator Workstation" -- "Ops Switch" : Secure Link
"Ops Switch" -- Master1 : Management Net

note "Redundant Power\n(ASR-009)" as NP
NP .. "Power Control Unit"

@enduml
```

11. Container — Physical View: Container Diagram

```plantuml
@startuml ContainerDiagram
title CMCS Physical View - Container Diagram

rectangle "External Systems" {
  container "VLA Expansion M&C" as VLA
  container "Operator Browser" as Browser
}

rectangle "Correlator M&C System Boundary" {
  container "VCI Web App" as WebApp
  container "Control API" as API
  container "State Database" as DB
  container "Message Queue" as Queue
  container "CMIB Controller" as Controller
}

Browser --> WebApp : HTTPS
WebApp --> API : JSON/REST
API --> DB : SQL
API --> Queue : Publish Config
Controller --> Queue : Subscribe Config
Controller --> "CMIB Hardware" : TCP/IP
VLA --> API : External Config

note "Spooling for\nOffline Operation\n(ASR-007)" as N1
N1 .. Queue

note "99.99% Availability\n(NFR-016)" as N2
N2 .. DB

@enduml
```