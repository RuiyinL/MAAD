# Functional Requirements Results:
[FR-001]: Sun Acquisition
**Description**: The system collects measurement data from gyroscopes and sun sensors to determine current satellite attitude. 
**Rationale:** This requirement describes a specific behavior of the system, which is to determine the satellite's attitude.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-002]: Satellite Attitude Control
**Description**: The system controls rotation about pitch/roll axes to achieve sun-pointing attitude. 
**Rationale:** This requirement describes a function of the system, which is to control the satellite's attitude.
**Dependencies** / **Conflicts**:
- **Depends on:** FR-001
- **Conflicts with:** None
---

[FR-003]: Ground Command Reception
**Description**: The system accepts ground commands on serial port 0x88DA with the frame: Header (1 byte = 0xAA), Length (1 byte), Payload (N bytes), Checksum (1 byte, sum mod 256). Acceptance: Message is processed only if header==0xAA, length matches, checksum correct, and HMAC-SHA256 authentication against configured KMS key passes.
**Rationale:** This requirement describes a function of the system, which is to receive and process ground commands.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-004]: Sun Sensor Data Acquisition
**Description**: The system acquires sun sensor data from AD register address 0x8123, with a data format of {angle:uint12_be [0,0xFFF] (deg*scale); sun_visible:bool; encoding: little-endian, packed bits [11:0]=angle, [12]=flag}.
**Rationale:** This requirement describes a specific behavior of the system, which is to acquire data from the sun sensor.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-005]: Thruster Data Acquisition
**Description**: The system acquires thruster data, with a data contract of {status:bool, power:uint8[0-255]}; encoding: little-endian.
**Rationale:** This requirement describes a specific behavior of the system, which is to acquire data from the thruster.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-006]: Three-Axis Attitude Determination
**Description**: The system determines the three-axis attitude of the satellite, which is carried out every 160 ms.
**Rationale:** This requirement describes a function of the system, which is to determine the satellite's attitude.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-007]: Sun Search Mode Switching
**Description**: The system transitions from 'Rate Damping' to 'Pitch Search Mode' when angular velocity < 0.2 deg/sec for 5 cycles, or triggers 'Backup Sun Sensor' after 2 mode failures (see Section 4.2.1).
**Rationale:** This requirement describes a specific behavior of the system, which is to manage the sun search mode switching.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-008]: Fault Management
**Description**: The system detects and isolates failed gyroscope/thruster within 1s of fault, recovers operation using backup in under 5s, with fault event rate < 1/mission day.
**Rationale:** This requirement describes a function of the system, which is to manage faults and ensure the satellite's continuous operation.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---

[FR-009]: Telemetry Data Transmission
**Description**: The system collects and transmits the current operating status of its software, with telemetry sent on 0x88DB as {mode:byte, angle:uint16, velocity:q15}, every 160ms, AES-128 encrypted with HMAC-SHA256.
**Rationale:** This requirement describes a specific behavior of the system, which is to transmit telemetry data.
**Dependencies** / **Conflicts**:
- **Depends on:** None
- **Conflicts with:** None
---