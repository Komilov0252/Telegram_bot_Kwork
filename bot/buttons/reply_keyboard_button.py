from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def reply_keyboard_button(buttons : list, adjust: list):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        *[KeyboardButton(text = i) for i in buttons ]
    )
    rkb.adjust(*adjust)
    return rkb.as_markup(resize_keyboard=True)
async def reply_keyboard_button_phone():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text='Share phone number', request_contact=True)
    )
    return rkb.as_markup(resize_keyboard=True)
