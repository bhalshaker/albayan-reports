import base64
import pathlib
import uuid
import uno
import re
import logging

logger = logging.getLogger(__name__)


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


def create_document_url(file_path) -> str:
    """Converts a local file path (str or pathlib.Path) to a LibreOffice-compatible file URL.

    UNO expects a native string path; ensure we pass a string to avoid
    `pyuno.systemPathToFileUrl: expecting one string argument` errors."""
    return uno.systemPathToFileUrl(str(file_path))


def save_document(document, output_folder: str, report_id: str, filter_name: str):
    """
    Save the given LibreOffice document to a new file URL with the specified filter.

    Writes files to: <output_folder>/<report_id>/<report_id><ext>

    Args:
        document: The LibreOffice document to be saved.
        output_folder (str): The base folder where the document will be saved.
        report_id (str): The report identifier to be used in the file name and folder.
        filter_name (str): The filter name to be used for saving the document.
    Returns:
        str: The full path of the saved file on disk.
    """
    # Determine the file extension based on the filter name
    file_extension = determince_extention_from_filter_name(filter_name)
    # Construct file name based on report id and extension
    file_name = report_id + file_extension
    try:
        # Construct the target directory and file path using pathlib (safe join)
        target_dir = pathlib.Path(output_folder)
        target_dir.mkdir(parents=True, exist_ok=True)
        full_path = target_dir / file_name

        # Log where we are going to save
        logger.debug("Saving document to path=%s (filter=%s)", full_path, filter_name)

        # Create a PropertyValue for the filter name
        filter_prop = create_prop()
        filter_prop.Name = "FilterName"
        filter_prop.Value = filter_name

        # Convert to a UNO file URL and save
        new_file_url = create_document_url(str(full_path))
        document.storeToURL(new_file_url, (filter_prop,))

        # Verify file was created (best-effort check)
        try:
            if full_path.exists():
                logger.info("Document saved to %s", full_path)
            else:
                logger.warning(
                    "Document storeToURL did not produce a file at %s", full_path
                )
        except Exception:
            logger.debug("Could not stat saved file at %s", full_path)

        return str(full_path)
    except Exception as e:
        logger.exception("Failed to save document for report_id=%s: %s", report_id, e)
        raise


def writer_fill_tables(document, data: dict):
    """Fills tables in a writer document with provided data."""
    # If there are no writer tables, return the document as is
    writer_tables = data.get("writer_tables", [])
    logger.info(writer_tables)
    if not writer_tables:
        logger.info("No tables found")
        return document
    # Get all tables in the document
    tables = document.getTextTables()
    # If there are no tables in the document, return as is
    if tables.getCount() == 0:
        logger.info("No tables in document")
        return document
    for table in tables:
        table_name = table.getName()
        # Check if the table is in the provided writer tables and skip if not
        if table_name not in [
            writer_table["table_name"] for writer_table in writer_tables
        ]:
            logger.info(
                f"Table {table_name} has no matching record in writer_table array {writer_tables}"
            )
            continue
        # Get the corresponding data for the table
        table_data = next(
            (
                writer_table
                for writer_table in writer_tables
                if writer_table["table_name"] == table_name
            ),
            None,
        )
        logger.info(f"Table data {table_data}")
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
    return document


def generate_writer_table_columns_map(table) -> dict:
    """Generates a mapping of column headers to their respective column names."""
    # Get all columns in the table
    columns = table.getColumns()
    # Create a mapping of column headers to column names
    columns_header_map = {}
    for column_index in range(columns.getCount()):
        cell_name = chr(ord("A") + column_index)
        header_text = cell_name
        try:
            cell = table.getCellByName(cell_name + "1")
            # Try straightforward string first
            try:
                header_text = cell.String if isinstance(cell.String, str) else ""
                header_text = header_text.strip() if header_text else ""
            except Exception:
                header_text = ""

            # If blank, try the cell's text content which may include anchor text
            if not header_text:
                try:
                    t = cell.getText()
                    header_text = t.getString() if hasattr(t, "getString") else ""
                    header_text = header_text.strip() if header_text else ""
                except Exception:
                    header_text = ""

            # If still blank, inspect contained text fields and use their anchor text
            if not header_text:
                try:
                    fields = cell.getTextFields()
                    try:
                        enum = fields.createEnumeration()
                        parts = []
                        while enum.hasMoreElements():
                            ff = enum.nextElement()
                            try:
                                anchor = ff.getAnchor()
                                try:
                                    part = anchor.getString()
                                    if part:
                                        parts.append(part)
                                except Exception:
                                    pass
                            except Exception:
                                pass
                        if parts:
                            header_text = " ".join(parts).strip()
                    except Exception:
                        pass
                except Exception:
                    pass

            # Final fallback
            if not header_text:
                header_text = cell_name
        except Exception:
            header_text = cell_name
        columns_header_map[header_text] = cell_name
    return columns_header_map


