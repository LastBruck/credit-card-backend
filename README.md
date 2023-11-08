# Бэкенд кредитной карты.

Данный сервис написан на языке **Python**.  
Использует framework **FastAPI**, СУБД **PostgreSQL** и несколько библиотек:

- **uvicorn** = "0.22.0"
- **fastapi** = "0.81"
- **envparse** = "0.2.0"
- **starlette** = "0.19.1"
- **pydantic** = "1.10.6"
- **anyio** = "3.7.0"
- **psycopg2-binary** = "2.9.9"
- **alembic** = "1.12.1"
- **asyncpg** = "0.28.0"
- **deepface**

## Запуск docker-compose:

```sh
docker compose up -d
```

Проверка создания топика:

```sh
docker exec -it kafka_container kafka-topics.sh --list --bootstrap-server kafka:24328
```

## Запуск на локальной машине:

Создание сертификата:

```sh
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```

Запуск Kafka:

```sh
kafka/bin/zookeeper-server-start.sh kafka/config/zookeeper.properties
kafka/bin/kafka-server-start.sh kafka/config/server.properties
```

Запуск сервисов:

```sh
python -m auth_service.src.main
python -m base_service.src.main
python -m verify_service.src.main
```

Создание топика:

```sh
kafka/bin/kafka-topics.sh --create --topic verify --bootstrap-server localhost:24328
```

Проверка топика:

```sh
kafka/bin/kafka-topics.sh --describe --topic verify --bootstrap-server localhost:24328
```

Чтение топика:

```sh
kafka/bin/kafka-console-consumer.sh --topic verify --from-beginning --bootstrap-server localhost:24328
```
