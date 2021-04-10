from trivia import TriviaGame, Question
from spin import SpinGame, Box, Whammy
from tkinter import *

class Player:
	def __init__(self):
		self.bank = 0
		self.passedSpins = 0
		self.spins = 0

	def __str__(self):
		return "This player has ${}, {} passed spins, and {} regular spins".format(self.bank, self.passedSpins, self.spins)
	
	def passTo(otherPlayer):
		otherPlayer.passedSpins += self.spins
		self.spins = 0

#main class for the game to take place in
class GameGui(Frame):
	def __init__(self):
		self.players = [Player() for x in range(3)]
		
		self.highlightedBox = None

	

def main():
	pass

if __name__ == '__main__':
	main()