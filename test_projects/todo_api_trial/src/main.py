from fastapi import FastAPI

from src.api.routes.todos import router as todos_router
from src.infrastructure.database import Base, engine

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    application = FastAPI(title="Todo API", version="1.0.0")
    application.include_router(todos_router)
    return application


app = create_app()
