import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_connection():
    try:
        logger.debug("Starting connection test...")
        
        # Test credentials loading
        SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        SERVICE_ACCOUNT_FILE = 'credentials.json'
        
        logger.debug(f"Loading credentials from {SERVICE_ACCOUNT_FILE}")
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        logger.debug("Building service...")
        service = build('sheets', 'v4', credentials=credentials)
        
        # Test API connection
        spreadsheet_id = '1k7XRNbQUMWSXtSiljeBo1nuTYj8p7gBAHutCYqBzOEw'  # Your spreadsheet ID
        test_range = 'Sheet1!A1:A1'
        
        logger.debug("Testing API call...")
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=test_range
        ).execute()
        
        logger.info("Successfully connected to Google Sheets API")
        print("Connection test passed!")
        return True
        
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        print(f"Connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()