from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callback import EventDetails
from aiogram.types import (
    InlineKeyboardButton,
)


def get_more_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="⬇️Подробнее", callback_data=EventDetails(id=event_id, action="more", listing=True).pack())
        )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_exit_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="⬆️Скрыть", callback_data=EventDetails(id=event_id, action="exit", listing=True).pack())
        )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_owner_more_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="⬇️Подробнее", callback_data=EventDetails(id=event_id, action="more",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text="🗑️Удалить", callback_data=EventDetails(id=event_id, action="delete",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text="⚙️Изменить", callback_data=EventDetails(id=event_id, action="change",  listing=False).pack())
        )
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()

def get_owner_exit_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text="⬆️Скрыть", callback_data=EventDetails(id=event_id, action="exit",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text="🗑️Удалить", callback_data=EventDetails(id=event_id, action="delete",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text="⚙️Изменить", callback_data=EventDetails(id=event_id, action="change",  listing=False).pack())
        )
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()