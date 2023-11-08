"""Main feryfi service."""
import asyncio
import json
from contextlib import asynccontextmanager

import aiojobs
import uvicorn
from aiohttp import ClientSession
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI

import settings
from verify_service.src.api.verify import verify_rout

resources = {}


async def verify_user():
    """Функция консюмера кафки."""
    consumer: AIOKafkaConsumer = resources.get('kafka_consumer_request')
    producer: AIOKafkaProducer = resources.get('kafka_producer_result')
    while True:
        await asyncio.sleep(1)
        new_req = await consumer.getone()
        new_req = json.loads(new_req.value.decode('utf-8').replace("'", '"'))
        card_number = new_req.get('card_number')
        selfie_name = new_req.get('selfie_name')
        document_name = new_req.get('document_name')
        input_data = {'card_number': card_number, 'selfie_name': selfie_name, 'document_name': document_name}
        url = 'http://{host}:{port}/api/verify/'.format(host=settings.APP_HOST, port=settings.APP_VERIFY_PORT)
        async with ClientSession() as session:
            resp = await session.post(url, params=input_data)
            data = await resp.json()
            status = resp.status
        event = json.dumps({'status': status, 'resoult': data})
        await producer.send_and_wait(topic=settings.KAFKA_TOPIC_RESULT, value=bytes(str(event), encoding='utf-8'))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan.

    Args:
        app (FastAPI): _description_

    Yields:
        _type_: _description_
    """
    scheduler = aiojobs.Scheduler()
    kafka_producer = AIOKafkaProducer(bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}')
    await kafka_producer.start()
    resources['kafka_producer_result'] = kafka_producer
    kafka_consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_REQUEST,
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
    )
    await kafka_consumer.start()
    resources['kafka_consumer_request'] = kafka_consumer
    await scheduler.spawn(verify_user())
    yield
    await kafka_producer.stop()
    await kafka_consumer.stop()
    await scheduler.close()
    resources.clear()


app = FastAPI(title='verify-service', lifespan=lifespan)

app.include_router(verify_rout, prefix='/api/verify', tags=['verify'])


if __name__ == '__main__':
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_VERIFY_PORT)
