from bot.dispatcher import dp
from bot.handlers.customer_handler import customer_router
from bot.handlers.employee_handler import employee_router
from bot.handlers.main_handler import main_router
from bot.handlers.personal_handler import personal_router

dp.include_routers(*[main_router,
                     personal_router,
                     employee_router,
                     customer_router])