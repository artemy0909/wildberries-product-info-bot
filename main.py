import logging
import sys
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from loader import dp, bot, scheduler
from handlers import ROUTERS
from api import router as api_router
from utils.scheduler import init_schedulers_from_db
from utils.database.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("FastAPI: startup event")
    await init_db()
    await init_schedulers_from_db(scheduler)
    dp.include_routers(*ROUTERS)
    asyncio.create_task(dp.start_polling(bot))
    scheduler.start()

    yield

    logging.info("FastAPI: shutdown event")
    scheduler.shutdown(wait=False)
    await bot.session.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aiogram Bot & FastAPI Service",
        version="1.0.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


main_app = create_app()


@main_app.get("/", include_in_schema=False)
async def docs_redirect(request: Request):
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    uvicorn.run("main:main_app", host="127.0.0.1", port=8000, reload=False)
