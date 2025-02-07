from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select

from bot.buttons import inline_keyboard_job_button, inline_keyboard_job_button_customer
from bot.dispatcher import dp

from bot.handlers.post_handler import IN_POST_state
from db import DB
from db.models import Customer, User, Job, Post

customer_router = Router()

@customer_router.message(F.text == 'Customer 🕴')
async def Customer_handler(message: Message, state:FSMContext):
     # Customer tablega user_id sini save qilamz
     query = (select(Customer.id).select_from(Customer)
              .join(User, User.id == Customer.user_id)
              .where(User.user_id == message.from_user.id))
     result = await DB.execute(query)
     result_date = result.scalars().first()
     if not result_date:
          query = (select(User.id)
                   .where(User.user_id == message.from_user.id))
          result = await DB.execute(query)
          user_id = result.scalars().first()
          await Customer.create(user_id = user_id)
     data = await Job.get_name_id()
     button = data.copy()
     ikb = await inline_keyboard_job_button_customer(button)
     await message.answer(text='E`lon uchun yo`nalish tanlasng', reply_markup= ikb)
@customer_router.callback_query(lambda c: c.data in ['1c', '2c', '3c'])
async def Customer_data_callback(callback_query: CallbackQuery, state: FSMContext):
     callback_data = callback_query.data
     job_id = int(callback_data[0])
     await state.set_data({'job_id': job_id})
     await callback_query.answer(text = ' ')
     await callback_query.message.answer(text = 'titleni kiriting 🗒')
     await state.set_state(IN_POST_state.state_description)

