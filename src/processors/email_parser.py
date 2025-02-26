"""Email content parsing using LangChain."""
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from config import OPENAI_API_KEY

def parse_email_content(email_body):
    """Parse email content to extract structured information.
    
    Args:
        email_body: Raw email text
        
    Returns:
        Dictionary with extracted information
    """
    # Initialize LLM
    llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
    
    # Create prompt
    prompt = PromptTemplate(
        input_variables=["email"],
        template="""
        Extract the following information from this email:
        1. Customer name (if available)
        2. Product mentioned (if any)
        3. Sentiment (positive, negative, neutral)
        4. Main issue or request
        5. Priority (high, medium, low)
        
        Email:
        {email}
        
        Format as JSON with these keys: customer_name, product, sentiment, main_issue, priority
        """
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run chain
    result = chain.run(email=email_body)
    
    # Parse JSON result
    try:
        parsed_result = json.loads(result.strip())
        return parsed_result
    except json.JSONDecodeError:
        # Fallback in case of parsing error
        return {
            'customer_name': 'Unknown',
            'product': 'Unknown',
            'sentiment': 'neutral',
            'main_issue': result,
            'priority': 'medium'
        }