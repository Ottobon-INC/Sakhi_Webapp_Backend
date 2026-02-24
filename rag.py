# rag.py
import os

import supabase_client  # ensures .env is loaded once
from openai import OpenAI, AsyncOpenAI

EMBEDDING_MODEL = "text-embedding-3-small"  # 1536 dimensions

_api_key = os.getenv("OPENAI_API_KEY")
client = None
async_client = None
if _api_key:
    client = OpenAI(api_key=_api_key, timeout=60.0)
    async_client = AsyncOpenAI(api_key=_api_key, timeout=60.0)


# =============================================================================
# SYNC FUNCTIONS (kept for startup anchor computation)
# =============================================================================

def generate_embedding(text: str):
    """
    Converts text into a 1536-dimensional embedding vector using OpenAI.
    """
    if not client:
        raise Exception("OPENAI_API_KEY missing. Cannot generate embeddings.")
    cleaned = text.strip().replace("\n", " ")

    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned
    )

    return resp.data[0].embedding


def generate_embeddings(texts: list[str]):
    """
    Converts a list of texts into embedding vectors in a single batch call.
    """
    if not client:
        raise Exception("OPENAI_API_KEY missing. Cannot generate embeddings.")
    
    cleaned_texts = [t.strip().replace("\n", " ") for t in texts]
    
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned_texts
    )
    
    return [item.embedding for item in resp.data]


# =============================================================================
# ASYNC FUNCTIONS (for hot-path chat processing — true async I/O)
# =============================================================================

async def async_generate_embedding(text: str):
    """
    Async version of generate_embedding — non-blocking I/O.
    """
    if not async_client:
        raise Exception("OPENAI_API_KEY missing. Cannot generate embeddings.")
    cleaned = text.strip().replace("\n", " ")

    resp = await async_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned
    )

    return resp.data[0].embedding


async def async_generate_embeddings(texts: list[str]):
    """
    Async version of generate_embeddings — non-blocking batch I/O.
    """
    if not async_client:
        raise Exception("OPENAI_API_KEY missing. Cannot generate embeddings.")
    
    cleaned_texts = [t.strip().replace("\n", " ") for t in texts]
    
    resp = await async_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=cleaned_texts
    )
    
    return [item.embedding for item in resp.data]
