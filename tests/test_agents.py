"""Tests for agents."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.decision_agent import create_analysis_agent, generate_recommendation

class TestDecisionAgent(unittest.TestCase):
    """Tests for decision agent."""
    
    @patch('src.agents.decision_agent.OpenAI')
    @patch('src.agents.decision_agent.initialize_agent')
    def test_create_analysis_agent(self, mock_initialize_agent, mock_openai):
        """Test create_analysis_agent."""
        # Setup mocks
        mock_llm = MagicMock()
        mock_openai.return_value = mock_llm
        
        mock_agent = MagicMock()
        mock_initialize_agent.return_value = mock_agent
        
        # Run test
        tools = [MagicMock(), MagicMock()]
        agent = create_analysis_agent(tools)
        
        # Assert
        mock_openai.assert_called_once()
        mock_initialize_agent.assert_called_once()
        self.assertEqual(agent, mock_agent)
    
    @patch('src.agents.decision_agent.OpenAI')
    def test_generate_recommendation(self, mock_openai):
        """Test generate_recommendation."""
        # Setup mock
        mock_llm = MagicMock()
        mock_openai.return_value = mock_llm
        
        mock_generation = MagicMock()
        mock_generation.generations = [[MagicMock(text="Improve the product page")]]
        mock_llm.generate.return_value = mock_generation
        
        # Run test
        analysis_result = "The product page has a high bounce rate of 85%."
        result = generate_recommendation(analysis_result)
        
        # Assert
        mock_openai.assert_called_once()
        mock_llm.generate.assert_called_once()
        self.assertEqual(result, "Improve the product page")

if __name__ == '__main__':
    unittest.main()