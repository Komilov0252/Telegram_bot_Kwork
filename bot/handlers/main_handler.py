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
@main_router.message(MakeStates.first_name)
async def command_start(message: Message, state: FSMContext):
    await message.answer(f"Ismingizni kiriting ⬇️")
    await state.clear()
    await state.set_state(MakeStates.first_name)

@main_router.message(MakeStates.first_name)
async def save_first_name(message: Message, state: FSMContext):
    await state.update_data({"first_name": message.text})
    await state.set_state(MakeStates.last_name)
    await message.answer("Familiyangizni kiriting ⬇️")
@main_router.message(MakeStates.last_name)
async def save_last_name(message: Message, state: FSMContext):
    await state.update_data({"last_name": message.text})
    await state.set_state(MakeStates.phone_number)
    reply_markup = await reply_keyboard_button_phone()
    await message.answer("Share phone number ☎️", reply_markup = reply_markup)
@main_router.message(MakeStates.phone_number)
async def save_phone_number(message: Message, state: FSMContext):
    await state.update_data({"phone_number": message.contact.phone_number})
    await state.update_data({"user_id": message.from_user.id})
    data = await state.get_data()
    data.pop('locale')
    await User.create(**data)

@main_router.message(CommandStart())
async def command_start(message: Message):
    reply_markup = await reply_keyboard_button(['Employee 💻', 'Customer 🕴'], [2])
    await message.answer('Yo`nalishingizni tanlang ️⬇️', reply_markup = reply_markup)


