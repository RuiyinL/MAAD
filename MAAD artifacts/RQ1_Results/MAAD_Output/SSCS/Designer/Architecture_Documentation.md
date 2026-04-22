Scope: Produce production-ready architecture documentation for the Sun Search Control System (SSCS) aligned to the provided requirements and the 11 referenced UML diagrams.  
Approach: Normalize narrative requirements into atomic `INF-*` FR/NFR/ASR IDs, map them to the given 4+1 views, and specify implementable contracts (OpenAPI + internal proto), schemas, and ops/security/testing plans.  
Top validation steps: (1) full traceability matrix coverage, (2) timing/serial constraints verification (<5us, >=5ms, 32ms/160ms/128ms), (3) fault-mode and mode-transition acceptance tests.

# A. Executive Summary (≤1 page)

## System overview
The Sun Search Control System (SSCS) is an embedded control firmware running on an 80C32E-based control computer that performs cyclic (160ms) attitude acquisition and control: it reads gyroscope and sun sensor data, estimates attitude, manages mode transitions (RDSM/PASM/RASM/CSM), outputs thruster switch commands at a fixed time slot (t=128ms), handles faults (gyro comm, frequent jetting), receives ground commands, and transmits telemetry.

**Primary diagram mapping (one-line):** Context and behavior are captured by *UseCase_SunSearchControl* (SSCS: UC_Init/UC_RxCmd/UC_AcqSensors/UC_ModeMgr/UC_ThrOut/UC_Tlm), runtime cycle by *Activity_ControlCycle160ms* and *Sequence_Scenario1_ControlCycle160ms*, mode logic by *State_ModeRegister* (ModeSM states RDSM/PASM/RASM/CSM + Backup + Faults), and deployment by *Deployment_SunSearchControl* (MCU↔Gyro/Sun/Thr/Ground links).

## Architectural style(s)
- **Style:** Time-triggered cyclic executive + interrupt-driven tick ISR (single ISR) with layered drivers/services/domain.  
- **Deployment topology:** Single-node embedded firmware (monolithic image) on 80C32E with external peripherals over serial/ADC/IO.

## Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---|---|
| Timing noncompliance (160±2ms cycle, thruster output at 128ms, inter-byte <5us, gyro fetch->read >=5ms) | Loss of control authority, invalid sensor reads, missed thruster slot | Implement a deterministic cyclic executive with a tick counter; precompute thruster command before 128ms; use hardware UART with tight loops/DMA-like buffering; add cycle duration measurement + alert after 3 violations (INF-NFR-001, INF-NFR-004, INF-NFR-006, INF-NFR-007). |
| Gyro comm instability leading to repeated bad frames | Attitude estimate invalid; unsafe control outputs | Enforce strict frame validation; implement the specified 5-cycle error → power-off → wait 5 → power-on → wait 5 → retry policy; latch “await ground” after second failure (INF-FR-019). |
| Sun not detected and sensor redundancy switching errors | Failure to acquire sun; mission power risk | Track PASM/RASM attempts; after 2+2 failures switch to backup sensor with 190±1ms instruction and 1ms pulse; reset to RDSM and restart search (INF-FR-016, INF-FR-017). |

## Key QA coverage mapping

| Quality attribute | Requirement IDs | Test types |
|---|---|---|
| Performance/real-time | INF-NFR-001, INF-NFR-004, INF-NFR-006, INF-NFR-007, INF-ASR-002 | HIL timing tests, cycle profiling, UART waveform capture, ISR jitter tests |
| Availability/reliability | INF-FR-018, INF-FR-019, INF-FR-016 | Fault-injection, endurance tests, power-cycle recovery tests |
| Security (command integrity) | INF-FR-003, INF-FR-022 | Protocol fuzzing, checksum negative tests, replay tests (if added) |
| Maintainability | INF-ASR-004, INF-ASR-003 | Static analysis, modular build, interface contract tests |
| Scalability | N/A (embedded single node) | Not applicable; verify resource bounds (PROM/SRAM) via map-file checks |

---

# B. Traceability & Rationale

## Normalized requirement set (inferred IDs)
The provided requirements text has no stable IDs; the following `INF-*` IDs are inferred and used for traceability.

**Traceability matrix (CSV):**

