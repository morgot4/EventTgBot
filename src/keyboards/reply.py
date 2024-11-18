from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
import emoji

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=emoji.emojize(":plus:Создать")),
            KeyboardButton(text=emoji.emojize(":page_with_curl:Мероприятия")),
        ],
        [
            KeyboardButton(text=emoji.emojize(":locked_with_key:Стать организатором")),
            KeyboardButton(text=emoji.emojize(":bust_in_silhouette:Мои мероприятия")),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие",
    
)


rmk = ReplyKeyboardRemove()