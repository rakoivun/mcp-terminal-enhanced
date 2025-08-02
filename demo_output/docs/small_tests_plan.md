# Small Tests Plan: Git Bash MCP Integration

## Current Problem
- ✅ Source code modified to use Git Bash (`create_subprocess_exec` with bash.exe)
- ✅ MCP server restarted  
- ❌ Still getting CMD errors for Unix commands (`ls`, `pwd`, `which`)
- ❌ `echo $SHELL` returns literal `$SHELL` (CMD behavior)

## Test Plan: 5-minute incremental tests

### Test 1: Verify Git Bash Path (2 mins)
**Goal**: Confirm Git Bash executable exists and works
```bash
# Test 1a: File exists
ls -la "C:/Program Files/Git/bin/bash.exe"

# Test 1b: Direct execution  
"C:/Program Files/Git/bin/bash.exe" -c "echo test"

# Test 1c: Test with echo
"C:/Program Files/Git/bin/bash.exe" -c "echo hello"
```
**Expected**: All should work, confirming Git Bash is accessible

### Test 2: Debug MCP Source Loading (3 mins)
**Goal**: Verify our modification is actually being used
```bash
# Test 2a: Add debug print to source
# Add: print(f"[DEBUG] Using Git Bash: {cmd}", file=sys.stderr)

# Test 2b: Test simple command
echo "test debug"

# Test 2c: Check server output for debug message
```
**Expected**: Should see debug message in server terminal

### Test 3: Test Alternative Git Bash Paths (2 mins)
**Goal**: Try different Git Bash paths in case path is wrong
```python
# Test 3a: Try usr/bin/bash
"/usr/bin/bash" -c "ls"

# Test 3b: Try different path format
"C:\\Program Files\\Git\\bin\\bash.exe" -c "ls"

# Test 3c: Try direct bash if in PATH
"bash" -c "ls"
```
**Expected**: One of these might work

### Test 4: Minimal Git Bash Test (2 mins)  
**Goal**: Test simplest possible Git Bash command
```bash
# Test 4a: Simple echo with bash
bash -c "echo hello_from_bash"

# Test 4b: Bash version
bash --version

# Test 4c: Test Unix-style path
bash -c "pwd"
```
**Expected**: Should show Unix-style behavior

### Test 5: Check Multiple Python Installations (3 mins)
**Goal**: Verify we're modifying the right terminal_controller
```bash
# Test 5a: Find all terminal_controller.py files
find . -name "terminal_controller.py"

# Test 5b: Check which python is running MCP
which python

# Test 5c: Verify pip package location
pip show terminal-controller
```
**Expected**: Should confirm we're editing the right file

## Quick Tests Sequence (Total: 15 mins)

1. **Test Git Bash directly** (confirm it works)
2. **Add debug logging** (confirm our code runs)  
3. **Try path variations** (find working path)
4. **Test minimal cases** (isolate the issue)
5. **Verify installation** (ensure we're editing right file)

## Success Criteria Per Test

### Test 1 Success: 
- Git Bash executable found and runs commands

### Test 2 Success:
- Debug messages appear in MCP server output
- Confirms our modified code is running

### Test 3 Success:
- Unix commands work with corrected path
- `ls`, `pwd` return Unix-style output

### Test 4 Success:
- Basic bash commands work through MCP
- `echo $SHELL` shows actual shell path

### Test 5 Success:
- Only one terminal_controller.py found
- We're editing the active version

## If All Tests Fail
**Fallback**: Create wrapper script approach instead of direct source modification

## Next Step
Start with **Test 1** - verify Git Bash basics work outside MCP context