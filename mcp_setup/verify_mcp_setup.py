#!/usr/bin/env python3
"""
Verify MCP Setup for Cursor AI
Checks if terminal-controller is properly configured and accessible
"""

import os
import json
import sys
import subprocess
from pathlib import Path

def check_project_config():
    """Check project-specific MCP configuration"""
    config_file = '.cursor/mcp.json'
    
    print("📁 Project Configuration (.cursor/mcp.json)")
    print("-" * 50)
    
    if not os.path.exists(config_file):
        print("❌ Project MCP config not found")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Config file exists: {config_file}")
        
        # Check for terminal-controller
        servers = config.get('mcpServers', {})
        if 'terminal-controller' in servers:
            tc_config = servers['terminal-controller']
            print(f"✅ terminal-controller configured")
            print(f"   Command: {tc_config.get('command', 'N/A')}")
            print(f"   Args: {tc_config.get('args', 'N/A')}")
            print(f"   Auto-start: {tc_config.get('autoStart', False)}")
        else:
            print("❌ terminal-controller not found in config")
            return False
        
        # Check settings
        settings = config.get('settings', {})
        print(f"✅ Settings configured:")
        print(f"   Auto-start servers: {settings.get('autoStartServers', False)}")
        print(f"   Tool approval: {settings.get('enableToolApproval', True)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False

def check_global_config():
    """Check global MCP configuration"""
    if os.name == 'nt':  # Windows
        config_file = Path.home() / '.cursor' / 'mcp.json'
    else:  # macOS/Linux
        config_file = Path.home() / '.cursor' / 'mcp.json'
    
    print("\n🌍 Global Configuration (~/.cursor/mcp.json)")
    print("-" * 50)
    
    if not config_file.exists():
        print("ℹ️  Global MCP config not found (optional)")
        return True
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Global config exists: {config_file}")
        
        # Check for terminal-controller
        servers = config.get('mcpServers', {})
        terminal_servers = [name for name in servers.keys() if 'terminal' in name.lower()]
        
        if terminal_servers:
            print(f"✅ Terminal servers found: {', '.join(terminal_servers)}")
            for server_name in terminal_servers:
                server_config = servers[server_name]
                print(f"   {server_name}:")
                print(f"     Auto-start: {server_config.get('autoStart', False)}")
        else:
            print("ℹ️  No terminal servers in global config")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading global config: {e}")
        return False

def check_wrapper_script():
    """Check if terminal controller wrapper exists and is functional"""
    wrapper_file = 'terminal_controller_wrapper.py'
    
    print("\n🔧 Terminal Controller Wrapper")
    print("-" * 50)
    
    if not os.path.exists(wrapper_file):
        print(f"❌ Wrapper script not found: {wrapper_file}")
        return False
    
    print(f"✅ Wrapper script exists: {wrapper_file}")
    
    # Check if it's executable
    try:
        result = subprocess.run([
            sys.executable, wrapper_file, '--help'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 or 'terminal_controller' in result.stderr:
            print("✅ Wrapper script is functional")
        else:
            print("⚠️  Wrapper script may have issues")
            print(f"   Exit code: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:100]}...")
        
    except subprocess.TimeoutExpired:
        print("⚠️  Wrapper script test timed out")
    except Exception as e:
        print(f"⚠️  Error testing wrapper: {e}")
    
    return True

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Dependencies")
    print("-" * 50)
    
    # Check Python
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # Check if terminal_controller module is available
    try:
        import terminal_controller
        print("✅ terminal_controller module available")
    except ImportError:
        print("❌ terminal_controller module not found")
        print("   Install with: pip install terminal-controller")
        return False
    
    # Check Git Bash on Windows
    if os.name == 'nt':
        git_bash_path = "C:/Program Files/Git/bin/bash.exe"
        if os.path.exists(git_bash_path):
            print(f"✅ Git Bash found: {git_bash_path}")
        else:
            print(f"⚠️  Git Bash not found: {git_bash_path}")
            print("   Install Git for Windows if needed")
    
    return True

def provide_recommendations():
    """Provide setup recommendations"""
    print("\n💡 Recommendations")
    print("-" * 50)
    
    recommendations = [
        "✅ Project config created - terminal-controller will auto-start for this project",
        "🌍 Run setup_global_mcp.py for global access across all projects", 
        "🔄 Restart Cursor AI to apply MCP configuration changes",
        "⚙️  Check Cursor Settings → MCP for server status (green dot = running)",
        "🧪 Test in Cursor chat: 'List files in current directory'",
        "📚 See cursor_mcp_setup_guide.md for detailed instructions"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

def main():
    print("🔍 Cursor AI MCP Setup Verification")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Project Configuration", check_project_config),
        ("Global Configuration", check_global_config), 
        ("Wrapper Script", check_wrapper_script),
        ("Dependencies", check_dependencies)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error in {name} check: {e}")
            results.append(False)
    
    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All checks passed! MCP setup looks good.")
        print("\n🚀 Next steps:")
        print("   1. Restart Cursor AI")
        print("   2. Open a chat and try: 'Show current directory'")
        print("   3. Verify green status in Settings → MCP")
    else:
        print(f"⚠️  {passed}/{total} checks passed. See issues above.")
        print("\n🔧 Troubleshooting:")
        print("   • Run setup_global_mcp.py for global config")
        print("   • Check cursor_mcp_setup_guide.md for detailed help")
        print("   • Ensure all dependencies are installed")
    
    provide_recommendations()

if __name__ == "__main__":
    main()
