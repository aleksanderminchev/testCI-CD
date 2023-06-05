TopTutors Flask-react application
===============

# Backend Python API
### Run API locally

Set up a Python 3 virtualenv and install the dependencies on it:

```bash
cd toptutors-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
The application runs on `localhost:5000`

### Use Flake8 as linter.

## Troubleshooting

On macOS Monterey and newer, Apple decided to use port 5000 for its AirPlay
service, which means that the API server will not be able to run on
this port. There are two possible ways to solve this problem:

1. Disable the AirPlay Receiver service. To do this, open the System
Preferences, go to "Sharing" and uncheck "AirPlay Receiver".


# Frontend React
Start React locally:
```bash
npm run start
```
or 
```bash
yarn start
```

Create build:
```bash
npm run build
```

# Deployment
Use Docker for deployment:

## Quickly test production build
```bash
npm run build
npx serve -s build
```

## Dockerize application
```bash
npm run deploy
```



## Troubleshooting
If you want to get into the Docker container's shell:

Get the Docker ID:

```bash
docker exec -ti DOCKER_NAME sh
```

## Database Migration

```bash
flask db migrate
flask db upgrade
```

Typical error codes:
```bash
ERROR [flask_migrate] Error: Target database is not up to date.
```

Fix that by:

```bash
flask db stamp head
```

From the result use the id:

```bash
INFO  [alembic.runtime.migration] Running stamp_revision  -> c35019e04da2
```

And write this command:

```bash
flask db revision --rev-id c35019e04da2
```

Then run:
```bash
flask db migrate
flask db upgrade
```

Another typical error:

```bash
ERROR [flask_migrate] Error: Can't locate revision identified by 'a7a398b4ecdb'
```

Do the same above, but we already have the revision ID.