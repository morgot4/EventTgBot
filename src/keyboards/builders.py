from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    
    [builder.button(text=txt) for txt in text]
    builder.adjust(*[1] * len(text))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)