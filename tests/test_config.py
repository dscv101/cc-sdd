"""Tests for configuration system."""

import json

import pytest

from cc_sdd_mcp.models.config import ServerConfig


class TestServerConfig:
    """Test the ServerConfig model."""

    def test_server_config_defaults(self):
        """Test server config with default values."""
        config = ServerConfig()
        assert config.server_name == "cc-sdd-mcp"
        assert config.server_version == "0.1.0"
        assert config.log_level == "INFO"
        assert config.kiro_dir == ".kiro"
        assert config.default_language == "en"
        assert config.template_cache_enabled is True
        assert config.strict_phase_gates is True

    def test_server_config_custom_values(self):
        """Test server config with custom values."""
        config = ServerConfig(
            server_name="custom-server",
            log_level="DEBUG",
            kiro_dir=".custom_kiro",
            strict_phase_gates=False,
        )
        assert config.server_name == "custom-server"
        assert config.log_level == "DEBUG"
        assert config.kiro_dir == ".custom_kiro"
        assert config.strict_phase_gates is False

    def test_from_file(self, tmp_path):
        """Test loading config from JSON file."""
        config_file = tmp_path / "config.json"
        config_data = {
            "server_name": "test-server",
            "log_level": "WARNING",
            "kiro_dir": ".test_kiro",
        }
        config_file.write_text(json.dumps(config_data))

        config = ServerConfig.from_file(config_file)
        assert config.server_name == "test-server"
        assert config.log_level == "WARNING"
        assert config.kiro_dir == ".test_kiro"

    def test_from_file_not_found(self, tmp_path):
        """Test loading config from non-existent file."""
        config_file = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            ServerConfig.from_file(config_file)

    def test_from_file_invalid_json(self, tmp_path):
        """Test loading config from invalid JSON file."""
        config_file = tmp_path / "invalid.json"
        config_file.write_text("{ invalid json }")

        with pytest.raises(ValueError):
            ServerConfig.from_file(config_file)

    def test_from_env(self, monkeypatch):
        """Test loading config from environment variables."""
        monkeypatch.setenv("CC_SDD_SERVER_NAME", "env-server")
        monkeypatch.setenv("CC_SDD_LOG_LEVEL", "ERROR")
        monkeypatch.setenv("CC_SDD_KIRO_DIR", ".env_kiro")
        monkeypatch.setenv("CC_SDD_STRICT_PHASE_GATES", "false")

        config = ServerConfig.from_env()
        assert config.server_name == "env-server"
        assert config.log_level == "ERROR"
        assert config.kiro_dir == ".env_kiro"
        assert config.strict_phase_gates is False

    def test_from_env_boolean_conversion(self, monkeypatch):
        """Test boolean conversion from environment variables."""
        monkeypatch.setenv("CC_SDD_TEMPLATE_CACHE_ENABLED", "true")
        monkeypatch.setenv("CC_SDD_AUTO_CREATE_STEERING", "1")
        monkeypatch.setenv("CC_SDD_STRICT_PHASE_GATES", "yes")

        config = ServerConfig.from_env()
        assert config.template_cache_enabled is True
        assert config.auto_create_steering is True
        assert config.strict_phase_gates is True

        monkeypatch.setenv("CC_SDD_TEMPLATE_CACHE_ENABLED", "false")
        monkeypatch.setenv("CC_SDD_AUTO_CREATE_STEERING", "0")
        monkeypatch.setenv("CC_SDD_STRICT_PHASE_GATES", "no")

        config = ServerConfig.from_env()
        assert config.template_cache_enabled is False
        assert config.auto_create_steering is False
        assert config.strict_phase_gates is False

    def test_load_priority(self, tmp_path, monkeypatch):
        """Test config loading priority."""
        # Create a local config file
        local_config = tmp_path / ".cc-sdd.config.json"
        local_config.write_text(json.dumps({"server_name": "local-server"}))

        # Set environment variables
        monkeypatch.setenv("CC_SDD_SERVER_NAME", "env-server")

        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        # Load should prioritize local file over env
        config = ServerConfig.load()
        assert config.server_name == "local-server"

    def test_load_with_provided_path(self, tmp_path):
        """Test loading config with provided path."""
        config_file = tmp_path / "custom.json"
        config_file.write_text(json.dumps({"server_name": "custom-server"}))

        config = ServerConfig.load(config_path=config_file)
        assert config.server_name == "custom-server"

    def test_load_env_config_path(self, tmp_path, monkeypatch):
        """Test loading config from CC_SDD_CONFIG_PATH env var."""
        config_file = tmp_path / "env_config.json"
        config_file.write_text(json.dumps({"server_name": "env-path-server"}))

        monkeypatch.setenv("CC_SDD_CONFIG_PATH", str(config_file))

        config = ServerConfig.load()
        assert config.server_name == "env-path-server"

    def test_save(self, tmp_path):
        """Test saving config to file."""
        config = ServerConfig(server_name="save-test", log_level="DEBUG")
        config_file = tmp_path / "save_test.json"

        config.save(config_file)

        # Load and verify
        assert config_file.exists()
        saved_data = json.loads(config_file.read_text())
        assert saved_data["server_name"] == "save-test"
        assert saved_data["log_level"] == "DEBUG"

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = ServerConfig(server_name="dict-test", log_level="INFO")
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert config_dict["server_name"] == "dict-test"
        assert config_dict["log_level"] == "INFO"
        assert isinstance(config_dict["project_dir"], str)  # Path should be converted to string


class TestServerConfigIntegration:
    """Integration tests for server configuration."""

    def test_config_roundtrip(self, tmp_path):
        """Test saving and loading config maintains values."""
        original = ServerConfig(
            server_name="roundtrip-test",
            log_level="WARNING",
            kiro_dir=".test",
            strict_phase_gates=False,
        )

        config_file = tmp_path / "roundtrip.json"
        original.save(config_file)

        loaded = ServerConfig.from_file(config_file)

        assert loaded.server_name == original.server_name
        assert loaded.log_level == original.log_level
        assert loaded.kiro_dir == original.kiro_dir
        assert loaded.strict_phase_gates == original.strict_phase_gates

    def test_partial_config_file(self, tmp_path):
        """Test loading config file with partial values."""
        config_file = tmp_path / "partial.json"
        config_file.write_text(json.dumps({"log_level": "DEBUG"}))

        config = ServerConfig.from_file(config_file)

        # Specified value
        assert config.log_level == "DEBUG"
        # Default values
        assert config.server_name == "cc-sdd-mcp"
        assert config.strict_phase_gates is True
