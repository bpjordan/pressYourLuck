from trivia import TriviaGame, Question
from spin import SpinGame, Box, Whammy
from tkinter import *

#Useful little dummy module to use instead of always testing on an rpi
#install with pip install Mock.GPIO
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
	import Mock.GPIO as GPIO

#Constants for GPIO buttons
PLAYER0 = 23
PLAYER1 = 24
PLAYER2 = 25

#Player Class, pretty self explanatory
class Player:
	def __init__(self):
		self.bank = 0
		self.passedSpins = 0
		self.spins = 0

	#Pretty much just for debugging
	def __str__(self):
		return "This player has ${}, {} passed spins, and {} regular spins".format(self.bank, self.passedSpins, self.spins)
	
	#Pass this player's spins to another player
	def passTo(otherPlayer):
		otherPlayer.passedSpins += self.spins
		self.spins = 0

#main class for the game to take place in
class GameGui(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.players = [Player() for x in range(3)]
		
		self.highlightedBox = None

	def initGPIO(self):
		GPIO.setmode(GPIO.BCM)
		pins = [PLAYER0, PLAYER1, PLAYER2]

	

def main():
	#witchcraft that initializes the GUI
	window = Tk()

	game = GameGui(window)
	game.initGPIO()

if __name__ == '__main__':
	main()