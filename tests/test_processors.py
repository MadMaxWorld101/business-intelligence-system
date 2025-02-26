"""Tests for processors."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processors.email_parser import parse_email_content
from src.processors.analytics import identify_underperforming_pages

class TestEmailParser(unittest.TestCase):
    """Tests for email parser."""
    
    @patch('src.processors.email_parser.OpenAI')
    def test_parse_email_content(self, mock_openai):
        """Test parse_email_content."""
        # Setup mock
        mock_llm = MagicMock()
        mock_openai.return_value = mock_llm
        
        expected_result = {
            'customer_name': 'John Doe',
            'product': 'Widget X',
            'sentiment': 'positive',
            'main_issue': 'Feature request',
            'priority': 'medium'
        }
        
        mock_llm.run.return_value = json.dumps(expected_result)
        
        # Run test
        email_body = "Hello, I'm John Doe. I love your Widget X product but would like to request a new feature."
        result = parse_email_content(email_body)
        
        # Assert
        mock_llm.run.assert_called_once()
        self.assertEqual(result, expected_result)
    
    @patch('src.processors.email_parser.OpenAI')
    def test_parse_email_content_error(self, mock_openai):
        """Test parse_email_content with error."""
        # Setup mock
        mock_llm = MagicMock()
        mock_openai.return_value = mock_llm
        
        # Invalid JSON response
        mock_llm.run.return_value = "Not JSON"
        
        # Run test
        email_body = "Hello, I'm John Doe."
        result = parse_email_content(email_body)
        
        # Assert
        mock_llm.run.assert_called_once()
        self.assertEqual(result['customer_name'], 'Unknown')
        self.assertEqual(result['sentiment'], 'neutral')

class TestAnalyticsProcessor(unittest.TestCase):
    """Tests for analytics processor."""
    
    def test_identify_underperforming_pages(self):
        """Test identify_underperforming_pages."""
        # Create test data
        data = {
            'ga:pagePath': ['/home', '/about', '/contact', '/product'],
            'ga:pageviews': [1000, 500, 200, 300],
            'ga:bounceRate': [30.0, 60.0, 90.0, 80.0],
            'ga:avgSessionDuration': [120.0, 60.0, 30.0, 45.0]
        }
        df = pd.DataFrame(data)
        
        # Run test
        result = identify_underperforming_pages(df, threshold=0.6)
        
        # Assert
        self.assertEqual(len(result), 2)  # Contact and Product pages should be underperforming
        self.assertTrue('/contact' in result['ga:pagePath'].values)
        self.assertTrue('/product' in result['ga:pagePath'].values)

if __name__ == '__main__':
    unittest.main()