from fastapi import APIRouter, Depends, HTTPException, status

from utils import database
from utils.auth import get_current_user
from utils.config import Config
from utils.entites import ProductBody, ResponseSchema
from utils.wildberries import fetch_product_info, fetch_schedule

router = APIRouter(prefix="/api/v1", tags=["APIv1"])


@router.post("/products", status_code=201)
async def create_product(
        body: ProductBody,
        token: str = Depends(get_current_user)
):
    article = body.article.strip()
    product_data = await fetch_product_info(article)
    if product_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Не удалось найти данные по артикулу {article}"
        )
    await database.add_product_data(product_data)
    return ResponseSchema(data=product_data).model_dump(exclude_none=True)


@router.get("/subscribe/{article}")
async def subscribe_article(
        article: str,
        token: str = Depends(get_current_user)
):
    article = article.strip()
    product_data = await fetch_schedule(article, Config.ARTICLE_UPDATE_INTERVAL)
    if product_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать периодическую задачу"
        )
    return ResponseSchema(
        data=product_data, update_interval_minutes=Config.ARTICLE_UPDATE_INTERVAL
    ).model_dump()
