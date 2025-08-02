# Repository Cleanup Plan for GitHub

## Current Status: IN PROGRESS

The goal is to keep only essential files for the MCP Terminal Controller project on GitHub, removing debug files, build artifacts, and demo outputs.

## What We're Keeping (Essential Files)

### Core Source Code
- `src/terminal_controller_standalone.py` - Main standalone implementation
- `src/terminal_controller_wrapper.py` - Original wrapper (if needed for reference)
- `src/gitbash_terminal_controller.py` - Git Bash integration (if needed)

### Documentation
- `README.md` - Main project documentation
- `LICENSE` - License file
- `CONTRIBUTING.md` - Contribution guidelines
- `CREDITS.md` - Credits and acknowledgments
- `docs/` - Documentation directory
- `examples/` - Usage examples

### Configuration
- `.gitignore` - Git ignore rules
- `requirements-dev.txt` - Development dependencies
- `mcp_wrapper_config.json` - MCP configuration example
- `config/` - Configuration examples

### Project Management
- `plan.md` - Current project status/plans
- `TERMINAL_CONTROLLER_SUCCESS.md` - Implementation success documentation

## What We're Removing

### COMPLETED - Debug and Test Files
- [x] `test_*.py` - All test files (debugging only)
- [x] `fix_*.py` - All fix/debug scripts
- [x] `nvdiffrast_*.py` - Demo files not related to terminal controller
- [x] `gitbash_terminal_controller.py` - Old implementation (root level)
- [x] `terminal_controller_wrapper.py` - Duplicate wrapper (root level)
- [x] Temporary files (`--help.txt`, `how --name-only e1d8634`)

### IN PROGRESS - Build Artifacts and Demo Outputs
- [x] `demo_output/` - Generated demo files and images
- [ ] `nvdiffrast_py310/` - Python virtual environment
- [ ] `terminal_controller_env/` - MCP environment  
- [ ] `nvdiffrast/` - Git submodule (needs special handling)

### PENDING - Optional Cleanup
- [ ] `.cursor/` - IDE-specific configuration (consider keeping for MCP setup)
- [ ] `tests/` - Check if contains essential tests vs debug files
- [ ] `mcp_setup/` - Setup scripts (may be useful for users)

## Current Issues

### Git Submodule Problem
- `nvdiffrast/` is a Git submodule causing removal issues
- Need to properly deinitialize submodule before removal

### Virtual Environments
- Large directories that shouldn't be in Git
- Need to ensure .gitignore prevents future inclusion

## Next Steps

1. **Handle Git Submodule**
   - Deinitialize nvdiffrast submodule
   - Remove from .gitmodules
   - Remove directory

2. **Remove Virtual Environments**
   - Remove nvdiffrast_py310/ 
   - Remove terminal_controller_env/
   - Update .gitignore

3. **Evaluate Optional Directories**
   - Check tests/ content
   - Decide on mcp_setup/ utility
   - Consider .cursor/ for user convenience

4. **Final Git Commit**
   - Commit all removals
   - Update .gitignore
   - Clean repository ready for GitHub

## Expected Final Structure
```
mcp-terminal-enhanced/
├── src/
│   └── terminal_controller_standalone.py
├── docs/
├── examples/
├── config/
├── mcp_setup/ (maybe)
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CREDITS.md
├── requirements-dev.txt
├── .gitignore
└── mcp_wrapper_config.json
```

## Success Criteria
- Repository size significantly reduced
- Only essential source code and documentation
- No build artifacts or virtual environments
- Clean Git history
- Ready for public GitHub repository