
# Builds the braingeneers docker image
build:
	docker build -f docker/Dockerfile -t braingeneers/braingeneers:latest .

# Starts the full braingeneers stack of services, this is typically run
# on the braingeneers server, wherever that is hosted. These services include
# MQTT, website, listeners and other tools. This depends on docker-compose
# being installed.
start-services:
	docker-compose create && docker-compose start

# Stops the full braingeneers stack of services.
stop-services:
	docker-compose down

