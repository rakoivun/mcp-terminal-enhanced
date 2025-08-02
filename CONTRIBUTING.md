# Contributing to MCP Terminal Enhanced

Thank you for your interest in contributing to the MCP Terminal Enhanced project! This guide will help you get started with contributing.

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/mcp-terminal-enhanced.git
   cd mcp-terminal-enhanced
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate  # Windows
   ```
4. **Install dependencies:**
   ```bash
   pip install terminal-controller
   pip install -r requirements-dev.txt  # When available
   ```

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Terminal-controller MCP package
- Git Bash (Windows) for full testing

### Environment Setup
```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Test the wrapper directly
python src/terminal_controller_wrapper.py --version
```

## Types of Contributions

We welcome several types of contributions:

### Bug Reports
- Use the [GitHub Issues](https://github.com/rakoivun/mcp-terminal-enhanced/issues) page
- Include detailed reproduction steps
- Provide environment information (OS, Python version, etc.)
- Include debug output when possible

### Feature Requests
- Open an issue to discuss the feature first
- Explain the use case and benefits
- Consider backward compatibility

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

### 📚 Documentation
- Fix typos or unclear instructions
- Add new examples
- Improve existing guides
- Translate documentation

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 2. Make Your Changes
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 3. Test Your Changes
```bash
# Run existing tests
python -m pytest tests/ -v

# Test manual functionality
MCP_ENHANCED_DEBUG=1 python src/terminal_controller_wrapper.py

# Test on different platforms if possible
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "Add feature: description of your changes"
```

Use clear, descriptive commit messages:
- `Add feature: smart workspace detection for VS Code`
- `Fix bug: Git Bash detection on Windows with custom install path`
- `Docs: improve installation guide for Linux users`
- `Test: add unit tests for project detection`

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference any related issues
- Include testing information

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_project_detection.py -v

# Run with coverage (if coverage installed)
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests
- Add tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases and error conditions

Example test structure:
```python
def test_new_feature_success_case(self):
    """Test that new feature works in normal conditions."""
    # Arrange
    test_input = "test_value"
    
    # Act
    result = your_function(test_input)
    
    # Assert
    self.assertEqual(result, expected_output)
```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 conventions
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def get_project_root(start_path: Optional[str] = None) -> str:
    """
    Dynamically determine the project root directory.
    
    Args:
        start_path: Directory to start searching from. 
                   Defaults to script location.
        
    Returns:
        Path to the detected project root.
    """
    # Implementation here
```

### Documentation Style
- Use clear, concise language
- Include code examples
- Update existing docs when changing functionality
- Use markdown for formatting

## Submitting Changes

### Pull Request Guidelines
1. **Describe your changes** clearly in the PR description
2. **Reference related issues** using `#issue-number`
3. **Include testing information** - how you tested the changes
4. **Update documentation** if needed
5. **Keep PRs focused** - one feature/fix per PR when possible

### PR Template
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement
- [ ] Performance improvement

## Testing
Describe how you tested these changes:
- [ ] Existing tests pass
- [ ] Added new tests
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Reporting Issues

### Bug Report Template
```markdown
**Environment:**
- OS: [Windows 11 / macOS 14 / Ubuntu 22.04]
- Python: [3.9.7]
- terminal-controller: [0.1.9]
- IDE: [Cursor / VS Code / Other]

**Description:**
Clear description of the bug.

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Bug occurs

**Expected Behavior:**
What should happen.

**Actual Behavior:**
What actually happens.

**Error Messages:**
```
Paste any error messages here
```

**Debug Output:**
```
Output from MCP_ENHANCED_DEBUG=1
```
```

## Development Priorities

Current areas where contributions are especially welcome:

### High Priority
- **Cross-platform testing** - especially macOS and Linux
- **Error handling improvements** - better error messages and recovery
- **Performance optimizations** - faster project detection
- **Additional project markers** - support for more project types

### Medium Priority
- **IDE integrations** - VS Code, PyCharm, etc.
- **Configuration management** - better config file handling
- **Logging improvements** - structured logging, log levels
- **Documentation translations** - non-English documentation

### Nice to Have
- **Shell integrations** - fish, zsh compatibility
- **Container support** - Docker, Podman integration
- **Plugin system** - extensible project detection
- **GUI configuration tool** - easier setup for non-technical users

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Collaborative
- Help others learn and contribute
- Share knowledge and resources
- Provide constructive feedback
- Celebrate others' contributions

## 📞 Getting Help

### Development Questions
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rakoivun/mcp-terminal-enhanced/discussions)
- **Issues**: [GitHub Issues](https://github.com/rakoivun/mcp-terminal-enhanced/issues)

### Before Asking
1. Check existing issues and discussions
2. Review the documentation
3. Try the troubleshooting guide
4. Include relevant details in your question

## Recognition

Contributors are recognized in several ways:
- Listed in repository contributors
- Mentioned in release notes
- Credit in documentation where appropriate

Thank you for contributing to MCP Terminal Enhanced!