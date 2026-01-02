import base64
import pathlib
import uno
import uuid


def initilize_libreoffice_sync(libreoffice_host: str, libreoffice_port: int):
    """
    Synchronous helper function to initialize LibreOffice connection.
    """
    # Get the local UNO component context
    localContext = uno.getComponentContext()
    # Create a UNO URL resolver to connect to the remote LibreOffice instance
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext
    )
    # Resolve the connection to the LibreOffice instance
    context = resolver.resolve(
        f"uno:socket,host={libreoffice_host},port={str(libreoffice_port)};urp;StarOffice.ComponentContext"
    )
    # Get the LibreOffice desktop service
    libreoffice = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", context
    )
    return libreoffice


def create_prop():
    """Creates and returns a UNO PropertyValue struct."""
    return uno.createUnoStruct("com.sun.star.beans.PropertyValue")


def create_document_url(file_path: str) -> str:
    """Converts a local file path to a LibreOffice-compatible file URL."""
    return uno.systemPathToFileUrl(file_path)


def save_document(document, output_folder: str, report_id: str, filter_name: str):
    """
    Save the given LibreOffice document to a new file URL with the specified filter.

    Args:
        document: The LibreOffice document to be saved.
        output_folder (str): The folder where the document will be saved.
        report_id (str): The report identifier to be used in the file name.
        filter_name (str): The filter name to be used for saving the document.
    Returns:
        str: The name of the saved file.
    """
    # Determine the file extension based on the filter name
    file_extension = determince_extention_from_filter_name(filter_name)
    # Constuct file name based on report id and extension
    file_name = report_id + file_extension
    try:
        # Create the full file path and URL
        full_path = pathlib.Path(output_folder + report_id + file_name)
        new_file_url = create_document_url(str(full_path))
        # Ensure the output directory exists
        pathlib.Path(output_folder + report_id + file_name).parent.mkdir(
            parents=True, exist_ok=True
        )
        # Create a PropertyValue for the filter name
        filter_prop = create_prop()
        filter_prop.Name = "FilterName"
        filter_prop.Value = filter_name

        # Save the document to the new file URL with the specified filter
        document.storeToURL(new_file_url, (filter_prop,))
        return file_name
    except Exception as e:
        raise e


def writer_fill_tables(document, data: dict):
    """Fills tables in a writer document with provided data."""
    # If there are no writer tables, return the document as is
    writer_tables = data.get("writer_tables", [])
    if not writer_tables:
        return document
    # Get all tables in the document
    tables = document.getTextTables()
    # If there are no tables in the document, return as is
    if tables.getCount() == 0:
        return document
    for table in tables:
        table_name = table.getName()
        # Check if the table is in the provided writer tables and skip if not
        if table_name not in [writer_table["name"] for writer_table in writer_tables]:
            continue
        # Get the corresponding data for the table
        table_data = next(
            (
                writer_table
                for writer_table in writer_tables
                if writer_table["name"] == table_name
            ),
            None,
        )
        # Get the original number of rows in the table
        orginal_table_rows = table.getRows().getCount()
        # Determine the number of footer rows
        footer_rows = 0 if orginal_table_rows <= 2 else orginal_table_rows - 2
        # If there is no data to fill, skip to the next table
        if not table_data or len(table_data.get("content", [])) == 0:
            continue
        # Create a mapping of column headers to their respective column names
        columns_header_map = generate_writer_table_columns_map(table)
        # Insert empty rows if needed
        table = insert_writer_table_rows_before_footer(
            table, len(table_data.get("content", []))
        )
        # Fill the table rows with data
        table = fill_writer_table_rows(table, table_data, columns_header_map)
        # Fill the footer placeholder if exists
        table = fill_writer_table_footer(table, table_data, footer_rows)


