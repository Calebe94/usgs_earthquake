##
# USGS Earthquake
#
.POSIX:

CONTAINER=web

.env:
	cp .env.example .env

install: .env
	@poetry install

shell:
	@poetry shell

# I did that to insure that the front end will be built before running the Django app
start: .env build
	@docker compose up -d --build

stop:
	@docker compose down

restart: stop start

build:
	@docker compose up frontend_builder

log:
	@docker compose logs "${CONTAINER}"

logs:
	@docker compose logs -f -t "${CONTAINER}"

.PHONY: .env install shell start stop restart build log logs
# end
