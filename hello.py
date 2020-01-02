from flask import Flask, render_template, request

from Hangman import Hangman

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST', 'GET'])
@app.route('/result', methods=['POST', 'GET'])
def start_game():
    if request.method == 'POST':
      if request.form['submit_button'] in ['Start Single Player Mode', 'Replay Single Player Mode']:
        game = Hangman.new_game()
        return render_game(game,'')
      elif request.form['submit_button'] in ['Start Two Player Mode', 'Replay Two Player Mode']:
        pass
      elif request.form['submit_button'] == "Menu":
        return render_template('index.html')
    return "Game started"

@app.route('/guess', methods=['POST'])
def guess():
    if request.method == 'POST':
        letter = request.form['character']
        game_id = int(request.form['gameId'])
        print("Game to play:", game_id)
        game = Hangman.get_game(game_id)
        if not len(letter) == 1 or not letter.isalpha():
            message = " Please enter a letter only!"
            return render_game(game, message)
        game.guess(letter.lower())
        if game.isWinning():
            return render_template("single_result.html", result= "won", secret_word=game.secretWord)
        if game.isLosing():
            return render_template("single_result.html", result= "lost", secret_word=game.secretWord)
        return render_game(game, " Your guess is: " + letter)

def render_game(game, message):
    display = "".join(game.get_word())
    return render_template('game.html', game_id=game.id, secret_word=display, incorrect_guesses=game.get_incorrect(),
                           step=len(game.get_incorrect()), message=message)

if __name__ == '__main__':
    app.run(debug=True)