```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-ASR-001,MCU platform 80C32E 11.0592MHz PROM32KB SRAM8KB,Deployment_SunSearchControl:MCU; Container_SunSearchControl:MCU/Firmware/HAL,platform/HAL,architecture.md,Constrains runtime, memory, and implementation approach.
INF-ASR-002,Single 32ms timer interrupt drives 160ms cycle (5 ticks),Activity_ControlCycle160ms:start/tick32ms; Class_SunSearchControl:ControlCycleScheduler; Component_SunSearchControl:C_Sched,app/Scheduler,architecture.md,Implements mandated main+interrupt model and deterministic scheduling.
INF-ASR-003,Fixed serial port addresses for cmd/gyro/tlm (0x88DA/0x881A/0x88DB),Deployment_SunSearchControl:MCU--Ground/MCU--Gyro; Class_SunSearchControl:SerialPortDriver,drivers/SerialPortDriver,architecture.md,Ensures correct hardware integration and prevents address drift.
INF-ASR-004,Mode-based control with redundancy and fault management,State_ModeRegister:ModeSM; Component_SunSearchControl:C_Mode/C_Fault,domain/ModeManager services/FaultManagers,architecture.md,Defines core control behavior and safety fallbacks.
INF-FR-001,Perform sun acquisition using gyro+sun sensor to determine attitude and rotate to detect/maintain sun-pointing,UseCase_SunSearchControl:UC_Att/UC_ModeMgr/UC_ThrOut; Activity_ControlCycle160ms:Determine attitude/Manage mode/Thruster output,Domain+Services,architecture.md,Core mission function.
INF-FR-002,Receive ground commands via serial and set operating mode word,UseCase_SunSearchControl:UC_RxCmd/UC_SetMode; Sequence_Scenario1_ControlCycle160ms:Command receive/verify,CommandProcessor,openapi.yaml internal.proto,Defines command ingress and mode control.
INF-FR-003,Command verification: length/header/checksum per spec,UseCase_SunSearchControl:UC_VerCmd; Activity_ControlCycle160ms:Verify command,CommandProcessor/SensorFrameValidator,internal.proto,Ensures only valid commands affect control.
INF-FR-004,Initialization executed once on power-on/reset; set initial mode=RDSM; power on components; start timer via GTCR0 D0 at 0x8083,UseCase_SunSearchControl:UC_Init; Class_SunSearchControl:ControlCycleScheduler/ModeRegister; Deployment_SunSearchControl:MCU,platform/HAL + app init,architecture.md,Implements required boot sequence and timer start.
INF-FR-005,Collect SP signal and tuning element state via latch circuit,Deployment_SunSearchControl:MCU--SunP/SunB; Class_SunSearchControl:SunSensorDriver,drivers/SunSensorDriver,architecture.md,Defines sun visibility acquisition path.
INF-FR-006,Gyro data acquisition each 160ms: send 0xEB91 (2 bytes) and receive frame on 0x881A,Activity_ControlCycle160ms:Send gyro fetch/Read gyro frame; Class_SunSearchControl:GyroDriver,drivers/GyroDriver,architecture.md,Defines gyro comm behavior.
INF-NFR-007,Delay >=5ms between sending fetch and reading gyro data,Class_SunSearchControl:GyroDriver note; Activity_ControlCycle160ms:Wait >=5ms,drivers/GyroDriver,architecture.md,Prevents reading before gyro response is ready.
INF-NFR-006,Inter-byte spacing <5us for gyro cmds and telemetry,Class_SunSearchControl:SerialPortDriver note; Sequence_Scenario1_ControlCycle160ms:sendBytes notes,drivers/SerialPortDriver,architecture.md,Meets strict UART timing.
INF-FR-007,Validate gyro frame length/header/checksum,UseCase_SunSearchControl:UC_ValGyro; Activity_ControlCycle160ms:Validate gyro frame,SensorFrameValidator,internal.proto,Ensures data integrity for attitude estimation.
INF-FR-008,Angle measurement via 12-bit ADC offset-binary 0x000-0xFFF,Deployment_SunSearchControl:MCU--SunP/SunB; Class_SunSearchControl:AdcDriver/SunSensorDriver,drivers/AdcDriver,architecture.md,Defines sensor data representation.
INF-FR-009,Collect power status signals via ADC (components),UseCase_SunSearchControl:UC_AcqThrStat; Activity_ControlCycle160ms:Acquire thruster power status,AdcDriver/ThrusterIoDriver,architecture.md,Supports health monitoring and telemetry.
INF-FR-010,Acquire sun sensor data every 160ms: power status + SP + angle,UseCase_SunSearchControl:UC_AcqSun; Activity_ControlCycle160ms:Acquire sun sensor,SunSensorDriver,architecture.md,Provides sun detection inputs.
INF-FR-011,Acquire thruster status every 160ms via ADC,UseCase_SunSearchControl:UC_AcqThrStat; Activity_ControlCycle160ms:Acquire thruster power status,ThrusterIoDriver,architecture.md,Supports fault detection and reporting.
INF-FR-012,Determine 3-axis attitude every 160ms using gyro rates + sun angle + SP,UseCase_SunSearchControl:UC_Att; Sequence_Scenario1_ControlCycle160ms:AttitudeEstimator,AttitudeEstimator,architecture.md,Defines estimation cadence and inputs.
INF-FR-013,Mode RDSM: rate damping to reduce 3-axis angular velocity to ~0,State_ModeRegister:RDSM; Class_SunSearchControl:ModeManager.executeRDSM,ModeManager,architecture.md,Implements stabilization mode.
INF-FR-014,Mode PASM: rotate about pitch axis at specified rate to search sun,State_ModeRegister:PASM; Class_SunSearchControl:ModeManager.executePASM,ModeManager/ThrusterController,architecture.md,Implements pitch search.
INF-FR-015,Mode RASM: rotate about roll axis at specified rate to search sun,State_ModeRegister:RASM; Class_SunSearchControl:ModeManager.executeRASM,ModeManager/ThrusterController,architecture.md,Implements roll search.
INF-FR-016,Mode CSM: after sun detected, stabilize and track sun; also manage repeated search failure and switch to backup sensor after 2 PASM+2 RASM failures,State_ModeRegister:CSM/Backup; Sequence_Scenario2_BackupSunSensorSwitch,ModeManager/SunSensorDriver,architecture.md,Defines cruise and redundancy behavior.
INF-FR-017,Sun sensor switching instruction: 190±1ms with 1ms positive pulse via register enable write,Class_SunSearchControl:SunSensorDriver.switchToBackupPulse note,SunSensorDriver + HAL timer,architecture.md,Ensures correct hardware switching waveform.
INF-FR-018,Frequent jetting fault: if thruster firing interval <1s continuously for 5s then shut down thruster,State_ModeRegister:Faults.ThrusterShutdown; UseCase_SunSearchControl:UC_JetFault,ThrusterIntervalMonitor/ThrusterIoDriver,architecture.md,Prevents unsafe rapid firing.
INF-FR-019,Gyro comm fault handling: 5 consecutive bad cycles -> power off; wait 5; power on; wait 5; retry; if again 5 bad -> power off and await ground,State_ModeRegister:Faults.GyroCommRecovery; UseCase_SunSearchControl:UC_GyroFault,GyroFaultManager/GyroDriver,architecture.md,Implements mandated recovery ladder.
INF-FR-020,Gyro power-on init: send 0xEB92 then control command on 0x881A with <5us inter-byte,Class_SunSearchControl:GyroDriver.powerOn/control note,GyroDriver/SerialPortDriver,architecture.md,Ensures gyro starts correctly.
INF-FR-021,Thruster switch output: at 128ms of each 160ms cycle sequentially output 12 thruster switch data,Activity_ControlCycle160ms:t==128ms; Class_SunSearchControl:ThrusterCommand.scheduledMs=128,ThrusterController/ThrusterIoDriver,architecture.md,Meets actuation timing slot.
INF-NFR-004,Thruster output completes within 2ms at t=128ms,Class_SunSearchControl:ThrusterController note,ThrusterController/ThrusterIoDriver,architecture.md,Bounds actuation latency.
INF-FR-022,Telemetry every 160ms: pack mode/angle/velocity and send via 0x88DB with <5us inter-byte,UseCase_SunSearchControl:UC_Tlm; Sequence_Scenario1_ControlCycle160ms:TelemetryTransmitter,TelemetryPacker/TelemetryTransmitter,architecture.md,Provides ground monitoring.
INF-NFR-001,Control cycle duration 160±2ms; alert after 3 consecutive violations,Class_SunSearchControl:ControlCycleScheduler note; Activity_ControlCycle160ms:Measure cycle duration,ControlCycleScheduler,architecture.md,Ensures deterministic control timing.
INF-FR-023,Remote command receive each 160ms from 0x88DA; at most 1 command per 160ms,Activity_ControlCycle160ms:Receive remote command; Deployment_SunSearchControl:MCU--Ground,CommandProcessor/SerialPortDriver,architecture.md,Matches ground interface constraint.
INF-FR-024,Timer start by writing 1 to GTCR0 D0 at address 0x8083,Class_SunSearchControl:ControlCycleScheduler; Deployment_SunSearchControl:MCU,platform/HAL,architecture.md,Defines exact register-level behavior.
```

---

# C. Architecture Overview

## Context (Scenario View)
- Actors and use cases are defined in *UseCase_SunSearchControl* (SSCS rectangle; UC_Init, UC_RxCmd, UC_AcqSensors, UC_Att, UC_ModeMgr, UC_ThrOut, UC_Tlm; fault extensions UC_GyroFault/UC_JetFault/UC_SunSwitch).
- SSCS interacts with GroundOperator via command RX (0x88DA) and telemetry TX (0x88DB), with Gyroscope via serial (0x881A), with Sun Sensors via ADC+latch, and with Thruster Assembly via digital outputs + ADC status (*Deployment_SunSearchControl*: MCU links).