def fill_writer_table_rows(table, table_data: dict, columns_header_map: dict):
    """Fills the rows of a writer table with the provided data."""
    try:
        rows = table.getRows()
        existing_row_count = rows.getCount()
    except Exception:
        logger.debug("fill_writer_table_rows: could not access table rows")
        return table

    # Get data rows to be filled (accept 'data' or 'content')
    data_rows = table_data.get("data") or table_data.get("content") or []
    if not data_rows:
        logger.debug(
            "fill_writer_table_rows: no data rows present in table_data; keys=%s",
            list(table_data.keys()),
        )

    # Add new rows if there are more data rows than existing rows (accounting for header)
    try:
        if len(data_rows) > (existing_row_count - 1):
            rows_to_add = len(data_rows) - (existing_row_count - 1)
            if rows_to_add > 0:
                rows.insertByIndex(existing_row_count, rows_to_add)
                logger.debug(
                    "fill_writer_table_rows: inserted %s rows (existing=%s, needed=%s)",
                    rows_to_add,
                    existing_row_count,
                    len(data_rows),
                )
    except Exception:
        logger.exception("fill_writer_table_rows: failed while inserting rows")

    # Fill the table with data.
    for row_index, data_row in enumerate(data_rows):
        row_written = False
        for column_header, value in data_row.items():
            try:
                # Prefer header-text -> column mapping
                cell_letter = columns_header_map.get(column_header)
                # Accept single-letter column names as direct input
                if (
                    not cell_letter
                    and isinstance(column_header, str)
                    and len(column_header) == 1
                    and column_header.isalpha()
                ):
                    cell_letter = column_header.upper()

                # If still not found, attempt fuzzy matching against headers
                if not cell_letter:
                    try:
                        key_low = str(column_header).strip().lower()
                        for hdr, letter in columns_header_map.items():
                            try:
                                hdr_low = str(hdr).strip().lower()
                                if not hdr_low:
                                    continue
                                # exact containment (header contains key or key in header)
                                if key_low in hdr_low or hdr_low in key_low:
                                    cell_letter = letter
                                    break
                                # token overlap
                                if set(hdr_low.split()) & set(key_low.split()):
                                    cell_letter = letter
                                    break
                            except Exception:
                                continue
                    except Exception:
                        pass

                if not cell_letter:
                    logger.debug(
                        "fill_writer_table_rows: no column mapping for header '%s' (row %s); available_headers=%s",
                        column_header,
                        row_index,
                        list(columns_header_map.keys()),
                    )
                    continue

                cell_name = f"{cell_letter}{row_index + 2}"
                try:
                    cell = table.getCellByName(cell_name)
                    cell.String = str(value) if value is not None else ""
                    row_written = True
                    any_written = True
                except Exception:
                    logger.debug(
                        "fill_writer_table_rows: failed to set cell %s for row %s",
                        cell_name,
                        row_index,
                    )
                    continue
            except Exception:
                logger.exception(
                    "fill_writer_table_rows: unexpected error while filling row %s",
                    row_index,
                )
                continue
        if not row_written:
            logger.debug(
                "fill_writer_table_rows: no values written for row %s (data_row=%s)",
                row_index,
                data_row,
            )

    return table


