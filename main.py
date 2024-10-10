import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import bot_messages, user_commands, questionaire, owner_code, callback
from config_reader import config
from middlewares.dbmiddleware import DbSession
import asyncpg
from utils.commands import set_commands

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(1008265857, text="<strong>Бот запущен!</strong>")

async def stop_bot(bot: Bot):
    await bot.send_message(1008265857, text="<strong>Бот остановлен!</strong>")


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='postgres', database='eventdb', 
                                             host='127.0.0.1', port=5433, command_timeout=60)


async def main():
    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = await create_pool()
    dp = Dispatcher()
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

