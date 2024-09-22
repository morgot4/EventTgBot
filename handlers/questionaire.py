from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk

router = Router()

@router.message(Command("profile"))
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "👋 Давай начнем, введите название мероприятия", reply_markup=rmk
    )


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.date)
    await message.answer("📅 Отлично, теперь введите дату проведения мероприятия в формате ДД.ММ.ГГГГ")

@router.message(Form.date)
async def form_date(message: Message, state: FSMContext):
    lst_date = message.text.split(".")

    # TODO Реализовать более точную проверку даты используя datetime (вводимая дата всегда должна быть больше текущей)

    if all([num.isdigit() for num in lst_date]) and 1 <= int(lst_date[0]) <= 31 and 1 <= int(lst_date[1]) <= 12 and int(lst_date[2]) >= 2024:
        await state.update_data(date=message.text)
        await state.set_state(Form.info)
        await message.answer(
            "ℹ️ Теперь добавьте дополнительную информацию"
        )
        
    else:
        await message.answer("🚫 Неправильная дата. Введите новую")

        
@router.message(Form.info)
async def form_info(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("😒 Введите что-то поинтереснее")
    elif len(message.text) > 500:
        await message.answer("🫤 Слишком много текста. Попробуйте еще раз")
    else:
        await state.update_data(info=message.text)
        await state.set_state(Form.link)
        await message.answer("🔗 Теперь добавьте ссылку на запись.")

@router.message(Form.link)
async def form_link(message: Message, state: FSMContext):

    # TODO Реализовать проверку ссылки

    await state.update_data(info=message.text)
    await state.set_state(Form.photo)
    await message.answer("📷 Последний шаг! Добавьте фотографию для вашего мероприятия")

@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()

    await message.answer("🎉 Поздравляю! Вы успешно создали мероприятие")

    # TODO реализовать другой вывод всех данных чтобы key был на русском языке

    formatted_text = []
    [
        formatted_text.append(f"{key}: {value}")
        for key, value in data.items()
    ]
    await message.answer_photo(
        photo_file_id,
        "\n".join(formatted_text)
    )

@router.message(Form.photo, ~F.photo)
async def incorrect_form_photo(message: Message, state: FSMContext):

    # TODO текущая проверка фото не разрешает отправку фото файлом, нужно разрешить. 
    # TODO А так же реализовать проверку размера фотографии

    await message.answer("Это не фотография")