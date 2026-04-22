## ScenarioView
1. UseCase — Scenario View: Use Case Diagram
```plantuml
@startuml UseCase_SunSearchControl
left to right direction
skinparam packageStyle rectangle

actor GroundOperator as GroundOperator
actor "Gyroscope" as Gyroscope
actor "Sun Sensor (Primary)" as SunSensorPrimary
actor "Sun Sensor (Backup)" as SunSensorBackup
actor "Thruster Assembly" as ThrusterAssembly
actor "Telemetry Monitor" as TelemetryMonitor

rectangle "Sun Search Control System (SSCS)" as SSCS {
  usecase "InitializeSystem" as UC_Init
  usecase "ReceiveCommand" as UC_RxCmd
  usecase "VerifyCommand" as UC_VerCmd
  usecase "SetOperatingMode" as UC_SetMode

  usecase "AcquireSensors" as UC_AcqSensors
  usecase "AcquireGyroData" as UC_AcqGyro
  usecase "ValidateGyroFrame" as UC_ValGyro
  usecase "AcquireSunSensorData" as UC_AcqSun
  usecase "AcquireThrusterStatus" as UC_AcqThrStat

  usecase "DetermineAttitude" as UC_Att
  usecase "ManageModeSwitching" as UC_ModeMgr
  usecase "OutputThrusterCommands" as UC_ThrOut
  usecase "TransmitTelemetry" as UC_Tlm

  usecase "HandleGyroCommFault" as UC_GyroFault
  usecase "DetectFrequentJetting" as UC_JetFault
  usecase "SwitchSunSensor" as UC_SunSwitch
}

GroundOperator --> UC_RxCmd
UC_RxCmd ..> UC_VerCmd : <<include>>
UC_RxCmd ..> UC_SetMode : <<include>>

GroundOperator --> UC_Init

Gyroscope --> UC_AcqGyro
UC_AcqGyro ..> UC_ValGyro : <<include>>

SunSensorPrimary --> UC_AcqSun
SunSensorBackup --> UC_AcqSun

ThrusterAssembly --> UC_AcqThrStat
ThrusterAssembly <-- UC_ThrOut

TelemetryMonitor <-- UC_Tlm

UC_AcqSensors ..> UC_AcqGyro : <<include>>
UC_AcqSensors ..> UC_AcqSun : <<include>>
UC_AcqSensors ..> UC_AcqThrStat : <<include>>

UC_Att ..> UC_AcqSensors : <<include>>
UC_ModeMgr ..> UC_Att : <<include>>
UC_ThrOut ..> UC_ModeMgr : <<include>>
UC_Tlm ..> UC_ModeMgr : <<include>>

UC_GyroFault ..> UC_ValGyro : <<extend>>
UC_JetFault ..> UC_AcqThrStat : <<extend>>
UC_SunSwitch ..> UC_ModeMgr : <<extend>>

note right of SSCS
assumption: "Telemetry Monitor" represents the ground display/monitoring endpoint
connected to the telemetry serial port (FR-022).
end note
@enduml
```

