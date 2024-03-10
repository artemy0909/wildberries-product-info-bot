import asyncio
import logging
import sys


async def main() -> None:
    from loader import dp, bot, scheduler
    from handlers import ROUTERS
    from utils.database import get_all_subscriptions

    for subscription in get_all_subscriptions():
        scheduler.add_subscribe_alert(subscription.telegram_id, subscription.article)
    asyncio.get_event_loop().create_task(scheduler.start())

    dp.include_routers(*ROUTERS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
