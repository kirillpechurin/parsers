# Parsers
___

1. [Project objective](#project-objective)
2. [Realization](#realization)
   + [Technical part](#technical-part)
   + [Business tasks](#business-tasks)
3. [Project structure](#project-structure)
4. [Description of environment variables](#description-of-environment-variables)
5. [Launch](#launch)
   + [Requirements](#requirements)
   + [Start in docker](#start-in-docker)
___


## Project objective
Implementation of web resource parsing with the ability to conveniently 
view and download results via the web.


## Realization
___

### Technical part

#### Backend
* The application is implemented using [FastAPI](https://fastapi.tiangolo.com/).
* MongoDB is used for data storage.
* JWT is used for authorization.
* Sending emails with SMTP.
* Task management is implemented using Celery/RabbitMQ.
* The application is containerized using Docker.

#### Frontend
* The example client is implemented using [Flask](https://flask.palletsprojects.com/en/2.0.x/).
* The application is containerized using Docker.

### Business tasks
* Registration by email with confirmation of the email address.
* The ability to make order on parsing for each registered user.
* Implemented map reviews parsing - google, yandex, 2gis.


## Project structure
___
- `backend`
  - `app` - FastAPI web application.
  - `fixtures`
    - `bootstrap` - Bootstrap scripts for load fixtures.
  - `management` - Project management.
  - `src`
    - `biz` - Business-logic (services, errors).
    - `bootstrap` - Bootstrap of application.
    - `cel` - Celery configuration.
    - `parsers` - Parsers.
    - `utils` - Utilities.
  - `static`
  - `storage`
  - `.env` - Environment variables for backend.
  - `.env.example` - Example of environment variables.
  - `create_dirs.py` - Script for create dirs.
  - `loaddata.py` - Script for load fixtures.
  - `main.py` - Entrypoint of web application.
  - `requirements.txt` - Main dependencies of the web application.
- `frontend`
  - `src` - Internal package for web application client.
    - `bootstrap` - Web application client bootstrap
    - `services` - Services.
  - `templates` - HTML Templates.
  - `views` - Views
  - `.env` - environment variables for frontend.
  - `.env.example` - Example of environment variables.
  - `main.py` - Entrypoint of web application client.
  - `requirements.txt` - Main dependencies of the web application client.
- `mongodb` - MongoDB configuration.
- `nginx` - Nginx configuration.


## Description of environment variables
___

### For backend 
`File: backend/.env`

* `MAIL_SENDER_NAME` - SMTP server user.
* `MAIL_SENDER_PASSWORD` - Password for SMTP server user.
* `SECRET_KEY_TOKEN` - Secret key.
* `ALGORITHM_TOKEN` - The algorithm from the PyJWT library which will be used to perform 
  signing/verification operations on tokens.
* `MONGO_DB_USERNAME` - Database user.
* `MONGO_DB_PASSWORD` - Password for database user.
* `MONGO_DB_NAME` - Database name.
* `ADMIN_EMAIL` - Admin email.
* `STORAGE_ZIP_URL` - Storage zip url.
* `STATIC_ZIP_URL` - Static zip url.

### For frontend 
`File: frontend/.env`

* `SECRET_KEY` - Secret key.
* `PERMANENT_SESSION_DAYS` - Session days.
* `ORIGIN` - Backend url.

### For project 
`File: .env`

* `MONGO_DB_USERNAME` - Database user.
* `MONGO_DB_PASSWORD` - Password for database user.
* `MONGO_DB_NAME` - Database name.


## Launch
___

### Requirements
* Installed Python version `3.8`.
* Installed packages:
  * `docker`
  * `docker-compose`

### Start in docker
1. Create a `backend/.env` file and specify environment variables by example `backend/.env.example`
2. Create a `frontend/.env` file and specify environment variables by example `frontend/.env.example`
3. Create a `.env` file and specify environment variables by example `.env.example`
4. You are already to start! 
Run following command
```shell
docker-compose up -d --build
```

#### Load Fixtures
- Run following command for load fixtures.
```shell
docker-compose exec backend python3 loaddata.py fixtures/init_data.json
```

#### Create Dirs
- Run following command for load fixtures.
```shell
docker-compose exec backend python3 create_dirs.py
```


#### Local development server
Local development server starts on [http://localhost:80](http://localhost:80)


### Additional scripts for working with mongodb

- Entering the container
```shell
docker exec -it parsers-mongodb bash
```

- Switching to mongo
```shell
mongo
```

- Checking for user creation
  - The mongodb version supports user creation via env variables. But the user may not be created immediately.
```shell
db.auth("<username>", "<password>");
```

- Viewing all databases
```shell
show dbs
```

#### If `Authentication Failed` error.
- Please, do the following steps:
  1. `exit;` - Exit the container.
  2. `docker-compose down -v` - Delete all containers with volumes.
  3. Restart the build, log into the container and verify through authentication.

