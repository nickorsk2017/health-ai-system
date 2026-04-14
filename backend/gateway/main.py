import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers.analyses_router import router as analyses_router
from routers.consilium_router import router as consilium_router
from routers.devices_router import router as devices_router
from routers.diagnosis_router import router as diagnosis_router
from routers.history_router import router as history_router
from routers.patients_router import router as patients_router
from routers.visits_router import router as visits_router

app = FastAPI(title="Personal Health OS Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients_router)
app.include_router(visits_router)
app.include_router(history_router)
app.include_router(consilium_router)
app.include_router(diagnosis_router)
app.include_router(analyses_router)
app.include_router(devices_router)


def run() -> None:
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    run()
