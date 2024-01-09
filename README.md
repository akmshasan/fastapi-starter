# FastAPI Starter

```markdown
This is a simple API demonstrating CRUD operations using FastAPI 
framework. It uses SQLite3 as in-memory  database for preserving 
the contents. 
It has custom logging  middleware and utilizes prometheus 
instrumentor to expose the metrics.

In general, the API does the following operations:

C (Create) -> Adds a fruit in the basket
R (Read) -> Returns a specific fruit or all fruits
U (Update) -> Updates a specific fruit in the basket
D (Delete) -> Deletes a specific fruit from the basket 
```

## This API has the following endpoints:
```markdown
Tags = ["Fruits"]
1. POST Operation - /api/v1/fruits -> Adds a fruit
2. GET Operation - /api/v1/fruits -> Returns all fruits
3. GET Operation - /api/v1/fruits/{fruit_id} -> Returns a specific fruit
4. PUT Operation - /api/v1/fruits/{fruit_id} -> Updates a specific fruit
5. DELETE Operation - /api/v1/fruits/{fruit_id} -> Deletes a specific fruit

Tags = ["Default"]
1. Index/Root endpoint - "/"
2. Health check endpoint - "/health"
3. Metrics enabled on endpoint - "/metrics"
```

## How to run locally
```markdown
Make sure docker is running. docker-compose is also installed.
This repository contains a Makefile which will bring up all the
required components. Make sure GNU make is installed.
```
Clone the repository:
```bash
git clone https://github.com/akmshasan/fastapi-starter.git
```
Change directory to the cloned directory:
```bash
cd fastapi-starter
```
Star the application:
```bash
make up
```
Stop the application:
```bash
make down
```

## How to test locally
### =================================
```markdown
Three docker containers will be run upon starting:
1. app -> http://localhost:8000
2. Prometheus -> http://localhost:9090
3. Grafana -> http://localhost:3000

To log on to the Grafana dashboard:
-----------------------------------
Username: admin
Password: admin

Swagger docs -> http://localhost:8000/docs
Metrics -> http://localhost:8000/metrics
Healthcheck -> http://localhost:8000/health
```
### Adds a fruit in the basket
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/fruits/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fruit": "Grape",
  "color": "Purple"
}'
```
Expected output:
```json
{
  "message": "New fruit has been added in the basket"
}
```
### Get all fruits from the basket
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/fruits/?limit=10&page=1' \
  -H 'accept: application/json'
```
Expected output:
```json
[
  {
    "id": 1,
    "fruit": "Apple",
    "color": "Red"
  },
  {
    "id": 2,
    "fruit": "Banana",
    "color": "Yellow"
  },
  {
    "id": 4,
    "fruit": "Dragonfruit",
    "color": "Red"
  },
  {
    "id": 5,
    "fruit": "Cherry",
    "color": "Red"
  },
  {
    "id": 6,
    "fruit": "Grape",
    "color": "Purple"
  }
]
```
### Get a specific fruit (e.g. fruit id: 1) from the basket
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/fruits/1' \
  -H 'accept: application/json'
```
Expected output:
```json
{
  "id": 1,
  "fruit": "Apple",
  "color": "Red"
}
```
### Update a specific fruit (e.g. fruit id: 6)
```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/fruits/6' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fruit": "Grape",
  "color": "Green"
}'
```
Expected output:
```json
{
  "message": "Fruit having fruit id: 6 has been updated"
}
```
### Delete a specific fruit (e.g. fruit id: 6) from the basket
```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/v1/fruits/6' \
  -H 'accept: application/json'
```
Expected output:
```json
{
  "message": "Fruit having fruit id: 6 has been deleted"
}
```




