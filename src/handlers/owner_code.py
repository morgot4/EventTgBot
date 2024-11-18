from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.utils.states import OwnerCode
from src.utils.dbconnect import Request
from src.keyboards.reply import main
import emoji

router = Router()

@router.message(OwnerCode.get_code)
async def get_code(message: Message, request: Request, state: FSMContext):
    if message.text == "15011984":
        await request.add_owner(message.from_user.id)
        await message.answer(femoji.emojize(":key:Теперь у вас есть права организатора!"), reply_markup=main)
    else:
        await message.answer(femoji.emojize(":prohibited:Неверный код"), reply_markup=main)
    await state.clear()