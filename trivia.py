


class Question:
    def __init__(self, prompt:str, correct:str, *incorrect:str):
        pass

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
