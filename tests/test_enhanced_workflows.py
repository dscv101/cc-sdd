"""Tests for enhanced template-based workflows."""

import pytest
from pathlib import Path
from cc_sdd_mcp.workflows.spec_workflow import SpecWorkflow
from cc_sdd_mcp.models.specification import SpecPhase


@pytest.fixture
def workflow(tmp_path):
    """Create a spec workflow for testing."""
    return SpecWorkflow(project_dir=tmp_path)


@pytest.mark.asyncio
async def test_generate_requirements_with_enhanced_template(workflow, tmp_path):
    """Test requirements generation uses enhanced EARS template."""
    # Initialize spec
    result = await workflow.initialize_spec(
        feature_name="test-feature",
        description="Test feature for enhanced template"
    )
    assert result["success"]
    
    # Generate requirements
    result = await workflow.generate_requirements("test-feature", auto_approve=True)
    assert result["success"]
    assert "enhanced EARS template" in result["message"]
    
    # Verify file was created with template content
    req_file = Path(result["requirements_file"])
    assert req_file.exists()
    
    content = req_file.read_text()
    # Check for EARS notation markers
    assert "Document Metadata" in content or "Version" in content
    assert len(content) > 500  # Enhanced template should produce substantial content


@pytest.mark.asyncio
async def test_generate_design_with_enhanced_template(workflow, tmp_path):
    """Test design generation uses enhanced template."""
    # Initialize and generate requirements first
    await workflow.initialize_spec(
        feature_name="test-design",
        description="Test design with enhanced template"
    )
    await workflow.generate_requirements("test-design", auto_approve=True)
    
    # Generate design
    result = await workflow.generate_design("test-design", auto_approve=True)
    assert result["success"]
    assert "enhanced template" in result["message"]
    
    # Verify file was created with template content
    design_file = Path(result["design_file"])
    assert design_file.exists()
    
    content = design_file.read_text()
    # Check for template structure
    assert "Design Specification" in content or "Architecture" in content
    assert len(content) > 500  # Enhanced template should produce substantial content


@pytest.mark.asyncio
async def test_generate_tasks_with_enhanced_template(workflow, tmp_path):
    """Test tasks generation uses enhanced template."""
    # Initialize and generate requirements and design first
    await workflow.initialize_spec(
        feature_name="test-tasks",
        description="Test tasks with enhanced template"
    )
    await workflow.generate_requirements("test-tasks", auto_approve=True)
    await workflow.generate_design("test-tasks", auto_approve=True)
    
    # Generate tasks
    result = await workflow.generate_tasks("test-tasks", auto_approve=True)
    assert result["success"]
    assert "enhanced template" in result["message"]
    
    # Verify file was created with template content
    tasks_file = Path(result["tasks_file"])
    assert tasks_file.exists()
    
    content = tasks_file.read_text()
    # Check for template structure
    assert "Implementation Task Plan" in content or "Task Structure" in content
    assert len(content) > 500  # Enhanced template should produce substantial content


@pytest.mark.asyncio
async def test_requirements_context_builder(workflow):
    """Test requirements context builder provides all necessary variables."""
    metadata = await workflow._load_metadata("test-feature")
    context = workflow._build_requirements_context(metadata)
    
    # Check key metadata fields
    assert "VERSION" in context
    assert "STATUS" in context
    assert "AUTHORS" in context
    assert "LAST_UPDATED" in context
    
    # Check EARS-style fields
    assert "SPECIFIC_ROLE" in context
    assert "CAPABILITY" in context
    assert "WHY_THIS_REQUIREMENT" in context
    
    # Check constraint fields
    assert "CONSTRAINT_1" in context
    assert "WHY_THIS_CONSTRAINT" in context


@pytest.mark.asyncio
async def test_design_context_builder(workflow):
    """Test design context builder provides all necessary variables."""
    metadata = await workflow._load_metadata("test-feature")
    context = workflow._build_design_context(metadata)
    
    # Check key metadata fields
    assert "VERSION" in context
    assert "STATUS" in context
    assert "REQ_VERSION" in context
    
    # Check architecture decision fields
    assert "DECISION_1" in context
    assert "REASONING_1" in context
    assert "REASON" in context
    
    # Check risk management fields
    assert "RISK" in context
    assert "RISK_1" in context
    assert "MITIGATION_STRATEGY" in context


