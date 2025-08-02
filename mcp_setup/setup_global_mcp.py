#!/usr/bin/env python3
"""
Setup Global MCP Configuration for Cursor AI
Creates ~/.cursor/mcp.json with terminal-controller auto-start
"""

import os
import json
import sys
from pathlib import Path

def get_cursor_config_dir():
    """Get Cursor configuration directory based on OS"""
    if os.name == 'nt':  # Windows
        return Path.home() / '.cursor'
    else:  # macOS/Linux
        return Path.home() / '.cursor'

def get_current_project_path():
    """Get absolute path to current project"""
    return os.path.abspath(os.path.dirname(__file__))

def create_global_mcp_config():
    """Create global MCP configuration"""
    config_dir = get_cursor_config_dir()
    config_file = config_dir / 'mcp.json'
    project_path = get_current_project_path()
    wrapper_path = os.path.join(project_path, 'terminal_controller_wrapper.py')
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(exist_ok=True)
    
    # MCP configuration
    mcp_config = {
        "mcpServers": {
            "terminal-controller-global": {
                "command": "python",
                "args": [wrapper_path],
                "description": "Global terminal controller with Git Bash support",
                "autoStart": True,
                "env": {
                    "SHELL": "C:/Program Files/Git/bin/bash.exe" if os.name == 'nt' else "/bin/bash",
                    "MCP_WORKSPACE_DIR": project_path
                }
            },
            "context7": {
                "url": "https://mcp.context7.com/mcp",
                "description": "Context7 library documentation access",
                "autoStart": False
            }
        },
        "settings": {
            "autoStartServers": True,
            "enableToolApproval": False,
            "logLevel": "info"
        }
    }
    
    # Check if config file already exists
    if config_file.exists():
        print(f"[INFO] Existing config found: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                existing_config = json.load(f)
            
            # Merge configurations
            if 'mcpServers' not in existing_config:
                existing_config['mcpServers'] = {}
            
            existing_config['mcpServers'].update(mcp_config['mcpServers'])
            existing_config['settings'] = mcp_config['settings']
            
            mcp_config = existing_config
            print("[SUCCESS] Merged with existing configuration")
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Error reading existing config: {e}")
            print("[INFO] Creating new configuration")
    
    # Write configuration
    try:
        with open(config_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        
        print(f"[SUCCESS] Global MCP configuration created: {config_file}")
        print(f"[INFO] Terminal controller path: {wrapper_path}")
        print("\n[INFO] Configuration Summary:")
        print(f"   • Auto-start: Enabled")
        print(f"   • Shell: {mcp_config['mcpServers']['terminal-controller-global']['env']['SHELL']}")
        print(f"   • Workspace: {project_path}")
        print(f"   • Tool approval: Disabled (seamless execution)")
        
        print("\n[INFO] Next Steps:")
        print("   1. Restart Cursor AI")
        print("   2. Check Settings → MCP for green status indicator")
        print("   3. Test in chat: 'List current directory files'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing config: {e}")
        return False

def main():
    print("[INFO] Cursor AI Global MCP Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('terminal_controller_wrapper.py'):
        print("❌ Error: terminal_controller_wrapper.py not found!")
        print("   Please run this script from the nvdiffrast-trials directory")
        sys.exit(1)
    
    # Create global configuration
    success = create_global_mcp_config()
    
    if success:
        print("\n[SUCCESS] Setup completed successfully!")
        print("\n💡 Pro Tips:")
        print("   • Use project-specific .cursor/mcp.json for per-project settings")
        print("   • Global config works across all Cursor projects")
        print("   • Disable auto-start for servers you don't always need")
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
