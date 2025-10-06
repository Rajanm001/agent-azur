"""
© Rajan AI — 2025
Agentic AI for Azure Supportability Test
"""
"""
Diagnostic Agent - Analyzes Azure resource data using OpenAI
"""
from openai import OpenAI
import os
import json
from typing import Dict, Any

# Import logger from utils
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.logger import log


class DiagnosticAgent:
    """
    AI-powered diagnostic agent that analyzes Azure resource data
    and identifies potential issues, optimization opportunities, and risks
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using cost-effective model
        
        log.info("diagnostic_agent.initialized", model=self.model)
    
    def analyze(self, azure_data: Dict[str, Any]) -> str:
        """
        Analyze Azure resource data and provide diagnostic insights
        
        Args:
            azure_data: Dictionary containing Azure resource information
            
        Returns:
            AI-generated diagnostic analysis as string
        """
        log.info("diagnostic_agent.analysis_start", 
                 resource_count=azure_data.get("count", 0),
                 simulation=azure_data.get("simulation", False))
        
        # Prepare data for AI analysis
        data_summary = self._prepare_data_summary(azure_data)
        
        # Create analysis prompt
        prompt = f"""
You are an expert Azure Cloud Architect and Site Reliability Engineer.
Analyze the following Azure infrastructure data and provide a comprehensive diagnostic report.

Azure Resource Data:
{data_summary}

Please provide:
1. Health Assessment: Overall health status of the infrastructure
2. Configuration Issues: Any misconfigurations or suboptimal settings
3. Performance Concerns: Potential performance bottlenecks
4. Security Risks: Security vulnerabilities or compliance issues
5. Cost Optimization: Opportunities to reduce costs
6. Recommendations: Top 3-5 actionable recommendations

Format your response in a clear, structured manner suitable for technical and non-technical stakeholders.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Azure cloud architect specializing in infrastructure diagnostics, performance optimization, and security."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content or ""
            
            # Safe token usage extraction
            tokens_used = getattr(response.usage, "total_tokens", 0) if response.usage else 0
            
            log.info("diagnostic_agent.analysis_complete",
                     tokens_used=tokens_used,
                     model=self.model)
            
            return result
            
        except Exception as e:
            log.error("diagnostic_agent.analysis_failed", error=str(e))
            return f"⚠️ Analysis failed: {str(e)}"
    
    def _prepare_data_summary(self, azure_data: Dict[str, Any]) -> str:
        """Prepare a formatted summary of Azure data for AI analysis"""
        
        if azure_data.get("error"):
            return f"Error fetching data: {azure_data.get('message', 'Unknown error')}"
        
        summary_parts = []
        
        # Add simulation mode indicator
        if azure_data.get("simulation"):
            summary_parts.append("⚠️ Running in SIMULATION MODE (using mock data)\n")
        
        # Summarize VMs
        vms = azure_data.get("value", [])
        summary_parts.append(f"Total VMs: {len(vms)}")
        
        for idx, vm in enumerate(vms, 1):
            vm_info = f"""
VM {idx}: {vm.get('name', 'Unknown')}
- Location: {vm.get('location', 'N/A')}
- Size: {vm.get('properties', {}).get('hardwareProfile', {}).get('vmSize', 'N/A')}
- State: {vm.get('properties', {}).get('powerState', 'N/A')}
- Tags: {json.dumps(vm.get('tags', {}), indent=2)}
"""
            summary_parts.append(vm_info)
        
        return "\n".join(summary_parts)
    
    def quick_health_check(self, azure_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a quick health check without AI (for testing/metrics)
        """
        vms = azure_data.get("value", [])
        
        health = {
            "total_vms": len(vms),
            "running_vms": 0,
            "stopped_vms": 0,
            "locations": set(),
            "issues": []
        }
        
        for vm in vms:
            power_state = vm.get("properties", {}).get("powerState", "unknown")
            if power_state == "running":
                health["running_vms"] += 1
            else:
                health["stopped_vms"] += 1
            
            location = vm.get("location")
            if location:
                health["locations"].add(location)
        
        health["locations"] = list(health["locations"])
        
        # Simple heuristics
        if health["stopped_vms"] > 0:
            health["issues"].append(f"{health['stopped_vms']} VMs are not running")
        
        if len(health["locations"]) > 3:
            health["issues"].append(f"Resources spread across {len(health['locations'])} regions - consider consolidation")
        
        return health
