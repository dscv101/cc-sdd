# MCP Server API Reference

Complete reference for all MCP tools provided by cc-sdd-mcp server.

## Tool Categories

- [Steering Management](#steering-management) - 4 tools
- [Specification Lifecycle](#specification-lifecycle) - 5 tools
- [Template Management](#template-management) - 3 tools
- [Validation Tools](#validation-tools) - 3 tools

---

## Steering Management

Tools for managing project steering documents (project memory).

### steering_init

Initialize steering documents for a project.

**Description**: Creates the default steering files (product.md, tech.md, structure.md) in the `.kiro/steering/` directory.

**Parameters**:
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `language` (string, optional): Language code for templates (en, ja, zh-TW, etc.). Defaults to "en".

**Returns**: JSON with initialization status and created files.

**Example**:
```json
{
  "project_dir": ".",
  "language": "en"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Steering initialized successfully",
  "created_files": [
    ".kiro/steering/product.md",
    ".kiro/steering/tech.md",
    ".kiro/steering/structure.md"
  ]
}
```

---

### steering_status

Get the current status of steering documents.

**Description**: Shows which steering files exist and their last modification times.

**Parameters**:
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with steering file status.

**Example**:
```json
{
  "project_dir": "."
}
```

**Response**:
```json
{
  "initialized": true,
  "steering_dir": ".kiro/steering",
  "files": {
    "product.md": {
      "exists": true,
      "last_modified": "2024-01-15T10:30:00"
    },
    "tech.md": {
      "exists": true,
      "last_modified": "2024-01-15T10:30:00"
    },
    "structure.md": {
      "exists": true,
      "last_modified": "2024-01-15T10:30:00"
    }
  }
}
```

---

### steering_read

Read steering document content.

**Description**: Retrieves the content of one or all steering documents.

**Parameters**:
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `file_name` (string, optional): Specific file to read (product.md, tech.md, structure.md). If not provided, reads all files.

**Returns**: JSON with file content.

**Example** (read specific file):
```json
{
  "project_dir": ".",
  "file_name": "product.md"
}
```

**Example** (read all files):
```json
{
  "project_dir": "."
}
```

**Response**:
```json
{
  "files": {
    "product.md": "# Product Requirements\n\n...",
    "tech.md": "# Technical Architecture\n\n...",
    "structure.md": "# Project Structure\n\n..."
  }
}
```

---

### steering_update

Update a steering document with new content.

**Description**: Replaces or appends content to an existing steering document.

**Parameters**:
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `file_name` (string, required): File to update (product.md, tech.md, structure.md).
- `content` (string, required): New content for the file.
- `append` (boolean, optional): If true, appends content instead of replacing. Defaults to false.

**Returns**: JSON with update status.

**Example**:
```json
{
  "project_dir": ".",
  "file_name": "tech.md",
  "content": "## New Section\n\nNew technical details...",
  "append": true
}
```

**Response**:
```json
{
  "success": true,
  "message": "Steering document updated successfully",
  "file": ".kiro/steering/tech.md"
}
```

---

## Specification Lifecycle

Tools for managing feature specifications through their lifecycle.

### spec_init

Initialize a new feature specification.

**Description**: Creates a new specification directory with initial metadata.

**Parameters**:
- `feature_name` (string, required): Name of the feature (will be normalized to kebab-case).
- `description` (string, required): Brief description of the feature.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with initialization status and spec location.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "description": "Add OAuth 2.0 authentication with social providers",
  "project_dir": "."
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "spec_dir": ".kiro/specs/user-authentication-en",
  "description": "Add OAuth 2.0 authentication with social providers",
  "created_at": "2024-01-15T10:30:00"
}
```

---

### spec_requirements

Generate requirements document for a specification.

**Description**: Creates a requirements.md file with detailed feature requirements.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `auto_approve` (boolean, optional): Skip approval step. Defaults to false.

**Returns**: JSON with requirements document path and content.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": ".",
  "auto_approve": false
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "requirements_file": ".kiro/specs/user-authentication-en/requirements.md",
  "approval_required": true,
  "content": "# Requirements: User Authentication\n\n..."
}
```

---

### spec_design

Generate design document for a specification.

**Description**: Creates a design.md file with technical design details.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `auto_approve` (boolean, optional): Skip approval step. Defaults to false.

**Returns**: JSON with design document path and content.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": ".",
  "auto_approve": false
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "design_file": ".kiro/specs/user-authentication-en/design.md",
  "approval_required": true,
  "content": "# Design: User Authentication\n\n..."
}
```

---

### spec_tasks

Generate task breakdown for a specification.

**Description**: Creates a tasks.md file with detailed implementation tasks.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `auto_approve` (boolean, optional): Skip approval step. Defaults to false.

**Returns**: JSON with tasks document path and content.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": ".",
  "auto_approve": false
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "tasks_file": ".kiro/specs/user-authentication-en/tasks.md",
  "approval_required": true,
  "task_count": 12,
  "content": "# Tasks: User Authentication\n\n..."
}
```

---

### spec_status

Check the current status of a specification.

**Description**: Shows which specification documents exist and their completion status.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with specification status.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": "."
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "spec_dir": ".kiro/specs/user-authentication-en",
  "phases": {
    "requirements": {
      "completed": true,
      "file": "requirements.md",
      "last_modified": "2024-01-15T10:30:00"
    },
    "design": {
      "completed": true,
      "file": "design.md",
      "last_modified": "2024-01-15T10:45:00"
    },
    "tasks": {
      "completed": false,
      "file": null
    },
    "implementation": {
      "completed": false
    }
  },
  "progress": "50%"
}
```

---

## Template Management

Tools for managing and rendering templates.

### template_list

List all available templates.

**Description**: Shows all templates available in the system and custom project templates.

**Parameters**:
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `category` (string, optional): Filter by category (settings, specs, etc.).

**Returns**: JSON with list of templates.

**Example**:
```json
{
  "project_dir": ".",
  "category": "specs"
}
```

**Response**:
```json
{
  "success": true,
  "count": 8,
  "templates": [
    {
      "name": "requirements.md",
      "path": "specs/requirements.md",
      "category": "specs",
      "language": "en"
    },
    {
      "name": "design.md",
      "path": "specs/design.md",
      "category": "specs",
      "language": "en"
    }
  ],
  "category_filter": "specs"
}
```

---

### template_get

Get the raw content of a template.

**Description**: Retrieves the template source code (with Jinja2 syntax if applicable).

**Parameters**:
- `template_name` (string, required): Name of the template (e.g., "product", "tech", "structure").
- `template_type` (string, optional): Type of template ("steering", "requirements", "design", "tasks"). Defaults to "steering".
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with template content.

**Example**:
```json
{
  "template_name": "product",
  "template_type": "steering",
  "project_dir": "."
}
```

**Response**:
```json
{
  "success": true,
  "template_name": "product",
  "template_type": "steering",
  "content": "# Product Requirements\n\n## Overview\n{{ overview }}\n\n..."
}
```

---

### template_render

Render a template with Jinja2.

**Description**: Renders a template string or file using Jinja2 with provided context variables.

**Parameters**:
- `template_content` (string, required): Template content (Jinja2 syntax) or file path if use_file=true.
- `context` (object, optional): Dictionary of context variables for rendering. Defaults to {}.
- `use_file` (boolean, optional): If true, template_content is treated as a file path. Defaults to false.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with rendered content.

**Example** (render string):
```json
{
  "template_content": "# {{ title }}\n\n{{ description }}\n\n{% for item in items %}\\n- {{ item }}\\n{% endfor %}",
  "context": {
    "title": "My Feature",
    "description": "Feature description",
    "items": ["Item 1", "Item 2", "Item 3"]
  }
}
```

**Example** (render file):
```json
{
  "template_content": "specs/requirements.md",
  "context": {
    "feature_name": "user-auth",
    "description": "OAuth authentication"
  },
  "use_file": true
}
```

**Response**:
```json
{
  "success": true,
  "rendered_content": "# My Feature\n\nFeature description\n\n- Item 1\n- Item 2\n- Item 3\n",
  "context_used": {
    "title": "My Feature",
    "description": "Feature description",
    "items": ["Item 1", "Item 2", "Item 3"]
  }
}
```

---

## Validation Tools

Tools for validating specifications and implementations.

### validate_gap

Analyze the gap between existing codebase and requirements.

**Description**: Compares the current codebase with the requirements document to identify what needs to be implemented.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `scope_paths` (array of strings, optional): Specific paths to analyze. If not provided, analyzes entire project.

**Returns**: JSON with gap analysis.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": ".",
  "scope_paths": ["src/auth", "src/api"]
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "gaps": [
    {
      "requirement": "OAuth 2.0 provider integration",
      "status": "missing",
      "severity": "high",
      "suggested_files": ["src/auth/oauth.py"]
    },
    {
      "requirement": "Social login buttons",
      "status": "partial",
      "severity": "medium",
      "current_implementation": "src/components/LoginForm.tsx",
      "missing_providers": ["GitHub", "Google"]
    }
  ],
  "summary": {
    "total_requirements": 15,
    "implemented": 8,
    "partial": 4,
    "missing": 3
  }
}
```

---

### validate_design

Validate design document completeness.

**Description**: Checks if the design document adequately addresses all requirements.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.

**Returns**: JSON with validation results.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": "."
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "validation_results": {
    "completeness": "85%",
    "missing_sections": [
      "Error handling strategy",
      "Security considerations"
    ],
    "requirements_coverage": {
      "covered": 12,
      "missing": 3,
      "details": [
        {
          "requirement": "Session management",
          "covered": false,
          "reason": "Not mentioned in design document"
        }
      ]
    }
  },
  "recommendations": [
    "Add section on error handling",
    "Document security measures for OAuth tokens",
    "Specify session timeout strategy"
  ]
}
```

---

### validate_impl

Validate implementation against task breakdown.

**Description**: Checks if the implementation matches the tasks defined in the specification.

**Parameters**:
- `feature_name` (string, required): Name of the feature specification.
- `project_dir` (string, optional): Project directory path. Defaults to current directory.
- `scope_paths` (array of strings, optional): Specific paths to validate. If not provided, validates entire project.

**Returns**: JSON with validation results.

**Example**:
```json
{
  "feature_name": "user-authentication",
  "project_dir": ".",
  "scope_paths": ["src/auth"]
}
```

**Response**:
```json
{
  "success": true,
  "feature_name": "user-authentication",
  "validation_results": {
    "task_completion": "75%",
    "completed_tasks": [
      "1.1 Create OAuth service class",
      "1.2 Implement Google OAuth flow",
      "2.1 Add login UI components"
    ],
    "pending_tasks": [
      "1.3 Implement GitHub OAuth flow",
      "3.1 Add session management",
      "3.2 Implement token refresh"
    ],
    "files_validated": [
      {
        "path": "src/auth/oauth_service.py",
        "tasks": ["1.1", "1.2"],
        "status": "complete"
      },
      {
        "path": "src/components/LoginForm.tsx",
        "tasks": ["2.1"],
        "status": "partial",
        "issues": ["Missing GitHub login button"]
      }
    ]
  },
  "summary": {
    "total_tasks": 8,
    "completed": 6,
    "pending": 2,
    "completion_rate": "75%"
  }
}
```

---

## Error Handling

All tools return errors in a consistent format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "details": {
    "error_type": "ValueError",
    "error_code": "INVALID_PARAMETER"
  }
}
```

