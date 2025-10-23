# Editor Integration Guide for cc-sdd-mcp

Complete guide for integrating the cc-sdd-mcp server with popular AI-powered code editors and IDEs.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Augment Code (VS Code)](#augment-code-vs-code)
- [Cursor IDE](#cursor-ide)
- [Claude Desktop](#claude-desktop)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

The cc-sdd-mcp server implements the Model Context Protocol (MCP), enabling AI assistants to understand and enforce specification-driven development workflows. This guide covers setup for the most popular AI coding environments.

### What You'll Get

Once configured, your AI assistant can:
- **Create and manage specifications** using structured templates
- **Generate design documents** following best practices
- **Validate requirements** automatically
- **Track task dependencies** and relationships
- **Enforce workflow** from specification → design → implementation

---

## Prerequisites

Before setting up with any editor, ensure you have:

1. **Python 3.11 or higher** installed
2. **cc-sdd-mcp installed**:
   ```bash
   pip install cc-sdd-mcp
   ```
3. **Verify installation**:
   ```bash
   cc-sdd-mcp --version
   cc-sdd-mcp list-tools
   ```

---

## Augment Code (VS Code)

Augment Code is a VS Code extension that brings AI-powered coding assistance with MCP support.

### Installation

1. **Install the Augment Code extension**:
   - Open VS Code
   - Go to Extensions (Cmd/Ctrl + Shift + X)
   - Search for "Augment Code"
   - Click Install

2. **Sign in to Augment**:
   - After installation, click the Augment icon in the sidebar
   - Sign in with your Augment account
   - Complete the authentication process

### Configuration Method 1: Via Settings UI (Recommended)

1. **Open Augment Settings**:
   - Click the Augment icon in the VS Code sidebar
   - Click the gear icon (⚙️) to open settings
   - Navigate to "MCP Servers" section

2. **Add cc-sdd-mcp server**:
   - Click "Add MCP Server"
   - Enter the following details:
     - **Name**: `cc-sdd`
     - **Command**: `cc-sdd-mcp`
     - **Arguments**: `["start"]`
     - **Working Directory**: `/path/to/your/project`

3. **Save and restart**:
   - Click "Save"
   - Reload VS Code (Cmd/Ctrl + Shift + P → "Reload Window")

### Configuration Method 2: Via JSON Import

1. **Create configuration file** `augment-mcp-config.json`:
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

2. **Import configuration**:
   - Open Augment settings
   - Navigate to MCP Servers section
   - Click "Import from JSON"
   - Select your `augment-mcp-config.json` file

### Advanced Configuration

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
        "CC_SDD_DEBUG": "true"
      }
    }
  }
}
```

### Usage in Augment Code

Once configured, you can use cc-sdd tools in Augment Agent:

1. **Open Augment Agent** (Cmd/Ctrl + Shift + A)
2. **Ask about available tools**:
   ```
   What spec-driven development tools do you have available?
   ```
3. **Create a specification**:
   ```
   Create a new specification for a user authentication feature
   ```
4. **Generate design**:
   ```
   Generate a design document for the authentication spec
   ```

### Verification

To verify the integration is working:

1. Open Augment Agent
2. Type: "List all MCP tools available"
3. You should see cc-sdd tools including:
   - `spec_create`
   - `spec_update`
   - `design_generate`
   - `task_create`
   - And more

---

## Cursor IDE

Cursor is an AI-first code editor with native MCP support, perfect for spec-driven development workflows.

### Installation

1. **Download Cursor**:
   - Visit [cursor.com](https://cursor.com)
   - Download and install for your platform
   - Launch Cursor and complete initial setup

### Configuration

#### Locate Configuration File

The MCP configuration file location varies by platform:

- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/mcp.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/mcp.json`

#### Setup Steps

1. **Create or edit `mcp.json`**:
   
   If the file doesn't exist, create it with this content:
   
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

2. **For existing configuration**, add cc-sdd to the `mcpServers` object:
   
   ```json
   {
     "mcpServers": {
       "existing-server": {
         "command": "existing-command"
       },
       "cc-sdd": {
         "command": "cc-sdd-mcp",
         "args": ["start"],
         "cwd": "/path/to/your/project"
       }
     }
   }
   ```

