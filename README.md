<div align="center">

# 🛡️ encry-outcry

## Privacy-First Log Processing  
## Zero-Trust Architecture and Build

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Security: AES-256-GCM](https://img.shields.io/badge/encryption-AES--256--GCM-green)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/Odiambo/encry-outcry?style=social)](https://github.com/Odiambo/encry-outcry)

</div>

---

> **Enterprise-grade log encryption system** providing AES-256-GCM encryption,  
> PII redaction, and tamper-evident audit trails for cloud-native applications.  
> Designed to support GDPR, HIPAA, and Zero Trust security models.

**Keywords**: encrypted logging, privacy-preserving analytics, homomorphic encryption,  
zero trust security, PII redaction, audit logging, GDPR compliance, DevSecOps,  
log encryption, data privacy, AES-256-GCM, tamper-evident logs

---
## Why Privacy-Centric Logging Matters
In a world where every byte of data is valuable and surveillance capabilities grow exponentially, protecting the confidentiality and integrity of logs is critical. System logs, administrative activity, authentication records, and error trails are often goldmines of sensitive information. Exposure of them, whether accidentally or by breach, can unravel an organization's security posture.

Zero Trust principles demand that **no system component is inherently trusted**, not even internal logs. Encrypting logs -especially admin logs and high-sensitivity application traces- extends Zero Trust protections to the observability layer.

### Homomorphic Encryption Ideation           
Traditional encryption protects data at rest and in transit, but not during processing. **Homomorphic Encryption (HE)** allows limited computation on encrypted data without decryption, producing encrypted results that, once decrypted, match the result of operations on plaintext.

**HE:** 
- Eliminates the need to decrypt sensitive data during processing.
- Reduces attack surface in shared, microservice, and AI environments.
- Enables privacy preserving computations in highly regulated domains like healthcare and finance.

This opens the door to privacy-preserving analytics on log streams without ever exposing raw contents, especially powerful in regulated, zero-trust, or multi-tenant environments.

While our current system implements symmetric encryption (AES-GCM), the architecture is modular enough to support homomorphic log indexing or future federated learning extensions.


### Encryption + Logging = Modern Defense-in-Depth
The threat arena has malware-as-a-service, microservice killchain, and AI-assisted tools. Deep observability, log integrity and privacy must be built-in not taped on later. 

Zero-trust 4.0 requires incident response strategies to be in constant iteration, so continuous logging, rotating access and authentication, and encryption of data should occur per transaction.

 Our system uses:
- **Redaction** to neutralize PII and secrets
- **AES-256-GCM encryption** for end-to-end confidentiality
- **Tamper-evident audit trails** for forensic verifiability
- **Role-based access to logs and API metrics**
- **Real-time monitoring via Prometheus and FastAPI**

These techniques form a multilayered, Zero Trust-aligned log strategy suited for enterprises, cloud-native apps, and regulated environments.

## Threat Model & Trust Assumptions

This project’s threat model is grounded in protecting sensitive observability data processed and stored in cloud-native environments. The objectives are confidentiality of log contents, integrity of audit trails, and resilience against active and passive adversaries.

**Primary Assets**
- Encrypted log payloads and metadata.
- Audit event streams and tamper-evident audit chains.
- Redacted representations of sensitive events (PII removed).
- Encryption keys and cryptographic nonces.

**Threat Actors**
- **External adversaries** with network access capable of eavesdropping, traffic replay, or tampering with log transport layers.
- **Compromised internal components** (e.g., unprivileged microservices, CI pipelines) able to observe logs prior to ingestion.
- **Insider threats** with legitimate access to parts of the observability stack (e.g., developers or administrators).
- **Cloud control plane attackers** with potential access to observability infrastructure metadata.

**Assumptions**
1. **Key Confidentiality** — Cryptographic keys are provisioned and stored securely outside of application source code and are rotated according to policy; compromise of keys outside immediate logging services is outside scope.
2. **Unique Nonces per Encryption** — The AES-256-GCM encryption primitive requires unique nonces for each log record to prevent cryptanalytic weaknesses (reuse undermines confidentiality and integrity). A secure nonce generation strategy is assumed.
3. **Authenticated Transport** — TLS-terminated ingress and egress between services ensure in-flight protection; underlying network is not implicitly trusted.
4. **Immutable Audit Logs** — Once committed, audit entries are append-only and verifiable via hash chaining.
5. **Service Isolation** — Individual microservices are isolated via role-based access controls and Zero Trust policies; no lateral trust is assumed.

**Attack Vectors and Mitigations**
- **Eavesdropping / Interception:**  
  Encrypted log content uses AES-256-GCM (industry-standard authenticated encryption), preventing plaintext recovery or forged modifications by passive observers. :contentReference[oaicite:1]{index=1}
- **Tampering with Logs or Audit Entries:**  
  Tamper-evident audit trails with hash chaining ensure unauthorized modifications are detectable; any alteration to encrypted logs invalidates authentication tags.
- **Replay Attacks:**  
  Unique nonces and session fingerprints mitigate replay of old log traffic; replay detection is supported at ingest endpoints.
- **Insider Access:**  
  PII redaction prior to encryption reduces sensitive surface exposure; explicit role-based access prevents unwarranted decryption or audit log enumeration.
- **Key Compromise:**  
  The model acknowledges that if encryption keys are compromised externally (outside strict boundary assumptions), confidentiality may be lost; key rotation and secure key stores are recommended.

**Out-of-Scope**
- Cryptanalysis of AES-256-GCM or fundamental algorithm weaknesses.
- Side-channel attacks on host hardware.
- Protection against complete cloud provider control plane compromise.
- Homomorphic encryption.
---

## System Overview: Privacy Log Processor

This project implements a modular, end-to-end encrypted logging system with:

### 🧩 Core Components
- **Pattern Detection Engine**: Tags risky patterns in logs (e.g. SQL injection, failed logins)
- **Redaction Processor**: Removes emails, IPs, SSNs, and other sensitive elements
- **Encryptor**: AES-256-GCM encryption for all processed logs
- **Configuration Manager**: Centralized redaction + encryption policy control
- **Audit Logger**: Immutable, hash-chained event trail
- **Prometheus Exporter**: Monitors ingestion and audit rates
- **FastAPI Dashboard**: Fetch logs and audit events through HTTP APIs
- **React Frontend**: Live UI to view logs and trace audit trails

### ⚙️ Features
- Defense-in-depth: redaction → encryption → tamper-logging
- Modular, scalable, and Docker/Kubernetes-ready
- Python + FastAPI backend; React + Vite frontend
- Full observability via structured logs and Prometheus metrics

### 🚀 Use Cases
- Encrypted logs for healthcare, finance, or defense sectors
- Zero Trust observability in AI-era applications
- Secure, auditable DevOps monitoring
- Privacy-preserving logging for cloud-native services
- Red team environments that must maintain operational secrecy

### API Reference

The FastAPI backend exposes the following endpoints:

#### `GET /logs/{log_id}`
- **Description**: Retrieve the encrypted contents of a specific log file by ID.
- **Response**: `{ "log_id": "<uuid>", "content": "<base64_encrypted_log>" }`
- **Example**: `curl http://localhost:8000/logs/abc123-uuid`

#### `GET /audit`
- **Description**: Returns all audit log entries as JSON objects.
- **Response**:
```json
[
  {
    "timestamp": "2025-07-16T12:00:00Z",
    "log_id": "abc123",
    "action": "store_log",
    "user": "app-x",
    "hash": 12345678901234567890
  },
  ...
]
```
- **Example**: `curl http://localhost:8000/audit`


---

## 🛠️ Deployment Instructions
### 📋 Prerequisites

- Python 3.11 or higher
- Docker 20.10+ and Docker Compose 2.0+
- Kubernetes 1.24+ (for production deployments)
- Prometheus (optional, for monitoring)
- Git

>Install: docker, python (slim or whatever comes next), git, and prometheus.<br>
Maintainers will monitor dependencies for the Dockerfile. 

To get started quickly with the full system using Docker Compose:

```bash
# 1. Clone the repository
$ git clone https://github.com/Odiambo/encry-outcry.git
$ cd encry-outcry

# 2. Build and start the services
$ docker-compose up --build

# 3. Access the FastAPI backend
http://localhost:8000/docs

# 4. Access the Prometheus metrics endpoint
http://localhost:9100/metrics

# 5. Access the React dashboard (if configured)
http://localhost:8000/frontend/dist/
```

For Kubernetes deployments, apply the manifests in the `k8s/` directory:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

> ⚠️ Logs and audit entries are stored in ephemeral volumes by default. Modify to use `PersistentVolumeClaims` for production durability.

### **5. License Section**

```markdown
## 📄 License

This project is licensed under the GNU AGPL v3.0 - 
see the [LICENSE](https://github.com/Odiambo/encry-outcry/blob/chef/LICENSE) file for details.




