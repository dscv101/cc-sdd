"""Workflow logic for specification lifecycle management."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from cc_sdd_mcp.models.specification import (
    DesignDocument,
    RequirementsDocument,
    SpecificationMetadata,
    SpecPhase,
    TaskItem,
    TasksDocument,
)
from cc_sdd_mcp.models.steering import SteeringConfig
from cc_sdd_mcp.utils.filesystem import FileSystemManager
from cc_sdd_mcp.utils.templates import TemplateLoader

logger = logging.getLogger(__name__)


class SpecWorkflow:
    """Manages the specification lifecycle workflow."""

    def __init__(self, project_dir: Path = Path(".")):
        """Initialize the spec workflow.

        Args:
            project_dir: Project directory path
        """
        self.project_dir = project_dir
        self.fs_manager = FileSystemManager(project_dir)
        self.template_loader = TemplateLoader(project_dir)
        self.config = SteeringConfig()

    def _get_spec_dir(self, feature_name: str) -> Path:
        """Get the spec directory for a feature.

        Args:
            feature_name: Feature name

        Returns:
            Path to spec directory
        """
        return self.project_dir / self.config.kiro_dir / "specs" / feature_name

    def _load_metadata(self, feature_name: str) -> SpecificationMetadata:
        """Load specification metadata.

        Args:
            feature_name: Feature name

        Returns:
            Specification metadata

        Raises:
            FileNotFoundError: If metadata file doesn't exist
        """
        spec_dir = self._get_spec_dir(feature_name)
        metadata_file = spec_dir / "metadata.json"

        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Specification '{feature_name}' not found. Run spec_init first."
            )

        metadata_data = json.loads(metadata_file.read_text())
        return SpecificationMetadata(**metadata_data)

    def _save_metadata(self, metadata: SpecificationMetadata) -> None:
        """Save specification metadata.

        Args:
            metadata: Specification metadata to save
        """
        spec_dir = self._get_spec_dir(metadata.feature_name)
        metadata_file = spec_dir / "metadata.json"

        # Update timestamp
        metadata.updated_at = datetime.now()

        metadata_file.write_text(metadata.model_dump_json(indent=2))
        logger.info(f"Updated metadata for {metadata.feature_name}")

    async def generate_requirements(
        self, feature_name: str, auto_approve: bool = False
    ) -> dict[str, Any]:
        """Generate requirements document for a specification.

        Args:
            feature_name: Feature name
            auto_approve: Auto-approve and move to next phase

        Returns:
            Result dictionary with generation status
        """
        # Load metadata
        metadata = self._load_metadata(feature_name)

        # Check current phase
        if metadata.current_phase not in [SpecPhase.INITIALIZED, SpecPhase.REQUIREMENTS]:
            return {
                "success": False,
                "error": f"Cannot generate requirements in phase: {metadata.current_phase.value}",
                "current_phase": metadata.current_phase.value,
            }

        # Load steering context
        steering_status = self.fs_manager.get_steering_status()
        steering_context = []
        for doc in steering_status.documents:
            steering_context.append(f"# {doc.file_type.value}\n{doc.content}")

        # Generate requirements using enhanced template
        template = self.template_loader.load_spec_template("requirements", "requirements")
        if not template:
            return {"success": False, "error": "Requirements template not found"}

        # Create requirements document
        requirements = RequirementsDocument(
            feature_name=feature_name,
            functional_requirements=[
                f"Functional requirement for {metadata.description}",
                "User can interact with the feature",
                "System responds appropriately",
            ],
            non_functional_requirements=[
                "Performance: Response time < 2s",
                "Security: Data validation required",
                "Scalability: Support 1000+ concurrent users",
            ],
            constraints=[
                "Must use existing authentication system",
                "Cannot modify database schema",
            ],
            acceptance_criteria=[
                "Feature meets all functional requirements",
                "All tests pass with >80% coverage",
                "Documentation is complete",
            ],
        )

        # Save requirements
        spec_dir = self._get_spec_dir(feature_name)
        requirements_file = spec_dir / "requirements.md"

        content = f"""# Requirements: {feature_name}

**Description**: {metadata.description}

## Functional Requirements

{chr(10).join(f"- {req}" for req in requirements.functional_requirements)}

## Non-Functional Requirements

{chr(10).join(f"- {req}" for req in requirements.non_functional_requirements)}

## Constraints

{chr(10).join(f"- {constraint}" for constraint in requirements.constraints)}

## Acceptance Criteria

