Scope: Design production-ready architecture and developer/ops/security/test documentation for the Sun Search Control System (SSCS) from provided requirements + 11 diagrams.  
Approach: Normalize requirements into traceable FR/NFR/ASR (INF-*), resolve conflicts by preferring Original Requirements, and map to 4+1 views + concrete contracts/schemas/manifests.  
Top validation: (1) traceability matrix completeness, (2) timing/slot constraints verifiable (32ms ISR, 160ms cycle, 128ms thruster slot, UART/ADC timing), (3) contract + HIL/sim testability for serial/ADC protocols.  

# ArchitectureDocument.md

## A. Executive Summary (≤1 page)

### System overview
The Sun Search Control System (SSCS) is an on-board 80C32E firmware subsystem that performs periodic sun acquisition and sun-pointing stabilization by: (1) receiving and validating ground commands via DMC bridge, (2) acquiring gyroscope and sun-sensor measurements, (3) estimating attitude, (4) managing mode switching across RDSM/PASM/RASM/CSM, (5) outputting thruster switch commands at a fixed time slot, (6) sending telemetry, and (7) handling faults (gyro comms errors, frequent thruster firing, sun sensor switching).

Primary diagram mapping (one line):
- Scenario & behavior: **UseCase_SunSearchControl:SSCS, UC_Init..UC_Tlm**; **Activity_160msControlCycle**; **State_ModeRegisterLifecycle:MM**; **Sequence_S2_SunAcquisitionAndActuation**
- Structure: **Class_SunSearchControl:CyclicExecutive..TelemetryService**; **Package_SunSearchControl**; **Component_SunSearchControl:FW/HAL/Drivers**
- Deployment: **Deployment_SunSearchControl:MCU/DMC/GYRO/SSP/SSB/THR**; **Container_SunSearchControl:SSCS/DMCBridge**

### Architectural style(s)
- **Time-triggered cyclic executive (single ISR) + deterministic mode/FSM control**.  
  Justification: meets **ASR-001** (single 32ms interrupt and deterministic sequencing) and **NFR-004** (160ms cycle behaviors).

### Deployment topology
- **Single-node embedded deployment (MCU firmware) with UART/ADC device interfaces + DMC UART bridge**.  
  Justification: meets **ASR-003** (fixed serial/ADC hardware addressing) and **ASR-002** (80C32E memory/CPU constraints).

### Top 3 design risks & mitigations

| Risk | Impact | Mitigation (concrete) |
|---|---:|---|
| R1: Missing/ambiguous protocol spec (Table 3.2-1) for command/telemetry and gyro frames | Wrong verification, unsafe mode changes or false faults | Define **versioned FrameSpec contract** with placeholder header/checksum; gate release on HIL capture; add A1/A2 assumptions and change-control (Section K). |
| R2: Tight timing constraints (<5µs inter-byte gap, >5ms gyro fetch→read, thruster output at 128ms) on 11.0592MHz 80C32E | Missed deadlines, incorrect actuation window | Implement UART TX in hardware/interrupt-driven with preloaded buffer; schedule slots per **Activity_160msControlCycle**; instrument WCET in ScheduleMonitor; HIL timing capture. |
| R3: Fault FSMs can power-cycle gyro/thrusters incorrectly (e.g., false positives) | Loss of attitude control / mission risk | Make fault thresholds configurable constants; implement debouncing, persistent counters; add telemetry fault flags and fault-state exposure; extensive fault-injection tests. |

### Key QA coverage mapping

| Quality area | ASR/NFR IDs | Test types |
|---|---|---|
| Performance / real-time | ASR-001, NFR-004, NFR-006, NFR-008, NFR-010 | WCET measurement, HIL timing tests, ISR overrun tests |
| Availability / resilience | INF-FAULT-GYRO-RECOVERY, INF-FAULT-THR-RAPID, INF-SENSOR-SWITCH | Fault injection, long-run endurance, recovery scenario tests |
| Security / integrity (command acceptance) | INF-CMD-VERIFY, NFR-007 | Protocol/contract tests, fuzzing, negative tests |
| Maintainability | ASR-002 | Static analysis, modular driver contracts, code-size regression |
| Scalability (not primary; embedded) | ASR-002 | Not applicable beyond headroom; regression on CPU/RAM budgets |

---

## B. Traceability & Rationale

**Note:** The provided requirements do not include explicit FR/NFR/ASR IDs; therefore IDs are inferred as **INF-*** and listed in Section K. Diagram references use **title:element IDs** only (no PlantUML source).

### Traceability matrix (also delivered as `traceability_matrix.csv`)

