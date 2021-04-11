from trivia import *
from spin import *
from tkinter import *
import random

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

HIGHLIGHTCOLOR = 'yellow2'
UNHIGHLIGHTCOLOR = 'dim gray'


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
		self.gameState = 1 #states: 0-trivia, 1-spinner


		self.validBoxes = [(x,y) for x in range(6) for y in range(5) if (x < 1 or x > 4) or (y < 1 or y > 3)]

		self.addTrivia() #TODO: Remove this once it is handled by gameTick

		self.initGPIO()
		self.initGUI()

		self.shuffleBoard()


	#Initializer functions
	def initGPIO(self):
		GPIO.setmode(GPIO.BCM)
		pins = [PLAYER0, PLAYER1, PLAYER2]
		for button in pins:
			GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			GPIO.add_event_detect(button, GPIO.RISING, bouncetime=100)

	def initGUI(self):
		for row in range(5):
			Grid.rowconfigure(self, row, weight = 1)
		for col in range(6):
			Grid.columnconfigure(self, col, weight = 1)

	def shuffleBoard(self):

		for x,y in self.validBoxes:
			placeholder = Label(self, text="{}".format((x,y)), font=("Calibri", 35), bg=UNHIGHLIGHTCOLOR, borderwidth=10)
			placeholder.grid(row=y, column=x, sticky = N+S+E+W)

	def highlightNewBox(self):
		possibleLocations = list(filter(lambda box: box is not self.highlightedBox, self.validBoxes))
		newBox = random.choice(possibleLocations)

		#Unhighlight the old box
		if self.highlightedBox is not None:
			placeholder = Label(self, text="{}".format(self.highlightedBox), font=("Calibri", 35), bg=UNHIGHLIGHTCOLOR, borderwidth=10)
			placeholder.grid(column=self.highlightedBox[0], row=self.highlightedBox[1], sticky=N+S+E+W)

		#highlight the new box
		placeholder = Label(self, text="{}".format(newBox), font=("Calibri", 35), bg=HIGHLIGHTCOLOR, borderwidth=10, relief='solid')
		placeholder.grid(column=newBox[0], row=newBox[1], sticky=N+S+E+W)

		#note the newly old highlighted box (try puzzling out THAT comment)
		self.highlightedBox = newBox


	def addTrivia(self):
		#get a trivia question and put it in the middle of the screen
		#TODO: Make this a lot prettier

		#Get a question from the trivia object
		self.currQuestion, self.currAnswers = self.trivia.generateQuestion()

		#Parse the question data into something we can display
		self.answerText = list(self.currAnswers.keys())
		self.questionText = "{}\n\nA. {}\nB. {}\nC. {}".format(self.currQuestion, self.answerText[0], self.answerText[1], self.answerText[2])

		#Hopefully, display the question in the middle of the grid
		self.questionDisplay = Label(self, text=self.questionText, bg= "white", font = ("Calibri", 50))
		self.questionDisplay.grid(row = 1, column = 1, columnspan = 4, rowspan = 3, sticky=N+S+E+W)

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
			self.addTrivia()
		#Otherwise, we are spinning
		else:
			self.highlightNewBox()
		

		self.pack(fill=BOTH, expand=1)
		#be like goofy and do it again
		parent.after(TICKRATE, self.gameTick, parent)
		
		

	

def main():
	#start with the witchcraft that initializes the GUI
	window = Tk()
	window.attributes("-fullscreen", True)

	game = GameGui(window)

	game.gameTick(window)

	window.mainloop()

	GPIO.cleanup()

if __name__ == '__main__':
	main()