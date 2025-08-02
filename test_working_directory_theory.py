#!/usr/bin/env python3
"""
Test if working directory affects subprocess execution
Hypothesis: MCP running in nvdiffrast/ directory causes subprocess issues
"""
import asyncio
import os
import platform

async def test_subprocess_from_directory(test_dir, description):
    """Test subprocess execution from specific directory"""
    print(f"\n=== Testing from {description} ===")
    print(f"Directory: {test_dir}")
    
    # Change to test directory
    original_cwd = os.getcwd()
    try:
        if os.path.exists(test_dir):
            os.chdir(test_dir)
            print(f"Changed to: {os.getcwd()}")
        else:
            print(f"ERROR: Directory does not exist: {test_dir}")
            return False
            
        # Test simple subprocess execution
        cmd = "echo test_from_directory"
        
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), 10)
            stdout = stdout.decode('utf-8', errors='replace').strip()
            stderr = stderr.decode('utf-8', errors='replace').strip()
            
            print(f"SUCCESS from {description}")
            print(f"Return code: {process.returncode}")
            print(f"Output: '{stdout}'")
            if stderr:
                print(f"Stderr: '{stderr}'")
            return True
            
        except asyncio.TimeoutError:
            print(f"TIMEOUT from {description}")
            return False
        except Exception as e:
            print(f"ERROR from {description}: {e}")
            return False
            
    finally:
        # Always restore original directory
        os.chdir(original_cwd)

async def main():
    print("Testing Working Directory Theory for MCP execute_command timeouts")
    
    # Test from various directories
    test_directories = [
        ("C:/code/nvdiffrast-trials", "main project directory"),
        ("C:/code/nvdiffrast-trials/nvdiffrast", "MCP current directory"), 
        ("C:/code/nvdiffrast-trials/terminal_controller_env", "Python env directory"),
        ("C:/Windows/System32", "system directory"),
        ("C:/", "root directory")
    ]
    
    results = {}
    
    for test_dir, description in test_directories:
        success = await test_subprocess_from_directory(test_dir, description)
        results[description] = success
    
    print(f"\n=== RESULTS SUMMARY ===")
    for desc, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status}: {desc}")
    
    # Analysis
    all_success = all(results.values())
    if all_success:
        print("\nCONCLUSION: Working directory does NOT affect subprocess execution")
        print("   The issue is NOT related to working directory")
    else:
        failed_dirs = [desc for desc, success in results.items() if not success]
        print(f"\n🚨 CONCLUSION: Some directories fail: {failed_dirs}")
        print("   Working directory MIGHT be the issue")

if __name__ == "__main__":
    asyncio.run(main())