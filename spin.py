from tkinter import *
from random import *

class Box(PhotoImage):
    def __init__(self, img:str, value:int):
            self.value = value
            PhotoImage.__init__(file=img, bg='dim gray', borderwidth=10)

# a prize box is
# - an int value
# - an image

# a prize box has
# - a fn that adds its value to the players bank
class PrizeBox(Box):
        def __init__(self, img, value, prize):
            Box.__init__(img,value)
            raise NotImplementedError

# a whammy is
# - a box with specific conditions
# - an image of a whammy

# a whammy has
# - a value that distiguishes it from any other box
# - maybe a function that clears a players bank and adds a whammy to their whammy count
class Whammy(Box):
    def __init__(self):
        img = "Whammy{}.png".format(randint(1,10))
        Box.__init__(img, 0)


class SpinGame:
    def __init__(self):
        pass

########
# MAIN #
########

#PhotoImage(file="{}.png")
