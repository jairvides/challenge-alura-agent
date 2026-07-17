import pytest
from src.core.rag_chain import query_agent
import os

def test_query_agent():
    # This test assumes ingest.py has been run and GOOGLE_API_KEY is set
    if not os.path.exists("vectorstore"):
        pytest.skip("Vector store not populated. Run ingest.py first.")
    
    query = "How do I return a product?"
    response = query_agent(query)
    assert response is not None
    assert len(response) > 0
    # The answer should come from faq.json
    assert "30 days" in response or "returns portal" in response
