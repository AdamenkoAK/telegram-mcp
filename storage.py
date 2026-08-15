import sqlite3


class MessageStorage:
    def __init__(self, db_path: str = "telegram_messages.db") -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    message_id INTEGER NOT NULL,
                    sender_id INTEGER,
                    username TEXT,
                    first_name TEXT,
                    text TEXT,
                    sent_at INTEGER NOT NULL,
                    UNIQUE(chat_id, message_id)
                )
                """
            )

    def save_message(self, message: dict) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO messages (
                    chat_id,
                    message_id,
                    sender_id,
                    username,
                    first_name,
                    text,
                    sent_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    message["chat_id"],
                    message["message_id"],
                    message["sender_id"],
                    message["username"],
                    message["first_name"],
                    message["text"],
                    message["sent_at"],
                ),
            )

    def get_recent_messages(
        self,
        chat_id: int,
        limit: int = 20,
    ) -> list[dict]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT
                    chat_id,
                    message_id,
                    sender_id,
                    username,
                    first_name,
                    text,
                    sent_at
                FROM messages
                WHERE chat_id = ?
                ORDER BY sent_at DESC
                LIMIT ?
                """,
                (
                    chat_id,
                    limit,
                ),
            ).fetchall()

        messages = []

        for row in reversed(rows):
            messages.append(
                {
                    "chat_id": row["chat_id"],
                    "message_id": row["message_id"],
                    "sender_id": row["sender_id"],
                    "username": row["username"],
                    "first_name": row["first_name"],
                    "text": row["text"],
                    "sent_at": row["sent_at"],
                }
            )

        return messages