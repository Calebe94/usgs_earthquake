##
# USGS Earthquake
#
.POSIX:

CONTAINER=web

install:
	@poetry install

shell:
	@poetry shell

start:
	@docker-compose up -d --build

stop:
	@docker-compose down

restart: stop start

log:
	@docker-compose logs "${CONTAINER}"

logs:
	@docker-compose logs -f -t "${CONTAINER}"

# end
