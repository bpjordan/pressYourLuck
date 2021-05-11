from tkinter import *
import random

class Box(PhotoImage):
    def __init__(self, img:str, value:int):
        PhotoImage.__init__(self, file=img)
        self.value = value
    
    def affect(self, player):
        player.bank += self.value

# a prize box is
# - an int value
# - an image

# a prize box has
# - a fn that adds its value to the players bank
class PrizeBox(Box):
    def __init__(self, img, value):
        Box.__init__(self, img,value)
        raise NotImplementedError

    def affect(self, player):
        player.bank += self.value

        
# a whammy is
# - a box with specific conditions
# - an image of a whammy

# a whammy has
# - a value that distiguishes it from any other box
# - maybe a function that clears a players bank and adds a whammy to their whammy count
class Whammy(Box):
    def __init__(self):
        img = "Whammies/Whammy{}.png".format(random.randint(1,10))
        Box.__init__(self, img, 0)
        # self.img = "Whammy"

    def affect(self, player):
        player.bank = 0
        player.whammies += 1

class SpinGame:

    def __init__(self):
        self.prizes = list()
        self.prizes.append("$2000")
        self.prizes.append("$2250")
        self.prizes.append("$3000")
        self.prizes.append("3wheeler")
        self.prizes.append("5loungers")
        self.prizes.append("Acapulco")
        self.prizes.append("Africansafari")
        self.prizes.append("Alaska")
        self.prizes.append("Alaskancruise")
        self.prizes.append("Amsterdam")
        self.prizes.append("Athens")
        self.prizes.append("Australia")
        self.prizes.append("Bahamas")
        self.prizes.append("Balanschairs")
        self.prizes.append("Banff")
        self.prizes.append("Barbque")
        self.prizes.append("Bedroomset")
        self.prizes.append("Bermuda")
        self.prizes.append("Bicycles")
        self.prizes.append("Bigbucks")
        self.prizes.append("Bigscreentv")
        self.prizes.append("Billiardtable")
        self.prizes.append("Binoculars")
        self.prizes.append("Boston")
        self.prizes.append("Bracelet")
        self.prizes.append("Brassbed")
        self.prizes.append("Brazil")
        self.prizes.append("Britain")
        self.prizes.append("Calgary")
        self.prizes.append("Canadianrockies")
        self.prizes.append("Cancun")
        self.prizes.append("Car")
        self.prizes.append("Caribbeancruise")
        self.prizes.append("Carpeting")
        self.prizes.append("Carstereo")
        self.prizes.append("Cassetteradio")
        self.prizes.append("Catamaran")
        self.prizes.append("Clock")
        self.prizes.append("Clusterring")
        self.prizes.append("Coasttocoasttour")
        self.prizes.append("Coloradonewmexicotour")
        self.prizes.append("Concord")
        self.prizes.append("Cookware")
        self.prizes.append("Crystaldecanterset")
        self.prizes.append("Curacao")
        self.prizes.append("Cutlery")
        self.prizes.append("Dallas")
        self.prizes.append("Deltaqueen")
        self.prizes.append("Denver")

        self.cost = list()
        self.cost.append(2000)
        self.cost.append(2250)
        self.cost.append(3000)
        self.cost.append(20000)
        self.cost.append(700)
        self.cost.append(1500)
        self.cost.append(1950)
        self.cost.append(1500)
        self.cost.append(1100)
        self.cost.append(1100)
        self.cost.append(1350)
        self.cost.append(2000)
        self.cost.append(4500)
        self.cost.append(350)
        self.cost.append(550)
        self.cost.append(50)
        self.cost.append(1350)
        self.cost.append(500)
        self.cost.append(150)
        self.cost.append(50000)
        self.cost.append(600)
        self.cost.append(650)
        self.cost.append(50)
        self.cost.append(400)
        self.cost.append(250)
        self.cost.append(300)
        self.cost.append(4000)
        self.cost.append(3250)
        self.cost.append(1000)
        self.cost.append(1000)
        self.cost.append(2000)
        self.cost.append(24000)
        self.cost.append(900)
        self.cost.append(800)
        self.cost.append(350)
        self.cost.append(30)
        self.cost.append(250)
        self.cost.append(1500)
        self.cost.append(5500)
        self.cost.append(2500)
        self.cost.append(1200)
        self.cost.append(500)
        self.cost.append(450)
        self.cost.append(150)
        self.cost.append(700)
        self.cost.append(50)
        self.cost.append(250)
        self.cost.append(150)
        self.cost.append(900)

        self.numBoxes = 18
        self.numWhammies = 3

    def populate(self):
        values = random.sample(range(len(self.prizes)), self.numBoxes-self.numWhammies)
        bigBoard = []
        for i in range(self.numBoxes):
            if i < self.numBoxes - self.numWhammies:
                bigBoard.append(Box("Big Board Images/" + self.prizes[values[i]] + ".png", self.cost[values[i]]))
            else:
                bigBoard.append(Whammy())
        
        random.shuffle(bigBoard)
        return bigBoard
                
    def addWhammies(bigBoard,value):
        j = 0
        while j < value:
            bigBoard.append(Whammy())

#PhotoImage(file="{}.png")
