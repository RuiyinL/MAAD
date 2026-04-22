## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SunSearchControl
left to right direction
skinparam packageStyle rectangle

actor GroundOperator as GroundOperator
actor DataManagementComputer as DataManagementComputer
actor Gyroscope as Gyroscope
actor SunSensorPrimary as SunSensorPrimary
actor SunSensorBackup as SunSensorBackup
actor ThrusterCluster as ThrusterCluster
actor ControlComputerTimer as ControlComputerTimer

rectangle "Sun Search Control System (SSCS)" as SSCS {
  usecase "InitializeSystem" as UC_Init
  usecase "ReceiveCommand" as UC_RxCmd
  usecase "VerifyCommandFrame" as UC_VerCmd
  usecase "SetOperatingMode" as UC_SetMode

  usecase "AcquireGyroData" as UC_Gyro
  usecase "AcquireSunSensorData" as UC_Sun
  usecase "AcquireThrusterStatus" as UC_ThrStat

  usecase "EstimateAttitude" as UC_Att
  usecase "ManageModeSwitching" as UC_ModeMgr
  usecase "ExecuteControlMode" as UC_ModeExec

  usecase "OutputThrusterSwitchData" as UC_ThrOut
  usecase "TransmitTelemetry" as UC_Tlm

  usecase "ManageFaults" as UC_Faults
  usecase "SwitchSunSensor" as UC_SwitchSS
}

' Actors -> use cases
ControlComputerTimer --> UC_Init
ControlComputerTimer --> UC_RxCmd
ControlComputerTimer --> UC_Gyro
ControlComputerTimer --> UC_Sun
ControlComputerTimer --> UC_ThrStat
ControlComputerTimer --> UC_Att
ControlComputerTimer --> UC_ModeMgr
ControlComputerTimer --> UC_ModeExec
ControlComputerTimer --> UC_ThrOut
ControlComputerTimer --> UC_Tlm
ControlComputerTimer --> UC_Faults

GroundOperator --> DataManagementComputer
DataManagementComputer --> UC_RxCmd
DataManagementComputer --> UC_Tlm

Gyroscope --> UC_Gyro
SunSensorPrimary --> UC_Sun
SunSensorBackup --> UC_Sun
ThrusterCluster --> UC_ThrStat
ThrusterCluster --> UC_ThrOut

' Includes / extends
UC_RxCmd .> UC_VerCmd : <<include>>
UC_RxCmd .> UC_SetMode : <<include>>

UC_Att .> UC_Gyro : <<include>>
UC_Att .> UC_Sun : <<include>>

UC_ModeMgr .> UC_Att : <<include>>
UC_ModeExec .> UC_ModeMgr : <<include>>

UC_Faults .> UC_ThrStat : <<include>>
UC_Faults .> UC_Gyro : <<include>>
UC_SwitchSS .> UC_Sun : <<include>>
UC_Faults .> UC_SwitchSS : <<extend>>

UC_ThrOut .> UC_ModeExec : <<include>>
UC_Tlm .> UC_Att : <<include>>
UC_Tlm .> UC_ModeMgr : <<include>>

note right of SSCS
assumption: DataManagementComputer (on-board) is the interface to GroundOperator,
bridging command RX and telemetry TX; SSCS receives commands from DMC via UART @0x88DA and
sends telemetry via UART @0x88DB.
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_SunSearchControl
skinparam classAttributeIconSize 0

class CyclicExecutive <<control>> {
  -tickCount5 : uint8
  -superframeStartMs : uint16
  +onTimerTick32ms() : void
  +runSlot(slotId:uint8) : void
  +detectOverrun() : void
}

class ScheduleMonitor <<service>> {
  -isrOverrunCount : uint16
  -cycleMissCount : uint16
  -lastIsrDurationMs : uint16
  +beginIsr() : void
  +endIsr() : void
  +markCycleComplete() : void
}

class HardwareIO <<boundary>> {
  +uartRx(port:uint16, maxLen:uint8) : byte[]
  +uartTx(port:uint16, data:byte[]) : void
  +adcRead(channel:uint8) : uint16
  +writeReg(addr:uint16, value:uint8) : void
  +delayMs(ms:uint16) : void
}

