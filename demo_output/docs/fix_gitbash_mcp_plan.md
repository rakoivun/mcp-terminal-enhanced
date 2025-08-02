# Fix Git Bash MCP Execution Plan

## Problem Summary
- ✅ **CMD execution in MCP**: WORKS (we saw successful `dir`, `echo` commands)
- ❌ **Git Bash execution in MCP**: TIMES OUT (all commands timeout after 10 seconds)

## Root Cause Analysis
The issue is specific to **Git Bash subprocess execution within MCP context**, not general MCP timeouts.

**Current Git Bash approach (failing):**
```python
process = await asyncio.create_subprocess_exec(
    "C:/Program Files/Git/bin/bash.exe", "-c", cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
)
```

**Working CMD approach:**
```python
process = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    shell=True
)
```

## Potential Solutions to Try (in order)

### Solution 1: Add stdin=DEVNULL to Git Bash
**Theory**: Git Bash subprocess hangs because it inherits stdin and waits for input
**From web search**: StackOverflow solution for Windows subprocess hanging

```python
process = await asyncio.create_subprocess_exec(
    "C:/Program Files/Git/bin/bash.exe", "-c", cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    stdin=asyncio.subprocess.DEVNULL  # <- ADD THIS
)
```

### Solution 2: Use create_subprocess_shell with Git Bash executable
**Theory**: Maybe shell=True with executable parameter works better than exec

```python
process = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    shell=True,
    executable="C:/Program Files/Git/bin/bash.exe"
)
```

### Solution 3: Try different Git Bash command format
**Theory**: Maybe Git Bash needs different command format

```python
# Try without -c flag
process = await asyncio.create_subprocess_exec(
    "C:/Program Files/Git/bin/bash.exe", cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    stdin=asyncio.subprocess.DEVNULL
)
```

### Solution 4: Test with simpler bash executable
**Theory**: Maybe full Git Bash path has issues, try simpler approach

```python
# Try just 'bash' if it's in PATH
process = await asyncio.create_subprocess_exec(
    "bash", "-c", cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    stdin=asyncio.subprocess.DEVNULL
)
```

## Implementation Strategy

1. **Start with Solution 1** (most likely to work based on web search)
2. **Test with simple command** (`echo "test"`)
3. **If working, test Unix commands** (`ls`, `pwd`)
4. **If not working, try Solution 2**
5. **Continue until we find working approach**

## Success Criteria
- ✅ `echo "test"` returns `test` (not timeout)
- ✅ `ls` returns Unix-style file listing
- ✅ `pwd` returns Unix-style path (`/c/code/nvdiffrast-trials`)
- ✅ Commands execute in reasonable time (< 1 second)

## Next Step
Try Solution 1: Add `stdin=asyncio.subprocess.DEVNULL` to the Git Bash subprocess execution.