def fill_writer_table_footer(table, table_data: dict, footer_rows: int):
    footer_data = table_data.get("footer", {})
    if not footer_data or not table:
        return table

    try:
        # Get all cell names (e.g., ['A1', 'B1', 'A2'...])
        cell_names = table.getCellNames()
        rows_count = table.getRows().getCount()

        # We only want to process cells in the last 'footer_rows'
        # To do this safely, we find the starting letter/number for the footer
        footer_start_row = rows_count - footer_rows + 1

        for name in cell_names:
            match = re.search(r"\d+$", name)
            if not match:
                continue

            row_num = int(match.group())

            # Only process if this cell is in the footer section
            if row_num >= footer_start_row:
                cell = table.getCellByName(name)
                cell_text = cell.getString()
                replaced = False
                new_text = cell_text
                for key, value in footer_data.items():
                    if key in new_text:
                        new_text = new_text.replace(key, str(value))
                        replaced = True

                if replaced:
                    cell.setString(new_text)

    except Exception:
        pass

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
    # Validate input
    writer_variables = data.get("writer_variables") if isinstance(data, dict) else None
    if not writer_variables:
        return document
    # Get the text fields from the document (guard against unexpected errors)
    try:
        document_fields = document.getTextFieldMasters()
    except Exception:
        return document

    # Try to obtain a safe list of field names to avoid calling __contains__ on a
    # UNO object (which can trigger unsafe behaviour in some pyuno versions).
    try:
        field_names = list(document_fields.getElementNames())
    except Exception:
        field_names = None
    if not field_names:
        return document
    # Normalize writer_variables to an iterable of (name, value) pairs
    items = []
    if isinstance(writer_variables, dict):
        items = list(writer_variables.items())
    elif isinstance(writer_variables, list):
        for entry in writer_variables:
            if isinstance(entry, dict):
                items.extend(entry.items())

    for variable_name, value in items:
        pattern = rf".{re.escape(variable_name)}$"
        matching_variables = [
            field for field in field_names if re.search(pattern, field)
        ]
        if not matching_variables:
            continue
        for matching_variable in matching_variables:
            # First attempt to fetch the field by name; separate getByName and set ops
            try:
                try:
                    field = document_fields.getByName(matching_variable)
                except Exception as e:
                    continue
                try:
                    field.setPropertyValue("Content", str(value))
                except Exception:
                    try:
                        setattr(field, "Content", str(value))
                    except Exception:
                        continue
            except Exception:
                continue
    return document


def writer_fill_placeholder_fields(document, data: dict):
    """Fills placeholder fields in a writer document with provided data."""
    # Get the placeholders from the data
    placeholders = data.get("writer_placeholders", [])
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


def update_all_text_fields(doc, return_samples=False):
    """Update all text fields in a document (safe, returns number updated)."""

    # Helper to read a sample of fields for debugging
    def _sample_fields(fields_enum, limit=10):
        samples = []
        try:
            i = 0
            while fields_enum.hasMoreElements() and i < limit:
                f = fields_enum.nextElement()
                info = {}
                # Best-effort: implementation name / repr
                try:
                    info["repr"] = repr(f)
                except Exception:
                    info["repr"] = "<unreprable>"
                try:
                    impl = f.getImplementationName()
                    info["impl"] = impl
                except Exception:
                    info["impl"] = None
                # Try to get a presentable value
                val = None
                try:
                    val = f.getPropertyValue("Content")
                except Exception:
                    try:
                        val = getattr(f, "Content", None)
                    except Exception:
                        val = None
                # Truncate large strings
                try:
                    if isinstance(val, str) and len(val) > 120:
                        val = val[:120] + "..."
                except Exception:
                    pass
                info["value"] = val
                samples.append(info)
                i += 1
        except Exception:
            pass
        return samples

    try:
        fields = doc.getTextFields()
    except Exception:
        logger.debug("update_all_text_fields: no text fields present or failed")
        if return_samples:
            return 0, [], []
        return 0

    # Log + collect a pre-update sample for debugging
    pre_sample = []
    try:
        try:
            pre_enum = fields.createEnumeration()
            pre_sample = _sample_fields(pre_enum, limit=10)
            logger.debug("update_all_text_fields: pre-update sample=%s", pre_sample)
        except Exception:
            logger.debug("update_all_text_fields: failed to sample pre-update fields")
    except Exception:
        pass

    updated = 0
    try:
        enum = fields.createEnumeration()
        while enum.hasMoreElements():
            f = enum.nextElement()
            try:
                if hasattr(f, "update"):
                    f.update()
                    updated += 1
            except Exception:
                # ignore per-field update failures
                continue
    except Exception:
        logger.debug("update_all_text_fields: could not enumerate fields")

    # Best-effort refresh
    try:
        if hasattr(doc, "refresh"):
            doc.refresh()
    except Exception:
        try:
            controller = doc.getCurrentController()
            if hasattr(controller, "getFrame"):
                frame = controller.getFrame()
                if hasattr(frame, "repaint"):
                    frame.repaint()
        except Exception:
            pass

    # Try a Dispatch-based update as a stronger fallback that forces layout
    try:
        try:
            dispatched = dispatch_update_fields(doc)
            logger.debug(
                "update_all_text_fields: dispatch_update_fields result=%s", dispatched
            )
        except Exception:
            logger.exception("update_all_text_fields: dispatch_update_fields failed")
    except Exception:
        pass

    # Log + collect a post-update sample for debugging
    post_sample = []
    try:
        try:
            post_enum = fields.createEnumeration()
            post_sample = _sample_fields(post_enum, limit=10)
            logger.debug("update_all_text_fields: post-update sample=%s", post_sample)
        except Exception:
            logger.debug("update_all_text_fields: failed to sample post-update fields")
    except Exception:
        pass

    logger.debug("update_all_text_fields: updated %s fields", updated)
    if return_samples:
        return updated, pre_sample, post_sample
    return updated


