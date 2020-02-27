serve: serve_back serve_front

serve_back:
	cd backend; python manage.py runserver

serve_front:
	cd frontend; npm run serve

install:
	cd frontend; npm install
	cd backend; python setup.py develop && pip install -r requirements-dev.txt
