from flask import Flask, render_template, request, Response, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from main import Game
from Player import Player
from User import User
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,6,0), Player("Ethan",None,None,1000,6,0), Player("Jack",None,None,1000,6,0)]
game = Game(player, 10, 20)
game.newRound()

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")






@app.route('/poker', methods=["GET", "POST"])
def pokerTable():
    return render_template("table.html", game=game)


@app.route('/bet/', methods=["GET", "POST"])
def getBets():
    if request.method == "POST":
        bet = request.form.get("bet")
        bet = int(bet)
        if bet == -1:
            bet = None
        game.placeBetFold(bet)
        return render_template("table.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)