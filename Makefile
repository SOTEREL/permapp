dev: back_dev front_dev

config:
	cp -n .env.template design_perma/.env

back_dev: config
	python manage.py runserver

front_dev:
	npm run serve

install: config
	mkdir -p spa/static/spa/build
	mkdir -p spa/templates/spa
	npm install
	python setup.py develop && pip install -r requirements-dev.txt
	pre-commit install
