"""Main orchestration script for the business intelligence system."""
import schedule
import time
import logging
from datetime import datetime

from config import DATA_REFRESH_INTERVAL, LOG_LEVEL
from connectors.gmail import get_unread_emails, get_gmail_credentials
from connectors.sheets import get_sheets_service, write_to_sheets
from processors.email_parser import parse_email_content
from agents.decision_agent import create_analysis_agent

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_emails():
    """Process unread emails and store extracted data in Google Sheets."""
    try:
        logger.info("Starting email processing job")
        
        # Get Gmail credentials
        credentials = get_gmail_credentials()
        
        # Fetch unread emails
        emails = get_unread_emails(credentials)
        logger.info(f"Found {len(emails)} unread emails")
        
        # Process each email
        for email in emails:
            # Parse email content
            parsed_data = parse_email_content(email['body'])
            logger.debug(f"Parsed data: {parsed_data}")
            
            # Write to Google Sheets
            sheets_service = get_sheets_service()
            write_to_sheets(
                service=sheets_service,
                spreadsheet_id=SPREADSHEET_ID,
                data=[
                    email['sender'],
                    email['subject'],
                    parsed_data['sentiment'],
                    parsed_data['main_issue'],
                    parsed_data['product'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ],
                sheet_range='Emails!A:F'
            )
            
        logger.info("Email processing completed successfully")
    except Exception as e:
        logger.error(f"Error in email processing: {str(e)}", exc_info=True)

def run_analysis():
    """Run analysis on collected data and take actions."""
    try:
        logger.info("Starting analysis job")
        # TODO: Implement analysis
        logger.info("Analysis completed successfully")
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}", exc_info=True)

def main():
    """Main function to set up scheduled jobs."""
    logger.info("Starting Business Intelligence System")
    
    # Schedule jobs
    schedule.every(1).hours.do(process_emails)
    schedule.every().day.at("07:00").do(run_analysis)
    
    # Run jobs immediately on startup
    process_emails()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()