from tkinter import *
from random import *

class Box(PhotoImage):
	def __init__(self, img:str, value:int):
                
		pass
# a prize box is
# - an int value
# - an image 

# a prize box has
# - a fn that adds its value to the players bank
class PrizeBox(PhotoImage):
        def __init__(self):
                pass

# a whammy is
# - a prize box with specific conditions
# - an int value of -1
# - cordinates
# - an image of a whammy

# a whammy has
# - a value that distiguishes it from any other box
# - maybe a function that clears a players bank and adds a whammy to their whammy count
class Whammy(Box):
	def __init__(self):
                super().__init__(parent)
                self.cords

        @property
        def whammy(self):
                return self._whammy
        @whammy.setter
        def whammy(self, rand):
                self._whammy = PhotoImage(file="Whammy{}.png".format(randint(1,10))
                

class SpinGame:
	def __init__(self):
		pass

########
# MAIN #
########

PhotoImage(file="{}.png")
