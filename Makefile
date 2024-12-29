SHELL := /bin/zsh

polling:
	(set -a && source .env && cd ./bot && uv run polling.py)

compose-db:
	set -a && source .env && docker compose -f docker-compose.dev.yml up --build redis

compose-bot:
	set -a && source .env && docker compose -f docker-compose.dev.yml up --build bot

db-migrate:
	(set -a && source .env && cd ./bot && uv run migrate.py)

deploy:
	/bin/bash deploy.sh
