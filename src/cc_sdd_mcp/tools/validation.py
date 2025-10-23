"""MCP tools for specification validation."""

import logging
from pathlib import Path
from typing import Any

from mcp.types import Tool

from cc_sdd_mcp.tools.registry import register_tool
from cc_sdd_mcp.workflows.validation_workflow import ValidationWorkflow

logger = logging.getLogger(__name__)


# Tool: validate_gap
async def validate_gap_handler(arguments: dict[str, Any]) -> str:
    """Analyze gap between existing code and requirements.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory

    Returns:
        JSON string with gap analysis result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = ValidationWorkflow(project_dir)
    result = await workflow.validate_gap(feature_name)

    return result.model_dump_json(indent=2)


validate_gap_tool = Tool(
    name="validate_gap",
    description="Analyze the gap between existing codebase and requirements",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(validate_gap_tool, validate_gap_handler)


# Tool: validate_design
async def validate_design_handler(arguments: dict[str, Any]) -> str:
    """Validate design document against requirements.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory

    Returns:
        JSON string with design validation result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = ValidationWorkflow(project_dir)
    result = await workflow.validate_design(feature_name)

    return result.model_dump_json(indent=2)


validate_design_tool = Tool(
    name="validate_design",
    description="Validate design document completeness and alignment with requirements",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(validate_design_tool, validate_design_handler)


# Tool: validate_impl
async def validate_impl_handler(arguments: dict[str, Any]) -> str:
    """Validate implementation against task breakdown.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory

    Returns:
        JSON string with implementation validation result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = ValidationWorkflow(project_dir)
    result = await workflow.validate_implementation(feature_name)

    return result.model_dump_json(indent=2)


validate_impl_tool = Tool(
    name="validate_impl",
    description="Validate implementation completeness against task breakdown",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(validate_impl_tool, validate_impl_handler)
