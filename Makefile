SHELL := /bin/zsh


compose-db:
	docker compose -f docker-compose.dev.yml up --build redis

compose-bot:
	docker compose -f docker-compose.dev.yml up --build bot

deploy:
	/bin/bash deploy.sh

polling:
	python ./bot/polling.py
