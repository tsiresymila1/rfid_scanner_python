import pymongo

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DB():

    __metaclass__ = Singleton

    def __init__(self,host="localhost",port=27017):
        self.client = pymongo.MongoClient(host,port,username='root',password='toor')
        self.db = self.client['rfid']

    def create(self, json_data):

        pass