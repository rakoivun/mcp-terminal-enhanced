# Basic Usage Examples

## Quick Start

### 1. Simple Project Setup

```bash
# Clone the enhanced MCP terminal
git clone https://github.com/rakoivun/mcp-terminal-enhanced.git
cd mcp-terminal-enhanced

# Install dependencies
pip install terminal-controller

# Test the wrapper
python src/terminal_controller_wrapper.py --version
```

### 2. Add to Your Project

```bash
# Copy to your project
cp src/terminal_controller_wrapper.py /path/to/your/project/

# Update MCP configuration
cat >> ~/.cursor/mcp_wrapper_config.json << 'EOF'
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/your/project/terminal_controller_wrapper.py"]
    }
  }
}
EOF
```

## Common Use Cases

### Development Workflow

```bash
# Navigate to your project
cd ~/projects/my-web-app

# The MCP terminal will automatically start here
# Run common development commands:
npm install
npm run dev
git status
git add .
git commit -m "Feature update"
```

### Python Project Development

```bash
# In a Python project with pyproject.toml or setup.py
cd ~/projects/my-python-app

# Virtual environment commands work seamlessly
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows Git Bash
pip install -r requirements.txt
python -m pytest
```

### Multi-Language Projects

```bash
# Go project
cd ~/projects/my-go-app
go mod tidy
go run main.go

# Rust project  
cd ~/projects/my-rust-app
cargo build
cargo test

# Node.js project
cd ~/projects/my-node-app
npm install
npm test
```

## Working with Different Project Types

### Git Repository

The wrapper automatically detects Git repositories:

```bash
# Any directory with .git/ will be detected as project root
/home/user/projects/my-app/
├── .git/                    # ← Detected as project marker
├── src/
├── tests/
└── README.md

# Terminal will start in /home/user/projects/my-app/
```

### Node.js Project

Detects `package.json` as project marker:

```bash
# Project structure
/home/user/projects/web-app/
├── package.json             # ← Detected as project marker
├── src/
├── public/
└── node_modules/

# Common commands that work:
npm install
npm run build
npm test
npm start
```

### Python Project

Detects various Python project markers:

```bash
# Modern Python project
/home/user/projects/ml-app/
├── pyproject.toml           # ← Detected as project marker
├── src/
├── tests/
└── README.md

# Traditional Python project  
/home/user/projects/legacy-app/
├── setup.py                 # ← Detected as project marker
├── mypackage/
└── requirements.txt

# Common commands:
pip install -e .
python -m pytest
python setup.py build
```

## Environment Configuration Examples

### Custom Workspace Directory

```bash
# Override automatic detection
export MCP_WORKSPACE_DIR="/path/to/specific/workspace"

# Or in MCP configuration:
{
  "mcpServers": {
    "terminal-controller": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/custom/workspace/path"
      }
    }
  }
}
```

### Windows Git Bash Setup

```bash
# The wrapper automatically finds Git Bash, but you can override:
export SHELL="C:/Program Files/Git/bin/bash.exe"

# Test Unix commands work:
ls -la
grep -r "TODO" src/
find . -name "*.py" | xargs wc -l
```

### Debug Mode

```bash
# Enable debug output to see what's happening
MCP_ENHANCED_DEBUG=1 python terminal_controller_wrapper.py

# Output will show:
# [MCP Enhanced] Starting terminal controller...
# [MCP Enhanced] Workspace: /detected/project/path
# [MCP Enhanced] Git Bash: C:/Program Files/Git/bin/bash.exe
```

## Integration Examples

### Cursor IDE Workflow

1. **Open project in Cursor:**
   ```bash
   cursor /path/to/your/project
   ```

2. **Terminal automatically starts in project root:**
   ```bash
   pwd  # Shows: /path/to/your/project
   ```

3. **Run development commands:**
   ```bash
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   
   # Run tests in watch mode
   npm run test:watch
   ```

### VS Code Workflow

1. **Configure in settings.json:**
   ```json
   {
     "mcp.servers": {
       "terminal-controller": {
         "command": "python",
         "args": ["/path/to/terminal_controller_wrapper.py"]
       }
     }
   }
   ```

2. **Open integrated terminal:**
   - Terminal starts in project workspace
   - All commands run in correct context

### Command Line Development

Even without an IDE, the enhanced terminal is useful:

```bash
# Start the MCP server manually for testing
python terminal_controller_wrapper.py

# Use with tmux or screen for persistent sessions
tmux new-session -d 'python terminal_controller_wrapper.py'
```

## Advanced Usage Patterns

### Multi-Project Development

Set up different configurations for different projects:

```json
{
  "mcpServers": {
    "frontend-terminal": {
      "command": "python",
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/projects/frontend-app"
      }
    },
    "backend-terminal": {
      "command": "python", 
      "args": ["/path/to/terminal_controller_wrapper.py"],
      "env": {
        "MCP_WORKSPACE_DIR": "/projects/backend-api"
      }
    }
  }
}
```

### Monorepo Development

For large monorepos, point to specific subdirectories:

```bash
# For a monorepo like:
/workspace/monorepo/
├── .git/
├── apps/
│   ├── web-app/
│   ├── mobile-app/
│   └── admin-panel/
└── packages/
    ├── shared-ui/
    └── shared-utils/

# Configure for specific app:
export MCP_WORKSPACE_DIR="/workspace/monorepo/apps/web-app"
```

### Docker Development

Works great with Docker-based development:

```bash
# In your project root (auto-detected)
docker-compose up -d
docker-compose exec app bash
docker logs -f app

# Build and test
docker build -t myapp .
docker run --rm myapp npm test
```

## Tips and Best Practices

### 1. Project Organization
- Always use version control (`.git` directory)
- Include project metadata files (`package.json`, `pyproject.toml`, etc.)
- Keep your project structure consistent

### 2. Environment Management  
- Use virtual environments for Python projects
- Use `.nvmrc` for Node.js version consistency
- Document environment setup in README

### 3. Configuration
- Use absolute paths in MCP configuration
- Test configuration changes by restarting your IDE
- Keep backup of working configurations

### 4. Troubleshooting
- Enable debug mode when issues occur
- Check project detection with `MCP_ENHANCED_DEBUG=1`
- Verify dependencies are installed in correct environment

## Next Steps

- Read [Configuration Guide](../docs/configuration.md) for advanced options
- Check [Troubleshooting Guide](../docs/troubleshooting.md) for common issues
- See [Development Guide](../docs/development.md) for customization