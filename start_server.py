from flask import Flask, render_template, request
from Hangman import Hangman

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST', 'GET'])
@app.route('/result', methods=['POST', 'GET'])
@app.route('/double_start', methods=['POST', 'GET'])
@app.route('/join', methods=['POST', 'GET'])
def start_game():
    if request.method == 'POST':
      # username = request.form['username']
      if request.form['submit_button'] in ['Start Single Player Mode', 'Replay Single Player Mode']:
        game = Hangman.new_game()
        return render_game(game,'')
      elif request.form['submit_button'] in ['Start Two Player Mode', 'Replay Two Player Mode']:
        return render_template('double_options.html')
      elif request.form['submit_button'] == "Join Game":
        id = int(request.form['id'])
        game = Hangman.get_game(id)
        return render_game(game,'')
      elif request.form['submit_button'] == "Menu":
        return render_template('index.html')
    return "Game started"

@app.route('/guess', methods=['POST'])
def guess():
    if request.method == 'POST':
        letter = request.form['character'].lower()
        game_id = int(request.form['gameId'])
        print("Game to play:", game_id)
        game = Hangman.get_game(game_id)

        if not len(letter) == 1 or not letter.isalpha() or letter in game.usedLetters:
          if not letter.isalpha():
            message = " You have to guess a letter!"
          elif len(letter) != 1:
            message = " You can't guess more than one letter at a time!"
          elif letter in game.usedLetters:
            message = " You already tried that letter!"   
          return render_game(game, message)

        game.guess(letter)
        if game.isWinning():
            return render_template("single_result.html", result= "won", secret_word=game.secretWord)
        if game.isLosing():
            return render_template("single_result.html", result= "lost", secret_word=game.secretWord)
        return render_game(game, " Your guess is: " + letter)

@app.route('/create', methods=['POST', 'GET'])
def create_join_game():
    if request.method == 'POST':
      if request.form['submit_button'] == "Create A New Game":
        return render_template("double_create_game.html")
      if request.form['submit_button'] == "Join A Game":
        return render_template("double_create_game.html", '')
      return "Create/Join Game"

@app.route('/create_success', methods=['POST', 'GET'])
def create_success():
    if request.method == 'POST':
      secretWord = request.form['word_to_guess'].lower()

      for ch in secretWord:
        if not ch.isalpha():
          message = "Invalid input: only a secret word with all alphabetical letters allowed!"
          return render_template("double_create_game.html", message=message) 
      if len(set(list(secretWord))) >= 20:
          message = "Invalid input: only a word fewer than 20 dictict digits allowed"
          return render_template("double_create_game.html", message=message)     

      game = Hangman.new_game(secretWord)
      id = game.id
    return render_template("double_create_success.html", secretWord=secretWord, id=id)

def render_game(game, message):
    display = "".join(game.get_word())
    return render_template('game.html', game_id=game.id, secret_word=display, incorrect_guesses=game.get_incorrect(),
                           step=len(game.get_incorrect()), message=message)

if __name__ == '__main__':
    app.run(debug=True)
