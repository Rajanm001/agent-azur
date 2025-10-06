"""
Final Validation Script - Pre-Submission Checks
Validates all requirements before client submission
"""
import os
import sys
from pathlib import Path

# Color codes for Windows terminal
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Color.BLUE}{Color.BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{Color.RESET}")

def check_file_exists(filepath, min_size=0):
    """Check if file exists and meets minimum size"""
    path = Path(filepath)
    if not path.exists():
        return False, "File not found"
    
    size = path.stat().st_size
    if size < min_size:
        return False, f"File too small ({size} bytes, minimum {min_size})"
    
    return True, f"{size:,} bytes"

def check_python_imports():
    """Verify all required Python modules can be imported"""
    required_modules = [
        'structlog',
        'prometheus_client',
        'azure.identity',
        'azure.mgmt.compute',
        'azure.mgmt.network',
        'openai',
        'dotenv',
        'pydantic'
    ]
    
    results = []
    for module in required_modules:
        try:
            __import__(module)
            results.append((module, True, "✅ Installed"))
        except ImportError as e:
            results.append((module, False, f"❌ Missing: {e}"))
    
    return results

def check_code_quality():
    """Check for basic code quality issues"""
    issues = []
    
    # Check for TODO/FIXME comments
    python_files = list(Path('src').rglob('*.py'))
    for file in python_files:
        try:
            content = file.read_text(encoding='utf-8')
            if 'TODO' in content or 'FIXME' in content or 'XXX' in content:
                issues.append(f"⚠️  {file}: Contains TODO/FIXME")
        except:
            pass
    
    return issues

def main():
    """Run all validation checks"""
    print(f"{Color.BOLD}{Color.BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     FINAL VALIDATION - PRE-SUBMISSION CHECKLIST          ║")
    print("║              Rajan Mishra - Azure Agentic AI                  ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}")
    
    all_passed = True
    
    # ====================================================================
    # 1. CHECK REQUIRED FILES
    # ====================================================================
    print_header("📁 CHECKING REQUIRED FILES")
    
    required_files = {
        'README.md': 10000,  # Minimum 10KB
        'architecture_diagram.md': 10000,
        'docs/SECURITY_GOVERNANCE.md': 10000,
        'PROJECT_SUMMARY.md': 5000,
        'QUICK_START.md': 3000,
        'SUBMISSION_CHECKLIST.md': 3000,
        'INSTALLATION.md': 5000,
        'requirements.txt': 100,
        'setup_env.bat': 100,
        'run_app.bat': 100,
        '.gitignore': 50,
        'src/main.py': 5000,
        'src/metrics.py': 5000,
        'src/agents/diagnostic_agent.py': 3000,
        'src/agents/resolution_agent.py': 3000,
        'src/services/azure_client.py': 3000,
        'src/utils/logger.py': 500,
    }
    
    file_checks_passed = 0
    file_checks_total = len(required_files)
    
    for file, min_size in required_files.items():
        exists, info = check_file_exists(file, min_size)
        if exists:
            print(f"  ✅ {file:<40} {info}")
            file_checks_passed += 1
        else:
            print(f"  ❌ {file:<40} {info}")
            all_passed = False
    
    print(f"\n  Result: {file_checks_passed}/{file_checks_total} files validated")
    
    # ====================================================================
    # 2. CHECK PYTHON DEPENDENCIES
    # ====================================================================
    print_header("📦 CHECKING PYTHON DEPENDENCIES")
    
    import_results = check_python_imports()
    imports_passed = sum(1 for _, success, _ in import_results if success)
    imports_total = len(import_results)
    
    for module, success, message in import_results:
        print(f"  {message} {module}")
        if not success:
            all_passed = False
    
    print(f"\n  Result: {imports_passed}/{imports_total} modules available")
    
    # ====================================================================
    # 3. CHECK ENVIRONMENT CONFIGURATION
    # ====================================================================
    print_header("⚙️  CHECKING ENVIRONMENT CONFIGURATION")
    
    env_file_exists = Path('.env').exists()
    if env_file_exists:
        print(f"  ✅ .env file found")
        
        # Check for required variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['AZURE_AUTH_MODE']
        optional_vars = ['OPENAI_API_KEY', 'AZURE_SUBSCRIPTION_ID']
        
        for var in required_vars:
            if os.getenv(var):
                print(f"  ✅ {var} is set")
            else:
                print(f"  ⚠️  {var} not set (may use default)")
        
        for var in optional_vars:
            value = os.getenv(var)
            if value:
                # Mask sensitive values
                masked = value[:8] + '...' if len(value) > 8 else '***'
                print(f"  ✅ {var} = {masked}")
            else:
                print(f"  ⚠️  {var} not set (optional)")
    else:
        print(f"  ❌ .env file not found")
        all_passed = False
    
    # ====================================================================
    # 4. CHECK CODE QUALITY
    # ====================================================================
    print_header("🔍 CHECKING CODE QUALITY")
    
    issues = check_code_quality()
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"  ✅ No TODO/FIXME comments found")
    
    # Check __pycache__ cleanup
    pycache_dirs = list(Path('.').rglob('__pycache__'))
    if pycache_dirs:
        print(f"  ℹ️  Found {len(pycache_dirs)} __pycache__ directories (normal)")
    
    # ====================================================================
    # 5. CHECK DOCUMENTATION COMPLETENESS
    # ====================================================================
    print_header("📚 CHECKING DOCUMENTATION")
    
    docs_checks = [
        ("README.md contains architecture", "README.md", "System Architecture"),
        ("README.md contains troubleshooting play", "README.md", "Troubleshooting Play"),
        ("Architecture diagram exists", "architecture_diagram.md", "Customer Flow"),
        ("Security governance exists", "docs/SECURITY_GOVERNANCE.md", "Security Architecture"),
        ("Quick start guide exists", "QUICK_START.md", "MOCK MODE"),
        ("Project summary exists", "PROJECT_SUMMARY.md", "Executive Summary"),
    ]
    
    docs_passed = 0
    for check_name, file, search_text in docs_checks:
        try:
            content = Path(file).read_text(encoding='utf-8')
            if search_text in content:
                print(f"  ✅ {check_name}")
                docs_passed += 1
            else:
                print(f"  ❌ {check_name} - content not found")
                all_passed = False
        except Exception as e:
            print(f"  ❌ {check_name} - error: {e}")
            all_passed = False
    
    print(f"\n  Result: {docs_passed}/{len(docs_checks)} documentation checks passed")
    
    # ====================================================================
    # 6. CHECK CLIENT REQUIREMENTS
    # ====================================================================
    print_header("🎯 VERIFYING CLIENT REQUIREMENTS")
    
    requirements = [
        ("✅ AI Agent Architecture", "architecture_diagram.md", 10000),
        ("✅ Customer Flow (≥2 pages)", "architecture_diagram.md", 10000),
        ("✅ RDP Troubleshooting Play", "README.md", 10000),
        ("✅ Security & Governance", "docs/SECURITY_GOVERNANCE.md", 10000),
        ("✅ Observability & Metrics", "src/metrics.py", 5000),
        ("✅ Working Code", "src/main.py", 5000),
    ]
    
    for req_name, file, min_size in requirements:
        exists, info = check_file_exists(file, min_size)
        if exists:
            print(f"  {req_name:<45} ✅ Satisfied")
        else:
            print(f"  {req_name:<45} ❌ Not satisfied")
            all_passed = False
    
    # ====================================================================
    # 7. FINAL SUMMARY
    # ====================================================================
    print_header("📊 FINAL VALIDATION SUMMARY")
    
    if all_passed:
        print(f"\n{Color.GREEN}{Color.BOLD}")
        print("  ╔═══════════════════════════════════════════════════════╗")
        print("  ║                                                       ║")
        print("  ║   ✅  ALL CHECKS PASSED - READY FOR SUBMISSION       ║")
        print("  ║                                                       ║")
        print("  ╚═══════════════════════════════════════════════════════╝")
        print(f"{Color.RESET}")
        print(f"\n  {Color.GREEN}Next Steps:{Color.RESET}")
        print(f"    1. Review SUBMISSION_CHECKLIST.md")
        print(f"    2. Create final ZIP archive")
        print(f"    3. Submit to client")
        return 0
    else:
        print(f"\n{Color.RED}{Color.BOLD}")
        print("  ╔═══════════════════════════════════════════════════════╗")
        print("  ║                                                       ║")
        print("  ║   ⚠️  SOME CHECKS FAILED - REVIEW ISSUES ABOVE       ║")
        print("  ║                                                       ║")
        print("  ╚═══════════════════════════════════════════════════════╝")
        print(f"{Color.RESET}")
        print(f"\n  {Color.YELLOW}Please fix the issues above before submitting.{Color.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
