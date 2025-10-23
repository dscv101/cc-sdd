# Contributing to cc-sdd

Thank you for your interest in contributing to cc-sdd! This document provides guidelines and instructions for contributing to both the NPM package and the MCP server.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes**:
- Using welcoming and inclusive language
- Respecting differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes**:
- Trolling, insulting comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- **Python 3.11+** for MCP server development
- **Node.js 18+** for NPM package development
- **Git** for version control
- **uv** (recommended) or **pip** for Python dependencies
- **npm** or **pnpm** for Node dependencies

### Setting Up Development Environment

#### For MCP Server Development

```bash
# Clone the repository
git clone https://github.com/yourusername/cc-sdd.git
cd cc-sdd

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest
cc-sdd-mcp --version
```

#### For NPM Package Development

```bash
# Navigate to package directory
cd tools/cc-sdd

# Install dependencies
npm install

# Build the package
npm run build

# Run tests
npm test

# Test locally
npm link
```

---

## Development Workflow

### Branch Naming Convention

Use descriptive branch names with prefixes:

- `feature/` - New features (e.g., `feature/add-template-caching`)
- `fix/` - Bug fixes (e.g., `fix/validation-error-handling`)
- `docs/` - Documentation changes (e.g., `docs/update-api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/template-loader`)
- `test/` - Test additions/improvements (e.g., `test/add-cli-tests`)
- `chore/` - Maintenance tasks (e.g., `chore/update-dependencies`)

### Workflow Steps

1. **Create a branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make changes**:
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test locally**:
   ```bash
   # Run tests
   pytest
   
   # Check code quality
   ruff check .
   ruff format .
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create PR**:
   ```bash
   git push origin feature/my-new-feature
   ```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples**:

```bash
feat(cli): add validate-config command

Add a new CLI command to validate server configuration.
This helps users debug configuration issues before starting the server.

Closes #123
```

```bash
fix(templates): handle missing template gracefully

Previously threw uncaught exception when template file was missing.
Now returns a helpful error message.

Fixes #456
```

---

## Testing

### Running Tests

#### MCP Server Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src/cc_sdd_mcp --cov-report=html

# Run specific test
pytest tests/test_cli.py::test_list_tools

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

#### NPM Package Tests

```bash
cd tools/cc-sdd

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- --grep "template installation"
```

### Writing Tests

#### Python Tests (MCP Server)

```python
# tests/test_my_feature.py
import pytest
from cc_sdd_mcp.my_module import my_function


def test_my_function_success():
    """Test successful execution of my_function."""
    result = my_function("input")
    assert result == "expected_output"


def test_my_function_error():
    """Test error handling in my_function."""
    with pytest.raises(ValueError, match="Expected error message"):
        my_function("invalid_input")


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result is not None
```

#### TypeScript Tests (NPM Package)

```typescript
// tests/my-feature.test.ts
import { describe, it, expect } from 'vitest';
import { myFunction } from '../src/my-module';

describe('myFunction', () => {
  it('should return expected output', () => {
    const result = myFunction('input');
    expect(result).toBe('expected_output');
  });

  it('should throw error for invalid input', () => {
    expect(() => myFunction('invalid')).toThrow('Expected error');
  });
});
```

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 100% coverage required
- **Documentation**: All public APIs must have tests

---

## Code Quality

### Python Code Quality (MCP Server)

#### Formatting with Ruff

```bash
# Format all Python files
ruff format .

# Check formatting without changes
ruff format --check .
```

#### Linting with Ruff

```bash
# Lint all files
ruff check .

# Auto-fix issues
ruff check --fix .

# Show specific rule violations
ruff check --select E,F,W .
```

#### Type Checking with Pyrefly

```bash
# Type check the codebase
pyrefly check src/cc_sdd_mcp

# Type check specific file
pyrefly check src/cc_sdd_mcp/cli.py
```

#### Security Scanning with Bandit

```bash
# Scan for security issues
bandit -r src/cc_sdd_mcp

# Scan with confidence level
bandit -r src/cc_sdd_mcp -ll
```

### TypeScript Code Quality (NPM Package)

```bash
cd tools/cc-sdd

# Format code
npm run format

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type check
npm run type-check
```

### Pre-commit Hooks

The repository uses pre-commit hooks to ensure code quality:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

### Code Style Guidelines

#### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable names
- Document all public functions with docstrings

**Example**:

```python
def process_specification(
    feature_name: str,
    project_dir: Path,
    auto_approve: bool = False
) -> SpecificationResult:
    """Process a feature specification.
    
    Args:
        feature_name: Name of the feature to process
        project_dir: Directory containing the project
        auto_approve: Skip manual approval if True
        
    Returns:
        SpecificationResult with processing status
        
    Raises:
        ValueError: If feature_name is invalid
        FileNotFoundError: If project_dir doesn't exist
    """
    # Implementation...
