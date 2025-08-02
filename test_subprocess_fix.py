#!/usr/bin/env python3
"""
Test subprocess execution to isolate the terminal controller hanging issue
"""
import asyncio
import subprocess
import platform
import os
from datetime import datetime

async def test_basic_subprocess():
    """Test basic asyncio subprocess without MCP context"""
    print("=== Testing Basic Asyncio Subprocess ===")
    
    cmd = "echo hello"
    start_time = datetime.now()
    
    try:
        if platform.system() == "Windows":
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL,
                shell=True
            )
        else:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL,
                shell=True,
                executable="/bin/bash"
            )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
        duration = datetime.now() - start_time
        
        print(f"✅ SUCCESS - Duration: {duration}")
        print(f"   stdout: '{stdout.decode().strip()}'")
        print(f"   stderr: '{stderr.decode().strip()}'")
        print(f"   return_code: {process.returncode}")
        return True
        
    except asyncio.TimeoutError:
        print(f"❌ TIMEOUT after 5 seconds")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def test_git_bash_direct():
    """Test Git Bash execution directly"""
    print("\n=== Testing Git Bash Direct ===")
    
    if platform.system() != "Windows":
        print("Skipping - not Windows")
        return True
    
    git_bash = "C:/Program Files/Git/bin/bash.exe"
    if not os.path.exists(git_bash):
        print(f"Git Bash not found at {git_bash}")
        return False
    
    cmd = "echo hello_git_bash"
    start_time = datetime.now()
    
    try:
        process = await asyncio.create_subprocess_exec(
            git_bash, "-c", cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
        duration = datetime.now() - start_time
        
        print(f"✅ SUCCESS - Duration: {duration}")
        print(f"   stdout: '{stdout.decode().strip()}'")
        print(f"   stderr: '{stderr.decode().strip()}'")
        print(f"   return_code: {process.returncode}")
        return True
        
    except asyncio.TimeoutError:
        print(f"❌ TIMEOUT after 5 seconds")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_sync_subprocess():
    """Test synchronous subprocess for comparison"""
    print("\n=== Testing Synchronous Subprocess ===")
    
    cmd = "echo hello_sync"
    start_time = datetime.now()
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        duration = datetime.now() - start_time
        
        print(f"✅ SUCCESS - Duration: {duration}")
        print(f"   stdout: '{result.stdout.strip()}'")
        print(f"   stderr: '{result.stderr.strip()}'")
        print(f"   return_code: {result.returncode}")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT after 5 seconds")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def test_different_configurations():
    """Test various subprocess configurations"""
    print("\n=== Testing Different Configurations ===")
    
    configs = [
        ("No stdin config", {}),
        ("stdin=DEVNULL", {"stdin": asyncio.subprocess.DEVNULL}),
        ("stdin=PIPE", {"stdin": asyncio.subprocess.PIPE}),
    ]
    
    cmd = "echo config_test"
    
    for name, config in configs:
        print(f"\nTesting {name}:")
        start_time = datetime.now()
        
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
                **config
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=3)
            duration = datetime.now() - start_time
            
            print(f"  ✅ SUCCESS - Duration: {duration}")
            print(f"     stdout: '{stdout.decode().strip()}'")
            
        except asyncio.TimeoutError:
            print(f"  ❌ TIMEOUT after 3 seconds")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")

async def main():
    """Run all tests"""
    print("Starting subprocess diagnostics...\n")
    
    results = []
    
    # Test 1: Basic subprocess
    results.append(await test_basic_subprocess())
    
    # Test 2: Git Bash direct
    results.append(await test_git_bash_direct())
    
    # Test 3: Sync subprocess
    results.append(test_sync_subprocess())
    
    # Test 4: Different configurations
    await test_different_configurations()
    
    print(f"\n=== SUMMARY ===")
    print(f"Basic subprocess: {'✅' if results[0] else '❌'}")
    print(f"Git Bash direct: {'✅' if results[1] else '❌'}")
    print(f"Sync subprocess: {'✅' if results[2] else '❌'}")
    
    if all(results):
        print("\n🎉 All basic tests passed! Issue might be MCP-specific.")
    else:
        print("\n⚠️ Basic subprocess issues detected. Need to fix these first.")

if __name__ == "__main__":
    asyncio.run(main())