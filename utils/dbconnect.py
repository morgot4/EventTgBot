import asyncpg
import datetime
from keyboards import inline, reply
from config_reader import config
from utils.event_text_formater import EventTextFormater

event_txt = EventTextFormater()


class Request:
    def __init__(self, connector: asyncpg.pool.Pool) -> None:
        self.connector = connector


    async def get_id(self, telegram_id):
        return await self.connector.fetch("SELECT id FROM owners WHERE telegram_id = $1", telegram_id)
    
    async def is_owner(self, telegram_id):
        if await self.connector.fetch("SELECT FROM owners WHERE telegram_id = $1", telegram_id)  != []:
            return True
        return False
    
    async def add_owner(self, telegram_id):
        return await self.connector.execute(f"INSERT INTO owners (telegram_id) VALUES ({telegram_id})")
    
    async def add_event(self, data):
        date = data["date"].split(".")
        time = data["time"].split(":")
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
        owner_id = await self.connector.fetchrow(f"SELECT id FROM owners WHERE telegram_id = $1", data["owner_telegram_id"])
        return await self.connector.execute("INSERT INTO events(name, date, info, link, owner_id, photo_file_id, place, owner_info) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", data["name"], date, data["info"], data['link'], owner_id["id"], data["photo_file_id"], data["place"], data["owner_info"])
    
    async def set_event(self, data):
        date = data["date"].split(".")
        time = data["time"].split(":")
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
        owner_id = await self.get_id(data["owner_telegram_id"])
        event_id  = await self.connector.fetchrow(f"SELECT id FROM events WHERE owner_id = $1", owner_id[0]["id"])
        event_id= event_id[0]
        return await self.connector.execute("UPDATE events SET name = $1, date = $2, info = $3, link = $4, owner_id = $5, photo_file_id = $6, place = $7, owner_info = $8 WHERE id = $9", data["name"], date, data["info"], data['link'], owner_id[0]["id"], data["photo_file_id"], data["place"], data["owner_info"], event_id)

    async def get_events(self, id=None):
        if id != None:
            return await self.connector.fetch(f"SELECT * FROM events WHERE id = $1", id)
        return await self.connector.fetch(f"SELECT * FROM events")

    async def get_events_list(self, message, user_id=None):
        events = await self.get_events()
        if user_id !=  None:
            if events == [] or user_id == []:
                await message.answer("У вас нет мероприятий🥱", reply_markup=reply.main)
                return
        elif events == []:
            await message.answer("Сейчас нет мероприятий😞", reply_markup=reply.main)
            return
        if user_id != None:
            user_id = user_id[0]["id"]
        for event in events:
            basic_info = await event_txt.get_basic_info(event)
            owner_id = event["owner_id"]
            event_id = event["id"]
            photo_file_id = event["photo_file_id"]
            admin_id = config.admin_id.get_secret_value()
            if photo_file_id != None:
                if user_id != None and (user_id == owner_id or int(message.from_user.id) == int(admin_id)):
                    await message.answer_photo(
                        photo_file_id,
                        basic_info,
                        reply_markup=inline.get_owner_more_inline_keyboard(event_id)
                    )
                elif user_id == None:
                    await message.answer_photo(
                        photo_file_id,
                        basic_info,
                        reply_markup=inline.get_more_inline_keyboard(event_id)
                    )

            else:
                if user_id != None and (user_id == owner_id or user_id == config.admin_id.get_secret_value()):
                    await message.answer(basic_info, reply_markup=inline.get_owner_more_inline_keyboard(event_id))
                elif user_id == None:
                    await message.answer(basic_info, reply_markup=inline.get_more_inline_keyboard(event_id))
    
    async def delete_event(self, id):
        await self.connector.fetch(f"DELETE FROM events WHERE id = $1", id)