def generate_writer_table_columns_map(table) -> dict:
    """Generates a mapping of column headers to their respective column names."""
    columns = table.getColumns()
    columns_header_map = {}
    for column_index in range(columns.getCount()):
        cell_name = chr(ord("A") + column_index)
        cell = table.getCellByName(cell_name + "1")
        columns_header_map[cell.String] = cell_name
    return columns_header_map


def fill_writer_table_rows(table, table_data: dict, columns_header_map: dict):
    """Fills the rows of a writer table with the provided data."""
    rows = table.getRows()
    existing_row_count = rows.getCount()
    data_rows = table_data.get("data", [])
    # Add new rows if there are more data rows than existing rows
    if len(data_rows) > existing_row_count - 1:
        rows_to_add = len(data_rows) - (existing_row_count - 1)
        rows.insertByIndex(existing_row_count, rows_to_add)
    # Fill the table with data
    for row_index, data_row in enumerate(data_rows):
        for column_header, cell_name in columns_header_map.items():
            cell = table.getCellByName(cell_name + str(row_index + 2))
            cell_value = data_row.get(column_header, "")
            cell.String = str(cell_value)
    return table


def fill_writer_table_footer(table, table_data: dict, footer_rows):
    """Fills the footer of a writer table if footer data is provided."""
    footer_data = table_data.get("footer", {})
    if not footer_data:
        return table
    last_row_index = table.getRows().getCount()
    footer_start = last_row_index - footer_rows
    for row_index in range(footer_start, last_row_index):
        raw = raw.getRows().getByIndex(row_index)
        number_of_cells = raw.getCount()
        # To access the content of those cells:
        for cell_index in range(number_of_cells):
            cell = raw.getCellByIndex(cell_index)
            if cell.String in footer_data.keys():
                cell.String = footer_data.get(cell.String)
    return table


def insert_writer_table_rows_before_footer(table, data_rows: int):
    """Inserts empty rows before the footer row in a writer table."""
    # If there are no data rows to insert, return the table as is
    if data_rows == 0:
        return table
    # Insert the required number of rows before the footer
    table.getRows().insertByIndex(1, data_rows - 1)
    # Return the modified table
    return table


def generate_footer_rows_map(
    number_of_rows: int, number_of_columns: int, table
) -> dict:
    """Generates a mapping for footer rows in a table."""
    footer_rows_map = {}
    for row_index in range(number_of_rows):
        for column_index in range(number_of_columns):
            cell_name = chr(ord("A") + column_index) + str(row_index + 1)
            cell = table.getCellByName(cell_name)
            footer_rows_map[cell.String] = cell_name
    return footer_rows_map


def determince_extention_from_filter_name(filter_name: str) -> str:
    """Determines the file extension based on the given filter name."""
    # Extension mapping for various filter names
    filter_extension_map = {
        "writer_pdf_Export": ".pdf",
        "calc_pdf_Export": ".pdf",
        "impress_pdf_Export": ".pdf",
        "writer8": ".odt",
        "calc8": ".ods",
        "Rich Text Format": ".rtf",
        "impress8": ".odp",
        "MS Word 2007 XML": ".docx",
        "MS Word 97": ".doc",
        "MS Excel 2007 XML": ".xlsx",
        "Calc MS Excel 97": ".xls",
        "MS PowerPoint 2007 XML": ".pptx",
        "Calc MS Excel 2007 XML": ".xlsx",
    }
    # Return the corresponding file extension or an empty string if not found
    return filter_extension_map.get(filter_name, "")


def writer_fill_variable_fields(document, data: dict):
    """Fills variable fields in a writer document with provided data."""
    # If there are no writer variables, return the document as is
    if not data.get("writer_variables", []):
        return document
    # Get the text fields from the document
    document_fields = document.getTextFieldMaster()
    # Loop through the provided data and set the field values
    for variable_name, value in data.get("writer_variables", {}).items():
        # Construct the field name based on the variable_name
        field_name = f"com.sun.star.text.FieldMaster.User.{variable_name}"
        # Check if the field exists in the document
        if field_name in document_fields:
            # Get the field and set its content
            field = document_fields.getByName(field_name)
            field.setPropertyValue("Content", str(variable_name))
    # Return the modified document
    return document


