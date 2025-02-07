from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from bot.buttons import reply_keyboard_button_phone
from bot.handlers.main_handler import MakeStates
from db import DB
from db.models import User, Employee, Job, Subjob

personal_router = Router()

@personal_router.message(F.text == 'Men haqimda 🕴')
async def about_me_handler(message: Message):
    query = (select(Employee.id).select_from(Employee)
                   .join(User, User.id == Employee.user_id)
                   .where(User.user_id == message.from_user.id))
    result = await DB.execute(query)
    employee_id = result.scalars().first()
    if employee_id:
        query = (select(User.first_name, User.last_name, User.phone_number,
                        Employee.job_id, Employee.experience, Employee.linkedin,
                        Employee.CV, Job.name, Job.id).select_from(User)
                 .join(Employee, User.id == Employee.user_id)
                 .join(Job, Job.id == Employee.job_id)
                 .where(User.user_id == message.from_user.id))
        result = await DB.execute(query)
        result_data = result.mappings().first()
        job_id = result_data['job_id']
        query2 = (select(Subjob.name).select_from(Subjob)
                  .where(Subjob.job_id == job_id))
        result = await DB.execute(query2)
        names = result.scalars().all()


        await message.answer(text = f"Ismingiz : {result_data['first_name']} {result_data['last_name']}!\n"
                                    f"Tajribangiz :  {result_data['experience']}\n"
                                    f"telefon raqamingiz : {result_data['phone_number']}\n"
                                    f"Yo`nalishingiz : {result_data['name']}\n"
                                    f"ko`nikmalaringiz : {names}\n"
                                    f"Linkedin :  {result_data['linkedin']}\n")
        await message.bot.send_document(chat_id = message.chat.id, document = f"{result_data['CV']}")


@personal_router.message(MakeStates.first_name)
async def command_start(message: Message, state: FSMContext):
    await message.answer(f"Ismingizni kiriting ⬇️")
    await state.clear()
    await state.set_state(MakeStates.first_name)

@personal_router.message(MakeStates.first_name)
async def save_first_name(message: Message, state: FSMContext):
    await state.update_data({"first_name": message.text})
    await state.set_state(MakeStates.last_name)
    await message.answer("Familiyangizni kiriting ⬇️")
@personal_router.message(MakeStates.last_name)
async def save_last_name(message: Message, state: FSMContext):
    await state.update_data({"last_name": message.text})
    await state.set_state(MakeStates.phone_number)
    reply_markup = await reply_keyboard_button_phone()
    await message.answer("Share phone number ☎️", reply_markup = reply_markup)
@personal_router.message(MakeStates.phone_number)
async def save_phone_number(message: Message, state: FSMContext):
    await state.update_data({"phone_number": message.contact.phone_number})
    await state.update_data({"user_id": message.from_user.id})
    data = await state.get_data()
    data.pop('locale')
    await User.create(**data)