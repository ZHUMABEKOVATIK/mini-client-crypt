# Deribit Price Tracker

Сервис, который раз в минуту забирает индексные цены BTC/USD и ETH/USD с криптобиржи Deribit,
сохраняет их в PostgreSQL и отдаёт через REST API на FastAPI.

## Стек

- Python 3.14, FastAPI, SQLAlchemy 2.0 (async)
- PostgreSQL
- Celery + Redis - Для сбора цены (раз в минуту)
- aiohttp — клиент для Deribit API
- Docker / docker-compose
- pytest - юнит-тесты (SQLite in-memory, без внешних зависимостей)

## Быстрый запуск

```bash
cp .env.example .env
docker compose up --build
```

API будет доступно на `http://localhost:8000`, документация - `http://localhost:8000/docs`.

## Сервисы 

| Название сервиса | Стек |
|---|---|
| `app` | FastAPI |
| `db` | Postgres |
| `redis` | Redis |
| `celery-worker` | Celery |
| `celery-beat` | Celery |

## Эндпоинты

| Метод | Путь | Описание | Query-параметр |
|---|---|---|---|
| GET | `/api/price?ticker=btc_usd` | Все сохранённые данные по тикеру | `ticker` |
| GET | `/api/price/latest?ticker=btc_usd` | Последняя цена по тикеру | `ticker` |
| GET | `/api/price/history?ticker=btc_usd&date_from=...&date_to=...` | Цены с фильтром по дате | `ticker` |

## Тесты

```bash
uv run pytest -v
```