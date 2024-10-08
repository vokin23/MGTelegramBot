from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Создание кнопок
vk = InlineKeyboardButton(text='Группа ВК', url='https://vk.com/mgpdayz')
discord = InlineKeyboardButton(text='Discord', url='https://discord.gg/mgstalkerrp')
start_game = InlineKeyboardButton(text='Как начать играть?', callback_data='start_game')
site = InlineKeyboardButton(text='Наш сайт', url='https://mindgamesproject.ru/')
rp_roles = InlineKeyboardButton(text='РП правила', url='https://docs.google.com/document/d/1QMIgG2OeUzLBrfB5wkx-UZpvJTYjuPjc1qP1_hYGieE/edit')
donat = InlineKeyboardButton(text='Пожертвования', callback_data='donat')
game_servers = InlineKeyboardButton(text='Игровые Сервера', callback_data='game_servers')

# Создание клавиатуры
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
    [vk, discord, site],
    [start_game, rp_roles],
    [donat, game_servers]
])