Common error types:
- `FileNotFoundError`: Requested file or specification not found
- `ValueError`: Invalid parameter or configuration
- `PermissionError`: Insufficient permissions to access or modify files
- `ValidationError`: Data validation failed

---

## Best Practices

### 1. Always Check Status First

Before performing operations, check status to understand current state:

```json
// Check steering status before initializing
{ "tool": "steering_status" }

// Check spec status before generating documents
{ "tool": "spec_status", "arguments": { "feature_name": "my-feature" } }
```

### 2. Use Auto-Approve Carefully

The `auto_approve` flag bypasses human review:

```json
// Development/testing - OK to use auto_approve
{ "tool": "spec_design", "arguments": { "auto_approve": true } }

// Production - prefer human review
{ "tool": "spec_design", "arguments": { "auto_approve": false } }
```

### 3. Validate Before Implementation

Always run validation tools before and after implementation:

```json
// Before implementation
{ "tool": "validate_gap", "arguments": { "feature_name": "my-feature" } }

// After implementation
{ "tool": "validate_impl", "arguments": { "feature_name": "my-feature" } }
```

### 4. Use Specific Scope Paths

For large projects, limit validation scope for better performance:

```json
{
  "tool": "validate_gap",
  "arguments": {
    "feature_name": "my-feature",
    "scope_paths": ["src/features/my-feature", "src/lib/related"]
  }
}
```

---

## Version History

- **v0.1.0** (2024-01): Initial release with 15 MCP tools
  - 4 steering management tools
  - 5 specification lifecycle tools
  - 3 template management tools
  - 3 validation tools

---

For more information, see:
- [Server README](../src/cc_sdd_mcp/README.md)
- [Integration Guide](./integration_guide.md)
- [Main Project Documentation](../README.md)

