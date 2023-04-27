from flask import Flask, render_template, redirect, jsonify, request, session, url_for, Response
from flask_session import Session
from forms import *
from Game import Game
from Player import Player
from User import User
import sqlite3
import os
import cv2
import random
import json
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from flask_modals import Modal
from flask_modals import render_template_modal

app = Flask(__name__)
modal = Modal(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!'
Session(app)

#player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,7,0), Player("Ethan",None,None,1000,8,0), Player("Jack",None,None,1000,9,0)]
player = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0), Player("Jackson",None,None,1000,0), Player("David",None,None,1000,0)]
#player = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0)]
game = Game(1, player, 10, 20)
game.newRound()
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(20)
# game.placeBetFold(10)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)
# game.placeBetFold(0)


theUser = User(1, 'LunarSleep', 'hollowknight@gmail.com', 'juul12345')
@app.route('/')
def home():
    conn = connectDB()
    cursor = int(str(conn.execute("SELECT COUNT(*) FROM User").fetchall()[0]).strip('(').strip(')').strip(','))
    val = cursor
    return render_template_modal('home.html', theUser=theUser, val=val)


@app.route('/userProfile/')
def profileCard():
    return render_template(
        'userProfile.html',
        theUser = theUser,
    )

@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        pass
    return jsonify({'htmlresponse': render_template('response.html',theUser=theUser)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        loginname = str(request.form.get("username"))
        loginpassword = str(request.form.get("password"))
        
        conn = connectDB()
        user = str(conn.execute("SELECT userName FROM User WHERE userName=?", (loginname,)).fetchall()).strip('(').strip(')').strip(',')
        password = str(conn.execute("SELECT password FROM User WHERE userName=?", (loginname,)).fetchall()).strip('(').strip(')').strip(',')
        
        
        password = list(password)
        newp = ""
        for i in password:
            if i.isalnum() or i in ['!', '%', '$', '#']:
                newp += i
        
        user= list(user)
        newu = ""
        for i in user:
            if i.isalnum() or i in ['!', '%', '$', '#']:
                newu += i
        
        session["name"] = loginname
        
        
        if newu==loginname and newp==loginpassword:
            session["name"] = loginname
            return "SUCCESS"
        else:
            return "User Not Found"
        
    else:
        return render_template("login.html")
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        registername = str(request.form.get("username"))
        registerpassword = str(request.form.get("password"))
        registeremail = str(request.form.get("email"))
        conn = connectDB()
        user = list(str(conn.execute("SELECT userName FROM User WHERE userName=?", (registername,)).fetchall()).strip('(').strip(')').strip(','))
        email = list(str(conn.execute("SELECT userName FROM User WHERE email=?", (registeremail,)).fetchall()).strip('(').strip(')').strip(','))
        if int(len(user)) == int(2) and len(email) == int(2):
            session["name"] = registername
            id = int(str(conn.execute("SELECT COUNT(*) FROM User").fetchall()[0]).strip('(').strip(')').strip(','))+1
            conn.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?)", (id, registername, registerpassword, None, None, registeremail))
            conn.commit()
            print("User Added")
            return "SUCCESS"
        return "Username or Email Taken!"
    else:
        return render_template("login.html")


@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if request.method == "POST":
        bet = request.form.get("bet")
        
        if bet in ["2blind", "pottt2", "allin"]:
            return "Ignore"
        
        if bet == 'BOMB POT':
            game.setBombPot()
            return "BOMB POT"
        
        bet = int(bet)
        if bet < 0:
            bet = None
        re = game.placeBetFold(bet)
        if re != None:
            return re
        else:
            return redirect("/table")
    return redirect("/table")
    
@app.route('/getGame')
def getGame():
    return game.json()

@app.route('/test')
def test():
    return render_template('test.html')

def connectDB():
    conn = None
    try:
        conn = sqlite3.connect('temp-db.db')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/table')
def table():
    return render_template('table.html', game=game)
