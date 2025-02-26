"""Review content parsing using LangChain."""
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from config import OPENAI_API_KEY

def parse_review_content(review_text, source='unknown'):
    """Parse review content to extract structured information.
    
    Args:
        review_text: Raw review text
        source: Source of the review (e.g., 'shopify', 'google', 'amazon')
        
    Returns:
        Dictionary with extracted information
    """
    # Initialize LLM
    llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
    
    # Create prompt
    prompt = PromptTemplate(
        input_variables=["review", "source"],
        template="""
        Extract the following information from this {source} review:
        1. Product name (if mentioned)
        2. Rating (extract or estimate on a scale of 1-5)
        3. Sentiment (positive, negative, neutral)
        4. Key positive points
        5. Key negative points
        6. Main suggestions for improvement (if any)
        
        Review:
        {review}
        
        Format as JSON with these keys: product_name, rating, sentiment, positive_points, negative_points, suggestions
        """
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    result = chain.run(review=review_text, source=source)
    
    # Parse JSON result
    try:
        parsed_result = json.loads(result.strip())
        return parsed_result
    except json.JSONDecodeError:
        # Fallback in case of parsing error
        return {
            'product_name': 'Unknown',
            'rating': 3,
            'sentiment': 'neutral',
            'positive_points': [],
            'negative_points': [],
            'suggestions': []
        }