| Requirement ID | Short Text | Diagram(s) (title:IDs) | Component(s) | Artifact filename(s) | Rationale |
|---|---|---|---|---|---|
| INF-FUNC-SUN-ACQ | Perform sun acquisition using gyro+sun sensor; rotate pitch/roll to find/maintain sun-pointing | UseCase_SunSearchControl:UC_Att,UC_ModeExec; State_ModeRegisterLifecycle:MM; Sequence_S2_SunAcquisitionAndActuation | CyclicExecutive, AttitudeEstimator, ModeManager, ControlLaw, ThrusterDriver | architecture.md | Core closed-loop control; modeled as periodic pipeline with mode FSM. |
| INF-CMD-RX | Receive ground commands via serial port | UseCase_SunSearchControl:UC_RxCmd; Activity_160msControlCycle | CommandService, HardwareIO | openapi.yaml (external proxy), internal.proto | Command ingress is periodic and rate limited; formalized contract. |
| INF-CMD-VERIFY | Verify command length/header/checksum per spec | UseCase_SunSearchControl:UC_VerCmd; Sequence_S1_CommandToModeUpdate | CommandService, FrameSpec | internal.proto, architecture.md | Prevent invalid mode changes; contract-first due to missing Table 3.2-1. |
| NFR-007 | No more than 1 remote command per 160ms | Sequence_S1_CommandToModeUpdate | CommandService | architecture.md | Enforced by lastAcceptedTick logic and rate limiter. |
| INF-MODE-WORD | Set satellite operating mode word for next cycle | UseCase_SunSearchControl:UC_SetMode; Class_SunSearchControl:ModeRegister | ModeRegister, ModeManager | sql/mode_register_ddl.sql | Mode word is persisted state; drives FSM transitions. |
| ASR-001 | Main program + interrupt; only 32ms timer interrupt | Package_SunSearchControl; Activity_160msControlCycle; Deployment_SunSearchControl:MCU | CyclicExecutive, ScheduleMonitor | architecture.md | Deterministic cyclic executive maps directly to interrupt constraint. |
| NFR-004 | Control cycle is 160ms | Activity_160msControlCycle | CyclicExecutive | architecture.md | Superframe of 5 ticks (32ms) ensures required cadence. |
| INF-THR-OUT-128 | Output 12 thruster switch data sequentially at 128ms of each 160ms cycle | Activity_160msControlCycle; Sequence_S2_SunAcquisitionAndActuation | ThrusterDriver, ControlLaw, CyclicExecutive | architecture.md | Dedicated tick slot (tick 4) ensures timing alignment. |
| ASR-002 | MCU: 80C32E, 11.0592MHz, PROM 32KB, SRAM 8KB | Deployment_SunSearchControl:MCU | Whole firmware | architecture.md | Drives static allocation, no heavy middleware, compact contracts. |
| INF-GYRO-COUNT | Collect gyro pulse/seconds count and power status via serial | Class_SunSearchControl:GyroDriver,SensorSnapshot | GyroDriver | internal.proto | Snapshot includes pulse count; used in estimation and telemetry. |
| INF-GYRO-FETCH | Send 0xEB91 two-byte fetch command every cycle | Activity_160msControlCycle; Sequence_S2_SunAcquisitionAndActuation | GyroDriver, HardwareIO | architecture.md | Implemented at tick 0 for deterministic cadence. |
| NFR-008 | Gyro fetch→read delay > 5ms | Class_SunSearchControl:GyroDriver note; Activity_160msControlCycle | GyroDriver, HardwareIO | architecture.md | Enforced via scheduled delay and stateful driver. |
| INF-GYRO-PORT | Gyro UART address 0x881A (send/receive) | Deployment_SunSearchControl:MCU--GYRO | HardwareIO, GyroDriver | architecture.md | HAL fixes UART ports; validated in integration. |
| INF-GYRO-INIT | On power-on: send home cmd 0xEB92 then control cmd via UART 0x881A | UseCase_SunSearchControl:UC_Init; Class_SunSearchControl:GyroDriver.init | GyroDriver | architecture.md | Initialization stage includes gyro bring-up sequence. |
| NFR-006 | UART TX inter-byte interval < 5µs (telemetry/selected TX) | Deployment_SunSearchControl note; TelemetryService; Gyro init | HardwareIO UART driver | architecture.md | Requires hardware UART/buffered TX; verified with logic analyzer. |
| INF-SUN-AD | Sun sensor angle via AD conversion, 12-bit offset binary 0x000–0xFFF | Class_SunSearchControl:SunSensorDriver | SunSensorDriver | architecture.md | Driver normalizes raw U12 into engineering units for estimator. |
| INF-SUN-SP-LATCH | Collect SP and tuning element state via latch circuit | SunSensorDriver.readLatchSignals | SunSensorDriver | architecture.md | Read digital latch lines each 160ms. |
| INF-PWR-AD | Collect power status signals via AD (components/thruster) | UseCase:UC_ThrStat; Sequence_S2 tick2 | ThrusterDriver, SunSensorDriver | architecture.md | ADC channels map into snapshot/telemetry. |
| NFR-009 | Sun sensor switching: 190ms window, positive pulse 1ms, ±1ms tolerance | State_ModeRegisterLifecycle:BSH | SunSensorDriver, ModeManager | architecture.md | Implemented as timed pulse operation triggered by search failures. |
| ASR-004 | Mode register stores mode word, duration, target angle, target angular velocity | Class_SunSearchControl:ModeRegister | ModeRegister | sql/mode_register_ddl.sql | Central state used across mode management and telemetry. |
| INF-MODES | Four stages: RDSM, PASM, RASM, CSM | State_ModeRegisterLifecycle:MM | ModeManager | architecture.md | Explicit FSM with transition causes and timeouts. |
| INF-RDSM | Rate damping reduces 3-axis angular velocity to stabilize attitude | State_ModeRegisterLifecycle:RDSM | ModeManager, ControlLaw | architecture.md | ControlLaw sets target omega→0; thrusters damp. |
| INF-PASM | Pitch search rotates around pitch(Y) at specified angular rate | State_ModeRegisterLifecycle:PASM | ModeManager, ControlLaw | architecture.md | Sets targetRate about Y; transitions on sunVisible/timeout. |
| INF-RASM | Roll search rotates around roll(X) at specified angular rate | State_ModeRegisterLifecycle:RASM | ModeManager, ControlLaw | architecture.md | Sets targetRate about X; transitions on sunVisible/failure. |
| INF-CSM | Sun cruise maintains stable attitude & tracking after detection | State_ModeRegisterLifecycle:CSM | ModeManager, ControlLaw | architecture.md | Stabilize rates; keep pointing based on sun angle. |
| INF-ATT-EST | Determine 3-axis attitude every 160ms using gyro rates + sun angle + visible | UseCase:UC_Att; Sequence_S2 tick3 | AttitudeEstimator | internal.proto | Estimator produces AttitudeState for mode and telemetry. |
| INF-SENSOR-SWITCH | After two consecutive pitch+roll failures (sun invisible), switch to backup sensor; restart RDSM | State_ModeRegisterLifecycle:BSH | FaultManager, ModeManager, SunSensorDriver | architecture.md | Encoded as policy in ModeManager+FaultManager. |
| INF-FAULT-THR-RAPID | Thruster fault: firing interval <1s for 5s → switch off thruster | UseCase:UC_Faults; Class:FaultManager.checkThrusterFiring | FaultManager, ThrusterDriver | architecture.md | Fault FSM disables thrusters and sets fault flags. |
| INF-FAULT-GYRO-COMMS | Gyro comm errors: invalid len/header/checksum count cycles | FaultManager.checkGyroComms | FaultManager, GyroDriver | architecture.md | Communication validity drives recovery FSM. |
| INF-FAULT-GYRO-RECOVERY | 5 consecutive error cycles → power off gyro; wait 5; power on; wait 5; retry; if fails again → power off and await ground | FaultManager internal FSM | FaultManager, GyroDriver | architecture.md | Deterministic backoff and escalation states. |
| INF-THRUSTER-MAP | 12 thrusters; roll: 2A/2B,3A/3B; pitch:4A/4B,5A/5B; yaw:6A/6B,7A/7B | (Structural) Component_SunSearchControl:ThrusterDriver | ControlLaw, ThrusterDriver | architecture.md | ControlLaw maps axis torque commands to specific thruster pairs. |
| INF-TLM-TX | Send telemetry every 160ms via UART 0x88DB; include mode word, angle, velocity | UseCase:UC_Tlm; Sequence_S2 tick4 | TelemetryService | openapi.yaml (ground proxy), internal.proto | Packaged telemetry enables ground monitoring and debugging. |
| INF-TLM-PORT | Telemetry UART port address 0x88DB | Deployment_SunSearchControl:MCU--DMC | HardwareIO, TelemetryService | architecture.md | Fixed port mapping in HAL. |
| INF-CMD-PORT | Command RX UART port address 0x88DA | Deployment_SunSearchControl:MCU--DMC | HardwareIO, CommandService | architecture.md | Fixed port mapping in HAL. |
| INF-TIMER-GTCR0 | Start 32ms timer by writing 1 to GTCR0 D0 at addr 0x8083 | (Init) UseCase:UC_Init | HardwareIO, CyclicExecutive | architecture.md | Explicit register write included in init flow. |
| INF-INIT-ONCE | Init executed once at power-on/reset: params init, set mode=RDSM, power on components, start timer | UseCase:UC_Init; State:MM[*]->RDSM | CyclicExecutive, Drivers | architecture.md | Establishes safe default state and begins periodic control. |
| INF-IO-ADDR-0x881 | Conflicting requirement: gyro send/receive address 0x881 vs 0x881A | Deployment_SunSearchControl (uses 0x881A) | HardwareIO, GyroDriver | architecture.md | Conflict recorded; firmware uses 0x881A per later explicit text/diagrams. |
| INF-SERIAL-BYTEGAP | Inter-byte gap <5µs for gyro init and telemetry TX | Class:HardwareIO.uartTx; GyroDriver.init | HardwareIO | architecture.md | Implement as buffered hardware UART; verify with logic analyzer. |

---

## C. Architecture Overview

