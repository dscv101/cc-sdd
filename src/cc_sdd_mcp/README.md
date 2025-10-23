# cc-sdd MCP Server

Model Context Protocol (MCP) server for cc-sdd - Spec-Driven Development workflows.

## Overview

This MCP server exposes cc-sdd's powerful spec-driven development workflow as tools that AI assistants can call programmatically. It enables AI coding assistants to:

- Initialize and manage project steering (project memory)
- Create and manage feature specifications
- Generate requirements, design documents, and task breakdowns
- Validate implementations against specifications
- Manage templates with Jinja2 support
- Configure server behavior through JSON or environment variables

## Features

### 🎯 Steering Management (4 tools)
- `steering_init`: Initialize steering documents (product.md, tech.md, structure.md)
- `steering_status`: Get current steering configuration
- `steering_update`: Update steering documents
- `steering_read`: Read steering content

### 📋 Specification Lifecycle (5 tools)
- `spec_init`: Initialize a new feature specification
- `spec_requirements`: Generate requirements document
- `spec_design`: Generate design document
- `spec_tasks`: Generate task breakdown
- `spec_status`: Check specification progress

### 📄 Template Management (3 tools)
- `template_list`: List all available templates
- `template_get`: Get raw template content
- `template_render`: Render templates with Jinja2

### ✅ Validation Tools (3 tools)
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

## Quick Start

### Start the MCP Server

```bash
# Start with default configuration
cc-sdd-mcp

# Or explicitly use the start command
cc-sdd-mcp start

# Start with debug logging
cc-sdd-mcp start --log-level DEBUG

# Start with custom config file
cc-sdd-mcp start --config .cc-sdd.config.json
```

### Explore Available Tools

```bash
# List all MCP tools
cc-sdd-mcp list-tools

# List tools in JSON format
cc-sdd-mcp list-tools --json

# Inspect a specific tool
cc-sdd-mcp inspect-tool spec_init

# Show tool details in JSON
cc-sdd-mcp inspect-tool spec_init --json
```

### Test Tools

```bash
# Test a tool without arguments
cc-sdd-mcp test-tool steering_status

# Test a tool with arguments
cc-sdd-mcp test-tool spec_init --args '{"description": "Add user authentication", "feature_name": "auth"}'

# Test template rendering
cc-sdd-mcp test-tool template_render --args '{"template_content": "Hello {{ name }}!", "context": {"name": "World"}}'
```

### Validate Configuration

```bash
# Validate default configuration
cc-sdd-mcp validate-config

# Validate a specific config file
cc-sdd-mcp validate-config --config .cc-sdd.config.json
```

### Show Version

```bash
cc-sdd-mcp version

# Or use the flag
cc-sdd-mcp --version
```

## Configuration

### Configuration File

Create a `.cc-sdd.config.json` file in your project root:

```json
{
  "server_name": "cc-sdd-mcp",
  "server_version": "0.1.0",
  "log_level": "INFO",
  "project_dir": ".",
  "kiro_dir": ".kiro",
  "default_language": "en",
  "template_cache_enabled": true,
  "auto_create_steering": false,
  "strict_phase_gates": true
}
```

### Environment Variables

Configure via environment variables (prefixed with `CC_SDD_`):

```bash
export CC_SDD_LOG_LEVEL=DEBUG
export CC_SDD_PROJECT_DIR=/path/to/project
export CC_SDD_DEFAULT_LANGUAGE=ja
export CC_SDD_TEMPLATE_CACHE_ENABLED=true
export CC_SDD_AUTO_CREATE_STEERING=false
export CC_SDD_STRICT_PHASE_GATES=true
```

### Configuration Priority

Configuration is loaded in this order (later sources override earlier ones):

1. Default values
2. Configuration file (if exists)
3. Environment variables
4. Command-line arguments

## MCP Client Configuration

### Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### With Custom Config

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", ".cc-sdd.config.json", "--log-level", "DEBUG"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Using Python Module

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
# Clone the repository
git clone https://github.com/yourusername/cc-sdd.git
cd cc-sdd

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
pytest tests/test_cli.py

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
├── cli.py               # Click-based CLI implementation
├── server.py            # MCP server implementation
├── models/              # Pydantic data models
│   ├── config.py        # Server configuration
│   ├── steering.py      # Steering models
│   ├── specification.py # Specification models
│   └── validation.py    # Validation models
├── tools/               # MCP tool implementations
│   ├── registry.py      # Tool registry
│   ├── steering.py      # Steering tools (4 tools)
│   ├── specification.py # Specification tools (5 tools)
│   ├── templates.py     # Template tools (3 tools)
│   └── validation.py    # Validation tools (3 tools)
├── workflows/           # Business logic
│   ├── steering_workflow.py
│   ├── spec_workflow.py
│   └── validation_workflow.py
└── utils/               # Utilities
    ├── filesystem.py
    ├── templates.py     # Jinja2 template support
    ├── paths.py
    └── renderer.py
