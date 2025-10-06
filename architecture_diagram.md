# Azure Agentic AI Architecture - Reference Diagram

## 🏗️ High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER / SUPPORT ENTRY                             │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐          │
│  │ Azure Portal │    │ Support Ticket│    │  AI Chat Bot   │          │
│  │   Request    │───▶│    System     │───▶│   Interface    │          │
│  └──────────────┘    └──────────────┘    └─────────────────┘          │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI ORCHESTRATOR (Central Agent)                     │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │  • Ticket ingestion and prioritization                       │      │
│  │  • Context gathering from Azure APIs                         │      │
│  │  • Decision making with OpenAI GPT-4                         │      │
│  │  • Workflow orchestration                                    │      │
│  │  • Logging and audit trail                                   │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
│  Permissions: Managed Identity + RBAC (Reader, Contributor)             │
│  Runtime: Python 3.11+, FastAPI, Async I/O                              │
│  Guardrails: Human approval for destructive actions                     │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌──────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  DIAGNOSTIC      │ │  REMEDIATION    │ │  VALIDATION      │
│     AGENT        │ │     AGENT       │ │     AGENT        │
│                  │ │                 │ │                  │
│ Checks:          │ │ Actions:        │ │ Verifies:        │
│ • VM Power State │ │ • Start VM      │ │ • RDP Port Open  │
│ • NSG Rules      │ │ • Fix NSG       │ │ • Service Status │
│ • RDP Service    │ │ • Restart RDP   │ │ • Connectivity   │
│ • Firewall       │ │ • RunCommand    │ │ • Final Test     │
│ • Connectivity   │ │ • Rollback      │ │                  │
└────────┬─────────┘ └────────┬────────┘ └────────┬─────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES & TOOLS                                │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ Azure REST   │  │ Azure CLI    │  │ PowerShell   │                 │
│  │     API      │  │  RunCommand  │  │   Scripts    │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ Network      │  │  Compute     │  │   Monitor    │                 │
│  │  Watcher     │  │   Metrics    │  │     Logs     │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY & METRICS LAYER                         │
│                                                                          │
│  ┌────────────────────┐         ┌────────────────────┐                 │
│  │   Prometheus       │         │  Azure Monitor     │                 │
│  │   Metrics          │◀───────▶│   Integration      │                 │
│  │   (Port 8000)      │         │                    │                 │
│  └────────────────────┘         └────────────────────┘                 │
│                                                                          │
│  Metrics Tracked:                                                       │
│  • rdp_issues_detected_total                                            │
│  • auto_resolutions_successful_total                                    │
│  • mean_time_to_resolve_seconds                                         │
│  • diagnostic_checks_performed_total                                    │
│  • openai_api_calls_total                                               │
│  • failed_remediation_attempts_total                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Customer Flow to Resolution (Detailed)

### Phase 1: Entry & Triage
```
Customer Reports Issue
        │
        ├─▶ Portal/Chat/Email
        │
        ▼
   Ticket Created
        │
        ├─▶ Priority Assignment (P1-P4)
        │
        ▼
AI Orchestrator Invoked
        │
        ├─▶ Context Gathering
        │   ├─ VM Metadata
        │   ├─ Historical Issues
        │   └─ Network Topology
        │
        ▼
   Routing to Diagnostic Agent
```

### Phase 2: Diagnosis
```
Diagnostic Agent Start
        │
        ├─▶ Hypothesis 1: VM Power State
        │   ├─ Check: compute_client.virtual_machines.get()
        │   ├─ Result: Running / Stopped / Deallocated
        │   └─ Confidence: High
        │
        ├─▶ Hypothesis 2: NSG Blocking Port 3389
        │   ├─ Check: network_client.security_rules.list()
        │   ├─ Result: Rule exists / Missing / Deny
        │   └─ Confidence: High
        │
        ├─▶ Hypothesis 3: RDP Service Status
        │   ├─ Check: RunCommand "Get-Service TermService"
        │   ├─ Result: Running / Stopped / Error
        │   └─ Confidence: Medium
        │
        ├─▶ Hypothesis 4: Windows Firewall
        │   ├─ Check: RunCommand "Get-NetFirewallRule"
        │   ├─ Result: Enabled / Disabled / Blocking
        │   └─ Confidence: Medium
        │
        └─▶ Hypothesis 5: Network Connectivity
            ├─ Check: Network Watcher connectivity test
            ├─ Result: Reachable / Unreachable / Timeout
            └─ Confidence: High
```

### Phase 3: AI Reasoning & Plan
```
OpenAI GPT-4 Analysis
        │
        ├─▶ Analyze diagnostic results
        │   ├─ Pattern recognition
        │   ├─ Root cause identification
        │   └─ Confidence scoring
        │
        ▼
   Remediation Plan Generated
        │
        ├─▶ Step 1: Start VM (if stopped)
        ├─▶ Step 2: Add NSG rule for 3389
        ├─▶ Step 3: Restart RDP service
        ├─▶ Step 4: Enable firewall rule
        └─▶ Step 5: Verify connectivity
```