class CommandFrame <<immutable>> {
  +length : uint8
  +header : uint16
  +payload : byte[]
  +checksum : uint16
  +isValid(spec:FrameSpec) : bool
}

class TelemetryPacket <<immutable>> {
  +modeWord : uint16
  +attitude : int16[3]
  +angularRate : int16[3]
  +faultFlags : uint16
  +scheduleStatus : uint16
  +encode(spec:FrameSpec) : byte[]
}

class FrameSpec <<value>> {
  +minLen : uint8
  +header : uint16
  +checksumType : uint8
  +verify(bytes:byte[]) : bool
}

class ModeRegister <<persisted>> {
  +modeWord : uint16
  +modeDurationTicks : uint16
  +targetAngleU12 : uint16
  +targetRate : int16[3]
  +sunSensorSel : uint8
  +reset() : void
  +updateTargets(rate:int16[3], angleU12:uint16) : void
}

class SensorSnapshot <<value>> {
  +gyroPulseCount : uint32
  +gyroValid : bool
  +sunPowerOn : bool
  +sunVisible : bool
  +sunSign : bool
  +sunAngleU12 : uint16
  +thrusterPowerOn : bool
}

class GyroDriver <<driver>> {
  -portAddr : uint16 = 0x881A
  -fetchCmd : uint16 = 0xEB91
  -homeCmd : uint16 = 0xEB92
  -spec : FrameSpec
  +init() : void
  +fetch() : void
  +readAndValidate() : SensorSnapshot
}

class SunSensorDriver <<driver>> {
  -angleAdFormat : uint8
  +readAdAngleU12() : uint16
  +readLatchSignals() : void
  +switchPulse190ms() : void
}

class ThrusterDriver <<driver>> {
  +readPowerStatus() : bool
  +outputSwitchDataAt128ms(cmd:ThrusterCommand) : void
  +disableThrusters() : void
}

class AttitudeEstimator <<service>> {
  +estimate(snapshot:SensorSnapshot) : AttitudeState
}

class AttitudeState <<value>> {
  +eulerDegX10 : int16[3]
  +omegaMdps : int16[3]
}

class ModeManager <<service>> {
  +evaluate(state:AttitudeState, reg:ModeRegister, sunVisible:bool) : void
  +logTransition(from:uint16, to:uint16, cause:uint8) : void
}

class ControlLaw <<service>> {
  +computeTargets(reg:ModeRegister, state:AttitudeState) : ThrusterCommand
}

class ThrusterCommand <<value>> {
  +switchBits12 : uint16
  +sequenceId : uint8
}

class FaultManager <<service>> {
  -gyroErrCount : uint8
  -gyroRecoveryState : uint8
  -thrusterRapidFireCount : uint8
  +checkGyroComms(gyroValid:bool) : void
  +checkThrusterFiring(intervalMs:uint16) : void
  +requestSunSensorSwitch() : bool
}

class TelemetryService <<service>> {
  -portAddr : uint16 = 0x88DB
  -spec : FrameSpec
  +build(state:AttitudeState, reg:ModeRegister, faults:uint16, sched:uint16) : TelemetryPacket
  +transmit(pkt:TelemetryPacket) : void
}

class CommandService <<service>> {
  -portAddr : uint16 = 0x88DA
  -spec : FrameSpec
  -lastAcceptedTick : uint16
  +receive() : CommandFrame
  +verify(cmd:CommandFrame) : bool
  +apply(cmd:CommandFrame, reg:ModeRegister) : void
  +enforceRateLimit(nowTick:uint16) : bool
}

CyclicExecutive "1" *-- "1" ScheduleMonitor
CyclicExecutive "1" *-- "1" CommandService
CyclicExecutive "1" *-- "1" GyroDriver
CyclicExecutive "1" *-- "1" SunSensorDriver
CyclicExecutive "1" *-- "1" ThrusterDriver
CyclicExecutive "1" *-- "1" AttitudeEstimator
CyclicExecutive "1" *-- "1" ModeManager
CyclicExecutive "1" *-- "1" ControlLaw
CyclicExecutive "1" *-- "1" FaultManager
CyclicExecutive "1" *-- "1" TelemetryService
CyclicExecutive "1" *-- "1" ModeRegister

