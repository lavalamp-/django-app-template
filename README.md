# django-app-template

Basic template for Django apps.

To make it your own:

0. using a recent version of python3, create virtualenv, and pip install -r requirements.txt
1. find and replace (case-sensitive) "MyGreatProject" with "YourNewProjectName"
2. find and replace (case-sensitive) "mygreatproject" with "yournewprojectname"
3. rename `mygreatproject` and `tests/mygreatproject` folders to "yournewprojectname"
4. to use postgres locally, `psql -h localhost` and run `CREATE DATABASE yournewprojectname;`
5. run `make migrate` to apply migrations
6. run `make generate_swagger` to update swagger.json
7. run `make run_server` to develop locally
8. visit `http://localhost:8000/swagger/` to see the current schema
9. add new api endpoints to `api/views.py`, `urls.py`
10. profit
