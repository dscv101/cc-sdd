"""Integration tests for validation workflows."""

import json

import pytest

from cc_sdd_mcp.workflows.validation_workflow import ValidationWorkflow


class TestValidationWorkflowIntegration:
    """Integration tests for validation workflows."""

    @pytest.mark.asyncio
    async def test_gap_analysis_without_requirements(self, temp_project_with_kiro):
        """Test gap analysis when requirements don't exist."""
        workflow = ValidationWorkflow(temp_project_with_kiro)

        # Create spec without requirements
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "missing-req"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "missing-req",
            "description": "Test feature",
            "current_phase": "initialized",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": [],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))

        # Perform gap analysis
        result = await workflow.validate_gap("missing-req")
        assert result.passed is False
        assert result.feature_name == "missing-req"
        assert len(result.issues) > 0
        assert any("not found" in issue.message.lower() for issue in result.issues)

    @pytest.mark.asyncio
    async def test_gap_analysis_with_requirements(self, temp_project_with_kiro):
        """Test gap analysis with requirements present."""
        workflow = ValidationWorkflow(temp_project_with_kiro)

        # Create spec with requirements
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "has-req"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "has-req",
            "description": "Test feature",
            "current_phase": "requirements",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": [],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))
        (spec_dir / "requirements.md").write_text("# Requirements\n- Feature 1\n- Feature 2")

        # Perform gap analysis
        result = await workflow.validate_gap("has-req")
        assert result.feature_name == "has-req"
        assert result.validation_type == "gap_analysis"
        assert isinstance(result.existing_implementations, list)
        assert isinstance(result.missing_requirements, list)

    @pytest.mark.asyncio
    async def test_design_validation_complete(self, temp_project_with_kiro):
        """Test design validation with all documents present."""
        workflow = ValidationWorkflow(temp_project_with_kiro)

        # Create spec with requirements and design
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "complete-design"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "complete-design",
            "description": "Test feature",
            "current_phase": "design",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": ["requirements"],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))
        (spec_dir / "requirements.md").write_text("# Requirements\n- Auth required")

        design_content = """# Design

## Architecture Overview
Microservices architecture

## Components
- Frontend service
- Backend API

## Data Models
- User model
- Session model

## API Endpoints
- POST /api/auth

## Security Considerations
- JWT tokens
- Rate limiting
"""
        (spec_dir / "design.md").write_text(design_content)

        # Validate design
        result = await workflow.validate_design("complete-design")
        assert result.feature_name == "complete-design"
        assert result.validation_type == "design_validation"
        # With all sections present, should have fewer missing elements
        assert len(result.missing_components) < 3
        assert result.design_completeness >= 0.0
        assert result.requirements_coverage >= 0.0

    @pytest.mark.asyncio
    async def test_implementation_validation(self, temp_project_with_kiro):
        """Test implementation validation."""
        workflow = ValidationWorkflow(temp_project_with_kiro)

        # Create spec with tasks
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "impl-test"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "impl-test",
            "description": "Test feature",
            "current_phase": "tasks",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": ["requirements", "design"],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))
        (spec_dir / "tasks.md").write_text("# Tasks\n- 1.1 Setup\n- 1.2 Implement")

        # Validate implementation
        result = await workflow.validate_implementation("impl-test")
        assert result.feature_name == "impl-test"
        assert result.validation_type == "implementation_validation"
        assert isinstance(result.tasks_completed, int)
        assert isinstance(result.tasks_total, int)
        assert isinstance(result.incomplete_tasks, list)

    @pytest.mark.asyncio
    async def test_validation_error_handling(self, temp_project_with_kiro):
        """Test validation error handling for non-existent specs."""
        workflow = ValidationWorkflow(temp_project_with_kiro)

        # Try to validate non-existent spec
        with pytest.raises(FileNotFoundError):
            await workflow.validate_gap("non-existent")

        with pytest.raises(FileNotFoundError):
            await workflow.validate_design("non-existent")

        with pytest.raises(FileNotFoundError):
            await workflow.validate_implementation("non-existent")
