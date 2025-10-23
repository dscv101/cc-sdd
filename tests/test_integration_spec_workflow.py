"""Integration tests for specification workflow."""

import json

import pytest

from cc_sdd_mcp.workflows.spec_workflow import SpecWorkflow


class TestSpecWorkflowIntegration:
    """Integration tests for complete spec workflow."""

    @pytest.mark.asyncio
    async def test_complete_spec_workflow(self, temp_project_with_kiro):
        """Test complete workflow from init to tasks generation."""
        workflow = SpecWorkflow(temp_project_with_kiro)

        # Initialize spec metadata manually
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "user-auth"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "user-auth",
            "description": "Add user authentication",
            "current_phase": "initialized",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": [],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))

        # Generate requirements
        result = await workflow.generate_requirements("user-auth", auto_approve=True)
        assert result["success"] is True
        assert result["current_phase"] == "requirements"
        assert (spec_dir / "requirements.md").exists()

        # Generate design
        result = await workflow.generate_design("user-auth", auto_approve=True)
        assert result["success"] is True
        assert result["current_phase"] == "design"
        assert (spec_dir / "design.md").exists()

        # Generate tasks
        result = await workflow.generate_tasks("user-auth", auto_approve=True)
        assert result["success"] is True
        assert result["current_phase"] == "tasks"
        assert (spec_dir / "tasks.md").exists()
        assert result["total_tasks"] > 0

    @pytest.mark.asyncio
    async def test_spec_status(self, temp_project_with_kiro):
        """Test getting spec status."""
        workflow = SpecWorkflow(temp_project_with_kiro)

        # Create a spec
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "feature-x"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "feature-x",
            "description": "Test feature",
            "current_phase": "requirements",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": ["requirements"],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))
        (spec_dir / "requirements.md").write_text("# Requirements")

        # Get status
        status = await workflow.get_spec_status("feature-x")
        assert status["feature_name"] == "feature-x"
        assert status["current_phase"] == "requirements"
        assert "requirements" in status["approved_phases"]
        assert status["files"]["requirements"] is True
        assert status["files"]["design"] is False

    @pytest.mark.asyncio
    async def test_phase_gate_without_approval(self, temp_project_with_kiro):
        """Test that phase gates block progression without approval."""
        workflow = SpecWorkflow(temp_project_with_kiro)

        # Create spec in requirements phase without approval
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "gated-feature"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "gated-feature",
            "description": "Test gating",
            "current_phase": "requirements",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": [],  # No approval
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))
        (spec_dir / "requirements.md").write_text("# Requirements")

        # Try to generate design without approval
        result = await workflow.generate_design("gated-feature", auto_approve=False)
        assert result["success"] is False
        assert "must be approved" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_requirements_generation_with_steering(self, temp_project_with_kiro):
        """Test requirements generation loads steering context."""
        workflow = SpecWorkflow(temp_project_with_kiro)

        # Add steering documents
        steering_dir = temp_project_with_kiro / ".kiro" / "steering"
        (steering_dir / "product.md").write_text("# Product Context\nB2B SaaS platform")
        (steering_dir / "tech.md").write_text("# Tech Stack\nPython, FastAPI")

        # Create spec
        spec_dir = temp_project_with_kiro / ".kiro" / "specs" / "api-feature"
        spec_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "feature_name": "api-feature",
            "description": "New API endpoint",
            "current_phase": "initialized",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "approved_phases": [],
        }
        (spec_dir / "metadata.json").write_text(json.dumps(metadata))

        # Generate requirements
        result = await workflow.generate_requirements("api-feature")
        assert result["success"] is True

        # Check requirements file exists and has content
        req_file = spec_dir / "requirements.md"
        assert req_file.exists()
        content = req_file.read_text()
        assert "api-feature" in content.lower()
        assert "Functional Requirements" in content
