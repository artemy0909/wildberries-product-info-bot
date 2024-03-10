import asyncio

import aioschedule
from .subscription_alert import article_alert


class Scheduler:

    def __init__(self, bot):
        self.tasks = {}
        self.bot = bot

    def add_subscribe_alert(self, user_id, article):
        self.add_task(article_alert, minutes=1, id_=f"{user_id}:{article}", user_id=user_id, article=article)

    def remove_subscribe_alert(self, user_id, article):
        id_ = f"{user_id}:{article}"
        self.remove_task(id_)

    def remove_all_user_alerts(self, user_id):
        on_delete = []
        for task in self.tasks:
            if task.startswith(f"{user_id}"):
                on_delete.append(task)
        for task in on_delete:
            self.remove_task(task)

    def add_task(self, job, minutes, id_, **kwargs):
        schedule: aioschedule.Job = aioschedule.every(minutes).minutes.do(job, self.bot, **kwargs)
        self.tasks[id_] = schedule

    def remove_task(self, id_):
        if id_ in self.tasks:
            aioschedule.cancel_job(self.tasks[id_])
            del self.tasks[id_]

    @staticmethod
    async def start():
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