GyroDriver ..> HardwareIO : uses
SunSensorDriver ..> HardwareIO : uses
ThrusterDriver ..> HardwareIO : uses
CommandService ..> HardwareIO : uses
TelemetryService ..> HardwareIO : uses

CommandService ..> FrameSpec
TelemetryService ..> FrameSpec
CommandFrame ..> FrameSpec
TelemetryPacket ..> FrameSpec

AttitudeEstimator ..> SensorSnapshot
AttitudeEstimator ..> AttitudeState

ModeManager ..> ModeRegister
ModeManager ..> AttitudeState

ControlLaw ..> ModeRegister
ControlLaw ..> AttitudeState
ControlLaw ..> ThrusterCommand

FaultManager ..> ModeRegister
FaultManager ..> GyroDriver
FaultManager ..> ThrusterDriver
FaultManager ..> SunSensorDriver

note right of CyclicExecutive
ASR-001/NFR-004: 32ms tick, 160ms superframe (5 ticks),
reserved output slot at t=128ms (tick 4).
end note

note right of HardwareIO
ASR-003/NFR-011: UART ports fixed:
0x88DA cmd RX, 0x88DB telemetry TX, 0x881A gyro only.
NFR-006: inter-byte gap < 5us for certain TX.
end note

note right of GyroDriver
NFR-008: fetch-to-read delay > 5ms (instrumented).
end note

note right of SunSensorDriver
NFR-009: switch pulse 190ms ±1ms via control register enable.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SunSearchControl
skinparam objectAttributeIconSize 0

object exec1 as "exec1 : CyclicExecutive [ControlCycle]"
object reg1 as "reg1 : ModeRegister [ModeState]" {
  modeWord = 0x0001
  modeDurationTicks = 37
  targetAngleU12 = 0x7A0
  targetRate = "{0,0,0}"
  sunSensorSel = 0
}
object snap1 as "snap1 : SensorSnapshot [AcquireSensors]" {
  gyroPulseCount = 1280345
  gyroValid = true
  sunPowerOn = true
  sunVisible = false
  sunSign = false
  sunAngleU12 = 0x3F2
  thrusterPowerOn = true
}
object att1 as "att1 : AttitudeState [EstimateAttitude]" {
  eulerDegX10 = "{-12, 35, 4}"
  omegaMdps = "{120, -80, 25}"
}
object cmd1 as "cmd1 : CommandFrame [ReceiveCommand]" {
  length = 12
  header = 0x55AA
  checksum = 0x1F2C
}
object thrCmd1 as "thrCmd1 : ThrusterCommand [OutputThrusters]" {
  switchBits12 = 0x05A3
  sequenceId = 4
}
object tlm1 as "tlm1 : TelemetryPacket [TransmitTelemetry]" {
  modeWord = 0x0001
  faultFlags = 0x0000
  scheduleStatus = 0x0000
}

exec1 -- reg1
exec1 -- snap1
snap1 -- att1
cmd1 -- reg1
att1 -- thrCmd1
reg1 -- thrCmd1
att1 -- tlm1
reg1 -- tlm1

note right of cmd1
assumption: command frame spec uses header 0x55AA and a 16-bit checksum placeholder
until Table 3.2-1 is provided.
end note
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_ModeRegisterLifecycle
hide empty description

state "ModeManager FSM" as MM {
  [*] --> RDSM : InitializeSystem / reg.reset()\nset modeWord=RDSM

  RDSM : Rate Damping
  PASM : Pitch Search (Y-axis)
  RASM : Roll Search (X-axis)
  CSM  : Sun Cruise

  RDSM --> PASM : RateDamped [omega<thr] / setTargetRate(pitchRate)
  PASM --> CSM  : SunDetected [sunVisible] / setTargetRate(0)
  PASM --> RASM : SearchTimeout [!sunVisible] / setTargetRate(rollRate)
  RASM --> CSM  : SunDetected [sunVisible] / setTargetRate(0)
  RASM --> RDSM : SearchFailedTwice / setTargetRate(0)\nincSearchFail()

  CSM --> RDSM : SunLost / setTargetRate(0)

  state "Backup Sensor Handling" as BSH {
    [*] --> PrimaryActive
    PrimaryActive --> PulseSwitch : NeedSwitch / switchPulse190ms()
    PulseSwitch --> BackupActive : PulseComplete / reg.sunSensorSel=1
    BackupActive --> [*]
  }

  RDSM --> BSH : SearchFailedTwice [sunSensorSel==0] / requestSwitch
  BSH --> RDSM : SwitchDone / resetSearchCounters
}

