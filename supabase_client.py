# supabase_client.py

import os
import uuid
import time
from typing import Any, Dict, Optional

import httpx
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Ensure .env is loaded exactly once from this module
_ENV_LOADED = False


def _ensure_env_loaded() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    load_dotenv()
    _ENV_LOADED = True


_ensure_env_loaded()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise Exception("Supabase environment variables missing")

HEADERS = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

from supabase.lib.client_options import ClientOptions

opts = ClientOptions().replace(
    postgrest_client_timeout=60,
    storage_client_timeout=60,
    schema="public",
)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, options=opts)

# ================================================
# HIGH-PERFORMANCE ASYNC DB CLIENT (Connection Pool)
# ================================================
_async_client: Optional[httpx.AsyncClient] = None


async def get_db_client() -> httpx.AsyncClient:
    """Return the shared async HTTP client. Initialized once at startup."""
    global _async_client
    if _async_client is None:
        _async_client = httpx.AsyncClient(
            base_url=f"{SUPABASE_URL}/rest/v1",
            headers=HEADERS,
            timeout=30.0,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
    return _async_client


async def close_db_client():
    """Close the shared async HTTP client. Called at server shutdown."""
    global _async_client
    if _async_client:
        await _async_client.aclose()
        _async_client = None


# =============================================================================
# ASYNC OPERATIONS (Using Connection Pooling — for chat hot path)
# =============================================================================

async def async_supabase_insert(table: str, data: Dict[str, Any]):
    """Async insert using pooled connection."""
    client = await get_db_client()
    resp = await client.post(f"/{table}", json=data)
    if resp.status_code >= 300:
        raise Exception(f"Supabase insert failed: {resp.status_code} - {resp.text}")
    return resp.json()


async def async_supabase_select(
    table: str,
    select: str = "*",
    filters: str = "",
    limit: Optional[int] = None,
    rpc: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
):
    """Async select/RPC using pooled connection."""
    client = await get_db_client()
    if rpc:
        resp = await client.post(f"/rpc/{rpc}", json=payload or {})
    else:
        query_params = {"select": select}
        if filters:
            for f in filters.split("&"):
                if "=" in f:
                    k, v = f.split("=", 1)
                    query_params[k] = v
        if limit:
            query_params["limit"] = str(limit)
        resp = await client.get(f"/{table}", params=query_params)

    if resp.status_code >= 300:
        raise Exception(f"Supabase select failed: {resp.status_code} - {resp.text}")
    return resp.json()


async def async_supabase_rpc(function_name: str, params: Dict[str, Any]):
    """Async RPC call using pooled connection."""
    return await async_supabase_select(table="", rpc=function_name, payload=params)


# =============================================================================
# LEGACY SYNC OPERATIONS (kept for non-chat paths)
# =============================================================================

def supabase_insert(table: str, data: Dict[str, Any]):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code >= 300:
        raise Exception(f"Supabase insert failed: {resp.status_code} - {resp.text}")
    return resp.json()


def supabase_select(
    table: str,
    select: str = "*",
    filters: str = "",
    limit: Optional[int] = None,
    rpc: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
):
    """
    Fetch rows from a table or call an RPC when rpc is provided.
    """
    if rpc:
        url = f"{SUPABASE_URL}/rest/v1/rpc/{rpc}"
        resp = requests.post(url, headers=HEADERS, json=payload or {})
    else:
        base_query = f"{SUPABASE_URL}/rest/v1/{table}?select={select}"
        if filters:
            base_query = f"{base_query}&{filters}"
        if limit:
            base_query = f"{base_query}&limit={limit}"
        resp = requests.get(base_query, headers=HEADERS)

    if resp.status_code >= 300:
        raise Exception(f"Supabase select failed: {resp.status_code} - {resp.text}")
    return resp.json()


def supabase_update(table: str, match: str, data: Dict[str, Any]):
    """
    match example: \"user_id=eq.<id>\"
    """
    url = f"{SUPABASE_URL}/rest/v1/{table}?{match}"
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code >= 300:
        raise Exception(f"Supabase update failed: {resp.status_code} - {resp.text}")
    return resp.json()


def generate_user_id() -> str:
    return str(uuid.uuid4())


def supabase_rpc(function_name: str, params: Dict[str, Any]):
    """
    Call a Postgres function via Supabase RPC.
    """
    res = supabase.rpc(function_name, params=params).execute()

    # supabase-py returns data and possibly error on the response object
    if hasattr(res, "error") and res.error:
        raise Exception(f"Supabase RPC error: {res.error}")

    if hasattr(res, "data"):
        return res.data

    return res
