"""Tests for template system functionality."""

import pytest

from cc_sdd_mcp.utils.templates import TemplateLoader


class TestTemplateLoader:
    """Test the TemplateLoader class."""

    def test_template_loader_initialization(self, tmp_path):
        """Test template loader can be initialized."""
        loader = TemplateLoader(project_dir=tmp_path, language="en")
        assert loader.language == "en"
        assert loader.project_dir == tmp_path
        assert loader.jinja_env is not None

    def test_render_jinja_template(self, tmp_path):
        """Test rendering a Jinja2 template from string."""
        loader = TemplateLoader(project_dir=tmp_path)

        template_content = "Hello {{ name }}! You are {{ age }} years old."
        context = {"name": "Alice", "age": 30}

        result = loader.render_jinja_template(template_content, context)
        assert result == "Hello Alice! You are 30 years old."

    def test_render_jinja_template_with_filters(self, tmp_path):
        """Test rendering with Jinja2 filters."""
        loader = TemplateLoader(project_dir=tmp_path)

        template_content = "{{ name | upper }}"
        context = {"name": "alice"}

        result = loader.render_jinja_template(template_content, context)
        assert result == "ALICE"

    def test_render_jinja_template_with_conditionals(self, tmp_path):
        """Test rendering with Jinja2 conditionals."""
        loader = TemplateLoader(project_dir=tmp_path)

        template_content = """
        {%- if is_admin -%}
        Admin User
        {%- else -%}
        Regular User
        {%- endif -%}
        """

        result_admin = loader.render_jinja_template(template_content, {"is_admin": True})
        assert "Admin User" in result_admin

        result_user = loader.render_jinja_template(template_content, {"is_admin": False})
        assert "Regular User" in result_user

    def test_render_jinja_template_with_loops(self, tmp_path):
        """Test rendering with Jinja2 loops."""
        loader = TemplateLoader(project_dir=tmp_path)

        template_content = """
        {% for item in items -%}
        - {{ item }}
        {% endfor -%}
        """
        context = {"items": ["apple", "banana", "cherry"]}

        result = loader.render_jinja_template(template_content, context)
        assert "- apple" in result
        assert "- banana" in result
        assert "- cherry" in result

    def test_render_jinja_file(self, tmp_path):
        """Test rendering a Jinja2 template from file."""
        loader = TemplateLoader(project_dir=tmp_path)

        # Create a template file
        template_file = tmp_path / "test_template.md"
        template_file.write_text("# {{ title }}\n\n{{ content }}")

        context = {"title": "Test Document", "content": "This is a test."}
        result = loader.render_jinja_file("test_template.md", context)

        assert "# Test Document" in result
        assert "This is a test." in result

    def test_render_jinja_file_not_found(self, tmp_path):
        """Test rendering a non-existent template file."""
        loader = TemplateLoader(project_dir=tmp_path)

        with pytest.raises(FileNotFoundError):
            loader.render_jinja_file("nonexistent.md", {})

    def test_list_templates_empty(self, tmp_path):
        """Test listing templates when none exist."""
        loader = TemplateLoader(project_dir=tmp_path)
        templates = loader.list_templates()
        # Will list templates from package directory if it exists
        assert isinstance(templates, list)

    def test_extract_language(self, tmp_path):
        """Test language extraction from filename."""
        loader = TemplateLoader(project_dir=tmp_path)

        assert loader._extract_language("product.en.md") == "en"
        assert loader._extract_language("product.ja.md") == "ja"
        assert loader._extract_language("product.md") == "default"

    def test_substitute_variables_backward_compat(self, tmp_path):
        """Test that old string substitution still works."""
        loader = TemplateLoader(project_dir=tmp_path)

        template = "Hello {{name}}! You are {{age}} years old."
        variables = {"name": "Bob", "age": "25"}

        result = loader.substitute_variables(template, variables)
        assert result == "Hello Bob! You are 25 years old."

    def test_load_steering_template(self, tmp_path):
        """Test loading steering templates."""
        loader = TemplateLoader(project_dir=tmp_path)

        # Should fall back to default templates
        product_template = loader.load_steering_template("product")
        assert product_template is not None
        assert "Product Context" in product_template

    def test_load_spec_template(self, tmp_path):
        """Test loading spec templates."""
        loader = TemplateLoader(project_dir=tmp_path)

        # Should fall back to default templates
        req_template = loader.load_spec_template("requirements", "requirements")
        assert req_template is not None
        assert "Requirements" in req_template


@pytest.mark.asyncio
class TestTemplateTools:
    """Test template management tools."""

    async def test_template_list_handler(self, tmp_path):
        """Test template_list tool handler."""
        from cc_sdd_mcp.tools.templates import template_list_handler

        result = await template_list_handler({"project_dir": str(tmp_path)})
        assert isinstance(result, str)

        import json

        data = json.loads(result)
        assert data["success"] is True
        assert "templates" in data
        assert isinstance(data["templates"], list)

    async def test_template_get_handler(self, tmp_path):
        """Test template_get tool handler."""
        from cc_sdd_mcp.tools.templates import template_get_handler

        result = await template_get_handler(
            {
                "template_name": "product",
                "template_type": "steering",
                "project_dir": str(tmp_path),
            }
        )

        import json

        data = json.loads(result)
        assert data["success"] is True
        assert "content" in data
        assert "Product Context" in data["content"]

    async def test_template_render_handler_string(self, tmp_path):
        """Test template_render tool handler with string template."""
        from cc_sdd_mcp.tools.templates import template_render_handler

        result = await template_render_handler(
            {
                "template_content": "Hello {{ name }}!",
                "context": {"name": "World"},
                "project_dir": str(tmp_path),
            }
        )

        import json

        data = json.loads(result)
        assert data["success"] is True
        assert data["rendered_content"] == "Hello World!"

    async def test_template_render_handler_file(self, tmp_path):
        """Test template_render tool handler with file template."""
        from cc_sdd_mcp.tools.templates import template_render_handler

        # Create a template file
        template_file = tmp_path / "test.md"
        template_file.write_text("# {{ title }}")

        result = await template_render_handler(
            {
                "template_content": "test.md",
                "context": {"title": "Test"},
                "use_file": True,
                "project_dir": str(tmp_path),
            }
        )

        import json

        data = json.loads(result)
        assert data["success"] is True
        assert "# Test" in data["rendered_content"]

    async def test_template_render_handler_error(self, tmp_path):
        """Test template_render tool handler with error."""
        from cc_sdd_mcp.tools.templates import template_render_handler

        # Invalid Jinja2 syntax
        result = await template_render_handler(
            {
                "template_content": "{{ unclosed",
                "context": {},
                "project_dir": str(tmp_path),
            }
        )

        import json

        data = json.loads(result)
        assert data["success"] is False
        assert "error" in data
