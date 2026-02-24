import httpx
import time
import json

NGROK_URL = "https://ungaraged-soony-maricela.ngrok-free.dev"
CHAT_ENDPOINT = f"{NGROK_URL}/sakhi/chat"

payload = {
    "user_id": "47404344-4cb5-4bd3-8665-2b9d294cf85f",
    "message": "Hello Sakhi, testing your public URL!",
    "language": "en"
}

def test_query():
    print(f"\n📡 Querying Public Ngrok URL: {CHAT_ENDPOINT}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)
    
    start_time = time.time()
    try:
        # Use a longer timeout for LLM processing
        with httpx.Client(timeout=60.0) as client:
            response = client.post(CHAT_ENDPOINT, json=payload)
            
        latency = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS (HTTP {response.status_code})")
            print(f"⏱️  Latency: {latency:.2f}s")
            print(f"🤖 Sakhi's Reply: {data.get('reply')}")
            print(f"🛤️  Route Trace: {data.get('route')}")
        else:
            print(f"❌ FAILED (HTTP {response.status_code})")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_query()
