from root import ApplicationRoot
import _thread as thread
if __name__ == "__main__": 
    app = ApplicationRoot()
    thread.start_new_thread(app.startScanner,())
    app.start()
   
    
