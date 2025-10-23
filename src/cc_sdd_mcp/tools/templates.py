"""MCP tools for template management."""

import json
import logging
from pathlib import Path
from typing import Any

from mcp.types import Tool

from cc_sdd_mcp.tools.registry import register_tool
from cc_sdd_mcp.utils.templates import TemplateLoader

logger = logging.getLogger(__name__)


# Tool: template_list
async def template_list_handler(arguments: dict[str, Any]) -> str:
    """List all available templates.

    Args:
        arguments: Tool arguments containing:
            - project_dir: Optional project directory
            - category: Optional category filter

    Returns:
        JSON string with list of templates
    """
    project_dir = Path(arguments.get("project_dir", "."))
    category = arguments.get("category")

    loader = TemplateLoader(project_dir=project_dir)
    templates = loader.list_templates(category=category)

    return json.dumps(
        {
            "success": True,
            "count": len(templates),
            "templates": templates,
            "category_filter": category,
        },
        indent=2,
    )


template_list_tool = Tool(
    name="template_list",
    description="List all available templates with their paths and categories",
    inputSchema={
        "type": "object",
        "properties": {
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
            "category": {
                "type": "string",
                "description": "Optional category filter (e.g., 'settings', 'specs')",
            },
        },
        "required": [],
    },
)

register_tool(template_list_tool, template_list_handler)


# Tool: template_get
async def template_get_handler(arguments: dict[str, Any]) -> str:
    """Get raw template content.

    Args:
        arguments: Tool arguments containing:
            - template_name: Name of the template
            - template_type: Type (steering or spec)
            - project_dir: Optional project directory

    Returns:
        JSON string with template content
    """
    template_name = arguments.get("template_name")
    template_type = arguments.get("template_type", "steering")
    project_dir = Path(arguments.get("project_dir", "."))

    if not template_name:
        raise ValueError("template_name is required")

    loader = TemplateLoader(project_dir=project_dir)

    # Load template based on type
    if template_type == "steering":
        content = loader.load_steering_template(template_name)
    else:
        content = loader.load_spec_template(template_name, spec_type=template_type)

    if content is None:
        return json.dumps(
            {
                "success": False,
                "error": f"Template '{template_name}' not found for type '{template_type}'",
            },
            indent=2,
        )

    return json.dumps(
        {
            "success": True,
            "template_name": template_name,
            "template_type": template_type,
            "content": content,
        },
        indent=2,
    )


template_get_tool = Tool(
    name="template_get",
    description="Get the raw content of a template",
    inputSchema={
        "type": "object",
        "properties": {
            "template_name": {
                "type": "string",
                "description": "Name of the template (e.g., 'product', 'tech', 'structure')",
            },
            "template_type": {
                "type": "string",
                "description": "Type of template: 'steering', 'requirements', 'design', or 'tasks'",
            },
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["template_name"],
    },
)

register_tool(template_get_tool, template_get_handler)


# Tool: template_render
async def template_render_handler(arguments: dict[str, Any]) -> str:
    """Render a template with context variables.

    Args:
        arguments: Tool arguments containing:
            - template_content: Template content or path
            - context: Dictionary of context variables
            - use_file: Whether template_content is a file path
            - project_dir: Optional project directory

    Returns:
        JSON string with rendered content
    """
    template_content = arguments.get("template_content")
    context = arguments.get("context", {})
    use_file = arguments.get("use_file", False)
    project_dir = Path(arguments.get("project_dir", "."))

    if not template_content:
        raise ValueError("template_content is required")

    loader = TemplateLoader(project_dir=project_dir)

    try:
        if use_file:
            # Render from file
            rendered = loader.render_jinja_file(template_content, context)
        else:
            # Render from string
            rendered = loader.render_jinja_template(template_content, context)

        return json.dumps(
            {"success": True, "rendered_content": rendered, "context_used": context}, indent=2
        )

    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        return json.dumps(
            {"success": False, "error": f"Failed to render template: {str(e)}"}, indent=2
        )


template_render_tool = Tool(
    name="template_render",
    description="Render a template with Jinja2 using provided context variables",
    inputSchema={
        "type": "object",
        "properties": {
            "template_content": {
                "type": "string",
                "description": "Template content (Jinja2 syntax) or file path if use_file=true",
            },
            "context": {
                "type": "object",
                "description": "Context variables for template rendering",
            },
            "use_file": {
                "type": "boolean",
                "description": "If true, template_content is treated as a file path",
            },
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["template_content"],
    },
)

register_tool(template_render_tool, template_render_handler)
