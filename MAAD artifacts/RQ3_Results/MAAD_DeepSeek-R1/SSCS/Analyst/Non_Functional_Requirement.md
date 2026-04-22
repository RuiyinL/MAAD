# Non-Functional Requirements Results:  
[NFR-001]: Inter-Byte Timing  
**Description**: Commands/outputs must maintain <5µs intervals between serial port bytes. Metric: SERIAL_PORT_INTER_BYTE_DELAY_MAX per output burst; alert if >5µs.  
**Quality Attributes**: Performance  
**Measurable Criteria**: 5µs max interval with continuous validation.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-002, FR-008  
---  
[NFR-002]: Gyro Command-Response Delay  
**Description**: Fetch command to data read must have >5ms latency.  
**Quality Attributes**: Performance  
**Measurable Criteria**: Minimum 5ms delay.  
**Dependencies** / **Conflicts**:  
- **极epends on**: FR-002  
---  
[NFR-003]: Sensor Pulse Precision  
**Description**: Sun sensor switching requires 190ms pulse with ±1ms tolerance. Acceptance: SUN_SENSOR_PULSE_WIDTH_MS in [189,191]ms as measured during switch event; test: test_sunsensor_pulse_width().  
**Quality Attributes**: Reliability  
**Measurable Criteria**: 189ms–191ms pulse width with automated tests.  
**极ependencies** / **Conflicts**: None  
---  
[NFR-004]: Telemetry Timing  
**Description**: Telemetry transmission requires <5µs inter-byte intervals.  
**Quality Attributes**: Performance  
**Measurable Criteria**: 5µs max interval.  
**Dependencies** / **Conflicts**:  
- **Depends on**: FR-008  
---  
[NFR-005]: Hardware Constraints  
**Description**: Control computer uses 80C32E CPU (11.0592MHz), 32KB PROM, 8KB SRAM.  
**Quality Attributes**: Resource Utilization  
**Measurable Criteria**: Fixed hardware specifications.  
**Dependencies** / **Conflicts**: None  
---