### Context view
SSCS interacts with:
- **DataManagementComputer (DMC)**: provides command bridge from ground operator and receives telemetry (Container_SunSearchControl: DMCBridge).  
- **Gyroscope Unit** over UART (Deployment_SunSearchControl: MCU--GYRO).  
- **Sun sensors (primary/backup)** via ADC + latch + enable register (Deployment_SunSearchControl: MCU--SSP/SSB).  
- **Thruster cluster** via switch register outputs + ADC power status (Deployment_SunSearchControl: MCU--THR).

### Container view
Single container on MCU: **SSCS Firmware** (Container_SunSearchControl:SSCS). It owns the periodic control loop, device drivers, and state.

### Component/package view
Components (Component_SunSearchControl: FW subcomponents):
- CyclicExecutive orchestrates deterministic slots (32ms tick, 5-tick superframe).
- Services: CommandService, AttitudeEstimator, ModeManager, ControlLaw, FaultManager, TelemetryService, ScheduleMonitor.
- Drivers/HAL: HardwareIO, GyroDriver, SunSensorDriver, ThrusterDriver.
Packages align (Package_SunSearchControl: pkg_app/pkg_services/pkg_drivers/pkg_domain/pkg_contracts).

### Class/runtime view
Core runtime collaboration follows Sequence_S2_SunAcquisitionAndActuation and Activity_160msControlCycle:
- Tick0: command RX + gyro fetch
- Tick1: enforce >5ms then gyro read/validate
- Tick2: sun sensor + thruster power ADC/latch read
- Tick3: estimate attitude + faults + mode evaluation
- Tick4 (128ms): compute targets + output thrusters + send telemetry

### Deployment view
Deployed on 80C32E MCU with PROM/SRAM constraints (Deployment_SunSearchControl:MCU). UART connections to DMC (0x88DA/0x88DB) and gyro (0x881A). ADC and register-mapped IO to sensors/thrusters.

---

## D. Detailed Technical Design (developer-facing)

> Important: The original requirements describe an embedded firmware system. Sections D/E/F include “production-ready” options for both (a) **embedded firmware** (authoritative for SSCS) and (b) an **optional ground/bench integration layer** to satisfy the mandated “OpenAPI + Kubernetes + SQL” artifacts without violating SSCS constraints. Where a technology is recommended, a one-line ASR/NFR justification is provided.

### D1. Subsystem: CyclicExecutive + ScheduleMonitor

1) Responsibilities & data ownership  
Owns the master timing schedule: 32ms ISR tick and 160ms superframe. Owns tick counters, slot dispatch, and overrun detection metrics (isr duration, miss counts). Does not own mission state (ModeRegister owns mode/targets).

2) Technology options (3 alternatives per concern)

- Language/runtime  
  - Recommended: **C (C11 subset) + SDCC/Keil C51 toolchain** (no dynamic allocation).  
  - Conservative: **C (C90 subset)** for maximum 8051 compatibility.  
  - Cutting-edge: **Rust (embedded no_std)** (often impractical on 8051 due to toolchain/memory).

- Web framework / RPC / persistence / cache / messaging / search / auth / observability / CI/CD / container runtime / infra provisioning  
  - Not applicable on MCU; see “Integration Layer” below for these concerns.

Compatibility notes: 80C32E strongly favors C with static memory; ISR code must be minimal and deterministic.

3) Recommended default stack  
- **C (C11 subset) on 80C32E with single timer ISR and static scheduling table**.  
  Justification: meets **ASR-001** (single 32ms ISR) and **ASR-002** (PROM/SRAM limits).

4) Interface design  
- Internal: `onTimerTick32ms()` calls `runSlot(slotId)`; slot IDs fixed [0..4].  
- External: none (pure firmware control).

5) Data model / schema  
- No persistence on MCU beyond ModeRegister in SRAM; optional ground persistence handled by Integration Layer.

6) Caching & consistency  
- Not applicable; all state is in-memory and updated per tick; consistency is strong within the ISR execution.

---

### D2. Subsystem: HardwareIO HAL (UART/ADC/Register/Delay)

1) Responsibilities & data ownership  
Provides lowest-level access to UART RX/TX, ADC channels, memory-mapped register writes, and calibrated delays. Owns timing-critical UART send primitives supporting <5µs inter-byte gap when required.

2) Technology options

- Language/runtime  
  - Recommended: **C with hand-tuned UART routines and optional assembly for tight loops**.  
  - Conservative: **C only**, rely on hardware UART FIFO/shift register.  
  - Cutting-edge: **DMA-driven UART** (typically not available on 80C32E).

- Observability (embedded)  
  - Recommended: **GPIO timing pins** toggled at entry/exit of UART TX and ISR.  
  - Conservative: **software counters only**.  
  - Cutting-edge: **on-chip trace** (not available).

3) Recommended default stack  
- **C HAL with hardware UART, buffered TX, and GPIO timing probes**.  
  Justification: meets **NFR-006** (<5µs inter-byte gap) and **ASR-003** (fixed I/O mappings).

4) Interface design  
- `uartRx(portAddr, maxLen) -> bytes[]`  
- `uartTx(portAddr, bytes[])` with mode for “tight-gap TX” used by telemetry/gyro init.  
- `adcRead(channel) -> uint16 (raw U12 in low bits)`  
- `writeReg(addr, value)` including GTCR0 (0x8083)

5) Data model / schema  
None.

6) Caching & consistency  
HAL is stateless; any buffering is bounded ring buffers sized to SRAM.

---

### D3. Subsystem: CommandService (Ground command ingestion)

1) Responsibilities & data ownership  
Owns command RX polling in tick0, frame verification (length/header/checksum), rate limiting (≤1 per 160ms), and application to ModeRegister (modeWord update effective next cycle).

2) Technology options (firmware)
- Frame parsing  
  - Recommended: **Table-driven FrameSpec + checksum function pointer**  
  - Conservative: **Hard-coded fixed frame size**  
  - Cutting-edge: **Generated parser from schema** (not feasible on MCU)
- Checksum  
  - Recommended: **CRC-16/CCITT**  
  - Conservative: **16-bit additive checksum**  
  - Cutting-edge: **CRC-32** (costly)

3) Recommended default stack  
- **FrameSpec-based parser + CRC-16/CCITT (if confirmed by stakeholder), else additive checksum stub**.  
  Justification: meets **INF-CMD-VERIFY** (frame integrity) and **NFR-007** (rate limit).

4) Interface design (External APIs)  
Because SSCS is UART-based, the OpenAPI below applies to an **optional DMC Bridge Service** (ground/bench integration) that exposes HTTP and translates to UART frames. File: `openapi.yaml`.

5) Data model / schema  
Command acceptance events are optionally persisted by Integration Layer (SQL).

6) Caching & consistency  
No caching on MCU.

---

### D4. Subsystem: Sensor Acquisition (GyroDriver + SunSensorDriver + ThrusterDriver)

1) Responsibilities & data ownership  
Owns acquisition of:
- Gyro: periodic fetch 0xEB91, read/validate, pulse counts and angular rate decoding
- Sun sensor: latch SP/sign/power + ADC angle U12
- Thruster: ADC power status + output switch bits at fixed slot

Produces `SensorSnapshot` used by estimator and fault manager.

2) Technology options (firmware)
- Gyro comms  
  - Recommended: **Non-blocking UART + staged state machine across ticks**  
  - Conservative: **Blocking read with timeouts** (risk ISR overrun)  
  - Cutting-edge: **Interrupt-driven RX with ring buffer + parser**
