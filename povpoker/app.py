from flask import Flask, render_template, redirect, jsonify, request, session, url_for, Response
from flask_session import Session
from forms import *
from Game import Game
from Player import Player
from User import User
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

player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,7,0), Player("Ethan",None,None,1000,8,0), Player("Jack",None,None,1000,9,0)]
# player = [Player("Ethan",None,None,1000,8,0), Player("Jack",None,None,1000,9,0)]
game = Game(player, 10, 20)
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
    return render_template_modal('home.html', theUser=theUser)


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
    form = LoginForm()
    if form.validate_on_submit():
        next_page = url_for('table')
        name = form.name.data
        session["name"] = name
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    if request.method == "POST":
        bet = request.form.get("bet")
        print(bet)
        if bet in ["2blind", "pottt2", "allin"]:
            return "Ignore"
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

@app.route('/d')
def d():
    return render_template('slider.html')

@app.route('/test')
def test():
    return render_template('pokerTable.html')





@app.route('/table')
def table():
    return render_template('table.html', game=game)