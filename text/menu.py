from utils.database import UserQuery

SEND_ARTICLE = "🔢 Для продолжения введите артикул товара"
ALL_NOTIFICATIONS_IS_STOPPED = "🔕 Все уведомления отключены"
USE_BUTTONS = "👇 Используйте кнопки для продолжения"
ARTICLE_NOT_FOUND = "🫤 Нет актуальных данных по данному артикулу в БД"
WRONG_INPUT = "❌ Неверный ввод, используйте только цифры"


def product_info_to_description(article: str, title: str, price_in_coins: int, rating: float, quantity: int) -> str:
    rub = price_in_coins // 100
    kop = price_in_coins % 100
    return (
        f"Aрт. <code>{article}</code>\n"
        f"<b>{title}</b>\n"
        "--------------------\n"
        f" 💵 Цена: <i>{rub}.{kop:02d} &#8381;</i>\n"
        f" ⭐️ Рейтинг: <i>{rating}</i>\n"
        f" 📦 Наличие: <i>{quantity} шт.</i>"
    )


def summary_of_queries(queries: list[UserQuery]):
    text_result = "Последние записи из БД:\n\n"
    for q in queries:
        text_result += str(q) + "\n\n"
    return text_result.strip()
