#!/usr/bin/env python3
"""
Enhanced Terminal Controller MCP Wrapper
- Forces Git Bash usage on Windows
- Automatically sets workspace directory 
- No site-packages modification required
"""

import os
import sys
import subprocess
import json

def get_project_root():
    """
    Dynamically determine the project root directory.
    Looks for common project markers like .git, package.json, pyproject.toml, etc.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for common project root indicators
    project_markers = ['.git', 'package.json', 'pyproject.toml', 'setup.py', 'Cargo.toml', 'go.mod']
    
    # Start from current directory and go up
    search_dir = current_dir
    while search_dir != os.path.dirname(search_dir):  # Not root directory
        for marker in project_markers:
            if os.path.exists(os.path.join(search_dir, marker)):
                return search_dir
        search_dir = os.path.dirname(search_dir)
    
    # Fallback to current script's directory
    return current_dir

def main():
    # Determine project workspace directory
    workspace_path = get_project_root()
    
    # Set environment for Git Bash and workspace
    env = os.environ.copy()
    env['SHELL'] = 'C:/Program Files/Git/bin/bash.exe'
    env['COMSPEC'] = 'C:/Program Files/Git/bin/bash.exe'
    env['MCP_WORKSPACE_DIR'] = workspace_path
    
    print(f"[MCP Wrapper] Setting workspace to: {workspace_path}", file=sys.stderr)
    print(f"[MCP Wrapper] Using Git Bash: {env['SHELL']}", file=sys.stderr)
    
    # Call the original terminal controller
    try:
        result = subprocess.run([
            sys.executable, '-m', 'terminal_controller'
        ] + sys.argv[1:], env=env)
        
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error starting terminal controller: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()