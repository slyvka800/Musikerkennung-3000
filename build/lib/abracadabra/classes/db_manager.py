from tinydb import TinyDB

class DataBaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataBaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, 'db'):
            self.db = TinyDB("music_hashes.json")
        if not hasattr(self, 'table'):
            self.table = self.db.table("hashes")

    def insert(self, data):
        self.table.insert(data)
    
    def get(self, query):
        return self.table.search(query)
    
    def update(self, query, data):
        self.table.update(data, query)

    def delete(self, query):
        self.table.remove(query)

