
import asyncio
import json
from search_hierarchical import async_hierarchical_rag_query

async def test_rag():
    print("--- TESTING RAG RESULTS FOR 'ivf' ---")
    query = "ivf"
    results = await async_hierarchical_rag_query(query)
    
    print(f"\nFound {len(results)} results")
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Source: {res.get('source_type')}):")
        print(f"  Content snippet: {str(res.get('section_content', res.get('answer')))[:100]}...")
        print(f"  YouTube: {res.get('youtube_link')}")
        print(f"  Infographic: {res.get('infographic_url')}")
        
if __name__ == "__main__":
    asyncio.run(test_rag())
