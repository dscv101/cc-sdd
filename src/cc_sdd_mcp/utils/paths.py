"""Utilities for path resolution and project discovery."""

from pathlib import Path


def find_project_root(start_path: Path | None = None) -> Path | None:
    """Find the project root directory.

    Searches upward from start_path for common project indicators:
    - .git directory
    - .kiro directory
    - pyproject.toml, package.json, etc.

    Args:
        start_path: Path to start searching from (defaults to current directory)

    Returns:
        Path to project root, or None if not found
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    # Indicators of a project root
    indicators = [
        ".git",
        ".kiro",
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
    ]

    # Search upward until we find a project root or hit filesystem root
    while current != current.parent:
        for indicator in indicators:
            if (current / indicator).exists():
                return current
        current = current.parent

    return None


def get_kiro_dir(project_root: Path | None = None) -> Path:
    """Get the .kiro directory path.

    Args:
        project_root: Project root path (will be auto-detected if None)

    Returns:
        Path to .kiro directory

    Raises:
        ValueError: If project root cannot be determined
    """
    if project_root is None:
        project_root = find_project_root()
        if project_root is None:
            # Default to current directory if no project root found
            project_root = Path.cwd()

    kiro_dir = project_root / ".kiro"
    return kiro_dir


def get_steering_dir(project_root: Path | None = None) -> Path:
    """Get the steering directory path.

    Args:
        project_root: Project root path (will be auto-detected if None)

    Returns:
        Path to .kiro/steering directory
    """
    kiro_dir = get_kiro_dir(project_root)
    return kiro_dir / "steering"


def get_specs_dir(project_root: Path | None = None) -> Path:
    """Get the specs directory path.

    Args:
        project_root: Project root path (will be auto-detected if None)

    Returns:
        Path to .kiro/specs directory
    """
    kiro_dir = get_kiro_dir(project_root)
    return kiro_dir / "specs"


def get_spec_dir(feature_name: str, project_root: Path | None = None) -> Path:
    """Get the directory path for a specific feature spec.

    Args:
        feature_name: Name of the feature
        project_root: Project root path (will be auto-detected if None)

    Returns:
        Path to .kiro/specs/{feature_name} directory
    """
    specs_dir = get_specs_dir(project_root)
    # Sanitize feature name
    safe_feature_name = feature_name.lower().replace(" ", "-")
    return specs_dir / safe_feature_name


def ensure_directory_exists(directory: Path) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Path to directory
    """
    directory.mkdir(parents=True, exist_ok=True)


def get_project_path_from_args(project_path: str | None = None) -> Path:
    """Get project root path from optional argument.

    Args:
        project_path: Optional project path string

    Returns:
        Resolved Path object
    """
    if project_path:
        return Path(project_path).resolve()

    # Try to find project root
    root = find_project_root()
    if root:
        return root

    # Default to current directory
    return Path.cwd()


def normalize_feature_name(feature_name: str) -> str:
    """Normalize a feature name to a safe directory name.

    Args:
        feature_name: Raw feature name

    Returns:
        Normalized feature name (lowercase, hyphens instead of spaces)
    """
    return feature_name.strip().lower().replace(" ", "-").replace("_", "-")