@pytest.mark.asyncio
async def test_tasks_context_builder(workflow):
    """Test tasks context builder provides all necessary variables."""
    metadata = await workflow._load_metadata("test-feature")
    context = workflow._build_tasks_context(metadata)
    
    # Check key metadata fields
    assert "VERSION" in context
    assert "STATUS" in context
    assert "REQ_VERSION" in context
    assert "DESIGN_VERSION" in context
    
    # Check estimation fields
    assert "TOTAL_ESTIMATE" in context
    assert "PHASE_1_ESTIMATE" in context
    assert "PHASE_2_ESTIMATE" in context
    
    # Check task detail fields
    assert "TASK_ID" in context
    assert "TASK_DESCRIPTION" in context
    assert "WHY_THIS_TASK" in context
    
    # Check testing fields
    assert "TEST_SCOPE" in context
    assert "COVERAGE" in context


@pytest.mark.asyncio
async def test_full_workflow_with_enhanced_templates(workflow):
    """Test complete workflow from initialization to tasks using enhanced templates."""
    feature_name = "complete-workflow-test"
    
    # Step 1: Initialize
    result = await workflow.initialize_spec(
        feature_name=feature_name,
        description="Complete workflow test"
    )
    assert result["success"]
    assert result["current_phase"] == SpecPhase.INITIALIZED.value
    
    # Step 2: Generate requirements
    result = await workflow.generate_requirements(feature_name, auto_approve=True)
    assert result["success"]
    assert "enhanced EARS template" in result["message"]
    assert result["current_phase"] == SpecPhase.REQUIREMENTS.value
    
    # Step 3: Generate design
    result = await workflow.generate_design(feature_name, auto_approve=True)
    assert result["success"]
    assert "enhanced template" in result["message"]
    assert result["current_phase"] == SpecPhase.DESIGN.value
    
    # Step 4: Generate tasks
    result = await workflow.generate_tasks(feature_name, auto_approve=True)
    assert result["success"]
    assert "enhanced template" in result["message"]
    assert result["current_phase"] == SpecPhase.TASKS.value
    
    # Verify all files exist
    spec_dir = workflow._get_spec_dir(feature_name)
    assert (spec_dir / "requirements.md").exists()
    assert (spec_dir / "design.md").exists()
    assert (spec_dir / "tasks.md").exists()


@pytest.mark.asyncio
async def test_template_rendering_error_handling(workflow, tmp_path):
    """Test proper error handling when template rendering fails."""
    # Initialize spec
    await workflow.initialize_spec(
        feature_name="error-test",
        description="Test error handling"
    )
    
    # Mock template loader to return invalid template
    original_load = workflow.template_loader.load_spec_template
    
    def mock_load_invalid(*args, **kwargs):
        return "{{ UNCLOSED_TAG"  # Invalid Jinja2 syntax
    
    workflow.template_loader.load_spec_template = mock_load_invalid
    
    # Attempt to generate requirements
    result = await workflow.generate_requirements("error-test")
    assert not result["success"]
    assert "rendering failed" in result["error"].lower()
    
    # Restore original loader
    workflow.template_loader.load_spec_template = original_load


@pytest.mark.asyncio
async def test_template_missing_error_handling(workflow):
    """Test proper error handling when template file is missing."""
    # Initialize spec
    await workflow.initialize_spec(
        feature_name="missing-test",
        description="Test missing template"
    )
    
    # Mock template loader to return None (template not found)
    original_load = workflow.template_loader.load_spec_template
    workflow.template_loader.load_spec_template = lambda *args, **kwargs: None
    
    # Attempt to generate requirements
    result = await workflow.generate_requirements("missing-test")
    assert not result["success"]
    assert "template not found" in result["error"].lower()
    
    # Restore original loader
    workflow.template_loader.load_spec_template = original_load


@pytest.mark.asyncio
async def test_context_variables_use_metadata(workflow):
    """Test that context variables properly use metadata values."""
    # Initialize with specific description
    description = "Very specific test description for validation"
    await workflow.initialize_spec(
        feature_name="metadata-test",
        description=description
    )
    
    metadata = workflow._load_metadata("metadata-test")
    
    # Build contexts
    req_context = workflow._build_requirements_context(metadata)
    design_context = workflow._build_design_context(metadata)
    tasks_context = workflow._build_tasks_context(metadata)
    
    # Verify metadata values are used
    assert metadata.feature_name in req_context["NAME"]
    assert metadata.feature_name in design_context["NAME"]
    
    # Verify description is incorporated
    assert description in req_context["BUSINESS_PROBLEM"]
    assert metadata.feature_name in design_context["IMPACT"]

