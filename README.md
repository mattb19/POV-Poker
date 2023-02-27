# POV-Poker
POV Poker is a work in progress. The end goal of this project is for users to be able to player poker with eachother online, and for special abilities to be added.

As of right now, POV Poker is still in early development. Some features do not work as expected while others have not been implemented yet. 

## Classes
* main.py: This is the game file. All attributes for the game are stored in this class, and all actions carried out by the users are passed through this class. All poker logic is present in this file.
* Player.py: This class contains all individual player attributes, for use by main.py - Each player contains a User
* User.py: This class has not yet been implemented, it will be used for database storage of player account attributes
* run.py: This is where the flask server is ran


## Dependencies
```console
pip install bs4
pip install selenium
pip install webdriver-manager
pip install flask-cors
pip install sqlite
pip install turbo-flask
pip install Flask-Sessions
pip install Flask-SQLAlchemy
```

## How to Run
Run it using the following command:
```console
cd POV-Poker
python3 run.py
```
app.py is a test flask server, please ignore

## How to play
1. Enter your name and hit register
2. Hit join table
3. Start playing around with the betting, folding and such

## Fixes in progress
* Minor tweaks to poker logic
* ALL-IN capability
* Joining mid game
* Leaving mid game
* Session management/correct data being presented to the correct players
