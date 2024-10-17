import asyncpg
import datetime
from src.keyboards import inline, reply
from src.utils.event_text_formater import EventTextFormater
import emoji
emoji.emojize
event_txt = EventTextFormater()


class Request:
    def __init__(self, connector: asyncpg.pool.Pool) -> None:
        self.connector = connector


    async def get_id(self, telegram_id):
        return await self.connector.fetchval("SELECT id FROM owners WHERE telegram_id = $1", telegram_id)
    
    async def is_owner(self, telegram_id):
        if await self.get_id(telegram_id=telegram_id) != None:
            return True
        return False
    
    async def add_owner(self, telegram_id):
        return await self.connector.execute(f"INSERT INTO owners (telegram_id) VALUES ({telegram_id})")
    
    async def add_event(self, data):
        date = data["date"].split(".")
        time = data["time"].split(":")
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
        owner_id = await self.get_id(data["owner_telegram_id"])
        return await self.connector.execute("INSERT INTO events(name, date, info, link, owner_id, photo_file_id, place, owner_info, status) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)", data["name"], date, data["info"], data['link'], owner_id, data["photo_file_id"], data["place"], data["owner_info"], "active")
    
    async def add_template(self, name, value, telegram_id):
        owner_id = await self.get_id(telegram_id)
        return await self.connector.execute("INSERT INTO templates(owner_id, name, value) VALUES ($1, $2, $3)", owner_id, name, value) 

    async def set_event(self, data: dict):
        date = data["date"].split(".")
        time = data["time"].split(":")
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
        owner_id = await self.get_id(data["owner_telegram_id"])
        event_id  = await self.connector.fetchrow(f"SELECT id FROM events WHERE owner_id = $1", owner_id)
        event_id= event_id[0]
        return await self.connector.execute("UPDATE events SET name = $1, date = $2, info = $3, link = $4, owner_id = $5, photo_file_id = $6, place = $7, owner_info = $8 WHERE id = $9", data["name"], date, data["info"], data['link'], owner_id, data["photo_file_id"], data["place"], data["owner_info"], event_id)
    
    async def set_event_value(self, value_name, value, event_id):
        return await self.connector.execute(f"UPDATE events SET {value_name} = $1 WHERE id = $2", value, event_id)

    async def get_events(self, id=None):
        if id != None:
            return await self.connector.fetch(f"SELECT * FROM events WHERE id = $1", id)
        return await self.connector.fetch(f"SELECT * FROM events")
    
    async def get_templates(self, telegram_id):
        owner_id = await self.get_id(telegram_id=telegram_id)
        return await self.connector.fetch(f"SELECT name, value FROM templates WHERE owner_id = $1", owner_id)
    
    async def get_template_value(self, name, telegram_id):
        owner_id = await self.get_id(telegram_id=telegram_id)
        return await self.connector.fetchval(f"SELECT value FROM templates WHERE owner_id = $1 AND name = $2", owner_id, name)

    async def filter_events(self, events: list, user_id, admin_id=None) -> list:
        res_events = events
        if user_id == None:
            return []
        i = 0
        while i < len(events):
            if events[i]["date"] < datetime.datetime.now():
                await self.set_event_value("status", "stopped", events[i]['id'])\
                
            if (user_id == "all" and events[i]["status"] == 'stopped') or (user_id != "all" and user_id != events[i]["owner_id"]):
                res_events.pop(i)
            else:
                i+=1

        res_events = sorted(res_events, key=lambda x: x["date"])

        return res_events

    async def get_events_list(self, message, user_id="all"):
        events = await self.get_events()
        # admin_id = settings.ADMIN_ID
        admin_id = 1
        events = await self.filter_events(events, user_id, admin_id)
        if user_id !=  "all":
            if events == []:
                await message.answer("У вас нет мероприятий🥱", reply_markup=reply.main)
                return
        else:
            if events == []:
                await message.answer("Сейчас нет мероприятий😞", reply_markup=reply.main)
                return

        for event in events:
            basic_info = await event_txt.get_basic_info(event)
            owner_id = event["owner_id"]
            event_id = event["id"]
            photo_file_id = event["photo_file_id"]
            status = event["status"]
            if photo_file_id != None:
                if user_id != "all":
                    if status == "stopped":
                        await message.answer_photo(photo_file_id, f"🗣️Название: {event["name"]}" + f"\n\n{emoji.emojize(":CROSS MARK:")}МЕРОПРИЯТИЕ ЗАВЕРШЕНО", reply_markup=inline.get_owner_remove_inline_keyboard(event_id))
                    else:
                        await message.answer_photo(photo_file_id, basic_info, reply_markup=inline.get_owner_more_inline_keyboard(event_id))

                elif user_id == "all":
                    if status == "active":
                        await message.answer_photo(
                            photo_file_id,
                            basic_info,
                            reply_markup=inline.get_more_inline_keyboard(event_id)
                        )

            else:
                if user_id != "all":
                    if status == "stopped":
                        await message.answer(f"🗣️Название: {event["name"]}" + f"\n\n{emoji.emojize(":CROSS MARK:")}МЕРОПРИЯТИЕ ЗАВЕРШЕНО", reply_markup=inline.get_owner_remove_inline_keyboard(event_id))
                    else:
                        await message.answer(basic_info, reply_markup=inline.get_owner_more_inline_keyboard(event_id))
                elif user_id == "all":
                    if status == "active":
                        await message.answer(basic_info, reply_markup=inline.get_more_inline_keyboard(event_id))

    
    async def delete_event(self, id):
        await self.connector.fetch(f"DELETE FROM events WHERE id = $1", id)

    async def delete_template(self, name, telegram_id):
        owner_id = await self.get_id(telegram_id=telegram_id)
        try:
            await self.connector.fetch(f"DELETE FROM templates WHERE (owner_id = $1 AND name  = $2)", owner_id, name)
            return True
        except Exception as ex:
            print(ex)
            return False