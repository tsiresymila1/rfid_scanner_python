

from database.history import History
from database.present import Present
from datetime import datetime
from database.db import DB


class Student(DB):

    def __init__(self, database : DB,name="",lastname="",classe="",matricule="",rfid=""):
        self.name = name
        self.id = None;
        self.lastname = lastname
        self.classe = classe
        self.matricule = matricule
        self.rfid = rfid
        self.database = database
        self.collection = database.db['student']

    def create(self, json_data):
        self.id = json_data['_id']
        self.name = json_data['name']
        self.lastname = json_data['lastname']
        self.classe = json_data['classe']
        self.matricule = json_data['matricule']
        self.rfid = json_data['rfid']

    def save(self):
        self.collection.save(self.toJson())

    def update(self,id):
        self.collection.update_one({'_id': id}, {'$set': self.toJson()})
    
    def processRFID(self,rfid):
        data = self.collection.find_one({'rfid': rfid})
        if data is not None:
            self.create(data)
            isPresent = self.database.db['present'].find_one({"student": self.toJson(),"date":datetime.today().strftime("%d-%m-%Y")})
            if not isPresent :
                present = Present(self.database,self)
                mode = 1
                present.save()
            else:
                mode = 0 
                cursor = self.database.db['history'].find({"student":self.toJson()}).sort([('date', -1)]).limit(1)
                for el in cursor:
                    if int (el['mode']) == 0 :
                        mode = 1 
            history = History(self.database,self,mode)
            history.save()
            return True
        return False

    def getPresent(self):
        data = self.database.db['present'].find({"student": self.toJson()})

    def getHistory(self):
        data = self.database.db['history'].find({"student": self.toJson()})

    def getAll(self):
        return list(self.collection.find())

    def toJson(self):
        if self.id is not None :
            return {
                "_id" : self.id,
                "name" : self.name,
                "lastname" : self.lastname,
                "classe" : self.classe,
                "matricule" : self.matricule,
                "rfid" : self.rfid
            }
        else :
            return {
                "name" : self.name,
                "lastname" : self.lastname,
                "classe" : self.classe,
                "matricule" : self.matricule,
                "rfid" : self.rfid
            }
              