3. **Restart Cursor** for changes to take effect

### Quick Setup Script

Use this script to automatically configure Cursor:

**macOS/Linux**:
```bash
#!/bin/bash

# Determine config location
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Cursor/User/globalStorage"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Cursor/User/globalStorage"
fi

# Create directory if needed
mkdir -p "$CONFIG_DIR"

# Create or update mcp.json
cat > "$CONFIG_DIR/mcp.json" << 'EOF'
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "."
    }
  }
}
EOF

echo "✅ Cursor MCP configuration created at: $CONFIG_DIR/mcp.json"
echo "Please restart Cursor to apply changes."
```

**Windows (PowerShell)**:
```powershell
# Set configuration path
$ConfigDir = "$env:APPDATA\Cursor\User\globalStorage"

# Create directory if needed
New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null

# Create mcp.json
$Config = @{
    mcpServers = @{
        "cc-sdd" = @{
            command = "cc-sdd-mcp"
            args = @("start")
            cwd = "."
        }
    }
} | ConvertTo-Json -Depth 10

Set-Content -Path "$ConfigDir\mcp.json" -Value $Config

Write-Host "✅ Cursor MCP configuration created at: $ConfigDir\mcp.json"
Write-Host "Please restart Cursor to apply changes."
```

### Advanced Configuration

#### Project-Specific Config

For different settings per project, use the `cwd` parameter:

```json
{
  "mcpServers": {
    "cc-sdd-project-a": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", "/path/to/project-a/.cc-sdd.config.json"],
      "cwd": "/path/to/project-a"
    },
    "cc-sdd-project-b": {
      "command": "cc-sdd-mcp",
      "args": ["start"],
      "cwd": "/path/to/project-b"
    }
  }
}
```

#### Debug Configuration

