from tkinter import *
from random import *

class Box(PhotoImage):
    def __init__(self, img:str, value:int):
            PhotoImage.__init__(file=img, bg='dim gray', borderwidth=10)
            self.value = value
    

# a prize box is
# - an int value
# - an image

# a prize box has
# - a fn that adds its value to the players bank
class PrizeBox(Box):
    def __init__(self, img, value):
        Box.__init__(img,value)
        raise NotImplementedError

    def affect(Player):
        Player.bank += self.value

        
# a whammy is
# - a box with specific conditions
# - an image of a whammy

# a whammy has
# - a value that distiguishes it from any other box
# - maybe a function that clears a players bank and adds a whammy to their whammy count
class Whammy(Box):
    def __init__(self):
        Box.__init__(img, 0)
        #img = "Whammy{}.png".format(randint(1,10))
        self.img = "Whammy"

    def affect(Player):
        Player.bank = 0
        Player.whammies += 1

class SpinGame:

    def populate():
        prizes = list()
        prizes.append("$2000")
        prizes.append("$2250")
        prizes.append("$3000")
        prizes.append("3wheeler")
        prizes.append("5loungers")
        prizes.append("Acapulco")
        prizes.append("Africansafari")
        prizes.append("Alaska")
        prizes.append("Alaskancruise")
        prizes.append("Amsterdam")
        prizes.append("Athens")
        prizes.append("Australia")
        prizes.append("Bahamas")
        prizes.append("Balanschairs")
        prizes.append("Banff")
        prizes.append("Barbque")
        prizes.append("Bedroomset")
        prizes.append("Bermuda")
        prizes.append("Bicycles")
        prizes.append("Bigbucks")
        prizes.append("Bigscreentv")
        prizes.append("Billiardtable")
        prizes.append("Binoculars")
        prizes.append("Boston")
        prizes.append("Bracelet")
        prizes.append("Brassbed")
        prizes.append("Brasil")
        prizes.append("Britian")
        prizes.append("Calgary")
        prizes.append("Canadianrockies")
        prizes.append("Cancun")
        prizes.append("Car")
        prizes.append("Caribbeancruise")
        prizes.append("Carpeting")
        prizes.append("Carstereo")
        prizes.append("Cassetteradio")
        prizes.append("Catamaran")
        prizes.append("Clock")
        prizes.append("Clusterring")
        prizes.append("Coasttocoasttour")
        prizes.append("Coloradonewmexicotour")
        prizes.append("Concord")
        prizes.append("Cookware")
        prizes.append("Crystaldecanterset")
        prizes.append("Curacao")
        prizes.append("Cutlery")
        prizes.append("Dallas")
        prizes.append("Deltaqueen")
        prizes.append("Denver")

        cost = list()
        cost.append(2000)
        cost.append(2250)
        cost.append(3000)
        cost.append(20000)
        cost.append(700)
        cost.append(1500)
        cost.append(1950)
        cost.append(1500)
        cost.append(1100)
        cost.append(1100)
        cost.append(1350)
        cost.append(2000)
        cost.append(4500)
        cost.append(350)
        cost.append(550)
        cost.append(50)
        cost.append(1350)
        cost.append(500)
        cost.append(150)
        cost.append(50000)
        cost.append(600)
        cost.append(650)
        cost.append(50)
        cost.append(400)
        cost.append(250)
        cost.append(300)
        cost.append(4000)
        cost.append(3250)
        cost.append(1000)
        cost.append(1000)
        cost.append(2000)
        cost.append(24000)
        cost.append(900)
        cost.append(800)
        cost.append(350)
        cost.append(30)
        cost.append(250)
        cost.append(1500)
        cost.append(5500)
        cost.append(2500)
        cost.append(1200)
        cost.append(500)
        cost.append(450)
        cost.append(150)
        cost.append(700)
        cost.append(50)
        cost.append(250)
        cost.append(150)
        cost.append(900)

        bigBoard = list()        
        i = 0
        for i in prizes:
            bigBoard.append(PrizeBox(prizes[i], cost[i]))
                
    def addWhammies(bigBoard,value):
        j = 0
        while j < value:
            bigBoard.append(Whammy())

#PhotoImage(file="{}.png")
