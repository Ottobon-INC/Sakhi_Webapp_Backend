# manual_webapp_test.py
import httpx
import asyncio
import time

async def main():
    url = "http://localhost:8000/sakhi/chat"
    user_id = "47404344-4cb5-4bd3-8665-2b9d294cf85f"  # Valid UUID found in database
    
    print("\n" + "="*50)
    print("🚀 SAKHI WEBAPP MANUAL LATENCY TESTER")
    print("="*50)
    print(f"Target: {url}")
    print("Type 'exit' to stop the test.\n")

    async with httpx.AsyncClient(timeout=90.0) as client:
        while True:
            try:
                user_input = input("Enter message: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("\nTest terminated.")
                    break

                print("⏳ Waiting for response...", end="", flush=True)
                
                start_time = time.time()
                response = await client.post(url, json={
                    "message": user_input,
                    "user_id": user_id,
                    "language": "en"
                })
                end_time = time.time()
                
                # Clear the "Waiting" line
                print("\r" + " " * 40 + "\r", end="", flush=True)

                latency_sec = end_time - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    message = data.get("reply", "N/A")
                    route = data.get("route", "N/A")
                    intent = data.get("intent", "N/A")
                    
                    print(f"✅ Response Received in {latency_sec:.2f}s")
                    print(f"👉 Route: {route}")
                    print(f"👉 Intent: {intent}")
                    print(f"💬 Answer: {message}")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                
                print("-" * 50)

            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nTest terminated.")
                break
            except Exception as e:
                print(f"\n❌ Client Error: {e}")
                print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
