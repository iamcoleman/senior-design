# Sentiment Analysis Flask API

### NOTE

A lot of this code was taken from a Flask boilerplate. There's random pieces of code left over from the boilerplate that Coleman is still working on removing - things like the Node server, the HTML and CSS, the assets, etc. Ignore for now while I continue to clear it out.

---

## Setup for local development

#### Requirements

- Python
- PostgreSQL installed locally
    - I (Coleman) am using **pgAdmin** to access my Postgres instance easily
- A Celery Worker and Redis running locally
- The Python virtual environment described in `senior-design/code/README.md`


#### Environment Variables

Using a `.env` file to get variables to the Flask application. 

1. Copy the contents of the `.env.example` file to a new `.env` file
1. The only value that needs to be changed (for now) is the `DATABASE_URL`
    1. Create a database on your Postgres instance - I named mine `engine_dev`
    1. Get the connection URL for the database. Should look something like `postgresql://<username>:<password>@localhost:5432/engine_dev`
    1. Put this connection URL in the `DATABASE_URL` variable in the `.env` file
    
#### Initializing the Postgres database locally

This must be done after a local Postgres database has already been created and your connection URL has been put in the `.env` file.

1. Make sure you have the Python virtual environment activated
1. Navigate to `senior-design/code/engine_api` in CMD/Terminal
1. Run the following three commands in order
```bash
flask db init
flask db migrate
flask db upgrade
```

If you have made changes to the database schema or models and need to update the database, then you only have to run `flask db migrate` and `flask db upgrade` in order.

_Note: I have had problems with Flask not recognizing a change to the schema/models, which means the database never actually gets updated. To fix this, I have been deleting the Postgres database entirely and making a new one with the same name. Then I'll run the three commands above over again._

#### Starting a local Redis server for Celery

Redis is used with the task scheduler Celery. The following command will start a basic Redis server using Docker. This will create a Redis URI of `redis://localhost:6379`. 

1. `docker run --name some-redis -p 6379:6379 -d redis`

#### Starting a Celery worker

Celery workers are required to actually run the Celery tasks, or else the tasks will be handled by the request handler instead.

1. Activate the virtual environment
1. Navigate to `/code/engine_api` in CMD/Terminal
1. `celery -A celery_worker.celery worker --loglevel=INFO --pool=solo`


---

## Running locally

1. Make sure you have...
   - the Python virtual environment activated 
   - have set up and initialized the Postgres database 
   - have the Redis docker running
1. Navigate to `senior-design/code/engine_api` in CMD/Terminal
1. Run the command: `flask run`
1. Activate the Celery worker using the instructions above
   - _Note: Sometimes I got errors starting the Celery worker before the Flask server and sometimes I didn't, so I recommend just starting the worker after the Flask server is already running_
1. This should launch a development Flask server at `127.0.0.1:5000` with automatic refresh when the Flask files are changed and saved

#### Swagger API Documentation

Swagger API documentation will be available at `127.0.0.1:5000/apidocs` 
