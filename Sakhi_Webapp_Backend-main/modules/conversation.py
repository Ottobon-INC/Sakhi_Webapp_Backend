# modules/conversation.py
from datetime import datetime
import uuid

from supabase_client import supabase_insert, supabase_select, supabase_delete


def _cleanup_old_messages(user_id: str):
    try:
        # Fetch timestamps for all messages of this user
        rows = supabase_select(
            "sakhi_conversations",
            select="created_at",
            filters=f"user_id=eq.{user_id}"
        )
        if not rows or not isinstance(rows, list) or len(rows) <= 100:
            return

        # Sort descending by created_at and find the 100th message's timestamp
        # messages are stored with isoformat strings
        sorted_times = sorted([r["created_at"] for r in rows], reverse=True)
        threshold_time = sorted_times[99]

        # Delete messages older than the threshold time
        # This will keep exactly 100 messages (or slightly more if multiple have the same timestamp as threshold)
        supabase_delete("sakhi_conversations", f"user_id=eq.{user_id}&created_at=lt.{threshold_time}")
    except Exception as e:
        print(f"Warning: Failed to cleanup old messages for user {user_id}: {e}")


def _save_message(user_id: str, message: str, lang: str, message_type: str, chat_id: str | None = None, youtube_link: str | None = None, infographic_url: str | None = None):
    payload = {
        "user_id": user_id,
        "message_text": message,
        "message_type": message_type,
        "language": lang,
        "created_at": datetime.utcnow().isoformat(),
    }
    if chat_id:
        payload["chat_id"] = chat_id
    if youtube_link:
        payload["youtube_link"] = youtube_link
    if infographic_url:
        payload["infographic_url"] = infographic_url
        
    result = supabase_insert("sakhi_conversations", payload)
    
    # After saving, cleanup old messages to keep only 100
    _cleanup_old_messages(user_id)
    
    return result


def save_user_message(user_id: str, text: str, lang: str = "en"):
    return _save_message(user_id, text, lang, "user")


def save_sakhi_message(user_id: str, text: str, lang: str = "en", youtube_link: str | None = None, infographic_url: str | None = None):
    chat_id = str(uuid.uuid4())
    return _save_message(user_id, text, lang, "sakhi", chat_id=chat_id, youtube_link=youtube_link, infographic_url=infographic_url)


def save_conversation(user_id: str, message: str, message_type: str, language: str):
    return _save_message(user_id, message, language, message_type)


def get_last_messages(user_id: str, limit: int = 5):
    """
    Fetch last N messages for a user ordered by created_at descending.
    Returns list of {"role": "user"|"sakhi", "content": "..."}.
    """
    rows = supabase_select(
        "sakhi_conversations",
        select="user_id,message_text,message_type,language,created_at",
        filters=f"user_id=eq.{user_id}",
        limit=50,  # grab recent chunk, then trim
    )

    if not rows or not isinstance(rows, list):
        return []

    sorted_rows = sorted(rows, key=lambda r: r.get("created_at", ""), reverse=True)
    recent = sorted_rows[:limit]

    history = []
    for r in reversed(recent):  # oldest to newest
        role = "user" if r.get("message_type") == "user" else "sakhi"
        history.append({"role": role, "content": r.get("message_text", "")})

    return history
