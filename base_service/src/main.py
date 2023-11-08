"""Main base service."""
import uvicorn
from fastapi import APIRouter, FastAPI

import settings
from base_service.src.api.balance import balance, create_user, get_history, get_user
from base_service.src.api.rout_transactions import change_limit, deposit, withdrawal

app = FastAPI(title='base-service')

main_api_router = APIRouter()

main_api_router.include_router(get_user, prefix='/api/get_user', tags=['get-user'])
main_api_router.include_router(create_user, prefix='/api/create_user', tags=['create-user'])
main_api_router.include_router(balance, prefix='/api/balance', tags=['balance'])
main_api_router.include_router(get_history, prefix='/api/balance/history', tags=['history'])
main_api_router.include_router(deposit, prefix='/api/deposit', tags=['deposit'])
main_api_router.include_router(withdrawal, prefix='/api/withdrawal', tags=['withdrawal'])
main_api_router.include_router(change_limit, prefix='/api/change_limit', tags=['change-limit'])
app.include_router(main_api_router)


if __name__ == '__main__':
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_BASE_PORT)
