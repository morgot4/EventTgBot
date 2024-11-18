from aiogram.fsm.state import StatesGroup, State
from src.keyboards import reply, builders
import emoji

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
        "Form:name" : (emoji.emojize(":waving_hand: Давай начнем, введите название мероприятия"), builders.profile([emoji.emojize(":left_arrow:назад")])),
        "Form:date" : (emoji.emojize(":calendar: Отлично, теперь введите дату проведения мероприятия в формате ДД.ММ.ГГГГ"), builders.profile([emoji.emojize(":left_arrow:назад")])),
        "Form:time" : (emoji.emojize(":stopwatch:Укажите время начала в формате ЧЧ:MM"), builders.profile([emoji.emojize(":left_arrow:назад")])),
        "Form:place" : (emoji.emojize(":world_map:Добавьте место проведения мероприятия"), builders.profile([emoji.emojize(":left_arrow:назад")])),
        "Form:info" : (emoji.emojize(":information: Теперь добавьте комментарий от организатора"), builders.profile([emoji.emojize(":cross_mark:Без комментария"), emoji.emojize(":left_arrow:назад")])),
        "Form:link" : (emoji.emojize(":link: Добавьте ссылку на запись"), builders.profile([emoji.emojize(":cross_mark:Без ссылки"), emoji.emojize(":left_arrow:назад")])),
        "Form:owner_info" : (emoji.emojize(":bust_in_silhouette:Добавьте контактную информацию организатора"), builders.profile([emoji.emojize(":page_with_curl:Использовать шаблон"), emoji.emojize(":plus:Добавить шаблон"), emoji.emojize(":wastebasket:Удалить шаблон"), emoji.emojize(":left_arrow:назад")])),
        "Form:photo" : (emoji.emojize(":camera: Добавьте фотографию для вашего мероприятия"), builders.profile([emoji.emojize(":cross_mark:Без фотографии"), emoji.emojize(":left_arrow:назад")])),
        "Form:final" : ("Вы создали черновик мероприятия.", builders.profile(["Опубликовать", "Изменить", emoji.emojize(":left_arrow:назад")]))

    }

class OwnerCode(StatesGroup):
    get_code = State()