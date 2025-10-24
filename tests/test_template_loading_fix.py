"""Test that template loading correctly accesses enhanced templates."""

import pytest
from pathlib import Path

from cc_sdd_mcp.utils.templates import TemplateLoader


class TestEnhancedTemplateLoading:
    """Test the fixed template loading for enhanced EARS templates."""

    def test_requirements_template_loads(self):
        """Test that requirements template loads from correct path."""
        loader = TemplateLoader()
        template = loader.load_spec_template("requirements", "requirements")
        
        assert template is not None, "Requirements template should load"
        assert len(template) > 1000, "Requirements template should have substantial content"
        assert "EARS" in template, "Requirements template should mention EARS"
        assert "Intent" in template or "intent" in template, "Requirements template should include Intent sections"

    def test_design_template_loads(self):
        """Test that design template loads from correct path."""
        loader = TemplateLoader()
        template = loader.load_spec_template("design", "design")
        
        assert template is not None, "Design template should load"
        assert len(template) > 1000, "Design template should have substantial content"
        assert "Rationale" in template or "rationale" in template, "Design template should include rationale sections"

    def test_tasks_template_loads(self):
        """Test that tasks template loads from correct path."""
        loader = TemplateLoader()
        template = loader.load_spec_template("tasks", "tasks")
        
        assert template is not None, "Tasks template should load"
        assert len(template) > 1000, "Tasks template should have substantial content"
        assert "Traceability" in template or "traceability" in template, "Tasks template should include traceability"

    def test_template_path_resolution(self):
        """Test that template path resolves to correct location."""
        loader = TemplateLoader()
        
        # Test the internal path resolution
        expected_path = loader.templates_dir / "shared" / "settings" / "templates" / "specs" / "requirements.md"
        assert expected_path.exists(), f"Expected template path should exist: {expected_path}"
        
        # Verify all three enhanced templates exist
        assert (loader.templates_dir / "shared" / "settings" / "templates" / "specs" / "requirements.md").exists()
        assert (loader.templates_dir / "shared" / "settings" / "templates" / "specs" / "design.md").exists()
        assert (loader.templates_dir / "shared" / "settings" / "templates" / "specs" / "tasks.md").exists()

    def test_template_content_quality(self):
        """Test that loaded templates have enhanced quality markers."""
        loader = TemplateLoader()
        
        # Requirements template quality markers
        req_template = loader.load_spec_template("requirements", "requirements")
        assert "VERSION:" in req_template, "Requirements should have version metadata"
        assert "STATUS:" in req_template, "Requirements should have status metadata"
        assert "REQ-" in req_template, "Requirements should use REQ-X.Y format"
        
        # Design template quality markers
        design_template = loader.load_spec_template("design", "design")
        assert "VERSION:" in design_template, "Design should have version metadata"
        assert "Design Rationale" in design_template or "Intent" in design_template, "Design should document intent"
        
        # Tasks template quality markers
        tasks_template = loader.load_spec_template("tasks", "tasks")
        assert "VERSION:" in tasks_template, "Tasks should have version metadata"
        assert "References REQ-" in tasks_template or "Requirement ID" in tasks_template, "Tasks should reference requirements"

    def test_fallback_still_works(self):
        """Test that fallback to default templates still works for non-existent templates."""
        loader = TemplateLoader()
        
        # Try to load a non-existent template - should fall back to default
        template = loader.load_spec_template("nonexistent", "requirements")
        assert template is not None, "Should fall back to default template"
        assert "Requirements:" in template, "Default fallback should still work"