note right of MM
ASR-004: four explicit modes, evaluated every 160ms.
FR-016/FR-020/NFR-009: after two pitch+roll failures, switch to backup sensor with 190ms±1ms pulse, then re-enter RDSM.
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_160msControlCycle
start
:ISR tick 32ms;
:ScheduleMonitor.beginIsr();

if (tick == 0?) then (yes)
  :CommandService.receive() [UART 0x88DA];
  :VerifyCommandFrame [SpecCheck];
  if (RateLimit ok?) then (yes)
    :SetOperatingMode;
  else (no)
    :LogCmdReject;
  endif
  :GyroDriver.fetch() [UART 0x881A];
  note right
  NFR-008: enforce fetch->read delay > 5ms
  end note
endif

if (tick == 1?) then (yes)
  :delayMs(>5ms);
  :GyroDriver.readAndValidate();
endif

if (tick == 2?) then (yes)
  :SunSensorDriver.readLatchSignals();
  :SunSensorDriver.readAdAngleU12() [12-bit];
  :ThrusterDriver.readPowerStatus();
endif

if (tick == 3?) then (yes)
  :AttitudeEstimator.estimate();
  :FaultManager.checkGyroComms();
  :FaultManager.checkThrusterFiring();
  :ModeManager.evaluate();
endif

if (tick == 4?) then (yes)
  :ControlLaw.computeTargets();
  :OutputThrusterSwitchData @128ms;
  :TelemetryService.build();
  :TelemetryService.transmit() [UART 0x88DB];
endif

:ScheduleMonitor.endIsr();
if (Overrun?) then (yes)
  :LogScheduleOverrun;
endif
stop

note bottom
ASR-001/NFR-004/NFR-010: 5 ticks per 160ms superframe, reserved thruster output at t=128ms (tick 4).
NFR-006: telemetry TX inter-byte gap <5us (driver-level).
end note
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_S1_CommandToModeUpdate
hide footbox
actor DataManagementComputer as DataManagementComputer
participant CyclicExecutive as CyclicExecutive
participant CommandService as CommandService
participant HardwareIO as HardwareIO
participant ModeRegister as ModeRegister
participant ModeManager as ModeManager

== 160ms cycle: command handling ==
DataManagementComputer -> HardwareIO : uartWrite(0x88DA, cmdBytes)
CyclicExecutive -> CommandService : receiveCommand
CommandService -> HardwareIO : uartRx(0x88DA)
HardwareIO --> CommandService : cmdBytes
CommandService -> CommandService : verifyCommandFrame
CommandService -> CommandService : enforceRateLimit

alt valid & within rate
  CommandService -> ModeRegister : apply(cmd)\nset modeWord
  CommandService -> ModeManager : logTransition(from,to,cause=GROUND_CMD)
else invalid or rate-limited
  CommandService -> ModeManager : logTransition(from,to,cause=CMD_REJECT)
end

note right of CommandService
FR-003/NFR-007: accept <= 1 command per 160ms.
FR-004: verify length/header/checksum (spec pending).
end note
@enduml
```

```plantuml
@startuml Sequence_S2_SunAcquisitionAndActuation
hide footbox
participant CyclicExecutive as CyclicExecutive
participant ScheduleMonitor as ScheduleMonitor
participant GyroDriver as GyroDriver
participant SunSensorDriver as SunSensorDriver
participant ThrusterDriver as ThrusterDriver
participant AttitudeEstimator as AttitudeEstimator
participant ModeManager as ModeManager
participant ControlLaw as ControlLaw
participant TelemetryService as TelemetryService
participant HardwareIO as HardwareIO
participant ModeRegister as ModeRegister

== tick 0 ==
CyclicExecutive -> ScheduleMonitor : beginIsr
CyclicExecutive -> GyroDriver : fetch
GyroDriver -> HardwareIO : uartTx(0x881A, 0xEB91)