## Containers (Physical View)
- *Container_SunSearchControl* shows a single embedded container: **SSCS Firmware** plus **Platform HAL** and **Drivers**, connected to external devices (Gyro, SunP/SunB, Thrusters, Ground).

## Components/Packages (Development View)
- *Package_SunSearchControl* partitions code into `platform`, `drivers`, `services`, `domain`, `interfaces`, `app`.
- *Component_SunSearchControl* defines runtime components: Scheduler, Command, Sensing, Estimation, Mode Control, Actuation, Fault Management, Telemetry, backed by Serial/ADC/Platform HAL.

## Class/Runtime (Logic + Process Views)
- *Class_SunSearchControl* provides the implementable class model: `ControlCycleScheduler`, `ModeRegister`, `CommandProcessor`, `GyroDriver`, `SunSensorDriver`, `ThrusterIoDriver`, `AttitudeEstimator`, `ModeManager`, `ThrusterController`, `GyroFaultManager`, `ThrusterIntervalMonitor`, `TelemetryPacker/Transmitter`.
- *Activity_ControlCycle160ms* and *Sequence_Scenario1_ControlCycle160ms* define the 160ms cycle flow and ordering constraints (gyro fetch, >=5ms wait, validation, attitude, mode, thruster at 128ms, telemetry).
- *State_ModeRegister* defines the mode state machine and fault substates.

## Deployment
- *Deployment_SunSearchControl* is the authoritative topology: 80C32E MCU running monolithic firmware connected to Gyro (serial 0x881A), Ground (serial 0x88DA/0x88DB), Sun sensors (ADC+latch), Thrusters (12 outputs + ADC status).

---

# D. Detailed Technical Design (developer-facing)

> Note: The original system is embedded firmware on 80C32E. Sections D.2 “technology options” are provided as requested, but the **Recommended** choices are constrained to embedded C/8051 toolchains and bare-metal patterns to satisfy INF-ASR-001/002/003 and timing NFRs.

## D.1 Subsystem: Cyclic Executive & Scheduler (app + platform)

### D.1.1 Responsibilities & data ownership
Owns the 32ms ISR tick, derives the 160ms control cycle (5 ticks), enforces the t=128ms thruster output slot, measures cycle duration, and orchestrates calls to command/sensing/estimation/mode/actuation/telemetry. Owns `cycleId`, `tick32ms`, and timing diagnostics.

### D.1.2 Technology options (by concern; 3 alternatives each)

- **Language/runtime**
  - Recommended: Embedded C (Keil C51 or SDCC for 8051)  
  - Conservative: 8051 assembly for ISR + C for rest  
  - Cutting-edge: Rust (only if an 8051 Rust toolchain is proven; typically not)

- **Web framework**
  - Recommended: N/A (embedded)  
  - Conservative: N/A  
  - Cutting-edge: N/A

- **RPC/HTTP**
  - Recommended: N/A (serial protocols)  
  - Conservative: N/A  
  - Cutting-edge: N/A

- **Persistence (SQL/NoSQL)**
  - Recommended: N/A (SRAM structs + optional ring-buffer logs)  
  - Conservative: N/A  
  - Cutting-edge: FRAM/EEPROM-backed event log (if hardware exists)

- **Cache**
  - Recommended: In-memory last-value cache (structs)  
  - Conservative: None  
  - Cutting-edge: Double-buffered sensor frames with lock-free swap

- **Messaging**
  - Recommended: In-process message structs (no queue)  
  - Conservative: Function-call only  
  - Cutting-edge: Static ring-buffer event bus

- **Search**
  - Recommended: N/A  
  - Conservative: N/A  
  - Cutting-edge: N/A

- **Authn/authz**
  - Recommended: N/A (ground link assumed trusted; integrity via checksum)  
  - Conservative: N/A  
  - Cutting-edge: Add command signing (if allowed) (see K)

- **Observability**
  - Recommended: Telemetry counters + fault flags + cycle timing stats  
  - Conservative: Minimal counters only  
  - Cutting-edge: On-target trace buffer with host decode

- **CI/CD**
  - Recommended: GitHub Actions/GitLab CI building firmware + unit tests in host simulator  
  - Conservative: Local build scripts only  
  - Cutting-edge: Hardware-in-the-loop CI with UART capture

- **Container runtime / infra provisioning**
  - Recommended: N/A (embedded)  
  - Conservative: N/A  
  - Cutting-edge: N/A

### D.1.3 Recommended default stack
- **Keil C51 v9.x** (or SDCC 4.2–4.4) + bare-metal HAL for GTCR0 (0x8083) + cyclic executive.  
Justification: meets INF-ASR-001 (80C32E constraints) and INF-ASR-002 (single 32ms ISR scheduling).

### D.1.4 Interface design
- External API: provided in `openapi.yaml` as a *ground-segment façade* (see D.6) because embedded serial is not OpenAPI-native.  
- Internal contract: `internal.proto` defines logical messages between components (even if implemented as C structs) to enforce schema stability.

### D.1.5 Data model / schema
Persisted entities are minimal; see `sql/` artifacts for ground-side storage of telemetry/commands (optional but recommended for test/ops).

### D.1.6 Caching & consistency
Cache last valid sensor frames and last computed `AttitudeEstimate` in SRAM; strong consistency within a cycle (single-threaded), overwrite each cycle.

---

## D.2 Subsystem: Command Ingress & Verification (CommandProcessor)

### D.2.1 Responsibilities & data ownership
Reads at most one command per 160ms from serial address 0x88DA, validates length/header/checksum, and updates `ModeRegister` for the next cycle (mode word, targets). Owns command rejection counters.

### D.2.2 Technology options
- **Language/runtime**
  - Recommended: Embedded C  
  - Conservative: C + table-driven parser  
  - Cutting-edge: Generated parser from a DSL

- **RPC/HTTP**
  - Recommended: Serial frame parser (binary)  
  - Conservative: Fixed-length frames only  
  - Cutting-edge: CBOR framing (not required)

- **Authn/authz**
  - Recommended: Frame integrity (checksum) only  
  - Conservative: Header+length only (not acceptable)  
  - Cutting-edge: Add MAC/signature (requires requirement change)

(Other concerns N/A for embedded; see D.1 list.)

### D.2.3 Recommended default stack
- C parser with strict validation and “execute-next-cycle” semantics.  
Justification: meets INF-FR-023 (≤1 cmd/160ms) and INF-FR-003 (verify length/header/checksum).

### D.2.4 Interface design
- Serial command frame schema is represented in `internal.proto` (`CommandFrame`).

### D.2.5 Data model / schema
Ground-side command log table: `sql/command_log_ddl.sql`.

### D.2.6 Caching & consistency
Keep only the last accepted command; apply at cycle boundary to avoid mid-cycle mode changes.

---

## D.3 Subsystem: Gyro Acquisition & Validation (GyroDriver + SensorFrameValidator + GyroFaultManager)

