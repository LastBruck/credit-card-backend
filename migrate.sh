#!/bin/bash

alembic revision --autogenerate -m "comment"
sleep 10
alembic upgrade heads
