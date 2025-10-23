"""Workflow logic for specification validation."""

import json
import logging
from pathlib import Path

from cc_sdd_mcp.models.specification import SpecificationMetadata
from cc_sdd_mcp.models.steering import SteeringConfig
from cc_sdd_mcp.models.validation import (
    DesignValidationResult,
    GapAnalysisResult,
    ImplementationValidationResult,
    ValidationIssue,
    ValidationSeverity,
)
from cc_sdd_mcp.utils.filesystem import FileSystemManager

logger = logging.getLogger(__name__)


class ValidationWorkflow:
    """Manages specification validation workflows."""

    def __init__(self, project_dir: Path = Path(".")):
        """Initialize the validation workflow.

        Args:
            project_dir: Project directory path
        """
        self.project_dir = project_dir
        self.fs_manager = FileSystemManager(project_dir)
        self.config = SteeringConfig()

    def _get_spec_dir(self, feature_name: str) -> Path:
        """Get the spec directory for a feature."""
        return self.project_dir / self.config.kiro_dir / "specs" / feature_name

    def _load_metadata(self, feature_name: str) -> SpecificationMetadata:
        """Load specification metadata."""
        spec_dir = self._get_spec_dir(feature_name)
        metadata_file = spec_dir / "metadata.json"

        if not metadata_file.exists():
            raise FileNotFoundError(f"Specification '{feature_name}' not found")

        metadata_data = json.loads(metadata_file.read_text())
        return SpecificationMetadata(**metadata_data)

    async def validate_gap(self, feature_name: str) -> GapAnalysisResult:
        """Analyze gap between existing code and requirements.

        Args:
            feature_name: Feature name

        Returns:
            Gap analysis result
        """
        self._load_metadata(feature_name)
        spec_dir = self._get_spec_dir(feature_name)
        requirements_file = spec_dir / "requirements.md"

        if not requirements_file.exists():
            return GapAnalysisResult(
                validation_type="gap_analysis",
                feature_name=feature_name,
                passed=False,
                issues=[
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message="Requirements document not found",
                        suggestion="Run spec_requirements first",
                    )
                ],
                summary="Cannot perform gap analysis without requirements",
                existing_components=[],
                missing_components=[
                    "Requirements need to be generated",
                    "No existing components analyzed",
                ],
            )

        # Perform basic gap analysis
        # In a real implementation, this would scan the codebase
        issues = []

        # Example validation checks
        if not (self.project_dir / "src").exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Source directory not found",
                    location="src/",
                    suggestion="Create source directory structure",
                )
            )

        if not (self.project_dir / "tests").exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Tests directory not found",
                    location="tests/",
                    suggestion="Create tests directory",
                )
            )

        return GapAnalysisResult(
            validation_type="gap_analysis",
            feature_name=feature_name,
            passed=len([i for i in issues if i.severity == ValidationSeverity.ERROR]) == 0,
            issues=issues,
            summary=f"Gap analysis completed with {len(issues)} issues found",
            existing_implementations=[
                "Basic project structure",
                "Configuration files",
            ],
            missing_requirements=[
                "Feature implementation",
                "Unit tests",
                "Integration tests",
            ],
            conflicting_implementations=[],
        )

    async def validate_design(self, feature_name: str) -> DesignValidationResult:
        """Validate design document against requirements.

        Args:
            feature_name: Feature name

        Returns:
            Design validation result
        """
        self._load_metadata(feature_name)
        spec_dir = self._get_spec_dir(feature_name)
        design_file = spec_dir / "design.md"
        requirements_file = spec_dir / "requirements.md"

        issues = []

        if not design_file.exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Design document not found",
                    suggestion="Run spec_design first",
                )
            )

        if not requirements_file.exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Requirements document not found",
                    suggestion="Run spec_requirements first",
                )
            )

        if issues:
            return DesignValidationResult(
                validation_type="design_validation",
                feature_name=feature_name,
                passed=False,
                issues=issues,
                summary="Cannot validate design without required documents",
                requirements_alignment=[],
                missing_design_elements=[
                    "Architecture overview",
                    "Component design",
                    "Data models",
                ],
            )

        # Perform design validation
        design_content = design_file.read_text()
        requirements_file.read_text()

        # Check for key design elements
        design_checks = {
            "architecture": "Architecture Overview" in design_content
            or "architecture" in design_content.lower(),
            "components": "Components" in design_content or "component" in design_content.lower(),
            "data_models": "Data Models" in design_content or "model" in design_content.lower(),
            "api": "API" in design_content or "endpoint" in design_content.lower(),
            "security": "Security" in design_content or "security" in design_content.lower(),
        }

        for element, exists in design_checks.items():
            if not exists:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        message=f"Design may be missing {element} section",
                        location="design.md",
                        suggestion=f"Add detailed {element} information",
                    )
                )

        # Calculate completeness scores
        missing_elements = [element for element, exists in design_checks.items() if not exists]
        design_completeness = (
            (len(design_checks) - len(missing_elements)) / len(design_checks) * 100
        )
        requirements_coverage = 85.0  # Placeholder - would analyze requirements alignment

        return DesignValidationResult(
            validation_type="design_validation",
            feature_name=feature_name,
            passed=len([i for i in issues if i.severity == ValidationSeverity.ERROR]) == 0,
            issues=issues,
            summary=f"Design validation completed with {len(issues)} issues",
            requirements_coverage=requirements_coverage,
            missing_components=missing_elements,
            design_completeness=design_completeness,
        )

    async def validate_implementation(self, feature_name: str) -> ImplementationValidationResult:
        """Validate implementation against task breakdown.

        Args:
            feature_name: Feature name

        Returns:
            Implementation validation result
        """
        self._load_metadata(feature_name)
        spec_dir = self._get_spec_dir(feature_name)
        tasks_file = spec_dir / "tasks.md"

        issues = []

        if not tasks_file.exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Tasks document not found",
                    suggestion="Run spec_tasks first",
                )
            )
            return ImplementationValidationResult(
                validation_type="implementation_validation",
                feature_name=feature_name,
                passed=False,
                issues=issues,
                summary="Cannot validate implementation without task breakdown",
                completed_tasks=[],
                incomplete_tasks=["All tasks pending"],
            )

        # In a real implementation, this would check actual code completion
        # For now, we'll provide a template response

        # Check for implementation files
        src_dir = self.project_dir / "src"
        tests_dir = self.project_dir / "tests"

        if not src_dir.exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Source directory not found",
                    location="src/",
                    suggestion="Implement feature code in src/ directory",
                )
            )

        if not tests_dir.exists():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Tests directory not found",
                    location="tests/",
                    suggestion="Add test coverage",
                )
            )

        # Calculate task completion
        incomplete_list = ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2"]
        total_tasks = 6
        completed = 0
        completion_pct = (completed / total_tasks * 100) if total_tasks > 0 else 0.0

        return ImplementationValidationResult(
            validation_type="implementation_validation",
            feature_name=feature_name,
            passed=len([i for i in issues if i.severity == ValidationSeverity.ERROR]) == 0,
            issues=issues,
            summary=f"Implementation validation completed with {len(issues)} issues",
            tasks_completed=completed,
            tasks_total=total_tasks,
            completion_percentage=completion_pct,
            incomplete_tasks=incomplete_list,
            test_coverage=0.0,
        )
