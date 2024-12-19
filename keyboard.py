from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


async def start_kb():
    kbs = [[]]
    return InlineKeyboardMarkup(inline_keyboard=kbs)