{chr(10).join(f"- {criteria}" for criteria in requirements.acceptance_criteria)}

---
*Generated: {requirements.created_at}*
"""

        requirements_file.write_text(content)

        # Update metadata
        metadata.current_phase = SpecPhase.REQUIREMENTS
        if auto_approve and SpecPhase.REQUIREMENTS not in metadata.approved_phases:
            metadata.approved_phases.append(SpecPhase.REQUIREMENTS)
        self._save_metadata(metadata)

        return {
            "success": True,
            "feature_name": feature_name,
            "requirements_file": str(requirements_file),
            "current_phase": metadata.current_phase.value,
            "auto_approved": auto_approve,
            "message": "Requirements generated successfully",
        }

    async def generate_design(
        self, feature_name: str, auto_approve: bool = False
    ) -> dict[str, Any]:
        """Generate design document for a specification.

        Args:
            feature_name: Feature name
            auto_approve: Auto-approve and move to next phase

        Returns:
            Result dictionary with generation status
        """
        # Load metadata
        metadata = self._load_metadata(feature_name)

        # Check current phase
        if metadata.current_phase not in [SpecPhase.REQUIREMENTS, SpecPhase.DESIGN]:
            return {
                "success": False,
                "error": f"Cannot generate design in phase: {metadata.current_phase.value}",
                "current_phase": metadata.current_phase.value,
            }

        # Check if requirements are approved
        if (
            SpecPhase.REQUIREMENTS not in metadata.approved_phases
            and metadata.current_phase == SpecPhase.REQUIREMENTS
            and not auto_approve
        ):
            return {
                "success": False,
                "error": "Requirements must be approved before generating design",
                "current_phase": metadata.current_phase.value,
                "message": "Please review and approve requirements first, or use auto_approve=true",
            }

        # Load requirements
        spec_dir = self._get_spec_dir(feature_name)
        requirements_file = spec_dir / "requirements.md"
        # Note: requirements content would be used in a full implementation
        _ = requirements_file.read_text() if requirements_file.exists() else ""

        # Create design document
        design = DesignDocument(
            feature_name=feature_name,
            architecture_overview=f"Architecture for {metadata.description}",
            components=[
                {"name": "Frontend", "description": "User interface components"},
                {"name": "Backend", "description": "API and business logic"},
                {"name": "Database", "description": "Data persistence layer"},
            ],
            data_models=[
                {"name": "User", "description": "User account model"},
                {"name": "Session", "description": "User session tracking"},
            ],
            api_endpoints=[
                {"path": "/api/feature", "method": "GET", "description": "Retrieve feature data"},
                {"path": "/api/feature", "method": "POST", "description": "Create feature data"},
            ],
            dependencies=["pydantic", "fastapi", "sqlalchemy"],
            security_considerations=[
                "Input validation on all endpoints",
                "Authentication required for all operations",
                "Rate limiting on API endpoints",
            ],
        )

        # Save design
        design_file = spec_dir / "design.md"
        content = f"""# Design: {feature_name}

**Architecture Overview**: {design.architecture_overview}

## Components

{chr(10).join(f"### {comp['name']}{chr(10)}{comp['description']}" for comp in design.components)}

## Data Models

{chr(10).join(f"### {model['name']}{chr(10)}{model['description']}" for model in design.data_models)}

## API Endpoints

{chr(10).join(f"- **{ep['method']}** `{ep['path']}`: {ep.get('description', '')}" for ep in design.api_endpoints)}

## Dependencies

{chr(10).join(f"- {dep}" for dep in design.dependencies)}

## Security Considerations

{chr(10).join(f"- {sec}" for sec in design.security_considerations)}

