"""
==============================================================
  🚀 SAKHI WEBAPP — COMPREHENSIVE LATENCY TEST SUITE
==============================================================
  Tests every major endpoint and exercises all 3 chat routes:
    • SLM_DIRECT  (small talk, no RAG)
    • SLM_RAG     (simple medical, RAG + SLM)
    • OPENAI_RAG  (complex medical, RAG + GPT-4)

  Measures: connection time, TTFB, total round-trip, p95
  Usage:   python sakhi_latency_test.py
==============================================================
"""

import httpx
import asyncio
import time
import statistics
import sys
from typing import Optional

# ─── Configuration ──────────────────────────────────────────
BASE_URL = "http://localhost:8000"
USER_ID = "47404344-4cb5-4bd3-8665-2b9d294cf85f"   # existing user in DB
TIMEOUT = 90.0   # seconds — chat can be slow on cold starts
ITERATIONS = 3   # how many times to repeat each chat test

# ─── Test Messages (designed to trigger specific routes) ────
CHAT_TESTS = [
    {
        "label": "Small Talk (SLM_DIRECT)",
        "message": "Hello, how are you today?",
        "expected_route": "slm_direct",
    },
    {
        "label": "Simple Medical (SLM_RAG)",
        "message": "What foods should I eat during pregnancy?",
        "expected_route": "slm_rag",
    },
    {
        "label": "Complex Medical (OPENAI_RAG)",
        "message": "What is the cost of IVF treatment and what are the success rates for women over 35?",
        "expected_route": "openai_rag",
    },
]

# ─── Quick-ping endpoints ──────────────────────────────────
PING_ENDPOINTS = [
    ("GET",  "Health Check (/)",              "/"),
    ("GET",  "API Docs (/docs)",              "/docs"),
    ("GET",  "Knowledge Hub",                 "/api/knowledge-hub/"),
    ("GET",  "Knowledge Hub Recommendations", "/api/knowledge-hub/recommendations"),
]


# ═════════════════════════════════════════════════════════════
#                       HELPERS
# ═════════════════════════════════════════════════════════════
def color(text: str, code: int) -> str:
    """ANSI color wrapper (works in Windows Terminal & PowerShell 7)."""
    return f"\033[{code}m{text}\033[0m"

GREEN  = lambda t: color(t, 32)
YELLOW = lambda t: color(t, 33)
RED    = lambda t: color(t, 31)
CYAN   = lambda t: color(t, 36)
BOLD   = lambda t: color(t, 1)
DIM    = lambda t: color(t, 2)


def latency_color(ms: float) -> str:
    """Color-code a latency value."""
    text = f"{ms:>9.2f} ms"
    if ms < 1000:
        return GREEN(text)
    elif ms < 5000:
        return YELLOW(text)
    else:
        return RED(text)


def p95(values: list[float]) -> float:
    """Compute 95th-percentile."""
    if not values:
        return 0.0
    sorted_v = sorted(values)
    idx = int(len(sorted_v) * 0.95)
    return sorted_v[min(idx, len(sorted_v) - 1)]


def stats_row(label: str, times: list[float]) -> str:
    """Format a stats row with min/avg/max/p95."""
    if not times:
        return f"  {label:<40} | {'NO DATA':>10}"
    mn = min(times)
    avg = statistics.mean(times)
    mx = max(times)
    p = p95(times)
    return (
        f"  {label:<40} | "
        f"Min: {latency_color(mn)} | "
        f"Avg: {latency_color(avg)} | "
        f"Max: {latency_color(mx)} | "
        f"P95: {latency_color(p)}"
    )


