# cc-sdd MCP Server

Model Context Protocol (MCP) server for cc-sdd - Spec-Driven Development workflows.

## Overview

This MCP server exposes cc-sdd's powerful spec-driven development workflow as tools that AI assistants can call programmatically. It enables AI coding assistants to:

- Initialize and manage project steering (project memory)
- Create and manage feature specifications
- Generate requirements, design documents, and task breakdowns
- Validate implementations against specifications

## Features

### Steering Management
- `steering_init`: Initialize steering documents (product.md, tech.md, structure.md)
- `steering_status`: Get current steering configuration
- `steering_update`: Update steering documents
- `steering_read`: Read steering content

### Specification Lifecycle
- `spec_init`: Initialize a new feature specification
- `spec_requirements`: Generate requirements document
- `spec_design`: Generate design document
- `spec_tasks`: Generate task breakdown
- `spec_status`: Check specification progress

### Validation Tools
- `validate_gap`: Analyze gap between existing code and requirements
- `validate_design`: Validate design against requirements
- `validate_impl`: Validate implementation against tasks

## Installation

```bash
# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .

# Install with dev dependencies
uv pip install -e ".[dev]"
```

## Usage

### Running the MCP Server

```bash
# Start the server (stdio transport)
python -m cc_sdd_mcp

# Or use the CLI command
cc-sdd-mcp
```

### Configuration for MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "python",
      "args": ["-m", "cc_sdd_mcp"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

## Development

### Setup

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov-report=html
open htmlcov/index.html
```

### Code Quality

```bash
# Format code with ruff
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Security scan with bandit
bandit -r src/cc_sdd_mcp

# Type checking with pyrefly
pyrefly check src/cc_sdd_mcp
```

## Architecture

```
src/cc_sdd_mcp/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── server.py            # MCP server implementation
├── models/              # Pydantic data models
│   ├── steering.py
│   ├── specification.py
│   └── validation.py
├── tools/               # MCP tool implementations
│   ├── steering.py
│   ├── specification.py
│   └── validation.py
├── workflows/           # Business logic
│   ├── steering_workflow.py
│   ├── spec_workflow.py
│   └── validation_workflow.py
└── utils/               # Utilities
    ├── filesystem.py
    ├── templates.py
    ├── paths.py
    └── renderer.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

See CONTRIBUTING.md for development guidelines.

