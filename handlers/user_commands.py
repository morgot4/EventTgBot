from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import reply

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Hello, <b>{message.from_user.first_name}</b>.", reply_markup=reply.main)