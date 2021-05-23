from functools import lru_cache
import os

class Config:

    TG_APP_ID:int
    TG_APP_HASH :str
    SESSION_STRING :str
    ADMIN_UID:int
    
    DATABASE_URL:str


    APP_NAME        = 'Movie Blog'
    APP_DESC        = 'A simple telegram indexer for movie channel'
    APP_URL         = 'https://tgflix.herokuapp.com'

    BUFFER_SIZE:int                 = 1024
    MAX_ITEMS_PER_PAGE:int          = 20
    DOWNLOAD_ENABLED:bool           = True
    MAX_SIMULTANIOUS_DOWNLOAD:int   = 20
    
    DEFAULT_COVER_IMG:int   = 1
    DEBUG:bool              = True
    
    def __init__(self):
        for i in dir( self):
            if not i.startswith('__'):
                try:
                    self.__setattr__(i, os.getenv(i,self.__getattribute__(i)))
                except:
                    raise Exception('required env variables missing')


@lru_cache()
def get_config():
	return Config()

CONFIG = get_config()