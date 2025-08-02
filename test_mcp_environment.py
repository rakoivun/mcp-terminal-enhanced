#!/usr/bin/env python3
"""
Test environment differences between MCP context and normal Python
"""
import os
import sys

def analyze_environment():
    print("=== ENVIRONMENT ANALYSIS ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Platform: {os.name}")
    
    print("\n=== ENVIRONMENT VARIABLES ===")
    important_vars = ['PATH', 'COMSPEC', 'SHELL', 'PYTHONPATH', 'VIRTUAL_ENV']
    for var in important_vars:
        value = os.environ.get(var, "NOT SET")
        print(f"{var}: {value}")
    
    print("\n=== STDIN/STDOUT STATUS ===")
    print(f"stdin.isatty(): {sys.stdin.isatty()}")
    print(f"stdout.isatty(): {sys.stdout.isatty()}")
    print(f"stderr.isatty(): {sys.stderr.isatty()}")
    
    print("\n=== CURRENT PROCESS INFO ===")
    print(f"Process ID: {os.getpid()}")
    print(f"Parent Process ID: {os.getppid()}")

if __name__ == "__main__":
    analyze_environment()