from database.db import DB
from database.student import Student
import serial
import time
import _thread as thread

class RDFIDReader(object):

    def __init__(self,port,baudrate=9600):
        self.port = port
        self.baudrate = baudrate


    def scan(self,messagebox,save):
        rfid_uuid = self.serial.readline().decode().rstrip()
        if rfid_uuid is not  None and rfid_uuid != "" :
            sdt = Student(DB())
            isFound = sdt.processRFID(rfid_uuid)
            if isFound:
                data = sdt.toJson()
                message = data['name']+" "+ data['lastname'] +" "+ data['classe'] + " was passed with RFID  : " + data['rfid'] 
                # if messagebox : thread.start_new_thread(messagebox.showinfo,("NEW STUDENT PASS",message,))
                if save : thread.start_new_thread(save,())
            elif messagebox:
                # thread.start_new_thread(messagebox.showwarning,("NEW STUDENT PASS","Unkown card  "+rfid_uuid+" passed ",))4
                pass
        
        return  rfid_uuid
    
    def send(self, data:str):
        if(self.serial.isOpen):
            self.serial.write(str(data).encode())
        else :
            print("Port not openning")

    def start(self,messagebox=None,save=None):
        self.serial = serial.Serial(self.port,self.baudrate)
        while True :
            rfid = self.scan(messagebox,save)
            time.sleep(.1)