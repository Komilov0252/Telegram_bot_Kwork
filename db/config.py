from utils.Conf import CF

class Config:
    DB_NAME = CF.db.DBNAME
    DB_USER = CF.db.USERNAME
    DB_PASSWORD = CF.db.PASSWORD
    DB_HOST = CF.db.HOST
    DB_PORT = CF.db.PORT
    DB_CONFIG = f"postgresql+asyncpg://postgres:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"