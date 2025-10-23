"""Configuration models for the MCP server."""

import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """Configuration for the MCP server."""

    # Server settings
    server_name: str = Field(default="cc-sdd-mcp", description="Name of the MCP server")
    server_version: str = Field(default="0.1.0", description="Server version")
    log_level: str = Field(
        default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    # Project settings
    project_dir: Path = Field(default_factory=lambda: Path("."), description="Project directory")
    kiro_dir: str = Field(default=".kiro", description="Kiro directory name")

    # Template settings
    default_language: str = Field(default="en", description="Default language for templates")
    template_cache_enabled: bool = Field(
        default=True, description="Enable template caching for performance"
    )

    # Steering settings
    auto_create_steering: bool = Field(
        default=False, description="Auto-create steering documents if missing"
    )

    # Validation settings
    strict_phase_gates: bool = Field(
        default=True, description="Enforce strict phase gate approval requirements"
    )

    @classmethod
    def from_file(cls, config_path: Path | str) -> "ServerConfig":
        """Load configuration from a JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            ServerConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            config_data = json.loads(config_path.read_text())
            return cls(**config_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to load config: {e}") from e

    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Load configuration from environment variables.

        Environment variables should be prefixed with CC_SDD_
        Example: CC_SDD_LOG_LEVEL=DEBUG

        Returns:
            ServerConfig instance with values from environment
        """
        env_config: dict[str, Any] = {}

        # Map environment variables to config fields
        env_mapping = {
            "CC_SDD_SERVER_NAME": "server_name",
            "CC_SDD_SERVER_VERSION": "server_version",
            "CC_SDD_LOG_LEVEL": "log_level",
            "CC_SDD_PROJECT_DIR": "project_dir",
            "CC_SDD_KIRO_DIR": "kiro_dir",
            "CC_SDD_DEFAULT_LANGUAGE": "default_language",
            "CC_SDD_TEMPLATE_CACHE_ENABLED": "template_cache_enabled",
            "CC_SDD_AUTO_CREATE_STEERING": "auto_create_steering",
            "CC_SDD_STRICT_PHASE_GATES": "strict_phase_gates",
        }

        for env_var, field_name in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Handle boolean conversion
                if field_name in [
                    "template_cache_enabled",
                    "auto_create_steering",
                    "strict_phase_gates",
                ]:
                    env_config[field_name] = value.lower() in ("true", "1", "yes")
                # Handle Path conversion
                elif field_name == "project_dir":
                    env_config[field_name] = Path(value)
                else:
                    env_config[field_name] = value

        return cls(**env_config)

    @classmethod
    def load(cls, config_path: Path | str | None = None) -> "ServerConfig":
        """Load configuration with automatic detection.

        Tries the following in order:
        1. Load from provided config_path
        2. Load from CC_SDD_CONFIG_PATH environment variable
        3. Load from .cc-sdd.config.json in current directory
        4. Load from environment variables
        5. Use defaults

        Args:
            config_path: Optional path to configuration file

        Returns:
            ServerConfig instance
        """
        # Try provided path
        if config_path:
            try:
                return cls.from_file(config_path)
            except FileNotFoundError:
                pass  # Fall through to next option

        # Try environment variable path
        env_config_path = os.getenv("CC_SDD_CONFIG_PATH")
        if env_config_path:
            try:
                return cls.from_file(env_config_path)
            except FileNotFoundError:
                pass

        # Try local config file
        local_config = Path(".cc-sdd.config.json")
        if local_config.exists():
            try:
                return cls.from_file(local_config)
            except (FileNotFoundError, ValueError):
                pass

        # Try environment variables
        try:
            return cls.from_env()
        except Exception:
            pass

        # Return defaults
        return cls()

    def save(self, config_path: Path | str) -> None:
        """Save configuration to a JSON file.

        Args:
            config_path: Path where to save the configuration
        """
        config_path = Path(config_path)

        # Convert to dict and handle Path serialization
        config_dict = self.model_dump()
        config_dict["project_dir"] = str(config_dict["project_dir"])

        config_path.write_text(json.dumps(config_dict, indent=2))

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Configuration as dictionary
        """
        config_dict = self.model_dump()
        config_dict["project_dir"] = str(config_dict["project_dir"])
        return config_dict
