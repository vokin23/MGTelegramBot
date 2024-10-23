import asyncio

from app.bot.publish import publish_post
from app.tasks.celery_app import celery_instance


@celery_instance.task(name="publish_post")
def cheek_vips_everyday():
    asyncio.run(publish_post())
    print("publish_post успешно завершена!")
