import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.init import redis_manager
from datetime import datetime
from aiogram.enums import ParseMode
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import insert, select
from app.config import settings
from app.datebase import async_session_maker
from app.keyboards.admin import admin_start, publish_post_kb
from app.keyboards.start import keyboard_start
from app.models.posts import Post
from aiogram.fsm.state import State, StatesGroup
from app.models import UserTelegram
from aiogram.fsm.context import FSMContext

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


class OnlinePost(StatesGroup):
    text = State()


class PublishOldPost(StatesGroup):
    cheek = State()
    id = State()


class CreatePost(StatesGroup):
    text = State()
    time_posted_post = State()


class CreateEvent(StatesGroup):
    text = State()
    promo = State()


async def cheek_or_create_user(message: types.Message):
    async with async_session_maker() as session:
        user_stmt = select(UserTelegram).where(UserTelegram.username == message.from_user.username)
        user = await session.execute(user_stmt)
        user = user.scalars().first()
        if user is None:
            user = insert(UserTelegram).values(username=message.from_user.username,
                                               first_name=message.from_user.first_name,
                                               last_name=message.from_user.last_name,
                                               user_id=message.from_user.id).returning(UserTelegram)
            user = await session.execute(user)
            await session.commit()
            user = user.scalar()
        return user


@dp.message(Command(commands=['start']))
async def start(message: types.Message):
    if (await cheek_or_create_user(message)).admin:
        await message.answer(f"Привет, {message.from_user.username}.\n"
                             "Сейчас я покажу тебе экранную клавиатуру, "
                             "на ней ты сможешь выбрать направление диалога!", reply_markup=admin_start)

    if not (await cheek_or_create_user(message)).admin:
        await message.answer("Привет, Я бот Mind Games.\n"
                             "Сейчас я покажу тебе экранную клавиатуру, "
                             "на ней ты сможешь выбрать направление диалога!", reply_markup=keyboard_start)


@dp.callback_query(lambda c: c.data == 'start_game')
async def start_game_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🚀 *Добро пожаловать в мир DayZ\\!*\n\n"
        "Если у вас еще нет игры, вы можете приобрести и скачать её по следующей ссылке:\n"
        "[Скачать DayZ](https://store.steampowered.com/app/221100/DayZ/)\n\n"
        "❌ *Обратите внимание: пиратские версии игры не подходят для игры на данном проекте\\.*\n\n"
        "📋 *Прежде чем начать, выполните следующие шаги:*\n"
        "1\\. Ознакомьтесь с правилами проекта и его ЛОР\\.\n"
        "2\\. В лаунчере на вкладке *ПАРАМЕТРЫ* 'ВСЕ ПАРАМЕТРЫ' установите галочку в поле «Имя профиля»\\. Напишите свой игровой позывной так же, как в Discord\\. "
        "Используйте ТОЛЬКО латинские буквы\\.\n"
        "   ⚠ Игроки с никнеймами «SURVIVOR» не допускаются к игре на сервере\\.\n"
        "3\\. После того как вы установите позывной, перейдите на вкладку *«СЕРВЕРЫ»* \\-\\> *«СООБЩЕСТВО»* и найдите сервер *Mind Games DayZ STALKER* \\(или по IP \\- 185\\.207\\.214\\.145:2302\\)\\. "
        "Нажмите на красную кнопку *«ВСТУПИТЬ»* \\-\\> *«УСТАНОВИТЬ МОДЫ И ДОПОЛНЕНИЯ»*, чтобы подключиться к серверу\\. Дальше моды загрузятся автоматически\\.\n\n"
        "🔗 [Ссылка на нашу коллекцию модов](https://steamcommunity.com/sharedfiles/filedetails/?id=2879158215)",
        parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.callback_query(lambda c: c.data == 'donat')
async def donat_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🤲 *Пожертвования* \\- это личное желание каждого помочь проекту развиваться\\.\n"
        "💡 *Никто не заставляет вас делать это\\. Пожалуйста, имейте в виду, что пожертвования не подлежат возврату\\.*\n\n"
        "🌟 *Если вы хотите поддержать проект, вы можете сделать это следующими способами:*\n"
        "1\\. Отправьте пожертвование на карту: *2202 2061 9960 2256*\\.\n"
        "2\\. Также вы можете воспользоваться нашим сайтом: [Mind Games Project](https://mindgamesproject.ru/)\n\n"
        "🙏 *Спасибо вам за поддержку\\!* Мы стремимся создать качественный проект, и для этого требуется много времени, сил и средств\\.\n"
        "📩 *По всем вопросам о пожертвованиях обращайтесь напрямую к создателям проекта\\.*",
        parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.callback_query(lambda c: c.data == 'game_servers')