# ═════════════════════════════════════════════════════════════
#              ENDPOINT PING TESTS
# ═════════════════════════════════════════════════════════════
async def ping_endpoint(client: httpx.AsyncClient, method: str, name: str, path: str):
    """Quick-ping an endpoint and measure latency."""
    url = BASE_URL + path
    start = time.perf_counter()
    try:
        if method == "GET":
            resp = await client.get(url)
        else:
            resp = await client.post(url, json={})
        latency = (time.perf_counter() - start) * 1000

        if resp.status_code < 400:
            status = GREEN("✅ UP ")
        elif resp.status_code < 500:
            status = YELLOW(f"⚠️  {resp.status_code}")
        else:
            status = RED(f"❌ {resp.status_code}")

        print(f"  {name:<40} | {status} | {latency_color(latency)}")
        return latency
    except Exception as e:
        print(f"  {name:<40} | {RED('❌ DOWN')} | Error: {str(e)[:60]}")
        return None


async def run_ping_tests(client: httpx.AsyncClient):
    """Run quick-ping on all non-chat endpoints."""
    print(BOLD("\n╔══════════════════════════════════════════════════════════════╗"))
    print(BOLD("║           SECTION 1 — ENDPOINT AVAILABILITY                 ║"))
    print(BOLD("╚══════════════════════════════════════════════════════════════╝"))
    print()

    for method, name, path in PING_ENDPOINTS:
        await ping_endpoint(client, method, name, path)

    print()


