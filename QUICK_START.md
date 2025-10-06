# Quick Start Guide - 3 Ways to Run the Project

No Azure secrets? No problem! Choose from 3 authentication modes based on what you have available.

---

## 📋 TL;DR - Choose Your Mode

| Mode | When to Use | Setup Time | Requires |
|------|-------------|------------|----------|
| **🎭 MOCK** | Demo/testing without Azure | 30 seconds | Nothing! |
| **💻 CLI** | You have Azure access | 2 minutes | Azure CLI + `az login` |
| **🔐 SERVICE_PRINCIPAL** | Production deployment | 5 minutes | Azure subscription + credentials |

---

## 🎭 OPTION 1: MOCK MODE (Easiest - No Azure Needed!)

Perfect for testing, demos, or when you don't have Azure credentials.

### Steps:

1. **Open your `.env` file** and add:
   ```bash
   AZURE_AUTH_MODE=MOCK
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

2. **Run the application**:
   ```bash
   python src\main.py
   ```

3. **That's it!** The system will use simulated data:
   - ✅ 2 mock VMs (vm-web-01, vm-db-01)
   - ✅ Mock NSG rules (missing RDP - simulating the problem)
   - ✅ All agents work normally with dummy data
   - ✅ OpenAI analysis still works (if you have API key)

### What You'll See:
```
🚀 Initializing Azure Client mode='MOCK'
✅ Mock mode initialized - using simulated data
💡 TIP: Set AZURE_AUTH_MODE=CLI to use real Azure (after 'az login')

📦 MOCK MODE: Returning simulated VMs
[DIAGNOSTIC] Analyzing VM: vm-web-01
[DIAGNOSTIC] Status: running, RDP Port: BLOCKED by NSG

🔍 Root Cause: NSG missing RDP rule (port 3389)
📊 Confidence: 95%

[REMEDIATION] 📦 MOCK MODE: Simulating NSG rule addition for RDP
✅ Would add NSG rule 'Allow-RDP-3389' with priority 100

✨ RESOLUTION COMPLETE (Mock Mode)
```

---

## 💻 OPTION 2: CLI MODE (Recommended for Real Azure Data)

Use your existing Azure login session - **no secrets needed!**

### Prerequisites:
- Azure CLI installed ([Download here](https://aka.ms/installazurecli))
- An active Azure subscription

### Steps:

1. **Login to Azure CLI**:
   ```bash
   az login
   ```
   → Opens browser → Sign in with your Microsoft account → Success!

2. **Verify your subscription**:
   ```bash
   az account show
   ```
   Copy the `"id"` value (your subscription ID)

3. **Update your `.env` file**:
   ```bash
   AZURE_AUTH_MODE=CLI
   AZURE_SUBSCRIPTION_ID=your-subscription-id-from-step-2
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

4. **Run the application**:
   ```bash
   python src\main.py
   ```

### What You'll See:
```
🚀 Initializing Azure Client mode='CLI'
🔍 Detected Azure CLI login
✅ Azure CLI authentication successful subscription_id='76dfe244-...'

🌐 Calling Azure API to fetch VMs...
✅ Successfully fetched 5 VMs from Azure

[DIAGNOSTIC] Analyzing REAL VM: vm-production-01
[DIAGNOSTIC] Real NSG rules: 12 rules found
...
```

### Troubleshooting:
- **Error: "Azure CLI not logged in"** → Run `az login` first
- **Error: "No subscription found"** → Run `az account set --subscription <id>`
- **Still not working?** → Falls back to MOCK mode automatically

---

## 🔐 OPTION 3: SERVICE_PRINCIPAL MODE (Production)

Full authentication with secrets - for production deployments.

### Prerequisites:
- Azure subscription with contributor access
- Ability to create app registrations in Azure AD

### Steps:

1. **Create Service Principal** (one-time setup):
   
   **Option A: Via Azure CLI**
   ```bash
   az ad sp create-for-rbac --name "RajanAI-AgenticApp" --role contributor --scopes /subscriptions/YOUR-SUBSCRIPTION-ID
   ```
   
   **Option B: Via Azure Portal**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to **Microsoft Entra ID** (Azure AD)
   - Go to **App registrations** → **New registration**
   - Name: `RajanAI-AgenticApp`
   - Under **Certificates & Secrets** → **New client secret**
   - Copy:
     - Application (client) ID
     - Directory (tenant) ID
     - Client secret value (copy immediately!)

2. **Update your `.env` file**:
   ```bash
   AZURE_AUTH_MODE=SERVICE_PRINCIPAL
   AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

3. **Run the application**:
   ```bash
   python src\main.py
   ```

### What You'll See:
```
🚀 Initializing Azure Client mode='SERVICE_PRINCIPAL'
🔍 Detected Service Principal credentials
✅ Service Principal authentication successful subscription_id='76dfe244-...'

