from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

from app.keyboards.start import keyboard_start

# Инициализация бота и диспетчера
bot = Bot(token="7818325729:AAHcAt1mizfCW_XsCS42ArHSIYidi4gxjZo")
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start(message: types.Message):
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


async def on_startup():
    print("Bot started!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(on_startup())
