from os import getenv
from dotenv import load_dotenv

from utils.path import PATH_ENV

load_dotenv(PATH_ENV)

class BotConf:
    TOKEN = getenv("TOKEN")

class DBConf:
    DBNAME = getenv("DBNAME")
    USERNAME = getenv("USERNAME")
    PASSWORD = getenv("PASSWORD")
    HOST = getenv("HOST")
    PORT = getenv("PORT")

class WebConf:
    ADMIN_USERNAME = getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

class PaymentConf:
    PAY_APP = getenv("PAY_APP")
    PAY_TOKEN = getenv("PAY_TOKEN")

class CF:
    db = DBConf()
    bot = BotConf()
    web = WebConf()
    pay = PaymentConf()

