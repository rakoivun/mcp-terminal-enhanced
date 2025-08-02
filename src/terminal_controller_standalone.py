#!/usr/bin/env python3
"""
Self-Sufficient Terminal Controller MCP Server

This is a standalone implementation that includes:
- Complete MCP protocol implementation
- Git Bash integration on Windows
- Smart workspace detection
- No external dependencies except mcp

Author: rakoivun
License: MIT
Based on: terminal-controller-mcp by GongRzhe
"""

import asyncio
import os
import subprocess
import platform
import sys
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

# Import MCP framework
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: MCP framework not found. Please install: pip install mcp", file=sys.stderr)
    sys.exit(1)

__version__ = "2.0.0-standalone"

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
            if os.path.exists(bash_path):
                return bash_path
    except Exception:
        pass
    
    return None

def setup_environment() -> Dict[str, str]:
    """
    Setup environment variables for the MCP server.
    
    Returns:
        Dictionary of environment variables to use.
    """
    env = os.environ.copy()
    
    # Detect and set workspace directory
    workspace_dir = os.environ.get('MCP_WORKSPACE_DIR')
    if not workspace_dir:
        workspace_dir = get_project_root()
    
    env['MCP_WORKSPACE_DIR'] = workspace_dir
    
    # Set up Git Bash on Windows
    if os.name == 'nt':
        git_bash = detect_git_bash()
        if git_bash:
            env['SHELL'] = git_bash
            env['COMSPEC'] = git_bash
            print(f"[Standalone MCP] Git Bash detected: {git_bash}", file=sys.stderr)
        else:
            print("[Standalone MCP] Git Bash not found, using default Windows shell", file=sys.stderr)
    
    print(f"[Standalone MCP] Workspace: {workspace_dir}", file=sys.stderr)
    print(f"[Standalone MCP] Shell: {env.get('SHELL', 'default')}", file=sys.stderr)
    
    return env

# Initialize MCP server
mcp = FastMCP("terminal-controller-enhanced", log_level="INFO")

# List to store command history
command_history = []

# Maximum history size
MAX_HISTORY_SIZE = 50

# Set up environment
ENV = setup_environment()

# Change to workspace directory
workspace_dir = ENV.get('MCP_WORKSPACE_DIR')
if workspace_dir and os.path.exists(workspace_dir):
    try:
        os.chdir(workspace_dir)
        print(f"[Standalone MCP] Changed to workspace: {workspace_dir}", file=sys.stderr)
    except Exception as e:
        print(f"[Standalone MCP] Warning: Could not change to workspace {workspace_dir}: {e}", file=sys.stderr)

async def run_command(cmd: str, timeout: int = 30) -> Dict:
    """
    Execute command and return results with Git Bash support
    
    Args:
        cmd: Command to execute
        timeout: Command timeout in seconds
        
    Returns:
        Dictionary containing command execution results
    """
    start_time = datetime.now()
    
    try:
        # Create command appropriate for current OS with Git Bash support
        if platform.system() == "Windows":
            # Use Git Bash if available, otherwise default shell
            git_bash = ENV.get('SHELL')
            if git_bash and os.path.exists(git_bash):
                # Use Git Bash for Unix-style commands
                process = await asyncio.create_subprocess_exec(
                    git_bash, "-c", cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    stdin=asyncio.subprocess.DEVNULL
                )
            else:
                # Fallback to CMD if Git Bash not available
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    stdin=asyncio.subprocess.DEVNULL,
                    shell=True
                )
        else:
            process = await asyncio.create_subprocess_exec(
                "/bin/bash", "-c", cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL
            )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
            stdout = stdout.decode('utf-8', errors='replace')
            stderr = stderr.decode('utf-8', errors='replace')
            return_code = process.returncode
        except asyncio.TimeoutError:
            try:
                process.kill()
            except:
                pass
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "return_code": -1,
                "duration": str(datetime.now() - start_time),
                "command": cmd
            }
    
        duration = datetime.now() - start_time
        result = {
            "success": return_code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code,
            "duration": str(duration),
            "command": cmd
        }
        
        # Add to history
        command_history.append({
            "timestamp": datetime.now().isoformat(),
            "command": cmd,
            "success": return_code == 0
        })
        
        # If history is too long, remove oldest record
        if len(command_history) > MAX_HISTORY_SIZE:
            command_history.pop(0)
            
        return result
    
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "return_code": -1,
            "duration": str(datetime.now() - start_time),
            "command": cmd
        }

