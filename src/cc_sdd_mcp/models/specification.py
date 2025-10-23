"""Data models for feature specifications."""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class SpecPhase(str, Enum):
    """Phases in the spec-driven development lifecycle."""

    INITIALIZED = "initialized"
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    TASKS = "tasks"
    IMPLEMENTATION = "implementation"
    COMPLETED = "completed"


class SpecificationMetadata(BaseModel):
    """Metadata for a feature specification."""

    feature_name: str = Field(..., description="Name/identifier of the feature")
    description: str = Field(..., description="Brief description of the feature")
    current_phase: SpecPhase = Field(
        default=SpecPhase.INITIALIZED, description="Current phase in the workflow"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    approved_phases: list[SpecPhase] = Field(
        default_factory=list, description="Phases that have been approved"
    )

    @field_validator("feature_name")
    @classmethod
    def validate_feature_name(cls, v: str) -> str:
        """Validate feature name format."""
        if not v or not v.strip():
            raise ValueError("Feature name cannot be empty")
        # Replace spaces with hyphens, convert to lowercase
        return v.strip().lower().replace(" ", "-")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "feature_name": "user-authentication",
                "description": "Add OAuth authentication to the system",
                "current_phase": "requirements",
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:30:00",
                "approved_phases": ["initialized"],
            }
        }


class RequirementsDocument(BaseModel):
    """Schema for requirements.md document."""

    feature_name: str = Field(..., description="Feature identifier")
    functional_requirements: list[str] = Field(
        default_factory=list, description="List of functional requirements"
    )
    non_functional_requirements: list[str] = Field(
        default_factory=list, description="List of non-functional requirements"
    )
    constraints: list[str] = Field(
        default_factory=list, description="Known constraints or limitations"
    )
    acceptance_criteria: list[str] = Field(
        default_factory=list, description="Acceptance criteria for the feature"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "feature_name": "user-authentication",
                "functional_requirements": [
                    "Users must be able to log in with OAuth providers",
                    "Support Google and GitHub OAuth",
                ],
                "non_functional_requirements": [
                    "Authentication must complete within 2 seconds",
                    "Must support 10,000 concurrent users",
                ],
                "constraints": [
                    "Must integrate with existing user database",
                    "Cannot modify existing API endpoints",
                ],
                "acceptance_criteria": [
                    "User can successfully authenticate with Google",
                    "User session persists across page reloads",
                ],
                "created_at": "2025-01-01T12:00:00",
            }
        }


class DesignDocument(BaseModel):
    """Schema for design.md document."""

    feature_name: str = Field(..., description="Feature identifier")
    architecture_overview: str = Field(..., description="High-level architecture description")
    components: list[dict[str, str]] = Field(
        default_factory=list, description="List of components with descriptions"
    )
    data_models: list[dict[str, str]] = Field(
        default_factory=list, description="Data models and schemas"
    )
    api_endpoints: list[dict[str, str]] = Field(
        default_factory=list, description="API endpoints if applicable"
    )
    dependencies: list[str] = Field(default_factory=list, description="External dependencies")
    security_considerations: list[str] = Field(
        default_factory=list, description="Security considerations"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "feature_name": "user-authentication",
                "architecture_overview": "OAuth 2.0 flow with JWT tokens",
                "components": [
                    {"name": "AuthController", "description": "Handles OAuth flow"},
                    {"name": "TokenService", "description": "Manages JWT tokens"},
                ],
                "data_models": [
                    {"name": "User", "description": "User account model"},
                    {"name": "OAuthToken", "description": "OAuth token storage"},
                ],
                "api_endpoints": [
                    {"path": "/auth/oauth/google", "method": "GET"},
                    {"path": "/auth/callback", "method": "POST"},
                ],
                "dependencies": ["passport-js", "jsonwebtoken"],
                "security_considerations": [
                    "Store OAuth secrets securely",
                    "Validate redirect URIs",
                ],
                "created_at": "2025-01-01T12:00:00",
            }
        }


class TaskItem(BaseModel):
    """Individual task in a task breakdown."""

    task_id: str = Field(..., description="Task identifier (e.g., 1.1, 2.3)")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    estimated_hours: float | None = Field(None, description="Estimated hours to complete")
    dependencies: list[str] = Field(
        default_factory=list, description="Task IDs this task depends on"
    )
    completed: bool = Field(default=False, description="Whether task is completed")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "task_id": "1.1",
                "title": "Set up OAuth configuration",
                "description": "Configure OAuth client IDs and secrets",
                "estimated_hours": 2.0,
                "dependencies": [],
                "completed": False,
            }
        }


class TasksDocument(BaseModel):
    """Schema for tasks.md document."""

    feature_name: str = Field(..., description="Feature identifier")
    tasks: list[TaskItem] = Field(default_factory=list, description="List of tasks")
    total_estimated_hours: float | None = Field(None, description="Total estimated hours")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "feature_name": "user-authentication",
                "tasks": [
                    {
                        "task_id": "1.1",
                        "title": "Set up OAuth configuration",
                        "description": "Configure OAuth client IDs",
                        "estimated_hours": 2.0,
                        "dependencies": [],
                        "completed": False,
                    }
                ],
                "total_estimated_hours": 16.0,
                "created_at": "2025-01-01T12:00:00",
            }
        }


class SpecificationStatus(BaseModel):
    """Complete status of a specification."""

    feature_name: str = Field(..., description="Feature identifier")
    spec_dir: Path = Field(..., description="Path to spec directory")
    metadata: SpecificationMetadata = Field(..., description="Specification metadata")
    files_present: dict[str, bool] = Field(
        ..., description="Which files are present (requirements.md, design.md, etc.)"
    )
    can_proceed_to_next_phase: bool = Field(..., description="Whether can move to next phase")
    next_recommended_action: str | None = Field(None, description="Recommended next action")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "feature_name": "user-authentication",
                "spec_dir": ".kiro/specs/user-authentication",
                "metadata": {
                    "feature_name": "user-authentication",
                    "description": "Add OAuth authentication",
                    "current_phase": "requirements",
                    "created_at": "2025-01-01T12:00:00",
                    "updated_at": "2025-01-01T12:30:00",
                    "approved_phases": ["initialized"],
                },
                "files_present": {
                    "spec.json": True,
                    "requirements.md": True,
                    "design.md": False,
                    "tasks.md": False,
                },
                "can_proceed_to_next_phase": True,
                "next_recommended_action": "Run spec_design to generate design document",
            }
        }
