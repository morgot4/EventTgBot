from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards import reply, inline, builders, fabrics
from data.subloader import get_json

router = Router()

@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    smiles = await get_json("smiles.json")
    if msg == 'ссылки':
        await message.answer("Вот ваши ссылки", reply_markup=inline.links)
    elif msg == 'спец кнопки':
        await message.answer("Спец кнопки: ", reply_markup=reply.spec)
    elif msg == 'калькулятор':
        await message.answer("Введите выражение: ", reply_markup=builders.calc())
    elif msg == "смайлики":
        await message.answer(f"{smiles[0][0]} <b>{smiles[0][1]}</b>", reply_markup=fabrics.paginator())