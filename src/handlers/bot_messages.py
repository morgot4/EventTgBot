from aiogram import Router, F
from aiogram.types import Message
from src.keyboards import reply, inline, builders
from src.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from src.utils.states import OwnerCode, Form

router = Router()

@router.message()
async def echo(message: Message, request: Request, state: FSMContext):
    msg = message.text.lower()
    telegram_id = message.from_user.id
    is_user_owner = await request.is_owner(telegram_id)
    user_id = await request.get_id(telegram_id)
    if msg == "🔐стать организатором":
        if is_user_owner:
            await message.answer(f"Вы уже организатор", reply_markup=reply.main)
        else:
            await message.answer(f"Введите код организатора")
            await state.set_state(OwnerCode.get_code)

    elif msg == "➕создать":
        if is_user_owner:
            await state.set_state(Form.name)
            await message.answer(
                "👋 Давай начнем, введите название мероприятия", reply_markup=builders.profile(["⬅️Назад"])
            )
        else:
            await message.answer(f"Только организатор может создать мероприятие!", reply_markup=reply.main)
    elif msg == "📃мероприятия":
        await message.answer("👇Все мероприятия", reply_markup=reply.main)
        await request.get_events_list(message=message)

    elif msg == "👤мои мероприятия":
        await message.answer("👇Ваши мероприятия",  reply_markup=builders.profile(["⬅️Назад в меню"]))
        await request.get_events_list(message=message, user_id=user_id)

    elif msg == "⬅️назад в меню":
        await message.answer("Выберите действие", reply_markup=reply.main)