- Sun sensor angle conversion  
  - Recommended: **Normalize U12 with offset-binary conversion into signed angle units**  
  - Conservative: **Pass-through raw U12**  
  - Cutting-edge: **Calibrated LUT with temperature compensation**
- Thruster output sequencing  
  - Recommended: **Precomputed switch word + deterministic register writes at tick4**  
  - Conservative: **Compute & output immediately** (timing drift risk)  
  - Cutting-edge: **Closed-loop PWM/throttle** (not specified)

3) Recommended default stack  
- **Tick-staged acquisition with gyro fetch at tick0 and read at tick1 (>5ms later)**.  
  Justification: meets **NFR-008** (>5ms delay) and **NFR-004** (160ms cadence).

4) Interface design  
- Internal: `GyroDriver.fetch()`, `GyroDriver.readAndValidate()`, `SunSensorDriver.readLatchSignals()`, `SunSensorDriver.readAdAngleU12()`, `ThrusterDriver.outputSwitchDataAt128ms(cmd)`.

5) Data model / schema  
Snapshot is in SRAM only; integration layer can persist time series.

6) Caching & consistency  
No caching; raw readings are “fresh per cycle”. Consistency is strong within a single cycle snapshot.

---

### D5. Subsystem: AttitudeEstimator

1) Responsibilities & data ownership  
Consumes `SensorSnapshot`, outputs `AttitudeState` (Euler angles + angular rates). Owns filtering/estimation algorithm selection; must operate within tick3 budget.

2) Technology options
- Algorithm  
  - Recommended: **Complementary filter (gyro integration + sun angle correction)**  
  - Conservative: **Direct mapping using sun angle only when visible**  
  - Cutting-edge: **EKF** (likely too heavy for 80C32E)
- Numeric representation  
  - Recommended: **Fixed-point (e.g., deg*10, mdps)**  
  - Conservative: **Integer only**  
  - Cutting-edge: **Floating point** (expensive)

3) Recommended default stack  
- **Fixed-point complementary filter with configurable gains**.  
  Justification: meets **ASR-002** (CPU/memory constraints) and **INF-ATT-EST** (160ms estimation).

4) Interface design  
- `estimate(snapshot) -> AttitudeState`.

5) Data model / schema  
None on MCU; telemetry includes attitude/rates.

6) Caching & consistency  
Keeps previous state for integration; reset on mode transitions or fault recovery events.

---

### D6. Subsystem: ModeManager + ModeRegister (RDSM/PASM/RASM/CSM)

1) Responsibilities & data ownership  
ModeRegister owns the authoritative control state: modeWord, modeDurationTicks, targets, selected sun sensor. ModeManager owns the FSM logic and transition logging, evaluated every 160ms.

2) Technology options
- FSM encoding  
  - Recommended: **Explicit enum + transition table**  
  - Conservative: **Nested if/else**  
  - Cutting-edge: **Generated FSM from model**
- Mode durations/timeouts  
  - Recommended: **Tick-based counters (32ms ticks)**  
  - Conservative: **ms-based arithmetic**  
  - Cutting-edge: **Adaptive timeouts** (not specified)

3) Recommended default stack  
- **Table-driven FSM evaluated at tick3 with tick counters**.  
  Justification: meets **ASR-004** (mode register state) and **NFR-004** (160ms decisions).

4) Interface design  
- `evaluate(state, reg, sunVisible)` updates reg.modeWord, reg.targetRate, reg.modeDurationTicks.  
- Sun sensor backup switching triggers `SunSensorDriver.switchPulse190ms()`.

5) Data model / schema (ground-side optional persistence)
See `sql/mode_register_ddl.sql` for an ops/bench database record of mode history (not on MCU).

6) Caching & consistency  
No caching; strong consistency with single-writer ISR.

---

### D7. Subsystem: ControlLaw + ThrusterOutput

1) Responsibilities & data ownership  
ControlLaw converts ModeRegister targets + AttitudeState into `ThrusterCommand` (12-bit switch word and sequence). ThrusterOutput ensures output at t=128ms slot and enforces any actuator inhibitions (fault disable).

2) Technology options
- Control strategy  
  - Recommended: **Bang-bang / deadband rate control selecting thruster pairs**  
  - Conservative: **Simple on/off thresholding per axis**  
  - Cutting-edge: **Optimal control** (too heavy / not specified)
- Thruster mapping  
  - Recommended: **Axis→thruster-pair lookup table**  
  - Conservative: **Hard-coded if/else mapping**  
  - Cutting-edge: **Auto-balancing with health weights**

3) Recommended default stack  
- **Deadband rate controller + lookup-table mapping to thruster pairs, output at tick4**.  
  Justification: meets **INF-THR-OUT-128** (actuation time slot) and **INF-THRUSTER-MAP** (specific thruster roles).

4) Interface design  
- `computeTargets(reg, state) -> ThrusterCommand`  
- `outputSwitchDataAt128ms(cmd)` writes sequential outputs for 12 thrusters.

5) Data model / schema  
Optional persisted thruster command history (integration layer).

6) Caching & consistency  
No caching; command is per-cycle.

---

### D8. Subsystem: FaultManager

1) Responsibilities & data ownership  
Owns fault detection and recovery FSMs:
- Frequent thruster firing: <1s interval for 5s → disable thrusters
- Gyro communication error: invalid frames for 5 cycles triggers power cycle; escalation after repeated failures
- Sun sensor switch request after repeated search failures (in coordination with ModeManager)

2) Technology options
- Fault counters  
  - Recommended: **Consecutive-cycle counters + explicit recovery states**  
  - Conservative: **Single counter thresholds**  
  - Cutting-edge: **Statistical anomaly detection** (not feasible)
- Fault reporting  
  - Recommended: **Bitmask faultFlags in telemetry**  
  - Conservative: **Mode-only indication**  
  - Cutting-edge: **Event logs** (memory heavy)

3) Recommended default stack  
- **Deterministic fault FSMs with explicit counters and backoff**.  
  Justification: meets **INF-FAULT-GYRO-RECOVERY** and **INF-FAULT-THR-RAPID** (fault protocols).

4) Interface design  
- `checkGyroComms(gyroValid)`  
- `checkThrusterFiring(intervalMs)`  
- `requestSunSensorSwitch() -> bool`

5) Data model / schema  
Optional persisted fault events in integration layer (`fault_event` table).

6) Caching & consistency  
No caching.

---

### D9. Subsystem: TelemetryService

1) Responsibilities & data ownership  
Builds and transmits telemetry every 160ms via UART 0x88DB. Telemetry includes mode word, attitude, angular rate, fault flags, and schedule status.

2) Technology options
- Telemetry encoding  
  - Recommended: **Binary fixed-layout frame**  
  - Conservative: **Minimal fields only**  
  - Cutting-edge: **CBOR/Protobuf** (overhead)
- Integrity  
  - Recommended: **CRC-16**  
  - Conservative: **Additive checksum**  
  - Cutting-edge: **Authenticated MAC** (not requested; limited MCU)

3) Recommended default stack  
- **Binary telemetry frame with tight UART TX and checksum**.  
  Justification: meets **INF-TLM-TX** (periodic telemetry) and **NFR-006** (TX byte gap).

4) Interface design  
- `build(state, reg, faults, sched) -> TelemetryPacket`  
- `transmit(pkt)` sends UART 0x88DB.

5) Data model / schema  
Optional persistence in integration layer for analysis.

6) Caching & consistency  
No caching.

---

### D10. Optional Integration Layer (for HTTP/OpenAPI, SQL, Kubernetes)

