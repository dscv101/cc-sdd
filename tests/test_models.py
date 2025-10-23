"""Unit tests for data models."""

from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from cc_sdd_mcp.models.specification import (
    SpecificationMetadata,
    SpecPhase,
    TaskItem,
)
from cc_sdd_mcp.models.steering import (
    SteeringConfig,
    SteeringDocument,
    SteeringFileType,
)
from cc_sdd_mcp.models.validation import (
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)


class TestSteeringModels:
    """Tests for steering data models."""

    def test_steering_document_creation(self):
        """Test creating a SteeringDocument."""
        doc = SteeringDocument(
            file_type=SteeringFileType.PRODUCT,
            file_path=Path(".kiro/steering/product.md"),
            content="# Product Context\n\nTest content",
        )
        assert doc.file_type == SteeringFileType.PRODUCT
        assert doc.content == "# Product Context\n\nTest content"
        assert isinstance(doc.last_modified, datetime)

    def test_steering_document_empty_content_fails(self):
        """Test that empty content fails validation."""
        with pytest.raises(ValidationError):
            SteeringDocument(
                file_type=SteeringFileType.PRODUCT,
                file_path=Path(".kiro/steering/product.md"),
                content="",
            )

    def test_steering_config_defaults(self):
        """Test SteeringConfig default values."""
        config = SteeringConfig()
        assert config.kiro_dir == Path(".kiro")
        assert config.steering_dir == Path(".kiro/steering")
        assert config.language == "en"
        assert len(config.default_files) == 3

    def test_steering_config_invalid_language(self):
        """Test that invalid language fails validation."""
        with pytest.raises(ValidationError):
            SteeringConfig(language="invalid")


class TestSpecificationModels:
    """Tests for specification data models."""

    def test_specification_metadata_creation(self):
        """Test creating SpecificationMetadata."""
        metadata = SpecificationMetadata(
            feature_name="user-authentication",
            description="Add OAuth authentication",
        )
        assert metadata.feature_name == "user-authentication"
        assert metadata.current_phase == SpecPhase.INITIALIZED
        assert isinstance(metadata.created_at, datetime)

    def test_feature_name_normalization(self):
        """Test that feature names are normalized."""
        metadata = SpecificationMetadata(
            feature_name="User Authentication",
            description="Test",
        )
        assert metadata.feature_name == "user-authentication"

    def test_task_item_creation(self):
        """Test creating a TaskItem."""
        task = TaskItem(
            task_id="1.1",
            title="Setup OAuth",
            description="Configure OAuth providers",
            estimated_hours=2.0,
        )
        assert task.task_id == "1.1"
        assert task.completed is False
        assert task.estimated_hours == 2.0


class TestValidationModels:
    """Tests for validation data models."""

    def test_validation_issue_creation(self):
        """Test creating a ValidationIssue."""
        issue = ValidationIssue(
            severity=ValidationSeverity.WARNING,
            message="Missing security consideration",
            location="design.md:45",
            suggestion="Add security section",
        )
        assert issue.severity == ValidationSeverity.WARNING
        assert issue.message == "Missing security consideration"

    def test_validation_result_counts(self):
        """Test validation result issue counts."""
        result = ValidationResult(
            validation_type="design",
            feature_name="test-feature",
            passed=True,
            issues=[
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Error 1",
                ),
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Warning 1",
                ),
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    message="Info 1",
                ),
            ],
            summary="Test validation",
        )
        assert result.error_count == 1
        assert result.warning_count == 1
        assert result.info_count == 1