### D.3.1 Responsibilities & data ownership
Sends fetch command `0xEB91` each 160ms to gyro over 0x881A, waits >=5ms, reads response frame, validates it, and provides parsed rates to estimator. On init, sends `0xEB92` then control command with <5us inter-byte. Fault manager enforces the specified power-cycle ladder.

### D.3.2 Technology options
- **Serial implementation**
  - Recommended: Hardware UART with tight polling TX loop ensuring <5us inter-byte  
  - Conservative: Bit-banged serial (high risk)  
  - Cutting-edge: UART with interrupt-driven TX FIFO (if available)

- **Validation**
  - Recommended: Central `SensorFrameValidator` used by gyro and command  
  - Conservative: Inline checks in driver  
  - Cutting-edge: Generated validators from schema

### D.3.3 Recommended default stack
- Hardware UART driver + deterministic delay function + validator + fault ladder.  
Justification: meets INF-NFR-006 (<5us inter-byte) and INF-NFR-007 (>=5ms fetch->read) and INF-FR-019 (recovery policy).

### D.3.4 Interface design
- `internal.proto` includes `GyroFetchRequest`, `GyroFrame`, `GyroFaultState`.

### D.3.5 Data model / schema
Ground-side gyro error events: `sql/fault_event_ddl.sql`.

### D.3.6 Caching & consistency
Cache last valid gyro frame; if invalid, estimator uses last-known-good with a “stale” flag (A-assumption; see K) or zeros depending on safety policy.

---

## D.4 Subsystem: Sun Sensor Acquisition & Switching (SunSensorDriver)

### D.4.1 Responsibilities & data ownership
Reads sun sensor power status, SP (sun visible sign) via latch, and 12-bit angle code via ADC each 160ms. Performs sensor switching to backup by generating a 190±1ms instruction with a 1ms positive pulse via control register write.

### D.4.2 Technology options
- **ADC**
  - Recommended: MCU ADC peripheral driver with calibrated conversion to 12-bit code  
  - Conservative: External ADC driver (if ADC external)  
  - Cutting-edge: Oversampling + digital filtering (if CPU budget allows)

- **Switch pulse generation**
  - Recommended: Timer-based pulse scheduling (non-blocking)  
  - Conservative: Busy-wait delay loops (timing drift risk)  
  - Cutting-edge: Hardware PWM/compare output (if available)

### D.4.3 Recommended default stack
- Timer-based pulse generation + ADC driver returning raw 12-bit code.  
Justification: meets INF-FR-017 (190±1ms, 1ms pulse) and INF-FR-008 (12-bit code range).

### D.4.4 Interface design
- `internal.proto` includes `SunSensorSample` and `SunSensorSwitchCommand`.

### D.4.5 Data model / schema
Ground-side sun sensor samples: `sql/telemetry_sample_ddl.sql`.

### D.4.6 Caching & consistency
Cache last sample per active sensor; switching updates `ModeRegister.activeSunSensor` atomically at cycle boundary.

---

## D.5 Subsystem: Attitude Estimation + Mode Management + Thruster Output (Domain)

### D.5.1 Responsibilities & data ownership
- `AttitudeEstimator`: converts gyro frame + sun angle/SP into `AttitudeEstimate` (roll/pitch/yaw + rates + sunVisible).
- `ModeManager`: implements RDSM/PASM/RASM/CSM, tracks mode duration, attempts, and triggers backup sensor switching and fault transitions.
- `ThrusterController`: computes 12-bit thruster switch command and outputs it at t=128ms within 2ms.

### D.5.2 Technology options
- **Control law implementation**
  - Recommended: Fixed-point integer math (int16/int32)  
  - Conservative: Lookup-table control  
  - Cutting-edge: Floating-point (not suitable on 80C32E)

- **Thruster scheduling**
  - Recommended: Precompute command early in cycle; output in 128ms slot  
  - Conservative: Compute at 128ms (risk missing 2ms window)  
  - Cutting-edge: Two-stage pipeline with shadow registers

### D.5.3 Recommended default stack
- Fixed-point control + precomputed thruster command + deterministic output routine.  
Justification: meets INF-FR-021 (output at 128ms) and INF-NFR-004 (complete within 2ms).

### D.5.4 Interface design
- `internal.proto` includes `ModeRegisterState`, `ThrusterCommand`, `AttitudeEstimate`.

### D.5.5 Data model / schema
Ground-side mode transitions and thruster commands: `sql/mode_transition_ddl.sql` and `sql/thruster_command_ddl.sql`.

### D.5.6 Caching & consistency
Strong consistency within cycle; mode changes apply next cycle. Thruster command is “write-once per cycle” and immutable after computed.

---

## D.6 Subsystem: Telemetry Packaging & Transmission (TelemetryPacker/Transmitter)

### D.6.1 Responsibilities & data ownership
Every 160ms, packages current mode word, angle, and velocity into telemetry bytes and transmits via serial 0x88DB with <5us inter-byte spacing.

### D.6.2 Technology options
- **Encoding**
  - Recommended: Fixed binary frame with header/len/checksum  
  - Conservative: Raw fields only (no integrity)  
  - Cutting-edge: COBS/SLIP framing

- **Transmission**
  - Recommended: Hardware UART with tight TX loop  
  - Conservative: Interrupt-driven TX (risk spacing)  
  - Cutting-edge: DMA (unlikely on 80C32E)

### D.6.3 Recommended default stack
- Fixed binary telemetry frame + UART TX loop enforcing <5us inter-byte.  
Justification: meets INF-FR-022 (telemetry every 160ms) and INF-NFR-006 (<5us inter-byte).

### D.6.4 External APIs (OpenAPI YAML) — `openapi.yaml`
Because SSCS uses serial ports, the OpenAPI describes a **ground-side gateway/service** that (a) accepts operator commands, (b) logs and forwards them to the serial link, and (c) exposes telemetry and fault state to tools. This is a production-ready integration surface for test rigs and operations.

(Full file in Section L.)

### D.6.5 Internal contracts — `internal.proto`
Defines canonical message schemas used across firmware modules and the ground gateway.

(Full file in Section L.)

### D.6.6 Data model / schema
Telemetry storage: `sql/telemetry_sample_ddl.sql`.

### D.6.7 Caching & consistency
Ground gateway caches last telemetry sample per spacecraft for 1s TTL; firmware does not cache telemetry beyond current pack.

---

# E. Operations & Deployment (ops-facing)

> Embedded firmware is not deployed on Kubernetes. The k8s plan below applies to the **ground gateway** (serial bridge + API + storage) used for integration testing, commanding, and telemetry monitoring.

## E.1 Kubernetes-ready plan (representative manifest)
- Component: `sscs-ground-gateway` (REST API + serial bridge)
Justification: supports verification of INF-FR-022 (telemetry handling) and INF-FR-002/003 (command verification) in an automated ops environment.

(Manifest in Section L: `k8s/sscs-ground-gateway-deployment.yaml`.)

