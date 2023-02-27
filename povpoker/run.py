from flask import Flask, render_template, request, session, redirect, flash
from turbo_flask import Turbo
import threading
from Player import Player
from main import Game
from flask_session import Session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from .models import User
# from .forms import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://////Users/mattbryan/POV-Poker/povpoker/user.db'
db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!'
Session(app)
turbo = Turbo(app)

player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,6,0), Player("Ethan",None,None,1000,6,0), Player("Jack",None,None,1000,6,0)]
game = Game(player, 10, 20, True)
game.newRound()


@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    username = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.password.data = ''
        flash("User added Succesfully!")
    our_users = User.query.all()
    return render_template('addUser.html', form=form, username=username, our_users=our_users)



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

@app.route('/help')
def help():
    return render_template('help.html')

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