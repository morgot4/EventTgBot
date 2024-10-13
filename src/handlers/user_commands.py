from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.keyboards import reply

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>. Начнем работу!", reply_markup=reply.main)