"""MCP tools for steering (project memory) management."""

from typing import Any

from mcp.types import Tool

from cc_sdd_mcp.models.steering import SteeringFileType, SteeringStatus
from cc_sdd_mcp.tools.registry import register_tool
from cc_sdd_mcp.utils.filesystem import FileSystemManager
from cc_sdd_mcp.utils.paths import get_project_path_from_args
from cc_sdd_mcp.utils.templates import TemplateLoader


async def steering_init_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Initialize steering documents.

    Args:
        arguments: Tool arguments containing:
            - project_path (optional): Path to project
            - language (optional): Language code

    Returns:
        Dictionary with initialization result
    """
    project_path_str = arguments.get("project_path")
    language = arguments.get("language", "en")

    project_root = get_project_path_from_args(project_path_str)
    fs_manager = FileSystemManager(project_root)
    template_loader = TemplateLoader(language)

    # Ensure steering directory exists
    fs_manager.ensure_steering_exists()

    # Create default steering files
    created_files = []
    for file_type in [
        SteeringFileType.PRODUCT,
        SteeringFileType.TECH,
        SteeringFileType.STRUCTURE,
    ]:
        # Load template
        template = template_loader.load_steering_template(file_type.value)
        if template:
            # Write steering document
            doc = fs_manager.write_steering_document(file_type, template)
            created_files.append(str(doc.file_path))

    return {
        "status": "success",
        "message": f"Initialized {len(created_files)} steering documents",
        "files_created": created_files,
        "steering_dir": str(fs_manager.steering_dir),
        "language": language,
    }


async def steering_status_handler(arguments: dict[str, Any]) -> SteeringStatus:
    """Get status of steering documents.

    Args:
        arguments: Tool arguments containing:
            - project_path (optional): Path to project

    Returns:
        SteeringStatus object
    """
    project_path_str = arguments.get("project_path")
    project_root = get_project_path_from_args(project_path_str)
    fs_manager = FileSystemManager(project_root)

    # Check if steering directory exists
    exists = fs_manager.steering_dir.exists()

    # List existing documents
    documents = fs_manager.list_steering_documents()

    # Find missing defaults
    default_types = [
        SteeringFileType.PRODUCT,
        SteeringFileType.TECH,
        SteeringFileType.STRUCTURE,
    ]
    existing_types = {doc.file_type for doc in documents}
    missing_defaults = [file_type for file_type in default_types if file_type not in existing_types]

    # Get most recent modification time
    last_updated = None
    if documents:
        last_updated = max(doc.last_modified for doc in documents)

    return SteeringStatus(
        exists=exists,
        steering_dir=fs_manager.steering_dir,
        documents=documents,
        missing_defaults=missing_defaults,
        last_updated=last_updated,
    )


async def steering_read_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Read steering documents.

    Args:
        arguments: Tool arguments containing:
            - file_name (optional): Specific file to read (product, tech, structure)
            - project_path (optional): Path to project

    Returns:
        Dictionary with steering content
    """
    project_path_str = arguments.get("project_path")
    file_name = arguments.get("file_name")

    project_root = get_project_path_from_args(project_path_str)
    fs_manager = FileSystemManager(project_root)

    if file_name:
        # Read specific file
        try:
            file_type = SteeringFileType(file_name)
            doc = fs_manager.read_steering_document(file_type)
            if doc is None:
                return {
                    "status": "error",
                    "message": f"Steering document '{file_name}' not found",
                }
            return {
                "status": "success",
                "file_type": doc.file_type.value,
                "file_path": str(doc.file_path),
                "content": doc.content,
                "last_modified": doc.last_modified.isoformat(),
            }
        except ValueError:
            return {
                "status": "error",
                "message": f"Invalid file name '{file_name}'. Valid: product, tech, structure",
            }
    else:
        # Read all documents
        documents = fs_manager.list_steering_documents()
        return {
            "status": "success",
            "count": len(documents),
            "documents": [
                {
                    "file_type": doc.file_type.value,
                    "file_path": str(doc.file_path),
                    "content": doc.content,
                    "last_modified": doc.last_modified.isoformat(),
                }
                for doc in documents
            ],
        }


async def steering_update_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Update a steering document.

    Args:
        arguments: Tool arguments containing:
            - file_name: Name of file to update (product, tech, structure)
            - content: New content for the file
            - project_path (optional): Path to project

    Returns:
        Dictionary with update result
    """
    file_name = arguments.get("file_name")
    content = arguments.get("content")
    project_path_str = arguments.get("project_path")

    if not file_name:
        return {"status": "error", "message": "file_name is required"}
    if not content:
        return {"status": "error", "message": "content is required"}

    project_root = get_project_path_from_args(project_path_str)
    fs_manager = FileSystemManager(project_root)

    try:
        file_type = SteeringFileType(file_name)
        doc = fs_manager.write_steering_document(file_type, content)
        return {
            "status": "success",
            "message": f"Updated {file_name}.md",
            "file_path": str(doc.file_path),
            "last_modified": doc.last_modified.isoformat(),
        }
    except ValueError:
        return {
            "status": "error",
            "message": f"Invalid file name '{file_name}'. Valid: product, tech, structure",
        }


# Register tools
register_tool(
    Tool(
        name="steering_init",
        description="Initialize steering documents (project memory) for cc-sdd. Creates product.md, tech.md, and structure.md in .kiro/steering/ directory.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Optional path to project root (defaults to current directory)",
                },
                "language": {
                    "type": "string",
                    "description": "Language code for templates (en, ja, zh-TW, etc.)",
                    "default": "en",
                },
            },
        },
    ),
    steering_init_handler,
)

register_tool(
    Tool(
        name="steering_status",
        description="Get the status of steering documents in the project. Shows which files exist and when they were last updated.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Optional path to project root (defaults to current directory)",
                },
            },
        },
    ),
    steering_status_handler,
)

register_tool(
    Tool(
        name="steering_read",
        description="Read steering documents. Can read a specific file or all files.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Optional name of specific file to read (product, tech, or structure). Omit to read all files.",
                    "enum": ["product", "tech", "structure"],
                },
                "project_path": {
                    "type": "string",
                    "description": "Optional path to project root (defaults to current directory)",
                },
            },
        },
    ),
    steering_read_handler,
)

register_tool(
    Tool(
        name="steering_update",
        description="Update a steering document with new content.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of file to update (product, tech, or structure)",
                    "enum": ["product", "tech", "structure"],
                },
                "content": {
                    "type": "string",
                    "description": "New content for the steering document (Markdown format)",
                },
                "project_path": {
                    "type": "string",
                    "description": "Optional path to project root (defaults to current directory)",
                },
            },
            "required": ["file_name", "content"],
        },
    ),
    steering_update_handler,
)
