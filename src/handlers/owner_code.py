from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import OwnerCode
from utils.dbconnect import Request
from keyboards.reply import main
from config.config_reader import config

router = Router()

@router.message(OwnerCode.get_code)
async def get_code(message: Message, request: Request, state: FSMContext):
    if message.text == config.owner_code.get_secret_value():
        await request.add_owner(message.from_user.id)
        await message.answer(f"🔑Теперь у вас есть права организатора!", reply_markup=main)
    else:
        await message.answer(f"🚫Неверный код", reply_markup=main)
    await state.clear()