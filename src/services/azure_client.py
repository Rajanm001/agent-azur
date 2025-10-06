"""
© Rajan AI — 2025
Agentic AI for Azure Supportability Test
"""
"""
Azure Client Service - Multi-Mode Authentication Support
Supports 3 modes: MOCK (offline), CLI (az login), SERVICE_PRINCIPAL (secrets)
"""
import os
import requests
import subprocess
from dotenv import load_dotenv
from azure.identity import AzureCliCredential, ClientSecretCredential
from typing import Dict, Any, Optional
import structlog

load_dotenv()
logger = structlog.get_logger()


class AzureClient:
    """
    Azure Client with 3 authentication modes:
    1. MOCK - Local simulation (no Azure connection)
    2. CLI - Use `az login` session (no secrets needed)
    3. SERVICE_PRINCIPAL - Full auth with secrets (production)
    
    Set AZURE_AUTH_MODE environment variable to force a mode:
    - AZURE_AUTH_MODE=MOCK (offline testing)
    - AZURE_AUTH_MODE=CLI (use Azure CLI login)
    - AZURE_AUTH_MODE=SERVICE_PRINCIPAL (use secrets)
    - AZURE_AUTH_MODE=AUTO (default - auto-detect)
    """
    
    def __init__(self):
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "demo-subscription-12345")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        
        # Determine authentication mode
        self.mode = os.getenv("AZURE_AUTH_MODE", "AUTO").upper()
        
        if self.mode == "AUTO":
            self.mode = self._detect_mode()
        
        logger.info(f"🚀 Initializing Azure Client", mode=self.mode)
        
        # Initialize based on mode
        if self.mode == "MOCK":
            self._init_mock_mode()
        elif self.mode == "CLI":
            self._init_cli_mode()
        elif self.mode == "SERVICE_PRINCIPAL":
            self._init_service_principal_mode()
        else:
            logger.warning(f"⚠️  Unknown mode '{self.mode}', falling back to MOCK")
            self._init_mock_mode()
    
    def _detect_mode(self) -> str:
        """Auto-detect authentication mode based on environment."""
        # Check if Service Principal credentials exist
        if all([self.tenant_id, self.client_id, self.client_secret]):
            logger.info("🔍 Detected Service Principal credentials")
            return "SERVICE_PRINCIPAL"
        
        # Check if Azure CLI is logged in
        try:
            result = subprocess.run(
                ["az", "account", "show"], 
                capture_output=True, 
                timeout=5,
                text=True
            )
            if result.returncode == 0:
                logger.info("🔍 Detected Azure CLI login")
                return "CLI"
        except FileNotFoundError:
            logger.debug("Azure CLI not installed")
        except Exception as e:
            logger.debug(f"Azure CLI check failed: {e}")
        
        # Fallback to mock mode
        logger.warning("⚠️  No Azure credentials found, using MOCK mode")
        return "MOCK"
    
    def _init_mock_mode(self):
        """Initialize in mock mode (no Azure connection)."""
        self.credential = None
        self.auth_method = "MOCK Mode"
        logger.info("✅ Mock mode initialized - using simulated data")
        logger.info("💡 TIP: Set AZURE_AUTH_MODE=CLI to use real Azure (after 'az login')")
    
    def _init_cli_mode(self):
        """Initialize using Azure CLI credentials."""
        try:
            self.credential = AzureCliCredential()
            # Test the credential
            token = self.credential.get_token("https://management.azure.com/.default")
            if token:
                self.auth_method = "Azure CLI"
                logger.info("✅ Azure CLI authentication successful", subscription_id=self.subscription_id)
            else:
                raise Exception("Token acquisition failed")
        except Exception as e:
            logger.error(f"❌ Azure CLI authentication failed: {e}")
            logger.warning("💡 Run 'az login' first, then try again")
            logger.warning("Falling back to MOCK mode")
            self._init_mock_mode()
    
    def _init_service_principal_mode(self):
        """Initialize using Service Principal credentials."""
        try:
            self.credential = ClientSecretCredential(
                tenant_id=self.tenant_id or "",
                client_id=self.client_id or "",
                client_secret=self.client_secret or ""
            )
            # Test the credential
            token = self.credential.get_token("https://management.azure.com/.default")
            if token:
                self.auth_method = "Service Principal"
                logger.info("✅ Service Principal authentication successful", subscription_id=self.subscription_id)
            else:
                raise Exception("Token acquisition failed")
        except Exception as e:
            logger.error(f"❌ Service Principal authentication failed: {e}")
            logger.warning("Falling back to MOCK mode")
            self._init_mock_mode()
    
    def _get_token(self) -> Optional[str]:
        """Get Azure access token."""
        if self.credential:
            try:
                token = self.credential.get_token("https://management.azure.com/.default")
                return token.token
            except Exception as e:
                logger.error(f"❌ Token acquisition failed: {e}")
                return None
        return None
    
    def get_vm_list(self) -> Dict[str, Any]:
        """Fetch list of VMs in the subscription."""
        # MOCK MODE - Return simulated data
        if self.mode == "MOCK" or not self.credential:
            logger.info("📦 MOCK MODE: Returning simulated VMs")
            return {
                "value": [
                    {
                        "name": "vm-web-01",
                        "location": "eastus",
                        "properties": {
                            "hardwareProfile": {"vmSize": "Standard_DS2_v2"},
                            "provisioningState": "Succeeded",
                            "powerState": "running",
                            "networkProfile": {
                                "networkInterfaces": [
                                    {"id": "/subscriptions/.../networkInterfaces/vm-web-01-nic"}
                                ]
                            }
                        },
                        "tags": {"environment": "production", "app": "web"}
                    },
                    {
                        "name": "vm-db-01",
                        "location": "eastus",
                        "properties": {
                            "hardwareProfile": {"vmSize": "Standard_E4s_v3"},
                            "provisioningState": "Succeeded",
                            "powerState": "stopped",
                            "networkProfile": {
                                "networkInterfaces": [
                                    {"id": "/subscriptions/.../networkInterfaces/vm-db-01-nic"}
                                ]
                            }
                        },
                        "tags": {"environment": "production", "app": "database"}
                    }
                ],
                "count": 2,
                "simulation": True,
                "mode": "MOCK"
            }
        
        # REAL AZURE MODE - Call Azure API
        token = self._get_token()
        if not token:
            logger.error("❌ Failed to get Azure token")
            return {"error": "Authentication failed", "simulation": False}
        
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/providers/Microsoft.Compute/virtualMachines?api-version=2023-09-01"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            logger.info("🌐 Calling Azure API to fetch VMs...")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                data["simulation"] = False
                data["mode"] = self.mode
                vm_count = len(data.get("value", []))
                logger.info(f"✅ Successfully fetched {vm_count} VMs from Azure")
                return data
            else:
                logger.error(f"❌ Azure API returned {response.status_code}: {response.text}")
                return {
                    "error": f"Azure API returned {response.status_code}",
                    "message": response.text,
                    "simulation": False
                }
        except Exception as e:
            logger.error(f"❌ Failed to fetch VMs: {e}")
            return {
                "error": "Failed to fetch VMs",
                "message": str(e),
                "simulation": False
            }
    
    def get_nsg_rules(self, resource_group: str = "rg-demo", nsg_name: str = "vm-web-01-nsg") -> Dict[str, Any]:
        """Fetch Network Security Group rules."""
        # MOCK MODE - Return simulated NSG rules (missing RDP rule)
        if self.mode == "MOCK" or not self.credential:
            logger.info(f"📦 MOCK MODE: Returning simulated NSG rules for {nsg_name}")
            return {
                "value": [
                    {
                        "name": "default-allow-ssh",
                        "properties": {
                            "priority": 1000,
                            "direction": "Inbound",
                            "access": "Allow",
                            "protocol": "TCP",
                            "sourcePortRange": "*",
                            "destinationPortRange": "22",
                            "sourceAddressPrefix": "*",
                            "destinationAddressPrefix": "*"
                        }
                    },
                    {
                        "name": "allow-https",
                        "properties": {
                            "priority": 1010,
                            "direction": "Inbound",
                            "access": "Allow",
                            "protocol": "TCP",
                            "sourcePortRange": "*",
                            "destinationPortRange": "443",
                            "sourceAddressPrefix": "*",
                            "destinationAddressPrefix": "*"
                        }
                    }
                    # NOTE: No RDP (3389) rule - simulating the problem!
                ],
                "simulation": True,
                "mode": "MOCK",
                "issue": "RDP port 3389 is NOT in NSG rules"
            }
        
        # REAL AZURE MODE
        token = self._get_token()
        if not token:
            return {"error": "Authentication failed"}
        
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/networkSecurityGroups/{nsg_name}?api-version=2023-05-01"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                rules = data.get("properties", {}).get("securityRules", [])
                logger.info(f"✅ Fetched {len(rules)} NSG rules")
                return {"value": rules, "simulation": False, "mode": self.mode}
            else:
                logger.error(f"❌ NSG API returned {response.status_code}")
                return {"error": response.text, "simulation": False}
        except Exception as e:
            logger.error(f"❌ Failed to fetch NSG rules: {e}")
            return {"error": str(e), "simulation": False}
    
    def add_nsg_rule_for_rdp(self, resource_group: str = "rg-demo", nsg_name: str = "vm-web-01-nsg") -> Dict[str, Any]:
        """Add NSG rule to allow RDP (port 3389)."""
        # MOCK MODE - Simulate success
        if self.mode == "MOCK" or not self.credential:
            logger.info(f"📦 MOCK MODE: Simulating NSG rule addition for RDP (port 3389)")
            return {
                "success": True,
                "message": "✅ Would add NSG rule 'Allow-RDP-3389' with priority 100",
                "simulation": True,
                "mode": "MOCK",
                "rule_name": "Allow-RDP-3389",
                "port": 3389,
                "priority": 100
            }
        
        # REAL AZURE MODE - Add the rule via Azure API
        token = self._get_token()
        if not token:
            return {"success": False, "error": "Authentication failed"}
        
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/networkSecurityGroups/{nsg_name}/securityRules/Allow-RDP-3389?api-version=2023-05-01"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "properties": {
                "priority": 100,
                "direction": "Inbound",
                "access": "Allow",
                "protocol": "TCP",
                "sourcePortRange": "*",
                "destinationPortRange": "3389",
                "sourceAddressPrefix": "*",
                "destinationAddressPrefix": "*",
                "description": "Allow RDP from anywhere (added by AI agent)"
            }
        }
        
        try:
            logger.info("🌐 Adding NSG rule via Azure API...")
            response = requests.put(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code in [200, 201]:
                logger.info("✅ Successfully added NSG rule for RDP")
                return {
                    "success": True,
                    "message": "NSG rule added successfully",
                    "simulation": False,
                    "mode": self.mode,
                    "rule_name": "Allow-RDP-3389",
                    "port": 3389
                }
            else:
                logger.error(f"❌ Failed to add NSG rule: {response.status_code}")
                return {
                    "success": False,
                    "error": f"Azure API returned {response.status_code}",
                    "message": response.text
                }
        except Exception as e:
            logger.error(f"❌ Exception while adding NSG rule: {e}")
            return {"success": False, "error": str(e)}
    
    def get_resource_groups(self) -> Dict[str, Any]:
        """Fetch list of resource groups."""
        if self.mode == "MOCK" or not self.credential:
            return {
                "value": [
                    {"name": "rg-production", "location": "eastus"},
                    {"name": "rg-development", "location": "westus"}
                ],
                "simulation": True
            }
        
        token = self._get_token()
        if not token:
            return {"error": "Authentication failed"}
        
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourcegroups?api-version=2021-04-01"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                data["simulation"] = False
                return data
            else:
                return {"error": response.text, "simulation": False}
        except Exception as e:
            return {"error": str(e), "simulation": False}
    
    def get_subscription_info(self) -> Dict[str, Any]:
        """Get subscription and authentication details."""
        return {
            "subscriptionId": self.subscription_id,
            "tenantId": self.tenant_id,
            "authMethod": self.auth_method,
            "mode": self.mode,
            "authenticated": self.credential is not None
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Azure connection and return status."""
        if self.mode == "MOCK":
            return {
                "status": "ok",
                "mode": "MOCK",
                "message": "✅ Mock mode active - no Azure connection needed",
                "tip": "Set AZURE_AUTH_MODE=CLI to use real Azure (after 'az login')"
            }
        
        token = self._get_token()
        if token:
            return {
                "status": "ok",
                "mode": self.mode,
                "message": f"✅ Azure connection successful via {self.auth_method}",
                "authenticated": True
            }
        else:
            return {
                "status": "error",
                "mode": self.mode,
                "message": f"❌ Azure authentication failed",
                "authenticated": False
            }
