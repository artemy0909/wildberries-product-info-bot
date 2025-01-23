from utils.config import Config
from utils.database import get_all_subscriptions, get_all_update_schedules


async def init_schedulers_from_db(scheduler):
    for sub in await get_all_subscriptions():
        scheduler.add_subscribe_alert(sub.telegram_id, sub.article, Config.SUBSCRIBE_PUSH_INTERVAL)

    for sch in await get_all_update_schedules():
        scheduler.add_api_subscribe_alert(sch.article, Config.ARTICLE_UPDATE_INTERVAL)
