# Troubleshooting Guide

## Quick Diagnosis

### 1. Test Basic Functionality

```bash
# Test wrapper directly
python src/terminal_controller_wrapper.py --version

# Test with debug output
MCP_ENHANCED_DEBUG=1 python src/terminal_controller_wrapper.py
```

### 2. Check Dependencies

```bash
# Verify terminal-controller is installed
python -c "import terminal_controller; print('OK')"

# Check version
pip show terminal-controller
```

### 3. Test Project Detection

```bash
# From your project directory
cd /path/to/your/project
python /path/to/terminal_controller_wrapper.py
```

## Common Issues and Solutions

### Issue 1: "terminal-controller package not found"

**Symptoms:**
- Error: `ImportError: No module named 'terminal_controller'`
- Wrapper fails to start

**Solutions:**
1. Install the package:
   ```bash
   pip install terminal-controller
   ```

2. Check if you're using the correct Python environment:
   ```bash
   which python
   python -m pip list | grep terminal
   ```

3. For virtual environments:
   ```bash
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   pip install terminal-controller
   ```

### Issue 2: MCP Server Doesn't Start in Project Directory

**Symptoms:**
- Terminal opens in home directory instead of project
- `pwd` shows wrong directory

**Solutions:**
1. **Add project markers:** Create a `.git` directory or `package.json` file:
   ```bash
   git init  # Creates .git directory
   # or
   echo '{}' > package.json  # Creates package.json
   ```

2. **Manual override:** Set environment variable:
   ```bash
   export MCP_WORKSPACE_DIR="/path/to/your/project"
   ```

3. **Check project detection:** Run with debug:
   ```bash
   MCP_ENHANCED_DEBUG=1 python terminal_controller_wrapper.py
   ```

4. **Verify MCP configuration:** Check absolute paths:
   ```json
   {
     "mcpServers": {
       "terminal-controller": {
         "command": "python",
         "args": ["/absolute/path/to/terminal_controller_wrapper.py"]
       }
     }
   }
   ```

### Issue 3: Git Bash Not Working (Windows)

**Symptoms:**
- Unix commands fail on Windows
- "bash: command not found" errors
- "Git Bash not found" warning

**Solutions:**
1. **Install Git for Windows:**
   - Download from: https://git-scm.com/download/win
   - Use default installation path

2. **Verify Git Bash location:**
   ```cmd
   dir "C:\Program Files\Git\bin\bash.exe"
   ```

3. **Manual path override:**
   ```bash
   export SHELL="C:/Program Files/Git/bin/bash.exe"
   export COMSPEC="C:/Program Files/Git/bin/bash.exe"
   ```

4. **Check for custom Git installation:**
   ```cmd
   where bash
   ```

### Issue 4: Permission Denied Errors

**Symptoms:**
- "Permission denied" when running wrapper
- Cannot execute script

**Solutions:**
1. **Make script executable (Linux/macOS):**
   ```bash
   chmod +x src/terminal_controller_wrapper.py
   ```

2. **Check file ownership:**
   ```bash
   ls -l src/terminal_controller_wrapper.py
   ```

3. **Run with explicit python:**
   ```bash
   python src/terminal_controller_wrapper.py
   ```

### Issue 5: MCP Configuration Not Loading

**Symptoms:**
- Changes to configuration don't take effect
- MCP server not starting

**Solutions:**
1. **Validate JSON syntax:**
   ```bash
   python -m json.tool mcp_config.json
   ```

2. **Check configuration file location:**
   - Cursor: `~/.cursor/mcp_wrapper_config.json`
   - VS Code: User/workspace settings
   - Custom: Check your IDE's documentation

3. **Restart IDE completely** after configuration changes

4. **Use absolute paths:**
   ```json
   {
     "args": ["C:\\full\\path\\to\\terminal_controller_wrapper.py"]
   }
   ```

### Issue 6: Environment Variables Not Working

**Symptoms:**
- Custom `MCP_WORKSPACE_DIR` ignored
- Debug output not showing

