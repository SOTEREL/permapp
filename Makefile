dev: back_dev front_dev

back_dev:
	python manage.py runserver

front_dev:
	npm run serve

install:
	mkdir -p spa/static/spa/build
	mkdir -p spa/templates/spa
	npm install
	python setup.py develop && pip install -r requirements-dev.txt
	pre-commit install
