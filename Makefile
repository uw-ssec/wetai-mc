#
# Starts the full braingeneers stack of services, this is typically run
# on the braingeneers server, wherever that is hosted. These services include
# MQTT, website, listeners and other tools. This depends on docker-compose
# being installed.
#
start-services:
	docker-compose create && docker-compose start

# Stops the full braingeneers stack of services.
stop-services:
	docker-compose down

#
# Builds the braingeneers docker image
#
update-braingeneers-image: build-braingeneers-image push-braingeneers-image

build-braingeneers-image:
	docker build -f braingeneers_docker_image/Dockerfile -t braingeneers/braingeneers:latest .

push-braingeneers-image:
	docker push braingeneers/braingeneers:latest

shell-braingeneers-image:
	docker run --rm -it braingeneers/braingeneers:latest bash

#
# S3 -> Glacier backup service
#
build-s3-glacier-backup-service:
	docker build -f service_s3_glacier_backup/Dockerfile -t braingeneers/service-s3-glacier-backup:latest service_s3_glacier_backup

push-s3-glacier-backup-service:
	docker push braingeneers/service-s3-glacier-backup:latest

shell-s3-glacier-backup-service:
	docker run --rm -it braingeneers/service-s3-glacier-backup:latest bash
