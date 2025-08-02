# Terminal Controller Subprocess Fix Plan

## Current Problem
- ✅ **10 tools created** in standalone version
- ✅ **File operations working** (list_directory, get_current_directory)
- ❌ **Command execution timing out** (execute_command fails)
- ❌ **Same issue affects all subprocess commands**

## Root Cause Analysis
Based on your documentation, this is the **Git Bash subprocess hanging issue** that was already solved before. The solution involves proper subprocess configuration in MCP context.

## Investigation Plan

### Phase 1: Test Current Approaches (15 min)
1. **Test simple subprocess outside MCP context**
   - Create test script that mimics our subprocess call
   - Verify if issue is MCP-specific or general subprocess issue
   
2. **Test different subprocess configurations**
   - `stdin=DEVNULL` (already tried)
   - `shell=True` vs `shell=False` 
   - `create_subprocess_exec` vs `create_subprocess_shell`

3. **Test timeout values**
   - Maybe 30 second timeout is too short
   - Try 60 seconds or no timeout

### Phase 2: Find Working Solution (20 min)
1. **Check git history for working version**
   - Look at commits when terminal controller was working
   - Compare subprocess implementation

2. **Test your documented solutions**
   - Solution 1: `stdin=asyncio.subprocess.DEVNULL` ✅ (tried)
   - Solution 2: `shell=True, executable=git_bash` ✅ (tried)
   - Solution 3: Direct exec without -c flag
   - Solution 4: Simple 'bash' instead of full path

3. **Test alternative approaches**
   - Use threading instead of asyncio
   - Use regular subprocess with proper async wrapper

### Phase 3: Implementation (15 min)
1. **Apply working solution**
2. **Test with various commands**
   - `echo "test"`
   - `pwd`
   - `ls` (Unix) / `dir` (Windows)
   - `git status`

3. **Verify all 10 tools work**

## Testing Strategy

### Test Script Approach
Create `test_subprocess_fix.py` to isolate the issue:
```python
import asyncio
import subprocess

async def test_various_approaches():
    # Test 1: Simple subprocess.run (synchronous)
    # Test 2: asyncio subprocess with various configs
    # Test 3: Threading approach
    # Test 4: Different shells and executables
```

### Progressive Testing
1. **Start simple**: Test outside MCP context
2. **Add complexity**: Test with MCP framework
3. **Add Git Bash**: Once basic working, add Git Bash
4. **Integration**: Full terminal controller test

## Expected Solutions

### Most Likely (from your docs):
```python
# Solution from fix_gitbash_mcp_plan.md
process = await asyncio.create_subprocess_exec(
    "C:/Program Files/Git/bin/bash.exe", "-c", cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    stdin=asyncio.subprocess.DEVNULL
)
```

### Alternative Approaches:
1. **Threading wrapper** around subprocess.run
2. **Different MCP framework** subprocess handling
3. **Environment variable fixes** (like your nvdiffrast solution)

## Success Criteria
- ✅ `echo "test"` returns immediately (< 1 second)
- ✅ `pwd` returns current directory
- ✅ Commands work consistently
- ✅ All 10 tools functional
- ✅ Auto-starts with Cursor

## Next Steps
1. Create test script to isolate issue
2. Test systematically through documented solutions
3. Implement working solution
4. Verify full functionality

Would you like me to proceed with Phase 1 testing?