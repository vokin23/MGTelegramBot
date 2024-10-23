import asyncio
from datetime import datetime
from aiogram import Bot
from sqlalchemy import select
from app.config import settings
from app.datebase import async_session_maker_null_pool
from app.main import bot
from app.models import Post
from aiogram.exceptions import AiogramError

async def publish_post(bot: Bot):
    try:
        async with async_session_maker_null_pool() as session:
            no_published_posts = await session.execute(select(Post).where(Post.posted == False))
            no_published_posts = no_published_posts.scalars().all()
            for post in no_published_posts:
                if post.time_posted <= datetime.now().strftime("%Y-%m-%d %H:%M"):
                    await bot.send_message(chat_id=settings.MAIN_CHANNEL, text=post.content)
                    post.posted = True
                    await session.commit()
    except AiogramError as e:
        print(f"An error occurred: {e}")
    finally:
        await asyncio.sleep(10)


async def publish():
    while True:
        print("Start publish")
        await publish_post(bot)


if __name__ == "__main__":
    asyncio.run(publish())