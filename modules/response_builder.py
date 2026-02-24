# modules/response_builder.py
import os
import asyncio
from typing import List, Optional, Dict, Tuple

import supabase_client  # ensures .env is loaded once
from openai import OpenAI, AsyncOpenAI

from modules.rag_search import add_kb_entry
from modules.text_utils import truncate_response
# Import from root (assuming running from main.py)
from search_hierarchical import hierarchical_rag_query, async_hierarchical_rag_query, format_hierarchical_context

_api_key = os.getenv("OPENAI_API_KEY")
client = None
async_client = None
if _api_key:
    client = OpenAI(api_key=_api_key)
    async_client = AsyncOpenAI(api_key=_api_key)

import re

# Rule-based detection for extreme latency optimization
CRITICAL_KEYWORDS = [
    "pain", "bleeding", "emergency", "accident", "broken", "severe", "worst", 
    "suicide", "hurt", "die", "kill", "hospital", "doctor", "ambulance",
    "not moving", "sharp", "cramp", "fever", "vision", "headache"
]

MEDICAL_TOPICS = [
    "ivf", "iui", "icsi", "pcos", "pcod", "fertility", "pregnant", "pregnancy",
    "egg freezing", "sperm freezing", "embryo freezing", "laparoscopy", "hysteroscopy",
    "surrogacy", "c-section", "natural birth", "postpartum"
]

def detect_language_rule_based(text: str) -> str:
    """Fast heuristic for language detection."""
    # Check for Telugu characters
    if re.search(r"[\u0c00-\u0c7f]", text):
        return "telugu"
    # Basic check for Tinglish (Telugu in Roman script) - very simplified
    # This is a placeholder; a real implementation might use more complex patterns
    tinglish_patterns = ["namaste", "ela", "unnaru", "cheppu", "enti", "ledu"]
    if any(p in text.lower() for p in tinglish_patterns):
        return "tinglish"
    return "en"

def get_signal_rule_based(text: str) -> str:
    """Keyword-based critical signal detection."""
    text_low = text.lower()
    if any(k in text_low for k in CRITICAL_KEYWORDS):
        return "YES"
    return "NO"

def get_intent_rule_based(text: str) -> str:
    """Generate intent locally based on keywords."""
    text_low = text.lower()
    if any(k in text_low for k in ["hi", "hello", "hey"]):
        return "We're so glad you're here — this is a safe space where you can ask anything."
    if any(t in text_low for t in ["thank", "thanks"]):
        return "We're touched by your gratitude, and we're always here whenever you need support."
    for topic in MEDICAL_TOPICS:
        if topic in text_low:
            return f"We're here to gently guide you through understanding {topic.upper()} with care."
    return "We're here to support you with care and understanding — you're in a safe space."

async def get_metadata_async(message: str) -> Dict[str, str]:
    """
    Optimized metadata generator:
    1. Runs rule-based detection first (~0ms).
    2. Only calls OpenAI for translation if language != English (~1.5s).
    3. If English, returns immediately, saving 1.5s.
    """
    lang = detect_language_rule_based(message)
    signal = get_signal_rule_based(message)
    intent = get_intent_rule_based(message)
    
    # If it's plain English, we skip OpenAI entirely for metadata
    if lang == "en":
        return {
            "language": "en",
            "signal": signal,
            "intent": intent,
            "translation": message
        }

    # If non-English, we still need the AI for a quality translation
    if not async_client:
        return {"language": lang, "signal": signal, "intent": intent, "translation": message}

    try:
        # We only ask for translation now, which is faster and more focused
        completion = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate to plain English. Output ONLY the translation."},
                {"role": "user", "content": message},
            ],
            temperature=0.0,
            max_tokens=200,
        )
        translation = completion.choices[0].message.content.strip()
        
        return {
            "language": lang,
            "signal": signal,
            "intent": intent,
            "translation": translation
        }
    except Exception as e:
        print(f"Metadata/Translation error: {e}")
        return {
            "language": lang,
            "signal": signal,
            "intent": intent,
            "translation": message
        }


