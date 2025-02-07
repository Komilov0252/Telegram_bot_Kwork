from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.buttons import reply_keyboard_button_phone, reply_keyboard_button
from db.models import User

main_router = Router()

class MakeStates(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    main = State()

@main_router.message(CommandStart())
@main_router.message(MakeStates.main)
@main_router.message(F.text == 'Saqlash 💾')
async def command_start(message: Message):
    reply_markup = await reply_keyboard_button(['Employee 💻', 'Customer 🕴', 'Men haqimda 🕴'], [2])
    await message.answer('Asosiy Menyu ️⬇️', reply_markup = reply_markup)