def dispatch_update_fields(doc) -> bool:
    """Use DispatchHelper to force-update fields and layout in the document."""
    try:
        # Get the frame from the document's current controller
        try:
            frame = doc.getCurrentController().getFrame()
        except Exception:
            logger.debug("dispatch_update_fields: no frame available")
            return False

        # Obtain the local component context and DispatchHelper
        try:
            ctx = uno.getComponentContext()
            smgr = ctx.ServiceManager
            dispatcher = smgr.createInstanceWithContext(
                "com.sun.star.frame.DispatchHelper", ctx
            )
        except Exception:
            logger.exception("dispatch_update_fields: failed to create DispatchHelper")
            return False

        # Dispatch UpdateFields and UpdateAll commands
        try:
            dispatcher.executeDispatch(frame, ".uno:UpdateFields", "", 0, ())
        except Exception:
            logger.debug(
                "dispatch_update_fields: .uno:UpdateFields dispatch failed, continuing"
            )
        try:
            dispatcher.executeDispatch(frame, ".uno:UpdateAll", "", 0, ())
        except Exception:
            logger.debug("dispatch_update_fields: .uno:UpdateAll dispatch failed")

        logger.debug("dispatch_update_fields: dispatched update commands")
        return True
    except Exception:
        logger.exception("dispatch_update_fields: unexpected error")
        return False