== tick 1 ==
CyclicExecutive -> HardwareIO : delayMs(>5ms)
CyclicExecutive -> GyroDriver : readAndValidate
GyroDriver -> HardwareIO : uartRx(0x881A)
HardwareIO --> GyroDriver : gyroBytes
GyroDriver --> CyclicExecutive : snapshot(gyroValid, pulseCount)

== tick 2 ==
CyclicExecutive -> SunSensorDriver : readLatchSignals
SunSensorDriver -> HardwareIO : adcRead(chSunAngle)
HardwareIO --> SunSensorDriver : angleU12
SunSensorDriver --> CyclicExecutive : sunVisible/sign/angleU12
CyclicExecutive -> ThrusterDriver : readPowerStatus
ThrusterDriver -> HardwareIO : adcRead(chThrPwr)
HardwareIO --> ThrusterDriver : thrPwrU12

== tick 3 ==
CyclicExecutive -> AttitudeEstimator : estimate(snapshot)
AttitudeEstimator --> CyclicExecutive : attitudeState
CyclicExecutive -> ModeManager : evaluate(attitudeState, reg, sunVisible)

== tick 4 (t=128ms slot) ==
CyclicExecutive -> ControlLaw : computeTargets(reg, attitudeState)
ControlLaw --> CyclicExecutive : thrusterCommand
CyclicExecutive -> ThrusterDriver : outputSwitchDataAt128ms(thrusterCommand)
ThrusterDriver -> HardwareIO : writeReg(thrusterSwitchReg, dataSeq)
CyclicExecutive -> TelemetryService : build(...)
TelemetryService -> HardwareIO : uartTx(0x88DB, tlmBytes)

CyclicExecutive -> ScheduleMonitor : endIsr

note right of CyclicExecutive
ASR-001/NFR-010: thruster output aligned to 128ms within 160ms superframe.
NFR-008: gyro fetch->read delay >5ms.
NFR-006: telemetry UART TX inter-byte gap <5us (implemented in UART driver).
end note
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_S1_CommandToModeUpdate
skinparam linetype ortho

actor DataManagementComputer as DataManagementComputer
rectangle CyclicExecutive as CyclicExecutive
rectangle CommandService as CommandService
rectangle HardwareIO as HardwareIO
rectangle ModeRegister as ModeRegister
rectangle ModeManager as ModeManager

DataManagementComputer -- HardwareIO
CyclicExecutive -- CommandService
CommandService -- HardwareIO
CommandService -- ModeRegister
CommandService -- ModeManager

note bottom
Scenario S1 (FR-002/FR-003/FR-004/NFR-007): Receive+verify ground command and set mode word (rate-limited).
end note

DataManagementComputer -> HardwareIO : 1 uartWrite(0x88DA, cmdBytes)
CyclicExecutive -> CommandService : 2 receiveCommand
CommandService -> HardwareIO : 3 uartRx(0x88DA)
CommandService -> CommandService : 4 verifyFrame
CommandService -> CommandService : 5 enforceRateLimit
CommandService -> ModeRegister : 6 apply(cmd)
CommandService -> ModeManager : 7 logTransition
@enduml
```

```plantuml
@startuml Collaboration_S2_SunAcquisitionAndActuation
skinparam linetype ortho

rectangle CyclicExecutive as CyclicExecutive
rectangle ScheduleMonitor as ScheduleMonitor
rectangle GyroDriver as GyroDriver
rectangle SunSensorDriver as SunSensorDriver
rectangle ThrusterDriver as ThrusterDriver
rectangle AttitudeEstimator as AttitudeEstimator
rectangle ModeManager as ModeManager
rectangle ControlLaw as ControlLaw
rectangle TelemetryService as TelemetryService
rectangle HardwareIO as HardwareIO
rectangle ModeRegister as ModeRegister

CyclicExecutive -- ScheduleMonitor
CyclicExecutive -- GyroDriver
CyclicExecutive -- SunSensorDriver
CyclicExecutive -- ThrusterDriver
CyclicExecutive -- AttitudeEstimator
CyclicExecutive -- ModeManager
CyclicExecutive -- ControlLaw
CyclicExecutive -- TelemetryService
GyroDriver -- HardwareIO
SunSensorDriver -- HardwareIO
ThrusterDriver -- HardwareIO
TelemetryService -- HardwareIO
ModeManager -- ModeRegister
ControlLaw -- ModeRegister

