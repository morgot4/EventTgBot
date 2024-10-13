
class EventTextFormater:
    def __init__(self):
        pass

    async def get_more_info(self, event) -> str:
        place = ""
        info = ""
        link = ""
        if event["place"].replace(" ", "") not in ["", "-"]:
            place = f"<b>🗺️Где?</b> {event["place"]}\n\n"
        if event["info"].replace(" ", "") not in ["", "-"]:
            info = f"<b>ℹ️Инфо:</b> {event["info"]}\n\n"
        if event["link"].replace(" ", "") not in ["", "-"]:
            link = f"<b>🔗Ссылка:</b> {event["link"]}\n\n"
        owner_info = event["owner_info"]
        more_info = f"{place}{info}{link}👤<b>Организатор:</b> {owner_info}"
        return more_info
    
    async def get_basic_info(self, event):
        name = event["name"]
        date = event["date"]
        basic_info = f"<b>🗣️Название:</b> {name}\n\n<b>📅Когда?</b> {date.strftime("%d.%m.%Y")} в {date.strftime("%H:%M")}"
        return basic_info