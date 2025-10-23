"""Template discovery and loading utilities."""

from pathlib import Path

# Path to templates directory relative to package root
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "tools" / "cc-sdd" / "templates"


class TemplateLoader:
    """Loads templates for steering and specification documents."""

    def __init__(self, language: str = "en"):
        """Initialize the template loader.

        Args:
            language: Language code for templates (en, ja, zh-TW, etc.)
        """
        self.language = language
        self.templates_dir = TEMPLATES_DIR

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
            template_name: Name of the template
            spec_type: Type of spec (requirements, design, tasks)

        Returns:
            Template content if found, None otherwise
        """
        template_path = self._get_template_path(f"settings/specs/{spec_type}", template_name)

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
