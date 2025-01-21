import json
from types import NoneType
from json import loads
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot.dispatcher import dp

class IN_employee_states(StatesGroup):
    experience = State()
    linkedin = State()
    description = State()
    cv = State()


@dp.message(F.text == 'Employee')
async def employee_handler(message: Message, state: FSMContext):
    await message.answer('nechchi yillik stajiz bor ', reply_markup = ReplyKeyboardRemove())
    await state.set_state(IN_employee_states.experience)

@dp.message(IN_employee_states.experience)
async def experience_handler(message: Message, state: FSMContext):
    try:
        await state.set_data({'experience': int(message.text)})
        await state.set_state(IN_employee_states.linkedin)
        await message.answer(" linkedin linkini yuboring")
    except ValueError:
        await state.set_state(IN_employee_states.experience)
        await message.answer(" Iltimos to`g`ri kiriting")

@dp.message(IN_employee_states.linkedin)
async def linkedin_handler(message: Message, state: FSMContext):
    try:
        await state.update_data({'linkedin': message.link_preview_options.url})
        await state.set_state(IN_employee_states.description)
        await message.answer('Description yozing')
    except (KeyError, AttributeError):
        await message.reply("likn yuborishingiz kerak")
        await state.set_state(IN_employee_states.linkedin)
@dp.message(IN_employee_states.description)
async def description_handler(message: Message, state: FSMContext):
    try:
        if message.content_type != 'text':
            raise ValueError('Message is not text')
        await state.update_data({'description': message.text})
        await state.set_state(IN_employee_states.cv)
        await message.answer(" CV yuboring ")
    except (ValueError, KeyError):
        await message.reply("description matn shaklida bo`lishi kerak")
        await state.set_state(IN_employee_states.description)

@dp.message(IN_employee_states.cv)
async def cv_handler(message: Message, state: FSMContext):
    try:
        await state.update_data({'cv': message.document.file_name})
        data = await state.get_data()
        data_str = json.dumps(data, indent = 4)
        await message.answer(f" ma`lumotlariz {data_str}")
    except (ValueError, AttributeError):
        await message.reply("CV format PDF")
        await state.set_state(IN_employee_states.cv)