def replace_text_field_instances_with_concrete_text(doc, variables):
    """Replace text field instances linked to variable masters with plain text."""
    try:
        # Normalize variables to a dict
        vars_map = {}
        if isinstance(variables, dict):
            vars_map = variables
        elif isinstance(variables, list):
            for e in variables:
                if isinstance(e, dict):
                    vars_map.update(e)
        if not vars_map:
            logger.debug("replace_text_field_instances: no variables provided")
            return 0

        # Gather masters that match variable names and their new content
        try:
            masters = doc.getTextFieldMasters()
            master_names = list(masters.getElementNames())
        except Exception:
            logger.debug("replace_text_field_instances: no masters present")
            return 0

        master_map = {}
        for var_name, var_value in vars_map.items():
            pattern = f".{re.escape(var_name)}$"
            matches = [m for m in master_names if re.search(pattern, m)]
            for m in matches:
                try:
                    master_obj = masters.getByName(m)
                    try:
                        content = master_obj.getPropertyValue("Content")
                    except Exception:
                        try:
                            content = getattr(master_obj, "Content", None)
                        except Exception:
                            content = None
                    master_map[m] = (
                        str(var_value) if var_value is not None else str(content)
                    )
                except Exception:
                    logger.exception(
                        "replace_text_field_instances: failed to inspect master %s",
                        m,
                    )

        if not master_map:
            logger.debug("replace_text_field_instances: no matching masters found")
            return 0

        # Find instances and replace anchor text when linked to a known master
        replaced = 0
        try:
            fields = doc.getTextFields()
            enum = fields.createEnumeration()
        except Exception:
            logger.debug("replace_text_field_instances: cannot enumerate fields")
            return 0

        while enum.hasMoreElements():
            try:
                f = enum.nextElement()
            except Exception:
                break
            try:
                # Attempt to determine the master name for this instance via several
                # possible property names. Be defensive about unexpected return types.
                master_name = None
                for propname in (
                    "Master",
                    "TextFieldMaster",
                    "FieldMaster",
                    "TextFieldMasterName",
                    "FieldMasterName",
                ):
                    try:
                        val = f.getPropertyValue(propname)
                    except Exception:
                        try:
                            val = getattr(f, propname, None)
                        except Exception:
                            val = None
                    if val:
                        # If val is an object exposing a Name property, try to get it
                        try:
                            if hasattr(val, "Name"):
                                candidate = getattr(val, "Name")
                            else:
                                candidate = str(val)
                        except Exception:
                            try:
                                candidate = str(val)
                            except Exception:
                                candidate = None
                        if candidate:
                            # Normalize to matching master element name if possible
                            if candidate in master_map:
                                master_name = candidate
                                break
                            # Some APIs may return only the tail (e.g., "User.Name"); try suffix match
                            for m in master_map.keys():
                                if m.endswith(candidate) or candidate.endswith(
                                    m.split(".")[-1]
                                ):
                                    master_name = m
                                    break
                            if master_name:
                                break

                if not master_name:
                    # Could not determine master via properties; skip this instance
                    continue

                replacement = master_map.get(master_name)
                if replacement is None:
                    continue

                # Replace the anchored text with the replacement string
                try:
                    anchor = f.getAnchor()
                except Exception:
                    anchor = None

                if anchor is not None:
                    replaced_success = False
                    try:
                        # Prefer setString if available
                        if hasattr(anchor, "setString"):
                            anchor.setString(str(replacement))
                            replaced_success = True
                        else:
                            # Fallback: try to replace via the parent text range
                            try:
                                parent_text = anchor.getText()
                                start = anchor.getStart()
                                end = anchor.getEnd()
                                parent_text.replaceRange(str(replacement), start, end)
                                replaced_success = True
                            except Exception:
                                pass
                    except Exception:
                        logger.exception(
                            "replace_text_field_instances: failed to set anchor string"
                        )

                    # Try to remove the field instance object so it becomes plain text
                    try:
                        if replaced_success:
                            try:
                                parent_text = anchor.getText()
                                if hasattr(parent_text, "removeTextContent"):
                                    parent_text.removeTextContent(f)
                                else:
                                    # Some UNO builds expose removeTextContent under a different name; try removeTextField
                                    try:
                                        parent_text.removeTextField(f)
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                            replaced += 1
                    except Exception:
                        logger.exception(
                            "replace_text_field_instances: failed to remove field object after replacement"
                        )

            except Exception:
                logger.exception(
                    "replace_text_field_instances: unexpected error while handling an instance"
                )
                continue

        logger.info("replace_text_field_instances: replaced %s instances", replaced)
        return replaced
    except Exception:
        logger.exception("replace_text_field_instances: unexpected top-level error")
        return 0


def open_template(libreoffice: any, file_name: str, template_folder: str):
    """Opens the template document from the given path."""
    # Create properties for opening the document in hidden mode
    prop = create_prop()
    prop.Name = "Hidden"
    prop.Value = True
    args = [prop]
    template_path = pathlib.Path(template_folder + file_name)
    # Create the document URL from the template path
    url = create_document_url(template_path)
    # Load and return the document
    return libreoffice.loadComponentFromURL(url, "_blank", 0, args)


