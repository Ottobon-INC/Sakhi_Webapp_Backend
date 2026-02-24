# test_streaming.py
import httpx
import asyncio
import time
import json

async def test_sakhi_stream():
    url = "http://localhost:8000/sakhi/chat"
    user_id = "47404344-4cb5-4bd3-8665-2b9d294cf85f"
    
    print("\n" + "="*60)
    print("🚀 SAKHI INTERACTIVE STREAMING & LATENCY VERIFIER")
    print("="*60)
    print(f"Target: {url}")
    print("Type 'exit' or 'quit' to stop.")

    async with httpx.AsyncClient(timeout=90.0) as client:
        while True:
            print("\n" + "-"*30)
            message = input("💬 Ask Sakhi: ")
            if message.lower() in ["exit", "quit"]:
                break
            if not message.strip():
                continue

            payload = {
                "user_id": user_id,
                "message": message,
                "language": "en",
                "stream": True
            }

            start_time = time.perf_counter()
            ttfb = None
            full_response = ""
            
            try:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code != 200:
                        print(f"❌ Error {response.status_code}: {await response.aread()}")
                        continue

                    print("⏳ Connected. Awaiting chunks...")
                    
                    async for line in response.aiter_lines():
                        if not line: continue
                        
                        if ttfb is None:
                            ttfb = time.perf_counter() - start_time
                            print(f"\n✅ Time to First Byte (TTFB): {ttfb:.2f}s")
                        
                        try:
                            chunk = json.loads(line)
                            if chunk["type"] == "metadata":
                                print(f"📌 Intent: {chunk.get('intent')}")
                                print(f"📌 Route: {chunk.get('route')}")
                                if chunk.get("infographic_url"):
                                    print(f"🖼️  Infographic: {chunk.get('infographic_url')}")
                                if chunk.get("youtube_link"):
                                    print(f"🎥  YouTube: {chunk.get('youtube_link')}")
                                print("-" * 40)
                            elif chunk["type"] == "content":
                                content = chunk.get("reply", "")
                                full_response += content
                                print(content, end="", flush=True)
                        except json.JSONDecodeError:
                            # If not JSON, it might be a raw chunk or completion signal
                            pass
                    
                    total_time = time.perf_counter() - start_time
                    print(f"\n\n{'='*60}")
                    print(f"📊 Latency Summary:")
                    print(f"   - TTFB: {ttfb:.2f}s")
                    print(f"   - Completion Time: {total_time:.2f}s")
                    print(f"   - Words: {len(full_response.split())}")
                    print(f"{'='*60}")

            except Exception as e:
                print(f"\n❌ Client Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_sakhi_stream())
