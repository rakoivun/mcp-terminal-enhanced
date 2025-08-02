#!/usr/bin/env python3
"""
Legacy Git Bash Terminal Controller MCP Wrapper

This is a simpler wrapper focused specifically on Git Bash integration.
For full features, use terminal_controller_wrapper.py instead.

Author: rakoivun
License: MIT
Based on: terminal-controller-mcp by GongRzhe (https://github.com/GongRzhe/terminal-controller-mcp)
"""

import os
import sys
import subprocess

def main():
    """Legacy Git Bash wrapper for backward compatibility."""
    
    # Set environment to force Git Bash usage
    env = os.environ.copy()
    env['SHELL'] = 'C:/Program Files/Git/bin/bash.exe'
    env['COMSPEC'] = 'C:/Program Files/Git/bin/bash.exe'
    
    # Set workspace directory for the terminal controller
    # Use the directory where this wrapper script is located as the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from src/
    env['MCP_WORKSPACE_DIR'] = project_root
    
    print(f"[Git Bash MCP] Using workspace: {project_root}", file=sys.stderr)
    print(f"[Git Bash MCP] Using Git Bash: {env['SHELL']}", file=sys.stderr)
    
    # Call the original terminal controller with Git Bash environment
    try:
        # Use the same arguments passed to this wrapper
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