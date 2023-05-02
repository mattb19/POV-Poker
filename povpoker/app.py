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
from werkzeug.security import generate_password_hash, check_password_hash

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

player4 = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0), Player("Jackson",None,None,1000,0), Player("David",None,None,1000,0), 
           Player("Ryan",None,None,1000,0), Player("Max",None,None,1000,0), Player("Ethan",None,None,1000,0), Player("Luke",None,None,1000,0)]
player = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0), Player("Jackson",None,None,1000,0), Player("David",None,None,1000,0)]
player3 = [Player("Matt",None,None,1000,0), Player("Trent",None,None,1000,0), Player("Jack",None,None,1000,0), Player("Jeremy",None,None,1000,0)]
player2 = [Player("Matt",None,None,1000,0), Player("Jeremy",None,None,1000,0)]
game = Game(0, player, 10, 20)
game2 = Game(2, player2, 10, 20)
game3 = Game(3, player3, 10, 20)
game4 = Game(4, player4, 10, 20)
game5 = Game(5, player4, 10, 20)
games = [game, game2, game3, game4, game5]
game.newRound()
game2.newRound()
game3.newRound()
game4.newRound()
game5.newRound()

# game2.placeBetFold(20)
# game2.placeBetFold(0)
# game2.placeBetFold(0)
# game2.placeBetFold(0)

# game3.placeBetFold(20)
# game3.placeBetFold(20)
# game3.placeBetFold(20)
# game3.placeBetFold(0)
# game3.placeBetFold(0)
# game3.placeBetFold(0)
# game3.placeBetFold(0)
# game3.placeBetFold(0)
# game3.placeBetFold(0)
# game3.placeBetFold(0)

# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(20)
# game4.placeBetFold(0)

# game.placeBetFold(1000)
# game.placeBetFold(1000)
# game.placeBetFold(1000)
# game.placeBetFold(1000)
# game.placeBetFold(1000)



theUser = User(1, 'LunarSleep', 'hollowknight@gmail.com', 'juul12345')
@app.route('/')
def home():
    conn = connectDB()
    cursor = int(str(conn.execute("SELECT COUNT(*) FROM User").fetchall()[0]).strip('(').strip(')').strip(','))
    val = cursor
    return render_template_modal('home.html', theUser=theUser, val=val, games=games)

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
            if i.isalnum() or i in ['!', '%', '$', '#', ':']:
                newp += i
        
        user= list(user)
        newu = ""
        for i in user:
            if i.isalnum() or i in ['!', '%', '$', '#']:
                newu += i
        
        session["name"] = loginname
        
        if newu==loginname and check_password_hash(newp, loginpassword)==True:
            session["name"] = loginname
            return "SUCCESS"
        else:
            return "User Not Found"
        
    else:
        return render_template("login.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        buy = request.form.get("buyIn")
        blinds = request.form.get("blinds")
        name = request.form.get("name")
        
        print(name, blinds, buy)

        conn = connectDB()
        id = int(str(conn.execute("SELECT COUNT(*) FROM Game").fetchall()[0]).strip('(').strip(')').strip(','))+1
        
        players = [Player(name,None,None,1000,0)]
        newGame = Game(id, players, 10, 20)
        gameJSON = newGame.json()
        gameJSON = str(gameJSON)
        
        conn.execute("INSERT INTO Game VALUES (?, ?)", (id, gameJSON))
        conn.commit()
        return str(id)
    else:
        return render_template("create.html")
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        registername = str(request.form.get("username"))
        registerpassword = str(request.form.get("password"))
        if len(registerpassword) < 8:
            return "Password too Short!"
        registerpassword = generate_password_hash(registerpassword)
        registeremail = str(request.form.get("email"))
        conn = connectDB()
        user = list(str(conn.execute("SELECT userName FROM User WHERE userName=?", (registername,)).fetchall()).strip('(').strip(')').strip(','))
        email = list(str(conn.execute("SELECT userName FROM User WHERE email=?", (registeremail,)).fetchall()).strip('(').strip(')').strip(','))
        if len(registername) < 6:
            return "Username too short!"
        elif len(registername) > 15:
            return "Username too Long!"
        elif int(len(user)) == int(2) and len(email) == int(2):
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
        id = request.form.get("id")
        print(id)
        #print(bet)
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
     
@app.route('/getGame/<int:Number>')
def getGame(Number):
    if Number == 0:
        return game.json()
    conn = connectDB()
    name = str(conn.execute("SELECT JSON FROM Game WHERE GameID=?", (str(Number),)).fetchone())
    name = name.strip('(').strip(')')
    name = name.replace("\\", "")
    name = name[1:]
    name = name[:-1]
    name = name[:-1]
    poker = convertGame(name)
    return poker.json()

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

@app.route('/table/<int:Number>')
def table(Number):
    if Number == 0:
        return render_template('table.html', game=game)
    conn = connectDB()
    name = str(conn.execute("SELECT JSON FROM Game WHERE GameID=?", (str(Number),)).fetchone())
    name = name.strip('(').strip(')')
    name = name.replace("\\", "")
    name = name[1:]
    name = name[:-1]
    name = name[:-1]
    
    poker = convertGame(name)
        
    return render_template('table.html', game=poker)

def convertGame(g):
    data = g
    print(data)
    datas = eval(data)
    players = [Player(**i) for i in datas["players"]]
    del datas["players"]
    x = Game(**datas, players=players)
    return x
