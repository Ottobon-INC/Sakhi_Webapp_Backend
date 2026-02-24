import httpx
import asyncio
import time

BASE_URL = "http://localhost:8000"

ENDPOINTS = [
    ("GET",  "Health Check",       "/"),
    ("GET",  "Docs",               "/docs"),
    ("POST", "Chat Endpoint",      "/chat"),
    ("POST", "Onboarding",         "/onboarding"),
]

async def ping(client, method, name, path):
    url = BASE_URL + path
    start = time.time()
    try:
        if method == "GET":
            resp = await client.get(url)
        else:
            resp = await client.post(url, json={})
        latency = (time.time() - start) * 1000
        status = "✅ UP" if resp.status_code < 500 else f"⚠️  {resp.status_code}"
        print(f"  {name:<25} | {status:<12} | {latency:>8.2f} ms")
    except Exception as e:
        print(f"  {name:<25} | ❌ DOWN       | Error: {str(e)[:60]}")

async def main():
    print("\n🔬 Sakhi Webapp Backend — Latency Report")
    print(f"   Target: {BASE_URL}")
    print("=" * 65)
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [ping(client, m, n, p) for m, n, p in ENDPOINTS]
        await asyncio.gather(*tasks)
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
