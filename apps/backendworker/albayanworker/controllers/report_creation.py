from albayanworker.schema.document_schemas import DocumentCreationRequestSchema
from albayanworker.dependancies.libreoffice import (
    create_prop,
    create_document_url,
    get_libreoffice,
)


def make_prop(name: str, value):
    """Helper function to create a UNO PropertyValue."""
    prop = create_prop()
    prop.Name = name
    prop.Value = value
    return prop


def create_report(request_data: DocumentCreationRequestSchema):
    """Creates a report based on the provided template and data."""
    # Implementation for report creation
    pass


def create_writer_report(report_data: dict):
    """Creates a report in Writer format."""
    # Implementation for writer report creation
    pass


def create_impress_report(report_data: dict):
    """Creates a report in Impress format."""
    # Implementation for impress report creation
    pass


def create_calc_report(report_data: dict):
    """Creates a report in Calc format."""
    # Implementation for calc report creation
    pass


def fill_variable_fields(document, data: dict):
    """Fills variable fields in the document with provided data."""
    # Get the text fields from the document
    document_fields = document.getTextFieldMaster()
    # Loop through the provided data and set the field values
    for key, value in data["variables"].items():
        # Construct the field name based on the key
        field_name = f"com.sun.star.text.FieldMaster.User.{key}"
        # Check if the field exists in the document
        if field_name in document_fields:
            # Get the field and set its content
            field = document_fields.getByName(field_name)
            field.setPropertyValue("Content", str(value))
    # Return the modified document
    return document


def fill_table_fields(document, data: dict):
    """Fills table fields in the document with provided data."""
    # Implementation for filling table fields
    pass


def fill_image_fields(document, data: dict):
    """Fills image fields in the document with provided data."""
    # Implementation for filling image fields
    pass


def fill_placeholder_fields(document, data: dict):
    """Fills placeholder fields in the document with provided data."""
    # Implementation for filling placeholder fields
    pass


def export_to_pdf(document, output_file: str):
    """Exports the document to PDF format."""
    # Implementation for exporting to PDF
    pass


def save_document(document, document_extention: str, output_file: str):
    """Saves the document with the given file name."""
    # Implementation for saving the document
    pass


def open_template(template_path: str):
    """Opens the template document from the given path."""
    args = [make_prop("Hidden", True)]
    url = create_document_url(template_path)
    return get_libreoffice().loadComponentFromURL(url, "_blank", 0, args)