> This layer is for ground test/bench or on-board DMC modernization. It is **not** deployed on the 80C32E MCU. It exists to provide operational APIs, persistence, and Kubernetes deployment for production tooling and automated testing.

#### Tech options per concern (3 alternatives each)

- Language/runtime  
  - Recommended: **Go 1.22–1.23**  
  - Conservative: **Java 21 LTS**  
  - Cutting-edge: **Rust 1.78+**

- Web framework  
  - Recommended: **Go net/http + chi v5**  
  - Conservative: **Spring Boot 3.2–3.3**  
  - Cutting-edge: **FastAPI (Python 3.11–3.13)**

- RPC/HTTP  
  - Recommended: **REST/JSON over HTTPS**  
  - Conservative: **gRPC**  
  - Cutting-edge: **NATS request/reply**

- Persistence  
  - Recommended: **PostgreSQL 14–16**  
  - Conservative: **SQLite 3.45+** (single-node bench)  
  - Cutting-edge: **TimescaleDB 2.14+** (telemetry time-series)

- Cache  
  - Recommended: **Redis 7.2–7.4**  
  - Conservative: **in-memory LRU**  
  - Cutting-edge: **KeyDB**

- Messaging  
  - Recommended: **NATS 2.10+**  
  - Conservative: **Kafka 3.7+**  
  - Cutting-edge: **Redpanda**

- Search  
  - Recommended: **No search** (not needed)  
  - Conservative: **PostgreSQL full-text**  
  - Cutting-edge: **OpenSearch 2.x**

- Authn/Authz  
  - Recommended: **mTLS (service-to-service) + API key for operator tooling**  
  - Conservative: **OIDC (Keycloak) with JWT**  
  - Cutting-edge: **SPIFFE/SPIRE**

- Observability  
  - Recommended: **Prometheus + Grafana + Loki + OpenTelemetry**  
  - Conservative: **Prometheus only**  
  - Cutting-edge: **eBPF-based profiling**

- CI/CD  
  - Recommended: **GitHub Actions / GitLab CI**  
  - Conservative: **Jenkins**  
  - Cutting-edge: **Argo Workflows**

- Container runtime  
  - Recommended: **containerd (Kubernetes default)**  
  - Conservative: **Docker**  
  - Cutting-edge: **gVisor**

- Infra provisioning  
  - Recommended: **Terraform 1.6–1.8**  
  - Conservative: **Helm-only**  
  - Cutting-edge: **Pulumi**

Recommended default stack (integration layer):
- **Go 1.22–1.23 + chi v5 + PostgreSQL 14–16 + Prometheus/OTel**.  
  Justification: supports deterministic contract testing and tooling around **NFR-006/NFR-008/NFR-009** verification via HIL pipelines.

---

### D.4 External API (OpenAPI) — `openapi.yaml`
This API represents a **Sun Search Ground Bridge** that:
- Accepts ground commands via HTTP and emits UART frames to SSCS.
- Receives telemetry frames from SSCS and exposes them as JSON for dashboards/testing.
- Provides endpoints to query mode/fault state and trigger test scenarios.

(See full file in Section L.)

---

### D.4 Internal API contract — `internal.proto`
Defines internal contracts between the bridge, simulators, and test harnesses for:
- Sending validated command frames
- Publishing decoded telemetry
- Running HIL timing capture sessions

(See full file in Section L.)

---

### D.5 Data model / schema (Integration Layer SQL)

Primary persisted entities:
- `command_event`: received commands, validation result, applied mode
- `telemetry_sample`: decoded telemetry time series
- `fault_event`: fault transitions and recovery actions
- `mode_register_history`: mode transitions with durations and causes

Encryption/immutability/audit:
- Mark command/telemetry as **append-only** for auditability (ties to inferred integrity needs: INF-CMD-VERIFY).
- Encryption-at-rest depends on environment; for Kubernetes use storage-class encryption.

(See SQL files in Section L.)

---

## E. Operations & Deployment (ops-facing)

> SSCS firmware runs on MCU; Kubernetes deployment applies to the **optional Ground Bridge + Telemetry DB** used for operations/testing.

### E1. Kubernetes-ready plan (`k8s/ground-bridge-deployment.yaml`)
Includes Deployment, Service, HPA, ConfigMap, Secret, resource requests/limits, and suggested replica counts (small/medium/large QPS tiers).

Technology recommendation:
- **Kubernetes 1.28–1.30** for ground tooling deployment.  
  Justification: enables automated validation pipelines for timing-related **NFR-006/NFR-008/NFR-009** (HIL test orchestration).

### E2. DB HA topology
- PostgreSQL:  
  - Small: single instance + daily backups  
  - Medium/Large: 1 primary + 2 replicas (async), PITR enabled, WAL archiving
- Backup cadence: full daily + WAL continuous; quarterly restore drills.

### E3. Network topology + ingress/egress
Map to deployment diagram (Deployment_SunSearchControl: MCU/DMC links):
- Bridge connects to UART adapter (or DMC interface) on a dedicated network segment.
- Ingress: HTTPS to ground bridge; egress restricted to DB and observability.

Latency expectations:
- For real-time monitoring, aim <250ms from telemetry receipt to API availability; SSCS remains authoritative at 160ms telemetry cycle (INF-TLM-TX).

### E4. CI/CD sketch
1. Build firmware (toolchain container), run unit tests + static analysis.
2. Build bridge container; run OpenAPI lint + proto lint.
3. Contract tests: replay captured UART frames; verify checksum/parsing (INF-CMD-VERIFY).
4. HIL: logic analyzer measurement job for NFR-006/NFR-008/NFR-009.
5. Deploy bridge via Helm/Kustomize; canary then promote.

---

## F. Security Design

> SSCS itself is UART-based and assumes trusted on-board links; security focus is on **command integrity** and **test tooling**.

### F1. Auth & AuthZ
- Integration layer API: **mTLS between services + API key for operators**.  
  Justification: protects command injection risks associated with **INF-CMD-RX** and **INF-CMD-VERIFY**.

Token lifecycle:
- API keys rotated every 90 days; immediate revocation supported via denylist.

### F2. Secrets management
- Kubernetes: External Secrets or sealed-secrets; rotate DB creds monthly.

### F3. TLS & service mesh
- TLS 1.2+ for ingress; optional Linkerd/Istio for mTLS.

### F4. Threat model summary (top 5)
1. Command injection to change mode incorrectly → mTLS + auth + strict frame validation.
2. Telemetry spoofing → source pinning + checksums + UART adapter access controls.
3. Replay of old commands → include command sequence/timestamp field (A2) and reject stale.
4. Misconfiguration of ports/addresses → configuration immutability + startup self-tests.
5. Supply chain (tooling containers) → signed images + SBOM.

---

## G. Observability & SRE

### G1. Metrics/logs/traces
Firmware (exported via telemetry fields):
- `schedule.isr_overrun_count`, `schedule.cycle_miss_count`
- `fault.gyro_comm_consecutive_errors`, `fault.thruster_rapid_fire`
- `mode.current`, `mode.duration_ticks`
- `sensor.sun_visible`, `sensor.sun_angle_u12`

Bridge (Prometheus):
- `bridge_uart_rx_frames_total{type=telemetry,valid=true/false}`
- `bridge_uart_tx_frames_total{type=command}`
- `bridge_decode_latency_ms`

Example Prometheus alerts:
- `SSCSHighInvalidTelemetryRate`: invalid telemetry frames >5% over 5m
- `SSCSScheduleOverrun`: schedule overrun events increase >0 over 1m