## E.2 DB HA topology, backups
- PostgreSQL 14–15 (ground side) with streaming replication (1 primary + 1 standby).
- Backups: nightly full + WAL archiving; restore test monthly.
Justification: supports auditability of commands/telemetry for diagnosing INF-FR-019/018 behaviors (fault history).

## E.3 Network topology + ingress/egress rules
- Ingress: HTTPS to gateway API only.
- Egress: gateway to serial device server (or USB serial) only; DB internal.
- Latency expectations: telemetry ingestion < 200ms end-to-end on ground (A-assumption; see K), while on-target timing remains governed by *Deployment_SunSearchControl* links.
Justification: does not alter embedded constraints; preserves INF-ASR-003 address mapping via gateway configuration.

## E.4 CI/CD sketch
1. Build firmware (Keil/SDCC) + run host-based unit tests (estimator/mode logic).
2. Build gateway container + run OpenAPI contract tests.
3. HIL stage: flash firmware to target, run scripted UART tests verifying <5us spacing and >=5ms delay.
4. Deploy gateway via Helm/Kustomize; canary 10% traffic; promote.
Justification: validates INF-NFR-006/007 and INF-NFR-001 deterministically.

---

# F. Security Design

## F.1 Auth & AuthZ
- Ground gateway: OAuth2/OIDC with JWT (RS256), roles: `operator`, `viewer`, `admin`.
- Firmware: no auth; relies on physical link + checksum validation.
Justification: gateway hardening is an enhancement; firmware compliance remains INF-FR-003 (checksum-based verification).

Token lifecycle:
- Access token TTL 15 minutes; refresh token TTL 24 hours; revocation via server-side denylist.

## F.2 Secrets management & rotation
- Kubernetes: External Secrets Operator or sealed-secrets; rotate DB creds every 90 days; rotate JWT signing keys every 180 days.
Justification: supports operational integrity around command/telemetry handling (INF-FR-002/022) though not mandated by embedded SRS.

## F.3 TLS & service-mesh
- TLS 1.2+ at ingress; optional mTLS inside cluster via Linkerd/Istio.
Justification: protects ground command channel; does not conflict with INF-ASR-003 (serial addresses remain internal).

## F.4 Threat model summary (top 5)
| Threat | Mitigation |
|---|---|
| Unauthorized command injection (ground) | OIDC RBAC + audit logs + rate limits |
| Replay of old commands | Include nonce/sequence in gateway; firmware can reject out-of-window (A-assumption) |
| Telemetry tampering | TLS + DB immutability flags |
| Serial bridge compromise | Run as non-root, seccomp, minimal egress |
| Log leakage of sensitive data | Redaction middleware; no raw secrets in logs |

---

# G. Observability & SRE

## G.1 Metrics/logs/traces + example Prometheus alerts
Key metrics (gateway):
- `sscs_commands_received_total{valid=...}`
- `sscs_telemetry_frames_total`
- `sscs_serial_write_errors_total`
- `sscs_last_telemetry_age_seconds`
- `sscs_fault_events_total{type=gyro_comm|frequent_jetting|sensor_switch}`

Example alert rules:
```promql
# Alert if telemetry stops arriving for > 1s
(sscs_last_telemetry_age_seconds > 1)
```
```promql
# Alert on spike of invalid commands
(rate(sscs_commands_received_total{valid="false"}[5m]) > 0.1)
```

Firmware observability:
- Telemetry includes mode word, angle, velocity; add counters for gyro frame errors and thruster shutdown state (A-assumption).

## G.2 SLOs, error budgets, RTO/RPO
Gateway SLOs:
- Telemetry availability: 99.9% monthly (A-assumption).
- RTO 30 minutes, RPO 24 hours (nightly backups).
Justification: supports operational monitoring of INF-FR-022 and post-incident analysis of INF-FR-019/018.

## G.3 Dashboard & runbook sketch
Dashboards:
- “Control cycle health”: last telemetry age, mode distribution, fault events.
- “Command pipeline”: valid/invalid commands, latency to serial write.
Runbooks:
- Gyro comm fault: verify UART wiring, check error counters, confirm power-cycle ladder executed.
- Frequent jetting: confirm thruster shutdown latched, require ground clear.

---

# H. Testing Strategy

## H.1 Test matrix

| Test type | Components | Examples |
|---|---|---|
| Unit | ModeManager, AttitudeEstimator, validators | Mode transitions; attempt counters; checksum calc |
| Integration | GyroDriver+Serial, SunSensorDriver+ADC, ThrusterIoDriver | UART timing; ADC range mapping; output bit patterns |
| Contract | Gateway OpenAPI; internal.proto schema | OpenAPI lint; backward compatible proto changes |
| E2E (HIL) | Full firmware on target + devices/simulators | 160ms cycle timing; t=128ms thruster output; sensor switch pulse |
| Chaos/fault injection | Fault managers | 5 bad gyro frames → power-cycle; frequent jetting detection |

## H.2 Test data management & environment isolation
Environments:
- `dev` (simulated serial), `staging` (HIL bench), `prod` (ops).
Refresh cadence: staging DB reset weekly; prod retained 90 days (A-assumption).

---

# I. Migration, Data Conversion & Rollout Plan

## I.1 Migration steps
If introducing the ground gateway alongside existing tooling:
1. Deploy gateway in “observe-only” mode (telemetry ingest only).
2. Enable command forwarding for a subset of commands (shadow mode).
3. Cut over operator tooling to gateway endpoints.
Rollback: revert to direct serial tooling; gateway remains passive.

## I.2 Backwards compatibility & API versioning
- OpenAPI versioned under `/api/v1`; breaking changes require `/api/v2`.
- Proto uses field-number stability; only additive changes allowed.

---

# J. Tradeoffs & Alternatives

| Decision | Alternatives | Pros/Cons | Why chosen |
|---|---|---|---|
| Cyclic executive with single ISR | RTOS; multiple interrupts | RTOS adds jitter/overhead; multiple ISRs violate constraint | Required by INF-ASR-002 and timing INF-NFR-001 |
| UART tight-loop for <5us spacing | Interrupt TX; bit-bang | Interrupt TX may violate spacing; bit-bang risky | Meets INF-NFR-006 deterministically |
| Timer-based sensor switch pulse | Busy-wait | Busy-wait can break 160ms cycle | Meets INF-FR-017 while preserving INF-NFR-001 |
| Ground gateway OpenAPI | No gateway; custom scripts | Gateway adds complexity but enables automation and audit | Enables production-grade ops/testing around INF-FR-002/022 |

---

# K. Open Questions & Assumptions

## Assumptions
- **A1:** Gyro response frame format (header/len/checksum polynomial) is available in “Table 3.2-1” but not provided; we assume a standard 1-byte header + len + payload + 1-byte checksum.  
- **A2:** “Gyroscope control command” after 0xEB92 is not specified; we assume it is a fixed 2-byte command configured per gyro vendor.  
- **A3:** Attitude estimation math and thresholds for “RateDamped”, “PitchSearchFailed”, “RollSearchFailed” are not specified; we assume they are configurable constants in PROM.  
- **A4:** On invalid gyro frame, control uses last-known-good rates marked stale for one cycle; if stale persists >N cycles, force RDSM and/or safe mode (needs stakeholder confirmation).  
- **A5:** Ground gateway is permitted as an integration/ops enhancement and does not change embedded serial protocol.

