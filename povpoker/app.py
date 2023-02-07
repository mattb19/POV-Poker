from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def pokerTable():
    return render_template("table.html")