# modules/streaming_utils.py
import json
import asyncio
from typing import AsyncGenerator, Any, Dict

async def sakhi_stream_generator(
    stream_iterator: AsyncGenerator[str, None],
    intent: str,
    metadata: Dict[str, Any] = None
) -> AsyncGenerator[str, None]:
    """
    Wraps an AI text stream into a JSON-chunked stream for the frontend.
    """
    # 1. Send initial metadata (intent, etc.)
    init_chunk = {
        "type": "metadata",
        "intent": intent,
        "mode": metadata.get("mode", "general"),
        "language": metadata.get("language", "en"),
        "route": metadata.get("route", "unknown")
    }
    
    # Send extra metadata if present
    if metadata.get("youtube_link"):
        init_chunk["youtube_link"] = metadata["youtube_link"]
    if metadata.get("infographic_url"):
        init_chunk["infographic_url"] = metadata["infographic_url"]
        
    yield json.dumps(init_chunk) + "\n"
    
    # 2. Stream the actual content
    full_response = ""
    async for chunk in stream_iterator:
        if chunk:
            full_response += chunk
            yield json.dumps({"type": "content", "reply": chunk}) + "\n"
            
    # 3. Optional: Send a final chunk or signal completion
    # (FastAPI handles closing the connection, but we can send a 'done' message)
    # yield json.dumps({"type": "done"}) + "\n"
