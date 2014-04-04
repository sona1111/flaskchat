#from app import app
#from app import app as socketio
from flask import Flask, render_template, flash, redirect, jsonify, send_file, request
from forms import loginForm
from flask.ext.socketio import  SocketIO, emit
from threading import Thread
import threading
import time
import pymongo
from trackUsers import trackMain

import cStringIO
import os
import shutil

fl = Flask(__name__)
fl.debug = True
fl.config['SECRET_KEY'] = 'secret!'
app = SocketIO(fl)




loggedIn = trackMain(app)
connection_string = 'www.jewellsmusicstudio.tk:12345'
connection = pymongo.MongoClient(connection_string)
database = connection.test56
msgs = database.msgs
users = database.users



def getThreadCount():
    while True:
        time.sleep(10)
        print "Active: " + str(threading.activeCount())


'''
def heartbeat_thread(user):
    global loggedIn
    while True:
        #time between checks
        time.sleep(3)
        
        loggedIn[user] = False
        app.emit('heartbeat')
                        

        #time before timeout after sanding signal       
        time.sleep(2)
        if loggedIn[user] == False:
            userLeft(user)
            break
        
'''


@fl.route('/', methods = ['GET', 'POST'])
@fl.route('/index', methods = ['GET', 'POST'])
def index():

    
    form = loginForm()
    
    
    if form.validate_on_submit():
        
        
        if (users.find({'name':form.username.data}).count()) == 1:
            user = form.username.data            
            return render_template("main.html", user = user)
            
        else:
            flash('This is not a valid username')
            return render_template("login.html", form = form)
    
    else:
    
        return render_template("login.html", form = form)
    



@app.on('connected')
def connected():
    
    emit('connected', {'users':loggedIn.getUsers()})

@app.on('joined')
def joined(user):
    
    #at some point, twisted will be implemented instead of this
    loggedIn.addUser(user)
    
    print loggedIn.getUsers()
    emit('joined', {'user':user,'users':loggedIn.getUsers()}, broadcast = True)

@app.on('sendMessage')
def add_message(message):
    
    #msgs.insert({'post':message})
    if message['data'] != 'connected':
    
        emit('update', message, broadcast=True)
        
@app.on('crazyrotate')
def crazyrotate():
    emit('crazyrotate', broadcast=True)
        
    
#used to send any data before disconnect
@app.on('preDisconnect')
def preDisconnect(user):
    pass
    #userLeft(user)

# 'disconnected' is a special event
@app.on('disconnect')
def disconnected():
    pass

Thread(target=getThreadCount).start()

