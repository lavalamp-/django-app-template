# django-app-template

Basic template for Django apps.

## To make it your own:

1. find and replace (case-sensitive) "MyGreatProject" with "YourNewProjectName"
2. find and replace (case-sensitive) "mygreatproject" with "yournewprojectname"
3. rename `mygreatproject` and `tests/mygreatproject` folders to "yournewprojectname"

## To get it running:

1. using a recent version of python3, create virtualenv, and pip install -r requirements.txt
2. to use postgres locally, `psql -h localhost` and run `CREATE DATABASE yournewprojectname;`
3. run `make run_server` to develop locally
4. visit `http://localhost:8000/swagger/` to see the current schema
5. add new api endpoints to `api/views.py`, `urls.py`

## Other useful commands

1. run `make tests` to run tests, `make lint` to run lint
2. run `make make_migrations` to create migrations when you change models, `make migrate` to apply them
3. run `make generate_swagger` to update `swagger.json` to the latest schema

## To deploy to Heroku

1. Create a new Heroku project
2. Create a new Heroku postgres mini/free add-on
3. Update the herokuapp.com URL in settings.py to enable in production
4. Probably deploy, it should kinda just work!
