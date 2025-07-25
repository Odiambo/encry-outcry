
# 🛡️ Privacy-First Log Processing: Zero-trst design

## Why Privacy-Centric Logging Matters
In a world where every byte of data is valuable and surveillance capabilities grow exponentially, protecting the confidentiality and integrity of logs is critical. System logs, administrative activity, authentication records, and error trails are often goldmines of sensitive information. Exposure of them, whether accidentally or by breach, can unravel an organization's security posture.

Zero Trust principles demand that **no system component is inherently trusted**, not even internal logs. Encrypting logs -especially admin logs and high-sensitivity application traces- extends Zero Trust protections to the observability layer.

### Homomorphic Encryption Ideatioin           
Traditional encryption protects data at rest and in transit—but not during processing. **Homomorphic Encryption (HE)** allows limited computation on encrypted data without decryption, producing encrypted results that, once decrypted, match the result of operations on plaintext.

**HE:** 
- Eliminates the need to decrypt sensitive data during processing.
- Reduces attack surface in shared, microservice, and AI environments.
- Enables privacy perserving comptations in highly regulated domains like healthcare and finance.

This opens the door to privacy-preserving analytics on log streams without ever exposing raw contents—especially powerful in regulated, zero-trust, or multi-tenant environments.

While our current system implements symmetric encryption (AES-GCM), the architecture is modular enough to support homomorphic log indexing or future federated learning extensions.


### Encryption + Logging = Modern Defense-in-Depth
The threat arena has malware-as-a-service, microservice killchain, and AI-assisted tools. Deep observability, log integrity and privacy must be built-in not taped on later. 

Zero-trust 4.0 requires incident response strategies to be in constent iteration, so contious logging, rotating access and authentication, and encryption of data should occur per transaction.

 Our system uses:
- **Redaction** to neutralize PII and secrets
- **AES-256-GCM encryption** for end-to-end confidentiality
- **Tamper-evident audit trails** for forensic verifiability
- **Role-based access to logs and API metrics**
- **Real-time monitoring via Prometheus and FastAPI**

These techniques form a multilayered, Zero Trust-aligned log strategy—suited for enterprises, cloud-native apps, and regulated environments.

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

### 🛠️ Deployment Instructions

To get started quickly with the full system using Docker Compose:

```bash
# 1. Clone the repository
$ git clone https://github.com/your-org/privacy-log-processor.git
$ cd privacy-log-processor

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
