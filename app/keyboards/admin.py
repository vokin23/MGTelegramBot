from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Создание кнопок
create_event = InlineKeyboardButton(text='Создать розыгрыш', callback_data='create_event')
create_post = InlineKeyboardButton(text='Создать отложенный пост', callback_data='create_post')
publish_post = InlineKeyboardButton(text='Опубликовать пост', callback_data='publish_post')

publish_new_post = InlineKeyboardButton(text='Опубликовать(Создать) новый пост', callback_data='publish_new_post')
publish_old_post = InlineKeyboardButton(text='Опубликовать(из отложенных) старый пост', callback_data='set_publish_old_post')

# Создание клавиатуры
admin_start = InlineKeyboardMarkup(inline_keyboard=[
    [create_event],
    [create_post],
    [publish_post]
])

# Создание клавиатуры
publish_post_kb = InlineKeyboardMarkup(inline_keyboard=[
    [publish_new_post],
    [publish_old_post]
])
