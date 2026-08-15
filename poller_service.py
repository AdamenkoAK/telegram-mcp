import asyncio

from storage import MessageStorage
from telegram_client import TelegramClient


def normalize_message(message: dict) -> dict:
    sender = message.get("from", {})

    return {
        "chat_id": message["chat"]["id"],
        "message_id": message["message_id"],
        "sender_id": sender.get("id"),
        "username": sender.get("username"),
        "first_name": sender.get("first_name"),
        "text": message.get("text"),
        "sent_at": message["date"],
    }


class TelegramPoller:
    def __init__(
        self,
        telegram: TelegramClient,
        storage: MessageStorage,
    ):
        self.telegram = telegram
        self.storage = storage

    async def run(self):
        offset = None

        while True:
            updates = await self.telegram.get_updates(
                offset=offset
            )

            for update in updates:
                offset = update["update_id"] + 1

                message = update.get("message")

                if message is None:
                    continue

                normalized = normalize_message(
                    message
                )

                if normalized["text"] is None:
                    continue

                self.storage.save_message(
                    normalized
                )

                print(
                    f"Stored: {normalized['text']}"
                )

            await asyncio.sleep(0.1)