## LogicView
2. Class — Logic View: Class Diagram
```plantuml
@startuml Class_SunSearchControl
skinparam classAttributeIconSize 0

class ControlCycleScheduler <<control>> {
  -cycleId : uint32
  -tick32ms : uint8
  +onTimerTick32ms() : void
  +runCycle160ms() : void
  +measureCycleDurationMs() : uint16
}

class ModeRegister <<persisted>> {
  +modeWord : uint8
  +modeDurationTicks : uint16
  +targetAngleDeg : int16
  +targetRateDps : int16
  +pasmAttempts : uint8
  +rasmAttempts : uint8
  +activeSunSensor : uint8
  +resetAttemptsOnSunDetect() : void
}

class CommandFrame <<immutable>> {
  +header : uint8
  +len : uint8
  +data : uint8[*]
  +checksum : uint8
}

class CommandProcessor <<control>> {
  +receiveCommand() : CommandFrame
  +verifyCommand(cmd:CommandFrame) : bool
  +setOperatingMode(cmd:CommandFrame, modeReg:ModeRegister) : void
}

class SerialPortDriver <<boundary>> {
  +baseAddr : uint16
  +sendBytes(buf:uint8[*]) : void
  +readBytes(maxLen:uint8) : uint8[*]
  +measureInterByteUs() : uint16
}

class AdcDriver <<boundary>> {
  +readChannel(ch:uint8) : uint16
}

class GyroDriver <<boundary>> {
  +fetchCmd : uint16 = 0xEB91
  +powerOnCmd : uint16 = 0xEB92
  +sendFetch() : void
  +readFrame() : uint8[*]
  +powerOn() : void
  +powerOff() : void
  +control() : void
}

class SunSensorDriver <<boundary>> {
  +readPowerStatus() : bool
  +readSunVisible() : bool
  +readAngleCode12bit() : uint16
  +switchToBackupPulse() : void
}

class ThrusterIoDriver <<boundary>> {
  +readPowerStatus() : bool
  +outputSwitchData12(thrCmd:ThrusterCommand) : void
  +shutdownThruster() : void
}

class SensorFrameValidator <<service>> {
  +verifyLength(frame:uint8[*]) : bool
  +verifyHeader(frame:uint8[*]) : bool
  +verifyChecksum(frame:uint8[*]) : bool
}

class AttitudeEstimate {
  +rollDeg : int16
  +pitchDeg : int16
  +yawDeg : int16
  +wxDps : int16
  +wyDps : int16
  +wzDps : int16
  +sunVisible : bool
}

class AttitudeEstimator <<service>> {
  +determineAttitude(gyroFrame:uint8[*], sunAngleCode:uint16, sunVisible:bool) : AttitudeEstimate
}

class ModeManager <<service>> {
  +manage(modeReg:ModeRegister, est:AttitudeEstimate) : void
  +executeRDSM(modeReg:ModeRegister, est:AttitudeEstimate) : void
  +executePASM(modeReg:ModeRegister, est:AttitudeEstimate) : void
  +executeRASM(modeReg:ModeRegister, est:AttitudeEstimate) : void
  +executeCSM(modeReg:ModeRegister, est:AttitudeEstimate) : void
  +detectRepeatedSearchFailure(modeReg:ModeRegister, est:AttitudeEstimate) : bool
}

class ThrusterCommand {
  +switchBits12 : uint16
  +scheduledMs : uint16 = 128
}

class ThrusterController <<service>> {
  +computeThrusterCommand(modeReg:ModeRegister, est:AttitudeEstimate) : ThrusterCommand
  +outputAt128ms(thrCmd:ThrusterCommand) : void
}

class GyroFaultManager <<service>> {
  -consecutiveErrorCycles : uint8
  -waitCycles : uint8
  +onGyroFrameError() : void
  +onGyroFrameOk() : void
  +stepRecovery(gyro:GyroDriver) : void
}

class ThrusterIntervalMonitor <<service>> {
  +updateFireTimestamp(tsMs:uint32) : void
  +detectFrequentJetting() : bool
}

class TelemetryMsg <<immutable>> {
  +mode : uint8
  +angle : int16
  +velocity : int16
}

class TelemetryPacker <<service>> {
  +pack(modeReg:ModeRegister, est:AttitudeEstimate) : TelemetryMsg
  +encode(msg:TelemetryMsg) : uint8[*]
}

class TelemetryTransmitter <<boundary>> {
  +send(msgBytes:uint8[*]) : void
}

ControlCycleScheduler --> CommandProcessor
ControlCycleScheduler --> GyroDriver
ControlCycleScheduler --> SunSensorDriver
ControlCycleScheduler --> ThrusterIoDriver
ControlCycleScheduler --> AttitudeEstimator
ControlCycleScheduler --> ModeManager
ControlCycleScheduler --> ThrusterController
ControlCycleScheduler --> TelemetryPacker
ControlCycleScheduler --> TelemetryTransmitter
ControlCycleScheduler --> GyroFaultManager
ControlCycleScheduler --> ThrusterIntervalMonitor
ControlCycleScheduler --> ModeRegister

CommandProcessor --> SerialPortDriver : uses (0x88DA)
GyroDriver --> SerialPortDriver : uses (0x881A)
TelemetryTransmitter --> SerialPortDriver : uses (0x88DB)
SunSensorDriver --> AdcDriver : uses (angle/power)
ThrusterIoDriver --> AdcDriver : uses (power)

GyroDriver --> SensorFrameValidator
AttitudeEstimator --> SensorFrameValidator

ModeManager --> ModeRegister
ThrusterController --> ThrusterIoDriver
ThrusterController --> ThrusterCommand
TelemetryPacker --> TelemetryMsg

note right of ControlCycleScheduler
ASR-002/NFR-001/NFR-003:
Single 32ms timer ISR drives 160ms (5 ticks) cyclic executive.
Measure ControlCycleDuration = 160±2ms; alert on 3 consecutive violations.
end note

note right of SerialPortDriver
ASR-003/NFR-006:
Inter-byte spacing < 5us for gyro cmds and telemetry.
end note

note right of GyroDriver
FR-006/NFR-007:
Fetch-to-read delay >= 5ms after 0xEB91.
FR-020: power-on cmd 0xEB92 then control cmd <5us interval.
end note

note right of ThrusterController
NFR-004/FR-021:
Output 12 thruster switch lines at t=128ms; complete within 2ms.
end note

note right of SunSensorDriver
NFR-008/FR-017:
Switching instruction 190±1ms with 1ms pulse.
end note
@enduml
```

