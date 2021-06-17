from datetime import datetime
from typing import Text
from database.present import Present
from database.history import History
import tkinter as tk
import serial.tools.list_ports
from tkinter import messagebox
from tkinter.ttk import *
from database.student import Student
from database.db import DB
from rfid import RDFIDReader

class TkTable(tk.Frame):

    def __init__(self, parent, rows=10, columns=2,data=[],edit=None,delete=None):
        tk.Frame.__init__(self, parent,)
        self._widgets = []
        width = int(90/(columns+2))
        for row in range(rows):
            current_row = []
            for column in range(columns):
                
                label = tk.Label(self, text="%s/%s" % (row, column), borderwidth=0, width=width)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            if row != 0 :
                if edit :
                    editBtn = tk.Button(self, text="Edit", fg="white", bg="blue", command = lambda: edit(data[row-1]))
                    editBtn.grid(row=row, column=column+1, sticky="nsew", padx=1, pady=1)
                    current_row.append(editBtn)
                if delete:
                    delBtn = tk.Button(self, text="Supprimer", fg="white",  bg="red",command = lambda:delete(data[row-1]['_id']))
                    delBtn.grid(row=row, column=column+2, sticky="nsew", padx=1, pady=1)
                    current_row.append(delBtn)
            else :
                if edit or delete:
                    label = tk.Label(self, text="Action", borderwidth=0, width=width)
                    label.grid(row=row, column=column+1, sticky="nsew", padx=1, pady=1,columnspan=2)
                    current_row.append(label)

            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
            self.grid_rowconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

