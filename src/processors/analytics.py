"""Analytics data processing."""
import pandas as pd
import numpy as np

def identify_underperforming_pages(analytics_df, threshold=0.7):
    """Identify underperforming pages based on bounce rate and session duration.
    
    Args:
        analytics_df: DataFrame with analytics data
        threshold: Threshold for identifying underperforming pages
        
    Returns:
        DataFrame with underperforming pages
    """
    # Normalize metrics
    if 'ga:bounceRate' in analytics_df.columns:
        # Lower is better for bounce rate, so invert
        analytics_df['bounce_score'] = 1 - (analytics_df['ga:bounceRate'] / 100)
    else:
        analytics_df['bounce_score'] = 0.5  # Default if missing
    
    if 'ga:avgSessionDuration' in analytics_df.columns:
        # Normalize session duration (higher is better)
        max_duration = analytics_df['ga:avgSessionDuration'].max()
        if max_duration > 0:
            analytics_df['duration_score'] = analytics_df['ga:avgSessionDuration'] / max_duration
        else:
            analytics_df['duration_score'] = 0.5  # Default if all zeros
    else:
        analytics_df['duration_score'] = 0.5  # Default if missing
    
    # Calculate performance score (simple average of normalized metrics)
    analytics_df['performance_score'] = (analytics_df['bounce_score'] + analytics_df['duration_score']) / 2
    
    # Filter underperforming pages
    underperforming = analytics_df[analytics_df['performance_score'] < threshold].copy()
    
    # Sort by performance score (ascending)
    underperforming = underperforming.sort_values('performance_score')
    
    return underperforming

def calculate_conversion_funnel(analytics_df, funnel_steps):
    """Calculate conversion funnel metrics.
    
    Args:
        analytics_df: DataFrame with analytics data
        funnel_steps: List of page paths representing the funnel
        
    Returns:
        DataFrame with funnel metrics
    """
    funnel_metrics = []
    
    for i, step in enumerate(funnel_steps):
        step_data = analytics_df[analytics_df['ga:pagePath'] == step]
        
        if not step_data.empty:
            pageviews = step_data['ga:pageviews'].values[0]
            
            # For the first step, conversion rate is 100%
            if i == 0:
                conversion_rate = 100
                previous_step = None
                dropoff_rate = 0
            else:
                previous_step_data = analytics_df[analytics_df['ga:pagePath'] == funnel_steps[i-1]]
                if not previous_step_data.empty:
                    previous_pageviews = previous_step_data['ga:pageviews'].values[0]
                    conversion_rate = (pageviews / previous_pageviews) * 100
                    dropoff_rate = 100 - conversion_rate
                    previous_step = funnel_steps[i-1]
                else:
                    conversion_rate = np.nan
                    dropoff_rate = np.nan
                    previous_step = funnel_steps[i-1]
            
            funnel_metrics.append({
                'step': i + 1,
                'page_path': step,
                'pageviews': pageviews,
                'previous_step': previous_step,
                'conversion_rate': conversion_rate,
                'dropoff_rate': dropoff_rate
            })
    
    return pd.DataFrame(funnel_metrics)