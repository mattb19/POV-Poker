from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from forms import *
from Game import Game
from Player import Player

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret!'
Session(app)

player = [Player("Jeremy",None,None,1000,0,0), Player("Matt",None,None,1000,1,0), Player("Trent",None,None,1000,2,0), Player("Ryan",None,None,1000,3,0), Player("Jackson",None,None,1000,4,0), Player("Luke",None,None,1000,5,0), Player("David",None,None,1000,6,0), Player("Max",None,None,1000,6,0), Player("Ethan",None,None,1000,6,0), Player("Jack",None,None,1000,6,0)]
game = Game(player, 10, 20, True)
game.newRound()




@app.route('/')
def home():
    return render_template('home.html')

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
        bet = int(bet)
        if bet == -1:
            bet = None
        game.placeBetFold(bet)
    return redirect("/table")
    

@app.route('/table')
def table():
    return render_template('table.html', game=game)