
try:
    from search_hierarchical import async_hierarchical_rag_query
    print(f"SUCCESS: Imported async_hierarchical_rag_query: {async_hierarchical_rag_query}")
except Exception as e:
    print(f"FAILURE: Could not import: {e}")
    import traceback
    traceback.print_exc()
