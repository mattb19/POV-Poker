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

player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,6,0), Player("Jack",None,None,1000,6,0)]
game = Game(player, 10, 20)
game.newRound()
name = "Matt"

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('table.html'), 'load'))

@app.route("/")
def index2():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        name = session["name"]
        return redirect("/")
    return render_template("login.html")

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
    return {'load1': game.getPot(), 'name': name, 'game' : game}

@app.route('/bet/', methods=["GET", "POST"])
def getBets():
    if request.method == "POST":
        bet = request.form.get("bet")
        bet = 20
        bet = int(bet)
        if bet == -1:
            bet = None
        game.placeBetFold(bet)
        return render_template("table.html", game=game)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)