@mcp.tool()
async def execute_command(command: str, timeout: int = 30) -> str:
    """
    Execute terminal command and return results
    
    Args:
        command: Command line command to execute
        timeout: Command timeout in seconds, default is 30 seconds
    
    Returns:
        Output of the command execution
    """
    # Check for dangerous commands (can add more security checks)
    dangerous_commands = ["rm -rf /", "mkfs"]
    if any(dc in command.lower() for dc in dangerous_commands):
        return "For security reasons, this command is not allowed."
    
    result = await run_command(command, timeout)
    
    if result["success"]:
        output = f"Command executed successfully (duration: {result['duration']})\n\n"
        
        if result["stdout"]:
            output += f"Output:\n{result['stdout']}\n"
        else:
            output += "Command had no output.\n"
            
        if result["stderr"]:
            output += f"\nWarnings/Info:\n{result['stderr']}"
            
        return output
    else:
        output = f"Command execution failed (duration: {result['duration']})\n"
        
        if result["stdout"]:
            output += f"\nOutput:\n{result['stdout']}\n"
            
        if result["stderr"]:
            output += f"\nError:\n{result['stderr']}"
            
        output += f"\nReturn code: {result['return_code']}"
        return output

@mcp.tool()
async def get_command_history(count: int = 10) -> str:
    """
    Get recent command execution history
    
    Args:
        count: Number of recent commands to return
    
    Returns:
        Formatted command history record
    """
    if not command_history:
        return "No command execution history."
    
    count = min(count, len(command_history))
    recent_commands = command_history[-count:]
    
    output = f"Recent {count} command history:\n\n"
    
    for i, cmd in enumerate(recent_commands):
        status = "✓" if cmd["success"] else "✗"
        output += f"{i+1}. [{status}] {cmd['timestamp']}: {cmd['command']}\n"
    
    return output

@mcp.tool()
async def get_current_directory() -> str:
    """
    Get current working directory
    
    Returns:
        Path of current working directory
    """
    return os.getcwd()

@mcp.tool()
async def change_directory(path: str) -> str:
    """
    Change current working directory
    
    Args:
        path: Directory path to switch to
    
    Returns:
        Operation result information
    """
    try:
        os.chdir(path)
        return f"Switched to directory: {os.getcwd()}"
    except FileNotFoundError:
        return f"Error: Directory '{path}' does not exist"
    except PermissionError:
        return f"Error: No permission to access directory '{path}'"
    except Exception as e:
        return f"Error changing directory: {str(e)}"

@mcp.tool()
async def list_directory(path: Optional[str] = None) -> str:
    """
    List files and subdirectories in the specified directory
    
    Args:
        path: Directory path to list contents, default is current directory
    
    Returns:
        List of directory contents
    """
    if path is None:
        path = os.getcwd()
    
    try:
        items = os.listdir(path)
        
        dirs = []
        files = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(f"📁 {item}/")
            else:
                files.append(f"📄 {item}")
        
        # Sort directories and files
        dirs.sort()
        files.sort()
        
        if not dirs and not files:
            return f"Directory '{path}' is empty"
        
        output = f"Contents of directory '{path}':\n\n"
        
        if dirs:
            output += "Directories:\n"
            output += "\n".join(dirs) + "\n\n"
        
        if files:
            output += "Files:\n"
            output += "\n".join(files)
        
        return output
    
    except FileNotFoundError:
        return f"Error: Directory '{path}' does not exist"
    except PermissionError:
        return f"Error: No permission to access directory '{path}'"
    except Exception as e:
        return f"Error listing directory contents: {str(e)}"

