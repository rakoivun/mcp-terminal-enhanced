# Installation Guide

This project enhances the original [terminal-controller-mcp](https://github.com/GongRzhe/terminal-controller-mcp) by **GongRzhe**. The original package is required as a dependency.

## Prerequisites

### Required
- **Python 3.8+** 
- **terminal-controller** MCP package (by GongRzhe)

### Optional (Recommended)
- **Git for Windows** (Windows only) - For Git Bash support
- **Cursor IDE** or other MCP-compatible editor

## Installation Methods

### Method 1: Direct Clone (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rakoivun/mcp-terminal-enhanced.git
   cd mcp-terminal-enhanced
   ```

2. **Install the original terminal-controller package:**
   ```bash
   pip install terminal-controller
   ```
   
   This installs the foundational MCP package by GongRzhe that this project enhances.

3. **Make scripts executable (Linux/macOS):**
   ```bash
   chmod +x src/terminal_controller_wrapper.py
   chmod +x src/gitbash_terminal_controller.py
   ```

### Method 2: Download Individual Files

If you only need the wrapper without the full repository:

1. **Download the main wrapper:**
   ```bash
   curl -O https://raw.githubusercontent.com/rakoivun/mcp-terminal-enhanced/main/src/terminal_controller_wrapper.py
   ```

2. **Install dependencies:**
   ```bash
   pip install terminal-controller
   ```

3. **Make executable (Linux/macOS):**
   ```bash
   chmod +x terminal_controller_wrapper.py
   ```

## Platform-Specific Setup

### Windows

1. **Install Git for Windows:**
   - Download from: https://git-scm.com/download/win
   - During installation, ensure "Git Bash Here" is selected
   - Default installation path should be: `C:\Program Files\Git\`

2. **Verify Git Bash installation:**
   ```cmd
   "C:\Program Files\Git\bin\bash.exe" --version
   ```

3. **Test the wrapper:**
   ```cmd
   python src\terminal_controller_wrapper.py
   ```

### Linux/macOS

1. **Verify bash is available:**
   ```bash
   which bash
   ```

2. **Test the wrapper:**
   ```bash
   python src/terminal_controller_wrapper.py
   ```

## Configuration

### MCP Configuration

Update your MCP configuration file (typically `~/.cursor/mcp_wrapper_config.json` for Cursor):

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-terminal-enhanced/src/terminal_controller_wrapper.py"]
    }
  }
}
```

### Environment Variables (Optional)

You can set these environment variables to customize behavior:

```bash
# Override workspace directory detection
export MCP_WORKSPACE_DIR="/custom/workspace/path"

# Debug mode (shows detailed startup information)
export MCP_ENHANCED_DEBUG=1
```

## Verification

### Test Project Detection

1. **Navigate to a project directory:**
   ```bash
   cd /path/to/your/project
   ```

2. **Run the wrapper with debug output:**
   ```bash
   python /path/to/mcp-terminal-enhanced/src/terminal_controller_wrapper.py --version
   ```

3. **Check the output for:**
   - Detected workspace path
   - Git Bash detection (Windows)
   - No error messages

### Test MCP Integration

1. **Start your MCP-compatible editor** (e.g., Cursor)

2. **Open the terminal in the editor**

3. **Run a simple command:**
   ```bash
   pwd
   ```

4. **Verify the output shows your project directory**

## Troubleshooting

### Common Issues

1. **"terminal-controller package not found"**
   ```bash
   pip install terminal-controller
   ```

2. **"Git Bash not found" (Windows)**
   - Reinstall Git for Windows
   - Check installation path: `C:\Program Files\Git\bin\bash.exe`

3. **Permission denied (Linux/macOS)**
   ```bash
   chmod +x src/terminal_controller_wrapper.py
   ```

4. **MCP server doesn't start in project directory**
   - Ensure your project has a recognizable marker (`.git`, `package.json`, etc.)
   - Check absolute paths in MCP configuration
   - Verify wrapper script location

### Debug Mode

Add debug output to see what's happening:

```python
import os
os.environ['MCP_ENHANCED_DEBUG'] = '1'
```

This will show:
- Detected project root
- Environment variables set
- Git Bash detection results
- Startup sequence information

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/rakoivun/mcp-terminal-enhanced/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rakoivun/mcp-terminal-enhanced/discussions)
- 📖 **Documentation**: Check other files in the `docs/` directory

## Next Steps

After installation:
1. Read [Configuration Guide](configuration.md) for advanced options
2. See [Basic Usage Examples](../examples/basic_usage.md)
3. Review [Troubleshooting Guide](troubleshooting.md) for common issues