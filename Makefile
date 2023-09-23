SHELL := /bin/bash


docker:
	docker-compose up --build redis

deploy:
	/bin/bash deploy.sh