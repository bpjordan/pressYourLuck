from random import randint


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
        x = randint(0,len(questions)-1)
        currentQuestion = questions[x]
        questions.remove(questions[x])
        return currentQuestion.prompt , currentQuestion.answer
        #return "This is a question", {"Yes":False, "No":False, "Waa":True}

#instantiates questions
questions = []
q1 = Question("What meat are you really eating if you eat Hossenfeffer? \n\n A: Rabbit \n B: Veal \n C: Chicken",0)
questions.append(q1)
q2 = Question("What is a clavichord? \n\n A: Bone \n B: Musical Instrument \n C: Type of Ship",1)
questions.append(q2)
q3 = Question("What is the largest freshwater lake in the world? \n\n A: Caspian Sea \n B: Lake Huron \n C: Lake Victoria",0)
questions.append(q3)
q4 = Question("Where can you find the oldest ancinet wonder of the world? \n\n A: Greece \n B: Turkey \n C: Egypt",2)
questions.append(q4)
q5 = Question("What is the most densely populated U.S. state? \n\n A: Connecticut \n B: New Jersey \n C: Rhode Island",1)
questions.append(q5)
q6 = Question("How many red stripes are there on the U.S. flag? \\n A: 6 \n B: 5 \n C: 7",2)
questions.append(q6)
q7 = Question("What is the color of Donald Duck’s bowtie? \n\n A: White \n B: Red \n C: Blue",1)
questions.append(q7)
q8 = Question("How many bones are there in the human body? \n\n A: 206 \n B: 205 \n C: 208",0)
questions.append(q8)
q9 = Question("What language is the most spoken worldwide? \n\n A: English \n B: Spanish \n C: Chinese",2)
questions.append(q9)
q10 = Question("In the U.S. version of The Office, Michael Scott burns his foot on: \n\n A: Hot Coals \n B: George Foreman Grill \n C: Pavement",1)
questions.append(q10)
q11 = Question("What breed of dog is the most popular in the U.S.? \n\n A: Pug \n B: German Shepherd  \n C: Golden Retriever",2)
questions.append(q11)
q12 = Question("The UK is made up of the following countries: England, Ireland, Scotland, and… \n\n A: Wales \n B: Northen Ireland \n C: Falkland Islands",0)
questions.append(q12)


