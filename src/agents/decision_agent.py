"""Decision-making agent using LangChain."""
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from config import OPENAI_API_KEY

def create_analysis_agent(tools):
    """Create an agent for analyzing business data and making decisions.
    
    Args:
        tools: List of LangChain tools
        
    Returns:
        Initialized agent
    """
    # Initialize LLM
    llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
    
    # Create agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent

def analyze_business_data(agent, query):
    """Run the agent to analyze business data.
    
    Args:
        agent: Initialized agent
        query: Analysis query
        
    Returns:
        Agent's response
    """
    return agent.run(query)

def generate_recommendation(analysis_result):
    """Generate a recommendation based on analysis result.
    
    Args:
        analysis_result: Analysis result from agent
        
    Returns:
        Recommendation string
    """
    # Initialize LLM
    llm = OpenAI(temperature=0.2, api_key=OPENAI_API_KEY)
    
    prompt = f"""
    Based on the following analysis result, provide a concise recommendation
    for business actions to take. Focus on actionable steps.
    
    Analysis Result:
    {analysis_result}
    
    Recommendation:
    """
    
    return llm.generate([prompt]).generations[0][0].text.strip()