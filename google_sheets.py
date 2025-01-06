# google_sheet.py

import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_sheets_service():
    """Establishes a connection to the Google Sheets API."""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials.json'  # Replace with your credentials file path

    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        logger.debug("Successfully created sheets service")
        return service
    except Exception as e:
        logger.error(f"Failed to create sheets service: {e}")
        return None


def export_to_google_sheets(data, spreadsheet_id, range_name):
    """Exports data to a specified Google Sheet.

    Args:
        data: The data to export, in the form of a list of lists or a dictionary.
        spreadsheet_id: The ID of the spreadsheet to export to.
        range_name: The range of cells to update in the spreadsheet (e.g., 'Sheet1!A1').

    Returns:
        True if the export was successful, False otherwise.
    """

    try:
        service = get_sheets_service()
        if not service:
            raise Exception("Failed to get sheets service")

        logger.debug(f"Processing data for export: {data}")

        # Clear existing data
        clear_result = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        logger.debug(f"Cleared sheet: {clear_result}")

        # Process incoming data
        if isinstance(data, dict):
            headers = list(data.keys())
            values = [headers, list(str(v)[:50000] for v in data.values())]
        elif isinstance(data, list) and data:
            headers = data[0]
            values = [headers]
            for item in data[1:]:
                row = [str(cell)[:50000] for cell in item]  # Truncate each cell to 50000 characters
                values.append(row)
        else:
            raise ValueError("Invalid data format")

        # Log the length of each cell to ensure it does not exceed 50000 characters
        # and identify the problematic cell
        for row_index, row in enumerate(values):
            for col_index, cell in enumerate(row):
                if len(cell) > 50000:
                    logger.error(f"Cell exceeds 50000 characters: "
                                f"Row {row_index + 1}, Column {col_index + 1} - {cell[:100]}... (length: {len(cell)})")
                    raise ValueError(f"Cell in row {row_index + 1}, column {col_index + 1} exceeds 50000 characters")

        body = {'values': values}
        logger.debug(f"Preparing to write data: {body}")

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        updated_cells = result.get('updatedCells', 0)
        logger.info(f"Successfully updated {updated_cells} cells")
        return True

    except Exception as e:
        logger.error(f"Export failed: {e}")
        return False