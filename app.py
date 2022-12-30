from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "ManchesterUnited"
app.config['TESTING'] = True
app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

boggle_game = Boggle()
games_played = 0
high_score = 0

@app.route("/")
def get_home():
  session["board"] = boggle_game.make_board()
  session["guesses"] = []
  session["guessed_words"] = []
  return render_template('index.html')


@app.route("/guess", methods=["POST"])
def post_guess():
  guess = request.json["guess"]
  board = session["board"]
  if guess not in session["guessed_words"]:
    session["guessed_words"].append(guess)
    session.modified = True
    return jsonify(result=boggle_game.check_valid_word(board, guess))
  else: 
    return jsonify(result="repeat-guess")  


@app.route("/high-score", methods=["POST"])
def post_score():
  global games_played
  global high_score 
  games_played = games_played + 1
  score = request.json["score"]
  message = f"Nice try but not enough, the high score is {high_score}"
  if score >= high_score:
    high_score = score
    message = f"Woohoo you set a new high score with {score} points"
  return jsonify(message=message, games_played=games_played)