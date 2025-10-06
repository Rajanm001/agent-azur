# Safety, Security, and Governance Plan
### Azure Agentic AI for RDP Supportability
Designed by: Rajan AI

---

## 🛡️ Security Architecture

### 1. Identity & Access Management

#### Authentication Methods

```
┌─────────────────────────────────────────┐
│   Authentication Options                │
├─────────────────────────────────────────┤
│ 1. Azure Managed Identity (Preferred)  │
│    ├─ System-assigned MSI               │
│    └─ User-assigned MSI                 │
│                                         │
│ 2. Service Principal                    │
│    ├─ Client ID + Secret                │
│    └─ Certificate-based auth            │
│                                         │
│ 3. Azure CLI (Development only)         │
│    └─ User credential flow              │
└─────────────────────────────────────────┘
```

#### RBAC Role Assignments

| Role | Scope | Purpose | Justification |
|------|-------|---------|---------------|
| Reader | Subscription | Read VM metadata, NSG rules, diagnostics | Minimum required for diagnostics |
| Virtual Machine Contributor | Resource Group | Start/stop VMs, restart services | Required for VM-level remediation |
| Network Contributor | Resource Group | Modify NSG rules | Required for network remediation |
| Monitoring Contributor | Subscription | Write to Azure Monitor | Required for observability |

#### Least Privilege Implementation

```python
# Example: Scoped permissions
{
  "permissions": [
    {
      "actions": [
        "Microsoft.Compute/virtualMachines/read",
        "Microsoft.Compute/virtualMachines/start/action",
        "Microsoft.Compute/virtualMachines/restart/action",
        "Microsoft.Network/networkSecurityGroups/read",
        "Microsoft.Network/networkSecurityGroups/write"
      ],
      "notActions": [
        "Microsoft.Compute/virtualMachines/delete",  # Cannot delete VMs
        "Microsoft.Network/virtualNetworks/delete"    # Cannot delete VNets
      ],
      "dataActions": [],
      "notDataActions": []
    }
  ],
  "scope": "/subscriptions/{sub-id}/resourceGroups/rg-production"
}
```

---

### 2. Secrets Management

#### Azure Key Vault Integration

```
All secrets stored in Azure Key Vault:

┌─────────────────────────────────────┐
│   Azure Key Vault                   │
├─────────────────────────────────────┤
│ • OpenAI API Key                    │
│ • Service Principal Secret          │
│ • Database connection strings       │
│ • Encryption keys                   │
└─────────────────────────────────────┘
           │
           ├──▶ Managed Identity access
           ├──▶ Soft-delete enabled
           ├──▶ Purge protection enabled
           └──▶ Access policies: Least privilege
```

#### Secret Rotation Policy

| Secret Type | Rotation Frequency | Automated |
|------------|-------------------|-----------|
| Service Principal Secret | 90 days | ✅ Yes |
| OpenAI API Key | 180 days | ⚠️ Manual |
| Database Passwords | 30 days | ✅ Yes |

---

### 3. Data Protection

#### Encryption Standards

| Data State | Encryption | Standard |
|-----------|------------|----------|
| At Rest | Azure Storage encryption | AES-256 |
| In Transit | TLS 1.3 | TLS 1.3 |
| In Memory | Secure enclave (optional) | N/A |

#### Data Classification

```
┌─────────────────────────────────────────────┐
│ Data Classification & Handling              │
├─────────────────────────────────────────────┤
│ PUBLIC: Architecture diagrams               │
│   └─ No restrictions                        │
│                                             │
│ INTERNAL: VM names, resource IDs            │
│   └─ Logged with sanitization               │
│                                             │
│ CONFIDENTIAL: Customer data, API keys       │
│   └─ Encrypted, access-controlled           │
│                                             │
│ RESTRICTED: PII, PHI, payment info          │
│   └─ NOT collected by this system           │
└─────────────────────────────────────────────┘
```

---

## 🚨 Safety Guardrails

### 1. Pre-Flight Checks

Before any remediation action:

```python
def pre_flight_checks(vm_name: str, action: str) -> bool:
    """
    Safety checks before executing any action
    
    Returns:
        True if safe to proceed, False to abort
    """
    checks = [
        verify_vm_exists(vm_name),
        verify_permissions(action),
        check_maintenance_window(),
        validate_action_scope(),
        backup_current_state(),
    ]
    
    return all(checks)
```

### 2. Human-in-the-Loop (HITL)

Configurable approval gates for high-risk actions:

```
┌─────────────────────────────────────────┐
│ HITL Approval Required For:             │
├─────────────────────────────────────────┤
│ ✅ VM Shutdown/Restart                  │
│ ✅ Network topology changes             │
│ ✅ Firewall rule modifications          │
│ ✅ Actions affecting >1 VM              │
│ ✅ Production environment changes       │
└─────────────────────────────────────────┘

Approval Flow:
User triggers → Agent analyzes → Creates approval request →
Engineer reviews → Approves/Rejects → Agent executes/cancels
```

### 3. Automatic Rollback

```python
class RollbackManager:
    """
    Manages automatic rollback on failure
    """
    
    def __init__(self):
        self.backup_state = {}
    
    def backup(self, resource_id: str, current_state: dict):
        """Save current state before changes"""
        self.backup_state[resource_id] = {
            "timestamp": datetime.utcnow(),
            "state": current_state,
            "checksum": hash(str(current_state))
        }
    
    def rollback(self, resource_id: str) -> bool:
        """Restore to previous state on failure"""
        if resource_id in self.backup_state:
            restore_state(self.backup_state[resource_id])
            logger.warning("rollback_executed", resource=resource_id)
            return True
        return False
```

