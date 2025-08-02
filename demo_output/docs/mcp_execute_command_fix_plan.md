# MCP Terminal Controller execute_command Fix Plan

## Current Status Summary

### ✅ What's Working
- **MCP Server Connection**: Fully operational, green status
- **File Operations**: get_current_directory, change_directory, list_directory, read_file all work perfectly
- **Environment**: COMSPEC correctly points to cmd.exe, PATH includes system32
- **Subprocess Code**: Direct testing proves the asyncio.create_subprocess_shell code works fine

### ❌ What's Broken  
- **execute_command**: Always times out after 5-15 seconds for ANY command (even "echo test")
- **get_command_history**: Empty because execute_command never succeeds

### 🔍 Key Discoveries
1. **Root Cause**: Issue is MCP framework-specific, NOT subprocess-related
2. **Working Directory Mismatch**: MCP runs in `C:\code\nvdiffrast-trials\nvdiffrast`, normal Python in different dirs
3. **Environment Difference**: MCP uses STDIO communication, not interactive terminal
4. **Code Verification**: Exact same subprocess code works perfectly outside MCP context

## Diagnostic Plan

### Phase 1: Working Directory Investigation ⏱️ 15 mins
**Hypothesis**: Wrong working directory causes subprocess to fail or hang

**Actions**:
1. **Test working directory impact**
   - Create test script that changes to different directories
   - Run subprocess from various working directories  
   - Compare success rates

2. **Check MCP working directory handling**
   - Verify where MCP server actually runs commands
   - Test if change_directory affects execute_command
   - Check for path resolution issues

**Success Criteria**: Determine if working directory affects subprocess execution

### Phase 2: MCP Framework Investigation ⏱️ 20 mins  
**Hypothesis**: MCP STDIO communication interferes with subprocess execution

**Actions**:
1. **Analyze MCP server logs**
   - Look for subprocess timeout errors in MCP output
   - Check for asyncio event loop issues
   - Identify any Windows-specific MCP problems

2. **Test subprocess isolation**
   - Try different subprocess creation methods in MCP context
   - Test with creationflags on Windows (DETACHED_PROCESS, etc.)
   - Experiment with different shell/executable parameters

3. **Test timeout variations**
   - Try longer timeouts (30s, 60s)
   - Test immediate vs delayed subprocess creation
   - Check if process.communicate() is the bottleneck

**Success Criteria**: Identify specific MCP framework interference

### Phase 3: Source Code Modification ⏱️ 25 mins
**Hypothesis**: Minor subprocess parameter tweaks can resolve the issue

**Actions**:
1. **Windows subprocess flags**
   ```python
   process = await asyncio.create_subprocess_shell(
       cmd,
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE,
       shell=True,
       creationflags=subprocess.CREATE_NO_WINDOW  # Windows-specific
   )
   ```

2. **Alternative subprocess methods**
   - Try `create_subprocess_exec` instead of `create_subprocess_shell`
   - Test direct cmd.exe execution: `["cmd.exe", "/c", cmd]`
   - Experiment with different shell parameter values

3. **Error handling improvements**
   - Add more detailed logging in subprocess section
   - Capture process creation vs communication timing
   - Add Windows-specific error handling

**Success Criteria**: execute_command works without timeouts

### Phase 4: Workaround Implementation ⏱️ 10 mins
**If Phases 1-3 fail**: Implement production-ready workaround

**Actions**:
1. **Document the limitation**
   - Update memory with confirmed execute_command limitation
   - Document which functions work vs don't work

2. **Optimize working functions**
   - Focus on file operations automation
   - Create helper scripts for common command patterns
   - Integration guide for hybrid MCP + terminal usage

**Success Criteria**: Clear documentation and optimized workflow

## Implementation Order

### Priority 1: Quick Wins (15 mins)
1. Test working directory theory - likely culprit
2. Try simple subprocess parameter tweaks
3. Test longer timeouts

### Priority 2: Deep Investigation (25 mins)  
1. MCP framework analysis
2. Windows subprocess flags testing
3. Alternative subprocess methods

### Priority 3: Fallback (10 mins)
1. Document limitations if unfixable
2. Optimize working functionality

## Success Metrics

### Minimum Success
- ✅ Understand root cause of timeout
- ✅ Document what works vs doesn't work
- ✅ Clear hybrid usage strategy

### Optimal Success  
- ✅ execute_command works for basic commands
- ✅ get_command_history shows executed commands
- ✅ Full MCP functionality restored

## Risk Assessment

**Low Risk**: File operations already work perfectly  
**Medium Risk**: execute_command might be fundamentally incompatible with MCP STDIO  
**Mitigation**: Hybrid approach already proven effective

## Timeline: 70 minutes total
- **Phase 1**: 15 mins
- **Phase 2**: 20 mins  
- **Phase 3**: 25 mins
- **Phase 4**: 10 mins

## Next Steps
1. **START**: Phase 1 - Working Directory Investigation
2. **User approval**: Confirm plan before execution
3. **Execute systematically**: One phase at a time
4. **Update progress**: Document findings after each phase