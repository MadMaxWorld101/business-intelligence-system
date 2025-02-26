"""Gmail connector for fetching emails."""
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_CREDENTIALS_PATH, GMAIL_USER

def get_gmail_credentials():
    """Get Google API credentials for Gmail."""
    return service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )

def get_unread_emails(credentials, max_results=10):
    """Fetch unread emails from Gmail.
    
    Args:
        credentials: Google API credentials
        max_results: Maximum number of emails to fetch
        
    Returns:
        List of dictionaries containing email data
    """
    gmail = build('gmail', 'v1', credentials=credentials)
    results = gmail.users().messages().list(
        userId=GMAIL_USER, 
        q='is:unread',
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    if not messages:
        return []
    
    emails = []
    for message in messages:
        msg = gmail.users().messages().get(
            userId=GMAIL_USER, 
            id=message['id']
        ).execute()
        
        payload = msg['payload']
        headers = payload['headers']
        
        # Extract subject and sender
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        
        # Extract body
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        emails.append({
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'body': body
        })
    
    return emails

def mark_as_read(credentials, message_id):
    """Mark an email as read.
    
    Args:
        credentials: Google API credentials
        message_id: Email message ID
    """
    gmail = build('gmail', 'v1', credentials=credentials)
    gmail.users().messages().modify(
        userId=GMAIL_USER,
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()