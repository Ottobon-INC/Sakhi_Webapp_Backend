import httpx
import asyncio
import time
import logging
import os
from datetime import datetime
from typing import Optional, Literal

logger = logging.getLogger("control_tower")

class ControlTowerClient:
    """
    Client for mirroring Sakhi events to the Control Tower.
    Designed to be asynchronous, non-blocking, and isolated from main chat logic.
    """
    def __init__(self):
        self.url = os.getenv("CONTROL_TOWER_URL", "http://localhost:3000/control-tower/events")
        self.api_key = os.getenv("CT_SECRET", "internal-secret-key")
        self.timeout = 2.0  # 2 seconds max as per requirements
        
    async def mirror_event(
        self, 
        thread_id: str, 
        user_id: str, 
        sender_type: Literal["user", "ai"], 
        message: str,
        channel: str = "web"
    ):
        """
        Send a non-blocking POST request to Control Tower.
        Catches all errors to ensure Sakhi continues even if Control Tower is down.
        """
        payload = {
            "thread_id": thread_id,
            "user_id": user_id,
            "channel": channel,
            "sender_type": sender_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        headers = {
            "x-internal-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        start_time = time.time()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url, 
                    json=payload, 
                    headers=headers, 
                    timeout=self.timeout
                )
                
                if response.status_code >= 400:
                    logger.warning(f"⚠️ [ControlTower] Mirroring returned status {response.status_code}: {response.text}")
                else:
                    duration = time.time() - start_time
                    logger.info(f"✅ [ControlTower] Mirrored {sender_type} message for {user_id} in {duration:.2f}s")
                    
        except httpx.TimeoutException:
            logger.error(f"⏱️ [ControlTower] Timeout ({self.timeout}s) mirroring event for {user_id}")
        except Exception as e:
            logger.error(f"❌ [ControlTower] Failed to mirror event: {str(e)}")

# Singleton instance
_client = None

def get_control_tower_client() -> ControlTowerClient:
    global _client
    if _client is None:
        _client = ControlTowerClient()
    return _client
