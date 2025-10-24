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

    def _build_requirements_context(self, metadata: SpecificationMetadata) -> dict[str, Any]:
        """Build context for requirements template rendering.
        
        Args:
            metadata: Specification metadata
            
        Returns:
            Context dictionary for template rendering
        """
        now = datetime.now()
        return {
            # Metadata
            "VERSION": "1.0.0",
            "STATUS": metadata.current_phase.value,
            "AUTHORS": "AI Assistant",
            "AUTHOR": "AI Assistant",
            "REVIEWERS": "TBD",
            "LAST_UPDATED": now.strftime("%Y-%m-%d"),
            "DATE": now.strftime("%Y-%m-%d"),
            "RELATED_SPECS": "None",
            
            # Feature details
            "NAME": metadata.feature_name,
            "BUSINESS_PROBLEM": metadata.description,
            "IMPACT": f"Implements {metadata.feature_name}",
            "BENEFIT": f"Provides {metadata.feature_name} capability",
            "MEASURABLE_BENEFIT": "TBD - to be defined during review",
            
            # Requirements areas (examples)
            "REQUIREMENT_AREA_1": "Core Functionality",
            "REQUIREMENT_AREA_2": "User Experience",
            "SUB_REQUIREMENT_AREA": "Integration",
            
            # EARS-style placeholders
            "SPECIFIC_ROLE": "user",
            "ROLE": "system",
            "CAPABILITY": "process requests",
            "SPECIFIC_CAPABILITY": "handle edge cases",
            "WHY_THIS_REQUIREMENT": "to ensure system reliability",
            "WHY_THIS_BEHAVIOR": "to meet user expectations",
            "WHY": "to satisfy business requirements",
            
            # Constraints and assumptions
            "CONSTRAINT_1": "Must integrate with existing authentication",
            "WHY_THIS_CONSTRAINT": "to maintain security standards",
            "ASSUMPTION_1": "Users have valid accounts",
            
            # Alternatives and rationale
            "ALT_1": "Alternative approach A",
            "ALT_2": "Alternative approach B",
            "RATIONALE_1": "Chosen for performance",
            "RATIONALE_2": "Aligns with architecture",
            
            # Non-goals
            "NON_GOAL_1": "Supporting legacy systems",
            "NON_GOAL_2": "Backward compatibility with deprecated APIs",
            
            # Success metrics
            "SUCCESS_METRIC_1": ">80% test coverage",
            "SUCCESS_METRIC_2": "Response time <2s",
            
            # Conflicts and resolution
            "CONFLICT_DESCRIPTION": "None identified",
            "HOW_RESOLVED": "N/A",
            
            # Questions and ownership
            "QUESTION_1": "TBD during design phase",
            "OWNER": "TBD",
            "OTHER_STAKEHOLDER": "Product Team",
            "PRIORITY": "Medium",
            "CHANGES": "Initial version",
        }

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

        # Build context and render template
        context = self._build_requirements_context(metadata)
        try:
            content = self.template_loader.render_jinja_template(template, context)
        except Exception as e:
            logger.error(f"Failed to render requirements template: {e}")
            return {"success": False, "error": f"Template rendering failed: {str(e)}"}

        # Save requirements
        spec_dir = self._get_spec_dir(feature_name)
        requirements_file = spec_dir / "requirements.md"
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
            "message": "Requirements generated successfully using enhanced EARS template",
        }

    def _build_design_context(self, metadata: SpecificationMetadata) -> dict[str, Any]:
        """Build context for design template rendering.
        
        Args:
            metadata: Specification metadata
            
        Returns:
            Context dictionary for template rendering
        """
        now = datetime.now()
        return {
            # Metadata
            "VERSION": "1.0.0",
            "STATUS": metadata.current_phase.value,
            "AUTHORS": "AI Assistant",
            "AUTHOR": "AI Assistant",
            "REVIEWERS": "TBD",
            "LAST_UPDATED": now.strftime("%Y-%m-%d"),
            "DATE": now.strftime("%Y-%m-%d"),
            "REQ_VERSION": "1.0.0",
            "RELATED_DESIGNS": "None",
            
            # Overview and goals
            "IMPACT": f"Implements {metadata.feature_name}",
            "ANTI_GOAL_1": "Supporting legacy systems",
            "ANTI_GOAL_2": "Backward compatibility at expense of performance",
            
            # Architecture decisions
            "DECISION_1": "Use microservices architecture",
            "REASONING_1": "Enables independent scaling",
            "REASONING_2": "Improves maintainability",
            "REASONING_3": "Supports team autonomy",
            "REASON": "Based on scalability requirements",
            
            # Assumptions and constraints
            "ASSUMPTION_1": "Users have modern browsers",
            "TRIGGER_FOR_CHANGE": "User feedback or requirements changes",
            
            # Design rationale
            "HOW_TO_VERIFY": "Through integration testing and code review",
            "ITEMS": "Architecture components, Data models, API design",
            "ITEM_1": "Component architecture",
            
            # Risk management
            "RISK": "Medium",
            "RISK_1": "Integration complexity may increase",
            "MITIGATION_STRATEGY": "Incremental rollout with feature flags",
            
            # Future considerations
            "FUTURE_1": "Support for real-time updates",
            "FUTURE_2": "Mobile application integration",
            
            # System integration
            "SYSTEM_1": "Authentication service",
            
            # Questions and ownership
            "QUESTION_1": "TBD during implementation",
            "OWNER": "TBD",
            "NAME": metadata.feature_name,
            "CONTACT": "TBD",
            "COMMENTS": "Initial design",
            "CHANGES": "Initial version",
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

        # Load design template
        template = self.template_loader.load_spec_template("design", "design")
        if not template:
            return {"success": False, "error": "Design template not found"}

        # Build context and render template
        context = self._build_design_context(metadata)
        try:
            content = self.template_loader.render_jinja_template(template, context)
        except Exception as e:
            logger.error(f"Failed to render design template: {e}")
            return {"success": False, "error": f"Template rendering failed: {str(e)}"}

        # Save design
        spec_dir = self._get_spec_dir(feature_name)
        design_file = spec_dir / "design.md"
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
            "message": "Design generated successfully using enhanced template",
        }

    def _build_tasks_context(self, metadata: SpecificationMetadata) -> dict[str, Any]:
        """Build context for tasks template rendering.
        
        Args:
            metadata: Specification metadata
            
        Returns:
            Context dictionary for template rendering
        """
        now = datetime.now()
        return {
            # Metadata
            "VERSION": "1.0.0",
            "STATUS": metadata.current_phase.value,
            "AUTHOR": "AI Assistant",
            "LAST_UPDATED": now.strftime("%Y-%m-%d"),
            "DATE": now.strftime("%Y-%m-%d"),
            "REQ_VERSION": "1.0.0",
            "DESIGN_VERSION": "1.0.0",
            "SPRINT": "Sprint 1",
            
            # Overview estimates
            "TOTAL_ESTIMATE": "34 hours",
            "CRITICAL_TASKS": "1.1 (Foundation setup)",
            "HIGH_RISK_TASKS": "2.2 (Authentication integration)",
            
            # Phase estimates
            "PHASE_1_ESTIMATE": "12 hours",
            "PHASE_2_ESTIMATE": "16 hours",
            "PHASE_3_ESTIMATE": "6 hours",
            
            # Task details (examples)
            "TASK_ID": "1.1",
            "TASK_DESCRIPTION": "Setup project foundation",
            "WHY_THIS_TASK": "to establish development environment",
            "ASSIGNEE": "TBD",
            "ESTIMATE": "4h",
            "RISK_LEVEL": "Low",
            
            # Implementation details
            "DETAIL_1": "Initialize repository structure",
            "DETAIL_2": "Configure development tools",
            
            # Acceptance criteria
            "CRITERIA_1": "Project builds successfully",
            "CRITERIA_2": "CI pipeline runs all checks",
            
            # Traceability
            "ID": "REQ-001",
            "SPECIFIC_EARS_CRITERIA": "System shall process requests within 2s",
            
            # Testing
            "TEST_SCOPE": "Unit and integration tests",
            "MANUAL_STEPS": "Verify deployment to staging",
            "COVERAGE": "80%",
            
            # Status tracking
            "TOTAL_TASKS": "6",
            "COMPLETED_TASKS": "0",
            "IN_PROGRESS_TASKS": "0",
            "BLOCKED_TASKS": "0",
            "PERCENTAGE": "0%",
            
            # Process
            "MIN_REVIEWERS": "2",
            "SECURITY_TOOL": "bandit, trufflehog",
            
            # Notes and risks
            "NOTE_1": "Consider incremental rollout",
            "NOTES": "Initial task breakdown",
            "ISSUE": "None identified",
            "RISK_DESCRIPTION": "Integration complexity",
            
            # Planning
            "NEXT_PHASE": "Implementation",
            "NEXT_MAJOR_TASK": "Begin Phase 1 foundation work",
            
            # Ownership
            "OWNER": "TBD",
            "CHANGES": "Initial version",
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

        # Load tasks template
        template = self.template_loader.load_spec_template("tasks", "tasks")
        if not template:
            return {"success": False, "error": "Tasks template not found"}

        # Build context and render template
        context = self._build_tasks_context(metadata)
        try:
            content = self.template_loader.render_jinja_template(template, context)
        except Exception as e:
            logger.error(f"Failed to render tasks template: {e}")
            return {"success": False, "error": f"Template rendering failed: {str(e)}"}

        # Save tasks
        spec_dir = self._get_spec_dir(feature_name)
        tasks_file = spec_dir / "tasks.md"
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
            "current_phase": metadata.current_phase.value,
            "auto_approved": auto_approve,
            "message": "Tasks generated successfully using enhanced template",
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
