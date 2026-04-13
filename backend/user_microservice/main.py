from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db.engine import create_tables
from routers.patients_router import router as patients_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_tables()
    yield


app = FastAPI(title="User Microservice", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients_router)


def run() -> None:
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    run()
