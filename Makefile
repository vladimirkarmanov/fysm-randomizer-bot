SHELL := /bin/zsh


docker:
	docker-compose up --build redis

deploy:
	/bin/bash deploy.sh

polling:
	python ./bot/polling.py