**Solutions:**
1. **Set in MCP configuration:**
   ```json
   {
     "mcpServers": {
       "terminal-controller": {
         "command": "python",
         "args": ["/path/to/wrapper.py"],
         "env": {
           "MCP_WORKSPACE_DIR": "/custom/path",
           "MCP_ENHANCED_DEBUG": "1"
         }
       }
     }
   }
   ```

2. **Check environment inheritance:**
   ```bash
   env | grep MCP
   ```

3. **Test in terminal first:**
   ```bash
   MCP_WORKSPACE_DIR=/test/path python wrapper.py
   ```

### Issue 7: Multiple Python Versions

**Symptoms:**
- Package installed but not found
- Wrong Python version used

**Solutions:**
1. **Use specific Python version:**
   ```json
   {
     "command": "python3.9",
     "args": ["/path/to/wrapper.py"]
   }
   ```

2. **Check Python path:**
   ```bash
   which python
   python --version
   ```

3. **Use virtual environment:**
   ```json
   {
     "command": "/path/to/venv/bin/python",
     "args": ["/path/to/wrapper.py"]
   }
   ```

## Advanced Troubleshooting

### Debug Mode Analysis

Enable debug mode and analyze the output:

```bash
MCP_ENHANCED_DEBUG=1 python terminal_controller_wrapper.py
```

Look for:
- **Project root detection:** Should show your project path
- **Environment setup:** Should list all environment variables
- **Git Bash detection:** Should find Git Bash on Windows
- **Dependency check:** Should confirm terminal-controller is available

### Logging Configuration

Add detailed logging to the wrapper:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp-debug.log'),
        logging.StreamHandler()
    ]
)
```

### Network and Firewall Issues

If MCP communication fails:

1. **Check firewall settings**
2. **Verify port availability**
3. **Test with minimal configuration**

### IDE-Specific Issues

#### Cursor IDE
- Check `~/.cursor/logs/` for error messages
- Verify MCP extension is enabled
- Restart Cursor completely

#### VS Code
- Check Developer Console (F12) for errors
- Verify MCP extension compatibility
- Check workspace vs user settings

## Getting Help

### Before Asking for Help

1. **Run diagnostic commands:**
   ```bash
   # Basic info
   python --version
   pip show terminal-controller
   
   # Test wrapper
   MCP_ENHANCED_DEBUG=1 python terminal_controller_wrapper.py
   
   # Check environment
   env | grep -E "(MCP|SHELL|PATH)"
   ```

2. **Collect error messages:**
   - Copy complete error output
   - Include debug information
   - Note your operating system and Python version

### Where to Get Help

- **Issues**: [GitHub Issues](https://github.com/rakoivun/mcp-terminal-enhanced/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rakoivun/mcp-terminal-enhanced/discussions)
- 📖 **Documentation**: Check other files in `docs/` directory

### Issue Template

When reporting issues, include:

```
**Environment:**
- OS: [Windows 11 / macOS 14 / Ubuntu 22.04]
- Python: [3.9.7]
- terminal-controller: [0.1.9]
- IDE: [Cursor / VS Code / Other]

**Configuration:**
[Paste your MCP configuration]

**Error Message:**
[Paste complete error output]

**Debug Output:**
[Paste output from MCP_ENHANCED_DEBUG=1]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Error occurs]
```

## Frequently Asked Questions

### Q: Why does the terminal open in the wrong directory?
A: The wrapper couldn't detect your project root. Add a `.git` directory or `package.json` file, or set `MCP_WORKSPACE_DIR` manually.

### Q: Can I use this with WSL?
A: Yes, set `SHELL=/usr/bin/bash` and `MCP_WORKSPACE_DIR=/mnt/c/your/project`.

### Q: Does this work with virtual environments?
A: Yes, install `terminal-controller` in your virtual environment and use the virtual environment's Python path in the MCP configuration.

### Q: Can I customize the project detection logic?
A: Yes, modify the `PROJECT_MARKERS` list in `terminal_controller_wrapper.py`.

### Q: Is this compatible with the original terminal-controller?
A: Yes, this is a wrapper that enhances the original package without modifying it.