### 4. Rate Limiting & Circuit Breaker

```
Rate Limits:
├─ Max 5 remediation attempts per VM per hour
├─ Max 10 OpenAI API calls per minute
└─ Max 100 Azure API calls per minute

Circuit Breaker:
├─ Open after 3 consecutive failures
├─ Half-open after 5 minutes cooldown
└─ Close after 1 successful operation
```

---

## 📋 Governance Framework

### 1. Audit Logging

Every action is logged immutably to Azure Monitor:

```json
{
  "timestamp": "2025-10-05T12:34:56Z",
  "event_type": "remediation_executed",
  "actor": {
    "type": "service_principal",
    "app_id": "562d445e-eb86-44a6-a35f-045663952c27",
    "tenant_id": "350d5725-064c-495c-98be-ee6fc42c3871"
  },
  "target": {
    "subscription_id": "76dfe244-9ff7-4423-90f8-2165d5ec144d",
    "resource_group": "rg-production",
    "vm_name": "vm-web-01"
  },
  "action": {
    "type": "nsg_rule_add",
    "details": {
      "rule_name": "AllowRDP-Inbound",
      "port": 3389,
      "protocol": "TCP",
      "source": "0.0.0.0/0"
    }
  },
  "result": "success",
  "duration_ms": 1234,
  "correlation_id": "abc-123-def-456"
}
```

### 2. Compliance Standards

| Standard | Requirement | Implementation |
|----------|------------|----------------|
| SOC 2 Type II | Audit trail for all changes | ✅ Azure Monitor Logs (90-day retention) |
| GDPR | No PII without consent | ✅ Data minimization, anonymization |
| ISO 27001 | Access controls | ✅ RBAC, MFA, least privilege |
| HIPAA | PHI protection | ✅ Encryption, access logs (if applicable) |
| PCI DSS | Payment data security | ⚠️ N/A (no payment data handled) |

### 3. Change Management

```
Change Approval Process:

┌──────────────┐
│ Agent        │
│ proposes fix │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Risk         │  ─┐
│ assessment   │   │ Automated
└──────┬───────┘   │
       │           │
       ▼          ─┘
┌──────────────┐
│ Approval     │  ─┐ High-risk: Human approval
│ required?    │   │ Low-risk: Auto-approve
└──────┬───────┘  ─┘
       │
       ▼
┌──────────────┐
│ Execute      │
│ with backup  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Verify &     │
│ log result   │
└──────────────┘
```

---

## 🔒 Incident Response

### Security Incident Classification

| Severity | Examples | Response Time | Escalation |
|----------|----------|---------------|------------|
| P1 - Critical | Unauthorized access, data breach | < 15 min | Immediate |
| P2 - High | Failed auth attempts spike | < 1 hour | If persists |
| P3 - Medium | Unusual API usage | < 4 hours | If continues |
| P4 - Low | Single failed login | < 24 hours | N/A |

### Incident Response Playbook

```
1. DETECT
   ├─ Automated monitoring alerts
   ├─ Anomaly detection via ML
   └─ Manual report

2. CONTAIN
   ├─ Isolate affected resources
   ├─ Revoke compromised credentials
   └─ Enable enhanced logging

3. INVESTIGATE
   ├─ Review audit logs
   ├─ Identify root cause
   └─ Determine scope

4. REMEDIATE
   ├─ Patch vulnerabilities
   ├─ Reset credentials
   └─ Update security rules

5. RECOVER
   ├─ Restore from backup if needed
   ├─ Verify system integrity
   └─ Resume normal operations

6. LESSONS LEARNED
   ├─ Document incident
   ├─ Update playbooks
   └─ Implement preventive measures
```

---

## 📊 Monitoring & Alerting

### Security Monitoring

```kusto
// Azure Monitor Query: Detect suspicious activity
AzureRDPAgentLogs
| where TimeGenerated > ago(1h)
| where EventType in ("unauthorized_access", "failed_authentication", "anomalous_behavior")
| summarize Count=count() by Actor, TargetResource
| where Count > 10
| project TimeGenerated, Actor, TargetResource, Count
| order by Count desc
```

### Alert Rules

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Unauthorized API Call | 403/401 response | Critical | Page on-call, revoke token |
| Failed Auth Spike | >10 failures in 5 min | High | Lock account, notify SOC |
| Unusual Remediation | Off-hours execution | Medium | Email security team |
| High Token Usage | >10k tokens/hour | Low | Cost alert, review usage |

---

## ✅ Compliance Checklist

- [x] Authentication: Managed Identity with RBAC
- [x] Authorization: Least privilege access
- [x] Audit Logging: All actions logged to Azure Monitor
- [x] Encryption: TLS 1.3 in transit, AES-256 at rest
- [x] Secret Management: Azure Key Vault integration
- [x] Data Protection: No PII collected, GDPR compliant
- [x] Incident Response: Documented playbook
- [x] Monitoring: Real-time security alerts
- [x] Backup & Recovery: Automatic state backup before changes
- [x] Rate Limiting: Protection against abuse
- [x] Circuit Breaker: Automatic failure handling
- [x] Human Approval: Configurable for high-risk actions

---

## 📚 References

- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/fundamentals/best-practices-and-patterns)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Azure Foundations Benchmark](https://www.cisecurity.org/benchmark/azure)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

Document Version: 1.0.0  
Last Updated: October 5, 2025  
Author: Rajan AI  
Classification: Internal Use