### Phase 4: Remediation
```
Remediation Agent Execution
        │
        ├─▶ Pre-flight Checks
        │   ├─ Backup current config
        │   ├─ Validate permissions
        │   └─ Log action plan
        │
        ├─▶ Execute Fixes (Sequential)
        │   ├─ Action 1: Start VM
        │   │   └─ Result: Success ✓
        │   ├─ Action 2: Update NSG
        │   │   └─ Result: Success ✓
        │   ├─ Action 3: Restart Service
        │   │   └─ Result: Success ✓
        │   └─ Rollback on Failure ✗
        │
        └─▶ Post-Action Validation
            ├─ Wait for propagation
            └─ Run verification tests
```

### Phase 5: Validation
```
Validation Agent Start
        │
        ├─▶ Port Scan Test
        │   ├─ TCP Connect to :3389
        │   └─ Result: Port Open ✓
        │
        ├─▶ RDP Handshake Test
        │   ├─ Initiate RDP protocol
        │   └─ Result: Responding ✓
        │
        ├─▶ End-to-End Test
        │   ├─ Full RDP connection attempt
        │   └─ Result: Connected ✓
        │
        └─▶ Final Report
            ├─ Issue: Resolved ✓
            ├─ Time: 42 seconds
            └─ Actions: 3 fixes applied
```

### Phase 6: Closure & Learning
```
Closure Process
        │
        ├─▶ Update Ticket Status → RESOLVED
        │
        ├─▶ Send Customer Notification
        │   ├─ Resolution summary
        │   ├─ Actions taken
        │   └─ Prevention tips
        │
        ├─▶ Log to Knowledge Base
        │   ├─ Issue pattern
        │   ├─ Solution steps
        │   └─ Success metrics
        │
        └─▶ Metrics Update
            ├─ Increment success counter
            ├─ Record resolution time
            └─ Update dashboards
```

---

## 🛡️ Safety, Security & Governance

### Identity & Access Management
```
┌─────────────────────────────────────┐
│   Azure Managed Identity            │
│   ├─ System-assigned identity       │
│   └─ User-assigned identity         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   RBAC Role Assignments             │
│   ├─ Reader (diagnostics)           │
│   ├─ Contributor (remediation)      │
│   └─ Network Contributor (NSG)      │
└─────────────────────────────────────┘
```

### Guardrails & Controls
- **Human-in-the-Loop**: Destructive actions require approval
- **Dry-Run Mode**: Test fixes without applying
- **Rollback Capability**: Automatic rollback on failure
- **Action Logging**: Every action logged to Azure Monitor
- **Rate Limiting**: Max 5 remediation attempts per hour
- **Scope Restriction**: Only authorized subscriptions/RGs

### Compliance & Audit
- **SOC 2 Type II**: Compliant logging and access controls
- **GDPR**: No PII in logs (sanitized)
- **ISO 27001**: Encrypted at rest and in transit
- **Audit Trail**: Immutable logs for 90+ days

---

## 📊 Observability Dashboard

```
┌────────────────────────────────────────────────────────┐
│              AZURE RDP AGENT DASHBOARD                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Total Issues Detected:        147                    │
│  Auto-Resolved:                132 (89.8%)            │
│  Escalated to Human:           15  (10.2%)            │
│  Mean Time to Resolve:         34 seconds             │
│                                                        │
├────────────────────────────────────────────────────────┤
│  Top Root Causes (Last 7 Days):                       │
│  ┌──────────────────────────┬─────────────┐          │
│  │ NSG Blocking 3389        │ 67%  ██████ │          │
│  │ VM Stopped/Deallocated   │ 18%  ██     │          │
│  │ RDP Service Crashed      │ 11%  █      │          │
│  │ Windows Firewall         │ 4%   ▌      │          │
│  └──────────────────────────┴─────────────┘          │
│                                                        │
├────────────────────────────────────────────────────────┤
│  Agent Performance:                                    │
│  • Diagnostic Time: 8.2s avg                          │
│  • Remediation Time: 12.5s avg                        │
│  • Validation Time: 4.1s avg                          │
│  • OpenAI API Latency: 2.3s avg                       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Runtime** | Python 3.11+ |
| **Framework** | FastAPI + Async |
| **Azure SDK** | azure-identity, azure-mgmt-* |
| **AI/ML** | OpenAI GPT-4, LangChain |
| **Observability** | Prometheus, Grafana, Azure Monitor |
| **Logging** | Structlog (JSON) |
| **Testing** | Pytest, Mock Azure APIs |
| **CI/CD** | GitHub Actions, Azure DevOps |

---

## 📚 Key Design Principles

1. **Autonomous First**: AI makes decisions, human as fallback
2. **Safe by Default**: Dry-run mode, rollback, approval gates
3. **Observable**: Every action logged and metered
4. **Scalable**: Async, event-driven, multi-tenant ready
5. **Extensible**: Plugin architecture for new diagnostics
6. **Resilient**: Retry logic, circuit breakers, graceful degradation

---

**Designed and Developed by Rajan AI**  
*Azure Expert | AI/ML Specialist | Production Systems Architect*
