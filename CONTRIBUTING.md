Для накатывания миграций, из папки alembic в каждом сервисе, нужно запустить в терминале команду:

```sh
alembic revision --autogenerate -m "comment"
```

Дальше вводим:

```sh
alembic upgrade heads
```
