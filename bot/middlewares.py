from typing import Dict, Callable, Awaitable, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from sqlalchemy import select
from sqlalchemy.event import dispatcher

from bot.handlers.main_handler import MakeStates
from db import DB
from db.models import User, Employee


class SaveUserMiddleware(BaseMiddleware):
    async def __call__(self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        message_user = data.get("event_from_user")
        user = await User.get_by_user_id(id_ = message_user.id)
        if not user:
            await User.create(first_name = message_user.first_name, last_name = message_user.last_name  , user_id = message_user.id, username = message_user.username)
        return await handler(event, data)

class SaveEmployeeMiddleware(BaseMiddleware):
    async def __call__(self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        message_user = data.get("event_from_user")
        employee = await Employee.get_by_user_id(id_ = message_user.id)
        # if not employee:
        #     await Employee.create()
        return await handler(event, data)

async def all_middleware(dp: Dispatcher, i18n):
    dp.update.middleware(FSMI18nMiddleware(i18n))
    dp.update.outer_middleware(SaveUserMiddleware())
