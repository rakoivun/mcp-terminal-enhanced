#!/usr/bin/env python3
"""
Enhanced Terminal Controller MCP Wrapper

This is an enhanced wrapper for the terminal-controller MCP package that provides:
- Smart project workspace detection
- Git Bash integration on Windows  
- Dynamic configuration without hard-coded paths
- Cross-platform compatibility

Author: rakoivun
License: MIT
Based on: terminal-controller-mcp by GongRzhe (https://github.com/GongRzhe/terminal-controller-mcp)
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, List

__version__ = "1.0.0"

# Common project root indicators in order of preference
PROJECT_MARKERS = [
    '.git',           # Git repository
    'package.json',   # Node.js project
    'pyproject.toml', # Modern Python project
    'setup.py',       # Python project
    'Cargo.toml',     # Rust project
    'go.mod',         # Go project
    'pom.xml',        # Maven project
    'build.gradle',   # Gradle project
    'composer.json',  # PHP project
    'Gemfile',        # Ruby project
    'Rakefile',       # Ruby project
    'Makefile',       # Make-based project
    'CMakeLists.txt', # CMake project
    'requirements.txt', # Python requirements
    'environment.yml', # Conda environment
    '.vscode',        # VS Code workspace
    '.idea',          # IntelliJ workspace
]


def get_project_root(start_path: Optional[str] = None) -> str:
    """
    Dynamically determine the project root directory.
    
    Searches upward from the starting path looking for common project markers.
    
    Args:
        start_path: Directory to start searching from. Defaults to script location.
        
    Returns:
        Path to the detected project root, or start_path if no markers found.
    """
    if start_path is None:
        start_path = os.path.dirname(os.path.abspath(__file__))
    
    search_dir = Path(start_path).resolve()
    
    # Search upward through parent directories
    for current_dir in [search_dir] + list(search_dir.parents):
        # Check for project markers
        for marker in PROJECT_MARKERS:
            marker_path = current_dir / marker
            if marker_path.exists():
                return str(current_dir)
    
    # Fallback to starting directory if no markers found
    return str(search_dir)


def detect_git_bash() -> Optional[str]:
    """
    Detect Git Bash installation on Windows.
    
    Returns:
        Path to Git Bash executable, or None if not found.
    """
    if os.name != 'nt':  # Not Windows
        return None
    
    # Common Git Bash locations
    possible_paths = [
        "C:/Program Files/Git/bin/bash.exe",
        "C:/Program Files (x86)/Git/bin/bash.exe",
        os.path.expanduser("~/AppData/Local/Programs/Git/bin/bash.exe"),
    ]
    
    for bash_path in possible_paths:
        if os.path.exists(bash_path):
            return bash_path
    
    # Try to find in PATH
    try:
        result = subprocess.run(['where', 'bash'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            bash_path = result.stdout.strip().split('\n')[0]
            if 'Git' in bash_path:  # Prefer Git Bash over other bash installations
                return bash_path
    except Exception:
        pass
    
    return None


def setup_environment() -> dict:
    """
    Setup environment variables for the MCP server.
    
    Returns:
        Dictionary of environment variables to set.
    """
    env = os.environ.copy()
    
    # Detect and set workspace directory
    workspace_path = os.environ.get('MCP_WORKSPACE_DIR')
    if not workspace_path:
        workspace_path = get_project_root()
    
    env['MCP_WORKSPACE_DIR'] = workspace_path
    
    # Setup Git Bash on Windows
    if os.name == 'nt':  # Windows
        git_bash = detect_git_bash()
        if git_bash:
            env['SHELL'] = git_bash
            env['COMSPEC'] = git_bash
        else:
            print("Warning: Git Bash not found. Unix commands may not work properly.", 
                  file=sys.stderr)
    
    return env


def print_startup_info(workspace_path: str, git_bash: Optional[str] = None):
    """Print startup information for debugging."""
    print(f"[MCP Enhanced] Starting terminal controller...", file=sys.stderr)
    print(f"[MCP Enhanced] Workspace: {workspace_path}", file=sys.stderr)
    
    if os.name == 'nt' and git_bash:
        print(f"[MCP Enhanced] Git Bash: {git_bash}", file=sys.stderr)
    elif os.name == 'nt':
        print(f"[MCP Enhanced] Git Bash: Not found - using system shell", file=sys.stderr)
    else:
        print(f"[MCP Enhanced] Shell: {os.environ.get('SHELL', 'default')}", file=sys.stderr)


def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import terminal_controller
        return True
    except ImportError:
        print("Error: terminal-controller package not found.", file=sys.stderr)
        print("Please install it with: pip install terminal-controller", file=sys.stderr)
        return False


def main():
    """Main entry point for the enhanced MCP wrapper."""
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    env = setup_environment()
    workspace_path = env['MCP_WORKSPACE_DIR']
    git_bash = env.get('SHELL') if os.name == 'nt' else None
    
    # Print startup info
    print_startup_info(workspace_path, git_bash)
    
    # Validate workspace directory
    if not os.path.exists(workspace_path):
        print(f"Warning: Workspace directory does not exist: {workspace_path}", 
              file=sys.stderr)
        print("Continuing with current directory...", file=sys.stderr)
    
    # Launch the original terminal controller with enhanced environment
    try:
        result = subprocess.run([
            sys.executable, '-m', 'terminal_controller'
        ] + sys.argv[1:], env=env)
        
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n[MCP Enhanced] Received interrupt signal, shutting down...", 
              file=sys.stderr)
        sys.exit(0)
        
    except Exception as e:
        print(f"[MCP Enhanced] Error starting terminal controller: {e}", 
              file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()