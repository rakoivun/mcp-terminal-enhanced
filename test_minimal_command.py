#!/usr/bin/env python3
"""
Test subprocess with minimal CMD command that doesn't need terminal interaction
"""
import asyncio
import platform

async def test_minimal_command():
    """Test a command that should work without terminal interaction"""
    
    # Use absolute path and minimal command
    cmd = r'C:\WINDOWS\system32\cmd.exe /c "echo hello > nul"'
    
    print(f"Testing minimal command: {cmd}")
    
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), 5)
        print(f"SUCCESS: return_code={process.returncode}")
        return True
        
    except asyncio.TimeoutError:
        print("TIMEOUT: Even minimal command failed")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_minimal_command())
    print(f"Result: {result}")