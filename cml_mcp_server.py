#!/usr/bin/env python3
"""
CML Application Entrypoint for Cloudera ML MCP Server
"""
import os
import sys

# Add current directory to path so we can import server
sys.path.append(os.getcwd())

from server import mcp

if __name__ == "__main__":
    # Get port from CML environment
    port = os.environ.get("CDSW_APP_PORT")
    if not port:
        print("Warning: CDSW_APP_PORT not found. Defaulting to 8080.")
        port = "8080"
    
    print(f"Starting MCP Server on port {port} (SSE)")
    
    # Run with SSE transport
    mcp.run(transport='sse', host='127.0.0.1', port=int(port))
