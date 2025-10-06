"""
© Rajan AI — 2025
Agentic AI for Azure Supportability Test
"""
"""
Resolution Agent - Generates actionable fixes and remediation steps
"""
from openai import OpenAI
import os
from typing import Dict, Any, List

# Import logger
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.logger import log


class ResolutionAgent:
    """
    AI-powered resolution agent that generates actionable fixes
    and remediation steps based on diagnostic findings
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
        log.info("resolution_agent.initialized", model=self.model)
    
    def suggest_fixes(self, diagnostic_summary: str) -> str:
        """
        Generate resolution steps based on diagnostic findings
        
        Args:
            diagnostic_summary: The diagnostic analysis from DiagnosticAgent
            
        Returns:
            AI-generated resolution steps and fixes
        """
        log.info("resolution_agent.generation_start")
        
        prompt = f"""
You are an expert DevOps Engineer and Azure Solutions Architect.
Based on the following diagnostic analysis, provide detailed, actionable resolution steps.

Diagnostic Analysis:
{diagnostic_summary}

Please provide:
1. **Immediate Actions**: Steps that can be taken right now to address critical issues
2. **Short-term Fixes** (1-7 days): Tactical improvements
3. **Long-term Solutions** (1-3 months): Strategic improvements
4. **Automation Opportunities**: Tasks that can be automated
5. **Implementation Steps**: Detailed step-by-step instructions for each fix

For each recommendation, include:
- Priority level (Critical/High/Medium/Low)
- Estimated effort (hours/days)
- Required tools or services
- Expected impact
- Potential risks

Format your response clearly with numbered steps and bullet points.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert DevOps engineer specializing in Azure infrastructure automation, remediation, and optimization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content or ""
            
            # Safe token usage extraction
            tokens_used = getattr(response.usage, "total_tokens", 0) if response.usage else 0
            
            log.info("resolution_agent.generation_complete",
                     tokens_used=tokens_used,
                     model=self.model)
            
            return result
            
        except Exception as e:
            log.error("resolution_agent.generation_failed", error=str(e))
            return f"⚠️ Resolution generation failed: {str(e)}"
    
    def generate_automation_script(self, fix_description: str) -> Dict[str, Any]:
        """
        Generate automation scripts for a specific fix
        (Future enhancement)
        """
        log.info("resolution_agent.automation_generation", fix=fix_description)
        
        prompt = f"""
Generate Azure CLI or PowerShell commands to implement this fix:
{fix_description}

Provide:
1. The exact commands
2. Required permissions
3. Rollback procedure
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            script_content = response.choices[0].message.content or ""
            return {
                "script": script_content,
                "status": "generated"
            }
            
        except Exception as e:
            log.error("resolution_agent.automation_failed", error=str(e))
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def prioritize_fixes(self, fixes: List[str]) -> List[Dict[str, Any]]:
        """
        Prioritize a list of fixes based on impact and urgency
        """
        log.info("resolution_agent.prioritization_start", fix_count=len(fixes))
        
        prioritized = []
        for fix in fixes:
            # Simple heuristic prioritization
            priority = "Medium"
            if any(word in fix.lower() for word in ["critical", "security", "down", "failed"]):
                priority = "Critical"
            elif any(word in fix.lower() for word in ["performance", "slow", "timeout"]):
                priority = "High"
            elif any(word in fix.lower() for word in ["cost", "optimize", "unused"]):
                priority = "Low"
            
            prioritized.append({
                "fix": fix,
                "priority": priority
            })
        
        # Sort by priority
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        prioritized.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return prioritized
