"""MCP server implementation for cc-sdd."""

import json
import logging
from collections.abc import Sequence
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    TextContent,
    Tool,
)

from cc_sdd_mcp.tools.registry import get_all_tools, get_tool_handler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_server() -> Server:
    """Create and configure the MCP server.

    Returns:
        Configured MCP server instance
    """
    server = Server("cc-sdd-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available cc-sdd tools.

        Returns:
            List of Tool definitions with their schemas
        """
        logger.info("Listing available tools")
        tools = get_all_tools()
        logger.info(f"Found {len(tools)} tools")
        return tools

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any]
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool invocation.

        Args:
            name: Name of the tool to invoke
            arguments: Arguments passed to the tool

        Returns:
            List of content items (text, images, or embedded resources)

        Raises:
            ValueError: If tool is not found or arguments are invalid
        """
        logger.info(f"Calling tool: {name} with arguments: {arguments}")

        try:
            # Get the tool handler
            handler = get_tool_handler(name)
            if handler is None:
                raise ValueError(f"Unknown tool: {name}")

            # Execute the tool handler
            result = await handler(arguments)

            # Format result as TextContent
            if isinstance(result, str):
                content = result
            elif isinstance(result, dict):
                content = json.dumps(result, indent=2)
            else:
                # Assume it's a Pydantic model
                content = result.model_dump_json(indent=2)

            logger.info(f"Tool {name} executed successfully")
            return [TextContent(type="text", text=content)]

        except Exception as e:
            error_msg = f"Error executing tool {name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise ValueError(error_msg) from e

    return server


async def serve() -> None:
    """Run the MCP server with stdio transport.

    This is the main entry point for the server. It sets up the server
    and runs it with stdio transport for communication with MCP clients.
    """
    logger.info("Starting cc-sdd MCP server")

    server = create_server()
    options = server.create_initialization_options()

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server ready, waiting for requests")
        await server.run(read_stream, write_stream, options)