🌐 Calling Azure API to fetch VMs...
✅ Successfully fetched 5 VMs from Azure
...
```

---

## ⚙️ AUTO MODE (Smart Detection)

Don't want to choose? Just leave `AZURE_AUTH_MODE` unset (or set to `AUTO`):

```bash
# .env file
# AZURE_AUTH_MODE=AUTO   <-- This is the default
AZURE_SUBSCRIPTION_ID=...
OPENAI_API_KEY=...
```

The system will **automatically detect** the best mode:
1. ✅ **Check for Service Principal** (tenant_id, client_id, client_secret)
2. ✅ **Check for Azure CLI login** (`az account show`)
3. ✅ **Fallback to MOCK mode** (if nothing found)

---

## 🧪 Testing All Modes

Want to test all 3 modes? Easy!

### Test MOCK Mode:
```bash
$env:AZURE_AUTH_MODE="MOCK" ; python src\main.py
```

### Test CLI Mode (after `az login`):
```bash
$env:AZURE_AUTH_MODE="CLI" ; python src\main.py
```

### Test SERVICE_PRINCIPAL Mode:
```bash
$env:AZURE_AUTH_MODE="SERVICE_PRINCIPAL" ; python src\main.py
```

---

## 📊 Comparison Table

| Feature | MOCK | CLI | SERVICE_PRINCIPAL |
|---------|------|-----|-------------------|
| **Setup Time** | 30 sec | 2 min | 5 min |
| **Azure Connection** | ❌ Offline | ✅ Real | ✅ Real |
| **Secrets Required** | ❌ None | ❌ None | ✅ Yes |
| **Real VM Data** | ❌ Simulated | ✅ Live | ✅ Live |
| **Can Modify Azure** | ❌ No | ✅ Yes | ✅ Yes |
| **Production Ready** | ❌ No | ⚠️ Dev only | ✅ Yes |
| **Best For** | Demos, testing | Dev, exploration | Production, CI/CD |

---

## 🎯 Recommended Setup by Use Case

### 1. **Assignment Submission / Demo**
```bash
AZURE_AUTH_MODE=MOCK
OPENAI_API_KEY=sk-proj-...
```
✅ No Azure needed
✅ Shows full workflow
✅ Fast and reliable

### 2. **Testing with Real Azure Resources**
```bash
AZURE_AUTH_MODE=CLI
AZURE_SUBSCRIPTION_ID=...
OPENAI_API_KEY=sk-proj-...
```
✅ Use `az login` session
✅ No secrets in `.env`
✅ Real Azure data

### 3. **Production Deployment**
```bash
AZURE_AUTH_MODE=SERVICE_PRINCIPAL
AZURE_SUBSCRIPTION_ID=...
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
OPENAI_API_KEY=sk-proj-...
```
✅ Secure authentication
✅ CI/CD friendly
✅ No interactive login

---

## 🚨 Troubleshooting

### Issue: "Authentication failed"
**Solution:**
- MOCK mode → Ignore, it's simulated
- CLI mode → Run `az login` first
- SERVICE_PRINCIPAL → Check credentials in `.env`

### Issue: "No VMs found"
**Solution:**
- MOCK mode → Should return 2 mock VMs (check code)
- CLI/SERVICE_PRINCIPAL → Your subscription might be empty
  ```bash
  az vm list --output table
  ```

### Issue: "Module not found: structlog"
**Solution:**
```bash
pip install structlog
```

### Issue: "OpenAI API key not set"
**Solution:** Add to `.env`:
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```
Get one free at: https://platform.openai.com/api-keys

---

## 📝 Complete `.env` Examples

### Example 1: MOCK Mode (Simplest)
```bash
AZURE_AUTH_MODE=MOCK
OPENAI_API_KEY=sk-proj-xxxxx
```

### Example 2: CLI Mode
```bash
AZURE_AUTH_MODE=CLI
AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d
OPENAI_API_KEY=sk-proj-xxxxx
```

### Example 3: Service Principal Mode
```bash
AZURE_AUTH_MODE=SERVICE_PRINCIPAL
AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-secret
OPENAI_API_KEY=sk-proj-xxxxx
```

### Example 4: Auto Mode
```bash
# No AZURE_AUTH_MODE specified - auto-detects!
AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d
OPENAI_API_KEY=sk-proj-xxxxx
```

---

## ✅ Verification Commands

### Check Your Setup:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Test Azure connection
python -c "from src.services.azure_client import AzureClient; client = AzureClient(); print(client.test_connection())"
```

### Expected Output:
**MOCK Mode:**
```json
{
  "status": "ok",
  "mode": "MOCK",
  "message": "✅ Mock mode active - no Azure connection needed",
  "tip": "Set AZURE_AUTH_MODE=CLI to use real Azure (after 'az login')"
}
```

**CLI/SERVICE_PRINCIPAL Mode:**
```json
{
  "status": "ok",
  "mode": "CLI",
  "message": "✅ Azure connection successful via Azure CLI",
  "authenticated": true
}
```

---

## 🎓 Next Steps

1. ✅ Choose your authentication mode
2. ✅ Update `.env` file
3. ✅ Run `python src\main.py`
4. ✅ See the AI agents in action!
5. ✅ Check metrics at `http://localhost:8000/metrics`

---

## 📞 Need Help?

- **MOCK Mode Issues** → Should always work (no dependencies)
- **CLI Mode Issues** → Check `az login` and `az account show`
- **SERVICE_PRINCIPAL Issues** → Verify credentials in Azure Portal
- **OpenAI Issues** → Check API key at https://platform.openai.com

---

**🚀 Ready to run?** Choose your mode above and follow the steps!

*Last updated: October 2025*
