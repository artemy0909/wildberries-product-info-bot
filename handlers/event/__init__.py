import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .subscription_alert import article_alert
from utils.wildberries import fetch_product_info
from utils.database import add_product_data


class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="UTC")

    def start(self):
        self.scheduler.start()
        logging.info("APScheduler started.")

    def shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)
        logging.info("APScheduler shutdown.")

    def add_subscribe_alert(self, user_id, article, interval_minutes: int):
        job_id = f"{user_id}:{article}"
        if self.scheduler.get_job(job_id):
            return
        self.scheduler.add_job(
            article_alert,
            trigger=IntervalTrigger(minutes=interval_minutes),
            args=[self.bot, user_id, article],
            id=job_id,
            replace_existing=True
        )

    def remove_subscribe_alert(self, user_id, article):
        job_id = f"{user_id}:{article}"
        job = self.scheduler.get_job(job_id)
        if job:
            job.remove()

    def remove_all_user_alerts(self, user_id):
        for job in self.scheduler.get_jobs():
            if job.id.startswith(f"{user_id}:"):
                job.remove()

    def add_api_subscribe_alert(self, article: str, interval_minutes: int):
        async def api_job():
            product_info = await fetch_product_info(article)
            if product_info:
                await add_product_data(product_info)

        job_id = f"api:{article}"
        if self.scheduler.get_job(job_id):
            return
        self.scheduler.add_job(
            api_job,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id=job_id,
            replace_existing=True
        )

    def get_job(self, job_id: str):
        return self.scheduler.get_job(job_id)
