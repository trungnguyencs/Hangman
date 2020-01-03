import subprocess as sp
import random

class Hangman:
    games = dict()
    counter = 1

    def getWord():
      wordList = ['apple', 'banana', 'kiwi', 'orange', 'tomato', 'juice', 'firewood', 'beautiful', 'pencil']
      randomWord = random.choice(wordList)
      return randomWord

    @classmethod
    def new_game(cls, secretWord=getWord()):
        game = cls(secretWord, cls.counter)
        cls.games[game.id] = game
        cls.counter = cls.counter + 1
        return game

    @classmethod
    def get_game(cls, id):
        return cls.games[id]

    def __init__(self, secretWord, counter):
        self.secretWord = secretWord.lower()
        self.displayWord = list('_ ' * len(secretWord))
        self.incorrectLetters = []
        self.id = counter
        self.usedLetters = set()

    def guess(self, guessLetter):
        self.usedLetters.add(guessLetter)
        if guessLetter in self.secretWord:
            for index in range(len(self.secretWord)):
                if self.secretWord[index] == guessLetter:
                    self.displayWord[2 * index] = guessLetter
        else:
            self.incorrectLetters.append(guessLetter)

    def get_word(self):
        return self.displayWord

    def get_incorrect(self):
        return self.incorrectLetters

    def gameOver(self):
        return self.isWinning() or self.isLosing()

    def isWinning(self):
        return len(self.incorrectLetters) < 6 and not ('_' in self.displayWord)

    def isLosing(self):
        return len(self.incorrectLetters) >= 6
