Определить папку миграций - alembic init app/migrations
Сгенерировать миграцию - alembic revision --autogenerate
Применить миграцию - alembic upgrade head

Расширить файл requirements.txt новой зависимостью - pip freeze > requirements.txt

Запуск проекта из папки app - uvicorn app.main:app --reload


docker network create tg

docker run --name tg -p 5435:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=tg --network=tg -d postgres:16

docker run --name redis_tg -p 6379:6379 --network=tg -d redis:7.4

docker run --name booking_back -p 7777:8000  --network=test booking_image
