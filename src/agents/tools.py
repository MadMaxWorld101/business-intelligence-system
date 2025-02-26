"""Custom tools for LangChain agents."""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class GoogleSheetsInput(BaseModel):
    """Input for Google Sheets tool."""
    sheet_range: str = Field(..., description="Sheet range in A1 notation, e.g., 'Sheet1!A1:D10'")
    
class GoogleSheetsTool(BaseTool):
    """Tool for reading from Google Sheets."""
    name = "google_sheets_reader"
    description = "Use this tool to read data from a Google Sheets spreadsheet"
    args_schema: Type[BaseModel] = GoogleSheetsInput
    
    def __init__(self, sheets_service):
        """Initialize with sheets service."""
        super().__init__()
        self.sheets_service = sheets_service
    
    def _run(self, sheet_range: str) -> str:
        """Run the tool."""
        from src.connectors.sheets import read_from_sheets
        
        try:
            df = read_from_sheets(self.sheets_service, sheet_range=sheet_range)
            return df.to_string()
        except Exception as e:
            return f"Error reading from Google Sheets: {str(e)}"
            
    def _arun(self, sheet_range: str):
        """Run the tool asynchronously."""
        raise NotImplementedError("GoogleSheetsTool does not support async")

class EmailAnalysisInput(BaseModel):
    """Input for email analysis tool."""
    email_body: str = Field(..., description="Full body text of the email to analyze")
    
class EmailAnalysisTool(BaseTool):
    """Tool for analyzing email content."""
    name = "email_analyzer"
    description = "Use this tool to analyze the content of an email and extract structured information"
    args_schema: Type[BaseModel] = EmailAnalysisInput
    
    def _run(self, email_body: str) -> str:
        """Run the tool."""
        from src.processors.email_parser import parse_email_content
        
        try:
            result = parse_email_content(email_body)
            return str(result)
        except Exception as e:
            return f"Error analyzing email: {str(e)}"
            
    def _arun(self, email_body: str):
        """Run the tool asynchronously."""
        raise NotImplementedError("EmailAnalysisTool does not support async")

class PagePerformanceInput(BaseModel):
    """Input for page performance analysis tool."""
    days: int = Field(default=30, description="Number of days of data to analyze")
    
class PagePerformanceTool(BaseTool):
    """Tool for analyzing page performance."""
    name = "page_performance_analyzer"
    description = "Use this tool to identify underperforming pages on the website"
    args_schema: Type[BaseModel] = PagePerformanceInput
    
    def __init__(self, analytics_service, view_id):
        """Initialize with analytics service."""
        super().__init__()
        self.analytics_service = analytics_service
        self.view_id = view_id
    
    def _run(self, days: int = 30) -> str:
        """Run the tool."""
        from datetime import datetime, timedelta
        from src.connectors.analytics import get_page_metrics
        from src.processors.analytics import identify_underperforming_pages
        
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            metrics = get_page_metrics(
                self.analytics_service,
                self.view_id,
                start_date,
                end_date
            )
            
            underperforming = identify_underperforming_pages(metrics)
            
            if underperforming.empty:
                return "No underperforming pages identified."
            
            return underperforming.to_string()
        except Exception as e:
            return f"Error analyzing page performance: {str(e)}"
            
    def _arun(self, days: int = 30):
        """Run the tool asynchronously."""
        raise NotImplementedError("PagePerformanceTool does not support async")