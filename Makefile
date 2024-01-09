fmt:
	black .
	isort ./api
	autoflake --in-place -r ./api

test:
	pytest tests/tests.py
	coverage run -m pytest tests/tests.py
	coverage report -m

up:
	docker-compose down -v
	docker-compose up

down:
	docker-compose down -v

run:
	uvicorn api.main:app --reload
	