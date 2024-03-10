from aiogram.utils.markdown import hbold, hitalic, hcode

from utils.database import UserQuery
from utils.misc import ProductInfo

SEND_ARTICLE = "🔢 Для продолжение введи артикул товара"
ALL_NOTIFICATIONS_IS_STOPPED = "🔕 Все уведомления отключены"
USE_BUTTONS = "👇 Используйте кнопки для продолжения"
ARTICLE_NOT_FOUND = "🫤 Не удалось получить данные артикула"
WRONG_INPUT = "❌ Неверный ввод, используйте только цифры"


def product_info_to_description(product_info: ProductInfo) -> str:
    return (f"{hitalic('Aрт. ')}{hcode(product_info.article)}\n{hbold(product_info.title)}\n--------------------\n"
            f"  💵 Цена: {product_info.price}\n  ⭐️ Рейтинг: {product_info.rating}\n"
            f"  📦 Наличие: {product_info.quantity} шт.")


def summary_of_queries(queries: list[UserQuery]) -> str:
    return f"Последние записи из БД:\n\n" + "\n\n".join([str(query) for query in queries])
