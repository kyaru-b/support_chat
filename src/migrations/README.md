# Database Migrations

This directory contains SQL migration files and a runner script.

## How to run migrations

Run the following command from the project root directory:

```bash
python -m src.main
python -m src.migrations.runner
```

## Files

- `001_init.sql`: Initial schema creation for users, tickets, and messages.
- `main.py`: Python script using to start main app and connect to db
- `runner.py`: Python script to execute the SQL migrations using `asyncpg`.
