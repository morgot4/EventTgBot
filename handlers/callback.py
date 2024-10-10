from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from utils.callback import EventDetails
from utils.dbconnect import Request
from utils.states import Form
from utils.event_text_formater import EventTextFormater
from aiogram.enums import ParseMode
from keyboards import inline
from keyboards.builders import profile

event_txt = EventTextFormater()
router = Router()

@router.callback_query(EventDetails.filter(F.action == "more"))
async def details(call: CallbackQuery, callback_data: EventDetails, request: Request):
    text1 = call.message.caption
    text2 = call.message.text
    event = await request.get_events(callback_data.id)
    more_info = await event_txt.get_more_info(event[0])
    photo = event[0]["photo_file_id"]
    if photo != None:
        new_text = InputMediaPhoto(media=photo, caption=f"{text1}\n\n{more_info}", parse_mode=ParseMode.HTML)
        if callback_data.listing:
            await call.message.edit_media(new_text, reply_markup=inline.get_exit_inline_keyboard(callback_data.id))
        else:
            await call.message.edit_media(new_text, reply_markup=inline.get_owner_exit_inline_keyboard(callback_data.id))
    else:
        if callback_data.listing:
            await call.message.edit_text(f"{text2}\n\n{more_info}", parse_mode=ParseMode.HTML, reply_markup=inline.get_exit_inline_keyboard(callback_data.id))
        else:
            await call.message.edit_text(f"{text2}\n\n{more_info}", parse_mode=ParseMode.HTML, reply_markup=inline.get_owner_exit_inline_keyboard(callback_data.id))
    await call.answer()

@router.callback_query(EventDetails.filter(F.action == "exit"))
async def details(call: CallbackQuery, callback_data: EventDetails, request: Request):
    event = await request.get_events(callback_data.id)
    basic_info = await event_txt.get_basic_info(event[0])
    photo = event[0]["photo_file_id"]
    if photo != None:
        new_text = InputMediaPhoto(media=photo, caption=basic_info, parse_mode=ParseMode.HTML)
        if callback_data.listing:
            await call.message.edit_media(new_text, reply_markup=inline.get_more_inline_keyboard(callback_data.id))
        else:
            await call.message.edit_media(new_text, reply_markup=inline.get_owner_more_inline_keyboard(callback_data.id))
    else:
        if callback_data.listing:
            await call.message.edit_text(basic_info, parse_mode=ParseMode.HTML, reply_markup=inline.get_more_inline_keyboard(callback_data.id))
        else:
            await call.message.edit_text(basic_info, parse_mode=ParseMode.HTML, reply_markup=inline.get_owner_more_inline_keyboard(callback_data.id))
    await call.answer()

@router.callback_query(EventDetails.filter(F.action == "delete"))
async def details(call: CallbackQuery, callback_data: EventDetails, request: Request):
    await request.delete_event(callback_data.id)
    await call.message.delete()
    
    #await call.answer()


@router.callback_query(EventDetails.filter(F.action == "change"))
async def details(call: CallbackQuery, callback_data: EventDetails, state: FSMContext, request: Request):
    event = await request.get_events(callback_data.id)
    event = event[0]
    date = event["date"]
    time = date.strftime("%H:%M")
    date = date.strftime("%d.%m.%Y")
    data = {"name": event["name"],
            "date": date,
            "time": time,
            "place": event["place"],
            "info": event["info"], 
            "link": event["link"],
            "owner_info": event["owner_info"],
            "photo_file_id": event["photo_file_id"]}
    await state.set_data(data)  
    await state.set_state(Form.change_after_publish)
    await call.message.answer("Выберите изменения", reply_markup=profile([
        "⬅️назад", "Изменить название", "Изменить дату", "Изменить время", "Изменить место", "Изменить комментарий", 
        "Изменить ссылку", "Изменить организатора", "Изменить фотографию"
    ]))
    return
    