from threading import Thread
import time

class trackMain(object):
    
    def __init__(self, app):
        self.loggedIn = {}
        self.socket = app
        self.checkTime = 3
        self.timeoutThreshhold = 2
        @app.on('heartbeat')
        def heartbeat(name):
            self.loggedIn[name] = True
    
    
    def addUser(self, user):
        
        Thread(target=self.heartbeat_thread, args=(user,)).start()
        self.loggedIn[user] = True 
        
    def heartbeat_thread(self, user):
    
        while True:
            #time between checks
            time.sleep(self.checkTime)
            
            self.loggedIn[user] = False
            self.socket.emit('heartbeat')
                            

            #time before timeout after sanding signal       
            time.sleep(self.timeoutThreshhold)
            if self.loggedIn[user] == False:
                self.userLeft(user)
                break
                
    def userLeft(self, user):  
        
        del self.loggedIn[user]
        self.socket.emit('left', {'user':user,'users':self.getUsers()})   
        
    def getUsers(self):
        return self.loggedIn.keys()
        
    
