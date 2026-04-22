# Architecturally Significant Requirements Results:
[ASR-001]: Unalterable Audit Trail  
**Description**: Audit logs are strictly append-only; no delete or soft-delete operations (including by admins) are permitted for audit trail data. Application data may use soft-deletion.  
**Architectural Impact:**  
Mandates append-only storage, cryptographic integrity (e.g., hashing), and event broadcasting. Requires ACID-compliant databases (e.g., PostgreSQL) to prevent tampering, impacting transaction design.  

**Quality Attributes Affected:**  
Security, Reliability  

**Architectural Constraints:**  
Append-only log architecture with TTL-based retention; rejects deletes/updates.  

**Rationale:**  
Critical for legal admissibility, high risk if compromised. Cross-cutting (affects CRUD operations).  

**Dependencies** / **Conflicts**:  
- **Depends on:**   
- **Conflicts with:** FR-012 (soft deletes)  
---

[ASR-002]: Offline Mode Operation  
**Description**: Offline mode must store all new/modified data up to 10GB (configurable) and support at least 72h operation without sync. Upon 24h sync failure, SRE incident ticket is opened. If local cache is corrupted/unavailable, station function must degrade gracefully with notification.  
**Architectural Impact:**  
Demands local storage/caching, conflict-resolution mechanisms (e.g., CQRS/event replay), and eventual consistency trade-offs.  

**Quality Attributes Affected:**  
Reliability, Availability  

**Architectural Constraints:**  
Hybrid sync architecture; offline-first design with TTL-based conflict resolution.  

**Rationale:**  
High-risk requirement impacting scalability & consistency; unacceptable downtime in law enforcement.  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-009  
- **Conflicts with:** NFR-010 (performance SLAs)  
---

[ASR-003]: SOA & Centralized Deployment  
**Description**: System uses SOA/modular design deployed centrally in 3-tier architecture.  
**Architectural Impact:**  
Enforces strict layer separation (presentation/business/data) and standardized services. Mandates broker/API gateways for integration.  

**Quality Attributes Affected:**  
Modifiability, Scalability  

**Architectural Constraints:**  
Microkernel with adapters; disallows monolithic design.  

**Rationale:**  
Deviates from default architectures; high business value for distributed police stations.  

**Dependencies** / **Conflicts**:  
- **Depends on:** NFR-008  
- **Conflicts with:**   
---

[ASR-004]: Multi-Platform Access  
**Description**: Browser-based access with minimal client requirements; extensible to PDAs/mobile.  
**Architectural Impact:**  
Requires thin-client patterns, responsive UI, and API-first interfaces for diverse devices.  

**Quality Attributes Affected:**  
Portability, Compatibility  

**Architectural Constraints:**  
Stateless backend services; decoupled client-server interactions.  

**Rationale:**  
Cross-cutting; precludes native client dependencies.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-007  
- **Conflicts with:**   
---

[ASR-005]: Performance Optimization  
**Description**: Batch fetching (10-20 records), pagination, AJAX, caching, static hosting on web servers.  
**Architectural Impact:**  
Drives cache hierarchies (distributed/global), connection pooling, and selective query design.  

**Quality Attributes Affected:**  
Performance, Scalability  

**Architectural Constraints:**  
RESTful pagination; read/write decoupling; CDN-like static delivery.  

**Rationale:**  
Key to meeting strict search SLAs; large-volume data handling.  

**Dependencies** / **Conflicts**:  
- **Depends on:** FR-004  
- **Conflicts with:** ASR-002 (offline caching syncing)  
---