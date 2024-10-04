from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    date =  State()
    info = State()
    link = State()
    photo = State()
    final = State()
    publish = State()
    change = State()
    change_name = State()
    change_date =  State()
    change_info = State()
    change_link = State()
    change_photo = State()