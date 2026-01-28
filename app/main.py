import uvicorn
from fastapi import FastAPI

from app.api import ticker_route


def create_app() -> FastAPI:
    app = FastAPI(title="Currency", version="0.1.0")
    app.include_router(currencies_route.router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":

    uvicorn.run("app.main:app", host="0.0.0.0", port=5050, reload=True)