## Conflicts / naming issues (logged per rule)
- **C1:** Requirements mention serial address 0x881 for gyro send/receive, but later specify 0x881A. Diagrams consistently use **0x881A** (*Class_SunSearchControl:GyroDriver uses 0x881A*). **Preference:** keep both as configurable; default to 0x881A; confirm with hardware ICD.  
- **C2:** Sun sensor switching described as “190ms instruction with 1ms positive pulse” (wording ambiguous). Diagrams state “190±1ms instruction, 1ms pulse”. **Preference:** implement 1ms high pulse within a 190ms command window; confirm exact waveform.

## Unresolved stakeholder questions
1. Provide exact command frame format (header value, checksum algorithm, payload schema) for 0x88DA.  
2. Provide exact gyro frame format and checksum algorithm; confirm whether 0x881 vs 0x881A is correct.  
3. Define numeric thresholds: rate damping completion, search failure timeouts, PASM/RASM rates, and CSM tracking behavior.  
4. Confirm whether thruster “shutdown” is latched until ground clear and what the ground-clear command is.  
5. Confirm telemetry frame format and whether it requires checksum.

---

# L. Deliverables

## 1) `architecture.md` (this document)
```md
# architecture.md
(Contents are exactly the sections A–L of ArchitectureDocument.md)
```

## 2) `openapi.yaml`
```yaml
openapi: 3.0.3
info:
  title: SSCS Ground Gateway API
  version: 1.0.0
  description: >
    Ground-side API that bridges operator tools to the Sun Search Control System (SSCS)
    over serial links, and exposes telemetry/fault state for monitoring and testing.
servers:
  - url: https://sscs-gateway.example.com/api/v1
tags:
  - name: Commands
  - name: Telemetry
  - name: Faults
  - name: Admin
components:
  securitySchemes:
    oidc:
      type: openIdConnect
      openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration
  schemas:
    Error:
      type: object
      required: [code, message, requestId]
      properties:
        code: { type: string, example: "INVALID_FRAME" }
        message: { type: string, example: "Checksum mismatch" }
        requestId: { type: string, example: "req_01HXYZ..." }
        details: { type: object, additionalProperties: true }
    CommandRequest:
      type: object
      required: [spacecraftId, modeWord]
      properties:
        spacecraftId: { type: string, example: "SAT-001" }
        modeWord:
          type: integer
          minimum: 0
          maximum: 255
          example: 1
        targetAngleDeg:
          type: integer
          minimum: -32768
          maximum: 32767
          example: 0
        targetRateDps:
          type: integer
          minimum: -32768
          maximum: 32767
          example: 5
        rawFrame:
          type: string
          description: Optional hex-encoded raw command frame to forward as-is.
          example: "A5040100053C"
    CommandResponse:
      type: object
      required: [commandId, accepted, receivedAt]
      properties:
        commandId: { type: string, example: "cmd_01HXYZ..." }
        accepted: { type: boolean, example: true }
        receivedAt: { type: string, format: date-time }
        rejectionReason: { type: string, nullable: true }
    TelemetrySample:
      type: object
      required: [spacecraftId, ts, modeWord, angleDeg, rateDps, sunVisible, activeSunSensor]
      properties:
        spacecraftId: { type: string }
        ts: { type: string, format: date-time }
        modeWord: { type: integer, minimum: 0, maximum: 255 }
        angleDeg: { type: integer, minimum: -32768, maximum: 32767 }
        rateDps: { type: integer, minimum: -32768, maximum: 32767 }
        sunVisible: { type: boolean }
        activeSunSensor: { type: string, enum: [PRIMARY, BACKUP] }
        gyroFrameOk: { type: boolean }
        thrusterShutdown: { type: boolean }
    FaultEvent:
      type: object
      required: [spacecraftId, ts, type, severity]
      properties:
        spacecraftId: { type: string }
        ts: { type: string, format: date-time }
        type: { type: string, enum: [GYRO_COMM, FREQUENT_JETTING, SENSOR_SWITCH, TIMING] }
        severity: { type: string, enum: [INFO, WARN, CRITICAL] }
        details: { type: object, additionalProperties: true }
paths:
  /commands:
    post:
      tags: [Commands]
      summary: Submit an operator command to SSCS (forwarded over serial)
      security: [{ oidc: [] }]
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/CommandRequest" }
      responses:
        "202":
          description: Command accepted for forwarding
          content:
            application/json:
              schema: { $ref: "#/components/schemas/CommandResponse" }
        "400":
          description: Invalid command payload/frame
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Error" }
        "401":
          description: Unauthorized
        "403":
          description: Forbidden
  /commands/{commandId}:
    get:
      tags: [Commands]
      summary: Get command status and forwarding result
      security: [{ oidc: [] }]
      parameters:
        - name: commandId
          in: path
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Command status
          content:
            application/json:
              schema:
                type: object
                required: [commandId, status]
                properties:
                  commandId: { type: string }
                  status: { type: string, enum: [RECEIVED, FORWARDED, REJECTED, FAILED] }
                  lastError: { $ref: "#/components/schemas/Error" }
        "404":
          description: Not found
  /telemetry/latest:
    get:
      tags: [Telemetry]
      summary: Get latest telemetry sample
      security: [{ oidc: [] }]
      parameters:
        - name: spacecraftId
          in: query
          required: true
          schema: { type: string }
      responses:
        "200":
          description: Latest telemetry
          content:
            application/json:
              schema: { $ref: "#/components/schemas/TelemetrySample" }
        "404":
          description: No telemetry available
  /telemetry:
    get:
      tags: [Telemetry]
      summary: Query telemetry samples by time range
      security: [{ oidc: [] }]
      parameters:
        - name: spacecraftId
          in: query
          required: true
          schema: { type: string }
        - name: from
          in: query
          required: true
          schema: { type: string, format: date-time }
        - name: to
          in: query
          required: true
          schema: { type: string, format: date-time }
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 10000, default: 1000 }
      responses:
        "200":
          description: Telemetry list
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/TelemetrySample" }
  /faults:
    get:
      tags: [Faults]
      summary: Query fault events
      security: [{ oidc: [] }]
      parameters:
        - name: spacecraftId
          in: query
          required: true
          schema: { type: string }
        - name: from
          in: query
          required: false
          schema: { type: string, format: date-time }
        - name: to
          in: query
          required: false
          schema: { type: string, format: date-time }
      responses:
        "200":
          description: Fault events
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items: { $ref: "#/components/schemas/FaultEvent" }
  /admin/serial/ports:
    get:
      tags: [Admin]
      summary: List configured serial ports/addresses (0x88DA/0x88DB/0x881A)
      security: [{ oidc: [] }]
      responses:
        "200":
          description: Serial configuration
          content:
            application/json:
              schema:
                type: object
                required: [commandRxAddr, telemetryTxAddr, gyroAddr]
                properties:
                  commandRxAddr: { type: string, example: "0x88DA" }
                  telemetryTxAddr: { type: string, example: "0x88DB" }
                  gyroAddr: { type: string, example: "0x881A" }
```

