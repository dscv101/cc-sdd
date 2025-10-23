"""Data models for steering (project memory) documents."""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class SteeringFileType(str, Enum):
    """Types of steering documents."""

    PRODUCT = "product"
    TECH = "tech"
    STRUCTURE = "structure"
    CUSTOM = "custom"


class SteeringDocument(BaseModel):
    """Represents a steering document (project memory)."""

    file_type: SteeringFileType = Field(..., description="Type of steering document")
    file_path: Path = Field(..., description="Path to the steering document file")
    content: str = Field(..., description="Content of the steering document")
    last_modified: datetime = Field(
        default_factory=datetime.now, description="Last modification timestamp"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate content is not empty."""
        if not v or not v.strip():
            raise ValueError("Steering document content cannot be empty")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "file_type": "product",
                "file_path": ".kiro/steering/product.md",
                "content": "# Product Context\n\nThis is the product context...",
                "last_modified": "2025-01-01T12:00:00",
            }
        }


class SteeringConfig(BaseModel):
    """Configuration for steering documents."""

    kiro_dir: Path = Field(default=Path(".kiro"), description="Path to the .kiro directory")
    steering_dir: Path = Field(
        default=Path(".kiro/steering"), description="Path to the steering directory"
    )
    language: str = Field(
        default="en", description="Language code for templates (en, ja, zh-TW, etc.)"
    )
    default_files: list[SteeringFileType] = Field(
        default=[SteeringFileType.PRODUCT, SteeringFileType.TECH, SteeringFileType.STRUCTURE],
        description="Default steering files to create",
    )

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        """Validate language code."""
        supported = ["en", "ja", "zh-TW", "zh", "es", "pt", "de", "fr", "ru", "it", "ko", "ar"]
        if v not in supported:
            raise ValueError(f"Language {v} not supported. Supported: {supported}")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "kiro_dir": ".kiro",
                "steering_dir": ".kiro/steering",
                "language": "en",
                "default_files": ["product", "tech", "structure"],
            }
        }


class SteeringStatus(BaseModel):
    """Status of steering documents in a project."""

    exists: bool = Field(..., description="Whether steering directory exists")
    steering_dir: Path = Field(..., description="Path to steering directory")
    documents: list[SteeringDocument] = Field(
        default_factory=list, description="List of steering documents found"
    )
    missing_defaults: list[SteeringFileType] = Field(
        default_factory=list, description="Default files that are missing"
    )
    last_updated: datetime | None = Field(
        None, description="Most recent modification time across all documents"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "exists": True,
                "steering_dir": ".kiro/steering",
                "documents": [
                    {
                        "file_type": "product",
                        "file_path": ".kiro/steering/product.md",
                        "content": "# Product Context",
                        "last_modified": "2025-01-01T12:00:00",
                    }
                ],
                "missing_defaults": ["tech", "structure"],
                "last_updated": "2025-01-01T12:00:00",
            }
        }
