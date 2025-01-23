import json
import requests
from dataclasses import dataclass, field
from datetime import datetime, timezone

from utils.database import add_product_data


@dataclass
class ProductInfo:
    article: str
    title: str
    rating: float
    price: int
    quantity: int
    fetched_at: datetime = field(default_factory=datetime.utcnow)


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


async def fetch_schedule(article: str, interval_minutes: int) -> bool:
    from loader import scheduler
    job_id = f"api:{article}"
    if scheduler.get_job(job_id):
        return True

    product_data = await fetch_product_info(article)
    if product_data:
        await add_product_data(product_data)
    else:
        return False

    scheduler.add_api_subscribe_alert(article, interval_minutes)
    return True