@mcp.tool()
async def read_file(path: str) -> str:
    """
    Read content from a file
    
    Args:
        path: Path to the file
    
    Returns:
        File content
    """
    try:
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist."
            
        if not os.path.isfile(path):
            return f"Error: '{path}' is not a file."
        
        with open(path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
        
        return content
            
    except PermissionError:
        return f"Error: No permission to read file '{path}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """
    Write content to a file
    
    Args:
        path: Path to the file
        content: Content to write
    
    Returns:
        Operation result information
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(os.path.abspath(path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(path, 'w', encoding="utf-8") as file:
            file.write(content)
        
        # Verify the write operation was successful
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            return f"Successfully wrote {file_size} bytes to '{path}'."
        else:
            return f"Write operation completed, but unable to verify file exists at '{path}'."
    
    except PermissionError:
        return f"Error: No permission to write to file '{path}'."
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@mcp.tool()
async def delete_file(path: str) -> str:
    """
    Delete a file
    
    Args:
        path: Path to the file to delete
    
    Returns:
        Operation result information
    """
    try:
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist."
            
        if os.path.isfile(path):
            os.remove(path)
            return f"Successfully deleted file '{path}'."
        else:
            return f"Error: '{path}' is not a file."
    
    except PermissionError:
        return f"Error: No permission to delete file '{path}'."
    except Exception as e:
        return f"Error deleting file: {str(e)}"

@mcp.tool()
async def insert_file_content(path: str, content: str, row: int = None) -> str:
    """
    Insert content at specific row in a file
    
    Args:
        path: Path to the file
        content: Content to insert
        row: Row number to insert at (0-based, optional)
    
    Returns:
        Operation result information
    """
    try:
        # Create file if it doesn't exist
        directory = os.path.dirname(os.path.abspath(path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as file:
                pass
            
        with open(path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
        
        # Ensure content ends with a newline
        if content and not content.endswith('\n'):
            content += '\n'
        
        # Insert at specified row or end of file
        if row is not None:
            if row < 0:
                return "Error: Row number must be non-negative."
            if row > len(lines):
                lines.extend(['\n'] * (row - len(lines)))
                lines.append(content)
            else:
                lines.insert(row, content)
        else:
            lines.append(content)
        
        # Write back to file
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            
        return f"Successfully inserted content at row {row if row is not None else len(lines)-1} in '{path}'."
        
    except PermissionError:
        return f"Error: No permission to modify file '{path}'."
    except Exception as e:
        return f"Error inserting content: {str(e)}"

@mcp.tool()
async def update_file_content(path: str, content: str, row: int = None, substring: str = None) -> str:
    """
    Update content at specific row in a file
    
    Args:
        path: Path to the file
        content: New content to replace with
        row: Row number to update (0-based, optional)
        substring: If provided, only replace this substring, not the entire row
    
    Returns:
        Operation result information
    """
    try:
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist."
            
        if not os.path.isfile(path):
            return f"Error: '{path}' is not a file."
            
        with open(path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
        
        total_lines = len(lines)
        
        # Ensure content ends with a newline if replacing full line
        if substring is None and content and not content.endswith('\n'):
            content += '\n'
        
        if row is not None:
            if row < 0:
                return "Error: Row number must be non-negative."
            if row >= total_lines:
                return f"Error: Row {row} is out of range (file has {total_lines} lines)."
                
            # If substring is provided, only replace that part
            if substring is not None:
                if substring in lines[row]:
                    original_line = lines[row]
                    lines[row] = lines[row].replace(substring, content)
                    # Ensure line ends with newline if original did
                    if original_line.endswith('\n') and not lines[row].endswith('\n'):
                        lines[row] += '\n'
                else:
                    return f"Substring '{substring}' not found in row {row}."
            else:
                # Replace entire line
                lines[row] = content
        else:
            # Update entire file if no row specified
            if substring is not None:
                # Replace substring throughout file
                updated_count = 0
                for i in range(len(lines)):
                    if substring in lines[i]:
                        original_line = lines[i]
                        lines[i] = lines[i].replace(substring, content)
                        if original_line.endswith('\n') and not lines[i].endswith('\n'):
                            lines[i] += '\n'
                        updated_count += 1
                
                if updated_count == 0:
                    return f"Substring '{substring}' not found in any line."
            else:
                # Replace entire file content
                lines = [content if content.endswith('\n') else content + '\n']
        
        # Write back to file
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
            
        if substring is not None:
            return f"Successfully updated substring in '{path}'."
        else:
            return f"Successfully updated content in '{path}'."
            
    except PermissionError:
        return f"Error: No permission to modify file '{path}'."
    except Exception as e:
        return f"Error updating content: {str(e)}"

def main():
    """
    Entry point function that runs the MCP server.
    """
    print("Starting Self-Sufficient Terminal Controller MCP Server...", file=sys.stderr)
    print(f"Version: {__version__}", file=sys.stderr)
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()