3. Object — Logic View: Object Diagram
```plantuml
@startuml Object_SunSearchControl
skinparam classAttributeIconSize 0

object scheduler1 as "scheduler1:ControlCycleScheduler [ControlCycle]" {
  cycleId = 1024
  tick32ms = 3
}

object modeReg1 as "modeReg1:ModeRegister [ModeControl]" {
  modeWord = 2
  modeDurationTicks = 15
  targetAngleDeg = 0
  targetRateDps = 5
  pasmAttempts = 1
  rasmAttempts = 0
  activeSunSensor = 0
}

object cmd1 as "cmd1:CommandFrame [ReceiveCommand]" {
  header = 0xA5
  len = 4
  checksum = 0x3C
}

object gyroDrv1 as "gyroDrv1:GyroDriver [AcquireGyroData]" {
  fetchCmd = 0xEB91
  powerOnCmd = 0xEB92
}

object sunDrv1 as "sunDrv1:SunSensorDriver [AcquireSunSensorData]" {
}

object est1 as "est1:AttitudeEstimate [DetermineAttitude]" {
  rollDeg = 12
  pitchDeg = -3
  yawDeg = 5
  wxDps = 2
  wyDps = 5
  wzDps = 1
  sunVisible = false
}

object thrCmd1 as "thrCmd1:ThrusterCommand [OutputThrusterCommands]" {
  switchBits12 = 0x05A
  scheduledMs = 128
}

scheduler1 -- modeReg1
scheduler1 -- cmd1
scheduler1 -- gyroDrv1
scheduler1 -- sunDrv1
scheduler1 -- est1
scheduler1 -- thrCmd1
@enduml
```

