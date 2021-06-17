import tkinter as tk
from ui import Application,ListStudent,AddStudent,ListStudentPresent,ListStudentHistory

class ApplicationRoot():

    def __init__(self) -> None:
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center')
        root.title("RFID CONTROL")
        tabs = dict()
        tabs['List student'] = ListStudent
        tabs['Add Student'] = AddStudent
        tabs['List presence'] = ListStudentPresent
        tabs['History'] = ListStudentHistory
        self.app = Application(master=root,tabs=tabs)
        w = 680
        h = 480
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def start(self):
        self.app.mainloop()

    def startScanner(self):
        self.app.startScanner()


        