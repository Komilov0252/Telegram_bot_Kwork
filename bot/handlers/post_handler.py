from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.dispatcher import dp

class IN_POST_state(StatesGroup):
    state_title = State()
    state_description = State()
    state_file = State()
    state_deadline = State()
    state_status = State()


@dp.message(StateFilter(IN_POST_state.state_title))
async def post_title_handler(message: Message, state: FSMContext):
    await state.set_state(IN_POST_state.state_description)
    await state.set_data({'title' : message.text})
    await message.answer(" Post matnini kiriting kiriting ")

@dp.message(StateFilter(IN_POST_state.state_description))
async def post_description_handler(message: Message, state: FSMContext):
    await state.update_data({'description' : message.text})
    await state.set_state(IN_POST_state.state_file)
    await message.answer(" File yuboring ")

@dp.message(StateFilter(IN_POST_state.state_file))
async def post_file_handler(message: Message, state: FSMContext):
    try:
        await state.set_state(IN_POST_state.state_deadline)
        await state.update_data({'file' : message.document.file_id})
        await message.answer(" deadline muddatini kiriting ")
    except (AttributeError, FileNotFoundError):
        await state.set_state(IN_POST_state.state_file)
        await message.answer(" Iltimos file yuboring")

@dp.message(StateFilter(IN_POST_state.state_deadline))
async def post_deadline_handler(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d-%m-%Y")
        await state.update_data({'deadline' : deadline})
        await message.answer(f"deadline set to {deadline}")
    except ValueError:
        await message.reply("Deadline format: DD-MM-YYYY")
        await state.set_state(IN_POST_state.state_deadline)



