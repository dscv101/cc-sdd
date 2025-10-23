"""Command-line interface for cc-sdd MCP server."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

import click

from cc_sdd_mcp.models.config import ServerConfig
from cc_sdd_mcp.server import serve
from cc_sdd_mcp.tools.registry import get_all_tools, get_tool_handler

__version__ = "0.1.0"


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to configuration file",
)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
def cli(ctx: click.Context, config: Path | None, version: bool) -> None:
    """cc-sdd MCP Server - Spec-Driven Development for AI assistants.

    Run without a command to start the MCP server (equivalent to 'start' command).
    """
    if version:
        click.echo(f"cc-sdd-mcp version {__version__}")
        ctx.exit(0)

    # If no subcommand is provided, default to start
    if ctx.invoked_subcommand is None:
        ctx.invoke(start, config=config)


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to configuration file",
)
@click.option(
    "--log-level",
    "-l",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    help="Logging level",
)
def start(config: Path | None, log_level: str | None) -> None:
    """Start the MCP server.

    The server communicates via stdio (standard input/output) using the
    Model Context Protocol. It should be configured in your MCP client
    (e.g., Claude Desktop) to use this command.

    Examples:

        # Start with default configuration
        cc-sdd-mcp start

        # Start with custom config file
        cc-sdd-mcp start --config .cc-sdd.config.json

        # Start with debug logging
        cc-sdd-mcp start --log-level DEBUG
    """
    try:
        # Load configuration
        server_config = ServerConfig.load(config) if config else ServerConfig.load()

        # Override log level if provided
        if log_level:
            server_config.log_level = log_level.upper()

        # Start the server
        click.echo(
            f"Starting {server_config.server_name} v{server_config.server_version}",
            err=True,
        )
        click.echo(f"Project directory: {server_config.project_dir}", err=True)
        click.echo(f"Log level: {server_config.log_level}", err=True)

        # Run the server
        asyncio.run(serve(server_config))

    except KeyboardInterrupt:
        click.echo("\nServer stopped by user", err=True)
        sys.exit(0)
    except Exception as e:
        click.echo(f"Fatal error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
def list_tools(json_output: bool) -> None:
    """List all available MCP tools.

    Shows all registered tools with their names and descriptions.

    Examples:

        # List tools in human-readable format
        cc-sdd-mcp list-tools

        # List tools in JSON format
        cc-sdd-mcp list-tools --json
    """
    tools = get_all_tools()

    if json_output:
        tool_list = [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in tools
        ]
        click.echo(json.dumps({"count": len(tools), "tools": tool_list}, indent=2))
    else:
        click.echo(f"\n✨ Available MCP Tools ({len(tools)})\n")
        click.echo("=" * 60)

        # Group tools by category
        categories = {
            "Steering": [],
            "Specification": [],
            "Template": [],
            "Validation": [],
        }

        for tool in tools:
            if tool.name.startswith("steering_"):
                categories["Steering"].append(tool)
            elif tool.name.startswith("spec_"):
                categories["Specification"].append(tool)
            elif tool.name.startswith("template_"):
                categories["Template"].append(tool)
            elif tool.name.startswith("validate_"):
                categories["Validation"].append(tool)

        for category, cat_tools in categories.items():
            if cat_tools:
                click.echo(f"\n📁 {category} Tools:")
                for tool in cat_tools:
                    click.echo(f"   • {tool.name:30} - {tool.description}")

        click.echo("\n" + "=" * 60)
        click.echo("\nUse 'cc-sdd-mcp inspect-tool <name>' for detailed information")


@cli.command()
@click.argument("tool_name")
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
def inspect_tool(tool_name: str, json_output: bool) -> None:
    """Inspect a specific MCP tool.

    Shows detailed information about a tool including its input schema
    and available parameters.

    Examples:

        # Inspect a tool
        cc-sdd-mcp inspect-tool spec_init

        # Inspect a tool with JSON output
        cc-sdd-mcp inspect-tool spec_init --json
    """
    tools = get_all_tools()
    tool = next((t for t in tools if t.name == tool_name), None)

    if not tool:
        click.echo(f"❌ Tool '{tool_name}' not found", err=True)
        click.echo(f"\nAvailable tools: {', '.join(t.name for t in tools)}", err=True)
        sys.exit(1)

    if json_output:
        tool_info = {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.inputSchema,
        }
        click.echo(json.dumps(tool_info, indent=2))
    else:
        click.echo(f"\n🔍 Tool: {tool.name}\n")
        click.echo("=" * 60)
        click.echo(f"\nDescription: {tool.description}\n")

        if tool.inputSchema and "properties" in tool.inputSchema:
            click.echo("Parameters:")
            properties = tool.inputSchema["properties"]
            required = tool.inputSchema.get("required", [])

            for param_name, param_info in properties.items():
                required_marker = " (required)" if param_name in required else ""
                param_type = param_info.get("type", "unknown")
                param_desc = param_info.get("description", "No description")

                click.echo(f"\n  • {param_name}{required_marker}")
                click.echo(f"    Type: {param_type}")
                click.echo(f"    Description: {param_desc}")

        click.echo("\n" + "=" * 60)


@cli.command()
@click.argument("tool_name")
@click.option("--args", "-a", help="JSON string of arguments to pass to the tool")
def test_tool(tool_name: str, args: str | None) -> None:
    """Test a tool with sample arguments.

    This command executes a tool with the provided arguments and shows
    the result. Useful for debugging and testing tool behavior.

    Examples:

        # Test spec_init
        cc-sdd-mcp test-tool spec_init --args '{"description": "Test feature"}'

        # Test steering_status
        cc-sdd-mcp test-tool steering_status
    """
    handler = get_tool_handler(tool_name)

    if not handler:
        click.echo(f"❌ Tool '{tool_name}' not found", err=True)
        tools = get_all_tools()
        click.echo(f"\nAvailable tools: {', '.join(t.name for t in tools)}", err=True)
        sys.exit(1)

    # Parse arguments
    tool_args: dict[str, Any] = {}
    if args:
        try:
            tool_args = json.loads(args)
        except json.JSONDecodeError as e:
            click.echo(f"❌ Invalid JSON arguments: {e}", err=True)
            sys.exit(1)

    # Execute the tool
    click.echo(f"\n🔧 Testing tool: {tool_name}\n")
    click.echo("=" * 60)
    click.echo(f"\nArguments: {json.dumps(tool_args, indent=2)}\n")

    try:

        async def run_test() -> Any:
            return await handler(tool_args)

        result = asyncio.run(run_test())
        click.echo("Result:")
        click.echo(result)
        click.echo("\n" + "=" * 60)
        click.echo("\n✅ Tool executed successfully")

    except Exception as e:
        click.echo(f"\n❌ Tool execution failed: {e}", err=True)
        import traceback

        click.echo("\nTraceback:", err=True)
        click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to configuration file to validate",
)
def validate_config(config: Path | None) -> None:
    """Validate server configuration.

    Checks if the configuration file is valid and shows the current
    configuration settings.

    Examples:

        # Validate default configuration
        cc-sdd-mcp validate-config

        # Validate specific config file
        cc-sdd-mcp validate-config --config .cc-sdd.config.json
    """
    click.echo("\n🔍 Validating configuration...\n")
    click.echo("=" * 60)

    try:
        server_config = ServerConfig.load(config) if config else ServerConfig.load()

        click.echo("\n✅ Configuration is valid\n")
        click.echo("Current Settings:")
        click.echo(f"  • Server Name: {server_config.server_name}")
        click.echo(f"  • Server Version: {server_config.server_version}")
        click.echo(f"  • Log Level: {server_config.log_level}")
        click.echo(f"  • Project Directory: {server_config.project_dir}")
        click.echo(f"  • Kiro Directory: {server_config.kiro_dir}")
        click.echo(f"  • Default Language: {server_config.default_language}")
        click.echo(f"  • Template Cache: {server_config.template_cache_enabled}")
        click.echo(f"  • Auto Create Steering: {server_config.auto_create_steering}")
        click.echo(f"  • Strict Phase Gates: {server_config.strict_phase_gates}")

        click.echo("\n" + "=" * 60)
        click.echo("\n✨ Configuration loaded successfully")

    except Exception as e:
        click.echo(f"\n❌ Configuration validation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def version() -> None:
    """Show version information."""
    click.echo(f"cc-sdd-mcp version {__version__}")
    click.echo("Model Context Protocol (MCP) server for Spec-Driven Development")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
