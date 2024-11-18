import emoji

class EventTextFormater:
    def __init__(self):
        pass

    async def get_more_info(self, event) -> str:
        place = ""
        info = ""
        link = ""
        if event["place"].replace(" ", "") not in ["", "-"]:
            place = emoji.emojize("<b>:world_map:Где?</b> ") + str(event["place"]) + "\n\n"
        if event["info"].replace(" ", "") not in ["", "-"]:
            info = emoji.emojize("<b>:information:Инфо:</b> ") + str(event["info"]) + "\n\n"
        if event["link"].replace(" ", "") not in ["", "-"]:
            link = emoji.emojize("<b>:link:Ссылка:</b> ") + str(event["link"]) + "\n\n"
        owner_info = event["owner_info"]
        more_info = f"{place}{info}{link}" + emoji.emojize(":bust_in_silhouette:<b>Организатор:</b> ") + str(owner_info)
        return more_info
    
    async def get_basic_info(self, event):
        name = event["name"]
        date = event["date"]
        basic_info = emoji.emojize("<b>:speaking_head:Название:</b> ") + f"{name}\n\n<b>" + emoji.emojize(":calendar:Когда?</b> ") + f"{date.strftime("%d.%m.%Y")} в {date.strftime("%H:%M")}"
        return basic_info