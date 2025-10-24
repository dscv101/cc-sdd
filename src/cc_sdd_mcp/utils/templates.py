"""Template discovery and loading utilities with Jinja2 support."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

# Path to templates directory relative to package root
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "tools" / "cc-sdd" / "templates"


class TemplateLoader:
    """Loads and renders templates for steering and specification documents.

    Supports both simple string substitution and Jinja2 templating.
    """

    def __init__(self, project_dir: Path = Path("."), language: str = "en"):
        """Initialize the template loader.

        Args:
            project_dir: Project directory for loading custom templates
            language: Language code for templates (en, ja, zh-TW, etc.)
        """
        self.language = language
        self.templates_dir = TEMPLATES_DIR
        self.project_dir = project_dir

        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader([str(self.templates_dir), str(self.project_dir)]),
            autoescape=False,  # Markdown doesn't need HTML escaping
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _get_template_path(self, category: str, filename: str) -> Path | None:
        """Get path to a template file.

        Args:
            category: Template category (settings, agents, etc.)
            filename: Template filename

        Returns:
            Path to template file if it exists, None otherwise
        """
        # Try language-specific template first
        lang_path = self.templates_dir / category / f"{filename}.{self.language}.md"
        if lang_path.exists():
            return lang_path

        # Fall back to English
        en_path = self.templates_dir / category / f"{filename}.en.md"
        if en_path.exists():
            return en_path

        # Try without language suffix
        default_path = self.templates_dir / category / f"{filename}.md"
        if default_path.exists():
            return default_path

        return None

    def load_steering_template(self, template_name: str) -> str | None:
        """Load a steering template.

        Args:
            template_name: Name of the template (product, tech, structure)

        Returns:
            Template content if found, None otherwise
        """
        # Steering templates are in settings directory
        template_path = self._get_template_path("settings/steering", template_name)

        if template_path and template_path.exists():
            return template_path.read_text(encoding="utf-8")

        # Fall back to default template
        return self._get_default_steering_template(template_name)

    def load_spec_template(self, template_name: str, spec_type: str = "requirements") -> str | None:
        """Load a specification template.

        Args:
            template_name: Name of the template (use spec_type for enhanced templates)
            spec_type: Type of spec (requirements, design, tasks)

        Returns:
            Template content if found, None otherwise
        """
        # For enhanced templates, use spec_type as the filename in shared/settings/templates/specs
        template_path = self._get_template_path("shared/settings/templates/specs", spec_type)

        if template_path and template_path.exists():
            return template_path.read_text(encoding="utf-8")

        return self._get_default_spec_template(spec_type)

    def _get_default_steering_template(self, template_name: str) -> str:
        """Get default steering template content.

        Args:
            template_name: Name of the template

        Returns:
            Default template content
        """
        templates = {
            "product": """# Product Context

## Overview
Describe the product's purpose and vision.

## Target Users
Who are the users of this product?

## Key Features
What are the main features?

## Business Goals
What business goals does this product support?
""",
            "tech": """# Technical Context

## Tech Stack
List the technologies used in this project.

## Architecture
Describe the high-level architecture.

## Key Patterns
What design patterns or conventions are used?

## Dependencies
List major dependencies and their purposes.
""",
            "structure": """# Project Structure

## Directory Layout
Describe the directory structure.

## Module Organization
How are modules/packages organized?

## Testing Strategy
Where are tests located? What's the testing approach?

## Build and Deployment
How is the project built and deployed?
""",
        }
        return templates.get(template_name, f"# {template_name.title()}\n\n")

    def _get_default_spec_template(self, spec_type: str) -> str:
        """Get default specification template content.

        Args:
            spec_type: Type of spec (requirements, design, tasks)

        Returns:
            Default template content
        """
        templates = {
            "requirements": """# Requirements: {feature_name}

## Feature Description
Brief description of the feature.

## Functional Requirements
1. Requirement 1
2. Requirement 2

## Non-Functional Requirements
1. Performance requirement
2. Security requirement

## Constraints
List any constraints or limitations.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
""",
            "design": """# Design: {feature_name}

## Architecture Overview
High-level architecture description.

## Components
### Component 1
Description of component 1

### Component 2
Description of component 2

## Data Models
Description of data models.

## API Design
API endpoints if applicable.

## Security Considerations
Security aspects to consider.
""",
            "tasks": """# Tasks: {feature_name}

## Task Breakdown

### Phase 1: Setup
- [ ] 1.1: Task description
- [ ] 1.2: Task description

### Phase 2: Implementation
- [ ] 2.1: Task description
- [ ] 2.2: Task description

### Phase 3: Testing
- [ ] 3.1: Task description
- [ ] 3.2: Task description

## Estimated Timeline
Total: X hours
""",
        }
        return templates.get(spec_type, f"# {spec_type.title()}\n\n")

    def substitute_variables(self, template: str, variables: dict[str, str]) -> str:
        """Substitute variables in template.

        Args:
            template: Template content with {{VARIABLE}} placeholders
            variables: Dictionary of variable name to value mappings

        Returns:
            Template with variables substituted
        """
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, value)
        return result

    def render_jinja_template(self, template_content: str, context: dict) -> str:
        """Render a template string using Jinja2.

        Args:
            template_content: Template content with Jinja2 syntax
            context: Dictionary of context variables for rendering

        Returns:
            Rendered template content
        """
        template = Template(template_content)
        return template.render(**context)

    def render_jinja_file(self, template_path: str | Path, context: dict) -> str:
        """Render a template file using Jinja2.

        Args:
            template_path: Path to template file (relative to template directories)
            context: Dictionary of context variables for rendering

        Returns:
            Rendered template content

        Raises:
            FileNotFoundError: If template file is not found
        """
        try:
            template = self.jinja_env.get_template(str(template_path))
            return template.render(**context)
        except Exception as e:
            raise FileNotFoundError(f"Template not found: {template_path}") from e

    def list_templates(self, category: str | None = None) -> list[dict[str, str]]:
        """List all available templates.

        Args:
            category: Optional category filter (settings, specs, etc.)

        Returns:
            List of template info dictionaries with name, path, and category
        """
        templates = []

        # Search in templates directory
        search_dir = self.templates_dir
        if category:
            search_dir = search_dir / category

        if search_dir.exists():
            for template_file in search_dir.rglob("*.md"):
                rel_path = template_file.relative_to(self.templates_dir)
                templates.append(
                    {
                        "name": template_file.stem,
                        "path": str(rel_path),
                        "category": str(rel_path.parent),
                        "language": self._extract_language(template_file.name),
                    }
                )

        return templates

    def _extract_language(self, filename: str) -> str:
        """Extract language code from filename.

        Args:
            filename: Template filename (e.g., "product.en.md")

        Returns:
            Language code or "default" if none found
        """
        parts = filename.split(".")
        if len(parts) >= 3:  # name.lang.md
            return parts[-2]
        return "default"
