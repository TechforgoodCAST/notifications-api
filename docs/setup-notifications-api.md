# How to setup Notifications API

ℹ️ **Before running through the steps below, please ensure you've completed all the steps in our [Setup Python Dev Environment](./setup-python-dev-environment.md) documentation.**

## Downloading the `notifications-api` application

First, let's clone the notifications-api codebase from GitHub:

```
git clone git@github.com:bitzesty/notifications-api.git
```

Next, let's use the `virtualenv` tool to create a new (virtual) environment into which our Python dependencies will be installed. Using `virtualenv` allows us to keep our dependencies separate between Python projects, avoiding any chance of conflicts between different applications.

```
virtualenv venv
source venv/bin/activate
```

ℹ️ **It's important to note that you'll need to run the above `activate` command each time you `cd` into a project's codebase.**

## Setup the `Postgresql` database and `Redis` cache within `Docker`

The next step requires you to have `Docker` and `Docker Compose` installed on your computer.  

Visit the [Docker Website](https://docs.docker.com/get-docker/) to download the installation package for all major operating systems.  

For Windows and MacOS users, `Docker Compose` should have been installed as part of the main Docker installation. For Linux users, you'll need to install Docker Compose separately by following [these instructions](https://docs.docker.com/compose/install/) from the Docker Compose website.

Once you have `Docker` and `Docker Compose` installed, it's time to spin up some containers running our core dependencies.  

The `notifications-api` application depends upon a `Postgresql` database and `Redis` cache in order to operate correctly. Rather than requiring developers to run these services locally, we've provided a `Docker Compose` configuration that'll download prebuilt containers, configured to "just work" with the `notifications-api` application running on your localhost.  

To start `Postgresql` and `Redis` within Docker, simply run the command below.

```
docker-compose -f docker/docker-compose-development.yml up
```

ℹ️ **If Docker is struggling to intialize the `Postgresql` container, take a moment to ensure you don't have `postgres` running locally as the processes will fight over the same local port (`5432`).**


 ## Bootstrapping the notifications-api application for local development

  Next, we can install dependencies, configuring our local development environment with minimal fuss and effort.
  ```
  make bootstrap
  ```

 ## How to run the application

 Congratulations, you're all set to run the `notifications-api` application locally:

```
scripts/run_app.sh # Starts the API server on localhost:6011
scripts/run_celery.sh # Starts the background worker (Celery) to run background jobs
```

You should now be able to query the API on localhost:6011:

```
curl localhost:6011
{
  "status": "ok"
}
```
