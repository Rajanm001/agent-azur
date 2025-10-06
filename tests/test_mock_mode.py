
# © Rajan Mishra — 2025
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.path.dirname(__file__))))

def test_azure_client_mock():
    os.environ["AZURE_AUTH_MODE"] = "MOCK"
    from src.services.azure_client import AzureClient
    client = AzureClient()
    assert client.mode == "MOCK"
    assert client.auth_method == "MOCK Mode"

def test_vm_list_mock():
    os.environ["AZURE_AUTH_MODE"] = "MOCK"
    from src.services.azure_client import AzureClient
    client = AzureClient()
    vms = client.get_vm_list()
    assert "value" in vms
    assert vms["simulation"] == True
    assert len(vms["value"]) >= 2

def test_nsg_rules_mock():
    os.environ["AZURE_AUTH_MODE"] = "MOCK"
    from src.services.azure_client import AzureClient
    client = AzureClient()
    rules = client.get_nsg_rules()
    assert "value" in rules
    assert rules["simulation"] == True
