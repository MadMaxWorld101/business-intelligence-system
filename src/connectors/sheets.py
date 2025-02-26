"""Google Sheets connector for reading and writing data."""
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from config import GOOGLE_CREDENTIALS_PATH, SPREADSHEET_ID

def get_sheets_service():
    """Get Google Sheets API service."""
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=credentials)

def read_from_sheets(service, spreadsheet_id=SPREADSHEET_ID, sheet_range='Sheet1!A:Z'):
    """Read data from Google Sheets.
    
    Args:
        service: Google Sheets API service
        spreadsheet_id: ID of the spreadsheet
        sheet_range: Range to read (e.g., 'Sheet1!A:Z')
        
    Returns:
        Pandas DataFrame containing the sheet data
    """
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()
    
    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def write_to_sheets(service, data, spreadsheet_id=SPREADSHEET_ID, sheet_range='Sheet1!A:Z'):
    """Write data to Google Sheets.
    
    Args:
        service: Google Sheets API service
        data: List of values to write
        spreadsheet_id: ID of the spreadsheet
        sheet_range: Range to write to (e.g., 'Sheet1!A:Z')
    """
    body = {
        'values': [data] if not isinstance(data[0], list) else data
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    return result