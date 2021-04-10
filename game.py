from trivia import *
from spin import *
from tkinter import *

#Useful little dummy module to use instead of always testing on an rpi
#install with pip install Mock.GPIO
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
	import Mock.GPIO as GPIO

#Delay in ms between game updates
TICKRATE = 500

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

		#There is one object to process trivia and one object to process the spinning
		self.trivia = TriviaGame()
		self.spin = SpinGame()

		self.players = [Player() for x in range(3)]

		#We must keep track of the highlighterd box in order to un-highlight it more easily		
		self.highlightedBox = None
		self.gameState = 0 #states: 0-trivia, 1-spinner

	def initGPIO(self):
		GPIO.setmode(GPIO.BCM)
		pins = [PLAYER0, PLAYER1, PLAYER2]
		GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		for button in pins:
			GPIO.add_event_detect(button)

	def gameTick(self, parent):
		#Tasks to do every game update
		if self.gameState == 0:
			#do trivia things
			pass
		else:
			#do spinny things
			pass
		

		#be like goofy and do it again
		parent.after(TICKRATE, self.gameTick, parent)
		
		

	

def main():
	#witchcraft that initializes the GUI
	window = Tk()
	window.attributes("-fullscreen", True)

	game = GameGui(window)
	game.initGPIO()

	game.gameTick(window)

	#window.mainloop()

	GPIO.cleanup()

if __name__ == '__main__':
	main()