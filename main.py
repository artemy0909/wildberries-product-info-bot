import asyncio
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api import router as api_router
from handlers import ROUTERS
from loader import dp, bot, scheduler
from utils.database.db import init_db
from utils.scheduler import init_schedulers_from_db


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
    uvicorn.run("main:main_app", host="0.0.0.0", port=80, reload=False)
