# Configuration Guide

## Overview

The enhanced MCP terminal controller supports multiple configuration methods to customize its behavior for different environments and use cases.

## Configuration Methods

### 1. Environment Variables

The most flexible way to configure the wrapper:

```bash
# Override automatic workspace detection
export MCP_WORKSPACE_DIR="/custom/workspace/path"

# Force specific shell (Windows)
export SHELL="/c/Program Files/Git/bin/bash.exe"

# Enable debug output
export MCP_ENHANCED_DEBUG=1

# Disable Git Bash detection (Windows)
export MCP_NO_GITBASH=1
```

### 2. MCP Server Configuration

Configure in your MCP configuration file (e.g., `~/.cursor/mcp_wrapper_config.json`):

#### Basic Configuration
```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"]
    }
  }
}
```

#### Advanced Configuration with Environment Variables
```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/custom/workspace",
        "MCP_ENHANCED_DEBUG": "1"
      }
    }
  }
}
```

### 3. Script Modification

For permanent customization, modify the wrapper script directly:

```python
# In terminal_controller_wrapper.py
def setup_environment() -> dict:
    env = os.environ.copy()
    
    # Custom workspace (override detection)
    env['MCP_WORKSPACE_DIR'] = '/your/custom/workspace'
    
    # Custom shell
    if os.name == 'nt':
        env['SHELL'] = 'C:/path/to/your/shell.exe'
    
    return env
```

## Configuration Options

### Workspace Detection

#### Automatic Detection (Default)
The wrapper automatically detects the project root by looking for these markers in order:

1. `.git` - Git repository
2. `package.json` - Node.js project
3. `pyproject.toml` - Modern Python project
4. `setup.py` - Python project
5. `Cargo.toml` - Rust project
6. `go.mod` - Go project
7. And many more...

#### Manual Override
```bash
export MCP_WORKSPACE_DIR="/path/to/your/workspace"
```

#### Custom Detection Logic
Modify the `PROJECT_MARKERS` list in the wrapper:

```python
PROJECT_MARKERS = [
    '.git',
    'your-custom-marker.txt',
    'project.config',
    # ... other markers
]
```

### Shell Configuration (Windows)

#### Automatic Git Bash Detection (Default)
Searches for Git Bash in common locations:
- `C:/Program Files/Git/bin/bash.exe`
- `C:/Program Files (x86)/Git/bin/bash.exe`
- User's local Git installation

#### Manual Shell Override
```bash
export SHELL="/path/to/your/preferred/shell.exe"
export COMSPEC="/path/to/your/preferred/shell.exe"
```

#### Disable Git Bash
```bash
export MCP_NO_GITBASH=1
```

### Debug Configuration

#### Enable Debug Output
```bash
export MCP_ENHANCED_DEBUG=1
```

This will show:
- Detected project root path
- Environment variables being set
- Git Bash detection results
- Shell configuration
- Startup sequence details

#### Verbose Logging
For even more detailed output, modify the wrapper:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Platform-Specific Configuration

### Windows Configuration

#### Git Bash Paths
If Git Bash is installed in a non-standard location:

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "SHELL": "D:/Tools/Git/bin/bash.exe",
        "COMSPEC": "D:/Tools/Git/bin/bash.exe"
      }
    }
  }
}
```

#### WSL Integration
For Windows Subsystem for Linux:

```bash
export SHELL="/usr/bin/bash"
export MCP_WORKSPACE_DIR="/mnt/c/your/project"
```

### Linux/macOS Configuration

#### Custom Shell
```bash
export SHELL="/bin/zsh"  # Use zsh instead of bash
```

#### Alternative Bash Location
```bash
export SHELL="/usr/local/bin/bash"  # Homebrew bash on macOS
```

## IDE-Specific Configuration

### Cursor IDE

Configuration file location: `~/.cursor/mcp_wrapper_config.json`

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp-terminal-enhanced\\src\\terminal_controller_wrapper.py"]
    }
  }
}
```

### VS Code (with MCP extension)

Configuration in `settings.json`:

```json
{
  "mcp.servers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Configuration Examples

### Development Environment

For active development with debugging:

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_ENHANCED_DEBUG": "1",
        "MCP_WORKSPACE_DIR": "${workspaceFolder}"
      }
    }
  }
}
```

### Production Environment

For stable production use:

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/opt/production/workspace"
      }
    }
  }
}
```

### Multi-Project Setup

Configure different instances for different projects:

```json
{
  "mcpServers": {
    "terminal-project-a": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/path/to/project-a"
      }
    },
    "terminal-project-b": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/path/to/project-b"
      }
    }
  }
}
```

## Validation

### Test Your Configuration

1. **Run the wrapper directly:**
   ```bash
   python terminal_controller_wrapper.py --version
   ```

2. **Check environment detection:**
   ```bash
   MCP_ENHANCED_DEBUG=1 python terminal_controller_wrapper.py
   ```

3. **Verify workspace detection:**
   ```bash
   cd /your/project && python /path/to/terminal_controller_wrapper.py
   ```

### Configuration Troubleshooting

1. **Invalid JSON in MCP config:**
   - Use a JSON validator
   - Check for trailing commas
   - Verify quote marks

2. **Path issues:**
   - Use absolute paths
   - Escape backslashes on Windows: `C:\\path\\to\\file`
   - Test paths in terminal first

3. **Environment variable conflicts:**
   - Use `env` command to check current environment
   - Clear conflicting variables: `unset VARIABLE_NAME`

## Next Steps

- Review [Troubleshooting Guide](troubleshooting.md) for common issues
- See [Basic Usage Examples](../examples/basic_usage.md)
- Check [Development Guide](development.md) for customization