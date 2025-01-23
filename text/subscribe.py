SUBSCRIPTION_ALREADY_EXISTS = "❌ Вы уже подписаны на данный артикул"
UNSUBSCRIPTION_NOT_EXISTS = "❌ Вы не подписаны на данный артикул"
SUBSCRIPTION_TITLE = "🔔 Подписка на артикул\n\n"


def cannot_find_article(article: str):
    return f"❌ Не удалось получить информацию об артикуле <code>{article}</code>"
