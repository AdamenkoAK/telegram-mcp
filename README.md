# Telegram MCP Server

MCP-сервер для управления Telegram через AI-ассистентов.

Сервер выступает мостом между LLM и Telegram Bot API и предоставляет
инструменты для: - отправки сообщений в Telegram; - получения информации
о чатах; - получения последних сообщений из чатов.

## Возможности

Доступные MCP tools:

### `send_message`

Отправляет сообщение в Telegram-чат.

Параметры: - `chat_id` --- ID Telegram-чата - `text` --- текст сообщения

### `get_chat_info`

Возвращает информацию о Telegram-чате.

Параметр: - `chat_id` --- ID Telegram-чата

### `get_recent_messages`

Возвращает последние сохранённые сообщения из Telegram-чата.

Параметры: - `chat_id` --- ID Telegram-чата - `limit` --- количество
сообщений

## Архитектура

    AI Assistant
          |
          v
     MCP Server
          |
          +----------------+
          |                |
          v                v
    Telegram Bot API    SQLite
          |
          v
     Telegram Chat

Компоненты:

    server.py
        MCP tools и запуск сервера

    telegram_client.py
        Клиент для Telegram Bot API

    storage.py
        SQLite-хранилище сообщений

    poller_service.py
        Фоновый сбор новых сообщений Telegram

## Установка

Создать виртуальное окружение:

``` bash
python -m venv .venv
```

Активировать:

``` bash
source .venv/bin/activate
```

Установить зависимости:

``` bash
pip install -r requirements.txt
```

## Настройка Telegram Bot

Создать бота через BotFather и получить токен.

Создать файл `.env`:

``` env
TELEGRAM_BOT_TOKEN=your_token_here
```

## Запуск MCP Inspector

``` bash
npx @modelcontextprotocol/inspector python server.py
```

Доступные tools:

-   `send_message`
-   `get_chat_info`
-   `get_recent_messages`

## Хранение сообщений

Сервер получает новые сообщения через Telegram `getUpdates` и сохраняет
их в локальную SQLite базу.

SQLite используется как локальное хранилище сообщений без необходимости
отдельного сервера базы данных.

## Требования

-   Python 3.13+
-   Telegram Bot API
-   MCP SDK
-   httpx
-   python-dotenv