note bottom
Scenario S2 (FR-001/FR-007/FR-008/FR-010/FR-011/FR-022/FR-023, ASR-001/ASR-003):
Acquire sensors -> estimate attitude -> manage modes -> output thrusters at 128ms -> send telemetry.
end note

CyclicExecutive -> ScheduleMonitor : 1 beginIsr
CyclicExecutive -> GyroDriver : 2 fetch
GyroDriver -> HardwareIO : 3 uartTx(0x881A, 0xEB91)
CyclicExecutive -> HardwareIO : 4 delayMs(>5ms)
CyclicExecutive -> GyroDriver : 5 readAndValidate
GyroDriver -> HardwareIO : 6 uartRx(0x881A)
CyclicExecutive -> SunSensorDriver : 7 readAdAngleU12
SunSensorDriver -> HardwareIO : 8 adcRead(chSunAngle)
CyclicExecutive -> AttitudeEstimator : 9 estimate
CyclicExecutive -> ModeManager : 10 evaluate
CyclicExecutive -> ControlLaw : 11 computeTargets
CyclicExecutive -> ThrusterDriver : 12 outputAt128ms
CyclicExecutive -> TelemetryService : 13 transmitTelemetry
TelemetryService -> HardwareIO : 14 uartTx(0x88DB, tlmBytes)
CyclicExecutive -> ScheduleMonitor : 15 endIsr
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SunSearchControl
skinparam packageStyle rectangle

package "app" as pkg_app {
  class CyclicExecutive
}

package "domain" as pkg_domain {
  class ModeRegister
  class SensorSnapshot
  class AttitudeState
  class ThrusterCommand
}

package "services" as pkg_services {
  class CommandService
  class AttitudeEstimator
  class ModeManager
  class ControlLaw
  class FaultManager
  class TelemetryService
  class ScheduleMonitor
}

package "drivers" as pkg_drivers {
  class HardwareIO
  class GyroDriver
  class SunSensorDriver
  class ThrusterDriver
}

package "contracts" as pkg_contracts {
  class FrameSpec
  class CommandFrame
  class TelemetryPacket
}

pkg_app ..> pkg_services : orchestrates
pkg_services ..> pkg_domain : uses
pkg_services ..> pkg_drivers : uses
pkg_services ..> pkg_contracts : uses
pkg_drivers ..> pkg_contracts : validates frames
pkg_contracts ..> pkg_domain : maps fields

note right of pkg_app
ASR-001: time-triggered cyclic executive (single 32ms ISR).
end note

note right of pkg_drivers
ASR-003/NFR-011: fixed UART addresses and ADC formats.
NFR-006: inter-byte TX gap constraint.
end note

note right of pkg_domain
ASR-004: mode register holds modeWord, duration, targets.
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SunSearchControl
skinparam componentStyle rectangle

component "SSCS Firmware" as FW <<device>> {
  component "CyclicExecutive" as CExec
  component "CommandService" as CmdSvc
  component "SensorAcquisition" as SensAcq
  component "AttitudeEstimator" as AttEst
  component "ModeManager" as ModeMgr
  component "FaultManager" as FaultMgr
  component "ControlLaw" as CtrlLaw
  component "ThrusterOutput" as ThrOut
  component "TelemetryService" as TlmSvc
  component "ScheduleMonitor" as SchedMon
  component "ModeRegister" as ModeReg
}

component "HardwareIO HAL" as HAL <<HAL>>
component "GyroDriver" as GyroDrv <<driver>>
component "SunSensorDriver" as SunDrv <<driver>>
component "ThrusterDriver" as ThrDrv <<driver>>

interface "IUart" as IUart
interface "IAdc" as IAdc
interface "IReg" as IReg

HAL - IUart
HAL - IAdc
HAL - IReg

GyroDrv ..> IUart : requires\n(0x881A)
SunDrv ..> IAdc : requires\n(12-bit offset)
SunDrv ..> IReg : requires\n(switch pulse)
ThrDrv ..> IAdc : requires\n(power status)
ThrDrv ..> IReg : requires\n(thruster bits)

