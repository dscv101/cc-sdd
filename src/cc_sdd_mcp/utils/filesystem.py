"""File system operations for managing .kiro directory structure."""

import json
from datetime import datetime
from pathlib import Path

from cc_sdd_mcp.models.specification import SpecificationMetadata
from cc_sdd_mcp.models.steering import SteeringDocument, SteeringFileType, SteeringStatus
from cc_sdd_mcp.utils.paths import (
    ensure_directory_exists,
    get_spec_dir,
    get_steering_dir,
)


class FileSystemManager:
    """Manages file system operations for cc-sdd."""

    def __init__(self, project_root: Path):
        """Initialize the file system manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.steering_dir = get_steering_dir(project_root)

    def ensure_steering_exists(self) -> None:
        """Ensure the steering directory exists."""
        ensure_directory_exists(self.steering_dir)

    def read_steering_document(self, file_type: SteeringFileType) -> SteeringDocument | None:
        """Read a steering document.

        Args:
            file_type: Type of steering document to read

        Returns:
            SteeringDocument if file exists, None otherwise
        """
        filename = f"{file_type.value}.md"
        file_path = self.steering_dir / filename

        if not file_path.exists():
            return None

        content = file_path.read_text(encoding="utf-8")
        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)

        return SteeringDocument(
            file_type=file_type,
            file_path=file_path,
            content=content,
            last_modified=last_modified,
        )

    def write_steering_document(
        self, file_type: SteeringFileType, content: str
    ) -> SteeringDocument:
        """Write a steering document.

        Args:
            file_type: Type of steering document
            content: Content to write

        Returns:
            SteeringDocument representing the written file
        """
        self.ensure_steering_exists()

        filename = f"{file_type.value}.md"
        file_path = self.steering_dir / filename

        file_path.write_text(content, encoding="utf-8")

        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)

        return SteeringDocument(
            file_type=file_type,
            file_path=file_path,
            content=content,
            last_modified=last_modified,
        )

    def list_steering_documents(self) -> list[SteeringDocument]:
        """List all steering documents.

        Returns:
            List of SteeringDocument objects
        """
        if not self.steering_dir.exists():
            return []

        documents = []
        for file_path in self.steering_dir.glob("*.md"):
            # Determine file type from filename
            stem = file_path.stem
            try:
                file_type = SteeringFileType(stem)
            except ValueError:
                file_type = SteeringFileType.CUSTOM

            content = file_path.read_text(encoding="utf-8")
            stat = file_path.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime)

            documents.append(
                SteeringDocument(
                    file_type=file_type,
                    file_path=file_path,
                    content=content,
                    last_modified=last_modified,
                )
            )

        return documents

    def get_steering_status(self) -> SteeringStatus:
        """Get status of steering documents.

        Returns:
            SteeringStatus object with current state
        """
        # Check if steering directory exists
        exists = self.steering_dir.exists()

        # List existing documents
        documents = self.list_steering_documents()

        # Find missing defaults
        default_types = [
            SteeringFileType.PRODUCT,
            SteeringFileType.TECH,
            SteeringFileType.STRUCTURE,
        ]
        existing_types = {doc.file_type for doc in documents}
        missing_defaults = [
            file_type for file_type in default_types if file_type not in existing_types
        ]

        # Get most recent modification time
        last_updated = None
        if documents:
            last_updated = max(doc.last_modified for doc in documents)

        return SteeringStatus(
            exists=exists,
            steering_dir=self.steering_dir,
            documents=documents,
            missing_defaults=missing_defaults,
            last_updated=last_updated,
        )

    def ensure_spec_dir_exists(self, feature_name: str) -> Path:
        """Ensure a spec directory exists for a feature.

        Args:
            feature_name: Name of the feature

        Returns:
            Path to the spec directory
        """
        spec_dir = get_spec_dir(feature_name, self.project_root)
        ensure_directory_exists(spec_dir)
        return spec_dir

    def write_spec_metadata(self, feature_name: str, metadata: SpecificationMetadata) -> None:
        """Write specification metadata to spec.json.

        Args:
            feature_name: Name of the feature
            metadata: Metadata to write
        """
        spec_dir = self.ensure_spec_dir_exists(feature_name)
        spec_file = spec_dir / "spec.json"

        spec_file.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")

    def read_spec_metadata(self, feature_name: str) -> SpecificationMetadata | None:
        """Read specification metadata from spec.json.

        Args:
            feature_name: Name of the feature

        Returns:
            SpecificationMetadata if file exists, None otherwise
        """
        spec_dir = get_spec_dir(feature_name, self.project_root)
        spec_file = spec_dir / "spec.json"

        if not spec_file.exists():
            return None

        data = json.loads(spec_file.read_text(encoding="utf-8"))
        return SpecificationMetadata(**data)

    def write_spec_file(self, feature_name: str, filename: str, content: str) -> None:
        """Write a file in the spec directory.

        Args:
            feature_name: Name of the feature
            filename: Name of the file (e.g., requirements.md)
            content: Content to write
        """
        spec_dir = self.ensure_spec_dir_exists(feature_name)
        file_path = spec_dir / filename
        file_path.write_text(content, encoding="utf-8")

    def read_spec_file(self, feature_name: str, filename: str) -> str | None:
        """Read a file from the spec directory.

        Args:
            feature_name: Name of the feature
            filename: Name of the file (e.g., requirements.md)

        Returns:
            File content if exists, None otherwise
        """
        spec_dir = get_spec_dir(feature_name, self.project_root)
        file_path = spec_dir / filename

        if not file_path.exists():
            return None

        return file_path.read_text(encoding="utf-8")

    def spec_file_exists(self, feature_name: str, filename: str) -> bool:
        """Check if a spec file exists.

        Args:
            feature_name: Name of the feature
            filename: Name of the file

        Returns:
            True if file exists, False otherwise
        """
        spec_dir = get_spec_dir(feature_name, self.project_root)
        return (spec_dir / filename).exists()

    def list_specs(self) -> list[str]:
        """List all feature specifications.

        Returns:
            List of feature names
        """
        from cc_sdd_mcp.utils.paths import get_specs_dir

        specs_dir = get_specs_dir(self.project_root)
        if not specs_dir.exists():
            return []

        return [d.name for d in specs_dir.iterdir() if d.is_dir() and (d / "spec.json").exists()]
