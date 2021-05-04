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
q11 = Question("What dog breed is the most popular in the U.S.? \n\n A: Pug \n B: German Shepherd  \n C: Golden Retriever",2)
questions.append(q11)
q12 = Question("The UK is made up of the following countries: England, Ireland, Scotland, and… \n\n A: Wales \n B: Northen Ireland \n C: Falkland Islands",0)
questions.append(q12)
q13 = Question("During what war did Francis Scott Key write 'The Star-Spangled Banner'? \n\n A: American Revolution \n B: War of 1812 \n C: Civil War",1)
questions.append(q13)
q14 = Question("How long is Hanukkah? \n\n A: 2 weeks \n B: 5 days \n C: 8 days",2)
questions.append(q14)
q15 = Question("If you are truly afraid of the dark, what do you suffer from? \n\n A: Nyctophobia \n B: Hypnophobia \n C: Hadephobia",0)
questions.append(q15)
q16 = Question("In the television network abbreviation 'ABC' what does the 'A' stand for? \n\n A: Audio \n B: American \n C: Artistic",1)
questions.append(q16)
q17 = Question ("Where did Magic Johnson play professional basketball during the 1999 season? \n \n A: United States \n B: Denmark \n C: Sweden",2)
questions.append(q17)
q18 = Question("John D. Rockefeller made his fortune in what industry? \n\n A: Oil \n B: Railroad \n C: Steel ",0)
questions.append(q18)
q19 = Question("Paper will burn at approximately what temperature, in Fahrenheit? \n\n A: 398.5 \n B: 451.0 \n C: 212.5",1)
questions.append(q19)
q20 = Question("The Original Apple iMac computer was available in all of the following colors except? \n\n A: Tangerine \n B: Grape \n C: Kiwi",2)
questions.append(q20)
q21 = Question("What biological process replicates DNA? \n\n A: Mitosis \n B: Diffusion \n C: Peristalsis ",0)
questions.append(q21)
q22 = Question("What company once manufactured and sold the 'Datsun' line of automobiles? \n\n A: Mazda \n B: Nissan \n C: Toyota",1)
questions.append(q22)
q23 = Question("What city did the Beatles originally call home? \n\n A: London \n B: Manchester \n C: Liverpool",2)
questions.append(q23)
q24 = Question("What company makes Oreo cookies? \n\n A: Nabisco \n B: General Mills \n C: Keebler",0)
questions.append(q24)
q25 = Question("What Greek poet wrote 'The Iliad' and 'The Odyssey'? \n\n A: Socrates \n B: Homer \n C: Plato",1)
questions.append(q25)
q26 = Question("What is the 7-Eleven company's trademarked name for its super-large sodas? \n\n A: Big Slurp \n B: Big Sip \n C: Big Gulp",2)
questions.append(q26)
q27 = Question("What is the capital of New Zealand? \n\n A: Wellington \n B: Auckland \n C: Melbourne",0)
questions.append(q27)
q28 = Question("Which of these is a fish? \n\n A: Sea Lion \n B:Sea Horse \n C: Sea Snake",1)
questions.append(q28)
q29 = Question("Which of these states is not the birthplace of a US president? \n\n A: Nebraska \n B: New Jersey \n C: Kansas",2)
questions.append(q29)
q30 = Question("Who was on the $500 bill? \n\n A: William McKinley \n B: Calvin Coolidge \n C: Aaron Burr",0)
questions.append(q30)
