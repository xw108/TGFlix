from sqlalchemy import  MetaData
from databases import Database
from .config import CONFIG

try:
    db = Database( CONFIG.DATABASE_URL)
except:
    raise('Invalid or missing database url')
metadata = MetaData()