## 3) `internal.proto`
```proto
syntax = "proto3";

package sscs.v1;

message CommandFrame {
  uint32 header = 1;   // e.g., 0xA5 (A1)
  uint32 len = 2;
  bytes data = 3;
  uint32 checksum = 4;
}

enum ModeWord {
  MODE_UNSPEC = 0;
  MODE_RDSM = 1;
  MODE_PASM = 2;
  MODE_RASM = 3;
  MODE_CSM  = 4;
}

message ModeRegisterState {
  ModeWord mode = 1;
  uint32 modeDurationTicks = 2; // 32ms ticks
  int32 targetAngleDeg = 3;
  int32 targetRateDps = 4;
  uint32 pasmAttempts = 5;
  uint32 rasmAttempts = 6;
  enum SunSensorSel { PRIMARY = 0; BACKUP = 1; }
  SunSensorSel activeSunSensor = 7;
}

message GyroFetchRequest {
  uint32 fetchCmd = 1; // 0xEB91
}

message GyroFrame {
  bytes raw = 1;
  bool valid = 2;
  string invalidReason = 3;
}

message SunSensorSample {
  bool powerOn = 1;
  bool sunVisible = 2;     // SP
  uint32 angleCode12 = 3;  // 0x000..0xFFF
}

message ThrusterStatus {
  bool powerOn = 1;
  uint32 powerCode = 2; // raw ADC if applicable
}

message AttitudeEstimate {
  int32 rollDeg = 1;
  int32 pitchDeg = 2;
  int32 yawDeg = 3;
  int32 wxDps = 4;
  int32 wyDps = 5;
  int32 wzDps = 6;
  bool sunVisible = 7;
}

message ThrusterCommand {
  uint32 switchBits12 = 1; // 12 thrusters
  uint32 scheduledMs = 2;  // 128
}

enum FaultType {
  FAULT_UNSPEC = 0;
  FAULT_GYRO_COMM = 1;
  FAULT_FREQUENT_JETTING = 2;
  FAULT_SENSOR_SWITCH = 3;
  FAULT_TIMING = 4;
}

message FaultState {
  FaultType type = 1;
  uint32 consecutiveErrorCycles = 2;
  uint32 waitCycles = 3;
  bool thrusterShutdown = 4;
}
```

## 4) `k8s/sscs-ground-gateway-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sscs-ground-gateway
  namespace: sscs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sscs-ground-gateway
  template:
    metadata:
      labels:
        app: sscs-ground-gateway
    spec:
      containers:
        - name: gateway
          image: ghcr.io/example/sscs-ground-gateway:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: sscs-gateway-config
            - secretRef:
                name: sscs-gateway-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: sscs-ground-gateway
  namespace: sscs
spec:
  selector:
    app: sscs-ground-gateway
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sscs-ground-gateway
  namespace: sscs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sscs-ground-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: sscs-gateway-config
  namespace: sscs
data:
  COMMAND_RX_ADDR: "0x88DA"
  TELEMETRY_TX_ADDR: "0x88DB"
  GYRO_ADDR: "0x881A"
  SERIAL_DEVICE: "/dev/ttyUSB0"
  DATABASE_URL: "postgres://sscs@postgres.sscs.svc.cluster.local:5432/sscs"
---
apiVersion: v1
kind: Secret
metadata:
  name: sscs-gateway-secrets
  namespace: sscs
type: Opaque
stringData:
  DATABASE_PASSWORD: "REPLACE_ME"
  OIDC_CLIENT_SECRET: "REPLACE_ME"
```

## 5) SQL DDL examples

### `sql/telemetry_sample_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS telemetry_sample (
  id              BIGSERIAL PRIMARY KEY,
  spacecraft_id   TEXT NOT NULL,
  ts              TIMESTAMPTZ NOT NULL,
  mode_word       SMALLINT NOT NULL CHECK (mode_word BETWEEN 0 AND 255),
  angle_deg       SMALLINT NOT NULL,
  rate_dps        SMALLINT NOT NULL,
  sun_visible     BOOLEAN NOT NULL,
  active_sun_sensor TEXT NOT NULL CHECK (active_sun_sensor IN ('PRIMARY','BACKUP')),
  gyro_frame_ok   BOOLEAN NOT NULL,
  thruster_shutdown BOOLEAN NOT NULL,
  raw_frame       BYTEA NULL
);

CREATE INDEX IF NOT EXISTS idx_telemetry_spacecraft_ts
  ON telemetry_sample(spacecraft_id, ts DESC);
```

### `sql/command_log_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS command_log (
  id            BIGSERIAL PRIMARY KEY,
  command_id    TEXT NOT NULL UNIQUE,
  spacecraft_id TEXT NOT NULL,
  received_at   TIMESTAMPTZ NOT NULL,
  mode_word     SMALLINT NOT NULL CHECK (mode_word BETWEEN 0 AND 255),
  target_angle_deg SMALLINT NULL,
  target_rate_dps  SMALLINT NULL,
  accepted      BOOLEAN NOT NULL,
  rejection_reason TEXT NULL,
  raw_frame     BYTEA NULL
);

CREATE INDEX IF NOT EXISTS idx_command_spacecraft_received
  ON command_log(spacecraft_id, received_at DESC);
