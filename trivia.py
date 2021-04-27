


class Question:
	def __init__(self, prompt:str, answer:int):
                self.prompt = prompt
                self.answer = answer

class TriviaGame:
	def __init__(self):
		self.state = 0 #states: 0-need to ask a question, 1-waiting for first response, 2-waiting for second response
						#3-waiting for 3rd response, 4-revealing answer
		self.stateTime = 0 #keep track of the amount of time we've been in this state

	#function to cycle through states
	def nextState(self, forceState:int = None):
		if forceState is not None:
			self.state = forceState
		elif self.state >=4:
			self.state = 0
		else:
			self.state += 1
		
		self.stateTime = 0

	def generateQuestion(self):
		return "This is a question", {"Yes":False, "No":False, "Waa":True}

#instantiates questions
q1 = Question("What meat are you really eating if you eat Hossenfeffer? \n\n A: Rabbit \n B: Veal \n C: Chicken",0)
q2 = Question("What is a clavichord? \n\n A: Bone \n B: Musical Instrument \n C: Type of Ship",1)
q3 = Question("What is the largest freshwater lake in the world? \n\n A: Caspian Sea \n B: Lake Huron \n C: Lake Victoria",0)  
q4 = Question("Where can you find the oldest ancinet wonder of the world? \n\n A: Greece \n B: Turkey \n C: Egypt",2)
q5 = Question("What is the most densely populated U.S. stae? \n\n A: Connecticut \n B: New Jersey \n C: Rhode Island"1)