Enable detailed logging for troubleshooting:

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--log-level", "DEBUG"],
      "cwd": "/path/to/your/project",
      "env": {
        "CC_SDD_DEBUG": "true",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Usage in Cursor

Once configured, cc-sdd tools are available in Cursor's AI chat:

1. **Open Cursor Chat** (Cmd/Ctrl + L)
2. **Query available tools**:
   ```
   Show me all the spec-driven development tools available
   ```
3. **Create specifications**:
   ```
   Create a specification for a REST API endpoint that handles user registration
   ```
4. **Generate designs**:
   ```
   Generate a technical design for the user registration spec
   ```

### Verification

To verify Cursor can access cc-sdd-mcp:

1. Open Cursor Chat
2. Type: "What MCP servers are currently connected?"
3. Ask: "Can you create a specification?"
4. The AI should confirm it has access to cc-sdd tools

---

## Claude Desktop

Claude Desktop is Anthropic's official MCP client with excellent cc-sdd-mcp support.

### Quick Setup

For detailed Claude Desktop setup, see our [Integration Guide](./integration_guide.md#claude-desktop).

**Summary**:

1. **Locate config file**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add cc-sdd server**:
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

For more configuration options and troubleshooting, refer to the [full integration guide](./integration_guide.md).

---

## Troubleshooting

### Common Issues

#### Server Not Appearing

**Symptoms**: AI assistant doesn't recognize cc-sdd tools

**Solutions**:
1. Verify installation:
   ```bash
   which cc-sdd-mcp
   cc-sdd-mcp --version
   ```
2. Check configuration file syntax (must be valid JSON)
3. Restart the editor/client completely
4. Check editor logs for MCP connection errors

#### Command Not Found

**Symptoms**: Error message about `cc-sdd-mcp` not being found

**Solutions**:
1. Use full path to cc-sdd-mcp:
   ```bash
   which cc-sdd-mcp  # Get the full path
   ```
2. Update configuration with full path:
   ```json
   {
     "command": "/usr/local/bin/cc-sdd-mcp"
   }
   ```
3. Ensure Python environment is activated in the terminal

#### Connection Timeouts

**Symptoms**: MCP server connection times out or fails

**Solutions**:
1. Increase timeout in configuration (if supported)
2. Check for port conflicts
3. Verify no firewall is blocking stdio communication
4. Try debug mode to see detailed connection logs

#### Tools Not Working

**Symptoms**: Server connects but tool calls fail

**Solutions**:
1. Verify working directory exists and is accessible
2. Check file permissions in the project directory
3. Enable debug logging:
   ```json
   {
     "args": ["start", "--log-level", "DEBUG"]
   }
   ```
4. Check log file: `~/.cc-sdd/logs/cc-sdd-mcp.log`

### Debug Mode

Enable detailed logging for all editors:

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--log-level", "DEBUG"],
      "env": {
        "CC_SDD_DEBUG": "true",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

View logs:
```bash
tail -f ~/.cc-sdd/logs/cc-sdd-mcp.log
```

### Platform-Specific Issues

#### macOS

- **Issue**: Permission denied errors
- **Solution**: Grant Full Disk Access to your editor in System Settings → Privacy & Security

#### Windows

- **Issue**: Path with spaces causing errors
- **Solution**: Use forward slashes and quote paths:
  ```json
  {
    "cwd": "C:/Users/Your Name/Projects/my-project"
  }
  ```

#### Linux

- **Issue**: Python command not found
- **Solution**: Ensure Python is in PATH or use full path to Python:
  ```json
  {
    "command": "/usr/bin/python3",
    "args": ["-m", "cc_sdd_mcp", "start"]
  }
  ```

---

## Best Practices

### 1. Use Project-Specific Configurations

Create a `.cc-sdd.config.json` in each project:

```json
{
  "project_name": "my-awesome-app",
  "spec_dir": "./specs",
  "design_dir": "./designs",
  "task_dir": "./tasks"
}
```

Reference it in your MCP config:

```json
{
  "mcpServers": {
    "cc-sdd": {
      "command": "cc-sdd-mcp",
      "args": ["start", "--config", ".cc-sdd.config.json"],
      "cwd": "/path/to/project"
    }
  }
}
```

### 2. Set Working Directory Correctly

Always set `cwd` to your project root:

```json
{
  "cwd": "/absolute/path/to/your/project"
}
```

This ensures:
- Relative paths work correctly
- Specs are created in the right location
- Git integration functions properly

### 3. Use Version Control for Configs

**Do commit**:
- `.cc-sdd.config.json` (project configuration)
- Template customizations
- Workflow definitions

**Don't commit**:
- Editor-specific MCP configurations
- Personal API keys or tokens
- Local development paths

### 4. Enable Logging During Initial Setup

Start with debug mode enabled:

```json
{
  "args": ["start", "--log-level", "DEBUG"]
}
```

Once everything works, switch to INFO or WARNING level.

### 5. Test Before Production Use

Before using cc-sdd-mcp in real projects:

1. Create a test project
2. Configure the MCP server
3. Test all key workflows:
   - Specification creation
   - Design generation
   - Task management
   - Validation

### 6. Keep cc-sdd-mcp Updated

Regularly update to get new features and fixes:

```bash
pip install --upgrade cc-sdd-mcp
```

After updating, restart your editor/client to load the new version.

### 7. Customize Templates

Create custom templates for your team's workflow:

1. Export default templates:
   ```bash
   cc-sdd-mcp template-get spec > custom-spec.md
   ```
2. Customize the template
3. Reference in configuration:
   ```json
   {
     "templates": {
       "spec": "./templates/custom-spec.md"
     }
   }
   ```

---

## Next Steps

- **[API Reference](./api_reference.md)**: Detailed documentation of all tools and methods
- **[Integration Guide](./integration_guide.md)**: Advanced integration patterns and Docker setup
- **[Workflow Guide](../README.md#workflows)**: Learn about specification-driven workflows
- **[Contributing](../CONTRIBUTING.md)**: Help improve cc-sdd-mcp

---

## Support

Need help?

- **Issues**: [GitHub Issues](https://github.com/dscv101/cc-sdd/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dscv101/cc-sdd/discussions)
- **Documentation**: [Main README](../README.md)

---

*Last updated: 2025-10-23*

