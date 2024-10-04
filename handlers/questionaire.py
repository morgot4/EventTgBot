from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import datetime
from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk

router = Router()


def check_date(date: str) -> bool: #YYYY MM DD
    try:
        date = date.split(".")[::-1]
        date[1] = date[1].zfill(2); date[2] = date[2].zfill(2)
        datetime.date.fromisoformat("-".join(date))
        date[1] = date[1].rstrip(); date[2] = date[2].rstrip()
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])) >= datetime.datetime.now():
            return True
        else:
            raise ValueError
    except Exception as ex:
        print(ex)
        return False
async def print_event_data(state, message, photo_file_id=None):
    data = await state.get_data()
    await message.answer("Вы создали черновик мероприятия.", reply_markup=profile(["Опубликовать", "Изменить"]))

    equals = {  "name": "<b>Название</b>",
                "date": "<b>Дата</b>",
                "info": "<b>Комментарий от организатора</b>",
                "link": "<b>Ссылка на запись</b>"}
    print(data.items())
    formatted_text = []
    [
        formatted_text.append(f"{equals[key]}: {value}")
        for key, value in data.items() if value != ""
    ]
    if photo_file_id != None:
        await message.answer_photo(
            photo_file_id,
            "\n".join(formatted_text)
        )
    else:
        await message.answer("\n".join(formatted_text))

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
    lst_date = message.text # DD MM YYYY
    if check_date(lst_date):
        await state.update_data(date=message.text)
        await state.set_state(Form.info)
        await message.answer(
            "ℹ️ Теперь добавьте комментарий от организатора", reply_markup=profile(["Без комментария"])
        )
        
    else:
        await message.answer("🚫 Неправильная дата. Введите новую")


@router.message(Form.info, F.text.casefold().in_(["без комментария"]))
async def with_out_info(message: Message, state: FSMContext):
    await state.update_data(info="")
    await state.set_state(Form.link)
    await message.answer("🔗 Добавьте ссылку на запись.", reply_markup=rmk)

@router.message(Form.info, F.text.casefold().in_(["изменить комментарий"]))
async def with_out_info(message: Message, state: FSMContext):
    await state.update_data(info="")
    await state.set_state(Form.link)
    await message.answer("🔗 Добавьте ссылку на запись.", reply_markup=rmk)
        
@router.message(Form.info)
async def form_info(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("😒 Введите что-то поинтереснее", reply_markup=profile(["Без комментария"]))
    elif len(message.text) > 500:
        await message.answer("🫤 Слишком много текста. Попробуйте еще раз", reply_markup=profile(["Без комментария"]))
    else:
        await state.update_data(info=message.text)
        await state.set_state(Form.link)
        await message.answer("🔗 Добавьте ссылку на запись.", reply_markup=rmk)

@router.message(Form.link)
async def form_link(message: Message, state: FSMContext):

    # TODO Реализовать проверку ссылки

    await state.update_data(link=message.text)
    await state.set_state(Form.photo)
    await message.answer("📷 Добавьте фотографию для вашего мероприятия", reply_markup=profile(["Без фотографии"]))

@router.message(Form.photo, F.text.casefold().in_(["без фотографии"]))
async def with_out_photo(message: Message, state: FSMContext):
    await print_event_data(state=state, message=message)
    await state.set_state(Form.final)

@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await print_event_data(state=state, message=message, photo_file_id=photo_file_id)
    await state.set_state(Form.final)

@router.message(Form.photo, ~F.photo)
async def incorrect_form_photo(message: Message, state: FSMContext):

    # TODO текущая проверка фото не разрешает отправку фото файлом, нужно разрешить. 
    # TODO А так же реализовать проверку размера фотографии

    await message.answer("Это не фотография. (*подсказка* Не отправляйте файлом)")

@router.message(Form.final, F.text.casefold().in_(["опубликовать"]))
async def publish(message: Message, state: FSMContext):

    # TODO реализовать запись мероприятия в базу данных
    await message.answer("🎉Поздравляю! Мероприятие успешно опубликовано!", reply_markup=rmk)
    await state.clear()

@router.message(Form.final, F.text.casefold().in_(["изменить"]))
async def final_change(message: Message, state: FSMContext):

    await message.answer("Выберите", reply_markup=profile([
        "Изменить название", "Изменить дату", "Изменить комментарий", "Изменить ссылку", "Изменить фотографию"
    ]))
    await state.set_state(Form.change)