def process_writer_document_and_save(
    libreoffice: any,
    template_file_name: str,
    report_issue_id: str,
    report_output_format: str,
    report_data: dict,
    templates_folder: str,
    temp_folder: str,
    output_folder: str,
):
    """Synchronously process a Writer template and save outputs."""
    try:
        document = open_template(libreoffice, template_file_name, templates_folder)

        # 1. Fill Content
        if report_data.get("writer_placeholders"):
            document = writer_fill_placeholder_fields(document, report_data)

        if report_data.get("writer_variables"):
            document = writer_fill_variable_fields(document, report_data)
            # Replace fields with concrete text for persistence
            replace_text_field_instances_with_concrete_text(
                document, report_data.get("writer_variables")
            )

        if report_data.get("writer_images"):
            document = replace_writer_images(
                document, report_data.get("writer_images"), temp_folder
            )

        if report_data.get("writer_tables"):
            document = writer_fill_tables(document, report_data)

        update_all_text_fields(document)

        saved_paths = []

        # 3. Export PDF
        if "PDF" in report_output_format:
            pdf_path = save_document(
                document, output_folder, str(report_issue_id), "writer_pdf_Export"
            )
            saved_paths.append(pdf_path)

        # 4. Export ODT
        if "OPENOFFICE" in report_output_format:
            odt_path = save_document(
                document, output_folder, str(report_issue_id), "writer8"
            )
            saved_paths.append(odt_path)

        if saved_paths:
            logger.info("Saved files for issue %s: %s", report_issue_id, saved_paths)

        document.close(True)
        return True

    except Exception as e:
        logger.exception(
            "Failed processing document for issue_id=%s: %s", report_issue_id, e
        )
        if "document" in locals():
            try:
                document.close(True)
            except:
                pass
        raise


def replace_writer_images(document, images_data, temp_folder):
    """Safely replace named graphics in a writer document with provided base64 images."""
    if not images_data:
        return document

    # Obtain GraphicProvider safely
    try:
        component_context = uno.getComponentContext()
        query_provider = component_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.graphic.GraphicProvider", component_context
        )
    except Exception:
        logger.exception("Failed to obtain GraphicProvider; skipping image replacement")
        return document

    # Get a collection of graphics in the document
    try:
        images = document.getGraphicObjects()
    except Exception:
        logger.exception(
            "Document does not expose graphic objects; skipping image replacement"
        )
        return document

    # Safely list element names (convert to Python list)
    try:
        image_names = list(images.getElementNames())
    except Exception:
        # If getElementNames fails return without attempting replacements
        logger.exception(
            "Failed to enumerate graphic names; skipping image replacement"
        )
        return document

    # Loop through requested image replacements
    for image_name, b64 in images_data.items():
        if image_name not in image_names:
            logger.debug(
                "Image '%s' not found in document graphics; skipping", image_name
            )
            continue

        try:
            image = images.getByName(image_name)
        except Exception:
            logger.exception("Failed to get graphic by name '%s'; skipping", image_name)
            continue

        # Write base64 to a temporary file
        try:
            temp_file_path = base64_string_to_file(temp_folder, b64)
        except Exception:
            logger.exception(
                "Failed to write base64 to file for image '%s'; skipping", image_name
            )
            continue

        # Basic file checks (size + type detection) to avoid passing invalid files
        try:

            # Use header-based detection from file bytes (imghdr removed in Python 3.13)
            try:
                image_ext = determine_file_extension_from_path(temp_file_path)
                if not image_ext:
                    continue
            except Exception:
                continue
        except Exception:
            continue

        # Convert filesystem path to file URL accepted by UNO
        try:
            temp_file_url = create_document_url(temp_file_path)
        except Exception:
            logger.exception(
                "Failed to convert file path to file URL for image '%s'; skipping",
                image_name,
            )
            continue

        # Create the graphic resource and assign it
        try:
            prop = create_prop()
            prop.Name = "URL"
            prop.Value = temp_file_url

            # Prefer setting GraphicURL (string) where supported because it avoids
            # invoking the GraphicProvider, which can trigger native crashes.
            try:
                try:
                    image.setPropertyValue("GraphicURL", temp_file_url)
                    continue
                except Exception:
                    try:
                        setattr(image, "GraphicURL", temp_file_url)
                        continue
                    except Exception:
                        continue
            except Exception:
                pass

            # Fallback: attempt to use GraphicProvider (less safe)
            try:
                new_image = query_provider.queryGraphic((prop,))
            except Exception:
                continue

            if not new_image:
                continue

            # Replace the current image's graphic in a safe manner
            try:
                image.Graphic = new_image
            except Exception:
                continue
        except Exception:
            continue

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
    # Create a unique file path (ensure uuid is string and join as a path)
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path_obj = pathlib.Path(file_path) / file_name
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


def determine_file_extension_from_path(file_path: str) -> str:
    """Determine the image file extension by reading the file header bytes.

    This avoids relying on `imghdr` (removed in Python 3.13) and mirrors the
    signature checks used by `determine_mime_extension`.
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(12)
    except Exception:
        return ""

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