SensAcq ..> GyroDrv : uses
SensAcq ..> SunDrv : uses
SensAcq ..> ThrDrv : uses

CmdSvc ..> HAL : uses IUart\n(0x88DA)
TlmSvc ..> HAL : uses IUart\n(0x88DB)

CExec ..> CmdSvc
CExec ..> SensAcq
CExec ..> AttEst
CExec ..> ModeMgr
CExec ..> FaultMgr
CExec ..> CtrlLaw
CExec ..> ThrOut
CExec ..> TlmSvc
CExec ..> SchedMon

ModeMgr ..> ModeReg
CtrlLaw ..> ModeReg
FaultMgr ..> ModeReg
ThrOut ..> ThrDrv
ThrOut ..> ModeReg
TlmSvc ..> ModeReg

note right of FW
ASR-002: 80C32E constraints => static allocation, compact components compiled into single firmware image.
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SunSearchControl
skinparam linetype ortho
skinparam nodesep 35

node "ControlComputer\n80C32E @11.0592MHz\nPROM32KB SRAM8KB" as MCU <<device>> {
  artifact "SSCS Firmware" as FW
}

node "DataManagementComputer (DMC)" as DMC <<device>> {
  artifact "Cmd/Tlm Bridge" as Bridge
}

node "Gyroscope Unit" as GYRO <<device>>
node "Sun Sensor Primary" as SSP <<device>>
node "Sun Sensor Backup" as SSB <<device>>
node "Thruster Cluster (12x 10N)" as THR <<device>>

MCU -- DMC : UART 0x88DA (Cmd RX)\nUART 0x88DB (Tlm TX)
MCU -- GYRO : UART 0x881A (Gyro)\n(fetch/read timing)
MCU -- SSP : ADC + Latch + EnableReg
MCU -- SSB : ADC + Latch + EnableReg
MCU -- THR : ADC (power)\nSwitchReg (output@128ms)

note right of MCU
NFR-004/ASR-001: 32ms single ISR, 160ms cycle.
NFR-006: inter-byte gap <5us for telemetry/selected TX.
end note

note bottom of GYRO
NFR-008: fetch->read delay >5ms; validate len/header/checksum.
end note

note bottom of MCU
assumption: sun sensor switch enable register is memory-mapped; exact address TBD in HW map.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SunSearchControl
skinparam rectangleStyle rounded
left to right direction

rectangle "ControlComputer MCU\n<<device>>" as MCU {
  rectangle "SSCS Firmware\n[CyclicExecutive]\n[ModeControl][FaultFSM]\n[Drivers+HAL]" as SSCS
}

rectangle "DataManagementComputer\n<<external system>>" as DMC {
  rectangle "Cmd/Tlm Handler\n[GroundBridge]" as DMCBridge
}

rectangle "Gyroscope\n<<external device>>\n[UART 0x881A]" as Gyro
rectangle "Sun Sensor Primary\n<<external device>>\n[ADC+Latch]" as SSP
rectangle "Sun Sensor Backup\n<<external device>>\n[ADC+Latch]" as SSB
rectangle "Thruster Cluster\n<<external device>>\n[Switch outputs]" as Thrusters
rectangle "Ground Operator\n<<actor>>" as GroundOperator

GroundOperator --> DMCBridge : Operate/Configure
DMCBridge --> SSCS : UART Cmd RX\n0x88DA [<=1/160ms]
SSCS --> DMCBridge : UART Telemetry TX\n0x88DB [<5us gap]
SSCS --> Gyro : UART fetch/read\n0x881A [>5ms delay]
SSCS --> SSP : Sample sun angle/status\n(160ms)
SSCS --> SSB : Sample sun angle/status\n(160ms)
SSCS --> Thrusters : Output switch data\n@128ms slot

note right of SSCS
ASR-001: time-triggered cyclic executive (5 ticks).
ASR-004: mode-based control (RDSM/PASM/RASM/CSM) with ModeRegister.
ASR-005: deterministic fault FSMs (gyro comms, thruster overfire).
ASR-006: 190ms±1ms sun-sensor switch pulse.
end note
@enduml
```