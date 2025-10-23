"""Tests for the CLI module."""

import json
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cc_sdd_mcp.cli import cli


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def setup_registry():
    """Set up the tool registry before each test."""
    # Tools are automatically registered on import
    # Just ensure they're imported
    import cc_sdd_mcp.tools.specification  # noqa: F401
    import cc_sdd_mcp.tools.steering  # noqa: F401
    import cc_sdd_mcp.tools.templates  # noqa: F401
    import cc_sdd_mcp.tools.validation  # noqa: F401

    yield


class TestVersion:
    """Tests for version command."""

    def test_version_command(self, runner):
        """Test version command output."""
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "cc-sdd-mcp version" in result.output
        assert "Model Context Protocol" in result.output

    def test_version_flag(self, runner):
        """Test --version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "cc-sdd-mcp version" in result.output


class TestListTools:
    """Tests for list-tools command."""

    def test_list_tools_default(self, runner):
        """Test listing tools in human-readable format."""
        result = runner.invoke(cli, ["list-tools"])
        assert result.exit_code == 0
        assert "Available MCP Tools" in result.output
        assert "Steering Tools:" in result.output
        assert "Specification Tools:" in result.output
        assert "Template Tools:" in result.output
        assert "Validation Tools:" in result.output
        assert "steering_init" in result.output
        assert "spec_init" in result.output
        assert "template_list" in result.output
        assert "validate_gap" in result.output

    def test_list_tools_json(self, runner):
        """Test listing tools in JSON format."""
        result = runner.invoke(cli, ["list-tools", "--json"])
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert "count" in data
        assert "tools" in data
        assert data["count"] > 0
        assert len(data["tools"]) == data["count"]

        # Verify tool structure
        tool = data["tools"][0]
        assert "name" in tool
        assert "description" in tool


class TestInspectTool:
    """Tests for inspect-tool command."""

    def test_inspect_tool_default(self, runner):
        """Test inspecting a tool in human-readable format."""
        result = runner.invoke(cli, ["inspect-tool", "spec_init"])
        assert result.exit_code == 0
        assert "Tool: spec_init" in result.output
        assert "Description:" in result.output
        assert "Parameters:" in result.output
        assert "feature_name" in result.output
        assert "description" in result.output

    def test_inspect_tool_json(self, runner):
        """Test inspecting a tool in JSON format."""
        result = runner.invoke(cli, ["inspect-tool", "spec_init", "--json"])
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert data["name"] == "spec_init"
        assert "description" in data
        assert "inputSchema" in data
        assert "properties" in data["inputSchema"]

    def test_inspect_nonexistent_tool(self, runner):
        """Test inspecting a tool that doesn't exist."""
        result = runner.invoke(cli, ["inspect-tool", "nonexistent_tool"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestTestTool:
    """Tests for test-tool command."""

    def test_test_tool_without_args(self, runner):
        """Test executing a tool without arguments."""
        result = runner.invoke(cli, ["test-tool", "steering_status"])
        assert result.exit_code == 0
        assert "Testing tool: steering_status" in result.output
        assert "Arguments:" in result.output

    def test_test_tool_with_args(self, runner, tmp_path):
        """Test executing a tool with arguments."""
        args = json.dumps({"project_dir": str(tmp_path)})
        result = runner.invoke(cli, ["test-tool", "steering_status", "--args", args])
        assert result.exit_code == 0
        assert "Testing tool: steering_status" in result.output

    def test_test_tool_invalid_json(self, runner):
        """Test tool execution with invalid JSON arguments."""
        result = runner.invoke(cli, ["test-tool", "spec_init", "--args", "invalid json"])
        assert result.exit_code == 1
        assert "Invalid JSON" in result.output

    def test_test_nonexistent_tool(self, runner):
        """Test executing a tool that doesn't exist."""
        result = runner.invoke(cli, ["test-tool", "nonexistent_tool"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestValidateConfig:
    """Tests for validate-config command."""

    def test_validate_config_default(self, runner):
        """Test validating default configuration."""
        result = runner.invoke(cli, ["validate-config"])
        assert result.exit_code == 0
        assert "Validating configuration" in result.output
        assert "Configuration is valid" in result.output
        assert "Server Name:" in result.output
        assert "Log Level:" in result.output

    def test_validate_config_with_file(self, runner, tmp_path):
        """Test validating a specific config file."""
        config_file = tmp_path / ".cc-sdd.config.json"
        config_data = {
            "server_name": "test-server",
            "log_level": "DEBUG",
            "project_dir": str(tmp_path),
        }
        config_file.write_text(json.dumps(config_data))

        result = runner.invoke(cli, ["validate-config", "--config", str(config_file)])
        assert result.exit_code == 0
        assert "Configuration is valid" in result.output
        assert "test-server" in result.output
        assert "DEBUG" in result.output

    def test_validate_invalid_config(self, runner, tmp_path):
        """Test validating an invalid config file."""
        config_file = tmp_path / ".cc-sdd.config.json"
        config_file.write_text("invalid json")

        result = runner.invoke(cli, ["validate-config", "--config", str(config_file)])
        assert result.exit_code == 1
        assert "validation failed" in result.output

    def test_validate_missing_config(self, runner):
        """Test validating a non-existent config file."""
        result = runner.invoke(cli, ["validate-config", "--config", "/nonexistent/config.json"])
        # Exit code is 2 for Click parameter errors, 1 for validation errors
        assert result.exit_code in (1, 2)
        assert "validation failed" in result.output or "does not exist" in result.output


class TestStart:
    """Tests for start command."""

    @patch("cc_sdd_mcp.cli.asyncio.run")
    def test_start_default(self, mock_run, runner):
        """Test starting server with default configuration."""
        # Mock asyncio.run to prevent actual server start
        mock_run.return_value = None

        result = runner.invoke(cli, ["start"])
        assert result.exit_code == 0
        assert mock_run.called

    @patch("cc_sdd_mcp.cli.asyncio.run")
    def test_start_with_log_level(self, mock_run, runner):
        """Test starting server with custom log level."""
        mock_run.return_value = None

        result = runner.invoke(cli, ["start", "--log-level", "DEBUG"])
        assert result.exit_code == 0
        assert "DEBUG" in result.output

    @patch("cc_sdd_mcp.cli.asyncio.run")
    def test_start_with_config(self, mock_run, runner, tmp_path):
        """Test starting server with config file."""
        mock_run.return_value = None

        config_file = tmp_path / ".cc-sdd.config.json"
        config_data = {"server_name": "test-server", "log_level": "INFO"}
        config_file.write_text(json.dumps(config_data))

        result = runner.invoke(cli, ["start", "--config", str(config_file)])
        assert result.exit_code == 0
        assert "test-server" in result.output

    @patch("cc_sdd_mcp.cli.asyncio.run")
    def test_default_command_is_start(self, mock_run, runner):
        """Test that running CLI without command defaults to start."""
        mock_run.return_value = None

        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert mock_run.called


class TestHelp:
    """Tests for help functionality."""

    def test_main_help(self, runner):
        """Test main CLI help."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "cc-sdd MCP Server" in result.output
        assert "start" in result.output
        assert "list-tools" in result.output
        assert "inspect-tool" in result.output
        assert "test-tool" in result.output
        assert "validate-config" in result.output
        assert "version" in result.output

    def test_start_help(self, runner):
        """Test start command help."""
        result = runner.invoke(cli, ["start", "--help"])
        assert result.exit_code == 0
        assert "Start the MCP server" in result.output
        assert "--config" in result.output
        assert "--log-level" in result.output

    def test_list_tools_help(self, runner):
        """Test list-tools command help."""
        result = runner.invoke(cli, ["list-tools", "--help"])
        assert result.exit_code == 0
        assert "List all available MCP tools" in result.output
        assert "--json" in result.output

    def test_inspect_tool_help(self, runner):
        """Test inspect-tool command help."""
        result = runner.invoke(cli, ["inspect-tool", "--help"])
        assert result.exit_code == 0
        assert "Inspect a specific MCP tool" in result.output
        assert "--json" in result.output

    def test_test_tool_help(self, runner):
        """Test test-tool command help."""
        result = runner.invoke(cli, ["test-tool", "--help"])
        assert result.exit_code == 0
        assert "Test a tool with sample arguments" in result.output
        assert "--args" in result.output

    def test_validate_config_help(self, runner):
        """Test validate-config command help."""
        result = runner.invoke(cli, ["validate-config", "--help"])
        assert result.exit_code == 0
        assert "Validate server configuration" in result.output
        assert "--config" in result.output


class TestIntegration:
    """Integration tests for CLI."""

    def test_full_workflow(self, runner, tmp_path):
        """Test a complete workflow: validate, list, inspect, test."""
        # 1. Validate config
        result = runner.invoke(cli, ["validate-config"])
        assert result.exit_code == 0

        # 2. List tools
        result = runner.invoke(cli, ["list-tools"])
        assert result.exit_code == 0
        assert "steering_init" in result.output

        # 3. Inspect tool
        result = runner.invoke(cli, ["inspect-tool", "steering_init"])
        assert result.exit_code == 0

        # 4. Test tool
        args = json.dumps({"project_dir": str(tmp_path)})
        result = runner.invoke(cli, ["test-tool", "steering_init", "--args", args])
        assert result.exit_code == 0

    def test_json_output_workflow(self, runner):
        """Test workflow using JSON output."""
        # 1. List tools in JSON
        result = runner.invoke(cli, ["list-tools", "--json"])
        assert result.exit_code == 0
        tools = json.loads(result.output)
        assert len(tools["tools"]) > 0

        # 2. Inspect first tool in JSON
        tool_name = tools["tools"][0]["name"]
        result = runner.invoke(cli, ["inspect-tool", tool_name, "--json"])
        assert result.exit_code == 0
        tool_details = json.loads(result.output)
        assert tool_details["name"] == tool_name
