# MCP Server Integration Guide

Complete guide for integrating cc-sdd-mcp with various MCP clients.

## Table of Contents

- [Overview](#overview)
- [Claude Desktop](#claude-desktop)
- [Custom MCP Clients](#custom-mcp-clients)
- [Docker Deployment](#docker-deployment)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The cc-sdd-mcp server implements the Model Context Protocol (MCP) and communicates via standard input/output (stdio). This makes it compatible with any MCP client that supports stdio transport.

### Prerequisites

- Python 3.11 or higher
- cc-sdd-mcp installed (`pip install cc-sdd-mcp`)
- An MCP-compatible client (e.g., Claude Desktop)

### Quick Test

Before integrating with a client, test the server directly:

```bash
# Check installation
cc-sdd-mcp version

# List available tools
cc-sdd-mcp list-tools

# Validate configuration
cc-sdd-mcp validate-config
```

---

## Claude Desktop

Claude Desktop is the primary MCP client. Here's how to integrate cc-sdd-mcp.

### Basic Configuration

1. **Locate the configuration file**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add cc-sdd-mcp server**:

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

3. **Restart Claude Desktop**

4. **Verify integration**:
   - Open Claude Desktop
   - Type a message like "What MCP tools do you have available?"
   - Claude should list cc-sdd tools

### Configuration Options

#### Custom Config File

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", ".cc-sdd.config.json"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

#### Debug Mode

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--log-level", "DEBUG"],
      "cwd": "/path/to/your/project",
      "env": {
        "CC_SDD_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### Using Python Module

If `cc-sdd-mcp` command isn't in PATH:

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "python",
      "args": ["-m", "cc_sdd_mcp", "start"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

#### Using Virtual Environment

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "cc_sdd_mcp", "start"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Multiple Projects

Configure different instances for different projects:

```json
{
  "mcpServers": {
    "cc-sdd-project-a": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/project-a"
    },
    "cc-sdd-project-b": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", "custom-config.json"],
      "cwd": "/path/to/project-b"
    }
  }
}
```

### Troubleshooting Claude Desktop

1. **Check Claude Desktop logs**:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`
   - Linux: `~/.config/Claude/logs/`

2. **Verify server starts**:
   ```bash
   # Test server manually
   cd /path/to/your/project
   cc-sdd-mcp start
   ```

3. **Check permissions**:
   ```bash
   # Ensure Claude can execute the command
   which cc-sdd-mcp
   ls -la $(which cc-sdd-mcp)
   ```

---

## Custom MCP Clients

### Python Client Example

```python
import asyncio
import json
from mcp.client import Client
from mcp.client.stdio import stdio_client

async def main():
    # Create client connection
    async with stdio_client(
        command="cc-sdd-mcp",
        args=["start"],
        cwd="/path/to/project"
    ) as (read, write):
        async with Client(read, write) as client:
            # Initialize connection
            await client.initialize()
            
            # List available tools
            tools = await client.list_tools()
            print(f"Available tools: {len(tools)}")
            
            # Call a tool
            result = await client.call_tool(
                "spec_init",
                {
                    "feature_name": "my-feature",
                    "description": "Test feature"
                }
            )
            print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript Client Example

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function main() {
  // Create transport
  const transport = new StdioClientTransport({
    command: "cc-sdd-mcp",
    args: ["start"],
    cwd: "/path/to/project"
  });

  // Create client
  const client = new Client({
    name: "my-client",
    version: "1.0.0"
  }, {
    capabilities: {}
  });

  // Connect
  await client.connect(transport);

  // List tools
  const tools = await client.listTools();
  console.log(`Available tools: ${tools.tools.length}`);

  // Call a tool
  const result = await client.callTool({
    name: "spec_init",
    arguments: {
      feature_name: "my-feature",
      description: "Test feature"
    }
  });

  console.log("Result:", result);

  // Disconnect
  await client.close();
}

main();
```

---

## Docker Deployment

### Dockerfile

Create a `Dockerfile` for the MCP server:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install cc-sdd-mcp
RUN pip install cc-sdd-mcp

# Set up project directory
COPY . /project
WORKDIR /project

# Run server
CMD ["cc-sdd-mcp", "start"]
```

### Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  cc-sdd-mcp:
    build: .
    volumes:
      - ./project:/project
      - ./config:/config
    environment:
      - CC_SDD_LOG_LEVEL=INFO
      - CC_SDD_PROJECT_DIR=/project
      - CC_SDD_CONFIG_PATH=/config/.cc-sdd.config.json
    stdin_open: true
    tty: true
```

### Usage

```bash
# Build image
docker-compose build

# Run server
docker-compose run cc-sdd-mcp

# Run with custom command
docker-compose run cc-sdd-mcp cc-sdd-mcp list-tools
```

### Kubernetes Deployment

Create a deployment manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cc-sdd-mcp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cc-sdd-mcp
  template:
    metadata:
      labels:
        app: cc-sdd-mcp
    spec:
      containers:
      - name: server
        image: your-registry/cc-sdd-mcp:latest
        command: ["cc-sdd-mcp", "start"]
        env:
        - name: CC_SDD_LOG_LEVEL
          value: "INFO"
        - name: CC_SDD_PROJECT_DIR
          value: "/project"
        volumeMounts:
        - name: project-data
          mountPath: /project
        - name: config
          mountPath: /config
      volumes:
      - name: project-data
        persistentVolumeClaim:
          claimName: project-pvc
      - name: config
        configMap:
          name: cc-sdd-config
```

---

## Advanced Configuration

### Environment Variables

Complete list of supported environment variables:

```bash
# Server settings
export CC_SDD_SERVER_NAME="cc-sdd-mcp"
export CC_SDD_SERVER_VERSION="0.1.0"
export CC_SDD_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR

# Project settings
export CC_SDD_PROJECT_DIR="/path/to/project"
export CC_SDD_KIRO_DIR=".kiro"

# Template settings
export CC_SDD_DEFAULT_LANGUAGE="en"  # en, ja, zh-TW, etc.
export CC_SDD_TEMPLATE_CACHE_ENABLED="true"

# Workflow settings
export CC_SDD_AUTO_CREATE_STEERING="false"
export CC_SDD_STRICT_PHASE_GATES="true"

# Configuration file
export CC_SDD_CONFIG_PATH="/path/to/config.json"
```

### Configuration File

Create `.cc-sdd.config.json` in your project:

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

### Configuration Profiles

#### Development Profile

```json
{
  "log_level": "DEBUG",
  "auto_create_steering": true,
  "strict_phase_gates": false,
  "template_cache_enabled": false
}
```

#### Production Profile

```json
{
  "log_level": "WARNING",
  "auto_create_steering": false,
  "strict_phase_gates": true,
  "template_cache_enabled": true
}
```

### Custom Templates

Override default templates by placing them in your project:

```
your-project/
├── .cc-sdd.config.json
└── .kiro/
    └── templates/
        ├── steering/
        │   ├── product.md
        │   ├── tech.md
        │   └── structure.md
        └── specs/
            ├── requirements.md
            ├── design.md
            └── tasks.md
```

The server will use these instead of built-in templates.

---

## Integration Patterns

### Pattern 1: Single Project Integration

Best for: Individual projects with one codebase.

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/project"
    }
  }
}
```

**Workflow**:
1. Initialize steering once: `steering_init`
2. Create specs as needed: `spec_init`, `spec_requirements`, etc.
3. Validate regularly: `validate_gap`, `validate_impl`

### Pattern 2: Monorepo Integration

Best for: Large repositories with multiple services.

```json
{
  "mcpServers": {
    "cc-sdd-frontend": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/monorepo/frontend",
      "env": { "CC_SDD_KIRO_DIR": ".kiro/frontend" }
    },
    "cc-sdd-backend": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/monorepo/backend",
      "env": { "CC_SDD_KIRO_DIR": ".kiro/backend" }
    }
  }
}
```

**Structure**:
```
monorepo/
├── .kiro/
│   ├── frontend/
│   │   ├── steering/
│   │   └── specs/
│   └── backend/
│       ├── steering/
│       └── specs/
├── frontend/
└── backend/
```

### Pattern 3: Multi-Language Projects

Best for: Projects with different language templates.

```json
{
  "mcpServers": {
    "cc-sdd-en": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/project",
      "env": { "CC_SDD_DEFAULT_LANGUAGE": "en" }
    },
    "cc-sdd-ja": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/project",
      "env": {
        "CC_SDD_DEFAULT_LANGUAGE": "ja",
        "CC_SDD_KIRO_DIR": ".kiro-ja"
      }
    }
  }
}
```

### Pattern 4: Team Integration

Best for: Teams with different config requirements.

```json
{
  "mcpServers": {
    "cc-sdd-dev": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", "dev-config.json"],
      "cwd": "/path/to/project"
    },
    "cc-sdd-prod": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", "prod-config.json"],
      "cwd": "/path/to/project"
    }
  }
}
```

---

## Troubleshooting

### Server Won't Start

**Symptom**: MCP client shows connection errors.

**Solutions**:

1. Test server directly:
   ```bash
   cc-sdd-mcp start
   # Should wait for input without errors
   ```

2. Check installation:
   ```bash
   which cc-sdd-mcp
   cc-sdd-mcp version
   ```

3. Verify Python version:
   ```bash
   python --version  # Should be 3.11+
   ```

4. Check configuration:
   ```bash
   cc-sdd-mcp validate-config
   ```

### Tools Not Appearing in Client

**Symptom**: Client doesn't show cc-sdd tools.

**Solutions**:

1. Verify server registration in client config
2. Restart the MCP client completely
3. Check client logs for errors
4. Test tool listing:
   ```bash
   cc-sdd-mcp list-tools
   ```

### Tool Execution Errors

**Symptom**: Tools fail when called from client.

**Solutions**:

1. Test tool directly:
   ```bash
   cc-sdd-mcp test-tool TOOL_NAME --args '{}'
   ```

2. Check project directory permissions:
   ```bash
   ls -la /path/to/project/.kiro
   ```

3. Verify tool arguments match schema:
   ```bash
   cc-sdd-mcp inspect-tool TOOL_NAME
   ```

4. Enable debug logging:
   ```bash
   cc-sdd-mcp start --log-level DEBUG
   ```

### Permission Errors

**Symptom**: "Permission denied" errors when creating files.

**Solutions**:

1. Check directory permissions:
   ```bash
   ls -la /path/to/project
   chmod -R u+w /path/to/project/.kiro
   ```

2. Verify user running the server:
   ```bash
   id
   ps aux | grep cc-sdd-mcp
   ```

3. Use explicit working directory:
   ```json
   {
     "cwd": "/path/with/write/permissions"
   }
   ```

### Configuration Not Loading

**Symptom**: Server uses defaults instead of config file.

**Solutions**:

1. Verify config file exists:
   ```bash
   ls -la .cc-sdd.config.json
   cat .cc-sdd.config.json | jq  # Validate JSON
   ```

2. Use explicit config path:
   ```bash
   cc-sdd-mcp start --config /full/path/to/config.json
   ```

3. Check environment variables:
   ```bash
   env | grep CC_SDD
   ```

4. Validate configuration:
   ```bash
   cc-sdd-mcp validate-config --config .cc-sdd.config.json
   ```

### Template Errors

**Symptom**: Template rendering fails.

**Solutions**:

1. List available templates:
   ```bash
   cc-sdd-mcp test-tool template_list
   ```

2. Check template syntax:
   ```bash
   cc-sdd-mcp test-tool template_get --args '{
     "template_name": "product",
     "template_type": "steering"
   }'
   ```

3. Test rendering with minimal context:
   ```bash
   cc-sdd-mcp test-tool template_render --args '{
     "template_content": "{{ test }}",
     "context": {"test": "value"}
   }'
   ```

---

## Performance Optimization

### Template Caching

Enable template caching for better performance:

```json
{
  "template_cache_enabled": true
}
```

### Scope Limiting

Limit validation scope to relevant directories:

```python
{
  "tool": "validate_gap",
  "arguments": {
    "feature_name": "my-feature",
    "scope_paths": ["src/features/my-feature"]
  }
}
```

### Parallel Processing

For monorepos, run separate instances per service:

```json
{
  "mcpServers": {
    "service-a": {
      "command": "cc-sdd-mcp",
      "cwd": "/monorepo/services/a"
    },
    "service-b": {
      "command": "cc-sdd-mcp",
      "cwd": "/monorepo/services/b"
    }
  }
}
```

---

## Security Considerations

### File System Access

The server has read/write access to the project directory. Ensure:

1. **Run with least privilege**: Don't run as root
2. **Restrict directory access**: Use `cwd` to limit scope
3. **Review generated files**: Always review steering/spec documents before committing

### Sensitive Data

1. **Don't store secrets in steering documents**
2. **Use `.gitignore` for sensitive specs**:
   ```
   .kiro/specs/internal-*
   .kiro/steering/credentials.md
   ```

3. **Review before sharing**: Check specs before sharing with AI

### Network Isolation

The server doesn't make network requests, but be aware:

1. MCP clients may send tool outputs to external services
2. Review client privacy policies
3. Consider running in isolated environments for sensitive projects

---

## Best Practices

### 1. Version Control

Include in `.gitignore`:
```
.kiro/specs/*/notes.md
.kiro/temp/
*.tmp.md
```

Commit to version control:
```
.kiro/steering/
.kiro/specs/*/requirements.md
.kiro/specs/*/design.md
.kiro/specs/*/tasks.md
.cc-sdd.config.json
```

### 2. Team Workflow

1. **Share steering documents**: Commit to Git
2. **Review specs together**: Use pull requests for spec changes
3. **Standardize config**: Include `.cc-sdd.config.json` in repo
4. **Document conventions**: Add to `CONTRIBUTING.md`

### 3. CI/CD Integration

Run validation in CI:

```yaml
# .github/workflows/validate.yml
name: Validate Specs
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install cc-sdd-mcp
      - run: |
          for spec in .kiro/specs/*; do
            cc-sdd-mcp test-tool validate_impl --args "{\"feature_name\": \"$(basename $spec)\"}"
          done
```

### 4. Documentation

Document your setup in README:

```markdown
## Development with cc-sdd

This project uses cc-sdd for spec-driven development.

### Setup
1. Install: `pip install cc-sdd-mcp`
2. Configure Claude Desktop (see `.claude-config-example.json`)
3. Initialize steering: Ask Claude to run `steering_init`

### Workflow
1. Create spec: `spec_init "feature-name" "description"`
2. Generate docs: `spec_requirements`, `spec_design`, `spec_tasks`
3. Implement and validate: `validate_impl`
```

---

## Support

For issues and questions:

- [GitHub Issues](https://github.com/yourusername/cc-sdd/issues)
- [Documentation](../README.md)
- [API Reference](./api_reference.md)

