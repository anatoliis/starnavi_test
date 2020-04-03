# Take-home task

by Anatolii S.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run this application you will need `docker` and `docker-compose` installed in your system.

### Building and executing
- This application requires several environment variables to be set in order to be successfully built and executed.
These variables are automatically picked up from `.env` file inside project root folder by `docker-compose`.
Or you can use existing sample `.env.docker` file, which will be enough to run the application (see next step).

- Build and run Docker containers with Django application, PostgreSQL, Redis and Nginx:
```
$ docker-compose --env-file=.env.docker up --build
```

- Now you can access the API under:
    
    [http://localhost:80/api/][http://localhost:80/api/redoc/]

- Automatically generated OpenAPI documentation will be available here:

    http://localhost:80/api/redoc/

## Prepare virtual environment
_It might be needed for executing tests or running "automated_bot" script._

- As a prerequisite, you must have `pipenv` installed in your system. If you don't have it yet, run:
```
$ pip install pipenv
```

- Set up virtual environment with all required dependencies by executing the following command inside project root:
```
$ pipenv install --dev
```

- Activate virtual environment:
```
$ pipenv shell
```

- Make a copy of `social_network/.env.example` copy and name it `social_network/.env` by executing (in project root folder):
```
$ cp social_network/{.env.example,.env}
```

- Apply Django migrations:
```
$ python manage.py migrate
```

## Running the tests

- Run `py.test` inside project root.

## Executing automated script

All automated bot settings are located in default file:
```
automated_bot/autobot.ini
```

Example contents:
```
[DEFAULT]
number_of_users=100
max_posts_per_user=20
max_likes_per_user=100
```

To execute automated bot use command:
```
python automated_bot/autobot.py
```

It will use the default configuration file and will try to find root API endpoint under address: http://localhost:80/api/ 

Several command line arguments are available though:
```
$ python automated_bot/autobot.py --help
usage: autobot.py [-h] [-c CONFIG] [-u URL]

optional arguments:
  -h, --help                    show this help message and exit
  -c CONFIG, --config CONFIG    Path to configuration file (default: "./autobot.ini")
  -u URL, --url URL             API root URL (default: "http://127.0.0.1:80/api/")
```


[http://localhost:80/api/redoc/]: http://localhost:80/api/
