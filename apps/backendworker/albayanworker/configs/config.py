from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class Config:
    # Application environment (e.g., DEVELOPMENT, PRODUCTION)
    environment: str
    # AWS Related Configurations
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    dynamodb_endpoint: str
    definition_table: str
    processing_table: str
    # LibreOffice Configurations
    libreoffice_host: str
    libreoffice_port: int
    # Folders
    templates_folder: str
    output_folder: str
    temp_folder: str

    def create_directories_if_not_exists(self):
        """Creates a directory if it does not exist."""
        for path in [
            self.templates_folder,
            self.output_folder,
            self.temp_folder,
        ]:
            Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def from_env():
        return Config(
            environment=os.getenv("ENVIRONMENT", "DEVELOPMENT").upper(),
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "dummy"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "dummy"),
            dynamodb_endpoint=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000"),
            definition_table=os.getenv("DEFINITION_TABLE_NAME", "reports_definition"),
            processing_table=os.getenv("PROCESSING_TABLE_NAME", "reports_processing"),
            libreoffice_host=os.getenv("LIBREOFFICE_HOST", "localhost").lower(),
            libreoffice_port=int(os.getenv("LIBREOFFICE_PORT", "2002")),
            templates_folder=os.getenv("TEMPLATES_FOLDER", "/tmp/input"),
            output_folder=os.getenv("OUTPUT_FOLDER", "/tmp/output"),
            temp_folder=os.getenv("TEMP_FOLDER", "/tmp/albayanworker_temp"),
        )


config = Config.from_env()
