# MCP Terminal Enhanced

Self-sufficient terminal controller for Model Context Protocol (MCP) with Git Bash integration.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-Working-brightgreen.svg)

## Features

- **Standalone** - No external dependencies
- **10 Terminal Tools** - Complete command execution, file operations, directory management
- **Git Bash Support** - Unix commands on Windows
- **Auto-detect Workspace** - Finds project root automatically
- **Auto-start** - Launches with Cursor

## Quick Setup

1. **Install MCP framework:**
   ```bash
   pip install mcp
   ```

2. **Clone and configure:**
   ```bash
   git clone https://github.com/rakoivun/mcp-terminal-enhanced.git
   ```

3. **Add to Cursor MCP config:**
   ```json
   {
     "mcpServers": {
       "terminal-controller-standalone": {
         "command": "python",
         "args": ["/path/to/mcp-terminal-enhanced/src/terminal_controller_standalone.py"],
         "autoStart": true
       }
     }
   }
   ```

4. **Restart Cursor**

## Tools Available

- `execute_command` - Run shell commands
- `get_command_history` - View recent commands  
- `get_current_directory` - Show working directory
- `change_directory` - Navigate directories
- `list_directory` - List directory contents
- `read_file` - Read file contents
- `write_file` - Write to files
- `delete_file` - Delete files
- `insert_file_content` - Insert content at specific line
- `update_file_content` - Update specific file content

## Project Detection

Automatically detects workspace root by finding:
- `.git` directory
- `package.json`, `pyproject.toml`, `setup.py`
- `Cargo.toml`, `go.mod`

## Troubleshooting

**Server won't start?**
- Check Python path in MCP config
- Ensure `autoStart: true` is set
- Restart Cursor after config changes

**Commands timeout?**
- Verify Git Bash is installed (Windows)
- Check file permissions

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE)

## Credits

Built on [terminal-controller-mcp](https://github.com/GongRzhe/terminal-controller-mcp) by GongRzhe.