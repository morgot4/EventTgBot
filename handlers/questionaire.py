from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import datetime
from keyboards.reply import main
from utils.states import Form
from utils.dbconnect import Request
from utils.event_text_formater import EventTextFormater
from keyboards.builders import profile
from keyboards.reply import rmk
from urllib.parse import urlparse

router = Router()
event_txt = EventTextFormater()



async def check_date(date: str) -> bool: #YYYY MM DD
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

async def check_time(time: str) -> bool:
    try:
        hours, minutes = time.split(":")
        if 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59:
            return True
        else:
            return False
    except Exception as ex:
        return False
    

async def print_event_data(state, message, after_publish=False):
    data = await state.get_data()
    if after_publish:
        await message.answer("Вы создали черновик мероприятия.", reply_markup=profile(["✅Применить изменения", "⚙️Добавить изменение"]))
    else:
        await message.answer("Вы создали черновик мероприятия.", reply_markup=profile(["🗣️Опубликовать", "⚙️Изменить", "⬅️назад"]))
    date = data["date"].split(".")
    time = data["time"].split(":")
    date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
    data["date"] = date
    basic_info = await event_txt.get_basic_info(data)
    more_info = await event_txt.get_more_info(data)
    photo_file_id = data["photo_file_id"]

    formatted_text = f"{basic_info}\n\n{more_info}"
    if photo_file_id != None:
        await message.answer_photo(
            photo_file_id,
            formatted_text,
        )
    else:
        await message.answer(formatted_text)


@router.message(StateFilter("*"), F.text.casefold().in_(["⬅️назад"]))
async def back_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Form.name:
        await state.clear()
        await message.answer("Создание мероприятия отменено", reply_markup=main)
        return
    elif current_state == Form.change_after_publish:
        await state.clear()
        await message.answer("Изменение мероприятия отменено", reply_markup=main)
        return
    prev = None
    for st in Form.__all_states__:
        if st.state == current_state:
            match prev.state[5:]:
                case "name":
                    await state.update_data(name="")
                case "date":
                    await state.update_data(date="")
                case "time":
                    await state.update_data(time="")
                case "place":
                    await state.update_data(place="")
                case "info":
                    await state.update_data(info="")
                case "link":
                    await state.update_data(link="")
                case "photo":
                    await state.update_data(photo="")
                case "owner_info":
                    await state.update_data(owner_info="")

            await state.set_state(prev)
            if prev.state != "Form:final":
                await message.answer(Form.texts[prev.state][0], reply_markup=Form.texts[prev.state][1])
            else:
                await print_event_data(state=state, message=message)
            return
        prev = st



