#!/usr/bin/env python3
"""
Deploy the MCP Server as a CML Application
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.functions.create_application import create_application
from server import get_config

def main():
    load_dotenv()
    
    # Get configuration (reuses logic from server.py which now supports CML env vars)
    config = get_config()
    
    if not config["host"] or not config["api_key"]:
        print("Error: Missing CLOUDERA_ML_HOST or CLOUDERA_ML_API_KEY")
        print("Or CDSW_DOMAIN / CDSW_APIV2_KEY if running in CML.")
        return 1
        
    project_id = config.get("project_id")
    if not project_id:
        print("Error: Missing CLOUDERA_ML_PROJECT_ID or CDSW_PROJECT_ID")
        return 1
        
    print(f"Deploying to project: {project_id} at {config['host']}")
    
    # Application parameters
    app_params = {
        "project_id": project_id,
        "name": "Cloudera MCP Server",
        "description": "MCP Server for Cloudera Machine Learning",
        "script": "cml_mcp_server.py",
        "cpu": 4,
        "memory": 16, 
        "nvidia_gpu": 0
    }
    
    # Create the application
    result = create_application(config, app_params)
    
    print(json.dumps(result, indent=2))
    
    if result.get("success"):
        print(f"\nApplication created successfully!")
        if "data" in result and "subdomain" in result["data"]:
             subdomain = result["data"]["subdomain"]
             # Construct URL roughly
             host_domain = config['host'].split('//')[1]
             print(f"Application URL: https://{subdomain}.{host_domain}")
    else:
        print("\nDeployment failed.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