4. State — Logic View: State Diagram
```plantuml
@startuml State_ModeRegister
hide empty description
skinparam shadowing false

state "ModeRegister.modeWord" as ModeSM {
  [*] --> RDSM : PowerOnReset / initMode=RDSM\n(FR-004, FR-012)

  RDSM : do/ targetRate=0\naccumulateTime\n(FR-012)
  PASM : do/ rotatePitch\naccumulateTime\n(FR-013)
  RASM : do/ rotateRoll\naccumulateTime\n(FR-014)
  CSM  : do/ stabilizeRate=0\naccumulateTime\n(FR-015)

  RDSM --> PASM : RateDamped [sunNotVisible] / setPitchSearch\nincAttempts? (FR-013)
  PASM --> CSM  : SunDetected [SP==visible] / resetAttempts (FR-015)
  PASM --> RASM : PitchSearchFailed / pasmAttempts++ (FR-014, FR-016A)
  RASM --> CSM  : SunDetected [SP==visible] / resetAttempts (FR-015)
  RASM --> PASM : RollSearchFailed / rasmAttempts++ (FR-013, FR-016A)

  state "Backup Sensor Recovery" as Backup {
    [*] --> SwitchSensor : RepeatedFailure / switchOffPrimary+activateBackup (FR-016B)
    SwitchSensor --> AdjustThrusters : afterSwitch / adjustThrusterSettings (FR-016C)
    AdjustThrusters --> RestartRDSM : restart / enterRDSM (FR-016D)
    RestartRDSM --> [*]
  }

  PASM --> Backup : RepeatedFailure [pasmAttempts>=2 && rasmAttempts>=2 && SP==notVisible] (FR-016A)
  RASM --> Backup : RepeatedFailure [pasmAttempts>=2 && rasmAttempts>=2 && SP==notVisible] (FR-016A)
  Backup --> RDSM : Completed / modeWord=RDSM

  state "Fault Handling" as Faults {
    [*] --> Nominal
    Nominal --> GyroCommRecovery : GyroFrameError / startCounters (FR-019)
    GyroCommRecovery --> Nominal : GyroOk / resetErrorCount (FR-019)
    Nominal --> ThrusterShutdown : FrequentJetting [<1s for 5s] / shutdownThruster (FR-018)
    ThrusterShutdown --> Nominal : GroundClear / (FR-002)
  }

  RDSM --> Faults : FaultEvent
  PASM --> Faults : FaultEvent
  RASM --> Faults : FaultEvent
  CSM  --> Faults : FaultEvent
  Faults --> RDSM : ResumeNominal / keepModeOrReset
}

note right of ModeSM
ASR-004: mode-based control with redundancy and fault management.
assumption: "RateDamped" and "PitchSearchFailed/RollSearchFailed" are internal events
computed by ModeManager thresholds (FR-011..FR-015).
end note
@enduml
```

## ProcessView
5. Activity — Process View: Activity Diagram
```plantuml
@startuml Activity_ControlCycle160ms
skinparam shadowing false

start
:On 32ms Timer Tick (ISR);\nupdate tick32ms;
if (tick32ms == 0?) then (yes)
  :Start 160ms Control Cycle;\ncycleId++;
  note right
  NFR-001: ControlCycleDuration = 160±2ms
  end note

  :Receive remote command (0x88DA);
  :Verify command [IntegrityCheck]; 
  if (Command valid?) then (yes)
    :Set operating mode word;
  else (no)
    :Drop command;\nlog CommandRejected;
  endif

  :Send gyro fetch 0xEB91 (0x881A);
  :Wait >= 5ms before read;
  :Read gyro frame;
  :Validate gyro frame (len/header/checksum);
  if (Gyro frame valid?) then (yes)
    :Reset gyro error counters;
  else (no)
    :Update gyro error counters;\nstep power-cycle/retry policy;
  endif

  :Acquire sun sensor (AD + latch);\nSP + angleCode12bit;
  :Acquire thruster power status (AD);

  :Determine attitude (3-axis);\nroll/pitch/yaw + rates;
  :Manage mode switching;\nupdate ModeRegister;

  if (t == 128ms?) then (yes)
    :Compute thruster switch data (12);
    :Output 12 thruster switches\nwithin 2ms;
    note right
    NFR-004/FR-021: output at t=128ms, complete within 2ms
    end note
  else (no)
    :Defer thruster output until 128ms slot;
  endif

  :Detect frequent jetting fault;\nshutdown if triggered;

  :Pack telemetry (mode, angle, velocity);
  :Transmit telemetry (0x88DB);\ninter-byte <5us;

  :Measure cycle duration;\nlog {cycleId,duration};
  if (3 consecutive out-of-bounds?) then (yes)
    :Raise timing alert;
  endif
  :End 160ms Control Cycle;
endif
stop
@enduml
```

