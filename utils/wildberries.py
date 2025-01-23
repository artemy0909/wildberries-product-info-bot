import json

import requests

from utils import database
from utils.entites import ProductInfo


def __get_product_info(article: str) -> ProductInfo | None:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    response = requests.get(url)
    if response.ok:
        try:
            data = json.loads(response.content)["data"]["products"][0]
            total_quantity = 0
            for sizes in data.get("sizes", []):
                for stocks in sizes.get("stocks", []):
                    total_quantity += stocks["qty"]

            return ProductInfo(
                article=article,
                title=data["name"],
                rating=data["reviewRating"],
                price=data["salePriceU"],
                quantity=total_quantity,
            )
        except (IndexError, KeyError):
            return None
    return None


async def fetch_product_info(article: str) -> ProductInfo | None:
    return __get_product_info(article)


async def fetch_schedule(article: str, interval_minutes: int) -> ProductInfo | None:
    from loader import scheduler
    job_id = f"api:{article}"
    if scheduler.get_job(job_id):
        product_data_db = await database.get_product_fresh_record(article)
        return ProductInfo(**product_data_db.__dict__)

    product_data = await fetch_product_info(article)
    if product_data:
        scheduler.add_api_subscribe_alert(article, interval_minutes)
        await database.schedule_update(article)
        await database.add_product_data(product_data)
        return product_data
    else:
        return None