```

#### TypeScript

- Use ESLint rules defined in `.eslintrc`
- Prefer `const` over `let`
- Use async/await over promises
- Type all function parameters and return values

**Example**:

```typescript
async function processTemplate(
  templateName: string,
  context: Record<string, any>
): Promise<string> {
  // Implementation...
}
```

---

## Documentation

### Documentation Requirements

All contributions must include appropriate documentation:

1. **Code Comments**: Explain complex logic
2. **Docstrings/JSDoc**: Document all public APIs
3. **README Updates**: Update relevant README files
4. **API Reference**: Update API docs for new tools
5. **Integration Guide**: Update if changing configuration or setup

### Writing Documentation

#### Python Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of the function.
    
    Longer description if needed. Can span multiple lines and include
    examples, notes, or warnings.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is negative
        
    Examples:
        >>> my_function("test", 42)
        True
        
        >>> my_function("", 0)
        Traceback (most recent call last):
        ValueError: param1 cannot be empty
    """
```

#### TypeScript JSDoc

```typescript
/**
 * Brief description of the function.
 *
 * Longer description if needed.
 *
 * @param param1 - Description of first parameter
 * @param param2 - Description of second parameter
 * @returns Description of return value
 * @throws {Error} When param1 is empty
 *
 * @example
 * ```typescript
 * myFunction("test", 42);
 * // Returns: true
 * ```
 */
function myFunction(param1: string, param2: number): boolean {
  // Implementation...
}
```

### Documentation Locations

- **MCP Server**: `src/cc_sdd_mcp/README.md`
- **API Reference**: `docs/api_reference.md`
- **Integration Guide**: `docs/integration_guide.md`
- **NPM Package**: `tools/cc-sdd/README.md`
- **Main README**: `README.md`

---

## Pull Request Process

### Before Submitting

1. **Test thoroughly**:
   ```bash
   # Run full test suite
   pytest
   npm test
   
   # Check code quality
   ruff check .
   ruff format .
   npm run lint
   ```

2. **Update documentation**:
   - Update README if adding features
   - Add/update docstrings
   - Update API reference if needed

3. **Verify coverage**:
   ```bash
   pytest --cov=src/cc_sdd_mcp --cov-report=term-missing
   ```

### Creating a Pull Request

1. **Title**: Use conventional commit format
   - Good: `feat(cli): add validate-config command`
   - Bad: `Updated CLI`

2. **Description**: Include:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Related issues (use `Closes #123`, `Fixes #456`)

3. **Template**:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Coverage meets requirements (80%+)

## Documentation
- [ ] README updated
- [ ] API reference updated
- [ ] Integration guide updated
- [ ] Docstrings added/updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No new warnings generated
- [ ] Dependent changes merged

## Related Issues
Closes #123
Fixes #456
```

### Review Process

1. **Automated checks**: CI must pass
   - Tests
   - Linting
   - Type checking
   - Coverage

2. **Code review**: At least one approval required
   - Focus on correctness
   - Check for edge cases
   - Verify documentation

3. **Addressing feedback**:
   - Respond to all comments
   - Make requested changes
   - Push updates to same branch

---

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes (e.g., `1.0.0` → `2.0.0`)
- **MINOR**: New features, backwards compatible (e.g., `1.0.0` → `1.1.0`)
- **PATCH**: Bug fixes, backwards compatible (e.g., `1.0.0` → `1.0.1`)

### Release Steps

#### For Maintainers

1. **Update version**:
   ```bash
   # MCP Server
   # Update version in src/cc_sdd_mcp/cli.py
   
   # NPM Package
   cd tools/cc-sdd
   npm version major|minor|patch
   ```

2. **Update CHANGELOG**:
   ```markdown
   ## [1.1.0] - 2024-01-15
   
   ### Added
   - New CLI commands for validation
   - Template caching support
   
   ### Changed
   - Improved error messages
   
   ### Fixed
   - Template loading bug on Windows
   ```

3. **Create release commit**:
   ```bash
   git add .
   git commit -m "chore: release v1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

4. **Publish**:
   ```bash
   # MCP Server (PyPI)
   python -m build
   twine upload dist/*
   
   # NPM Package
   cd tools/cc-sdd
   npm publish
   ```

---

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas
- **Pull Requests**: Code contributions

### Issue Templates

When creating issues, use the appropriate template:

- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Documentation**: For documentation improvements
- **Question**: For asking questions

### Good Issue Examples

**Bug Report**:
```markdown
**Description**: Validation fails with empty spec directory

**Steps to Reproduce**:
1. Create new spec with `spec_init`
2. Run `validate_impl` immediately
3. See error

**Expected**: Helpful message about missing files
**Actual**: Uncaught exception

**Environment**:
- cc-sdd-mcp version: 0.1.0
- Python version: 3.11.5
- OS: macOS 14.0
```

**Feature Request**:
```markdown
**Feature**: Add JSON output option to all CLI commands

**Motivation**: Makes it easier to parse CLI output in scripts

**Proposed Solution**: Add `--json` flag to all commands

**Alternatives Considered**: Using stdout parsing

**Additional Context**: Similar to how `gh` CLI works
```

---

## Recognition

Contributors will be recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- Project README

Thank you for contributing to cc-sdd! 🎉