def writer_fill_placeholder_fields(document, data: dict):
    """Fills placeholder fields in a writer document with provided data."""
    # Get the placeholders from the data
    placeholders = data.get("placeholders", [])
    # If there are no placeholders, return the document as is
    if not placeholders:
        return document
    # Create a search descriptor for finding and replacing placeholders
    search_descriptor = document.createSearchDescriptor()
    # Loop through each placeholder and replace it in the document
    for placeholder_dict in placeholders:
        try:
            # Safely unpack the single key-value pair from the dictionary
            placeholder, value = list(placeholder_dict.items())[0]
        except IndexError:
            # If the dictionary is empty, skip to the next one
            continue
        # Set the search and replace strings
        search_descriptor.SearchString = placeholder
        search_descriptor.ReplaceString = str(value)
        # Perform the replace operation
        document.replaceAll(search_descriptor)
    # Return the modified document
    return document


def open_template(libreoffice: any, template_path: str):
    """Opens the template document from the given path."""
    # Create properties for opening the document in hidden mode
    args = [create_prop("Hidden", True)]
    # Create the document URL from the template path
    url = create_document_url(template_path)
    # Load and return the document
    return libreoffice.loadComponentFromURL(url, "_blank", 0, args)


def replace_writer_images(document, images_data, temp_folder):
    if images_data is None:
        return document
    # Creater a Graphic Query provider to create new images
    component_context = uno.getComponentContext()
    query_provider = component_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.graphic.GraphicProvider", component_context
    )
    # Get a list of all graphics in the writer document
    images = document.getGraphicObjects()
    # Get a list of all images name
    image_names = images.getElementNames()
    # Loop throught list of images to be changed names
    for image_name in images_data.keys():
        # If one of the images in the document has a matching name then proceed with changing the images
        if image_name in image_names:
            # Get image object in the document
            image = images.getByName(image_name)
            # Create a temporary image file
            temp_image_url = base64_string_to_file(temp_folder, images_data[image_name])
            # Create a new image object
            prop = create_prop()
            prop.Name = "URL"
            prop.Value = temp_image_url
            new_image = query_provider.queryGraphic((prop,))
            # Replace the value of the current image object with the new one
            image.Graphic = new_image
    return document


def base64_string_to_file(file_path: str, base64_string: str):
    """
    Convert a base64 encoded string to a file.

    Args:
        base64_string (str): The base64 encoded string.

    Returns:
        str: file path.
    """
    # Decode the base64 string
    file_data = base64.b64decode(base64_string)
    # Determine the file extension
    file_extension = determine_mime_extension(base64_string)
    # Create a unique file path
    file_path_obj = pathlib.Path(file_path + uuid.uuid4() + file_extension)
    try:
        # Create directories if they do not exist
        file_path_obj.parent.mkdir(parents=True, exist_ok=True)
        # Write the decoded data to the file
        with open(file_path_obj, "wb") as file:
            file.write(file_data)
        # Return the file path as a string
        return str(file_path_obj)
    except Exception as e:
        raise e


def determine_mime_extension(base64_string):
    """
    Determine the MIME type and file extension from a base64 encoded string.

    Args:
        base64_string (str): The base64 encoded string.
    Returns:
        str: The file extension corresponding to the MIME type.
    """
    # Decode base64 string to bytes
    file_bytes = base64.b64decode(base64_string)
    # Grap the first few bytes to identify the file type
    header = file_bytes[:12]
    # Identify the file type based on the header bytes and return extension
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    elif header.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    elif header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return ".gif"
    elif header.startswith(b"BM"):
        return ".bmp"
    elif header.startswith(b"II*\x00") or header.startswith(b"MM\x00*"):
        return ".tiff"
    elif header.startswith(b"RIFF") and b"WEBP" in header:
        return ".webp"
    else:
        return ""