# ═════════════════════════════════════════════════════════════
#                 CHAT LATENCY TESTS
# ═════════════════════════════════════════════════════════════
async def chat_request(client: httpx.AsyncClient, message: str) -> dict:
    """
    Send a single chat request and return detailed timing info.
    """
    url = f"{BASE_URL}/sakhi/chat"
    payload = {
        "user_id": USER_ID,
        "message": message,
        "language": "en",
    }

    start = time.perf_counter()
    try:
        resp = await client.post(url, json=payload)
        total_ms = (time.perf_counter() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            return {
                "ok": True,
                "total_ms": total_ms,
                "route": data.get("route", "unknown"),
                "reply_preview": (data.get("reply", "") or "")[:80],
                "intent": data.get("intent", "N/A"),
                "status": resp.status_code,
            }
        else:
            return {
                "ok": False,
                "total_ms": total_ms,
                "route": "error",
                "reply_preview": resp.text[:80],
                "intent": "N/A",
                "status": resp.status_code,
            }
    except Exception as e:
        total_ms = (time.perf_counter() - start) * 1000
        return {
            "ok": False,
            "total_ms": total_ms,
            "route": "exception",
            "reply_preview": str(e)[:80],
            "intent": "N/A",
            "status": 0,
        }


async def run_chat_tests(client: httpx.AsyncClient):
    """Run chat latency tests across all routes with multiple iterations."""
    print(BOLD("╔══════════════════════════════════════════════════════════════╗"))
    print(BOLD("║           SECTION 2 — CHAT LATENCY BY ROUTE                ║"))
    print(BOLD(f"║           ({ITERATIONS} iterations per message)                        ║"))
    print(BOLD("╚══════════════════════════════════════════════════════════════╝"))
    print()

    all_results = {}   # label -> list of total_ms

    for test in CHAT_TESTS:
        label = test["label"]
        message = test["message"]
        expected = test["expected_route"]
        times = []

        print(f"  {CYAN(BOLD(label))}")
        print(f"  Message: {DIM(message)}")
        print(f"  Expected route: {DIM(expected)}")
        print()

        for i in range(ITERATIONS):
            result = await chat_request(client, message)

            if result["ok"]:
                times.append(result["total_ms"])
                route_match = "✔" if result["route"] == expected else f"✘ got {result['route']}"
                print(
                    f"    Run {i+1}/{ITERATIONS}: "
                    f"{latency_color(result['total_ms'])} | "
                    f"Route: {result['route']} ({route_match}) | "
                    f"Intent: {DIM(str(result['intent'])[:30])}"
                )
            else:
                print(
                    f"    Run {i+1}/{ITERATIONS}: "
                    f"{RED('FAILED')} ({result['status']}) | "
                    f"{result['reply_preview']}"
                )

            # Small delay between iterations to avoid overloading
            if i < ITERATIONS - 1:
                await asyncio.sleep(1)

        all_results[label] = times
        print()

    # ─── Summary Table ──────────────────────────────────────
    print(BOLD("┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐"))
    print(BOLD("│                              CHAT LATENCY SUMMARY                                                      │"))
    print(BOLD("├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤"))

    for label, times in all_results.items():
        print(stats_row(label, times))

    # Overall stats
    all_times = [t for times in all_results.values() for t in times]
    if all_times:
        print(BOLD("├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤"))
        print(stats_row(BOLD("ALL ROUTES COMBINED"), all_times))

    print(BOLD("└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘"))
    print()


# ═════════════════════════════════════════════════════════════
#              SEQUENTIAL vs PARALLEL COMPARISON
# ═════════════════════════════════════════════════════════════
async def run_concurrent_test(client: httpx.AsyncClient):
    """
    Fire 3 chat requests simultaneously to test concurrency handling.
    This simulates multiple users chatting at the same time.
    """
    print(BOLD("╔══════════════════════════════════════════════════════════════╗"))
    print(BOLD("║           SECTION 3 — CONCURRENT REQUEST TEST              ║"))
    print(BOLD("║           (3 simultaneous chat requests)                    ║"))
    print(BOLD("╚══════════════════════════════════════════════════════════════╝"))
    print()

    messages = [t["message"] for t in CHAT_TESTS]

    wall_start = time.perf_counter()
    results = await asyncio.gather(
        *[chat_request(client, msg) for msg in messages]
    )
    wall_total = (time.perf_counter() - wall_start) * 1000

    for i, (test, result) in enumerate(zip(CHAT_TESTS, results)):
        if result["ok"]:
            print(
                f"  {test['label']:<40} | "
                f"{latency_color(result['total_ms'])} | "
                f"Route: {result['route']}"
            )
        else:
            print(
                f"  {test['label']:<40} | "
                f"{RED('FAILED')} | {result['reply_preview']}"
            )

    print()
    individual_sum = sum(r["total_ms"] for r in results if r["ok"])
    print(f"  Sum of individual times:  {latency_color(individual_sum)}")
    print(f"  Wall-clock time (parallel): {latency_color(wall_total)}")
    if individual_sum > 0:
        savings = ((individual_sum - wall_total) / individual_sum) * 100
        print(f"  Parallelism savings:       {GREEN(f'{savings:.1f}%') if savings > 0 else RED(f'{savings:.1f}%')}")
    print()


# ═════════════════════════════════════════════════════════════
#                         MAIN
# ═════════════════════════════════════════════════════════════
async def main():
    print()
    print(BOLD("=" * 70))
    print(BOLD("  🔬 SAKHI WEBAPP — COMPREHENSIVE LATENCY TEST"))
    print(BOLD(f"     Target: {BASE_URL}"))
    print(BOLD(f"     User:   {USER_ID}"))
    print(BOLD(f"     Time:   {time.strftime('%Y-%m-%d %H:%M:%S')}"))
    print(BOLD("=" * 70))
    print()

    # Connectivity check
    print("  Checking server connectivity...", end="", flush=True)
    try:
        async with httpx.AsyncClient(timeout=5.0) as quick:
            resp = await quick.get(f"{BASE_URL}/")
            if resp.status_code == 200:
                print(GREEN(" ✅ Server is UP\n"))
            else:
                print(YELLOW(f" ⚠️  Server responded with {resp.status_code}\n"))
    except Exception as e:
        print(RED(f" ❌ Server is DOWN — {e}"))
        print(RED("\n  Please start the backend first:"))
        print(RED("    cd Sakhi_Webapp_Backend"))
        print(RED("    python main.py\n"))
        sys.exit(1)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Section 1: Endpoint pings
        await run_ping_tests(client)

        # Section 2: Chat latency by route
        await run_chat_tests(client)

        # Section 3: Concurrent requests
        await run_concurrent_test(client)

    print(BOLD("=" * 70))
    print(BOLD("  ✅ Test suite complete"))
    print(BOLD("=" * 70))
    print()


if __name__ == "__main__":
    asyncio.run(main())
