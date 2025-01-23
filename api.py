from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from utils.auth import get_current_user
from utils.config import Config
from utils.wildberries import fetch_product_info, fetch_schedule
from utils.database import add_product_data, schedule_update

router = APIRouter(prefix="/api/v1", tags=["APIv1"])


class ProductBody(BaseModel):
    article: str


@router.post("/products", status_code=201)
async def create_product(
        body: ProductBody,
        token: str = Depends(get_current_user)
):
    article = body.article.strip()
    product_data = await fetch_product_info(article)
    if not product_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Не удалось найти данные по артикулу {article}"
        )
    await add_product_data(product_data)
    return {"status": "created", "article": article}


@router.get("/subscribe/{article}")
async def subscribe_article(
        article: str,
        token: str = Depends(get_current_user)
):
    article = article.strip()
    scheduled = await fetch_schedule(article, Config.ARTICLE_UPDATE_INTERVAL)
    if not scheduled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать периодическую задачу"
        )
    else:
        await schedule_update(article)
    return {"status": "subscribed", "article": article, "interval_minutes": Config.ARTICLE_UPDATE_INTERVAL}
