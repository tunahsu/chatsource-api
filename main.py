import os
import sys
import uvicorn

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings

# Get the absolute path of the current file and move up two directory levels to obtain the parent directory path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Append this path to Python's module search path
sys.path.append(path)

from db import Base, engine
from routers.auth import auth_router
from routers.users import user_router
from routers.chatbots import chatbot_router
from exception import NewHTTPException

Base.metadata.create_all(bind=engine)

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(chatbot_router)

app = FastAPI(openapi_url=settings.OPENAPI_URL)
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Unexpected error
@app.middleware('http')
async def get_request(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print('Error:', e)
        return JSONResponse(
            status_code=500,
            content={'detail': 'Internal Server Error'},
        )


# Expected error
@app.exception_handler(NewHTTPException)
async def exception_handler(request: Request, exc: NewHTTPException):
    print('Error:', exc.msg)
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
    )


if __name__ == '__main__':
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=settings.PORT,
                reload=settings.RELOAD)
