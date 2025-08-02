#!/usr/bin/env python3
"""
Direct subprocess test to isolate the MCP timeout issue
"""
import asyncio
import platform
from datetime import datetime

async def test_subprocess_execution():
    print("Testing direct subprocess execution...")
    
    start_time = datetime.now()
    cmd = "echo test_output"
    
    try:
        if platform.system() == "Windows":
            print(f"Running Windows command: {cmd}")
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
        else:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True,
                executable="/bin/bash"
            )
        
        print("Process created, waiting for communication...")
        
        try:
            # Test with 10 second timeout like MCP
            stdout, stderr = await asyncio.wait_for(process.communicate(), 10)
            stdout = stdout.decode('utf-8', errors='replace')
            stderr = stderr.decode('utf-8', errors='replace')
            return_code = process.returncode
            
            duration = datetime.now() - start_time
            
            print(f"✅ SUCCESS!")
            print(f"Duration: {duration}")
            print(f"Return code: {return_code}")
            print(f"Stdout: '{stdout.strip()}'")
            print(f"Stderr: '{stderr.strip()}'")
            
        except asyncio.TimeoutError:
            print("❌ TIMEOUT ERROR!")
            try:
                process.kill()
                print("Process killed")
            except:
                print("Failed to kill process")
                
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    print("Starting subprocess test...")
    asyncio.run(test_subprocess_execution())
    print("Test completed.")