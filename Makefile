# Include environment variables from .env file
ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

# Activate virtual environment (Note: This might not work as expected within Makefile)

act:
	. sync_venv/bin/activate && python3

# Docker commands
build:
	docker-compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

# Django commands
serv:
	python3 manage.py runserver

mmig: # Run with "make mmig" or "make mmig app='app'"
	if [ -z "$(app)" ]; then \
		python3 manage.py makemigrations; \
	else \
		python3 manage.py makemigrations "$(app)"; \
	fi

mig: # Run with "make mig" or "make mig app='app'"
	if [ -z "$(app)" ]; then \
		python3 manage.py migrate; \
	else \
		python3 manage.py migrate "$(app)"; \
	fi

init:
	python3 manage.py initial_data

test:
	pytest --disable-warnings -vv -x

shell:
	python3 manage.py shell

suser:
	python3 manage.py createsuperuser

cpass:
	python3 manage.py changepassword

# Install Python dependencies from requirements.txt
reqm:
	pip install -r requirements.txt

# Update requirements.txt with installed packages
ureqm:
	pip freeze > requirements.txt

# Generate a random Django secret key
secretk:
	python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  act          Activate virtual environment (Note: Might not work as expected)"
	@echo "  build        Build Docker images and start containers"
	@echo "  up           Start Docker containers"
	@echo "  down         Stop and remove Docker containers"
	@echo "  show-logs    Show logs for Docker containers"
	@echo "  serv         Run Django development server"
	@echo "  mmig         Make Django database migrations"
	@echo "  mig          Apply Django database migrations"
	@echo "  init         Initialize data in the database"
	@echo "  test         Run tests using pytest"
	@echo "  shell        Open Django shell"
	@echo "  suser        Create superuser"
	@echo "  cpass        Change password for a user"
	@echo "  reqm         Install Python dependencies from requirements.txt"
	@echo "  ureqm        Update requirements.txt with installed packages"
	@echo "  secretk      Generate a random Django secret key"
