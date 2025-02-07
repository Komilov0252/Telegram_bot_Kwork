from typing import List, Tuple

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_keyboard_job_button(buttons: List[Tuple[str, str]]):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text = i[0], callback_data=str(i[1])) for i in buttons])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()
async def inline_keyboard_job_button_customer(buttons: List[Tuple[str, str]]):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text = i[0], callback_data=(str(i[1])) + 'c') for i in buttons])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()
