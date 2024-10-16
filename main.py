import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.handlers import bot_messages, user_commands, questionaire, owner_code, callback
from src.utils.dbconnect import Request
from src.middlewares.dbmiddleware import DbSession
import asyncpg
import time
from src.utils.commands import set_commands
import os
from dotenv import load_dotenv
    
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DB_USER = os.getenv("DB_USER")
DB_PASS= os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")



async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text="<strong>Бот запущен!</strong>")

async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text="<strong>Бот остановлен!</strong>")


# async def sql_init(request):
#     async with request.acquire() as connect:
#         await connect.execute("""CREATE TABLE events(
#                               id serial PRIMARY KEY,
#                               name TEXT, 
#                               date DATETIME, 
#                               info TEXT, 
#                               link TEXT, 
#                               owner_id INT, 
#                               photo_file_id TEXT, 
#                               place TEXT, 
#                               owner_info TEXT, 
#                               status TEXT""")



async def create_pool():
    conn = await asyncpg.create_pool(user=DB_USER, password=DB_PASS, database=DB_NAME, host=DB_HOST, port=DB_PORT, command_timeout=60)
    return conn


async def main():
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = await create_pool()
    dp = Dispatcher()
    # request = pool_connect
    # await sql_init(request)
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(
        user_commands.router,
        questionaire.router,
        callback.router,
        owner_code.router,
        bot_messages.router,
        
    )
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
