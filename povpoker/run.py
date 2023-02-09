from flask import Flask, render_template, request, session, redirect
from turbo_flask import Turbo
import threading
import time
from Player import Player
from main import Game
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!'
Session(app)
turbo = Turbo(app)

player = [Player("Ryan",None,None,1000,2,0), Player("Jack",None,None,1000,0,0), Player("Matt",None,None,1000,1,0)]
game = Game(player, 10, 20, True)
game.newRound()

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        turbo.push(turbo.replace(render_template('table.html'), 'load'))
        redirect("/poker")

def printCurrent():
    print(game.getPlayers()[game.getCurrentPlayer()].getUser())

@app.route("/")
def index2():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        big = request.form.get("bigBlind")
        small = request.form.get("smallBlind")
        buy = request.form.get("buy")
        p1 = Player(request.form.get("player1"), None, None, buy, 0, "small")
        p2 = Player(request.form.get("player2"), None, None, buy, 1, "big")
        p3 = Player(request.form.get("player3"), None, None, buy, 2, None)
        if not game.isActive():
            game.reset(big, small, p1, p2, p3)
            return redirect("/poker")
        return redirect("/")
    return render_template("create.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/poker')
def index():
    return render_template('index2.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.context_processor
def inject_load():
    return {'game' : game, 'player0' : game.getPlayers()[1].getUser()}

@app.route('/bet/', methods=["GET", "POST"])
def getBets():
    if request.method == "POST":
        bet = request.form.get("bet")
        bet = int(bet)
        if bet == -1:
            bet = None
        printCurrent()
        game.placeBetFold(bet)
        update_load()
    return redirect("/poker")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)