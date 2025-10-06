#!/usr/bin/env python3
"""
© Rajan Mishra — 2025
Quick Setup & Test Script
Sets up environment and runs basic validation tests
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_cmd(cmd, cwd=None):
    """Run command and return result."""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    """Main setup and validation."""
    print("🚀 Rajan Mishra - Quick Setup & Validation")
    print("="*50)
    
    # 1. Create virtual environment if needed
    venv_dir = ROOT / ".venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        if not run_cmd([sys.executable, "-m", "venv", str(venv_dir)]):
            return False
    
    # 2. Get Python and pip paths
    if os.name == "nt":
        python_path = venv_dir / "Scripts" / "python.exe"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        python_path = venv_dir / "bin" / "python"
        pip_path = venv_dir / "bin" / "pip"
    
    # 3. Install requirements
    print("Installing requirements...")
    if not run_cmd([str(pip_path), "install", "--upgrade", "pip"]):
        return False
    
    requirements = ROOT / "requirements.txt"
    if requirements.exists():
        if not run_cmd([str(pip_path), "install", "-r", str(requirements)]):
            return False
    
    # 4. Test imports
    print("Testing imports...")
    test_imports = [
        "import structlog",
        "import prometheus_client", 
        "from src.services.azure_client import AzureClient",
        "from src.agents.diagnostic_agent import DiagnosticAgent"
    ]
    
    for import_stmt in test_imports:
        if not run_cmd([str(python_path), "-c", import_stmt]):
            print(f"❌ Import failed: {import_stmt}")
            return False
        print(f"✅ {import_stmt}")
    
    # 5. Run quick test
    print("Running quick test in MOCK mode...")
    env = {**os.environ, "AZURE_AUTH_MODE": "MOCK", "PYTHONUNBUFFERED": "1"}
    
    proc = subprocess.Popen(
        [str(python_path), "src/main.py"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        output, _ = proc.communicate(timeout=30)
        print("Application output:")
        print(output)
        
        if "Azure Client initialized" in output:
            print("✅ Application runs successfully")
            return True
        else:
            print("❌ Application output incomplete")
            return False
            
    except subprocess.TimeoutExpired:
        proc.kill()
        print("❌ Application timed out")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Setup complete! Ready to run comprehensive validation.")
        print("Next step: python tools/comprehensive_validation.py")
    else:
        print("\n❌ Setup failed. Please check errors above.")
    sys.exit(0 if success else 1)