@router.message(Form.name)
async def form_name(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    name = message.text
    if len(name) > 50:
        await message.answer("🚫Cлишком длинное названи. Попробуйте еще раз.")
    else:
        await state.update_data(name=name)
        if "name" in data.keys() and data["name"] == "CHANGE_AFTER_PUBLISH_NAME":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "name" in data.keys() and data["name"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.date)
            await message.answer("📅 Отлично, теперь введите дату проведения мероприятия в формате ДД.ММ.ГГГГ", reply_markup=profile(["⬅️назад"]))



@router.message(Form.date, F.text)
async def form_date(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    lst_date = message.text # DD MM YYYY
    if await check_date(lst_date):
        await state.update_data(date=message.text)
        if "date" in data.keys() and data["date"] == "CHANGE_AFTER_PUBLISH_DATE":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "date" in data.keys() and data["date"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.time)
            await message.answer("⏱️Укажите время начала в формате ЧЧ:MM", reply_markup=profile(["⬅️назад"]))
        
    else:
        await message.answer("🚫 Неправильная дата. Введите новую")


@router.message(Form.date)
async def incorrect_form_date(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных даты")


@router.message(Form.time, F.text)
async def form_time(message: Message, state: FSMContext):
    time = message.text
    data = await state.get_data()
    if await check_time(time):
        await state.update_data(time=message.text)
        if "time" in data.keys() and data["time"] == "CHANGE_AFTER_PUBLISH_TIME":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "time" in data.keys() and data["time"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.place)
            await message.answer(
                "🗺️Добавьте место проведения мероприятия", reply_markup=profile(["⬅️назад"])
            )
    else:
        await message.answer("🚫 Неправильное время. Введите новое")

@router.message(Form.time)
async def incorrect_form_time(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных для времени")

@router.message(Form.place, F.text)
async def form_place(message: Message, state: FSMContext):
    data = await state.get_data()
    place = message.text
    if len(place) > 70:
        await message.answer("🚫Cлишком много инфорамции. Попробуйте еще раз.")
    else:
        await state.update_data(place=message.text)
        if "place" in data.keys() and data["place"] == "CHANGE_AFTER_PUBLISH_PLACE":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "place" in data.keys() and data["place"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.info)
            await message.answer(
                "ℹ️ Теперь добавьте комментарий от организатора", reply_markup=profile(["❌Без комментария", "⬅️назад"])
            )

@router.message(Form.place)
async def incorrect_form_place(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных места")

@router.message(Form.info, F.text.casefold().in_(["❌без комментария"]))
async def with_out_info(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(info="-")
    if "info" in data.keys() and data["info"] == "CHANGE_AFTER_PUBLISH_INFO":
        await print_event_data(state=state, message=message, after_publish=True)
        await state.set_state(Form.final)
    elif "info" in data.keys() and data["info"] != "":
        await print_event_data(state=state, message=message)
        await state.set_state(Form.final)
    else:
        await state.set_state(Form.link)
        await message.answer("🔗 Добавьте ссылку на запись.", reply_markup=profile(["❌Без ссылки", "⬅️назад"]))

        
@router.message(Form.info, F.text)
async def form_info(message: Message, state: FSMContext):
    data = await state.get_data()
    if len(message.text) < 5:
        await message.answer("😒 Введите что-то поинтереснее", reply_markup=profile(["❌Без комментария", "⬅️назад"]))
    elif len(message.text) > 800:
        await message.answer("🫤 Слишком много текста. Попробуйте еще раз", reply_markup=profile(["❌Без комментария", "⬅️назад"]))
    else:
        await state.update_data(info=message.text)
        if "info" in data.keys() and data["info"] == "CHANGE_AFTER_PUBLISH_INFO":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "info" in data.keys() and data["info"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.link)
            await message.answer("🔗 Добавьте ссылку на запись.", reply_markup=profile(["❌Без ссылки", "⬅️назад"]))

@router.message(Form.info)
async def incorrect_form_info(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных комментария")

@router.message(Form.link, F.text.casefold().in_(["❌без ссылки"]))
async def with_out_info(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(link="-")
    if "link" in data.keys() and data["link"] == "CHANGE_AFTER_PUBLISH_LINK":
        await print_event_data(state=state, message=message, after_publish=True)
        await state.set_state(Form.final)
    elif "link" in data.keys() and data["link"] != "":
        await print_event_data(state=state, message=message)
        await state.set_state(Form.final)
    else:
        await state.set_state(Form.owner_info)
        await message.answer("👤Добавьте контактную информацию организатора", reply_markup=profile(["⬅️назад"]))

@router.message(Form.link, F.text)
async def form_link(message: Message, state: FSMContext):
    data = await state.get_data()
    if urlparse(message.text).scheme:
        await state.update_data(link=message.text)
        if "link" in data.keys() and data["link"] == "CHANGE_AFTER_PUBLISH_LINK":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
        elif "link" in data.keys() and data["link"] != "":
            await print_event_data(state=state, message=message)
            await state.set_state(Form.final)
        else:
            await state.set_state(Form.owner_info)
            await message.answer("👤Добавьте контактную информацию организатора", reply_markup=profile(["📃Использовать шаблон", "➕Добавить шаблон","⬅️назад"]))
    else:
        await message.answer("🚫Ссылка некорректа! Введите еще раз")

@router.message(Form.link)
async def incorrect_form_link(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных ссылки")


@router.message(Form.owner_info, F.text.casefold().in_(["📃использовать шаблон"]))
async def form_owner(message: Message, state: FSMContext):
    await state.set_state(Form.use_template)
    await message.answer("Выберите шаблон")

# @router.message(Form.owner_info, F.text)
# async def form_owner(message: Message, state: FSMContext):
#     data = await state.get_data()
#     owner_info = message.text
#     if len(owner_info) > 70:
#         await message.answer("🚫Слишком много контактной информации. Попробуйте еще раз.")
#     else:
#         await state.update_data(owner_info=owner_info)
#         if "owner_info" in data.keys() and data["owner_info"] == "CHANGE_AFTER_PUBLISH_OWNER":
#             await print_event_data(state=state, message=message, after_publish=True)
#             await state.set_state(Form.final)
#         elif "owner_info" in data.keys() and data["owner_info"] != "":
#             await print_event_data(state=state, message=message)
#             await state.set_state(Form.final)
#         else:
#             await state.set_state(Form.photo)
#             await message.answer("📷 Добавьте фотографию для вашего мероприятия", reply_markup=profile(["❌Без фотографии", "⬅️назад"]))

@router.message(Form.owner_info)
async def incorrect_form_owner(message: Message, state: FSMContext):
    await message.answer("🚫Некорректный тип данных контактной информации")

@router.message(Form.photo, F.text.casefold().in_(["❌без фотографии"]))
async def with_out_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(photo_file_id=None)
    if "photo_file_id" in data.keys() and data["photo_file_id"] == "CHANGE_AFTER_PUBLISH_PHOTO_FILE_ID":
        await print_event_data(state=state, message=message, after_publish=True)
        await state.set_state(Form.final)
    else:
        await print_event_data(state=state, message=message)
        await state.set_state(Form.final)

@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    if "photo_file_id" in data.keys() and data["photo_file_id"] == "CHANGE_AFTER_PUBLISH_PHOTO_FILE_ID":
            await print_event_data(state=state, message=message, after_publish=True)
            await state.set_state(Form.final)
    else:
        await print_event_data(state=state, message=message)
        await state.set_state(Form.final)


@router.message(Form.photo, ~F.photo)
async def incorrect_form_photo(message: Message, state: FSMContext):
    
    await message.answer("Это не фотография. (*подсказка* Не отправляйте файлом)")

@router.message(Form.final, F.text.casefold().in_(["🗣️опубликовать"]))
async def publish(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    data["owner_telegram_id"] = message.from_user.id
    await request.add_event(data)
    await message.answer("🎉Поздравляю! Мероприятие успешно опубликовано!", reply_markup=main)
    await state.clear()

@router.message(Form.final, F.text.casefold().in_(["⚙️изменить"]))
async def final_change(message: Message, state: FSMContext):
    await state.set_state(Form.change_before_publish)
    await message.answer("Выберите", reply_markup=profile([
        "⬅️назад", "Изменить название", "Изменить дату", "Изменить время", "Изменить место", "Изменить комментарий", 
        "Изменить ссылку", "Изменить организатора", "Изменить фотографию"
    ]))

@router.message(Form.final, F.text.casefold().in_(["⚙️добавить изменение"]))
async def final_change(message: Message, state: FSMContext):
    await state.set_state(Form.change_after_publish)
    await message.answer("Выберите", reply_markup=profile([
        "⬅️назад", "Изменить название", "Изменить дату", "Изменить время", "Изменить место", "Изменить комментарий", 
        "Изменить ссылку", "Изменить организатора", "Изменить фотографию"
    ]))

@router.message(Form.final, F.text.casefold().in_(["✅применить изменения"]))
async def final_change_after_publish(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    data["owner_telegram_id"] = message.from_user.id
    await request.set_event(data)
    await message.answer("🎉Мероприятие успешно изменено!", reply_markup=main)
    await state.clear()


async def all_changes(message, state, after_publish=False):
    msg = message.text.lower()
    if msg == "изменить название":
        if after_publish:
            await state.update_data(name="CHANGE_AFTER_PUBLISH_NAME")
        await state.set_state(Form.name)
        await message.answer("Введите название еще раз")
    elif msg == "изменить дату":
        if after_publish:
            await state.update_data(date="CHANGE_AFTER_PUBLISH_DATE")
        await state.set_state(Form.date)
        await message.answer("Введите новую дату в формате ДД.ММ.ГГГГ")
    elif msg == "изменить время":
        if after_publish:
            await state.update_data(time="CHANGE_AFTER_PUBLISH_TIME")
        await state.set_state(Form.time)
        await message.answer("Введите новое время в формате ЧЧ:ММ")
    elif msg == "изменить место":
        if after_publish:
            await state.update_data(place="CHANGE_AFTER_PUBLISH_PLACE")
        await state.set_state(Form.place)
        await message.answer("Введите новое место")
    elif msg == "изменить комментарий":
        if after_publish:
            await state.update_data(info="CHANGE_AFTER_PUBLISH_INFO")
        await state.set_state(Form.info)
        await message.answer("Введите комментарий от организатора заново", reply_markup=profile(["❌Без комментария"]))
    elif msg == "изменить ссылку":
        if after_publish:
            await state.update_data(link="CHANGE_AFTER_PUBLISH_LINK")
        await state.set_state(Form.link)
        await message.answer("Добавьте другую ссылку на запись", reply_markup=profile(["❌Без ссылки"]))
    elif msg == "изменить организатора":
        if after_publish:
            await state.update_data(owner="CHANGE_AFTER_PUBLISH_OWNER")
        await state.set_state(Form.owner_info)
        await message.answer("Добавьте новую информацию об организаторе")
    elif msg == "изменить фотографию":
        if after_publish:
            await state.update_data(photo_file_id="CHANGE_AFTER_PUBLISH_PHOTO_FILE_ID")
        await state.set_state(Form.photo)
        await message.answer("Пришлите новую фотографию", reply_markup=profile(["❌Без фотографии"]))


@router.message(Form.change_before_publish, F.text)
async def changes(message: Message, state: FSMContext):
    await all_changes(message=message, state=state)
    
@router.message(Form.change_before_publish)
async def incorrect_changes(message: Message, state: FSMContext):
    await message.asnwer("Некоректный тип данных для изменений")


@router.message(Form.change_after_publish, F.text)
async def changes_after_publish(message: Message, state: FSMContext):
    await all_changes(message=message, state=state, after_publish=True)
    
@router.message(Form.change_after_publish)
async def incorrect_changes(message: Message, state: FSMContext):
    await message.asnwer("Некоректный тип данных для изменений")
