from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands='start', prefix='/'))
async def start(message: Message):
    await message.answer(
        'Welcome, do You need help? (/commands for list of all commands)',
    )


@router.message(
    Command(commands='commands')
)
async def commands(message: Message):
    await message.answer(
        'Commands:\n'
        '/naurok (link or code)\n'
    )
