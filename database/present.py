
from datetime import datetime

class Present():

    def __init__(self, database, student=None,date=datetime.today()):
        self.student = student
        self.id = None
        self.date = date
        self.databse = database
        self.collection = database.db['present']
        self.mode = 1


    def save(self):
        self.collection.save(self.toJson())
    
    def getAll(self):
        return list(self.collection.find())
    
    def toJson(self):
        if self.id is not None :
            return {
                "_id" : self.id,
                "student" : self.student.toJson(),
                "date" : self.date.strftime('%d-%m-%Y'),
            }  
        else :
            return {
                "student" : self.student.toJson(),
                "date" : self.date.strftime('%d-%m-%Y'),
            }    