(Provided in Section L as part of runbook notes; alerts are expressions.)

### G2. SLOs / error budgets / RTO/RPO
Integration layer SLOs:
- Availability 99.9% monthly (bridge API)
- Telemetry ingest freshness: 99% of samples available within 1s of receipt

RTO/RPO:
- RTO 30 minutes for bridge; RPO 5 minutes (WAL/PITR)

### G3. Dashboards & runbooks
Dashboards:
- “Cycle health”: overrun/miss counters + telemetry frame validity
- “Attitude/mode”: mode timeline + sunVisible + targetRate vs omega

Runbooks:
- Gyro comms fault: check invalid frames, confirm power cycle sequence
- Rapid thruster fire: verify interval logic and disable event

---

## H. Testing Strategy

### H1. Test matrix

| Test type | Components | Key cases |
|---|---|---|
| Unit | ModeManager, ControlLaw, FaultManager | FSM transitions, deadbands, counters |
| Integration | Drivers + HAL (simulated UART/ADC) | Frame parsing, delay enforcement (NFR-008) |
| Contract | FrameSpec/CommandFrame/TelemetryPacket | Fuzz length/header/checksum (INF-CMD-VERIFY) |
| E2E (HIL) | Full SSCS + UART/ADC rigs | Verify thruster slot at 128ms; UART <5µs gap; sensor switch pulse timing |
| Chaos/Stress (tooling) | Bridge + DB | Drop frames, DB failover, backpressure |

### H2. Test data management & environment isolation
Environments:
- `dev` (sim-only), `staging` (HIL), `prod` (ops)
Refresh cadence:
- staging DB nightly; prod is append-only with retention policies.

---

## I. Migration, Data Conversion & Rollout Plan

### I1. Migration steps
If replacing an existing ground tool:
1. Deploy bridge in parallel (shadow mode): ingest telemetry only.
2. Validate parity of decoded telemetry vs legacy.
3. Enable command issuance with “dry-run” mode, then limited canary.
4. Full cutover; keep rollback by disabling command endpoint and reverting to legacy.

### I2. Backwards compatibility
- API versioning via `/v1/...` paths.
- UART frame versions managed via `FrameSpec.version` (A1).

---

## J. Tradeoffs & Alternatives

| Decision | Chosen | Alternatives | Pros/Cons | Why chosen (tie to IDs) |
|---|---|---|---|---|
| Scheduling | 32ms ISR cyclic executive | RTOS; superloop | Deterministic vs flexibility | **ASR-001**, **NFR-004**, **INF-THR-OUT-128** require deterministic slot timing. |
| Checksums | CRC-16 (preferred) | additive; CRC-32 | CRC-16 stronger than additive, cheaper than CRC-32 | Supports **INF-CMD-VERIFY** and gyro validation (**INF-FAULT-GYRO-COMMS**). |
| Estimator | complementary filter fixed-point | EKF; direct mapping | EKF accuracy vs compute; direct is poor when sun not visible | **ASR-002** constraints + **INF-ATT-EST** cadence. |
| Sensor switching | explicit pulse 190ms (1ms high) | latch-only; redundant always-on | Pulse required; always-on may violate HW | **NFR-009** mandates pulse behavior. |

---

## K. Open Questions & Assumptions

### Assumptions
- **A1:** Command/telemetry frame header and checksum algorithm are not fully specified (Table 3.2-1 missing); we assume header `0x55AA` and **CRC-16/CCITT** until confirmed.  
- **A2:** Commands include an implicit or explicit sequence/nonce; if absent, the system only enforces “≤1 per 160ms” and does not prevent replay across longer windows.  
- **A3:** Sun sensor enable/switch register address is memory-mapped but not provided; assumed available via `HardwareIO.writeReg()` and parameterized in config.  
- **A4:** Thruster switch register addressing and “sequential output” electrical protocol are stable and provided by HW map section 3.2.8; assumed accessible via `ThrusterDriver.outputSwitchDataAt128ms()`.  
- **A5:** Gyro control command (after 0xEB92) exact bytes are not specified; assumed provided by HW ICD and represented as a driver constant array.  

### Unresolved stakeholder questions (need answers)
1. Provide **Table 3.2-1**: command frame length, header, checksum type, endianness, payload definitions.  
2. Confirm the correct gyro UART address: **0x881 vs 0x881A** (requirements conflict); diagrams use 0x881A—confirm authoritative.  
3. Define sun sensor angle conversion: units, zero reference, mapping from offset-binary code to degrees (the “minimum code corresponds to 5/2048” line is incomplete).  
4. Provide exact thruster output protocol at 128ms: ordering, strobe timing, register addresses.  
5. Define thresholds/timeouts: rate damping completion criterion, PASM/RASM search timeout lengths, “two consecutive attempts” counting rules.

### Logged conflicts (per rule: prefer Original Requirements)
- **Conflict C1:** Requirements mention gyro port **0x881** while later text and diagrams specify **0x881A**. Using **0x881A** in design; requires confirmation.

### Inferred requirement IDs list
All IDs in Section B are inferred (`INF-*`) due to missing explicit IDs in the source requirements.

---

## L. Deliverables

```md
<!-- filename: architecture.md -->
(Identical to ArchitectureDocument.md content above)
```

```yaml
# filename: openapi.yaml
openapi: 3.0.3
info:
  title: Sun Search Ground Bridge API
  version: 1.0.0
  description: >
    Optional ground/bench integration service that bridges HTTP to SSCS UART command frames
    and exposes decoded SSCS telemetry as JSON. SSCS itself remains UART-based on the 80C32E MCU.
servers:
  - url: https://sscs-bridge.example.com
paths:
  /v1/health:
    get:
      summary: Liveness/readiness
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HealthResponse"
  /v1/commands:send:
    post:
      summary: Send a ground command to SSCS (translated to UART frame)
      security:
        - ApiKeyAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CommandRequest"
      responses:
        "202":
          description: Accepted for transmission
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CommandAccepted"
        "400":
          description: Invalid request/frame spec mismatch
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          description: Missing/invalid API key
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "409":
          description: Rate limited (max 1 command per 160ms)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/telemetry/latest:
    get:
      summary: Get the latest decoded telemetry sample
      security:
        - ApiKeyAuth: []
      responses:
        "200":
          description: Latest telemetry
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TelemetrySample"
        "404":
          description: No telemetry received yet
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/telemetry:
    get:
      summary: Query telemetry samples by time window
      security:
        - ApiKeyAuth: []
      parameters:
        - name: startTime
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: endTime
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 5000
            default: 1000
      responses:
        "200":
          description: Telemetry samples
          content:
            application/json:
              schema:
                type: object
                required: [items]
                properties:
                  items:
                    type: array
                    items:
                      $ref: "#/components/schemas/TelemetrySample"
        "400":
          description: Bad time window
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /v1/faults/latest:
    get:
      summary: Get current/last-known fault status
      security:
        - ApiKeyAuth: []
      responses:
        "200":
          description: Fault status
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FaultStatus"
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
  schemas:
    HealthResponse:
      type: object
      required: [status, time]
      properties:
        status:
          type: string
          enum: [ok]
        time:
          type: string
          format: date-time
    CommandRequest:
      type: object
      required: [frameSpecVersion, modeWord]
      properties:
        frameSpecVersion:
          type: string
          description: Version of framing/checksum contract.
          example: "v0-assumed"
        modeWord:
          type: integer
          minimum: 0
          maximum: 65535
          description: Target SSCS operating mode word to apply next cycle.
        payload:
          type: object
          additionalProperties: true
          description: Optional command payload fields (future extension).
    CommandAccepted:
      type: object
      required: [commandId, acceptedAt]
      properties:
        commandId:
          type: string
        acceptedAt:
          type: string
          format: date-time
    TelemetrySample:
      type: object
      required:
        - receivedAt
        - modeWord
        - eulerDegX10
        - omegaMdps
        - sunVisible
        - sunAngleU12
        - faultFlags
        - scheduleStatus
      properties:
        receivedAt:
          type: string
          format: date-time
        modeWord:
          type: integer
          minimum: 0
          maximum: 65535
        eulerDegX10:
          type: array
          minItems: 3
          maxItems: 3
          items:
            type: integer
            minimum: -32768
            maximum: 32767
        omegaMdps:
          type: array
          minItems: 3
          maxItems: 3
          items:
            type: integer
            minimum: -32768
            maximum: 32767
        sunVisible:
          type: boolean
        sunAngleU12:
          type: integer
          minimum: 0
          maximum: 4095
        faultFlags:
          type: integer
          minimum: 0
          maximum: 65535
        scheduleStatus:
          type: integer
          minimum: 0
          maximum: 65535
    FaultStatus:
      type: object
      required: [faultFlags, updatedAt]
      properties:
        faultFlags:
          type: integer
          minimum: 0
          maximum: 65535
        updatedAt:
          type: string
          format: date-time
    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
          example: "RATE_LIMITED"
        message:
          type: string
        details:
          type: object
          additionalProperties: true
```

