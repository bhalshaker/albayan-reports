from dataclasses import dataclass
import os

@dataclass
class Config:
    # Application environment (e.g., DEVELOPMENT, PRODUCTION)
    environment: str
    # AWS Related Configurations
    aws_region: str
    definition_table : str
    processing_table : str
    # LibreOffice Configurations
    libreoffice_host: str
    libreoffice_port : int
    # Kafka Configurations
    kafka_topic: str
    kafka_bootstrap_servers: str
    kafka_group_id: str

    @staticmethod
    def from_env():
        return Config(
            environment=os.getenv("ENVIRONMENT", "DEVELOPMENT").upper(),
            aws_region=os.getenv("AWS_REGION", "us-west-2"),
            definition_table=os.getenv("DEFINITION_TABLE_NAME", "my_table"),
            processing_table=os.getenv("PROCESSING_TABLE_NAME", "my_table"),
            libreoffice_host=os.getenv("LIBREOFFICE_HOST", "localhost").lower(),
            libreoffice_port=int(os.getenv("LIBREOFFICE_PORT", "2002")),
            kafka_topic=os.getenv("KAFKA_TOPIC", "albayan_topic"),
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            kafka_group_id=os.getenv("KAFKA_GROUP_ID", "libreoffice_group"),
        )
    
config=Config.from_env()