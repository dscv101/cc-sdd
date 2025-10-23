"""CLI entry point for cc-sdd MCP server."""

import asyncio
import sys

from cc_sdd_mcp.server import serve


def main() -> None:
    """Main entry point for the cc-sdd MCP server.

    This function is called when running:
    - python -m cc_sdd_mcp
    - cc-sdd-mcp (via console script)
    """
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