def _classify_message_sync(message: str) -> Dict[str, str]:
    """Internal sync classifier."""
    if not client:
        return {"language": "en", "signal": "NO"}

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CLASSIFIER_PROMPT},
            {"role": "user", "content": message},
        ],
        temperature=0.2,
    )

    content = completion.choices[0].message.content
    language = ""
    signal = ""

    for line in content.splitlines():
        low = line.lower()
        if low.startswith("identified language"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                language = parts[1].strip()
        elif "[signal]" in low:
            parts = line.split(":", 1)
            if len(parts) == 2:
                signal = parts[1].strip().upper()

    return {
        "language": language or "en",
        "signal": signal or "NO",
    }


def classify_message(message: str) -> Dict[str, str]:
    """Synchronous wrapper kept for backward compatibility."""
    return _classify_message_sync(message)


async def classify_message_async(message: str) -> Dict[str, str]:
    """Native async version — uses AsyncOpenAI directly, no thread pool."""
    if not async_client:
        return {"language": "en", "signal": "NO"}

    try:
        completion = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.2,
        )

        content = completion.choices[0].message.content
        language = ""
        signal = ""

        for line in content.splitlines():
            low = line.lower()
            if low.startswith("identified language"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    language = parts[1].strip()
            elif "[signal]" in low:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    signal = parts[1].strip().upper()

        return {
            "language": language or "en",
            "signal": signal or "NO",
        }
    except Exception as e:
        print(f"Classification error: {e}")
        return {"language": "en", "signal": "NO"}


def _friendly_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    trimmed = name.strip()
    if not trimmed:
        return None
    lowered = trimmed.lower()
    if lowered in {"null", "none", "user", "test", "unknown"}:
        return None
    # shorten if very long
    parts = trimmed.split()
    candidate = parts[0]
    if len(candidate) > 14:
        candidate = candidate[:14]
    return candidate


def _build_history_block(history: Optional[List[Dict[str, str]]]) -> str:
    if not history:
        return "### Conversation History:\nNone."
    lines = ["### Conversation History:"]
    for msg in history:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def generate_smalltalk_response(
    prompt: str,
    target_lang: str,
    history: Optional[List[Dict[str, str]]],
    user_name: Optional[str] = None,
    store_to_kb: bool = False,
) -> str:
    user_name = _friendly_name(user_name)
    history_block = _build_history_block(history)
    has_history = bool(history)
    name_line = f"User name: {user_name}" if user_name else "User name: Not provided"
    greeting_rule = (
        "If this is the first turn, start with a warm greeting and the name (e.g., 'Hi <name>,'). "
        "If this is a follow-up, do NOT say 'Hi' again; instead give a brief caring acknowledgement with the name (e.g., '<name>, I'm here for you.'). "
        "If no usable name, use a gentle greeting without a name."
    )
    system_content = (
        "You are Sakhi, an emotional south indian companion.\n"
        "User is NOT asking medical questions.\n"
        "Give a warm, supportive, friendly, empathetic reply.\n"
        "Avoid medical or fertility information completely.\n"
        f"{greeting_rule}\n"
        "Match the language of the user prompt: respond ONLY in target_lang. "
        "If target_lang is Tinglish, write Telugu words using Roman letters; do not switch to English.\n"
        "Keep sentences short, clear, and grammatically simple. For Tinglish, use natural, easy-to-read Roman Telugu (no awkward transliterations).\n"
        "Keep the tone conversational like two people chatting; avoid headings or bullet labels. Use full stops/commas naturally.\n"
        f"{name_line}\n"
        "Address the user by name when available; if the name is long, use a shorter friendly form.\n"
        "Maintain continuity using the conversation history.\n"
        f"{history_block}"
    )

    if not client:
        return "I'm here to support you with warmth and care. (Missing API Key for full response)"

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    final_text = completion.choices[0].message.content
    
    # Truncate response to maximum 2000 characters
    final_text = truncate_response(final_text)

    return final_text


async def generate_medical_response(
    prompt: str,
    target_lang: str,
    history: Optional[List[Dict[str, str]]],
    user_name: Optional[str] = None,
    kb_results: Optional[List[dict]] = None,
) -> Tuple[str, List[dict]]:
    """
    Medical path: RAG + history. (ASYNC — native non-blocking I/O)
    Returns (final_text, kb_results)
    """
    # Use pre-fetched RAG results if available, otherwise fetch now
    if kb_results is None:
        kb_results = await async_hierarchical_rag_query(prompt)
    
    context_text = format_hierarchical_context(kb_results)
    
    history_block = _build_history_block(history)

    user_name = _friendly_name(user_name)
    name_line = f"User name: {user_name}" if user_name else "User name: Not provided"
    has_history = bool(history)
    greeting_rule = (
        "If this is the first turn, start with a warm greeting and the name (e.g., 'Hi <name>,'). "
        "If this is a follow-up, do NOT say 'Hi' again; instead give a brief caring acknowledgement with the name (e.g., '<name>, I understand.'). "
        "If no usable name, use a gentle greeting without a name."
    )
    system_content = (
        "You are Sakhi, a warm emotional south indian companion but medically safe.\n"
        "Use retrieved knowledge when available. If none is retrieved, you may give general, high-level, medically safe guidance.\n"
        "Be conservative and clearly state when guidance is general; advise consulting a doctor for specifics.\n"
        f"{greeting_rule}\n"
        "Match the language of the user prompt: respond ONLY in target_lang. "
        "If target_lang is Tinglish, write Telugu words using Roman letters; do not switch to English.\n"
        "Keep sentences short, clear, and grammatically simple. For Tinglish, use natural, easy-to-read Roman Telugu (no awkward transliterations).\n"
        "\n"
        "MANDATORY RESPONSE STRUCTURE:\n"
        "1. Write your main conversational reply with caring tone. If a usable name is available, open with it naturally.\n"
        "2. After the main reply, add EXACTLY two newline characters.\n"
        "3. Write ' Follow ups : ' (space before 'Follow', space after 'ups', space after colon).\n"
        "4. Immediately after the colon and space (NO extra newlines), write the first question.\n"
        "5. Each subsequent question goes on a new line.\n"
        "\n"
        "EXACT FORMAT TO FOLLOW:\n"
        "[Your main reply here, ending with punctuation.]\n"
        "\n"
        " Follow ups : What is your first question?\n"
        "What is your second question?\n"
        "What is your third question?\n"
        "\n"
        "CRITICAL: Do NOT add blank lines after ' Follow ups : ' - the first question must appear immediately.\n"
        "IMPORTANT: Each follow-up question MUST be under 65 characters long.\n"
        f"Always answer in {target_lang}.\n"
        f"{name_line}\n"
        "Address the user by name when available; if the name is long, use a shorter friendly form.\n"
        "Maintain continuity using the conversation history.\n"
        f"{history_block}"
    )

    if context_text:
        system_content += f"\n\n{context_text}"
        system_content += (
            "\nUse the above knowledge directly. If something is unclear, stay conservative and safe."
        )
    else:
        system_content += (
            "\n\n### Retrieved Knowledge:\nNone."
            "\nNo KB retrieved. Provide general, high-level, medically safe guidance."
            "\nState clearly that advice is general and suggest consulting a doctor for specifics."
        )

    if not async_client:
        return "I understand your concern. Since my medical brain is currently offline (Missing API Key), I recommend consulting a doctor for specific guidance.", []

    completion = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    final_text = completion.choices[0].message.content
    
    # Truncate response to maximum 2000 characters
    final_text = truncate_response(final_text)

    return final_text, kb_results


# Intent generation system prompt
INTENT_GENERATOR_PROMPT = """You are generating intent for a patient-facing fertility care application.

The intent must be written as if the APPLICATION is speaking directly to the patient.

Rules:
- Write in first-person plural or neutral guiding voice (e.g., "We aim to…", "This is meant to…")
- Include empathy, reassurance, or emotional safety
- Be warm, calm, and supportive
- Use ONE sentence only
- Do not mention "user", "message", or "intent"
- Do not give medical advice or technical explanations
- Assume the reader may be anxious, confused, or emotionally vulnerable

Based on the patient's question, generate a single warm, empathetic sentence that describes why the application is responding.

IMPORTANT: Output ONLY the intent sentence, nothing else. No quotes, no labels, just the sentence."""


def _generate_intent_sync(query: str) -> str:
    """Internal sync intent generator."""
    if not client:
        return "We're here to support you with care and understanding — you're in a safe space."
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": INTENT_GENERATOR_PROMPT},
                {"role": "user", "content": f"Patient's question: {query}"},
            ],
            temperature=0.7,
            max_tokens=100,
        )
        intent = completion.choices[0].message.content.strip()
        intent = intent.strip('"\'')
        return intent
    except Exception:
        return "We're here to support you with care and understanding — you're in a safe space."


def generate_intent(query: str) -> str:
    """Synchronous wrapper kept for backward compatibility."""
    return _generate_intent_sync(query)


async def generate_intent_async(query: str) -> str:
    """Native async version — uses AsyncOpenAI directly, no thread pool."""
    if not async_client:
        return "We're here to support you with care and understanding — you're in a safe space."
    try:
        completion = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": INTENT_GENERATOR_PROMPT},
                {"role": "user", "content": f"Patient's question: {query}"},
            ],
            temperature=0.7,
            max_tokens=100,
        )
        intent = completion.choices[0].message.content.strip()
        intent = intent.strip('"\'')
        return intent
    except Exception:
        return "We're here to support you with care and understanding — you're in a safe space."


async def translate_to_english_async(text: str) -> str:
    """
    Translate user query to English for better internal routing and search.
    Only translates if input is likely non-English or mixed.
    """
    if not async_client:
        return text

    try:
        # Detect if it's already plain English (simple heuristic)
        # If it's mostly ASCII and no obvious non-English scripts, we might skip,
        # but for routing accuracy, a quick translate call is safer.
        
        completion = await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate the following user message to plain English for internal technical processing. Output ONLY the translation."},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
            max_tokens=150,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text

