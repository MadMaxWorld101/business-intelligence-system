"""Google Analytics connector for fetching website metrics."""
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from config import GOOGLE_CREDENTIALS_PATH

def get_analytics_service():
    """Get Google Analytics API service."""
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    return build('analyticsreporting', 'v4', credentials=credentials)

def get_page_metrics(service, view_id, start_date, end_date):
    """Get page metrics from Google Analytics.
    
    Args:
        service: Google Analytics API service
        view_id: Analytics view ID
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        
    Returns:
        Pandas DataFrame with page metrics
    """
    response = service.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [
                        {'expression': 'ga:sessions'},
                        {'expression': 'ga:pageviews'},
                        {'expression': 'ga:bounceRate'},
                        {'expression': 'ga:avgSessionDuration'}
                    ],
                    'dimensions': [{'name': 'ga:pagePath'}],
                    'orderBys': [
                        {'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}
                    ],
                    'pageSize': 100
                }
            ]
        }
    ).execute()
    
    # Process the response
    report = response['reports'][0]
    dimensions = report['columnHeader']['dimensions']
    metrics = [m['name'] for m in report['columnHeader']['metricHeader']['metricHeaderEntries']]
    
    all_data = []
    for row in report['data'].get('rows', []):
        dimension_values = row['dimensions']
        metric_values = row['metrics'][0]['values']
        all_data.append(dimension_values + metric_values)
    
    # Create DataFrame
    columns = dimensions + metrics
    df = pd.DataFrame(all_data, columns=columns)
    
    # Convert numeric columns
    for metric in metrics:
        df[metric] = pd.to_numeric(df[metric], errors='ignore')
    
    return df