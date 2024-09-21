import asyncio, random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Hello, <b>{message.from_user.first_name}</b>.")

@dp.message(Command(commands=["rn", "random_numbers"]))
async def get_random_number(message: Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split("-")]
    rnum = random.randint(a, b)
    await message.reply(f"Random number: {rnum}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

