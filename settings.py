"""Настройки и переменные окружения."""
from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@postgres:5432/postgres'
)

APP_HOST = env.str('APP_HOST', default='localhost')
KAFKA_HOST = env.str('KAFKA_HOST', default='localhost')
APP_AUTH_PORT = env.int('APP_AUTH_PORT', default=24028)
APP_BASE_PORT = env.int('APP_BASE_PORT', default=24128)
APP_VERIFY_PORT = env.int('APP_VERIFY_PORT', default=24228)
KAFKA_PORT = env.int('KAFKA_PORT', default=24328)
KAFKA_TOPIC_REQUEST = env.str('KAFKA_TOPIC_REQUEST', default='verify_req')
KAFKA_TOPIC_RESULT = env.str('KAFKA_TOPIC_RESULT', default='verify_res')

SSL_KEYFILE_PATH = env.str('SSL_KEYFILE_PATH', default='localhost.key')
SSL_CERTFILE_PATH = env.str('SSL_CERTFILE_PATH', default='localhost.crt')

SECRET_KEY: str = env.str('SECRET_KEY', default='salary')
ALGORITHM: str = env.str('ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
