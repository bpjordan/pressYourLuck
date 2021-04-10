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

		#We also have to keep track of what part of the game we are in
		self.gameState = 0 #states: 0-trivia, 1-spinner


	#Initializer functions
	def initGPIO(self):
		GPIO.setmode(GPIO.BCM)
		pins = [PLAYER0, PLAYER1, PLAYER2]
		for button in pins:
			GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.add_event_detect(button, GPIO.RISING, bouncetime=100)

	def initGUI(self):
		pass

	def addTrivia(self):
		#get a trivia question and put it in the middle of the screen
		#TODO: Make this a lot prettier
		self.currQuestion, self.currAnswers = self.trivia.generateQuestion()
		self.questionDisplay = Label(self, text="", anchor=CENTER,\
			bg= "white", height=2, font = ("Calibri", 100))
		self.questionDisplay.grid(row = 1, column = 1, columnspan = 4)

		self.answerText = self.currAnswers.keys()
		self.questionDisplay['text'] += "{}\n\nA. {}\nB. {}\nC. {}"\
			.format(self.currQuestion, self.currAnswers[0], self.currAnswers[1], self.currAnswers[2])

		self.pack(fill=BOTH, expand=1)

	def startSpin(self):
		#clear the middle of the screen and shuffle the board
		pass

	def gameTick(self, parent):
		'''
		Tasks that must be completed every game update
		'''
		#If we are in trivia
		if self.gameState == 0:
			#do trivia things
		#Otherwise, we are spinning
		else:
			#so do spinny things
			pass
		

		#be like goofy and do it again
		parent.after(TICKRATE, self.gameTick, parent)
		
		

	

def main():
	#start with the witchcraft that initializes the GUI
	window = Tk()
	window.attributes("-fullscreen", True)

	game = GameGui(window)
	game.initGPIO()

	game.gameTick(window)

	# window.mainloop()

	GPIO.cleanup()

if __name__ == '__main__':
	main()