```

### `sql/fault_event_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS fault_event (
  id            BIGSERIAL PRIMARY KEY,
  spacecraft_id TEXT NOT NULL,
  ts            TIMESTAMPTZ NOT NULL,
  type          TEXT NOT NULL CHECK (type IN ('GYRO_COMM','FREQUENT_JETTING','SENSOR_SWITCH','TIMING')),
  severity      TEXT NOT NULL CHECK (severity IN ('INFO','WARN','CRITICAL')),
  details       JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_fault_spacecraft_ts
  ON fault_event(spacecraft_id, ts DESC);
```

### `sql/mode_transition_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS mode_transition (
  id            BIGSERIAL PRIMARY KEY,
  spacecraft_id TEXT NOT NULL,
  ts            TIMESTAMPTZ NOT NULL,
  from_mode     SMALLINT NOT NULL CHECK (from_mode BETWEEN 0 AND 255),
  to_mode       SMALLINT NOT NULL CHECK (to_mode BETWEEN 0 AND 255),
  reason        TEXT NOT NULL,
  attempts      JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_mode_transition_spacecraft_ts
  ON mode_transition(spacecraft_id, ts DESC);
```

### `sql/thruster_command_ddl.sql`
```sql
CREATE TABLE IF NOT EXISTS thruster_command (
  id            BIGSERIAL PRIMARY KEY,
  spacecraft_id TEXT NOT NULL,
  ts            TIMESTAMPTZ NOT NULL,
  switch_bits12 INTEGER NOT NULL CHECK (switch_bits12 BETWEEN 0 AND 4095),
  scheduled_ms  INTEGER NOT NULL CHECK (scheduled_ms = 128)
);

CREATE INDEX IF NOT EXISTS idx_thruster_command_spacecraft_ts
  ON thruster_command(spacecraft_id, ts DESC);
```

## 6) `traceability_matrix.csv`
```csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-ASR-001,MCU platform 80C32E 11.0592MHz PROM32KB SRAM8KB,Deployment_SunSearchControl:MCU; Container_SunSearchControl:MCU,platform/HAL,architecture.md,Platform constraints drive implementation.
INF-ASR-002,Single 32ms timer interrupt drives 160ms cycle,Activity_ControlCycle160ms:start; Class_SunSearchControl:ControlCycleScheduler,app/Scheduler,architecture.md,Deterministic scheduling.
INF-ASR-003,Fixed serial port addresses 0x88DA/0x88DB/0x881A,Deployment_SunSearchControl:MCU links; Class_SunSearchControl:SerialPortDriver,drivers/SerialPortDriver,architecture.md;k8s/sscs-ground-gateway-deployment.yaml,Prevents integration drift.
INF-ASR-004,Mode-based control with redundancy and faults,State_ModeRegister:ModeSM,domain/ModeManager+FaultManagers,architecture.md,Core behavior.
INF-FR-001,Sun acquisition and sun-pointing control,UseCase_SunSearchControl:UC_Att/UC_ModeMgr/UC_ThrOut,Domain,architecture.md,Primary mission function.
INF-FR-002,Receive ground commands and set mode,UseCase_SunSearchControl:UC_RxCmd/UC_SetMode,CommandProcessor,openapi.yaml;internal.proto,Command ingress.
INF-FR-003,Verify command length/header/checksum,UseCase_SunSearchControl:UC_VerCmd,CommandProcessor/SensorFrameValidator,internal.proto,Integrity gate.
INF-FR-004,Initialization: set RDSM, power on components, start timer,UseCase_SunSearchControl:UC_Init,platform+app init,architecture.md,Required boot behavior.
INF-FR-005,Collect SP and tuning element state via latch,Deployment_SunSearchControl:MCU--SunP/SunB,SunSensorDriver,architecture.md,Sun visibility input.
INF-FR-006,Gyro fetch 0xEB91 each cycle on 0x881A,Activity_ControlCycle160ms:Send gyro fetch,GyroDriver,architecture.md,Sensor acquisition.
INF-NFR-007,Fetch->read delay >=5ms,Activity_ControlCycle160ms:Wait >=5ms,GyroDriver,architecture.md,Timing constraint.
INF-NFR-006,Inter-byte spacing <5us,Class_SunSearchControl:SerialPortDriver note,SerialPortDriver,architecture.md,UART constraint.
INF-FR-007,Validate gyro frame len/header/checksum,UseCase_SunSearchControl:UC_ValGyro,SensorFrameValidator,internal.proto,Data integrity.
INF-FR-008,12-bit ADC angle code 0x000..0xFFF,Deployment_SunSearchControl:MCU--Sun sensors,AdcDriver/SunSensorDriver,architecture.md,Data representation.
INF-FR-009,Collect power status via ADC,Activity_ControlCycle160ms:Acquire thruster power status,AdcDriver/ThrusterIoDriver,architecture.md,Health monitoring.
INF-FR-010,Acquire sun sensor data every 160ms,UseCase_SunSearchControl:UC_AcqSun,SunSensorDriver,architecture.md,Sun detection.
INF-FR-011,Acquire thruster status every 160ms,UseCase_SunSearchControl:UC_AcqThrStat,ThrusterIoDriver,architecture.md,Thruster monitoring.
INF-FR-012,Determine attitude every 160ms,UseCase_SunSearchControl:UC_Att,AttitudeEstimator,architecture.md,Estimation cadence.
INF-FR-013,RDSM rate damping to zero,State_ModeRegister:RDSM,ModeManager,architecture.md,Mode behavior.
INF-FR-014,PASM pitch search,State_ModeRegister:PASM,ModeManager/ThrusterController,architecture.md,Mode behavior.
INF-FR-015,RASM roll search,State_ModeRegister:RASM,ModeManager/ThrusterController,architecture.md,Mode behavior.
INF-FR-016,CSM cruise + repeated failure triggers backup switch,State_ModeRegister:CSM/Backup; Sequence_Scenario2_BackupSunSensorSwitch,ModeManager,architecture.md,Redundancy logic.
INF-FR-017,Sun sensor switch pulse 190±1ms with 1ms positive pulse,Class_SunSearchControl:SunSensorDriver.switchToBackupPulse,SunSensorDriver,architecture.md,Hardware control waveform.
INF-FR-018,Frequent jetting fault shutdown,State_ModeRegister:Faults.ThrusterShutdown,ThrusterIntervalMonitor/ThrusterIoDriver,architecture.md,Fault safety.
INF-FR-019,Gyro comm fault ladder power-cycle and await ground,State_ModeRegister:Faults.GyroCommRecovery,GyroFaultManager,architecture.md,Fault recovery.
INF-FR-020,Gyro power-on 0xEB92 then control cmd with <5us inter-byte,Class_SunSearchControl:GyroDriver.powerOn/control,GyroDriver/SerialPortDriver,architecture.md,Initialization requirement.
INF-FR-021,Thruster output at 128ms each cycle,Activity_ControlCycle160ms:t==128ms,ThrusterController/ThrusterIoDriver,architecture.md,Actuation timing.
INF-NFR-004,Thruster output completes within 2ms,Class_SunSearchControl:ThrusterController note,ThrusterController,architecture.md,Latency bound.
INF-FR-022,Telemetry every 160ms via 0x88DB with <5us inter-byte,UseCase_SunSearchControl:UC_Tlm,TelemetryPacker/Transmitter,architecture.md;openapi.yaml;sql/telemetry_sample_ddl.sql,Monitoring.
INF-NFR-001,160±2ms cycle duration; alert after 3 violations,Class_SunSearchControl:ControlCycleScheduler note,ControlCycleScheduler,architecture.md,Determinism.
INF-FR-023,Receive remote command each 160ms from 0x88DA; max 1 per cycle,Activity_ControlCycle160ms:Receive remote command,CommandProcessor/SerialPortDriver,architecture.md,Ground interface constraint.
INF-FR-024,Start timer by writing 1 to GTCR0 D0 at 0x8083,Class_SunSearchControl:ControlCycleScheduler,platform/HAL,architecture.md,Register-level requirement.
```

---

## Verification table (Acceptance Criteria)
| Item | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | [x] |
| [ ] Sections A-L included. | [x] |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | [x] (all are `INF-*` and mapped) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | [x] |
| [ ] Representative k8s manifest snippet included. | [x] |
| [ ] SQL DDL / NoSQL models for primary entities included. | [x] |
| [ ] All major components have at least one API contract and a data schema. | [x] (firmware via proto; ground via OpenAPI+SQL) |
| [ ] Assumptions and unresolved questions listed. | [x] |

---

## How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and data schema?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?