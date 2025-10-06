"""
© Rajan AI — 2025
Agentic AI for Azure Supportability Test
"""
"""
Main Application - Azure Diagnostic AI Agent
Orchestrates Azure data fetching, AI analysis, and resolution generation
"""
import os
import sys
import time
import codecs
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Fix Windows console encoding for Unicode support
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.diagnostic_agent import DiagnosticAgent
from src.agents.resolution_agent import ResolutionAgent
from src.services.azure_client import AzureClient
from src.utils.logger import log

# Load environment variables
load_dotenv()

# Check if running in mock mode
MOCK_MODE = os.getenv('MOCK_MODE', '0').lower() in ('1', 'true', 'yes')

# Prometheus Metrics
agent_runs = Counter('agent_runs_total', 'Total times the agent has run')
agent_errors = Counter('agent_errors_total', 'Total errors encountered')
vms_monitored = Gauge('azure_vms_monitored', 'Number of Azure VMs being monitored')
analysis_duration = Histogram('analysis_duration_seconds', 'Time spent on AI analysis')


def print_banner():
    """Display the application banner."""
    banner = """
====================================================================
  RAJAN AI - AGENTIC AZURE SUPPORTABILITY TEST
  Windows VM RDP (Port 3389) Troubleshooter
====================================================================
"""
    print(banner)


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def main():
    """Main application entry point"""
    
    print_banner()
    
    log.info("system.start", message="Starting Azure Diagnostic AI Agent")
    
    # Start Prometheus metrics server
    try:
        metrics_port = 8000
        start_http_server(metrics_port)
        log.info("metrics.started", port=metrics_port)
        print(f"\n[METRICS] Server started on http://localhost:{metrics_port}")
    except Exception as e:
        log.warning("metrics.failed", error=str(e))
        print(f"\n[WARNING] Metrics server failed to start: {e}")
    
    # Initialize components
    print_section("[INIT] Initializing Components")
    
    try:
        azure_client = AzureClient()
        print(f"[OK] Azure Client initialized")
        print(f"   Auth Method: {azure_client.auth_method}")
        print(f"   Subscription: {azure_client.subscription_id}")
        
        # Initialize agents (skip in mock mode to avoid OpenAI API calls)
        if MOCK_MODE:
            print("📦 MOCK MODE: Skipping AI agent initialization")
            diagnostic_agent = None
            resolution_agent = None
        else:
            diagnostic_agent = DiagnosticAgent()
            print(f"✅ Diagnostic Agent initialized (Model: {diagnostic_agent.model})")
            
            resolution_agent = ResolutionAgent()
            print(f"✅ Resolution Agent initialized (Model: {resolution_agent.model})")
        
    except Exception as e:
        log.error("initialization.failed", error=str(e))
        print(f"\n❌ Initialization failed: {e}")
        print("\nPlease check:")
        print("  1. .env file has OPENAI_API_KEY")
        print("  2. Azure credentials are set (or run 'az login')")
        return
    
    # Main execution loop
    try:
        agent_runs.inc()
        
        # Fetch Azure Data
        print_section("[AZURE] Fetching Azure Resource Data")
        
        start_time = time.time()
        
        subscription_info = azure_client.get_subscription_info()
        log.info("azure.subscription_info", info=subscription_info)
        
        vm_data = azure_client.get_vm_list()
        fetch_duration = time.time() - start_time
        
        # Initialize vm_count with default value
        vm_count = 0
        
        if vm_data.get("error"):
            print(f"[ERROR] Error fetching VMs: {vm_data.get('message')}")
            log.error("azure.fetch_failed", error=vm_data)
        else:
            vm_count = len(vm_data.get("value", []))
            vms_monitored.set(vm_count)
            
            is_simulation = vm_data.get("simulation", False)
            mode_indicator = "🔵 SIMULATION MODE" if is_simulation else "🟢 LIVE DATA"
            
            print(f"{mode_indicator}")
            print(f"[OK] Fetched {vm_count} VMs in {fetch_duration:.2f}s")
            
            log.info("azure.data_fetched", 
                     vm_count=vm_count,
                     simulation=is_simulation,
                     duration_seconds=fetch_duration)
            
            # Quick health check
            # Quick health analysis
        if MOCK_MODE:
            health = {"total": 2, "running": 1, "stopped": 1, "issues": 1}
        else:
            health = diagnostic_agent.quick_health_check(vm_data) if diagnostic_agent else {}
            print(f"\n[INFO] Quick Health Check:")
            print(f"   Total VMs: {health['total_vms']}")
            print(f"   Running: {health['running_vms']}")
            print(f"   Stopped: {health['stopped_vms']}")
            print(f"   Regions: {', '.join(health['locations'])}")
            if health['issues']:
                print(f"   [WARNING] Issues found: {len(health['issues'])}")
        
        # AI Diagnostic Analysis
        print_section("🧠 Running AI Diagnostic Analysis")
        
        if MOCK_MODE:
            print("📦 MOCK MODE: Using simulated AI analysis...")
            diagnostic_summary = "Mock diagnostic analysis completed. Found 1 VM stopped (vm-db-01) and potential NSG issues for RDP access on vm-web-01."
        else:
            print("⏳ Analyzing with OpenAI GPT-4o-mini...")
            with analysis_duration.time():
                diagnostic_summary = diagnostic_agent.analyze(vm_data) if diagnostic_agent else "No diagnostic agent available"
        
        print("\n" + "─" * 70)
        print("📋 DIAGNOSTIC REPORT")
        print("─" * 70)
        print(diagnostic_summary)
        print("─" * 70)
        
        log.info("diagnostic.completed", summary_length=len(diagnostic_summary))
        
        # Generate Resolution Steps
        print_section("🔧 Generating Resolution Steps")
        
        if MOCK_MODE:
            print("📦 MOCK MODE: Using simulated resolution steps...")
            resolution_steps = "Mock resolution steps: 1) Start vm-db-01 if needed, 2) Add NSG rule for RDP (port 3389) on vm-web-01, 3) Validate connectivity."
        else:
            print("⏳ Generating fixes with AI...")
            resolution_steps = resolution_agent.suggest_fixes(diagnostic_summary) if resolution_agent else "No resolution agent available"
        
        print("\n" + "─" * 70)
        print("[ACTION PLAN] RECOMMENDED FIXES & ACTION PLAN")
        print("─" * 70)
        print(resolution_steps)
        print("─" * 70)
        
        log.info("resolution.completed", steps_length=len(resolution_steps))
        
        # Summary
        print_section("[SUMMARY] Execution Summary")
        print(f"✓ Azure data fetched successfully")
        print(f"✓ AI diagnostic analysis completed")
        print(f"✓ Resolution steps generated")
        print(f"\n[METRICS] Metrics available at: http://localhost:8000")
        print(f"📝 All actions logged in JSON format")
        
        log.info("system.completed",
                 status="success",
                 vms_analyzed=vm_count,
                 total_duration_seconds=time.time() - start_time)
        
    except KeyboardInterrupt:
        log.info("system.interrupted", reason="User interrupted")
        print("\n\n[WARNING] Interrupted by user")
        
    except Exception as e:
        agent_errors.inc()
        log.error("system.error", error=str(e), error_type=type(e).__name__)
        print(f"\n\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Keep metrics server running
    print("\n" + "="*70)
    print("🔄 Agent run complete. Metrics server still running...")
    print("   Press Ctrl+C to exit")
    print("="*70 + "\n")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        log.info("system.shutdown", reason="User exit")


if __name__ == "__main__":
    main()
