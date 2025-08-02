# Cursor AI MCP Auto-Start Setup Guide

## ✅ What We've Configured

### Project-Specific Configuration (`.cursor/mcp.json`)
This enables MCP servers **only for this project**:

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["terminal_controller_wrapper.py"],
      "autoStart": true
    }
  },
  "settings": {
    "autoStartServers": true,
    "enableToolApproval": false
  }
}
```

## 🌍 Global Configuration (Optional)

To enable terminal-controller across **all projects**, create/update `~/.cursor/mcp.json`:

### Windows Path: `C:\Users\<username>\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "terminal-controller-global": {
      "command": "python",
      "args": ["C:\\code\\nvdiffrast-trials\\terminal_controller_wrapper.py"],
      "description": "Global terminal controller with Git Bash",
      "autoStart": true,
      "env": {
        "SHELL": "C:/Program Files/Git/bin/bash.exe"
      }
    },
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "description": "Context7 library documentation",
      "autoStart": false
    }
  },
  "settings": {
    "autoStartServers": true,
    "enableToolApproval": false,
    "logLevel": "info"
  }
}
```

## 🔧 Setup Instructions

### Method 1: Cursor UI (Recommended)

1. **Open Cursor Settings**
   - `File` → `Preferences` → `Settings`
   - Or press `Ctrl+,`

2. **Navigate to MCP Section**
   - Search for "MCP" in settings
   - Click on "MCP" in the sidebar

3. **Add MCP Server**
   - Click "Add new MCP server"
   - **Name**: `terminal-controller`
   - **Command**: `python`
   - **Args**: `["terminal_controller_wrapper.py"]`
   - **Auto-start**: ✅ Enable
   - **Enable tool approval**: ❌ Disable (for seamless use)

4. **Verify Setup**
   - Look for green dot next to server name
   - Check that tools are listed in the MCP section

### Method 2: Direct File Configuration (Advanced)

1. **Project-specific** (already done): `.cursor/mcp.json`
2. **Global**: Create `~/.cursor/mcp.json` with content above

## 🚀 Auto-Start Features

### What Happens on Cursor Startup:

✅ **terminal-controller starts automatically**  
✅ **Git Bash environment configured**  
✅ **Workspace directory auto-detected**  
✅ **No manual server startup needed**  
✅ **Tools available immediately in chat**  

### Usage in Cursor Chat:

```
# Examples of commands that will use MCP terminal:
"Run ls -la to show current directory"
"Execute python script.py"
"Check git status"
"Create a new directory called test"
```

## 🔍 Troubleshooting

### Server Not Starting:
1. Check Cursor's Developer Tools (`Help` → `Toggle Developer Tools`)
2. Look for MCP-related errors in console
3. Verify Python is in PATH
4. Ensure `terminal_controller_wrapper.py` exists and is executable

### Tools Not Available:
1. Open MCP settings in Cursor
2. Check server status (should show green dot)
3. Restart Cursor if needed
4. Verify `mcp.json` syntax is valid

### Permission Issues:
1. Run Cursor as Administrator (if needed)
2. Check file permissions on wrapper script
3. Verify Git Bash path: `C:/Program Files/Git/bin/bash.exe`

## 📊 Verification Steps

### 1. Check Server Status
- Open Cursor settings → MCP
- Should see `terminal-controller` with green status

### 2. Test in Chat
```
Type: "List files in current directory using MCP"
Expected: Directory listing using terminal-controller
```

### 3. Check Logs
- Developer Tools → Console
- Look for MCP startup messages
- Should see: `[MCP Wrapper] Setting workspace to: ...`

## ⚙️ Advanced Configuration

### Custom Environment Variables:
```json
"env": {
  "SHELL": "C:/Program Files/Git/bin/bash.exe",
  "PATH": "C:/Program Files/Git/bin;%PATH%",
  "TERM": "xterm-256color"
}
```

### Multiple Terminal Controllers:
```json
"terminal-controller-bash": {
  "command": "python",
  "args": ["terminal_controller_wrapper.py"],
  "env": { "SHELL": "C:/Program Files/Git/bin/bash.exe" }
},
"terminal-controller-powershell": {
  "command": "python", 
  "args": ["terminal_controller_wrapper.py"],
  "env": { "SHELL": "powershell.exe" }
}
```

## 🎯 Benefits of This Setup

✅ **No manual server management**  
✅ **Automatic workspace detection**  
✅ **Git Bash integration on Windows**  
✅ **Seamless tool execution**  
✅ **Project-specific configuration**  
✅ **Cross-platform compatibility**  

Your terminal controller will now start automatically every time you open Cursor AI!
