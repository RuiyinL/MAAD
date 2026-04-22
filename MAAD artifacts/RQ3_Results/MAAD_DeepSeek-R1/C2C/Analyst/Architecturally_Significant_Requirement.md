# Architecturally Significant Requirements Results:
[ASR-003]: Public network remote control  
**Description**: All remote command/control transmissions must use TLS 1.2+ with AES-256-GCM, ECDHE-RSA/ECDHE-ECDSA ciphersuites; mutual TLS (PKI CA X.509) or OAuth2.1 Authorization Code Flow with PKCE and rotating secrets every 90 days mandated; audit logs must be WORM-protected and include {timestamp, operator ID, command, target device, result}; logs are to be archived for 180 days and reviewed quarterly.  
**Architectural Impact:**  
Demands security gateway implementation with TLS/mTLS encryption, RBAC authorization, credential management, and audit logging with secret redaction.  
**Quality Attributes Affected:**  
Security, Reliability  
**Architectural Constraints:**  
Requires API gateway pattern, end-to-end encryption for command channels, and credential security measures  
**Rationale:**  
High-risk requirement impacting security architecture, cross-cutting concerns, and regulatory compliance.  
**Dependencies** / **Conflicts**:  
- **Depends on:** FR-055, FR-063, FR-064  
---