6. Sequence — Process View: Sequence Diagram
```plantuml
@startuml Sequence_Scenario1_ControlCycle160ms
skinparam shadowing false
actor GroundOperator as GroundOperator

participant "ControlCycleScheduler" as ControlCycleScheduler
participant "CommandProcessor" as CommandProcessor
participant "SerialPortDriver(0x88DA)" as SerialCmd
participant "GyroDriver" as GyroDriver
participant "SerialPortDriver(0x881A)" as SerialGyro
participant "SensorFrameValidator" as SensorFrameValidator
participant "SunSensorDriver" as SunSensorDriver
participant "AdcDriver" as AdcDriver
participant "AttitudeEstimator" as AttitudeEstimator
participant "ModeManager" as ModeManager
participant "ModeRegister" as ModeRegister
participant "ThrusterController" as ThrusterController
participant "ThrusterIoDriver" as ThrusterIoDriver
participant "TelemetryPacker" as TelemetryPacker
participant "TelemetryTransmitter" as TelemetryTransmitter
participant "SerialPortDriver(0x88DB)" as SerialTlm

ControlCycleScheduler -> ControlCycleScheduler : runCycle160ms()

== Command receive/verify ==
CommandProcessor -> SerialCmd : readBytes(maxLen)
SerialCmd --> CommandProcessor : cmdBytes
CommandProcessor -> CommandProcessor : receiveCommand()
CommandProcessor -> CommandProcessor : verifyCommand()
alt CommandValid
  CommandProcessor -> ModeRegister : set modeWord/targets
else CommandInvalid
  CommandProcessor -> CommandProcessor : log CommandRejected
end

== Gyro acquisition ==
GyroDriver -> SerialGyro : sendBytes(0xEB91)
note right of GyroDriver
NFR-007: wait >=5ms between fetch and read
end note
GyroDriver -> GyroDriver : delayMs(>=5)
GyroDriver -> SerialGyro : readBytes(maxLen)
SerialGyro --> GyroDriver : gyroFrame
GyroDriver -> SensorFrameValidator : verifyLength/header/checksum
SensorFrameValidator --> GyroDriver : ok?

== Sun sensor + thruster status ==
SunSensorDriver -> AdcDriver : readChannel(angle)
AdcDriver --> SunSensorDriver : angleCode12bit
SunSensorDriver -> SunSensorDriver : readSunVisible()
ThrusterIoDriver -> AdcDriver : readChannel(thrusterPower)
AdcDriver --> ThrusterIoDriver : powerCode

== Attitude + mode management ==
AttitudeEstimator -> AttitudeEstimator : determineAttitude(gyroFrame,angle,SP)
AttitudeEstimator --> ModeManager : AttitudeEstimate
ModeManager -> ModeRegister : manage(modeReg, est)

== Thruster output at 128ms ==
note over ControlCycleScheduler,ThrusterController
NFR-004/FR-021: at t=128ms output 12 thruster switches within 2ms
end note
ThrusterController -> ThrusterController : computeThrusterCommand(modeReg, est)
ThrusterController -> ThrusterIoDriver : outputSwitchData12(thrCmd)

== Telemetry ==
TelemetryPacker -> TelemetryPacker : pack(modeReg, est)
TelemetryPacker -> TelemetryPacker : encode(msg)
TelemetryTransmitter -> SerialTlm : sendBytes(tlmBytes)
note right of TelemetryTransmitter
NFR-006: inter-byte spacing <5us
end note

ControlCycleScheduler -> ControlCycleScheduler : measureCycleDurationMs()
@enduml
```

