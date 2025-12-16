from config.settings import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from pymongo import MongoClient

class mongo_db_manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(mongo_db_manager, cls).__new__(cls)
            cls._instance._client = MongoClient(MONGO_URI)
            cls._instance._db = cls._instance._client[DATABASE_NAME]
        return cls._instance
    
    def get_collection(self):
        return self._db[COLLECTION_NAME]
    

    def ping_server(self):
        try:
            self._client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Erreur de connexion MongoDB : {e}")
            return False
    
    def close_connection(self):
        self._client.close()

mongo_manager = mongo_db_manager()