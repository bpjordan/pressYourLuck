from trivia import Question, TriviaGame
from spin import Box, Whammy, SpinGame
from tkinter import *
import random
from gpiozero import Button, LED
import gpiozero, gpiozero.pins.mock
from time import sleep

# try:
#     gpiozero.pi_info()
# except gpiozero.exc.BadPinFactory:
#     print("GPIO not connected. Defaulting to mock GPIO library")
#     from gpiozero.pins.mock import MockFactory
#     Button.pin_factory = MockFactory()
#     LED.pin_factory = MockFactory()

#Delay in ms between game updates
TICKRATE = 500

#Constants for GPIO buttons
PLAYERBUTTONS = [22,23]
PLAYERLEDS = [21,24]

TRIVIABUTTONS = [25,26,27]

NUMPLAYERS = 2

HIGHLIGHTCOLOR = 'yellow2'
UNHIGHLIGHTCOLOR = 'dim gray'

QUESTIONSPERROUND = 4
NUMROUNDS = 2


#Player Class, pretty self explanatory
class Player:
    def __init__(self, button, led):
        self.bank = 0
        self.passedSpins = 0
        self.spins = 0

        try:
            self.button = Button(button)
        except gpiozero.exc.BadPinFactory:
            self.button = Button(button, pin_factory=gpiozero.pins.mock.MockFactory())
            print("Pin {} not found, defaulting to mock pin factory".format(button))
        
        try:
            self.led = LED(led)
        except gpiozero.exc.BadPinFactory:
            self.led = LED(led, pin_factory=gpiozero.pins.mock.MockFactory())
            print("Pin {} not found, defaulting to mock pin factory".format(button))

    #Pretty much just for debugging
    def __str__(self):
        return "Bank: ${}\n\nSpins: {}\n".format(self.bank,self.spins + self.passedSpins, self.passedSpins)
    
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

        #Our list of players
        self.players = [Player(button = PLAYERBUTTONS[x], led = PLAYERLEDS[x]) for x in range(NUMPLAYERS)]

        #state tracking stuff
        self.handleButton = False
        self._buttonPress = None
        self.handleButton = False
        self.answeringPlayer = None
        self.triviaAnswer = None
        self.spinningPlayer = 0
        self.roundsRemaining = NUMROUNDS

        #We must keep track of the highlighterd box in order to un-highlight it more easily		
        self.highlightedBox = None

        #We also have to keep track of what part of the game we are in
        self.gameState = 0 #states: 0-waiting to start, 1-trivia, 2-spinner
        self.subState = 0


        self.validBoxes = [(x,y) for x in range(6) for y in range(5) if (x < 1 or x > 4) or (y < 1 or y > 3)]

        self.displayPlayers() #TODO: Remove this from initialization once it is handled by gameTick

        self.initGPIO()
        self.initGUI()

        self.shuffleBoard()

    @property
    def buttonPress(self):
        val = self._buttonPress
        self._buttonPress = None
        self.handleButton = False
        return val

    def pressButton(self, value):
        if self.handleButton == False:
            self._buttonPress = value
            self.handleButton = True

    def pressTrivia(self, value):
        self.triviaAnswer = value

    @property
    def gameState(self):
        return self._gameState
    
    @gameState.setter
    def gameState(self, value):
        self._gameState = value
        self.subState = 0
    
    #Initializer functions
    def initGPIO(self):
        # for currPlayer in range(len(self.players)):
        #     self.players[currPlayer].button.when_pressed = lambda: self.pressButton(currPlayer)
        #     self.players[currPlayer].led.on()
        self.players[0].button.when_pressed = lambda: self.pressButton(0)
        self.players[1].button.when_pressed = lambda: self.pressButton(1)

        self.answerButtons = [Button(x) for x in TRIVIABUTTONS]
        for index in range(len(self.answerButtons)):
            self.answerButtons[index].when_pressed = lambda: self.pressTrivia(index)

    def initGUI(self):
        for row in range(5):
            Grid.rowconfigure(self, row, weight = 1)
        for col in range(6):
            Grid.columnconfigure(self, col, weight = 1)

    def shuffleBoard(self):

        self.boxes = self.spin.populate()
        for index in range(len(self.boxes)):
            img = Label(self, image = self.boxes[index], bg = UNHIGHLIGHTCOLOR, borderwidth = 5, relief = SOLID)
            img.grid(column=self.validBoxes[index][0], row=self.validBoxes[index][1], sticky=N+S+E+W)
    
    def highlightBox(self, box):
        img = Label(self, image=self.boxes[box], bg = HIGHLIGHTCOLOR, borderwidth = 5, relief = SOLID)
        img.grid(column=self.validBoxes[box][0], row=self.validBoxes[box][1], sticky=N+S+E+W)
        self.highlightedBox = box

    def unHighlightBox(self, highlightNewBox = True):

        #Unhighlight the old box
        if self.highlightedBox is not None:
            img = Label(self, image=self.boxes[self.highlightedBox], bg=UNHIGHLIGHTCOLOR, borderwidth = 5, relief = SOLID)
            img.grid(column=self.validBoxes[self.highlightedBox][0], row=self.validBoxes[self.highlightedBox][1], sticky=N+S+E+W)

        if highlightNewBox:
            #highlight the new box
            possibleLocations = list(filter(lambda box: box is not self.highlightedBox, range(len(self.boxes))))
            self.highlightBox(random.choice(possibleLocations))
        else:
            self.highlightedBox = None

    def spinBoard(self, shuffle=False):
        if shuffle:
            self.shuffleBoard()
        self.unHighlightBox()

    def addTrivia(self):
        #get a trivia question and put it in the middle of the screen
        #TODO: Make this a lot prettier

        #Get a question from the trivia object
        self.currQuestion, self.correctAnswer = self.trivia.generateQuestion()

        #Hopefully, display the question in the middle of the grid
        self.questionDisplay = Label(self, text=self.currQuestion + "\n\nBuzz in with your button", bg= "white", font = ("Calibri", 50))
        self.questionDisplay.grid(row = 1, column = 1, columnspan = 4, rowspan = 3, sticky=N+S+E+W)
        
    def updateTrivia(self, text=""):
        self.questionDisplay = Label(self, text=self.currQuestion + "\n\n" + text, bg= "white", font = ("Calibri", 50))
        self.questionDisplay.grid(row = 1, column = 1, columnspan = 4, rowspan = 3, sticky=N+S+E+W)

    def displayPlayers(self, **kwargs):
        #When we're not in trivia, put a display with all of the players' information
        #start by creating a frame to put all of this in

        self.playerDisplay = Frame(self)

        #define the grid for this frame
        Grid.rowconfigure(self.playerDisplay, 0, weight=1)
        for col in range(NUMPLAYERS):
            Grid.columnconfigure(self.playerDisplay, col, weight=1)

        #Place a box for each player in this grid
        self.playerLabels = []
        for player in range(len(self.players)):
            labelText = "Player {}:\n\n{}\n\n".format(player + 1, self.players[player])

            #append text to this label if we have anything to add in kwargs
            if str(player) in kwargs.keys():
                labelText += kwargs[str(player)]

            
            self.playerLabels.append(Frame(self.playerDisplay))
            # bkgdLabel = Label(self.playerLabels[-1], image=bkgd)
            # bkgdLabel.pack(expand=True)
            textLabel = Label(self.playerLabels[-1], text=labelText, font=("Calibri", 50), bg = "Orange", borderwidth = 5, relief = SOLID)
            textLabel.pack(fill=BOTH, expand=True)
            #Put it on the grid
            self.playerLabels[-1].grid(row=0, column=player,sticky=N+S+E+W)
        #Finally, put this frame in the spot that it goes in on the Big Board
        self.playerDisplay.grid(row = 1, column = 1, columnspan = 4, rowspan = 3, sticky=N+S+E+W)


    #########################
    #       GAME LOGIC      #
    #########################


    def waitTick(self):
        '''
        Game Tick to loop until game starts
        '''
        if self.subState == 4:
            self.subState = 1
            self.spinBoard(shuffle=True)
        else:
            self.spinBoard()

    def awaitButton(self):
        if self.handleButton:
            self.subState += 1


    #####################
    #   Trivia Funcs    #
    #####################

    def startQuestion(self):
        self.addTrivia()
        self.triviaAnswer = None
        temp = self.buttonPress
        self.playersRemaining = NUMPLAYERS
        self.subState += 1

    def awaitBuzzIn(self):
        if self.handleButton:
            self.answeringPlayer = self.buttonPress
            self.updateTrivia("Player {}, Enter your answer".format(self.answeringPlayer + 1))
            self.subState += 1
            self.triviaAnswer = None

    def awaitAnswer(self, firstPlayer = False):
        if self.triviaAnswer is None:
            return

        self.playersRemaining -= 1
        if self.triviaAnswer == self.correctAnswer:
            if firstPlayer:
                self.players[self.answeringPlayer].spins += 3
            else:
                self.players[self.answeringPlayer].spins += 1

        if self.answeringPlayer == len(self.players) - 1:
            self.answeringPlayer = 0
        else:
            self.answeringPlayer += 1

        if firstPlayer or self.playersRemaining == 0:
            self.subState += 1
            self.questionsRemaining -= 1

        if self.playersRemaining != 0:
            self.updateTrivia("Player {}, Enter your answer".format(self.answeringPlayer + 1))

        self.triviaAnswer = None

    def displayAnswer(self):
        if self.correctAnswer == 0:
            letter = 'A'
        elif self.correctAnswer == 1:
            letter = 'B'
        else:
            letter = 'C'

        self.updateTrivia("Correct Answer: " + letter)

        if self.questionsRemaining < 0:
            self.gameState += 1
        else:
            self.subState = 0
        
        self.pack(fill=BOTH, expand=True)
        sleep(3)



    #####################
    #   Spinning Funcs  #
    #####################

    def startSpin(self):
        #first, check if this player can spin, or if we need to move on to another player or round
        if self.players[self.spinningPlayer].spins + self.players[self.spinningPlayer].passedSpins == 0:
            self.playersRemaining -= 1
            if self.playersRemaining <= 0:
                self.roundsRemaining -= 1
                if self.roundsRemaining == 0:
                    self.gameState += 1
                else:
                    self.gameState -= 1
            else:
                if self.spinningPlayer == len(self.players) - 1:
                    self.spinningPlayer = 0
                else:
                    self.spinningPlayer += 1
            return

        #clear the middle of the screen and shuffle the board
        statusText = {str(self.spinningPlayer): "Press your button to spin"}
        if self.players[self.spinningPlayer].passedSpins == 0:
            statusText[str(self.spinningPlayer)] += "\nOr hit any of the trivia buttons to pass\nyour spins to the next player"
        self.displayPlayers(**statusText)
        self.shuffleBoard()
        self.subState += 1

    def awaitSpin(self):
        if self.handleButton:
            if self.buttonPress == self.spinningPlayer:
                self.subState = 5

    def landOnBox(self):
        box = self.boxes[self.highlightedBox]
        box.affect(self.players[self.spinningPlayer])

        if box.value == 0:
            statusText = {str(self.spinningPlayer): "Oh no! You got Whammied!"}
        else:
            statusText = {str(self.spinningPlayer): "Congratulations! ${} was\nadded to your bank!".format(box.value)}
        self.displayPlayers(**statusText)
        
        if self.players[self.spinningPlayer].passedSpins > 0:
            self.players[self.spinningPlayer].passedSpins -= 1
        elif self.players[self.spinningPlayer].spins > 0:
            self.players[self.spinningPlayer].spins -= 1
        
        if self.players[self.spinningPlayer].spins + self.players[self.spinningPlayer].passedSpins == 0:
            self.playersRemaining -= 1
            if self.playersRemaining <= 0:
                self.roundsRemaining -= 1
                if self.roundsRemaining == 0:
                    self.gameState += 1
                else:
                    self.gameState -= 1
            else:
                if self.spinningPlayer == len(self.players) - 1:
                    self.spinningPlayer = 0
                else:
                    self.spinningPlayer += 1
        else:
            self.subState = 0

            

    #####################
    #   Logic Handler   #
    #####################

    def eventLoop(self, parent):
        '''
        Event loop which determines where we are in the game, and processes the next tick accordingly

        God do I miss switch statements
        '''
        currState = self.gameState

        if currState == 0:          #Waiting to start
            if self.subState == 0:
                self.displayPlayers()
                self.waitTick()
                self.subState += 1
            else:
                self.waitTick()
            
            if self.handleButton:
                self.buttonPress
                self.questionsRemaining = QUESTIONSPERROUND
                self.gameState += 1
            else:
                self.subState += 1

        elif currState == 1:        #Trivia
            if self.subState == 0:
                self.startQuestion()
            elif self.subState == 1:
                self.awaitBuzzIn()
            elif self.subState == 2:
                self.awaitAnswer(True)
            elif self.subState == 3:
                self.awaitAnswer()
            elif self.subState == 4:
                self.displayAnswer()

        elif currState == 2:        #spin
            if self.subState == 0:
                self.startSpin()
            elif self.subState in range(1,5):
                self.awaitSpin()
                self.waitTick()
            elif self.subState == 5:
                self.landOnBox()

        elif currState == 3:
            self.displayWinner()
            

        self.pack(fill=BOTH, expand=True)

        #now queue up next tick
        parent.after(TICKRATE, self.eventLoop, parent)

    

def main():
    #start with the witchcraft that initializes the GUI
    window = Tk()
    window.attributes("-fullscreen", True)

    game = GameGui(window)

    game.eventLoop(window)

    window.mainloop()

if __name__ == '__main__':
    main()