async def game_servers_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🤲 *Список наших серверов:*\n"
        "1\\. *Mind Games S\\.T\\.A\\.L\\.K\\.E\\.R\\. RP*\\.\n"
        "*Адрес* \\- 195\\.18\\.27\\.49\n"
        "*Порт* \\- 2302\n"
        "*Discord сервер* \\- [Mind Games Project STALKER](https://discord.gg/mgstalkerrp)\n\n"
        "2\\. *Mind Games life RP*\n"
        "*Адрес* \\- 185\\.207\\.214\\.145\n"
        "*Порт* \\- 2302\n"
        "*Discord сервер* \\- [Mind Games Project Life](https://discord.gg/SWzXJJmu7n)\n\n",
        parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.callback_query(lambda c: c.data == 'create_event')
async def create_event_callback(callback_query: types.CallbackQuery, state: FSMContext):
    pass


@dp.callback_query(lambda c: c.data == 'create_post')
async def create_post_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите текст поста")
    await state.set_state(CreatePost.text)


@dp.message(StateFilter(CreatePost.text))
async def time_posted_post(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Введите дату и время буликации поста. Пример: 2021-09-01 12:00")
    await state.set_state(CreatePost.time_posted_post)


@dp.message(StateFilter(CreatePost.time_posted_post))
async def create_post(message: types.Message, state: FSMContext):
    await state.update_data(time_posted_post=message.text)
    data = await state.get_data()
    await message.answer(f"Текст поста: {data['text']}\n"
                         f"Дата и время публикации: {data['time_posted_post']}")
    async with async_session_maker() as session:
        new_post = insert(Post).values(content=data['text'],
                                       time_created=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       time_posted=data['time_posted_post'],
                                       user_id=message.from_user.id).returning(Post).returning(Post)
        new_post = await session.execute(new_post)
        await session.commit()
        new_post = new_post.scalar()
    await message.answer(f"Пост успешно создан! ID поста: {new_post.id}")
    await state.clear()


@dp.callback_query(lambda c: c.data == 'publish_post')
async def publish_post_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Выбурите пункт:", reply_markup=publish_post_kb)
    await state.set_state(CreatePost.text)


@dp.callback_query(lambda c: c.data == 'publish_new_post')
async def publish_new_post_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите текст поста")
    await state.set_state(OnlinePost.text)


@dp.message(StateFilter(OnlinePost.text))
async def create_post(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f"Текст поста: {data['text']}\n"
                         f"Дата и время публикации: {datetime.now().strftime("%Y-%m-%d %H:%M")}")
    async with async_session_maker() as session:
        new_post = insert(Post).values(content=data['text'],
                                       time_created=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       time_posted=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       user_id=message.from_user.id,
                                       posted=True).returning(Post).returning(Post)
        new_post = await session.execute(new_post)
        await session.commit()
        new_post = new_post.scalar()
        await bot.send_message(chat_id=settings.MAIN_CHANNEL, text=new_post.content)
    await message.answer(f"Пост успешно создан и опубликован! ID поста: {new_post.id}")
    await state.clear()


@dp.callback_query(lambda c: c.data == 'set_publish_old_post')
async def select_post_callback(callback_query: types.CallbackQuery):
    async with async_session_maker() as session:
        posts = await session.execute(select(Post).where(Post.posted == False))
        posts = posts.scalars().all()
        if not posts:
            await callback_query.message.answer("Нет неопубликованных постов")
            return
        buttons = [InlineKeyboardButton(text=str(post.id), callback_data=f"post_{post.id}") for post in posts]
        kb = InlineKeyboardMarkup(inline_keyboard=[buttons], row_width=5 if len(buttons) > 5 else len(buttons))

    await callback_query.message.answer("Выберите пост чтобы подробно его просмотреть:", reply_markup=kb)


@dp.callback_query(lambda c: c.data.startswith('post_'))
async def view_post_callback(callback_query: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Опубликовать', callback_data='publish')],
        [InlineKeyboardButton(text='Назад', callback_data='set_publish_old_post')]
    ])
    async with async_session_maker() as session:
        post_stmt = select(Post).where(Post.id == int(callback_query.data.split('_')[1]))
        post_obj = await session.execute(post_stmt)
        post = post_obj.scalar()  # Corrected method call
        await state.set_state(PublishOldPost.id)
        await state.update_data(post_id=post.id)
    await callback_query.message.answer(f"ID поста: {post.id}\n"
                                        f"Текст: {post.content}\n", reply_markup=kb)


@dp.callback_query(lambda c: c.data == 'publish')
async def publish_new_post(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    async with async_session_maker() as session:
        post_stmt = select(Post).where(Post.id == data['post_id'])
        post_obj = await session.execute(post_stmt)
        post = post_obj.scalar()
        post.posted = True
        await session.commit()
    await bot.send_message(chat_id=settings.MAIN_CHANNEL, text=post.content)
    await callback_query.message.answer("Пост успешно опубликован!")
    await state.clear()


async def on_startup():
    print("Start")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(redis_manager.connect())
    asyncio.run(on_startup())
