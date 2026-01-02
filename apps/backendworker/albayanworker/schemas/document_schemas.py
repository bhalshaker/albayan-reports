from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ProcessingStatus(Enum):
    """
    An enumeration of processing statuses.
    """

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"


@dataclass
class SchemaValidationResponse:
    """Schema validation response dataclass."""

    is_valid: bool
    error: Optional[str] = None


@dataclass
class ReportGenerationSchema:
    """Report generation schema dataclass."""

    succesful: bool
    error: Optional[str] = None


# Default JSON schema for validating writer data
writter_default_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Writer Data Schema",
    "type": "object",
    "required": [
        "writer_placeholders",
        "writer_variables",
        "writer_images",
        "writer_tables",
    ],
    "properties": {
        "writer_placeholders": {
            "type": "array",
            "items": {
                "type": "object",
                "patternProperties": {"^.*$": {"type": "string"}},
                "description": "An object where keys are placeholder names and values are strings.",
            },
        },
        "writer_variables": {
            "type": "array",
            "items": {
                "type": "object",
                "patternProperties": {"^.*$": {"type": "string"}},
                "description": "An object where keys are variable names and values are strings.",
            },
        },
        "writer_images": {
            "type": "object",
            "patternProperties": {
                "^.*$": {
                    "type": "string",
                    "description": "Base64 encoded image string.",
                }
            },
        },
        "writer_tables": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["table_name", "content"],
                "properties": {
                    "table_name": {"type": "string"},
                    "content": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "patternProperties": {"^.*$": {"type": "string"}},
                        },
                    },
                    "footer": {
                        "type": "object",
                        "patternProperties": {"^.*$": {"type": "string"}},
                    },
                },
            },
        },
    },
}
