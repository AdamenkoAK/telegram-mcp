import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress

from dotenv import load_dotenv
from mcp.server import MCPServer

from poller_service import TelegramPoller
from storage import MessageStorage
from telegram_client import TelegramClient


load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


telegram = TelegramClient(BOT_TOKEN)

storage = MessageStorage()
storage.initialize()

poller = TelegramPoller(
    telegram,
    storage,
)


@asynccontextmanager
async def app_lifespan(_: MCPServer) -> AsyncIterator[None]:
    poller_task = asyncio.create_task(poller.run())

    try:
        yield
    finally:
        poller_task.cancel()
        with suppress(asyncio.CancelledError):
            await poller_task
        await telegram.close()


mcp = MCPServer(
    "Telegram MCP Bridge",
    version="0.1.0",
    lifespan=app_lifespan,
)


@mcp.tool()
async def send_message(
    chat_id: int,
    text: str,
) -> dict:
    """Send a Telegram message."""

    message = await telegram.send_message(
        chat_id,
        text,
    )

    return {
        "ok": True,
        "message_id": message["message_id"],
        "chat_id": message["chat"]["id"],
        "text": message.get("text"),
    }


@mcp.tool()
async def get_chat_info(
    chat_id: int,
) -> dict:
    """Get Telegram chat information."""

    chat = await telegram.get_chat_info(
        chat_id
    )

    return {
        "id": chat["id"],
        "type": chat["type"],
        "username": chat.get("username"),
        "first_name": chat.get("first_name"),
    }


@mcp.tool()
async def get_recent_messages(
    chat_id: int,
    limit: int = 20,
) -> list[dict]:
    """Get recent Telegram messages."""

    return storage.get_recent_messages(
        chat_id,
        limit,
    )


if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )
