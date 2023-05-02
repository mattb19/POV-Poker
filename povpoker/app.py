from flask import Flask, render_template, redirect, jsonify, request, session, url_for, Response
from flask_session import Session
from forms import *
from Game import Game
from Player import Player
from User import User
import time
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
game1 = Game(0, player, 10, 20)
# game2 = Game(2, player2, 10, 20)
# game3 = Game(3, player3, 10, 20)
# game4 = Game(4, player4, 10, 20)
# game5 = Game(5, player4, 10, 20)
games = [game1]
game1.newRound()
# game2.newRound()
# game3.newRound()
# game4.newRound()
# game5.newRound()



@app.route('/reset', methods=["POST", "GET"])
def reset():
    if request.method == 'POST':
        if request.form.get("data") != "admin":
            return "ERROR"
        conn = connectDB()
        conn.execute("DELETE FROM Game")
        conn.commit()
        return 'SUCCESS'
    else:
        return redirect(url_for('home'))


theUser = User(1, 'LunarSleep', 'hollowknight@gmail.com', 'juul12345')
@app.route('/')
def home():
    try:
        s = session["name"]
    except:
        return redirect(url_for("login"))
    games = []
    conn = connectDB()
    test = int(str(conn.execute("SELECT COUNT(*) FROM Game").fetchall()[0]).strip('(').strip(')').strip(','))
    for i in range(test):
        id = str(conn.execute("SELECT GameID FROM Game").fetchall()[i]).strip('(').strip(')').strip(',')
        game = str(conn.execute("SELECT JSON FROM Game WHERE GameID=?", (id,)).fetchone())
        game = game.strip('(').strip(')')
        game = game.replace("\\", "")
        game = game[1:]
        game = game[:-1]
        game = game[:-1]
        games.append(convertGame(game))
    cursor = str(conn.execute("SELECT GameID FROM Game").fetchall()).strip('(').strip(')').strip(',')
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

        conn = connectDB()
        id = int(str(conn.execute("SELECT COUNT(*) FROM Game").fetchall()[0]).strip('(').strip(')').strip(','))+1
        
        players = [Player(name,'../static/PNG-cards-1.3/None_of_None.png','../static/PNG-cards-1.3/None_of_None.png',1000,0),
                   Player("Jeremy",'../static/PNG-cards-1.3/None_of_None.png','../static/PNG-cards-1.3/None_of_None.png',1000,0),
                   Player("Jackcc",'../static/PNG-cards-1.3/None_of_None.png','../static/PNG-cards-1.3/None_of_None.png',1000,0)]
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
            return "SUCCESS"
        return "Username or Email Taken!"
    else:
        return render_template("login.html")

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method ==  "POST":
        conn = connectDB()
        
        user = request.form.get("user")
        id = request.form.get("id")
        
        if id == "buttonTech":
            return "No."
        
        print(user, id)
        
        game = str(conn.execute("SELECT JSON FROM Game WHERE GameID=?", (id,)).fetchone())
        game = game.strip('(').strip(')')
        game = game.replace("\\", "")
        game = game[1:]
        game = game[:-1]
        game = game[:-1]
        poker = convertGame(game)
        e = [i.strip(' ') for i in poker.getPlayerNames()]
        if user in e:
            return "SUCCESS"
        poker.addPlayer(user)
        game = poker.json()
        game = str(game)
        conn.execute("UPDATE Game SET JSON=? WHERE GameID=?", (game, id,))
        conn.commit()
        
        return 'SUCCESS'
    else:
        return "No."

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if request.method == "POST":
        conn = connectDB()
        bet = request.form.get("bet")
        id = request.form.get("id")
        re = "no."
        
        print(id, bet)
        
        ssid = session["name"]

        # Don't allow requests with no game ID to be fulfilled
        if id == None:
            return re
        
        
        # Get json game data from database and convert it to game object to be modified
        game = str(conn.execute("SELECT JSON FROM Game WHERE GameID=?", (id,)).fetchone())
        game = game.strip('(').strip(')')
        game = game.replace("\\", "")
        game = game[1:]
        game = game[:-1]
        game = game[:-1]
        poker = convertGame(game)       #convert json to game object
        
        
        # Handle mucks
        if bet == "muck":
            playerNames = poker.getPlayerNames()
            x = playerNames.index(ssid)
            poker.muckPlayer(x)
        
        
        # Rate limiting to make sure new round isn't started until 10 seconds has passed
        if poker.getRound() == 4 and time.time()-poker.getTime() < 10:
            return 'Error'
        
        # Rate limiting to not fold player unless necessary
        if time.time()-poker.getTime() <= 30 and bet == "timeOut":
            return "invalid"
        elif time.time()-poker.getTime() > 30 and bet == "timeOut":
            bet = -1
        
        # Rate limiting to make sure players cant spam bet for eachother
        if time.time()-poker.getTime() > 0.1:       # make condition > 2.0 when not debugging
            poker.setTime(time.time())
        else:
            return "You're being rate limited"
        
        
        # Handle various bet values
        if bet == 'BOMB POT':
            poker.setBombPot()
        elif bet == 'begin':
            poker.activate()
        elif bet == 'newRound' and poker.getRound() == 4:
            poker.newRound()
        elif bet == 'newRound' and poker.getRound() != 4:
            return "Error"
        elif bet == 'rTen':
            poker.setR10()
            poker.placeBetFold(poker.getBuyIn()*0.01)
        elif bet == 'muck':
            bet = None
        else:
            bet = int(bet)
            if bet < 0:
                bet = None
            poker.placeBetFold(bet)
        
        # Convert game back to a json string and update it in the database
        game = poker.json()
        game = str(game)
        conn.execute("UPDATE Game SET JSON=? WHERE GameID=?", (game, id,))
        conn.commit()
        return "SUCCESS"
    
    return redirect(url_for("home"))
     
@app.route('/getGame/<int:Number>')
def getGame(Number):
    if Number == 0:
        return game1.json()
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
        return render_template('table.html', game=game1)
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
    datas = eval(data)
    players = [Player(**i) for i in datas["players"]]
    del datas["players"]
    x = Game(**datas, players=players)
    return x