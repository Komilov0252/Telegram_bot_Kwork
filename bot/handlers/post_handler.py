from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select

from bot.dispatcher import dp
from bot.handlers.main_handler import MakeStates
from db import DB
from db.models import Post, Customer, User, Employee


class IN_POST_state(StatesGroup):
    state_title = State()
    state_description = State()
    state_file = State()
    state_deadline = State()
    state_status = State()



@dp.message(StateFilter(IN_POST_state.state_description))
async def post_description_handler(message: Message, state: FSMContext):
    try:
        if not message.text:
            raise Exception
        await state.update_data({'title' : message.text})
        await state.set_state(IN_POST_state.state_file)
        await message.answer(" post haqida ma`lumot yozing ")
        query = (select(Customer.id).select_from(Customer)
                 .join(User, User.id == Customer.user_id)
                 .where(User.user_id == message.from_user.id))
        result = await DB.execute(query)
        result_date = result.scalars().first()
        await state.update_data({'customer_id' : result_date})
    except Exception:
        await message.answer(" Post titlini to`g`ri kiriting ")
        await state.set_state(IN_POST_state.state_description)

@dp.message(StateFilter(IN_POST_state.state_file))
async def post_file_handler(message: Message, state: FSMContext):
    try:
        await state.set_state(IN_POST_state.state_title)
        await state.update_data({'description' : message.text})
        await message.answer(" file yuboring ")
    except (AttributeError, FileNotFoundError):
        await state.set_state(IN_POST_state.state_file)
        await message.answer(" Iltimos descriptionni to`g`ri yozing")
        await state.set_state(IN_POST_state.state_file)

@dp.message(StateFilter(IN_POST_state.state_title))
async def post_title_handler(message: Message, state: FSMContext):
    try:
        await state.set_state(IN_POST_state.state_deadline)
        await state.update_data({'file' : message.document.file_id})
        await message.answer(" Deadline muaddatini kiriting ")
    except (ValueError, AttributeError):
        await message.reply("Format PDF")
        await state.set_state(IN_POST_state.state_title)

@dp.message(StateFilter(IN_POST_state.state_deadline))
async def post_deadline_handler(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d-%m-%Y")
        await state.update_data({'deadline' : deadline})
        await message.answer(f"deadline set to {deadline}")
        data = await state.get_data()
        await Post.create(title = data['title'],
                          description = data['description'],
                          file = data['file'],
                          deadline = data['deadline'],
                          customer_id = data['customer_id'])
        query = (select(User.user_id).select_from(User)
                 .join(Employee, Employee.user_id == User.id)
                 .where(Employee.job_id == data['job_id'] ))
        result = await DB.execute(query)
        result_date = result.scalars().all()

        query1 = (select(User.username).select_from(User)
                 .join(Customer, Customer.user_id == User.id)
                 .where(Customer.id == data['customer_id']))
        result1 = await DB.execute(query1)
        result_date1 = result1.scalars().first()


        for i in result_date:
            await message.bot.send_message(chat_id = int(i),text = f"""title : {data['title']}'
                                                                    \ndescription : {data['description']}'
                                                                    \ndeadline : {data['deadline']}'
                                                                   \nusername: @{result_date1}"""
                                                                        )
            await message.bot.send_document(chat_id = int(i), document = data['file'])
            await message.bot.send_message(chat_id = message.from_user.id, text = "Post yuborildi")
        await state.set_state(MakeStates.main)
    except ValueError:
        await message.reply("Deadline format: DD-MM-YYYY")
        await state.set_state(IN_POST_state.state_deadline)





