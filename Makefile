.PHONY: up down

CURRENT_HOSTNAME := $(shell hostname)

ifeq ($(CURRENT_HOSTNAME), 1738991-cy22118.twc1.net)
    COMPOSE_FILE = docker-compose_prod.yml
else
    COMPOSE_FILE = docker_compose_local.yml
endif

up:
	docker-compose -f $(COMPOSE_FILE) up

build:
	docker-compose -f $(COMPOSE_FILE) up --build

down:
	docker-compose -f $(COMPOSE_FILE) down

log_report:
	docker exec -it all_in_one-report_bot-1 /bin/sh -c "cat bot.log"

log_guru:
	docker exec -it all_in_one-guide_guru-1 /bin/sh -c "cat bot.log"

debug:
	@echo "Current Hostname: $(CURRENT_HOSTNAME)"
	@echo "Using Compose File: $(COMPOSE_FILE)"


