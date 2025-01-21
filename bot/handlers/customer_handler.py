from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot.dispatcher import dp

from bot.handlers.post_handler import IN_POST_state



@dp.message(F.text == 'Customer')
async def Customer_handler(message: Message, state:FSMContext):
     # Customer tablega user_id sini save qilamz
     await state.set_state(IN_POST_state.state_title)
     await message.answer("Ish uchun e`lon berishingiz mumkin", reply_markup = ReplyKeyboardRemove())
     await message.answer(" Post Sarlavxasini kiriting ")

