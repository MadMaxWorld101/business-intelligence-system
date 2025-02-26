"""Tests for connectors."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.connectors.gmail import get_unread_emails
from src.connectors.sheets import read_from_sheets, write_to_sheets

class TestGmailConnector(unittest.TestCase):
    """Tests for Gmail connector."""
    
    @patch('src.connectors.gmail.build')
    def test_get_unread_emails(self, mock_build):
        """Test get_unread_emails."""
        # Setup mock
        mock_gmail = MagicMock()
        mock_build.return_value = mock_gmail
        
        mock_messages_list = MagicMock()
        mock_gmail.users().messages().list.return_value = mock_messages_list
        mock_messages_list.execute.return_value = {
            'messages': [{'id': '123'}, {'id': '456'}]
        }
        
        mock_message_get = MagicMock()
        mock_gmail.users().messages().get.return_value = mock_message_get
        mock_message_get.execute.side_effect = [
            {
                'id': '123',
                'payload': {
                    'headers': [
                        {'name': 'Subject', 'value': 'Test Subject 1'},
                        {'name': 'From', 'value': 'test1@example.com'}
                    ],
                    'body': {'data': 'VGVzdCBib2R5IDE='}  # Base64 for "Test body 1"
                }
            },
            {
                'id': '456',
                'payload': {
                    'headers': [
                        {'name': 'Subject', 'value': 'Test Subject 2'},
                        {'name': 'From', 'value': 'test2@example.com'}
                    ],
                    'parts': [
                        {
                            'mimeType': 'text/plain',
                            'body': {'data': 'VGVzdCBib2R5IDI='}  # Base64 for "Test body 2"
                        }
                    ]
                }
            }
        ]
        
        # Run test
        credentials = MagicMock()
        emails = get_unread_emails(credentials)
        
        # Assert
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0]['subject'], 'Test Subject 1')
        self.assertEqual(emails[0]['sender'], 'test1@example.com')
        self.assertEqual(emails[0]['body'], 'Test body 1')
        self.assertEqual(emails[1]['subject'], 'Test Subject 2')
        self.assertEqual(emails[1]['sender'], 'test2@example.com')
        self.assertEqual(emails[1]['body'], 'Test body 2')

class TestSheetsConnector(unittest.TestCase):
    """Tests for Google Sheets connector."""
    
    @patch('src.connectors.sheets.build')
    def test_read_from_sheets(self, mock_build):
        """Test read_from_sheets."""
        # Setup mock
        mock_sheets = MagicMock()
        mock_build.return_value = mock_sheets
        
        mock_get = MagicMock()
        mock_sheets.spreadsheets().values().get.return_value = mock_get
        mock_get.execute.return_value = {
            'values': [
                ['Header1', 'Header2', 'Header3'],
                ['Value1', 'Value2', 'Value3'],
                ['Value4', 'Value5', 'Value6']
            ]
        }
        
        # Run test
        service = mock_sheets
        df = read_from_sheets(service, 'test_id', 'Sheet1!A:C')
        
        # Assert
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['Header1', 'Header2', 'Header3'])
        self.assertEqual(df.iloc[0, 0], 'Value1')
        self.assertEqual(df.iloc[1, 2], 'Value6')
    
    @patch('src.connectors.sheets.build')
    def test_write_to_sheets(self, mock_build):
        """Test write_to_sheets."""
        # Setup mock
        mock_sheets = MagicMock()
        mock_build.return_value = mock_sheets
        
        mock_append = MagicMock()
        mock_sheets.spreadsheets().values().append.return_value = mock_append
        mock_append.execute.return_value = {'updates': {'updatedRows': 1}}
        
        # Run test
        service = mock_sheets
        data = ['test1', 'test2', 'test3']
        result = write_to_sheets(service, data, 'test_id', 'Sheet1!A:C')
        
        # Assert
        mock_sheets.spreadsheets().values().append.assert_called_once()
        self.assertEqual(result['updates']['updatedRows'], 1)

if __name__ == '__main__':
    unittest.main()