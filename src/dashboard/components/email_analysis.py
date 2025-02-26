"""Email analysis component for the dashboard."""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def render_email_analysis(email_data):
    """Render email analysis component.
    
    Args:
        email_data: DataFrame with email data
    """
    st.header("Email Analysis")
    
    if email_data.empty:
        st.info("No email data available for the selected date range.")
        return
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Emails", len(email_data))
    
    with col2:
        if 'Sentiment' in email_data.columns:
            positive = sum(email_data['Sentiment'] == 'positive')
            st.metric("Positive Sentiment", f"{positive} ({positive/len(email_data):.1%})")
    
    with col3:
        if 'Sentiment' in email_data.columns:
            negative = sum(email_data['Sentiment'] == 'negative')
            st.metric("Negative Sentiment", f"{negative} ({negative/len(email_data):.1%})")
    
    # Display sentiment trend
    if 'Sentiment' in email_data.columns and 'Date' in email_data.columns:
        st.subheader("Sentiment Trend")
        
        # Prepare data
        email_data['Date'] = pd.to_datetime(email_data['Date'])
        email_data['Week'] = email_data['Date'].dt.isocalendar().week
        
        # Count sentiments by week
        sentiment_by_week = pd.crosstab(email_data['Week'], email_data['Sentiment'])
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sentiment_by_week.plot(kind='bar', stacked=True, ax=ax)
        ax.set_xlabel('Week')
        ax.set_ylabel('Count')
        ax.set_title('Email Sentiment by Week')
        st.pyplot(fig)
    
    # Display most common issues
    if 'Main Issue' in email_data.columns:
        st.subheader("Most Common Issues")
        
        issues = email_data['Main Issue'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        issues.plot(kind='barh', ax=ax)
        ax.set_xlabel('Count')
        ax.set_ylabel('Issue')
        ax.set_title('Most Common Issues')
        st.pyplot(fig)
    
    # Display recent emails
    st.subheader("Recent Emails")
    st.dataframe(email_data.head(10))