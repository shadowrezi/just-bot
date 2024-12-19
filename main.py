from time import sleep
from os import getenv, system
import sys
from asyncio import run
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from routers import (
    others,
    naurok,
    music,
)


load_dotenv()

bot_token = getenv('TG_TOKEN')


async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.include_routers(
        others.router,
        naurok.router,
        music.router
    )

    await dp.start_polling(bot)

    await bot.session.close()


if __name__ == "__main__":
    basicConfig(level=INFO, stream=sys.stdout)
    try:
        run(main())
    except KeyboardInterrupt:
        sleep(3)
        system('clear')
    except Exception as ex:
        print(ex)
