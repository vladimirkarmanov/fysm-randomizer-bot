SHELL := /bin/zsh

polling:
	env PYTHONPATH=bot uv run ./bot/telegram/polling.py

compose-db:
	set -a && source .env && docker compose -f docker-compose.dev.yml up --build postgres redis

compose-bot:
	set -a && source .env && docker compose -f docker-compose.dev.yml up --build bot

db-migrate:
	(set -a && source .env && env PYTHONPATH=bot uv run ./bot/infra/db/migrate.py)

deploy:
	/bin/bash deploy.sh