class ListStudent(Frame):

    def __init__(self, master=None,id=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.id=None
        self.pack(fill="both", expand=True, padx=20, pady=20)
        # self.place(in_=master, anchor="c", relx=.5, rely=.5)
        self.student = Student(DB())
        self.allStudent = self.student.getAll()

        self.create_widgets()

    def create_widgets(self):
        self.t = TkTable(self, len(self.allStudent)+1,5,self.allStudent,self.edit,self.delete)
        self.t.place(in_=self,relx=.02, rely=.02)
        self.t.set(0,0,"Name")
        self.t.set(0,1,"Lastname")
        self.t.set(0,2,"Grade")
        self.t.set(0,3,"Matricule")
        self.t.set(0,4,"RFID")
        row = 1 
        for std in self.allStudent:
            self.t.set(row,0,std['name'])
            self.t.set(row,1,std['lastname'])
            self.t.set(row,2,std['classe'])
            self.t.set(row,3,std['matricule'])
            self.t.set(row,4,std['rfid'])
            row += 1 
    
    def delete(self,id):
        self.student.collection.delete_one({"_id":id})
        self.allStudent = self.student.getAll()
        self.t.destroy()
        self.create_widgets()
        self.master.update()

    def edit(self,row):
       self.master.edit(row)


class ListStudentPresent(Frame):

    def __init__(self, master=None,id=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.id = id
        self.presence = Present(DB())
        self.allPresence = self.presence.getAll()
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.t = TkTable(self, len(self.allPresence)+1,6, self.allPresence,delete=self.delete)
        self.t.place(in_=self,relx=.02, rely=.02)
        self.t.set(0,1,"Date")
        self.t.set(0,1,"Name")
        self.t.set(0,2,"Lastname")
        self.t.set(0,3,"Grade")
        self.t.set(0,4,"Matricule")
        self.t.set(0,5,"RFID")
        row = 1 
        for pt in self.allPresence:
            std = pt['student']
            self.t.set(row,0,pt['date'])
            self.t.set(row,1,std['name'])
            self.t.set(row,2,std['lastname'])
            self.t.set(row,3,std['classe'])
            self.t.set(row,4,std['matricule'])
            self.t.set(row,5,std['rfid'])
            row += 1 
    def delete(self,id):
        self.presence.collection.delete_one({"_id":id})
        self.allPresence = self.presence.getAll()
        self.t.destroy()
        self.create_widgets()
        self.master.update()

class ListStudentHistory(Frame):

    def __init__(self, master=None,id=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.id = id
        self.history = History(DB())
        self.allhistory = self.history.getAll()
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.t = TkTable(self, len(self.allhistory)+1,7, self.allhistory,delete=self.delete)
        self.t.place(in_=self,relx=.02, rely=.02)
        self.t.set(0,0,"Date")
        self.t.set(0,1,"Name")
        self.t.set(0,2,"Lastname")
        self.t.set(0,3,"Grade")
        self.t.set(0,4,"Matricule")
        self.t.set(0,5,"RFID")
        self.t.set(0,6,"Position")
        row = 1 
        for pt in self.allhistory:
            std = pt['student']
            self.t.set(row,0,pt['date'])
            self.t.set(row,1,std['name'])
            self.t.set(row,2,std['lastname'])
            self.t.set(row,3,std['classe'])
            self.t.set(row,4,std['matricule'])
            self.t.set(row,5,std['rfid'])
            self.t.set(row,6, "IN" if int(pt['mode']) == 1 else "OUT")
            row += 1 
    
    def delete(self,id):
        self.history.collection.delete_one({"_id":id})
        self.allhistory = self.history.getAll()
        self.t.destroy()
        self.create_widgets()
        self.master.update()

class AddStudent(Frame):

    def __init__(self, master=None,id=None,row=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.row = row
        self.id = id
        # self.pack(fill="both", expand=True, padx=20, pady=20)
        self.place(in_=self.master, anchor="c", relx=.5, rely=.5)
        self.create_widgets()

    def create_widgets(self):
        l1 = tk.Label(self, text = "Name:")
        l2 = tk.Label(self, text = "Lastname:")
        l3 = tk.Label(self, text = "Grade:")
        l4 = tk.Label(self, text = "Matricule:")
        l5 = tk.Label(self, text = "RFID:")
        l1.grid(row = 1, column = 0, sticky = tk.W, pady = (5,5))
        l2.grid(row = 2, column = 0, sticky = tk.W, pady = (5,5))
        l3.grid(row = 3, column = 0, sticky = tk.W, pady = (5,5))
        l4.grid(row = 4, column = 0, sticky = tk.W, pady = (5,5))
        l5.grid(row = 5, column = 0, sticky = tk.W, pady = (5,5))
        self.entry_name = Entry(self)
        self.entry_lastname = Entry(self)
        self.entry_grade = Entry(self)
        self.entry_matricule = Entry(self)
        self.entry_rfid = Entry(self)
        self.entry_name.grid(row = 1, column = 1, pady =  (5,5))
        self.entry_lastname.grid(row = 2, column = 1, pady =  (5,5))
        self.entry_grade.grid(row = 3, column = 1, pady =  (5,5))
        self.entry_matricule.grid(row = 4, column = 1, pady =  (5,5))
        self.entry_rfid.grid(row = 5, column = 1, pady =  (5,5))
        if self.row :
            self.entry_name.insert(0,self.row['name'])
            self.entry_lastname.insert(0,self.row['lastname'])
            self.entry_grade.insert(0,self.row['classe'])
            self.entry_matricule.insert(0,self.row['matricule'])
            self.entry_rfid.insert(0,self.row['rfid'])


        self.btnSave = tk.Button(self, text="Save", fg="blue", command=self.save)
        self.btnSave.grid(row = 6, column = 1,  columnspan=2,pady = 2)

    def save(self):
        self.name = self.entry_name.get()
        self.lastname = self.entry_lastname.get()
        self.grade = self.entry_grade.get()
        self.matricule = self.entry_matricule.get()
        self.rfid = self.entry_rfid.get()
        if self.verify():
            student = Student(DB(),name=self.name,lastname=self.lastname,classe=self.grade,matricule=self.matricule,rfid=self.rfid)
            if self.row :
                student.update(self.row['_id'])
            else:
                student.save()
            self.resetEntry()
            messagebox.showinfo(title="ADD STUDENT", message="Student added successfully")
        else :
            messagebox.showerror(title="ADD STUDENT", message="Student added error, Please, Verify the information")
        
        self.master.save()

    def resetEntry(self):
        self.entry_name.delete(0, 'end')
        self.entry_lastname.delete(0, 'end')
        self.entry_matricule.delete(0, 'end')
        self.entry_rfid.delete(0, 'end')
        self.entry_grade.delete(0, 'end')
            

    def verify(self):
        return self.name != "" and self.lastname != "" and self.grade != "" and self.matricule != "" and self.isValidRifd()

    def isValidRifd(self):
        rfidInfo = self.rfid.split(' ')
        if len(rfidInfo) == 4 :
            isOk = False
            if len(rfidInfo[0]) == 2 and len(rfidInfo[1]) == 2 and len(rfidInfo[2]) == 2 and len(rfidInfo[3]) == 2 :
                isOk = True
            else:
                isOk = False
            return isOk
        return False

    
class Application(Notebook):

    def __init__(self, master=None,tabs=[]):
        super().__init__(master)
        self.master = master
        self.tabus = tabs
        self.pack(expand = 1, fill ="both")
        self.isEdit = False
        self.bind('<<NotebookTabChanged>>', self.on_tab_change)
        for title,tab in tabs.items():
            self.add(tab(self,title,width=200,),text=title)

    def save(self):
        for child in self.winfo_children():
            child.destroy()
        for title,tab in self.tabus.items():
            self.add(tab(self,title,width=200,),text=title)

    def edit(self,row):
        for child in self.winfo_children():
            child.destroy()
        for title,tab in self.tabus.items():
            if title == "Add Student":
                title = "Edit Student"
                self.add(tab(self,title,row=row,width=200,),text=title)
            else:
                self.add(tab(self,title,width=200,),text=title) 
        for tb in self.tabs():
            if 'addstudent' in tb :
                self.select(tb)
                self.isEdit = True

    def updateHistory(self):
        for child in self.winfo_children():
            if  "presen" in str(child):
                child.destroy()
            elif "history" in str(child):
                child.destroy()
        self.add(self.tabus['List presence'](self,"List presence",width=200),text="List presence")
        self.add(self.tabus['History'](self,"History",width=200),text="History")
        


    def  on_tab_change(self,event):
        if 'addstudent' not in self.select() and self.isEdit:
            for child in self.winfo_children():
                child.destroy()
            for title,tab in self.tabus.items():
                self.add(tab(self,title,width=200,),text=title)
            self.isEdit = False

    def startScanner(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) != 0 :
            port = ports[0].name
            rfidreader = RDFIDReader(port)
            rfidreader.start(messagebox,self.updateHistory)
                
            


            



        

