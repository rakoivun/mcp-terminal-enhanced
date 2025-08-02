# MCP Terminal Enhanced

Enhanced terminal controller for Model Context Protocol (MCP) with smart workspace detection and Git Bash support on Windows.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🏗️ About This Project

This project is an **enhancement wrapper** built on top of the excellent [terminal-controller-mcp](https://github.com/GongRzhe/terminal-controller-mcp) package by **GongRzhe**. 

The original terminal-controller provides the core MCP terminal functionality, while this project adds:
- Smart workspace detection
- Cross-platform Git Bash integration  
- Dynamic configuration
- Comprehensive troubleshooting tools

**Full credit goes to GongRzhe for the foundational terminal-controller-mcp package that makes this project possible.**

## ✨ Features

- 🎯 **Smart Project Detection** - Automatically detects workspace root using common project markers
- 🐚 **Git Bash Integration** - Full Unix command support on Windows with Git Bash
- 📁 **Dynamic Workspace** - No hard-coded paths, works with any project structure  
- 🔧 **Easy Configuration** - Simple JSON-based setup
- 🛠️ **Comprehensive Troubleshooting** - Tested solutions for common MCP issues
- 🔄 **Zero Site-packages Modification** - Clean wrapper approach that doesn't modify installed packages

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [terminal-controller](https://github.com/GongRzhe/terminal-controller-mcp) MCP package
- Git Bash (Windows only) - Comes with Git for Windows

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/rakoivun/mcp-terminal-enhanced.git
   cd mcp-terminal-enhanced
   ```

2. **Install the base terminal controller:**
   ```bash
   pip install terminal-controller
   ```

3. **Copy the wrapper to your project:**
   ```bash
   cp src/terminal_controller_wrapper.py /path/to/your/project/
   ```

4. **Update your MCP configuration:**
   ```json
   {
     "mcpServers": {
       "terminal-controller": {
         "command": "python",
         "args": ["/path/to/your/project/terminal_controller_wrapper.py"]
       }
     }
   }
   ```

## 📋 How It Works

### Smart Project Detection

The wrapper automatically finds your project root by looking for common markers:
- `.git` directory
- `package.json` (Node.js projects)
- `pyproject.toml` (Python projects)
- `setup.py` (Python projects)
- `Cargo.toml` (Rust projects)
- `go.mod` (Go projects)

### Git Bash Integration (Windows)

On Windows, the wrapper automatically:
- Detects Git Bash installation
- Sets proper environment variables
- Enables Unix-style command execution
- Provides consistent cross-platform behavior

### Environment Variables

The wrapper sets these environment variables for the MCP server:
- `MCP_WORKSPACE_DIR` - Automatically detected project root
- `SHELL` - Git Bash path (Windows only)
- `COMSPEC` - Git Bash path (Windows only)

## 🔧 Configuration

### Basic Configuration

Create or update your MCP configuration file:

```json
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["./terminal_controller_wrapper.py"]
    }
  }
}
```

### Advanced Configuration

You can override the workspace directory by setting an environment variable:

```bash
export MCP_WORKSPACE_DIR="/custom/workspace/path"
```

Or in your wrapper script:
```python
os.environ['MCP_WORKSPACE_DIR'] = '/custom/workspace/path'
```

## 📁 Project Structure

```
mcp-terminal-enhanced/
├── README.md
├── LICENSE
├── src/
│   ├── terminal_controller_wrapper.py    # Main enhanced wrapper
│   └── gitbash_terminal_controller.py    # Legacy Git Bash wrapper
├── config/
│   ├── mcp_wrapper_config.json          # Example MCP configuration
│   └── cursor_mcp_config.json           # Cursor-specific configuration
├── docs/
│   ├── installation.md                  # Detailed installation guide
│   ├── configuration.md                 # Configuration options
│   ├── troubleshooting.md               # Common issues and solutions
│   └── development.md                   # Development guidelines
├── tests/
│   ├── test_project_detection.py        # Test project root detection
│   ├── test_environment_setup.py        # Test environment configuration
│   └── test_gitbash_integration.py      # Test Git Bash functionality
└── examples/
    ├── basic_usage.md                   # Basic usage examples
    ├── cursor_integration.md            # Cursor IDE integration
    └── troubleshooting_scenarios.md     # Common troubleshooting scenarios
```

## 🐛 Troubleshooting

### Common Issues

1. **MCP server doesn't start in project directory**
   - Ensure your project has a recognizable marker (`.git`, `package.json`, etc.)
   - Check that the wrapper script has execute permissions
   - Verify the path in your MCP configuration

2. **Git Bash commands fail on Windows**
   - Ensure Git for Windows is installed
   - Check that Git Bash is in the default location: `C:/Program Files/Git/bin/bash.exe`
   - Try running the wrapper script directly to see error messages

3. **Permission denied errors**
   - Ensure the wrapper script has execute permissions: `chmod +x terminal_controller_wrapper.py`
   - Check that your user has permissions to the detected workspace directory

### Debug Mode

Add debug output to see what's happening:

```python
import os
print(f"[DEBUG] Detected project root: {get_project_root()}", file=sys.stderr)
print(f"[DEBUG] MCP_WORKSPACE_DIR: {os.environ.get('MCP_WORKSPACE_DIR')}", file=sys.stderr)
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -r requirements-dev.txt`
5. Run tests: `python -m pytest tests/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Attribution

This project builds upon the excellent work of:
- [terminal-controller-mcp](https://github.com/GongRzhe/terminal-controller-mcp) by **GongRzhe**

For complete attribution details, see [CREDITS.md](CREDITS.md).

## 🙏 Acknowledgments

- **GongRzhe** for creating the foundational [terminal-controller-mcp](https://github.com/GongRzhe/terminal-controller-mcp) package
- **Anthropic** for the Model Context Protocol specification
- **Git for Windows** team for providing Git Bash
- The open source community for inspiration and feedback

For detailed credits and attribution, see [CREDITS.md](CREDITS.md).

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/rakoivun/mcp-terminal-enhanced/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rakoivun/mcp-terminal-enhanced/discussions)
- 📧 **Email**: Create an issue for support requests

---

**⭐ If this project helps you, please consider giving it a star!**