from flask import Flask, render_template, url_for, redirect
from forms import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/table')
def table():
    return render_template('table.html')