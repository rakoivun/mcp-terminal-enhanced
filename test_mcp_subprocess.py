#!/usr/bin/env python3
"""
Test MCP subprocess execution to isolate the framework-specific issue
"""
import asyncio
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create minimal MCP server
mcp = FastMCP("test-subprocess", log_level="INFO")

@mcp.tool()
async def test_simple_command(command: str = "echo test") -> str:
    """Test simple command execution within MCP context"""
    print(f"[MCP Test] Executing: {command}", file=__import__('sys').stderr)
    start_time = datetime.now()
    
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
            shell=True
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
        duration = datetime.now() - start_time
        
        result = f"SUCCESS in {duration}\nstdout: {stdout.decode().strip()}\nstderr: {stderr.decode().strip()}\nreturn_code: {process.returncode}"
        print(f"[MCP Test] {result}", file=__import__('sys').stderr)
        return result
        
    except asyncio.TimeoutError:
        result = f"TIMEOUT after 5 seconds"
        print(f"[MCP Test] {result}", file=__import__('sys').stderr)
        return result
    except Exception as e:
        result = f"ERROR: {e}"
        print(f"[MCP Test] {result}", file=__import__('sys').stderr)
        return result

def main():
    """Run the test MCP server"""
    print("Starting test MCP server...", file=__import__('sys').stderr)
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()