# Fix Terminal Controller Duplicate Entries Plan

## Problem
Still seeing 2 "terminal-controller" entries in Cursor MCP interface after restart:
- One with "10 tools enabled" ✅ 
- One with "No tools or prompts" ❌

## Investigation Results ✅

### Found 3 Config Files with terminal-controller:

1. **`.cursor/mcp.json`** (HIDDEN CULPRIT!)
   - Name: "terminal-controller" 
   - Path: "terminal_controller_wrapper.py" ❌ BROKEN (missing src/ and full path)
   - Status: "No tools or prompts" ❌

2. **`mcp_wrapper_config.json`** (root)
   - Name: "terminal-controller"
   - Path: "C:\\code\\nvdiffrast-trials\\src\\terminal_controller_wrapper.py" ✅ WORKING
   - Status: "10 tools enabled" ✅

3. **`config/mcp_wrapper_config.json`** 
   - Name: "terminal-controller-enhanced" ✅ PROPERLY NAMED
   - Name: "terminal-controller-legacy" 
   - Paths: Both correct ✅

### Root Cause
The hidden `.cursor/mcp.json` file has a broken terminal-controller entry that's causing the duplicate "No tools or prompts" entry!

## Proposed Solution Strategy

### ✅ RECOMMENDED: Fix the Hidden Culprit
**Action**: Remove the broken "terminal-controller" entry from `.cursor/mcp.json`
**Keep**: The working "terminal-controller" in `mcp_wrapper_config.json` (root)
**Result**: Single working entry with proper path

### Alternative: Use Proper Naming  
**Action**: Switch to use `config/mcp_wrapper_config.json` with "terminal-controller-enhanced"
**Remove**: All "terminal-controller" entries from other files
**Result**: Proper naming convention with enhanced vs legacy options

## Implementation Plan
1. ✅ **Investigation**: Found all config files with terminal-controller
2. ✅ **Analysis**: Identified `.cursor/mcp.json` as the hidden culprit
3. ✅ **Cleanup**: Removed the broken entry from `.cursor/mcp.json`
4. ✅ **Git Commit**: Changes committed to git (commit 1a87bed)
5. ✅ **Verification**: Restarted Cursor - confirmed single working entry
6. ✅ **Naming Fix**: Updated to use "terminal-controller-enhanced" for proper naming
7. ✅ **Git Push**: Changes pushed to origin (commit 4a0a635)
8. ✅ **Global Config Fix**: Found and updated global config at /c/Users/rami/.cursor/mcp.json
9. **Documentation**: Final working configuration completed

## Root Cause Resolution ✅
The issue was that the **global Cursor config** had the old "terminal-controller" name and was taking precedence over local project configs. All configs now use "terminal-controller-enhanced".

## Success Criteria
- Only ONE terminal-controller entry visible in Cursor MCP interface
- That entry shows "10 tools enabled"
- No "No tools or prompts" entries
- Terminal controller functions properly

---
*Status: PLANNING - Ready for investigation phase*