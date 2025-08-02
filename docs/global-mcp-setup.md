# Global MCP Setup Guide

This guide shows how to configure the terminal-controller-enhanced globally for personal use across all projects.

## Global Configuration

The MCP is now configured globally in `~/.cursor/mcp.json` with these benefits:

- **No project-specific paths** - works in any project directory
- **Auto workspace detection** - automatically finds the correct project root
- **Git Bash integration** - uses Git Bash on Windows by default
- **Cross-platform compatibility** - works on Windows, macOS, and Linux

## Required Files in Your Project

For the global MCP to work, you need these files in your project root:

### 1. `terminal_controller_wrapper.py` (in root or src/)

This is the enhanced wrapper that provides smart workspace detection. Copy from:
- `src/terminal_controller_wrapper.py` (main enhanced version, 205 lines)
- OR `terminal_controller_wrapper.py` (basic version, 62 lines)

### 2. Dependencies

Install the required package:
```bash
pip install terminal-controller>=0.1.9
```

## Global Config Structure

```json
{
  "mcpServers": {
    "terminal-controller-enhanced": {
      "command": "python",
      "args": ["terminal_controller_wrapper.py"],
      "description": "Enhanced terminal controller with smart workspace detection and Git Bash support",
      "autoStart": true,
      "env": {
        "PYTHONPATH": "src",
        "SHELL": "C:/Program Files/Git/bin/bash.exe"
      }
    }
  }
}
```

## How It Works

1. **Global Loading**: Cursor loads `~/.cursor/mcp.json` for ALL projects
2. **Workspace Detection**: The wrapper automatically detects the current project directory
3. **Path Resolution**: Uses relative paths (`terminal_controller_wrapper.py`) that work anywhere
4. **Environment Setup**: Sets `PYTHONPATH=src` to find the wrapper in either root or src/ directories

## Benefits

- **No Git Pollution**: No project-specific config files in version control
- **Easy Deployment**: Copy one wrapper file to enable MCP in any project
- **Consistent Experience**: Same MCP tools available across all projects
- **Maintainable**: Update global config once, affects all projects

## Migration from Project-Specific Setup

If you had project-specific configs before:

1. **Removed**: Project-specific config files from git tracking
2. **Added**: Config files to `.gitignore` 
3. **Created**: Global config in `~/.cursor/mcp.json`
4. **Required**: Copy `terminal_controller_wrapper.py` to new projects

## Troubleshooting

### "No tools or prompts" Issue
- Ensure `terminal_controller_wrapper.py` exists in project root or `src/` directory
- Check that `terminal-controller` package is installed: `pip show terminal-controller`

### Wrong Working Directory
- The enhanced wrapper automatically detects and sets the correct workspace directory
- No manual configuration needed

### Multiple MCP Entries
- Remove any local project configs (`.cursor/mcp.json`, `mcp_wrapper_config.json`)
- Only the global config should exist

## Next Projects

To enable MCP in a new project:

1. Copy `terminal_controller_wrapper.py` to the project root
2. Install: `pip install terminal-controller>=0.1.9`
3. Restart Cursor - MCP will automatically work!

No project-specific configuration needed!