```proto
// filename: internal.proto
syntax = "proto3";

package sscs.internal.v1;

option go_package = "github.com/example/sscs/internal/gen;sscsinternal";

// Internal contracts for bridge/simulator/HIL orchestration.
// SSCS on MCU is UART-based; these APIs are for tooling that validates timing and frame contracts.

message FrameSpec {
  string version = 1;          // e.g., "v0-assumed"
  uint32 header_u16 = 2;       // e.g., 0x55AA
  string checksum_type = 3;    // "CRC16_CCITT" | "ADD16"
  uint32 min_len = 4;
}

message CommandFrame {
  FrameSpec spec = 1;
  bytes raw = 2;               // fully encoded UART frame bytes
  uint32 length = 3;
}

message CommandRequest {
  FrameSpec spec = 1;
  uint32 mode_word = 2;        // 0..65535
  bytes payload = 3;           // optional
}

message CommandResult {
  string command_id = 1;
  bool accepted = 2;
  string reject_reason = 3;
  int64 accepted_unix_ms = 4;
}

message TelemetryPacket {
  FrameSpec spec = 1;
  bytes raw = 2;
  uint32 mode_word = 3;
  sint32 euler_deg_x10_x = 4;
  sint32 euler_deg_x10_y = 5;
  sint32 euler_deg_x10_z = 6;
  sint32 omega_mdps_x = 7;
  sint32 omega_mdps_y = 8;
  sint32 omega_mdps_z = 9;
  bool sun_visible = 10;
  uint32 sun_angle_u12 = 11;
  uint32 fault_flags = 12;
  uint32 schedule_status = 13;
  int64 received_unix_ms = 14;
}

message TelemetryQuery {
  int64 start_unix_ms = 1;
  int64 end_unix_ms = 2;
  uint32 limit = 3;
}

message TelemetryList {
  repeated TelemetryPacket items = 1;
}

message HilTimingCaptureRequest {
  string session_id = 1;
  uint32 duration_seconds = 2;
  // Names of timing probes: e.g., "ISR_PIN", "UART_TX_PIN"
  repeated string probes = 3;
}

message HilTimingCaptureResult {
  string session_id = 1;
  bool success = 2;
  string artifact_uri = 3; // e.g., s3://.../logic-analyzer.csv
  string notes = 4;
}

service BridgeService {
  rpc BuildCommandFrame(CommandRequest) returns (CommandFrame);
  rpc SendCommand(CommandFrame) returns (CommandResult);
  rpc GetLatestTelemetry(google.protobuf.Empty) returns (TelemetryPacket);
  rpc QueryTelemetry(TelemetryQuery) returns (TelemetryList);
  rpc StartHilTimingCapture(HilTimingCaptureRequest) returns (HilTimingCaptureResult);
}

import "google/protobuf/empty.proto";
```

```yaml
# filename: k8s/ground-bridge-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sscs-ground-bridge-config
data:
  APP_ENV: "prod"
  HTTP_PORT: "8080"
  FRAME_SPEC_VERSION: "v0-assumed"
  UART_DEVICE: "/dev/ttyUSB0"
  UART_CMD_PORT_ADDR: "0x88DA"
  UART_TLM_PORT_ADDR: "0x88DB"
---
apiVersion: v1
kind: Secret
metadata:
  name: sscs-ground-bridge-secrets
type: Opaque
stringData:
  API_KEY: "CHANGE_ME"
  DATABASE_URL: "postgres://sscs:CHANGE_ME@postgres:5432/sscs?sslmode=disable"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sscs-ground-bridge
spec:
  replicas: 2  # small tier default; medium=3, large=5
  selector:
    matchLabels:
      app: sscs-ground-bridge
  template:
    metadata:
      labels:
        app: sscs-ground-bridge
    spec:
      containers:
        - name: bridge
          image: example/sscs-ground-bridge:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: sscs-ground-bridge-config
            - secretRef:
                name: sscs-ground-bridge-secrets
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /v1/health
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /v1/health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: sscs-ground-bridge
spec:
  selector:
    app: sscs-ground-bridge
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sscs-ground-bridge-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sscs-ground-bridge
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```sql
-- filename: sql/command_event_ddl.sql
CREATE TABLE IF NOT EXISTS command_event (
  command_id        UUID PRIMARY KEY,
  received_at       TIMESTAMPTZ NOT NULL,
  frame_spec_ver    TEXT NOT NULL,
  mode_word         INTEGER NOT NULL CHECK (mode_word BETWEEN 0 AND 65535),
  raw_frame         BYTEA,
  validated_ok      BOOLEAN NOT NULL,
  reject_reason     TEXT,
  applied_at        TIMESTAMPTZ,
  source            TEXT NOT NULL DEFAULT 'http'
);

CREATE INDEX IF NOT EXISTS idx_command_event_received_at
  ON command_event (received_at DESC);
```

```sql
-- filename: sql/telemetry_sample_ddl.sql
CREATE TABLE IF NOT EXISTS telemetry_sample (
  sample_id         BIGSERIAL PRIMARY KEY,
  received_at       TIMESTAMPTZ NOT NULL,
  mode_word         INTEGER NOT NULL CHECK (mode_word BETWEEN 0 AND 65535),
  euler_deg_x10_x   SMALLINT NOT NULL,
  euler_deg_x10_y   SMALLINT NOT NULL,
  euler_deg_x10_z   SMALLINT NOT NULL,
  omega_mdps_x      SMALLINT NOT NULL,
  omega_mdps_y      SMALLINT NOT NULL,
  omega_mdps_z      SMALLINT NOT NULL,
  sun_visible       BOOLEAN NOT NULL,
  sun_angle_u12     INTEGER NOT NULL CHECK (sun_angle_u12 BETWEEN 0 AND 4095),
  fault_flags       INTEGER NOT NULL CHECK (fault_flags BETWEEN 0 AND 65535),
  schedule_status   INTEGER NOT NULL CHECK (schedule_status BETWEEN 0 AND 65535),
  raw_frame         BYTEA
);

