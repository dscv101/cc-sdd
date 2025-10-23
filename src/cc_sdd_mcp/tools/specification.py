"""MCP tools for specification lifecycle management."""

import json
import logging
from pathlib import Path
from typing import Any

from mcp.types import Tool

from cc_sdd_mcp.models.specification import (
    SpecificationMetadata,
    SpecPhase,
)
from cc_sdd_mcp.models.steering import SteeringConfig
from cc_sdd_mcp.tools.registry import register_tool
from cc_sdd_mcp.utils.filesystem import FileSystemManager
from cc_sdd_mcp.workflows.spec_workflow import SpecWorkflow

logger = logging.getLogger(__name__)


# Tool: spec_init
async def spec_init_handler(arguments: dict[str, Any]) -> str:
    """Initialize a new feature specification.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - description: Brief description
            - project_dir: Optional project directory

    Returns:
        JSON string with initialization result
    """
    feature_name = arguments.get("feature_name")
    description = arguments.get("description")
    project_dir = Path(arguments.get("project_dir", "."))

    if not feature_name or not description:
        raise ValueError("Both feature_name and description are required")

    # Initialize spec
    config = SteeringConfig()

    # Create metadata
    metadata = SpecificationMetadata(
        feature_name=feature_name, description=description, current_phase=SpecPhase.INITIALIZED
    )

    # Create spec directory
    spec_dir = project_dir / config.kiro_dir / "specs" / metadata.feature_name
    spec_dir.mkdir(parents=True, exist_ok=True)

    # Write metadata
    metadata_file = spec_dir / "metadata.json"
    metadata_file.write_text(metadata.model_dump_json(indent=2))

    logger.info(f"Initialized specification: {metadata.feature_name}")

    return json.dumps(
        {
            "success": True,
            "feature_name": metadata.feature_name,
            "spec_dir": str(spec_dir),
            "current_phase": metadata.current_phase.value,
            "message": f"Specification '{metadata.feature_name}' initialized successfully",
        },
        indent=2,
    )


spec_init_tool = Tool(
    name="spec_init",
    description="Initialize a new feature specification",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {
                "type": "string",
                "description": "Name of the feature (will be normalized)",
            },
            "description": {"type": "string", "description": "Brief description of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
        },
        "required": ["feature_name", "description"],
    },
)

register_tool(spec_init_tool, spec_init_handler)


# Tool: spec_requirements
async def spec_requirements_handler(arguments: dict[str, Any]) -> str:
    """Generate requirements document for a specification.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory
            - auto_approve: Optional auto-approval flag

    Returns:
        JSON string with requirements generation result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))
    auto_approve = arguments.get("auto_approve", False)

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = SpecWorkflow(project_dir)
    result = await workflow.generate_requirements(feature_name, auto_approve=auto_approve)

    return json.dumps(result, indent=2)


spec_requirements_tool = Tool(
    name="spec_requirements",
    description="Generate requirements document for a feature specification",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
            "auto_approve": {
                "type": "boolean",
                "description": "Auto-approve and move to next phase (default: false)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(spec_requirements_tool, spec_requirements_handler)


# Tool: spec_design
async def spec_design_handler(arguments: dict[str, Any]) -> str:
    """Generate design document for a specification.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory
            - auto_approve: Optional auto-approval flag

    Returns:
        JSON string with design generation result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))
    auto_approve = arguments.get("auto_approve", False)

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = SpecWorkflow(project_dir)
    result = await workflow.generate_design(feature_name, auto_approve=auto_approve)

    return json.dumps(result, indent=2)


spec_design_tool = Tool(
    name="spec_design",
    description="Generate design document for a feature specification",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
            "auto_approve": {
                "type": "boolean",
                "description": "Auto-approve and move to next phase (default: false)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(spec_design_tool, spec_design_handler)


# Tool: spec_tasks
async def spec_tasks_handler(arguments: dict[str, Any]) -> str:
    """Generate task breakdown for a specification.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory
            - auto_approve: Optional auto-approval flag

    Returns:
        JSON string with tasks generation result
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))
    auto_approve = arguments.get("auto_approve", False)

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = SpecWorkflow(project_dir)
    result = await workflow.generate_tasks(feature_name, auto_approve=auto_approve)

    return json.dumps(result, indent=2)


spec_tasks_tool = Tool(
    name="spec_tasks",
    description="Generate task breakdown for a feature specification",
    inputSchema={
        "type": "object",
        "properties": {
            "feature_name": {"type": "string", "description": "Name of the feature"},
            "project_dir": {
                "type": "string",
                "description": "Project directory (defaults to current directory)",
            },
            "auto_approve": {
                "type": "boolean",
                "description": "Auto-approve and move to next phase (default: false)",
            },
        },
        "required": ["feature_name"],
    },
)

register_tool(spec_tasks_tool, spec_tasks_handler)


# Tool: spec_status
async def spec_status_handler(arguments: dict[str, Any]) -> str:
    """Check status of a feature specification.

    Args:
        arguments: Tool arguments containing:
            - feature_name: Name of the feature
            - project_dir: Optional project directory

    Returns:
        JSON string with specification status
    """
    feature_name = arguments.get("feature_name")
    project_dir = Path(arguments.get("project_dir", "."))

    if not feature_name:
        raise ValueError("feature_name is required")

    workflow = SpecWorkflow(project_dir)
    status = await workflow.get_spec_status(feature_name)

    return json.dumps(status, indent=2)


spec_status_tool = Tool(
    name="spec_status",
    description="Check the current status of a feature specification",
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

register_tool(spec_status_tool, spec_status_handler)
