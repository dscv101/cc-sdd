"""Tool registry for managing MCP tool definitions and handlers."""

import contextlib
from collections.abc import Awaitable, Callable
from typing import Any

from mcp.types import Tool

# Type alias for tool handler functions
ToolHandler = Callable[[dict[str, Any]], Awaitable[Any]]

# Registry of tool handlers
_TOOL_HANDLERS: dict[str, ToolHandler] = {}

# Registry of tool definitions
_TOOL_DEFINITIONS: dict[str, Tool] = {}


def register_tool(tool: Tool, handler: ToolHandler) -> None:
    """Register a tool with its handler.

    Args:
        tool: Tool definition with name, description, and inputSchema
        handler: Async function that handles tool invocation
    """
    _TOOL_DEFINITIONS[tool.name] = tool
    _TOOL_HANDLERS[tool.name] = handler


def get_tool_handler(name: str) -> ToolHandler | None:
    """Get the handler for a tool by name.

    Args:
        name: Name of the tool

    Returns:
        Tool handler function, or None if not found
    """
    return _TOOL_HANDLERS.get(name)


def get_all_tools() -> list[Tool]:
    """Get all registered tool definitions.

    Returns:
        List of all registered Tool definitions
    """
    return list(_TOOL_DEFINITIONS.values())


def clear_registry() -> None:
    """Clear all registered tools (useful for testing)."""
    _TOOL_HANDLERS.clear()
    _TOOL_DEFINITIONS.clear()


# Import tool modules to register them
# These imports will trigger tool registration via decorators or direct calls
# For now, we'll add them as we implement each tool module

with contextlib.suppress(ImportError):
    from cc_sdd_mcp.tools import steering  # noqa: F401

with contextlib.suppress(ImportError):
    from cc_sdd_mcp.tools import specification  # noqa: F401

with contextlib.suppress(ImportError):
    from cc_sdd_mcp.tools import validation  # noqa: F401
