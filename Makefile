fmt:
	black .

test:
	pytest tests/tests.py
	coverage run -m pytest tests/tests.py
	coverage report -m

# build:
# 	docker-compose --build

up:
	docker-compose down -v
	docker-compose up --build

down:
	docker-compose down -v

run:
	uvicorn api.main:app --reload
	