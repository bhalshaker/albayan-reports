import logging
from uuid import UUID
from jsonschema import validate, ValidationError
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
    try:
        # Get dyanamodb table for document creation requests
        document_creation_table = await get_dynamodb_table(config.processing_table)
        # Fetch the document creation request from DynamoDB
        document_creation_request = await DynamodbController.get_document_creation(
            issue_id, document_creation_table
        )
    except Exception as excep:
        # Log and return any exceptions encountered during the process
        logging.error(excep)
        # Return failure response
        return ReportGenerationSchema(False, excep)
    if not document_creation_request:
        # Return that the issue id was not found
        return ReportGenerationSchema(False, "Report creation record does not exist")
    try:
        # Fetch the report template information
        template_id = UUID(document_creation_request.get("report_template_id"))
        # Get dyanamodb table for document definitions
        document_definition_table = await get_dynamodb_table(config.definition_table)
        # Retrieve the document report template from DynamoDB
        document_report_template = await DynamodbController.get_template_info(
            template_id, document_definition_table
        )
    except Exception as excep:
        # Log and return any exceptions encountered during the process
        logging.error(excep)
        return ReportGenerationSchema(False, excep)
    if not document_report_template:
        # Return that the template in the request is not found
        return ReportGenerationSchema(
            False, "Refrencing template definition does not exist"
        )
    try:
        # Extract necessary information from the request and template
        report_output_format = str(
            document_creation_request.get("report_output_format")
        )
        template_format = str(document_report_template.get("template_file_type"))
        template_file_name = document_report_template.get("template_file")
        report_data = document_creation_request.get("report_data")
        # Validate the report data against the template schema
        validation_results = schema_validation(report_data, writter_default_schema)
        if not validation_results.is_valid:
            # Register that the creation was not valid
            DynamodbController.update_document_creation(
                issue_id, ProcessingStatus.FAILED, document_creation_table
            )
            # Return failure
            return ReportGenerationSchema(
                False, "Report data does not match report template definition"
            )
        # Process report creation based on the template format
        if template_format == "odf":
            # Call the function to create a Writer report
            create_writer_report(template_file_name, report_output_format, report_data)
            # Update the document creation status to completed
            DynamodbController.update_document_creation(
                issue_id, ProcessingStatus.SUCCESSFUL, document_creation_table
            )
            # Return success response
            return ReportGenerationSchema(True)
    except Exception as excep:
        # Log and return any exceptions encountered during the process
        logging.error(excep)
        return ReportGenerationSchema(False, excep)


def create_writer_report(
    report_issue_id: UUID,
    template_file_name: str,
    report_output_format: str,
    report_data: dict,
):
    """
    Create a Writer report using LibreOffice based on the provided template and data."""
    try:
        # Get LibreOffice instance
        libreoffice = get_libreoffice()
        # Open the template document
        document = libreoffice_utilites.open_template(
            libreoffice, template_file_name, config.templates_folder
        )
        # Fill in the document placeholder with the provided data
        if len(report_data.get("writer_placeholders")) > 0:
            document = libreoffice_utilites.writer_fill_placeholder_fields(
                document, report_data
            )
        # Fill in the document variables with the provided data
        if len(report_data.get("writer_variables")) > 0:
            document = libreoffice_utilites.writer_fill_variable_fields(
                document, report_data
            )
        # Replace images in the document with the provided data
        if len(report_data.get("writer_images").keys()) > 0:
            document = libreoffice_utilites.replace_writer_images(
                document, report_data.get("writer_images"), config.temp_folder
            )
        # Fill in the document tables with the provided data
        if len(report_data.get("writer_tables")) > 0:
            document = libreoffice_utilites.writer_fill_tables(document, report_data)
        # Save the document in the requested output format(s)
        if report_output_format == "PDF" or report_output_format == "PDF+OPENOFFICE":
            libreoffice_utilites.save_document(
                document,
                config.output_folder,
                str(report_issue_id),
                "writer_pdf_Export",
            )
        if (
            report_output_format == "OPENOFFICE"
            or report_output_format == "PDF+OPENOFFICE"
        ):
            libreoffice_utilites.save_document(
                document, config.output_folder, str(report_issue_id), "writer8"
            )
    except Exception as excep:
        # Log and raise any exceptions encountered during the process
        logging.error(excep)
        raise
