from typing import Any

import httpx


class TelegramClient:
    def __init__(self, token: str) -> None:
        self.client = httpx.AsyncClient(
            base_url=f"https://api.telegram.org/bot{token}",
            timeout=httpx.Timeout(40.0),
        )

    async def close(self):
        await self.client.aclose()

    async def _request(
        self,
        method: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        response = await self.client.post(
            f"/{method}",
            json=payload or {},
        )

        response.raise_for_status()

        data = response.json()

        return data["result"]

    async def send_message(
        self,
        chat_id: int,
        text: str,
    ) -> dict:
        return await self._request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
            },
        )

    async def get_chat_info(
        self,
        chat_id: int,
    ) -> dict:
        return await self._request(
            "getChat",
            {
                "chat_id": chat_id,
            },
        )

    async def get_updates(
        self,
        offset: int | None = None,
    ) -> list[dict]:
        payload = {
            "timeout": 30,
        }

        if offset is not None:
            payload["offset"] = offset

        return await self._request(
            "getUpdates",
            payload,
        )