```plantuml
@startuml Sequence_Scenario2_BackupSunSensorSwitch
skinparam shadowing false

participant "ControlCycleScheduler" as ControlCycleScheduler
participant "ModeManager" as ModeManager
participant "ModeRegister" as ModeRegister
participant "SunSensorDriver" as SunSensorDriver
participant "ThrusterController" as ThrusterController
participant "ThrusterIoDriver" as ThrusterIoDriver

ControlCycleScheduler -> ModeManager : manage(modeReg, est)

ModeManager -> ModeManager : detectRepeatedSearchFailure()
alt RepeatedFailure (FR-016A)
  ModeManager -> SunSensorDriver : switchToBackupPulse()
  note right of SunSensorDriver
FR-017/NFR-008: 190±1ms instruction, 1ms pulse
end note
  ModeManager -> ModeRegister : activeSunSensor=BACKUP\nmodeWord=RDSM\nreset timers/attempts?
  ModeManager -> ThrusterController : computeThrusterCommand(modeReg, est)
  ThrusterController -> ThrusterIoDriver : outputSwitchData12(thrCmd)\n(adjust settings) (FR-016C)
  ModeManager -> ModeManager : executeRDSM() (FR-016D)
else NotRepeatedFailure
  ModeManager -> ModeManager : continue nominal mode logic
end
@enduml
```

7. Collaboration — Process View: Collaboration Diagram
```plantuml
@startuml Collaboration_Scenario1_ControlCycle160ms
skinparam shadowing false

object ControlCycleScheduler
object CommandProcessor
object "SerialPortDriver(0x88DA)" as SerialCmd
object GyroDriver
object "SerialPortDriver(0x881A)" as SerialGyro
object SensorFrameValidator
object SunSensorDriver
object AdcDriver
object AttitudeEstimator
object ModeManager
object ModeRegister
object ThrusterController
object ThrusterIoDriver
object TelemetryPacker
object TelemetryTransmitter
object "SerialPortDriver(0x88DB)" as SerialTlm

ControlCycleScheduler -- CommandProcessor
CommandProcessor -- SerialCmd
ControlCycleScheduler -- GyroDriver
GyroDriver -- SerialGyro
GyroDriver -- SensorFrameValidator
ControlCycleScheduler -- SunSensorDriver
SunSensorDriver -- AdcDriver
ControlCycleScheduler -- AttitudeEstimator
AttitudeEstimator -- ModeManager
ModeManager -- ModeRegister
ControlCycleScheduler -- ThrusterController
ThrusterController -- ThrusterIoDriver
ControlCycleScheduler -- TelemetryPacker
TelemetryPacker -- TelemetryTransmitter
TelemetryTransmitter -- SerialTlm

note right of ControlCycleScheduler
Scenario1: 160ms control cycle (FR-003/010/011/021/022, NFR-001/004)
end note

ControlCycleScheduler : 1. runCycle160ms()
CommandProcessor : 2. readBytes()
CommandProcessor : 3. verifyCommand()
ModeRegister : 4. setMode()
GyroDriver : 5. sendFetch()
GyroDriver : 6. readFrame()
SensorFrameValidator : 7. validateFrame()
SunSensorDriver : 8. readAngle/SP()
AttitudeEstimator : 9. determineAttitude()
ModeManager : 10. manage()
ThrusterController : 11. computeThrusterCommand()
ThrusterIoDriver : 12. outputSwitchData12()
TelemetryPacker : 13. pack+encode()
TelemetryTransmitter : 14. sendBytes()
@enduml
```

