from aiogram.fsm.state import StatesGroup, State
from keyboards import reply, builders
class Form(StatesGroup):
    name = State()
    date =  State()
    time = State()
    place = State()
    info = State()
    link = State()
    owner_info = State()
    delete_template = State()
    add_template_name = State()
    add_template_value = State()
    photo = State()
    final = State()
    change_before_publish = State()
    change_after_publish = State()

    texts = {
        "Form:name" : ("👋 Давай начнем, введите название мероприятия", builders.profile(["⬅️назад"])),
        "Form:date" : ("📅 Отлично, теперь введите дату проведения мероприятия в формате ДД.ММ.ГГГГ", builders.profile(["⬅️назад"])),
        "Form:time" : ("⏱️Укажите время начала в формате ЧЧ:MM", builders.profile(["⬅️назад"])),
        "Form:place" : ("🗺️Добавьте место проведения мероприятия", builders.profile(["⬅️назад"])),
        "Form:info" : ("ℹ️ Теперь добавьте комментарий от организатора", builders.profile(["❌Без комментария", "⬅️назад"])),
        "Form:link" : ("🔗 Добавьте ссылку на запись", builders.profile(["❌Без ссылки", "⬅️назад"])),
        "Form:owner_info" : ("👤Добавьте контактную информацию организатора", builders.profile(["📃Использовать шаблон", "➕Добавить шаблон","⬅️назад"])),
        "Form:photo" : ("📷 Добавьте фотографию для вашего мероприятия", builders.profile(["❌Без фотографии", "⬅️назад"])),
        "Form:final" : ("Вы создали черновик мероприятия.", builders.profile(["Опубликовать", "Изменить", "⬅️назад"]))

    }

class OwnerCode(StatesGroup):
    get_code = State()