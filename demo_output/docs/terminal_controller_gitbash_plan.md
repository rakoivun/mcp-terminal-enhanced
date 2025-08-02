# Terminal Controller Git Bash Integration Plan

## Problem Analysis

### Current Status
- ✅ Terminal Controller MCP working with default Windows shell
- ❌ Git Bash environment variables caused MCP server to hang
- ✅ Configuration successfully reverted to working state
- 🔄 Need alternative approach for Git Bash integration

### Root Cause Analysis
**Issue**: Adding `SHELL` and `COMSPEC` environment variables to MCP config caused timeouts
**Hypothesis**: Terminal Controller may not properly handle shell environment overrides via MCP config

## Alternative Approaches for Git Bash Integration

### Option A: Terminal Controller Source Code Modification (HIGH EFFORT)
**Approach**: Modify Terminal Controller to use Git Bash by default
**Pros**: 
- Complete control over shell behavior
- Native Git Bash integration
**Cons**: 
- Requires forking/modifying the source code
- Maintenance burden for updates

### Option B: Wrapper Script Approach (MEDIUM EFFORT)
**Approach**: Create a wrapper script that sets Git Bash environment before launching Terminal Controller
**Pros**: 
- No source code changes needed
- Clean separation of concerns
**Cons**: 
- Additional layer of complexity
- May still have environment issues

### Option C: Environment Variable Setup (LOW EFFORT - RECOMMENDED)
**Approach**: Set system-wide or session-wide environment variables
**Pros**: 
- Simple implementation
- Affects all terminal operations
- No MCP config changes needed
**Cons**: 
- May affect other applications

### Option D: Hybrid Approach (FALLBACK)
**Approach**: Keep current working setup, use Git Bash commands via specific tool calls
**Pros**: 
- Guaranteed to work
- Best of both worlds
**Cons**: 
- Mixed command syntax

## RECOMMENDED PLAN - Option C: Environment Variables

### Phase 1: Environment Setup (10 minutes)
1. **Test current working state** 
   - Verify Terminal Controller MCP responds
   - Confirm basic commands work
   
2. **Set session environment variables**
   ```bash
   export SHELL="/c/Program Files/Git/bin/bash.exe"
   export COMSPEC="/c/Program Files/Git/bin/bash.exe"
   ```

3. **Restart Terminal Controller with new environment**

### Phase 2: Testing & Validation (10 minutes)
1. **Test Unix commands**: `ls -la`, `pwd`, `which bash`
2. **Test file operations**: `rm`, `cp`, `mv`
3. **Test Git integration**: `git status`, `git log --oneline`
4. **Verify MCP communication**: All tool functions work

### Phase 3: Persistence Setup (5 minutes)
1. **Add to bash profile** if successful
2. **Document working configuration**
3. **Update memory with final setup**

## Fallback Strategy
If environment variables still cause issues:
- **Immediate**: Revert to working Windows shell setup
- **Medium-term**: Implement Option D (hybrid approach)
- **Long-term**: Consider Option B (wrapper script)

## Success Criteria
- [ ] Terminal Controller MCP responds to all tool calls
- [ ] Unix-style commands work (`ls`, `rm`, `cp`, etc.)
- [ ] Git commands work natively
- [ ] No hanging or timeout issues
- [ ] File operations work correctly

## Risk Assessment
**Low Risk**: Environment variables are easily reversible
**Mitigation**: Can quickly revert by unsetting variables
**Testing**: Start with temporary session variables before making permanent

---
**Time Estimate**: 25 minutes total
**Ready to proceed?** This approach minimizes risk while testing Git Bash integration.