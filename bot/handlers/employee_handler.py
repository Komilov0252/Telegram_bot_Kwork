import json
from types import NoneType
from json import loads
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
from sqlalchemy import select, insert

from bot.buttons import inline_keyboard_job_button, reply_keyboard_button
from bot.dispatcher import dp
from db import DB
from db.models import Employee, Job, Subjob, SubjobEmployee, User

employee_router = Router()
class IN_employee_states(StatesGroup):
    experience = State()
    linkedin = State()
    job = State()
    subjob = State()
    cv = State()


@employee_router.message(F.text == 'Employee 💻')
@employee_router.message(F.text == 'qaytadan boshlash ⬅️')
async def employee_handler(message: Message, state: FSMContext):
    if message.text in [ 'qaytadan boshlash ⬅️']:
        user_id = message.from_user.id
        employee_id = await Employee.get_employee_id_by_user_id(user_id)
        await Employee.delete(employee_id[0])
    try:
        id =  await Employee.get_user_id(message.from_user.id)
        if id is not None:
            raise Exception
        await message.answer('namuna: 8 yil')
        await message.answer('Yillik tajribangizni kiriting: ⬇️', reply_markup = ReplyKeyboardRemove())
        await state.set_state(IN_employee_states.experience)
    except Exception:
        rkb = await reply_keyboard_button(['Davom ettirish ➡️', 'qaytadan boshlash ⬅️'], [2])
        await message.answer(text = 'tanlang', reply_markup=rkb)
        await state.set_state(IN_employee_states.subjob)

@employee_router.message(IN_employee_states.experience)
async def experience_handler(message: Message, state: FSMContext):
    try:
        await state.set_data({'experience': message.text})
        await state.set_state(IN_employee_states.cv)
        await message.answer(" Resumeingizni (CV) yuboring ⬇️")
    except ValueError:
        await state.set_state(IN_employee_states.experience)
        await message.answer(" text bolishi kerak")

@employee_router.message(IN_employee_states.cv)
async def cv_handler(message: Message, state: FSMContext):
    try:
        await state.update_data({'cv': message.document.file_id})
        await state.update_data({'user_id': message.from_user.id})
        data = await state.get_data()
        await state.set_state(IN_employee_states.linkedin)
        await message.answer(" Linkedin linkini yuboring ⬇️")
    except (ValueError, AttributeError):
        await message.reply("Format PDF")
        await state.set_state(IN_employee_states.cv)

@employee_router.message(IN_employee_states.linkedin)
async def linkedin_handler(message: Message, state: FSMContext):
    try:
        if  not message.text.startswith('https://'):
            raise KeyError
        await state.update_data({'linkedin': message.text})
        data = await Job.get_name_id()
        button =data.copy()
        ikb = await inline_keyboard_job_button(button)
        await message.answer('Yo`nalishlardan birini tanlang ⬇️', reply_markup = ikb)
    except (KeyError, AttributeError):
        await message.reply("link yuborishingiz kerak ⬇")
        await state.set_state(IN_employee_states.linkedin)


@employee_router.callback_query(lambda c: c.data in ['1', '2', '3'])
async def callback_data_handler(callback_query: CallbackQuery, state: FSMContext):
    callback_data = callback_query.data
    await callback_query.answer(text = 'Muaffaqiyatli saqlandi')
    job_id = int(callback_data)
    await state.update_data({'job_id': job_id})
    data = await state.get_data()
    user_id = await User.get_by_user_id(data['user_id'])
    data_str = json.dumps(data, indent=4)
    await Employee.create(experience=data['experience'],
                          linkedin=data['linkedin'],
                          user_id=user_id[0],
                          rating='5',
                          CV=data['cv'],
                          job_id = job_id)

    rkb = await reply_keyboard_button(['Davom ettirish ➡️'], [1])
    await callback_query.message.answer(text = 'Davom ettirish ➡️', reply_markup = rkb)
    await state.set_state(IN_employee_states.subjob)

@employee_router.message(IN_employee_states.subjob)
async def subjob_handler(message: Message, state: FSMContext):

    global name, job_id
    if message.text in [ 'Davom ettirish ➡️'] :
        query =(select(Employee.job_id).select_from(Employee)
                .join(User, Employee.user_id == User.id)
                .where(User.user_id == message.from_user.id)
        )
        result = await DB.execute(query)
        job_id = result.scalar()
        query2 = (select(Subjob.name).select_from(Subjob)
                  .where(Subjob.job_id == job_id))
        result2 = await DB.execute(query2)
        name = result2.scalars().all()
        name.append('Saqlash 💾')
        rkb = await reply_keyboard_button(name, [2])
        await message.answer(text = 'biladigan skillarizni tanlang', reply_markup = rkb)

    if  not message.text == 'Saqlash 💾':
        query3 = (select(Subjob.id).select_from(Subjob)
                 .where(Subjob.name == message.text))
        result3 = await DB.execute(query3)
        subjob_id = result3.scalars().first()

        query4 = (select(Employee.id).select_from(Employee)
                  .where(Employee.job_id == job_id))
        result4 = await DB.execute(query4)
        employee_id = result4.scalars().first()

        await SubjobEmployee.create(
            employee_id = employee_id,
            subjob_id = subjob_id
        )
        name.remove(message.text)

        rkb = await reply_keyboard_button(name, [3])
        await message.answer(text = f'{message.text} muaffaqiyatli saqlandi')
        await message.answer(text = 'davom etish uchun Keyingi tugmasini bosing', reply_markup = rkb)
        await state.set_state(IN_employee_states.subjob)