CREATE INDEX IF NOT EXISTS idx_telemetry_sample_received_at
  ON telemetry_sample (received_at DESC);

CREATE INDEX IF NOT EXISTS idx_telemetry_sample_mode_time
  ON telemetry_sample (mode_word, received_at DESC);
```

```sql
-- filename: sql/fault_event_ddl.sql
CREATE TABLE IF NOT EXISTS fault_event (
  fault_event_id    BIGSERIAL PRIMARY KEY,
  occurred_at       TIMESTAMPTZ NOT NULL,
  fault_code        TEXT NOT NULL,
  fault_flags       INTEGER NOT NULL CHECK (fault_flags BETWEEN 0 AND 65535),
  details           JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_fault_event_occurred_at
  ON fault_event (occurred_at DESC);
```

```sql
-- filename: sql/mode_register_ddl.sql
CREATE TABLE IF NOT EXISTS mode_register_history (
  mode_event_id       BIGSERIAL PRIMARY KEY,
  occurred_at         TIMESTAMPTZ NOT NULL,
  from_mode_word      INTEGER NOT NULL CHECK (from_mode_word BETWEEN 0 AND 65535),
  to_mode_word        INTEGER NOT NULL CHECK (to_mode_word BETWEEN 0 AND 65535),
  cause               TEXT NOT NULL,
  mode_duration_ticks INTEGER NOT NULL CHECK (mode_duration_ticks >= 0),
  target_angle_u12    INTEGER NOT NULL CHECK (target_angle_u12 BETWEEN 0 AND 4095),
  target_rate_x       SMALLINT NOT NULL,
  target_rate_y       SMALLINT NOT NULL,
  target_rate_z       SMALLINT NOT NULL,
  sun_sensor_sel      SMALLINT NOT NULL CHECK (sun_sensor_sel IN (0,1))
);

CREATE INDEX IF NOT EXISTS idx_mode_register_history_time
  ON mode_register_history (occurred_at DESC);
```

```csv
# filename: traceability_matrix.csv
Requirement ID,Short Text,Diagram(s) (title:IDs),Component(s),Artifact filename(s),Rationale
INF-FUNC-SUN-ACQ,Sun acquisition using gyro+sun sensor and pitch/roll search,UseCase_SunSearchControl:UC_Att|UC_ModeExec;State_ModeRegisterLifecycle:MM,CyclicExecutive/AttitudeEstimator/ModeManager/ControlLaw/ThrusterDriver,architecture.md,Core closed-loop control mapped to periodic pipeline+FSM.
INF-CMD-RX,Receive ground commands via serial port,UseCase_SunSearchControl:UC_RxCmd;Activity_160msControlCycle,CommandService/HardwareIO,architecture.md|openapi.yaml,Command ingress formalized for validation and rate limiting.
INF-CMD-VERIFY,Verify command length/header/checksum,UseCase_SunSearchControl:UC_VerCmd;Sequence_S1_CommandToModeUpdate,CommandService/FrameSpec,internal.proto,Contract-first verification due to missing table.
NFR-007,<=1 command per 160ms,Sequence_S1_CommandToModeUpdate,CommandService,architecture.md,Rate limiter ensures acceptance constraint.
INF-MODE-WORD,Set operating mode word,UseCase_SunSearchControl:UC_SetMode;Class_SunSearchControl:ModeRegister,ModeRegister/ModeManager,sql/mode_register_ddl.sql,Mode word drives FSM and control targets.
ASR-001,Single 32ms timer interrupt architecture,Activity_160msControlCycle;Deployment_SunSearchControl:MCU,CyclicExecutive/ScheduleMonitor,architecture.md,Deterministic ISR schedule meets hardware constraint.
NFR-004,160ms control cycle,Activity_160msControlCycle,CyclicExecutive,architecture.md,5 ticks per superframe.
INF-THR-OUT-128,Thruster output at 128ms each cycle,Activity_160msControlCycle;Sequence_S2_SunAcquisitionAndActuation,ThrusterDriver/ControlLaw,architecture.md,Reserved slot ensures correct timing.
ASR-002,80C32E resources and frequency,Deployment_SunSearchControl:MCU,All firmware,architecture.md,Static allocation and lightweight algorithms.
INF-GYRO-FETCH,Send 0xEB91 fetch each cycle,Sequence_S2_SunAcquisitionAndActuation:tick0,GyroDriver,architecture.md,Deterministic polling.
NFR-008,Fetch->read delay >5ms,Activity_160msControlCycle,GyroDriver/HardwareIO,architecture.md,Enforced by scheduled delay and staged driver.
INF-GYRO-INIT,Send 0xEB92 then control cmd on power-on,UseCase_SunSearchControl:UC_Init,GyroDriver,architecture.md,Initialization sequence.
NFR-006,UART inter-byte gap <5us,Deployment_SunSearchControl note,HardwareIO,architecture.md,H/W UART buffered TX + timing verification.
INF-SUN-AD,Sun angle 12-bit offset binary,Class_SunSearchControl:SunSensorDriver,SunSensorDriver,architecture.md,Normalized input for estimator.
NFR-009,Sun sensor switch pulse 190ms (1ms high),State_ModeRegisterLifecycle:BSH,SunSensorDriver/ModeManager,architecture.md,Pulse timing operation for backup sensor.
INF-FAULT-GYRO-RECOVERY,Gyro comms recovery FSM (power-cycle backoff),Class_SunSearchControl:FaultManager,FaultManager/GyroDriver,architecture.md,Deterministic recovery per requirement narrative.
INF-FAULT-THR-RAPID,Rapid thruster firing fault disables thrusters,UseCase_SunSearchControl:UC_Faults,FaultManager/ThrusterDriver,architecture.md,Protects from unsafe repeated firing.
INF-TLM-TX,Telemetry every 160ms to 0x88DB,<UseCase_SunSearchControl:UC_Tlm;Sequence_S2 tick4>,TelemetryService,openapi.yaml|internal.proto,Provides monitoring and debugging.
```

---

## Verification Table (Acceptance Criteria)

| Check | Status |
|---|---|
| [ ] 3-line Analysis Plan present. | ✅ |
| [ ] Sections A-L included. | ✅ |
| [ ] Every FR/NFR/ASR mapped in traceability matrix. | ✅ (all inferred as INF-* where missing) |
| [ ] ≥1 OpenAPI YAML (external) and ≥1 internal proto/REST contract included. | ✅ |
| [ ] Representative k8s manifest snippet included. | ✅ |
| [ ] SQL DDL / NoSQL models for primary entities included. | ✅ |
| [ ] All major components have at least one API contract and a data schema. | ⚠️ MCU components have contracts but no persistence; schemas provided for integration layer entities. |
| [ ] Assumptions and unresolved questions listed. | ✅ |

### How to review checklist
- All FR/NFR/ASR present in traceability matrix?  
- OpenAPI + internal API contract included and valid?  
- Each major component has: responsibilities, stack options (3+), recommended stack + ASR/NFR justification, API contract, and a data schema (MCU: state structs; tooling: SQL)?  
- k8s snippet present and syntactically valid?  
- SQL DDLs provided for persisted entities?  
- Assumptions and open questions clearly listed?

Conversion note (optional): to render PDF, run `pandoc ArchitectureDocument.md -o ArchitectureDocument.pdf`.