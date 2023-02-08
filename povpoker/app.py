from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from main import Game
from Player import Player
from User import User

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def pokerTable():
    player = [Player("1",None,None,1000,0,0), Player("2",None,None,1000,1,0), Player("3",None,None,1000,2,0), Player("4",None,None,1000,3,0), Player("5",None,None,1000,4,0), Player("6",None,None,1000,5,0), Player("7",None,None,1000,6,0), Player("8",None,None,1000,6,0), Player("9",None,None,1000,6,0), Player("10",None,None,1000,6,0)]
    return render_template("table.html", Player1=player[0], Player2=player[1], Player3=player[2], Player4=player[3], Player5=player[4], Player6=player[5], Player7=player[6], Player8=player[7], Player9=player[8], Player10=player[9], )

@app.route('/', methods=["GET", "POST"])
def getBets():
    if request.method == "POST":
        bet = request.form.get("bet")
        return "You have bet"+str(bet)
    return render_template("table.html")