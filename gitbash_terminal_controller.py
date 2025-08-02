#!/usr/bin/env python3
"""
Git Bash Terminal Controller MCP Wrapper
Wrapper that forces Git Bash usage instead of Windows CMD
"""

import os
import sys
import subprocess

def main():
    # Set environment to force Git Bash usage
    env = os.environ.copy()
    env['SHELL'] = 'C:/Program Files/Git/bin/bash.exe'
    env['COMSPEC'] = 'C:/Program Files/Git/bin/bash.exe'
    
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