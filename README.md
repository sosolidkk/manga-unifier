# manga-unifier
Personal project to test scraping architecture with Django and DRF

## Dependencies

This project is built with:

* Python (3.8.0)
* Poetry
* Django
* DjangoRestFramework
* Docker
* Postgres
* Unittest

## Setup

As we are using Docker for this project, you do not need to configure it locally, just make sure Docker is installed on your machine. Follow these steps:

```shell
# To build the application
docker-compose build
# To run the application
docker-compose up -d app # docker-compose up --build -d app
# For testing
docker-compose run --rm integration-tests
# Check linters
docker-compose run --rm <command>
```
