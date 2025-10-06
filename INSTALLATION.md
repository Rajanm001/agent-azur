# Installation Guide - Agentic AI for Azure Supportability

Complete setup instructions for Windows, macOS, and Linux

---

## 📋 System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.11 or higher
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 500 MB for project + dependencies
- **Internet:** Required for Azure API and OpenAI

### Optional Requirements
- **Azure CLI:** For CLI authentication mode ([Download](https://aka.ms/installazurecli))
- **Azure Subscription:** For production use (MOCK mode works without)
- **OpenAI API Key:** For AI-powered diagnostics ([Get key](https://platform.openai.com/api-keys))

---

## 🚀 Quick Installation (5 Minutes)

### Windows (PowerShell)

```powershell
# 1. Navigate to project directory
cd "c:\Users\Rajan mishra Ji\assisngment 1"

# 2. Run automated setup
.\setup_env.bat

# 3. Configure credentials (opens notepad)
notepad .env

# 4. Add your credentials (at minimum):
# AZURE_AUTH_MODE=MOCK
# OPENAI_API_KEY=sk-proj-your-key-here

# 5. Run the application
.\run_app.bat
```

### macOS / Linux (Bash)

```bash
# 1. Navigate to project directory
cd ~/assisngment_1

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cat > .env << 'EOF'
AZURE_AUTH_MODE=MOCK
OPENAI_API_KEY=sk-proj-your-key-here
EOF

# 6. Run the application
python src/main.py
```

---

## 📦 Detailed Installation Steps

### Step 1: Verify Python Installation

```bash
# Check Python version (must be 3.11+)
python --version
# or
python3 --version

# Expected output:
# Python 3.11.0 (or higher)
```

**If Python not installed:**
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** `brew install python@3.11`
- **Linux:** `sudo apt install python3.11`

### Step 2: Clone or Download Project

```bash
# Option A: If using Git
git clone <repository-url>
cd assisngment_1

# Option B: If downloaded as ZIP
# Extract ZIP file
cd assisngment_1
```

### Step 3: Create Virtual Environment

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system Python
- Easy to delete and recreate

```bash
# Create virtual environment
python -m venv .venv

# Or on macOS/Linux:
python3 -m venv .venv
```

### Step 4: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Verify activation:** Your prompt should show `(.venv)` prefix:
```
(.venv) PS C:\Users\Rajan mishra Ji\assisngment 1>
```

### Step 5: Install Dependencies

```bash
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install all project dependencies
pip install -r requirements.txt

# Verify installation (should show all packages)
pip list
```

**Expected packages:**
```
Package                Version
---------------------- --------
azure-identity         1.25.0
azure-mgmt-compute     37.0.0
azure-mgmt-network     29.0.0
openai                 2.1.0
structlog              25.4.0
prometheus-client      0.23.1
pydantic               2.11.10
python-dotenv          1.1.1
```

### Step 6: Configure Environment Variables

Create `.env` file in project root:

```bash
# Windows
notepad .env

# macOS/Linux
nano .env
# or
vim .env
```

**Add the following content:**

#### Option A: MOCK Mode (No Azure Needed)
```env
# ============================================
# RAJAN AI - AZURE AGENTIC AI CONFIGURATION
# ============================================

# AUTHENTICATION MODE (choose one)
AZURE_AUTH_MODE=MOCK

# OPENAI CONFIGURATION
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7

# METRICS & LOGGING
METRICS_PORT=8000
LOG_LEVEL=INFO
```

#### Option B: Azure CLI Mode
```env
AZURE_AUTH_MODE=CLI
AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d

OPENAI_API_KEY=sk-proj-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7

METRICS_PORT=8000
LOG_LEVEL=INFO
```

#### Option C: Service Principal Mode (Production)
```env
AZURE_AUTH_MODE=SERVICE_PRINCIPAL
AZURE_SUBSCRIPTION_ID=76dfe244-9ff7-4423-90f8-2165d5ec144d
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

OPENAI_API_KEY=sk-proj-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7

METRICS_PORT=8000
LOG_LEVEL=INFO
```

**Security Note:** 
- ⚠️ Never commit `.env` file to Git
- ⚠️ Keep API keys and secrets confidential
- ✅ `.env` is already in `.gitignore`

---

## ✅ Verify Installation

### Test 1: Import Check
```bash
python -c "from src.services.azure_client import AzureClient; print('✅ Imports successful')"
```

### Test 2: Run Mock Mode
```bash
# Set environment variable for this session
# Windows PowerShell:
$env:AZURE_AUTH_MODE="MOCK"
python src/main.py

# macOS/Linux:
AZURE_AUTH_MODE=MOCK python src/main.py
```

**Expected output:**
```
====================================================================
  RAJAN AI - AGENTIC AZURE SUPPORTABILITY TEST
  Windows VM RDP (Port 3389) Troubleshooter
====================================================================

{"message": "Starting Azure Diagnostic AI Agent", "event": "system.start", ...}
✅ Metrics server started on http://localhost:8000
✅ Azure Client initialized (MOCK Mode)
✅ Diagnostic Agent initialized (gpt-4o-mini)
✅ Resolution Agent initialized (gpt-4o-mini)
```

### Test 3: Check Metrics Endpoint
```bash
# Open browser to:
http://localhost:8000

# Or using curl/PowerShell:
# PowerShell:
Invoke-WebRequest http://localhost:8000/metrics

# Bash:
curl http://localhost:8000/metrics
```

---

## 🔧 Troubleshooting

### Issue 1: "Python not found"
**Solution:**
```bash
# Windows: Add Python to PATH
# 1. Open System Properties → Environment Variables
# 2. Add: C:\Python311\Scripts and C:\Python311

# macOS/Linux: Use full path
/usr/local/bin/python3 --version
```

### Issue 2: "pip: command not found"
**Solution:**
```bash
# Use python -m pip instead
python -m pip install -r requirements.txt
```

### Issue 3: "ModuleNotFoundError: No module named 'structlog'"
**Solution:**
```bash
# Ensure virtual environment is activated
# Look for (.venv) in your prompt

# Then reinstall:
pip install -r requirements.txt
```

### Issue 4: "Cannot activate virtual environment (PowerShell)"
**Solution:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.venv\Scripts\Activate.ps1
```

### Issue 5: "Azure authentication failed"
**Solution:**
```bash
# For CLI mode:
az login
az account show

# For Service Principal: verify .env credentials
# For MOCK mode: should always work (no auth needed)
```

### Issue 6: "Port 8000 already in use"
**Solution:**
```bash
# Change port in .env file:
METRICS_PORT=8001

# Or kill existing process:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue 7: "OpenAI API key invalid"
**Solution:**
1. Verify key at: https://platform.openai.com/api-keys
2. Ensure key starts with `sk-proj-`
3. Check for extra spaces in `.env` file
4. Regenerate key if needed

---

## 🧪 Running Tests

### Run Mock Mode Tests
```bash
python tests/test_mock_mode.py
```

### Run Comprehensive Validation
```bash
python tools/comprehensive_validation.py
```

### Run All Verification Checks
```bash
python tools/verify_all.py
```

---

## 🔄 Updating Dependencies

### Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```bash
pip install --upgrade openai
```

### Freeze Current Versions
```bash
pip freeze > requirements.txt
```

---

## 🧹 Uninstallation

### Remove Virtual Environment
```bash
# Deactivate first
deactivate

# Delete virtual environment folder
# Windows:
Remove-Item -Recurse -Force .venv

# macOS/Linux:
rm -rf .venv
```

### Complete Cleanup
```bash
# Remove all generated files
# Windows PowerShell:
Remove-Item -Recurse -Force .venv, __pycache__, src/__pycache__, .pytest_cache

# macOS/Linux:
rm -rf .venv __pycache__ src/__pycache__ .pytest_cache
find . -name "*.pyc" -delete
```

---

## 📚 Next Steps

After installation:

1. ✅ Read [QUICK_START.md](./QUICK_START.md) - Learn the 3 authentication modes
2. ✅ Read [README.md](./README.md) - Understand the architecture
3. ✅ Read [architecture_diagram.md](./architecture_diagram.md) - See detailed flows
4. ✅ Run the application: `python src/main.py`
5. ✅ Check metrics: `http://localhost:8000/metrics`

---

## 💡 Pro Tips

### Tip 1: Use MOCK mode for demos
```bash
# No Azure/OpenAI needed for basic testing
AZURE_AUTH_MODE=MOCK python src/main.py
```

### Tip 2: Keep virtual environment active
```bash
# Add to your shell profile (~/.bashrc or PowerShell profile)
# Auto-activate when entering project directory
```

### Tip 3: Use environment-specific .env files
```bash
.env.development
.env.staging
.env.production

# Load specific one:
# Windows:
Get-Content .env.production | ForEach-Object { $env:$($_.Split('=')[0]) = $_.Split('=')[1] }
```

### Tip 4: Monitor logs in real-time
```bash
# Windows PowerShell:
python src/main.py | Select-String "ERROR"

# macOS/Linux:
python src/main.py | grep ERROR
```

---

## 📞 Support

**Installation Issues:**
- Check [Troubleshooting](#-troubleshooting) section above
- Verify Python version: `python --version`
- Verify pip works: `pip --version`
- Check virtual environment: Look for `(.venv)` in prompt

**Azure Authentication Issues:**
- See [QUICK_START.md](./QUICK_START.md) for detailed auth guide
- Use MOCK mode if no Azure access
- Verify `az login` for CLI mode

**OpenAI Issues:**
- Get free API key: https://platform.openai.com/api-keys
- Check usage limits in OpenAI dashboard
- Try MOCK mode without AI (simulated responses)

---

## ✅ Installation Checklist

Before running the application, verify:

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated (see `.venv` in prompt)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] `.env` file created with credentials
- [ ] AZURE_AUTH_MODE set (MOCK/CLI/SERVICE_PRINCIPAL)
- [ ] OPENAI_API_KEY set (if using AI)
- [ ] Test import successful: `python -c "from src.services.azure_client import AzureClient"`
- [ ] Application runs: `python src/main.py`
- [ ] Metrics accessible: http://localhost:8000

**All checked?** 🎉 You're ready to run the AI agent!

---

*Last Updated: October 6, 2025*  
*Version: 1.0*  
*Developer: Rajan AI*
