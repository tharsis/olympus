import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.constants import ENV
from src.endpoints import add_routes

app = FastAPI()
# Config
ALLOWED_HOSTS = ['*']


# debug code only
def register_exception(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        print(request)
        print(exc_str)
        content = {'status_code': 10422, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if ENV != 'PROD':
    register_exception(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_routes(app)

if __name__ == '__main__':
    if ENV == 'DEV':
        uvicorn.run(app, port=7000)
    else:
        uvicorn.run(app, root_path='/api', uds='/tmp/socket.sock')
