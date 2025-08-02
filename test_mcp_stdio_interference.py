#!/usr/bin/env python3
"""
Test MCP Framework STDIO interference hypothesis
Theory: MCP uses STDIO for communication, which interferes with subprocess STDIO
"""
import asyncio
import os
import sys
import subprocess

def test_subprocess_stdio_redirection():
    """Test how subprocess behaves with different STDIO configurations"""
    print("=== Testing subprocess STDIO configurations ===")
    
    tests = [
        ("Normal STDIO", None, None, None),
        ("Redirect stdout", subprocess.PIPE, None, None),
        ("Redirect stderr", None, subprocess.PIPE, None), 
        ("Redirect both", subprocess.PIPE, subprocess.PIPE, None),
        ("Redirect all", subprocess.PIPE, subprocess.PIPE, subprocess.PIPE),
        ("Devnull stdout", subprocess.DEVNULL, None, None),
        ("Devnull all", subprocess.DEVNULL, subprocess.DEVNULL, subprocess.DEVNULL)
    ]
    
    for name, stdout, stderr, stdin in tests:
        try:
            result = subprocess.run(
                ["echo", "test"],
                stdout=stdout,
                stderr=stderr,
                stdin=stdin,
                shell=True,
                timeout=5,
                text=True,
                capture_output=(stdout==subprocess.PIPE)
            )
            print(f"SUCCESS {name}: return_code={result.returncode}")
            if hasattr(result, 'stdout') and result.stdout:
                print(f"   stdout: '{result.stdout.strip()}'")
        except subprocess.TimeoutExpired:
            print(f"ERROR {name}: TIMEOUT")
        except Exception as e:
            print(f"ERROR {name}: ERROR - {e}")

async def test_asyncio_subprocess_stdio():
    """Test asyncio subprocess with different STDIO configurations"""
    print(f"\n=== Testing asyncio subprocess STDIO ===")
    
    # Test different STDIO combinations that might work in MCP context
    configs = [
        ("Standard pipes", asyncio.subprocess.PIPE, asyncio.subprocess.PIPE),
        ("Devnull stdout", asyncio.subprocess.DEVNULL, asyncio.subprocess.PIPE),
        ("Devnull stderr", asyncio.subprocess.PIPE, asyncio.subprocess.DEVNULL),
        ("Devnull both", asyncio.subprocess.DEVNULL, asyncio.subprocess.DEVNULL)
    ]
    
    for name, stdout_cfg, stderr_cfg in configs:
        try:
            process = await asyncio.create_subprocess_shell(
                "echo asyncio_test",
                stdout=stdout_cfg,
                stderr=stderr_cfg,
                shell=True
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), 5)
            
            if stdout:
                stdout_str = stdout.decode('utf-8', errors='replace').strip()
            else:
                stdout_str = "None"
                
            print(f"SUCCESS {name}: return_code={process.returncode}, stdout='{stdout_str}'")
            
        except asyncio.TimeoutError:
            print(f"ERROR {name}: TIMEOUT")
        except Exception as e:
            print(f"ERROR {name}: ERROR - {e}")

def test_current_stdio_state():
    """Check current STDIO state to understand MCP context"""
    print(f"\n=== Current STDIO State ===")
    print(f"stdin.isatty(): {sys.stdin.isatty()}")
    print(f"stdout.isatty(): {sys.stdout.isatty()}")
    print(f"stderr.isatty(): {sys.stderr.isatty()}")
    print(f"stdin: {sys.stdin}")
    print(f"stdout: {sys.stdout}")
    print(f"stderr: {sys.stderr}")

async def test_detached_subprocess():
    """Test subprocess with Windows DETACHED_PROCESS flag"""
    print(f"\n=== Testing Windows Detached Process ===")
    
    try:
        # This should work on Windows to create detached process
        process = await asyncio.create_subprocess_shell(
            "echo detached_test",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True,
            creationflags=getattr(subprocess, 'DETACHED_PROCESS', 0)
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), 5)
        stdout_str = stdout.decode('utf-8', errors='replace').strip()
        print(f"SUCCESS Detached process: return_code={process.returncode}, stdout='{stdout_str}'")
        
    except Exception as e:
        print(f"ERROR Detached process: ERROR - {e}")

async def main():
    print("Testing MCP STDIO Interference Theory")
    
    test_current_stdio_state()
    test_subprocess_stdio_redirection()
    await test_asyncio_subprocess_stdio()
    await test_detached_subprocess()
    
    print(f"\n=== ANALYSIS ===")
    print("If all tests pass, the issue is likely:")
    print("1. MCP framework event loop interference")
    print("2. MCP protocol blocking subprocess communication")
    print("3. Windows-specific MCP server implementation issue")

if __name__ == "__main__":
    asyncio.run(main())