```

## CLI Commands Reference

### Global Options

```bash
cc-sdd-mcp [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config FILE  Path to configuration file
  -v, --version      Show version and exit
  --help             Show this message and exit
```

### start

Start the MCP server with stdio transport.

```bash
cc-sdd-mcp start [OPTIONS]

Options:
  -c, --config FILE         Path to configuration file
  -l, --log-level LEVEL     Logging level (DEBUG|INFO|WARNING|ERROR)
```

### list-tools

List all available MCP tools with descriptions.

```bash
cc-sdd-mcp list-tools [OPTIONS]

Options:
  --json  Output in JSON format
```

### inspect-tool

Show detailed information about a specific tool.

```bash
cc-sdd-mcp inspect-tool TOOL_NAME [OPTIONS]

Arguments:
  TOOL_NAME  Name of the tool to inspect

Options:
  --json  Output in JSON format
```

### test-tool

Test a tool with sample arguments.

```bash
cc-sdd-mcp test-tool TOOL_NAME [OPTIONS]

Arguments:
  TOOL_NAME  Name of the tool to test

Options:
  -a, --args JSON  JSON string of arguments
```

### validate-config

Validate server configuration and show current settings.

```bash
cc-sdd-mcp validate-config [OPTIONS]

Options:
  -c, --config FILE  Path to configuration file to validate
```

### version

Show version information.

```bash
cc-sdd-mcp version
```

## Examples

### Example 1: Initialize a Project with Steering

```bash
# Start the server in the background
cc-sdd-mcp start &

# Test the steering initialization
cc-sdd-mcp test-tool steering_init --args '{
  "project_dir": ".",
  "language": "en"
}'

# Check steering status
cc-sdd-mcp test-tool steering_status --args '{
  "project_dir": "."
}'
```

### Example 2: Create a Feature Specification

```bash
# Initialize a new feature
cc-sdd-mcp test-tool spec_init --args '{
  "feature_name": "user-auth",
  "description": "Add OAuth 2.0 authentication"
}'

# Generate requirements
cc-sdd-mcp test-tool spec_requirements --args '{
  "feature_name": "user-auth"
}'

# Check status
cc-sdd-mcp test-tool spec_status --args '{
  "feature_name": "user-auth"
}'
```

### Example 3: Template Rendering

```bash
# List available templates
cc-sdd-mcp test-tool template_list

# Get a template
cc-sdd-mcp test-tool template_get --args '{
  "template_name": "product",
  "template_type": "steering"
}'

# Render a template
cc-sdd-mcp test-tool template_render --args '{
  "template_content": "# {{ title }}\\n\\n{{ content }}",
  "context": {
    "title": "My Project",
    "content": "Project description here"
  }
}'
```

## Troubleshooting

### Server Won't Start

1. **Check Python version**: Requires Python 3.11+
   ```bash
   python --version
   ```

2. **Verify installation**:
   ```bash
   pip show cc-sdd-mcp
   ```

3. **Check configuration**:
   ```bash
   cc-sdd-mcp validate-config
   ```

4. **Enable debug logging**:
   ```bash
   cc-sdd-mcp start --log-level DEBUG
   ```

### Tools Not Working

1. **List available tools**:
   ```bash
   cc-sdd-mcp list-tools
   ```

2. **Inspect tool schema**:
   ```bash
   cc-sdd-mcp inspect-tool TOOL_NAME
   ```

3. **Test tool directly**:
   ```bash
   cc-sdd-mcp test-tool TOOL_NAME --args '{}'
   ```

### Configuration Issues

1. **Validate configuration**:
   ```bash
   cc-sdd-mcp validate-config
   ```

2. **Check environment variables**:
   ```bash
   env | grep CC_SDD
   ```

3. **Create explicit config file**:
   ```bash
   cat > .cc-sdd.config.json << 'EOF'
   {
     "log_level": "DEBUG",
     "project_dir": "."
   }
   EOF
   ```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](../../LICENSE) file for details.

## Related Resources

- [cc-sdd NPM Package](../../tools/cc-sdd/README.md) - Original CLI tool
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Kiro IDE](https://kiro.dev) - Compatible IDE for spec-driven development

