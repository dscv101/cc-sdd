"""Data models for validation operations."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationIssue(BaseModel):
    """Represents a single validation issue."""

    severity: ValidationSeverity = Field(..., description="Severity level of the issue")
    message: str = Field(..., description="Description of the issue")
    location: str | None = Field(
        None, description="Location where issue was found (file path, line number, etc.)"
    )
    suggestion: str | None = Field(None, description="Suggested fix or action")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "severity": "warning",
                "message": "Missing security consideration in design",
                "location": "design.md:45",
                "suggestion": "Add security considerations section",
            }
        }


class ValidationResult(BaseModel):
    """Result of a validation operation."""

    validation_type: str = Field(
        ..., description="Type of validation performed (gap, design, implementation)"
    )
    feature_name: str = Field(..., description="Feature being validated")
    passed: bool = Field(..., description="Whether validation passed (no errors or criticals)")
    issues: list[ValidationIssue] = Field(default_factory=list, description="List of issues found")
    summary: str = Field(..., description="Summary of validation results")
    validated_at: datetime = Field(default_factory=datetime.now, description="Validation timestamp")

    @property
    def error_count(self) -> int:
        """Count of error-level issues."""
        return sum(
            1
            for issue in self.issues
            if issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
        )

    @property
    def warning_count(self) -> int:
        """Count of warning-level issues."""
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.WARNING)

    @property
    def info_count(self) -> int:
        """Count of info-level issues."""
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.INFO)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "validation_type": "design",
                "feature_name": "user-authentication",
                "passed": True,
                "issues": [
                    {
                        "severity": "warning",
                        "message": "Consider adding rate limiting",
                        "location": "design.md:45",
                        "suggestion": "Add rate limiting to OAuth endpoints",
                    }
                ],
                "summary": "Design validation passed with 1 warning",
                "validated_at": "2025-01-01T12:00:00",
            }
        }


class GapAnalysisResult(ValidationResult):
    """Result of gap analysis between existing code and requirements."""

    existing_implementations: list[str] = Field(
        default_factory=list, description="Existing implementations found in codebase"
    )
    missing_requirements: list[str] = Field(
        default_factory=list, description="Requirements not implemented"
    )
    conflicting_implementations: list[str] = Field(
        default_factory=list, description="Implementations that conflict with requirements"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "validation_type": "gap",
                "feature_name": "user-authentication",
                "passed": False,
                "issues": [
                    {
                        "severity": "error",
                        "message": "OAuth provider configuration missing",
                        "location": "requirements.md:3",
                        "suggestion": "Implement OAuth configuration module",
                    }
                ],
                "summary": "Gap analysis found 3 missing requirements",
                "validated_at": "2025-01-01T12:00:00",
                "existing_implementations": ["Basic username/password authentication"],
                "missing_requirements": [
                    "OAuth Google integration",
                    "OAuth GitHub integration",
                    "Session management",
                ],
                "conflicting_implementations": ["Current auth uses sessions, design specifies JWT"],
            }
        }


class DesignValidationResult(ValidationResult):
    """Result of design document validation."""

    requirements_coverage: float = Field(
        ..., description="Percentage of requirements covered by design (0-100)"
    )
    missing_components: list[str] = Field(
        default_factory=list,
        description="Components mentioned in requirements but missing from design",
    )
    design_completeness: float = Field(
        ..., description="Completeness score of design document (0-100)"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "validation_type": "design",
                "feature_name": "user-authentication",
                "passed": True,
                "issues": [],
                "summary": "Design covers 95% of requirements",
                "validated_at": "2025-01-01T12:00:00",
                "requirements_coverage": 95.0,
                "missing_components": ["Session cleanup service"],
                "design_completeness": 90.0,
            }
        }


class ImplementationValidationResult(ValidationResult):
    """Result of implementation validation against tasks."""

    tasks_completed: int = Field(..., description="Number of tasks completed")
    tasks_total: int = Field(..., description="Total number of tasks")
    completion_percentage: float = Field(..., description="Percentage of tasks completed (0-100)")
    incomplete_tasks: list[str] = Field(
        default_factory=list, description="Task IDs that are incomplete"
    )
    test_coverage: float | None = Field(
        None, description="Code test coverage percentage if available"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "validation_type": "implementation",
                "feature_name": "user-authentication",
                "passed": False,
                "issues": [
                    {
                        "severity": "error",
                        "message": "Task 1.3 not implemented",
                        "location": "tasks.md:15",
                        "suggestion": "Implement OAuth callback handler",
                    }
                ],
                "summary": "Implementation 75% complete",
                "validated_at": "2025-01-01T12:00:00",
                "tasks_completed": 6,
                "tasks_total": 8,
                "completion_percentage": 75.0,
                "incomplete_tasks": ["1.3", "2.2"],
                "test_coverage": 82.5,
            }
        }
