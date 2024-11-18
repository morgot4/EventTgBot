from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils.callback import EventDetails
from aiogram.types import (
    InlineKeyboardButton,
)
import emoji


def get_more_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":down_arrow:Подробнее"), callback_data=EventDetails(id=event_id, action="more", listing=True).pack())
        )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_exit_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":up_arrow:Скрыть"), callback_data=EventDetails(id=event_id, action="exit", listing=True).pack())
        )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_owner_more_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":down_arrow:Подробнее"), callback_data=EventDetails(id=event_id, action="more",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":pause_button:Завершить"), callback_data=EventDetails(id=event_id, action="stop",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":writing_hand:Изменить"), callback_data=EventDetails(id=event_id, action="change",  listing=False).pack())
        )
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()


def get_owner_exit_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":up_arrow:Скрыть"), callback_data=EventDetails(id=event_id, action="exit",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":pause_button:Завершить"), callback_data=EventDetails(id=event_id, action="stop",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":writing_hand:Изменить"), callback_data=EventDetails(id=event_id, action="change",  listing=False).pack())
        )
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()


def get_owner_remove_inline_keyboard(event_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":wastebasket:Удалить"), callback_data=EventDetails(id=event_id, action="delete",  listing=False).pack())
        )
    keyboard_builder.add(
        InlineKeyboardButton(text=emoji.emojize(":play_button:Восстановить"), callback_data=EventDetails(id=event_id, action="play",  listing=False).pack())
        )
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()