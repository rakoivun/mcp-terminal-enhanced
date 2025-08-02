# Git Bash Terminal Controller MCP - Modification Plan

## Problem Analysis
- Existing Terminal Controller MCP hardcoded for Windows CMD
- Environment variable approaches failed due to subprocess spawning
- Need native Git Bash integration in the MCP server itself

## SOLUTION: Modify Terminal Controller MCP Source

### Why This Approach Works
1. **Full Control**: Modify shell spawning logic directly
2. **Maintain Features**: Keep all security, MCP protocol, file operations
3. **Clean Integration**: Native Git Bash instead of workarounds
4. **Open Source**: Terminal Controller MCP is available on GitHub

## Implementation Plan

### Phase 1: Source Code Analysis (15 minutes)
1. **Download Terminal Controller source** from GitHub repo
2. **Locate shell execution code** - find where `subprocess` or shell commands are spawned
3. **Identify modification points** - where CMD is hardcoded for Windows

### Phase 2: Modification Implementation (30 minutes)  
1. **Backup original** Terminal Controller installation
2. **Modify shell execution** to use Git Bash:
   ```python
   # Instead of: subprocess.run(command, shell=True)  # Uses CMD
   # Use: subprocess.run(command, shell=True, executable="C:/Program Files/Git/bin/bash.exe")
   ```
3. **Test modifications** with simple commands

### Phase 3: Integration & Testing (20 minutes)
1. **Install modified version** in our virtual environment
2. **Update MCP configuration** to use modified server
3. **Test Unix commands**: `ls -la`, `pwd`, `which bash`
4. **Verify all MCP functions** still work

### Phase 4: Validation (10 minutes)
1. **Test Git operations**: `git status`, `git log`
2. **Verify file operations**: read, write, delete
3. **Confirm no hanging issues**

## Technical Implementation Details

### Key Files to Modify (Expected):
- `terminal_controller.py` - Main server file
- Shell execution functions that use `subprocess`
- Windows-specific shell detection logic

### Modification Strategy:
```python
# Current (Windows CMD):
process = subprocess.Popen(command, shell=True, ...)

# Modified (Git Bash):  
process = subprocess.Popen(
    command, 
    shell=True, 
    executable="C:/Program Files/Git/bin/bash.exe",
    ...
)
```

### Expected Benefits:
- ✅ Native Unix commands (`ls`, `rm`, `cp`, `grep`)
- ✅ Git command integration (`git status`, `git commit`)
- ✅ Proper PATH environment with Unix tools
- ✅ Maintain all MCP security and protocol features

## Risk Assessment
**Low Risk**: 
- Modification is straightforward (change shell executable)
- Easy rollback to original version
- Source code is available and readable

## Success Criteria
- [ ] `ls -la` works via MCP
- [ ] `git status` works via MCP  
- [ ] File operations work normally
- [ ] No hanging or timeout issues
- [ ] All MCP protocol functions respond

## Fallback Plan
If modification fails:
- Revert to original Terminal Controller MCP
- Keep current working Windows CMD setup
- Consider creating custom MCP server from scratch

---
**Time Estimate**: 75 minutes total
**Difficulty**: Medium (straightforward Python subprocess modification)
**Success Probability**: High (direct source modification)