# django-app-template

Basic template for Django apps.

To make it your own:

0. using a recent version of python3, create virtualenv, and pip install -r requirements.txt
1. find and replace (case-sensitive) "MyGreatProject" with "YourNewProjectName"
2. find and replace (case-sensitive) "mygreatproject" with "yournewprojectname"
3. to use postgres locally, `psql -h localhost` and run `CREATE DATABASE yournewprojectname;`
4. run `make migrate` to apply migrations
5. run `make generate_swagger` to update swagger.json
6. run `make run_server` to develop locally
7. visit `http://localhost:8000/swagger/` to see the current schema
8. add new api endpoints to `api/views.py`
9. profit