```plantuml
@startuml Collaboration_Scenario2_BackupSunSensorSwitch
skinparam shadowing false

object ControlCycleScheduler
object ModeManager
object ModeRegister
object SunSensorDriver
object ThrusterController
object ThrusterIoDriver

ControlCycleScheduler -- ModeManager
ModeManager -- ModeRegister
ModeManager -- SunSensorDriver
ModeManager -- ThrusterController
ThrusterController -- ThrusterIoDriver

note right of ModeManager
Scenario2: repeated search failure triggers backup sun sensor switch
(FR-016A/B/C/D, FR-017, NFR-008)
end note

ControlCycleScheduler : 1. manage()
ModeManager : 2. detectRepeatedSearchFailure()
SunSensorDriver : 3. switchToBackupPulse()
ModeRegister : 4. set activeSunSensor=BACKUP\nmodeWord=RDSM
ThrusterController : 5. computeThrusterCommand()
ThrusterIoDriver : 6. outputSwitchData12()
ModeManager : 7. executeRDSM()
@enduml
```

## DevelopmentView
8. Package — Development View: Package Diagram
```plantuml
@startuml Package_SunSearchControl
skinparam packageStyle rectangle
skinparam shadowing false

package "app" as app {
  note bottom
  Cyclic executive entrypoint; binds ISR tick to 160ms cycle (ASR-002)
  end note
}

package "domain" as domain {
  note bottom
  Mode/state + control logic (ASR-004)
  end note
}

package "services" as services {
  note bottom
  Estimation, validation, fault mgmt, telemetry packing
  end note
}

package "drivers" as drivers {
  note bottom
  Serial/ADC/IO drivers with fixed addresses (ASR-003)
  end note
}

package "interfaces" as interfaces {
  note bottom
  Versioned message schemas: CommandFrame, TelemetryMsg (NFR-002, FR-022)
  end note
}

package "platform" as platform {
  note bottom
  80C32E MCU specifics, timer ISR, register access (ASR-001/002)
  end note
}

app ..> domain
app ..> services
app ..> drivers
services ..> domain
services ..> interfaces
drivers ..> platform
domain ..> interfaces

note right of drivers
NFR-006: inter-byte <5us
NFR-007: fetch->read >=5ms
end note
@enduml
```

9. Component — Development View: Component Diagram
```plantuml
@startuml Component_SunSearchControl
skinparam componentStyle rectangle
skinparam shadowing false

component "SSCS Application\n[ControlCycle]" as C_App
component "Scheduler Component\n[160ms/32ms]" as C_Sched
component "Command Component\n[Receive/Verify]" as C_Cmd
component "Sensing Component\n[Gyro/Sun/ThrStatus]" as C_Sense
component "Estimation Component\n[Attitude]" as C_Est
component "Mode Control Component\n[RDSM/PASM/RASM/CSM]" as C_Mode
component "Actuation Component\n[Thruster Output]" as C_Act
component "Fault Management Component\n[Gyro/Thruster]" as C_Fault
component "Telemetry Component\n[Pack/Send]" as C_Tlm

component "SerialPortDriver" as C_Serial
component "AdcDriver" as C_Adc
component "TimerISR/Platform HAL" as C_Platform

interface "ICommandRx" as I_CommandRx
interface "ISensorRead" as I_SensorRead
interface "IAttitudeEstimate" as I_AttEst
interface "IModeManage" as I_Mode
interface "IThrusterOut" as I_ThrOut
interface "ITelemetryTx" as I_TlmTx

C_App --> C_Sched
C_Sched --> C_Cmd : uses
C_Sched --> C_Sense : uses
C_Sched --> C_Est : uses
C_Sched --> C_Mode : uses
C_Sched --> C_Act : uses
C_Sched --> C_Fault : uses
C_Sched --> C_Tlm : uses

C_Cmd - I_CommandRx
C_Sense - I_SensorRead
C_Est - I_AttEst
C_Mode - I_Mode
C_Act - I_ThrOut
C_Tlm - I_TlmTx

C_Cmd ..> C_Serial : 0x88DA
C_Sense ..> C_Serial : 0x881A
C_Sense ..> C_Adc
C_Act ..> C_Adc
C_Act ..> C_Platform : timing slot t=128ms
C_Tlm ..> C_Serial : 0x88DB
C_Sched ..> C_Platform : 32ms ISR

note right of C_Platform
ASR-001/002: 80C32E, single 32ms interrupt, cyclic executive
end note

note right of C_Serial
ASR-003/NFR-006: fixed addresses; inter-byte <5us
end note
@enduml
```

