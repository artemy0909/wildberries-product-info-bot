from utils.config import Config


class MenuButtons:
    get_product_info = "🔍 Получить информацию по товару"
    stop_notifications = "🔕 Остановить все уведомления"
    get_database_info = "🗂 Получить информацию из БД"
    back_to_menu = "↪️ Вернуться в меню"


class SubInlineButtons:
    subscribe = f"📝 Подписаться (раз в {Config.SUBSCRIBE_PUSH_INTERVAL} минут)"
    unsubscribe = "🔕 Отписаться"