---
*Generated: {design.created_at}*
"""

        design_file.write_text(content)

        # Update metadata
        metadata.current_phase = SpecPhase.DESIGN
        if auto_approve and SpecPhase.DESIGN not in metadata.approved_phases:
            metadata.approved_phases.append(SpecPhase.DESIGN)
        self._save_metadata(metadata)

        return {
            "success": True,
            "feature_name": feature_name,
            "design_file": str(design_file),
            "current_phase": metadata.current_phase.value,
            "auto_approved": auto_approve,
            "message": "Design generated successfully",
        }

    async def generate_tasks(self, feature_name: str, auto_approve: bool = False) -> dict[str, Any]:
        """Generate task breakdown for a specification.

        Args:
            feature_name: Feature name
            auto_approve: Auto-approve and move to next phase

        Returns:
            Result dictionary with generation status
        """
        # Load metadata
        metadata = self._load_metadata(feature_name)

        # Check current phase
        if metadata.current_phase not in [SpecPhase.DESIGN, SpecPhase.TASKS]:
            return {
                "success": False,
                "error": f"Cannot generate tasks in phase: {metadata.current_phase.value}",
                "current_phase": metadata.current_phase.value,
            }

        # Check if design is approved
        if (
            SpecPhase.DESIGN not in metadata.approved_phases
            and metadata.current_phase == SpecPhase.DESIGN
            and not auto_approve
        ):
            return {
                "success": False,
                "error": "Design must be approved before generating tasks",
                "current_phase": metadata.current_phase.value,
                "message": "Please review and approve design first, or use auto_approve=true",
            }

        # Create task breakdown
        tasks = TasksDocument(
            feature_name=feature_name,
            tasks=[
                TaskItem(
                    task_id="1.1",
                    title="Setup project structure",
                    description="Initialize directories and configuration files",
                    estimated_hours=2.0,
                ),
                TaskItem(
                    task_id="1.2",
                    title="Implement data models",
                    description="Create Pydantic models for data validation",
                    estimated_hours=4.0,
                    dependencies=["1.1"],
                ),
                TaskItem(
                    task_id="2.1",
                    title="Implement API endpoints",
                    description="Create FastAPI routes and handlers",
                    estimated_hours=8.0,
                    dependencies=["1.2"],
                ),
                TaskItem(
                    task_id="2.2",
                    title="Add authentication",
                    description="Implement JWT-based authentication",
                    estimated_hours=6.0,
                    dependencies=["2.1"],
                ),
                TaskItem(
                    task_id="3.1",
                    title="Write unit tests",
                    description="Achieve >80% test coverage",
                    estimated_hours=8.0,
                    dependencies=["2.2"],
                ),
                TaskItem(
                    task_id="3.2",
                    title="Integration testing",
                    description="Test end-to-end workflows",
                    estimated_hours=6.0,
                    dependencies=["3.1"],
                ),
            ],
            total_estimated_hours=34.0,
        )

        # Save tasks
        spec_dir = self._get_spec_dir(feature_name)
        tasks_file = spec_dir / "tasks.md"

        content = f"""# Tasks: {feature_name}

**Total Estimated Hours**: {tasks.total_estimated_hours}

## Task Breakdown

{
            chr(10).join(
                f'''### Task {task.task_id}: {task.title}

**Description**: {task.description}
**Estimated**: {task.estimated_hours}h
**Dependencies**: {", ".join(task.dependencies) if task.dependencies else "None"}
**Status**: {"✅ Complete" if task.completed else "⏳ Pending"}

'''
                for task in tasks.tasks
            )
        }

---
*Generated: {tasks.created_at}*
"""

        tasks_file.write_text(content)

        # Update metadata
        metadata.current_phase = SpecPhase.TASKS
        if auto_approve and SpecPhase.TASKS not in metadata.approved_phases:
            metadata.approved_phases.append(SpecPhase.TASKS)
        self._save_metadata(metadata)

        return {
            "success": True,
            "feature_name": feature_name,
            "tasks_file": str(tasks_file),
            "total_tasks": len(tasks.tasks),
            "total_hours": tasks.total_estimated_hours,
            "current_phase": metadata.current_phase.value,
            "auto_approved": auto_approve,
            "message": "Tasks generated successfully",
        }

    async def get_spec_status(self, feature_name: str) -> dict[str, Any]:
        """Get the current status of a specification.

        Args:
            feature_name: Feature name

        Returns:
            Status dictionary
        """
        try:
            metadata = self._load_metadata(feature_name)
            spec_dir = self._get_spec_dir(feature_name)

            # Check which files exist
            files_exist = {
                "requirements": (spec_dir / "requirements.md").exists(),
                "design": (spec_dir / "design.md").exists(),
                "tasks": (spec_dir / "tasks.md").exists(),
            }

            return {
                "feature_name": metadata.feature_name,
                "description": metadata.description,
                "current_phase": metadata.current_phase.value,
                "approved_phases": [phase.value for phase in metadata.approved_phases],
                "created_at": metadata.created_at.isoformat(),
                "updated_at": metadata.updated_at.isoformat(),
                "files": files_exist,
                "spec_dir": str(spec_dir),
            }
        except FileNotFoundError as e:
            return {"error": str(e), "feature_name": feature_name}
