from trivia import Question, TriviaGame
from spin import Box, Whammy, SpinGame
from tkinter import *
import random
from PIL import Image, ImageTk
from gpiozero import Button, LED
import gpiozero, gpiozero.pins.mock

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
PLAYERBUTTONS = [23,24]
PLAYERLEDS = [17, 13]

TRIVIABUTTONS = [18,19,20]

NUMPLAYERS = 2

HIGHLIGHTCOLOR = 'yellow2'
UNHIGHLIGHTCOLOR = 'dim gray'


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
        s = "Bank: ${}\n\nSpins: {}\n".format(self.bank,self.spins + self.passedSpins, self.passedSpins)
        if self.passedSpins:
            s += "Must Spin"
        return s
    
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

        self.players = [Player(button = PLAYERBUTTONS[x], led = PLAYERLEDS[x]) for x in range(NUMPLAYERS)]

        #keep track of the states of all sets of buttons
        self.handleButton = False
        self._buttonPress = None
        self.handleButton = False
        self.answeringPlayer = None
        self.triviaAnswer = None

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

    def checkButtonPress(self, value):
        if self.handleButton == False:
            self._buttonPress = value
            self.handleButton = True

    @property
    def gameState(self):
        return self._gameState
    
    @gameState.setter
    def gameState(self, value):
        self._gameState = value
        self.subState = 0
    
    #Initializer functions
    def initGPIO(self):
        for player in range(len(self.players)):
            self.players[player].button.when_pressed = lambda: self.checkButtonPress(player)

    def initGUI(self):
        for row in range(5):
            Grid.rowconfigure(self, row, weight = 1)
        for col in range(6):
            Grid.columnconfigure(self, col, weight = 1)

    def shuffleBoard(self):

        #self.boxes = self.spin.populate()
        #Temporary for testing
        self.boxes = []
        for x,y in self.validBoxes:
            self.boxes.append(Label(self, text="{}\n{}".format((x,y), random.randint(0,10)), font=("Calibri", 35), bg='dim gray', borderwidth=10))
        for index in range(len(self.boxes)):
            self.boxes[index].grid(column=self.validBoxes[index][0], row=self.validBoxes[index][1], sticky=N+S+E+W)

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

    def spinBoard(self, shuffle=False):
        if shuffle:
            self.shuffleBoard()
        self.highlightNewBox()

    def addTrivia(self):
        #get a trivia question and put it in the middle of the screen
        #TODO: Make this a lot prettier

        #Get a question from the trivia object
        self.currQuestion, self.correctAnswer = self.trivia.generateQuestion()

        #Hopefully, display the question in the middle of the grid
        self.questionDisplay = Label(self, text=self.currQuestion, bg= "white", font = ("Calibri", 50))
        self.questionDisplay.grid(row = 1, column = 1, columnspan = 4, rowspan = 3, sticky=N+S+E+W)

    def displayPlayers(self):
        #When we're not in trivia, put a display with all of the players' information
        #start by creating a frame to put all of this in

        self.playerDisplay = Frame(self)

        #define the grid for this frame
        Grid.rowconfigure(self.playerDisplay, 0, weight=1)
        for col in range(NUMPLAYERS):
            Grid.columnconfigure(self.playerDisplay, col, weight=1)

        #make the background for each player's stats
        bkgd = ImageTk.PhotoImage(Image.open('Big Board Images/$2000.png').resize((500,500)))

        #Place a box for each player in this grid
        self.playerLabels = []
        for player in range(len(self.players)):
            labelText = "Player {}:\n\n{}".format(player + 1, self.players[player])

            #Make a canvas and put the background and text on it

            # self.playerLabels.append(Canvas(self.playerDisplay, height=500, width=500))
            # self.playerLabels[-1].create_image(200,200, image=bkgd)
            # self.playerLabels[-1].create_text(300,300, text=labelText, font=("Calibri", 50))

            # self.playerLabels.append(Label(self.playerDisplay, text=labelText, image=bkgd, compound='top', font=("Calibri", 50), borderwidth=10, relief='solid'))

            self.playerLabels.append(Frame(self.playerDisplay))
            bkgdLabel = Label(self.playerLabels[-1], image=bkgd)
            bkgdLabel.pack(expand=True)
            textLabel = Label(self.playerLabels[-1], text=labelText, font=("Calibri", 50))
            textLabel.place(anchor=N, relx=0.5, rely=0.25)
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
        if self.subState == 3:
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
        self.subState += 1

    def awaitAnswer(self, firstPlayer = False):
        if self.triviaAnswer is None:
            return

        if self.triviaAnswer == self.correctAnswer:
            if firstPlayer:
                self.players[self.answeringPlayer].bank += 300
            else:
                self.players[self.answeringPlayer].bank += 100

        if self.answeringPlayer == len(self.players) - 1:
            self.answeringPlayer = 0
        else:
            self.answeringPlayer += 1

        self.subState += 1

    def displayAnswers(self):
        pass

    #####################
    #   Spinning Funcs  #
    #####################

    def startSpin(self):
        #clear the middle of the screen and shuffle the board
        pass

    def landOnBox(self):
        pass

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
                    self.gameState += 1
                else:
                    self.subState += 1

        elif currState == 1:        #Trivia
            if self.subState == 0:
                self.startQuestion()
            elif self.subState == 1:
                self.awaitButton()
            elif self.subState == 2:
                self.awaitAnswer(True)
            elif self.subState == 3:
                self.awaitAnswer()
            elif self.subState == 4:
                self.displayAnswer()

        elif currState == 2:        #spin
            if self.subState == 0:
                self.startSpin()
            elif self.subState == 1:
                self.awaitButton()
                self.waitTick()
            elif self.subState == 2:
                self.landOnBox()

        elif currState == 3:
            self.displayWinner()
            

        self.pack(fill=BOTH, expand=True)

        #now queue up next tick
        parent.after(TICKRATE, self.eventLoop, parent)

    

def main():
    #start with the witchcraft that initializes the GUI
    window = Tk()
    # window.attributes("-fullscreen", True)

    game = GameGui(window)

    game.eventLoop(window)

    window.mainloop()

if __name__ == '__main__':
    main()