## PhysicalView
10. Deployment — Physical View: Deployment Diagram
```plantuml
@startuml Deployment_SunSearchControl
skinparam shadowing false

node "Satellite Control Computer\n<<80C32E>>\n11.0592MHz\nPROM 32KB, SRAM 8KB" as MCU {
  artifact "SSCS Firmware\n(monolithic image)" as FW
}

node "Gyroscope Unit" as Gyro
node "Sun Sensor Primary" as SunP
node "Sun Sensor Backup" as SunB
node "Thruster Assembly\n(12 channels)" as Thr
node "Ground Segment\nTelemetry Monitor" as Ground

MCU -- Gyro : Async Serial @0x881A\n(NFR-007 delay>=5ms)
MCU -- Ground : Async Serial @0x88DA (cmd rx)\n@0x88DB (telemetry tx)
MCU -- SunP : AD + latch signals\n(NFR-005 12-bit)
MCU -- SunB : AD + latch signals\n(NFR-005 12-bit)
MCU -- Thr : Digital outputs (12)\n+ AD status

note right of MCU
ASR-002: 32ms timer ISR; 160ms control cycle
NFR-004: thruster output at t=128ms within cycle
end note

note right of Ground
assumption: Ground sends commands over the same physical serial link
as telemetry but via distinct addresses/ports per ASR-003.
end note
@enduml
```

11. Container — Physical View: Container Diagram
```plantuml
@startuml Container_SunSearchControl
skinparam shadowing false
skinparam rectangleStyle rounded

rectangle "Satellite Control Computer\n<<80C32E MCU>>" as MCU {
  rectangle "SSCS Firmware\n[CyclicExecutive]\n- 32ms ISR\n- 160ms cycle\n- mode control\n- fault mgmt" as Firmware
  rectangle "Platform HAL\n[Timer/Registers]" as HAL
  rectangle "Drivers\n[Serial/ADC/IO]" as Drivers
  rectangle "Domain+Services\n[Estimation/Mode/Telemetry]" as Domain
}

rectangle "Gyroscope Unit\n[Serial]" as Gyro
rectangle "Sun Sensor Primary\n[AD+Latch]" as SunP
rectangle "Sun Sensor Backup\n[AD+Latch]" as SunB
rectangle "Thruster Assembly\n[12 outputs + status]" as Thr
rectangle "Ground Segment\n[Command+Telemetry]" as Ground

Firmware --> HAL : uses
Firmware --> Drivers : uses
Firmware --> Domain : uses
Domain --> Drivers : uses

Drivers --> Gyro : Serial 0x881A\n(fetch 0xEB91)
Drivers --> Ground : Serial 0x88DA (cmd)\n0x88DB (tlm)
Drivers --> SunP : AD angle 12-bit\nSP/power latch
Drivers --> SunB : AD angle 12-bit\nSP/power latch
Drivers --> Thr : output @128ms\nstatus via AD

note right of Firmware
Key constraints:
- NFR-001: 160±2ms cycle duration
- NFR-006: inter-byte <5us
- NFR-004: thruster output at 128ms, complete within 2ms
- ASR-004: RDSM/PASM/RASM/CSM + backup sensor + faults
end note
@enduml
```