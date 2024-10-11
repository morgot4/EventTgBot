from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕Создать"),
            KeyboardButton(text="📃Мероприятия"),
        ],
        [
            KeyboardButton(text="🔐Стать организатором"),
            KeyboardButton(text="👤Мои мероприятия"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие",
    
)


rmk = ReplyKeyboardRemove()