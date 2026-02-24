import httpx
import json
import sys
import time

BASE_URL = "http://localhost:8100"
CHAT_URL = f"{BASE_URL}/sakhi/chat"


def query_sakhi(message: str, user_id: str):
    payload = {
        "user_id": user_id,
        "message": message,
        "language": "en"
    }

    print(f"\n{'─'*55}")
    print(f"📡  Endpoint : POST {CHAT_URL}")
    print(f"💬  Message  : {message}")
    print(f"{'─'*55}")

    t0 = time.perf_counter()
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(CHAT_URL, json=payload)
        elapsed = time.perf_counter() - t0

        status_icon = "✅" if response.status_code == 200 else "❌"
        print(f"{status_icon}  Status  : HTTP {response.status_code}")
        print(f"⏱️   Latency : {elapsed:.2f}s  (client-side round-trip)")

        if response.status_code == 200:
            data = response.json()
            print(f"\n🤖  Sakhi   : {data.get('reply', '[no reply]')}")
            route  = data.get("route")
            mode   = data.get("mode")
            lang   = data.get("language")
            intent = data.get("intent")
            extras = []
            if route:   extras.append(f"route={route}")
            if mode:    extras.append(f"mode={mode}")
            if lang:    extras.append(f"lang={lang}")
            if intent:  extras.append(f"intent={intent}")
            if extras:
                print(f"📌  Info    : {' | '.join(extras)}")
        else:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            print(f"📄  Detail  : {detail}")

    except httpx.ConnectError:
        print("❌  ERROR: Cannot connect to server. Is it running on port 8100?")
    except httpx.TimeoutException:
        print("❌  ERROR: Request timed out after 120s.")
    except Exception as e:
        print(f"❌  ERROR: {e}")

    print(f"{'─'*55}")


def get_user_id():
    """Prompt user to enter their user_id."""
    print("=" * 55)
    print("  🌸  Sakhi Interactive Query Terminal")
    print(f"  🔗  Server : {BASE_URL}")
    print("=" * 55)
    print()
    print("Enter your user_id (from Supabase / DB).")
    print("💡  Tip: You can find it in Supabase → users table.")
    print("    Leave blank to use phone number instead.")
    print()
    user_id = input("user_id ▶  ").strip()
    if not user_id:
        phone = input("phone   ▶  ").strip()
        if not phone:
            print("❌ No user_id or phone provided. Exiting.")
            sys.exit(1)
        return None, phone
    return user_id, None


def interactive_mode(user_id: str, phone: str = None):
    print()
    if user_id:
        print(f"  👤  User ID : {user_id}")
    else:
        print(f"  📞  Phone   : {phone}")
    print("  Type your message and press Enter.")
    print("  Type 'exit' or press Ctrl+C to quit.")
    print("=" * 55)

    # Build payload key
    id_key   = "user_id"   if user_id else "phone_number"
    id_value = user_id     if user_id else phone

    while True:
        try:
            msg = input("\nYou ▶  ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋  Goodbye!")
            break

        if not msg:
            continue
        if msg.lower() in ("exit", "quit", "bye"):
            print("👋  Goodbye!")
            break

        # Rebuild payload each time with correct key
        payload = {id_key: id_value, "message": msg, "language": "en"}

        print(f"\n{'─'*55}")
        print(f"📡  Endpoint : POST {CHAT_URL}")
        print(f"💬  Message  : {msg}")
        print(f"{'─'*55}")

        t0 = time.perf_counter()
        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(CHAT_URL, json=payload)
            elapsed = time.perf_counter() - t0

            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon}  Status  : HTTP {response.status_code}")
            print(f"⏱️   Latency : {elapsed:.2f}s  (client-side round-trip)")

            if response.status_code == 200:
                data = response.json()
                print(f"\n🤖  Sakhi   : {data.get('reply', '[no reply]')}")
                route  = data.get("route")
                mode   = data.get("mode")
                lang   = data.get("language")
                intent = data.get("intent")
                extras = []
                if route:   extras.append(f"route={route}")
                if mode:    extras.append(f"mode={mode}")
                if lang:    extras.append(f"lang={lang}")
                if intent:  extras.append(f"intent={intent}")
                if extras:
                    print(f"📌  Info    : {' | '.join(extras)}")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                print(f"📄  Detail  : {detail}")

        except httpx.ConnectError:
            print("❌  ERROR: Cannot connect. Is the server running on port 8100?")
        except httpx.TimeoutException:
            print("❌  ERROR: Request timed out after 120s.")
        except Exception as e:
            print(f"❌  ERROR: {e}")

        print(f"{'─'*55}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Usage: python query_server.py <user_id> "your message"
        uid = sys.argv[1]
        msg = " ".join(sys.argv[2:])
        query_sakhi(msg, uid)
    else:
        uid, phone = get_user_id()
        interactive_mode(uid, phone)
