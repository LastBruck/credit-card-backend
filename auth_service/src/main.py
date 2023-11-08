"""Main auth service."""
from contextlib import asynccontextmanager

import uvicorn
from aiohttp import ClientSession
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter, FastAPI

import settings
from auth_service.src.api.auth import auth
from auth_service.src.api.requests import request_balance, request_deposit, request_history, request_verify, request_withdrawal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan.

    Args:
        app (FastAPI): _description_

    Yields:
        _type_: _description_
    """
    session = ClientSession()
    kafka_producer = AIOKafkaProducer(bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}')
    await kafka_producer.start()
    kafka_consumer_result = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_RESULT,
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
    )
    await kafka_consumer_result.start()
    yield {'client_session': session, 'kafka_producer': kafka_producer, 'kafka_consumer_result': kafka_consumer_result}
    await session.close()
    await kafka_producer.stop()
    await kafka_consumer_result.stop()

app = FastAPI(title='auth-service', lifespan=lifespan)

main_api_router = APIRouter()

main_api_router.include_router(auth, prefix='/api/auth', tags=['auth'])
main_api_router.include_router(request_balance, prefix='/api/balance', tags=['request-balance'])
main_api_router.include_router(request_history, prefix='/api/balance/history', tags=['request-history'])
main_api_router.include_router(request_deposit, prefix='/api/deposit', tags=['request-deposit'])
main_api_router.include_router(request_withdrawal, prefix='/api/withdrawal', tags=['request-withdrawal'])
main_api_router.include_router(request_verify, prefix='/api/verify', tags=['request-verify'])
app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_AUTH_PORT,
    )
