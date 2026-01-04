import logging
from uuid import UUID
from jsonschema import validate, ValidationError
import asyncio
from albayanworker.dependancies.dyanomodb import get_dynamodb_table
from albayanworker.dependancies.libreoffice import get_libreoffice
from albayanworker.schemas.document_schemas import (
    SchemaValidationResponse,
    ReportGenerationSchema,
    ProcessingStatus,
    writter_default_schema,
)
from albayanworker.controllers.dynamodb_controlller import DynamodbController
from albayanworker.configs.config import config
from albayanworker.utilities import libreoffice_utilites

logger = logging.getLogger(__name__)


def schema_validation(
    schema_instance: dict, validation_schema: dict
) -> SchemaValidationResponse:
    """
    Validates a given schema instance against a provided validation schema.
    """
    try:
        # Validate the schema instance against the validation schema
        validate(instance=schema_instance, schema=validation_schema)
        # If validation is successful, return a positive response
        return SchemaValidationResponse(True)
    except ValidationError as e:
        # If validation fails, return a negative response with the error message
        return SchemaValidationResponse(False, e.message)


async def process_report_creation(issue_id: UUID) -> ReportGenerationSchema:
    """
    Process the report creation request based on the provided issue ID.
    """
    logger.info("Starting process_report_creation for issue_id=%s", issue_id)
    # Retrieve document creation request
    try:
        document_creation_table = await get_dynamodb_table(config.processing_table)
        document_creation_request = await DynamodbController.get_document_creation(
            issue_id, document_creation_table
        )
    except Exception as excep:
        return ReportGenerationSchema(False, f"Failed to fetch request: {excep}")

    if not document_creation_request:
        return ReportGenerationSchema(False, "Report creation record does not exist")

    # Retrieve the template information
    try:
        template_id = UUID(document_creation_request.get("report_template_id"))
        document_definition_table = await get_dynamodb_table(config.definition_table)
        document_report_template = await DynamodbController.get_template_info(
            template_id, document_definition_table
        )
    except Exception as excep:
        return ReportGenerationSchema(False, f"Failed to fetch template: {excep}")

    if not document_report_template:
        logger.error(
            "Referencing template definition does not exist for issue_id=%s, template_id=%s",
            issue_id,
            document_creation_request.get("report_template_id"),
        )
        return ReportGenerationSchema(
            False, "Refrencing template definition does not exist"
        )

    # Validate input and execute creation flow
    try:
        report_output_format = str(
            document_creation_request.get("report_output_format")
        )
        template_format = str(document_report_template.get("template_file_type"))
        template_file_name = document_report_template.get("template_file")
        report_data = document_creation_request.get("report_data")

        logger.info("Validating report data for issue_id=%s against schema", issue_id)
        validation_results = schema_validation(report_data, writter_default_schema)
        if not validation_results.is_valid:
            logger.warning(
                "Validation failed for issue_id=%s: %s",
                issue_id,
                validation_results.message,
            )
            # Register that the creation was not valid
            try:
                await DynamodbController.update_document_creation(
                    issue_id, ProcessingStatus.FAILED, document_creation_table
                )
            except Exception:
                logger.exception(
                    "Failed to update document_creation status for issue_id=%s",
                    issue_id,
                )
            return ReportGenerationSchema(
                False, "Report data does not match report template definition"
            )

        # Process based on template format
        if template_format == "odf":
            # Normalize and validate output format before creating report
            requested_format = (
                str(report_output_format).strip().upper()
                if report_output_format is not None
                else ""
            )
            if requested_format in ("", "NONE", "NULL", "UNDEFINED"):
                logger.warning(
                    "No valid report_output_format provided for issue_id=%s — defaulting to 'PDF'",
                    issue_id,
                )
                requested_format = "PDF"
            await create_writer_report(
                issue_id, template_file_name, requested_format, report_data
            )
            try:
                await DynamodbController.update_document_creation(
                    issue_id, ProcessingStatus.SUCCESSFUL, document_creation_table
                )
            except Exception:
                logger.exception(
                    "Failed to update document_creation status to SUCCESSFUL for issue_id=%s",
                    issue_id,
                )
            return ReportGenerationSchema(True)

        return ReportGenerationSchema(
            False, f"Unsupported template format: {template_format}"
        )

    except Exception as excep:
        return ReportGenerationSchema(False, str(excep))


async def create_writer_report(
    report_issue_id: UUID,
    template_file_name: str,
    report_output_format: str,
    report_data: dict,
):
    """
    Create a Writer report using LibreOffice based on the provided template and data."""
    try:
        # Get LibreOffice instance (async)
        try:
            libreoffice = await get_libreoffice()
        except Exception:
            logger.exception(
                "Failed to obtain LibreOffice instance for issue_id=%s", report_issue_id
            )
            raise

        # Normalize format (accept uppercase form) to avoid branch misses
        normalized_format = (
            str(report_output_format).strip().upper()
            if report_output_format is not None
            else ""
        )
        if normalized_format in ("", "NONE", "NULL", "UNDEFINED"):
            normalized_format = "PDF"
        try:
            logger.info(
                "Processing writer document in worker thread for issue_id=%s (format=%s)",
                report_issue_id,
                normalized_format,
            )
            await asyncio.to_thread(
                libreoffice_utilites.process_writer_document_and_save,
                libreoffice,
                template_file_name,
                str(report_issue_id),
                normalized_format,
                report_data,
                config.templates_folder,
                config.temp_folder,
                config.output_folder,
            )
        except Exception:
            logger.exception(
                "Failed to process and save document for issue_id=%s", report_issue_id
            )
            raise
    except Exception as excep:
        # Log and raise any exceptions encountered during the process
        logger.exception(
            "Error while creating writer report for issue_id=%s: %s",
            report_issue_id,
            excep,
        )
        raise
