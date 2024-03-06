SHELL := /bin/sh
DIR := ${CURDIR}

lint :
	ruff mygreatproject/ tests/

test :
	pytest tests/

update_requirements :
	pip freeze > requirements.txt

make_migrations :
	python manage.py makemigrations mygreatproject

migrate : make_migrations
	python manage.py migrate

run_server :
	python manage.py runserver 127.0.0.1:8080

generate_swagger :
	python manage.py generate_swagger swagger.new.json
	mv -f swagger.new.json swagger.json
