SHELL := /bin/zsh

polling:
	(set -a && source .env.local && cd ./bot && uv run polling.py)

compose-db:
	set -a && source .env.local && docker compose -f docker-compose.dev.yml up --build redis

compose-bot:
	set -a && source .env.local && docker compose -f docker-compose.dev.yml up --build bot

deploy:
	/bin/bash deploy.sh
